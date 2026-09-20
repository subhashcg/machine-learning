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


@pytest.mark.parametrize("text, expected", [
    ("", {}),                                        # empty string: no words, not an error
    ("one", {"one": 1}),
    ("a b a", {"a": 2, "b": 1}),
    ("The the THE cat", {"the": 3, "cat": 1}),       # case is folded before counting
    ("  spaced \t out \n ", {"spaced": 1, "out": 1}),  # split() eats any run of whitespace
])
def test_word_count_cases(text, expected):
    assert word_count(text) == expected


def test_word_count_keeps_punctuation_attached():
    # Documenting current behaviour, not endorsing it: split() is whitespace-only,
    # so "hello," and "hello" are two different words. A future edit that strips
    # punctuation would be a real change, and this test will notice.
    assert word_count("Hello, hello world.") == {"hello,": 1, "hello": 1, "world.": 1}


def test_average_length_is_a_float():
    # 1 + 3 + 5 = 9 over 3 words; approx because the result is a float division
    assert average_length(["a", "abc", "abcde"]) == pytest.approx(3.0)
    assert average_length(["ab", "abcd", "a"]) == pytest.approx(7 / 3)


def test_average_length_rejects_empty():
    with pytest.raises(ValueError, match="at least one word"):
        average_length([])


def test_top_n_orders_by_frequency():
    assert top_n("a b b c c c") == [("c", 3), ("b", 2), ("a", 1)]


def test_top_n_defaults_to_three_and_never_returns_more_than_it_has():
    text = "a b b c c c d d d d"
    assert len(top_n(text)) == 3, "the default n is 3"
    assert top_n(text, n=99) == [("d", 4), ("c", 3), ("b", 2), ("a", 1)]


def test_top_n_tie_is_broken_by_first_appearance():
    # The docstring calls this "whichever word the sort happened to reach first",
    # which is an admission that it was never decided. What it ACTUALLY does:
    # word_count returns a dict in insertion order (first appearance in the text),
    # and sorted() is stable, so equal counts keep that order.
    # Pinned down here so a future edit cannot change it silently — this records
    # the behaviour, it does not endorse it as a good rule.
    assert top_n("b b a a c") == [("b", 2), ("a", 2), ("c", 1)]
    assert top_n("a a b b c") == [("a", 2), ("b", 2), ("c", 1)]


@pytest.fixture
def words_file(tmp_path):
    """A small UTF-8 file on disk, thrown away after each test."""
    path = tmp_path / "words.txt"
    path.write_text("The cat\nsat ON the MAT\n", encoding="utf-8")
    return path


def test_load_words_reads_and_lowercases(words_file):
    assert load_words(words_file) == ["the", "cat", "sat", "on", "the", "mat"]


def test_load_words_feeds_the_other_functions(words_file):
    assert word_count(" ".join(load_words(words_file)))["the"] == 2
    assert average_length(load_words(words_file)) == pytest.approx(17 / 6)


def test_load_words_missing_file(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_words(tmp_path / "nope.txt")
