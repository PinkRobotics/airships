"""Compare generated data without treating floating-point round-off as drift.

Numbers agree when abs(a-b) <= max(1e-9 * max(abs(a), abs(b)), 1e-12).
Signed zeros agree. Keys, strings, booleans, nulls, lengths and value types
are exact. Non-finite numbers are invalid, even when both inputs contain them.
"""
import json
import math
import re


def numeric_equal(a, b, *, tolerance=0):
    """Use the larger of an existing absolute tolerance and the data rule."""
    if type(a) not in (int, float) or type(b) not in (int, float):
        return False
    return (math.isfinite(a) and math.isfinite(b)
            and abs(a - b) <= max(tolerance, 1e-9 * max(abs(a), abs(b)), 1e-12))


def first_difference(a, b, path='$'):
    """Return the first differing path and both values, or None. Keys sort first."""
    if type(a) is not type(b):
        return f'{path}: {a!r} != {b!r} (value types differ)'
    if isinstance(a, dict):
        for key in sorted(a.keys() | b.keys()):
            child = f'{path}[{key!r}]'
            if key not in a:
                return f'{child}: <missing> != {b[key]!r}'
            if key not in b:
                return f'{child}: {a[key]!r} != <missing>'
            difference = first_difference(a[key], b[key], child)
            if difference:
                return difference
    elif isinstance(a, list):
        if len(a) != len(b):
            return f'{path}.length: {len(a)!r} != {len(b)!r}'
        for i, (left, right) in enumerate(zip(a, b)):
            difference = first_difference(left, right, f'{path}[{i}]')
            if difference:
                return difference
    elif type(a) in (int, float):
        if not numeric_equal(a, b):
            return f'{path}: {a!r} != {b!r}'
    elif a != b:
        return f'{path}: {a!r} != {b!r}'
    return None


def parse_json(text):
    """Refuse duplicate keys and non-JSON numeric constants."""
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise ValueError(f'duplicate key {key!r}')
            result[key] = value
        return result

    def invalid(value):
        raise ValueError(f'invalid JSON number {value}')

    return json.loads(text, object_pairs_hook=pairs, parse_constant=invalid)


def parse_skin_literal(text):
    """Read the single generated JSON literal; never execute JavaScript."""
    match = re.fullmatch(r'\s*/\*.*?\*/\s*export const SKIN = (.*);\s*', text, re.S)
    if not match:
        raise ValueError('expected one generated SKIN literal')
    data = parse_json(match[1])
    if not isinstance(data, dict):
        raise ValueError('SKIN literal must be an object')
    return data
