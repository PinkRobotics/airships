/* Conditional fixed-speed comparison; it does not replace the rotor model. */
import fs from 'node:fs';
import {pathToFileURL} from 'node:url';
import {S,profiles,replay,read,format,table,label} from './energy-rotor-common.mjs';
import {writeGenerated} from './energy-output.mjs';
import {ROTOR_POWER_SCOPE} from '../../sim/energy-label.js?v=01e992e3';
export {ROTOR_POWER_SCOPE};
export const COMPARISON_INPUTS={scope:'Reviewer’s stipulated sensitivity inputs, derived from the published CH-47D comparison family; not measured properties of these rotors.',
 source:'johnson-2017-ndarc-validation',locator:'December 2017 revision: Table 1, printed page 10; Tables 3a–b, printed pages 12–13',
 tipSpeedFtS:707,metresPerFoot:0.3048,solidity:0.0849,inducedFactor:1.15,basicMeanBladeDrag:0.0085,
 driveEfficiency:1,profileSpeedFactor:1};
export const POWER_SAMPLES=2000;
export function shaftPower(c,s){
 const k=COMPARISON_INPUTS,T=s.owners.rotorT*9810,vc=Math.max(0,-s.vz);
 const ideal=S.inducedMW(c,T,s.airV,vc,s.led.rho,1),mechanicalMW=T*vc/1e6;
 const inducedMW=k.inducedFactor*(ideal-mechanicalMW);
 const profileMW=s.led.rho*c.diskM2*(k.tipSpeedFtS*k.metresPerFoot)**3*k.solidity/8*k.basicMeanBladeDrag*k.profileSpeedFactor/1e6;
 return {mechanicalMW,inducedMW,profileMW,shaftMW:(mechanicalMW+inducedMW+profileMW)/k.driveEfficiency};
}
function acceptedProfiles(){
 const out=[],same=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 const file='tests/energy/served-route-distances.json';
 const data=JSON.parse(fs.readFileSync(file,'utf8'));
 for(const q of data.missions){
  const s=S.selectServedPlan(S.CLASSES[q.class],q.km,null,q.mode),{basis,...options}=s.options??{};
  if(s.state!=='ready'||s.mode!==q.mode||!same(options,q.options))throw Error('accepted served controls differ from their current selector: '+q.capture+'/'+q.mission);
  out.push({dataset:'accepted-served',class:q.class,km:q.km,basis:basis??'record',kind:'served',mode:q.mode,options:{basis:basis??'record',...q.options},capture:q.capture,mission:q.mission,provenance:file});
 }
 // Read the reviewer's reference-class water-access median from its accepted-plan record.
 const water=read('water-availability'),reference=water.classes.P100.acceptedPlans.medianByFire;
 if(reference.state==='ready'&&reference.feasible){
  const km=reference.km;
  if(km!==water.classes.P100.distanceKm.byFire.p50)throw Error('accepted reference median differs from its published distance record');
  for(const c of Object.values(S.CLASSES)){
   const s=S.selectServedPlan(c,km,null,'balanced');
   if(s.state==='ready'&&s.plan?.feasible)out.push({dataset:'served-reference-median',class:c.id,km,basis:s.options.basis??'record',kind:'served',mode:s.mode,options:s.options,provenance:'water-availability.json#classes.P100.acceptedPlans.medianByFire.km; current accepted selector at the reference-class water median'});
  }
 }
 // The allocator median is a separate published quantity; retain and label it separately.
 const distance=read('energy-feasible').distanceSelection;
 if(distance){
  const km=Number(distance.median.toFixed(2));
  for(const c of Object.values(S.CLASSES)){
   const s=S.selectServedPlan(c,km,null,'balanced');
   if(s.state==='ready'&&s.plan?.feasible)out.push({dataset:'served-median',class:c.id,km,basis:s.options.basis??'record',kind:'served',mode:s.mode,options:s.options,provenance:'energy-feasible.json#distanceSelection.median; current accepted served selector'});
  }
 }
 return out;
}
export function computePowerSensitivity(cases=null){
 return {scope:'Conditional comparison with favourable simplifications at published profiles’ fixed controls, with no re-search. It is not a bound, design or aircraft result. Original force allocation and priced independent-disk area stay; the negative-axial level-flight substitute stays. Rotor speed is fixed, drive efficiency and profile-speed factor are unity, and no stall, compressibility or accessory loss is assigned.',
  modelScope:ROTOR_POWER_SCOPE,inputs:COMPARISON_INPUTS,samplesPerPhase:POWER_SAMPLES,
  theory:{source:'johnson-2009-ndarc',locator:'sections 11-5 to 11-5.1, printed pages 95–96',method:'Mechanical axial power plus stipulated induced factor times ideal induced power plus blade profile power; the induced factor does not multiply mechanical power. Comparison total = original midpoint cycle effort minus finely sampled original rotor effort plus finely sampled comparison rotor demand.'},
  profiles:(cases??[...profiles({full:true}),...acceptedProfiles()]).map(q=>{
   const {c,m,p}=replay(q);let originalRotorMWh=0,comparisonRotorMWh=0,overdrawMinutes=0,peakOverdrawMW=0,lowThrust=null;
   for(const [phase] of S.PHASES){
    const dt=p.dur[phase]/60/POWER_SAMPLES;
    for(let i=0;i<POWER_SAMPLES;i++){
     const progress=(i+.5)/POWER_SAMPLES,s=S.drawAt(c,m,p,phase,progress),power=shaftPower(c,s);
     originalRotorMWh+=s.draw.rotors*dt;comparisonRotorMWh+=power.shaftMW*dt;
     const over=s.nonRotorMW+power.shaftMW-s.busMW;
     if(over>1e-6){overdrawMinutes+=dt*60;peakOverdrawMW=Math.max(peakOverdrawMW,over);}
     if(!lowThrust||s.owners.rotorT<lowThrust.rotorT)lowThrust={phase,progress,rotorT:s.owners.rotorT,originalMW:s.draw.rotors,comparisonMW:power.shaftMW,profileMW:power.profileMW};
    }
   }
   return {...q,baselineFeasible:p.feasible,originalTotalMWh:p.eCycleMWh,originalRotorMWh,comparisonRotorMWh,comparisonDemandMWh:p.eCycleMWh-originalRotorMWh+comparisonRotorMWh,overdrawMinutes,peakOverdrawMW,lowThrust};
  })};
}
export function powerTable(dataset){
 const data=read('energy-rotor-power'),k=data.inputs;
 let out='\n<!-- rotor:power:start -->\n\n## Separated rotor-power comparison\n\n'+data.modelScope+'\n\n'+data.scope+'\n\n';
 out+=`Stipulated sensitivity inputs: CH-47D-derived tip speed ${k.tipSpeedFtS} ft/s, solidity ${k.solidity}, induced factor ${k.inducedFactor} and basic mean blade drag coefficient ${k.basicMeanBladeDrag}; [Johnson’s NDARC validation](https://rotorcraft.arc.nasa.gov/ndarc/media/Files/reportsAndPapers/NDARC-results.pdf), ${k.locator}. These are not measured properties of these rotors. The unit drive efficiency and profile-speed factor are favourable stipulated simplifications. Theory: [NDARC](https://rotorcraft.arc.nasa.gov/ndarc/media/Files/reportsAndPapers/NDARC-NASA-TP-2009-215402.pdf), ${data.theory.locator}. ${data.theory.method} Sampling uses ${data.samplesPerPhase} midpoint intervals per phase.\n\n`;
 const rows=data.profiles.filter(q=>q.dataset===dataset||dataset==='energy-profiles'&&['accepted-served','served-median','served-reference-median'].includes(q.dataset));
 out+=table(['Fixed profile','Original supplied MWh','Comparison demand MWh','Change MWh','Sampled overdraw min','Provenance'],rows.map(q=>[label(q)+(q.capture?` / ${q.capture} mission ${q.mission}`:q.dataset==='served-median'?' / current rounded allocator median selection':q.dataset==='served-reference-median'?' / reference-class water median selection':''),format(q.originalTotalMWh,6),format(q.comparisonDemandMWh,6),format(q.comparisonDemandMWh-q.originalTotalMWh,6),format(q.overdrawMinutes,6),q.provenance??`${q.dataset}.json#rows / ${q.kind}`]));
 return out+'\nComparison demand is conditional demand on the original trace, not a reallocated or re-searched closing plan. Original figures on unsupported profiles remain clipped supplied effort. Rotor speed or pitch policy is an evaluator question, and neither this comparison nor a zero sampled overdraw validates an aircraft.\n\n<!-- rotor:power:end -->\n';
}
if(process.argv[1]&&pathToFileURL(process.argv[1]).href===import.meta.url){
 const data=computePowerSensitivity();
 writeGenerated('research/analysis/energy-rotor-power.json',JSON.stringify(data,null,2)+'\n');
 console.log(`PASS conditional rotor power: ${data.profiles.length} fixed profiles and accepted selections; ${process.argv.includes('--check')?'record fresh':'record written'}`);
}
