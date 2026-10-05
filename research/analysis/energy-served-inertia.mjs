/* Diagnostic only: omitted vertical inertia at every published/captured route.
 * It does not add a force owner or change a selector verdict. */
import fs from 'node:fs';
import {CLASSES,MODES,PHASES,planCycle,drawAt,cycleGeometry,selectServedPlan} from '../../sim/index.js?v=ae2bcece';
import {SERVED_CANDIDATES} from '../../sim/served-candidates.js?v=ae2bcece';
import {omittedInertia,ADDED_MASS_VALUES,GAP_CUTOFF_T,AUTHORITY_METHOD,WITHDRAWN_METHOD} from './energy-motion.mjs';
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
  rows.push({class:cid,candidate,km,basis,controls,feasible:p.feasible,...omittedInertia(c,m,p)});
 }
}
const same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
const servedMissions=read('tests/energy/served-route-distances.json').missions.map(m=>{
 const selection=selectServedPlan(CLASSES[m.class],m.km,null,m.mode);
 const {basis,...options}=selection.options??{};
 if(selection.state!=='ready'||selection.mode!==m.mode||!same(options,m.options))throw new Error('captured served mission no longer matches the selector: '+m.capture+'/'+m.mission);
 const row=rows.find(r=>r.class===m.class&&r.km===m.km&&r.basis==='record'&&r.controls.mode===m.mode&&same(r.controls.options,m.options));
 if(!row)throw new Error('served mission lacks candidate inertia replay');
 return {...m,candidate:row.candidate,peak:row.peak,phases:row.phases,worstSignedGaps:row.worstSignedGaps,withdrawnAbsoluteGaps:row.withdrawnAbsoluteGaps,qualification:row.qualification};
});
const source={title:'Munk, The Aerodynamic Forces on Airship Hulls, NACA Report 184 (1924)',url:'https://ntrs.nasa.gov/citations/19930091249',page:'printed page 20, table; PDF page 21',transverseCoefficientAtLengthDiameter2:0.702};
const flagged=(r,field,j)=>j===undefined?r[field].some(q=>q.gapT>GAP_CUTOFF_T):r[field][j].gapT>GAP_CUTOFF_T;
const count=all=>{
 const feasible=all.filter(r=>r.feasible!==false);
 return {cases:all.length,quasiStaticFeasible:feasible.length,
  signed:feasible.filter(r=>flagged(r,'worstSignedGaps')).length,
  withdrawnAbsolute:feasible.filter(r=>flagged(r,'withdrawnAbsoluteGaps')).length,
  signedOnly:feasible.filter(r=>flagged(r,'worstSignedGaps')&&!flagged(r,'withdrawnAbsoluteGaps')).length,
  absoluteOnly:feasible.filter(r=>!flagged(r,'worstSignedGaps')&&flagged(r,'withdrawnAbsoluteGaps')).length,
  byCoefficient:ADDED_MASS_VALUES.map((coefficient,j)=>({coefficient,
   signed:feasible.filter(r=>flagged(r,'worstSignedGaps',j)).length,
   withdrawnAbsolute:feasible.filter(r=>flagged(r,'withdrawnAbsoluteGaps',j)).length}))};
};
const result={source,samplesPerPhase:2001,coefficients:ADDED_MASS_VALUES,
 method:'Central second difference of altitude with progress step 0.0001, clamped inside each phase at its endpoints. Peak means largest absolute vertical acceleration; signed rotor demand is checked at every sampled instant.',
 mass:'Hull dry-mass target plus water and nitrogen aboard; added mass is coefficient times local displaced-air mass. The 0.70 and 1.00 coefficients are a sensitivity pair, not measured capsule values. Hull-only: hanging-bag, actuator and controller dynamics are excluded.',
 authority:AUTHORITY_METHOD,withdrawnMeasurement:WITHDRAWN_METHOD,
 summary:{candidates:count(rows),capturedMissions:count(servedMissions)},servedMissions,rows};
writeGenerated('research/analysis/energy-served-inertia.json',JSON.stringify(result,null,2)+'\n');
console.log('Served-candidate signed inertia: '+JSON.stringify(result.summary)+'; verdicts unchanged');
