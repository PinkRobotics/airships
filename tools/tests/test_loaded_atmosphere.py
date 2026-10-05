"""The published boundary reproduces the counterexample and refuses drift."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]

class LoadedAtmosphere(unittest.TestCase):
    def test_boundary_and_scratch_drift(self):
        data = json.loads((ROOT / 'research/analysis/loaded-atmosphere.json').read_text())
        for row in data['classes'].values():
            self.assertAlmostEqual(row['criticalDeltaK'], 14.286943, places=5)
            self.assertAlmostEqual(row['atISAPlus15K']['marginPct'], -0.248539, places=5)
            self.assertAlmostEqual(row['criticalDensityKgM3'] * row['displacementM3'] / 1000,
                                   row['loadedT'], places=8)
        with tempfile.TemporaryDirectory(dir=os.environ['TMPDIR']) as scratch:
            tree = Path(scratch)
            shutil.copytree(ROOT / 'sim', tree / 'sim')
            for path in ('research/analysis/loaded-atmosphere.mjs',
                         'research/analysis/loaded-atmosphere.json',
                         'docs/PHYSICS.md', 'docs/OPEN-QUESTIONS.md'):
                destination = tree / path
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(ROOT / path, destination)
            command = ['node', 'research/analysis/loaded-atmosphere.mjs', '--check']
            for name, path in [('boundary JSON', 'research/analysis/loaded-atmosphere.json'),
                               ('physics sentence', 'docs/PHYSICS.md'),
                               ('recovery sentence', 'docs/OPEN-QUESTIONS.md')]:
                target = tree / path
                original = target.read_text()
                target.write_text(original.replace('14.29', '15.29') if path.endswith('.md')
                                  else original.replace('14.286', '15.286'))
                red = subprocess.run(command, cwd=tree, capture_output=True, text=True)
                self.assertNotEqual(red.returncode, 0, red.stdout + red.stderr)
                target.write_text(original)
                green = subprocess.run(command, cwd=tree, capture_output=True, text=True)
                self.assertEqual(green.returncode, 0, green.stdout + green.stderr)
                print(name + ': RED; corrected copy GREEN')
