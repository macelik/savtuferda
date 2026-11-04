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
3. **Translate first, then fill in the cards.** If the teacher left the "Çeviri" section empty, fill `rows[i][2]` (the Turkish translation) and each card's `verseTr` **before** writing any card. Use the parsing procedure under "Translating literary Arabic" below; every card depends on reading the line correctly. Then fill in every TODO, card by card (rules below).
4. **Self-review**: go through the checklist at the end of this file and fix what fails.
5. **Build:**
   ```bash
   python3 lesson/build.py lesson/data/<slug>.json lesson/output/<Name>-Ders.html
   ```
   The build refuses to run if any TODO is left, a word has no harakat, `sarfNote` lacks the root, an `mg` key is unknown, or a verse's `<mark>` differs from the text's. Fix what it reports and rebuild.
6. **QA:**
   ```bash
   node lesson/tools/check.js lesson/output/<Name>-Ders.html qa/<slug>
   ```
   It must print `OK`. Then **open and look at every screenshot** with the Read tool. In the `root-dark.png` screenshot, the gold letters inside the three forms must be exactly the root letters.
7. **Report** (format at the end of this file).

## Card fields

Write every Arabic string with **full harakat**. Write every Turkish string in natural Turkish. Grammar terms use the Turkish tradition: mazi, muzari, masdar, harf-i cer, bab (I.–X.), ism-i fâil, ism-i mekân, müennes, tesniye, cemi, şart cümlesi, istiare…

| Field | What to write |
|---|---|
| `word` | The target word **exactly as vowelled in the text**; if the text has no harakat, add them (e.g. `يَتَسَلَّقُ`). For a phrase, the whole phrase. |
| `translit` | `"yanjalī <span class=\"sep\">·</span> fiil · VII. bab, muzari"`. Before the separator: the word **as vowelled in the text**, transliterated with this scheme: ā ī ū · ʾ (hamza) · ʿ (ʿayn) · ṯ (ث) · ḥ (ح) · ḫ (خ) · ḏ (ذ) · š (ش) · ṣ (ص) · ḍ (ض) · ṭ (ط) · ẓ (ظ) · ġ (غ) · q (ق). Write every short vowel, e.g. `yuʿāniqhu`, `wa-ndaṯar`, `al-qadar`. After the separator: a short Turkish grammar label. |
| `levels` | How hard the **word itself** is for a learner: everyday words `["A2","B1"]`, literary or rare words `["B1"]` or `["B1","B2"]`. This is a label for the word; it is **not** a list of the example levels (examples always span A2–B2). |
| `gist` | 1–3 Turkish words: the core meaning (`yükselmek`, `patlak vermek`). It appears under the animation and on the flash card. |
| `mg` | The motion-graphic key that best shows the meaning, from the table below. |
| `verseTr` | The Turkish translation of the text unit, in “typographic quotes”. |
| `sarf` | `[[mazi, muzari, masdar]]`, all vowelled: `[["اِنْتَظَرَ","يَنْتَظِرُ","اِنْتِظَارًا"]]`. For a noun or adjective, give the verb it comes from. Use two rows only when a card compares two verbs. |
| `sarfNote` | **Must start** `<b>Kök:</b> ن-ظ-ر · ` followed by one short Turkish note: the bab, a related noun, or the word form, e.g. `ism-i mekân`. The page reads the root letters from this string. |
| `def` | A simple Arabic definition at A2–B1 level, one or two short sentences. If the word is used figuratively in the text, explain that use: `«الجِدَارُ» فِي القِصَّةِ = الخَوْفُ الَّذِي يَمْنَعُهُ`. |
| `defTr` | `Türkçe: “…”` |
| `syn` | `[{"k":"syn","ar":"…، …"},{"k":"ant","ar":"…، …"}]`: 2–4 real Arabic synonyms and antonyms. If there is no true antonym, say so in Arabic (`لَا ضِدَّ مُبَاشِرًا`). |
| `note` | **One or two sentences** in Turkish: the single most useful thing about how this word is used in **this** text. Keep it short. |
| `harf` | Prepositions the word takes, with 1–2 examples (`<b>` around the preposition). If it takes none, delete `harf` entirely. |
| `meanings` | 2–3 senses. Each `t` is short Arabic with a Turkish gloss in parentheses: `يَتَرَقَّبُ وَيَتَوَقَّعُ (beklemek, gözlemek)`. Each sense has 1–3 examples tagged `A2`/`B1`/`B2`. |
| `extras` | 1–3 extra usages, each tagged `mecaz`, `basın` or `ayet`. An `ayet` entry **must** have `src` (e.g. `"Bakara 2:255"`). |
| `ayat` | Optional; only for special cards that need a whole "Ayetler" step. |
| `qs` | Exactly 2 discussion questions in Arabic: one A2, one B1. Make them personal and easy to discuss in class. **Use the target word in each.** |

