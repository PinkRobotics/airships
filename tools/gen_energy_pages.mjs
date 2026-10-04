/* Exact served sentences from generated records. No page figure is hand quoted. */
import fs from 'node:fs';
import {CLASSES,MODES,PHASES,planCycle} from '../sim/index.js';
import {batteryMass} from '../research/analysis/energy-omissions.mjs';
const load=name=>JSON.parse(fs.readFileSync('research/analysis/'+name+'.json'));
const forceCheck=load('energy-page-checks');
const profiles=load('energy-profiles'),unheld=load('energy-unheld'),requirements=load('energy-requirements'),omissions=load('energy-omissions'),crosschecks=load('energy-crosschecks'),study=load('payload-exchange');
const N=(n,d=1)=>n.toLocaleString('en-CA',{minimumFractionDigits:d,maximumFractionDigits:d,useGrouping:true});
const row=(data,cls,km,basis)=>{const r=data.rows.find(r=>r.class===cls&&r.km===km&&r.basis===basis);if(!r)throw new Error('missing generated record '+cls+' '+km+' '+basis);return r;};
const key=(file,cls,km,basis,suffix)=>`research/analysis/${file}.json#rows[class=${cls},km=${km},basis=${basis}].${suffix}`;
const keys=[];const sentences=[];const inventory=[];
function sentence(id,text,recordKeys){sentences.push({id,text,keys:recordKeys});keys.push(...recordKeys);return `<p data-energy-sentence="${id}">${text}</p>`;}
function accepted(b,element){
 if(!b.feasible)throw new Error('served record is infeasible: '+element);
 const p=planCycle(CLASSES[b.class],MODES[b.mode],b.km,null,b.options);
 if(!p.feasible)throw new Error('served record fails exact replay: '+element);
 for(const [field,source] of [['cycleMin','cycleMin'],['eCycleMWh','cycleMWh'],['deliveredT','deliveredT'],['retainedT','ballastT'],['kwhPerTonne','kwhPerTonne']]){
  if(!Number.isFinite(b[source])||Math.abs(b[source]-p[field])>1e-8)throw new Error('served record figure differs from replay: '+element+' '+field);
  inventory.push({page:'index.html / concept/index.html',element,quantity:field,value:b[source],plan:{class:b.class,km:b.km,basis:b.basis,mode:b.mode,windState:'not measured',wind:null},feasible:true});
 }
 return p;
}
let text='';
text+=sentence('force-ledger',`The simulated cycle assigns every vertical force to an owner, a limit and a price. The independent check covers ${N(forceCheck.report.instants,0)} simulated instants, with ${N(Object.values(forceCheck.report.violations).reduce((n,v)=>n+v,0),0)} force or bus violations; owner sums agree within the check's relative tolerance. No aircraft has flown.`,['research/analysis/energy-page-checks.json#report.{instants,violations}','tests/energy/closure.mjs']);
const at60=['record','favourable'].map(basis=>row(profiles,'P100',60,basis));
text+=sentence('p100-as-drawn',`At ${N(at60[0].km,0)} km one-way in still air, the prescribed balanced P-100 profile ${at60.every(r=>r.asDrawn.feasible)?'closes on both bases':'does not close on both bases'}. `+at60.map(r=>{
 const p=planCycle(CLASSES.P100,MODES.balanced,r.km,null,{basis:r.basis});
 if(!r.asDrawn.feasible)return `${r.basis}: ${r.asDrawn.bindingLimits.join(', ')}.`;
 if(!p.feasible)throw new Error('as-drawn record no longer closes');
 for(const [field,source] of [['cycleMin','cycleMin'],['eCycleMWh','cycleMWh'],['deliveredT','deliveredT']])if(Math.abs(p[field]-r.asDrawn[source])>1e-8)throw new Error('as-drawn record differs from exact replay: '+field);
 for(const q of ['cycleMin','eCycleMWh','deliveredT'])inventory.push({page:'index.html / concept/index.html',element:'p100-as-drawn',quantity:q,value:p[q],plan:{class:'P100',km:r.km,basis:r.basis,mode:'balanced',windState:'not measured'},feasible:true});
 const peak=forceCheck.examples.find(e=>e.basis===r.basis).peak;
 return `${r.basis}: ${N(r.asDrawn.deliveredT,0)} t delivered in ${N(r.asDrawn.cycleMin)} minutes for ${N(r.asDrawn.cycleMWh)} MWh of energy supplied; the sampled rotor peak is ${N(peak.rotorMW)} MW, with ${N(peak.grossMW)} MW gross demand against ${N(peak.supplyMW)} MW bus supply at that instant.`;
}).join(' '),[...at60.map(r=>key('energy-profiles','P100',r.km,r.basis,'asDrawn.{feasible,deliveredT,cycleMin,cycleMWh,bindingLimits}')),'research/analysis/energy-page-checks.json#examples[*].peak.{rotorMW,grossMW,supplyMW}']);
const p15=row(profiles,'P100',15,'record'),best15=accepted(p15.best,'p100-selected'),full15=accepted(p15.fullDeliveryBest,'p100-full-delivery');
text+=sentence('p100-selected',`At ${N(p15.km,0)} km, the P-100's prescribed profile does not close: ${p15.asDrawn.bindingLimits.join(', ')}; the worst unheld force is ${N(p15.asDrawn.worst.unheldT)} tf in ${p15.asDrawn.worst.phase.toLowerCase().replaceAll('_',' ')}. The cheapest feasible profile in the generated search is ${p15.best.mode}: ${N(p15.best.deliveredT)} t delivered, ${N(p15.best.ballastT)} t kept aboard, ${N(p15.best.cycleMin)} minutes and ${N(p15.best.cycleMWh)} MWh supplied (${N(p15.best.kwhPerTonne,0)} kWh per delivered tonne). The searched full-delivery profile delivers ${N(p15.fullDeliveryBest.deliveredT,0)} t in ${N(p15.fullDeliveryBest.cycleMin)} minutes for ${N(p15.fullDeliveryBest.cycleMWh)} MWh; the profile choice matters.`,[key('energy-profiles','P100',15,'record','asDrawn.{bindingLimits,worst}'),key('energy-profiles','P100',15,'record','best.{mode,deliveredT,ballastT,cycleMin,cycleMWh,kwhPerTonne}'),key('energy-profiles','P100',15,'record','fullDeliveryBest.{deliveredT,cycleMin,cycleMWh}')]);
let larger='Neither larger class delivers its nameplate payload on the drawn hardware. ';
for(const cls of ['P1000','P10000']){
 const c=CLASSES[cls];larger+=c.name+': ';
 for(const km of [15,60])for(const basis of ['record','favourable']){
  const u=row(unheld,cls,km,basis),r=row(profiles,cls,km,basis);accepted(r.best,'larger-classes');
  const peak=u.phases.reduce((a,b)=>Math.abs(a.unheldT)>Math.abs(b.unheldT)?a:b);
  larger+=`On the prescribed ${basis} profile at ${N(u.km,0)} km, force is unheld in ${u.phases.map(p=>p.phase.toLowerCase().replaceAll('_',' ')).join(', ')}; the largest is ${N(peak.unheldT)} tf (${peak.unheldT>=0?'surplus lift':'upward force requested'}) in ${peak.phase.toLowerCase().replaceAll('_',' ')}. On the drawn hardware, the feasible ${r.best.mode} plan delivers ${N(r.best.deliveredT)} of its ${N(c.payloadT,0)} tonnes per cycle and keeps ${N(r.best.ballastT)} aboard (${basis} basis, ${N(r.best.cycleMin)} minutes, ${N(r.best.cycleMWh)} MWh supplied). `;
  keys.push(key('energy-unheld',cls,km,basis,'phases[*].{phase,unheldT}'),key('energy-profiles',cls,km,basis,'best.{mode,deliveredT,ballastT,cycleMin,cycleMWh}'));
 }
}
text+=sentence('larger-classes',larger.trim(),keys.slice(-16));
let changes='First, the simulation searches a slower letdown at its own airspeed and a climb the buoyant surplus can drive; then keep water aboard. Changing battery power also requires adequate rotor thrust and storage mass. ';
const requirementKeys=[];
for(const cls of ['P1000','P10000'])for(const basis of ['record','favourable']){
 const r=row(requirements,cls,15,basis),power=r.powerAndThrust,c=CLASSES[cls],mass=batteryMass(c,power.requiredBatteryMW).cases;
 changes+=`${c.name}, ${basis}: the prescribed-profile requirement is ${N(power.requiredBatteryMW)} MW of battery power and ${N(power.requiredRotorT)} tf of rotor thrust; battery mass is ${Object.entries(mass).map(([name,v])=>N(v.tonnes,0)+' t ('+name+')').join(', ')} against a ${N(c.payloadT,0)} t dry-mass target. ${Object.values(mass).some(v=>v.exceedsDryTarget)?'Storage cases exceed the target; this is not offered as a hardware option.':'This is a conditional requirement, not a design.'} `;
 requirementKeys.push(key('energy-requirements',cls,15,basis,'powerAndThrust.{requiredBatteryMW,requiredRotorT}'),`research/analysis/energy-omissions.json#rows[class=${cls}].battery.{hours,cases.*.specificEnergyWhKg}`);
}
text+=sentence('closure-order',changes+'A different vehicle belongs to analysis, with its trade-offs stated.',requirementKeys);
const fav15=row(profiles,'P100',15,'favourable');
const controls=b=>JSON.stringify(Object.fromEntries(Object.entries(b.options).filter(([k])=>k!=='basis')));
if(p15.best.mode!==fav15.best.mode||controls(p15.best)!==controls(fav15.best))throw new Error('paired energy sentence requires identical controls');
accepted(fav15.best,'paired-energy');
text+=sentence('paired-energy',`For the feasible ${N(p15.km,0)} km P-100 ${p15.best.mode} profile, the record basis supplies ${N(p15.best.cycleMWh)} MWh and the same controls on the favourable basis supply ${N(fav15.best.cycleMWh)} MWh. A profile that fails force or bus closure supplies no delivery, endurance or fleet rate on these pages; its diagnostic effort is retained in the linked analysis tables.`,[key('energy-profiles','P100',15,'record','best.{mode,cycleMWh}'),key('energy-profiles','P100',15,'favourable','best.cycleMWh')]);
const dragCases=requirements.rows.filter(r=>r.km===15),cdValues=dragCases[0].dragSensitivity.map(s=>s.verticalCd);
let qualification=`These are simulated, quasi-static cycles. Feasible means force and bus closure at every checked instant. Battery hours are reported; they do not determine feasibility. Rotor efficiency, broadside drag, aerodynamic lift and span efficiency remain assumptions. Across the generated broadside-drag cases ${cdValues.map(v=>N(v,0)).join(', ')}, every prescribed ${N(dragCases[0].km,0)} km class/basis profile remains infeasible. `;
for(const cls of ['P1000','P10000']){
 const cases=dragCases.filter(r=>r.class===cls).flatMap(r=>r.dragSensitivity.map(s=>Math.abs(s.worst.unheldT)));
 qualification+=`${CLASSES[cls].name}'s largest unheld force ranges from ${N(Math.min(...cases))} to ${N(Math.max(...cases))} tf on both bases. `;
}
qualification+='Model feasibility does not establish structural float, transient control or flight performance.';
text+=sentence('qualifications',qualification,['research/analysis/energy-requirements.json#rows[km=15].dragSensitivity[*].{verticalCd,feasible,worst.unheldT}','research/analysis/energy-rotor-range.json#assumption']);
text+=sentence('fire-boundary','Nothing here says any fire would have burned differently. The fires are records or labelled inventions; the fleet is simulated and never flew.',['docs/ENERGY-MODEL-2026-10.md']);
const omissionText='The omissions analysis names unpriced beam-wind position holding, cable and storage mass, the bag pendulum and winch transients, day-average solar credited at every instant, and dry mass as a target rather than an assembled ledger.';
text+=sentence('omissions',omissionText.replace('omissions analysis','<a href="concept/energy-analysis.html#omissions">omissions analysis</a>'),['research/analysis/energy-omissions.json#rows[*]']);
text+=sentence('study-link','The <a href="concept/energy-analysis.html#study">payload-exchange study summary</a> is analysis of alternative force balances, not a design or a mission result.',['research/analysis/payload-exchange.json#ranking']);
// Five study sentences, under their own analysis heading. No unsupported mission energy or rate is promoted.
let analysis='<h4>Payload exchange · analysis</h4>\n';
analysis+=sentence('analysis-water','In the study, water kept aboard closes the exchange force balance on the drawn vehicle and bus, at a price in delivered water; the accepted mission figures use the integrated model instead.',['research/analysis/payload-exchange.json#ranking[route=b]']);
analysis+=sentence('analysis-half-load',`The study's half-load hull gives up fail-safe float-up: the loaded ${CLASSES.P1000.name} would be ${N(study.classes.P1000.routes.d.failureCase.heavyT,0)} t heavy after its rotors stop, and it needs rotors that push both ways, which the drawn rotors do not.`,['research/analysis/payload-exchange.json#classes.P1000.routes.d.failureCase.heavyT','research/analysis/payload-exchange.json#ranking[route=d]']);
analysis+=sentence('analysis-approach','The study analyses an approach at airspeed, but the hand-over to the bag has no coherent form at the drawn cable and hull lengths.',['research/analysis/payload-exchange.json#ranking[route=c]']);
analysis+=sentence('analysis-volume','The study analyses variable displacement for a partial exchange; it asks sealed cells to change volume every cycle and requires reopening that design decision.',['research/analysis/payload-exchange.json#ranking[route=e]']);
analysis+=sentence('analysis-cryo','The study finds that making the exchange ballast within the cycle exceeds the bus and dry-mass target on every class with a gap; cryogenic ballast is analysis of a different plant, not an accepted flight plan.',['research/analysis/payload-exchange.json#ranking[route=f]']);
function region(name,body){return `<!-- served-energy:${name}:start -->\n${body}\n<!-- served-energy:${name}:end -->`;}
const home=region('home','<details class="d"><summary>Energy · feasible simulated plans</summary><div class="dbody">\n'+text+analysis+'\n</div></details>');
const concept=region('concept','<details class="d"><summary>What the generated energy records say</summary><div class="dbody">\n'+text.replaceAll('href="concept/','href="')+analysis+'\n</div></details>');
const homeWorked=region('worked',sentence('worked-record',`The generated ${N(p15.km,0)} km P-100 ${p15.best.mode} example requests ${N(CLASSES.P100.payloadT,0)} t, keeps ${N(p15.best.ballastT)} t aboard and delivers ${N(p15.best.deliveredT)} t in ${N(p15.best.cycleMin)} minutes; supplied energy is ${N(p15.best.cycleMWh)} MWh on the record basis and ${N(fav15.best.cycleMWh)} MWh on the favourable basis. This is a feasible simulated example, separate from each mission's own route. Feasible means force and bus closure at every checked instant. Battery hours are reported; they do not determine feasibility.`,[key('energy-profiles','P100',15,'record','best'),key('energy-profiles','P100',15,'favourable','best.cycleMWh')]));
const outputs={'index.html':{home,worked:homeWorked},'concept/index.html':{concept}};
const files={};
files['concept/energy-analysis.html']=`<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Energy analysis summaries · Pink Robotics</title>
<style>html{color-scheme:dark}body{margin:0;background:#0a0a0c;color:#eceef2;font:16px/1.65 system-ui,sans-serif}main{max-width:72ch;margin:auto;padding:32px 20px}a{color:#ff75b4}code{overflow-wrap:anywhere}h1,h2{line-height:1.2}section{border-top:1px solid #33333c;margin-top:32px;padding-top:20px}</style>
</head><body><main><a href="./">How the model works</a><h1>Energy analysis summaries</h1>
<p>These are analysis of assumptions and alternative force balances. They are not mission results, an aircraft design or flight evidence. The full study, generated records and sources remain in the repository at the paths named below.</p>
${region('analysis','<section id="study">'+analysis+'<p>Source study: <code>research/analysis/payload-exchange.md</code>; generated records: <code>research/analysis/payload-exchange.json</code>. This summary publishes its ruled conclusions, without promoting the study’s sketch-cycle energies to mission results.</p></section>\n<section id="omissions"><h2>Model omissions · analysis</h2><p>'+omissionText+'</p><p>Source analysis: <code>research/analysis/energy-omissions.md</code>; generated records: <code>research/analysis/energy-omissions.json</code>. Model feasibility remains conditional on these omissions.</p></section>')}
</main><footer style="max-width:72ch;margin:auto;padding:20px"><a href="../notices.html">Data, licences and notices</a></footer></body></html>
`;
for(const [file,regions] of Object.entries(outputs)){
 let body=fs.readFileSync(file,'utf8');
 for(const [name,fresh] of Object.entries(regions)){
  const start=`<!-- served-energy:${name}:start -->`,end=`<!-- served-energy:${name}:end -->`;
  if(body.split(start).length!==2||body.split(end).length!==2||body.indexOf(start)>body.indexOf(end))throw new Error('expected one marker pair: '+file+' '+name);
  body=body.slice(0,body.indexOf(start))+fresh+body.slice(body.indexOf(end)+end.length);
 }
 files[file]=body;
}
if(process.argv.includes('--records'))console.log(JSON.stringify({sentences,inventory},null,2));
else if(process.argv.includes('--emit'))console.log(JSON.stringify(files));
else if(process.argv.includes('--check')){
 let failures=0;
 for(const [file,fresh] of Object.entries(files))if(!fs.existsSync(file)||fs.readFileSync(file,'utf8')!==fresh){console.error('FAIL stale generated served-energy sentence: '+file);failures++;}
 if(failures)process.exitCode=1;else console.log('PASS served energy sentences: exact regions match generated records and feasible profiles replay at their own inputs');
}else{for(const [file,body] of Object.entries(files))fs.writeFileSync(file,body);console.log('Generated served energy regions: '+Object.keys(files).join(', '));}
