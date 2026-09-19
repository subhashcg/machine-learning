"""Depends only on shared — no cycle."""

import shared


def describe():
    return f"gamma sees {shared.VALUE}"
