"""The library half: no printing, no click, just the counting."""


def word_count(text: str) -> dict[str, int]:
    """Count words case-insensitively, in first-appearance order."""
    counts: dict[str, int] = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts
