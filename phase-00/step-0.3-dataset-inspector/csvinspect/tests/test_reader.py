"""Reading real-world files: encodings, dialects, shape, and failing usefully."""

import pytest

from csvinspect import (
    EncodingProblem,
    FileProblem,
    MalformedCSV,
    NotTextCSV,
    Options,
    inspect_file,
)


# ------------------------------------------------------------------ D8, D9, D11

def test_missing_file_names_the_path(tmp_path):
    with pytest.raises(FileProblem, match="no such file"):
        inspect_file(tmp_path / "nope.csv")


def test_a_directory_is_not_a_csv(tmp_path):
    with pytest.raises(FileProblem, match="is a directory"):
        inspect_file(tmp_path)


def test_empty_file(write_csv):
    with pytest.raises(FileProblem, match="empty"):
        inspect_file(write_csv(""))


def test_binary_file_is_rejected_with_a_suggestion(tmp_path):
    path = tmp_path / "sheet.xlsx"
    path.write_bytes(b"PK\x03\x04\x00\x00binary junk")
    with pytest.raises(NotTextCSV, match="export it to CSV"):
        inspect_file(path)


def test_bad_encoding_is_loud_and_suggests_a_flag(tmp_path):
    path = tmp_path / "legacy.csv"
    path.write_bytes("name\ncafé\n".encode("latin-1"))
    with pytest.raises(EncodingProblem, match="--encoding latin-1"):
        inspect_file(path)


def test_the_suggested_flag_actually_works(tmp_path):
    path = tmp_path / "legacy.csv"
    path.write_bytes("name\ncafé\n".encode("latin-1"))
    report = inspect_file(path, Options(encoding="latin-1"))
    assert report.columns[0].top_values == [("café", 1)]


def test_a_bom_is_stripped_from_the_first_column_name(tmp_path):
    path = tmp_path / "bom.csv"
    path.write_bytes("﻿id,name\n1,bo\n".encode("utf-8"))
    report = inspect_file(path)
    assert report.columns[0].name == "id", "a BOM must not become part of a name"


def test_header_only_file_reports_zero_rows(write_csv):
    report = inspect_file(write_csv("a,b\n"))
    assert report.n_rows == 0
    assert [c.kind for c in report.columns] == ["unknown", "unknown"]


# ------------------------------------------------------------------ D7

def test_semicolons_are_sniffed(write_csv):
    report = inspect_file(write_csv("a;b\n1;x\n2;y\n"))
    assert report.dialect.delimiter == ";"
    assert report.n_columns == 2


def test_tabs_are_sniffed(write_csv):
    report = inspect_file(write_csv("a\tb\n1\tx\n2\ty\n"))
    assert report.dialect.delimiter == "\t"


def test_an_explicit_delimiter_wins(write_csv):
    report = inspect_file(write_csv("a|b\n1|x\n"), Options(delimiter="|"))
    assert report.dialect.delimiter == "|" and report.n_columns == 2


def test_quoted_commas_and_newlines_survive(write_csv):
    body = 'name,note\nWidget,"Red, large"\nMulti,"line\nbreak"\nQuote,"He said ""hi"""\n'
    report = inspect_file(write_csv(body))
    assert report.n_rows == 3, "a newline inside a quoted field is not a new row"
    values = dict(report.columns[1].top_values)
    assert "Red, large" in values
    assert 'He said "hi"' in values


# ------------------------------------------------------------------ D10

def test_ragged_rows_are_counted_not_fatal(write_csv):
    report = inspect_file(write_csv("a,b,c\n1,2,3\n4,5\n6,7,8,9\n"))
    assert report.issues.short_rows == 1 and report.issues.first_short == [2]
    assert report.issues.long_rows == 1 and report.issues.first_long == [3]
    assert report.n_rows == 3


def test_a_short_rows_missing_cells_are_counted_as_missing(write_csv):
    report = inspect_file(write_csv("a,b\n1,2\n3\n"))
    assert report.columns[1].n_missing == 1


def test_strict_rows_turns_shape_into_an_error(write_csv):
    with pytest.raises(MalformedCSV, match="expected 3"):
        inspect_file(write_csv("a,b,c\n1,2,3\n4,5\n"), Options(strict_rows=True))


def test_a_runaway_quoted_field_is_an_error_not_an_out_of_memory(write_csv):
    # csv would otherwise buffer the whole file into one field. The limit turns
    # that into a message; without it, a 2 GB file with one stray quote would
    # be read entirely into memory — which would also break the streaming claim.
    body = 'a,b\n1,"' + "x" * (5 * 1024 * 1024) + "\n"
    with pytest.raises(MalformedCSV, match="could not be parsed"):
        inspect_file(write_csv(body))


def test_an_unterminated_quote_swallows_the_rest_of_the_file(write_csv):
    """Documented, not fixed: this is what the csv module does.

    An opening quote with no closing one makes every later line part of that
    field, so the row count collapses. There is no way to tell this from a
    legitimately multi-line field, which is why the report shows the row count
    prominently — 1 row for a file you know has thousands is the tell.
    """
    report = inspect_file(write_csv('a,b\n1,"oops\n2,fine\n3,also fine\n'))
    assert report.n_rows == 1


def test_blank_lines_are_not_rows(write_csv):
    report = inspect_file(write_csv("a\n1\n\n2\n\n"))
    assert report.n_rows == 2


# ------------------------------------------------------------------ D5, D6

def test_limit_stops_early_and_records_it(write_csv):
    body = "n\n" + "\n".join(str(i) for i in range(1, 1001)) + "\n"
    report = inspect_file(write_csv(body), Options(limit=10))
    assert report.n_rows == 10 and report.truncated_at == 10
    assert report.columns[0].high == 10, "only the rows it read"


def test_no_header_names_columns_by_position(write_csv):
    report = inspect_file(write_csv("1,2,3\n4,5,6\n"), Options(has_header=False))
    assert [c.name for c in report.columns] == ["c1", "c2", "c3"]
    assert report.n_rows == 2, "the first row is data, not a header"


def test_a_numeric_header_row_produces_a_warning(write_csv):
    report = inspect_file(write_csv("1,2\n3,4\n"))
    assert any("--no-header" in w for w in report.warnings)


def test_duplicate_header_names_are_disambiguated(write_csv):
    report = inspect_file(write_csv("a,a\n1,2\n"))
    assert [c.name for c in report.columns] == ["a", "a__2"]
    assert any("duplicate" in w for w in report.warnings)


def test_an_empty_header_cell_is_named_by_position(write_csv):
    report = inspect_file(write_csv("a,,c\n1,2,3\n"))
    assert report.columns[1].name == "column_2"
    assert any("no name" in w for w in report.warnings)
