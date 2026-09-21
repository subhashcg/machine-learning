"""Decisions about a single string, made before anything knows about columns.

Everything here is a pure function of one cell: is it missing (D1), and what
could it be? The rules that were argued for in DESIGN.md live here, so they can
be tested one at a time without a file, a column, or a CSV in sight.
"""

from __future__ import annotations

from datetime import date, datetime

# D1 — what counts as missing. Compared after stripping and lowercasing, so
# " NA " and "n/a" are both caught. "" also covers whitespace-only cells.
DEFAULT_NA_VALUES = frozenset({
    "", "na", "n/a", "#n/a", "nan", "null", "none", "nil", "-", "?",
})

# D13 — only words are boolean. 0/1 stays integer, because 0/1 gets summed.
TRUE_WORDS = frozenset({"true", "t", "yes", "y"})
FALSE_WORDS = frozenset({"false", "f", "no", "n"})

# D3 — the whitelist, in priority order. Unambiguous formats first, so that a
# column which fits several is reported under the least surprising one.
DATE_FORMATS: tuple[str, ...] = (
    "%Y-%m-%d",
    "%Y/%m/%d",
    "%Y%m%d",
    "%d/%m/%Y",
    "%m/%d/%Y",
    "%d-%m-%Y",
    "%m-%d-%Y",
    "%d.%m.%Y",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M:%SZ",
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%dT%H:%M:%S.%fZ",
    "%Y-%m-%d %H:%M",
    "%d/%m/%Y %H:%M:%S",
    "%m/%d/%Y %H:%M:%S",
)

# Formats that are only distinguishable from each other by a day > 12 (D3).
_DAY_MONTH_AMBIGUOUS = {
    "%d/%m/%Y": "%m/%d/%Y",
    "%m/%d/%Y": "%d/%m/%Y",
    "%d-%m-%Y": "%m-%d-%Y",
    "%m-%d-%Y": "%d-%m-%Y",
}

_NUMERIC_LEAD = frozenset("+-.0123456789")


def is_missing(raw: str, na_values: frozenset[str] = DEFAULT_NA_VALUES) -> bool:
    """D1. Missing is empty, whitespace-only, or a known placeholder."""
    return raw.strip().lower() in na_values


def parse_boolean(text: str) -> bool | None:
    """D13. Words only — `true`/`yes`/`t`/`y` and their negatives."""
    lowered = text.strip().lower()
    if lowered in TRUE_WORDS:
        return True
    if lowered in FALSE_WORDS:
        return False
    return None


def has_leading_zero(text: str) -> bool:
    """D12. `007` is an identifier, not the number seven.

    A redundant leading zero is one followed by another digit: `007`, `01234`,
    `00.5`. `0`, `0.5` and `-0.75` are ordinary numbers and are not caught.
    """
    body = text[1:] if text[:1] in "+-" else text
    return len(body) > 1 and body[0] == "0" and body[1].isdigit() and body.isascii()


def parse_integer(text: str) -> int | None:
    """Digits, with an optional sign. Leading zeros disqualify it (D12).

    `str.isdigit()` is true for non-ASCII digits such as '٣', which `int()` would
    happily accept; the `isascii()` guard keeps those as text, because a column
    of Arabic-Indic digits is not something to silently arithmetic on.
    """
    body = text[1:] if text[:1] in "+-" else text
    if not body or not body.isascii() or not body.isdigit():
        return None
    if len(body) > 1 and body[0] == "0":
        return None
    return int(text)


def parse_decimal(text: str) -> float | None:
    """A finite number. No thousands separators, no currency, no inf/nan (D14).

    `float()` accepts 'inf' and 'nan' as words; those are rejected here, since a
    column containing the literal text 'nan' is either missing data (D1 caught it
    already) or a column of words.
    """
    if not text or text[0] not in _NUMERIC_LEAD or not text.isascii():
        return None
    if has_leading_zero(text):
        # D12 again: float("01234") is 1234.0, which is how zip codes die.
        return None
    try:
        value = float(text)
    except ValueError:
        return None
    if value != value or value in (float("inf"), float("-inf")):
        return None
    return value


