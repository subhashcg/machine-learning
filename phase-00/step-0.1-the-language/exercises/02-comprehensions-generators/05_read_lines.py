"""5. read_lines(path) and count_matching(path, word)

read_lines  — a generator yielding each stripped line of a file.
count_matching — uses it to count lines containing `word`, without ever
                 holding the file in memory.

Write a small file in the __main__ block to test against. Use `with`.
"""

import tempfile
import pathlib

def read_lines(path):
    """Path needs to be something acceptable by open.
    Returns a generator which yields each line stripped of leading and trailing whitespaces
    """
    with open(path) as f:
        for line in f:
            yield line.strip()


def count_matching(path, word):
    """
    Iterate over line and adds lines which contains word
    """
    return sum(1 for line in read_lines(path) if word in line)


if __name__ == "__main__":
  with tempfile.TemporaryDirectory() as d:
    path = pathlib.Path(d) / "test.txt"
    path.write_text("one word\nword is 2\nno w 0rd at all\n")
    print(count_matching(path, "word"))
