# DESIGN — csv-inspect

A command-line tool that reads a CSV and tells you what is in it, in one pass,
using nothing but the standard library.

```
$ csv-inspect data/sales.csv
```

This document is the plan and, more importantly, the record of the decisions.
Where a decision could reasonably have gone the other way, the reasoning is
written down — including what it costs.

---

## 1. The product

One command, one file, one report on stdout. No config file, no plugins, no
interactive mode. A person points it at a CSV they have never seen and, in about
a second, knows:

- how many rows and columns there are, and whether the file parsed cleanly
- what type each column really is
- how much of it is missing
- the shape of the numbers, and the vocabulary of the categories
- **what the tool is unsure about** — every guess is labelled as a guess

The last point is the one that matters. A summary that looks confident about a
column it got wrong is worse than no summary. Anywhere the tool infers rather
than measures, the output says so.

### Intended output

```
data/sales.csv — 1,204 rows × 5 columns  ·  utf-8, comma-delimited

  order_id      integer    1,204 values      0 missing   1 … 1,204
  region        text       1,180 values     24 missing   4 distinct
                           EMEA 612 · APAC 311 · AMER 244 · LATAM 13
  amount        decimal    1,204 values      0 missing   0.50 … 9,812.00
                           mean 412.55  ▁▂▅█▆▃▂▁▁▁
  ordered_at    date       1,199 values      5 missing   2024-01-03 … 2024-12-30
                           format %Y-%m-%d
  is_refunded   boolean    1,204 values      0 missing   87 true / 1,117 false

notes
  3 rows had more fields than the header (extra fields ignored): rows 811, 902, 1,144
```

---

## 2. Decisions

### D1 — What counts as missing

**Decision.** A value is missing if it is the empty string, or whitespace only,
or — case-insensitively, after stripping — one of:

```
na  n/a  #n/a  nan  null  none  nil  -  ?
```

`--na-values X,Y` replaces that list; `--no-default-na` reduces it to the empty
string alone.

**Why.** A CSV cannot express "absent"; every tool that produces one invents its
own spelling. Treating only `""` as missing would report a column of `N/A` as
text with 1 distinct value, which is worse than wrong — it is confidently wrong.

**What it costs.** `NA` is the ISO country code for Namibia. `-` is a real value
in a column of arithmetic signs. `?` is a real value in a survey about
uncertainty. In each of those, this tool will under-count the data and
over-count the missing. That is why the list is documented in `--help` and why
`--no-default-na` exists. A tool that guesses must let you turn the guess off.

### D2 — One bad value in 10,000

**Decision.** Type inference is **strict**: a column's type must accept *every*
non-missing value. One `n/a` in 10,000 integers makes the column text — **but
the tool reports the near-miss rather than silently demoting**:

```
  order_id      text       9,999 values      0 missing   9,999 distinct
                           ⚠ 99.99% parse as integer; 1 does not: "n/a" (row 5,213)
```

`--tolerance 0.001` re-types a column when the failures are below that fraction,
and always reports how many were ignored and where the first one was.

**Why.** The two failure modes are not symmetric. Calling a dirty integer column
"text" is visible: the user sees a column they expected to be numeric, reads the
warning, and learns there is one bad row. Calling it "integer" and quietly
dropping the bad value is invisible — and the bad value is usually the
interesting one. It is the row where the export broke.

So the default never discards evidence, and the warning carries the row number,
because "one value is bad" is useless without "which".

**What it costs.** On genuinely filthy data every column reads as text with a
warning, which is noisy. That is the honest description of filthy data, and
`--tolerance` is there when you have already accepted it.

### D3 — Inferring dates without dateutil

**Decision.** A fixed, ordered whitelist of formats:

```
%Y-%m-%d   %Y/%m/%d   %Y%m%d   %d/%m/%Y   %m/%d/%Y   %d-%m-%Y   %d.%m.%Y
%Y-%m-%dT%H:%M:%S   %Y-%m-%d %H:%M:%S   (with optional Z / fractional seconds)
```

Each column carries the **set of formats still viable**. Every value must parse
under a format for it to survive; at the end the column is a date if at least one
format survives. Ties are resolved by the order above and **the ambiguity is
printed**:

```
  application_date  date   364 values   0 missing   2016-03-08 … 2024-11-10
                           format %d/%m/%Y  ⚠ %m/%d/%Y also fits every value
```

**Why.** `03/06/2020` is 3 June in Buenos Aires and 6 March in Boston, and
nothing in the file says which. `dateutil` resolves this by picking a
convention; the honest answer is that the file does not contain the information.
A single value with a day above 12 disambiguates the whole column — which is why
this is computed over the full pass, not a sample: the disambiguating row is
often thousands of rows in.

Pure ISO (`%Y-%m-%d`) is never ambiguous, so the common case prints no warning.

**What it costs.** No natural-language dates (`March 3, 2020`), no locale month
names, no mixed formats within one column. Those read as text, with a near-miss
warning if most values parsed.

### D4 — A histogram from a single pass

The hard constraint: binning needs the range, the range needs the whole column,
and there is only one pass.

