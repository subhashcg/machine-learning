"""The one pass: read rows, feed accumulators, hand back a finished report.

This is the only function that knows about a whole file. It still never holds
more than one row: `read_rows` is a generator, and the loop below pushes each
cell into its column's accumulator and then drops the row.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from csvinspect.columns import ColumnAccumulator, ColumnSummary
from csvinspect.errors import FileProblem, MalformedCSV
from csvinspect.options import Options
from csvinspect.reader import (
    Dialect,
    RowIssues,
    check_readable,
    header_looks_like_data,
    peek_first_row,
    read_rows,
    resolve_names,
    sniff,
)


@dataclass
class Report:
    path: Path
    dialect: Dialect
    encoding: str
    n_rows: int
    columns: list[ColumnSummary]
    issues: RowIssues = field(default_factory=RowIssues)
    warnings: list[str] = field(default_factory=list)
    truncated_at: int | None = None

    @property
    def n_columns(self) -> int:
        return len(self.columns)


def inspect_file(path: str | Path, options: Options | None = None) -> Report:
    """Read `path` once and summarise every column. Raises InspectError only."""
    path = Path(path)
    options = options or Options()

    check_readable(path)
    dialect = sniff(path, options.encoding, options.delimiter)

    first_row = peek_first_row(path, options.encoding, dialect)
    if not first_row:
        raise FileProblem(f"{path} has no rows (only blank lines?)")

    names, warnings = resolve_names(first_row, options.has_header)
    warnings = list(dialect.warnings) + warnings
    if options.has_header and header_looks_like_data(first_row, options.na_values):
        warnings.append(
            "every cell in the header row parses as a number or a date — "
            "if this file has no header, re-run with --no-header"
        )

    accumulators = [ColumnAccumulator(name, options) for name in names]
    issues = RowIssues()
    width = len(names)
    n_rows = 0

    for row, row_number in read_rows(
        path, options.encoding, dialect, options.has_header, options.limit
    ):
        n_rows = row_number
        if len(row) != width:
            _record_shape(issues, row_number, len(row), width, path, options.strict_rows)

        for index, accumulator in enumerate(accumulators):
            # D10: a short row's absent cells are missing values, not an error.
            accumulator.add(row[index] if index < len(row) else "", row_number)

    return Report(
        path=path,
        dialect=dialect,
        encoding=options.encoding,
        n_rows=n_rows,
        columns=[a.finalize() for a in accumulators],
        issues=issues,
        warnings=warnings,
        truncated_at=options.limit if options.limit and n_rows >= options.limit else None,
    )


def _record_shape(
    issues: RowIssues, row_number: int, found: int, expected: int, path: Path, strict: bool
) -> None:
    if strict:
        raise MalformedCSV(
            f"{path} row {row_number:,} has {found} fields, expected {expected} "
            "(--strict-rows)"
        )
    if found < expected:
        issues.record_short(row_number)
    else:
        issues.record_long(row_number)
