"""Depends only on shared — no cycle."""

import shared


def describe():
    return f"delta sees {shared.VALUE}"