def parse_decimal_with_thousands(text: str, separator: str) -> float | None:
    """D14. Only used when the user opted in with --thousands."""
    return parse_decimal(text.replace(separator, ""))


def _fixed_width_date(text: str, year_first: bool, day_first: bool, sep: str):
    """Hand-rolled parser for the four common all-numeric layouts.

    `strptime` costs roughly 7 µs per call and this costs about 0.5. It is worth
    the duplication only because every value of every date column goes through
    it; anything it cannot handle (an unpadded month, say) returns None and the
    caller falls back to `strptime`, so correctness never depends on it.
    """
    if len(text) != 10 or not text.isascii():
        return None
    if year_first:
        year, month, day = text[0:4], text[5:7], text[8:10]
        separators = (text[4], text[7])
    elif day_first:
        day, month, year = text[0:2], text[3:5], text[6:10]
        separators = (text[2], text[5])
    else:
        month, day, year = text[0:2], text[3:5], text[6:10]
        separators = (text[2], text[5])
    if separators != (sep, sep):
        return None
    if not (year.isdigit() and month.isdigit() and day.isdigit()):
        return None
    try:
        return date(int(year), int(month), int(day))
    except ValueError:                      # 2024-02-30 and friends
        return None


_FAST_PARSERS = {
    "%Y-%m-%d": lambda t: _fixed_width_date(t, True, False, "-"),
    "%Y/%m/%d": lambda t: _fixed_width_date(t, True, False, "/"),
    "%d/%m/%Y": lambda t: _fixed_width_date(t, False, True, "/"),
    "%m/%d/%Y": lambda t: _fixed_width_date(t, False, False, "/"),
    "%d-%m-%Y": lambda t: _fixed_width_date(t, False, True, "-"),
    "%m-%d-%Y": lambda t: _fixed_width_date(t, False, False, "-"),
}


def parse_date(text: str, fmt: str) -> date | datetime | None:
    """Parse under one known format. Dates without a time come back as `date`."""
    fast = _FAST_PARSERS.get(fmt)
    if fast is not None:
        parsed = fast(text)
        if parsed is not None:
            return parsed
        # Fall through: strptime also accepts unpadded forms like 2024-1-3.
    try:
        parsed = datetime.strptime(text, fmt)
    except ValueError:
        return None
    has_time = any(part in fmt for part in ("%H", "%M", "%S"))
    return parsed if has_time else parsed.date()


def match_and_parse(
    text: str, candidates: tuple[str, ...] = DATE_FORMATS
) -> tuple[tuple[str, ...], date | datetime | None]:
    """Every candidate format that parses `text`, plus the value under the first.

    Returning all of them, rather than the first, is what makes D3's ambiguity
    warning possible: a column keeps the intersection across its values, so
    03/06/2020 leaves two formats alive and 13/06/2020 leaves one. Returning the
    parsed value alongside them means each date is parsed once, not twice.
    """
    if len(text) < 6 or len(text) > 32 or not any(c.isdigit() for c in text):
        return (), None
    matched: list[str] = []
    value = None
    for fmt in candidates:
        parsed = parse_date(text, fmt)
        if parsed is None:
            continue
        if value is None:
            value = parsed
        matched.append(fmt)
    return tuple(matched), value


def date_formats_matching(text: str, candidates: tuple[str, ...] = DATE_FORMATS) -> tuple[str, ...]:
    """Just the formats — the shape used by header sniffing and by tests."""
    return match_and_parse(text, candidates)[0]


def ambiguous_partner(fmt: str) -> str | None:
    """The format `fmt` cannot be told apart from, when every day is <= 12."""
    return _DAY_MONTH_AMBIGUOUS.get(fmt)
