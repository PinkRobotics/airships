/* A path check independent of the force allocation. */
import {describe,it,ok,close} from '../harness.js';
import {CLASSES,MODES,PHASES,planCycle,drawAt,cycleGeometry,altAt} from '../../sim/index.js?v=e6a94414';
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
