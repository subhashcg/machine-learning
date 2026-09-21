# WRITEUP — csv-inspect

What was decided, what it gets wrong, and who it would mislead.

The bar for this step was: *would you trust its output on a file you have never
seen, and can you say what it would get wrong?* This document is the second
half of that sentence.

---

## 1. What shipped

A `csv-inspect` console script, an installable `csvinspect` package under
`src/`, and 144 tests. One streaming pass; no dependencies. Measured on this
machine:

| | |
|---|---|
| 2,000,000 rows / 6 columns / 97 MB | 15.4 s, **27 MB peak RSS** |
| memory vs. row count | flat — 10× the rows, <2× the peak (asserted in `test_streaming.py`) |
| throughput | ~130,000 rows/s, so a 2 GB file is ~5 minutes |

Where the code departed from `DESIGN.md`: an `options.py` module was added (the
design listed the settings but not where they live), and two performance
changes — a hand-rolled parser for the four common numeric date layouts, and
integer extremes tracked as `int` rather than `float`. Both are described below.

---

## 2. The decisions, and what they actually cost

### Strict typing was the right call, and it is noisy

D2 says one unparseable value makes a column text, with the near-miss reported.
On the ESMA file this immediately earned its keep and immediately annoyed me,
which is about the right ratio.

The alternative — typing by majority — hides exactly the row you need. The cost
is real though: a column that is 99.99% integer reports as **text**, and the
word "text" is what a skimming reader takes away. The `!` note carries the
truth. Someone who reads only the type column will be misled, and the only
defence is that the note is on the very next line.

### The missing-value list is the decision I am least sure about

D1 treats `NA`, `None`, `-`, `?` and friends as missing. The ESMA file has a
column *Exemptions from the positive assessment* whose literal value is `None`
for 306 of 361 rows — meaning "no exemptions", which is information. The tool
reports it as 306 missing values.

That is wrong, and it is wrong in the most dangerous direction: it reads as
"this column is mostly empty, ignore it" when the column is mostly populated
with a meaningful answer.

There is no way to fix this from inside the file. `None` in that column means
"no exemptions"; `None` in a survey export means the respondent skipped it. So
the mitigation is: the list is printed in `--help`, `--no-default-na` turns it
off entirely, and `test_real_files.py` pins this exact case so nobody
"improves" the list without seeing the cost. **This is the single most likely
way the tool will mislead someone.**

### Dates: the ambiguity is reported, not resolved

D3 keeps every viable format alive and narrows on each value. `03/06/2020` alone
leaves both `%d/%m/%Y` and `%m/%d/%Y`, and the report says so. A single day
above 12 anywhere in the column collapses it to one — which is why type
inference reads the whole file rather than a sample (D5): on the ESMA file the
disambiguating row is not near the top.

What it still gets wrong: a column that is *entirely* ambiguous gets a format
chosen by my priority order (day-first), with a warning. A US user reading
quickly sees a plausible date range built on the wrong convention. The range is
real, the meaning may be transposed, and only the note says so.

It also cannot read `March 3, 2020`, any localised month name, mixed formats
within one column, or bare epochs. Those come out as text, with a near-miss
percentage if most values parsed.

### The histogram is sampled and says so

D4: exact count/min/max/mean/stdev via Welford, bars from a 20,000-value
reservoir. Bin edges come from the exact range, so the axis is right even when
the sample misses the extremes; only the heights are estimated, and the note
appears only when sampling actually happened.

Where this misleads: a rare-but-important bucket — 12 fraudulent transactions
in 2 million rows — will usually not be in the sample, so the histogram shows an
empty bin where the data has a spike. The exact min/max still betray its
existence, which is why they are on the same line.

### Leading zeros, 0/1, and thousands separators

D12 turned out to be the first real bug found by running the tool: I had guarded
`parse_integer` but not `parse_decimal`, so a zip-code column came back as
**decimal 21 … 90,210** — `float("01234") == 1234.0`, the canonical
spreadsheet data-loss bug, reproduced faithfully in my own code within ten
minutes of it existing. Now both reject it and the column is reported as text
with an "looks like an identifier" note.

D13 keeps `0`/`1` columns as integers (with a "may be a flag" note) because such
columns get summed. D14 refuses `1,234.50` and `$19.99` and offers
`--thousands`. All three are cases where a helpful guess destroys information
silently, and a note costs the reader one line.

---

## 3. Where it fails

