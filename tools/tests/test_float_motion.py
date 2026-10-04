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
    (r'remain(?:s|ed|ing)? in the air',
     ('remain in the air', 'remains in the air', 'remained in the air', 'remaining in the air')),
    (r'gain(?:s|ed|ing)? altitude', ('gain altitude', 'gains altitude', 'gained altitude', 'gaining altitude')),
    (r'hold(?:s|ing)? station(?: overhead)?',
     ('hold station', 'holds station', 'holding station',
      'hold station overhead', 'holds station overhead', 'holding station overhead')),
    (r'held station(?: overhead)?', ('held station', 'held station overhead')),
    (r'soar(?:s|ed|ing)?', ('soar', 'soars', 'soared', 'soaring')),
    (r'drift(?:s|ed|ing)? upward', ('drift upward', 'drifts upward', 'drifted upward', 'drifting upward')),
    (r'(?:take(?:s|n)?|took|taking) off by (?:itself|themselves)',
     ('take off by itself', 'takes off by itself', 'taken off by itself', 'took off by itself',
      'taking off by itself', 'take off by themselves', 'takes off by themselves',
      'taken off by themselves', 'took off by themselves', 'taking off by themselves')),
    (r'stay(?:s|ed|ing)? in the sky',
     ('stay in the sky', 'stays in the sky', 'stayed in the sky', 'staying in the sky')),
    (r'stay(?:s|ed|ing)? at (?:the )?(?:planned )?altitude',
     ('stay at altitude', 'stays at altitude', 'stayed at altitude', 'staying at altitude',
      'stay at the altitude', 'stays at the altitude', 'stayed at the altitude', 'staying at the altitude',
      'stay at planned altitude', 'stays at planned altitude', 'stayed at planned altitude', 'staying at planned altitude',
      'stay at the planned altitude', 'stays at the planned altitude',
      'stayed at the planned altitude', 'staying at the planned altitude')),
)
VEHICLE_ROWS = (
    (r'hulls?', ('hull', 'hulls')),
    (r'ships?', ('ship', 'ships')),
    (r'airships?', ('airship', 'airships')),
    (r'vehicles?', ('vehicle', 'vehicles')),
    (r'cells?', ('cell', 'cells')),
    (r'crafts?', ('craft', 'crafts')),
    (r'dirigibles?', ('dirigible', 'dirigibles')),
)
FRONT = 'Airborne, the drawn ship crosses the valley with its engines off.'
NONCLAIMS = (
    'We craft a diagram of a track that climbs a ridge.',
    'They craft a caption about a kite that soars.',
    'The craft of writing soars in popularity.',
    'The craft of carpentry remains in the workshop.',
    'The station holds a collection of maps.',
    'The station overhead carries electrical wires.',
    'The train remains in the station.',
    'The crane holds station beside the dock.',
    'The track gains altitude along the ridge.',
    'A green suite is not evidence that the craft is buildable.',
)


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

    def test_nonflight_senses(self):
        for sentence in NONCLAIMS:
            with self.subTest(sentence=sentence):
                self.assertFalse(relation(sentence))

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