**Decision.** Split what must be exact from what may be approximate.

- **Exact, streaming, O(1) memory:** count, missing count, min, max, sum, and
  mean/variance via Welford's algorithm.
- **Approximate, bounded memory:** the histogram is built from a **reservoir
  sample** of up to 20,000 values per numeric column (Algorithm R, seeded, so
  runs are reproducible). Bin edges come from the *exact* min and max, so the
  axis is always right; only the bar heights are sampled.
- When a column has ≤ 20,000 values the reservoir holds all of them and the
  histogram is exact. **Only when it is sampled does the output say so.**

**Alternatives rejected.** *Two passes on seekable files:* would be exact, but
splits the code into two paths and dies on stdin, which is where big inputs come
from. *Fixed bins with dynamic rebinning:* exact and O(1), but merging bins as
the range grows loses resolution unpredictably — an approximation that is harder
to explain than sampling. *t-digest or similar:* better accuracy per byte, but a
few hundred lines of numerics to get right, and still approximate.

20,000 values is ~160 KB per numeric column and puts the sampling error on a
ten-bin histogram well below the width of one character cell, which is the actual
resolution of the output.

### D5 — How much of the file to read

**Decision.** All of it, every time. `--limit N` stops early for a quick look and
then **labels the entire report** `based on the first N rows`.

**Why.** Sampling for type inference is exactly how a column gets typed integer
in the report and then explodes on row 900,000 in the consumer's pipeline. The
whole value of this tool is that its answer holds for the file, not for the
first megabyte of it. Streaming makes the full pass affordable, so there is no
reason to buy speed with correctness — and this is a tool you run once per file,
not in a loop.

### D6 — Headers

**Decision.** The first row is the header. `--no-header` names columns
`c1 … cn`. The tool warns when the header looks wrong:

- every cell parses as a number or a date → *"the header row looks like data;
  did you mean --no-header?"*
- duplicate names → disambiguated to `name`, `name__2`, and reported
- empty names → `column_4` (by position), and reported

**Why.** Sniffing headers heuristically (`csv.Sniffer.has_header`) is a guess
that fails silently in both directions. An explicit default plus a loud warning
puts the decision where it belongs — with the person who knows the file.

### D7 — Dialect

**Decision.** `csv.Sniffer` on the first 64 KB, limited to `, ; \t |`; fall back
to comma if it fails. `--delimiter` overrides. The chosen dialect is **printed in
the header line**, because a report on a semicolon file misread as one giant
comma column should be obvious at a glance, not a mystery.

### D8 — Encoding

**Decision.** Default `utf-8-sig`, which strips a BOM if present and is
otherwise identical to UTF-8. On a decode failure: **stop**, and report the byte
offset, the line, and a suggestion:

```
error: cannot decode data/legacy.csv as utf-8 at byte 4,213 (line 87)
       the file may be latin-1 or cp1252 — try: csv-inspect --encoding latin-1 …
```

**Why.** `errors="replace"` would let the run "succeed" while quietly turning
`café` into `caf<?>` and inflating the distinct count. Topic 7's whole lesson was
that latin-1 never raises; here the loud failure is the feature. There is no
encoding *detection*: a BOM is evidence, byte-frequency guessing is not.

### D9 — Files that are not CSV

**Decision.** A NUL byte in the first 64 KB → *"this does not look like a text
CSV (binary data at byte N)"*, exit 1. A file that decodes and has exactly one
column with no delimiter found → parsed as a single column, with a warning that
no delimiter was detected.

**Why.** Feeding a `.xlsx` or a `.parquet` to a CSV tool is the single most
common mistake this tool will see, and "0 rows, 1 column" is a terrible way to
find out.

### D10 — Ragged rows

**Decision.** Never crash on shape. A row with **fewer** fields than the header
has its absent cells counted as missing. A row with **more** has the extras
ignored and counted. Both are reported at the end with the first few row numbers.
`--strict-rows` turns either into an error.

**Why.** A malformed row is a fact about the file — the most useful fact, often.
Aborting on it hides the other 99.9%, which is what the user came for.

### D11 — Degenerate files

| input | behaviour |
|---|---|
| file does not exist | `error: no such file: path` + exit 1 |
| path is a directory | `error: path is a directory` + exit 1 |
| empty file (0 bytes) | `error: file is empty` + exit 1 |
| header only, no data | report with `0 rows`, every column type `unknown` |
| all values missing in a column | type `unknown (all values missing)` |
| 2 GB file | works; memory stays flat (see §4) |

