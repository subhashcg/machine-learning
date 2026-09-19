# Step 0.1 — notes

What surprised me, what I got wrong first, what I want to remember.
One section per topic. Keep it honest — the value is in recording the
things that *didn't* go smoothly.

## 1. Data structures
- list is ordered items. Scanning is slow but access is fast using index.
- Dict is ordered key, value pairs and accessible using key. Access is fast using keys
- Set is unordered keys as items. Access is fast, as is inclusion check. Deduplication is the side effect
- Tuple is fixed size list and immutable which allows these to be used as keys. Access is fast using index and acts same as list.
- Slicing list creates a shallow copy and items are still same references.
- inclusion test in list and tuple is O(n) while others is O(1)

## 2. Comprehensions and generators
- Nested comprehension reads left to right as outer to inner and runs like that.
- Comprehensions can have filter as if conditions at the end or have if else as transformer at start
- Generators can be iterated once only. Once exhausted they can't be iterated.
- Generators are lazy evaluated and one at a time which makes them highly useful for streaming and handling large amount of data
- readlines reads the while file and beats the efficiency gain by file handle itself being an iterator
- A for loop on generator takes an item from generator and then decides

## 3. Functions
- Default values in functions are created once when def statements runs. If it a object then same reference will be used for every invovaction.
- Unpacking a list as function arguments with default args can lead to unintended consequences if the size is not same as number of args expected.
- Using keyword arguments gives the flexibility to change signature without impacting all consumers
- Closuer captures the variable, not the value
- A default argument (`lambda i=i:`) captures the *value* instead, because defaults bind at definition time. Same mechanism as the mutable-default trap, working in the opposite direction.
- Use `is None`, never `== None`. `==` calls `__eq__`, which anything can override — `numpy_array == None` returns an array, and `if` on it raises ValueError. Identity can't be overridden.
- Assignment anywhere in a function makes the name local for the *whole* function, decided when Python compiles it. That's why UnboundLocalError can fire on a line *above* the assignment.
- `nonlocal` is only needed to assign to an enclosing variable. Reading needs nothing: lookup walks the LEGB chain automatically, and only binding forces the local-or-not decision.
- A wrapper's own options must sit after `*args`, so they're keyword-only. `times` before `*args` eats the caller's first argument — and the error surfaces inside the wrapped function, not the wrapper, which is what makes it hard to find.
- When you turn a value into a parameter, *every* use of it has to move. A hardcoded constant next to a parameter of the same value is invisible until someone changes the parameter, which they will, because it's a parameter.
- `Exception` is not the top of the tree; `BaseException` is. `KeyboardInterrupt`, `SystemExit` and `GeneratorExit` sit outside `Exception` on purpose, so `except Exception` doesn't swallow Ctrl+C. Never write a bare `except:`.

## 4. Classes

## 5. Modules and packages

## 6. Exceptions

## 7. Files and formats

## 8. Type hints
