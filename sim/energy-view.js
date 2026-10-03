/* Page binders use the same plans and records as the simulation. */
import {planCycle} from './plan.js?v=eae942b2';
const comparisons=new WeakMap();
export const feasibilityText=p=>p.feasible?'closes in the quasi-static model':'does not close on the drawn hardware';
export function energyComparison(cls,mode,km,wind,record){
  if(comparisons.has(record))return comparisons.get(record);
  const favourable=planCycle(cls,mode,km,wind,{basis:'favourable',ballastT:record.retainedT,
    speedMultiplier:record.speedMultiplier,movingPhaseRateMultiplier:record.movingPhaseRateMultiplier,verticalProfile:record.profile?.parameters,
    rotorEfficiency:record.rotorEfficiency,verticalCd:record.verticalCd,clMax:record.clMax,
    requiredBatteryMW:record.requiredBatteryMW,requiredRotorT:record.requiredRotorT});
  const pair={record,favourable};comparisons.set(record,pair);return pair;
}
export function cycleEnergyText(pair){
  return [pair.record,pair.favourable].map(p=>`${p.eCycleMWh.toFixed(1)} MWh ${p.basis}: ${feasibilityText(p)}`).join(' · ');
}
