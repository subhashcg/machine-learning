"""4. retry(fn, *args, times=3, **kwargs)

Call fn(*args, **kwargs), retrying up to `times` on exception, returning the
first success and raising if all attempts fail.

Test with a function that fails twice then succeeds. Then write retry_bad with
`times` before *args and show the argument collision — including which function
the error appears to come from.
"""


def retry(fn, *args, times=3, **kwargs):
    for trial in range(times):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            if trial < times - 1:
                print(f"Failed with error: {e}. {trial+1} try.")
            else:
                raise



def retry_bad(fn, times=3, *args, **kwargs):
    for trial in range(times):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            if trial < times - 1:
                print(f"Failed with error: {e}. {trial+1} try.")
            else:
                raise

def flaky(label):
    """Fails the first two times it is called, then succeeds."""
    flaky.calls = getattr(flaky, "calls", 0) + 1
    if flaky.calls < 3:
        raise ValueError(f"{label}: not ready (attempt {flaky.calls})")
    return f"{label}: succeeded on attempt {flaky.calls}"


def work(a, b):
    return f"work(a={a}, b={b})"


if __name__ == "__main__":
    print(retry(flaky, "job"))
    print(retry(work, 1, 2))

    try:
        print(retry_bad(work, 1, 2))
    except Exception as e:
        print(e)
