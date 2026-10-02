"""The README gate must reject edited figures and broken generation markers."""

import subprocess
import sys
import tempfile
from pathlib import Path
import re
import unittest


ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools/gen_readme.py"


class ReadmeGenerationTest(unittest.TestCase):
    def test_changed_figure_fails_then_regeneration_repairs_it(self):
        with tempfile.TemporaryDirectory() as directory:
            readme = Path(directory) / "README.md"
            original = (ROOT / "README.md").read_text()
            changed, count = re.subn(r"\*\*[\d,.]+ MWh/cycle\*\*", "**0 MWh/cycle**", original, count=1)
            self.assertEqual(count, 1)
            readme.write_text(changed)
            command = [sys.executable, str(TOOL), "--readme", str(readme)]
            red = subprocess.run(command + ["--check"], capture_output=True, text=True)
            self.assertEqual(red.returncode, 1, red.stdout + red.stderr)
            self.assertIn("differs", red.stderr)
            green = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(green.returncode, 0, green.stdout + green.stderr)
            checked = subprocess.run(command + ["--check"], capture_output=True, text=True)
            self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
            self.assertEqual(readme.read_text(), original)

    def test_missing_marker_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            readme = Path(directory) / "README.md"
            readme.write_text((ROOT / "README.md").read_text().replace(
                "<!-- readme:headline:end -->", "", 1))
            result = subprocess.run(
                [sys.executable, str(TOOL), "--readme", str(readme), "--check"],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("Expected one pair", result.stderr)


if __name__ == "__main__":
    unittest.main()
