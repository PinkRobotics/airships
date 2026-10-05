"""Boundary and negative controls for the generated-data comparison."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from data_compare import first_difference, numeric_equal, parse_json, parse_skin_literal


class DataComparison(unittest.TestCase):
    def test_relative_absolute_and_signed_zero(self):
        for a, b in ((1.0, 1.0 + 5e-10), (0.0, 1e-12), (0.0, -0.0)):
            self.assertIsNone(first_difference(a, b))
        for a, b in ((1.0, 1.0 + 2e-9), (0.0, 1.01e-12), (1.0, 1.0 + 1e-6)):
            self.assertIsNotNone(first_difference(a, b))
        self.assertTrue(numeric_equal(1.0, 1.01, tolerance=0.02))
        self.assertFalse(numeric_equal(1.0, 1.03, tolerance=0.02))

    def test_exact_structure_types_and_first_path(self):
        for a, b in ((1, 1.0), (True, 1), (None, False), ('a', 'b'),
                     ([], [0]), ({'a': 1}, {'b': 1})):
            self.assertIsNotNone(first_difference(a, b))
        self.assertEqual(first_difference({'z': 0, 'a': [1.0]}, {'a': [2.0], 'z': 1}),
                         "$['a'][0]: 1.0 != 2.0")
        self.assertIsNone(first_difference({'a': False, 'b': None}, {'b': None, 'a': False}))

    def test_invalid_numbers_and_documents(self):
        for value in (float('nan'), float('inf'), float('-inf')):
            self.assertIsNotNone(first_difference(value, value))
        for text in ('{', '{"a": 0, "a": 1}', 'NaN', 'Infinity'):
            with self.assertRaises(ValueError):
                parse_json(text)
        valid = '/* generated */\nexport const SKIN = {"x":-0.0};\n'
        self.assertEqual(parse_skin_literal(valid), {'x': 0.0})
        for text in ('export const SKIN = {};', valid + 'alert(1)',
                     valid.replace('{"x":-0.0}', 'null')):
            with self.assertRaises(ValueError):
                parse_skin_literal(text)
