"""1. Build a package

Create a `shop/` directory next to this file containing:

    shop/__init__.py    a module docstring, VERSION = "1.0",
                        re-exports of add / total, and __all__
    shop/cart.py        items = [], add(x), total()   -- total returns the count
    shop/pricing.py     VAT = 0.2, with_vat(amount)

Callers must be able to write `from shop import add` without ever mentioning
shop.cart. Nothing may print on import.
"""

import io, contextlib


# ---------------------------------------------------------------- checks
# Written for you. Build the files described above; run this to see where you stand.

def _run(checks):
    ok = 0
    for label, fn in checks:
        try:
            fn()
        except (ImportError, ModuleNotFoundError, FileNotFoundError) as e:
            print(f"  ·     {label}  — {e}"); continue
        except AssertionError as e:
            print(f"  FAIL  {label}" + (f"  — {e}" if str(e) else "")); continue
        except Exception as e:
            print(f"  ERR   {label}  — {type(e).__name__}: {e}"); continue
        print(f"  ok    {label}"); ok += 1
    print(f"{ok}/{len(checks)} passing")



def _importable_and_silent():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        import shop
    assert buf.getvalue() == "", f"importing printed: {buf.getvalue()!r}"
    assert shop.__doc__, "shop/__init__.py needs a module docstring (first statement)"


def _public_face():
    import shop
    assert shop.VERSION == "1.0", f"VERSION was {getattr(shop, 'VERSION', None)!r}"
    assert callable(getattr(shop, "add", None)), "shop.add should be re-exported"
    assert callable(getattr(shop, "total", None)), "shop.total should be re-exported"


def _all_declared():
    import shop
    assert hasattr(shop, "__all__"), "declare __all__ in shop/__init__.py"
    ns = {}
    exec("from shop import *", ns)
    public = {k for k in ns if not k.startswith("__")}
    assert public == set(shop.__all__), f"import * gave {sorted(public)}"


def _submodules_work():
    from shop import cart, pricing
    before = cart.total()
    cart.add("apple")
    assert cart.total() == before + 1, "add() should grow the cart"
    assert pricing.with_vat(100) == 120, f"with_vat(100) gave {pricing.with_vat(100)}"


if __name__ == "__main__":
    _run([
        ("shop imports cleanly and has a docstring", _importable_and_silent),
        ("__init__ re-exports the public names",     _public_face),
        ("__all__ matches what import * gives",      _all_declared),
        ("submodules work",                          _submodules_work),
    ])
