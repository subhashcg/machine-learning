"""6. Point and Config

Point(x, y) as a @dataclass. Show the generated __repr__ and __eq__.

Config with a list, a dict and a non-empty list default — all three via
field(default_factory=...). Prove two instances don't share.

Then, inside a try, define a dataclass with `tags: list = []` and print the
error. In a comment, say what test the dataclass is actually applying.
"""

from dataclasses import dataclass, field


# TODO: Point


# TODO: Config


if __name__ == "__main__":
    # TODO: repr and eq for free

    # TODO: two Configs, prove no sharing

    # TODO: try/except around a dataclass with a mutable default

    # TODO: comment — what test is it applying?
    pass
