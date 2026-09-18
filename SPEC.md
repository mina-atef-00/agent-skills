# agent-skills specification

This document is the internal contract for the pack: what the validator
enforces, what quality bar a skill must clear, the file format, the test
layout, and the procedure for adding a skill.

## Validator rules

`tools/validate_skills.py` scans every folder under `skills/` and fails on the
first unmet condition, listing every problem it finds. It prints `OK` and
exits 0 when the whole pack is clean.

For each skill folder it checks:

* a `SKILL.md` file exists
* YAML frontmatter opens and closes (`---` delimiters) and parses
* `name` is present and non-empty
* `description` is present and non-empty
* no absolute private paths (specific user home directories, private mounts)
* no banned terms: cheating, security-circumvention, piracy, account
  generation. Generic tilde tool paths (`~/.hermes/skills/...`) are allowed,
  and legitimate technical uses of otherwise-banned words are caught by the
  same string-level check, so the bar is specific: the scanner rejects the
  banned phrase patterns, not the topic.

Supporting files inside a skill folder are scanned for the private-path and
banned-term checks too. An unreadable file is reported as an error, not
skipped.

## Authorship bar

A skill is included only when there is positive evidence the owner wrote it:
a specific quirk, version pitfall, or error message that only turns up from
having done the work on this machine, or a demonstrable authoring record.
Skills shipped with an agent, attributed to a third party, or arriving as a
generic pack are left out. Authorship is never asserted where the evidence
does not support it, and the pack never claims to be anything other than a
personal selection rather than a general-purpose library.

## Skill file format

Each skill lives at `skills/<name>/SKILL.md`. Supporting files, where a skill
has them, sit next to it in the same folder.

The file is markdown with a YAML frontmatter block and a body:

```markdown
---
name: skill-name
description: Use when <trigger>. <one-line behavior>.
---

# Skill title

The procedure.
```

The `description` is what an agent reads first and matches against the current
task, so it should name the trigger condition and say what the skill does in
one line. The body is the procedure the agent follows when the skill applies.
Frontmatter may also carry `version`, `author`, `license`, `tags`, or a
`metadata` block; only `name` and `description` are required by the validator.

## Test layout

`tests/test_validate_skills.py` covers the same checks the validator makes,
through temp directories rather than the live pack:

* a valid skill passes
* missing `SKILL.md`, missing `name`, missing or empty `description`, and
  unterminated frontmatter each fail
* private paths are caught, generic tilde tool paths are allowed
* banned terms fail, including when they appear in a supporting file; genuine
  use of a banned word in a legitimate technical context is still caught
* an unreadable file is reported, not skipped, and the scan continues
* the validator's exit codes are exercised end to end

Run the suite with:

```bash
python3 -m unittest discover -s tests -v
```

## How to add a skill

1. Do the work on your own machine first. If the skill is about something you
   have not done, it does not meet the authorship bar yet.
2. Create `skills/<new-name>/SKILL.md` with the frontmatter above. Write the
   description so another person (or an agent) can tell from one line when it
   fires and what it does.
3. Put the specifics in the body: the commands, the pitfalls, the error
   strings you actually saw. Proprietary or private absolute paths stay out;
   use tilde paths for tool locations.
4. Run `python3 tools/validate_skills.py` and fix anything it reports.
5. Run `python3 -m unittest discover -s tests -v` and leave the suite green.
6. Commit the folder. Supporting files go beside `SKILL.md` in the same
   folder so the validator's scan covers them.
