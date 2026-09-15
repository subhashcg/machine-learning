"""1. squares_of_evens(numbers)

Squares of the even numbers, in order, as a list.

    [1, 2, 3, 4, 5, 6]  ->  [4, 16, 36]

One comprehension. Then the loop version beside it — keep both, so the
difference in what each one *says* is on the page.
"""


def squares_of_evens(numbers):
    # TODO — comprehension
    pass


def squares_of_evens_loop(numbers):
    # TODO — the same thing, written as a loop
    pass


if __name__ == "__main__":
    print(squares_of_evens([1, 2, 3, 4, 5, 6]))
    print(squares_of_evens_loop([1, 2, 3, 4, 5, 6]))
    print(squares_of_evens([]))
    print(squares_of_evens([1, 3, 5]))
