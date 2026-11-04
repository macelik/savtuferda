# Skill trials

Test input: `irade-el-hayat.request.md` (Ebu'l-Kasım eş-Şabbi, «إرادة الحياة»: 8 hemistichs, 9 targets incl. a conditional, translation left empty). Model under test: Haiku. Prompt: "follow SKILL.md exactly", nothing else.

| Check | v1 | v2 | v3 (parse-only check) |
|---|---|---|---|
| Builds, QA OK | ✓ | ✓ | n/a |
| Roots / bab / masdar on cards | ✓ | ✓ | ✗ يستجيب parsed as س-ج-ب → rule added |
| Line 5 «لَمْ يُعَانِقْهُ شَوْقُ الحَيَاةِ» (object pronoun, VOS order) | ✗ | ✓ | ✓ |
| Line 7 «لَمْ تَشُقْهُ الحَيَاةُ» (hollow vs doubled root) | ✗ | ✗ | ✓ |
| Poetic licence not reported as an error | ✗ | ✓ | ✓ |
| Motion graphic fits the meaning | ✗ (flame for "break") | ✓ | n/a |
| Transliteration | ✗ | ~ (one dropped vowel) | n/a |
| Quran citations exact | ✓ | ✓ | n/a |
| Idiomatic `basın` examples | ~ | ✓ | n/a |

What changed between versions (see git log):
- v1→v2: translate-first parsing procedure and traps, poetic-licence rule, transliteration scheme, meaning of `levels`, idiom rules, mg "would a student guess it" test + new keys (break/embrace/vanish) + per-lesson captions (`mgText`), self-review checklist. Skill examples were kept free of the test poem, to avoid leaking answers.
- v2→v3: mandatory `parse` entry per unit; explicit doubled-vs-hollow jussive test; strip pattern letters before naming the root; one-word labels for `shart`.

The v2 output, with the two remaining slips fixed by hand (line 7 translation, *wa-ndaṯar*), is kept as `examples/irade-el-hayat.json`.

When you change the skill, re-run this trial with a fresh Haiku agent and add a column here. Never put lines from the test poem into SKILL.md.
