"""Topic 1 — Data structures: list, dict, set, tuple.

What each costs and when to reach for it.

Run it:      uv run phase-00/step-0.1-the-language/01_data_structures.py
The demos print. The exercises at the bottom fail until you write them.
"""

import time
from collections import Counter, defaultdict

# =========================================================== 1. The four
# Python gives you four workhorses. The differences are not stylistic —
# each one is a different data structure underneath, with different costs.

books = ["Dune", "Neuromancer", "Dune"]          # list  — ordered, mutable, duplicates OK
prices = {"Dune": 9.99, "Neuromancer": 12.50}    # dict  — key -> value, fast lookup
genres = {"scifi", "cyberpunk", "scifi"}         # set   — unique, unordered
point = (3, 7)                                   # tuple — immutable, fixed shape

print("list ", books, "  len", len(books))
print("dict ", prices)
print("set  ", genres, " <- the duplicate vanished")
print("tuple", point)


# =========================================================== 2. list
# An array of pointers. Index and append are cheap; anything that shifts
# every element (insert at the front, delete from the front) is not.

nums = [4, 1, 9, 2]
nums.append(7)          # cheap: goes on the end
nums.insert(0, 0)       # expensive: every other element shifts right
print("\nlist ops     ", nums)
print("slice [1:4]  ", nums[1:4], " <- a NEW list, not a view (unlike NumPy)")
print("sorted       ", sorted(nums), " vs in-place .sort() which returns None")

# `in` on a list scans from the front. Fine for 10 items, a problem for 10 million.
print("membership   ", 9 in nums, "-> walks the list until it finds 9")


# =========================================================== 3. dict
# A hash table. Lookup by key is O(1) regardless of size — this is the
# single most useful fact in Python. Insertion order is preserved (3.7+).

print("\nlookup       ", prices["Dune"])
print(".get missing ", prices.get("Snow Crash"), " <- None instead of KeyError")
print(".get default ", prices.get("Snow Crash", 0.0))

prices["Snow Crash"] = 11.00
print("after insert ", prices, " <- insertion order kept")

for title, price in prices.items():          # .items() when you want both
    print(f"  {title:<12} {price:>6.2f}")

# Keys must be HASHABLE — immutable, essentially. This is why tuples matter.
grid = {(0, 0): "start", (3, 7): "goal"}     # tuple key: fine
print("tuple as key ", grid[(3, 7)])
try:
    {[0, 0]: "start"}                        # list key: not fine
except TypeError as e:
    print("list as key  ", e)


# =========================================================== 4. set
# A hash table with no values. Two things it is unbeatable at:
# membership testing, and answering questions about overlap.

a = {"pandas", "numpy", "torch"}
b = {"numpy", "scipy"}
print("\nunion        ", a | b)
print("intersection ", a & b)
print("difference   ", a - b, " <- in a but not b")
print("symmetric    ", a ^ b, " <- in one but not both")
print("dedupe a list", list(set(["x", "y", "x", "z"])), " <- order is NOT preserved")


# =========================================================== 5. tuple
# Immutable. Use it for a fixed-shape record, and anywhere you need
# something hashable. Unpacking is where it really earns its place.

x, y = point
print("\nunpacked     ", x, y)

first, *rest = [10, 20, 30, 40]
print("star unpack  ", first, rest)

# Swapping without a temp variable — a tuple is being built and unpacked here.
x, y = y, x
print("swapped      ", x, y)

try:
    point[0] = 99
except TypeError as e:
    print("immutable    ", e)


# =========================================================== 6. Cost
# The table everyone should know by heart. n = number of items.
#
#   operation              list      dict      set
#   ---------------------------------------------------
#   x in thing             O(n)      O(1)      O(1)
#   thing[i] / thing[key]  O(1)      O(1)       --
#   append / add           O(1)      O(1)      O(1)
#   insert / delete front  O(n)       --        --
#   ordered?               yes       yes       no
#
# O(n) versus O(1) is not an abstraction. Here it is in wall-clock time:

n = 200_000
haystack_list = list(range(n))
haystack_set = set(haystack_list)
needle = n - 1                      # worst case: the very last element

t0 = time.perf_counter()
needle in haystack_list
list_time = time.perf_counter() - t0

t0 = time.perf_counter()
needle in haystack_set
set_time = time.perf_counter() - t0

print(f"\nmembership in {n:,} items")
print(f"  list {list_time * 1e6:8.1f} µs")
print(f"  set  {set_time * 1e6:8.1f} µs")
print(f"  set is ~{list_time / set_time:,.0f}x faster, and the gap grows with n")


