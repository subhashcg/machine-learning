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

    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

    def read(self):
        return self.count

    def reset(self):
        self.count = 0

if __name__ == "__main__":
    inc, read = make_counter()
    print(f"Closure counter {read()}")
    inc()
    print(f"Closure counter {read()}")

    counter = Counter()
    print(f"Class counter {counter.read()}")
    counter.increment()
    print(f"Class counter {counter.read()}")

    counter.reset()
    print(f"Class counter after reset {counter.read()}")

    # Class can add more methods without changing the existing functionality. Closure encapsulates data better.
