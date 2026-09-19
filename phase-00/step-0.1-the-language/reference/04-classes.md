# Reference — classes

Lookup card. The judgement calls belong in your own `NOTES.md`.

## A class is a closure with syntax

```python
def make_counter():              class Counter:
    count = 0                        def __init__(self):
    def increment():                     self.count = 0
        nonlocal count               def increment(self):
        count += 1                       self.count += 1
    def read(): return count         def read(self):
    return increment, read               return self.count
```

Both bundle **state with the behaviour that operates on it**. The closure hides
its state completely; the class names it and scales past two functions.

---

## `self` is just the first parameter

```python
c.increment()          # sugar for
Counter.increment(c)   # this
```

A method is a plain function whose first argument is the instance. Consequences:

```python
def shout(self): return self.name.upper()
Dog.shout = shout          # attaching a function to a class at runtime works
f = Dog.speak; f(d)        # pulling one off gives the function back
```

**Why explicit?** Python has no implicit instance scope. A bare name inside a
method is a *local*, resolved by LEGB — there is no "I" in LEGB. So `self.` is not
ceremony; it is the only way to say "the instance's one". In Java a bare `name`
might mean `this.name`; in Python it never can.

`@staticmethod` (no first arg) and `@classmethod` (`cls` = the class) are ordinary
decorators changing what gets passed first — not language magic.

---

## Instance vs class attributes

```python
class Dog:
    species = "canis"          # CLASS — one, shared
    def __init__(self, name):
        self.name = name       # INSTANCE — one per object
```

```
Dog.species = "lupus"   ->  every instance sees it
a.species = "override"  ->  creates an INSTANCE attribute that shadows the class one
a.__dict__              ->  {'name': 'Rex', 'species': 'override'}
```

**Reading falls through instance → class. Writing always lands on the instance.**
Identical shape to LEGB one level up.

### The trap

```python
class Basket:
    items = []                          # shared by EVERY instance
    def add(self, x): self.items.append(x)
```
```
x.add("apple"); y.add("pear")
x.items -> ['apple', 'pear']    y.items -> ['apple', 'pear']    one list
```

`self.items.append(x)` contains **no assignment** — it reads `self.items` (falling
through to the class) and mutates what it finds. No instance attribute is ever
created. Build mutable state in `__init__`.

Fourth costume of the reference rule: `[[0]*cols]*rows`, `a[:]`, `basket=[]`, and
now this.

---

## Dunder methods

| method | powers |
|---|---|
| `__init__` | construction |
| `__repr__` | the REPL, debuggers, tracebacks — **write this one** |
| `__str__` | `print()`, `str()`; falls back to `__repr__` |
| `__eq__` | `==` |
| `__hash__` | dict keys, set members |
| `__lt__` | `<`, and therefore `sorted()` |
| `__len__` | `len()`, and truthiness |
| `__getitem__` | `obj[key]`, and iteration if no `__iter__` |
| `__iter__` / `__next__` | `for`, generators |
| `__enter__` / `__exit__` | `with` |
| `__call__` | `obj()` |

`__repr__` should ideally be something you could paste back in: `Money(10, 'GBP')`.
Without one you get `<Money object at 0x104...>` in every traceback.

### Defining `__eq__` removes `__hash__`

```python
class NoHash:
    def __eq__(self, o): return True
{NoHash()}   ->  TypeError: unhashable type: 'NoHash'
```

Deliberate. `a == b` must imply `hash(a) == hash(b)`, or equal objects land in
different buckets and become unfindable — the stranded key from Topic 1. Python
cannot guess which fields you compared, so it refuses.

Fix: hash the same tuple you compared.

```python
def __eq__(self, o): return (self.a, self.b) == (o.a, o.b)
def __hash__(self):  return hash((self.a, self.b))
```

`@dataclass(frozen=True)` writes both, correctly, for free.

---

## `@property`

A method accessed like an attribute — no parentheses. Callers cannot tell whether
it is stored or computed, which is the whole point.

```python
@property
def area(self): return self.w * self.h      # read
@area.setter
def area(self, v): ...                      # write   (optional)
@area.deleter
def area(self): ...                         # del     (rare)
```

- **Getter alone is fine** — that is a read-only attribute, and the common case.
- **A setter without a getter is impossible**: `@x.setter` is a method call on the
  property object that `@property` created.
- The decorated functions must all share the **same name** — each returns a new
  `property` object rebound to that class attribute.

```
type(Demo.v) -> property      Demo.v.fget -> <function>      Demo.v.fset -> None
```

Sugar for `v = property(fget=..., fset=..., fdel=...)`.

### Why it matters: derived values go stale

```python
self.area = w * h          # stored at construction
r.w = 10                   # -> w=10 h=3 area=6     a lie, silently
```

