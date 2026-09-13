"""6. make_grid(rows, cols)

Return a rows x cols grid of zeros where `grid[0][0] = 9` changes *only* that
cell.

`make_grid_broken` builds it the way that looks identical but shares one row.
The last line should prove the two differ.
"""


def make_grid(rows, cols):
    return [[0 for _ in range(cols)] for _ in range(rows)]

def make_grid_broken(rows, cols):
    return [[0] * cols] * rows

if __name__ == "__main__":
    good = make_grid(3, 2)
    bad = make_grid_broken(3, 2)

    good[0][0] = 9
    bad[0][0] = 9

    print("good  ", good)
    print("broken", bad)
    print("rows shared? good:", good[0] is good[1], " broken:", bad[0] is bad[1])
