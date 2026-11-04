# Developing the lesson-promo-video skill

This repo is the `lesson-promo-video` skill package. To **use** it, see the README. This file is for agents changing the skill itself.

The client is an Arabic teacher (Instagram **@savtuferda**). She teaches **Turkish-speaking** learners at A2–B2. Everything viewers see is in Turkish, with Arabic fully vowelled. Code, comments and docs are in English. The lesson pages come from the separate `arabic-lesson-page` skill; this skill only reads them.

## Layout rules

- The skill is self-contained under `skills/lesson-promo-video/`. Scripts find their files relative to their own location, and work files go to `videos/<slug>/` in the **user's working directory**. Nothing may assume this repo is the working directory.
- `SKILL.md` frontmatter: `name` matches the folder name; `description` is under 1024 characters.
- Big binaries (MP4s) stay in `showcase/`, never inside the skill folder; installing the skill copies that folder.

## Changing scenes

- The look lives in `assets/scene-kit.html`. Each scene type is a renderer function `r_<type>` in `scripts/compose.py`, with its minimum length in `MIN_DUR`, required fields in `REQUIRED`, its voice-over description in `SCREEN`, and optional cue points in `CUES`.
- New scene type: add all five, document it in `references/scene-types.md`, and add it to the mapping table in `SKILL.md`.
- Element entrances use `--r` (seconds after the scene starts) so the short cut can compress them with `--k`. Keep a scene's last entrance before its minimum length.
- After any change, compose the example and compare stills with `showcase/`:
  ```bash
  python3 skills/lesson-promo-video/scripts/compose.py skills/lesson-promo-video/examples/sahih/storyboard.json /tmp/pv
  ```
  ```bash
  node skills/lesson-promo-video/scripts/stills.js /tmp/pv full
  ```
  Look at every still.

## Accuracy

Arabic on screen is copied from the lesson or the teacher's script, never retyped from memory. Citations come only from the lesson's checked cards. Keep the teacher's words; shorten if needed, but don't rewrite her message or invent claims about her classes.
