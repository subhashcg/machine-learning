"""The cart: a module-level list of items."""

items = []


def add(x):
    items.append(x)


def total():
    """Return how many items are in the cart."""
    return len(items)
