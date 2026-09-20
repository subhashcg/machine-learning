"""4. Where hints run out

normalise(rows, means) standardises a table held as a list of lists — no numpy,
but the same problem: the TYPE cannot express shape.

    normalise(rows) -> list[list[float]]
        rows: (n_samples, n_features)
        subtract each column's mean, divide by its (population) std

The hint `list[list[float]]` permits a ragged table, an empty one, and a
transposed one. So assert what the type cannot:

    - every row the same length              -> ValueError
    - at least one row                       -> ValueError
    - a constant column produces NaN         -> document it, do not hide it

Write the docstring saying what shape it expects and what NaN means.
"""

import math


def normalise(rows):
    # TODO — annotate, assert the shape, then compute
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



def _normalises_columns():
    out = normalise([[1.0, 10.0], [3.0, 30.0]])
    assert out == [[-1.0, -1.0], [1.0, 1.0]], f"got {out}"


def _annotated_and_documented():
    a = normalise.__annotations__
    assert "rows" in a and "return" in a, "annotate both"
    doc = (normalise.__doc__ or "").lower()
    assert "n_samples" in doc or "shape" in doc, "say what shape it expects"
    assert "nan" in doc, "say what a constant column does"


def _ragged_is_rejected():
    try:
        normalise([[1.0, 2.0], [3.0]])
    except ValueError:
        return
    raise AssertionError("a ragged table should raise ValueError, not be guessed at")


def _empty_is_rejected():
    try:
        normalise([])
    except ValueError:
        return
    raise AssertionError("an empty table should raise ValueError")


def _constant_column_is_nan():
    out = normalise([[5.0, 1.0], [5.0, 3.0]])
    assert math.isnan(out[0][0]), f"a constant column has std 0 -> NaN, got {out}"
    assert out[0][1] == -1.0, f"the other column should still be fine, got {out}"


def _hint_does_not_catch_the_shape():
    import typing
    a = normalise.__annotations__["rows"]
    assert "list" in str(a), f"got {a!r}"
    # the point: this same hint would accept a ragged or empty table
    assert True


if __name__ == "__main__":
    _run([
        ("normalises each column",        _normalises_columns),
        ("annotated, and shape documented", _annotated_and_documented),
        ("ragged table raises",           _ragged_is_rejected),
        ("empty table raises",            _empty_is_rejected),
        ("constant column gives NaN",     _constant_column_is_nan),
        ("the hint alone would allow both", _hint_does_not_catch_the_shape),
    ])
