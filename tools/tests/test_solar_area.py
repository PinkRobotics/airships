"""Changing a hull dimension changes its projected collector, without editing a rate."""
import json
from pathlib import Path
import subprocess
import unittest
ROOT=Path(__file__).resolve().parents[2]
class SolarArea(unittest.TestCase):
 def test_geometry_and_resize(self):
  code="""
import {CLASSES,SOLAR_PROJECTED_FRACTION,aeroGeometry} from './sim/index.js';
const out=[];
for(const [id,c] of Object.entries(CLASSES)){
 const initial=c.solarM2,oldLength=c.lenM;c.lenM*=1.25;
 out.push({id,initial,changed:c.solarM2,expected:SOLAR_PROJECTED_FRACTION*aeroGeometry(c).areaM2});
 c.lenM=oldLength;
}
console.log(JSON.stringify(out));
"""
  rows=json.loads(subprocess.check_output(['node','--input-type=module','-e',code],cwd=ROOT,text=True))
  for r in rows:
   self.assertGreater(r['changed'],r['initial'])
   self.assertAlmostEqual(r['changed'],r['expected'],places=8)
  print('all three collectors follow a changed hull dimension at the fixed coverage assumption')
