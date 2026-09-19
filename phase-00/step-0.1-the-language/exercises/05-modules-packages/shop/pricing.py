"""Prices with VAT."""

VAT = 0.2


def with_vat(amount):
    return amount * (1 + VAT)
