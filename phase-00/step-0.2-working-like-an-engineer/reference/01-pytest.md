# Reference — pytest

Lookup card.

## Running it

```bash
uv add --dev pytest          # then: uv run pytest
uv run --with pytest pytest  # or one-off, without adding it
```

| flag | |
|---|---|
| `-q` / `-v` / `-vv` | quieter / per-test names / full diffs |
| `-x` | stop at the first failure |
| `-k 'name'` | run only tests whose name matches |
| `--lf` | re-run only last-failed |
| `--collect-only` | list tests without running |
| `pytest path::test_name[case]` | run exactly one |

Discovery: files `test_*.py` (or `*_test.py`), functions `test_*`, classes
`Test*` with no `__init__`.

---

## A test is a function with an assert

```python
def test_basic():
    assert only_in_first([1, 2, 3, 2], [2]) == [1, 3]
```

No base class, no `self`, no `assertEqual`.

### Assertion introspection

```
>   assert word_count("the The cat") == {"the": 2, "cat": 9}
E   AssertionError: assert {'the': 2, 'cat': 1} == {'the': 2, 'cat': 9}
E     Differing items:
E     {'cat': 1} != {'cat': 9}
```

pytest installs an import hook and **rewrites the bytecode** of collected test
files, capturing operands before the comparison collapses to a bool. A plain
`assert` cannot do this: by the time it fails, `a == b` is already `False` and
the operands are gone.

Only applies to files pytest collects — `assert` in your library code stays
plain.

---

## parametrize

```python
@pytest.mark.parametrize("a, b, expected", [
    ([1, 2, 3, 2], [2], [1, 3]),
    ([],           [1], []),
    ([1, 2],       [],  [1, 2]),
])
def test_cases(a, b, expected):
    assert only_in_first(a, b) == expected
```

**Independent tests, not one test with a loop.** A loop stops at the first
failure; parametrised cases each pass or fail on their own:

```
FAILED test_loop        - assert 2 == 99        stopped there
FAILED test_param[2-99] - assert 2 == 99        found BOTH
FAILED test_param[4-88] - assert 4 == 88
```

The case is named in the report, and you can re-run just one:

```bash
pytest "test_cmp.py::test_param[2-99]"
```

Use `ids=[...]` to name cases readably. Stacking two `parametrize` decorators
gives the cross product.

---

## Testing that something raises

```python
def test_raises():
    with pytest.raises(ValueError, match="divide by zero"):
        divide(1, 0)
```

`match=` is a **regex** against the message, so a `ValueError` raised for some
other reason does not pass by accident. Capture the exception if you need it:

```python
with pytest.raises(ConfigError) as info:
    load("bad")
assert info.value.key == "port"
assert isinstance(info.value.__cause__, ValueError)
```

Replaces the six-line `try/except/else: raise AssertionError(...)` dance.

---

## Floats

```python
assert 0.1 + 0.2 == pytest.approx(0.3)
assert result     == pytest.approx([0.1, 0.2])       # works on containers
assert stats      == pytest.approx({"mean": 0.0})
```

Relative tolerance (1e-6), so it scales across magnitudes. **Against zero a
relative tolerance is meaningless** — use `abs=`:

```python
assert x == pytest.approx(0.0, abs=1e-9)
```

Outside pytest: `math.isclose`, and `np.allclose` from Phase 1.

---

## Fixtures

```python
@pytest.fixture
def sample_file(tmp_path):
    p = tmp_path / "data.csv"
    p.write_text("a,b\n1,2\n", encoding="utf-8")
    return p

def test_reads(sample_file):          # asked for by NAME
    assert sample_file.read_text(encoding="utf-8").startswith("a,b")
```

A fixture builds something a test needs. Request it by putting its name in the
test's parameters; pytest matches by name and calls it.

**Fresh per test by default** — one test mutating it cannot affect another.

### Teardown uses the Topic 7 shape

```python
@pytest.fixture
def db():
    conn = connect()
    yield conn          # the test runs here
    conn.close()        # teardown, even if the test failed
```

### Scope

```python
@pytest.fixture(scope="function")   # default — once per test
@pytest.fixture(scope="module")     # once per file
@pytest.fixture(scope="session")    # once per run
```

Widen it only when setup is genuinely expensive (a database, a large model) —
and then nothing may mutate the shared object, or you get test-order
dependencies that pass locally and fail in CI.

### Built-in fixtures worth knowing

| | |
|---|---|
| `tmp_path` | a unique `Path` per test, cleaned up |
| `capsys` | capture stdout/stderr: `capsys.readouterr().out` |
| `monkeypatch` | patch attributes, dict items, env vars; undone automatically |
| `caplog` | capture log records |

`conftest.py` holds fixtures shared across files in that directory and below —
no import needed.

---

## Layout

```
project/
  src/mypkg/core.py
  tests/
    conftest.py          shared fixtures
    test_core.py
  pyproject.toml
```

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-q"
```

---

## What to test

- **The contract, not the implementation.** A test that breaks when you rename a
  private helper is a liability.
- **The edges you would not think to try by hand**: empty, one element,
  duplicates, the value that breaks a precondition.
- **Every bug you fix** gets a test that fails without the fix — otherwise it
  comes back.
- **Behaviour you cannot see in the return value**: that inputs are unmutated,
  that only `n` items were consumed, that a file handle got closed.

`assert` proves a claim; deciding *which* claims are worth pinning down is the
actual work, and no framework does it for you.

**Limitation:** pytest checks the examples you thought of. Property-based
testing (`hypothesis`) generates inputs to break assumptions you did not know
you had.
