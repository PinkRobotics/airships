/* One model: force-closure regressions plus plan/state and electrical ledger parity. */
import './energy-closure.cases.js';
import './energy-force.cases.js';
import './energy-profile.cases.js';
import './energy-assumptions.cases.js';
import './energy-planner.cases.js';
import {describe,it,ok,close,eq,deepEq} from '../harness.js';
import {CFG,WORK_ALT_MSL,ledger,CLASSES,CLASS_ORDER,MODES,PHASES,drawAt,planCycle,integrateCycle,inducedMW,diskMW,stateAt} from '../../sim/index.js?v=acbad6ee';
describe('one energy record',()=>{
  it('plan equals a finer independent phase integral on both bases',()=>{
    for(const c of Object.values(CLASSES))for(const basis of ['record','favourable']){
      const p=planCycle(c,MODES.balanced,15,null,{basis});let energy=0;
      for(const [id]of PHASES)for(let i=0;i<4000;i++){
        const s=drawAt(c,MODES.balanced,p,id,(i+.5)/4000);
        energy+=(Object.values(s.draw).reduce((a,b)=>a+b,0)-(s.gen.regen||0))*p.dur[id]/60/4000;
      }
      close(energy/p.eCycleMWh,1,.005,c.id+basis);
    }
  });
  it('stateAt uses the same draw and generation at 9000 instants',()=>{
    for(const c of Object.values(CLASSES))for(const mode of Object.values(MODES)){
      const plan=planCycle(c,mode,15),m={cls:c,mode,plan,offset:0,legKm:15,oneWayKm:15,fire:{id:'ENERGY',ll:[-120.05,50.05]},intake:[-120.3,50],delivery:[-120.05,50.05],cycleSec:plan.cycleMin*60,phaseEnds:[]};
      let t=0;for(const [id]of PHASES){t+=plan.dur[id]*60;m.phaseEnds.push(t);}
      for(let i=0;i<1000;i++){const s=stateAt(m,m.cycleSec*(i+.5)/1000),d=drawAt(c,mode,plan,s.phase,s.prog);deepEq(s.draw,d.draw);deepEq(s.gen,d.gen);}
    }
  });
  it('Glauert reduces to hover and satisfies the oblique-flow identity',()=>{
    for(const c of Object.values(CLASSES)){
      const T=c.payloadT*9810*.1;eq(inducedMW(c,T),diskMW(c,T));
      for(const [V,vc]of [[36,0],[7.5,2],[0,3]]){
        const P=inducedMW(c,T,V,vc),vi=P*1e6*CFG.propEta/T-vc;
        close(vi*Math.sqrt(V*V+(vc+vi)**2)/(T/(2*ledger(c,WORK_ALT_MSL).rho*c.diskM2)),1,1e-9);
      }
    }
  });
});
