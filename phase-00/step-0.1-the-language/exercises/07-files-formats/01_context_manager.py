"""1. Write a context manager twice

    class Tracker:      a class-based one, using __enter__ / __exit__
    tracker():          the same thing with @contextmanager

Both take a list and append to it, so the checks can see the order:
  "enter" on entry, "exit" on the way out — including when the body raises.

Both must give `as` something useful: the class returns the log, the generator
yields a dict {"log": log, "label": label}. `as` binds what __enter__ RETURNS
(or what the generator YIELDS), not the context manager itself — a method with
no return statement quietly gives you None.

Neither may swallow the exception. Then `swallowing()`, which DOES swallow —
so the contrast is on the page.
"""

from contextlib import contextmanager


class Tracker:
    def __init__(self, log):
        self.log = log

    def __enter__(self):
        self.log.append("enter")
        return self.log                 # this is what `as` binds

    def __exit__(self, exc_type, exc, tb):
        self.log.append("exit")
        return False                    # falsy: any exception carries on


@contextmanager
def tracker(log, label="t"):
    log.append("enter")
    try:
        yield {"log": log, "label": label}   # the body runs here
    finally:
        log.append("exit")                   # runs on both paths


@contextmanager
def swallowing(log):
    log.append("enter")
    try:
        yield log
    except Exception:                   # the body's exception is thrown in AT the yield
        log.append("swallowed")         # not re-raising it ends the `with` normally
    finally:
        log.append("exit")


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



def _class_happy_path():
    log = []
    with Tracker(log) as value:
        log.append("body")
        assert value is log, "__enter__ should return the log (bound by `as`)"
    assert log == ["enter", "body", "exit"], f"log was {log}"


def _class_cleans_up_on_error():
    log = []
    try:
        with Tracker(log):
            raise ValueError("boom")
    except ValueError:
        assert log == ["enter", "exit"], f"log was {log}"
        return
    raise AssertionError("Tracker must not swallow the exception")


def _generator_version_matches():
    log = []
    with tracker(log):
        log.append("body")
    assert log == ["enter", "body", "exit"], f"log was {log}"


def _as_binds_the_yielded_value():
    log = []
    with tracker(log, label="reader") as handle:
        assert isinstance(handle, dict), f"`as` bound {handle!r}, not the yielded dict"
        assert handle["label"] == "reader", f"got {handle}"
        assert handle["log"] is log, "the yielded dict should hold the same list"


def _as_is_optional():
    log = []
    with tracker(log):            # no `as` at all
        pass
    assert log == ["enter", "exit"], f"log was {log}"


def _generator_cleans_up_on_error():
    log = []
    try:
        with tracker(log):
            raise ValueError("boom")
    except ValueError:
        assert log == ["enter", "exit"], (
            f"log was {log} — without try/finally the cleanup after `yield` is skipped"
        )
        return
    raise AssertionError("tracker() must not swallow the exception")


def _swallowing_hides_it():
    log = []
    with swallowing(log):
        raise ValueError("never seen")
    assert "swallowed" in log, f"log was {log}"


if __name__ == "__main__":
    _run([
        ("class: enter / body / exit",        _class_happy_path),
        ("class: exit runs when body raises", _class_cleans_up_on_error),
        ("@contextmanager matches",           _generator_version_matches),
        ("`as` binds the YIELDED value",      _as_binds_the_yielded_value),
        ("`as` is optional",                  _as_is_optional),
        ("@contextmanager needs try/finally", _generator_cleans_up_on_error),
        ("swallowing() hides the exception",  _swallowing_hides_it),
    ])
