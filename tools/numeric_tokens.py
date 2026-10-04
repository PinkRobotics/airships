"""Numeric boundaries shared by prose gates; punctuation alone may end a token."""
import re

LEFT = r"(?<![\d.,])"
RIGHT = r"(?!\d|[.,]\d)"


def numeric_pattern(number):
    return LEFT + re.escape(number) + RIGHT
