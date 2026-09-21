"""The constraint that shapes the whole design: memory must not track row count.

This is the test that fails if someone "simplifies" the reader into
`rows = list(reader)`. It measures allocation rather than trusting the comment
at the top of reader.py.
"""

import tracemalloc

import pytest

from csvinspect import Options, inspect_file

HEADER = "id,region,amount,ordered_at,flag,note\n"
REGIONS = ("EMEA", "APAC", "AMER", "LATAM")


def write_rows(path, n_rows):
    """A file with a bit of everything: ints, floats, dates, categories, text."""
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(HEADER)
        for i in range(1, n_rows + 1):
            f.write(
                f"{i},{REGIONS[i % 4]},{(i % 9871) / 7:.2f},"
                f"2024-{(i % 12) + 1:02d}-{(i % 28) + 1:02d},"
                f"{'true' if i % 3 else 'false'},note-{i}\n"
            )
    return path


def peak_bytes(path, **options):
    tracemalloc.start()
    try:
        report = inspect_file(path, Options(**options))
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    return report, peak


def test_memory_does_not_grow_with_rows(tmp_path):
    small, _ = peak_bytes(write_rows(tmp_path / "small.csv", 20_000))
    large_report, large_peak = peak_bytes(write_rows(tmp_path / "large.csv", 200_000))
    small_report, small_peak = small, _

    assert large_report.n_rows == 200_000
    # Ten times the rows. Anything close to ten times the memory means the file
    # is being accumulated somewhere.
    assert large_peak < small_peak * 2, (
        f"peak went from {small_peak:,} to {large_peak:,} bytes for 10x the rows"
    )


def test_peak_memory_has_a_ceiling(tmp_path):
    report, peak = peak_bytes(write_rows(tmp_path / "big.csv", 200_000))
    assert report.n_rows == 200_000
    # Six columns: one reservoir (20k floats), one distinct map (1k keys), a few
    # counters. A generous ceiling that a `list(reader)` would blow through by
    # two orders of magnitude.
    assert peak < 16 * 1024 * 1024, f"peak was {peak / 1e6:.1f} MB"


def test_bounded_even_when_every_value_is_unique(tmp_path):
    """The worst case for D15: a high-cardinality text column."""
    path = tmp_path / "unique.csv"
    with open(path, "w", encoding="utf-8") as f:
        f.write("token\n")
        for i in range(200_000):
            f.write(f"{i:08x}-{i * 7919:012d}\n")

    report, peak = peak_bytes(path)
    column = report.columns[0]
    assert column.distinct_capped is True, "it must stop tracking, not stop working"
    assert peak < 8 * 1024 * 1024, f"peak was {peak / 1e6:.1f} MB"


def test_the_numbers_are_still_exact_after_sampling(tmp_path):
    """Sampling the histogram must not sample the statistics (D4)."""
    path = tmp_path / "nums.csv"
    with open(path, "w", encoding="utf-8") as f:
        f.write("n\n")
        for i in range(1, 100_001):
            f.write(f"{i}\n")

    report = inspect_file(path, Options(reservoir_size=1_000))
    column = report.columns[0]
    assert column.low == 1 and column.high == 100_000, "the range is exact"
    assert column.mean == pytest.approx(50_000.5), "the mean is exact"
    assert column.bins_exact is False, "the histogram is not, and says so"
    assert any("sample" in note for note in column.notes)
