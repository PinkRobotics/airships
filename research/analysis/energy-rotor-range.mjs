/* Rotor efficiency is a plan option; no class or configuration is mutated. */
import fs from 'node:fs';
import {ROTOR_POWER_SCOPE} from '../../sim/energy-label.js';
import {CLASSES,MODES,PHASES,ROTOR_EFFICIENCY_VALUES,planCycle,drawAt} from '../../sim/index.js?v=31a23fa3';
const rows=[];
for(const c of Object.values(CLASSES))for(const km of [15,60])for(const basis of ['record','favourable'])for(const rotorEfficiency of ROTOR_EFFICIENCY_VALUES){
  const p=planCycle(c,MODES.balanced,km,null,{basis,rotorEfficiency});
  let thrustCapMinT=Infinity,thrustCapMaxT=0;
  for(const [id] of PHASES)for(let i=0;i<=1000;i++){
    const s=drawAt(c,MODES.balanced,p,id,i/1000);
    thrustCapMinT=Math.min(thrustCapMinT,s.thrustLimitT);thrustCapMaxT=Math.max(thrustCapMaxT,s.thrustLimitT);
  }
  rows.push({class:c.id,km,basis,rotorEfficiency,thrustCapMinT,thrustCapMaxT,feasible:p.feasible,worstUnheldT:p.worst.unheldT,cycleMWh:p.eCycleMWh});
}
fs.writeFileSync('research/analysis/energy-rotor-range.json',JSON.stringify({assumption:ROTOR_POWER_SCOPE,
 regimes:'Hold-down descent is priced as climb, on the conservative side; climb against hold-down thrust is priced as level flight, with no bound claimed.',rows},null,2)+'\n');
for(const r of rows)console.log(`${r.class}/${r.km}/${r.basis} eta=${r.rotorEfficiency.toFixed(2)} cap=${r.thrustCapMinT.toFixed(3)}..${r.thrustCapMaxT.toFixed(3)} t feasible=${r.feasible} unheld=${r.worstUnheldT.toFixed(3)} t`);
