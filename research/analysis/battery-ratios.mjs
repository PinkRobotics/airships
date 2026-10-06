/* Per-class battery allowance from current configuration and budget evidence. */
import fs from 'node:fs';
import {CLASSES,ledger,WORK_ALT_MSL} from '../../sim/index.js?v=68694086';
const budget=JSON.parse(fs.readFileSync('research/analysis/mass-budget.json'));
const referenceWhKg=budget.evidence.battery_wh_per_kg.demonstrated.value;
const floorWhKg=budget.evidence.battery_wh_per_kg.floor.value;
const classes=Object.fromEntries(Object.entries(CLASSES).map(([id,c])=>{
 const dryT=ledger(c,WORK_ALT_MSL).dryT,packT=c.battMWh*1000/referenceWhKg;
 return [id,{name:c.name,batteryMWh:c.battMWh,dryAllowanceT:dryT,
  mwhPerDryT:c.battMWh/dryT,referencePackT:packT,referencePackPctOfDry:100*packT/dryT,
  minimumPackWhKgForBatteryAlone:c.battMWh*1000/dryT, floorPackPctOfDry:100*c.battMWh*1000/floorWhKg/dryT,
  completeFloorT:budget.classes[id].cases.floor.totalT,
  completeFloorOverBy:budget.classes[id].cases.floor.overBy}];
}));
const record={generator:'research/analysis/battery-ratios.mjs',
 reference:{whKg:referenceWhKg,floorWhKg,source:'Chin et al. 2021, printed p. 2; mass-budget.json evidence/battery_wh_per_kg/demonstrated/value'},
 basis:'Configured energy capacity and simulated dry allowance; reference-pack mass is a scaling comparison, not a pack design.',classes};
const rows=Object.values(classes),n=(x,d)=>x.toLocaleString('en-CA',{minimumFractionDigits:d,maximumFractionDigits:d});
const table='| Class | Battery MWh | Dry allowance t | MWh/t dry | Battery-only minimum Wh/kg | Reference pack t | Pack / dry ratio | Complete floor t | Floor / dry |\n'+
 '|---|---|---|---|---|---|---|---|---|\n'+rows.map(r=>`| ${r.name} | ${n(r.batteryMWh,0)} | ${n(r.dryAllowanceT,0)} | ${n(r.mwhPerDryT,2)} | ${n(r.minimumPackWhKgForBatteryAlone,0)} | ${n(r.referencePackT,1)} | ${n(r.referencePackPctOfDry,1)}% | ${n(r.completeFloorT,1)} | ${n(r.completeFloorOverBy,2)}× |`).join('\n')+'\n';
