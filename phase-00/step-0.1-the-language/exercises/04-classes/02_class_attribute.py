"""2. Basket and BasketOk

Basket puts `items = []` at class level. BasketOk builds it in __init__.
Both need an `add(self, x)` that appends to self.items.

In a comment, explain why self.items.append(x) reaches the class attribute while
self.items = [x] would not.
"""


class Basket:
    items = []

    def add(self, item):
        self.items.append(item)

class BasketOk:

    items = []

    def __init__(self):
        self.items = []

    def add(self, item):
        self.items.append(item)


# TODO: comment — read falls through to the class, write lands on the instance


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


def _shared():
    x, y = Basket(), Basket()
    x.add("apple"); y.add("pear")
    assert x.items == ["apple", "pear"], f"expected both items, got {x.items}"
    assert x.items is y.items, "the two baskets should be sharing ONE list"
    assert "items" not in x.__dict__, "no instance attribute should have been created"


def _not_shared():
    p, q = BasketOk(), BasketOk()
    p.add("apple"); q.add("pear")
    assert p.items == ["apple"] and q.items == ["pear"], f"{p.items} / {q.items}"
    assert p.items is not q.items, "each basket should have its own list"
    assert "items" in p.__dict__, "items should be an instance attribute"


def _rebind_makes_instance_attr():
    before = list(Basket.items)          # the class list is shared across checks too
    x = Basket()
    x.items = ["own"]
    assert "items" in x.__dict__, "assignment should create an instance attribute"
    assert x.items == ["own"], f"the instance should hold its own list, got {x.items}"
    assert Basket.items == before, f"the class list should be untouched, got {Basket.items}"


if __name__ == "__main__":
    _run([
        ("Basket shares one list across instances", _shared),
        ("BasketOk gives each instance its own",    _not_shared),
        ("assignment creates an instance attribute", _rebind_makes_instance_attr),
    ])
