"""A tiny command-line tool: importable, and runnable as a script."""


def greet(name):
    return f"hello {name}"


def main():
    print(greet("world"))


if __name__ == "__main__":
    main()
