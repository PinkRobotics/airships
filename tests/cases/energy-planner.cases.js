import {describe,it,close,ok,eq} from '../harness.js';
import {CLASSES,MODES,PHASES,planCycle,drawAt} from '../../sim/index.js?v=059cbc27';
describe('moving-phase time dilation',()=>{
  it('time dilation scales vertical rates without changing altitude or clearance',()=>{
    for(const c of Object.values(CLASSES))for(const km of [5,15,60])for(const k of [.5,.75]){
      const a=planCycle(c,MODES.balanced,km),b=planCycle(c,MODES.balanced,km,null,{movingPhaseRateMultiplier:k});
      let total=0;
      for(const [id] of PHASES){
        close(b.dur[id],a.dur[id]/(id==='WATER_FILL'?1:k),1e-10,'phase duration');total+=b.dur[id];
        for(let i=0;i<=100;i++){
          const x=drawAt(c,MODES.balanced,a,id,i/100),y=drawAt(c,MODES.balanced,b,id,i/100);
          close(y.alt,x.alt,1e-8,'same altitude');close(y.vz,k*x.vz,1e-8,'rate scaled');
        }
      }
      close(b.cycleMin,total,1e-9);ok(b.cycleMin>a.cycleMin);eq(b.deliveredT,a.deliveredT);
    }
  });
});