**If a value is derived from other attributes, compute it — don't store it.**
Storing creates a second source of truth you must keep in sync on every path.

### And it lets you add validation later

Ship a plain attribute; turn it into a property when you need checks. **Every
existing call site still works.** This is why Python code has no
`getX()`/`setX()` written "just in case" — the upgrade is free.

Inside a setter, store to `self._x`, not `self.x` — the latter recurses forever.

### When not to

Expensive work (callers expect attribute access to be cheap — use a method or
`functools.cached_property`), or anything with side effects.

---

## `@dataclass`

```python
from dataclasses import dataclass, field

@dataclass
class Point:
    x: float
    y: float = 0.0
    tags: list = field(default_factory=list)
```

Generates `__init__`, `__repr__`, `__eq__` from the annotations.
`frozen=True` adds immutability and `__hash__`; `order=True` adds comparisons.

### `field(default_factory=list)` — three parts on one line

```
tags:  list  =  field(default_factory=list)
^name  ^type    ^default
```

The first `list` is the **annotation**; the second is a **callable** — `list`
without parentheses is the list constructor, called once per instance. Same
distinction as `key=len` versus `key=len()`.

### A mutable default is a hard error

```
tags: list = []  ->  ValueError: mutable default <class 'list'> for field tags is
                     not allowed: use default_factory
```

The test is **hashability**, not the annotation:

```
0.0  "text"  (1, 2)  None   allowed
[]   {}      set()          REJECTED
```

`y: float = 0.0` is fine because floats are immutable — the default *is* shared
(`a.y is b.y` is True), but nothing can reveal it: every "change" rebinds rather
than mutates.

### Annotations are not enforced

```
P("not an int")  ->  P(x='not an int')
```

They are metadata. The dataclass reads them to find fields; nothing checks types
at runtime. That is `mypy`'s job — Topic 8.


---

## Inheritance

```python
class Animal:
    def speak(self): return "..."
    def describe(self): return f"{self.name} says {self.speak()}"

class Dog(Animal):
    def speak(self): return "woof"
```

`describe()` is written once and calls whichever `speak()` the object actually
has. The caller never branches on type.

### `super()`

```python
class Cat(Animal):
    def __init__(self, name, indoor=True):
        super().__init__(name)        # or the parent's setup never runs
        self.indoor = indoor
```

Override `__init__` and you must call `super().__init__(...)` unless you mean to
replace construction entirely. Forgetting it gives `AttributeError` later, far
from the cause.

**`super()` is not "my parent"** — it is "the next class in this object's MRO":

```python
class B(A): def who(self): return "B -> " + super().who()
class C(A): def who(self): return "C -> " + super().who()
class D(B, C): pass

D.__mro__   ->  ['D', 'B', 'C', 'A', 'object']
D().who()   ->  'B -> C -> A'          B's super() reached C, not A
```

### isinstance follows the chain; type() does not

```
isinstance(d, Dog)     -> True
isinstance(d, Animal)  -> True     <- the basis of `except AppError`
type(d) is Animal      -> False
```

`except SomeError` is an isinstance check. Prefer `isinstance` over
`type(x) is Y`, which rejects subclasses and defeats the point.

### Composition over inheritance

**Inheritance is IS-A; composition is HAS-A.**

```python
class CarInherits(Engine): ...          # a Car IS an Engine? no
class CarComposes:
    def __init__(self): self.engine = Engine()
```

Inheriting drags in every parent method forever and fixes you to one. Two
engines, or a swappable engine, is impossible by inheritance and trivial by
composition.

### The substitutability test

A subclass must be usable anywhere the parent is:

```python
def stretch(rect):          # written against Rectangle
    rect.w = 10
    return rect.area()

stretch(Square(2))  ->  20      the square is now 10x2
```

A mutable `Rectangle` promises width and height move independently; `Square`
cannot keep that promise. Mathematically IS-A, programmatically not.
**Inheriting means promising to honour every contract the parent's callers rely
on.** When in doubt, compose.

### Abstract base classes

```python
from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def save(self, key, value): ...
    def save_many(self, items):              # concrete, shared
        for k, v in items.items(): self.save(k, v)
```

```
Storage()     -> TypeError: Can't instantiate abstract class Storage with abstract method save
Incomplete()  -> TypeError: ... with abstract method save
```

The error arrives at **instantiation**, not at first call, so a half-finished
implementation fails immediately. An ABC can mix required methods with shared
concrete ones — which is how scikit-learn's estimator API is built.

### Exceptions are just classes

```
ConfigError.__mro__ -> ['ConfigError', 'AppError', 'Exception', 'BaseException', 'object']
```

Nothing special about them. `except AppError` catches `ConfigError` for the same
reason `isinstance(dog, Animal)` is True.
