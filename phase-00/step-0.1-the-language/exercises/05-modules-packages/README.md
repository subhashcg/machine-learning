# Exercises — Topic 5, modules and packages

Write these in `exercises/05-modules-packages/`. Standard library only.

Unlike earlier topics, most of these ask you to **create files** rather than fill
in a function. The numbered files are the checks — run them to see where you
stand. Don't edit the checks; if one looks wrong, say so.

```
  ok    __all__ matches what import * gives
  FAIL  __init__ re-exports the public names  — shop.add should be re-exported
  ·     submodules work  — No module named 'shop'
```

`·` means the file you need doesn't exist yet.

---

**1. Build a package**  ·  `01_package.py`

Create a `shop/` directory containing:

| file | holds |
|---|---|
| `shop/__init__.py` | a module docstring, `VERSION = "1.0"`, re-exports of `add`/`total`, and `__all__` |
| `shop/cart.py` | `items = []`, `add(x)`, `total()` returning the count |
| `shop/pricing.py` | `VAT = 0.2`, `with_vat(amount)` |

Callers must be able to write `from shop import add` without ever mentioning
`shop.cart`. Nothing may print on import.

---

**2. The `__main__` guard**  ·  `02_guard.py`

Create `tool.py` with `greet(name)`, `main()` which prints `greet("world")`, and
a guard so `main()` runs only when the file is executed directly.

Importing it must print nothing; running it must print `hello world`.

---

**3. from-import binds a reference**  ·  `03_binding.py`

Create `settings.py` with exactly `DEBUG = False` and `HOSTS = []`.

Nothing else to implement. **Read the four checks and predict each one before
running.** They encode the difference between rebinding a module attribute and
mutating the object it points at — the thing you got wrong in the discussion.

---

**4. Circular imports**  ·  `04_circular.py`

First build the broken pair: `alpha.py` imports `beta` then defines `A_VALUE`;
`beta.py` imports `alpha` and records `saw_a_value = hasattr(alpha, "A_VALUE")`
**at module level**. Importing `alpha` will run `beta` while `alpha` is only
half-built.

Then fix it: `shared.py` holds the common value, and `gamma.py` / `delta.py` both
import `shared` instead of each other.

---

**5. Loading a file that cannot be imported**  ·  `05_dynamic_load.py`

Write `load(path, name="ex")` using `importlib.util`. Then use it to reach back
into Topic 2 and call your own `flatten()` — the file is `03_flatten.py`, and
`import 03_flatten` is a `SyntaxError`.
