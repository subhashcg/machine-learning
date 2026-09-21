"""These tests describe what pipeline.py SHOULD do. Four of them fail.

Your job is to diagnose each failure using the tools from this topic, write
what you found in DIAGNOSIS.md, and then fix pipeline.py.

Do not change this file.

    uv run pytest phase-00/step-0.2-working-like-an-engineer/exercises/02-debugging -x -l
    uv run pytest ... --pdb
"""

import pytest

from pipeline import (
    parse_row, load_rows, total_value, apply_discount, summarise, running_totals
)

TEXT = """name,qty,price
widget,3,9.99
gadget,12,4.50
doohickey,1,100.00
"""


@pytest.fixture
def rows():
    return load_rows(TEXT)


def test_parse_row():
    assert parse_row("widget,3,9.99") == {"name": "widget", "qty": 3, "price": 9.99}


def test_load_rows_skips_header_and_blanks(rows):
    assert len(rows) == 3
    assert rows[0]["name"] == "widget"


def test_load_rows_handles_trailing_whitespace():
    rows = load_rows(" widget , 3 , 9.99 \n")
    assert rows[0] == {"name": "widget", "qty": 3, "price": 9.99}


def test_total_value(rows):
    # 3*9.99 + 12*4.50 + 1*100.00 = 29.97 + 54.00 + 100.00
    assert total_value(rows) == pytest.approx(183.97)


def test_apply_discount_reduces_qualifying_rows(rows):
    out = apply_discount(rows, percent=10)
    by_name = {r["name"]: r for r in out}
    assert by_name["gadget"]["price"] == pytest.approx(4.05)
    assert by_name["widget"]["price"] == pytest.approx(9.99)


def test_apply_discount_does_not_mutate_input(rows):
    before = [dict(r) for r in rows]
    apply_discount(rows, percent=10)
    assert rows == before, "apply_discount must not modify the rows it was given"


def test_summarise_returns_highest_first(rows):
    top = summarise(rows, top=2)
    assert [r["name"] for r in top] == ["doohickey", "gadget"]


def test_running_totals(rows):
    assert running_totals(rows) == pytest.approx([29.97, 83.97, 183.97])


def test_running_totals_is_independent_of_call_order(rows):
    first = list(running_totals(rows))      # copy: the bug returns the SAME list
    second = list(running_totals(rows))
    assert first == second, "calling it twice should give the same answer"
