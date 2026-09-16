"""7. exhaustion_demo()

Show, with prints, the bug from the discussion: a generator summed twice gives
the right answer and then 0. Then show the same data as a list behaving
correctly.

Two lines of output and a comment saying why. This is the one you'll thank
yourself for when it happens in real code.
"""


def exhaustion_demo():
    """
    Demo for generator exhaustion
    sum of an exhausted generator returns 0 rather than raising, because the sum of nothing is zero by definition.
    Operations with an identity element fail silently; max has none, so it raises.
    """
    gen_x = (x for x in range(5))
    print("Summing generator first time: ", sum(gen_x))
    print("Summing generator second time", sum(gen_x))

    list_x = [x for x in range(5)]
    print("Summing list first time", sum(list_x))
    print("Summing list second time", sum(list_x))


if __name__ == "__main__":
    exhaustion_demo()