Exit codes: **0** success, possibly with warnings; **1** the input could not be
read or parsed; **2** usage error (argparse's own convention).

### D12 — Leading zeros are not numbers

**Decision.** `007`, `01234` and other digit strings with a leading zero (and
more than one digit) are **text**, not integers — reported as:

```
  zip_code      text       1,204 values      0 missing   932 distinct
                           numeric with leading zeros — looks like an identifier
```

**Why.** Zip codes, account numbers, product SKUs and phone numbers are digits
that are not quantities. Typing them as integer is the specific bug that turns
`01234` into `1234` in every downstream system, and it is the single most common
data-loss bug in spreadsheet exports.

### D13 — 0/1 is an integer, true/false is a boolean

**Decision.** Boolean means `true/false`, `yes/no`, `t/f`, `y/n`,
case-insensitive. A column of `0` and `1` is an **integer**, with a note that it
holds only two values and may be a flag.

**Why.** `0`/`1` columns are summed and averaged, and calling a column boolean
suppresses the range and histogram that make it useful. The note recovers the
information without destroying the arithmetic.

### D14 — Numbers do not contain commas or currency

**Decision.** `1,234.50` and `$19.99` are text by default, with the near-miss
warning from D2 (`99.8% parse as decimal with a thousands separator`).
`--thousands ,` opts in.

**Why.** A comma inside a number in a comma-separated file is a quoting decision
someone else made, and `1,234` is `1234` in the US and `1.234` in Germany.
Guessing gets it silently wrong by a factor of 1,000.

### D15 — Text columns: exact until it is unsafe

**Decision.** Track distinct values exactly while there are ≤ 1,000 of them.
Past that, stop adding keys, keep counting the ones already seen, and report:

```
  description   text     8,412 values   31 missing   ≥1,000 distinct (not counted exactly)
```

Top values are shown only while the column is under the cap, because after the
cap the counts are biased toward whatever appeared early in the file. Once it is
approximate, it is not shown.

**Why.** Exact distinct counts need memory proportional to the data, which
violates the streaming constraint on the one column type most likely to be
high-cardinality (free text, IDs, URLs). HyperLogLog would give an approximate
count in O(1), and is the right answer at a scale beyond this tool's brief.

---

## 3. Shape of the code

```
csvinspect/
  pyproject.toml           src/ layout, hatchling, console script `csv-inspect`
  README.md                how a stranger runs it
  src/csvinspect/
    __init__.py            public API: inspect_file()
    errors.py              InspectError hierarchy — every user-facing failure
    options.py             every knob, frozen, so a run is reproducible
    reader.py              open, decode, sniff dialect, yield rows (streaming)
    values.py              missing detection, per-value type tests, date formats
    columns.py             ColumnAccumulator: one per column, O(1)+capped memory
    report.py              the single pass: rows in, Report out
    stats.py               Welford, reservoir sampling, histogram binning
    render.py              the report; all formatting lives here, no I/O elsewhere
    cli.py                 argparse, exit codes, error messages
  tests/
    test_values.py         D1, D12, D13, D14 — the per-value decisions
    test_columns.py        D2 near-misses, D3 ambiguity, D15 caps
    test_stats.py          Welford vs statistics, reservoir determinism, bins
    test_reader.py         BOM, dialects, ragged rows, NUL bytes, encodings
    test_cli.py            exit codes, messages, --no-header, --limit
    test_streaming.py      memory stays flat on a large generated file
    test_real_files.py     the two real CSVs (skipped if absent)
```

The dependency direction is one-way: `cli → render → columns → stats/values →
reader`. Nothing below `cli` prints, and nothing below `reader` touches the
filesystem, so every decision above is testable without a file on disk.

Runtime dependencies: **none**. Dev: pytest.

## 4. The streaming claim, made concrete

Memory is bounded by, per column: one accumulator (~15 scalars), the reservoir
(≤ 20,000 floats, numeric columns only), and the distinct map (≤ 1,000 keys).
That is a few MB for a wide file and it does not grow with the number of rows.

`test_streaming.py` asserts this rather than claiming it: generate ~2 million
rows to a temp file, run the inspector under `tracemalloc`, and assert peak
allocation stays under a fixed ceiling and does not scale with row count. A test
that would fail if someone "optimised" the reader into `list(reader)`.

## 5. Deliberately not doing

- **No pandas, no dependencies** — the brief's constraint, and the point.
- **No compressed input** (`.csv.gz`), no Excel, no JSON, no Parquet.
- **No `--json` output.** Worth having, but the brief is a report a human reads,
  and a machine-readable schema is a second product with a second contract.
- **No correlations, no outlier detection, no "data quality score".** One number
  that summarises a file is exactly the kind of confident wrongness §1 rejects.
- **No encoding detection** beyond the BOM (D8).
- **No parallelism.** The work is I/O bound and the file is read once.
- **No column-name-based inference.** A column called `date` full of integers is
  a column of integers, and saying so is the useful behaviour.

## 6. Test data

Two real files, neither constructed for this tool, both already on the machine:

- **ESMA transparency-opinion annex** (regulatory publication) — has a UTF-8
  BOM, quoted fields containing commas, `03/06/2020` dates that are genuinely
  ambiguous, accented text (`Comisión Nacional de Valores`), and a column that
  is `None` for nearly every row. Exercises D1, D3, D8.
- **TradingView OHLCV export** — epoch-second timestamps that are valid
  integers but mean dates, a `№` in a header name, floats with 16 significant
  digits, and eight columns that are entirely empty. Exercises D5, D11, D13.

Plus a generated multi-million-row file for the streaming test, which is the one
case where constructing the data is the point.
