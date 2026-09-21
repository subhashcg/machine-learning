"""The command line: parse arguments, run one inspection, choose an exit code.

Exit codes (D11): 0 success — warnings do not change it; 1 the input could not
be read or parsed; 2 usage error, which argparse produces itself.
"""

from __future__ import annotations

import argparse
import sys

from csvinspect.errors import InspectError
from csvinspect.options import Options
from csvinspect.render import render
from csvinspect.report import inspect_file
from csvinspect.values import DEFAULT_NA_VALUES

EXIT_OK = 0
EXIT_INPUT_ERROR = 1

_NA_LIST = ", ".join(sorted(v for v in DEFAULT_NA_VALUES if v))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="csv-inspect",
        description="Tell me what is in this CSV: types, missing values, ranges, shape.",
        epilog=(
            "Values treated as missing by default: an empty or whitespace-only "
            f"cell, or any of: {_NA_LIST} (case-insensitive)."
        ),
    )
    parser.add_argument("path", help="the CSV file to inspect")

    reading = parser.add_argument_group("reading the file")
    reading.add_argument("--encoding", default="utf-8-sig",
                         help="text encoding (default: utf-8-sig, which also strips a BOM)")
    reading.add_argument("--delimiter", default=None,
                         help="field delimiter; sniffed from the first 64 KB if omitted")
    reading.add_argument("--no-header", action="store_true",
                         help="the first row is data; columns are named c1, c2, …")
    reading.add_argument("--limit", type=int, default=None, metavar="N",
                         help="stop after N data rows (the report says so)")
    reading.add_argument("--strict-rows", action="store_true",
                         help="treat a row with the wrong number of fields as an error")

    values = parser.add_argument_group("what the values mean")
    values.add_argument("--na-values", default=None, metavar="LIST",
                        help="comma-separated placeholders to treat as missing, "
                             "replacing the default list")
    values.add_argument("--no-default-na", action="store_true",
                        help="only an empty cell counts as missing")
    values.add_argument("--thousands", default=None, metavar="CHAR",
                        help="accept CHAR as a thousands separator inside numbers")
    values.add_argument("--tolerance", type=float, default=0.0, metavar="FRACTION",
                        help="type a column even if up to FRACTION of its values "
                             "fail to parse (default 0: one bad value means text)")

    output = parser.add_argument_group("output")
    output.add_argument("--bins", type=int, default=10, help="histogram bins (default 10)")
    output.add_argument("--top-values", type=int, default=5, metavar="N",
                        help="how many frequent values to list for text columns")
    output.add_argument("--max-distinct", type=int, default=1_000, metavar="N",
                        help="stop counting distinct values past N (bounds memory)")
    output.add_argument("--reservoir", type=int, default=20_000, metavar="N",
                        help="sample size per numeric column for the histogram")
    output.add_argument("--seed", type=int, default=0,
                        help="random seed for that sample, so runs are reproducible")
    parser.add_argument("--version", action="version", version="csv-inspect 0.1.0")
    return parser


def options_from(args: argparse.Namespace) -> Options:
    if args.no_default_na:
        na_values = frozenset({""})
    elif args.na_values is not None:
        na_values = frozenset({""} | {v.strip().lower() for v in args.na_values.split(",")})
    else:
        na_values = DEFAULT_NA_VALUES

    return Options(
        encoding=args.encoding,
        delimiter=args.delimiter,
        has_header=not args.no_header,
        limit=args.limit,
        strict_rows=args.strict_rows,
        na_values=na_values,
        thousands=args.thousands,
        tolerance=args.tolerance,
        reservoir_size=args.reservoir,
        max_distinct=args.max_distinct,
        seed=args.seed,
        bins=args.bins,
        top_values=args.top_values,
    )


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.limit is not None and args.limit < 1:
        parser.error("--limit must be at least 1")
    if not 0.0 <= args.tolerance < 1.0:
        parser.error("--tolerance must be between 0 and 1")
    if args.bins < 1:
        parser.error("--bins must be at least 1")

    try:
        report = inspect_file(args.path, options_from(args))
    except InspectError as e:
        # Every user-facing failure arrives here as a sentence. Anything else is
        # a bug in this program and is allowed to produce a real traceback.
        print(f"error: {e}", file=sys.stderr)
        return EXIT_INPUT_ERROR

    print(render(report))
    return EXIT_OK


if __name__ == "__main__":
    raise SystemExit(main())
