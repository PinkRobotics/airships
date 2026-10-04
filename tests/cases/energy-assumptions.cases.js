import {describe,it,eq,ok,close,throws} from '../harness.js';
import {CLASSES,MODES,CFG,planCycle,drawAt,rotorThrustLimitT,inducedMW} from '../../sim/index.js?v=68fef878';
describe('declared rotor assumptions',()=>{
  it('every class declares downward-only authority and leaves an upward need unheld',()=>{
    for(const c of Object.values(CLASSES))eq(c.reversibleThrust,false,c.id);
    const c=CLASSES.P100,p=planCycle(c,MODES.balanced,15,null,{basis:'favourable'});
    const s=drawAt(c,MODES.balanced,p,'OUTBOUND_TRANSIT',.224);
    ok(s.unheldT<0,'loaded climb needs upward authority');
    eq(s.owners.rotorT,0,'no upward rotor assigned');
    ok(s.limits.includes('upward authority unavailable'),'authority named');
  });
  it('efficiency is per plan and changes rotor pricing and thrust capacity together',()=>{
    const prior=CFG.propEta;
    for(const c of Object.values(CLASSES)){
      const lo=planCycle(c,MODES.balanced,60,null,{rotorEfficiency:.55});
      const hi=planCycle(c,MODES.balanced,60,null,{rotorEfficiency:.70});
      eq(lo.rotorEfficiency,.55);eq(hi.rotorEfficiency,.70);
      const a=drawAt(c,MODES.balanced,lo,'WATER_FILL',.5),b=drawAt(c,MODES.balanced,hi,'WATER_FILL',.5);
      close(rotorThrustLimitT(c,a.led.rho,.55)/rotorThrustLimitT(c,a.led.rho,.70),(.55/.70)**(2/3),1e-12);
      close(inducedMW(c,1e6,0,0,a.led.rho,.55)/inducedMW(c,1e6,0,0,a.led.rho,.70),.70/.55,1e-12);
      ok(a.thrustLimitT<b.thrustLimitT,'lower efficiency lowers available thrust');
    }
    eq(CFG.propEta,prior,'plan option did not edit configuration');
    throws(()=>planCycle(CLASSES.P100,MODES.balanced,15,null,{rotorEfficiency:0}));
  });
});
