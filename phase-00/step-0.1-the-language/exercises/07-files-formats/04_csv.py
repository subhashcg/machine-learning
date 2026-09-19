"""4. CSV

    naive_parse(line)     line.split(",") — the wrong way, kept for contrast
    read_rows(path)       list of dicts, via csv.DictReader
    read_typed(path)      same, but qty -> int and price -> float
    write_rows(path, rows, fieldnames)   round-trips through DictWriter

The test data has a quoted comma, escaped quotes, and a newline inside a field.
read_typed must raise on a bad number rather than guessing.
"""

import csv
from pathlib import Path


def naive_parse(line):
    # TODO
    raise NotImplementedError


def read_rows(path):
    # TODO
    raise NotImplementedError


def read_typed(path):
    # TODO
    raise NotImplementedError


def write_rows(path, rows, fieldnames):
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

TRICKY = (
    'name,note,qty,price\n'
    'Widget,"Red, large",3,9.99\n'
    '"O\'Brien","He said ""hi""",1,0.5\n'
    'Multi,"line\nbreak",2,1.0\n'
)


def _write(tmp, text=TRICKY):
    p = Path(tmp) / "t.csv"
    p.write_text(text, encoding="utf-8")
    return p


def _naive_is_wrong():
    got = naive_parse('Widget,"Red, large",3,9.99')
    assert len(got) == 5, f"splitting gives 5 pieces, not 4 fields — got {got}"


def _dictreader_handles_quoting():
    with tempfile.TemporaryDirectory() as tmp:
        rows = read_rows(_write(tmp))
        assert len(rows) == 3, f"expected 3 records, got {len(rows)}"
        assert rows[0]["note"] == "Red, large", f"got {rows[0]['note']!r}"
        assert rows[1]["note"] == 'He said "hi"', f"got {rows[1]['note']!r}"
        assert "\n" in rows[2]["note"], "a field can contain a newline"


def _everything_is_a_string():
    with tempfile.TemporaryDirectory() as tmp:
        rows = read_rows(_write(tmp))
        assert rows[0]["qty"] == "3", "csv has no types — qty comes back as a string"


def _typed_converts():
    with tempfile.TemporaryDirectory() as tmp:
        rows = read_typed(_write(tmp))
        assert rows[0]["qty"] == 3 and isinstance(rows[0]["qty"], int)
        assert rows[0]["price"] == 9.99 and isinstance(rows[0]["price"], float)


def _typed_raises_on_bad_number():
    bad = 'name,note,qty,price\nWidget,x,three,9.99\n'
    with tempfile.TemporaryDirectory() as tmp:
        try:
            read_typed(_write(tmp, bad))
        except ValueError:
            return
        raise AssertionError("a non-numeric qty should raise, not be guessed at")


def _round_trip():
    with tempfile.TemporaryDirectory() as tmp:
        src = _write(tmp)
        rows = read_rows(src)
        out = Path(tmp) / "out.csv"
        write_rows(out, rows, ["name", "note", "qty", "price"])
        assert read_rows(out) == rows, "writing then reading should give the same rows"


if __name__ == "__main__":
    _run([
        ("naive_parse gets it wrong",        _naive_is_wrong),
        ("DictReader handles the quoting",   _dictreader_handles_quoting),
        ("csv values are strings",           _everything_is_a_string),
        ("read_typed converts qty and price", _typed_converts),
        ("read_typed raises on a bad number", _typed_raises_on_bad_number),
        ("write then read round-trips",      _round_trip),
    ])
