"""6. make_multipliers(n)

Return a list of n functions where function i multiplies its argument by i.

Write the broken version first (a plain comprehension over range(n)), show it
returns the wrong answers, then fix it. Keep both, with a comment naming what
the closure captured.
"""


def make_multipliers_broken(n):
    return [lambda x: x * i for i in range(n) ]

def make_multipliers(n):
    return [lambda x, i=i: x * i for i in range(n) ]


if __name__ == "__main__":
    # Closure captures the variable instead of value so all functions in broken version had the final version of i
    broken = make_multipliers_broken(3)
    argument = 2
    for index, fn in enumerate(broken):
        print(f"Broken function {index} with argument {argument}: {fn(argument)}")

    correct = make_multipliers(3)
    for index, fn in enumerate(correct):
        print(f"Correct function {index} with argument {argument}: {fn(argument)}")