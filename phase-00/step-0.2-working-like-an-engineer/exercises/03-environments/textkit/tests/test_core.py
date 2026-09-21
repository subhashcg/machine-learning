"""No import path juggling: textkit is installed, so it simply imports."""

import pytest

from textkit import word_count


@pytest.mark.parametrize("text, expected", [
    ("", {}),
    ("hello", {"hello": 1}),
    ("hello hello world", {"hello": 2, "world": 1}),
    ("The the THE cat", {"the": 3, "cat": 1}),
])
def test_word_count(text, expected):
    assert word_count(text) == expected


def test_counts_are_in_first_appearance_order():
    assert list(word_count("b a b")) == ["b", "a"]
