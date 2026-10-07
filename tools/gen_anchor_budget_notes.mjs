/* Refresh only the anchor-dependent current budget prose; retain dated corrections. */
import fs from 'node:fs';
const b=JSON.parse(fs.readFileSync('research/analysis/mass-budget.json'));
const c=b.classes.P100,r=c.rightSized.floor,h=r.hullThatCloses;
const fmt=(n,d=0)=>n.toLocaleString('en-US',{minimumFractionDigits:d,maximumFractionDigits:d});
const hull=x=>x.closes?`${fmt(x.volumeM3)} m³, ${x.lenM} × ${x.diaM} m`:'**never**';
const blocks={
 'nitrogen-table':`| | LN₂ made per cycle | energy | net of recovery | share of the current supplied cycle |
|---|---|---|---|---|
`+[['P100','P-100','1.83','0.824','0.658'],['P1000','P-1000','7.49','3.371','2.696'],['P10000','P-10000','21.12','9.504','7.604']].map(([id,name,n,e,net])=>`| ${name} | ${n} t | ${e} MWh | ${net} MWh | ${id==='P100'?'**':''}${fmt(b.classes[id].descentWithoutNitrogen.cycleSavingPct,1)}%${id==='P100'?'**':''} |`).join('\n'),
 question:`> Current anchor-reach correction to #11: the conditional equipment budget gives ${fmt(h['0.508'].volumeM3)} m³ and ${h['0.508'].lenM} m length, replacing the earlier 457,324 m³ after corrected reach changed energy-based battery sizing. This is not a checked design.`,
 'nitrogen-current':`The current table attributes ${fmt(c.descentWithoutNitrogen.cycleSavingPct,1)}% of the P-100's supplied prescribed-cycle energy to net liquefaction. The earlier 8.0% used 8.192 MWh; corrected anchor reach gives ${fmt(c.descentWithoutNitrogen.cycleMWhAsBuilt,3)} MWh, with the net nitrogen term still 0.658 MWh. This does not establish feasible flight.
The [earlier energy correction](../../docs/audit/26-10-02-energy-carry.md) retains its dated figures.`
};
const outputs={};
for(const [file,keys] of [['research/analysis/air-ballast.md',['nitrogen-table','nitrogen-current']],['docs/OPEN-QUESTIONS.md',['question']]]){
 let body=fs.readFileSync(file,'utf8');
 for(const key of keys){const start=`<!-- anchor-budget:${key}:start -->`,end=`<!-- anchor-budget:${key}:end -->`;
  if(body.split(start).length!==2||body.split(end).length!==2)throw new Error('Missing or duplicate current budget block: '+key);
  const a=body.indexOf(start)+start.length,z=body.indexOf(end,a);body=body.slice(0,a)+'\n'+blocks[key]+'\n'+body.slice(z);
 }
 outputs[file]=body;
 if(process.argv.includes('--emit'))continue;
 if(process.argv.includes('--check')){if(body!==fs.readFileSync(file,'utf8'))throw new Error('Stale current budget prose: '+file);}
 else fs.writeFileSync(file,body);
}
if(process.argv.includes('--emit'))console.log(JSON.stringify(outputs));
else console.log('PASS current anchor-dependent budget prose: three blocks; closure tables and floor remain checked by their existing producers; dated corrections retained.');
