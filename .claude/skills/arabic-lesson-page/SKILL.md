---
name: arabic-lesson-page
description: Build an interactive Arabic lesson page (single HTML, Turkish UI) for @savtuferda from an Arabic text with marked target words. Use when given a lesson request (templates/lesson-request.md format), a teacher's HTML draft with <mark>ed words, or "here is a poem / text / cartoon dialogue and the words to teach".
---

# Arabic lesson page

The teacher sends an Arabic text (a poem, prose, a cartoon dialogue or a song) and marks the words she wants to teach. You produce `lesson/output/<Konu>-<Yazar>-Ders.html`, a single self-contained page she presents in class to **Turkish-speaking A2–B2 learners**.

**Your job is the content.** The design, layout, animation and interactivity already exist in `lesson/src/template.html`. Never edit the template or write HTML by hand. You fill in one JSON file, and `lesson/build.py` turns it into the page.

The worked example to imitate is `lesson/data/kudus-mahmud-dervis.json` and its built page `lesson/output/Kudus-Mahmud-Dervis-Ders.html`. Open the JSON and read at least cards 1, 8 and 13 before you write anything.

## Workflow

Run all commands from the repo root.

1. **Scaffold.** Pick a short ASCII slug (e.g. `irade-el-hayat`):
   ```bash
   python3 .claude/skills/arabic-lesson-page/scripts/scaffold.py <request.md|draft.html> lesson/data/<slug>.json
   ```
   This fills every mechanical field: the text units, the translation rows, one card per marked word, and each card's `verse` with exactly one `<mark>`. Every content field it can't fill is set to `"TODO: …"`.
2. **Verify the source.** Who wrote the text, and where is it from? Check the requested `author`/`source` against what you know. If they're wrong or you're unsure, say so in `meta.notes` **and** in your final report. Never invent an attribution.
3. **Fill in every TODO** (rules below). Work card by card. If the teacher left the "Çeviri" section empty, also fill `rows[i][2]` (the Turkish translation) and each card's `verseTr`.
4. **Build:**
   ```bash
   python3 lesson/build.py lesson/data/<slug>.json lesson/output/<Name>-Ders.html
   ```
   The build refuses to run if any TODO is left, a word has no harakat, `sarfNote` lacks the root, an `mg` key is unknown, or a verse's `<mark>` differs from the text's. Fix what it reports and rebuild.
5. **QA:**
   ```bash
   node lesson/tools/check.js lesson/output/<Name>-Ders.html qa/<slug>
   ```
   It must print `OK`. Then **open and look at every screenshot** with the Read tool. In the `root-dark.png` screenshot, the gold letters inside the three forms must be exactly the root letters.
6. **Report** (format at the end of this file).

## Card fields

Write every Arabic string with **full harakat**. Write every Turkish string in natural Turkish. Grammar terms use the Turkish tradition: mazi, muzari, masdar, harf-i cer, bab (I.–X.), ism-i fâil, ism-i mekân, müennes, tesniye, cemi, şart cümlesi, istiare…

| Field | What to write |
|---|---|
| `word` | The target word as it appears in the text, **fully vowelled** (e.g. `يَنْجَلِيَ`). For a phrase, the whole phrase. |
| `translit` | `"yanjaliya <span class=\"sep\">·</span> fiil · VII. bab, muzari, mansub"`. Before the separator: a Latin transliteration. After it: a short Turkish grammar label. |
| `levels` | The levels the card covers, e.g. `["A2","B1"]`. Add `"B2"` when B2 examples are included. |
| `gist` | 1–3 Turkish words: the core meaning (`yükselmek`, `patlak vermek`). It appears under the animation and on the flash card. |
| `mg` | The motion-graphic key that best shows the meaning, from the table below. |
| `verseTr` | The Turkish translation of the text unit, in “typographic quotes”. |
| `sarf` | `[[mazi, muzari, masdar]]`, all vowelled: `[["اِنْجَلَى","يَنْجَلِي","اِنْجِلَاءً"]]`. For a noun or adjective, give the verb it comes from. Use two rows only when a card compares two verbs. |
| `sarfNote` | **Must start** `<b>Kök:</b> ج-ل-و · ` followed by one short Turkish note: the bab, a related noun, or the word form, e.g. `ism-i mekân`. The page reads the root letters from this string. |
| `def` | A simple Arabic definition at A2–B1 level, one or two short sentences. If the word is used figuratively in the text, explain that use: `«القَيْدُ» فِي البَيْتِ = الظُّلْمُ وَالاسْتِعْمَارُ`. |
| `defTr` | `Türkçe: “…”` |
| `syn` | `[{"k":"syn","ar":"…، …"},{"k":"ant","ar":"…، …"}]`: 2–4 real Arabic synonyms and antonyms. If there is no true antonym, say so in Arabic (`لَا ضِدَّ مُبَاشِرًا`). |
| `note` | **One or two sentences** in Turkish: the single most useful thing about how this word is used in **this** text. Keep it short. |
| `harf` | Prepositions the word takes, with 1–2 examples (`<b>` around the preposition). If it takes none, delete `harf` entirely. |
| `meanings` | 2–3 senses. Each `t` is short Arabic with a Turkish gloss in parentheses: `يَنْكَشِفُ وَيَزُولُ (açılmak, dağılmak)`. Each sense has 1–3 examples tagged `A2`/`B1`/`B2`. |
| `extras` | 1–3 extra usages, each tagged `mecaz`, `basın` or `ayet`. An `ayet` entry **must** have `src` (e.g. `"Bakara 2:255"`). |
| `ayat` | Optional; only for special cards that need a whole "Ayetler" step. |
| `qs` | Exactly 2 discussion questions in Arabic: one A2, one B1. Make them personal and easy to discuss in class. **Use the target word in each.** |

