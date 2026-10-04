/* Independent force audit adapted from gpt-6-sol's implementation.
 * The equations use observed state and class geometry, without the model's force helpers. */
import {describe,it,ok,close,eq} from '../harness.js';
import {CLASSES,MODES,PHASES,CFG,planCycle,drawAt} from '../../sim/index.js?v=182fd413';
const sum=o=>Object.values(o).reduce((a,b)=>a+b,0);
export function auditForce(c,p,s) {
  const target=s.led.liftT-s.massT, owned=sum(s.owners)+s.unheldT;
  const tolerance=1e-6*Math.max(1,Math.abs(target));
  close(target,owned,tolerance,'owner sum');
  if(s.airV===0)close(s.owners.aeroT,0,1e-12,'aero at zero airspeed');
  const area=Math.PI*(c.diaM/2)**2;
  const q=.5*s.led.rho*s.airV**2;
  const inducedN=q>0?(s.owners.aeroT*9810)**2/(q*Math.PI*c.diaM**2):0;
  const prop=(q*CFG.Cd*area+inducedN)*s.airV/CFG.propEta/1e6;
  close(s.draw.prop,prop,1e-7,'propulsion law');
  ok(sum(s.draw)<=s.busMW+1e-6,'whole bus');
  ok(s.owners.bagT>=0&&s.owners.bagT<=c.anchorBagT+tolerance,'bag limit');
  ok(s.owners.rotorT>=0&&s.owners.rotorT<=s.thrustLimitT+tolerance,'rotor limit');
  ok(s.owners.aeroT>=0&&s.owners.aeroT<=s.aeroLimitT+tolerance,'aero limit');
  if(p.basis==='record')eq(s.owners.aeroT,0,'record basis');
  eq(s.feasible,Math.abs(s.unheldT)<=tolerance&&sum(s.draw)<=s.busMW+1e-9,'verdict is the ledger');
  if(!s.feasible){ok(!p.feasible,'plan hid a force failure');ok(s.limits.length>0,'missing reason');}
}
describe('independent force and power equations',()=>{
  it('owners, zero-speed aero, propulsion and bus at 756 control points',()=>{
    let checked=0;
    for(const c of Object.values(CLASSES))for(const basis of ['record','favourable']){
      const p=planCycle(c,MODES.balanced,15,null,{basis});
      for(const [phase] of PHASES)for(let i=0;i<=20;i++){
        auditForce(c,p,drawAt(c,MODES.balanced,p,phase,i/20));checked++;
      }
    }
    eq(checked,756);
  });
});
