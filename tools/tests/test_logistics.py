"""Plants in disposable JSON copies; never mutate the working tree."""
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


class LogisticsPlants(unittest.TestCase):
    def test_refused_rates_and_corrected_copies(self):
        script = """
import {CLASSES,MODES,planCycle} from './sim/index.js';
import {acceptedLogistics} from './research/analysis/accepted-logistics.js';
const row=acceptedLogistics(CLASSES.P100,4.71);
const refused=planCycle(CLASSES.P100,MODES.balanced,4.71,null,{basis:'record'});
console.log(JSON.stringify({cid:'P100',row,refused:{feasible:refused.feasible,tph:refused.tph}}));
"""
        original = json.loads(subprocess.check_output(
            ['node', '--input-type=module', '-e', script], cwd=ROOT, text=True))
        self.assertFalse(original['refused']['feasible'])
        self.assertTrue(original['row']['feasible'])
        plants = {
            'infeasible-plan-rate': dict(feasible=False, tph=original['refused']['tph']),
            'forged-accepted-rate': dict(tph=original['refused']['tph']),
            'stand-down-with-rate': dict(state='stand-down', feasible=False),
            'wrong-exact-input': dict(km=15),
        }
        with tempfile.TemporaryDirectory(prefix='logistics-plants-', dir=os.environ['TMPDIR']) as td:
            candidate = Path(td)/'row.json'
            def run(row):
                candidate.write_text(json.dumps(dict(cid='P100', row=row)))
                return subprocess.run(['node','tools/check_logistics.mjs','--row',str(candidate)],
                                      cwd=ROOT, capture_output=True, text=True)
            for name, changes in plants.items():
                with self.subTest(name=name):
                    result = run(dict(original['row'], **changes))
                    self.assertNotEqual(result.returncode, 0, result.stdout+result.stderr)
                    print(f'plant {name}: RED ({result.stderr.strip()})')
                    result = run(original['row'])
                    self.assertEqual(result.returncode, 0, result.stdout+result.stderr)
                    print(f'plant {name}: corrected accepted copy GREEN')
            # Invalid distance has no accepted plan and therefore no rate.
            inactive = json.loads(subprocess.check_output(['node','--input-type=module','-e',
                "import {CLASSES} from './sim/index.js'; import {acceptedLogistics} from './research/analysis/accepted-logistics.js'; console.log(JSON.stringify(acceptedLogistics(CLASSES.P100,0)));"], cwd=ROOT,text=True))
            self.assertIsNone(inactive['tph'])
            self.assertEqual(run(inactive).returncode, 0)
            inactive['tph'] = 1
            result=run(inactive)
            self.assertNotEqual(result.returncode, 0)
            print('plant unavailable-with-rate: RED ('+result.stderr.strip()+')')
            inactive['tph'] = None
            self.assertEqual(run(inactive).returncode, 0)
            print('plant unavailable-with-rate: corrected inactive copy GREEN')

    def test_inactive_examples_produce_no_quotients(self):
        import shutil
        with tempfile.TemporaryDirectory(prefix='inactive-logistics-', dir=os.environ['TMPDIR']) as td:
            tree=Path(td)
            shutil.copytree(ROOT/'sim',tree/'sim')
            for file in ['research/analysis/accepted-logistics.js','research/analysis/water-availability.json',
                         'research/analysis/delivery.py','research/figures.json','data/fire-history-bc.json',
                         'tools/gen_release_states.mjs','tools/gen_logistics_prose.py','research/analysis/water-availability.md',
                         'research/analysis/delivery.md','docs/OPEN-QUESTIONS.md','docs/VERIFICATION-PLAN.md']:
                target=tree/file;target.parent.mkdir(parents=True,exist_ok=True);shutil.copy(ROOT/file,target)
            config=tree/'sim/config.js';original=config.read_text()
            import re
            config.write_text(re.sub(r'\b(?:battMW|genMW):\s*\d+',lambda m:m[0].split(':')[0]+': 0',original))
            script="""
import fs from 'node:fs';
import {CLASSES} from './sim/index.js';
import {acceptedLogistics} from './research/analysis/accepted-logistics.js';
const file='research/analysis/water-availability.json',water=JSON.parse(fs.readFileSync(file));
for(const [cid,c] of Object.entries(water.classes)){
 const cls=CLASSES[cid];
 for(const name of ['workedExample','medianByFire','medianByHectare'])c.acceptedPlans[name]=acceptedLogistics(cls,c.acceptedPlans[name].km);
 if(c.acceptedPlans.workedExample.state==='ready')throw Error('zero-power plant still accepted');
 c.throughputTph=Object.fromEntries(Object.keys(c.throughputTph).map(k=>[k,null]));
 water.geometry[cid].drawTonnesPer12h=null;water.geometry[cid].drawdownMetresPer12hOnMinBody=null;
}
fs.writeFileSync(file,JSON.stringify(water));
"""
            subprocess.run(['node','--input-type=module','-e',script],cwd=tree,check=True,capture_output=True,text=True)
            run=subprocess.run(['python3','-B','research/analysis/delivery.py','--json','research/analysis/delivery.json'],cwd=tree,capture_output=True,text=True)
            self.assertEqual(run.returncode,0,run.stdout+run.stderr)
            result=json.loads((tree/'research/analysis/delivery.json').read_text())
            for row in result['classes'].values():
                self.assertIsNone(row['payloadT']);self.assertIsNone(row['releaseRateM3s'])
                self.assertIsNone(row['atRealMedianLeg']['tonnesPer24h'])
                self.assertTrue(all(value is None for value in row['coverageLevelBySwath'].values()))
            run=subprocess.run(['python3','-B','tools/gen_logistics_prose.py'],cwd=tree,capture_output=True,text=True)
            self.assertEqual(run.returncode,0,run.stdout+run.stderr)
            text=(tree/'research/analysis/delivery.md').read_text()
            self.assertIn('not served',text)
            print('zero installed propulsion power: inactive worked/median plans; no release, coverage or daily rate')
