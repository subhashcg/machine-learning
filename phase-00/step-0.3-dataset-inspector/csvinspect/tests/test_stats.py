"""The numerics behind D4: exact where it claims exact, bounded where it samples."""

import random
import statistics

import pytest

from csvinspect.stats import Reservoir, RunningStats, histogram, sparkline


def test_welford_matches_the_statistics_module():
    values = [random.Random(1).uniform(-1000, 1000) for _ in range(5_000)]
    stats = RunningStats()
    for value in values:
        stats.add(value)

    assert stats.n == len(values)
    assert stats.mean == pytest.approx(statistics.fmean(values))
    assert stats.stdev == pytest.approx(statistics.pstdev(values))
    assert stats.minimum == min(values) and stats.maximum == max(values)


def test_welford_survives_large_values_close_together():
    """The case the naive sum-of-squares formula gets wrong.

    Epoch timestamps are ~1.7e9 and differ by seconds; squaring them loses the
    variance in float noise. Welford does not, and this asserts it.
    """
    values = [1_700_000_000.0 + i for i in range(1_000)]
    stats = RunningStats()
    for value in values:
        stats.add(value)
    assert stats.stdev == pytest.approx(statistics.pstdev(values), rel=1e-9)


def test_variance_of_a_single_value_is_zero_not_an_error():
    stats = RunningStats()
    stats.add(42.0)
    assert stats.variance == 0.0 and stats.stdev == 0.0


def test_reservoir_holds_everything_when_it_fits():
    reservoir = Reservoir(size=100, seed=0)
    for i in range(100):
        reservoir.add(float(i))
    assert reservoir.is_complete is True
    assert sorted(reservoir.values) == [float(i) for i in range(100)]


def test_reservoir_is_bounded_and_knows_it_sampled():
    reservoir = Reservoir(size=100, seed=0)
    for i in range(10_000):
        reservoir.add(float(i))
    assert len(reservoir.values) == 100, "memory must not grow with the input"
    assert reservoir.seen == 10_000
    assert reservoir.is_complete is False, "a sampled histogram must say so"


def test_reservoir_is_reproducible_for_a_seed():
    def run(seed):
        reservoir = Reservoir(size=50, seed=seed)
        for i in range(5_000):
            reservoir.add(float(i))
        return reservoir.values

    assert run(0) == run(0), "two runs of the same report must agree"
    assert run(0) != run(1), "the seed should actually do something"


def test_reservoir_sample_is_roughly_uniform():
    """A biased sample would make every histogram lie; check the mean is close."""
    reservoir = Reservoir(size=2_000, seed=7)
    for i in range(100_000):
        reservoir.add(float(i))
    assert statistics.fmean(reservoir.values) == pytest.approx(49_999.5, rel=0.05)


def test_histogram_edges_come_from_the_exact_range():
    counts = histogram([0.0, 5.0, 10.0], low=0.0, high=10.0, bins=10)
    assert sum(counts) == 3
    assert counts[0] == 1, "the minimum lands in the first bin"
    assert counts[-1] == 1, "the maximum lands in the last bin, not off the end"


def test_histogram_of_a_constant_column():
    counts = histogram([5.0, 5.0, 5.0], low=5.0, high=5.0, bins=10)
    assert counts[0] == 3 and sum(counts) == 3


def test_histogram_with_a_sample_still_spans_the_whole_range():
    # Bars from a sample, edges from the exact min/max: the sample here misses
    # both extremes, and the axis is still right.
    counts = histogram([4.0, 5.0, 6.0], low=0.0, high=10.0, bins=10)
    assert sum(counts) == 3 and counts[0] == 0 and counts[-1] == 0


def test_sparkline_never_hides_a_non_empty_bin():
    line = sparkline([1000, 1, 0])
    assert line[0] == "█"
    assert line[1] != " ", "one value in a bin must still be visible"
    assert line[2] == " ", "an empty bin is empty"


def test_sparkline_of_nothing():
    assert sparkline([]) == ""
    assert sparkline([0, 0]) == "▁▁"
