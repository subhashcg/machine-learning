"""4. countdown(n)

A generator yielding n, n-1, ... 1.

Then demonstrate, with prints, that:
  - calling it runs none of the body
  - it resumes where it left off
  - it raises StopIteration when done

The demonstration is the exercise. Make the output prove each claim.
"""


def countdown(n):
    """Yields n, n-1...1 values"""
    print("Countdown starting...")
    for x in range(n):
        print(f"  loop: about to yield {n - x}")
        yield n - x
    print("Countdown finished")


if __name__ == "__main__":
    print("about to call countdown(3)")
    count = countdown(3)
    print("called it — nothing has run yet")

    for i in ("first", "second", "third"):
        print(f"asking for the {i} value")
        print(f"got {next(count)}")

    print("asking for a fourth")
    try:
        print(next(count))
    except StopIteration:
        print("Stopped")
