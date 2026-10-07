/* A path check independent of the force allocation. */
import {describe,it,ok,close} from '../harness.js';
import {CLASSES,MODES,PHASES,planCycle,drawAt,cycleGeometry,altAt} from '../../sim/index.js?v=31a23fa3';
import {SERVED_CANDIDATES} from '../../sim/served-candidates.js?v=31a23fa3';
const load=async name=>{
 const url=new URL('../../'+name,import.meta.url);
 return typeof process!=='undefined'&&process.versions?.node
  ? JSON.parse(await (await import('node:fs/promises')).readFile(url,'utf8'))
  : (await fetch(url)).json();
};
const [profiles,feasible,requirements,fleet,routes]=await Promise.all(['research/analysis/energy-profiles.json','research/analysis/energy-feasible.json','research/analysis/energy-requirements.json','research/analysis/energy-fleet-distances.json','tests/energy/served-route-distances.json'].map(load));
export function largestVelocityStep(c,m,p) {
  let worst={dvz:0}, previous=null;
  const g=cycleGeometry(c,p);
  for(const [phase] of PHASES){
    if(!(p.dur[phase]>0))continue;
    for(let i=0;i<=2000;i++){
      const x=i/2000, s=drawAt(c,m,p,phase,x);
      if(previous){
        const dvz=Math.abs(s.vz-previous.vz);
        if(dvz>worst.dvz)worst={dvz,phase,x,previousPhase:previous.phase};
        if(i===0)close(altAt(g,p,phase,0),previous.alt,1e-9,'continuous altitude at seam');
      }
      previous={phase,vz:s.vz,alt:s.alt};
    }
  }
  const start=drawAt(c,m,p,'SOURCE_APPROACH',0);
  if(previous)worst= Math.abs(start.vz-previous.vz)>worst.dvz ? {dvz:Math.abs(start.vz-previous.vz),phase:'cycle seam'} : worst;
  return worst;
}
describe('smooth prescribed vertical motion',()=>{
  it('2001 samples per phase, every seam, baseline and retained-water profiles',()=>{
    let worst={dvz:0};
    for(const c of Object.values(CLASSES))for(const m of Object.values(MODES))for(const km of [5,15,60])for(const fraction of [0,.9,.99]){
      const p=planCycle(c,m,km,null,{ballastT:c.payloadT*fraction});
      const got=largestVelocityStep(c,m,p);
      if(got.dvz>worst.dvz)worst={...got,class:c.id,mode:m.id,km,fraction};
    }
    ok(worst.dvz<=.1,JSON.stringify(worst));
  });
});

describe('smooth printed and served vertical motion',()=>{
 it('every printed feasible row and candidate at each printed or captured route distance',()=>{
  let count=0,worst={dvz:0};
  const probe=(cid,km,mode,options,source)=>{
   const c=CLASSES[cid],m=MODES[mode],p=planCycle(c,m,km,null,options);
   if(!p.feasible)return;
   count++;const got=largestVelocityStep(c,m,p);
   if(got.dvz>worst.dvz)worst={...got,class:cid,km,mode,options,source};
   ok(got.dvz<=.1,JSON.stringify({class:cid,km,mode,options,source,...got}));
  };
  // Keep the reproduced row even if a later search chooses different controls.
  probe('P100',2.55029,'rapid',{basis:'favourable',speedMultiplier:1,ballastT:50},'reproduced E11 row');
  for(const data of [profiles,feasible])for(const r of data.rows){
   probe(r.class,r.km,'balanced',{basis:r.basis},'printed as drawn');
   for(const b of [r.best,r.fullDeliveryBest].filter(Boolean))probe(r.class,r.km,b.mode,b.options,'printed selected profile');
  }
  for(const r of requirements.rows){
   if(r.ballast.feasible)probe(r.class,r.km,'balanced',{basis:r.basis,ballastT:r.ballast.ballastT},'printed ballast requirement');
   const q=r.powerAndThrust;
   if(q.feasible)probe(r.class,r.km,'balanced',{basis:r.basis,requiredBatteryMW:q.requiredBatteryMW,requiredRotorT:q.requiredRotorT},'printed power and thrust requirement');
  }
  for(const [cid,candidates] of Object.entries(SERVED_CANDIDATES)){
   const distances=new Set([...profiles.rows,...feasible.rows].filter(r=>r.class===cid).map(r=>r.km));
   for(const r of fleet.rows)if(r.class===cid)distances.add(r.legKm);
   for(const r of routes.routes)if(r.className===cid)distances.add(r.km);
   for(const candidate of candidates){
    distances.add(candidate.source.km);
    for(const km of distances)for(const basis of ['record','favourable'])probe(cid,km,candidate.controls.mode,{...candidate.controls.options,basis},'served candidate');
   }
  }
  ok(profiles.rows.length===12&&feasible.rows.length===6*feasible.distances.length&&requirements.rows.length===12,'complete printed row sets');
  ok(count>0,'printed and served cases were exercised');
  console.log(`E11 printed and served replay: ${count} feasible cases; largest step ${worst.dvz.toFixed(9)} m/s ${worst.class}/${worst.km}/${worst.mode}/${worst.phase}`);
 });
});
