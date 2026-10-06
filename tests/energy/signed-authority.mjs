import assert from 'node:assert/strict';
import fs from 'node:fs';
import {CLASSES,MODES,planCycle,drawAt,cycleGeometry} from '../../sim/index.js?v=68694086';
import {accelerationAt,rotorAuthoritiesT,signedRotorDemand,ADDED_MASS_VALUES} from '../../research/analysis/energy-motion.mjs';
import {proveMutations} from './diagnostic-mutations.mjs';
const captures=JSON.parse(fs.readFileSync('tests/energy/served-route-distances.json')).missions;
function instant(mission,phase,progress){
 const r=captures.find(r=>r.capture==='exercise'&&r.mission===mission);
 assert.ok(r,'captured fixture exists');
 const c=CLASSES[r.class],mode=MODES[r.mode],p=planCycle(c,mode,r.km,null,{...r.options,basis:'record'});
 assert.equal(p.feasible,true,'fixture retains quasi-static closure');
 const s=drawAt(c,mode,p,phase,progress),a=accelerationAt(cycleGeometry(c,p),p,phase,progress),authority=rotorAuthoritiesT(c,p,s);
 return ADDED_MASS_VALUES.map(C=>signedRotorDemand(s,a,C,authority));
}
const upward=instant(9,'OUTBOUND_TRANSIT',.1495)[0];
assert.ok(upward.requiredRotorT<0,'upward fixture requires negative rotor thrust');
assert.ok(upward.gapT>1e-6,'signed screen flags unavailable upward authority');
assert.equal(upward.direction,'upward authority short');
assert.ok(Math.abs(upward.forceT)<upward.downwardReserveT,'withdrawn absolute comparison misses this instant');
assert.equal(upward.accelerationMps2.toFixed(4),'0.8135');
assert.equal(upward.forceT.toFixed(2),'30.29');
assert.equal(upward.upwardByRotorShedT.toFixed(2),'13.59');
assert.equal(upward.requiredRotorT.toFixed(2),'-16.70');
const downward=instant(0,'WATER_RELEASE',1);
for(const q of downward){
 assert.ok(q.forceT<0,'release deceleration has negative signed demand');
 assert.equal(q.direction,'downward authority short');
 assert.ok(q.requiredRotorT>q.availableRotorT,'release exceeds available downward thrust');
}
assert.equal(downward[0].gapT.toFixed(1),'1303.9');
assert.equal(downward[1].gapT.toFixed(1),'1837.5');
console.log('PASS signed fixtures: '+JSON.stringify({upward,downward}));
if(!process.env.DIAGNOSTIC_PROBE)proveMutations('tests/energy/signed-authority.mjs',[
 {label:'withdrawn absolute rule',file:'/research/analysis/energy-motion.mjs',
  old:'const gapT=Math.max(0,-requiredRotorT,requiredRotorT-authority.availableRotorT);',
  replacement:'const gapT=Math.max(0,Math.abs(forceT)-authority.downwardReserveT);',
  assertion:'signed screen flags unavailable upward authority'},
 {label:'flipped sign convention',file:'/research/analysis/energy-motion.mjs',
  old:'const requiredRotorT=s.owners.rotorT+s.unheldT-forceT;',
  replacement:'const requiredRotorT=s.owners.rotorT+s.unheldT+forceT;',
  assertion:'upward fixture requires negative rotor thrust'}
]);
