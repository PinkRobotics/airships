/* Inventory the exact current inputs of printed energy and force tables.
 * Dated historical readings and the separate payload-exchange study have no
 * replayable current planCycle inputs and are explicitly outside this inventory. */
import fs from 'node:fs';
import {SERVED_CANDIDATES} from '../../sim/served-candidates.js';
import {CLASSES,DEFAULTS} from '../../sim/index.js';
export const canonical=x=>JSON.stringify(x,(_,v)=>v&&typeof v==='object'&&!Array.isArray(v)?Object.fromEntries(Object.entries(v).sort(([a],[b])=>a.localeCompare(b))):v);
export const profileKey=b=>canonical({class:b.class,km:b.km,mode:b.mode??'balanced',options:{basis:b.basis??'record',...b.options},...(b.config?{config:b.config}:{}),...(b.hardware?{hardware:b.hardware}:{}),...(b.drawOptions?{drawOptions:b.drawOptions}:{})});
export const prescribed=r=>({class:r.class,km:r.km,mode:'balanced',options:{basis:r.basis}});
export const documentSensitivity=(r,s)=>({...prescribed({class:'P10000',km:15,basis:r.basis}),
 ...(r.key in DEFAULTS?{config:{[r.key]:DEFAULTS[r.key]*s.multiplier}}:{hardware:{[r.key]:CLASSES.P10000[r.key]*s.multiplier}})});
export function printedProfiles(){
 const read=n=>JSON.parse(fs.readFileSync(`research/analysis/${n}.json`));
 const unique=new Map();
 const add=(input,population,location,pages)=>{
  input={class:input.class,km:input.km,basis:input.options?.basis??input.basis??'record',mode:input.mode??'balanced',options:{basis:input.basis??'record',...input.options},
   ...(input.config?{config:input.config}:{}),...(input.hardware?{hardware:input.hardware}:{}),...(input.drawOptions?{drawOptions:input.drawOptions}:{})};
  const key=profileKey(input),found=unique.get(key);
  const occurrence={profileSet:population,location,pages};
  if(found){found.occurrences.push(occurrence);return;}
  unique.set(key,{...input,profile:location,pages,occurrences:[occurrence]});
 };
 for(const name of ['energy-profiles','energy-feasible'])for(const [i,r] of read(name).rows.entries()){
  const pages=[`research/analysis/${name}.md`];
  add(prescribed(r),name,`${name} row ${i} asDrawn`,pages);
  for(const kind of ['best','fullDeliveryBest']){
   const b=r[kind];if(!b)continue;
   add(b,name,`${name} row ${i} ${kind}`,pages);
   for(const s of b.sensitivity??[])add({...b,options:{...b.options,[s.parameter]:s.value}},
    name+' coefficient sweeps',`${name} row ${i} ${kind} ${s.parameter}=${s.value}`,pages);
  }
 }
 for(const r of read('energy-requirements').rows){
  const base=prescribed(r),pages=['research/analysis/energy-requirements.md'];
  add(base,'requirements','prescribed requirement',pages);
  if(r.ballast.feasible)add({...base,options:{...base.options,ballastT:r.ballast.ballastT}},'requirements','retained-water requirement',pages);
  if(r.powerAndThrust.feasible)add({...base,options:{...base.options,requiredBatteryMW:r.powerAndThrust.requiredBatteryMW,requiredRotorT:r.powerAndThrust.requiredRotorT}},'requirements','power-and-thrust requirement (nominal class energy capacity)',pages);
  for(const s of r.dragSensitivity)add({...base,options:{...base.options,verticalCd:s.verticalCd}},'requirements drag sweeps','prescribed drag sweep',pages);
 }
 for(const r of read('energy-rotor-range').rows)add({...prescribed(r),options:{basis:r.basis,rotorEfficiency:r.rotorEfficiency}},'rotor range','prescribed rotor-efficiency sweep',['research/analysis/energy-requirements.md']);
 const doc=read('energy-documents');
 for(const r of [...doc.records,...doc.readmeExamples])add(prescribed(r),'document prescribed profiles','current prescribed document reading',['docs/ENERGY-MODEL-2026-10.md','docs/ENERGY-CLOSURE-2026-10.md','docs/PHYSICS.md','sim/README.md']);
 for(const r of doc.sensitivity)for(const s of r.rows)add(documentSensitivity(r,s),'document sensitivity','prescribed single-input sensitivity',['docs/PHYSICS.md']);
 // Enumerate the owning candidate/route inputs, not the previous force-table cache.
 // The necessary-energy producer precedes that table in the served chain.
 const source=f=>JSON.parse(fs.readFileSync(f));
 const printed=[...read('energy-profiles').rows,...read('energy-feasible').rows];
 const fleet=read('energy-fleet-distances').rows,routes=source('tests/energy/served-route-distances.json').routes;
 for(const [cid,candidates] of Object.entries(SERVED_CANDIDATES)){
  const distances=new Set(printed.filter(r=>r.class===cid).map(r=>r.km));
  for(const r of fleet)if(r.class===cid)distances.add(r.legKm);
  for(const r of routes)if(r.className===cid)distances.add(r.km);
  for(const c of candidates)distances.add(c.source.km);
  for(const [i,c] of candidates.entries())for(const km of [...distances].sort((a,b)=>a-b))for(const basis of ['record','favourable'])
   add({class:cid,km,mode:c.controls.mode,options:{...c.controls.options,basis}},'served-candidate force tables',`candidate ${i+1}`,
    ['docs/ENERGY-CLOSURE-2026-10.md']);
 }
 // Both bag interventions printed by the descent tables use the prescribed route.
 for(const cid of Object.keys(CLASSES))for(const basis of ['record','favourable']){
  const base=prescribed({class:cid,km:15,basis}),pages=['research/analysis/descent.md'];
  add(base,'descent','prescribed descent',pages);
  add({...base,hardware:{anchorBagT:0}},'descent','bag hardware removed',pages);
  add({...base,drawOptions:{anchorCredit:false}},'descent','same path with bag force credit disabled',pages);
 }
 if(fs.existsSync('research/analysis/energy-zero-sun.json'))for(const r of read('energy-zero-sun').rows){
  add(r.input,'zero-sunlight sensitivity','selected profile with averaged sunlight',['docs/ENERGY-CLOSURE-2026-10.md']);
  add({...r.input,config:{solarWPerM2:0}},'zero-sunlight sensitivity','same selected profile with zero sunlight',['docs/ENERGY-CLOSURE-2026-10.md']);
 }
 if(fs.existsSync('research/analysis/energy-report-percentages.json')){
  const r=read('energy-report-percentages').replay;
  add(r.input,'report bag replay','current report replay with bag',['research/reports/02-paper.md','research/reports/03-diligence.md']);
  add({...r.input,hardware:r.intervention.hardware},'report bag replay','current report replay without bag',['research/reports/02-paper.md','research/reports/03-diligence.md']);
 }
 return [...unique.values()].map(r=>({...r,pages:[...new Set(r.occurrences.flatMap(o=>o.pages))]}));
}
