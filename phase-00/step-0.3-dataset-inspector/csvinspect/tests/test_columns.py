"""Column-level decisions: D2 near-misses, D3 narrowing, D13/D15 notes.

Each test names the decision it pins down. If one of these fails, a decision
changed — which is allowed, but it should be deliberate and DESIGN.md should
change with it.
"""

import pytest


def note_matching(column, fragment):
    return next((n for n in column.notes if fragment in n), None)


# ------------------------------------------------------------------ D2

def test_one_bad_value_makes_the_column_text(one_column):
    column = one_column(["1", "2", "oops", "4"])
    assert column.kind == "text", "strict by default: the type must accept everything"


def test_the_near_miss_is_reported_with_the_offending_row(one_column):
    column = one_column(["1", "2", "oops", "4"])
    note = note_matching(column, "parse as integer")
    assert note is not None, "a demotion without an explanation is useless"
    assert "75%" in note
    assert "'oops'" in note and "row 3" in note, f"got: {note}"


def test_a_near_miss_below_half_is_not_claimed(one_column):
    column = one_column(["alpha", "beta", "gamma", "4"])
    assert column.kind == "text"
    assert note_matching(column, "parse as integer") is None


def test_tolerance_retypes_and_says_what_it_dropped(one_column):
    column = one_column(["1", "2", "oops", "4"], tolerance=0.3)
    assert column.kind == "integer"
    note = note_matching(column, "--tolerance")
    assert "1 value" in note and "row 3" in note


def test_missing_values_do_not_count_against_a_type(one_column):
    # D1 and D2 interact: "n/a" is missing, so the column is still integer.
    column = one_column(["1", "n/a", "3"])
    assert column.kind == "integer"
    assert column.n_missing == 1 and column.n_values == 2


def test_a_type_must_accept_every_value_even_at_scale(one_column):
    values = [str(i) for i in range(1, 10_000)] + ["n\\a"]
    column = one_column(values)
    assert column.kind == "text"
    assert "99.99%" in note_matching(column, "parse as integer")


# ------------------------------------------------------------------ D3

def test_a_day_above_twelve_disambiguates_the_whole_column(one_column):
    column = one_column(["03/06/2020", "29/09/2020", "01/02/2021"])
    assert column.kind == "date"
    assert column.date_format == "%d/%m/%Y"
    assert note_matching(column, "ambiguous") is None


def test_an_ambiguous_column_says_so(one_column):
    column = one_column(["03/06/2020", "01/02/2021"])
    assert column.kind == "date"
    note = note_matching(column, "ambiguous")
    assert note is not None and "%m/%d/%Y" in note


def test_mixed_date_formats_are_text_not_a_guess(one_column):
    column = one_column(["2024-01-03", "03/06/2020", "2024-05-01"])
    assert column.kind == "text", "one column, two formats: nothing can parse all of it"


def test_date_range_is_ordered_by_date_not_by_string(one_column):
    column = one_column(["2024-12-30", "2024-01-03", "2024-06-15"])
    assert str(column.low) == "2024-01-03"
    assert str(column.high) == "2024-12-30"


def test_a_long_text_column_stops_paying_for_date_parsing(one_column):
    # Behavioural, not internal: 200 non-dates must still be typed text, and the
    # give-up rule must not accidentally type them as something else.
    column = one_column([f"item-{i}" for i in range(200)])
    assert column.kind == "text"


# ------------------------------------------------------------------ D12/D13

def test_leading_zero_column_is_flagged_as_an_identifier(one_column):
    column = one_column(["01234", "00021", "90210"])
    assert column.kind == "text"
    assert note_matching(column, "leading zeros") is not None


def test_zero_one_column_is_an_integer_with_a_hint(one_column):
    column = one_column(["0", "1", "1", "0"])
    assert column.kind == "integer", "0/1 gets summed; boolean would hide that"
    assert note_matching(column, "may be a flag") is not None


def test_true_false_column_is_boolean(one_column):
    column = one_column(["true", "FALSE", "yes", "n"])
    assert column.kind == "boolean"
    assert (column.n_true, column.n_false) == (2, 2)


def test_thousands_separators_are_offered_not_assumed(one_column):
    # Quoted, because in a comma-delimited file that is the only way a comma
    # can be inside a value at all.
    column = one_column(['"1,234.50"', '"2,000"'])
    assert column.kind == "text"
    assert "--thousands" in note_matching(column, "thousands")

    opted_in = one_column(['"1,234.50"', '"2,000"'], thousands=",")
    assert opted_in.kind == "decimal"
    assert opted_in.high == pytest.approx(2000.0)


# ------------------------------------------------------------------ D15

def test_distinct_is_exact_while_it_is_small(one_column):
    column = one_column(["a", "b", "a", "c"], max_distinct=10)
    assert column.distinct == 3
    assert column.distinct_capped is False
    assert column.top_values[0] == ("a", 2)


def test_past_the_cap_counts_are_not_reported(one_column):
    column = one_column([f"value-{i}" for i in range(50)], max_distinct=10)
    assert column.distinct_capped is True
    assert column.distinct is None
    assert column.top_values == [], "biased counts are worse than no counts"
    assert note_matching(column, "not counted exactly") is not None


# ------------------------------------------------------------------ misc

def test_an_all_missing_column_has_no_type(one_column):
    column = one_column(["NA", "-", "   "])
    assert column.kind == "unknown"
    assert column.n_values == 0 and column.n_missing == 3
    assert note_matching(column, "every value is missing") is not None


def test_epoch_looking_integers_get_a_hint_not_a_type(one_column):
    column = one_column(["862493400", "1316241905", "1770042600"])
    assert column.kind == "integer", "a guess must never become the type"
    assert note_matching(column, "Unix-epoch-seconds") is not None


def test_ordinary_integers_get_no_epoch_hint(one_column):
    column = one_column(["1", "2", "3", "4000"])
    assert note_matching(column, "Unix-epoch") is None


def test_whitespace_around_values_is_not_data(one_column):
    column = one_column([" 3 ", "\t4", "5  "])
    assert column.kind == "integer"
    assert column.low == 3 and column.high == 5


def test_a_blank_line_and_an_empty_value_are_indistinguishable(write_csv):
    """A real limit, recorded rather than papered over.

    In a single-column file, a row whose only value is empty is byte-identical
    to a blank separator line. `csv` yields `[]` for both, and this tool drops
    them as blank lines — so such a file reports fewer rows than a spreadsheet
    would show. With two or more columns the ambiguity disappears.
    """
    from csvinspect import inspect_file

    one = inspect_file(write_csv("col\nA\n\nB\n"))
    assert one.n_rows == 2, "the empty row vanished — nothing in the file distinguishes it"

    two = inspect_file(write_csv("a,b\nA,1\n,\nB,3\n"))
    assert two.n_rows == 3, "with a delimiter present, an empty row is still a row"
    assert two.columns[0].n_missing == 1


def test_huge_integers_keep_their_exact_value(one_column):
    """Above 2**53 a float cannot tell neighbouring integers apart.

    Snowflake ids, some account numbers and nanosecond timestamps live up here,
    and a range that is off by one is a range that is wrong.
    """
    biggest = 9_007_199_254_740_993          # 2**53 + 1; float() rounds this down
    column = one_column(["1", str(biggest)])
    assert column.kind == "integer"
    assert column.high == biggest, "the range must not go through a float"
    assert isinstance(column.high, int)
