# Exercises — Topic 1, data structures

Write these yourself in `phase-00/step-0.1-the-language/`. Name the file what you
like. Import nothing except `collections` and `copy`.

Add a `print` for each so running the file shows it working.

---

**1. `unique_preserving_order(items)`**

Remove duplicates, keep first-seen order.

```
[3, 1, 3, 2, 1]  ->  [3, 1, 2]
```

Must stay O(n). `set(items)` alone loses the order; scanning a list for
"have I seen this?" makes it quadratic. You need both structures.

---

**2. `word_frequencies(text)`**

Count words in a string, case-insensitively. Return a plain `dict`.

```
"the The cat"  ->  {"the": 2, "cat": 1}
```

Do it twice — once by hand, once with `Counter` — and keep both. Seeing what
`Counter` saves you is the point.

---

**3. `invert(mapping)`**

Swap keys and values. Assume values are unique and hashable.

```
{"a": 1, "b": 2}  ->  {1: "a", 2: "b"}
```

---

**4. `group_by_length(words)`**

Group words by their length.

```
["hi", "to", "cat"]  ->  {2: ["hi", "to"], 3: ["cat"]}
```

---

**5. `only_in_first(a, b)`**

Items in list `a` not in list `b`. Order preserved, no duplicates.

```
([1, 2, 3, 2], [2])  ->  [1, 3]
```

**Must be O(n+m), not O(n·m).** This is the accidental quadratic — get it right
deliberately rather than by luck.

---

**6. `make_grid(rows, cols)`**

Return a `rows × cols` grid of zeros where `grid[0][0] = 9` changes *only* that
cell.

Then write a second function that builds it the broken way, and a line that
proves the two differ.
