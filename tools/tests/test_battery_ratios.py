"""Per-class configuration changes and stale universal ratios are refused."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[2]
class BatteryRatios(unittest.TestCase):
 def test_p1000_exception_and_scratch_drift(self):
  data=json.loads((ROOT/'research/analysis/battery-ratios.json').read_text())
  self.assertEqual([r['mwhPerDryT'] for r in data['classes'].values()],[.2,.12,.2])
  self.assertAlmostEqual(data['classes']['P1000']['referencePackPctOfDry'],80.53691275167785)
  self.assertTrue(all(r['completeFloorOverBy']>1 for r in data['classes'].values()))
  with tempfile.TemporaryDirectory(dir=os.environ['TMPDIR']) as td:
   tree=Path(td);shutil.copytree(ROOT/'sim',tree/'sim')
   for file in ['research/analysis/battery-ratios.mjs','research/analysis/battery-ratios.json',
                'research/analysis/mass-budget.json','research/notes/chin-2021-battery-cell-to-pack.md','docs/OPEN-QUESTIONS.md','research/reports/02-paper.md','research/sources.json']:
    target=tree/file;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy(ROOT/file,target)
   command=['node','research/analysis/battery-ratios.mjs','--check']
   for label,file in [('false universal ratio','research/analysis/battery-ratios.json'),('changed capacity','sim/config.js'),('stale paper','research/reports/02-paper.md'),('stale source catalogue','research/sources.json')]:
    target=tree/file;original=target.read_text()
    if file.endswith('config.js'): changed=original.replace('battMWh: 120,','battMWh: 200,')
    elif file.endswith('battery-ratios.json'): changed=original.replace('"mwhPerDryT": 0.12','"mwhPerDryT": 0.2')
    else: changed=original.replace('0.12','0.20')
    target.write_text(changed)
    red=subprocess.run(command,cwd=tree,capture_output=True,text=True)
    self.assertNotEqual(red.returncode,0,red.stdout+red.stderr)
    target.write_text(original)
    green=subprocess.run(command,cwd=tree,capture_output=True,text=True)
    self.assertEqual(green.returncode,0,green.stdout+green.stderr)
    print(label+': RED; corrected copy GREEN')
