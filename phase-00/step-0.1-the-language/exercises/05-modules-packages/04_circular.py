"""4. Circular imports

Create three files next to this one.

First, the broken pair:

    alpha.py    imports beta, then defines  A_VALUE = "a"
                and  describe()  returning f"alpha sees {beta.B_VALUE}"
    beta.py     imports alpha, then defines B_VALUE = "b"
                and  saw_a_value  = hasattr(alpha, "A_VALUE")   <- at module level

Import alpha first and beta will run while alpha is only half-built, so
beta.saw_a_value will be False.

Then the fix:

    shared.py   VALUE = "shared"
                and gamma.py / delta.py which BOTH import shared instead of
                each other. Give each a  describe()  using shared.VALUE.
"""


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



def _circular_leaves_a_half_built_module():
    import alpha
    import beta
    assert beta.saw_a_value is False, (
        "beta should have seen alpha WITHOUT A_VALUE — check that beta reads "
        "hasattr(alpha, 'A_VALUE') at module level, and that alpha imports beta "
        "BEFORE defining A_VALUE"
    )


def _but_it_works_afterwards():
    import alpha, beta
    assert alpha.A_VALUE == "a" and beta.B_VALUE == "b"
    assert alpha.describe() == "alpha sees b", f"got {alpha.describe()!r}"


def _the_fix_has_no_cycle():
    import gamma, delta, shared, sys
    assert shared.VALUE == "shared"
    assert gamma.describe() == "gamma sees shared", f"got {gamma.describe()!r}"
    assert delta.describe() == "delta sees shared", f"got {delta.describe()!r}"
    src = (open(gamma.__file__).read() + open(delta.__file__).read())
    assert "import delta" not in src and "import gamma" not in src, (
        "gamma and delta must not import each other"
    )


if __name__ == "__main__":
    _run([
        ("the cycle leaves beta seeing a half-built alpha", _circular_leaves_a_half_built_module),
        ("both modules are complete once imports finish",   _but_it_works_afterwards),
        ("shared.py breaks the cycle",                      _the_fix_has_no_cycle),
    ])
