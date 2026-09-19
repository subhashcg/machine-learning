---
description: Close a topic — verify the code and notes, tick the box, commit and push
argument-hint: "[topic name, or its number within the step]"
---

Load the `tutor` skill, then close topic $ARGUMENTS.

1. Run every exercise file for this topic. Test the edges the learner did not:
   empty input, single element, duplicates, inputs that break the preconditions.
2. Where a brief stated a complexity, **measure it** at increasing sizes and show
   whether the time scaled linearly or squared. Do not take the claim on trust.
3. Review beyond correctness — function not script, `__main__` guard,
   preconditions documented, plain types returned, naming, repeated work in loops.
4. Confirm `reference/NN-topic.md` exists and that anything from the discussion
   worth keeping is in it — the transcript will not survive.
5. Tick the topic's box in `CURRICULUM.md`.
6. Commit and push to the step branch. One commit, named for the topic.

Then name the next topic in the step. Do not start it.
