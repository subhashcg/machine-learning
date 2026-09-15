"""4. group_by_length(words)

Group words by their length.

    ["hi", "to", "cat"]  ->  {2: ["hi", "to"], 3: ["cat"]}
"""
from collections import defaultdict

def group_by_length(words):
    """Returns words grouped by their length.
    """
    groups = defaultdict(list)
    for word in words:
        word_length = len(word)
        groups[word_length].append(word)
    return dict(groups)

if __name__ == "__main__":
    print(group_by_length(["hi", "to", "cat"]))
    print(group_by_length([]))
    print(group_by_length(["a", "bb", "cc", "ddd", "e"]))
