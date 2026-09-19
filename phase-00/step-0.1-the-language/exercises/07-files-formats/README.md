# Exercises — Topic 7, files and formats

Write these in `exercises/07-files-formats/`. Standard library only.
Each file ends with checks written for you — run it to see where you stand.

---

**1. Write a context manager twice**  ·  `01_context_manager.py`

`Tracker` as a class with `__enter__`/`__exit__`, then `tracker()` with
`@contextmanager`. Both append `"enter"` and `"exit"` to a list so the checks can
see the order, and neither may swallow the exception.

One check runs a body that raises. If your `@contextmanager` version lacks
`try/finally` around the `yield`, the cleanup is skipped and it fails.

Then `swallowing()`, which does swallow — so the contrast is on the page.

---

**2. pathlib**  ·  `02_pathlib.py`

`describe(path)`, `csv_files(dir)` (this level), `all_csv_files(dir)` (recursive,
POSIX-style relative paths), `swap_extension(path, suffix)`.

Return `Path` objects, not strings, except where stated.

---

**3. Encoding**  ·  `03_encoding.py`

`save` / `load` in UTF-8, `load_as(path, encoding)`, and
`round_trips(path, text, encoding) -> bool`.

The checks assert what matters: **latin-1 does not raise** — it silently returns
different text. ascii raises. Only one of those is the dangerous case.

---

**4. CSV**  ·  `04_csv.py`

`naive_parse` (the wrong way, kept for contrast), `read_rows` via `DictReader`,
`read_typed` converting qty and price, and `write_rows` via `DictWriter`.

The test data has a quoted comma, escaped quotes, and a newline inside a field.
`read_typed` must **raise** on a bad number rather than guessing.

---

**5. JSON and what it loses**  ·  `05_json.py`

`save_json` / `load_json`, `survives(obj) -> bool`, and `encode_dates` using the
`default=` hook.

`survives()` is the exercise: run it on a tuple, on a dict with int keys, and on
plain data, and see which come back unchanged. One check shows two distinct keys
collapsing into one — data lost, no error.
