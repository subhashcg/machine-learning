"""4. Temperature — properties

Temperature stores celsius. Give it:

    celsius      a property with a validating setter; below ABSOLUTE_ZERO_C
                 raises ValueError
    fahrenheit   read-only property, computed:  c * 9/5 + 32
    kelvin       property with getter AND setter; setting it updates celsius

TempStored is the cautionary version: it computes self.fahrenheit once in
__init__ and stores it. Give it a plain `celsius` attribute and nothing else.

Then a comment: for each of celsius, fahrenheit and kelvin, say whether it
should be a plain attribute, a property, or a method — and why.
"""

ABSOLUTE_ZERO_C = -273.15


class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius          # goes through the setter, so it's validated

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < ABSOLUTE_ZERO_C:
            raise ValueError(f"{value}C is below absolute zero ({ABSOLUTE_ZERO_C}C)")
        self._celsius = value

    @property
    def fahrenheit(self):
        return self.celsius * 9 / 5 + 32

    @property
    def kelvin(self):
        return self.celsius - ABSOLUTE_ZERO_C

    @kelvin.setter
    def kelvin(self, value):
        self.celsius = value + ABSOLUTE_ZERO_C   # reuse celsius's validation


class TempStored:
    def __init__(self, celsius):
        self.celsius = celsius
        self.fahrenheit = celsius * 9 / 5 + 32   # snapshot; never updated again


# celsius     property. It's the one piece of stored state, so it would be a
#             plain attribute — except it has an invariant (>= absolute zero).
#             A property keeps the `t.celsius = x` syntax and adds the check.
#             With no invariant, a plain attribute would be right.
# fahrenheit  read-only property. It's derived from celsius, cheap, and has no
#             arguments, so it reads like data. Storing it (TempStored) lets it
#             drift out of sync; computing it on access can't.
# kelvin      property with a setter. Also derived, but it's a natural thing to
#             assign to, and the setter just translates to celsius (so the
#             validation lives in one place). None of these should be methods:
#             a method suits work that's expensive, takes arguments, or has
#             side effects — `t.to_unit("F")` would be one; these aren't.


# ---------------------------------------------------------------- checks
# Written for you. Implement above; run the file to see where you stand.

def _run(checks):
    ok = 0
    for label, fn in checks:
        try:
            fn()
        except NotImplementedError:
            print(f"  ·     {label}"); continue
        except AssertionError as e:
            print(f"  FAIL  {label}" + (f"  — {e}" if str(e) else "")); continue
        except Exception as e:
            print(f"  ERR   {label}  — {type(e).__name__}: {e}"); continue
        print(f"  ok    {label}"); ok += 1
    print(f"{ok}/{len(checks)} passing")



def _conversions():
    t = Temperature(100)
    assert t.celsius == 100
    assert t.fahrenheit == 212, f"100C should be 212F, got {t.fahrenheit}"
    assert round(t.kelvin, 2) == 373.15, f"100C should be 373.15K, got {t.kelvin}"


def _celsius_setter_validates():
    t = Temperature(0)
    t.celsius = -100
    assert t.celsius == -100
    try:
        t.celsius = -300
    except ValueError:
        assert t.celsius == -100, "a rejected assignment must not change the value"
        return
    raise AssertionError("below absolute zero should raise ValueError")


def _kelvin_setter_updates_celsius():
    t = Temperature(0)
    t.kelvin = 373.15
    assert round(t.celsius, 2) == 100, f"celsius should have followed, got {t.celsius}"
    assert round(t.fahrenheit, 2) == 212, f"fahrenheit too, got {t.fahrenheit}"


def _kelvin_setter_validates():
    t = Temperature(0)
    try:
        t.kelvin = -1
    except ValueError:
        return
    raise AssertionError("negative kelvin is below absolute zero; should raise")


def _fahrenheit_is_read_only():
    t = Temperature(0)
    try:
        t.fahrenheit = 100
    except AttributeError:
        return
    raise AssertionError("fahrenheit is derived; assigning to it should fail")


def _stored_goes_stale():
    s = TempStored(0)
    assert s.fahrenheit == 32
    s.celsius = 100
    assert s.fahrenheit == 32, "TempStored should still be showing the OLD value"
    live = Temperature(100)
    assert live.fahrenheit == 212 != s.fahrenheit, "the computed one keeps up"


if __name__ == "__main__":
    _run([
        ("celsius / fahrenheit / kelvin agree",  _conversions),
        ("celsius setter rejects below abs zero", _celsius_setter_validates),
        ("setting kelvin updates celsius",        _kelvin_setter_updates_celsius),
        ("kelvin setter validates too",           _kelvin_setter_validates),
        ("fahrenheit is read-only",               _fahrenheit_is_read_only),
        ("TempStored goes stale, Temperature does not", _stored_goes_stale),
    ])
