#!/usr/bin/env python3
"""Recapture existing route records with the repository's browser, server and model.

Only bundled exercise and dated capture views are loaded. No agency feed is fetched.
The energy diagnostics consume exact distances and accepted controls from these records.
"""
import json
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from serve import serve_tree
ROOT=Path(__file__).resolve().parents[1]
# The exercise retains all-date guard context. An added capture must not silently
# alter the sampled scene; a deliberate repin and regeneration are required.
FLEET_INPUT_PINS={
 'data/exercise/exercise.json':'46a4ea516c46a083b3f38cff269da5157dd0737691b4a623cc37303e66b7db83',
 'data/season/2026.days.json':'62b43bdf43484c29e36fe9957a2005f4d20cf8273c86febfdf9f10498d80497e',
 'data/season/2026.guard.json':'803f6879c4aaad24865623a762250a39420da424811d41905a44d4b72f948626',
 'data/season/2026.json':'c71df207bbcec687a6c63e41a964a4ba941f450843540dfea2abb21b81771108',
 'data/season/2026.evac.json':'8c8318d86a467581d26f2ba5d9550e874f0bb9cc8efa4fc4be53e0118b4cecc3',
 'data/water-bc.json':'015fd2c383ef5d8a4ca409b209a76e6c6b5d78db847aa4ce0604542499775e05',
}
def verify_fleet_source(root=ROOT,pins=FLEET_INPUT_PINS):
    for rel,expected in pins.items():
        if hashlib.sha256((root/rel).read_bytes()).hexdigest()!=expected:
            raise ValueError('FLEET_DISTANCE_SOURCE_CHANGED: pinned input differs: '+rel)
READY="""async function readyApp() {
  // The page publishes readiness after boot; route planning yields between missions.
  // Navigation time is not proof of completion on a loaded hosted runner.
  const deadline = performance.now() + 180000;
  while (!(window.AIRSHIPS?.app?.ready && window.AIRSHIPS.app.planning?.state === 'settled')) {
    if (performance.now() >= deadline) throw new Error('fleet planning: readiness deadline exceeded (180 s)');
    await new Promise(resolve => setTimeout(resolve, 100));
  }

  const A=window.AIRSHIPS;
  if(!A?.app.ready || A.app.planning?.state!=='settled') throw new Error('planning did not settle');
  if(A.app.missions.some(m=>m.planState!=='ready')) throw new Error('captured mission has no accepted plan');
  return A;
}
"""
PROBE="(async () => {"+READY+"""
  const A=await readyApp();
  return A.app.missions.map((m,mission)=>{
    if(m.planState!=='ready') throw new Error('captured mission has no accepted plan: '+mission);
    A.sim.auditServedPlan(m.cls,m.legKm,m.wind,m.selection,m.mode.id);
    const {basis,...options}=m.selection.options;
    return {mission,class:m.cls.id,km:m.legKm,mode:m.selection.mode,options};
  });
})()"""
def write(rel,value):
    body=json.dumps(value,indent=2)+'\n';p=ROOT/rel
    if '--check' in sys.argv:
        if p.read_text()!=body:raise SystemExit('FAIL stale route record: '+rel)
    else:p.write_text(body)
    print(('Checked ' if '--check' in sys.argv else 'Generated ')+rel)
def render_fleet_note():
    import re
    fleet=json.loads((ROOT/'research/analysis/energy-fleet-distances.json').read_text())
    routes=json.loads((ROOT/'tests/energy/served-route-distances.json').read_text())
    code=(ROOT/'app/fleet.js').read_text()
    bands=re.findall(r"clsId === 'P10000' \? f.sizeHa >= (\d+) :\s*clsId === 'P1000' \? f.sizeHa >= (\d+) : f.sizeHa <= (\d+)",code)
    if len(bands)!=1:raise ValueError('Ambiguous fleet eligibility source')
    lines=['The printed distance set is the pinned invented exercise, with '
           +str(len(fleet['rows']))+' accepted hull legs. No captured incident day defines these quantiles.',
           '', '| Minimum km | Median km | Maximum km |', '|---|---|---|',
           '| '+' | '.join(f"{fleet[k]:.6f}" for k in ('min','median','max'))+' |', '',
           '| Class | Eligible incident area |', '|---|---|',
           '| P-10000 | at least '+bands[0][0]+' ha |',
           '| P-1000 | at least '+bands[0][1]+' ha |',
           '| P-100 | at most '+bands[0][2]+' ha |', '',
           'One hull is assigned per eligible fire. Unused hulls stand by at an unspecified base with their reason.',
           '', 'The diagnostic route capture contains '+str(len(routes['missions']))+
           ' accepted controls. Changing allocation changes this sample; it does not change nominal storage.',
           '', 'Source: `research/analysis/energy-fleet-distances.json`, '
           '`tests/energy/served-route-distances.json` and `app/fleet.js`. '
           'Generated and checked by `tools/gen_operations_records.py`.']
    name='research/analysis/fleet-envelope.md';p=ROOT/name;text=p.read_text()
    start='<!-- fleet-envelope:summary:start -->';end='<!-- fleet-envelope:summary:end -->'
    if text.count(start)!=1 or text.count(end)!=1:raise ValueError('Ambiguous fleet summary markers')
    lo=text.index(start)+len(start);hi=text.index(end,lo)
    result=text[:lo]+'\n'+'\n'.join(lines)+'\n'+text[hi:]
    return {name:result}

