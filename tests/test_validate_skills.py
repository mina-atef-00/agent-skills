"""Tests for tools/validate_skills.py.

Run with either of:

    python3 -m unittest discover -s tests -v
    python3 -m pytest tests/

Each test builds a throwaway ``skills/`` tree in a temp directory and asserts
what the validator reports. There is one passing fixture and several
deliberately broken fixtures that must each fail validation.
"""

import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT / "tools"))

import validate_skills  # noqa: E402


VALID_SKILL = """---
name: example-skill
description: "A short description of what this skill does."
---

# Example Skill

Body text with a /usr/share/fonts system path that is allowed.
"""


def make_skill(root: Path, name: str, body: str, supporting: dict[str, str] | None = None) -> Path:
    folder = root / "skills" / name
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "SKILL.md").write_text(body, encoding="utf-8")
    for rel, content in (supporting or {}).items():
        target = folder / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
    return folder


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    # Passing fixture ----------------------------------------------------

    def test_valid_skill_passes(self):
        make_skill(self.root, "example-skill", VALID_SKILL)
        errors = validate_skills.validate_skills(self.root)
        self.assertEqual(errors, [])

    def test_supporting_file_is_scanned_but_allowed(self):
        make_skill(
            self.root,
            "example-skill",
            VALID_SKILL,
            {"references/notes.md": "A note with a system path /usr/bin/env only."},
        )
        self.assertEqual(validate_skills.validate_skills(self.root), [])

    # Broken fixtures ----------------------------------------------------

    def test_missing_skill_md_fails(self):
        (self.root / "skills" / "empty-folder").mkdir(parents=True)
        errors = validate_skills.validate_skills(self.root)
        self.assertTrue(any("missing SKILL.md" in e for e in errors))

    def test_missing_description_fails(self):
        make_skill(self.root, "no-desc", "---\nname: no-desc\n---\n\nbody\n")
        errors = validate_skills.validate_skills(self.root)
        self.assertTrue(any("description" in e for e in errors))

    def test_empty_description_fails(self):
        make_skill(
            self.root, "empty-desc", '---\nname: empty-desc\ndescription: ""\n---\n\nbody\n'
        )
        errors = validate_skills.validate_skills(self.root)
        self.assertTrue(any("description" in e for e in errors))

    def test_unterminated_frontmatter_fails(self):
        make_skill(self.root, "bad-fm", "---\nname: bad-fm\n\nbody with no closing fence\n")
        errors = validate_skills.validate_skills(self.root)
        self.assertTrue(any("frontmatter" in e for e in errors))

    def test_private_path_fails(self):
        make_skill(
            self.root,
            "leaky",
            '---\nname: leaky\ndescription: "ok"\n---\n\nRun from /home/alice/code\n',
        )
        errors = validate_skills.validate_skills(self.root)
        self.assertTrue(any("private absolute path" in e for e in errors))

    def test_private_home_path_is_caught(self):
        for leak in [
            "/home/someuser/thing",
            "/Users/alice/Documents/x",
            "/root/notes.txt",
            "/var/mnt/private/disk.qcow2",
        ]:
            with self.subTest(leak=leak):
                make_skill(
                    self.root,
                    "leaky",
                    f'---\nname: leaky\ndescription: "ok"\n---\n\nSee {leak}\n',
                )
                errors = validate_skills.validate_skills(self.root)
                self.assertTrue(any("private absolute path" in e for e in errors))
                shutil.rmtree(self.root / "skills" / "leaky")

    def test_generic_tilde_tool_paths_are_allowed(self):
        make_skill(
            self.root,
            "tilde-ok",
            '---\nname: tilde-ok\ndescription: "ok"\n---\n\n'
            "Edit ~/.hermes/config.yaml, then ~/.config/zed/settings.json.\n",
        )
        self.assertEqual(validate_skills.validate_skills(self.root), [])

    def test_genuine_banned_term_is_still_caught(self):
        make_skill(
            self.root,
            "banned",
            '---\nname: banned\ndescription: "ok"\n---\n\n'
            "This documents a v2ray proxy chain for the great firewall.\n"
            "With anti-cheat and rootkit notes.\n",
        )
        errors = validate_skills.validate_skills(self.root)
        self.assertTrue(any("banned term" in e for e in errors))

    def test_legitimate_technical_proxy_is_allowed(self):
        make_skill(
            self.root,
            "proxy-ok",
            '---\nname: proxy-ok\ndescription: "ok"\n---\n\n'
            "Point the client at the reverse proxy, or a server-routed "
            "model via a proxy provider. Uses OPENAI proxy environment settings.\n",
        )
        self.assertEqual(validate_skills.validate_skills(self.root), [])

    def test_banned_term_fails(self):
        make_skill(
            self.root,
            "banned",
            '---\nname: banned\ndescription: "ok"\n---\n\nThis walks through a reverse engineer of the binary.\n',
        )
        errors = validate_skills.validate_skills(self.root)
        self.assertTrue(any("banned term" in e for e in errors))

    def test_banned_term_in_supporting_file_fails(self):
        make_skill(
            self.root,
            "banned-file",
            '---\nname: banned-file\ndescription: "ok"\n---\n\nbody\n',
            {"scripts/x.sh": "echo 'torrenting is not allowed'"},
        )
        errors = validate_skills.validate_skills(self.root)
        self.assertTrue(any("banned term" in e for e in errors))

    def test_unreadable_file_is_reported_not_skipped(self):
        folder = make_skill(
            self.root,
            "locked",
            '---\nname: locked\ndescription: "ok"\n---\n\nbody\n',
            {"secret.bin": "placeholder"},
        )
        locked = folder / "secret.bin"
        os.chmod(locked, 0o000)
        try:
            errors = validate_skills.validate_skills(self.root)
        finally:
            os.chmod(locked, 0o644)
        self.assertTrue(
            any("unreadable" in e and "secret.bin" in e for e in errors),
            f"unscannable file was silently skipped: {errors}",
        )

    def test_scan_continues_after_unreadable_file(self):
        folder = make_skill(
            self.root,
            "locked",
            '---\nname: locked\ndescription: "ok"\n---\n\nbody\n',
            {"a.bin": "x", "b.md": "leak /home/alice/notes"},
        )
        os.chmod(folder / "a.bin", 0o000)
        try:
            errors = validate_skills.validate_skills(self.root)
        finally:
            os.chmod(folder / "a.bin", 0o644)
        self.assertTrue(any("a.bin" in e and "unreadable" in e for e in errors))
        self.assertTrue(any("b.md" in e and "private absolute path" in e for e in errors),
                         "scan aborted instead of continuing past unreadable file")

    def test_missing_skills_dir_fails(self):
        errors = validate_skills.validate_skills(self.root)
        self.assertTrue(any("skills directory not found" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
