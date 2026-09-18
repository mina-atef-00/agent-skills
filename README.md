# agent-skills

A curated set of agent skills, each a single markdown file an agent loads when
a task matches it. These are written as reusable tooling: copy a folder into an
agent that understands the SKILL.md convention and it starts working.

## What a skill file is

A skill is a markdown document with a YAML frontmatter block and a body. The
frontmatter carries a `name` and a `description`. The body is the procedure.

An agent that supports skill files reads the description first, decides whether
the skill applies to the current task, and only then loads the body. When the
skill does not apply, it costs nothing: the body never enters the context
window.

That is the difference between a skill and a prompt pasted into chat. A pasted
prompt is always present, always taking up context, whether or not it is
relevant. A skill file is loaded on demand. The same document also survives as
a file you can version, review, diff, and share, where a pasted prompt lives
and dies inside one conversation.

## What is in this repo

This is a personal selection of 12 skill folders, not a general-purpose
library. Every skill here came out of real work on the author's own Fedora
Atomic workstation: single-GPU VFIO passthrough, immutable-OS browser fixes,
Zed and agent integration, OCR for scanned Arabic PDFs, flatpak quirks,
subtitles, PDFs. Each one documents a problem that was actually hit, including
the failure modes and error strings earned along the way.

| Skill | What it does |
|---|---|
| `custom-llm-provider-setup` | Wire any OpenAI-compatible LLM API into the agent as a custom provider |
| `device-connectivity` | Pair phones and transfer files on an immutable desktop (KDE Connect, Valent) |
| `flatpak-browser-open-html` | Open local HTML files in a flatpak browser and fix the default-handler trap |
| `hermes-browser-fedora-atomic` | Diagnose and fix browser backends failing on Fedora Atomic / bootc |
| `hermes-desktop-customization` | Customize the desktop app source safely (fonts, branches, update flow) |
| `hermes-web-tools` | How the web search and extract tools pick backends, and how to debug them |
| `marker-pdf` | Convert scanned PDFs, especially Arabic and RTL, to markdown, and clean up OCR output |
| `pdf-creation` | Unicode-safe PDFs with fpdf2 when reportlab is not an option |
| `single-gpu-passthrough` | Single-GPU VFIO passthrough to a Windows VM on Fedora bootc (QEMU/libvirt hooks) |
| `starship-prompt` | Starship cross-shell prompt reference with tested Fish config and TOML pitfalls |
| `subtitle-download` | Batch-download missing subtitles for a media library with Subliminal under Podman |
| `zed-hermes-acp` | Wire the agent into the Zed editor as an ACP external agent, native or Flatpak |

## Where these skills come from

A skill is included here only when there is positive evidence the owner wrote
it: a specific quirk, version pitfall, or error message that only turns up
from having done the work on this machine, or a demonstrable authoring record.
Skills shipped with an agent, attributed to a third party, or arriving as a
generic pack are left out, and authorship is never asserted where the evidence
does not support it.

Each skill lives at `skills/<name>/SKILL.md`. Supporting files, where a skill
has them, sit next to it in the same folder.

## Installing and using these

Copy the `skills/` directory into your agent's skill directory. The target
path depends on the agent:

* Hermes Agent: drop each folder under `~/.hermes/skills/<name>/` (a category
  subfolder also works), then load it with the skill view tool by name.
* Any agent that follows the same convention (a `SKILL.md` with `name` and
  `description` frontmatter): drop the folder into that agent's skills or
  commands directory.

The file format is the common part. YAML frontmatter with a name and a
description, markdown body after it. If your agent can read that, it can use
these skills.

A skill only fires when its description matches the task. To write your own,
copy an existing folder, change the name, description, and body, then run the
validator.

## Validation

`tools/validate_skills.py` checks every folder under `skills/` for:

* a `SKILL.md` file
* YAML frontmatter with a non-empty `name` and `description`
* no absolute private paths (user home directories, private mounts)
* no banned terms (cheating, security, circumvention, piracy, account
  generation)

Run it with:

```bash
python3 tools/validate_skills.py
```

It prints `OK` and exits 0 when everything passes, or lists every problem and
exits non-zero. The test suite covers the same checks:

```bash
python3 -m unittest discover -s tests -v
```

## License

MIT. See `LICENSE`.