def write_fleet_note():
    for name,result in render_fleet_note().items():
        p=ROOT/name
        if '--check' in sys.argv:
            if result!=p.read_text():raise SystemExit('FAIL stale fleet envelope prose')
        else:p.write_text(result)
    print('Checked fleet envelope prose against current records' if '--check' in sys.argv else 'Generated fleet envelope prose from current records')

def main():
    verify_fleet_source()
    with tempfile.TemporaryDirectory(prefix='ops-',dir=os.environ['TMPDIR']) as td, serve_tree(ROOT) as base:
        td=Path(td);probe=td/'capture.js';probe.write_text(PROBE)
        captures=[];missions=[];routes=[];seen=set()
        for label,query,viewport,stem in [('exercise','?seed=7&view=exercise','390x844','exercise-390'),
                                        ('exercise','?seed=7&view=exercise',None,'exercise'),
                                        ('replay','?seed=7&day=2026-09-22',None,'replay')]:
            output=td/(stem+'.json');env=dict(os.environ)
            if viewport:env['A3D_VIEWPORT']=viewport
            else:env.pop('A3D_VIEWPORT',None)
            subprocess.run([sys.executable,'tools/js_eval.py',base+'index.html'+query,str(probe),str(output),'5'],cwd=ROOT,env=env,check=True)
            rows=json.loads(output.read_text());captures.append(dict(capture=stem+'.json',missions=len(rows)))
            if not viewport:missions += [dict(capture=label,**r) for r in rows]
            for r in rows:
                key=(r['class'],r['km'])
                if key not in seen:seen.add(key);routes.append(dict(className=r['class'],km=r['km']))
        write('tests/energy/served-route-distances.json',dict(
            source='Local captured route inputs from the shipped exercise and dated replay; current controls replayed through the served selector. No emergency feed fetched.',
            routes=routes,captures=captures,
            method='Unique class and exact one-way distance pairs after all captured missions have accepted plans, with jitter pinned to seed 7; supplemented in the gate by every printed search distance and fleet-distance row.',
            missions=missions))
        output=td/'fleet.json'
        fleet_probe=td/'fleet-capture.js'
        fleet_probe.write_text('(async () => {'+READY+'await readyApp(); return '+
                               (ROOT/'research/analysis/energy-fleet-distances.js').read_text()+';})()')
        exercise=json.loads((ROOT/'data/exercise/exercise.json').read_text())
        if exercise['seed']!=7:raise SystemExit('FLEET_DISTANCE_SOURCE_UNPINNED: bundled exercise seed is not 7')
        subprocess.run([sys.executable,'tools/js_eval.py',base+'index.html?seed=7&view=exercise',
                        str(fleet_probe),str(output),'20'],cwd=ROOT,check=True)
        # This producer already owns the record's byte format (one-space indent).
        if '--check' in sys.argv:
            if (ROOT/'research/analysis/energy-fleet-distances.json').read_bytes()!=output.read_bytes():
                raise SystemExit('FAIL stale fleet-distance record')
        else:(ROOT/'research/analysis/energy-fleet-distances.json').write_bytes(output.read_bytes())
        write_fleet_note()
        print('Captured exact route controls and fleet distances with owned browser lifetimes')
if __name__=='__main__':
    if '--emit' in sys.argv:print(json.dumps(render_fleet_note()))
    else:main()