# =========================================================== 7. Choosing
# The decision rule, in order:
#
#   Do I look things up by a key?          -> dict
#   Do I only care whether it's present?   -> set
#   Is the shape fixed and never changes?  -> tuple
#   Otherwise                              -> list
#
# The most common real mistake is using a list for membership testing.
# If you find yourself writing `if x in some_long_list`, make it a set.


# =========================================================== 8. Idioms
# Four patterns that replace a lot of clumsy code.

words = ["red", "blue", "red", "green", "blue", "red"]

# Counting: don't hand-roll it.
print("\nCounter      ", Counter(words))
print("most common  ", Counter(words).most_common(2))

# Grouping: defaultdict removes the "does the key exist yet?" dance.
by_letter = defaultdict(list)
for w in words:
    by_letter[w[0]].append(w)
print("defaultdict  ", dict(by_letter))

# Comprehensions work for dicts and sets too, not just lists.
print("dict comp    ", {w: len(w) for w in set(words)})
print("set comp     ", {len(w) for w in words})

# enumerate and zip, instead of indexing by hand.
for i, w in enumerate(words[:3], start=1):
    print(f"  {i}. {w}")


# =========================================================== 9. The trap
# Assignment never copies. Two names can point at the same object, and
# mutating through one is visible through the other.

original = [1, 2, 3]
alias = original            # NOT a copy
alias.append(4)
print("\naliasing     ", original, " <- appending to `alias` changed `original`")

copy = original[:]          # a real (shallow) copy
copy.append(5)
print("after copy   ", original, copy)

# "Shallow" matters: the outer list is new, the inner objects are shared.
nested = [[1, 2], [3, 4]]
shallow = nested[:]
shallow[0].append(99)
print("shallow copy ", nested, " <- the inner list was shared")
# For a full copy: copy.deepcopy(nested)


# =========================================================== EXERCISES
# Replace each `raise NotImplementedError` with real code.
# Re-run the file; the checks at the bottom tell you how you're doing.

def unique_preserving_order(items):
    """Remove duplicates but keep first-seen order.

    `list(set(items))` loses the order — solve it properly.
    unique_preserving_order([3, 1, 3, 2, 1]) -> [3, 1, 2]
    """
    raise NotImplementedError


def word_frequencies(text):
    """Count words in a string, case-insensitively.

    Return a plain dict. word_frequencies("the The cat") -> {"the": 2, "cat": 1}
    """
    raise NotImplementedError


def invert(mapping):
    """Swap keys and values. Assume the values are unique and hashable.

    invert({"a": 1, "b": 2}) -> {1: "a", 2: "b"}
    """
    raise NotImplementedError


def group_by_length(words):
    """Group words by their length.

    group_by_length(["hi", "to", "cat"]) -> {2: ["hi", "to"], 3: ["cat"]}
    """
    raise NotImplementedError


def only_in_first(a, b):
    """Items in list `a` that are not in list `b`, order preserved, no duplicates.

    Make this O(n), not O(n*m) — that is the whole point of the exercise.
    only_in_first([1, 2, 3, 2], [2]) -> [1, 3]
    """
    raise NotImplementedError


# =========================================================== CHECKS
CHECKS = [
    ("unique_preserving_order", lambda: unique_preserving_order([3, 1, 3, 2, 1]), [3, 1, 2]),
    ("word_frequencies", lambda: word_frequencies("the The cat"), {"the": 2, "cat": 1}),
    ("invert", lambda: invert({"a": 1, "b": 2}), {1: "a", 2: "b"}),
    ("group_by_length", lambda: group_by_length(["hi", "to", "cat"]), {2: ["hi", "to"], 3: ["cat"]}),
    ("only_in_first", lambda: only_in_first([1, 2, 3, 2], [2]), [1, 3]),
]

print("\n" + "=" * 52)
passed = 0
for name, call, expected in CHECKS:
    try:
        got = call()
    except NotImplementedError:
        print(f"  ·  {name:<24} not written yet")
        continue
    except Exception as e:
        print(f"  ✗  {name:<24} raised {type(e).__name__}: {e}")
        continue
    if got == expected:
        print(f"  ✓  {name}")
        passed += 1
    else:
        print(f"  ✗  {name:<24} got {got!r}, expected {expected!r}")
print(f"{passed}/{len(CHECKS)} exercises passing")
