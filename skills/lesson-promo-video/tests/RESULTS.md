# Skill trials

## Trial 1 · Haiku, full pipeline

**Setup:**
- The skill was installed in an empty project, with the Şabbi «إرادة الحياة» lesson (from the `arabic-lesson-page` examples).
- The request was `yenceli.request.md`: card 4 «يَنْجَلِي», a new Turkish script, and the short cut too.
- The prompt was only "follow the skill exactly".

| Check | Result |
|---|---|
| Storyboard valid; compose, stills, both renders, cover | ✓ long 0:57, short 0:30, 1080×1920 H.264 |
| Script mapped to the right scene types | ✓ 11 scenes; her words kept |
| Step scenes filled from the lesson (`from_card`) | ✓ root ج-ل-و, forms, synonyms, mecaz, press example |
| Script line without lesson data ("Hangi harf-i cerle gelir?"; card 4 has no `harf`) | ✓ left out and reported, nothing invented |
| No ayah step (card has none) | ✓ |
| Reviewed stills and MP4 frames, found and fixed a problem | ✓ found the low-contrast press translation |
| Sensible hook | ✗ put a meaningless big «إ» in `glyph`; the long title wrapped badly |

**Changes after the trial:**
- The press translation colour is fixed in the renderer. (The published Reel in `showcase/` was made before this fix and has the faint line too.)
- Hook titles now shrink automatically when long.
- `glyph` only accepts `؟` or nothing, and is documented as "only when the headline is a question".

When you change `SKILL.md` or a scene renderer, re-run this trial with a fresh small model and add a section here.
