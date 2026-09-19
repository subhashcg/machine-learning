"""1. append_to(item, target=None)

Append `item` to `target` and return it. A call with no `target` must start from
a fresh empty list every time.

Then write append_to_broken with target=[] and show, with output, that repeated
calls accumulate. Print append_to_broken.__defaults__ after three calls —
watching the function's own metadata grow is the part that sticks.
"""


def append_to(item, target=None):
    """Appends item to the target list which is optional"""
    if target is None:
        target = []
    target.append(item)
    return target

def append_to_broken(item, target=[]):
    """Appends item to the target list which is optional"""
    target.append(item)
    return target

if __name__ == "__main__":
    print("append_to: 1 ->", append_to(1))
    print("append_to: 2 ->", append_to(2))
    print("append_to: 3 ->", append_to(3))

    print("append_to_broken: 1 ->", append_to_broken(1))
    print("append_to_broken: 2 ->", append_to_broken(2))
    print("append_to_broken: 3 ->", append_to_broken(3))

    print(append_to_broken.__defaults__)
