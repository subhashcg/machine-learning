"""5. retry, properly

Rewrite Topic 3's retry with what you now know about exceptions.

    retry(fn, *args, times=3, retry_on=Exception, **kwargs)

  - call fn(*args, **kwargs), returning the first success
  - retry only on `retry_on`; anything else propagates immediately
  - after the last failed attempt raise RetryError("...") FROM the last
    exception, so the traceback keeps both
  - record each failure's str() in the list `retry.log` (reset it per call)

RetryError is given. KeyboardInterrupt must never be retried — think about
what `retry_on=Exception` already guarantees.
"""


class RetryError(Exception):
    pass


def retry(fn, *args, times=3, retry_on=Exception, **kwargs):
    # TODO
    raise NotImplementedError


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



def _make_flaky(fails, exc=ValueError):
    state = {"n": 0}
    def f(label="x"):
        state["n"] += 1
        if state["n"] <= fails:
            raise exc(f"{label} attempt {state['n']}")
        return f"ok after {state['n']}"
    return f


def _succeeds_eventually():
    assert retry(_make_flaky(2), times=3) == "ok after 3"
    assert len(retry.log) == 2, f"expected 2 failures logged, got {retry.log}"


def _forwards_arguments():
    assert retry(_make_flaky(0), "job") == "ok after 1"


def _raises_retry_error_chained():
    try:
        retry(_make_flaky(99), times=2)
    except RetryError as e:
        assert isinstance(e.__cause__, ValueError), f"__cause__ was {e.__cause__!r}"
        assert len(retry.log) == 2, f"log was {retry.log}"
        return
    raise AssertionError("should raise RetryError after the last attempt")


def _non_matching_exception_propagates():
    try:
        retry(_make_flaky(99, exc=TypeError), times=5, retry_on=ValueError)
    except TypeError:
        assert len(retry.log) == 0, "a non-matching exception should not be logged or retried"
        return
    raise AssertionError("TypeError should propagate, not be retried")


def _keyboard_interrupt_is_never_retried():
    try:
        retry(_make_flaky(99, exc=KeyboardInterrupt), times=5)
    except KeyboardInterrupt:
        return
    raise AssertionError("KeyboardInterrupt is not an Exception; it must propagate")


if __name__ == "__main__":
    _run([
        ("succeeds after retries",             _succeeds_eventually),
        ("forwards *args",                     _forwards_arguments),
        ("raises RetryError chained from last", _raises_retry_error_chained),
        ("non-matching exception propagates",  _non_matching_exception_propagates),
        ("KeyboardInterrupt is never retried", _keyboard_interrupt_is_never_retried),
    ])
