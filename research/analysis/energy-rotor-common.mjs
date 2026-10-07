/* Shared record inputs for conditional rotor sensitivities; no controls are searched. */
import fs from 'node:fs';
const stamp=JSON.parse(fs.readFileSync(new URL('../../sim/version.json',import.meta.url))).version;
export const S=await import(new URL(`../../sim/index.js?v=${stamp}`,import.meta.url));
const {resolveClass}=await import('../../3d/model/config.js?v=ceaf69ab');
export const read=name=>JSON.parse(fs.readFileSync(`research/analysis/${name}.json`,'utf8'));
export const format=(v,digits=3)=>Number(v).toFixed(digits);
export function table(heads,rows){
 return '| '+heads.join(' | ')+' |\n|'+heads.map(()=>'---').join('|')+'|\n'+rows.map(r=>'| '+r.join(' | ')+' |').join('\n')+'\n';
}
export function geometry(){
 return Object.values(S.CLASSES).map(c=>{
  const d=resolveClass(c.id),footprintM2=d.primaryRotorStations*Math.PI*(d.primaryRotorDiameterM/2)**2;
  const rho=S.ledger(c,S.WORK_ALT_MSL).rho;
  return {class:c.id,stations:d.primaryRotorStations,bladeDisks:d.primaryRotorStations*d.rotorsPerStation,
   diameterM:d.primaryRotorDiameterM,pricedM2:c.diskM2,drawnSumM2:d.totalDiscAreaM2,footprintM2,rho,
   pricedCapT:S.rotorThrustLimitT(c,rho),footprintCapT:S.rotorThrustLimitT({...c,diskM2:footprintM2},rho),
   sameThrustHoverPowerRatio:Math.sqrt(c.diskM2/footprintM2)};
 });
}
export function profiles({full=false}={}){
 const out=[];
 for(const dataset of ['energy-profiles','energy-feasible'])for(const row of read(dataset).rows){
  for(const kind of full?['best','fullDeliveryBest']:['best']){
   const b=row[kind];if(!b)continue;
   const options={basis:row.basis,...b.options};
   out.push({dataset,class:row.class,km:row.km,basis:options.basis,kind,mode:b.mode,options});
  }
 }
 return out;
}
export function replay(q){
 const c=S.CLASSES[q.class],m=S.MODES[q.mode],p=S.planCycle(c,m,q.km,null,q.options);
 return {c,m,p};
}
export const label=q=>`${q.class} / ${format(q.km)} km / ${q.basis} / ${q.kind==='fullDeliveryBest'?'full delivery':'selected'}`;
