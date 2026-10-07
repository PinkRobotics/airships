/* Refresh numeric fixture pins after replaying the selected route controls.
 * Sign, authority-bound and mutation assertions in the test remain unchanged.
 * Expected force and demand are calculated here without signedRotorDemand. */
import fs from 'node:fs';
import {CLASSES,MODES,planCycle,drawAt,cycleGeometry} from '../sim/index.js';
import {accelerationAt,rotorAuthoritiesT,ADDED_MASS_VALUES} from '../research/analysis/energy-motion.mjs';
const file='tests/energy/signed-authority.mjs';
const captures=JSON.parse(fs.readFileSync('tests/energy/served-route-distances.json')).missions;
function instant(mission,phase,progress){
  const row=captures.find(r=>r.capture==='exercise'&&r.mission===mission);
  if(!row)throw new Error('Missing invented exercise fixture');
  const c=CLASSES[row.class],m=MODES[row.mode];
  const p=planCycle(c,m,row.km,null,{...row.options,basis:'record'});
  if(!p.feasible)throw new Error('Fixture no longer closes quasi-statically');
  const s=drawAt(c,m,p,phase,progress),a=accelerationAt(cycleGeometry(c,p),p,phase,progress);
  const authority=rotorAuthoritiesT(c,p,s);
  return ADDED_MASS_VALUES.map(C=>{
    const forceT=(s.massT+C*s.led.liftT)*a/9.81;
    const required=s.owners.rotorT+s.unheldT-forceT;
    return {accelerationMps2:a,forceT,upwardByRotorShedT:s.owners.rotorT,requiredRotorT:required,
      gapT:Math.max(0,-required,required-authority.availableRotorT)};
  });
}
const up=instant(9,'OUTBOUND_TRANSIT',.1495)[0],down=instant(0,'WATER_RELEASE',1);
const blocks={upward:[
  `assert.equal(upward.accelerationMps2.toFixed(4),'${up.accelerationMps2.toFixed(4)}');`,
  `assert.equal(upward.forceT.toFixed(2),'${up.forceT.toFixed(2)}');`,
  `assert.equal(upward.upwardByRotorShedT.toFixed(2),'${up.upwardByRotorShedT.toFixed(2)}');`,
  `assert.equal(upward.requiredRotorT.toFixed(2),'${up.requiredRotorT.toFixed(2)}');`
],downward:down.map((q,i)=>`assert.equal(downward[${i}].gapT.toFixed(1),'${q.gapT.toFixed(1)}');`)};
// Stored-energy pins come from the owning generated accounting record. Nominal
// storage, chronology, shortage and storage-mutation assertions remain fixed.
const energy=JSON.parse(fs.readFileSync('research/analysis/energy-necessary.json'));
const energyFixture=n=>{
  const row=energy.servedMissions.find(r=>r.capture==='exercise'&&r.mission===n);
  if(!row)throw new Error('Missing necessary-energy fixture record');
  return row.accounting;
};
const eleven=energyFixture(11),twelve=energyFixture(12);
const long=energy.routes.find(r=>r.class==='P1000'&&r.km===400&&r.profile==='ready selector');
if(!long)throw new Error('Missing long-route energy record');
const necessaryBlocks={necessary:[`for(const [q,energy,empty] of [[eleven,'${eleven.cumulativeDrawMWh.toFixed(1)}','${eleven.emptyAtMin.toFixed(1)}'],[twelve,'${twelve.cumulativeDrawMWh.toFixed(1)}','${twelve.emptyAtMin.toFixed(1)}']]){`],
  long:[`assert.equal(long.cumulativeDrawMWh.toFixed(1),'${long.accounting.cumulativeDrawMWh.toFixed(1)}');`]};
let body=fs.readFileSync(file,'utf8');
for(const [name,lines] of Object.entries(blocks)){
  const start=`// BEGIN generated anchor ${name} pins`,end=`// END generated anchor ${name} pins`;
  if(body.split(start).length!==2||body.split(end).length!==2)throw new Error('Ambiguous pin markers');
  const a=body.indexOf(start),b=body.indexOf(end,a)+end.length;
  body=body.slice(0,a)+[start,...lines,end].join('\n')+body.slice(b);
}
const necessaryFile='tests/energy/necessary-energy.mjs';
let necessaryBody=fs.readFileSync(necessaryFile,'utf8');
for(const [name,lines] of Object.entries(necessaryBlocks)){
  const start=`// BEGIN generated anchor ${name} pins`,end=`// END generated anchor ${name} pins`;
  if(necessaryBody.split(start).length!==2||necessaryBody.split(end).length!==2)throw new Error('Ambiguous necessary-energy pin markers');
  const a=necessaryBody.indexOf(start),b=necessaryBody.indexOf(end,a)+end.length;
  necessaryBody=necessaryBody.slice(0,a)+[start,...lines,end].join('\n')+necessaryBody.slice(b);
}
if(process.argv.includes('--check')){
  if(body!==fs.readFileSync(file,'utf8')||necessaryBody!==fs.readFileSync(necessaryFile,'utf8'))throw new Error('Stale anchor diagnostic pins');
  console.log('PASS anchor diagnostic pins: six independent signed-demand pins and five owning-record energy pins');
}else{
  fs.writeFileSync(file,body);fs.writeFileSync(necessaryFile,necessaryBody);
  console.log('Refreshed eleven anchor diagnostic pins; sign, bound, chronology, storage and mutation checks unchanged');
}
