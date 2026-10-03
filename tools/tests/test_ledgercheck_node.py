"""Missing Node must be one dependency refusal, before any prose comparisons."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
MESSAGE = 'ledgercheck: node is missing from PATH; install Node to run this gate.'


class MissingNode(unittest.TestCase):
    maxDiff = None

    def test_script_refuses_before_inventory(self):
        with tempfile.TemporaryDirectory() as empty:
            # Keep repository inventory available while removing only the Node dependency.
            (Path(empty) / 'git').symlink_to(shutil.which('git'))
            result = subprocess.run(
                [sys.executable, 'tools/check_float_ledger.py'], cwd=ROOT,
                env=dict(os.environ, PATH=empty), capture_output=True, text=True, timeout=60)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')
        self.assertEqual(result.stderr.strip(), MESSAGE)

    def test_make_reports_the_same_single_dependency_failure(self):
        make = shutil.which('make')
        self.assertIsNotNone(make)
        with tempfile.TemporaryDirectory() as empty:
            # Keep repository inventory available while removing only the Node dependency.
            (Path(empty) / 'git').symlink_to(shutil.which('git'))
            result = subprocess.run(
                [make, '--no-print-directory', 'ledgercheck', 'PY=' + sys.executable], cwd=ROOT,
                env=dict(os.environ, PATH=empty), capture_output=True, text=True, timeout=60)
        self.assertNotEqual(result.returncode, 0)
        text = result.stdout + result.stderr
        self.assertEqual(text.count(MESSAGE), 1)
        self.assertNotIn('inventoried blocks', text)
        self.assertNotIn('Traceback', text)


if __name__ == '__main__':
    unittest.main()
