# Promo Video Pipeline (Instagram Reels / Shorts / Stories)

The video is an **HTML page animated with CSS**. Each frame is captured in headless Chromium and encoded with ffmpeg. There's no video editor, and no After Effects project to keep in sync. Every frame is reproducible from `video/src/scene.html`.

## Files

| Path | What it is |
|---|---|
| `video/src/scene.html` | The composition: 15 scenes, 1080×1920, all CSS animation. **Edit this.** |
| `video/build.py` | Expands placeholders and writes two timelines: `video/build/full.html` (75 s) and `video/build/short.html` (30 s cut). |
| `video/render.js` | Seeks every animation to each frame time, screenshots it, and pipes the frames to ffmpeg, producing an MP4. |
| `video/stills.js` | Grabs single frames at given times, for a quick review without rendering the whole video. |
| `video/output/` | The delivered files: `Arapca-Atolye-Reel.mp4` (75 s), `Arapca-Atolye-30sn.mp4` (30 s), cover JPG. |
| `docs/reel-voiceover-cues.md` | Timing sheet that matches the teacher's script to the 75-second cut. |

## Build

```bash
python3 video/build.py
```

```bash
node video/stills.js video/build/full.html qa/stills 3.5 9.5 15.5 26 48 62.5 74
```

```bash
node video/render.js video/build/full.html video/output/Arapca-Atolye-Reel.mp4 75
```

```bash
node video/render.js video/build/short.html video/output/Arapca-Atolye-30sn.mp4 30
```

```bash
ffmpeg -y -ss 3.5 -i video/output/Arapca-Atolye-Reel.mp4 -frames:v 1 -q:v 2 video/output/Arapca-Atolye-Reel-kapak.jpg
```

Rendering takes about 4 s of wall-clock time per second of video on 4 cores, so the 75-second cut takes about 5 minutes. The two cuts can render in parallel. The output is H.264, yuv420p, 30 fps, CRF 18, with `+faststart`. It is **silent on purpose**: the teacher records her own voice-over, and music is added in Instagram or CapCut.

## How the timeline works

- Each scene is `<section class="sc" data-s="START" data-e="END">`, with times in seconds. A script turns these into the CSS variables `--s` and `--o`, which drive a fade in at the start and a fade out at the end.
- An element inside a scene animates when you give it class `a` plus an effect class (`up`, `pop`, `blur`, `drop`, `fade`, `dim`) and an inline `--r` (seconds after the scene starts). Its real delay is `--s + --r × --k`.
- `--k` (default 1) compresses a whole scene's choreography. The 30-second cut uses it, so the short version needs **no separate HTML**. Edit `SHORT_PLAN` in `video/build.py` to choose which scenes it keeps and their new start/end times.
- Looping ambience (`.spin`, `.ring`, `.flick`, `.dm` pulse, the background `.glow`) also runs off `--s`, so it is deterministic too.
- `window.seek(t)` pauses every animation and sets its `currentTime` to `t`. That's why a frame at any `t` is exact, whatever the capture speed.

## Layout rules for vertical social video

- Canvas: 1080×1920.
- Keep key content between **y ≈ 280 and y ≈ 1500**:
  - Reels and Stories overlay the profile and progress bars at the top (about 250 px);
  - the caption, buttons and reply box sit at the bottom (about 400 px);
  - the like and comment buttons sit on the right edge, roughly x > 960, y > 1100.
- The handle `@savtuferda` sits at the top (`.brand`) and large on the final call-to-action scene.
- Every scene has on-screen Turkish text, because Instagram autoplays muted. Arabic is large (70–260 px) with full harakat.
- Look: the same identity as the lesson pages. That means a deep green ground, gold accent, stone-coloured cards, Amiri for Arabic, and Alegreya / Alegreya Sans for Turkish.

## Making a new promo video

1. Get the teacher's script and match each sentence to a scene. Around 2.5 Turkish words per second is a natural speaking pace.
2. Copy `video/src/scene.html` to a new file (or edit it for a new word). Replace the content of each scene; reuse the effect classes and the step structure (dots + numbered title).
3. Set the `data-s`/`data-e` times. Scenes must not overlap; leave about 0.45 s for the fade out.
4. Check with `stills.js` at the **end** of each scene's entrance (once everything has appeared). Look for:
   - overlaps, where an Arabic diacritic hits the Turkish line below it (add `margin-top`);
   - mixed Arabic and Latin text on one line in the wrong order (put the Arabic and Turkish on separate lines);
   - tap or pointer targets that miss their button.
5. Render, pull 3–4 frames from the MP4 to confirm, and update the voice-over timing sheet.

## Gotchas

- Fonts come from Google Fonts with `display=block`, and `render.js` waits for `document.fonts.ready`. Without a network connection, the Arabic falls back to a system font, so check the stills.
- Never mix Arabic and Latin inside one `<text>`/inline run when the order matters (bidi reordering). Use two elements.
- Root letters coloured inside a word (`<span class="rl">`) keep their joining in Chromium, as long as the span only changes colour (no padding or margins).
- Playwright and Chromium: use the system install. Don't run `playwright install`. If this is a fresh machine, see the README.
