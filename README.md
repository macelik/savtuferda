# lesson-promo-video

An agent skill that turns an **Arabic lesson** and the **teacher's script** into promo videos for [@savtuferda](https://instagram.com/savtuferda)'s workshops. It produces:

- a **long cut** (Instagram Reel, usually 60–80 s) and a **~30 s cut** (Story / Shorts), both 1080×1920 MP4;
- a **cover image**;
- a **Turkish voice-over sheet** (`seslendirme.md`) with timestamps and `[[…]]` stage notes, so the teacher can record her narration in sync.

The videos are silent on purpose: she records her own voice and adds music in Instagram or CapCut. Every scene has on-screen text, so they also work muted.

Example output: [`showcase/`](showcase/) (the published Reel, the 30 s cut and the cover).

It works with the companion skill **`arabic-lesson-page`**, which builds the lesson page this skill reads. The two are separate repos and separate skills.

## How it works

1. The agent maps each idea in her script to a **scene type**: hook, motto, verse, zoom, the six "lens" steps on the word (root, preposition, synonyms, context/figurative, press, Qur'an), literary analysis, punch line, quiz, statement, call to action.
2. It writes a `storyboard.json`. The step scenes fill themselves from the lesson (`"from_card": 8`): root letters, mazi/muzari/masdar, prepositions, synonyms, the press example and the ayah all come from the already-checked lesson data.
3. `compose.py` builds both timelines and the voice-over sheet. Each scene's length follows what she says in it.
4. `stills.js` shows one still per scene for review; `render.js` captures every frame in headless Chromium and encodes with ffmpeg.

The worked example in [`skills/lesson-promo-video/examples/sahih/`](skills/lesson-promo-video/examples/sahih/) regenerates the published Reel from her original script.

## Install

### Option 1: the `skills` CLI (Claude Code, Codex, OpenCode, …)

Needs Node 22+.

```bash
npx skills add macelik/savtuferda --skill lesson-promo-video -a claude-code
```

```bash
npx skills add macelik/savtuferda --skill lesson-promo-video -a codex
```

```bash
npx skills add macelik/savtuferda --skill lesson-promo-video -a opencode
```

Add `-g` to install for all projects. `-a` can be repeated to install into several agents at once. (If this skill moves to its own repository, replace `macelik/savtuferda` with that repository's `owner/name`.)

### Option 2: Claude Code plugin

```
/plugin marketplace add macelik/savtuferda
/plugin install lesson-promo-video@lesson-promo-video
```

### Option 3: copy the folder

Copy `skills/lesson-promo-video` into the folder your agent reads:

| Harness | This project only | All projects |
|---|---|---|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Codex | `.agents/skills/` | `~/.agents/skills/` (older Codex: `~/.codex/skills/`) |
| OpenCode | `.opencode/skills/` | `~/.config/opencode/skills/` |

OpenCode also reads `.claude/skills/` and `.agents/skills/`. Restart the agent after installing.

### Requirements

- Python 3.9+ (standard library only).
- Node 18+ with Playwright and Chromium: in your project run `npm i -D playwright`, then `npx playwright install chromium`.
- `ffmpeg` with libx264.
- Internet access while rendering (Google Fonts: Amiri, Alegreya).

## Use

1. Fill in [`templates/video-request.md`](skills/lesson-promo-video/templates/video-request.md): the handle, the lesson file, which word (card) to feature, the motto, and her script.
2. Ask your agent:

   > Make the promo videos for `request.md` with the lesson-promo-video skill.

   To call the skill explicitly, type `/lesson-promo-video` in Claude Code or `$lesson-promo-video` in Codex. In OpenCode, name the skill in your request.
3. You get `videos/<slug>/<slug>-uzun.mp4`, `<slug>-kisa.mp4`, `<slug>-kapak.jpg` and `seslendirme.md`.

Rendering takes about 4 s per second of video, so roughly 5 minutes for the long cut and 2 for the short one.

## Layout

```
skills/lesson-promo-video/
  SKILL.md                     instructions the agent follows
  assets/scene-kit.html        shared look + scene system (CSS animation, seekable)
  scripts/compose.py           storyboard -> full.html, short.html, seslendirme.md, timeline.json
  scripts/stills.js            one still per scene (review before rendering)
  scripts/render.js            frame-accurate capture -> MP4
  references/scene-types.md    every scene type, its fields, timing and layout rules
  templates/video-request.md   the form the teacher fills in
  examples/sahih/              lesson + her script + the storyboard of the published Reel
showcase/                      published videos (not installed with the skill)
.claude-plugin/                Claude Code plugin + marketplace manifests
AGENTS.md                      guide for agents developing this skill
```
