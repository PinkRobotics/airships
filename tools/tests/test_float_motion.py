"""Fixed lexical rows: deleting a motion word cannot delete its counterexample."""
import re
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from float_text import MOTION, VEHICLE, dated_verdict, relation


# Deliberately independent of float_text's patterns. Each alternative has a row;
# inflections are literal examples too, rather than generated from the expression.
MOTION_ROWS = (
    (r'rise(?:s)?', ('rise', 'rises')),
    (r'rose', ('rose',)),
    (r'ris(?:en|ing)', ('risen', 'rising')),
    (r'climb(?:s|ed|ing)?', ('climb', 'climbs', 'climbed', 'climbing')),
    (r'ascend(?:s|ed|ing)?', ('ascend', 'ascends', 'ascended', 'ascending')),
    (r'stay(?:s|ed|ing)? (?:up|aloft)',
     ('stay up', 'stays up', 'stayed up', 'staying up',
      'stay aloft', 'stays aloft', 'stayed aloft', 'staying aloft')),
    (r'aloft', ('is aloft',)),
    (r'airborne', ('is airborne',)),
    (r'lift(?:s|ed|ing)? off', ('lift off', 'lifts off', 'lifted off', 'lifting off')),
    (r'(?:leave(?:s)?|left|leaving) the ground',
     ('leave the ground', 'leaves the ground', 'left the ground', 'leaving the ground')),
    (r'hover(?:s|ed|ing)?', ('hover', 'hovers', 'hovered', 'hovering')),
    (r'(?:go(?:es|ing)?|went) up', ('go up', 'goes up', 'going up', 'went up')),
)
VEHICLE_ROWS = (
    (r'hulls?', ('hull', 'hulls')),
    (r'ships?', ('ship', 'ships')),
    (r'airships?', ('airship', 'airships')),
    (r'vehicles?', ('vehicle', 'vehicles')),
    (r'cells?', ('cell', 'cells')),
)
FRONT = 'Airborne, the drawn ship crosses the valley with its engines off.'


def alternatives(pattern):
    """Split the outer finite-word union; nested alternatives stay in their row.

    Fail on a changed expression shape instead of silently missing new branches.
    This is a small splitter for these two expressions, not a regex parser.
    """
    prefix, suffix = r'\b(?:', r')\b'
    if not pattern.startswith(prefix) or not pattern.endswith(suffix):
        raise ValueError('lexical expression must remain a word-bounded union')
    body = pattern[len(prefix):-len(suffix)]
    rows, start, depth, escaped = [], 0, 0, False
    for i, char in enumerate(body):
        if escaped:
            escaped = False
        elif char == '\\':
            escaped = True
        elif char == '(':
            depth += 1
        elif char == ')':
            depth -= 1
        elif char in '[]':
            raise ValueError('character classes need explicit splitter support')
        elif char == '|' and depth == 0:
            rows.append(body[start:i])
            start = i + 1
    if depth or escaped:
        raise ValueError('unbalanced lexical expression')
    rows.append(body[start:])
    return rows


class MotionRows(unittest.TestCase):
    def assert_claim(self, sentence):
        self.assertTrue(relation(sentence), f'relation missed: {sentence}')
        self.assertTrue(dated_verdict(sentence), f'dated_verdict missed: {sentence}')

    def test_motion_rows(self):
        for branch, forms in MOTION_ROWS:
            for form in forms:
                with self.subTest(motion=form):
                    self.assertRegex(form, re.compile(branch, re.I))
                    self.assert_claim(f'The drawn hull {form} with its engines off.')

    def test_vehicle_rows(self):
        for branch, nouns in VEHICLE_ROWS:
            for noun in nouns:
                with self.subTest(vehicle=noun):
                    self.assertRegex(noun, re.compile(branch, re.I))
                    # Standalone airborne avoids the older structural relation rule.
                    self.assert_claim(f'The drawn {noun} is airborne with its engines off.')

    def test_front_form(self):
        self.assert_claim(FRONT)

    def test_every_alternative_has_an_independent_row(self):
        for pattern, rows in ((MOTION.pattern, MOTION_ROWS), (VEHICLE, VEHICLE_ROWS)):
            with self.subTest(pattern=pattern):
                actual, expected = alternatives(pattern), [branch for branch, _ in rows]
                self.assertEqual(len(actual), len(set(actual)), 'duplicate lexical branch')
                self.assertEqual(len(expected), len(set(expected)), 'duplicate fixed row')
                self.assertEqual(set(actual), set(expected),
                                 'every lexical alternative needs a fixed reviewed row')


if __name__ == '__main__':
    unittest.main()
