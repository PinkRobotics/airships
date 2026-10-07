/* Same selected controls and collecting area; remove only the solar bus input. */
import fs from 'node:fs';
import {CFG,CLASSES,MODES,planCycle,setConfig} from '../../sim/index.js';
import {writeGenerated} from './energy-output.mjs';
export function generateZeroSun(){
 const selected=JSON.parse(fs.readFileSync('research/analysis/energy-profiles.json')).rows;
 const prior={...CFG},rows=[];
 try {
  for(const r of selected){
   const b=r.best;if(!b)continue;
   const input={class:b.class,km:b.km,basis:r.basis,mode:b.mode,options:b.options};
   const c=CLASSES[b.class],m=MODES[b.mode];setConfig(prior);
   const current=planCycle(c,m,b.km,null,b.options);
   setConfig({solarWPerM2:0});const zeroSun=planCycle(c,m,b.km,null,b.options);
   const reading=p=>({feasible:p.feasible,worst:p.worst,cycleMin:p.cycleMin,suppliedMWh:p.eCycleMWh,bindingLimits:p.bindingLimits});
   rows.push({input,collectorM2:c.solarM2,averagedSolarMW:c.solarM2*prior.solarWPerM2/1e6,current:reading(current),zeroSun:reading(zeroSun)});
  }
 } finally { setConfig(prior); }
 return {generator:'research/analysis/energy-zero-sun.mjs',
  scope:'Replay every printed selected profile at the same hardware, collecting area, route, basis, mode and controls, changing only solarWPerM2 to zero. Averaged sunlight is credited to instantaneous bus supply before rotor thrust allocation. Unsupported energy is diagnostic supplied effort.',
  limitation:'No night search was run. This record does not show that no profile closes at night, and establishes no flight performance.',rows};
}
if(process.argv[1]?.endsWith('energy-zero-sun.mjs')){
 const result=generateZeroSun();writeGenerated('research/analysis/energy-zero-sun.json',JSON.stringify(result,null,2)+'\n');
 console.log(`${process.argv.includes('--check')?'PASS':'Generated'} zero-sunlight sensitivity: ${result.rows.length} selected profiles; ${result.rows.filter(r=>r.current.feasible&&!r.zeroSun.feasible).length} change from closes to fails; no night search`);
}