**Things it gets outright wrong:**

- **A sentinel it does not know about.** `-999`, `-1`, `9999-12-31` and `0000-00-00`
  are extremely common "missing" markers. The tool counts them as real values,
  so a numeric column reads as `-999 … 4,312` with 0 missing, and the mean is
  garbage. It does not attempt sentinel detection, and I would not trust one
  that did.
- **An unterminated quote swallows the file.** One stray `"` makes every later
  line part of that field, and the report shows 1 row. It cannot be told apart
  from a legitimate multi-line field. The tell is the row count, which is why it
  is in the headline. A 4 MB field-size limit turns the pathological case into
  an error instead of an out-of-memory, and both behaviours are pinned by tests.
- **In a single-column file, an empty value and a blank line are the same
  bytes.** Both are dropped, so the row count is lower than a spreadsheet would
  show. With two or more columns the ambiguity disappears. Tested and
  documented rather than papered over.
- **`--tolerance` reports a row count that includes values it excluded.**
  `n_values` counts non-missing cells; the stats exclude the ones that failed to
  parse. The note says how many were dropped, but the two numbers on the line do
  not add up without reading it.

**Things it refuses to do, which will annoy someone:**

- No encoding detection beyond the BOM. A cp1252 file is an error with a
  suggested flag, not a silent `errors="replace"` — deliberately, because
  latin-1 never raises and that is how `café` becomes `cafÃ©` three systems
  downstream.
- No compressed input, no Excel, no JSON output, no correlations, no "data
  quality score". A single number summarising a file is exactly the confident
  wrongness this tool exists to avoid.
- `--no-header` is a flag, not a detection. The tool warns when a header row
  looks entirely like data and otherwise believes you.

**Things that are merely unpolished:**

- A genuinely single-column file always warns that no delimiter was found. It is
  honest and it is noise.
- `--max-distinct` past the cap reports "many distinct" with no estimate.
  HyperLogLog would give an O(1) approximation; it was out of scope.
- Mean and standard deviation are floats even for integer columns, so a column
  of 19-digit ids has an approximate mean. The *range* is exact — integer
  extremes are tracked as `int` precisely because above 2⁵³ a float cannot tell
  neighbouring integers apart, and a range that is off by one is wrong.
  (Found while writing this document, fixed, and tested.)

---

## 4. Who it would mislead

- **Someone who reads the type column and not the notes.** Every hedge lives in
  the `!` lines. A near-miss integer column says "text", and a skim takes that
  at face value.
- **Anyone whose data legitimately contains `NA`, `None`, `-` or `?`.** They
  will see a column reported as mostly missing when it is mostly answered. This
  is observed on a real file, not hypothetical.
- **A US reader looking at an all-ambiguous `dd/mm/yyyy` column.** The range
  looks plausible and the months and days are transposed.
- **Anyone who trusts the histogram shape for rare events.** Sampling hides
  spikes of a few rows in a few million; the exact min/max are the mitigation.
- **Anyone who assumes "0 missing" means "clean".** It means "nothing matched
  the missing-value list" — which says nothing about `-999`, about
  whitespace-only-after-stripping oddities, or about a column of the literal
  string `"NULL "` with a trailing space inside quotes (that one *is* caught,
  because values are stripped).

---

## 5. What I would do next

1. **A `--json` output**, so the report can feed a pipeline instead of only a
   human. It is a second contract, which is why it was deliberately excluded.
2. **Sentinel detection as a *warning* only**: flag a numeric column whose
   minimum is `-999` or `-1` and whose distribution has a gap, and say "this may
   be a missing-value marker". Never act on it.
3. **HyperLogLog for distinct counts**, which would replace "many distinct" with
   "≈48,000 distinct (±2%)" in constant memory.
4. **Speed**: 130k rows/s is respectable for pure Python but the profile is now
   dominated by per-cell function call overhead rather than any one hot spot.
   Phase 2's answer is to stop writing the inner loop in Python at all.

---

## 6. What this step taught me

The technical content was the streaming constraint forcing an honest split
between what can be exact and what must be sampled. But the thing I will
actually carry forward is narrower: **the leading-zero bug was in my own code,
ten minutes after I had written a design document arguing that exact bug was the
most important one to avoid.** Knowing the failure mode is not the same as
having guarded every path to it. The test suite is what closed the gap, and the
test is named after the decision rather than the function, so the next person to
touch `parse_decimal` finds out what it is for.
