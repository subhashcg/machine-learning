"""Per-value rules: D1 (missing), D12 (leading zeros), D13 (booleans), D14 (numbers).

These are the decisions the whole report rests on, so they are tested one cell
at a time, where a failure names the rule rather than a column.
"""

import pytest

from csvinspect.values import (
    DEFAULT_NA_VALUES,
    ambiguous_partner,
    date_formats_matching,
    has_leading_zero,
    is_missing,
    parse_boolean,
    parse_decimal,
    parse_decimal_with_thousands,
    parse_integer,
)


# ------------------------------------------------------------------ D1

@pytest.mark.parametrize("cell", ["", "   ", "\t", "NA", "na", " n/a ", "NULL", "None", "-", "?", "NaN"])
def test_placeholders_count_as_missing(cell):
    assert is_missing(cell) is True


@pytest.mark.parametrize("cell", ["0", "false", "nan value", "N.A.", "--", "n/a/b"])
def test_real_values_are_not_missing(cell):
    assert is_missing(cell) is False


def test_missing_list_is_replaceable():
    # D1's escape hatch: "NA" is Namibia in a country column.
    assert is_missing("NA", frozenset({""})) is False
    assert is_missing("", frozenset({""})) is True


def test_default_list_is_lowercase_so_comparison_is_case_insensitive():
    assert all(value == value.lower() for value in DEFAULT_NA_VALUES)


# ------------------------------------------------------------------ D12

@pytest.mark.parametrize("cell", ["007", "01234", "00021", "-007", "00.5"])
def test_leading_zeros_are_identifiers(cell):
    assert has_leading_zero(cell) is True
    assert parse_integer(cell) is None, "an identifier must not become an int"
    assert parse_decimal(cell) is None, "float('01234') == 1234.0 is how zip codes die"


@pytest.mark.parametrize("cell", ["0", "0.5", "-0.75", "0.0", "7"])
def test_an_ordinary_zero_is_still_a_number(cell):
    assert has_leading_zero(cell) is False
    assert parse_decimal(cell) is not None


# ------------------------------------------------------------------ D13

@pytest.mark.parametrize("cell, expected", [
    ("true", True), ("TRUE", True), ("t", True), ("Yes", True), ("y", True),
    ("false", False), ("F", False), ("no", False), ("N", False),
])
def test_boolean_words(cell, expected):
    assert parse_boolean(cell) is expected


@pytest.mark.parametrize("cell", ["0", "1", "2", "on", "off", ""])
def test_zero_and_one_are_not_booleans(cell):
    # D13: 0/1 stays integer because 0/1 columns get summed.
    assert parse_boolean(cell) is None


# ------------------------------------------------------------------ D14

@pytest.mark.parametrize("cell", ["1,234.50", "$19.99", "19.99 USD", "1 234", "(500)"])
def test_decorated_numbers_are_not_numbers(cell):
    assert parse_decimal(cell) is None


def test_thousands_separator_is_opt_in():
    assert parse_decimal("1,234.50") is None
    assert parse_decimal_with_thousands("1,234.50", ",") == 1234.50


@pytest.mark.parametrize("cell", ["inf", "-inf", "Infinity", "nan"])
def test_infinity_and_nan_are_not_finite_numbers(cell):
    # float() accepts all of these; a column of them is words, not quantities.
    assert parse_decimal(cell) is None


def test_non_ascii_digits_stay_text():
    # int('٣') is 3. A column of Arabic-Indic digits should not silently
    # become arithmetic.
    assert parse_integer("٣") is None
    assert parse_decimal("٣") is None


@pytest.mark.parametrize("cell, expected", [
    ("42", 42), ("-7", -7), ("+3", 3), ("1000000", 1_000_000),
])
def test_plain_integers(cell, expected):
    assert parse_integer(cell) == expected


def test_scientific_notation_is_a_number():
    assert parse_decimal("1e5") == 100_000.0


# ------------------------------------------------------------------ D3

def test_iso_dates_are_unambiguous():
    matched = date_formats_matching("2024-03-06")
    assert matched == ("%Y-%m-%d",)


def test_slash_dates_are_ambiguous_until_a_day_above_twelve():
    both = date_formats_matching("03/06/2020")
    assert "%d/%m/%Y" in both and "%m/%d/%Y" in both, "the file does not say which"

    only_one = date_formats_matching("29/09/2020")
    assert only_one == ("%d/%m/%Y",), "day 29 rules out month-first"


def test_ambiguous_partner_pairs_are_symmetric():
    assert ambiguous_partner("%d/%m/%Y") == "%m/%d/%Y"
    assert ambiguous_partner("%m/%d/%Y") == "%d/%m/%Y"
    assert ambiguous_partner("%Y-%m-%d") is None


@pytest.mark.parametrize("cell", ["not a date", "2024", "13/13/2020", "2024-02-30"])
def test_non_dates(cell):
    # 2024-02-30 does not exist; strptime rejects it, and so do we.
    assert date_formats_matching(cell) == ()


def test_leap_day_is_a_date():
    assert date_formats_matching("2024-02-29") == ("%Y-%m-%d",)
