"""6. first_n(iterable, n)

The first n items of any iterable, as a list. Must work on a generator, and
must not consume more than n items.

    first_n((x*x for x in range(1000000)), 3)  ->  [0, 1, 4]

Write it yourself with a loop first. Then look up itertools.islice and write
the one-line version. Keep both.

Prove it doesn't over-consume: pass a generator that prints each value it
produces, and show only n lines appear.
"""

import itertools

def first_n(iterable, n):
    """
    Returns n items from a iterable object
    """
    n_items = []
    iterable = iter(iterable)
    Done = object()
    for i in range(n):
      next_item = next(iterable, Done)
      if next_item is Done:
          break
      n_items.append(next_item)
    return n_items

def first_n_islice(iterable, n):
    return list(itertools.islice(iterable, 0, n))


def noisy(limit):
    """A generator that announces every value it produces."""
    for i in range(limit):
        print(f"    producing {i}")
        yield i


if __name__ == "__main__":
    print(first_n((x * x for x in range(1_000_000)), 3))
    print(first_n_islice((x * x for x in range(1_000_000)), 3))

    print("proof it stops early:")
    print(first_n(noisy(1_000_000), 3))
