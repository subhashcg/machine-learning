"""Shared helpers. Every test writes its own file; none share state."""

from __future__ import annotations

import pytest

from csvinspect import Options, inspect_file


@pytest.fixture
def write_csv(tmp_path):
    """Write `text` to a temp file and hand back the path."""

    def _write(text: str, name: str = "t.csv", encoding: str = "utf-8") -> object:
        path = tmp_path / name
        path.write_text(text, encoding=encoding)
        return path

    return _write


@pytest.fixture
def one_column(write_csv):
    """Inspect a single column of values and return its summary.

    Most decisions are per-column, so this keeps the tests about the decision
    rather than about building a file.
    """

    def _inspect(values: list[str], name: str = "col", **option_overrides):
        body = "\n".join([name, *values]) + "\n"
        path = write_csv(body)
        report = inspect_file(path, Options(**option_overrides))
        return report.columns[0]

    return _inspect
