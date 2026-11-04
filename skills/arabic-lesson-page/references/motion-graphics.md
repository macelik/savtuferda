# Motion graphics: how the word animations work and how to make new ones

Each word slide has a small looping animation on the dark green "stage". It **shows what the word means**: a chain snapping for «اِنْكَسَرَ», steam rising for «تَبَخَّرَ». Students remember the picture before they remember the definition. That makes it the most important visual on the slide, so it must be clear rather than clever.

## 1. Which technology, and when

Use the simplest level that can show the idea.

| Level | Technology | Use it for | Where it lives |
|---|---|---|---|
| **1 (default)** | Inline **SVG + CSS keyframes** | Almost everything: things that move, grow, fade, turn, open, break or travel along a path | A built-in key (`"mg": "rise"`), or a **custom animation in the lesson JSON** (`"mg": "custom"`, §5) |
| 2 | SVG + a little **JavaScript** (`requestAnimationFrame`) | Real physics, randomness, or something that reacts to clicks | Template change only (§7) |
| 3 | **Canvas 2D** | Many moving particles (more than ~30 elements: rain, sand, a crowd) | Template change only (§7) |
| 4 | **three.js** (WebGL) | A genuinely 3D idea that 2D can't fake (a globe turning with the right continents) | Template change only, and rarely worth it (§7) |

Lesson JSON may only contain **Level 1**. `build.py` rejects scripts, event handlers and external URLs in lesson data. This keeps every lesson a safe, self-contained file the teacher can open offline. Faking 3D in 2D usually works better anyway: squeeze something with `scaleX` and it reads as "turning", as the door example below shows.

## 2. The drawing canvas

- Every animation is the inside of one `<svg viewBox="0 0 240 180">`. The page supplies the `<svg>` element; you write only what goes inside it.
- Centre (120, 90). Use y = 150 as the "ground" if you need one, and y = 170–176 for a caption at the bottom (or y ≈ 24 at the top). Keep shapes inside x 15–225 and y 15–170.
- **Colours: only `currentColor`, through the classes below** (it is gold on the stage in both themes). Never use hex colours. The one exception is an opaque shape that must cover something; use `style="fill:var(--stage)"` for it (the stage background colour).

| Class | Draws |
|---|---|
| `s` | gold stroke, 3 px, round ends, no fill. Use `stroke-width="4"`/`"5"` to emphasise. |
| `soft` | add to `s` for a faded (35%) helper line: ground, orbit, frame |
| `f` | gold fill |
| `lbl` | small Turkish caption text (12 px). For Arabic text use plain `<text>` (Amiri, 20 px). |

- **Simplicity budget: at most ~10 shapes**, with no long hand-drawn path data. Use circles, rects, lines and a few `Q`/`C` curves. A silhouette made of 3 shapes beats a detailed drawing.
- **Masks without masks.** To make something rise from behind the horizon or come out of a box, draw it first, then cover the hidden area with a rectangle filled `var(--stage)` and draw the edge line on top. The rectangle hides whatever is below it.
- **Never mix Arabic and Latin in one `<text>`.** The letter order breaks; use two `<text>` elements.

## 3. The motion kit

The template already defines these keyframes. Apply one with an inline style: `style="animation:mgPulse 2.4s ease-in-out infinite"`.

