# Working on savtuferda

The client is an Arabic teacher (Instagram: **@savtuferda**). She runs cartoon and poetry workshops for **Turkish-speaking** learners at A2–B2. Requests usually arrive through a family member and look like one of these:

- "Here is a text + the words she wants to teach → make the lesson page."
- "Make a promo video / a shorter cut / a version for another text."

## Ground rules

- **Everything students or followers see is in Turkish**, with Arabic content in Arabic, fully vowelled. Grammar terms follow the Turkish tradition (mazi, muzari, masdar, harf-i cer, bab, kök…). Code, comments and docs are in English.
- **Accuracy beats speed.** Verify the authorship of texts. The teacher's first draft credited the Darwish poem to Tamim al-Barghouti; the poem is by Darwish. Keep Arabic definitions free of Turkish or Persian loanwords. Quran and hadith citations must be real and exact. Report any correction you make in your hand-off note; never silently "fix" the teacher's content.
- **Don't redesign.** The teacher likes the current look: deep green, gold, stone-coloured cards, Amiri + Alegreya. New lessons are new **data**; new videos reuse the **scene system**.
- **Less text on screen.** The original complaint was "too much text". One idea per screen, Turkish revealed on demand, meaning shown through motion.

## Where to start

| Task | Read | Run |
|---|---|---|
| New lesson page | `docs/lesson-page-instructions.md` (the full brief) | `python3 lesson/build.py lesson/data/<x>.json lesson/output/<X>-Ders.html`, then `node lesson/tools/check.js <out.html> qa/` |
| New / changed promo video | `docs/video-pipeline.md` | `python3 video/build.py`, `node video/stills.js …`, `node video/render.js …` |
| Voice-over timing for a video | `docs/reel-voiceover-cues.md` (example) | — |

## Conventions

- Lesson content lives **only** in `lesson/data/*.json`. Change `lesson/src/template.html` only for features every lesson should get, then rebuild **all** lessons in `lesson/output/` and check at least one.
- Motion graphics are keys in the `MG` object in the template. When you add one, also add it to `MG_KEYS` in `lesson/build.py`.
- Output file names are ASCII: `<Konu>-<Yazar>-Ders.html`, `Arapca-Atolye-<…>.mp4`.
- Generated artefacts that are deliverables (`lesson/output/`, `video/output/`) are committed. Intermediate builds (`video/build/`, `qa/`) are not.
- QA is mandatory before you hand anything off:
  - for a lesson: `check.js` reports no errors, and you have looked at the screenshots;
  - for a video: stills at the end of each scene, plus 3–4 frames pulled from the final MP4.
- The page must open from `file://` with no server. External resources: Google Fonts only.

## Known limitations

- Videos are silent on purpose; the teacher records her own narration. Don't add synthetic TTS unless asked.
- A print/PDF button doesn't work when the page is shared inside a sandboxed viewer. If a handout is requested, make a separate print layout.
- In `lesson/data/kudus-mahmud-dervis.json`, the `poem`/`rows` keys hold generic text units. The names are historical; keep them.
