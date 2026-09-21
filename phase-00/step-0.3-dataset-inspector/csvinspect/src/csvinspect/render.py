"""Turning a Report into the text a person reads. All formatting lives here.

Nothing above this module formats a number, and this module reads no files, so
the report's content can be tested without matching whitespace and its layout
can be changed without touching a decision.
"""

from __future__ import annotations

from datetime import date, datetime

from csvinspect.columns import ColumnSummary
from csvinspect.report import Report
from csvinspect.stats import sparkline

NAME_WIDTH = 22
KIND_WIDTH = 8


def render(report: Report) -> str:
    lines = [_headline(report), ""]
    if not report.columns:
        return "\n".join(lines + ["  (no columns)"])

    name_width = min(max(len(c.name) for c in report.columns), NAME_WIDTH)
    for column in report.columns:
        lines.extend(_render_column(column, name_width))

    footer = _footer(report)
    if footer:
        lines.append("")
        lines.extend(footer)
    return "\n".join(lines)


def _headline(report: Report) -> str:
    rows = f"{report.n_rows:,} row{'' if report.n_rows == 1 else 's'}"
    cols = f"{report.n_columns} column{'' if report.n_columns == 1 else 's'}"
    where = f"{report.encoding}, {report.dialect.described}"
    head = f"{report.path} — {rows} × {cols}  ·  {where}"
    if report.truncated_at:
        head += f"  ·  stopped at --limit {report.truncated_at:,}"
    return head


def _render_column(column: ColumnSummary, name_width: int) -> list[str]:
    name = _clip(column.name, name_width)
    counts = f"{column.n_values:>9,} values {column.n_missing:>9,} missing"
    head = f"  {name:<{name_width}}  {column.kind:<{KIND_WIDTH}} {counts}   {_detail(column)}"
    lines = [head.rstrip()]

    indent = " " * (2 + name_width + 2 + KIND_WIDTH + 1)
    if column.bins:
        bars = sparkline(column.bins)
        mean = f"mean {_number(column.mean, column.is_integral)}" if column.mean is not None else ""
        spread = f"sd {_number(column.stdev, False)}" if column.stdev else ""
        lines.append(f"{indent}{bars}  {mean}  {spread}".rstrip())
    if column.top_values:
        lines.append(indent + _top_values(column))
    for note in column.notes:
        lines.append(f"{indent}! {note}")
    return lines


def _detail(column: ColumnSummary) -> str:
    """The right-hand summary: whatever is informative for this type."""
    if column.kind in ("integer", "decimal"):
        if column.low is None:
            return ""
        return f"{_number(column.low, column.is_integral)} … {_number(column.high, column.is_integral)}"
    if column.kind == "date":
        if column.low is None:
            return ""
        return f"{_moment(column.low)} … {_moment(column.high)}  [{column.date_format}]"
    if column.kind == "boolean":
        return f"{column.n_true:,} true / {column.n_false:,} false"
    if column.kind == "unknown":
        return "—"
    if column.distinct_capped:
        return "many distinct"
    return f"{column.distinct:,} distinct"


def _top_values(column: ColumnSummary) -> str:
    parts = [f"{_clip(value, 18)} {count:,}" for value, count in column.top_values]
    shown = " · ".join(parts)
    remaining = (column.distinct or 0) - len(column.top_values)
    if remaining > 0:
        shown += f" · +{remaining:,} more"
    return shown


def _footer(report: Report) -> list[str]:
    lines: list[str] = []
    issues = report.issues
    if issues.short_rows:
        lines.append(
            f"  {issues.short_rows:,} row(s) had fewer fields than the header "
            f"(missing cells counted as missing): {_rows(issues.first_short)}"
        )
    if issues.long_rows:
        lines.append(
            f"  {issues.long_rows:,} row(s) had extra fields (ignored): "
            f"{_rows(issues.first_long)}"
        )
    for warning in report.warnings:
        lines.append(f"  {warning}")
    return ["notes"] + lines if lines else []


def _rows(numbers: list[int]) -> str:
    shown = ", ".join(f"{n:,}" for n in numbers)
    return f"row {shown}" if len(numbers) == 1 else f"rows {shown}, …"


def _number(value: float | None, integral: bool) -> str:
    """Integers print as integers; decimals keep enough digits to be useful."""
    if value is None:
        return "—"
    if integral and float(value).is_integer():
        return f"{int(value):,}"
    if value and (abs(value) >= 1e12 or abs(value) < 1e-4):
        return f"{value:,.4g}"
    return f"{value:,.4f}".rstrip("0").rstrip(".")


def _moment(value: date | datetime | None) -> str:
    if value is None:
        return "—"
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d %H:%M:%S")
    return value.isoformat()


def _clip(text: str, width: int) -> str:
    text = text.replace("\n", "⏎")
    return text if len(text) <= width else text[: width - 1] + "…"
