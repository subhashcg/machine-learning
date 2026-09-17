"""7. counter_demo()

Reproduce UnboundLocalError deliberately, catch it, and print the message.

Then show three working versions of the same intent: one using `global`, one
using `nonlocal`, and one that just takes a parameter and returns a value.

In a comment, say which you would ship and why.
"""

total = 0


def broken(n):
    total = total + n
    return total


def with_global(n):
    global total
    total = total + n
    return total


def with_nonlocal(n):
    total = 0
    def add():
        nonlocal total
        total = total + n
        return total
    return add

def pure(total, n):
    total = total + n
    return total


if __name__ == "__main__":
    try:
        broken(1)
    except UnboundLocalError as e:
        print(f"broken(1): {e}")

    # One call makes all three look equally fine. Three calls show the difference.
    print("\nwith_global(2), three times:")
    for _ in range(3):
        print("   ->", with_global(2))
    print(f"   module `total` is now {total} — the function changed the world around it")

    print("\nwith_nonlocal(2)(), three times:")
    for _ in range(3):
        print("   ->", with_nonlocal(2)())
    print("   always 2 — a new closure each call, so its state is never reused")
    add = with_nonlocal(2)
    print("   reusing ONE closure:", [add() for _ in range(3)], "— state exists, but contained")

    print("\npure(2, 5), three times:")
    for _ in range(3):
        print("   ->", pure(2, 5))
    print("   same input, same output, in any order, whatever ran before")

    # I would ship `pure`, to avoid hidden side effects. Concretely that buys:
    #   testable          — no setup, no teardown, no reset between tests
    #   order-independent — calling it never changes what the next call does
    #   concurrency-safe  — no shared mutable state to race on
    #   readable          — the signature names everything it touches
    # `nonlocal` is the honest middle ground when state must persist across calls
    # and should stay encapsulated (a counter, a cache). `global` almost never is.
