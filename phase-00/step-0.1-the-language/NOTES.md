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

## 4. Classes

## 5. Modules and packages

## 6. Exceptions

## 7. Files and formats

## 8. Type hints
