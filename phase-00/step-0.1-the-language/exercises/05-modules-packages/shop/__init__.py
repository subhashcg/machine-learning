"""A tiny shop: a cart you can add to, and VAT pricing.

The public face is `add` and `total`; callers never need to know they live in
shop.cart.
"""

from .cart import add, total

VERSION = "1.0"

__all__ = ["add", "total", "VERSION"]
