"""3. Money

Fields `amount` and `currency` (default "GBP"). Implement:

    __repr__   something you could paste back in: Money(10, 'GBP')
    __str__    for humans: 10.00 GBP
    __eq__     equal amount AND currency
    __hash__   consistent with __eq__
    __lt__     by amount
    __add__    same currency only; raise ValueError otherwise

BadMoney has __eq__ but no __hash__ — leave it that way, the checks rely on it.
"""


class Money:
    # TODO
    pass


class BadMoney:
    def __init__(self, amount):
        self.amount = amount

    def __eq__(self, other):
        return self.amount == other.amount


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



def _repr_and_str():
    m = Money(10)
    assert repr(m) == "Money(10, 'GBP')", f"repr was {repr(m)!r}"
    assert str(m) == "10.00 GBP", f"str was {str(m)!r}"


def _equality():
    assert Money(10) == Money(10), "equal amounts and currencies should be =="
    assert Money(10) != Money(10, "USD"), "currency must matter"
    assert Money(10) is not Money(10), "== is not identity"


def _hashing():
    assert hash(Money(10)) == hash(Money(10)), "equal objects must hash the same"
    assert len({Money(10), Money(10)}) == 1, "a set should collapse them"
    assert {Money(10): "ten"}[Money(10)] == "ten", "an equal key must find the value"


def _ordering():
    got = sorted([Money(10), Money(2.5), Money(7)])
    assert [m.amount for m in got] == [2.5, 7, 10], f"sorted gave {got}"


def _addition():
    assert (Money(10) + Money(2.5)).amount == 12.5
    try:
        Money(10) + Money(5, "USD")
    except ValueError:
        return
    raise AssertionError("adding different currencies should raise ValueError")


def _bad_money_unhashable():
    try:
        {BadMoney(1)}
    except TypeError:
        return
    raise AssertionError("BadMoney defines __eq__ so it should be unhashable")


if __name__ == "__main__":
    _run([
        ("__repr__ and __str__",                _repr_and_str),
        ("__eq__ compares value, not identity", _equality),
        ("__hash__ agrees with __eq__",         _hashing),
        ("__lt__ makes sorted() work",          _ordering),
        ("__add__, and refusing mixed currency", _addition),
        ("BadMoney is unhashable",              _bad_money_unhashable),
    ])
