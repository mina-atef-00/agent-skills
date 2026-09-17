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

| Skill | What it does |
|---|---|
| `brainstormer` | Ideation via SCAMPER, reverse brainstorming, and analogies |
| `design-thinker` | The five-stage human-centered design process |
| `lateral-thinker` | Six Thinking Hats, random entry, and deliberate creativity |
| `mythmaker` | Hero's journey stages and the twelve archetypes for narrative |
| `pdf-creation` | Unicode-safe PDFs with fpdf2 when reportlab is not an option |
| `polymath` | Cross-disciplinary synthesis and a latticework of mental models |
| `presenter` | Slide hierarchy, the three-second rule, and data visualization |
| `provocateur` | Surrealist techniques for breaking creative blocks |
| `roundtable` | Facilitate a multi-persona discussion and synthesize the output |
| `storyteller` | Three-act structure, the hero's journey, and emotional arcs |
| `strategist` | Jobs-to-be-done, blue ocean strategy, and disruption diagnosis |
| `subtitle-download` | Batch-download missing subtitles for a movie library |
| `visionary` | Product vision, intersection thinking, and taste as a filter |

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
