/* Diagnostic only: omitted vertical inertia at every published/captured route.
 * It does not add a force owner or change a selector verdict. */
import fs from 'node:fs';
import {CLASSES,MODES,PHASES,planCycle,drawAt,cycleGeometry,selectServedPlan} from '../../sim/index.js?v=182fd413';
import {SERVED_CANDIDATES} from '../../sim/served-candidates.js?v=182fd413';
import {accelerationAt,rotorMarginT,ADDED_MASS_VALUES} from './energy-motion.mjs';
import {writeGenerated} from './energy-output.mjs';
const read=f=>JSON.parse(fs.readFileSync(f,'utf8'));
const printed=[...read('research/analysis/energy-profiles.json').rows,...read('research/analysis/energy-feasible.json').rows];
const fleet=read('research/analysis/energy-fleet-distances.json').rows,routes=read('tests/energy/served-route-distances.json').routes;
const rows=[];
for(const [cid,candidates] of Object.entries(SERVED_CANDIDATES)){
 const distances=new Set(printed.filter(r=>r.class===cid).map(r=>r.km));
 for(const r of fleet)if(r.class===cid)distances.add(r.legKm);
 for(const r of routes)if(r.className===cid)distances.add(r.km);
 for(const candidate of candidates)distances.add(candidate.source.km);
 for(let candidate=0;candidate<candidates.length;candidate++)for(const km of [...distances].sort((a,b)=>a-b))for(const basis of ['record','favourable']){
  const controls=candidates[candidate].controls,c=CLASSES[cid],m=MODES[controls.mode];
  const p=planCycle(c,m,km,null,{...controls.options,basis}),g=cycleGeometry(c,p);
  let peak=null;const gaps=ADDED_MASS_VALUES.map(coefficient=>({coefficient,gapT:0}));
  for(const [phase] of PHASES)for(let i=0;i<=2000;i++){
   if(!(p.dur[phase]>0))continue;
   const x=i/2000,s=drawAt(c,m,p,phase,x),acceleration=accelerationAt(g,p,phase,x),marginT=rotorMarginT(c,p,s);
   const forces=ADDED_MASS_VALUES.map(coefficient=>({coefficient,addedMassT:coefficient*s.led.liftT,forceT:(s.massT+coefficient*s.led.liftT)*acceleration/9.81}));
   if(!peak||Math.abs(acceleration)>Math.abs(peak.accelerationMps2))peak={phase,progress:x,accelerationMps2:acceleration,onboardMassT:s.massT,marginT,forces};
   for(let j=0;j<gaps.length;j++)if(Math.abs(forces[j].forceT)-marginT>gaps[j].gapT)gaps[j]={coefficient:forces[j].coefficient,gapT:Math.abs(forces[j].forceT)-marginT,phase,progress:x,forceT:forces[j].forceT,marginT};
  }
  rows.push({class:cid,candidate,km,basis,controls,feasible:p.feasible,peak,worstMarginGaps:gaps});
 }
}
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const servedMissions=read('tests/energy/served-route-distances.json').missions.map(m=>{
 const selection=selectServedPlan(CLASSES[m.class],m.km,null,m.mode);
 const {basis,...options}=selection.options??{};
 if(selection.state!=='ready'||selection.mode!==m.mode||!same(options,m.options))throw new Error('captured served mission no longer matches the selector: '+m.capture+'/'+m.mission);
 const row=rows.find(r=>r.class===m.class&&r.km===m.km&&r.basis==='record'&&r.controls.mode===m.mode&&same(r.controls.options,m.options));
 if(!row)throw new Error('served mission lacks candidate inertia replay');
 return {...m,candidate:row.candidate,peak:row.peak,worstMarginGaps:row.worstMarginGaps};
});
const source={title:'Munk, The Aerodynamic Forces on Airship Hulls, NACA Report 184 (1924)',url:'https://ntrs.nasa.gov/citations/19930091249',page:'printed page 20, table; PDF page 21',transverseCoefficientAtLengthDiameter2:0.702};
const result={source,samplesPerPhase:2001,coefficients:ADDED_MASS_VALUES,
 method:'Central second difference of altitude with progress step 0.0001, clamped inside each phase at its endpoints. Peak means largest absolute vertical acceleration; each coefficient also checks the force-minus-reserve gap at every sampled instant.',
 mass:'Hull dry-mass target plus water and nitrogen aboard; added mass is coefficient times local displaced-air mass. The 0.70 coefficient rounds the source’s 0.702 prolate-spheroid value at length/diameter 2; 1.0 is a sensitivity assumption. Hull and hanging-bag dynamics are unvalidated.',
 margin:'Additional downward rotor thrust at the same instant with aerodynamic force and other loads fixed; absolute inertial force is compared conservatively. This is a sampled diagnostic of the quasi-static omission, not an inertial closure or a changed verdict.',servedMissions,rows};
const outputs={'research/analysis/energy-served-inertia.json':JSON.stringify(result,null,2)+'\n'};
for(const [file,text] of Object.entries(outputs))writeGenerated(file,text);
if(!process.argv.includes('--emit'))console.log(`Served-candidate inertia: ${rows.length} exact-route cases; ${rows.filter(r=>r.feasible).length} quasi-static feasible; ${rows.filter(r=>r.feasible&&r.worstMarginGaps.some(g=>g.gapT>1e-6)).length} exceed sampled rotor reserve; verdicts unchanged`);
