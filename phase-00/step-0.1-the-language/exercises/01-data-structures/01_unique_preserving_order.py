def unique_preserving_order(items):
    """Return items with duplicates removed, first-seen order preserved.

      Items must be hashable (int, str, tuple, ...); a list of lists raises
      TypeError. O(n) — uses a set internally for the membership test.
    """
    
    unique_items = set()
    list_with_unique_items = []

    for x in items:
        if x not in unique_items:
            unique_items.add(x)
            list_with_unique_items.append(x)

    return list_with_unique_items

if __name__ == "__main__":
    print(unique_preserving_order([3, 1, 3, 2, 1]))