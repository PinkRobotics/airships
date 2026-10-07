/* Lossless recovery quotients and analytic ground-tank storage sensitivities. */
import fs from 'node:fs';
import {fileURLToPath} from 'node:url';
import {CLASSES,CFG,ledger,TERRAIN_MSL} from '../../sim/index.js?v=01e992e3';
import {writeGenerated} from './energy-output.mjs';

export function storageBalance(makeTDay,capacityT,targetT,rateDay){
 if(!(makeTDay>0&&capacityT>0&&targetT>=0&&rateDay>=0))throw new Error('invalid storage inputs');
 const netTDay=makeTDay-capacityT*rateDay;
 const equilibriumT=rateDay>0?makeTDay/rateDay:null;
 const fits=targetT<=capacityT;
 const fixedDays=targetT===0?0:fits&&netTDay>0?targetT/netTDay:null;
 const proportionalDays=targetT===0?0:!fits?null:rateDay===0?targetT/makeTDay:
  equilibriumT>targetT?-Math.log1p(-targetT/equilibriumT)/rateDay:null;
 return {fixed:{lossTDay:capacityT*rateDay,netTDay,days:fixedDays},
  proportional:{equilibriumT,capacityLimitedEquilibriumT:Math.min(capacityT,equilibriumT??capacityT),days:proportionalDays}};
}
export function computeStorage(){
 const inputs=JSON.parse(fs.readFileSync('research/analysis/plant-comparators.json'));
 const rows=Object.values(CLASSES).map(c=>{
  const solarMW=c.solarM2*CFG.solarWPerM2/1e6,hotelMW=c.genMW*.02,netMW=solarMW-hotelMW;
  const targetT=ledger(c,TERRAIN_MSL).surplusT,makeTDay=netMW*24/CFG.eLN2;
  return {class:c.id,solarMW,hotelMW,netMW,capacityT:c.ln2CapT,targetT,makeTDay,
   solarFractionRatedPct:100*netMW/c.cryoMW,losslessGroundDays:targetT/makeTDay,
   losslessTankDays:c.ln2CapT/makeTDay,maximumFixedLossPctCapacityDay:100*makeTDay/c.ln2CapT,
   sensitivity:inputs.storage.map(s=>({...s,...storageBalance(makeTDay,c.ln2CapT,targetT,s.lossFractionDay)}))};
 });
 return {scope:'Ground-tank comparators at the model’s fixed day-average solar, hotel load, plant energy and tank capacity; no operating schedule or new design is searched. Neither loss rate is an airborne property. Recovery is not shown impossible or established.',
  equations:{lossless:'target / make',fixed:'dM/dt = make - rate * capacity, bounded below by empty inventory',proportional:'dM/dt = make - rate * M, starting empty and limited by installed capacity'},
  requirement:'Fixed loss must be below the listed energy-based limit for positive accumulation. Equality leaves no net make. The limit excludes startup, cold maintenance, buffering and conversion losses; it is a requirement, not a selected tank property.',rows};
}
const f=x=>x==null?'not reached':Number(x).toFixed(3);
export function storageTables(record=JSON.parse(fs.readFileSync('research/analysis/energy-storage.json'))){
 let out='### Solar storage-balance requirement and ground sensitivities\n\n'+record.scope+'\n\n'+record.requirement+'\n\n';
 out+='| Class | Solar make t/day | Make / rated plant input % | Largest fixed loss % of capacity/day | Lossless energy quotient to ground ballast, days |\n|---|---:|---:|---:|---:|\n';
 for(const r of record.rows)out+=`| ${r.class} | ${f(r.makeTDay)} | ${f(r.solarFractionRatedPct)} | ${f(r.maximumFixedLossPctCapacityDay)} | ${f(r.losslessGroundDays)} |\n`;
 out+='\nStarting empty, the fixed-loss interpretation subtracts the stated share of installed capacity every day; the proportional interpretation subtracts that share of current inventory. The analytic balance uses constant average make, bounds inventory by tank capacity, and supplies no cold-state or power-buffering schedule. “Not reached” means no finite crossing in that stipulated balance.\n\n';
 for(const s of record.rows[0].sensitivity)out+=`${s.label}: ${f(s.lossFractionDay*100)}%/day; [published source](${s.url}), ${s.locator}. `;
 out+='These are ground-tank comparator rates, not airborne predictions.\n\n';
 out+='| Class | Ground tank comparator | Loss %/day | Fixed net t/day | Fixed loss days to target | Capacity-limited proportional equilibrium t | Inventory-proportional days to target |\n|---|---|---:|---:|---:|---:|---:|\n';
 for(const r of record.rows)for(const s of r.sensitivity)out+=`| ${r.class} | ${s.label} | ${f(s.lossFractionDay*100)} | ${f(s.fixed.netTDay)} | ${f(s.fixed.days)} | ${f(s.proportional.capacityLimitedEquilibriumT)} | ${f(s.proportional.days)} |\n`;
 return out;
}
if(process.argv[1]&&fileURLToPath(import.meta.url)===fs.realpathSync(process.argv[1])){
 const body=JSON.stringify(computeStorage(),null,2)+'\n';
 if(process.argv.includes('--emit'))console.log(JSON.stringify({'research/analysis/energy-storage.json':body}));
 else{writeGenerated('research/analysis/energy-storage.json',body);console.log('PASS solar storage: lossless quotients, allowable fixed loss and both ground-loss balances');}
}
