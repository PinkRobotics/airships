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


class DropAtmosphere(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import subprocess, tempfile
        cls.scratch = tempfile.TemporaryDirectory(prefix='drop-test-')
        cls.addClassCleanup(cls.scratch.cleanup)
        output = Path(cls.scratch.name) / 'delivery.json'
        subprocess.run(['python3', '-B', 'research/analysis/delivery.py', '--json', str(output)],
                       cwd=ROOT, check=True, stdout=subprocess.DEVNULL)
        cls.record = json.loads(output.read_text())
        # Read the constants and defaults from the live model, then integrate an analytic
        # ISA expression independently of the producer's sampled density column.
        script = "import {ISA,CFG,ALT,TERRAIN_MSL} from './sim/index.js'; console.log(JSON.stringify({ISA,rho0:CFG.rhoSL,drop:ALT.drop,terrain:TERRAIN_MSL}));"
        cls.model = json.loads(subprocess.check_output(['node', '--input-type=module', '-e', script], cwd=ROOT))

    def independent(self, diameter):
        m = self.model; isa = m['ISA']; v0 = self.record['references']['terminalMs'][str(float(diameter))]
        import math
        alpha = .375 + .025 * diameter
        beta = alpha * (isa['G0'] / (isa['R'] * isa['LAPSE']) - 1)
        c = isa['LAPSE'] / isa['T0']
        lo = 1 - c * m['terrain']; hi = 1 - c * (m['terrain'] + m['drop'])
        seconds = (m['rho0'] / 1.225) ** alpha / v0 * (lo ** (beta + 1) - hi ** (beta + 1)) / (c * (beta + 1))
        density = m['rho0'] * hi ** (isa['G0'] / (isa['R'] * isa['LAPSE']) - 1)
        speed = v0 * (1.225 / density) ** alpha
        return speed, seconds

    def test_two_diameters_match_independent_density_integral(self):
        for diameter in (2, 5):
            with self.subTest(diameter=diameter):
                speed, seconds = self.independent(diameter)
                row = self.record['fall']['P-series ALT.drop'][f'{float(diameter)} mm']
                self.assertAlmostEqual(row['fallSeconds'], seconds, delta=.051)
                self.assertAlmostEqual(row['fallSecondsExact'], seconds, delta=2e-6)
                self.assertAlmostEqual(row['terminalAtReleaseMs'], speed, delta=1e-10)
                self.assertAlmostEqual(row['driftExactM']['10 m/s'], 10 * seconds, delta=2e-5)

    def test_warm_threshold_is_qualified(self):
        row = self.record['updraftVerdict']['active flank']
        self.assertIn('threshold', row['uncertainty'])
        self.assertNotEqual(row.get('warmVerdict'), 'descends')

    def test_generated_regions_check_and_reject_stale_prose(self):
        # The public note is only written for the producer's canonical output path.
        # This check runs after the production generation in the lane and existing gate.
        import subprocess
        result = subprocess.run(['python3', '-B', 'research/analysis/delivery.py', '--check'],
                                cwd=ROOT, text=True, capture_output=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
