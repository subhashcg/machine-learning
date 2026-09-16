"""1. squares_of_evens(numbers)

Squares of the even numbers, in order, as a list.

    [1, 2, 3, 4, 5, 6]  ->  [4, 16, 36]

One comprehension. Then the loop version beside it — keep both, so the
difference in what each one *says* is on the page.
"""


def squares_of_evens(numbers):
    """Filter even numbers and then do the squares
    """
    return [x * x for x in numbers if x % 2 == 0]


def squares_of_evens_loop(numbers):
    squares = []
    for x in numbers:
        if x % 2 == 0:
            squares.append(x * x)
    return squares


if __name__ == "__main__":
    print(squares_of_evens([1, 2, 3, 4, 5, 6]))
    print(squares_of_evens_loop([1, 2, 3, 4, 5, 6]))
    print(squares_of_evens([]))
    print(squares_of_evens([1, 3, 5]))
