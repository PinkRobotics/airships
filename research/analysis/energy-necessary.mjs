/* Necessary stored-energy accounting only; never used by the plan selector. */
import fs from 'node:fs';
import {CLASSES,MODES,PHASES,planCycle,drawAt,selectServedPlan} from '../../sim/index.js?v=01e992e3';
import {writeGenerated} from './energy-output.mjs';
import {printedProfiles,profileKey} from './energy-printed-profiles.mjs';
import {CFG,setConfig} from '../../sim/index.js?v=01e992e3';
export const NECESSARY_ENERGY_SCOPE='Ideal, lossless chronological accounting with nominal class storage fully usable and the plan initial nitrogen inventory charged. No losses, health, state-of-charge window, reserve, external recharge or thermal limit. This is not an endurance rule, a mission-completion verdict or a battery model. Solar and nitrogen recovery are the existing bus inputs, not a promised recharge system.';
export function necessaryEnergy(c,m,p,steps=2000,drawOptions={}){
 let cumulativeDrawMWh=0,elapsedMin=0,maximumDrawMWh=0,minimumDrawMWh=0,emptyAtMin=null;
 const phases=[];
 for(const [phase] of PHASES){
  if(!(p.dur[phase]>0))continue;
  const begin=cumulativeDrawMWh,dtHours=p.dur[phase]/60/steps;
  for(let i=0;i<steps;i++){
   const powerMW=drawAt(c,m,p,phase,(i+.5)/steps,drawOptions).electrical.batteryPowerMW;
   const drawMWh=powerMW*dtHours;
   if(emptyAtMin===null&&cumulativeDrawMWh<=c.battMWh&&cumulativeDrawMWh+drawMWh>c.battMWh)
    emptyAtMin=elapsedMin+(c.battMWh-cumulativeDrawMWh)/powerMW*60;
   cumulativeDrawMWh+=drawMWh;
   maximumDrawMWh=Math.max(maximumDrawMWh,cumulativeDrawMWh);
   minimumDrawMWh=Math.min(minimumDrawMWh,cumulativeDrawMWh);
   elapsedMin+=dtHours*60;
  }
  phases.push({phase,startMin:elapsedMin-p.dur[phase],endMin:elapsedMin,
   phaseDrawMWh:cumulativeDrawMWh-begin,cumulativeDrawMWh,remainingNominalMWh:c.battMWh-cumulativeDrawMWh});
 }
 return {samplesPerPhase:steps,nominalStorageMWh:c.battMWh,cumulativeDrawMWh,maximumDrawMWh,minimumDrawMWh,
  emptyAtMin,shortageMWh:Math.max(0,maximumDrawMWh-c.battMWh),phases};
}
export function necessaryEnergyRecord(input){
 const prior={...CFG};
 try {
  if(input.config)setConfig(input.config);
  const c=input.hardware?{...CLASSES[input.class],...input.hardware}:CLASSES[input.class],m=MODES[input.mode];
  const p=planCycle(c,m,input.km,null,input.options);
  return {...input,quasiStaticFeasible:input.drawOptions?null:p.feasible,forceVerdictNote:input.drawOptions?'Force verdict not replayed for disabled-credit supplied-effort diagnostic':null,cycleMin:p.cycleMin,suppliedMWh:p.eCycleMWh,deliveredT:p.deliveredT,retainedT:p.retainedT,operatingMargins:p.operatingMargins,initialNitrogenT:p.ln2MakeT,
   accounting:necessaryEnergy(c,m,p,2000,input.drawOptions)};
 } finally { setConfig(prior); }
}
export function generateNecessaryEnergy(){
 const read=f=>JSON.parse(fs.readFileSync(f));
 const servedMissions=read('tests/energy/served-route-distances.json').missions.map(r=>necessaryEnergyRecord({
  ...r,options:{...r.options,basis:'record'},pages:['index.html']}));
 const inputs=printedProfiles();
 const routes=inputs.map(necessaryEnergyRecord);
 const profiles=read('research/analysis/energy-profiles.json').rows;
 const p100=profiles.find(r=>r.class==='P100'&&r.km===15&&r.basis==='record').best;
 const pairedP100=necessaryEnergyRecord({class:'P100',km:15,basis:'favourable',mode:p100.mode,
  options:{...p100.options,basis:'favourable'},profile:'paired record controls',
  pages:['index.html','concept/index.html'],location:'paired-energy and worked-record'});
 if(!routes.some(r=>profileKey(r)===profileKey(pairedP100)))routes.push(pairedP100);
 // An existing ready-selector counterexample, shown explicitly on the diagnostic page.
 const long=selectServedPlan(CLASSES.P1000,400,null,'endurance');
 if(long.state!=='ready')throw new Error('Long-route quasi-static verdict changed');
 if(!routes.some(r=>profileKey(r)===profileKey({class:'P1000',km:400,mode:long.mode,options:long.options})))routes.push(necessaryEnergyRecord({class:'P1000',km:400,basis:'record',mode:long.mode,options:long.options,
  profile:'ready selector',pages:['concept/energy-analysis.html'],location:'necessary-energy; the shared page selector returns ready for these exact inputs'}));
 const diagnostic=read('tests/energy/diagnostic-fixtures.json');
 const diagnosticProfiles=diagnostic.missions.map(r=>necessaryEnergyRecord({...r,options:{...r.options,basis:'record'}}));
 const diagnosticOriginalLong=necessaryEnergyRecord(diagnostic.originalLong);
 const shortages=items=>items.filter(r=>r.accounting.shortageMWh>1e-6);
 return {method:'Integrate the existing drawAt electrical.batteryPowerMW at 2000 midpoint samples per phase, in PHASES order. Record cumulative draw at every phase end; interpolate the first nominal-storage crossing inside its sample.',
  scope:NECESSARY_ENERGY_SCOPE,servedMissions,routes,pairedP100,diagnosticProfiles,diagnosticOriginalLong,
  excludedProfileSets:'Earlier historical cells, the payload-exchange study and static component-only scans are outside this planCycle storage diagnostic. Current prescribed, selected, full-delivery, coefficient, single-input, requirement, descent and served-candidate profile tables are covered, including unsupported paths as supplied-effort diagnostics.',
  coverage:Object.fromEntries([...new Set(inputs.flatMap(r=>r.occurrences.map(o=>o.profileSet)))].map(population=>{
   const rows=inputs.filter(r=>r.occurrences.some(o=>o.profileSet===population));
   return [population,{uniqueProfiles:rows.length,printedOccurrences:rows.reduce((n,r)=>n+r.occurrences.filter(o=>o.profileSet===population).length,0)}];
  })),
  shortages:{servedMissions:shortages(servedMissions),routes:shortages(routes)},
  summary:{capturedMissions:servedMissions.length,capturedShortages:shortages(servedMissions).length,
   printedProfiles:routes.length,printedProfileShortages:shortages(routes).length}};
}
if(process.argv[1]?.endsWith('energy-necessary.mjs')){
 const result=generateNecessaryEnergy();
 writeGenerated('research/analysis/energy-necessary.json',JSON.stringify(result,null,2)+'\n');
 console.log('Necessary energy: '+JSON.stringify(result.summary));
 for(const [population,rows] of Object.entries(result.shortages))for(const r of rows)
  console.log(`${population}: ${r.capture??r.profile} ${r.mission??''} ${r.class} ${r.km} km ${r.basis??'record'}: ${r.accounting.cumulativeDrawMWh.toFixed(1)} MWh / ${r.accounting.nominalStorageMWh} MWh; empty ${r.accounting.emptyAtMin.toFixed(1)} min; shortage ${r.accounting.shortageMWh.toFixed(1)} MWh; pages ${r.pages.join(', ')}`);
}
