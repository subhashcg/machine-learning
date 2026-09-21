"""The module under test. Do not change it — write tests for it.

Four functions with deliberate rough edges. Your job is to pin down what they
actually do, including the parts that are arguably wrong.
"""


def word_count(text):
    """Count words, case-insensitively. Returns a plain dict."""
    counts = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts


def top_n(text, n=3):
    """The n most common words, most frequent first.

    Ties are broken by whichever word the sort happened to reach first.
    """
    return sorted(word_count(text).items(), key=lambda kv: -kv[1])[:n]


def average_length(words):
    """Mean word length. Raises ValueError on an empty list."""
    if not words:
        raise ValueError("average_length needs at least one word")
    return sum(len(w) for w in words) / len(words)


def load_words(path):
    """Read a file and return its words, lowercased.

    Reads UTF-8. A missing file raises FileNotFoundError.
    """
    with open(path, encoding="utf-8") as f:
        return f.read().lower().split()
