"""State APIs, old-output invariance, and both directions of the bound predicate."""
import importlib.util
import math
from pathlib import Path
import unittest

from check import bound_row

ROOT = Path(__file__).resolve().parents[2]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'research/analysis' / (name+'.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


class StateAPIs(unittest.TestCase):
    def test_helium_legacy_unrounded_operations_at_working_state(self):
        gas = module('helium')
        t, p, rho = gas.isa(2500)
        for name, r in [('helium', gas.R_HE), ('hydrogen', gas.R_H2)]:
            old = p / (r * t)
            self.assertEqual(gas.gas_density(t, p, name), old)
            for structure in [0, 0.01, 0.455, 1.2]:
                self.assertEqual(gas.net_lift(t, p, old, structure), rho-old-structure)

    def test_helium_state_scaling_and_invalid_inputs(self):
        gas = module('helium')
        density = gas.gas_density(288.15, 101325)
        self.assertEqual(gas.gas_density(288.15, 202650), 2*density)
        self.assertEqual(gas.gas_density(576.3, 101325), density/2)
        for t, p, kind in [(0, 101325, 'helium'), (288, -1, 'helium'), (math.nan, 1, 'helium'),
                           (288, math.inf, 'air'), (288, 101325, 'unknown')]:
            with self.assertRaises(ValueError):
                gas.gas_density(t, p, kind)
        with self.assertRaises(ValueError):
            gas.net_lift(288, 101325, -1)

    def test_bound_directions_and_paper_mass_closure(self):
        for direction, model, expected in [('<=', 9, 'bound holds'), ('<=', 11, 'bound fails'),
                                            ('>=', 11, 'bound holds'), ('>=', 9, 'bound fails')]:
            r = bound_row('fixture', model, {'value': 10}, 'kg', 0, 'no slack', direction=direction)
            self.assertEqual(r['verdict'], expected)
        rep = module('reproductions')
        ak = rep.akhmeteli(2.5, 4.23e-5, 3.52e-3, 2500, 50, 1.29, 460e9)
        self.assertEqual(ak['thin_shell_mass_kg'] + ak['thin_payload_kg'], ak['displaced_air_kg'])
        self.assertAlmostEqual(ak['outer_face_kg'] + ak['inner_face_kg'] + ak['core_kg'], ak['shell_mass_kg'])
        je = rep.jenett(10, 101000, 1.225, 588e9, 1930)
        self.assertIsNone(je['net_lift_kg'])
        self.assertTrue(je['missing_inputs'])
        self.assertAlmostEqual(je['member_euler_load_N'], je['member_force_N'])
        heavier = rep.jenett(10, 101000, 1.225, 588e9, 1930, member_count=100)
        self.assertAlmostEqual(heavier['net_lift_kg'], je['displaced_air_kg'] - 100*je['member_mass_kg'])
