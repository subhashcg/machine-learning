"""2. word_lengths(words)

A dict mapping each word to its length, lowercased, duplicates collapsed.

    ["Cat", "hello", "cat"]  ->  {"cat": 3, "hello": 5}

Dict comprehension, one line.
"""


def word_lengths(words):
    """item in list needs to be string.
    we convert the word to lower to ensure correct reporting of length incase it chagnes becuase of lower
    """
    return {w: len(w) for w in (word.lower() for word in words)}

if __name__ == "__main__":
    print(word_lengths(["Cat", "hello", "cat"]))
    print(word_lengths([]))
    print(word_lengths(["a", "A", "a"]))
