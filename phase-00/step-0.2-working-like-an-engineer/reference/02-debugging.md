# Reference — debugging

Lookup card.

## Reading a traceback

**"Most recent call last"** — read bottom-up. The last frame is where it blew
up; each frame above is who called it.

```
File "deep.py",       line 10, in <module>       your code
File "deep.py",       line  7, in get_limits     your code
File "deep.py",       line  4, in load_settings  <- DEEPEST FRAME THAT IS YOURS
File "<stdlib>/json", line 346, in loads
File "<stdlib>/json", line 337, in decode
File "<stdlib>/json", line 353, in raw_decode
JSONDecodeError: Expecting property name enclosed in double quotes
```

**Start at the deepest frame that is yours.** The library frames tell you *what*
went wrong; your deepest frame tells you *where you caused it*. `json/decoder.py`
is correct code doing its job — there is no bug there to find.

If that frame looks innocent, keep walking up: the frames above are the chain of
who-passed-what, and you are tracing a wrong value back to where it entered.

A traceback with **no frames of yours at all** usually means a real library bug
or a version mismatch — a different investigation.

### The `^^^^` markers (3.11+)

```
return cfg["limits"]["threshold"]
       ~~~~~~~~~~~~~^^^^^^^^^^^^^
```

Names the exact sub-expression. Here `cfg["limits"]` succeeded and
`["threshold"]` failed — on a line with four chained calls, that is the
difference between knowing and guessing.

### Chained tracebacks — two halves

```
JSONDecodeError: Expecting property name ...

The above exception was the direct cause of the following exception:

ConfigError: config file is not valid JSON
```

The **first** traceback is the cause; the **second** is what you were told. The
wording says which kind of chaining happened (Topic 6):

- *"the direct cause of"* — someone wrote `raise X from e` deliberately
- *"During handling of ... another exception occurred"* — a second exception
  inside an `except` block, often a bug in the handler itself

---

## pdb

```python
breakpoint()        # stdlib since 3.7, no import needed
```

```bash
python -m pdb script.py      # start under the debugger
pytest --pdb                 # open at the moment a test fails
```

| | |
|---|---|
| `l` | list source around here (`ll` for the whole function) |
| `p expr` / `pp expr` | print / pretty-print any expression |
| `n` | next line — step **over** calls |
| `s` | step **into** a call |
| `r` | run to the **return** of this function |
| `unt` | run **until** the line number increases — escapes a loop body |
| `c` | continue to the next breakpoint |
| `w` | where — the full stack |
| `u` / `d` | move **up** / **down** a frame |
| `b 42, cond` | conditional breakpoint |
| `q` | quit |

**`n` vs `s`:** picking `n` wrongly steps *over* the line the bug was in — you
get a wrong result with no idea which part produced it, and must restart.
Picking `s` wrongly drops you into library code — annoying, but `r` pops you
straight back out. **`s` is recoverable; `n` is not.** When unsure, `s`.

**`u` / `d` are the commands people miss.** The bug is often not in the frame you
landed in; walking up shows the caller's locals without re-running anything.

Any Python works at the prompt — `p [v*t for v in values]` tests a fix before you
write it. If a local shares a name with a command (`l`, `n`, `c`, `s`), use
`p l`.

---

## pytest --pdb

```
> app.py(7)get_threshold()
-> return cfg["limits"]["threshold"]
(Pdb) p cfg
{'limits': {'max': 10}}
(Pdb) u
> app.py(10)scale_all()
(Pdb) p values
[1, 2, 3]
```

Opens **at the moment of failure**, inside the function, with every local alive.
No re-running, no added prints.

**The loop: failing test → `--pdb` → inspect → fix.**

### The limit

Post-mortem lands where the exception was *raised*. An `assert` raises in the
**test** frame, so the function has already returned and its locals are gone:

```
(Pdb) p values
*** NameError: name 'values' is not defined
```

Three fixes, cheapest first:

- **`u`** — the frames above are still alive; often that is enough
- **`pytest -l`** (`--showlocals`) — prints every local in every frame, no
  debugger at all
- **name the intermediate**: `result = run(...)` then `assert result == ...`, so
  the value is a local in the test frame

---

## Finding one bad row in 40,000

```python
if row["id"] == "bad-id":       # conditional breakpoint
    breakpoint()
```

But you usually do not know *which* row yet:

```python
for i, row in enumerate(rows):
    try:
        process(row)
    except Exception:
        print(i, row)
        raise                   # bare raise — keeps the original traceback
```

Or in a live session: `b 42, row["id"] == "bad-id"`.

When nothing raises and the *value* is merely wrong, none of that helps —
**bisect**. Check the halfway point, see which half is already wrong, halve
again. Twelve checks find one bad row in 40,000. Same idea as `git bisect`.

---

## Faster loops

```bash
pytest --lf -x        # re-run only last-failed, stop at the first
pytest -l             # show locals on failure
pytest -k 'name'      # only matching tests
```

```python
def test_output(capsys):
    main()
    assert "done" in capsys.readouterr().out     # assert on print, don't squint
```

---

## print vs pdb

**print wins** when you want a *pattern over time* (a loop where a value drifts
wrong, a loss that is fine at step 1 and NaN by step 400), when the code cannot
pause (a request handler, CI, a remote machine), when you want a record to diff
across runs, and when one print answers it.

**pdb wins** when you want to interrogate *one moment*: many variables, questions
you did not anticipate, and trying a fix before writing it.

The real argument against print is not that it is primitive — it is that **each
print is a guess about what you will need**, and changing the guess costs a
re-run.

In anything long-lived, `logging` replaces print: levels you can filter,
timestamps, and turning detail up without editing code.
