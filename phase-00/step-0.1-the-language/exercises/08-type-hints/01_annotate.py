"""1. Annotate, and see that nothing enforces it

Annotate these four functions. The checks read __annotations__, so the hints
themselves are what is being tested.

    word_count(text)          str -> dict[str, int]
    first_or_none(items)      list[int] -> int | None      (None when empty)
    scale(xs, factor)         list[float], float -> list[float]
    shout(text, times)        str, int=1 -> str            (upper, repeated)

Then `ignores_types()`: call one of them with the WRONG type and return the
result, to show Python does not care.
"""


def word_count(text):
    # TODO — annotate and implement
    raise NotImplementedError


def first_or_none(items):
    # TODO
    raise NotImplementedError


def scale(xs, factor):
    # TODO
    raise NotImplementedError


def shout(text, times=1):
    # TODO
    raise NotImplementedError


def ignores_types():
    """Call scale() with a list of strings and return whatever comes back."""
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



def _they_work():
    assert word_count("a b a") == {"a": 2, "b": 1}
    assert first_or_none([3, 1]) == 3
    assert first_or_none([]) is None
    assert scale([1.0, 2.0], 3.0) == [3.0, 6.0]
    assert shout("hi", 2) == "HIHI"
    assert shout("hi") == "HI"


def _annotations_present():
    for fn in (word_count, first_or_none, scale, shout):
        a = fn.__annotations__
        params = [p for p in fn.__code__.co_varnames[:fn.__code__.co_argcount]]
        missing = [p for p in params if p not in a]
        assert not missing, f"{fn.__name__} is missing hints for {missing}"
        assert "return" in a, f"{fn.__name__} has no return hint"


def _optional_is_declared():
    import typing
    r = first_or_none.__annotations__["return"]
    assert type(None) in typing.get_args(r), (
        f"first_or_none returns None sometimes; say so. Got {r!r}"
    )


def _default_is_not_a_hint():
    a = shout.__annotations__
    assert a["times"] is int, (
        f"times has a default but is always an int — hint it `int`, not `int | None`. Got {a['times']!r}"
    )


def _runtime_ignores_them():
    got = ignores_types()
    assert got is not None, "it should return something, not raise"
    assert got == ["aa", "bb"] or got == ["a", "b"] * 1 or isinstance(got, list), (
        f"scale() with strings still ran and gave {got!r} — annotations are not enforced"
    )


if __name__ == "__main__":
    _run([
        ("the four functions work",        _they_work),
        ("every parameter and return hinted", _annotations_present),
        ("first_or_none declares | None",  _optional_is_declared),
        ("a default is not the same as | None", _default_is_not_a_hint),
        ("runtime ignores the hints",      _runtime_ignores_them),
    ])
