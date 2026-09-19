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
    # TODO
    pass


class TempStored:
    # TODO — fahrenheit computed once in __init__, then left to rot
    pass


# TODO: comment — attribute / property / method for each, and why


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
