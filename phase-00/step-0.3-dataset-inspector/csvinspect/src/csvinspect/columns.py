"""One accumulator per column: sees every value once, keeps bounded memory.

This is where the type decisions from DESIGN.md are actually made. The rule is
D2: a type must accept *every* non-missing value, and when it nearly does, the
near-miss is reported rather than rounded away. Nothing here formats output and
nothing here reads a file; `add()` takes a raw cell and a row number, and
`finalize()` turns everything seen into a `ColumnSummary`.

Memory per column: a handful of counters, at most `max_distinct` keys, and at
most `reservoir_size` floats. Neither grows with the number of rows.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timezone

from csvinspect.options import Options
from csvinspect.stats import Reservoir, RunningStats, histogram
from csvinspect.values import (
    ambiguous_partner,
    has_leading_zero,
    match_and_parse,
    parse_boolean,
    parse_decimal,
    parse_decimal_with_thousands,
    parse_integer,
    DATE_FORMATS,
)

# If nothing in the first N values looks like a date, stop trying strptime on
# every cell. Date parsing is by far the most expensive test, and a column that
# is going to be a date says so immediately.
_DATE_GIVE_UP_AFTER = 50

KIND_UNKNOWN = "unknown"
KIND_TEXT = "text"


@dataclass
class ColumnSummary:
    """Everything the renderer needs. No strings formatted for display yet."""

    name: str
    kind: str
    n_values: int
    n_missing: int
    notes: list[str] = field(default_factory=list)

    # numeric / date range, already ordered
    low: float | date | datetime | None = None
    high: float | date | datetime | None = None
    mean: float | None = None
    stdev: float | None = None
    bins: list[int] | None = None
    bins_exact: bool = True
    is_integral: bool = False

    # categorical
    distinct: int | None = None
    distinct_capped: bool = False
    top_values: list[tuple[str, int]] = field(default_factory=list)
    n_true: int = 0
    n_false: int = 0

    date_format: str | None = None

    @property
    def n_rows(self) -> int:
        return self.n_values + self.n_missing


class ColumnAccumulator:
    """Streaming state for one column."""

    def __init__(self, name: str, options: Options) -> None:
        self.name = name
        self.options = options

        self.n_values = 0
        self.n_missing = 0

        # How many non-missing values each candidate type accepted (D2), and the
        # first value that it rejected, so the warning can name a row.
        self.ok: dict[str, int] = {"boolean": 0, "integer": 0, "decimal": 0, "date": 0}
        self.first_bad: dict[str, tuple[int, str]] = {}

        # D3: formats still viable for every value parsed so far.
        self.date_candidates: tuple[str, ...] = DATE_FORMATS
        self.date_low: date | datetime | None = None
        self.date_high: date | datetime | None = None

        self.numbers = RunningStats()
        self.reservoir = Reservoir(size=options.reservoir_size, seed=options.seed)

        # D15: exact while small, then frozen.
        self.distinct: dict[str, int] = {}
        self.distinct_capped = False

        self.n_true = 0
        self.n_false = 0
        self.n_digit_like = 0
        self._boolean_dead = False
        # Kept as ints, not floats: above 2**53 a float cannot represent
        # consecutive integers, and a 19-digit id would print as its neighbour.
        self.int_low: int | None = None
        self.int_high: int | None = None
        self.n_leading_zero = 0
        self.n_thousands_only = 0

    # ---------------------------------------------------------------- ingest

    def add(self, raw: str, row_number: int) -> None:
        """Take one cell. Surrounding whitespace is not data (see D1).

        This runs once per cell in the file, so the D1 test from `values` is
        inlined here rather than called: stripping and lowering twice per value
        is measurable at a few million cells.
        """
        text = raw.strip()
        if not text or text.lower() in self.options.na_values:
            self.n_missing += 1
            return

        self.n_values += 1
        self._count_distinct(text)
        if not self._boolean_dead:
            self._test_boolean(text, row_number)
        self._test_numbers(text, row_number)
        self._test_date(text, row_number)

    def _count_distinct(self, text: str) -> None:
        if text in self.distinct:
            self.distinct[text] += 1
        elif len(self.distinct) < self.options.max_distinct:
            self.distinct[text] = 1
        else:
            # Past the cap new values are not tracked at all; counts for the
            # values already held are therefore biased toward the start of the
            # file, which is why finalize() stops reporting them (D15).
            self.distinct_capped = True

    def _test_boolean(self, text: str, row_number: int) -> None:
        flag = parse_boolean(text)
        if flag is None:
            self.first_bad.setdefault("boolean", (row_number, text))
            # Same give-up rule as dates: a boolean column says so at once, and
            # a near-miss percentage for booleans would mean nothing anyway.
            if self.ok["boolean"] == 0 and self.n_values > _DATE_GIVE_UP_AFTER:
                self._boolean_dead = True
            return
        self.ok["boolean"] += 1
        if flag:
            self.n_true += 1
        else:
            self.n_false += 1

    def _test_numbers(self, text: str, row_number: int) -> None:
        body = text[1:] if text[:1] in "+-" else text
        if body.isascii() and body.isdigit():
            self.n_digit_like += 1
        if has_leading_zero(text):
            self.n_leading_zero += 1

        whole = parse_integer(text)
        if whole is None:
            self.first_bad.setdefault("integer", (row_number, text))
            number = parse_decimal(text)
        else:
            self.ok["integer"] += 1
            if self.int_low is None or whole < self.int_low:
                self.int_low = whole
            if self.int_high is None or whole > self.int_high:
                self.int_high = whole
            # Anything that parsed as an int is a decimal too; re-parsing the
            # same string through float() would be pure waste.
            number = float(whole)

        if number is None and self.options.thousands:
            number = parse_decimal_with_thousands(text, self.options.thousands)
        if number is None:
            self.first_bad.setdefault("decimal", (row_number, text))
            # D14: would it be a number if the comma were a thousands separator?
            if "," in text and parse_decimal_with_thousands(text, ",") is not None:
                self.n_thousands_only += 1
            return

        self.ok["decimal"] += 1
        self.numbers.add(number)
        self.reservoir.add(number)

    def _test_date(self, text: str, row_number: int) -> None:
        if not self.date_candidates:
            return
        if self.ok["date"] == 0 and self.n_values > _DATE_GIVE_UP_AFTER:
            self.date_candidates = ()          # not a date column; stop paying for it
            return

        matched, parsed = match_and_parse(text, self.date_candidates)
        if not matched:
            self.first_bad.setdefault("date", (row_number, text))
            return

        self.ok["date"] += 1
        # Narrowing, never widening: a format survives only while it has parsed
        # every value seen so far. This is what leaves exactly one format alive
        # the first time a day above 12 appears.
        self.date_candidates = matched

        # `parsed` came back from the same call that found the formats, under
        # this value's highest-priority one. In an ambiguous column (D3) that
        # choice is itself the ambiguity, which is why the summary carries the
        # warning alongside the range.
        if parsed is None:
            return
        if self.date_low is None or parsed < self.date_low:
            self.date_low = parsed
        if self.date_high is None or parsed > self.date_high:
            self.date_high = parsed

    # -------------------------------------------------------------- finalize

    def finalize(self) -> ColumnSummary:
        n = self.n_values
        if n == 0:
            reason = (
                "every value is missing — nothing to infer a type from"
                if self.n_missing
                else "no data rows"
            )
            return ColumnSummary(
                name=self.name,
                kind=KIND_UNKNOWN,
                n_values=0,
                n_missing=self.n_missing,
                notes=[reason],
            )

        kind, notes = self._decide_kind(n)
        summary = ColumnSummary(
            name=self.name,
            kind=kind,
            n_values=n,
            n_missing=self.n_missing,
            notes=notes,
            distinct=None if self.distinct_capped else len(self.distinct),
            distinct_capped=self.distinct_capped,
        )

        if kind in ("integer", "decimal"):
            self._fill_numeric(summary, integral=kind == "integer")
        elif kind == "date":
            summary.low, summary.high = self.date_low, self.date_high
            summary.date_format = self.date_candidates[0] if self.date_candidates else None
        elif kind == "boolean":
            summary.n_true, summary.n_false = self.n_true, self.n_false
        else:
            self._fill_categorical(summary)
        return summary

    def _decide_kind(self, n: int) -> tuple[str, list[str]]:
        """D2. A type must accept everything; a near miss is reported, not used."""
        notes: list[str] = []
        ordered = [(kind, self.ok[kind]) for kind in ("boolean", "integer", "decimal", "date")]

        exact = [kind for kind, count in ordered if count == n]
        if exact:
            kind = exact[0]
            notes.extend(self._notes_for(kind, n))
            return kind, notes

        best_kind, best_count = max(ordered, key=lambda pair: pair[1])
        share = best_count / n
        failures = n - best_count

        if self.options.tolerance > 0 and share >= 1 - self.options.tolerance:
            notes.append(
                f"typed {best_kind} under --tolerance: {_plural(failures, 'value')} "
                f"did not parse{self._first_bad_phrase(best_kind)} and "
                f"{'is' if failures == 1 else 'are'} excluded from the summary"
            )
            notes.extend(self._notes_for(best_kind, n))
            return best_kind, notes

        if best_count and share >= 0.5:
            verb = "does not" if failures == 1 else "do not"
            notes.append(
                f"{_percent(share)} parse as {best_kind}; "
                f"{_plural(failures, 'value')} {verb}"
                f"{self._first_bad_phrase(best_kind)}"
            )
        notes.extend(self._notes_for(KIND_TEXT, n))
        return KIND_TEXT, notes

    def _notes_for(self, kind: str, n: int) -> list[str]:
        notes: list[str] = []
        if kind == "text":
            # D12 — digits that are not quantities.
            if self.n_digit_like == n and self.n_leading_zero:
                notes.append(
                    "numeric with leading zeros — looks like an identifier, "
                    "not a number (kept as text)"
                )
            # D14 — numbers wearing thousands separators.
            if self.n_thousands_only and self.ok["decimal"] + self.n_thousands_only == n:
                notes.append(
                    "every value is a number if ',' is a thousands separator "
                    "— re-run with --thousands ,"
                )
        if kind == "integer":
            # D13 — a flag that is still arithmetic.
            if set(self.distinct) <= {"0", "1"} and not self.distinct_capped:
                notes.append("only 0 and 1 — this may be a flag rather than a quantity")
            if self.ok["date"] == n and self.date_candidates:
                notes.append(
                    f"also parses as {self.date_candidates[0]} dates — "
                    "typed integer because every value is a plain number"
                )
            elif self._looks_like_epoch_seconds():
                low = datetime.fromtimestamp(self.numbers.minimum, timezone.utc).date()
                high = datetime.fromtimestamp(self.numbers.maximum, timezone.utc).date()
                notes.append(
                    f"values sit in the Unix-epoch-seconds range — as timestamps "
                    f"this would be {low} … {high}"
                )
        if kind == "date" and self.date_candidates:
            chosen = self.date_candidates[0]
            partner = ambiguous_partner(chosen)
            if partner and partner in self.date_candidates:
                notes.append(
                    f"format is ambiguous: {partner} fits every value too — "
                    f"the file does not say which is meant"
                )
            elif len(self.date_candidates) > 1:
                others = ", ".join(self.date_candidates[1:])
                notes.append(f"these formats also fit every value: {others}")
        return notes

    def _looks_like_epoch_seconds(self) -> bool:
        """A heuristic, reported as a possibility and never used as the type.

        Bounded to 1980-2035 so that ordinary counts, prices and IDs do not
        collect a spurious timestamp note.
        """
        low, high = self.numbers.minimum, self.numbers.maximum
        if low is None or high is None or self.n_values < 3:
            return False
        return 315_532_800 <= low and high <= 2_051_222_400 and low != high

    def _first_bad_phrase(self, kind: str) -> str:
        found = self.first_bad.get(kind)
        if not found:
            return ""
        row, value = found
        shown = value if len(value) <= 30 else value[:27] + "..."
        return f", first {shown!r} at row {row:,}"

    def _fill_numeric(self, summary: ColumnSummary, integral: bool) -> None:
        stats = self.numbers
        summary.low, summary.high = stats.minimum, stats.maximum
        if integral and self.int_low is not None:
            summary.low, summary.high = self.int_low, self.int_high
        summary.mean, summary.stdev = stats.mean, stats.stdev
        summary.is_integral = integral
        if stats.minimum is not None and stats.maximum is not None:
            summary.bins = histogram(
                self.reservoir.values, stats.minimum, stats.maximum, self.options.bins
            )
            summary.bins_exact = self.reservoir.is_complete
            if not summary.bins_exact:
                summary.notes.append(
                    f"histogram from a sample of {len(self.reservoir.values):,} of "
                    f"{self.reservoir.seen:,} values; the range and mean are exact"
                )

    def _fill_categorical(self, summary: ColumnSummary) -> None:
        if self.distinct_capped:
            # Past the cap the counts are biased, so no top-values list (D15).
            summary.notes.append(
                f"more than {self.options.max_distinct:,} distinct values — "
                "not counted exactly, and frequencies are not shown"
            )
            return
        summary.top_values = sorted(
            self.distinct.items(), key=lambda kv: (-kv[1], kv[0])
        )[: self.options.top_values]


def _percent(share: float) -> str:
    """Never round a near miss up to 100%: '99.99%' is the whole point."""
    percent = share * 100
    if percent >= 99.995:
        return "99.99%"
    return f"{percent:.2f}".rstrip("0").rstrip(".") + "%"


def _plural(count: int, noun: str) -> str:
    return f"{count:,} {noun}" if count == 1 else f"{count:,} {noun}s"
