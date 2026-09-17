"""2. describe(*args, **kwargs)

Return a string like "2 positional (1, 2), 1 keyword {'x': 3}".

Then demonstrate the mirror operation: build a list and a dict, call describe by
unpacking them, and show the result matches passing the same values directly.

Finally show what happens when the unpacked list is one item short — same call
shape, different parameters filled.
"""


def describe(*args, **kwargs):
    # TODO
    pass


if __name__ == "__main__":
    print(describe(1, 2, x=3))

    # TODO: build a list and a dict, call describe by unpacking them

    # TODO: show the one-item-short case
