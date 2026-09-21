# Step 0.2 — Working like an engineer

Phase 0, *Python that holds up*

> Step 0.1 was the language. This is everything around it: proving code works,
> finding out why it doesn't, and keeping the environment reproducible.

*git and readable code were dropped from this step: git was already familiar,
and readable code is taught continuously through review rather than as a topic
of its own.*

## Topics

| | Topic | Covers |
|---|---|---|
| 1 | pytest | test functions, fixtures, `parametrize`, and what's worth testing |
| 2 | Debugging | reading a traceback properly, `breakpoint()`, stepping through code |
| 3 | Environments | `uv`, virtual environments, `pyproject.toml`, pinned dependencies |

## How we work a topic

1. I teach the topic, grounded in code you can see run.
2. Questions, to check what landed.
3. A reference card and an exercise brief, written after the questions so they
   cover what actually needed covering.
4. You implement. Each exercise file ends with checks written for you — run the
   file and it tells you where you stand.
5. I review what the checks can't see: naming, docstrings, whether it's
   idiomatic rather than merely correct.
6. You commit.

The session transcript disappears; `reference/NN-topic.md` does not.

## Layout

```
README.md                          this file
reference/NN-topic.md              lookup cards: syntax, costs, gotchas
exercises/NN-topic/README.md       the brief for that topic
exercises/NN-topic/*.py            the code you wrote, checks at the bottom
```

## Done when

- Every topic has code you wrote, passing its checks
- You could explain any item on the checklist without looking it up
- The code runs from a clean checkout

Then:

```bash
gh pr create --base main --title "Step 0.2 — Working like an engineer"
gh pr merge --merge --delete-branch
```
