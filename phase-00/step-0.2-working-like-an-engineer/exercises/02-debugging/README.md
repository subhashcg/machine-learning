# Exercises — Topic 2, debugging

One exercise. `pipeline.py` has **four bugs**; `test_pipeline.py` describes what
it should do, and four tests fail.

```
pipeline.py          the broken module
test_pipeline.py     the spec — do NOT change it
DIAGNOSIS.md         what you found, and how
```

```bash
cd phase-00/step-0.2-working-like-an-engineer/exercises/02-debugging
uv run pytest . -q          # see the four failures
uv run pytest . -x -l       # first failure, with locals
uv run pytest . --pdb       # stop at the failure and look around
```

## The actual exercise is DIAGNOSIS.md

The fixes are one line each. **Writing down how you found them is the point** —
for each failure, record the symptom, the deepest frame that is yours, which
tool told you, the cause, and the fix.

Diagnose first, fix second. If you fix before you can explain, you have guessed,
and the next bug of that shape will cost you the same hour again.

## What makes these realistic

None is a typo. All four produce plausible behaviour until you look closely, and
two of them pass their *other* tests perfectly — the function is right for the
input the other tests happen to use.

Three are shapes you have already met in Step 0.1. Recognising them is the skill
this topic is building.

## Constraints

- Do not change `test_pipeline.py`
- Do not rewrite `pipeline.py` — find the minimal change per bug
- Run `uv run pytest . -q` afterwards; all nine must pass

## Finally

The last section of `DIAGNOSIS.md` asks which tool actually found each bug, and
whether a different one would have been faster. Answer it honestly — that
reflection is worth more than the four fixes.
