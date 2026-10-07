"""Delivery weather boundaries; run by the existing first-party static gate."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[2]

class MissionWeather(unittest.TestCase):
    def test_remote_and_active_front_are_distinct(self):
        note = ' '.join((ROOT / 'research/analysis/delivery.md').read_text().split())
        self.assertIn('Remote pre-wetting', note)
        self.assertIn('ahead of an active front', note)
        self.assertNotIn('Pre-treatment has none of them', note)
        self.assertNotIn('There is no column over unburned fuel', note)
        self.assertIn('time-resolved wind profiles', note)
        self.assertIn('vertical velocity', note)
        self.assertIn('not an operating standoff', note)

    def test_plume_source_is_link_only(self):
        sources = json.loads((ROOT / 'research/sources.json').read_text())['sources']
        source = next(s for s in sources if s['id'] == 'lareau-clements-2017-plume')
        self.assertIsNone(source['file'])
        self.assertFalse(source['redistributable'])
        self.assertEqual(source['doi'], '10.1175/JAMC-D-16-0384.1')
