"""5. Loading a file that cannot be imported

`import 01_flatten` is a SyntaxError — module names must be identifiers. This is
how I have been loading your exercise files all along.

Write  load(path, name="ex")  that loads any .py file by PATH and returns the
module object. Use importlib.util.spec_from_file_location, module_from_spec and
spec.loader.exec_module.

Then use it to reach back into Topic 2 and call your own flatten().
"""

import importlib.util, pathlib

TOPIC2 = pathlib.Path(__file__).parents[1] / "02-comprehensions-generators"


def load(path, name="ex"):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)   # empty module, __name__ = name
    spec.loader.exec_module(module)                  # run the file's code inside it
    return module


if __name__ == "__main__":
    print(load(TOPIC2 / "03_flatten.py").flatten([[1, 2], [3], [], [4, 5]]))


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



def _plain_name_still_invalid():
    assert not "01_flatten".isidentifier(), "digits cannot start an identifier"


def _loads_a_numbered_file():
    m = load(TOPIC2 / "03_flatten.py")
    assert hasattr(m, "flatten"), "the loaded module should expose flatten"
    assert m.flatten([[1, 2], [3], [], [4, 5]]) == [1, 2, 3, 4, 5]


def _each_load_is_a_fresh_module():
    a = load(TOPIC2 / "03_flatten.py", "one")
    b = load(TOPIC2 / "03_flatten.py", "two")
    assert a is not b, "loading by path bypasses the sys.modules cache"


def _name_is_used():
    m = load(TOPIC2 / "03_flatten.py", "chosen")
    assert m.__name__ == "chosen", f"__name__ was {m.__name__!r}"


if __name__ == "__main__":
    _run([
        ("01_flatten is not a valid identifier", _plain_name_still_invalid),
        ("load() runs a numbered file",          _loads_a_numbered_file),
        ("each load is a fresh module",          _each_load_is_a_fresh_module),
        ("the name argument is used",            _name_is_used),
    ])
