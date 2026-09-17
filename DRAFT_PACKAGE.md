# DRAFT_PACKAGE: agent-skills

A curated, documented library of hand-authored agent skills. This document is
the owner's review draft. Nothing here has been published, pushed, or exposed to
any remote. Work happened only under
`/home/mina/Programming/portfolio/agent-skills`.

---

## 1. File tree

```
.github/workflows/ci.yml
.gitignore
LICENSE
README.md
skills/brainstormer/SKILL.md
skills/design-thinker/SKILL.md
skills/lateral-thinker/SKILL.md
skills/mythmaker/SKILL.md
skills/pdf-creation/SKILL.md
skills/pdf-creation/references/fpdf2-table-patterns.md
skills/polymath/SKILL.md
skills/presenter/SKILL.md
skills/provocateur/SKILL.md
skills/roundtable/SKILL.md
skills/storyteller/SKILL.md
skills/strategist/SKILL.md
skills/subtitle-download/SKILL.md
skills/subtitle-download/scripts/run_subliminal.sh
skills/subtitle-download/references/research-summary.md
skills/visionary/SKILL.md
tests/test_validate_skills.py
tools/validate_skills.py
```

13 skill folders, 22 files total (excluding any `.git/` and byte-compiled
`__pycache__`, which are gitignored).

---

## 2. README

The shipped `README.md` (verbatim):

---

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

---

## 3. Selection table

Included: 13 skills. Each is listed with why it was included and the
authorship evidence.

| Skill | Why included | Authorship evidence |
|---|---|---|
| brainstormer | Generic ideation technique, no agent-specific coupling | No `author:` field, no homepage, no license, no port/attribution notice |
| design-thinker | The standard five-stage design process, reusable by any engineer | Same as above |
| lateral-thinker | Concrete thinking tools (Six Hats, random entry) | Same as above |
| mythmaker | Narrative/archetype framework useful for writing and framing | Same as above |
| pdf-creation | Concrete, correct fpdf2 usage (Unicode pitfalls, table API) | Same as above; has `version: 1.0.0`, no author field |
| polymath | Cross-domain synthesis method, generic | Same as above |
| presenter | Slide/communication design rules | Same as above |
| provocateur | Creative-block-breaking techniques | Same as above |
| roundtable | Multi-persona facilitation is the one orchestration skill that ships clean | Same as above |
| storyteller | Narrative structures and emotional arcs | Same as above |
| strategist | Business-strategy frameworks (JTBD, blue ocean, disruption) | Same as above |
| subtitle-download | The one clean ops skill: a real, tested batch-subtitle procedure | Same as above |
| visionary | Product-vision and taste principles | Same as above |

The authorship test was applied uniformly: a skill is treated as hand-authored
only if its frontmatter carries no `author` field, no `homepage`, no
third-party `license`, and no "ported from" / "adapted from" / "based on
<external repo>" / "original author" notice in body or frontmatter. Every
included skill passes that test. The excluded skills (below) fail it.

---

## 4. Exclusion list

Everything else in the ~180-skill library was excluded. Buckets and reasons:

**Third-party authored or ported (the critical authorship filter).** Skills
whose frontmatter names an external author, an upstream homepage, or a port
notice were excluded, regardless of how useful they are. Examples:

- `github-workflow`, `github-issue-to-pr`, `email-inbox-triage`,
  `product-price-monitor`, `meeting-action-items`,
  `document-to-action-items`, `weekly-review-planning`,
  `competitor-news-monitor`, `sdlc-review`: `author: Ben Barclay
  (benbarclay)`.
- `obsidian`, `youtube-content`, `rss-feeds`, `reddit-reading`,
  `songwriting-and-ai-music`, `grounded-citations`, `polymarket`,
  `session-librarian`, `red-teaming/godmode`, `dynamic-workflow`,
  `hermes-agent`: `author: Teknium` or `Hermes Agent + Teknium` (third
  party).
- `docx`, `xlsx`, `pdf`: `author: Nous Research`.
- the whole `mlops/*` tree (axolotl, trl, unsloth, dspy, vllm, llama-cpp,
  outlines, segment-anything, audiocraft, weights-and-biases, evaluating-llms)
 : `author: Orchestra Research` or `Hugging Face`.
