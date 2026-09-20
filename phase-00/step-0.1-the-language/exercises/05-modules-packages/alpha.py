"""Half of a deliberate import cycle with beta. Import this one first."""

import beta

A_VALUE = "a"


def describe():
    return f"alpha sees {beta.B_VALUE}"
