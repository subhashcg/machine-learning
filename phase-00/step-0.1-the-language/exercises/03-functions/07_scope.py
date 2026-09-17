"""7. counter_demo()

Reproduce UnboundLocalError deliberately, catch it, and print the message.

Then show three working versions of the same intent: one using `global`, one
using `nonlocal`, and one that just takes a parameter and returns a value.

In a comment, say which you would ship and why.
"""

total = 0


def broken(n):
    # TODO — read `total` and assign to it, so Python makes it local
    pass


def with_global(n):
    # TODO
    pass


def with_nonlocal(n):
    # TODO — an inner function that mutates an enclosing variable
    pass


def pure(total, n):
    # TODO — no outer state at all
    pass


if __name__ == "__main__":
    # TODO: call broken(), catch UnboundLocalError, print it

    # TODO: show the three working versions

    # TODO: comment — which would you ship, and why
    pass
