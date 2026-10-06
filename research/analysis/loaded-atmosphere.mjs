/* Loaded-model density boundary at fixed reference pressure; no weather inference.
 * Run from the repository root. --check compares JSON and both qualified sentences. */
import fs from 'node:fs';
import {CLASSES,ISA,WORK_ALT_MSL,isaPressurePa,isaTemperatureK,ledger} from '../../sim/index.js?v=68694086';
const height=WORK_ALT_MSL,pressure=isaPressurePa(height),temperature=isaTemperatureK(height);
const classes=Object.fromEntries(Object.entries(CLASSES).map(([id,c])=>{
 const normal=ledger(c,height),loadedT=normal.dryT+c.payloadT;
 const density=loadedT*1000/c.dispM3,criticalTemperatureK=pressure/(ISA.R*density);
 const warmDensity=pressure/(ISA.R*(temperature+15)),warmLiftT=warmDensity*c.dispM3/1000;
 return [id,{name:c.name,loadedT,displacementM3:c.dispM3,criticalDensityKgM3:density,
  criticalTemperatureK,criticalDeltaK:criticalTemperatureK-temperature,
  referenceMarginPct:100*(normal.liftT/loadedT-1),
  atISAPlus15K:{densityKgM3:warmDensity,liftT:warmLiftT,marginPct:100*(warmLiftT/loadedT-1)}}];
}));
const data={generator:'research/analysis/loaded-atmosphere.mjs',
 method:'Loaded dry allowance plus water; no nitrogen ballast. Neutral when density times displacement equals loaded mass. Temperature counterfactual holds reference pressure fixed; not a weather observation or a complete off-standard atmosphere.',
 reference:{altitudeM:height,pressurePa:pressure,temperatureK:temperature,gasConstantJkgK:ISA.R},classes};
const thresholds=Object.values(classes).map(r=>`${r.name}: ${r.criticalDensityKgM3.toFixed(6)} kg/m³, reference temperature +${r.criticalDeltaK.toFixed(2)} K`).join('; ');
const warm=Object.values(classes).map(r=>`${r.name} ${r.atISAPlus15K.marginPct.toFixed(2)}%`).join('; ');
const physics=`**FAIL-SAFE FLOAT-UP SETS THE DISPLACEMENT.** The requirement, decided 2026-08-09, is that a
hull be positively buoyant at its working altitude *while fully loaded with water and unable
to drop it*. Nitrogen ballast is excluded from that mass because it vents to atmosphere in
seconds; water is the load a ship can be stuck with. In the reference atmosphere, the working altitude
h_t + \`ALT.cruise\` = 2,500 m MSL is the thinnest air in the nominal cycle, so sizing there
covers that reference cycle. At the working-altitude reference pressure of ${pressure.toFixed(2)} Pa,
loaded neutrality occurs at ${thresholds}. Float-up requires air denser than these boundaries;
at the same pressure, warmer air beyond them removes the margin. ISA+15 K gives ${warm}.
These are fixed-pressure model scenarios, not an established weather envelope; the
[generated boundary record](../research/analysis/loaded-atmosphere.json) holds the calculation.
At ρ_work = 0.95686 kg/m³ a loaded tonne needs 2,194.7 m³ of
displacement with a 5% margin; the classes carry 2,200 m³ per tonne of payload:\n`;
const question=`1. float up within the flight model's reference-atmosphere assumption (#1): a loaded model rises
   only when air density exceeds its computed boundary at ${height.toLocaleString('en-CA')} m MSL
   (${thresholds}). These temperature offsets hold reference pressure at ${pressure.toFixed(2)} Pa;
   they do not establish a weather envelope. See the [generated boundaries](../research/analysis/loaded-atmosphere.json);
2. recharge on solar alone;
3. liquefy enough nitrogen to make itself heavy enough to descend **with no rotor
   authority at all**; and
4. land empty on ballast alone.\n`;
const outputs={'research/analysis/loaded-atmosphere.json':JSON.stringify(data,null,2)+'\n'};
for(const [file,key,body] of [['docs/PHYSICS.md','physics',physics],['docs/OPEN-QUESTIONS.md','recovery',question]]){
 const text=fs.readFileSync(file,'utf8'),start=`<!-- atmosphere:${key}:start -->`,end=`<!-- atmosphere:${key}:end -->`;
 if(text.split(start).length!==2||text.split(end).length!==2)throw Error(file+': missing unique atmosphere region');
 outputs[file]=text.slice(0,text.indexOf(start))+start+'\n'+body+end+text.slice(text.indexOf(end)+end.length);
}
if(process.argv.includes('--emit'))console.log(JSON.stringify(outputs));
else if(process.argv.includes('--check')){
 const stale=Object.entries(outputs).filter(([p,v])=>!fs.existsSync(p)||fs.readFileSync(p,'utf8')!==v);
 if(stale.length){console.error('atmosphere RED: '+stale.map(([p])=>p).join(', '));process.exitCode=1;}
 else console.log('atmosphere: per-class loaded boundaries and both reference-atmosphere statements match');
}else{
 for(const [p,v] of Object.entries(outputs))fs.writeFileSync(p,v);
 for(const [id,r] of Object.entries(classes))console.log(`${id}: neutral density ${r.criticalDensityKgM3.toFixed(9)} kg/m3; reference +${r.criticalDeltaK.toFixed(2)} K; reference margin +${r.referenceMarginPct.toFixed(2)}%; ISA+15 K ${r.atISAPlus15K.marginPct.toFixed(2)}%`);
}