| Keyframes | Effect | Typical use | Notes |
|---|---|---|---|
| `mgFloat` | rise 110 px and fade out | dots/steam going up | stagger 3 copies with delays (0, .8s, 1.6s) |
| `mgDraw` | draw a line, hold, fade | paths, trajectories, rise-and-fall curves | needs `style="--len:300;stroke-dasharray:300;…"` (≈ the path length) |
| `mgPulse` | gently grow and shrink | a glowing centre, a heart, a sun | `transform-origin:center` |
| `mgRing` | ring expands and fades | sound, light, impact | stagger 2–3 rings |
| `mgGrow` | scale up from 0 in height, hold | plants, buildings, rising bars | `transform-origin:50% 100%` (grow from the bottom) |
| `mgSpin` | full turn | rays, wheels, orbits | slow: 6–18 s, `linear` |
| `mgFlick` | irregular flicker | weak light, a candle | |
| `mgFlame` | flame breathing | fire, anger | `transform-origin:50% 100%` |
| `mgBlink` | close, then open wide | an eye | |
| `mgAim` / `mgHit` | turn to aim, fly / target flash | aiming, directing | pair them |
| `mgScan` / `mgPick` | slide across / light up when chosen | choosing, meaning | |
| `mgBubble` | pop in, hold, vanish | thoughts, ideas, speech | stagger the delays |
| `mgTravel` | move along a path | anything that travels | needs `offset-path:path('M… L…')` on the moving element |
| `mgFlap` | wings beat | birds | |
| `mgSnapL` / `mgSnapR` | two halves break apart | breaking | origins at the break point |
| `mgHugL` / `mgHugR` | two arms close in | embracing, holding | |
| `mgSpark` | particle flies up and out | sparks, shards | set `--dx` per particle (e.g. `--dx:-20px`) |

**Pivot points (the most common bug).** Every shape inside `.mg` has `transform-box: fill-box`, so `transform-origin` is measured from **the shape's own box**:
- `transform-origin:center` scales or turns a shape around its own middle;
- `transform-origin:50% 100%` grows from its bottom edge;
- `transform-origin:0% 50%` hinges on its left edge (a door).

To rotate around a fixed point **in the drawing** (an orbit around 120, 90), set `transform-box:view-box;transform-origin:120px 90px` on that element.

**Timing.**
- One loop should last 2.4–3.6 s, and every animated element in one graphic should use the **same duration**, so the loop stays in sync.
- **Hold the meaningful state for about 30–40% of the loop**; students need time to see the result. A good shape for the cycle: start (0–15%) → change (15–45%) → hold (45–85%) → reset (85–100%).
- Use `ease-in-out`; use `linear` only for constant spinning.

## 4. From a description to an animation

When the teacher or user describes what they want ("a door opens and light comes out"), or no built-in key passes the test "would a student guess the word from this?", follow these steps:

1. **Find the one change.** What is different between the start and the end? (Closed door → open door with light.) If you can't say it in one sentence, the idea is too complicated; simplify it.
2. **Pick the actors.** One main subject, plus at most one or two context shapes (a frame, the ground, a target).
3. **Choose 1–2 motions** from the kit. If none fits, write your own `@keyframes` in `meta.css` (§5).
4. **Make the rest state meaningful.** Users who turn off motion (the `prefers-reduced-motion` setting) and the first frame of the page see the shapes **without** animation. So set each shape's own inline `transform`/`opacity` to the **meaningful end state** (door open, light visible). Let the keyframes start from the "before" state. Never leave the key shape at `opacity:0` at rest.
5. **Add a caption** of 1–4 Turkish words through `{{cap}}` and `"mgText": {"cap": "…"}`. The caption names the image, not the dictionary meaning.
6. **Build, then look:**
   - `check.js` saves two moments of every card's animation to `<qa>/anim/cardNN-a.png` and `-b.png`, plus the **rest state** to `cardNN-rest.png` (motion off). Read all three.
   - Ask yourself: are the two moments clearly different? Is anything cut off at the edges?
   - Does `-rest` show **only** the meaningful end state? If before- and after-shapes appear together (moon *and* sun, closed *and* open), an element is missing its inline end-state `opacity`/`transform`.
   - Fix what's wrong and rebuild.

## 5. Custom animation in a lesson (`"mg": "custom"`)

A card can bring its own SVG; the lesson can bring its own keyframes. No template change is needed.

```json
"mg": "custom",
"mgText": { "cap": "kapı açılır" },
"mgSvg": "<path d=\"M81 150 L159 150 L214 176 L26 176 Z\" class=\"f\" style=\"opacity:.3;animation:c-door-floor 3.2s ease-in-out infinite\"/><rect x=\"81\" y=\"41\" width=\"78\" height=\"109\" class=\"f\" style=\"opacity:.9;animation:c-door-light 3.2s ease-in-out infinite\"/><g style=\"transform-origin:0% 50%;transform:scaleX(.14);animation:c-door-swing 3.2s ease-in-out infinite\"><rect x=\"81\" y=\"41\" width=\"78\" height=\"109\" class=\"s\" style=\"fill:var(--stage)\"/><circle cx=\"148\" cy=\"98\" r=\"4\" class=\"f\"/></g><rect x=\"78\" y=\"38\" width=\"84\" height=\"113\" rx=\"3\" class=\"s\"/><text x=\"120\" y=\"24\" text-anchor=\"middle\" class=\"lbl\">{{cap}}</text>"
```

