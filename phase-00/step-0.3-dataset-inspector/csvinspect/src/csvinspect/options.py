"""Every knob in one place, with the defaults the design argued for.

Held as a frozen dataclass so that a run is reproducible from its options alone,
and so no module can quietly change a setting mid-pass.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from csvinspect.values import DEFAULT_NA_VALUES


@dataclass(frozen=True)
class Options:
    # input handling
    encoding: str = "utf-8-sig"          # D8: strips a BOM, otherwise plain utf-8
    delimiter: str | None = None         # None: sniff it (D7)
    has_header: bool = True              # D6
    limit: int | None = None             # D5: read everything unless asked not to
    strict_rows: bool = False            # D10: ragged rows are reported, not fatal

    # what counts as a value
    na_values: frozenset[str] = DEFAULT_NA_VALUES          # D1
    thousands: str | None = None                           # D14: opt-in only
    tolerance: float = 0.0                                 # D2: strict by default

    # bounded memory (D4, D15)
    reservoir_size: int = 20_000
    max_distinct: int = 1_000
    seed: int = 0

    # presentation
    bins: int = 10
    top_values: int = 5
    color: bool = False
