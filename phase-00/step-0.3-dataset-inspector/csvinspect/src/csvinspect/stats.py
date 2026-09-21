"""The numerics: what can be exact in one pass, and what has to be sampled.

D4 split the problem in two. Count, min, max, mean and standard deviation are
computed exactly in constant memory. The histogram cannot be — binning needs the
range, and the range is not known until the last row — so its bar heights come
from a bounded reservoir sample while its bin edges come from the exact min and
max. The axis is therefore always right; only the heights are estimated, and
only when there were more values than the reservoir could hold.
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field

BLOCKS = "▁▂▃▄▅▆▇█"


@dataclass
class RunningStats:
    """Welford's online algorithm: mean and variance without keeping the values.

    The naive alternative — accumulating sum and sum-of-squares — loses most of
    its significant digits when the values are large and close together, which is
    exactly what a column of epoch timestamps or prices looks like. Welford costs
    one extra multiply per value and does not.
    """

    n: int = 0
    mean: float = 0.0
    m2: float = 0.0
    minimum: float | None = None
    maximum: float | None = None

    def add(self, value: float) -> None:
        self.n += 1
        delta = value - self.mean
        self.mean += delta / self.n
        self.m2 += delta * (value - self.mean)
        if self.minimum is None or value < self.minimum:
            self.minimum = value
        if self.maximum is None or value > self.maximum:
            self.maximum = value

    @property
    def variance(self) -> float:
        """Population variance. Zero for fewer than two values."""
        return self.m2 / self.n if self.n > 1 else 0.0

    @property
    def stdev(self) -> float:
        return self.variance ** 0.5


@dataclass
class Reservoir:
    """Algorithm R: a uniform sample of unknown-length input, in fixed memory.

    Seeded from the options so two runs over the same file produce the same
    histogram — an unreproducible report is not much of a report.
    """

    size: int = 20_000
    seed: int = 0
    seen: int = 0
    values: list[float] = field(default_factory=list)
    _rng: random.Random = field(init=False, repr=False)

    def __post_init__(self) -> None:
        self._rng = random.Random(self.seed)

    def add(self, value: float) -> None:
        self.seen += 1
        if len(self.values) < self.size:
            self.values.append(value)
            return
        # Each later value replaces a random slot with probability size/seen,
        # which keeps every value seen so far equally likely to be held.
        j = self._rng.randrange(self.seen)
        if j < self.size:
            self.values[j] = value

    @property
    def is_complete(self) -> bool:
        """True when nothing was discarded, so the histogram below is exact."""
        return self.seen <= self.size


def histogram(values: list[float], low: float, high: float, bins: int = 10) -> list[int]:
    """Bin `values` into `bins` equal-width buckets spanning [low, high].

    The edges come from the exact range rather than from the sample, so the
    first and last bar always sit on the real extremes even when the sample
    missed them.
    """
    if bins < 1 or not values:
        return [0] * max(bins, 0)
    counts = [0] * bins
    if high <= low:                       # a constant column: one full bar
        counts[0] = len(values)
        return counts
    width = (high - low) / bins
    for value in values:
        index = int((value - low) / width)
        if index >= bins:                 # the maximum itself, and float slop
            index = bins - 1
        elif index < 0:
            index = 0
        counts[index] += 1
    return counts


def sparkline(counts: list[int]) -> str:
    """Render bin counts as one line of block characters.

    Heights are scaled to the tallest bar, so the shape is comparable within a
    column and meaningless between columns. Any non-empty bin gets at least the
    shortest block, so a rare-but-present bucket never renders as a gap.
    """
    if not counts:
        return ""
    peak = max(counts)
    if peak == 0:
        return BLOCKS[0] * len(counts)
    out = []
    for count in counts:
        if count == 0:
            out.append(" ")
            continue
        level = round((count / peak) * (len(BLOCKS) - 1))
        out.append(BLOCKS[max(level, 1)])
    return "".join(out)
