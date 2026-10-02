import copy
import io
import json
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from pipeline import live
from pipeline import vectors
from static import violations

FIXTURE = json.loads((Path(__file__).parent / 'fixtures/wind-response.json').read_text())


class WindTests(unittest.TestCase):
    def test_recorded_batch_to_vectors(self):
        grid = live.wind_grid(FIXTURE, [50, 54], [-128, -124])
        self.assertEqual(len(grid['vectors']), 4)
        self.assertAlmostEqual(grid['vectors'][0][0], 21.173326, places=5)
        self.assertAlmostEqual(grid['vectors'][0][1], 43.411750, places=5)
        self.assertEqual(grid['forecastAt'], '2026-10-02T02:00:00+00:00')

    def test_bad_or_partial_forecast_rejected(self):
        for change in ('missing', 'null', 'units', 'hour'):
            body = copy.deepcopy(FIXTURE)
            if change == 'missing': body.pop()
            if change == 'null': body[0]['hourly']['wind_speed_850hPa'][0] = None
            if change == 'units': body[0]['hourly_units']['wind_speed_850hPa'] = 'm/s'
            if change == 'hour': body[0]['hourly']['time'][0] = '2026-10-02T03:00'
            with self.subTest(change=change), self.assertRaises(ValueError):
                live.wind_grid(body, [50, 54], [-128, -124])

    def test_hourly_fetch_and_failed_attempt_preserve_age(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            body = [FIXTURE[i % 4] for i in range(25)]
            with patch.object(live, 'ROOT', root), patch.object(live, 'LIVE', root), \
                    patch.object(live.urllib.request, 'urlopen') as request:
                request.return_value = io.StringIO(json.dumps(body))
                self.assertTrue(live.fetch('wind', live.FEEDS['wind']))
                before = (root / 'wind.json').read_bytes()
                self.assertFalse(live.fetch('wind', live.FEEDS['wind']))
                request.assert_called_once()
                old = (datetime.now(timezone.utc) - timedelta(hours=2)).isoformat()
                (root / '.wind-attempt.json').write_text(json.dumps({'fetchedAt': old}))
                with patch.object(live, 'age_min', return_value=120):
                    request.side_effect = OSError('fixture outage')
                    with self.assertRaises(OSError): live.fetch('wind', live.FEEDS['wind'])
                self.assertEqual((root / 'wind.json').read_bytes(), before)
                # The retry is skipped even when the successful copy is old.
                doc = json.loads(before); doc['fetchedAt'] = old
                (root / 'wind.json').write_text(json.dumps(doc))
                self.assertFalse(live.fetch('wind', live.FEEDS['wind']))
                self.assertEqual(request.call_count, 2)


class StaticTests(unittest.TestCase):
    def test_load_positions(self):
        examples = ['<script src="https://cdn.invalid/a.js"></script>',
                    '<link rel="stylesheet" href="https://cdn.invalid/a.css">',
                    '<link rel="preload" href="https://cdn.invalid/a">',
                    '<link rel="icon" href="//cdn.invalid/a">',
                    'fetch("https://cdn.invalid/api")', 'import "https://cdn.invalid/a.js"',
                    'import("https://cdn.invalid/a.js")', 'import x from "https://cdn.invalid/a.js"',
                    'url(https://cdn.invalid/a.png)', 'image.src = "https://cdn.invalid/a.png"',
                    '<img srcset="/a.png 1x, https://cdn.invalid/b.png 2x">']
        for example in examples:
            with self.subTest(example=example): self.assertTrue(violations(example, '.html'))

    def test_non_loading_allowlist(self):
        text = '<a href="https://reference.invalid/">Source</a><link rel="canonical" href="https://site.invalid/">'
        self.assertEqual(violations(text, '.html'), [])


class VectorTests(unittest.TestCase):
    def test_crossing_segment_clips_even_if_both_ends_are_outside(self):
        self.assertEqual(vectors.clip_segment([-2, 1], [4, 1], [0, 0, 2, 2]), [[0, 1], [2, 1]])
        self.assertIsNone(vectors.clip_segment([-2, 3], [4, 3], [0, 0, 2, 2]))

    def test_tampered_archive_rejected_before_parsing(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'archive.tar.gz'
            path.write_bytes(b'wrong archive')
            with self.assertRaisesRegex(ValueError, 'SHA-256 mismatch'):
                vectors.read_archive(path)


if __name__ == '__main__':
    unittest.main()
