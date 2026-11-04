# savtuferda skills

Agent skills for the Arabic workshops of [@savtuferda](https://instagram.com/savtuferda).

| Skill | What it does |
|---|---|
| [`arabic-lesson-page`](skills/arabic-lesson-page/SKILL.md) | You give it an Arabic text (poem, prose, cartoon dialogue, song) with the target words marked. It produces **one self-contained interactive HTML lesson** for Turkish-speaking learners (A2–B2). |

The lesson page shows three views:
- **Text:** every target word is clickable, and there is a line-by-line reading mode.
- **Words:** one slide per word. A looping animation shows the meaning, and step tabs go Şiirde → Kök (animated root letters, mazi/muzari/masdar) → Anlam → Harf-i cer → Örnekler (level filter) → Ayetler → Konuşalım.
- **Practice:** a fill-in-the-blank quiz built from the text, plus flip cards.

Turkish translations stay blurred until tapped. The page has light and dark themes and works offline except for fonts. It also works on phones and in fullscreen presentation mode.

The skill follows the open `SKILL.md` format, so it works in **Claude Code, Codex and OpenCode**, and in other agents that read the same format.

## Install

### Option 1: the `skills` CLI (any harness)

The [`skills`](https://github.com/vercel-labs/skills) CLI copies the skill into the right folder for each agent. It needs Node 22+.

```bash
npx skills add macelik/savtuferda --skill arabic-lesson-page -a claude-code
```

```bash
npx skills add macelik/savtuferda --skill arabic-lesson-page -a codex
```

```bash
npx skills add macelik/savtuferda --skill arabic-lesson-page -a opencode
```

Add `-g` to install for all your projects instead of only the current one. `-a` can be repeated to install into several agents at once.

### Option 2: Claude Code plugin

Inside Claude Code:

```
/plugin marketplace add macelik/savtuferda
/plugin install savtuferda@savtuferda
```

(Claude Code 2.1.275 or later can also do both in one step: `/plugin install savtuferda --marketplace macelik/savtuferda`.)

### Option 3: copy the folder

```bash
git clone https://github.com/macelik/savtuferda
```

Then copy `savtuferda/skills/arabic-lesson-page` into the folder your agent reads:

| Harness | This project only | All projects |
|---|---|---|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Codex | `.agents/skills/` | `~/.agents/skills/` (older Codex versions: `~/.codex/skills/`) |
| OpenCode | `.opencode/skills/` | `~/.config/opencode/skills/` |

For example, for Claude Code in the current project:

```bash
mkdir -p .claude/skills && cp -r savtuferda/skills/arabic-lesson-page .claude/skills/
```

OpenCode also reads `.claude/skills/` and `.agents/skills/`, so one copy can serve several agents. Restart the agent after installing.

### Requirements

- `python3` 3.9+ (standard library only) to scaffold and build lessons.
- For the automatic QA step: Node 18+ with Playwright and its Chromium. In your project, run `npm i -D playwright`, then `npx playwright install chromium`.
- `beautifulsoup4` only if you import a teacher's HTML draft (`pip install beautifulsoup4`).
- Internet access when the page is opened, for its Google Fonts (Amiri, Alegreya).

## Use

1. Copy [`templates/lesson-request.md`](skills/arabic-lesson-page/templates/lesson-request.md) into your project and fill it in. Put the title, author and source at the top. Write the text one line (or dialogue turn) per row, with the target words in `[[double brackets]]`. The Turkish translation is optional. A teacher's HTML draft with the target words in `<mark>` works too.
2. Ask your agent:

   > Build the lesson page for `request.md` with the arabic-lesson-page skill.

   To call the skill explicitly, type `/arabic-lesson-page` in Claude Code or `$arabic-lesson-page` in Codex. In OpenCode, name the skill in your request.
3. The agent writes `lessons/<slug>/<slug>.json` (the content) and `lessons/<slug>/<Name>-Ders.html` (the page). It then runs QA and ends with a short report. The report lists any source or attribution check, corrections it suggests, the Quran citations it used, and its assumptions.

Open the `.html` file in any browser; it needs no server. Keys: `←`/`→` words, Space next step, `T` translations, `F` fullscreen.

**Review before class.** Smaller models do well on the structure, but they can still misread a literary line. The skill makes the agent write a per-line grammatical parse (`parse` in the JSON) so a reviewer can check its reasoning quickly. See [`tests/RESULTS.md`](skills/arabic-lesson-page/tests/RESULTS.md).

## Repository layout

```
skills/arabic-lesson-page/
  SKILL.md                 instructions the agent follows
  assets/template.html     the lesson page (design, animation, interactivity)
  scripts/scaffold.py      request.md or <mark>ed HTML -> JSON skeleton with TODOs
  scripts/build.py         validate JSON + render the page (refuses while TODOs remain)
  scripts/check.js         headless QA: console errors, overflow, screenshots
  scripts/extract_legacy.py  import an old long-scroll lesson into JSON
  templates/lesson-request.md  the form the teacher fills in
  examples/                two complete lessons (Derviş «في القدس», Şabbi «إرادة الحياة»)
  references/lesson-design.md  pedagogy, data model and design rationale
  tests/                   trial request + results of model trials
.claude-plugin/            Claude Code plugin + marketplace manifests
AGENTS.md                  guide for agents developing this skill
lesson/output/, lesson/source/, video/, docs/   finished lessons and the promo-video pipeline (see below)
```

## Also in this repo (not part of the skill)

The skill install only copies `skills/arabic-lesson-page/`. These live alongside it:

| Path | What it is |
|---|---|
| `lesson/output/` | Finished lesson pages: Derviş «في القدس» and Şabbi «إرادة الحياة». |
| `lesson/source/` | The teacher's original hand-made HTML for the Kudüs lesson. |
| `video/` | The promo-video pipeline: an HTML/CSS scene system rendered frame by frame to a 1080×1920 MP4. Outputs are in `video/output/` (the 75 s Reel, the 30 s cut and the cover image). See [`docs/video-pipeline.md`](docs/video-pipeline.md) and [`docs/reel-voiceover-cues.md`](docs/reel-voiceover-cues.md). |
