# Reference — files and formats

Lookup card.

## `with` is two dunder methods

```python
class Thing:
    def __enter__(self):
        return value              # whatever this returns is bound by `as`
    def __exit__(self, exc_type, exc, tb):
        return False              # False/None -> re-raise; True -> SWALLOW
```

`__exit__` runs whether the body succeeded or raised, and receives the exception
so it can inspect it.

**`as` binds what `__enter__` returns**, not the context manager:

```
def __enter__(self): return 42      ->  with X() as v:   v = 42
def __enter__(self): return self    ->  v is the manager  (what file objects do)
def __enter__(self): pass           ->  v = None          easy bug
```

With `@contextmanager`, `as` binds whatever you **yield**; a bare `yield` gives
`None`. And `as` is optional — a manager used only for its side effect needs
none.

**Returning `True` swallows the exception** — `except Exception: pass` hidden
inside a class, invisible at the call site, and it covers the whole block. The
only good use is when suppression is the declared purpose and is narrow:
`contextlib.suppress(FileNotFoundError)`.

### `@contextmanager` — the same thing as a generator

```python
from contextlib import contextmanager

@contextmanager
def timed(label):
    start = time.perf_counter()
    try:
        yield label                 # everything before = __enter__
    finally:
        print(...)                  # everything after  = __exit__
```

**The `try/finally` is not optional.** `@contextmanager` throws the body's
exception back in *at the `yield`*; without a `try`, it propagates out and every
line after `yield` is skipped — the cleanup never runs.

Use `except` inside if you want to inspect it; `finally` for cleanup that must
happen either way.

### Why bother at all

```
without with:  f.closed = False      leaked until the GC gets to it
with:          f.closed = True       closed even if the body raised
```

CPython's refcounting usually closes a dropped handle quickly, which is why
forgetting `with` seems to work — until a loop over thousands of files gives you
`OSError: Too many open files` from somewhere unrelated.

---

## pathlib

```python
p = Path("data") / "raw" / "sales.csv"        # / is the join operator
```

| | |
|---|---|
| `p.name` | `'sales.csv'` |
| `p.stem` | `'sales'` |
| `p.suffix` | `'.csv'` |
| `p.parent` | `PosixPath('data/raw')` |
| `p.parts` | `('data', 'raw', 'sales.csv')` |
| `p.with_suffix('.parquet')` | `data/raw/sales.parquet` |

```python
p.write_text(s, encoding="utf-8")    p.read_text(encoding="utf-8")
p.exists()   p.stat().st_size   p.mkdir(parents=True, exist_ok=True)   p.unlink()
d.glob("*.csv")      # this level
d.rglob("*.csv")     # recursive
```

`Path` objects know they are paths; `os.path` takes strings, so a typo produces a
string that looks fine until you use it.

---

## Encoding — pass it, always

```
written utf-8, read utf-8   ->  'café ☕'
read as latin-1             ->  'cafÃ© â\x98\x95'      silently wrong
read as ascii               ->  UnicodeDecodeError
```

**The default depends on the OS locale** — UTF-8 on macOS/Linux, often cp1252 on
Windows. Same code, same file, different result on two machines.

The dangerous part: latin-1 and cp1252 have a meaning for nearly every byte, so
they **never raise** — they hand you mojibake that flows into your database.

`encoding="utf-8"` on every read and every write.

---

## CSV

```
line.split(',')  ->  ['Widget', '"Red', ' large"', '3']      wrong
csv.reader       ->  ['Widget', 'Red, large', '3']           right
```

Three reasons splitting cannot work:

- **quoted commas** — `"Red, large"` is one field
- **escaped quotes** — `""` inside a quoted field means one literal `"`
- **embedded newlines** — a record can span lines, so *line-by-line is already
  wrong*, before you get to splitting

```python
import csv
with open(path, newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):      # keys from the header row
        ...

with open(path, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=[...])
    w.writeheader(); w.writerows(rows)
```

- **`newline=""` is required.** Without it Windows inserts a blank line between
  every row. The csv module handles line endings itself.
- **Everything reads back as a string.** `qty` is `'3'`, not `3`. CSV has no
  types — every conversion, and every conversion failure, is yours.

---

## JSON

Round-trips: `int` `float` `str` `bool` `None` `list` `dict`.

Refuses loudly:

```
date  set  Decimal  bytes   ->  TypeError: Object of type X is not JSON serializable
tuple as a KEY          ->  TypeError: keys must be str, int, float, bool or None
```

Coerces **silently** — the dangerous half:

```
tuple as a value  ->  [2, 3]            became a list
int keys          ->  {'1': 'a'}        keys are always strings
NaN / Infinity    ->  {"x": NaN}        emitted, but not valid JSON; other parsers reject it
```

And the one that loses data:

```
{1: 'int key', '1': 'string key'}   len 2
{'1': 'string key'}                 len 1     two keys collapsed, no error
```

**`json.loads(json.dumps(x)) == x` is False** for tuples, non-string keys, and
anything coerced. JSON is a lossy round-trip, silently. If types matter, use a
format with a schema (parquet) — which is why Phase 2 prefers it.

```python
json.dumps(obj, indent=2)              # for humans
json.dumps(obj, default=str)           # last-resort fallback for dates etc.
with open(p, encoding="utf-8") as f: data = json.load(f)
```

---

## Choosing a format

```
Human-editable config, small, nested        -> JSON (or TOML)
Tabular, exchanged with spreadsheets        -> CSV, and accept it is all strings
Tabular, typed, large, read repeatedly      -> parquet  (Phase 2)
Arbitrary Python objects                    -> pickle — never from an untrusted source
Append-only records, one per line           -> JSON Lines (one JSON object per line)
```
