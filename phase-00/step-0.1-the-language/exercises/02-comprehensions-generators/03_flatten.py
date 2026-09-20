"""3. flatten(nested)

Flatten one level.

    [[1, 2], [3], [], [4, 5]]  ->  [1, 2, 3, 4, 5]

Nested comprehension. Get the loop order right first time if you can — most
people write it backwards once.
"""


def flatten(nested):
    """Flatten one level
    Items must be iterable
    """
    return [x for row in nested for x in row]

if __name__ == "__main__":
    print(flatten([[1, 2], [3], [], [4, 5]]))
    print(flatten([]))
    print(flatten([[], []]))