### Example level guide
- **A2:** 4–7 words, everyday vocabulary, present or past tense. `اِنْتَظَرْتُ صَدِيقِي أَمَامَ المَدْرَسَةِ.`
- **B1:** one or two clauses, slightly abstract. `لَا بُدَّ أَنْ يَنْتَهِيَ الشِّتَاءُ مَهْمَا طَالَ.`
- **B2:** press or academic register, or figurative. `يَنْتَظِرُ المُسْتَثْمِرُونَ قَرَارَ البَنْكِ المَرْكَزِيِّ.`

Every example must be **original** and natural. Don't copy a sentence from the text itself, and don't repeat one structure across all examples.

- **Use real collocations.** Write examples an Arab journalist or teacher would actually write. For "the record was broken" Arabic says «تَحَطَّمَ الرَّقْمُ القِيَاسِيُّ» or «كُسِرَ الرَّقْمُ القِيَاسِيُّ», not «اِنْكَسَرَ الرَّقْمُ». If you aren't sure a combination is idiomatic, pick a simpler sentence you are sure of.
- **`basın` examples sound like headlines or news sentences**: governments, markets, matches, weather. Don't force the word into economic jargon where it doesn't belong.
- **A2 questions are concrete and personal**: your home, family, city, last weekend. Save abstract "what do you think…" questions for B1.

### Accuracy rules (non-negotiable)
- Quran: quote it **only if you are certain** of the exact wording **and** the sura:ayah. Use the Turkish sura name (Bakara, Âl-i İmrân, Nisâ, Mâide, En'âm, A'râf…). If you're not certain, leave it out. A missing ayah is fine; a wrong ayah is not.
- Hadith: give the collection (Buhârî, Müslim, Tirmizî…). Leave it out if you're unsure.
- Arabic definitions contain **no Turkish or Persian words** in Arabic script. Put Turkish only inside parentheses.
- The masdar and bab must match the sense used in the text (e.g. اِنْتَظَرَ = VIII. bab → اِنْتِظَار).
- Transliteration must agree with the harakat you show.
- Keep the teacher's text exactly as given. If you think the text has a typo or questionable vowelling, mention it in the report; don't change it.

## Translating literary Arabic

Most mistakes come from misreading who does what to whom. For **each** text unit, before translating, work out silently:
1. the verbs, with their roots and forms;
2. the subject (فَاعِل) of each verb;
3. the object (مَفْعُول), **including attached pronouns** (ـهُ، ـهَا، ـنِي…).

Then translate. Check yourself against these traps:
- **Word order is often verb–object–subject.** In «أَدْرَكَهُ المَوْتُ», the ـهُ is the object and المَوْتُ is the subject: "death overtook him". It does **not** mean "he reached death". Likewise «مَنْ لَمْ تُغْرِهِ الدُّنْيَا» means "whom the world did not tempt".
- **A hollow verb after لَمْ / لَا (jussive) loses its long vowel.** «لَمْ تَخُنْهُ» comes from خَانَ / يَخُونُ ("to betray"), so it means "did not betray him". It is not from a root خ-ن-ن. Always restore the full root before translating: يَقُلْ ← قَالَ, يَكُنْ ← كَانَ, تَخُنْ ← خَانَ, يَبِعْ ← بَاعَ. Look the root up in your head before choosing a meaning.
- **Figurative subjects.** Night, fate, death and nothingness act like people in poetry. Keep the image in Turkish; don't flatten it.
- **Translate the meaning, keep the image.** "Zincirin de kırılması kaçınılmazdır" is good. Don't paraphrase the line into an explanation.

**Poetic licence is not an error.** In verse, the rhyme letter often takes a sukun (e.g. يَنْتَظِرْ instead of يَنْتَظِرَ at the end of a line). A final long vowel may stay or be lengthened for the metre (أَنْ يَرْتَقِي). Case endings can bend to the rhyme. Don't report these as mistakes; at most, mention in a `note` that "kafiye gereği sükûnla okunur". Report only genuine typos (a wrong letter or a missing word).

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

