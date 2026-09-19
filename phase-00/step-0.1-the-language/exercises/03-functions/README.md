# Exercises — Topic 3, functions

Write these in `exercises/03-functions/`. Standard library only.
A `print` per function, and an `if __name__ == "__main__":` guard.

---

**1. `append_to(item, target=None)`**  ·  `01_mutable_default.py`

Append `item` to `target` and return it. A call with no `target` must start from
a fresh empty list every time.

Then write `append_to_broken` with `target=[]` and show, with output, that
repeated calls accumulate. Print `append_to_broken.__defaults__` after three
calls — watching the function's own metadata grow is the part that sticks.

---

**2. `describe(*args, **kwargs)`**  ·  `02_args_kwargs.py`

Return a string like `"2 positional (1, 2), 1 keyword {'x': 3}"`.

Then demonstrate the mirror operation: build a list and a dict, call `describe`
by unpacking them, and show the result matches passing the same values directly.

Finally show what happens when the unpacked list is one item short — same call
shape, different parameters filled.

---

**3. `resize(image, width, height, *, keep_ratio=True, upscale=False)`**  ·  `03_keyword_only.py`

It need not resize anything — return a description string. The point is the
signature.

Show that `resize("img", 800, 600, True, False)` raises, and say in a comment
why refusing that call is a feature.

---

**4. `retry(fn, *args, times=3, **kwargs)`**  ·  `04_retry.py`

Call `fn(*args, **kwargs)`, retrying up to `times` on exception, returning the
first success and raising if all attempts fail.

Test with a function that fails twice then succeeds. Then write `retry_bad` with
`times` *before* `*args` and show the argument collision — including which
function the error appears to come from.

---

**5. `make_counter()`**  ·  `05_closures.py`

Return two functions, `increment` and `read`, sharing one count. `read` must see
the current value, not a snapshot.

Then make two independent counters and show their counts don't interfere.
Print `increment.__closure__[0].cell_contents` to see the captured cell.

---

**6. `make_multipliers(n)`**  ·  `06_late_binding.py`

Return a list of `n` functions where function `i` multiplies its argument by `i`.

Write the broken version first (a plain comprehension over `range(n)`), show it
returns the wrong answers, then fix it. Keep both, with a comment naming what the
closure captured.

---

**7. `counter_demo()`**  ·  `07_scope.py`

Reproduce `UnboundLocalError` deliberately, catch it, and print the message.

Then show three working versions of the same intent: one using `global`, one
using `nonlocal`, and one that just takes a parameter and returns a value.

In a comment, say which you would ship and why.
