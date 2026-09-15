# Reference — comprehensions and generators

Lookup card. The judgement calls belong in your own `NOTES.md`.

## The four comprehension forms

Only the brackets differ.

```python
[x * x for x in xs]        # list
{x % 3 for x in xs}        # set
{x: x * x for x in xs}     # dict
(x * x for x in xs)        # GENERATOR — lazy, not a tuple
```

There is no tuple comprehension. `(...)` gives you a generator; use `tuple(x*x for x in xs)`.

A comprehension is an **expression that builds a collection**. The loop version is
statements that mutate one.

---

## Filter versus transform

Position decides which you get.

```python
[x for x in data if x > 0]          # filter    — result may be SHORTER
[x if x > 0 else 0 for x in data]   # transform — result is SAME LENGTH
```

Trailing `if` selects. Leading ternary maps. Both at once is legal and usually
unreadable:

```python
[x * 2 if x > 0 else 0 for x in data if x is not None]
```

---

## Nesting

Reads left to right, same order as the nested loops it replaces.

```python
[(a, b) for a in "ab" for b in (1, 2)]     # ('a',1) ('a',2) ('b',1) ('b',2)
[x for row in grid for x in row]           # flatten
[[0 for _ in range(cols)] for _ in range(rows)]   # build a grid
```

**Why the grid version is safe.** An expression *inside* a comprehension is
re-evaluated every iteration, so each row is a new list. An expression *outside*
runs once — which is why `[[0] * cols] * rows` builds one row and copies the
reference. Same mechanism as `[[]] * n` and mutable default arguments.

---

## Speed

```
loop + append      19.32 ms
comprehension      16.79 ms      ~13% faster
map + lambda       29.87 ms      slower than both
```

The gain: the loop does a `LOAD_METHOD` lookup for `.append` on every iteration;
the comprehension uses a specialised instruction. 13% is not a reason to choose
one — readability is. And `map` with a `lambda` is *slower*, because the per-item
function call costs more than it saves.

**Stop using a comprehension when** it needs a `try`, has side effects, or runs
past one line. "Build a collection from another" is a comprehension; "do something
to each item" is a loop.

---

## Generators

### Calling a generator function runs nothing

```python
def countdown(n):
    print("starting")
    while n > 0:
        yield n
        n -= 1

c = countdown(3)     # no output — returns a generator object
next(c)              # NOW "starting" prints, returns 3
```

`yield` **suspends** the function — locals, loop position, all frozen — and the
next request resumes it exactly there. Nothing else in Python does this.

When the body ends, the generator raises `StopIteration`. `for` catches that for
you; `next()` does not.

### Memory is the point

```
list comprehension  :    40.4 MB       1,000,000 items
generator expression:  0.00041 MB      99,138x less
sizeof(generator)   : 208 bytes        whatever the length
```

208 bytes for a million items, or a billion — it holds a recipe, not results.
This is how you process a file larger than RAM.

### Time is a wash

```
sum([x*x for x in range(5_000_000)])  ->  193.6 ms
sum( x*x for x in range(5_000_000) )  ->  194.3 ms
```

Same answer, same speed. The list's allocation cost offsets the generator's
per-item suspend/resume. This is a **memory** decision, not a speed one.

### One-shot, and silent about it

```python
g = (x * 2 for x in [1, 2, 3])
sum(g)   ->  12
sum(g)   ->  0        not an error, not None
```

```
sum(exhausted)    ->  0            operations WITH an identity fail silently
any(exhausted)    ->  False
sorted(exhausted) ->  []
max(exhausted)    ->  ValueError   operations WITHOUT one complain
len(generator)    ->  TypeError: object of type 'generator' has no len()
```

Worst bug class in this topic: totals silently become 0 and nothing crashes.
**Need it twice? Make it a list.** Can't afford the list? Restructure so one pass
does both jobs.

### What a generator costs you

No `len()`, no indexing, no slicing, no reuse. In exchange: constant memory, and
you can start work before the input has finished arriving.

---

## Files are already lazy

```python
f = open(path)
hasattr(f, "__next__")   # True — a file object IS an iterator over lines
```

So `(line for line in open(p))` wraps something that already streams. `for line in f:`
is enough. `open()` never blows up on a big file — `list()`, `.readlines()` or a
list comprehension around it does.

```python
import itertools
with open(path) as f:
    first_ten = list(itertools.islice(f, 10))
```

```
read-all then slice :   14.67 MB
islice(f, 10)       :  0.0219 MB      669x less
```

`islice` is slicing for anything iterable — it stops pulling once satisfied.
Generators cannot be sliced with `[:10]`; `islice` is how you do it.

Every `open()` gets a `with`. An unclosed handle survives until the garbage
collector reaches it, and a loop over many files hits `Too many open files`.

---

## The pipeline shape

Generators chain without materialising anything between stages:

```python
with open(path) as f:
    rows    = (line.rstrip("\n") for line in f)
    fields  = (r.split(",") for r in rows)
    wanted  = (fs for fs in fields if fs[2] == "ERROR")
    total   = sum(1 for _ in wanted)
```

One pass, constant memory, no intermediate lists. Each stage pulls one item from
the one before.

`heapq.nlargest(k, iterable)` is the same idea packaged: stream in, hold only k.

---

## Choosing

```
Need it more than once, or need len/indexing?   -> list
Feeding it straight into sum/max/any/join?      -> generator, drop the brackets
Input too big to hold?                          -> generator
Building a lookup table?                        -> dict comprehension
Deduplicating?                                  -> set comprehension
```

A generator saves you holding the **input**. It cannot save you holding the
**output** — so ask "how much must I hold at once?" before assuming it helps.
