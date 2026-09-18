#!/usr/bin/env python3
"""Validate a skills/ directory of SKILL.md files.

For every subfolder of ``<root>/skills`` this script checks that:

* a ``SKILL.md`` file exists,
* its YAML frontmatter parses and contains a non-empty ``name`` and
  ``description``,
* no file under the folder contains an absolute private path (a specific
  user's home directory or a private mount), and
* no file contains a banned term.

It exits with status 0 when everything passes and 1 when anything fails, so it
works directly as a CI gate.

Usage:
    python3 tools/validate_skills.py [root]

``root`` defaults to the repository directory that contains this script
(two levels up).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

REQUIRED_KEYS = ("name", "description")

# Absolute paths that would leak private information: a specific user's home
# (/home/<name>/, /Users/<name>/, /root/) or a private mount (/var/mnt/), plus
# Windows user profiles. System paths such as /usr, /tmp, /etc, and /proc are
# allowed. The portable "~/" form is NOT flagged: it is the documented generic
# form of public tool paths such as ~/.hermes/config.yaml or
# ~/.config/zed/settings.json and leaks nothing.
_PRIVATE_PATH_PATTERNS = [
    re.compile(r"(^|[\s`'\"])/(?:home|Users|root)/[^\s`'\"()/]+(?:/[^\s`'\"()]*)?", re.IGNORECASE),
    re.compile(r"(^|[\s`'\"])(?:\$HOME)?(?:/var/home)/[^\s`'\"()/]+(?:/[^\s'\"()]*)?", re.IGNORECASE),
    re.compile(r"(^|[\s`'\"])/var/mnt/", re.IGNORECASE),
    re.compile(r"[A-Za-z]:\\Users\\", re.IGNORECASE),
]

# Terms banned from this library (security, cheating, circumvention, piracy,
# and account-generation content). Multi-word terms match as substrings;
# short words use word boundaries so they do not false-positive inside longer
# words such as "cheatsheet".
_BANNED_SUBSTRINGS = (
    "anti-cheat",
    "game hack",
    "game cheat",
    "cheat engine",
    "reverse engineer",
    "kernel exploit",
    "driver exploit",
    "rootkit",
    "dma attack",
    "piracy",
    "pirated",
    "warez",
    "scene release",
    "repack",
    "v2ray",
    "shadowsocks",
    "great firewall",
    "account generator",
    "account generation",
    "torrent",
)

_BANNED_WORDS = ()


def _banned_regexes() -> list[re.Pattern]:
    regexes = [re.compile(re.escape(t), re.IGNORECASE) for t in _BANNED_SUBSTRINGS]
    regexes.extend(re.compile(rf"\b{re.escape(w)}\b", re.IGNORECASE) for w in _BANNED_WORDS)
    return regexes


_BANNED = _banned_regexes()


# ---------------------------------------------------------------------------
# Frontmatter parsing
# ---------------------------------------------------------------------------

def _parse_frontmatter(text: str) -> dict:
    """Return the YAML frontmatter as a dict, or raise ValueError.

    Tries PyYAML first (real YAML semantics), then falls back to a minimal
    parser that handles the ``key: value`` shapes this repository uses.
    """
    stripped = text.lstrip("\ufeff")
    if not stripped.startswith("---"):
        raise ValueError("no frontmatter block (file must start with '---')")

    lines = stripped.splitlines()
    # Find the closing '---' on its own line.
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        raise ValueError("unterminated frontmatter block (missing closing '---')")

    block = "\n".join(lines[1:end])

    try:
        import yaml  # type: ignore

        data = yaml.safe_load(block)
        if data is None:
            return {}
        if not isinstance(data, dict):
            raise ValueError("frontmatter is not a YAML mapping")
        return data
    except ImportError:
        return _parse_frontmatter_minimal(block)


def _parse_frontmatter_minimal(block: str) -> dict:
    """Small stdlib fallback for ``key: value`` frontmatter."""
    data: dict = {}
    key = None
    block_lines = block.splitlines()
    i = 0
    while i < len(block_lines):
        line = block_lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        if line[0] not in (" ", "\t"):
            # A top-level key line.
            if ":" not in line:
                raise ValueError(f"malformed frontmatter line: {line!r}")
            k, _, v = line.partition(":")
            key = k.strip()
            v = v.strip()
            if v in ("|", "|-", "|+", ">", ">-", ">+"):
                # Block scalar: consume following indented lines.
                buf = []
                j = i + 1
                while j < len(block_lines) and (
                    not block_lines[j].strip() or block_lines[j][0] in (" ", "\t")
                ):
                    if block_lines[j].strip():
                        buf.append(block_lines[j].strip())
                    j += 1
                sep = "\n" if v.startswith("|") else " "
                data[key] = sep.join(buf)
                i = j
                continue
            data[key] = _unquote(v)
        i += 1
    return data


def _unquote(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in ("\"", "'"):
        return value[1:-1]
    return value


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_skills(root: Path) -> list[str]:
    """Validate ``<root>/skills`` and return a list of human-readable errors."""
    errors: list[str] = []
    skills_dir = root / "skills"

    if not skills_dir.is_dir():
        return [f"skills directory not found: {skills_dir}"]

    folders = sorted(p for p in skills_dir.iterdir() if p.is_dir())
    if not folders:
        errors.append("no skill folders found under skills/")

    for folder in folders:
        label = folder.name
        skill_md = folder / "SKILL.md"

        if not skill_md.is_file():
            errors.append(f"{label}: missing SKILL.md")
            continue

        text = skill_md.read_text(encoding="utf-8", errors="replace")

        # Frontmatter.
        try:
            fm = _parse_frontmatter(text)
        except Exception as exc:  # noqa: BLE001 - surface any parse problem
            errors.append(f"{label}: invalid frontmatter ({exc})")
            fm = {}

        for key in REQUIRED_KEYS:
            value = fm.get(key)
            if not isinstance(value, str) or not value.strip():
                errors.append(
                    f"{label}: frontmatter key {key!r} is missing or empty"
                )

        # Content scan across SKILL.md and every supporting file.
        for path in sorted(folder.rglob("*")):
            if not path.is_file():
                continue
            try:
                content = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            rel = str(path.relative_to(root))
            for lineno, line in enumerate(content.splitlines(), start=1):
                for pattern in _PRIVATE_PATH_PATTERNS:
                    match = pattern.search(line)
                    if match:
                        errors.append(
                            f"{rel}:{lineno}: private absolute path "
                            f"{match.group(0).strip()!r}"
                        )
                for pattern in _BANNED:
                    if pattern.search(line):
                        errors.append(f"{rel}:{lineno}: banned term matched")

    return errors


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    root = Path(argv[0]) if argv else Path(__file__).resolve().parent.parent
    errors = validate_skills(root)
    if errors:
        print(f"{len(errors)} problem(s) found:")
        for error in errors:
            print(f"  - {error}")
        return 1
    print("OK: all skills passed validation")
    return 0


if __name__ == "__main__":
    sys.exit(main())
