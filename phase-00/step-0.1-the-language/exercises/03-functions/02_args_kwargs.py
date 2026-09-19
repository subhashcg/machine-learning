"""2. describe(*args, **kwargs)

Return a string like "2 positional (1, 2), 1 keyword {'x': 3}".

Then demonstrate the mirror operation: build a list and a dict, call describe by
unpacking them, and show the result matches passing the same values directly.

Finally show what happens when the unpacked list is one item short — same call
shape, different parameters filled.
"""


def describe(*args, **kwargs):
    """Describe the passed positional and keyword arguments
    """
    return f"{len(args)} positional {args}, {len(kwargs)} keyword {kwargs}"

def accept(param1, param2, param3="3rd Param"):
    return describe(param1, param2, param3)

if __name__ == "__main__":
    print(describe(1, 2, x=3))

    args = [1, 2]
    kwargs = {'x': 3}
    print(describe(*args, **kwargs))

    var_args = [1, 2, 3]
    print(accept(*var_args))
    var_args.pop()
    print(accept(*var_args))
    var_args.pop()
    try:
      print(accept(*var_args))
    except TypeError:
        print("Arg missing")

