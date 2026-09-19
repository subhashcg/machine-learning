# Reference — exceptions

Lookup card.

## The hierarchy

```
BaseException
  ├─ Exception            everything normal
  ├─ KeyboardInterrupt    Ctrl+C          NOT caught by `except Exception`
  ├─ SystemExit           sys.exit()      NOT caught by `except Exception`
  └─ GeneratorExit        generator close NOT caught by `except Exception`
```

The three siblings are control flow, not errors. That is why `except Exception`
is the right default — it leaves your program killable. **Never write a bare
`except:`** (it catches `BaseException`).

Common ones under `Exception`: `ValueError`, `TypeError`, `KeyError`,
`IndexError`, `AttributeError`, `OSError` (→ `FileNotFoundError`,
`PermissionError`), `RuntimeError`, `StopIteration`, `ZeroDivisionError`.

---

## The four clauses

```python
try:
    r = risky()
except SomeError as e:
    ...          # ran
else:
    use(r)       # only if try raised NOTHING
finally:
    cleanup()    # always
```

**`else` keeps the `try` narrow.** Put only the risky call in `try`; everything
downstream goes in `else`. Otherwise a handler written for `risky()` also catches
bugs in `use()`:

```python
try:
    v = fetch("a")
    r = use(v)          # a typo in here raises KeyError
except KeyError:
    r = "default"       # ...and is reported as "fetch failed"
```

**`finally` is for cleanup** — closing, releasing, restoring.

### Never return from `finally`

```python
def f():
    try:
        raise ValueError("lost")
    finally:
        return "done"        # -> "done", the ValueError is GONE
```

`return`, `break` or `continue` in a `finally` discards whatever was in flight,
including an exception on its way up. No trace, no log.

---

## Handler order

First match wins, and `except` is an `isinstance` check:

```python
except Exception:            # catches everything below it
except FileNotFoundError:    # DEAD CODE — unreachable
```

Order specific → general. Linters flag this; Python does not.

---

## Custom exceptions

```python
class AppError(Exception):
    """Base for everything this app raises."""

class ConfigError(AppError):
    def __init__(self, key, message="missing"):
        super().__init__(f"config {key!r}: {message}")
        self.key = key          # structured, not buried in the message
```

- **One base class per app or library**, so callers can `except AppError` and
  catch everything you raise without catching their own bugs. (`RequestException`,
  `SQLAlchemyError` do exactly this.)
- **Attach data a handler might act on.** `e.key` is usable; parsing the message
  string is not.
- `except AppError` catches `ConfigError` because `isinstance` follows the MRO —
  exceptions are ordinary classes.

---

## Chaining

```python
try:
    int(raw)
except ValueError as e:
    raise ConfigError(path) from e
```

| form | the traceback says |
|---|---|
| `raise X from e` | **"the direct cause of"** — deliberate translation |
| `raise X` inside `except` | **"During handling of ... another exception occurred"** |
| `raise X from None` | nothing — original suppressed |

Python chains automatically, so the difference is *wording*, and the wording
matters: without `from`, the traceback reads as though your handler itself
malfunctioned. With it, it reads as an intentional translation.

Use `from None` only when the internal error would mislead.

---

## `raise` vs `raise e`

```
bare  raise   frames: ['<module>', 'outer', 'inner']
raise e       frames: ['<module>', 'outer', 'outer', 'inner']
```

Inside an `except`, bare `raise` re-raises untouched. `raise e` adds a frame at
the re-raise point — noise that compounds through layers.

---

## Antipatterns

```python
except:                      # catches KeyboardInterrupt, SystemExit
except Exception: pass       # silent
except Exception: return None
```

The last one is the expensive one:

```
user genuinely absent  ->  None      expected
file does not exist    ->  None      deploy broken
file is corrupt        ->  None      data broken
a typo in your code    ->  None      your bug
```

Four situations, one answer, caller cannot distinguish them. Write instead:

```python
with open(path) as f:            # FileNotFoundError propagates
    data = json.load(f)          # JSONDecodeError propagates
return data["users"].get(uid)    # absent user -> None, and only that
```

**`None` is an answer, not an error signal.** If it can mean both "legitimately
nothing" and "something broke", the caller has to guess.

---

## Exception groups (3.11+)

```python
raise ExceptionGroup("two failures", [ValueError("bad"), KeyError("missing")])

except* ValueError as eg: ...    # eg.exceptions -> [ValueError('bad')]
except* KeyError   as eg: ...
```

For several failures at once — concurrent tasks, batch validation. `except*`
takes the matching ones and lets the rest continue up.

---

## Deciding

**Catch when you can act:** retry, fall back, substitute a default, or add
context and re-raise.

**Let it propagate when you cannot.** An exception reaching the top with a
traceback beats one swallowed into a `None` that surfaces as nonsense three
functions later.

**Catch the narrowest type you can actually handle.**
