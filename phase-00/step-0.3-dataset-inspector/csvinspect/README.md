# csv-inspect

Point it at a CSV you have never seen and find out what is in it — types,
missing values, ranges, shape — before loading it into anything.

Standard library only. No pandas, no click, no rich.

```bash
cd phase-00/step-0.3-dataset-inspector/csvinspect
uv sync
uv run csv-inspect path/to/data.csv
```

```
data/sales.csv — 1,204 rows × 5 columns  ·  utf-8-sig, comma-delimited

  order_id     integer      1,204 values         0 missing   1 … 1,204
  region       text         1,180 values        24 missing   4 distinct
                            EMEA 612 · APAC 311 · AMER 244 · LATAM 13
  amount       decimal      1,204 values         0 missing   0.5 … 9,812
                            ▁▂▅█▆▃▂▁▁▁  mean 412.55  sd 233.4
  ordered_at   date         1,199 values         5 missing   2024-01-03 … 2024-12-30  [%Y-%m-%d]
  is_refunded  boolean      1,204 values         0 missing   87 true / 1,117 false
```

Lines beginning with `!` are things the tool is unsure about or thinks you
should know. They are the most useful part of the output.

## What it does

- **Infers a type per column** — integer, decimal, boolean, date, text — from
  the values, never from the column name.
- **Counts missing values**, with a documented and overridable idea of what
  "missing" means.
- **Summarises appropriately**: a range and a histogram for numbers, a range
  and the detected format for dates, counts for booleans, distinct values and
  frequencies for categories.
- **Streams**. Memory does not grow with the number of rows: 2,000,000 rows of
  a 97 MB file peak at 27 MB of RSS, and a 2 GB file works the same way.
- **Says when it is guessing.** Sampled histograms, ambiguous date formats,
  near-miss types and capped distinct counts are all labelled.

## Options

```
  --encoding ENC        default utf-8-sig (strips a BOM); try latin-1 for legacy files
  --delimiter CHAR      skip sniffing
  --no-header           the first row is data; columns become c1, c2, …
  --limit N             stop after N rows (the report says it is partial)
  --strict-rows         a row with the wrong number of fields becomes an error

  --na-values LIST      replace the default list of missing-value placeholders
  --no-default-na       only an empty cell counts as missing
  --thousands CHAR      accept 1,234.50 as a number
  --tolerance FRACTION  allow this fraction of a column to fail and still type it

  --bins N              histogram bins (default 10)
  --top-values N        frequent values listed per text column (default 5)
  --max-distinct N      stop counting distinct values past N (default 1,000)
  --reservoir N         histogram sample size per numeric column (default 20,000)
  --seed N              seed for that sample, so two runs agree
```

By default these count as missing: an empty or whitespace-only cell, and
`na`, `n/a`, `#n/a`, `nan`, `null`, `none`, `nil`, `-`, `?` — case-insensitive.
**If any of those is a real value in your data** (`NA` is Namibia, `None` is a
real answer in a permissions column), use `--no-default-na` or `--na-values`.

Exit codes: `0` fine, `1` the input could not be read or parsed, `2` bad usage.

## As a library

```python
from csvinspect import inspect_file, Options, render

report = inspect_file("data.csv", Options(limit=1000))
print(render(report))

for column in report.columns:
    print(column.name, column.kind, column.n_missing, column.notes)
```

`inspect_file` raises only `InspectError` subclasses for bad input:
`FileProblem`, `NotTextCSV`, `EncodingProblem`, `MalformedCSV`.

## Development

```bash
uv sync
uv run pytest -q              # 144 tests
uv run pytest -q -k streaming # the memory-does-not-grow tests
```

The suite covers the decisions, not just the happy path: every rule in
`DESIGN.md` has a test named after it. `tests/test_streaming.py` measures peak
allocation and fails if the reader ever starts accumulating rows.
`tests/test_real_files.py` runs against real CSVs and skips when they are
absent — point `CSVINSPECT_REAL_DIR` at a directory of your own.

## Reading the rest

- `../DESIGN.md` — the decisions, with reasons and costs, written before the code
- `../WRITEUP.md` — where it fails, and who it would mislead
