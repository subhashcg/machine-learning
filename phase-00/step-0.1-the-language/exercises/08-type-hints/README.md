# Exercises — Topic 8, type hints

Write these in `exercises/08-type-hints/`. Standard library only.
Each file ends with checks written for you — run it to see where you stand.

Four exercises, not five: the topic is short and the fifth would have drilled
what 01 already covers.

**Run `mypy` on your answers too.** The checks read `__annotations__` and can
verify hints exist and say the right thing, but they cannot do what a checker
does:

```
uv run --with mypy mypy 01_annotate.py
```

---

**1. Annotate, and see that nothing enforces it**  ·  `01_annotate.py`

Four small functions to annotate and implement. The checks read
`__annotations__`, so the hints themselves are what is tested — including that
`first_or_none` declares `| None`, and that `shout(text, times=1)` hints `int`
rather than `int | None` (a default is not the same as a nullable type).

Then `ignores_types()` calls one of them with the wrong type and returns the
result, to show Python does not care.

---

**2. `| None`, and narrowing**  ·  `02_optional.py`

`find_user` returns `dict | None`. `greet_unsafe` indexes the result without
checking — **leave it broken**; a check asserts it raises `TypeError`.
`greet_safe` narrows first.

A type checker flags `greet_unsafe` without running it. Try it and see.

---

**3. `Protocol`**  ·  `03_protocol.py`

A `Store` protocol requiring `save` and `load`. `MemoryStore` satisfies it
**without inheriting**; `WriteOnly` has only `save`.

The last check is the point: `backup(WriteOnly(), ...)` **works at runtime**,
because `backup` never calls `load`. Only a static checker catches it. Run mypy
and watch it reject the same call.

---

**4. Where hints run out**  ·  `04_arrays.py`

`normalise(rows)` on a table held as a list of lists — the same problem as a
NumPy array, without needing NumPy. `list[list[float]]` permits a ragged table,
an empty one, and a transposed one.

So assert what the type cannot: equal row lengths, at least one row. Document
what a constant column does (NaN), and don't hide it.

**Hints for the plumbing, assertions for the arrays.**
