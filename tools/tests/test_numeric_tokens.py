"""Counterexamples to partial numeric matches, in disposable document copies."""
import contextlib
import json
import os
import subprocess
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
            paths = {gate.document_path(md) for md, _, _, _ in gate.MANIFEST}
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


class ClosureConservationTests(unittest.TestCase):
    """Plants live only in disposable copies under the caller's TMPDIR."""
    def copy_and_generate(self, root, old_equation=False):
        for rel in ('research/figures.json', 'research/analysis/mass-budget.py',
                    'research/analysis/vacuum-cell.py'):
            dest = root / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(gate.ROOT / rel, dest)
        model = root / 'research/analysis/mass-budget.py'
        if old_equation:
            text = model.read_text().replace(
                'effective_shell = shell_kg_m3 * (1.0 + sundries_frac)',
                'effective_shell = shell_kg_m3')
            model.write_text(text)
        output = root / 'research/analysis/mass-budget.json'
        subprocess.run([sys.executable, '-B', str(model), '--json', str(output)],
                       check=True, capture_output=True, text=True)
        return json.loads(output.read_text())

    def test_old_equation_red_then_corrected_copy_green(self):
        with tempfile.TemporaryDirectory(dir=os.environ['TMPDIR']) as td:
            root = Path(td)
            figures = json.loads((gate.ROOT / 'research/figures.json').read_text())
            old = self.copy_and_generate(root, old_equation=True)
            bad, count = gate.check_closure_bills(old, figures)
            self.assertEqual(count, 126)
            self.assertEqual(len(bad), count)
            label = 'P100/floor/hullThatCloses/0.508'
            witnesses = [x for x in bad if x.startswith(label + ':')]
            self.assertEqual(len(witnesses), 1)
            row = old['classes']['P100']['rightSized']['floor']['hullThatCloses']['0.508']
            expected = -0.508 * row['volumeM3'] * old['evidence']['sundries_frac']['floor']['value'] / 1000
            residual = float(witnesses[0].split(' = ', 1)[1].split(' t;', 1)[0])
            self.assertLess(residual, 0)
            rounding = 0.5 * figures['atmosphere']['rhoAtWorkAlt'] / 1000 + 1e-6
            self.assertAlmostEqual(residual, expected, delta=rounding)
            print(f'RED old closing equation: {len(bad)}/{count} bills fail')
            corrected = self.copy_and_generate(root)
            bad, count = gate.check_closure_bills(corrected, figures)
            self.assertEqual(bad, [])
            self.assertGreater(count, 0)
            print(f'GREEN corrected disposable copy: {count} bills conserve mass')

    def test_impossible_closure_red(self):
        with tempfile.TemporaryDirectory(dir=os.environ['TMPDIR']) as td:
            root = Path(td)
            document = self.copy_and_generate(root)
            figures = json.loads((gate.ROOT / 'research/figures.json').read_text())
            rows = document['classes']['P10000']['rightSized']['floor']['hullThatCloses']
            rows['0.900'] = dict(rows['0.508'])
            (root / 'plant.json').write_text(json.dumps(document))
            bad, _ = gate.check_closure_bills(json.loads((root / 'plant.json').read_text()), figures)
            self.assertEqual(len(bad), 1)
            self.assertIn('effective shell density 0.990000', bad[0])
            print('RED P10000 impossible closure: ' + bad[0])
            # Exact equality at the wall must be refused too.
            document['evidence']['sundries_frac']['floor']['value'] = figures['atmosphere']['rhoAtWorkAlt'] / .9 - 1
            bad, _ = gate.check_closure_bills(document, figures)
            self.assertTrue(any('P10000/floor/hullThatCloses/0.900: claims closure' in b for b in bad))

    def test_volume_rounding_is_the_only_mass_tolerance(self):
        document = json.loads((gate.A / 'mass-budget.json').read_text())
        figures = json.loads((gate.ROOT / 'research/figures.json').read_text())
        record = document['classes']['P100']['rightSized']['floor']['hullThatCloses']['0.508']
        record['volumeM3'] += 2
        bad, _ = gate.check_closure_bills(document, figures)
        self.assertTrue(any('P100/floor/hullThatCloses/0.508: lift - complete bill' in b for b in bad))
        print('RED volume moved by 2 m3 beyond rounding tolerance')


if __name__ == '__main__':
    unittest.main()
