---
description: Start a step — branch from main and scaffold its directory
argument-hint: "[step number, e.g. 1.2]"
---

Load the `tutor` skill, then start step $ARGUMENTS.

1. Read that step from `CURRICULUM.md` — its title, its checklist items, the
   branch name given under it.
2. From `main` (pull first), create the branch exactly as the curriculum names it.
3. Create `phase-0N/step-N.M-slug/` containing:
   - `README.md` — the step goal, a numbered table of its topics, and the loop:
     discuss, exercises, review, notes, commit
   - `NOTES.md` — a heading per topic and nothing else. It is theirs to fill.
   - empty `reference/` and `exercises/` directories
4. Commit the scaffold and push the branch.

Scaffold only. Do not teach the first topic, do not write reference cards, do not
write exercises. End by naming topic 1 and waiting.
