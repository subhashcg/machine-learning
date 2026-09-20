# Diagnosis

One section per failing test. Fill these in **before** you fix anything —
writing the diagnosis is the exercise; the fix is usually one line.

For each, record:

- **Symptom** — the assertion that failed, and the actual vs expected values
- **Where** — the deepest frame that is yours, and the line
- **How you found it** — which tool told you, and what you inspected
- **Cause** — why the code does what it does, not just what to change
- **Fix** — the change you made

---

## 1. test_load_rows_handles_trailing_whitespace

**Symptom:**
`assert rows[0] == {"name": "widget", "qty": 3, "price": 9.99}` fails at
`test_pipeline.py:41`. pytest's diff narrows it to a single key:

```
Omitting 2 identical items
Differing items:
{'name': ' widget '} != {'name': 'widget'}
```

`qty` and `price` are correct. Only `name` carries the surrounding spaces.

**Where:**
`pipeline.py:11`, in `parse_row`:

```python
name, qty, price = line.split(",")
return {"name": name, "qty": int(qty), "price": float(price)}
```

`load_rows` is innocent — it only filters blank lines and the header, and hands
the line through unchanged.

**How you found it:**
pytest's assertion diff alone; no debugger needed. It reported that two of the
three items were identical and showed exactly which key differed, which points
straight at the one field that is stored without conversion.

Then one probe in the REPL to explain why only that field is affected:

```
>>> int(' 3 '), float(' 9.99 ')
(3, 9.99)
```

**Cause:**
`str.split(",")` splits on the comma and nothing else, so each piece keeps the
whitespace that sat around it: `' widget '`, `' 3 '`, `' 9.99 '`.

`int()` and `float()` strip leading and trailing whitespace themselves, so
`qty` and `price` come out right **by accident** — the conversion hides the
problem. `name` is the only field stored raw, so it is the only one that shows
it. This is why the other tests pass: `TEXT` has no spaces around its commas.

**Fix:**
Strip in `parse_row` — one line:

```python
name, qty, price = (part.strip() for part in line.split(","))
```

(Stripping just `name` would pass the test, but the whitespace is in every
field, and only the two numeric conversions are covering for it.)

---

## 2. test_apply_discount_does_not_mutate_input

**Symptom:**
`assert rows == before, "apply_discount must not modify the rows it was given"`
fails at `test_pipeline.py:59`:

```
At index 1 diff: {'name': 'gadget', 'qty': 12, 'price': 4.05}
              != {'name': 'gadget', 'qty': 12, 'price': 4.5}
```

The caller's own `rows` came back discounted. `before` was copied *before* the
call, so it holds the original 4.50.

Note which test does **not** fail: `test_apply_discount_reduces_qualifying_rows`
passes perfectly. The arithmetic is right; only the ownership is wrong.

**Where:**
`pipeline.py:40`, in `apply_discount`:

```python
if row["qty"] >= minimum_qty:
    row["price"] = row["price"] * (1 - percent / 100)
out.append(row)
```

**How you found it:**
The failure message named the field and the two values, so the question was not
*what* changed but *whose* dict changed. Confirmed with an identity check:

```
>>> out = apply_discount(r, 10, minimum_qty=1)
>>> out[0] is r[0]
True
```

`is`, not `==`. That one line settles it: the returned list holds the *same dict
objects* the caller passed in.

**Cause:**
Building a new list (`out = []`) looks like it makes a copy, but a list holds
references. `out.append(row)` puts the caller's dict into the new list, and
`row["price"] = ...` writes through that shared reference. The function returns
a new **list** wrapped around the **original dicts** — a shallow copy, when the
docstring promises the caller's rows are untouched.

Same shape as the Topic-5 binding exercise: rebinding a name is private,
mutating the object it points at is visible everywhere.

**Fix:**
Copy each row before touching it — one line, inside the loop:

```python
row = dict(row)
```

placed as the first statement of the loop body, so both branches append a copy.

---

## 3. test_summarise_returns_highest_first

**Symptom:**
`assert [r["name"] for r in top] == ["doohickey", "gadget"]` fails at
`test_pipeline.py:64`:

```
assert ['widget', 'gadget'] == ['doohickey', 'gadget']
At index 0 diff: 'widget' != 'doohickey'
```

Row values are widget 29.97, gadget 54.00, doohickey 100.00. The result is the
*lowest* two, and `gadget` appearing in both lists is a coincidence of a
three-row fixture — it is the middle value, so it survives either way.

**Where:**
`pipeline.py:49`, in `summarise`:

```python
ranked = sorted(rows, key=lambda r: r["qty"] * r["price"])
return ranked[:top]
```

