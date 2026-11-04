# savtuferda

Teaching materials and promo videos for **@savtuferda**: Arabic cartoon and poetry workshops for Turkish speakers (A2–B2).

This repo contains two pipelines:

1. **Lesson pages:** an Arabic text (poem, prose, cartoon dialogue) plus the target words go in, and a single self-contained interactive HTML lesson comes out. The teacher presents it in class, and students can open it on their phones.
2. **Promo videos:** a 1080×1920 animated Reel/Short/Story is generated from HTML/CSS. Frames are captured in headless Chromium and encoded with ffmpeg.

## Repository layout

```
lesson/
  src/template.html           the lesson page (CSS + JS + motion graphics); data is injected at __DATA__
  data/<name>.json            one file per lesson: all content (see docs/lesson-page-instructions.md §5)
  build.py                    validate JSON + render -> lesson/output/<Name>-Ders.html
  tools/check.js              headless QA: console errors, overflow, screenshots
  tools/extract_legacy.py     import an old long-scroll lesson HTML into the JSON shape
  source/                     the teacher's original hand-made HTML (input for the first lesson)
  output/                     built lesson pages (deliverables)
video/
  src/scene.html              the promo video composition (15 scenes, CSS animation)
  build.py                    -> video/build/full.html (75 s) + short.html (30 s cut)
  render.js                   frame-accurate capture -> MP4
  stills.js                   preview single frames
  output/                     delivered MP4s + cover image
docs/
  lesson-page-instructions.md the brief for generating new lesson pages (pedagogy, data, design, accuracy)
  video-pipeline.md           how the video system works and how to make a new one
  reel-voiceover-cues.md      voice-over timing sheet for the 75 s Reel
CLAUDE.md                     working agreement for agents picking up this repo
```

## Requirements

- Python 3.9+. `build.py` uses only the standard library; `extract_legacy.py` needs `beautifulsoup4`.
- Node 18+ with `playwright` and a Chromium for it, used by `check.js`, `render.js` and `stills.js`.
- `ffmpeg` with libx264.
- Network access to `fonts.googleapis.com` (Amiri, Alegreya, Alegreya Sans).

On a fresh machine:

```bash
npm install
```

```bash
npx playwright install chromium
```

```bash
pip install -r requirements.txt
```

(In Claude Code cloud sessions, Playwright and Chromium are preinstalled: skip `playwright install`.)

## Quick start

```bash
python3 lesson/build.py lesson/data/kudus-mahmud-dervis.json lesson/output/Kudus-Mahmud-Dervis-Ders.html
```

```bash
node lesson/tools/check.js lesson/output/Kudus-Mahmud-Dervis-Ders.html qa/
```

```bash
python3 video/build.py
```

```bash
node video/render.js video/build/short.html video/output/Arapca-Atolye-30sn.mp4 30
```

Open any `lesson/output/*.html` directly in a browser. It needs no server.

## Lesson page in brief

Three views:
- **Şiir/Metin:** the full text, with the target words clickable and line-by-line reading mode.
- **Kelimeler:** one slide per word. A dark stage on the left shows the word, its transliteration and a looping motion graphic. Step tabs on the right go Şiirde → Kök (animated root letters, mazi/muzari/masdar with root letters in gold) → Anlam → Harf-i cer → Örnekler (level filter) → Ayetler → Konuşalım (60-second timer).
- **Pratik:** a fill-in-the-blank quiz and flip cards.

Turkish translations are blurred until tapped, or `T` reveals them all. Keys: `←`/`→` words, Space next step, `F` fullscreen. Light and dark themes are supported, and the page works on phones.

The first lesson: **«في القدس»** by Mahmud Derviş, with 15 words and one conditional sentence.
