"""Parallel runner policy and coverage; no model subprocesses needed."""
import os
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import test_float_hardening as plants


class RunnerPolicy(unittest.TestCase):
    def test_worker_limit_and_default(self):
        with patch.dict(os.environ, {}, clear=True), patch.object(os, 'cpu_count', return_value=64):
            self.assertEqual(plants.workers(), 8)
        for requested, expected in [('1', 1), ('2', 2), ('8', 8), ('99', 8)]:
            with patch.dict(os.environ, FLOAT_PLANT_WORKERS=requested):
                self.assertEqual(plants.workers(), expected)
        for requested in ('0', '-1', 'invalid'):
            with patch.dict(os.environ, FLOAT_PLANT_WORKERS=requested):
                with self.assertRaises(ValueError):
                    plants.workers()

    def test_command_timeout_default_and_override(self):
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(plants.command_timeout(), 600)
        for requested, expected in [('1', 1), ('240', 240), ('1800', 1800)]:
            with patch.dict(os.environ, FLOAT_PLANT_TIMEOUT=requested):
                self.assertEqual(plants.command_timeout(), expected)
        for requested in ('0', '-1', '1.5', 'invalid'):
            with patch.dict(os.environ, FLOAT_PLANT_TIMEOUT=requested):
                with self.assertRaises(ValueError):
                    plants.command_timeout()

    def test_fast_subset_retains_every_control_and_fixed_order(self):
        full, fast = plants.selected_cases('all'), plants.selected_cases('fast')
        self.assertEqual(list(fast), [name for name in full if name in fast])
        self.assertTrue(set(plants.FAST_CASES) <= set(fast))
        self.assertTrue({n for n, s in full.items() if s.get('green')} <= set(fast))
        self.assertLess(len(fast), len(full))
        with self.assertRaises(ValueError):
            plants.selected_cases('unrecognised')


if __name__ == '__main__':
    unittest.main()
