# Step 0.3 — 🔨 A command-line dataset inspector

Phase 0's project. **You design it and write every line.** I am the reviewer,
not the teacher: I will ask why, push on decisions, and try to break what you
build. I will not write project logic, and I will not hand you a checklist of
functions to fill in.

## The product

A CLI that points at a CSV and tells you what is in it, before you have loaded
it into anything.

```
$ inspect data/sales.csv

data/sales.csv — 1,204 rows × 5 columns

  order_id      integer     1,204 values    0 missing    1 … 1204
  region        text        1,180 values   24 missing    4 distinct
  amount        decimal     1,204 values    0 missing    0.50 … 9,812.00
                            ▁▂▅█▆▃▂▁▁▁
  ordered_at    date        1,199 values    5 missing    2024-01-03 … 2024-12-30
  is_refunded   boolean     1,204 values    0 missing    87 true / 1,117 false
```

That output is an illustration, not a spec. Design your own — but a person
should be able to run it on an unfamiliar file and immediately know whether the
data is usable.

## Requirements

- **Standard library only.** No pandas, no click, no rich. You will feel every
  gap; that is the point, and Phase 2 is the payoff.
- **Infer a type per column** from the values. At minimum: integer, decimal,
  boolean, date, text. A column of `"1"`, `"2"`, `"3"` is integer; one with a
  single `"n/a"` in it is not.
- **Count missing values.** You decide what counts as missing, and document it.
- **Summarise each column** appropriately for its inferred type — a range for
  numbers and dates, distinct counts or frequencies for categories.
- **A text histogram** for numeric columns.
- **Stream the file.** It must work on a CSV larger than memory. If you hold
  every row, you have failed the constraint.
- **An installable package** with a console entry point, `src/` layout, and a
  real test suite.
- **Fail usefully.** A missing file, a malformed row, a file that is not CSV at
  all — each should produce a message that tells the user what to do.

## Decisions that are yours

I will ask about these in review, so decide deliberately rather than by default:

- What counts as a missing value — empty string? `NA`? `null`? whitespace?
- Does one bad value in 10,000 make a column text, or is it an outlier to report?
- How do you infer a date without `dateutil`?
- Streaming means one pass — so how do you compute a histogram, which needs to
  know the range before it can bin anything?
- How much of the file do you read to decide types? All of it? A sample?
- What happens on a 2 GB file? On an empty file? On a file with no header?

## How this step runs

1. **Plan first.** Write `DESIGN.md`: what you are building, the decisions above
   with your answers and reasons, and what you are deliberately not doing.
   Show it to me before writing code.
2. **Build it.** Commit as you go.
3. **I review.** Expect to be asked why, and to have edge cases thrown at your
   parser.
4. **Defend it.** `WRITEUP.md` at the end: the decisions you made, where it
   fails, and who it would mislead.

## Done when

- It runs on a real CSV you did not construct — find one, do not invent one
- `uv run pytest` passes, and the tests cover the decisions, not just the happy path
- It streams: demonstrate it on a file bigger than you would want in memory
- `DESIGN.md` and `WRITEUP.md` are written
- A stranger could clone the repo and run it from the README

## The bar

Not "it works on my example file". The bar is: **would you trust its output on a
file you have never seen, and can you say what it would get wrong?**
