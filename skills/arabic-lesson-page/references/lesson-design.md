# Instructions: Interactive Arabic Lesson Page from a Text

You are building a **single, self-contained HTML lesson page** that an Arabic teacher presents in class to **Turkish-speaking learners (A2–B2)**. The teacher gives you an Arabic text and a list of target words or phrases. You produce one `.html` file that she projects in class and students can also open on their phones.

The reference implementation is `examples/kudus-mahmud-dervis.json` (Mahmud Derviş, «في القدس»), built with `assets/template.html` (paths are relative to this skill's folder). **For a new lesson, write a new JSON data file and run `scripts/build.py`. Don't redesign or copy the HTML by hand.** Change the template only to add a capability that every lesson gains (new motion graphic, new source type). This document says what to keep, what to change and why.

---

## 1. Inputs

The teacher will provide:

| Input | Required | Notes |
|---|---|---|
| Arabic source text | yes | A poem, book excerpt, cartoon/comic dialogue, song lyrics, news piece, etc. May or may not have harakat (vowel marks). |
| Target words/phrases | yes | Usually 8–20 items. They can be single verbs, nouns, adjectives, phrases (`يصعدون إلى`) or a whole structure (a conditional sentence, an idiom). |
| Source info | usually | Title, author, book/episode name. **Verify it** (see §8). |
| Level | optional | Default: A2–B1 core with B2 extensions. |
| Turkish translation | optional | If missing, write one yourself. |
| Special focus | optional | E.g. "focus on the shared root of these two verbs" or "this is a şart cümlesi". Give such items their own slide type. |

If something essential is ambiguous, ask once. Examples: which occurrence of a repeated word is meant, or whether a phrase should be split. Otherwise use sensible defaults and list your assumptions at the end.

## 2. Output

- **One `.html` file**, with all CSS and JS inline and the data embedded as JSON in `<script type="application/json" id="data">`. The only external resource is Google Fonts.
- It must work when opened directly from disk (`file://`), offline except for the fonts.
- File name: `<Konu>-<Yazar>-Ders.html` in ASCII, e.g. `Kudus-Mahmud-Dervis-Ders.html`.
- **All UI text is in Turkish.** Arabic content is in Arabic. Grammar terms use the Turkish tradition (mazi, muzari, masdar, harf-i cer, bab, kök, şart cümlesi, temyiz, tesniye, müennes…). Arabic labels go next to the Turkish headings (`Anlamı · المعنى`).

## 3. Teaching philosophy (why the page looks like this)

The previous version failed because it was **one long scroll with too much text at once**. Follow these rules:

1. **One idea per screen.** Each target word is one "slide". Inside it, content is split into steps that the teacher reveals one at a time.
2. **Arabic first, Turkish on demand.** Turkish translations are **blurred by default**. Students guess first; tapping a line reveals it, and the `T` key reveals all. Remember the choice in `localStorage` (inside try/catch).
3. **Show, don't explain.** Each word gets a small looping **motion graphic** that shows its meaning (see §6). The root letters **animate in** and are then highlighted inside the derived forms.
4. **The text comes first.** The page opens with the full source text, where every target word is a clickable link to its lesson.
5. **End with practice:** a quiz built from the source text, plus flip cards.
6. Keep everything the teacher would put on a paper handout (definitions, examples, synonyms, Quran/hadith/press usages), just **layered behind steps**, not removed.

## 4. Page structure

Sticky top bar: Arabic title (gold) + Turkish subtitle "Başlık · Yazar", three tabs, and tools: `TR çeviriler` toggle, `Sunum` (fullscreen), theme toggle.

Use hash routing: `#metin` (or `#siir` for poems), `#kelime-N`, `#pratik`.

### 4.1 Text view ("Şiir" / "Metin" / "Diyalog")
Name the tab after the source type: **Şiir** for a poem, **Metin** for prose, **Diyalog** for a cartoon or comic, **Şarkı** for a song.

- Show the source split into **units**: poem lines, prose sentences, or dialogue turns. Number each unit.
- Under each unit, put its Turkish translation (blurred by default). A "Satır altı çeviri" button hides or shows these.
- Every target word is a `<button class="wbtn">` with a small superscript number. Clicking it goes to `#kelime-N`.
- **"Satır satır oku" mode:** highlight the current unit, dim the rest, and move with ← → / Space; Esc exits.
- **For dialogue (cartoon/comic):** show each turn as a speech bubble with the speaker's name (`Speaker:` label, alternating left/right alignment in RTL). Optionally add a small character colour dot per speaker. Everything else stays the same.
- **For prose:** split into sentences. Long paragraphs are fine, but each sentence needs its own translation row.

### 4.2 Word view ("Kelimeler")
- A horizontal **strip** of all target words (number + short unvowelled form) to jump between them.
- **Left "stage"** (dark green panel, sticky on desktop, stacked on mobile):
  - "Kelime N / total"
  - the word, large, with full harakat
  - transliteration (italic) + grammar label (e.g. `fiil · VII. bab, muzari, 3. dişil`)
  - the motion graphic (SVG)
  - a 1–3 word Turkish **gist** in gold (e.g. `patlak vermek`)
  - level badges, plus Önceki / Sonraki buttons
- **Right panel:** step tabs plus one content box. Build the steps from the data available:

| # | Step (tab label) | Content |
|---|---|---|
| 1 | **Şiirde / Metinde / Diyalogda** | The source unit with the word in `<mark>`, large; Turkish under it. |
| 2 | **Kök** | Root letters drop in as tiles, then a grid of forms (الماضي · المضارع · المصدر, with Turkish labels geçmiş / şimdiki-geniş / masdar), root letters coloured gold inside each form; a note box (root info, related nouns). For nouns or adjectives, show the source verb or the relevant derivations instead. |
| 3 | **Anlam** | A simple Arabic definition (A2–B1 wording), the Turkish meaning (blurred), synonym/antonym boxes (مرادف / ضد), and a short usage note. |
| 4 | **Harf-i cer** *(only if relevant)* | Big preposition chips + 1–3 example sentences; then "Ek kullanımlar" (mecaz / basın / ayet tags with source). |
| 5 | **Örnekler** | Meanings by context (numbered), each with 1–3 example sentences tagged A2/B1/B2, plus a level filter (Hepsi / A2 / B1 / B2). |
| 6 | **Ayetler** *(optional)* | Quran/hadith citations with sura:ayah. |
| 7 | **Konuşalım** | 2 discussion questions in Arabic (A2 + B1), large, and a 60-second thinking timer. |

Keys: Space / ↓ next step (at the last step, go to the next word), ↑ previous step, ← → previous/next word, 1–7 jump to a step, T translations, F fullscreen.

**Special items** (a conditional sentence, an idiom, a pair of words sharing a root) get the same frame, with steps adapted to them. Example: the şart slide had Kök with two conjugation rows, a "root bond" grid, a "common meaning" box, and Ayetler. Don't force such items into the single-verb template.

### 4.3 Practice view ("Pratik")
- **Boşluğu doldur:** for each word, show its source unit with the word replaced by a blank; offer 4 options (the right one plus 3 other target words in the form used in the text); give right/wrong feedback, reveal the translation, keep score, and offer "Yeniden başla". Shuffle the order.
- **Hafıza kartları:** a grid of flip cards. The front shows the Arabic word; the back shows the Turkish gist and the root. Add a "Hepsini çevir" button.
- Optional, if the text suits it: a matching game (Arabic ↔ Turkish), or "who said it?" for dialogues.

Footer: sources (dictionaries, Quran references), plus a note about the source text and its author.

## 5. Data model

All content lives in one JSON file (`lessons/<slug>/<slug>.json` in the user's project). `scripts/build.py` validates it and injects it into the template. The Kudüs file is the full worked example; copy its shape.

```json
{
  "meta": {
    "title": "Kudüs'te — Mahmud Derviş",          // <title>: short name, no explanation
    "brandAr": "في القدس", "brandTr": "Kudüs'te · Mahmud Derviş",
    "textTab": "Şiir",                           // Şiir | Metin | Diyalog | Şarkı
    "textHeading": "Önce şiiri dinleyelim",
    "sources": ["<span lang=\"ar\">المعجم الوسيط …</span>", "Kur'an-ı Kerim: …"],
    "notes": ["Şiir, Mahmud Derviş'in … şiiridir.", "Tanımlar A2–B1 …"]
  },
  "parse": ["unit 1: every verb -> mazi/muzari + root + meaning; subject; object", "…"],   // agent's working notes per unit; not shown on the page
  "poem": ["في القدس، <mark>أَعني</mark> داخلَ السُّور القديمِ،", "…"],   // text units, target words in <mark>
  "rows": [["1", "في القدس، أَعني …", "Kudüs'te — yani eski surların içinde,"], "…"],  // [no, Arabic, Turkish], same length as poem
  "cards": [
    {
      "word": "أَعْنِي",
      "translit": "a‘nī <span class=\"sep\">·</span> fiil · muzari, 1. tekil şahıs",  // part before sep = transliteration, after = grammar
      "levels": ["A2","B1"],
      "gist": "kastetmek",                 // 1–3 Turkish words, shown under the animation and on flash cards
      "mg": "point",                       // motion graphic key, see §6 (must exist in MG in template.html)
      "mgText": {"cap": "tam olarak bunu"}, // optional captions inside the animation (slots per key: cap | a,b | a,b,aTr,bTr,mid)
      "short": "إن لم…",                   // optional: label in the word strip (default: unvowelled word)
      "flashFront": "تُؤْمِنُوا / تَأْمَنُوا", // optional: front of the flash card (default: word)
      "verse": "في القدس، <mark>أَعني</mark> داخلَ السُّور القديمِ،",  // the unit, mark text must equal the <mark> in poem[]
      "verseTr": "“Kudüs'te — yani eski surların içinde,”",
      "sarf": [["عَنَى","يَعْنِي","عَنْي"]],   // rows of [mazi, muzari, masdar]; 2 rows for paired items
      "sarfNote": "<b>Kök:</b> ع-ن-ي · …",   // MUST contain "<b>Kök:</b> x-y-z" (or <b>x-y-z</b>): the root is parsed from it
      "def": "أَعْنِي = أَقْصِدُ …", "defTr": "Türkçe: “kastediyorum …”",
      "syn": [{"k":"syn","ar":"يَقْصِدُ، يُرِيدُ"}, {"k":"ant","ar":"…"}],
      "noteH": "Kullanım notu", "note": "…",                 // optional
      "harf": {"chips":["بِـ"], "ex":[{"ar":"…","tr":"…"}]},   // optional → "Harf-i cer" step
      "meanings": [{"t":"أَقْصِدُ … (Turkish gloss)","ex":[{"lvl":"A2","ar":"…","tr":"…"}]}],
      "extras": [{"tag":"mecaz|basın|ayet","ar":"…","tr":"…","src":"Haşr 59:9"}],
      "ayat": [{"ar":"…","tr":"…","src":"En'âm 6:82"}],      // optional → "Ayetler" step
      "qs": [{"lvl":"A2","ar":"…"},{"lvl":"B1","ar":"…"}],
      "rootGrid": [{"ar":"…","tr":"…"}], "commonBoxAr": "…", "commonBoxTr": "…", "commonAr": [{"ar":"…","tr":"…"}]  // optional, special items (see card 13)
    }
  ]
}
```

(The `//` comments are explanations only; real JSON has none.)

Notes:
- `poem`/`rows` are named for the first project, but they hold any text units: lines, sentences or dialogue turns. For a dialogue, start each unit with `<b>Speaker:</b>`.
- The steps a card shows are built from what it has: Şiirde → Kök → Anlam → (Harf-i cer) → (Örnekler) → (Ayetler) → Konuşalım.
- Turkish glosses in parentheses inside Arabic meaning lines are isolated automatically.
- `scripts/extract_legacy.py` imports an old long-scroll lesson HTML into this shape (then add `meta`, `gist`, `mg`).

## 6. Motion graphics (one per word)

The motion graphic is the most memorable part of each slide. Rules:

- Inline SVG, `viewBox="0 0 240 180"`, drawn with `currentColor` (gold on the dark stage) and two or three classes: `.s` stroke, `.f` fill, `.soft` faded. Keep it simple: under ~10 shapes, and **no long hand-drawn path data**.
- It must **show the meaning**, not decorate. Pick a concrete scene from the word's sense, ideally the sense used in the text.
- Use CSS keyframes that loop every 2–4 s. Useful primitives: draw a line (`stroke-dashoffset`), scale up from the base (`transform-origin:50% 100%`), move along a path (`offset-path`), rotate, pulse, expanding rings.
- An optional tiny Turkish caption inside the SVG (`.lbl`, e.g. "göğe doğru"). Arabic inside the SVG only as a separate `<text>`; never mix Arabic and Latin in one `<text>` (the bidi order breaks).
- Wrap everything in `@media (prefers-reduced-motion: reduce)` → no animation.

Ready-made idea library (reuse and extend it):

| Meaning type | Scene |
|---|---|
| rise, ascend | dots floating up toward a glowing circle |
| descend, slope | a ball rolling down an incline |
| aim, direct, guide | an arrow rotating to align, then flying at a target |
| mean, specify | a magnifier scanning three boxes and stopping on one |
| disappointment, failure | a curve that rises, then falls ("umut → kırıklık") |
| think, worry, whisper to oneself | a head outline with thought bubbles popping in turn |
| differ, disagree | two paths branching from one point |
| scarce, dim, little | a stone with a weakly flickering light |
| break out, erupt (war, fire) | flames growing with sparks rising |
| stare, gaze | an eye that blinks, then opens wide |
| appear, manifest, light | rays rotating with a pulsing centre and an expanding ring |
| grow, sprout | grass blades growing from the ground, staggered |
| fly, hover, circle | two birds orbiting with flapping wings |
| shout, cry out | a speaker cone with expanding sound arcs |
| condition → result | two circles with a pulse travelling from cause to effect |
| break, shatter (`break`) | a chain snaps in the middle |
| embrace, hold (`embrace`) | two arms close around a glowing centre |
| evaporate, vanish (`vanish`) | wisps of steam rise from a dish and fade |
| eat, drink, run, open, close, give, take… | invent an equally simple scene in the same visual language |

Captions inside an animation come from the card's `mgText`; each key has a generic default. Never hard-code a lesson's own words into the `MG` strings in the template: that leaks one lesson's captions into every other lesson (this happened with the first version of `shart`). The full key list with caption slots is in `SKILL.md`.

## 7. Root highlighting algorithm

Colour the root letters inside each derived form. Shaping survives inline `<span>`s in modern browsers.

- Split the word into clusters: base letter + its following diacritics (U+064B–U+065F, U+0670, U+0640).
- Walk the clusters and match them to the root letters in order. A cluster matches when:
  - it is the same letter, or
  - both are hamza-family letters (`ءأإآؤئا`), or
  - the root letter is weak (`و`/`ي`) and the cluster is any of `اوىيئ`.
- If a matched cluster has a shadda (U+0651) and the next root letter is the same letter, consume both (`شَحَّ` ← ش-ح-ح).
- Wrap matched clusters in `<span class="rl">`.

Check the result visually for every card. Hollow and defective verbs and form VII/VIII verbs are where mistakes happen.

## 8. Content accuracy (non-negotiable)

- **Verify the author and source** of the text. Do not repeat a teacher's or video title's attribution blindly, and do not invent one. If you are unsure, say so in the footer and in your reply. (The reference project's draft wrongly credited Tamim al-Barghouti for Darwish's poem.)
- **Arabic definitions must be Arabic.** No Turkish/Persian loanwords disguised as Arabic (e.g. نيشان). Put Turkish glosses in parentheses; the renderer wraps them in a bidi-isolated `<span class="lt">`.
- Give full harakat on the target word, its forms, definitions and example sentences. Keep the source text's own vowelling as given, and make transliteration agree with the harakat you show. If the source and the dictionary differ, point it out.
- Masdar, bab and transitivity must be correct for the sense used. If a verb has several masdars, give the common one for that sense.
- Quran citations must be exact text with the correct sura:ayah. Mark hadith with the collection. Never invent citations; drop them if you can't confirm them.
- Example sentences must be original, natural, and match their level:
  - **A2:** short, high-frequency vocabulary.
  - **B1:** a clause or two.
  - **B2:** press or abstract register.
- Questions should be personal and discussion-friendly, at A2 and B1.
- Translations: natural Turkish, faithful to the text. For literary texts, keep the image ("Yaram, İncil'e ait beyaz bir güldür").
- Cartoons and comics may use colloquial or dialect Arabic. Name the dialect, give the فصحى equivalent in the Anlam step, and don't "correct" the original text.
- Don't sanitize a sensitive text (war, religion, politics). Treat it as literature, neutrally.

## 9. Visual design

Keep the established identity so the teacher's series looks consistent:

- **Palette tokens:**
  - Light: Jerusalem-stone background `#f2ece0`, surface `#fbf8f1`, ink `#1c2a23`, deep green `#1f5540`, stage `#163a2d`, gold `#a87a26`, glow `#e2b85a`.
  - Level colours: A2 green, B1 amber, B2 brick.
  - Provide a full dark theme: `prefers-color-scheme` + `[data-theme]` overrides, with all colours as tokens.
  - Optionally shift the accent hue to suit a new text (e.g. a sea-blue for a coastal story), but keep the structure.
- **Fonts:** `Amiri` for Arabic; `Alegreya` (display) and `Alegreya Sans` (body) for Turkish, since all three support Turkish characters. Always give fallback stacks.
- Arabic sizes are large (projected in class): word ≈ 60–74px, source unit ≈ 26–36px, examples ≈ 21–22px. Use `line-height` 1.8–1.9 for harakat.
- Set `dir="rtl" lang="ar"` on every Arabic element and `lang="tr"` on the document.
- **Mobile at 390px:** no horizontal scroll, the stage stacks above the panel, form grids collapse to one column, and keyboard hints are hidden.
- Keep a visible focus outline. All controls must be buttons or links.
- Animations: one orchestrated moment per step (root drop-in, staggered forms, text lines rising in); nothing gratuitous.

## 10. Build process

1. Read the text and split it into units; write or check the Turkish translation per unit.
2. For each target word, research and draft the card (§5), then run the accuracy checks (§8).
3. Pick an `mg` per word (§6). If none fits, add a new entry to the `MG` object in `assets/template.html` (and to `MG_KEYS` in `scripts/build.py`). This changes the skill itself, so it belongs in a pull request to the skill's repository, not in a lesson.
4. Build:
   ```bash
   python3 $SKILL_DIR/scripts/build.py lessons/<slug>/<slug>.json lessons/<slug>/<Name>-Ders.html
   ```
   It refuses to build with missing fields, unknown `mg` keys, or a verse without `<mark>`.
5. QA:
   ```bash
   node $SKILL_DIR/scripts/check.js lessons/<slug>/<Name>-Ders.html lessons/<slug>/qa
   ```
   It reports console errors and horizontal overflow, and saves screenshots: the text view, word 1, the Kök step in dark mode, Pratik, and the Örnekler step at 390px. Look at the screenshots. Also check by eye that:
   - the root highlighting is correct on every card;
   - every marked word in the text view opens the right card.
6. Deliver the `.html` file plus a short note listing:
   - what you assumed;
   - any corrections you made to the teacher's input (attribution, spelling, harakat);
   - anything you couldn't verify.

## 11. Things that don't work and should not be added

- A Print / PDF button: it doesn't work in sandboxed viewers. If the teacher wants a handout, generate a separate print-friendly page.
- Audio autoplay: if you add pronunciation audio, it must start from a button.
- External images or iframes (e.g. a YouTube embed of a cartoon): link out instead, or draw a simple SVG.
