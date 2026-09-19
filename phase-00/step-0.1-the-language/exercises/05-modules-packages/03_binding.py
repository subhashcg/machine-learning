"""3. from-import binds a reference

Create `settings.py` next to this file with exactly two module-level names:

    DEBUG = False
    HOSTS = []

Then predict each check below before running. They encode the difference between
rebinding a module attribute and mutating the object it points at.

Nothing to implement beyond settings.py — this one is about reading the checks
and being unsurprised.
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



def _rebinding_does_not_propagate():
    import settings
    from settings import DEBUG
    settings.DEBUG = True
    assert DEBUG is False, "the imported name should NOT have followed the rebind"
    assert settings.DEBUG is True
    settings.DEBUG = False


def _mutation_does_propagate():
    import settings
    from settings import HOSTS
    settings.HOSTS.append("db1")
    assert HOSTS == ["db1"], "same object, so the mutation is visible"
    assert HOSTS is settings.HOSTS
    settings.HOSTS.clear()


def _rebinding_the_list_detaches():
    import settings
    from settings import HOSTS
    settings.HOSTS = ["replaced"]
    assert HOSTS == [], "your name still points at the ORIGINAL list"
    assert HOSTS is not settings.HOSTS


def _module_is_a_singleton():
    import settings
    import settings as again
    assert settings is again, "one module object per process"


if __name__ == "__main__":
    _run([
        ("rebinding a module attribute does not propagate", _rebinding_does_not_propagate),
        ("mutating the object does propagate",              _mutation_does_propagate),
        ("rebinding the list detaches your name",           _rebinding_the_list_detaches),
        ("the module is a singleton",                       _module_is_a_singleton),
    ])
