"""3. Encoding

    save(path, text)              write UTF-8
    load(path)                    read UTF-8
    load_as(path, encoding)       read with whatever encoding is asked for

Then `round_trips(path, text, encoding)` -> bool: write UTF-8, read back with
`encoding`, and report whether the text survived. Use it to show that latin-1
does NOT raise — it just returns the wrong string.
"""

from pathlib import Path


def save(path, text):
    # TODO
    raise NotImplementedError


def load(path):
    # TODO
    raise NotImplementedError


def load_as(path, encoding):
    # TODO
    raise NotImplementedError


def round_trips(path, text, encoding):
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



import tempfile

TEXT = "café ☕ naïve"


def _utf8_round_trip():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "t.txt"
        save(p, TEXT)
        assert load(p) == TEXT, f"got {load(p)!r}"


def _latin1_is_silently_wrong():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "t.txt"
        save(p, TEXT)
        got = load_as(p, "latin-1")
        assert got != TEXT, "latin-1 should NOT give back the original"
        assert "Ã" in got, f"expected mojibake, got {got!r}"


def _ascii_raises():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "t.txt"
        save(p, TEXT)
        try:
            load_as(p, "ascii")
        except UnicodeDecodeError:
            return
        raise AssertionError("ascii cannot represent these bytes; it should raise")


def _round_trips_reports_correctly():
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp) / "t.txt"
        assert round_trips(p, TEXT, "utf-8") is True
        assert round_trips(p, TEXT, "latin-1") is False, (
            "latin-1 does not raise — it silently returns different text"
        )


if __name__ == "__main__":
    _run([
        ("utf-8 round-trips",              _utf8_round_trip),
        ("latin-1 is silently wrong",      _latin1_is_silently_wrong),
        ("ascii raises UnicodeDecodeError", _ascii_raises),
        ("round_trips() reports both",     _round_trips_reports_correctly),
    ])
