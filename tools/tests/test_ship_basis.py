"""Named reserve policy, perturbation continuity and independent model parity."""
import importlib.util
import json
from pathlib import Path
import subprocess
import unittest

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('cell', ROOT / 'research/analysis/vacuum-cell.py')
cell = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cell)
KNOCKDOWNS = [0.30, 0.30 - 1e-6, 0.30 + 1e-6, 0.31, 0.29]


class ShipBasisTests(unittest.TestCase):
    def test_continuity_and_full_case_parity(self):
        script = """
          import {ship0} from './ship/model.js';
          const out = {};
          for (const basis of ['record', 'favourable']) {
            out[basis] = [0.30, 0.30-1e-6, 0.30+1e-6, 0.31, 0.29].map(kd =>
              ship0('s1050', 1.2, null, kd, false, false, basis));
          }
          console.log(JSON.stringify(out));
        """
        twin = json.loads(subprocess.check_output(
            ['node', '--input-type=module', '-e', script], cwd=ROOT, text=True))

        def compare(a, b):
            if isinstance(a, dict):
                self.assertEqual(set(a), set(b))
                for k in a:
                    compare(a[k], b[k])
            elif isinstance(a, list):
                self.assertEqual(len(a), len(b))
                for x, y in zip(a, b):
                    compare(x, y)
            elif isinstance(a, (int, float)) and not isinstance(a, bool):
                self.assertAlmostEqual(a, b, delta=1e-9 * max(1, abs(a)))
            else:
                self.assertEqual(a, b)

        print('basis knockdown Python_t JavaScript_t Python_reserve_t JavaScript_reserve_t')
        for basis in ('record', 'favourable'):
            cases = [cell.ship0('s1050', 1.2, gi_knockdown=kd, basis=basis)
                     for kd in KNOCKDOWNS]
            compare(cases, twin[basis])
            for i, (kd, py, js) in enumerate(zip(KNOCKDOWNS, cases, twin[basis])):
                print(f'{basis} {kd:.6f} {py["totalT"]:.9f} {js["totalT"]:.9f} '
                      f'{py["ledgerT"]["stabilityReserve"]:.9f} '
                      f'{js["ledgerT"]["stabilityReserve"]:.9f}')
                if i in (1, 2):
                    self.assertLess(abs(py['totalT'] - cases[0]['totalT']), 0.01)
                    self.assertLess(abs(js['totalT'] - twin[basis][0]['totalT']), 0.01)

    def test_named_defaults_and_legacy_points(self):
        for basis, kd in (('record', cell.SHIP0['giKnockdown']),
                          ('favourable', cell.SHIP0['giKnockdownFrame'])):
            self.assertEqual(cell.ship0(basis=basis), cell.ship0(gi_knockdown=kd))
        self.assertGreater(cell.ship0(gi_knockdown=0.31, basis='record')['ledgerT']['stabilityReserve'], 0)
        self.assertEqual(cell.ship0(gi_knockdown=0.30, basis='favourable')['ledgerT']['stabilityReserve'], 0)

    def test_custom_knockdown_and_invalid_basis_are_refused_in_both_models(self):
        for kwargs in ({'gi_knockdown': 0.31}, {'basis': 'unknown'}):
            with self.assertRaises(ValueError):
                cell.ship0(**kwargs)
        script = """
          import assert from 'node:assert/strict';
          import {ship0} from './ship/model.js';
          assert.throws(() => ship0('s1050', 1.2, null, 0.31), /requires basis/);
          assert.throws(() => ship0(null, null, null, null, false, false, 'unknown'), /basis must/);
          for (const [basis, kd] of [['record', 0.30], ['favourable', 0.65]]) {
            assert.deepEqual(ship0(null, null, null, kd),
              ship0(null, null, null, null, false, false, basis));
          }
        """
        subprocess.run(['node', '--input-type=module', '-e', script], cwd=ROOT, check=True)


if __name__ == '__main__':
    unittest.main()
