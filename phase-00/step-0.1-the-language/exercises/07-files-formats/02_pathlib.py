"""2. pathlib

    describe(path)        -> dict with keys name, stem, suffix, parent (as str),
                             and is_absolute
    csv_files(directory)  -> sorted list of .csv filenames directly in it
    all_csv_files(dir)    -> sorted list of POSIX-style relative paths to every
                             .csv at any depth, e.g. ["a.csv", "sub/c.csv"]
    swap_extension(p, e)  -> the same path with a different suffix

Take and return pathlib.Path objects, not strings, except where stated.
"""

from pathlib import Path


def describe(path):
    # TODO
    raise NotImplementedError


def csv_files(directory):
    # TODO
    raise NotImplementedError


def all_csv_files(directory):
    # TODO
    raise NotImplementedError


def swap_extension(path, new_suffix):
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


def _describe_parts():
    d = describe(Path("data/raw/sales.csv"))
    assert d == {"name": "sales.csv", "stem": "sales", "suffix": ".csv",
                 "parent": "data/raw", "is_absolute": False}, f"got {d}"


def _swap_extension():
    got = swap_extension(Path("data/raw/sales.csv"), ".parquet")
    assert str(got) == "data/raw/sales.parquet", f"got {got}"
    assert isinstance(got, Path), "return a Path, not a string"


def _glob_this_level():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "sub").mkdir()
        for rel in ("a.csv", "b.csv", "notes.txt", "sub/c.csv"):
            (root / rel).write_text("x")
        assert csv_files(root) == ["a.csv", "b.csv"], f"got {csv_files(root)}"


def _glob_recursive():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "sub" / "deep").mkdir(parents=True)
        for rel in ("a.csv", "notes.txt", "sub/c.csv", "sub/deep/d.csv"):
            (root / rel).write_text("x")
        got = all_csv_files(root)
        assert got == ["a.csv", "sub/c.csv", "sub/deep/d.csv"], f"got {got}"


if __name__ == "__main__":
    _run([
        ("describe() splits a path",     _describe_parts),
        ("swap_extension returns a Path", _swap_extension),
        ("csv_files: this level only",   _glob_this_level),
        ("all_csv_files: recursive",     _glob_recursive),
    ])
