"""5. JSON and what it loses

    save_json(path, obj)     write UTF-8, indent=2
    load_json(path)          read it back
    survives(obj)            -> bool: does json.loads(json.dumps(obj)) == obj?
    encode_dates(obj)        dump an object containing datetime.date, using the
                             `default=` hook, so dates become ISO strings

survives() is the point: use it on a tuple, on a dict with int keys, and on a
plain dict, and see which come back unchanged.
"""

import json
import datetime
from pathlib import Path


def save_json(path, obj):
    # ensure_ascii=False keeps "café" as itself instead of "café"
    text = json.dumps(obj, indent=2, ensure_ascii=False)
    path.write_text(text, encoding="utf-8")


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def survives(obj):
    try:
        return json.loads(json.dumps(obj)) == obj
    except TypeError:                   # not serialisable at all
        return False


def _iso(value):
    """default= is called only for values json cannot handle itself."""
    if isinstance(value, (datetime.date, datetime.datetime)):
        return value.isoformat()
    raise TypeError(f"{type(value).__name__} is not JSON serialisable")


def encode_dates(obj):
    return json.dumps(obj, default=_iso)


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



import tempfile


def _file_round_trip():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "d.json"
        obj = {"name": "café", "n": 1, "ok": True, "xs": [1, 2]}
        save_json(p, obj)
        assert load_json(p) == obj
        assert "café" in p.read_text(encoding="utf-8"), "write UTF-8"


def _plain_data_survives():
    assert survives({"a": 1, "b": [1, 2], "c": None}) is True


def _tuples_do_not():
    assert survives({"k": (1, 2)}) is False, "a tuple comes back as a list"


def _int_keys_do_not():
    assert survives({1: "a"}) is False, "JSON keys are always strings"


def _colliding_keys_lose_data():
    obj = {1: "int key", "1": "string key"}
    back = json.loads(json.dumps(obj))
    assert len(back) == 1, "two distinct keys should have collapsed into one"


def _dates_need_a_hook():
    obj = {"when": datetime.date(2026, 1, 1)}
    try:
        json.dumps(obj)
    except TypeError:
        pass
    else:
        raise AssertionError("a bare date should not be serialisable")
    assert json.loads(encode_dates(obj)) == {"when": "2026-01-01"}, (
        f"got {encode_dates(obj)}"
    )


if __name__ == "__main__":
    _run([
        ("file round-trip in UTF-8",      _file_round_trip),
        ("plain data survives",           _plain_data_survives),
        ("tuples do not survive",         _tuples_do_not),
        ("int keys do not survive",       _int_keys_do_not),
        ("colliding keys lose data",      _colliding_keys_lose_data),
        ("dates need a default= hook",    _dates_need_a_hook),
    ])
