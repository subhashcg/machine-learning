# Reference — modules and packages

Lookup card.

## Importing runs the file, once

An `import` does three things: find the file, **execute it top to bottom**, cache
the result in `sys.modules`. Later imports of the same name skip to step three.

```
first import :   406.3 ms        (a sleep at module level)
second import:     0.0 ms        just a dict lookup
```

```python
sys.modules                      # a plain dict
del sys.modules["shop.cart"]     # next import re-runs the file
importlib.reload(shop.cart)      # same, without the delete
```

**Module-level code is startup cost.** A `read_csv()` at module level runs for
anyone who imports the file, including a test collector that wanted one function.
Keep module level to definitions and cheap constants.

**A module is a singleton.** One object per process, shared by every importer —
so module-level mutable state is global state.

---

## A module object is a namespace

```
type(shop.cart)  -> module        vars(shop.cart) -> ['items', 'add', 'total']
```

Running the file builds a dict of the names it defined. `shop.cart.add` is a dict
lookup; `shop.cart.add = fake` rebinds it for everyone (this is monkey-patching).

---

## `__name__` and the guard

Python sets `__name__` to the module's import path — except the file you ran,
which gets `"__main__"`.

```
the file you ran  ->  __main__
shop/cart.py      ->  shop.cart
```

```python
if __name__ == "__main__":     # only when this file is the entry point
```

A file both imported and run directly becomes **two modules** with two copies of
every class and global — `isinstance` then fails between them.

### `python script.py` vs `python -m package.module`

```
python script.py    __package__ = None   sys.path[0] = the FILE's directory
python -m script    __package__ = ''     sys.path[0] = the CURRENT directory
```

```
uv run python shop/billing/invoice.py  ->  ModuleNotFoundError: No module named 'shop'
```

Running a package file directly puts *its* directory on the path, not the project
root. Use `-m`. **Relative imports fail outright in a directly-run script** —
`__main__` has no package to be relative to.

---

## Packages

A directory Python imports. `__init__.py` runs when anything inside it is first
imported, all the way down the chain.

Its job is to be the package's **public face**:

```python
# shop/__init__.py
"""The shop package."""
VERSION = "1.0"
from shop.cart import add, total
__all__ = ["add", "total", "VERSION"]      # what `import *` exports
```

Callers write `from shop import add`, so you can reorganise internals freely
without breaking them.

**Namespace packages** — since 3.3 a directory without `__init__.py` still
imports, but has no `__file__` and silently merges same-named directories from
different path entries. Write the `__init__.py`.

---

## Import forms

```python
import shop.billing.invoice   # runs all three, binds ONLY the top name `shop`
import shop.cart as c         # binds c to the module object
from shop.cart import add     # binds add — a reference, taken at import time
from shop import *            # binds whatever __all__ lists
```

### `from x import y` copies a reference

```
cart.items.append("x")   ->  my_items sees it        mutation
cart.items = ["new"]     ->  my_items unchanged      rebinding
```

Sixth costume of mutate-vs-rebind (`[[0]*n]*m`, `a[:]`, `basket=[]`,
class attributes, now module attributes).

**Practical rule:** `import config` and read `config.DEBUG` at the point of use.
`from config import DEBUG` freezes the value at import time — which is before
most of your code has run.

---

## `sys.path`

Searched in order, first match wins:

```
''  (script's directory, or CWD under -m)    <- FIRST
.../python311.zip
.../lib/python3.11
.../site-packages                            <- installed packages, LAST
```

Your directory is searched **before the standard library**:

```
# a file named random.py in your project
import random
random.random  ->  AttributeError
```

And `sys.path` is process-wide, so *installed libraries* importing `random` also
get yours. The traceback appears inside code you have never opened.

Avoid naming files: `random json types email test copy select socket string time
queue logging platform`. Check with `python -c "import X"` first.

`PYTHONPATH` prepends entries; a virtualenv swaps which `site-packages` is on the
list — that is the whole mechanism behind `uv` and `pyproject.toml`.

---

## Circular imports

```
a imports b, b imports a
b sees a.VALUE?  False
```

`a` is in `sys.modules` already (to stop infinite recursion) but only **partially
built**, so `b` gets a module missing everything below the import line.

Sometimes `ImportError`, sometimes a silent half-module that works until someone
reorders two lines. Fix structurally: move the shared thing to a third module, or
defer the import into the function that needs it.

---

## Module names are identifiers

```
flatten      True          01_flatten   False   (starts with a digit)
utils        True          my-module    False   (hyphen is minus)
                           class        False   (keyword)
```

`import 01_flatten` is a `SyntaxError`. To load such a file anyway:

```python
import importlib.util
spec = importlib.util.spec_from_file_location("ex", "path/to/01_flatten.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
```

Filenames that sort nicely and filenames that import are different constraints.

---

## Docstrings

A module docstring is a string literal that is **the first statement**. Python
runs the file; a bare string first gets stored as `__doc__`. Anywhere else it is
an ordinary expression — built, evaluated, discarded.

Order: docstring, then imports.

---

## Layout that works

```
project/
  pyproject.toml
  src/
    mypkg/
      __init__.py       public face: re-exports, __all__, VERSION
      core.py
      io.py
  tests/
    test_core.py
```

`src/` layout means tests import the *installed* package, not the directory next
to them — so you test what you ship. Run modules with `-m`, not by path.
