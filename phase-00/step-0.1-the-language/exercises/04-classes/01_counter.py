"""1. Counter

Rewrite Topic 3's make_counter as a class: increment(), read(), and a reset()
the closure version couldn't easily add.

Then show the two are equivalent by running the same sequence through both and
printing the results side by side. In a comment, say what the class gained and
what it lost versus the closure.
"""


def make_counter():
    """Topic 3, exercise 5 — here for comparison."""
    count = 0

    def increment():
        nonlocal count
        count += 1

    def read():
        return count

    return increment, read


class Counter:
    # TODO
    pass


if __name__ == "__main__":
    # TODO: run the same sequence through both, side by side

    # TODO: show reset()

    # TODO: comment — what the class gained, what it lost
    pass
