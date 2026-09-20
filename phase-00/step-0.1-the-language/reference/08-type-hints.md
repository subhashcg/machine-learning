# Reference — type hints

Lookup card.

## They are not enforced

```python
def double(n: int) -> int: return n * 2
double("ab")  ->  'abab'                      no error, no warning
double.__annotations__  ->  {'n': int, 'return': int}
```

Python stores annotations as metadata and ignores them. **All the value is in
tools that read them before the code runs:**

- **type checkers** (`mypy`, `pyright`) — the real payoff
- **editors** — autocomplete, inline errors
- **runtime consumers** — `@dataclass` reads them to find fields; Pydantic and
  FastAPI actually validate against them (the exception to "not enforced")

A hint nothing checks is documentation that can silently rot.

---

## Syntax

```python
def f(
    a: int,
    b: str = "x",
    c: list[int] | None = None,
    *args: float,
    **kwargs: str,
) -> dict[str, int]: ...

total: float = 0.0                    # variables too
```

| | |
|---|---|
| builtin generics (3.9+) | `list[int]` `dict[str, float]` `tuple[int, ...]` `set[str]` |
| union (3.10+) | `int \| None` — older: `Optional[int]` |
| returns nothing | `-> None` |
| any callable | `Callable[[int, str], bool]` |
| a literal set of values | `Literal["r", "w"]` |
| self-reference | quote it: `-> "Node"` |

`Optional[X]` means `X | None`. It does **not** mean "this argument is optional" —
a defaulted argument and a nullable type are different things.

```python
def f(x: int = 0)          # always an int; x + 1 is fine
def f(x: int | None = None) # caller must handle None before using it
```

---

## What a checker catches that tests do not

```
Incompatible types in assignment (expression has type "float", variable has type "str")
Value of type "dict[str, float] | None" is not indexable
Argument 1 to "scale" has incompatible type "str"; expected "float"
```

None of it needs the code to run.

**100% line coverage does not overlap with this.** Coverage asks *did this line
execute*; a checker asks *is this line consistent with every other line*.

```python
def report(path: str) -> str:
    cfg = load(path)          # -> dict | None
    return f"n={cfg['n']}"    # 100% covered by report("x"), crashes on report("")
```

Three things coverage structurally cannot find: lines that ran with only *some*
of their possible values; call sites your tests never reached; and code that is
unreachable rather than merely untested.

---

## `| None` is the hint that pays for itself

```python
u = find_user("u2")
print(u["name"])          # error: "dict | None" is not indexable

v = find_user("u1")
if v is not None:
    print(v["name"])      # fine — the checker NARROWS the type
```

Checkers understand `if x is not None`, `isinstance`, `assert x`, and early
returns. Annotating functions that can return `None` finds every unchecked one in
the codebase — the failure mode from Topic 6 where a missing file becomes an
empty result.

**If you adopt one hint, adopt this one.**

---

## `Protocol` — duck typing, checked

```python
from typing import Protocol

class Storage(Protocol):
    def save(self, key: str, value: str) -> None: ...
    def load(self, key: str) -> str | None: ...

def backup(store: Storage, data: dict[str, str]) -> int: ...
```

An implementation **never mentions the protocol** — no import, no inheritance.
The checker verifies names *and* signatures:

```
"WriteOnly" is missing following "Storage" protocol member: load

Following member(s) of "WrongTypes" have conflicts:
    Expected: def save(self, key: str, value: str) -> None
    Got:      def save(self, key: int, value: str) -> None
```

Note `WriteOnly` **works at runtime** — `backup` never calls `load`. The bug
surfaces months later on a different code path; only the static check finds it.

Why it fits Python: it works on classes you do not own, it matches what duck
typing already did, and it creates no coupling.

```
ABC       when you are providing shared implementation
Protocol  when you only need a capability
```

`@runtime_checkable` enables `isinstance`, but checks method *names* only — much
weaker than the static check.

---

## Where hints run out: numpy and pandas

```python
def normalise(X: np.ndarray) -> np.ndarray: ...
```

mypy: **no issues**. At runtime:

```
(3,4) int64   ->  (3, 4)         what you meant
(1,) float    ->  [nan]          std is 0, silent NaN
(2,3,4)       ->  (2, 3, 4)      ran, but means what?
```

The type says nothing about **shape**, **dtype**, or **preconditions** — which is
most of what goes wrong. A `(4, 3)` array normalised along the wrong axis gives
plausible numbers that are simply wrong. `pd.DataFrame` says nothing about
columns.

What to do instead:

```python
from numpy.typing import NDArray

def normalise(X: NDArray[np.float64]) -> NDArray[np.float64]:
    """Standardise each column to zero mean, unit variance.

    X: (n_samples, n_features). Constant columns produce NaN.
    """
    assert X.ndim == 2, f"expected 2-D (n_samples, n_features), got {X.shape}"
```

**Hints for the plumbing, assertions for the arrays.** Paths, IDs, config,
return-or-None get hints; shapes, dtypes and value preconditions get asserts at
the top of the function. This is why sklearn calls `check_array()` in every
`fit` — Phase 6.

---

## When they are worth it

| | |
|---|---|
| **Yes** | public APIs, anything returning `None`, library code, non-obvious types, dataclasses |
| **Marginal** | short private helpers, notebooks, exploratory scripts |

**A stale hint is worse than none** — it is a confident lie. `-> dict` on a
function that now returns a list actively misleads, and nothing catches it unless
a checker runs.

Adopt gradually: `mypy` on new files first, never `--strict` on day one.
