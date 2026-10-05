/* Hull-only sampled signed authority screen; no force owner or verdict is changed. */
import fs from 'node:fs';
import {CLASSES,MODES,PHASES,planCycle,drawAt,cycleGeometry,altAt,inducedMW} from '../../sim/index.js?v=fc85766f';
import {writeGenerated} from './energy-output.mjs';
export const ADDED_MASS_COEFFICIENT = 0.70;
export const ADDED_MASS_VALUES = [ADDED_MASS_COEFFICIENT, 1.0];
export const GAP_CUTOFF_T = 1e-6;
export const ADDED_MASS_SOURCE = {
  assumption:'Sensitivity pair for transverse translation of a horizontal capsule hull with length/diameter 2.',
  citation:'Munk, NACA Report 184 (1924), Table I, printed page 20 (PDF page 21): https://ntrs.nasa.gov/citations/19930091249.',
  primarySourceRead:true,
  localPrimarySource:false,
  localBackgroundSource:'research/papers/hochstetler-2016-heavy-lift-airships.pdf, pages 3 and 13',
  qualification:'The source gives 0.702 for a prolate spheroid at length/diameter 2. The rounded 0.70 and 1.00 are sensitivity assumptions, not measured capsule coefficients. A capsule on the same axes has about 25% more volume. Hanging-load, actuator and controller dynamics are excluded.'
};
export const AUTHORITY_METHOD = 'Upward acceleration is positive. I = (m_onboard + C * m_displaced_air) * a_z / g; T_required = T_quasi + unheld - I. Accept the sampled rotor demand only if 0 <= T_required <= T_available. Gap = max(0, -T_required, T_required - T_available). Aerodynamic force, bag support, drag and other electrical loads remain fixed. Buoyancy is already in the ledger; shedding hold-down is an upward increment, not new buoyancy.';
export const WITHDRAWN_METHOD = 'Dated measurement at landing 16, 2026-10-05: absolute inertial force minus the additional downward rotor reserve at the same samples and coefficients. Withdrawn because it misses upward authority that cannot be obtained by shedding the existing downward thrust. Recomputed here solely to preserve that measurement.';
// Keep the original central second difference and endpoint clamp.
export function accelerationAt(g,p,id,x) {
  const h=1e-4, z=Math.max(h,Math.min(1-h,x)), dt=h*p.dur[id]*60;
  return (altAt(g,p,id,z+h)-2*altAt(g,p,id,z)+altAt(g,p,id,z-h))/(dt*dt);
}
export function rotorAuthoritiesT(c,p,s) {
  const nonRotor=Object.values(s.draw).reduce((a,b)=>a+b,0)-s.draw.rotors;
  const power=Math.max(0,s.busMW-nonRotor);
  let lo=0,hi=s.thrustLimitT;
  for(let i=0;i<40;i++){
    const t=(lo+hi)/2;
    if(inducedMW(c,t*9810,s.airV,Math.max(0,-s.vz),s.led.rho,p.rotorEfficiency)>power)hi=t;else lo=t;
  }
  const shedT=s.owners.rotorT,downwardReserveT=Math.max(0,lo-shedT);
  return {upwardByRotorShedT:shedT,downwardReserveT,availableRotorT:shedT+downwardReserveT};
}
export function signedRotorDemand(s,accelerationMps2,coefficient,authority) {
  const addedMassT=coefficient*s.led.liftT;
  const forceT=(s.massT+addedMassT)*accelerationMps2/9.81;
  const requiredRotorT=s.owners.rotorT+s.unheldT-forceT;
  const gapT=Math.max(0,-requiredRotorT,requiredRotorT-authority.availableRotorT);
  return {coefficient,accelerationMps2,onboardMassT:s.massT,addedMassT,forceT,
    ...authority,unheldT:s.unheldT,requiredRotorT,gapT,
    direction:gapT<=GAP_CUTOFF_T?'none':requiredRotorT<0?'upward authority short':'downward authority short'};
}
export function omittedInertia(c,m,p,steps=2000) {
  const geometry=cycleGeometry(c,p),phases=[];
  const empty=()=>ADDED_MASS_VALUES.map(coefficient=>({coefficient,gapT:0}));
  const worstSignedGaps=empty(),withdrawnAbsoluteGaps=empty();let peak=null;
  for(const [phase] of PHASES){
    if(!(p.dur[phase]>0))continue;
    const signed=empty(),withdrawn=empty();let phasePeak=null;
    for(let i=0;i<=steps;i++){
      const progress=i/steps,s=drawAt(c,m,p,phase,progress),a=accelerationAt(geometry,p,phase,progress);
      const authority=rotorAuthoritiesT(c,p,s);
      const demands=ADDED_MASS_VALUES.map(C=>signedRotorDemand(s,a,C,authority));
      const instant={phase,progress,accelerationMps2:a,onboardMassT:s.massT,...authority,demands};
      if(!phasePeak||Math.abs(a)>Math.abs(phasePeak.accelerationMps2))phasePeak=instant;
      for(let j=0;j<demands.length;j++){
        const q={phase,progress,...demands[j]};
        if(!signed[j].phase||q.gapT>signed[j].gapT)signed[j]=q;
        const old={...q,gapT:Math.max(0,Math.abs(q.forceT)-authority.downwardReserveT)};
        if(!withdrawn[j].phase||old.gapT>withdrawn[j].gapT)withdrawn[j]=old;
      }
    }
    if(!peak||Math.abs(phasePeak.accelerationMps2)>Math.abs(peak.accelerationMps2))peak=phasePeak;
    for(let j=0;j<signed.length;j++){
      if(!worstSignedGaps[j].phase||signed[j].gapT>worstSignedGaps[j].gapT)worstSignedGaps[j]=signed[j];
      if(!withdrawnAbsoluteGaps[j].phase||withdrawn[j].gapT>withdrawnAbsoluteGaps[j].gapT)withdrawnAbsoluteGaps[j]=withdrawn[j];
    }
    phases.push({phase,peak:phasePeak,worstSignedGaps:signed,withdrawnAbsoluteGaps:withdrawn});
  }
  return {peak,phases,worstSignedGaps,withdrawnAbsoluteGaps,
    qualification:p.feasible?(worstSignedGaps.some(q=>q.gapT>GAP_CUTOFF_T)?'quasi-static closure; dynamic profile unresolved':'quasi-static closure; hull-only sampled screen does not validate dynamics'):'does not close on the drawn hardware'};
}
if(process.argv[1]?.endsWith('energy-motion.mjs')){
  const rows=[];
  for(const c of Object.values(CLASSES))for(const km of [15,60])for(const basis of ['record','favourable']){
    const p=planCycle(c,MODES.balanced,km,null,{basis});
    rows.push({class:c.id,km,basis,feasible:p.feasible,...omittedInertia(c,MODES.balanced,p)});
  }
  const result={source:ADDED_MASS_SOURCE,coefficients:ADDED_MASS_VALUES,samplesPerPhase:2001,
    authorityMeaning:AUTHORITY_METHOD,withdrawnMeasurement:WITHDRAWN_METHOD,
    massMeaning:'Hull dry-mass target, water and nitrogen aboard, plus coefficient times local displaced-air mass. Hull-only: hanging-bag dynamics are excluded.',rows};
  const json=JSON.stringify(result,null,2)+'\n';
  let md='# Hull-only signed vertical authority screen\n\n<!-- energy:motion:start -->\nGenerated by `node research/analysis/energy-motion.mjs`. No quasi-static verdict changes.\n\n';
  md+=`${ADDED_MASS_SOURCE.assumption} ${ADDED_MASS_SOURCE.citation} ${ADDED_MASS_SOURCE.qualification}\n\n${AUTHORITY_METHOD}\n\n${WITHDRAWN_METHOD}\n\n${result.massMeaning}\n\n`;
  md+='Each phase reports its largest signed gap at the original samples, including simultaneous authority in both directions. A gap-free sample is not dynamic validation.\n\n';
  md+='| Class | km | Basis | Phase | C | Gap tf | Direction | Required rotor tf | Shed tf | Downward reserve tf | Acceleration m/s² | Withdrawn absolute gap tf |\n|---|---:|---|---|---:|---:|---|---:|---:|---:|---:|---:|\n';
  for(const r of rows)for(const phase of r.phases)for(const [j,q] of phase.worstSignedGaps.entries())md+=`| ${r.class} | ${r.km} | ${r.basis} | ${phase.phase} | ${q.coefficient.toFixed(2)} | ${q.gapT.toFixed(3)} | ${q.direction} | ${q.requiredRotorT.toFixed(3)} | ${q.upwardByRotorShedT.toFixed(3)} | ${q.downwardReserveT.toFixed(3)} | ${q.accelerationMps2.toFixed(6)} | ${phase.withdrawnAbsoluteGaps[j].gapT.toFixed(3)} |\n`;
  md+='\n<!-- energy:motion:end -->\n';
  if(process.argv.includes('--emit')){
    console.log(JSON.stringify({'research/analysis/energy-motion.json':json,'research/analysis/energy-motion.md':md}));
  }else{
    writeGenerated('research/analysis/energy-motion.json',json);
    writeGenerated('research/analysis/energy-motion.md',md);
    console.log('Generated hull-only signed authority screen: '+rows.length+' prescribed profiles');
  }
}
