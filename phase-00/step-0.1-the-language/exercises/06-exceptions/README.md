# Exercises — Topic 6, exceptions

Write these in `exercises/06-exceptions/`. Standard library only.
Each file ends with checks written for you — run it to see where you stand.

---

**1. try / except / else / finally**  ·  `01_clauses.py`

`parse_and_double(raw, log)` — `int(raw)` in `try`; on `ValueError` log `"bad"`
and return `None`; do the doubling in **`else`**; log `"done"` in `finally`.

One check passes an object whose `__mul__` raises. If your doubling sits inside
`try`, that bug gets caught by the handler written for `int()` — which is the
whole reason `else` exists.

`boom(log)` returns from `finally` while an exception is in flight. Leave it
broken; the check asserts the exception vanishes.

---

**2. A custom exception hierarchy**  ·  `02_hierarchy.py`

`AppError` base, `ConfigError(key, message="missing")` storing `.key`,
`RetryableError(message, attempts)` storing `.attempts`.

Then `classify(exc)` returning `"retryable"` / `"app"` / `"other"` — with the
checks in the right order, since `RetryableError` *is an* `AppError`.

---

**3. Chaining**  ·  `03_chaining.py`

Three versions of the same wrap, differing only in the `raise`:

| | sets |
|---|---|
| `raise X from e` | `__cause__` |
| `raise X` | `__context__` only |
| `raise X from None` | `__suppress_context__` |

The checks read those attributes directly, so you can see what each form
actually does rather than reading it off a traceback.

---

**4. Catch only what you can act on**  ·  `04_narrow.py`

`wide()` uses `except Exception: return None`. `narrow()` returns `None` **only**
when the user is genuinely absent.

The checks feed both a malformed payload — a missing `"users"` key, and a
`"users"` that is a list. `wide()` must swallow them; `narrow()` must let them
raise. Write the antipattern deliberately so the contrast is on the page.

---

**5. retry, properly**  ·  `05_retry.py`

Rewrite Topic 3's `retry` with exceptions you now understand:

```python
retry(fn, *args, times=3, retry_on=Exception, **kwargs)
```

Retry only on `retry_on`; anything else propagates immediately. After the last
failure, raise `RetryError` **from** the last exception. Log each failure's
message in `retry.log`.

One check asserts `KeyboardInterrupt` is never retried — you shouldn't need to
write anything special for that, and knowing why is the point.
