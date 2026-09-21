"""Getting rows out of a file, and failing usefully when that is not possible.

Everything that touches the filesystem lives here. The module yields rows one at
a time and never holds more than one — the streaming constraint is kept or
broken in this file alone.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator

from csvinspect.errors import EncodingProblem, FileProblem, MalformedCSV, NotTextCSV

SNIFF_BYTES = 64 * 1024
CANDIDATE_DELIMITERS = ",;\t|"

# csv defaults to 128 KB per field. A single field larger than this is either a
# pathological file or not a CSV at all, and the error says so rather than
# letting one runaway quote consume the machine's memory.
MAX_FIELD_BYTES = 4 * 1024 * 1024


@dataclass
class Dialect:
    delimiter: str
    quotechar: str = '"'
    sniffed: bool = True
    warnings: list[str] = field(default_factory=list)

    @property
    def described(self) -> str:
        names = {",": "comma", ";": "semicolon", "\t": "tab", "|": "pipe"}
        return f"{names.get(self.delimiter, repr(self.delimiter))}-delimited"


def check_readable(path: Path) -> None:
    """D11. Every way a path can be unusable, with the message the user needs."""
    if not path.exists():
        raise FileProblem(f"no such file: {path}")
    if path.is_dir():
        raise FileProblem(f"{path} is a directory, not a CSV file")
    try:
        size = path.stat().st_size
    except OSError as e:
        raise FileProblem(f"cannot read {path}: {e.strerror}") from e
    if size == 0:
        raise FileProblem(f"{path} is empty (0 bytes)")


def sniff(path: Path, encoding: str, delimiter: str | None) -> Dialect:
    """Decide the delimiter, and refuse files that are not text (D7, D9)."""
    with open(path, "rb") as f:
        head = f.read(SNIFF_BYTES)

    if b"\x00" in head:
        # D9: the commonest mistake is pointing this at a .xlsx or .parquet.
        offset = head.index(b"\x00")
        raise NotTextCSV(
            f"{path} does not look like a text CSV: binary data at byte {offset:,}. "
            "If this is a spreadsheet or a Parquet file, export it to CSV first."
        )

    try:
        sample = head.decode(encoding)
    except UnicodeDecodeError as e:
        raise _encoding_error(path, encoding, e) from e

    if delimiter is not None:
        return Dialect(delimiter=delimiter, sniffed=False)

    try:
        found = csv.Sniffer().sniff(sample, delimiters=CANDIDATE_DELIMITERS)
    except csv.Error:
        # Not an error: a single-column file has no delimiter to find. Say so
        # rather than silently pretending commas were chosen deliberately.
        return Dialect(
            delimiter=",",
            sniffed=False,
            warnings=[
                "no delimiter found in the first 64 KB — reading as a single "
                "column; pass --delimiter if that is wrong"
            ],
        )
    return Dialect(delimiter=found.delimiter, quotechar=found.quotechar or '"')


def _encoding_error(path: Path, encoding: str, e: UnicodeDecodeError) -> EncodingProblem:
    """D8. Loud, with the byte offset and a concrete next command."""
    return EncodingProblem(
        f"cannot decode {path} as {encoding}: {e.reason} at byte {e.start:,}. "
        f"The file may be latin-1 or cp1252 — try: "
        f"csv-inspect --encoding latin-1 {path}"
    )


@dataclass
class RowIssues:
    """D10. Shape problems are counted and reported, never fatal by default."""

    short_rows: int = 0
    long_rows: int = 0
    first_short: list[int] = field(default_factory=list)
    first_long: list[int] = field(default_factory=list)

    def record_short(self, row_number: int) -> None:
        self.short_rows += 1
        if len(self.first_short) < 3:
            self.first_short.append(row_number)

    def record_long(self, row_number: int) -> None:
        self.long_rows += 1
        if len(self.first_long) < 3:
            self.first_long.append(row_number)


def read_rows(
    path: Path, encoding: str, dialect: Dialect, has_header: bool, limit: int | None
) -> Iterator[tuple[list[str], int]]:
    """Yield `(row, row_number)` one row at a time, skipping the header row.

    Column names are not derived here — a `csv.reader` cannot be rewound, so the
    caller gets them from `peek_first_row()` first. Row numbers count *data*
    rows from 1, so they line up with what the user sees in a spreadsheet.

    One row is held at a time. Nothing in this function accumulates.
    """
    csv.field_size_limit(MAX_FIELD_BYTES)
    with open(path, encoding=encoding, newline="") as f:
        reader = csv.reader(f, delimiter=dialect.delimiter, quotechar=dialect.quotechar)
        row_number = 0
        header_skipped = not has_header
        while True:
            try:
                row = next(reader)
            except StopIteration:
                break
            except csv.Error as e:
                raise MalformedCSV(
                    f"{path} could not be parsed at line {reader.line_num:,}: {e}. "
                    "An unbalanced quote is the usual cause."
                ) from e
            except UnicodeDecodeError as e:
                raise _encoding_error(path, encoding, e) from e

            if not row:                     # a blank line is not a row of data
                continue
            if not header_skipped:
                header_skipped = True
                continue

            row_number += 1
            yield row, row_number
            if limit is not None and row_number >= limit:
                break


def peek_first_row(path: Path, encoding: str, dialect: Dialect) -> list[str]:
    """The first physical row, used to name columns and to sanity-check a header."""
    with open(path, encoding=encoding, newline="") as f:
        reader = csv.reader(f, delimiter=dialect.delimiter, quotechar=dialect.quotechar)
        for row in reader:
            if row:
                return row
    return []


def resolve_names(first_row: list[str], has_header: bool) -> tuple[list[str], list[str]]:
    """Turn the first row into column names, reporting anything odd (D6)."""
    warnings: list[str] = []
    if not has_header:
        return [f"c{i + 1}" for i in range(len(first_row))], warnings

    names: list[str] = []
    seen: dict[str, int] = {}
    for position, raw in enumerate(first_row, start=1):
        name = raw.strip()
        if not name:
            name = f"column_{position}"
            warnings.append(f"column {position} has no name in the header")
        if name in seen:
            seen[name] += 1
            warnings.append(f"duplicate column name {name!r} — renamed to {name}__{seen[name]}")
            name = f"{name}__{seen[name]}"
        else:
            seen[name] = 1
        names.append(name)
    return names, warnings


def header_looks_like_data(first_row: list[str], na_values) -> bool:
    """D6. A header of numbers and dates is usually a file with no header."""
    from csvinspect.values import date_formats_matching, is_missing, parse_decimal

    present = [cell.strip() for cell in first_row if not is_missing(cell, na_values)]
    if not present:
        return False
    return all(
        parse_decimal(cell) is not None or date_formats_matching(cell)
        for cell in present
    )
