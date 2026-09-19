---
description: Close a step — verify every topic, then open the pull request
argument-hint: "[step number, e.g. 1.2]"
---

Load the `tutor` skill, then close step $ARGUMENTS.

1. Verify **every** topic in the step is ticked in `CURRICULUM.md`. If any is not,
   list what remains and stop — a step is not finished early.
2. Run every file in `exercises/`. All must pass. Re-measure anything the briefs
   gave a complexity requirement for.
3. Confirm the step directory holds a reference card per topic.
5. Rebase the branch on `main`, push, and open the pull request. Body: what the
   step covered, one line per topic on what it exercised, and anything left
   deliberately undone.
6. Merge it with a merge commit and delete the branch, so one bubble marks the
   step.

Then say which step is next. Do not start it.