## Motion graphics (`mg`) and their captions (`mgText`)

Pick the scene that shows **the sense used in this text**. Ask: "If a student only saw this animation, would they guess the word?" If no key passes that test, use the closest one and say so in the report.

| key | scene | use for | caption slots |
|---|---|---|---|
| `point` | a magnifier picks one of three boxes | mean, specify, choose, intend | `cap` |
| `aim` | an arrow turns and flies at a target | aim, direct, guide, head for, intend towards | — |
| `rise` | dots float up to a glowing sky | rise, ascend, climb | `cap` |
| `deflate` | a curve rises then falls | disappointment, failure, decline, a blow | `a` (peak), `b` (fall) |
| `slope` | a ball rolls down an incline | descend, slope, fall, sink, decline, fade away over time | — |
| `thought` | a head with thought bubbles | think, worry, whisper, imagine, remember, long for | — |
| `diverge` | two paths split from one point | differ, disagree, separate | `a`, `b` |
| `dim` | a stone with a weak, flickering light | scarce, little, dim, stingy, weak | `cap` |
| `flame` | flames and sparks | erupt, burn, break out, anger, passion | — |
| `eye` | an eye blinks and stares | see, stare, watch, notice | — |
| `radiate` | rotating light rays, a pulsing centre | appear, shine, dawn, clear up (night/fog), reveal | — |
| `grow` | grass blades grow from the ground | grow, sprout, be born, spread | `cap` |
| `shart` | a pulse travels between two circles | condition → result, cause → effect, request → response | `a`, `b` (short Arabic), `aTr`, `bTr` (Turkish), `mid` (Arabic, optional) |
| `birds` | two birds circle | fly, hover, freedom, soar | `cap` |
| `shout` | a speaker with sound waves | shout, call, answer, respond, say, sing, hear | `cap` |
| `break` | a chain snaps in the middle | break, shatter, be defeated, free oneself | `cap` |
| `embrace` | two arms close around a glowing centre | embrace, hug, hold, contain, cling to | `cap` |
| `vanish` | wisps of steam rise from a dish and fade | evaporate, vanish, disappear, perish, die out | `cap` |

Captions are tiny labels inside the animation. Each key has a generic default. Set `mgText` to tie the animation to **this** text, using only the slots listed for that key, and keep each label to 1–4 words:

```json
"mg": "break", "mgText": {"cap": "kapı kırılır"}
"mg": "shart", "mgText": {"a": "اِجْتِهَاد", "b": "نَجَاح", "aTr": "çalışırsan", "bTr": "başarırsın"}
```

Never reuse captions from another lesson. A structure card with `mg: "shart"` **must** set `mgText`.
If two consecutive cards would get the same key, choose a different fitting key for one of them.

## Meta

- `title`: a short name, e.g. `Hayat İradesi — Ebu'l-Kasım eş-Şabbi`.
- `brandAr`, `brandTr`: from the request.
- `sources`: the dictionaries (already filled in), plus one line listing every Quran/hadith reference you used. Delete that TODO line if you used none.
- `notes[0]`: one Turkish sentence on the text and its **verified** source.

## Self-review checklist (do this before building)

- [ ] Every unit's Turkish translation matches the parse: subject, object and attached pronouns (re-read units with ـهُ/ـهَا and any verb after لَمْ).
- [ ] Each `mg` passes the "would a student guess the word" test, and the `mgText` captions are about this text.
- [ ] `translit` follows the scheme and the text's own vowels; no missing short vowels.
- [ ] No Quran or hadith quote you are not certain of, word for word.
- [ ] Each `basın` and `mecaz` example uses an idiomatic collocation.
- [ ] Poetic licence wasn't reported as an error.
- [ ] `notes[0]` states the source and whether you could verify it.

## Final report (reply to the user)

```
Built: lesson/output/<Name>-Ders.html  (<n> cards)  ·  QA: OK
Source check: <author/source confirmed | corrected from X to Y | could not verify>
Corrections / doubts about the teacher's input: <list or "none">
Citations used: <list of ayat/hadith with references, or "none">
Assumptions: <e.g. levels, how a phrase was split>
```
