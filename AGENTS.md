# Developing the savtuferda skills

This repo *is* the skill package. To **use** the skill, see the README. This file is for agents changing the skill itself.

The client is an Arabic teacher (Instagram **@savtuferda**). She teaches **Turkish-speaking** learners at A2–B2. Everything students see is in Turkish, with Arabic content fully vowelled. Code, comments and docs are in English.

## Layout rules

- Each skill is self-contained under `skills/<name>/`. Scripts must find their files relative to their own location (`Path(__file__)`), and they read and write lesson files in the **user's working directory**. Nothing may assume this repo is the working directory, because the skill is installed into other projects and harnesses.
- `SKILL.md` frontmatter: `name` matches the folder name (lowercase, hyphens, 1–64 characters); `description` is under 1024 characters and says when to use the skill.
- Keep `SKILL.md` focused on what the agent must do. Background goes in `references/`, worked examples in `examples/`.

## Changing the lesson template

- `assets/template.html` is shared by every lesson. Change it only for features every lesson should get.
- New motion graphic: add it to `MG` (and a default caption to `MGT`) in the template, add the key to `MG_KEYS` in `scripts/build.py`, and add a row to the table in `SKILL.md`.
- Never hard-code one lesson's words in the template; per-lesson text goes in the JSON (`mgText`, `meta`).
- After a template change, rebuild both examples and run QA on them:
  ```bash
  python3 skills/arabic-lesson-page/scripts/build.py skills/arabic-lesson-page/examples/kudus-mahmud-dervis.json /tmp/k.html
  ```
  ```bash
  node skills/arabic-lesson-page/scripts/check.js /tmp/k.html /tmp/qa
  ```
  Look at the screenshots.

## Changing SKILL.md

- Re-run the trial in `skills/arabic-lesson-page/tests/`: give a **fresh, small model** (e.g. Haiku) only the request file and "follow SKILL.md exactly". Record the outcome as a new column in `tests/RESULTS.md`.
- **Never put lines or words from the test poem into SKILL.md.** Examples in the skill must come from other texts, or the trial stops measuring anything.

## Accuracy rules (also for examples and docs)

Verify authorship of texts (the first draft of the Kudüs lesson credited a Darwish poem to Tamim al-Barghouti). Arabic definitions use no Turkish or Persian loanwords. Quran and hadith citations must be exact. Report corrections; never silently "fix" the teacher's text.