**How you found it:**
Read off the failure directly: expected `doohickey` (100.00) first, got `widget`
(29.97) first — the extremes are swapped, so the ordering is reversed. Confirmed
by computing the three products by hand; no tool beyond the assertion diff.

The near-miss is worth noticing: with `top=2` the second element matches by luck.
Had the test asked for `top=1` this would have been obvious, and had it asked for
all three it would have been obvious too.

**Cause:**
`sorted()` is ascending by default, and the key is the plain product, so the
smallest total value lands first. The slice `[:top]` then takes the cheapest
rows. The key function is correct; only the direction is wrong. Nothing in the
code says "descending" anywhere — the docstring says "highest first" and the
implementation never honours it.

**Fix:**
Sort descending — one argument:

```python
ranked = sorted(rows, key=lambda r: r["qty"] * r["price"], reverse=True)
```

`reverse=True` is preferred over negating the key (`-r["qty"] * r["price"]`)
because it keeps the sort stable in the intended direction, and it still works
if the key ever becomes non-numeric.

---

## 4. test_running_totals_is_independent_of_call_order

**Symptom:**
`assert first == second, "calling it twice should give the same answer"` fails at
`test_pipeline.py:74`:

```
Right contains 3 more items, first extra item: 29.97
```

The first call returns 3 entries, the second returns 6 — the same three values
appended again. Note that `test_running_totals` **passes**, but only because it
runs earlier in the file, while the accumulator is still empty. Run this test
alone and it passes too. Run the file and it fails. That order-dependence is the
tell.

**Where:**
`pipeline.py:55`, the signature of `running_totals`:

```python
def running_totals(rows, totals=[]):
```

**How you found it:**
The phrase "3 more items" said the result was growing rather than being wrong,
which means state is surviving between calls. A function with no globals that
still remembers something points at the default argument. Confirmed in the REPL:

```
>>> a = running_totals(rows); b = running_totals(rows)
>>> a is b
True
>>> a
[29.97, 29.97]
>>> running_totals.__defaults__
([29.97, 29.97],)
```

`__defaults__` is the decisive evidence: the default list itself now holds data
from previous calls.

**Cause:**
Default arguments are evaluated **once**, when the `def` statement runs, not on
each call. So `totals=[]` creates one list that is stored on the function object
and reused by every call that omits the argument. Each call appends to it and
returns it, so results accumulate and every caller is handed the *same* list —
which is why `first` kept growing even after it had been returned, and why the
test has to copy with `list(...)` to see anything at all.

Straight out of Topic 3's `01_mutable_default.py`.

**Fix:**
Use `None` as the sentinel and build the list inside the function:

```python
def running_totals(rows, totals=None):
    if totals is None:
        totals = []
```

---

## What the tools gave you

Three of the four were found by **pytest's assertion rewriting alone** — the diff
is doing the work of a debugger for free. It named the single differing key in
bug 1 (`{'name': ' widget '}`, with `qty` and `price` explicitly called out as
identical), the exact field and both values in bug 2, the swapped extremes in
bug 3, and "Right contains 3 more items" in bug 4, which is the whole diagnosis
of an accumulating default in five words. `-l` would have added the locals, but
in each case the values in question were already in the message; `--pdb` would
have been slower than reading it.

The debugger earned its place only for the **cause**, not the symptom, and even
then a REPL probe was quicker than a breakpoint. Two one-line checks settled bugs
2 and 4 — `out[0] is r[0]` → `True`, and `running_totals.__defaults__` →
`([29.97, 29.97],)`. Both are identity questions, and identity is exactly what an
assertion diff cannot show you: `==` is satisfied by two equal dicts, so nothing
in the failure output can distinguish "a copy with the same values" from "the
same object". That is the one place where `p`/`pp` in `--pdb`, or a plain `print`
of `id()`, is genuinely faster than staring harder at the diff.

The most useful signal was not a tool at all: noticing **which tests passed**.
`test_apply_discount_reduces_qualifying_rows` passing told me the arithmetic in
bug 2 was fine and only ownership was wrong. `test_running_totals` passing while
its sibling failed told me bug 4 was order-dependent before I had looked at the
code. And `qty`/`price` surviving the whitespace in bug 1 was the clue that
`int()` and `float()` strip for you — which is why that bug hides so well. What
a test suite does *not* complain about narrows the search as sharply as what it
does.

If I were to do it again, I would run `uv run pytest . -q` once, read all four
diffs before touching anything, and keep a REPL open for identity checks. The
one habit worth keeping from this exercise: when a value is *wrong*, read the
diff; when a value is *shared*, reach for `is`.
