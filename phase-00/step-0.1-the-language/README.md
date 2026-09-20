# Step 0.1 — The language

Phase 0, *Python that holds up*

> Stop fighting the language. Everything after this assumes you can write,
> structure and test Python without thinking about it.

## Topics

| | Topic | Covers |
|---|---|---|
| 1 | Data structures | list, dict, set, tuple: what each costs and when to reach for it |
| 2 | Comprehensions and generators | comprehensions, `yield`, iterators, lazy evaluation |
| 3 | Functions | `*args`/`**kwargs`, closures, scope, the mutable-default trap |
| 4 | Classes | `__init__`, dunder methods, `@property`, `@dataclass` |
| 5 | Modules and packages | imports, packages, `__main__`, project layout |
| 6 | Exceptions | try/except/finally, custom exceptions, failing usefully |
| 7 | Files and formats | context managers, `pathlib`, csv, json |
| 8 | Type hints | what they buy you and what they don't |

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

The session transcript disappears; `reference/NN-topic.md` does not. It is the
durable record of what was discussed.

## Done when

- Every topic has code you wrote, passing its checks
- You can explain any item on the checklist without looking it up
- The code runs from a clean checkout

Then:

```bash
git switch main
git merge --no-ff step/0.1-the-language
```

## Layout

```
README.md                          this file
reference/NN-topic.md              lookup cards: syntax, costs, gotchas
exercises/NN-topic/README.md       the brief for that topic
exercises/NN-topic/*.py            the code you wrote, checks at the bottom
```