### Example level guide
- **A2:** 4–7 words, everyday vocabulary, present or past tense. `اِنْكَسَرَ الكُوبُ.`
- **B1:** one or two clauses, slightly abstract. `لَا بُدَّ أَنْ يَنْجَلِيَ الظَّلَامُ مَهْمَا طَالَ.`
- **B2:** press or academic register, or figurative. `اِنْكَسَرَتْ مَوْجَةُ الاحْتِجَاجَاتِ أَمَامَ الإِصْلَاحَاتِ.`

Every example must be **original** and natural. Don't copy a sentence from the text itself, and don't repeat one structure across all examples.

### Accuracy rules (non-negotiable)
- Quran: quote it **only if you are certain** of the exact wording **and** the sura:ayah. Use the Turkish sura name (Bakara, Âl-i İmrân, Nisâ, Mâide, En'âm, A'râf…). If you're not certain, leave it out. A missing ayah is fine; a wrong ayah is not.
- Hadith: give the collection (Buhârî, Müslim, Tirmizî…). Leave it out if you're unsure.
- Arabic definitions contain **no Turkish or Persian words** in Arabic script. Put Turkish only inside parentheses.
- The masdar and bab must match the sense used in the text (e.g. اِنْكَسَرَ = VII. bab → اِنْكِسَار).
- Transliteration must agree with the harakat you show.
- Keep the teacher's text exactly as given. If you think the text has a typo or questionable vowelling, mention it in the report; don't change it.

## Special cards (a phrase or a structure)

When a mark is a whole structure (a conditional, an idiom, a word pair) or the request's "Notlar" asks for a special focus:
- `word` = the full phrase, with `short` set to a 1–2 word strip label and `flashFront` set to the key words.
- `translit` grammar label: e.g. `şart cümlesi`.
- `sarf`: one row per verb in the structure.
- `def` + `defTr`: what the whole structure means.
- `note`: explain the **structure** in Turkish, e.g. `إِذَا … فَـ: şart edatı + cevap; cevap cümlesi "فَلَا بُدَّ" ile gelir`.
- `mg`: `"shart"` for a condition→result relationship.
- Optional extra fields: `rootGrid`, `commonBoxAr`, `commonBoxTr`, `commonAr`, `ayat`. See card 13 in the Kudüs file.
- Delete `harf` if it doesn't apply.

## Motion graphics (`mg`)

| key | scene | use for |
|---|---|---|
| `point` | a magnifier picks one of three boxes | mean, specify, choose, intend |
| `aim` | an arrow turns and flies at a target | aim, direct, guide, head for |
| `rise` | dots float up to a glowing sky | rise, ascend, climb, hope |
| `deflate` | a curve rises then falls | disappointment, failure, decline |
| `slope` | a ball rolls down an incline | descend, slope, fall, sink |
| `thought` | a head with thought bubbles | think, worry, whisper, imagine, remember |
| `diverge` | two paths split from one point | differ, disagree, separate, choose between |
| `dim` | a stone with a weak, flickering light | scarce, little, dim, stingy, weak |
| `flame` | flames and sparks | erupt, burn, break out, anger, passion |
| `eye` | an eye blinks and stares | see, stare, watch, notice |
| `radiate` | rotating light rays, a pulsing centre | appear, shine, light, clear up, reveal |
| `grow` | grass blades grow from the ground | grow, sprout, rise up, be born, spread |
| `shart` | a pulse travels between two circles | condition → result, cause → effect |
| `birds` | two birds circle | fly, hover, freedom, soar |
| `shout` | a speaker with sound waves | shout, call, answer, say, sing, hear |

Choose by the **sense used in the text**, not the dictionary's first meaning. Two cards may share a key, but the same key on more than three cards looks repetitive. In that case, choose the next-best fit.

## Meta

- `title`: a short name, e.g. `Hayat İradesi — Ebu'l-Kasım eş-Şabbi`.
- `brandAr`, `brandTr`: from the request.
- `sources`: the dictionaries (already filled in), plus one line listing every Quran/hadith reference you used. Delete that TODO line if you used none.
- `notes[0]`: one Turkish sentence on the text and its **verified** source.

## Final report (reply to the user)

```
Built: lesson/output/<Name>-Ders.html  (<n> cards)  ·  QA: OK
Source check: <author/source confirmed | corrected from X to Y | could not verify>
Corrections / doubts about the teacher's input: <list or "none">
Citations used: <list of ayat/hadith with references, or "none">
Assumptions: <e.g. levels, how a phrase was split>
```
