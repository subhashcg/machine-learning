"""3. Chaining

load_port(raw) parses an int and wraps failure in ConfigError:

    wrapped(raw)    raise ConfigError(...) from e     -> __cause__ is the ValueError
    implicit(raw)   raise ConfigError(...)            -> __context__ set, __cause__ None
    hidden(raw)     raise ConfigError(...) from None  -> both suppressed

All three take a string and return int(raw) when it parses.
"""


class ConfigError(Exception):
    pass


def wrapped(raw):
    # TODO
    raise NotImplementedError


def implicit(raw):
    # TODO
    raise NotImplementedError


def hidden(raw):
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



def _all_parse_good_input():
    for fn in (wrapped, implicit, hidden):
        assert fn("8080") == 8080, f"{fn.__name__} should return the int"


def _from_e_sets_cause():
    try:
        wrapped("nope")
    except ConfigError as e:
        assert isinstance(e.__cause__, ValueError), f"__cause__ was {e.__cause__!r}"
        return
    raise AssertionError("should have raised ConfigError")


def _implicit_sets_context_only():
    try:
        implicit("nope")
    except ConfigError as e:
        assert e.__cause__ is None, "no `from`, so __cause__ should be None"
        assert isinstance(e.__context__, ValueError), f"__context__ was {e.__context__!r}"
        return
    raise AssertionError("should have raised ConfigError")


def _from_none_suppresses():
    try:
        hidden("nope")
    except ConfigError as e:
        assert e.__cause__ is None
        assert e.__suppress_context__ is True, "`from None` sets __suppress_context__"
        return
    raise AssertionError("should have raised ConfigError")


if __name__ == "__main__":
    _run([
        ("all three parse valid input",       _all_parse_good_input),
        ("`from e` sets __cause__",           _from_e_sets_cause),
        ("plain raise sets __context__ only", _implicit_sets_context_only),
        ("`from None` suppresses",            _from_none_suppresses),
    ])
