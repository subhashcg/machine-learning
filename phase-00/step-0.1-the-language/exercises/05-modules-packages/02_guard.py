"""2. The __main__ guard

Create `tool.py` next to this file. It must:

  - define  greet(name)  returning "hello NAME"
  - define  main()       which prints greet("world")
  - call main() ONLY when run directly

Importing tool must print nothing. Running `python tool.py` must print
"hello world".
"""

import io, contextlib, subprocess, sys, pathlib


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



def _silent_on_import():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        import tool
    assert buf.getvalue() == "", f"importing tool printed: {buf.getvalue()!r}"


def _greet_works():
    import tool
    assert tool.greet("world") == "hello world", f"got {tool.greet('world')!r}"


def _runs_as_script():
    path = pathlib.Path(__file__).parent / "tool.py"
    out = subprocess.run([sys.executable, str(path)], capture_output=True, text=True)
    assert out.returncode == 0, out.stderr
    assert out.stdout.strip() == "hello world", f"script printed {out.stdout!r}"


def _name_differs():
    import tool
    assert tool.__name__ == "tool", f"imported __name__ was {tool.__name__!r}"


if __name__ == "__main__":
    _run([
        ("importing tool prints nothing",  _silent_on_import),
        ("greet() works when imported",    _greet_works),
        ("running it prints hello world",  _runs_as_script),
        ("__name__ is 'tool' when imported", _name_differs),
    ])
