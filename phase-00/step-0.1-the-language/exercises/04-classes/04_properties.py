"""4. Temperature — properties

Stores celsius. Give it:
  - a validating setter — below absolute zero (-273.15) raises ValueError
  - a read-only `fahrenheit` property, computed
  - a `kelvin` property with both getter and setter, where setting kelvin
    updates celsius

Show that setting kelvin changes celsius and fahrenheit consistently, and that
an invalid temperature is refused from either direction.

Then, to see why computing beats storing: write TempStored, which computes
self.fahrenheit once in __init__. Change its celsius and print both values.
One of them will be lying.

Finish with a comment: for each of celsius, fahrenheit and kelvin, say whether
it should be a plain attribute, a property, or a method — and why.
"""

ABSOLUTE_ZERO_C = -273.15


class Temperature:
    # TODO
    pass


class TempStored:
    # TODO — fahrenheit computed once in __init__, then left to rot
    pass


if __name__ == "__main__":
    # TODO: build one, print all three scales

    # TODO: set kelvin, show celsius and fahrenheit followed

    # TODO: refuse an invalid celsius, and an invalid kelvin

    # TODO: TempStored — change celsius, show the stale fahrenheit

    # TODO: comment — attribute / property / method for each, and why
    pass
