# Scene types

A storyboard is a list of scenes. Each scene has a `type`, the fields that type needs, and these common fields:

| Field | Meaning |
|---|---|
| `say` | What the teacher says during this scene in the **long** cut (Turkish; Arabic quotes allowed). It also sets the scene's length (§ Timing). |
| `short` | Length in seconds of this scene in the **short** cut. Leave it out to drop the scene from the short cut. |
| `say_short` | What she says in the short cut. Leave it out for "music only". |
| `k` | Optional, short cut only: how much to speed up the scene's own choreography (0.45–1). By default it's derived from `short`. |
| `dur` | Optional: a minimum length in seconds for the long cut. Use it only to give a scene extra breathing room. |
| `note` | Optional: a delivery note for the voice-over sheet ("enerjik", "yavaş ve vakur"). |
| `from_card` | Step scenes, `zoom` and `verse`: the 1-based card number in the lesson. Missing fields are filled from that card. Any field you write yourself wins. |

Text fields accept simple markup: `<b>…</b>` (gold bold in captions), `<br>`, `<mark>` (the target word in a verse), and `<span class="rl">…</span>` (root letters in gold). Write `&amp;` for "&".

## Story scenes

| Type | Fields | Min. length | What it shows |
|---|---|---|---|
| `hook` | `eyebrow`, `line1`, `line2`, `glyph` (default `؟`) | 4.6 s | Big two-line question with rotating light rays. |
| `motto` | `eyebrow`, `items`: 1–3 × `{ar, tr}` | 6.0 s | Arabic words pop in one by one (at +0.5, +1.8 and +3.1 s), each with its Turkish meaning; the last one is gold. |
| `verse` | `eyebrow`, `before`: ≤ 2 Arabic context lines, `line` (Arabic with one `<mark>`), `tr`, `after`: ≤ 1 line, `caption` | 6.4 s | Text lines fade back; the target line pops forward as a card (+2.4 s) with its translation. |
| `zoom` | `word`, `q1`, `q2`, `caption` | 4.4 s | The word huge under a magnifier, plus two lines of question. |
| `literary` | `eyebrow`, `title`, `art`, `line`, `big`, `caption` | 5.4 s | A drawing, one explanatory line and one big gold term (e.g. *istiare*). |
| `punch` | `q`, `a` | 3.0 s | A question, then a big gold answer (+1.1 s). |
| `quiz` | `eyebrow`, `title`, `before`, `answer`, `after`, `options`: 4 Arabic choices including `answer`, `caption` | 6.0 s | Fill-in-the-blank card; a finger taps the right option (+2.6 s), which turns green (+3 s). |
| `statement` | `strike` (crossed-out phrase, optional), `line1`, `line2`, `caption` | 4.6 s | Two big lines, the second in gold. |
| `cta` | `motto`, `title`, `sub`, `button` | 6.4 s | Motto, invitation, a pulsing DM button and the handle (+2.5 s). Always last. |

## Step scenes (the "lens" on the word)

Step scenes are numbered automatically, 1…n, with progress dots, in storyboard order. Each has a `title`. With `from_card`, the rest is filled from the lesson card:

| Type | Filled from the card | Fields you can set yourself | Min. length |
|---|---|---|---|
| `root` | `letters` (from `sarfNote`'s *Kök*), `forms` (first `sarf` row) | `caption` | 6.2 s |
| `harf` | `chips`, `example` (first `harf.ex`) | | 4.2 s |
| `syn` | `syn`, `ant` (first two of each) | `caption` (e.g. "cimri, az ↔ cömert, bol") | 4.0 s |
| `context` | `mecaz` (the `mecaz` extra) | `rows`: 2 × `{tr, ar}` short pairs, e.g. `insan → cimri` / `رَجُلٌ شَحِيحٌ` (**write these yourself; they aren't in the card**) | 4.8 s |
| `press` | `ar`, `tr` (the `basın` extra) | | 4.2 s |
| `ayah` | `ar`, `tr`, `src` (the `ayet` extra or first `ayat`) | | 4.8 s |

Keep only the steps the lesson really has. A word without a preposition gets no `harf` step, and if there's no ayah, there's no `ayah` step. Don't invent content to fill a step.

## `art` for the literary scene

`art` is the inside of an `<svg viewBox="0 0 240 180">`, drawn in gold. It uses the same drawing classes (`s`, `f`, `soft`, `lbl`) and motion keyframes (`mgFloat`, `mgPulse`, `mgGrow`, …) as the lesson page's word animations. So you can paste a lesson card's custom `mgSvg` here. Put any custom `@keyframes` it needs in the storyboard's top-level `css`. Without `art` you get a stone with a flickering light. The full drawing rules are in the lesson skill's `references/motion-graphics.md`; in short: gold only via classes, ≤ 10 shapes, a 2.4–3.6 s loop.

## Timing

- **Long cut:** each scene lasts `max(minimum length, dur, words in say ÷ 2.6 + 0.9 s)`. So a longer narration automatically gets a longer scene. `compose.py` prints a note when a scene's narration is tight.
- **Short cut:** each kept scene lasts exactly `short` seconds, and its choreography is sped up by `k`. Keep the short cut around 30 s: hook 2.8, motto 3.8, verse 4, zoom 2.6, each step 1.8–3, cta 3.4.
- The last scene never fades out.

## Layout (1080 × 1920)

Everything important sits between y ≈ 280 and y ≈ 1500. Instagram's own interface covers the top ~250 px (profile, progress bar), the bottom ~400 px (caption, reply box) and the right edge low down (like and comment buttons). The handle sits at the top of every frame and big on the `cta` scene.
