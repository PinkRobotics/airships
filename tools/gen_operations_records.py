#!/usr/bin/env python3
"""Recapture existing route records with the repository's browser, server and model.

Only bundled exercise and dated capture views are loaded. No agency feed is fetched.
The energy diagnostics consume exact distances and accepted controls from these records.
"""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from serve import serve_tree
ROOT=Path(__file__).resolve().parents[1]
READY="""async function readyApp() {
  for(let i=0;i<1000 && (!window.AIRSHIPS?.app.ready || window.AIRSHIPS.app.planning?.state!=='settled');i++)
    await new Promise(r=>setTimeout(r,50));
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
def main():
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
            source='Local seed-7 captures of the shipped exercise and a dated replay; no emergency feed fetched.',
            routes=routes,captures=captures,
            method='Unique class and exact one-way distance pairs after all captured missions have accepted plans, with jitter pinned to seed 7; supplemented in the gate by every printed search distance and fleet-distance row.',
            missions=missions))
        output=td/'fleet.json'
        fleet_probe=td/'fleet-capture.js'
        fleet_probe.write_text('(async () => {'+READY+'await readyApp(); return '+
                               (ROOT/'research/analysis/energy-fleet-distances.js').read_text()+';})()')
        subprocess.run([sys.executable,'tools/js_eval.py',base+'index.html?seed=7&data=snapshot',
                        str(fleet_probe),str(output),'20'],cwd=ROOT,check=True)
        # This producer already owns the record's byte format (one-space indent).
        if '--check' in sys.argv:
            if (ROOT/'research/analysis/energy-fleet-distances.json').read_bytes()!=output.read_bytes():
                raise SystemExit('FAIL stale fleet-distance record')
        else:(ROOT/'research/analysis/energy-fleet-distances.json').write_bytes(output.read_bytes())
        print('Captured exact route controls and fleet distances with owned browser lifetimes')
if __name__=='__main__':main()
