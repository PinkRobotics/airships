"""Refuse both a stale floor sentence and a changed budget before publication."""
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
ROOT = Path(__file__).resolve().parents[2]

class FloorProse(unittest.TestCase):
    def test_prose_and_input_plants(self):
        with tempfile.TemporaryDirectory(dir=os.environ['TMPDIR']) as td:
            tree = Path(td)
            files = ['tools/gen_mass_budget_prose.py', 'research/analysis/mass-budget.json',
                     'research/analysis/mass-budget.md']
            for file in files:
                target = tree / file
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(ROOT / file, target)
            command = ['python3', '-B', 'tools/gen_mass_budget_prose.py', '--check']
            for label, file in [('stale nominal floor', files[2]), ('changed floor record', files[1])]:
                target = tree / file
                original = target.read_text()
                if file.endswith('.md'):
                    target.write_text(original.replace('**216.1 t, 2.16×**', '**181.3 t, 1.81×**'))
                else:
                    import json
                    data = json.loads(original)
                    data['classes']['P100']['cases']['floor']['totalT'] += 10
                    target.write_text(json.dumps(data))
                red = subprocess.run(command, cwd=tree, capture_output=True, text=True)
                self.assertNotEqual(red.returncode, 0, red.stdout + red.stderr)
                target.write_text(original)
                green = subprocess.run(command, cwd=tree, capture_output=True, text=True)
                self.assertEqual(green.returncode, 0, green.stdout + green.stderr)
                print(label + ': RED; corrected copy GREEN')
