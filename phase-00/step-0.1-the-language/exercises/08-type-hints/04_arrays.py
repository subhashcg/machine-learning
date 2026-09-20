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


def normalise(rows: list[list[float]]) -> list[list[float]]:
    """Standardise each column of a table of shape (n_samples, n_features).

    Subtracts the column mean and divides by the population std, so each column
    ends up with mean 0 and std 1. Shape is preserved.

    The hint `list[list[float]]` cannot say any of that, so it is checked here:
    at least one row, and every row the same length, else ValueError.

    A constant column has std 0, so its output is NaN. That is left visible on
    purpose — it means "this feature carries no information", and silently
    substituting 0 would hide a broken feature.
    """
    if not rows:
        raise ValueError("need at least one row")
    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise ValueError(f"ragged table: rows have lengths {sorted({len(r) for r in rows})}")

    n = len(rows)
    out = [[0.0] * width for _ in range(n)]
    for col in range(width):
        column = [row[col] for row in rows]
        mean = sum(column) / n
        std = math.sqrt(sum((x - mean) ** 2 for x in column) / n)   # population std
        for i, x in enumerate(column):
            out[i][col] = (x - mean) / std if std else math.nan
    return out


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
