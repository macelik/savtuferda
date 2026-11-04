---
name: lesson-promo-video
description: Make Instagram Reel / Story / Shorts promo videos (1080x1920 MP4, a long cut and a ~30 s cut) plus a timed Turkish voice-over sheet for @savtuferda's Arabic workshops, from a lesson (built with arabic-lesson-page, .html or .json) and the teacher's script. Use when asked for a promo video, reel, story or short about a lesson or a word.
---

# Lesson promo video

The teacher gives you **a lesson** (the page built by the `arabic-lesson-page` skill, or its JSON) and **her script** (what she will say). You produce:
- `videos/<slug>/<slug>-uzun.mp4`: the long cut (Reel), usually 60–80 s;
- `videos/<slug>/<slug>-kisa.mp4`: the ~30 s cut (Story / Shorts);
- `videos/<slug>/<slug>-kapak.jpg`: a cover frame;
- `videos/<slug>/seslendirme.md`: her voice-over sheet in Turkish, with timestamps and `[[…]]` stage notes.

The videos are **silent on purpose**: she records her own voice and adds music in Instagram or CapCut. Every scene carries on-screen text, so the videos also work muted.

**Your job is the storyboard.** The look (deep green, gold, stone cards, Amiri + Alegreya), the scene designs and their animation already exist in `assets/scene-kit.html` and `scripts/compose.py`. You write one `storyboard.json` that says which scenes appear, with what text, and what she says in each. Don't write video HTML by hand, and don't edit the kit.

The complete worked example is `examples/sahih/storyboard.json`. Its lesson is `examples/sahih/lesson.json`, card 8, «شَحِيح». It reproduces the published Reel, so read it before you start. The scene types and their fields are in `references/scene-types.md`.

**Paths.** `$SKILL_DIR` means the folder containing this `SKILL.md` (e.g. `.claude/skills/lesson-promo-video`, `.agents/skills/lesson-promo-video`, `~/.config/opencode/skills/lesson-promo-video`). Work files go in the **user's working directory** under `videos/<slug>/`.

**Requirements:**
- Python 3.9+ and Node 18+.
- Playwright with Chromium. If a script says it's missing, run `npm i -D playwright` and then `npx playwright install chromium` in the working directory.
- `ffmpeg` with libx264.
- Internet for Google Fonts while rendering.

## Workflow

1. **Read the inputs.** The request may follow `templates/video-request.md`. You need:
   - the lesson file;
   - which word (card) the video is about;
   - the motto, if any;
   - the handle;
   - her script;
   - whether a short cut is wanted (default: yes).
2. **Map her script to scenes.** Split the script into ideas and give each one the scene type that shows it (table below). Keep **her words**; you may shorten a sentence, but don't rewrite her message. Put each idea's text in that scene's `say`.
3. **Write `videos/<slug>/storyboard.json`.** Use `"lesson"` to point at the lesson file (the path is relative to the storyboard). Use `"from_card": N` on step scenes so the root letters, forms, prepositions, synonyms, press example and ayah come from the lesson itself. Only write by hand what the card doesn't have (`context.rows`, captions, the quiz options). Add `short` lengths for the short cut (≈ 30 s total) and a `say_short` for its opening and closing scenes.
4. **Compose:**
   ```bash
   python3 $SKILL_DIR/scripts/compose.py videos/<slug>/storyboard.json videos/<slug>
   ```
   It refuses to run on unknown scene types, missing fields, a quiz `answer` that isn't one of its `options`, scripts or external URLs. It prints both lengths and warns where narration is tight. If the long cut goes past ~90 s, shorten `say` texts.
5. **Look before rendering** (rendering takes minutes):
   ```bash
   node $SKILL_DIR/scripts/stills.js videos/<slug> full
   ```
   ```bash
   node $SKILL_DIR/scripts/stills.js videos/<slug> short
   ```
   Open **every** still in `videos/<slug>/stills-full/` and `stills-short/` with your file-reading tool. Check:
   - Arabic diacritics don't collide with the line below.
   - No text runs off the card or the screen.
   - Mixed Arabic and Turkish text is in the right order.
   - The root letters are gold inside the forms.
   - The quiz's tap lands on the right answer.
   - Nothing important sits in the bottom ~400 px.

   Fix the storyboard, compose again, and look again.
6. **Render:**
   ```bash
   node $SKILL_DIR/scripts/render.js videos/<slug>/full.html videos/<slug>/<slug>-uzun.mp4
   ```
   ```bash
   node $SKILL_DIR/scripts/render.js videos/<slug>/short.html videos/<slug>/<slug>-kisa.mp4
   ```
   ```bash
   ffmpeg -y -ss 3.5 -i videos/<slug>/<slug>-uzun.mp4 -frames:v 1 -q:v 2 videos/<slug>/<slug>-kapak.jpg
   ```
   Each render takes ~4 s of wall time per second of video, so the two can run in parallel. Then pull 3–4 frames from each MP4 (`ffmpeg -ss <t> -i <mp4> -frames:v 1 x.jpg`) and look at them.
7. **Report** (format at the end).

## Mapping her script to scenes

| She says something like… | Scene |
|---|---|
| the opening question / what the video is about | `hook` |
| a motto or slogan (often Arabic) | `motto` |
| "we heard a poem / watched a cartoon, and this line…" | `verse` (the lesson card's `verse` via `from_card`) |
| "what does X mean?" | `zoom` |
| root, mazi / muzari / masdar | `root` |
| prepositions (harf-i cer) | `harf` |
| synonyms / antonyms | `syn` |
| meaning in context, figurative use (mecaz) | `context` |
| press / news Arabic | `press` |
| Qur'an / hadith | `ayah` |
| literary analysis, imagery, what the poet means | `literary` |
| a rhetorical turn ("Is that all? Of course not!") | `punch` |
| practice, exercises, interactive questions | `quiz` (build it from the verse: `before` + `answer` + `after`, 3 other target words as distractors) |
| a summary or promise ("not passive listeners…") | `statement` |
| the invitation / contact | `cta` (always last) |

If her script has no idea for a scene type, leave that scene out. Never invent claims about her classes that aren't in her script.

## Accuracy

- Arabic on screen is **fully vowelled** and copied from the lesson or her script. Never retype it from memory.
- Any ayah must come from the lesson card (`from_card`), which has already been checked; never add a new citation in the video.
- Turkish on screen and in the voice-over sheet must read naturally. `[[…]]` stage notes are in Turkish too.

## Final report (reply to the user)

```
Videos: videos/<slug>/<slug>-uzun.mp4 (<mm:ss>), <slug>-kisa.mp4 (<mm:ss>), cover <slug>-kapak.jpg
Voice-over sheet: videos/<slug>/seslendirme.md
Scenes (long): <type list>  ·  short: <type list>
Script changes: <lines you shortened or moved, or "none">
Checks: stills reviewed (<n>), MP4 frames reviewed (<n>), notes from compose: <…>
```
