"""5. Point and Config

Point(x, y) as a @dataclass, y defaulting to 0.0.

Config as a @dataclass with three fields, all via field(default_factory=...):
    names   an empty list
    lookup  an empty dict
    limits  a list defaulting to [0, 100]

bad_dataclass_error() should attempt to define a dataclass with a mutable
default (`tags: list = []`) inside a try, and return the ValueError's message.

Then a comment: what test is the dataclass actually applying?
"""

from dataclasses import dataclass, field

@dataclass
class Point:
    x: float
    y: float = 0.0

@dataclass
class Config:
    names: list = field(default_factory=list)
    lookup: dict = field(default_factory=dict)
    limits: list = field(default_factory=lambda: [0, 100])


def bad_dataclass_error():
    """Attempt a dataclass with `tags: list = []`; return the error message."""
    try:
        @dataclass
        class Bad:
            tags: list = []
    except ValueError as e:
        return str(e)


# The test is "is the default's type unhashable?" — in 3.11+ it checks
# `type(default).__hash__ is None` (older versions only checked for exactly
# list, dict or set). Unhashable is used as a stand-in for "mutable": list,
# dict, set and any class that defines __eq__ without __hash__ get rejected.
# It's a heuristic, not a real mutability check — a mutable object whose class
# is still hashable (a plain custom class instance, say) slips through and is
# shared across every instance, just like the classic `def f(x=[])` bug.


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



def _generated_methods():
    p = Point(1, 2)
    assert repr(p) == "Point(x=1, y=2)", f"repr was {repr(p)!r}"
    assert Point(1, 2) == Point(1, 2), "__eq__ should compare by value"
    assert Point(1) == Point(1, 0.0), "y should default to 0.0"


def _defaults_are_per_instance():
    a, b = Config(), Config()
    assert a.names == [] and a.lookup == {} and a.limits == [0, 100], f"{a}"
    a.names.append("x"); a.lookup["k"] = 1; a.limits.append(200)
    assert b.names == [], "the second Config should be untouched"
    assert b.lookup == {}, "the second Config should be untouched"
    assert b.limits == [0, 100], "the second Config should be untouched"
    assert a.names is not b.names, "each instance needs its own list"


def _mutable_default_is_rejected():
    msg = bad_dataclass_error()
    assert msg is not None, "defining it should have raised — return the message"
    assert "default_factory" in msg, f"unexpected message: {msg!r}"


if __name__ == "__main__":
    _run([
        ("@dataclass generates __init__/__repr__/__eq__", _generated_methods),
        ("default_factory gives each instance its own",   _defaults_are_per_instance),
        ("a mutable default is a hard error",             _mutable_default_is_rejected),
    ])
