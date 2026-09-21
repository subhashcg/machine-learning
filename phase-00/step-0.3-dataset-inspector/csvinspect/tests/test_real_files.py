"""Against files nobody wrote for this tool.

Skipped when the files are absent, so the suite still passes on a fresh clone.
Point CSVINSPECT_REAL_DIR at a directory of your own CSVs to exercise these.
"""

import os
import pathlib

import pytest

from csvinspect import Options, inspect_file

REAL_DIR = pathlib.Path(os.environ.get("CSVINSPECT_REAL_DIR", pathlib.Path.home() / "Downloads"))
ESMA = REAL_DIR / "esma70-155-10816_annex_to_transparency_opinion_csv.csv"
OHLCV = REAL_DIR / "BATS_AMZN, 1M.csv"

needs_esma = pytest.mark.skipif(not ESMA.exists(), reason=f"{ESMA} not present")
needs_ohlcv = pytest.mark.skipif(not OHLCV.exists(), reason=f"{OHLCV} not present")


@needs_esma
def test_regulatory_file_with_a_bom_and_quoted_commas():
    report = inspect_file(ESMA)
    names = [c.name for c in report.columns]
    assert names[0] == "ESMA ID", "the BOM must not end up in the first column name"
    assert "Instruments in scope of the assessment" in names, "quoted commas survived"

    by_name = {c.name: c for c in report.columns}
    created = by_name["Created on"]
    assert created.kind == "date" and created.date_format == "%d/%m/%Y", (
        "a day above 12 somewhere in the column resolves the format"
    )
    assert by_name["Country"].kind == "text"
    assert by_name["Assessment"].n_values == report.n_rows


@needs_esma
def test_the_cost_of_the_default_missing_list_is_visible():
    """D1 biting on real data: the file's literal value 'None' reads as missing."""
    strict = {c.name: c for c in inspect_file(ESMA).columns}
    kept = {c.name: c for c in inspect_file(ESMA, Options(na_values=frozenset({""}))).columns}

    column = "Exemptions from the positive assessment"
    assert strict[column].n_missing > 300, "'None' was treated as absent"
    assert kept[column].n_missing == 0, "with --no-default-na it is a value again"


@needs_ohlcv
def test_market_data_export():
    report = inspect_file(OHLCV)
    by_name = {c.name: c for c in report.columns}

    time_column = by_name["time"]
    assert time_column.kind == "integer", "epoch seconds are integers, not dates"
    assert any("Unix-epoch" in note for note in time_column.notes), "but say what they look like"

    assert by_name["open"].kind == "decimal"
    assert by_name["MA №1"].n_missing > 0, "a non-ASCII column name still works"
    assert by_name["Regular Bullish"].kind == "unknown", "an entirely empty column"
