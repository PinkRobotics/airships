"""Numerical units, native result parsing, and scratch-path contracts for U1."""

import importlib.util
from pathlib import Path
import unittest


MODULE = Path(__file__).resolve().parents[1] / "tools/vacuum_u1_benchmarks.py"
SPEC = importlib.util.spec_from_file_location("vacuum_u1", MODULE)
u1 = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(u1)


class BenchmarkContracts(unittest.TestCase):
    def test_classical_sphere_pressure_in_si(self):
        self.assertAlmostEqual(u1.sphere_pressure(210e9, .3, .01, 1),
                               25_419_556.3720897, places=6)
        self.assertAlmostEqual(u1.sphere_pressure(210e9, .3, .02, 1),
                               4 * u1.sphere_pressure(210e9, .3, .01, 1))
        self.assertEqual(u1.sphere_pressure(210e9, .3, .02, 2),
                         u1.sphere_pressure(210e9, .3, .01, 1))

    def test_native_dat_keeps_all_modes_including_unwelcome_low_modes(self):
        dat = """
                        S T E P       1
     B U C K L I N G   F A C T O R   O U T P U T
 MODE NO       BUCKLING
                FACTOR
      1   0.1469241E+02
      2   0.2917707E+02
      3   0.5895219E+02
      4   0.7060272E+02
      5   0.2581284E+05
      6   0.2583039E+05
      7   0.2585942E+05
      8   0.2594742E+05
"""
        factors = u1.parse_factors(dat)
        self.assertEqual(len(factors), 8)
        self.assertEqual(min(factors), 14.69241)
        self.assertEqual(factors[-1], 25947.42)

    def test_cylinder_formula_has_line_load_units_and_classical_limit(self):
        line_load = u1.cylinder_line_load(210e9, .3, .01, 1, 2, 5, 9)
        self.assertAlmostEqual(line_load, 12_709_787.803709362, places=6)
        # Uniform scale doubles line load but leaves stress unchanged.
        self.assertAlmostEqual(u1.cylinder_line_load(210e9, .3, .02, 2, 4, 5, 9),
                               2*line_load)
        self.assertLess(abs(line_load/12_709_778.186044851 - 1), 1e-6)

    def test_missing_eigenvalue_section_is_not_a_result(self):
        self.assertEqual(u1.parse_factors("Job finished\n 1 123.000E+02\n"), [])
        self.assertEqual(u1.parse_factors("*ERROR reading *NODE"), [])

    def test_fortran_exponents_and_signed_modes_are_preserved(self):
        factors = u1.parse_factors("BUCKLING FACTOR OUTPUT\n1 -1.000D+02\n2 0.000E+00\n")
        self.assertEqual(factors, [-100.0, 0.0])

    def test_storage_path_resolves_before_allowlisting(self):
        for path in ("/tmp/u1", "/mnt/scratch/u1", "/mnt/24TB-A/u1", "/home/../tmp/u1"):
            with self.subTest(path=path), self.assertRaises(ValueError):
                u1.home_path(path)
        own = Path(__file__).resolve()
        self.assertEqual(u1.home_path(own), own)


if __name__ == "__main__":
    unittest.main()
