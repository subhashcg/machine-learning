# Exercises — Topic 2, comprehensions and generators

Write these in `phase-00/step-0.1-the-language/exercises/`. Standard library only.

Add a `print` per function, and an `if __name__ == "__main__":` guard.

---

**1. `squares_of_evens(numbers)`**

Squares of the even numbers, in order, as a list.

```
[1, 2, 3, 4, 5, 6]  ->  [4, 16, 36]
```

One comprehension. Then write the loop version beside it and keep both, so the
difference in what each one *says* is on the page.

---

**2. `word_lengths(words)`**

A dict mapping each word to its length, lowercased, duplicates collapsed.

```
["Cat", "hello", "cat"]  ->  {"cat": 3, "hello": 5}
```

Dict comprehension, one line.

---

**3. `flatten(nested)`**

Flatten one level.

```
[[1, 2], [3], [], [4, 5]]  ->  [1, 2, 3, 4, 5]
```

Nested comprehension. Get the loop order right first time if you can — most
people write it backwards once.

---

**4. `countdown(n)`**

A generator yielding `n, n-1, ... 1`. Then demonstrate, with prints, that:

- calling it runs none of the body
- it resumes where it left off
- it raises `StopIteration` when done

The demonstration is the exercise. Make the output prove each claim.

---

**5. `read_lines(path)` and `count_matching(path, word)`**

`read_lines` is a generator yielding each stripped line of a file.
`count_matching` uses it to count lines containing `word` — **without ever
holding the file in memory**.

Write a small file in the `__main__` block to test against. Use `with`.

---

**6. `first_n(iterable, n)`**

The first `n` items of any iterable, as a list. Must work on a generator, and
must not consume more than `n` items.

```
first_n((x*x for x in range(1000000)), 3)  ->  [0, 1, 4]
```

Write it yourself with a loop first. Then look up `itertools.islice` and write
the one-line version. Keep both.

Prove it doesn't over-consume: pass a generator that prints each value it
produces, and show only `n` lines appear.

---

**7. `exhaustion_demo()`**

Show, with prints, the bug from the discussion: a generator summed twice gives
the right answer and then `0`. Then show the same data as a list behaving
correctly.

Two lines of output and a comment saying why. This is the one you'll thank
yourself for when it happens in real code.
