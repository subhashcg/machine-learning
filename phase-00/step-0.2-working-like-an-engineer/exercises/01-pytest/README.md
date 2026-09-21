# Exercises — Topic 1, pytest

One exercise, not five. Writing a real test suite *is* the exercise — splitting
it into five would mean five toy suites instead of one honest one.

```
textstats.py           the module under test — do NOT change it
test_textstats.py      your suite goes here
meta_check.py          checks on your suite
```

## Run your tests

```bash
uv run pytest phase-00/step-0.2-working-like-an-engineer/exercises/01-pytest -v
```

## Then check the suite itself

```bash
uv run python phase-00/step-0.2-working-like-an-engineer/exercises/01-pytest/meta_check.py
```

It runs your tests, then parses the file to confirm you used the features the
brief asks for — so the tests you write are what's being marked.

## What's required

- at least **8 test functions**, all `test_*`
- a `@pytest.mark.parametrize` with **4+ cases** covering `word_count`,
  including the empty string and text where case matters
- a `pytest.raises` for `average_length([])`, **with `match=`**
- a `pytest.approx` somewhere
- a **fixture using `tmp_path`**, used by at least two tests
- a test for `load_words` on a missing file
- a test pinning down `top_n`'s **tie-breaking** behaviour

## The one that needs thought

`top_n` has a docstring saying ties are broken by "whichever word the sort
happened to reach first." That's an admission that the behaviour was never
decided.

Work out what it *actually* does, then assert it — with a comment explaining
that you're documenting the behaviour rather than endorsing it. That is what
you do with legacy code you cannot change: pin it down so a future edit can't
alter it silently.

Do not modify `textstats.py`. If you think a function is wrong, write a test
that records what it currently does and say so in a comment.
