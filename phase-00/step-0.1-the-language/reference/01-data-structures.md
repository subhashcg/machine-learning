# Reference — list, dict, set, tuple

Lookup card. The judgement calls belong in your own `NOTES.md`.

## At a glance

| | ordered | mutable | duplicates | hashable | lookup |
|---|---|---|---|---|---|
| `list` | yes | yes | yes | no | O(n) by value, O(1) by index |
| `dict` | yes (insertion) | yes | keys unique | no | O(1) by key |
| `set` | **no** | yes | **no** | no | O(1) |
| `tuple` | yes | **no** | yes | **yes** | O(n) by value, O(1) by index |

*"Hashable" = can itself be a dict key or set member.*

---

## list — `[1, 2, 3]`

An array of **references**, in order. The default container when you just have
a sequence of things.

**Cheap** — `x[i]`, `.append()`, `.pop()` from the end, iteration.
**Expensive** — `x in list` (O(n)), `.insert(0, …)` and `.pop(0)` (O(n): everything shifts).

Use it when order matters, duplicates are fine, and you mostly iterate.
Don't use it for repeated membership tests — that's the single most common
Python performance bug.

```python
xs.append(4)        xs.insert(0, 4)     # O(1) vs O(n)
xs[1:4]             # a new list (a shallow copy), not a view
sorted(xs)          # returns a new list
xs.sort()           # in place, returns None
```

---

## dict — `{"a": 1}`

A hash table: key → value. Finds a value by key in **constant time regardless
of size**. Keys are unique and must be hashable. Insertion order preserved (3.7+).

The most-used structure in Python, and the reason is the O(1), not the pairing.

```python
d.get(k)             # None instead of KeyError
d.get(k, default)
d.setdefault(k, [])  # get, inserting the default if missing
d.items() / .keys() / .values()
{k: v for k, v in pairs}

k in d               # O(1)  — tests KEYS
v in d.values()      # O(n)  — scans. easy to write by accident
```

`collections.Counter` — a dict that counts; missing keys return `0`; `.most_common(n)`.
`collections.defaultdict(list)` — auto-creates the default, removes the
"does this key exist yet?" dance when grouping.

---

## set — `{1, 2}` (empty set is `set()`, not `{}`)

A hash table with no values. Two things it is unbeatable at: **membership
testing** and **overlap questions**. Unordered; elements must be hashable.

Deduplication is a side effect of the mechanism, not the purpose.

```python
a | b    union            a & b    intersection
a - b    difference       a ^ b    symmetric difference
a <= b   subset
```

Costs ~4× a list's memory — the empty slots are what keep lookups O(1). Worth it
the moment you test membership more than a handful of times.

`frozenset` — the immutable version, so it *is* hashable and can be a dict key.

---

## tuple — `(1, 2)` (single element needs the comma: `(1,)`)

Immutable, so **hashable** — and that, not the fixed size, is the point. It is
what lets you key by more than one field:

```python
sales[("2026-09", "north")] += 1
grid[(row, col)] = cell
seen = {(user_id, article_id)}
```

Hashability goes all the way down: `(1, [2])` is **not** hashable, because the
inner list can still change.

Also the shape of multiple return values and of unpacking:

```python
x, y = point
first, *rest = xs
x, y = y, x           # a tuple is built and unpacked
```

---

## Complexity

| operation | list | dict | set |
|---|---|---|---|
| `x in thing` | O(n) | O(1) | O(1) |
| `thing[i]` / `thing[key]` | O(1) | O(1) | — |
| append / add / insert key | O(1) | O(1) | O(1) |
| insert or delete at front | O(n) | — | — |
| iterate | O(n) | O(n) | O(n) |

**The accidental quadratic.** One `x in list` is O(n). Inside a loop over m items
it becomes O(n·m) — and the multiplier squares as data grows: 5× the rows, 25× the
time. Rule: *the moment a membership test goes inside a loop, the thing being
searched should be a set.*

```python
[x for x in a if x not in b]        # O(n·m)   — 6.3 s at n=40,000
bs = set(b)
[x for x in a if x not in bs]       # O(n+m)   — 0.7 ms
```

---

## Hashable or not

```
yes   int  float  str  bytes  bool  None  tuple(of hashables)  frozenset
NO    list  dict  set  tuple containing any of those
```

A mutable key would be filed under its old hash and become **unreachable** after
mutation — still in the dict, findable by nothing. Python raises `TypeError`
upfront rather than let that happen silently.

---

## Copying

Assignment never copies — it binds another name to the same object.

```python
b = a            # same object
b = a[:]         # SHALLOW copy: new outer list, same inner objects
b = list(a)      # same as a[:]
b = copy.deepcopy(a)   # copies all the way down; slow on big structures
```

Shallow means **mutating an element reaches both, replacing one doesn't**:

```python
b[0].append(99)   # mutates the shared inner list  -> a sees it
b[0] = ["new"]    # rebinds b's slot only          -> a unaffected
```

Same trap when building grids — `*` replicates the reference:

```python
[[0, 0]] * 3                       # three references to ONE list
[[0, 0] for _ in range(3)]         # three separate lists
```

---

## Choosing

```
Do I look things up by a key?           -> dict
Do I only need "is it present?"         -> set
Is the shape fixed, or do I need a key? -> tuple
Otherwise                               -> list
```

A dict's keys are already a hash table, so a dict gives you the set for free —
`k in counts` is as fast as `k in seen`. Don't keep both.
