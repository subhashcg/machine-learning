# Step 0.1 — The language

`~18 hrs` · Phase 0, *Python that holds up*

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

1. We discuss the topic in the session — I ask what you expect to be true
   before I explain anything.
2. You get exercises. You write the file yourself, from scratch.
3. I run your code and review it — for idiom and cost, not just correctness.
4. You write up the topic in `NOTES.md`.
5. You commit.

The session transcript disappears; `NOTES.md` does not. It is the only durable
record of what was discussed, so it is part of the work, not an afterthought.

## Done when

- Every topic has code you wrote and notes you wrote
- You can explain any item on the checklist without looking it up
- The code runs from a clean checkout

Then:

```bash
git switch main
git merge --no-ff step/0.1-the-language
```
