"""5. only_in_first(a, b)

Items in list `a` not in list `b`. Order preserved, no duplicates.

    ([1, 2, 3, 2], [2])  ->  [1, 3]

Must be O(n+m), not O(n*m). This is the accidental quadratic — get it right
deliberately rather than by luck.
"""


def only_in_first(a, b):
    """Returns items which are in a but not in b
    Runs with n+m complexity 
    Items must be hashable
    """
    exclude = set(b)
    items_a_minus_b = []
    for item in a:
        if item not in exclude:
            items_a_minus_b.append(item)
            exclude.add(item)
    return items_a_minus_b



if __name__ == "__main__":
    print(only_in_first([1, 2, 3, 2], [2]))
    print(only_in_first([], [1, 2]))
    print(only_in_first([1, 2], []))
    print(only_in_first(["x", "y", "x"], ["y"]))
