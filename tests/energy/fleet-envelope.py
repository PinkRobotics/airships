#!/usr/bin/env python3
"""Exercise distance provenance, captured-day dispatch and cockpit grammar locally."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import importlib.util

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
from serve import serve_tree

PROBE = """(async () => {
  for(let i=0;i<1000 && (!window.AIRSHIPS?.app.ready || window.AIRSHIPS.app.planning?.state!=='settled');i++)
    await new Promise(r=>setTimeout(r,50));
  const S=window.AIRSHIPS?.app, checks=[];
  if(!S?.ready || S.planning?.state!=='settled') throw new Error('planning not settled');
  S.paused=true;
  const check=(name,pass,detail)=>checks.push({name,pass:!!pass,detail});
  if(S.exercise){
    const fitted=S.missions.every(m=>m.cls.id==='P10000'?m.fire.sizeHa>=3000:
      m.cls.id==='P1000'?m.fire.sizeHa>=300:m.fire.sizeHa<=5000);
    check('B exercise classes fit and never double up',fitted && S.missions.every(m=>m.planState==='ready') &&
      new Set(S.missions.map(m=>m.fire.id)).size===S.missions.length,
      {fitted,missions:S.missions.length,distinctFires:new Set(S.missions.map(m=>m.fire.id)).size});
    const code=await (await fetch('research/analysis/energy-fleet-distances.js')).text();
    const expected=await (await fetch('research/analysis/energy-fleet-distances.json')).json();
    const actual=await eval(code);
    check('A source regenerates exact record',JSON.stringify(actual)===JSON.stringify(expected),
      {source:actual.source,min:actual.min,median:actual.median,max:actual.max});
    check('A source pins exercise and seed',actual.capture?.view==='exercise' && actual.capture?.seed===7 &&
      actual.capture?.day===null && actual.capture?.query==='seed=7&view=exercise' &&
      actual.capture?.rerun==='python3 -B tools/gen_operations_records.py',actual.capture||actual.source);
    const saved=S.missions;
    try {
      for(const legs of [[1,1,2],[1,2],[1,1,1,1,2,3]]){
        S.missions=legs.map(legKm=>({idle:false,cls:{id:'P100'},legKm}));
        let reason='accepted';
        try{await eval(code);}catch(e){reason=e.message;}
        check('A degenerate set refused '+JSON.stringify(legs),reason.includes('FLEET_DISTANCE_SET_DEGENERATE'),reason);
      }
    } finally { S.missions=saved; }
    const index=S.missions.findIndex(m=>!m.idle && m.stations?.length===1);
    if(index>=0)window.APP.selRow(index);
    const words=document.getElementById('cpOps').textContent;
    check('C one station is singular',index>=0 && /1 hose station(?!s)/.test(words) && !/1 hose stations/.test(words),
      words.match(/[^·]*hose stations?/)?.[0]||'no one-station mission');
  }else{
    const ms=S.missions.filter(m=>!m.idle), standby=S.standby||[];
    check('B 21-ha fire receives one P100',S.day==='2026-10-01' && ms.length===1 &&
      ms[0].cls.id==='P100' && ms[0].fire.sizeHa===21,ms.map(m=>({class:m.cls.id,fire:m.fire.id,size:m.fire.sizeHa})));
    check('B all flown classes fit their bands',ms.every(m=>m.cls.id==='P10000'?m.fire.sizeHa>=3000:
      m.cls.id==='P1000'?m.fire.sizeHa>=300:m.fire.sizeHa<=5000),'P10000 >=3000; P1000 >=300; P100 <=5000 ha');
    check('B every unused hull stands by at base with visible reason',standby.length===15 &&
      new Set([...ms,...standby].map(m=>m.name)).size===16 && standby.every(m=>{
        const row=[...document.querySelectorAll('#roster [data-standby-hull]')].find(r=>r.dataset.standbyHull===m.name);
        return m.reason && m.location==='base' && row?.textContent.includes(m.reason) &&
          row.textContent.includes('standing by') && row.textContent.includes('at base');
      }),{standby:standby.length,listed:document.querySelectorAll('#roster [data-standby-hull]').length});
    const reasons=[...document.querySelectorAll('#roster [data-standby-hull] td:nth-child(2) small')];
    check('B standby reasons fit the panel',reasons.length===15 && reasons.every(el=>
      el.clientWidth>0 && el.scrollWidth<=el.clientWidth+1),
      reasons.map(el=>({width:el.clientWidth,contentWidth:el.scrollWidth,whiteSpace:getComputedStyle(el).whiteSpace})));
  }
  return checks;
})()"""

def main():
    failures = 0
    spec=importlib.util.spec_from_file_location('operations_records',ROOT/'tools/gen_operations_records.py')
    producer=importlib.util.module_from_spec(spec);spec.loader.exec_module(producer)
    reason='producer has no pinned-input check'
    if hasattr(producer,'verify_fleet_source'):
        name='data/season/2026.days.json'
        with tempfile.TemporaryDirectory(prefix='source-pin-',dir=os.environ['TMPDIR']) as tmp:
            p=Path(tmp)/name;p.parent.mkdir(parents=True)
            original=(ROOT/name).read_bytes();p.write_bytes(original)
            pins={name:producer.FLEET_INPUT_PINS[name]}
            producer.verify_fleet_source(Path(tmp),pins)
            d=json.loads(original);d['dates'].append('2026-10-02');p.write_text(json.dumps(d))
            try:producer.verify_fleet_source(Path(tmp),pins)
            except ValueError as e:reason=str(e)
    good='FLEET_DISTANCE_SOURCE_CHANGED' in reason
    print(('PASS' if good else 'FAIL')+' A added day refuses pinned source: '+reason,flush=True)
    failures+=not good
    if '--pins-only' in sys.argv:return int(bool(failures))
    with tempfile.TemporaryDirectory(prefix='fleet-envelope-', dir=os.environ['TMPDIR']) as td, serve_tree(ROOT) as base:
        script=Path(td)/'check.js'; script.write_text(PROBE)
        views=[('exercise','seed=7&view=exercise'),('day','seed=7&day=2026-10-01')]
        if '--wrap-only' in sys.argv:views=views[1:]
        for name,query in views:
            out=Path(td)/(name+'.json')
            subprocess.run([sys.executable,'tools/js_eval.py',base+'index.html?'+query,
                            str(script),str(out),'1'],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
            for row in json.loads(out.read_text()):
                if '--wrap-only' in sys.argv and row['name']!='B standby reasons fit the panel':continue
                print(('PASS' if row['pass'] else 'FAIL')+' '+row['name']+': '+json.dumps(row['detail']),flush=True)
                failures+=not row['pass']
    print(f'fleet-envelope: {failures} failures',flush=True)
    return int(bool(failures))

if __name__=='__main__':
    sys.exit(main())
