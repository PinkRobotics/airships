"""Counterexamples to partial numeric matches, in disposable document copies."""
import contextlib
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check_analysis as gate
import check_figures as figures


class NumericTokenTests(unittest.TestCase):
    def test_format_families(self):
        for value, fmt in ((54, 'd'), (1234, ',d'), (54.0, '.0f'), (-1.9, '+.1f'),
                           (1.9, '+.1f'), (1234.0, ',.0f'), (1.23, '.2f')):
            want = format(value, fmt)
            with self.subTest(fmt=fmt, want=want), tempfile.TemporaryDirectory() as td:
                doc = Path(td) / 'plant.md'
                for near in (want + '.74°', want + ',000', '9' + want, '.' + want):
                    doc.write_text(near)
                    self.assertFalse(gate.matches(doc.read_text(), want), near)
                doc.write_text(want + '. Next sentence; ' + want + ', a quantity.')
                self.assertTrue(gate.matches(doc.read_text(), want))
                print(f'RED {fmt} near-misses; GREEN complete {want}')

    def test_angle_is_not_ratio(self):
        with tempfile.TemporaryDirectory() as td:
            doc = Path(td) / 'plant.md'
            doc.write_text('54.74°')
            self.assertFalse(gate.matches(doc.read_text(), '54'))
            print('RED angle-only 54.74° for wanted 54')

    def test_every_manifest_row_and_stale_ratio(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            analysis = root / 'research/analysis'
            analysis.mkdir(parents=True)
            paths = {gate.A / md for md, _, _, _ in gate.MANIFEST}
            paths |= {gate.A / (name + '.json') for _, name, _, _ in gate.MANIFEST}
            for src in paths:
                dest = root / src.resolve().relative_to(gate.ROOT)
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src, dest)
            _, bad, checked = gate.check_rows(analysis)
            self.assertEqual(bad, [])
            self.assertEqual(checked, len(gate.MANIFEST))
            doc = analysis / 'vacuum-cell.md'
            correct = doc.read_text()
            self.assertIn('optimum here is **R/t ≈ 54**', correct)
            doc.write_text(correct.replace('optimum here is **R/t ≈ 54**',
                                           'optimum here is **R/t ≈ 76**'))
            _, bad, _ = gate.check_rows(analysis)
            self.assertEqual(len(bad), 1, bad)
            self.assertIn('designPoint/tubeROverT', bad[0])
            print('RED base line 63 despite angle elsewhere; GREEN corrected manifest')

    def test_unrelated_short_witness_does_not_rescue_ratio(self):
        context = gate.CONTEXTS[('vacuum-cell.md', 'designPoint/tubeROverT')]
        self.assertFalse(gate.matches('54 tubes. The optimum here is **R/t ≈ 76**', '54', context))
        self.assertTrue(gate.matches('The optimum here is **R/t ≈ 54**', '54', context))

    def test_report_citation_cannot_capture_numeric_suffix(self):
        for raw in ('.54', ',54', '.54.74'):
            self.assertIsNone(figures.CITE.search(raw + ' kg<!--f:test.value-->'))
        for raw in ('54', '54.74', '1,234', '-1.9'):
            self.assertEqual(figures.CITE.search(raw + ' kg<!--f:test.value-->').group(1), raw)


if __name__ == '__main__':
    unittest.main()