and in `meta`:

```json
"css": "@keyframes c-door-swing{0%,15%{transform:scaleX(1)}45%,85%{transform:scaleX(.14)}100%{transform:scaleX(1)}}@keyframes c-door-light{0%,15%{opacity:0}45%,85%{opacity:.9}100%{opacity:0}}@keyframes c-door-floor{0%,20%{opacity:0}50%,85%{opacity:.3}100%{opacity:0}}"
```

What this example shows:
- **Painter's order.** Later shapes draw on top: first the floor beam, then the light in the doorway, then the door leaf (an opaque `var(--stage)` fill hides the light while the door is closed), and the frame last.
- **Fake 3D.** The door "swings open" by squeezing (`scaleX(.14)`) around its hinge (`transform-origin:0% 50%`).
- **Meaningful rest state.** Inline `transform:scaleX(.14)` and `opacity:.9` mean the door stands open with light when motion is off.
- **One shared 3.2 s loop**, with the open state held from 45% to 85%.

Rules for custom animations:
- `mgSvg` is the **inside** of the SVG only. The page adds `<svg class="mg" viewBox="0 0 240 180">`.
- Name your keyframes `c-<thing>-<motion>` so they can't clash with the template's `mg*` keyframes. Put them all in `meta.css` (one string for the whole lesson).
- `{{cap}}`, `{{a}}`, `{{b}}` placeholders are filled from `mgText`.
- `build.py` rejects any of these:
  - `<script>`, `<foreignObject>`, `<image>` or `<iframe>`;
  - `on…=` event handlers;
  - `javascript:`;
  - external URLs;
  - `@import`;
  - an `mgSvg` over 6000 characters.

  If you hit the size limit, the drawing is too detailed.
- More tested examples: cards 4 (sunrise over the horizon, stars fading) and 9 (a hand slaps, a burst on impact) in `examples/irade-el-hayat.json`.
- Prefer a built-in key when one fits. Custom animations are for ideas the kit doesn't cover, or when the teacher asks for a specific picture.

## 6. Page-level motion (not per word)

The template also animates the page itself, the same for every lesson:
- root-letter tiles drop in one by one (`drop`);
- mazi/muzari/masdar cards rise in, staggered (`rise`);
- each step's box slides up on change (`boxIn`);
- text lines rise in on load (`lineIn`);
- the marked word glows once (`markGlow`).

These are part of the design, so don't change them for a single lesson. Everything stops under `prefers-reduced-motion`.

## 7. Going beyond CSS (a change to the skill, not to a lesson)

If an idea truly needs Level 2–4, it becomes a new **built-in key** for every lesson. That's a change to the skill's repository, not something to do inside one lesson:

1. Add the drawing to `MG` and default captions to `MGT` in `assets/template.html`, and the key to `MG_KEYS` in `scripts/build.py`. Add a row to the table in `SKILL.md`.
2. **JavaScript:** start the animation only when the card is on screen, stop it when the slide changes, and do nothing under `matchMedia('(prefers-reduced-motion: reduce)')`. Draw the meaningful rest state first, so the picture is right even if the script never runs.
3. **Canvas:** size it to the same 4:3 box and paint with the computed `color` of `.mg`, so it follows the theme.
4. **three.js:** load one pinned build from cdnjs (e.g. `https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js`). It adds about 600 KB and a network dependency, so the lesson no longer opens fully offline. Keep an SVG fallback for when it fails to load. Ask first whether a 2D trick (`scaleX` squeeze, `mgSpin`, an orbit) would do; it almost always does.
5. Rebuild both examples, run `check.js`, and look at the `anim/` screenshots.
