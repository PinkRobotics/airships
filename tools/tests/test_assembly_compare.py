"""The report omits only host durations; zero ledger tolerances allow round-off."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from check_assembly import _moved, comparable_report
from data_compare import first_difference
import numpy as np


class AssemblyComparison(unittest.TestCase):
    def test_surface_projection_agrees_for_single_points_and_batches(self):
        from check_assembly import field_points
        point = [13.492639541625977, -6.097604751586914, -9.41795539855957]
        axis = np.array([0.7224249839782715, 0.0, -0.6914493441581726], np.float32)
        single = field_points([point]) @ axis
        batch = field_points([point] * 4096) @ axis
        self.assertEqual(single.dtype, np.float32)
        self.assertTrue(np.array_equal(batch, np.repeat(single, 4096)))
        self.assertEqual(single[0], np.float32(16.25946))

    def test_minimum_labels_ties_in_discovery_order_without_moving_the_bound(self):
        from check_assembly import minimum_candidate_in_order
        self.assertEqual(minimum_candidate_in_order([(1.0 + 1e-15, 'first'), (1.0, 'last')]),
                         (1.0, 'first'))
        self.assertEqual(minimum_candidate_in_order([(1.0 + 1e-6, 'first'), (1.0, 'last')]),
                         (1.0, 'last'))

    def test_report_durations_and_every_other_value(self):
        a = {'verdict': {'runtimeS': 1.0, 'fieldS': 2.0}, 'data': [1.0, 'proof', True]}
        b = {'verdict': {'runtimeS': 3.0, 'fieldS': 4.0}, 'data': [1.0 + 1e-15, 'proof', True]}
        self.assertIsNone(first_difference(comparable_report(a), comparable_report(b)))
        b['data'][0] += 1e-6
        self.assertIn("['data'][0]", first_difference(comparable_report(a), comparable_report(b)))
        self.assertEqual(a['verdict']['runtimeS'], 1.0)

    def test_zero_ledger_float_tolerance_and_counts(self):
        self.assertFalse(_moved('sumEngagementMm', 2664.0, 2664.0 + 1e-12))
        self.assertTrue(_moved('sumEngagementMm', 2664.0, 2664.0 + 0.01))
        self.assertTrue(_moved('closingMembers', 166, 167))
        self.assertTrue(_moved('passed', False, 0))
        self.assertTrue(_moved('key', [1.0], [1.0, 2.0]))
        self.assertFalse(_moved('massG', 1.0, 1.005))
        self.assertTrue(_moved('massG', 1.0, 1.02))
        self.assertFalse(_moved('margin', 0.2008, np.float64(0.2008)))
        self.assertTrue(_moved('margin', 0.2008, np.float64(0.3)))
