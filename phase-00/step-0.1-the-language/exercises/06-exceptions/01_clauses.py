"""1. try / except / else / finally

parse_and_double(raw, log) must:
  - int(raw) inside try; on ValueError append "bad" to log and return None
  - do the doubling in `else`, so a bug there is NOT caught by that handler
  - append "done" to log in `finally`, on every path

boom(log) shows why you never return from finally: it raises ValueError inside
try and returns "swallowed" from finally. Leave it broken — that is the point.
"""


def parse_and_double(raw, log):
    try:
        n = int(raw)            # the only line the handler is meant for
    except ValueError:
        log.append("bad")
        return None
    else:
        return n * 2            # errors here propagate; the handler above can't see them
    finally:
        log.append("done")      # runs after either return, before the caller gets the value


def boom(log):
    try:
        raise ValueError("lost")
    finally:
        return "swallowed"      # discards the in-flight ValueError — never do this


# ---------------------------------------------------------------- checks
# Written for you. Implement above; run the file to see where you stand.

def _run(checks):
    ok = 0
    for label, fn in checks:
        try:
            fn()
        except NotImplementedError:
            print(f"  ·     {label}"); continue
        except AssertionError as e:
            print(f"  FAIL  {label}" + (f"  — {e}" if str(e) else "")); continue
        except Exception as e:
            print(f"  ERR   {label}  — {type(e).__name__}: {e}"); continue
        print(f"  ok    {label}"); ok += 1
    print(f"{ok}/{len(checks)} passing")



def _happy_path():
    log = []
    assert parse_and_double("21", log) == 42
    assert log == ["done"], f"log was {log}"


def _bad_input():
    log = []
    assert parse_and_double("abc", log) is None
    assert log == ["bad", "done"], f"log was {log}"


def _finally_always_runs():
    log = []
    parse_and_double("abc", log)
    assert "done" in log, "finally must run on the error path too"


def _else_is_outside_the_guard():
    log = []
    class Exploding:
        def __mul__(self, other): raise ValueError("bug in the doubling step")
    try:
        parse_and_double(Exploding(), log)
    except (ValueError, TypeError):
        return
    raise AssertionError(
        "a ValueError raised while doubling should NOT be caught by the "
        "handler written for int(); put the doubling in `else`"
    )


def _finally_return_swallows():
    log = []
    assert boom(log) == "swallowed", "returning from finally discards the exception"


if __name__ == "__main__":
    _run([
        ("happy path returns double",            _happy_path),
        ("bad input logs and returns None",      _bad_input),
        ("finally runs on the error path",       _finally_always_runs),
        ("else keeps the try block narrow",      _else_is_outside_the_guard),
        ("returning from finally swallows it",   _finally_return_swallows),
    ])
