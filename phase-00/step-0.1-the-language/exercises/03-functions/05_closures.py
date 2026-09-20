"""5. make_counter()

Return two functions, `increment` and `read`, sharing one count. `read` must see
the current value, not a snapshot.

Then make two independent counters and show their counts don't interfere.
Print increment.__closure__[0].cell_contents to see the captured cell.
"""


def make_counter():
    count = 0

    def increment():
        nonlocal count
        count += 1

    def read():
        return count

    return (increment, read)

if __name__ == "__main__":
    inc, read = make_counter()

    print(f"Counter value: {read()}")
    inc()
    print(f"Counter value: {read()}")

    inc_2, read_2 = make_counter()

    print(f"Second Counter value: {read_2()}")
    inc_2()
    inc_2()
    print(f"Second Counter value: {read_2()}")

    print(f"Cell Content {inc_2.__closure__[0].cell_contents}")