# Reference — functions

Lookup card. The judgement calls belong in your own `NOTES.md`.

## Parameter kinds

```python
def f(pos, /, normal, *args, kw_only, **kwargs):
```

| | means |
|---|---|
| before `/` | **positional-only** — cannot be passed by name |
| between | positional *or* keyword |
| `*args` | collects leftover positionals as a **tuple** |
| after `*args` or a bare `*` | **keyword-only** |
| `**kwargs` | collects leftover keywords as a **dict** |

```
f(1, 2, 3, x=4)   with def f(a, *args, **kwargs)   ->  1 (2, 3) {'x': 4}
```

### Collect in the signature, spread at the call

The same symbols do the mirror operation at the call site:

```python
f(*[1, 2, 3], **{"x": 4})      # identical to f(1, 2, 3, x=4)
```

Unpacking is textual substitution — **the list's length decides where arguments
land**. One item short and every parameter after it shifts, with no error.

### Wrappers: keep your own options keyword-only

```python
def retry(fn, *args, times=3, **kwargs):     # times AFTER *args
    return fn(*args, **kwargs)
```

```python
def retry_bad(fn, times=3, *args, **kwargs): # times BEFORE *args
retry_bad(work, 1, 2)     # times=1, args=(2,)  -> TypeError inside work()
```

The caller's first argument gets eaten by `times`, and the error surfaces in the
wrong function. Any wrapper that forwards arguments must keep its own options out
of the positional space.

---

## Defaults are evaluated ONCE, at definition time

```python
def add_item(item, basket=[]):
    basket.append(item)
    return basket
```

```
add_item('a') -> ['a']
add_item('b') -> ['a', 'b']          the SAME list every call
add_item.__defaults__ -> (['a', 'b', 'c'],)
```

The fix is to build it in the body, which runs per call:

```python
def add_item(item, basket=None):
    if basket is None:
        basket = []
```

**The rule is bigger than mutation.** Anything computed in a default is frozen at
import:

```python
def stamped(t=time.strftime("%H:%M:%S")):   # the clock is read at `def`
```
```
call 1: 23:26:15
call 2: 23:26:15      a second later
```

Timestamps, config reads, database handles, `datetime.now()` — all frozen.

**Anything in a default is built once at `def`; anything in the body is built per
call.** Third costume of the reference rule from Topic 1 (`[[0]*cols]*rows`,
`a[:]` being shallow).

---

## Scope — LEGB

Name resolution: **L**ocal → **E**nclosing → **G**lobal → **B**uiltin.

```python
total = 99
def f():
    print(total)     # line that never runs
    total = 5
```
```
UnboundLocalError: cannot access local variable 'total' where it is not
associated with a value
```

**Assignment anywhere in a function makes the name local for the whole function**,
including lines before the assignment. Python decides this when it *compiles* the
function:

```
f.__code__.co_varnames -> ('total',)
bytecode               -> LOAD_FAST      (local slot; never consults the global)
```

So the error points at a line that looks innocent and the cause is further down.

`global x` reaches module level; `nonlocal x` reaches the nearest enclosing
function. Both usually mean you should be returning a value instead.

---

## Closures

A nested function keeps access to the enclosing function's variables after that
function has returned.

```python
def multiplier(factor):
    def multiply(x):
        return x * factor
    return multiply

double = multiplier(2)
double(5)                            -> 10
double.__closure__[0].cell_contents  -> 2
```

### It captures the VARIABLE, not the value

```python
fs = [lambda: i for i in range(3)]
[f() for f in fs]  ->  [2, 2, 2]        not [0, 1, 2]
```

All three share one `i`, and the loop ended with `i == 2`.

**Freeze it with a default argument** (which binds at definition time — the thing
that makes mutable defaults a trap makes this the fix):

```python
fs = [lambda i=i: i for i in range(3)]   ->  [0, 1, 2]
```
`functools.partial(f, i)` does the same thing more explicitly.

### Following the variable is usually what you want

```python
def make_counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
    def read():
        return count      # must see the CURRENT count
    return increment, read
```

A snapshot would return `0` forever. Same for a callback reading a config that
changes at runtime. **Ask whether the closure should follow the variable or freeze
it** — following is the default; freezing takes deliberate action.

This is *not* the same fact as the mutable default. That one is "one object shared
across calls"; this is "one variable shared across closures".

---

## Functions are objects

```python
greet.__name__   -> 'greet'
greet.__doc__    -> 'Say hello.'
sorted(xs, key=len)          # passed as an argument
{"g": greet}["g"]("c")       # stored in a dict
```

`def` binds a function object to a name, like any other assignment. Every
decorator, every `key=`, every callback depends on this.

---

## Writing a good signature

```
Required, obvious, few                  -> positional
More than ~3 parameters                 -> make the rest keyword-only with `*`
A boolean flag                          -> keyword-only, always
Forwarding to another function          -> *args, **kwargs, own options after *args
Default is a list, dict, or set         -> use None and build it in the body
Default computes something              -> use None; compute in the body
```

`resize(img, 800, 600, True, False)` tells a reader nothing. A bare `*` before the
flags forces `resize(img, 800, 600, keep_ratio=True, upscale=False)`.
