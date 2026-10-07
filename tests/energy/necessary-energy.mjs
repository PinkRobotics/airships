import fs from 'node:fs';
import assert from 'node:assert/strict';
import {CLASSES,MODES,planCycle,selectServedPlan} from '../../sim/index.js?v=816a54f9';
import {necessaryEnergy} from '../../research/analysis/energy-necessary.mjs';
import {proveMutations} from './diagnostic-mutations.mjs';
const captures=JSON.parse(fs.readFileSync('tests/energy/served-route-distances.json')).missions;
const fixture=n=>{
 const r=captures.find(q=>q.capture==='exercise'&&q.mission===n),c=CLASSES[r.class],m=MODES[r.mode];
 const p=planCycle(c,m,r.km,null,{...r.options,basis:'record'});
 assert.equal(p.feasible,true);return necessaryEnergy(c,m,p);
};
const eleven=fixture(11),twelve=fixture(12),inside=fixture(9);
assert.equal(eleven.nominalStorageMWh,20,'captured storage fixture stays at nominal 20 MWh');
assert.equal(twelve.nominalStorageMWh,20);
// BEGIN generated anchor necessary pins
for(const [q,energy,empty] of [[eleven,'41.8','127.5'],[twelve,'59.2','169.0']]){
// END generated anchor necessary pins
 assert.equal(q.cumulativeDrawMWh.toFixed(1),energy);
 assert.equal(q.emptyAtMin.toFixed(1),empty);
 assert.ok(q.shortageMWh>0,'captured cycle exceeds nominal storage');
 assert.equal(q.phases.at(-1).cumulativeDrawMWh,q.cumulativeDrawMWh,'chronology closes at the final phase');
}
assert.equal(inside.emptyAtMin,null,'one captured cycle stays inside nominal storage');
assert.equal(inside.shortageMWh,0);
const selected=selectServedPlan(CLASSES.P1000,400,null,'endurance');
assert.equal(selected.state,'ready','necessary energy does not alter the selector');
const long=necessaryEnergy(CLASSES.P1000,MODES[selected.mode],selected.plan);
// BEGIN generated anchor long pins
assert.equal(long.cumulativeDrawMWh.toFixed(1),'332.3');
// END generated anchor long pins
assert.equal(long.nominalStorageMWh,120);
console.log('PASS necessary-energy fixtures: '+JSON.stringify([eleven,twelve,inside,long].map(q=>({drawMWh:q.cumulativeDrawMWh,storageMWh:q.nominalStorageMWh,emptyAtMin:q.emptyAtMin,shortageMWh:q.shortageMWh}))));
await import('./printed-storage.mjs');
if(!process.env.DIAGNOSTIC_PROBE)proveMutations('tests/energy/necessary-energy.mjs',[
 {label:'planted storage change',file:'/sim/config.js',old:'genMW: 8, battMWh: 20,',replacement:'genMW: 8, battMWh: 80,',
  assertion:'captured storage fixture stays at nominal 20 MWh'}
]);
