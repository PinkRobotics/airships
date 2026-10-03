/* Render the energy documents from model records. --emit writes only JSON to stdout. */
import fs from 'node:fs';
import {CLASSES,MODES,CFG,DEFAULTS,PHASES,planCycle,energySummary,dragMW,pumpMW,ledger,TERRAIN_MSL,WORK_ALT_MSL,sourceAltM,PROFILE_SEARCH,resetConfig,setConfig,RHO_SL_ISA,FORCE_TOL,LIMIT_STEPS,PLAN_STEPS,AERO_CL_MAX,AERO_CL_VALUES,VERTICAL_CD,ROTOR_EFFICIENCY_VALUES,HOIST_M,WINCH_ETA} from '../../sim/index.js';
import {specificEnergies,batteryMass} from './energy-omissions.mjs';
const read=n=>JSON.parse(fs.readFileSync(`research/analysis/${n}.json`));
const f=(x,n=3)=>x==null?'none':Number(x).toFixed(n);
const table=(heads,rows)=>'| '+heads.join(' | ')+' |\n|'+heads.map(()=>'---').join('|')+'|\n'+rows.map(r=>'| '+r.join(' | ')+' |').join('\n')+'\n';
const historical=read('energy-closure-history'),profiles=read('energy-profiles'),feasible=read('energy-feasible'),requirements=read('energy-requirements');
const archived=read('energy-document-history');
const unheld=read('energy-unheld'),cross=read('energy-crosschecks'),omissions=read('energy-omissions');
const records=[];
for(const c of Object.values(CLASSES))for(const km of [15,60])for(const basis of ['record','favourable']){
 const p=planCycle(c,MODES.balanced,km,null,{basis});
 records.push({class:c.id,km,basis,asDrawn:energySummary(c,p),phaseEnergy:p.E,channels:p.Echan,
  solarMWh:c.solarM2*CFG.solarWPerM2/1e6*p.cycleMin/60,ln2MakeT:p.ln2MakeT,letdownMWh:p.letdownMWh,anchorHoistMWh:p.anchorHoistMWh});
}
const classes=Object.values(CLASSES).map(c=>{
 const rho=ledger(c,WORK_ALT_MSL).rho,solarMW=c.solarM2*CFG.solarWPerM2/1e6,hotelMW=c.genMW*.02;
 const groundMassT=ledger(c,TERRAIN_MSL).surplusT,tankEnergyMWh=c.ln2CapT*CFG.eLN2,groundEnergyMWh=groundMassT*CFG.eLN2;
 return {class:c.id,payloadT:c.payloadT,lengthM:c.lenM,diameterM:c.diaM,designVolumeM3:c.dispM3,
  capsuleVolumeM3:Math.PI*(c.diaM/2)**2*(c.lenM-c.diaM)+4/3*Math.PI*(c.diaM/2)**3,
  diskM2:c.diskM2,batteryMWh:c.battMWh,batteryMW:c.battMW,generatorMW:c.genMW,solarMW,hotelMW,
  dragMW:dragMW(c,MODES.balanced,rho),dragDensity:rho,volumetricCd:CFG.Cd*Math.PI*(c.diaM/2)**2/c.dispM3**(2/3),sourceM:sourceAltM(c),pumpMW:pumpMW(c),
  pumpIdealMWh:c.payloadT*9810*sourceAltM(c)/3.6e9,pumpElectricalMWh:c.payloadT*9810*sourceAltM(c)/3.6e9/CFG.pumpEta,
  groundMassT,tankMassT:c.ln2CapT,tankEnergyMWh,groundEnergyMWh,
  groundSolarDays:groundEnergyMWh/(solarMW-hotelMW)/24,tankSolarDays:tankEnergyMWh/(solarMW-hotelMW)/24,
  tankPlantDays:tankEnergyMWh/c.cryoMW/24,battery:batteryMass(c)};
});
const sensitivity=[];
for(const basis of ['record','favourable']){
 const base=planCycle(CLASSES.P10000,MODES.balanced,15,null,{basis});
 for(const key of ['propEta','Cd','rhoAir','pumpEta','hoseMul','rhoSL','rtLN2','eLN2','solarWPerM2','cruiseKph','anchorBagT','dropKm','fillM3s','dispM3','diskM2','battMW','anchorM','solarM2']) {
  const rows=[];
  for(const multiplier of [.8,1.2]) {
   let p;if(key in DEFAULTS){setConfig({[key]:DEFAULTS[key]*multiplier});p=planCycle(CLASSES.P10000,MODES.balanced,15,null,{basis});resetConfig();}
   else p=planCycle({...CLASSES.P10000,[key]:CLASSES.P10000[key]*multiplier},MODES.balanced,15,null,{basis});
   rows.push({multiplier,energyPct:100*(p.eCycleMWh/base.eCycleMWh-1),cycleMinutes:p.cycleMin,feasible:p.feasible,worstUnheldT:p.worst.unheldT});
  }
  sensitivity.push({basis,key,rows});
 }
}
const readmeExamples=[15,45].flatMap(km=>['record','favourable'].map(basis=>({class:'P10000',km,basis,...energySummary(CLASSES.P10000,planCycle(CLASSES.P10000,MODES.balanced,km,null,{basis}))})));
const record={readmeExamples,constants:{rhoSL:CFG.rhoSL,Cd:CFG.Cd,propEta:CFG.propEta,pumpEta:CFG.pumpEta,eLN2:CFG.eLN2,rtLN2:CFG.rtLN2,solarWPerM2:CFG.solarWPerM2,forceTolerance:FORCE_TOL,limitSteps:LIMIT_STEPS,energySteps:PLAN_STEPS,clMax:AERO_CL_MAX,clValues:AERO_CL_VALUES,verticalCd:VERTICAL_CD,rotorEfficiencyRange:ROTOR_EFFICIENCY_VALUES,hoistM:HOIST_M,winchEfficiency:WINCH_ETA},date:'2026-10-02',classes,records,sensitivity,search:PROFILE_SEARCH};
const baselineTable=table(['Class','km','Basis','As drawn','Minutes','Supplied MWh','kWh/planned tonne','Battery-hours quotient'],records.map(r=>[r.class,r.km,r.basis,r.asDrawn.feasible?'closes':'does not close',f(r.asDrawn.cycleMin),f(r.asDrawn.cycleMWh),f(r.asDrawn.kwhPerTonne),f(r.asDrawn.hoursOnBattery)]));
const profileTable=table(['Class','km','Basis','Profile','Delivered t','Kept t','Minutes','MWh','kWh/delivered tonne'],profiles.rows.flatMap(r=>[
 [r.class,r.km,r.basis,'as drawn: '+(r.asDrawn.feasible?'closes':'does not close'),f(r.asDrawn.deliveredT),f(r.asDrawn.ballastT),f(r.asDrawn.cycleMin),f(r.asDrawn.cycleMWh),f(r.asDrawn.kwhPerTonne)],
 r.best?[r.class,r.km,r.basis,'cheapest feasible profile found in the stated space',f(r.best.deliveredT),f(r.best.ballastT),f(r.best.cycleMin),f(r.best.cycleMWh),f(r.best.kwhPerTonne)]:[r.class,r.km,r.basis,'none in the stated space','','','','','']
]));
const fullTable=table(['Class','km','Basis','Full-payload mode','Delivered t','Minutes','MWh','kWh/t','Inertia qualification'],profiles.rows.filter(r=>r.fullDeliveryBest).map(r=>{const b=r.fullDeliveryBest;return [r.class,r.km,r.basis,b.mode,f(b.deliveredT),f(b.cycleMin),f(b.cycleMWh),f(b.kwhPerTonne),b.inertia.qualification];}));
const searchHistory=read('energy-profile-history');
const movementTable=table(['Class','km','Basis','Kept t: earlier / current','Delivered t: earlier / current','Minutes: earlier / current','kWh/t: earlier / current','Effect'],searchHistory.movements.map(r=>{const pair=k=>[r.before?.[k],r.after?.[k]].map(v=>f(v)).join(' / ');return [r.class,r.km,r.basis,pair('ballastT'),pair('deliveredT'),pair('cycleMin'),pair('kwhPerTonne'),r.after&&r.before?(Math.abs(r.after.kwhPerTonne-r.before.kwhPerTonne)<0.0005?'Same cost at printed precision':r.after.kwhPerTonne<r.before.kwhPerTonne?'Lower cost in this changed search space':'Higher cost in this changed search space'):'Search result changed'];}));
const historyTable=table(['Class','km','Quantity','Earlier published','Intermediate published','Record as drawn','Favourable as drawn','Reason'],historical.flatMap(h=>['cycleMWh','kwhPerTonne','peakRotorMW','hoursOnBattery'].map(key=>{
 const a=records.find(r=>r.class===h.class&&r.km===h.km&&r.basis==='record').asDrawn,b=records.find(r=>r.class===h.class&&r.km===h.km&&r.basis==='favourable').asDrawn;
 return [h.class,h.km,key,f(h.old[key]),f(h.first[key]),f(a[key]),f(b[key]),'Limited and priced force owners; local density; bus reservation; paid bag inventory; smooth profile'];
})));
const reportChanges=read('energy-report-corrections').changes;
const reportsTable=table(['Report and former line','Generated field','Earlier printed','Current record','Current favourable','Reason'],reportChanges.map(r=>{const [id,group,...field]=r.key.split('.'),c=CLASSES[id],p=planCycle(c,MODES.balanced,15,null,{basis:'favourable'});const values={cycle:p,descent:{rotorCapT:p.rotorMaxT},energy:{letdownMWh:p.letdownMWh,anchorHoistMWh:p.anchorHoistMWh,ledgerMWh:p.E,deficitPerCycleMWh:p.eCycleMWh-c.solarM2*CFG.solarWPerM2/1e6*p.cycleMin/60}};let v=values[group];for(const key of field)v=v?.[key];return [r.file+':'+r.line,r.key,r.old,r.new,f(v),r.cause];}));
const correctionTable=table(['Earlier publication','Quantity','Earlier value','Current record / favourable','Cause and effect'],[
 ...classes.map((c,i)=>['PHYSICS section 6',c.class+' balanced cruise MW',[1.06,9.16,69.68][i],f(c.dragMW)+' / '+f(c.dragMW),'Capsule frontal area and local density; higher hull drag']),
 ...classes.filter(c=>c.class!=='P1000').map(c=>['PHYSICS section 5',c.class+' electrical fill MWh',c.class==='P100'?.091:9.08,f(c.pumpElectricalMWh)+' / '+f(c.pumpElectricalMWh),'Correct head in the published arithmetic; higher pumping bill']),
 ['PHYSICS section 5','P100 ideal fill MWh',.068,f(classes[0].pumpIdealMWh)+' / '+f(classes[0].pumpIdealMWh),'Correct head; higher potential energy'],
 ...classes.map((c,i)=>['PHYSICS section 8',c.class+' ground-surplus solar days',[2.6,5.7,12.9][i],f(c.groundSolarDays)+' / '+f(c.groundSolarDays),'Day-average solar replaces retired peak assumption; slower recovery']),
 ...classes.map((c,i)=>['PHYSICS section 8',c.class+' full tank MWh',[65,651,6505][i],f(c.tankEnergyMWh)+' / '+f(c.tankEnergyMWh),'Earlier energy used ground surplus, not tank capacity; higher tank bill']),
 ...classes.map((c,i)=>['sim README',c.class+' hull dimensions m',['190 × 47','404 × 102','876 × 219'][i],c.lengthM+' × '+c.diameterM,'Configured capsule; shorter and wider, no performance conclusion']),
 ['sim README','Nitrogen recovery fraction',.50,CFG.rtLN2+' / '+CFG.rtLN2,'Storage recovery constrained by exergy; less recovered energy'],
 ['Earlier physics reading','P10000 cycle MWh',88.2,records.filter(r=>r.class==='P10000'&&r.km===15).map(r=>f(r.asDrawn.cycleMWh)).join(' / '),'No reproducible old mode or snapshot; current unsupported-cycle effort is larger'],
]);
const laws=`## Force and energy rules\n\nThe ledger subtracts all onboard weight from local buoyant lift.\nIts owners are the cable-carried water, downward rotors, permitted aerodynamic downforce and signed vertical drag.\nUnheld force stays visible.\n\nSurplus is local displaced-air mass minus dry mass, water and nitrogen.\nThe signed residual is surplus minus bag support, rotor thrust, aerodynamic downforce and vertical drag.\n\nGlauert momentum pricing solves T = 2 ρ A v_i √(V² + (v_c + v_i)²), then P = T (v_c + v_i) / η.\nThe vertical drag owner is ρ C_D S v_z |v_z| / (2 g), with upward velocity positive.\nThe favourable downforce cap is C_L,max q S, and its induced drag is T_aero² / (q π b² e).\n\nThe force tolerance is ${FORCE_TOL} times the larger of unity and absolute surplus.\nConstraint sampling uses ${LIMIT_STEPS} intervals per phase, plus seams and internal profile joins.\nEnergy uses ${PLAN_STEPS} midpoint intervals per phase; constraint peaks are checked separately.\n\nThe unverified broadside coefficient is ${VERTICAL_CD}; the favourable lift coefficient is ${AERO_CL_MAX}.\nThe reported lift-coefficient sweep is ${AERO_CL_VALUES.join(', ')}; rotor-efficiency endpoints are ${ROTOR_EFFICIENCY_VALUES.join(', ')}.\nBag water is credited when carried; its ${HOIST_M} m lift at efficiency ${WINCH_ETA} remains priced.\n\nA cycle closes only when the residual and gross bus draw meet the stated tolerances at every checked instant.\nBus saturation alone is a note.\nThe rotors have no upward authority.\n\nRecord basis credits no aerodynamic hold-down.\nFavourable basis chooses the least-power split between capped rotors and capped aerodynamic downforce.\nInduced drag is charged to propulsion, and all force and power terms use local ISA density.\n\nRotor efficiency represents figure of merit times drive efficiency.\nHold-down descent is priced as climb, on the conservative side; climb against hold-down thrust is priced as level flight, with no bound claimed.\n\nThe installed thrust cap is an unverified hover surrogate at the battery-plus-generator rating.\nA feasible result is quasi-static.\nThe [inertia table](../research/analysis/energy-motion.md) compares omitted inertia with simultaneous rotor reserve.\nThe feasible-profile records also contain that comparison for every phase.\n`;
const search=`## What the profile search means\n\nThe prescribed profile is retained as "as drawn".\nThe result is the cheapest feasible profile found in the stated space, not a global optimum.\n\nCruise speed multipliers: ${PROFILE_SEARCH.speedMultipliers.join(', ')}.\nModes: ${PROFILE_SEARCH.modes.join(', ')}.\n\n`+table(['Independent parameter','Searched values'],Object.entries(PROFILE_SEARCH.verticalProfile).map(([k,v])=>[k,v.join(', ')]))+`\nClimb and letdown each have independent peak-rate and peak-airspeed caps.\nThe slowest peak letdown cap is ${Math.min(...PROFILE_SEARCH.verticalProfile.letdownRateMps)} m/s on each class.\nThis finite bound includes slow descents; smaller caps remain unsearched, not physically excluded.\n\nShort joins take longer when needed for smoothness.\nThe drop altitude, terrain clearance and cable reach stay fixed.\nThe approach remains stationary.\nSegment time and ground distance are integrated; energy uses the same instantaneous ledger.\nA profile exceeding the route distance is refused.\n\nRetained water is searched at five-percent payload steps and at each bisected first closing threshold.\nPrinted requirements round upward at the verdict resolution and replay through the model.\nThe older whole-phase dilation is named \`movingPhaseRateMultiplier\`; the new search does not use it.\n`;
const reqTable=fs.readFileSync('research/analysis/energy-requirements.md','utf8').replace(/^# /,'## ').replace('(energy-profiles.md)','(../research/analysis/energy-profiles.md)');
const omitted=fs.readFileSync('research/analysis/energy-omissions.md','utf8').replace('../../float/','../float/');
const checkText=`## How this was checked\n\nTwo ledger implementations used gpt-6-astra and gpt-6-sol.\nExecution tests and a second reading used muse-spark-1.3; a number-by-number comparison used claude-fable-5-1.\nClaude-opus-5-5 ruled on the supported claims.\nA second model family, glm-5.3, read the physics document; claude-fable-5-1 wrote the payload-exchange analysis.\nA person directs the project; no person checked the arithmetic.\n\nRun \`make energycheck energydoccheck\`.\nIndependent equations check force, power, supply, smoothness and printed-row replay.\nThe checks do not validate a hull or rotor in flight.\n`;
const unheldText=fs.readFileSync('research/analysis/energy-unheld.md','utf8').replace(/^# /,'## ').replace('(energy-profiles.md)','(../research/analysis/energy-profiles.md)');
const closure='# Energy closure, 2026-10-02\n\nNo aircraft has flown. The fleet is simulated. Nothing here says a past fire would have burned differently.\n\n'+
 'An infeasible row prices supplied effort along an unsupported profile. Its energy and battery-hours quotient do not establish delivery or endurance.\n\n'+profileTable+'\n'+unheldText+'\n'+
 'Neither larger class delivers its nameplate payload on the drawn hardware in this search; its delivered and retained figures appear above on both bases.\n\n'+
 '## Full payload where the search finds it\n\n'+fullTable+'\n'+'## What would close the gap\n\nFirst consider a slower letdown at lower airspeed and a climb the surplus can drive.\nThen consider water kept aboard, with its cost in delivered tonnes.\nThe battery-and-thrust requirements come next, with their implied mass.\n\n'+reqTable+'\n'+
 'A different vehicle is a separate question. The [payload-exchange study](../research/analysis/payload-exchange.md) is analysis, not design.\n'+
 'Its half-load hull gives up fail-safe float-up and needs upward thrust, which the drawn rotors lack.\n'+
 'An approach at airspeed needs a demonstrated hand-over to the bag. Variable displacement needs changing sealed cells; cryogenic ballast needs added energy and plant mass.\n\n'+
 '## Earlier published figures beside the model\n\nEarlier figures remain dated history. They used incomplete force allocation. The intermediate steps are preserved in `energy-closure-history.json`.\n\n'+historyTable+'\n'+movementTable+'\nIndependent vertical controls and smooth joins change the finite search space. Neither comparison proves a global minimum.\n\n'+correctionTable+'\n'+reportsTable+'\n'+
 'The [superseded document record](../research/analysis/energy-document-history.json) preserves the replaced energy text and its historical numbers. It is dated history, not a current model reading.\n\n'+
 omitted+'\n'+checkText;
const model='# Energy model, 2026-10-02\n\nOne ledger owns the modelled force and power. This is an unvalidated simulation, not a flight performance claim.\n\n'+laws+'\n'+search+'\n'+baselineTable+'\n'+
 '## Independent stationary cross-check\n\nThe analysis full bus means battery plus generator rating. The cycle instead receives the nitrogen recovery available in that phase, plus day-average solar.\n\n'+
 table(['Class','Mode','Full-bus model / independent t','Actual mode bus MW','Other draw MW','Mode thrust model / independent t','Full-bus empty floor t'],cross.modes.map(r=>[r.class,r.mode,`${f(r.fullBusModelT)} / ${f(r.independentFullBusT)}`,f(r.modeBusMW),f(r.nonRotorMW),`${f(r.modeModelT)} / ${f(r.independentModeT)}`,f(r.wholeBusFloorT)]))+'\n'+
 'A retained-water floor depends on altitude, available supply and the other loads aboard. The generated cross-check names nitrogen, newly loaded water and bag support at the stationary fill instant.\n\n'+
 '## Retained-water floor at the stationary fill\n\n'+table(['Class','km','Basis','Profile','Kept t','Independent floor t','Other support t'],cross.profiles.map(r=>[r.class,r.km,r.basis,r.kind,f(r.retainedT),f(r.independentRetainedFloorT),Object.entries(r.otherSupport).map(([k,v])=>k+' '+f(v)).join('; ')]))+'\n## Interfaces\n\n`planCycle(class, mode, distance, wind, options)` computes a cycle. `drawAt` supplies each instantaneous ledger.\n'+
 '`cheapestFeasible` performs the slow stated-space search; it is not suitable for a page-load fleet search.\n'+
 'Generated tables cover only their printed distances; they do not promise interpolation. The monitor is not yet bound to feasible profiles.\n';
const pumpTable=table(['Class','Head m','Pump MW','Ideal MWh','Electrical MWh'],classes.map(c=>[c.class,c.sourceM,f(c.pumpMW),f(c.pumpIdealMWh),f(c.pumpElectricalMWh)]));
const solarTable=table(['Class','Tank t','Tank fill MWh','Ground-surplus t','Ground-surplus MWh','Solar days: ground / tank','Tank days at rated plant'],classes.map(c=>[c.class,c.tankMassT,f(c.tankEnergyMWh),f(c.groundMassT),f(c.groundEnergyMWh),`${f(c.groundSolarDays)} / ${f(c.tankSolarDays)}`,f(c.tankPlantDays)]));
let physics='## 3. Storage inside the dry-mass target\n\n'+omitted+'\n## 4. The prescribed delivery cycle\n\n'+baselineTable+'\n'+profileTable+'\n'+
 'Cycle durations and supplied energy are model outputs. A cycle that does not close supplies no justified delivery rate.\n\n'+
 '## 5. Pumping energy\n\nPump power is water density times gravity, flow and head, divided by pump efficiency.\nThe electrical fill energy is delivered water times gravity and head, divided by the same efficiency.\n\n'+pumpTable+'\n'+
 `The lumped pump efficiency is ${CFG.pumpEta}; it covers the pump, motor, drive and hose losses. Hose mass and detailed friction are not separately modelled.\n\n`+
 '## 6. Drag and cruise power\n\nZero-lift drag power is dynamic pressure times frontal area and drag coefficient, times airspeed, divided by propulsion efficiency.\nInduced drag for aerodynamic hold-down is additional.\n\n'+
 table(['Class','Local density kg/m³','Balanced cruise drag MW','Volumetric drag coefficient'],classes.map(c=>[c.class,f(c.dragDensity,6),f(c.dragMW),f(c.volumetricCd,5)]))+'\n'+
 `The frontal drag coefficient is ${CFG.Cd}. This hull-only assumption does not price rotor installations, fins, the hose pod or their interference.\n\n`+
 '## 7. Vertical force and rotor pricing\n\n'+laws+'\n'+
 '## 8. Nitrogen storage and recovery\n\nNitrogen is storage, not an energy source. Recovery is bounded by the stored nitrogen and the generator rating.\n\n'+
 `Liquefaction costs ${CFG.eLN2} MWh per tonne in this model; round-trip recovery is ${CFG.rtLN2}. Solar is ${CFG.solarWPerM2} W/m² as a day average.\n\n`+
 solarTable+'\n'+
 'Solar-only days subtract hotel load and assume the day-average sun throughout. Tank capacity and ground-surplus ballast are different masses; their energy bills must not be interchanged.\n\n'+
 '## 9. Cycle energy and endurance\n\n'+baselineTable+'\n'+
 'Battery hours divide usable storage by the modelled energy deficit. On an infeasible row this is an accounting quotient, not demonstrated endurance.\n'+
 'Every phase draws from the same ledger. The phase and channel integrals are stored in `energy-documents.json`.\n\n'+
 '## 10. Sensitivity\n\nThese sweeps change one input at a time around the prescribed P-10000 balanced profile at the worked distance.\nAll displayed energy changes are supplied-effort changes when the row is infeasible.\n\n'+
 table(['Basis','Input','Energy change at −20%','Energy change at +20%','Verdict at −20% / +20%'],sensitivity.map(r=>[r.basis,r.key,f(r.rows[0].energyPct,1)+'%',f(r.rows[1].energyPct,1)+'%',r.rows.map(s=>s.feasible?'closes':'does not close').join(' / ')]))+'\n'+
 'The old fixed-density input has no effect because the force and power laws now use local ISA density. Drop distance can change the force-price integral even when metering fixes release time.\n\n'+
 '## 11. Corrections and remaining limits\n\nEarlier energy figures are retained beside current values in [the closure document](ENERGY-CLOSURE-2026-10.md).\nThe former unowned aerodynamic share, phase power discounts, split densities and silent bus overdraw have been removed.\n'+
 'Local-density force balance leaves the named endurance example infeasible; the generated unheld table records every failing phase.\n\n'+search+'\n';
const simulator='# The simulator and its energy ledger\n\nThe modules in this directory have no DOM or network dependency. Class dimensions and power ratings are assumptions, not measured aircraft data.\n\n'+
 '## Run a cycle\n\nImport `CLASSES`, `MODES` and `planCycle` from `sim/index.js` in Node. Pass a one-way distance in kilometres and an optional wind record.\n'+
 'The fifth argument selects basis, retained water and profile controls. Record basis is the default. Always read `feasible`, `worst` and `bindingLimits` beside energy and delivery.\n\n'+
 table(['Module','Owns'],[['config.js','Class constants, operating modes and declared assumptions'],['atmosphere.js','Local ISA density'],['physics.js','Lift, drag, pumping and actuator-disk equations'],['power.js','Instantaneous force owners, prices, bus and energy integral'],['profile.js','Independent vertical controls and segment distance'],['plan.js','Cycle timetable and integrated ledger'],['requirements.js','Replayed requirements and finite profile search'],['state.js','State and telemetry for a prescribed mission'],['energy-view.js','Paired basis readings for existing page binders'],['mission.js','Mission construction'],['assign.js / water.js / targets.js','Allocation, sources and drop lines'],['geo.js / rng.js / format.js','Geometry, repeatable randomness and presentation'],['selftest.js / index.js','Checks and public exports']])+'\n'+
 table(['Class','Hull m','Design volume m³','Battery MWh / MW','Generator MW'],classes.map(c=>[c.class,`${c.lengthM} × ${c.diameterM}`,c.designVolumeM3,`${c.batteryMWh} / ${c.batteryMW}`,c.generatorMW]))+'\n'+laws+'\n'+search+'\n'+
 '## Reading the output\n\n`eCycleMWh` is gross integrated draw minus nitrogen recovery. Solar is reported separately.\n`deliveredT`, `retainedT` and `cycleMin` describe the requested cycle. They establish delivery only when the force and bus verdict closes.\n'+
 '`E` contains phase integrals; `Echan` contains gross channel integrals. `drawAt` is the one source used by the telemetry adapters.\n'+
 'The detailed generated tables are in `research/analysis/energy-*.json`. Run `make energycheck energydoccheck` to replay their claims.\n'+
 'No aircraft has flown. The fleet remains simulated.\n';
const region=(id,text)=>`<!-- energy:${id}:start -->\n${text.trim()}\n<!-- energy:${id}:end -->\n`;
let oldPhysics=fs.readFileSync('docs/PHYSICS.md','utf8');
// Keep the shell and buoyancy sections outside this energy revision.
const notation=region('notation','## Energy notation\n\n'+table(['Input','Value or source'],[
 ['Air density','Local ISA density at each force and power evaluation'],['Sea-level density kg/m³',CFG.rhoSL],
 ['Frontal drag coefficient',CFG.Cd],['Propulsion efficiency',CFG.propEta],['Lumped pump efficiency',CFG.pumpEta],
 ['Pump head m',classes.map(c=>c.class+': '+c.sourceM).join('; ')],['Displacement','CLASSES[*].dispM3'],
 ['Dry-mass target','Equal to payload by assumption'],['Water density kg/m³',1000],['Gravity m/s²',9.81]
 ]));
const nstart=oldPhysics.includes('<!-- energy:notation:start -->')?oldPhysics.indexOf('<!-- energy:notation:start -->'):oldPhysics.indexOf('## Notation');
const nend=oldPhysics.indexOf('## 1. ');
oldPhysics=oldPhysics.slice(0,nstart)+notation+'\n'+oldPhysics.slice(nend);
const start=oldPhysics.includes('<!-- energy:physics:start -->')?oldPhysics.indexOf('<!-- energy:physics:start -->'):oldPhysics.indexOf('## 3. ');
const end=oldPhysics.includes('<!-- energy:physics:end -->')?oldPhysics.indexOf('<!-- energy:physics:end -->')+'<!-- energy:physics:end -->'.length:oldPhysics.indexOf('## 12. ');
const questionBodies={
 2:['Which measurements would validate the force owners?',
  'Can an aerospace reviewer establish attainable hull downforce and drag across the stated airspeeds? Which rotor thrust rating can replace the unverified hover surrogate?\n\n'+
  table(['Class','Full-bus static hold-down t','Actual balanced stationary supply MW'],cross.modes.filter(r=>r.mode==='balanced').map(r=>[r.class,f(r.independentFullBusT),f(r.modeBusMW)]))],
 3:['What vertical profile remains feasible with acceleration included?',
  `The search stops at a peak letdown cap of ${Math.min(...PROFILE_SEARCH.verticalProfile.letdownRateMps)} m/s. What lower bound would mission conditions justify?\n\n`+
  'Can added-mass and control measurements close the gap where omitted inertia exceeds simultaneous rotor reserve? Full-delivery profiles below are quasi-static analysis.\n\n'+fullTable],
 4:['How much delivery can be retained while holding the hull?',
  'Can a measured vehicle carry the retained-water requirements below throughout the cycle? What reserve is needed beyond the first closing threshold?\n\n'+profileTable],
 6:['What power can nitrogen recovery actually supply?',
  'Can the nitrogen expander supply the modelled phase output after its mass, heat exchangers and losses are counted? Which transient bus limits would reduce this supply?\n\n'+
  table(['Class','Mode','Stationary supply MW','Other load MW','Available hold-down t'],cross.modes.map(r=>[r.class,r.mode,f(r.modeBusMW),f(r.nonRotorMW),f(r.independentModeT)]))],
 8:['What rotor area, thrust and storage mass can be built?',
  'What evidence supports the installed disk area, downward-only thrust and battery rating together? Can any required storage mass fit inside the dry-mass target?\n\n'+reqTable],
 9:['How long can recovery take through a real day and night?',
  `The model uses ${CFG.solarWPerM2} W/m² as a day average. What storage and charging losses apply when instantaneous sunlight is zero?\n\n`+
  table(['Class','Day-average solar MW','Ground-surplus solar days','Full-tank solar days'],classes.map(c=>[c.class,f(c.solarMW),f(c.groundSolarDays),f(c.tankSolarDays)]))],
 10:['What nitrogen recovery fraction is demonstrable?',
  `Liquefaction costs ${CFG.eLN2} MWh/t and recovery returns ${CFG.rtLN2} of that investment. Can a complete airborne system reproduce that fraction without an external heat source?\n\n`+
  'Which plant and tank masses belong in the dry ledger, and what duty cycle can they sustain?'],
 14:['Can the bag be picked up and released at this scale?',
  'What cable, winch and control measurements would bound pickup shock and pendulum motion? How much station-keeping power is missing under a beam wind?\n\n'+omitted],
 15:['Which empty-hull strategy survives its failure case?',
  'The payload-exchange study is analysis, not design. What measurable advantage justifies giving up fail-safe float-up for a half-load hull with two-way rotors?\n\n'+
  'How would an approach at airspeed transfer load to the bag? How would variable displacement work with sealed cells? Can cryogenic ballast be produced within the available time and dry mass?\n\n'+
  'The current unheld phases and their signed force provide the requirement that each analysis must address.\n\n'+unheldText]
};
let questions=fs.readFileSync('docs/OPEN-QUESTIONS.md','utf8');
for(const [number,[title,body]] of Object.entries(questionBodies)) {
 const marker='<!-- energy:question-'+number+':start -->';
 const pos=questions.includes(marker)?questions.indexOf(marker):questions.indexOf('## '+number+'. ');
 const endMarker='<!-- energy:question-'+number+':end -->';
 const rest=questions.slice(pos+marker.length),next=rest.match(/\n## \d+\. /);
 const after=next?pos+marker.length+next.index+1:questions.length;
 let finish=questions.includes(endMarker)?questions.indexOf(endMarker)+endMarker.length:after;
 while(questions[finish]==='\n')finish++;
 questions=questions.slice(0,pos)+region('question-'+number,'## '+number+'. '+title+'\n\n'+body)+'\n'+questions.slice(finish);
}
const outputs={
 'research/analysis/energy-documents.json':JSON.stringify(record,null,2)+'\n',
 'docs/ENERGY-CLOSURE-2026-10.md':region('closure',closure),
 'docs/ENERGY-MODEL-2026-10.md':region('model',model),
 'sim/README.md':region('simulator',simulator.replace('[inertia table](../research/analysis/energy-motion.md)', 'inertia table (`research/analysis/energy-motion.md` in the repository)')),
 'docs/OPEN-QUESTIONS.md':questions,
 'docs/PHYSICS.md':oldPhysics.slice(0,start)+region('physics',physics)+'\n'+oldPhysics.slice(end).replace(/^\s+/,'')
};
if(process.argv.includes('--emit'))console.log(JSON.stringify(outputs));
else {for(const [path,text] of Object.entries(outputs))fs.writeFileSync(path,text);console.log('Generated the energy record and four bound documents.');}
