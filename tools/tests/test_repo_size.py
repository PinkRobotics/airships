"""Exercise both sides of the tracked-file size limit on a temporary repository."""
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

TOOL = Path(__file__).resolve().parents[1] / 'check_repo_size.py'


class RepositorySize(unittest.TestCase):
    def test_over_limit_red_then_under_limit_green(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            subprocess.run(['git', 'init', '-q', str(root)], check=True, capture_output=True)
            (root/'large.dat').write_bytes(b'x' * 11)
            (root/'small.dat').write_bytes(b'y' * 3)
            (root/'untracked.dat').write_bytes(b'z' * 20)
            subprocess.run(['git', '-C', str(root), 'add', 'large.dat', 'small.dat'], check=True)
            argv = [sys.executable, '-B', str(TOOL), '--root', str(root), '--limit', '10']
            red = subprocess.run(argv, capture_output=True, text=True)
            self.assertEqual(red.returncode, 1, red.stderr)
            self.assertIn('FAIL large.dat: 11 bytes exceeds 10', red.stdout)
            self.assertNotIn('untracked.dat', red.stdout)
            (root/'large.dat').write_bytes(b'x' * 10)
            green = subprocess.run(argv, capture_output=True, text=True)
            self.assertEqual(green.returncode, 0, green.stderr)
            self.assertIn('PASS; 2 tracked files; limit 10 bytes', green.stdout)
            self.assertIn('10\tlarge.dat', green.stdout)


if __name__ == '__main__':
    unittest.main()
