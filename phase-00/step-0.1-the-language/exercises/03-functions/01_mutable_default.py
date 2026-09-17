"""1. append_to(item, target=None)

Append `item` to `target` and return it. A call with no `target` must start from
a fresh empty list every time.

Then write append_to_broken with target=[] and show, with output, that repeated
calls accumulate. Print append_to_broken.__defaults__ after three calls —
watching the function's own metadata grow is the part that sticks.
"""


def append_to(item, target=None):
    # TODO
    pass


def append_to_broken(item, target=[]):
    # TODO — the version that shares one list across calls
    pass


if __name__ == "__main__":
    # TODO: three calls to each, labelled, so the difference is obvious

    # TODO: print append_to_broken.__defaults__
    pass
