# Step 0.1 — The language

`~18 hrs` · Phase 0, *Python that holds up*

> Stop fighting the language. Everything after this assumes you can write,
> structure and test Python without thinking about it.

## The eight topics

| | File | Covers |
|---|---|---|
| 1 | `01_data_structures.py` | list, dict, set, tuple: what each costs and when to reach for it |
| 2 | `02_comprehensions.py` | comprehensions, generators, `yield`, iterators, lazy evaluation |
| 3 | `03_functions.py` | `*args`/`**kwargs`, closures, scope, the mutable-default trap |
| 4 | `04_classes.py` | `__init__`, dunder methods, `@property`, `@dataclass` |
| 5 | `05_modules.py` | imports, packages, `__main__`, project layout |
| 6 | `06_exceptions.py` | try/except/finally, custom exceptions, failing usefully |
| 7 | `07_files.py` | context managers, `pathlib`, csv, json |
| 8 | `08_type_hints.py` | what they buy you and what they don't |

Files appear one at a time — finish a topic before the next is written, so the
examples build on what you've already got working.

## How each file works

```bash
uv run phase-00/step-0.1-the-language/01_data_structures.py
```

Each file has two halves:

- **Demos** — runnable code that prints. Read it, run it, then *change it* and
  run it again. The printed output is the point; predicting it before you run is
  the exercise nobody assigns but everybody needs.
- **Exercises** — functions raising `NotImplementedError`. Fill them in and re-run;
  the checks at the bottom report `✓` / `✗` per exercise.

The file is meant to be edited. Break things in it deliberately.

## Done when

- All eight files run with every exercise passing
- `NOTES.md` has something real in it for each topic
- You could explain any item on the Step 0.1 checklist without looking it up

Then merge back to `main`:

```bash
git switch main
git merge --no-ff step/0.1-the-language
```
