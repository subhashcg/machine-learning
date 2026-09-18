# Exercises — Topic 4, classes

Write these in `exercises/04-classes/`. Standard library only.
A `print` per function, and an `if __name__ == "__main__":` guard.

---

**1. `Counter`**  ·  `01_counter.py`

Rewrite Topic 3's `make_counter` as a class: `increment()`, `read()`, and a
`reset()` the closure version couldn't easily add.

Then show the two are equivalent by running the same sequence through both and
printing the results side by side. In a comment, say what the class gained and
what it lost versus the closure.

---

**2. `Basket` and `BasketOk`**  ·  `02_class_attribute.py`

`Basket` puts `items = []` at class level. `BasketOk` builds it in `__init__`.

Show two instances of each, with output that makes the sharing obvious. Then
prove it with `is`, not just by eye.

In a comment, explain why `self.items.append(x)` reaches the class attribute
while `self.items = [x]` would not.

---

**3. `Money`**  ·  `03_dunders.py`

Fields `amount` and `currency`. Implement `__repr__`, `__str__`, `__eq__`,
`__hash__`, `__lt__` and `__add__`.

Demonstrate each: repr vs str, equality vs identity, sorting a list of them,
using them as dict keys, and adding two.

Then write a `BadMoney` with `__eq__` but no `__hash__`, and show what breaks.
Make `__add__` refuse to add different currencies.

---

**4. `RectStored` and `RectComputed`**  ·  `04_property_staleness.py`

`RectStored` computes `self.area` in `__init__`. `RectComputed` makes `area` a
`@property`.

Change `w` on both and print all three values for each. One of them will be
lying. Also show what happens when you try to assign to the computed `area`.

---

**5. `Temperature`**  ·  `05_property_validation.py`

Stores celsius. Give it:

- a validating setter — below absolute zero (-273.15) raises `ValueError`
- a read-only `fahrenheit` property, computed
- a `kelvin` property with both getter and setter, where setting kelvin updates
  celsius

Show that setting `kelvin` changes `celsius` and `fahrenheit` consistently, and
that an invalid temperature is refused from either direction.

---

**6. `Point` and `Config`**  ·  `06_dataclasses.py`

`Point(x, y)` as a `@dataclass`. Show the generated `__repr__` and `__eq__`.

`Config` with a `list`, a `dict` and a non-empty list default — all three via
`field(default_factory=...)`. Prove two instances don't share.

Then, inside a `try`, define a dataclass with `tags: list = []` and print the
error. In a comment, say what test the dataclass is actually applying.

---

**7. `Grade`**  ·  `07_design.py`

A student's grade: a `score` (0–100), a read-only `letter` derived from it, and a
`passed` boolean also derived.

Decide for each of the three whether it should be a plain attribute, a
`@property`, or a method — and write a comment justifying each choice. Then
implement it.

Make `score` reject values outside 0–100. Show that changing `score` updates
`letter` and `passed` with no extra work.