- `box` (Chris Kim), `maps` (Mibayy), `nano-pdf` (community + homepage),
  `himalaya` (community + homepage), `markdown-viewer` / `apikey-image-gen` /
  `grok-image-to-video` / `hyperframes` / `remotion` (Ekko + source),
  `ascii-art` (0xbyt4), `pixel-art` (dodo-reach), `comfyui` (three authors),
  `baoyu-*` (JimLiu + homepage), `touchdesigner-mcp` (kshitijk4poor),
  `dexter` ("Ported from virattt/dexter"), `blogwatcher` ("fork of
  Hyaxia/blogwatcher").
- `ai-coding-agents` ("consolidated from claude-code, codex, opencode"),
  `computer-use` ("Francesco Bonacci... Hermes Agent" + ported),
  `humanizer` ("Siqi Chen... ported by Hermes Agent" + homepage),
  `subagent-driven-development`, `systematic-debugging`, `writing-plans`
  ("adapted from obra/superpowers"), `sketch` ("adapted from
  gsd-build/get-shit-done"), `simplify-code` ("inspired by Claude Code
  /simplify"), `html-artifact` ("Anthropic... adapted"), `creative-ideation`
  ("SHL0MS"), `custom-llm-provider-setup` ("agent-created" + ported).

**Banned domains (zero exceptions).** game security, anti-cheat, kernel and
driver exploits, reverse engineering, piracy, proxy/VPN/GFW, account
generation, personal wiki/psychology. Excluded: `anti-cheat-systems`,
`awesome-game-security-overview`, `game-hacking-techniques`,
`game-security-research-rigor`, `graphics-api-hooking`,
`reverse-engineering-tools`, `dma-attack-techniques`,
`windows-kernel-security`, `code-kb`, `code-kb-treesitter`,
`cheatkb-full-review`, `cheatkb-refresh-refs`, `red-teaming/godmode` and
`security/godmode` (LLM jailbreaking; also Teknium-attributed),
`workflow/openwrt`, `workflow/v2raya`, `devops/openwrt-v2raya-ap`
(proxy/VPN/GFW tooling), `devops/discord-server-scraping` (selfbot scraping),
`gaming/proton-gaming` (contains a "Repack / Scene Game Updates" section on
patching pirated game repacks), `gaming/pokemon-player` (emulator RAM reads).

**Personal content.** Skills that describe the owner's own hardware, devices,
study system, or psychology were excluded: `devops/single-gpu-passthrough`
(names "Mina's" exact CPU/GPU/host setup), `devops/device-connectivity` (his
phone pairing), `troubleshooter` (embeds his oraimo-headphone and BlueZ-regression
debugging in the body, alongside generic frameworks), `book-man` (a "dyslexic
graduate student" study companion), `revision-planner` (his bilingual
Arabic/English exam context), `note-taking/mina-wiki-system`,
`note-taking/study-wiki`, `note-taking/english-only-study-subjects` (his
personal wiki/study system), `productivity/language-learning-system` and
`productivity/srs-language-coach` (coupled to his study wiki and Anki MCP
setup).

**Agent-specific or machine-specific, not reusable.** `planner` (half of the
body is `hermes kanban` / `hermes profile` CLI and its
`references/agent-roster.md` leaks `~/.hermes` internals and BMAD origins),
`workflow/cli-workflow` (verbatim owner preference plus `hermes` CLI and
`skills_list` tool references), `webhook-subscriptions`, `hermes-themes`,
`hermes-session-introspection`, `devops/podman-compose` (Hermes WebUI deploy
with the owner's username and `~/.hermes` paths), `mcp/native-mcp`,
`devops/hermes-kanban-profile-routing`, `hermes-desktop-*`, and the
`wayland/*` compositor study notes.

**Agent-authored, not hand-authored.** Skills whose frontmatter says
`author: Hermes Agent` were treated as agent-generated rather than written by
hand, and were excluded under the strict authorship filter. The most useful of
these, called out so the owner can reverse the call if he considers them his
own: `creative/excalidraw`, `software-development/python-debugpy`,
`software-development/node-inspect-debugger`, `mcp/native-mcp`,
`software-development/plan`. They are original (not third-party) and mostly
generic, but they carry agent credit, so "hand-authored" fails.

**Vendored dependency.** `pretty-mermaid` bundles `node_modules/` with the
third-party `beautiful-mermaid` package and its LICENSE; it also ships
JavaScript, which is outside the allowlist (Python, Bash, Markdown, Git,
GitHub Actions).

**Allowlist.** No Lua, no JavaScript, no other languages were introduced
anywhere in the package.

---

## 5. Verbatim evidence

**Validator on the real skill set (passes, exit 0):**

```
$ python3 tools/validate_skills.py
OK: all skills passed validation
EXIT=0
```

**Validator on a deliberately broken fixture (fails, exit non-zero):**

```
$ python3 tools/validate_skills.py /tmp/broken-fixture
4 problem(s) found:
  - skills/leaky-skill/SKILL.md:6: private absolute path '/home/me/secrets.txt'
  - no-frontmatter: invalid frontmatter (no frontmatter block (file must start with '---'))
  - no-frontmatter: frontmatter key 'name' is missing or empty
  - no-frontmatter: frontmatter key 'description' is missing or empty
EXIT=1
```

**Tests (11 pass):**

```
$ python3 -m unittest discover -s tests -v
test_banned_term_fails ... ok
test_banned_term_in_supporting_file_fails ... ok
test_empty_description_fails ... ok
test_home_expansion_fails ... ok
test_missing_description_fails ... ok
test_missing_skill_md_fails ... ok
test_missing_skills_dir_fails ... ok
test_private_path_fails ... ok
test_supporting_file_is_scanned_but_allowed ... ok
test_unterminated_frontmatter_fails ... ok
test_valid_skill_passes ... ok

Ran 11 tests in 0.015s

OK
```

**Banned-terms grep over skill content (zero matches):**

```
$ grep -rinE "cheat|anti-cheat|game hack|reverse engineer|kernel exploit|driver exploit|rootkit|dma attack|piracy|pirated|torrent|warez|repack|scene release|v2ray|shadowsocks|great firewall|gfw|account gen" skills/
grep exit code: 1 (1 = zero matches in skill content)
```

**Leak scan over skill content (zero matches for names, home paths, dotfiles,
vpn/proxy):**

```
$ grep -rinE "\bmina\b|/home/|/var/mnt|~/\.(hermes|ssh|config|gnupg|aws|kube)|vpn|\bproxy\b" skills/
exit: 1 (1 = clean)
```

**Stdlib fallback (PyYAML blocked) also validates the real set:**

```
errors: []
RESULT: PASS
```

**Edits applied to the shipped artifacts (the only changes from source):**

- `skills/subtitle-download/SKILL.md`: fixed a dangling reference
  `references/workflow-podman.md` to the file that actually exists
  (`references/research-summary.md`).
- `skills/subtitle-download/scripts/run_subliminal.sh`: replaced the private
  NAS mount `/var/mnt/niabc/Videos/Movies` with `/path/to/Movies` and the home
  path `/home/mina/subliminal-run.log` with `/tmp/subliminal-run.log`.
- `skills/subtitle-download/references/research-summary.md`: replaced the
  private path `/home/mina/subtitle-downloader-research.md` with a note that
  the full report is not included.

No other content was rewritten. Skill bodies were copied byte-for-byte except
for the three edits above.

---

## 6. What a skeptical reviewer would attack

Being hard on this package, in order of how much it hurts:

**It is mostly personas, not tooling.** 11 of 13 skills are methodology
"persona" cards (ideation, storytelling, strategy, design, vision). An
engineer hoping for hard technical skills (CI, databases, testing, ops) will
find one PDF recipe and one subtitle script. The genuinely deep technical
skills in the source library are third-party (Ben Barclay's GitHub/email
work, Orchestra Research's ML stack) or agent-authored, and the authorship
filter excludes them. That leaves a package that leans creative/strategy. The
owner should decide whether "hand-authored" was meant to cover
`author: Hermes Agent` skills, because the three debugger skills and
`excalidraw` would materially improve the technical depth if they count as his.

**Is it reusable by someone else, or only by an agent with the same skills?**
The 11 persona skills are self-referential: `roundtable` names the other
personas as a roster, and one of them, `troubleshooter`, is not in this
package (it was cut for embedded personal Bluetooth content). A reviewer who
loads `roundtable` will see a roster entry pointing at a skill that is not
there. The personas work best as a set and make less sense one at a time. That
is disclosed, not hidden, but it is a real weakness for "reusable by another
engineer."

**The framing leaks.** `subtitle-download` still says "this user keeps
movies" and "on THIS user's system", which reads as a personal scratch note
rather than a published library. The instruction said to preserve artifacts
and only remove private absolute paths, so I left the wording; a reviewer
would call this under-edited.

**Authorship is asserted by absence, not by positive evidence.** "No
`author:` field and no port notice" is the basis for calling a skill
hand-authored. That is a reasonable negative filter, but it cannot prove the
owner wrote a given file, and two included skills (`pdf-creation`,
`subtitle-download`) have `version:` fields that suggest they may have passed
through tooling. If provenance matters more than my negative test, the owner
should confirm each of the 13 by hand.

**`troubleshooter` is a hole.** Its generic half (5 Whys, TRIZ, fishbone,
systems thinking) is exactly the kind of skill this package wants, but the
body embeds owner-specific oraimo/BlueZ debugging. Extracting the clean half
would require rewriting the artifact, which the task forbids, so the whole
skill was cut rather than shipped dirty. A reviewer may prefer a lightly
edited `troubleshooter` to no `troubleshooter`.

**The validator's ban list is my own definition.** "Forbidden terms" is a
hand-written list, not an exhaustive scanner. It would not catch, say, a
novel circumvention tool name. It catches the named categories and the known
terms, nothing more. The leak scan is likewise pattern-based (home paths,
mounts, dotfiles), so a private path spelled another way would pass.

**No live CI proof.** The workflow file is written but has never run on
GitHub Actions, because the binding rule forbids pushing or creating a remote.
The validator and tests pass locally (evidence above); the YAML workflow is
syntactically valid but unexercised.

None of these are fatal, but the honest summary is: this is a clean, coherent,
correctly-validated package of hand-authored creative and methodology skills,
thin on technical depth, with a few cosmetic rough edges left deliberately in
place to honor "do not rewrite the artifacts."
