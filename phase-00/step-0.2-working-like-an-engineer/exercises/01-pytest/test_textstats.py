"""1. Write a real test suite

`textstats.py` sits next to this file. Write tests for it here.

Run with:

    uv run pytest phase-00/step-0.2-working-like-an-engineer/exercises/01-pytest -v

What the meta-checks below require of you — they inspect this file and your
test results, so the tests themselves are the exercise:

  - at least 8 test functions, all named test_*
  - a @pytest.mark.parametrize with at least 4 cases, covering word_count
    (include the empty string, and text where case matters)
  - a pytest.raises for average_length([]) that uses match=
  - a pytest.approx somewhere (average_length returns a float)
  - a fixture that builds a file with tmp_path, used by at least two tests
  - a test for load_words on a missing file
  - a test that pins down the TIE-BREAKING behaviour of top_n — decide what it
    actually does and assert it, rather than avoiding the case

Do not modify textstats.py. If you think a function is wrong, write a test that
documents what it currently does and say so in a comment.
"""

import pytest

from textstats import word_count, top_n, average_length, load_words


# TODO: your tests
