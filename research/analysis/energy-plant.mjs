/* Fixed-control ground-comparator sensitivities. No search or model-default change. */
import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
import {CLASSES,MODES,CFG,resetConfig,setConfig,planCycle,drawAt,cryoOnFrac} from '../../sim/index.js?v=01e992e3';
import {writeGenerated} from './energy-output.mjs';

export const PLANT_ENERGY_NOTE='The liquefaction dial is an assumed all-in energy figure with no all-in source in the repository. Intake, separation, compression, liquefaction, transfer and heat rejection have no specified complete boundary.';
export const COLD_READY_NOTE='Cold-ready assumption: production is credited from the first instant of the return leg as if the liquefier were already cold, with no startup, standby or restart cost. This is an assumption, not a result.';
export const readComparators=()=>JSON.parse(fs.readFileSync('research/analysis/plant-comparators.json'));
export function energyComparators(inputs=readComparators()){
 const s=inputs.stirlin;
 return [
  {...inputs.liquidAir,eMWhT:inputs.liquidAir.specificEnergyMWhT},
  {...s,eMWhT:s.inputKW/(s.usableLitresHour*inputs.liquidDensityKgL.value)}
 ];
}
function result(p){return {feasible:p.feasible,cycleMWh:p.eCycleMWh,makeT:p.ln2MakeT,returnMin:p.dur.RETURN_TRANSIT,worstUnheldT:p.worst.unheldT};}
export function computePlant({profiles,comparators=readComparators()}={}){
 const saved={...CFG};
 try{
  resetConfig();
  const baselineSpecificEnergy=CFG.eLN2,recoveredMWhT=CFG.eLN2*CFG.rtLN2;
  const scenarios=energyComparators(comparators);
  const records=profiles||Object.fromEntries(['energy-profiles','energy-feasible'].map(name=>[name,JSON.parse(fs.readFileSync(`research/analysis/${name}.json`))]));
  const tables={};
  for(const [name,data] of Object.entries(records)){
   tables[name]=[];
   for(const r of data.rows)for(const [selection,b] of [['cheapest found',r.best],['full delivery',r.fullDeliveryBest]]){
    if(!b)continue;
    const c=CLASSES[r.class],m=MODES[b.mode];
    resetConfig();const baselinePlan=planCycle(c,m,r.km,null,b.options),baseline=result(baselinePlan);
    const coldReady={returnMin:baselinePlan.dur.RETURN_TRANSIT,operatingMin:baselinePlan.dur.RETURN_TRANSIT*cryoOnFrac(c,m,baselinePlan),firstPositiveSampleLN2T:drawAt(c,m,baselinePlan,'RETURN_TRANSIT',1e-6).ln2};
    const sensitivity=scenarios.map(s=>{
     resetConfig();setConfig({eLN2:s.eMWhT,rtLN2:recoveredMWhT/s.eMWhT});
     return {id:s.id,label:s.label,specificEnergyMWhT:s.eMWhT,recoveryFraction:CFG.rtLN2,...result(planCycle(c,m,r.km,null,b.options))};
    });
    resetConfig();setConfig({cryoMul:0});
    const noLiquid=result(planCycle(c,m,r.km,null,b.options));
    tables[name].push({class:r.class,km:r.km,basis:r.basis,selection,mode:b.mode,options:b.options,baseline,sensitivity,coldReady,noLiquid});
   }
  }
  return {scope:'Sensitivities at each selected profile’s fixed controls, with unchanged plant input and no re-search. Ground comparators are neither airborne specifications nor lower bounds. Lost closure concerns these controls only.',assumption:PLANT_ENERGY_NOTE,baselineSpecificEnergy,recoveredMWhT,comparators,tables};
 }finally{resetConfig();setConfig(saved);}
}
const f=x=>Number(x).toFixed(3);
export function plantEnergyTable(name,record=JSON.parse(fs.readFileSync('research/analysis/energy-plant.json'))){
 let out='\n## Plant energy: fixed-control ground sensitivities\n\n'+PLANT_ENERGY_NOTE+'\n\n'+record.scope+'\n\n';
 out+=`Recovered work is held fixed at ${f(record.recoveredMWhT*1000)} kWh/t by changing the round-trip parameter inversely with the comparator energy. Baseline specific energy is ${f(record.baselineSpecificEnergy)} MWh/t.\n\n`;
 for(const s of energyComparators(record.comparators))out+=`${s.label}: ${f(s.eMWhT)} MWh/t; [source](../sources.json), ${s.locator}. `;
 out+='The StirLIN comparison excludes supplied cooling and uses the atmospheric usable-output row with a stipulated density conversion.\n\n';
 out+='| Class | km | Basis | Selection | Ground comparator | Specific energy MWh/t | Baseline / sensitivity MWh | Sensitivity worst unheld tf | Baseline / sensitivity closure |\n|---|---:|---|---|---|---:|---:|---:|---|\n';
 for(const r of record.tables[name])for(const s of r.sensitivity)out+=`| ${r.class} | ${f(r.km)} | ${r.basis} | ${r.selection} | ${s.label} | ${f(s.specificEnergyMWhT)} | ${f(r.baseline.cycleMWh)} / ${f(s.cycleMWh)} | ${f(s.worstUnheldT)} | ${r.baseline.feasible?'closes':'does not close'} / ${s.feasible?'closes':'does not close'} |\n`;
 return out;
}
export function plantDutyTable(name,record=JSON.parse(fs.readFileSync('research/analysis/energy-plant.json'))){
 let out='\n## No-liquid cold-readiness sensitivity\n\n'+COLD_READY_NOTE+'\n\n';
 out+='At each selected profile’s fixed controls, setting cryogenic capacity to zero removes both liquid production and its power draw. This flatters the force ledger; it is not a startup-energy calculation, a restart-time assumption or a new search. Lost closure concerns these controls only.\n\n';
 out+='| Class | km | Basis | Selection | Baseline return min | Baseline / no-liquid closure | No-liquid worst unheld tf | Baseline / no-liquid MWh |\n|---|---:|---|---|---:|---|---:|---:|\n';
 for(const r of record.tables[name])out+=`| ${r.class} | ${f(r.km)} | ${r.basis} | ${r.selection} | ${f(r.coldReady.returnMin)} | ${r.baseline.feasible?'closes':'does not close'} / ${r.noLiquid.feasible?'closes':'does not close'} | ${f(r.noLiquid.worstUnheldT)} | ${f(r.baseline.cycleMWh)} / ${f(r.noLiquid.cycleMWh)} |\n`;
 return out;
}
if(process.argv[1]&&fileURLToPath(import.meta.url)===fs.realpathSync(process.argv[1])){
 const body=JSON.stringify(computePlant(),null,2)+'\n';
 if(process.argv.includes('--emit'))console.log(JSON.stringify({'research/analysis/energy-plant.json':body}));
 else{writeGenerated('research/analysis/energy-plant.json',body);console.log('PASS plant energy sensitivities: selected controls, ground boundaries and fixed recovered work');}
}
