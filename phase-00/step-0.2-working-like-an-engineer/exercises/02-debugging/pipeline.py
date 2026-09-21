"""A small data pipeline with four bugs. Do not rewrite it — diagnose it.

Each bug is realistic: none is a typo, all four produce plausible-looking
behaviour until you look closely. The tests in test_pipeline.py describe what
these functions are SUPPOSED to do.
"""


def parse_row(line):
    """Parse 'name,qty,price' into a dict with typed values."""
    name, qty, price = (part.strip() for part in line.split(","))
    return {"name": name, "qty": int(qty), "price": float(price)}


def load_rows(text):
    """Parse every non-empty line. Skips the header if present."""
    rows = []
    for line in text.splitlines():
        if not line.strip():
            continue
        if line.startswith("name,"):
            continue
        rows.append(parse_row(line))
    return rows


def total_value(rows):
    """Sum qty * price across all rows, rounded to 2dp."""
    total = 0
    for row in rows:
        total += row["qty"] * row["price"]
    return round(total, 2)


def apply_discount(rows, percent, minimum_qty=10):
    """Return rows with `price` reduced by `percent` where qty >= minimum_qty.

    Must not modify the rows it was given.
    """
    out = []
    for row in rows:
        row = dict(row)
        if row["qty"] >= minimum_qty:
            row["price"] = row["price"] * (1 - percent / 100)
        out.append(row)
    return out


def summarise(rows, top=3):
    """The `top` rows by total value (qty * price), highest first."""
    ranked = sorted(rows, key=lambda r: r["qty"] * r["price"], reverse=True)
    return ranked[:top]


def running_totals(rows, totals=None):
    """A running cumulative total of qty * price, one entry per row."""
    if totals is None:
        totals = []
    running = 0
    for row in rows:
        running += row["qty"] * row["price"]
        totals.append(round(running, 2))
    return totals