const exceeds=rows.filter(r=>r.referencePackPctOfDry>100).map(r=>r.name).join(' and ');
const floorHeavy=rows.filter(r=>r.completeFloorOverBy>1).map(r=>r.name).join(', ');
const body=`At the ${referenceWhKg} Wh/kg reference pack density, the battery alone exceeds the dry allowance on ${exceeds}.\nThe per-class ratio of reference-pack mass to dry allowance is shown below.\nThe complete nominal floor budget exceeds the dry allowance on ${floorHeavy}, as its own totals show below.\n\n${table}\nThe complete floor uses the budget’s own evidence choices, including its ${floorWhKg} Wh/kg battery assumption; it is separate from the ${referenceWhKg} Wh/kg reference-pack comparison.\n\nThis comparison comes from [battery-ratios.json](../analysis/battery-ratios.json), configuration and the generated mass budget. It does not establish a buildable pack or a complete aircraft.\n`;
const outputs={'research/analysis/battery-ratios.json':JSON.stringify(record,null,2)+'\n'};
for(const file of ['research/notes/chin-2021-battery-cell-to-pack.md','docs/OPEN-QUESTIONS.md','research/reports/02-paper.md']){
 const text=fs.readFileSync(file,'utf8'),start='<!-- battery:ratios:start -->',end='<!-- battery:ratios:end -->';
 if(text.split(start).length!==2||text.split(end).length!==2)throw Error(file+': missing unique battery region');
 const compact='| Class | MWh/t dry | Reference pack / dry | Floor pack / dry | Complete floor t | Floor / dry |\n|---|---|---|---|---|---|\n'+rows.map(r=>`| ${r.name} | ${n(r.mwhPerDryT,2)} | ${n(r.referencePackPctOfDry,1)}% | ${n(r.floorPackPctOfDry,1)}% | ${n(r.completeFloorT,1)} | ${n(r.completeFloorOverBy,2)}× |`).join('\n')+'\n';
 const fileBody=file.startsWith('research/reports/')?body.replace(table,compact):body;
 const local=fileBody.replace('(../analysis/battery-ratios.json)',file.startsWith('docs/')?'(../research/analysis/battery-ratios.json)':'(../analysis/battery-ratios.json)');
 outputs[file]=text.slice(0,text.indexOf(start))+start+'\n'+local+end+text.slice(text.indexOf(end)+end.length);
}
const catalogueText=fs.readFileSync('research/sources.json','utf8');
const catalogue=JSON.parse(catalogueText);
const source=catalogue.sources.find(r=>r.id==='chin-2021-battery-cell-to-pack');
if(!source)throw Error('missing Chin catalogue entry');
source.whatWeTakeFromIt=`Configured MWh per tonne of dry allowance: ${rows.map(r=>`${r.name} ${n(r.mwhPerDryT,2)}`).join('; ')}. At the ${referenceWhKg} Wh/kg reference-pack density, pack masses are ${rows.map(r=>`${r.name} ${n(r.referencePackT,1)} t (${n(r.referencePackPctOfDry,1)}% of dry allowance)`).join('; ')}. At the floor's ${floorWhKg} Wh/kg assumption the pack fractions are ${rows.map(r=>`${r.name} ${n(r.floorPackPctOfDry,1)}%`).join('; ')}. The complete nominal floor budgets are ${rows.map(r=>`${r.name} ${n(r.completeFloorT,1)} t (${n(r.completeFloorOverBy,2)} times dry allowance)`).join('; ')}. This is a scaling comparison, not a pack design; analysis/battery-ratios.json and mass-budget.json own the numbers.`;
const sourceStart=catalogueText.indexOf('\"id\": \"chin-2021-battery-cell-to-pack\"');
const fieldStart=catalogueText.indexOf('\"whatWeTakeFromIt\": ',sourceStart)+'\"whatWeTakeFromIt\": '.length;
const fieldEnd=catalogueText.indexOf('\n',fieldStart);
if(sourceStart<0||fieldStart<sourceStart||fieldEnd<fieldStart)throw Error('missing unique catalogue field');
outputs['research/sources.json']=catalogueText.slice(0,fieldStart)+JSON.stringify(source.whatWeTakeFromIt)+','+catalogueText.slice(fieldEnd);
if(process.argv.includes('--emit'))console.log(JSON.stringify(outputs));
else if(process.argv.includes('--check')){
 const stale=Object.entries(outputs).filter(([p,v])=>!fs.existsSync(p)||fs.readFileSync(p,'utf8')!==v);
 if(stale.length){console.error('battery ratios RED: '+stale.map(([p])=>p).join(', '));process.exitCode=1;}
 else console.log('battery ratios: configuration, reference-pack fractions, three passages and source catalogue match');
}else{
 for(const [p,v] of Object.entries(outputs))fs.writeFileSync(p,v);
 for(const [id,r] of Object.entries(classes))console.log(`${id}: ${r.mwhPerDryT.toFixed(2)} MWh/t; reference pack ${r.referencePackPctOfDry.toFixed(1)}% of dry allowance; complete floor ${r.completeFloorT.toFixed(1)} t (${r.completeFloorOverBy.toFixed(2)}x)`);
}
