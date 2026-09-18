# DRAFT_PACKAGE: agent-skills

A personal set of 12 agent skills, each one written from a real problem solved
on the author's own machine. This document is the owner's review draft. Nothing
here has been published, pushed, or exposed to any remote. Work happens only
under `~/Programming/portfolio/agent-skills`.

Status: the earlier 13-skill draft was retired. An authorship audit found that
11 of those 13 were an imported generic persona pack with no positive evidence
the owner wrote them, so they were removed. The current set is 12 defensible
skills plus a fixed validator.

TODO (none outstanding at last update).

---

## 1. File tree

```
LICENSE
README.md
skills/custom-llm-provider-setup/
skills/device-connectivity/
skills/flatpak-browser-open-html/
skills/hermes-browser-fedora-atomic/
skills/hermes-desktop-customization/
skills/hermes-web-tools/
skills/marker-pdf/
skills/pdf-creation/
skills/single-gpu-passthrough/
skills/starship-prompt/
skills/subtitle-download/
skills/zed-hermes-acp/
tests/test_validate_skills.py
tools/validate_skills.py
```

12 skill folders. Most carry supporting `references/` or `scripts/` files;
see the folders themselves for the full contents.

---

## 2. README

The shipped `README.md` describes the format, lists the same 12 skills as
`ls skills/`, and states the provenance rule plainly: a skill is included only
when there is positive evidence the owner wrote it, and this repo is a personal
selection of 12 rather than a comprehensive library.

---

## 3. Selection table

Included: 12 skills. Each is listed with why it was included and the
authorship evidence.

| Skill | Why included | Authorship evidence |
|---|---|---|
| pdf-creation | fpdf2 Unicode/table pitfalls only reachable from real use | uv/venv and API-rename gotchas, exact error strings |
| subtitle-download | A tested Podman + Subliminal batch procedure | Curator session record plus a real provider-failure run (OpenSubtitles only real hit, ~40% gap) |
| single-gpu-passthrough | A working VFIO guide with verified run data | Exact kernel, driver, IOMMU group, PCI ids, hook internals |
| hermes-browser-fedora-atomic | Two-failure-mode browser diagnosis on bootc | Curator session record plus dnf-vs-rpm-ostree pitfall |
| zed-hermes-acp | Wiring an agent into Zed via ACP, native and Flatpak | Curator session record, JSONC write-refusal and sandbox-path findings |
| hermes-web-tools | Backend selection and diagnosis for web tools | Curator session record, specific commit reference |
| marker-pdf | Scanned Arabic/RTL PDF to markdown with OCR cleanup | Arabic OCR failure taxonomy only visible after running it |
| flatpak-browser-open-html | Flatpak file-forwarding worked examples and MIME trap | Dated discovery session plus the `$BROWSER` refusal error string |
| starship-prompt | Tested Fish/Starship config and TOML pitfalls | Exact installed versions and warning strings from real config debugging |
| custom-llm-provider-setup | Custom OpenAI-compatible provider setup | Curator session record plus a source-level finding with the file cited |
| device-connectivity | Phone pairing on immutable systems (Valent vs KDE Connect) | Flathub gap discovered by test, exact alpha version pinned |
| hermes-desktop-customization | Safe desktop source customization workflow | Curator session record, a hard-won titlebar sizing map, exact commit |

The selection rule is positive evidence, not absence of attribution: a skill is
in only when its content could not be written by someone who had not done the
work, or it carries a demonstrable authoring record from the owner's own
sessions. The 11 persona cards in the old draft failed that test (uniform pack
arrival, byte-identical copies across profiles, textbook-generic,
self-referential roster) and were removed.

---

## 4. Exclusion summary

The library is not being published wholesale; this is a personal set of 12,
not a generic library. Buckets excluded:

- Imported persona pack (11 skills): brainstormer, design-thinker,
  lateral-thinker, mythmaker, polymath, presenter, provocateur, roundtable,
  storyteller, strategist, visionary — no positive authorship evidence.
- Third-party attributed work: Ben Barclay, Teknium, Nous Research,
  Orchestra Research / Hugging Face, obra/superpowers, ported skills
  (dexter, blogwatcher, sketch, humanizer, and the rest).
- Banned domains: game security, anti-cheat, kernel exploits, reverse
  engineering, DMA attacks, piracy and scene content, proxy/VPN/circumvention
  tooling, account generation.
- Sensitive personal content: the owner's psychology/study wiki, password /
  profile structure, public-presence and business-intel skills.
- Skills shipped with the runtime (bundled manifest, official hub registry,
  and plugin bundles), none of which overlap this set after redaction.

---

## 5. Verbatim evidence

**Tests: 14 pass (includes the four new validator-constraint tests):**

```
$ python3 -m unittest discover -s tests
..............
Ran 14 tests in 0.019s
OK
```

**Validator on the corrected set:**

```
$ python3 tools/validate_skills.py
OK: all skills passed validation
$ echo $?
0
```

**Validator on a deliberately broken fixture:**

```
$ python3 tools/validate_skills.py /tmp/broken-fixture
2 problem(s) found:
  - skills/leaky-skill/SKILL.md:6: private absolute path '/home/me/secrets.txt'
  - banned-skill: banned term matched
$ echo $?
1
```

**Leak scan over `skills/` (personal name, home path, private mount) — zero
hits:**

```
$ grep -rni 'mina\b\|/home/mina\|/var/mnt/' skills/
(no output)
$ echo $?
1   # grep exit 1 = zero matches
```

**README index matches `ls skills/` exactly:** verified by a set-difference
check between the two lists during review; the table has exactly the 12
folders that exist on disk.

---

## 6. What a skeptical reviewer would attack

Being hard on this package, in the order it hurts most:

**Twelve skills is small.** A reviewer expecting a library will find a dozen
folders. That is the honest outcome of the authorship audit; the alternative is
padding with an imported persona pack, which is the one error this draft exists
to prevent.

**Authorship is asserted on the owner's own word plus machine evidence.** For
the curator-session skills the record is an internal ledger, not a public
history. A reviewer cannot independently verify those session ids, only that
the content plausibly could not be generic.

**Environment-specific details remain.** The skills deliberately keep exact
versions, hardware identifiers, and error strings because that specificity is
their value; identifying strings (home paths, mount labels, names) have been
redacted to `~/`, `/mnt/data`, `/mnt/media`, and neutral wording.

**The validator is a hand-written list.** It catches named categories and
known terms, plus scoped private-path patterns (/home/, /Users/, /root/,
/var/home/, /var/mnt/, Windows profiles). A leak spelled another way would get
past it; the leak grep over `skills/` is the belt-and-braces check.

**No live CI proof.** The workflow file exists but has never run on GitHub
Actions, because the rule here forbids pushing. The validator and tests pass
locally with real output above; the YAML is syntactically valid but
unexercised.
