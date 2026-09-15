"""3. invert(mapping)

Swap keys and values. Assume values are unique and hashable.

    {"a": 1, "b": 2}  ->  {1: "a", 2: "b"}
"""
def invert(mapping):
    """Return a new dict with keys and values swapped.
    
    Values must be unique and hashable. Duplicate values collapse silently with last one winning.
    Unhashable valyes result in typeerror
    """
    inverted = {}
    for key, val in mapping.items():
        inverted[val] = key
    return inverted

if __name__ == "__main__":
    print(invert({"a": 1, "b": 2}))