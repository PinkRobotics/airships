/* Replay the exact decimal requirements and profiles that the document generator prints. */
import fs from 'node:fs';
import assert from 'node:assert/strict';
import {CLASSES,MODES,planCycle,REQUIREMENT_UNIT} from '../../sim/index.js';
let checked=0;
for(const r of JSON.parse(fs.readFileSync('research/analysis/energy-requirements.json')).rows){
 const c=CLASSES[r.class],b=r.ballast,p=r.powerAndThrust;
 if(b.feasible){assert.ok(planCycle(c,MODES.balanced,r.km,null,{basis:r.basis,ballastT:+b.ballastT.toFixed(3)}).feasible);if(b.threshold)assert.ok(b.ballastT>=b.threshold&&b.ballastT-b.threshold<=REQUIREMENT_UNIT);checked++;}
 if(p.feasible){assert.ok(planCycle(c,MODES.balanced,r.km,null,{basis:r.basis,requiredBatteryMW:+p.requiredBatteryMW.toFixed(3),requiredRotorT:+p.requiredRotorT.toFixed(3)}).feasible);
  for(const s of [p.batterySearch,p.rotorSearch])assert.ok(s.printed>=s.threshold&&s.printed-s.threshold<=REQUIREMENT_UNIT);checked++;}
}
for(const path of ['energy-profiles','energy-feasible'])for(const r of JSON.parse(fs.readFileSync(`research/analysis/${path}.json`)).rows){
 for(const b of [r.best,r.fullDeliveryBest].filter(Boolean)){
 const p=planCycle(CLASSES[b.class],MODES[b.mode],b.km,null,b.options);
 assert.ok(p.feasible,`${path}: infeasible row`);assert.ok(Math.abs(p.eCycleMWh-b.cycleMWh)<1e-8);assert.equal(p.deliveredT,b.deliveredT);assert.ok(Math.abs(p.cycleMin-b.cycleMin)<1e-8);
 for(const s of b.sensitivity||[]){const q=planCycle(CLASSES[b.class],MODES[b.mode],b.km,null,{...b.options,[s.parameter]:s.value});assert.equal(q.feasible,s.feasible);assert.ok(Math.abs(q.eCycleMWh-s.cycleMWh)<1e-8);}
 checked++;}
}
console.log('PASS printed requirement/profile replays:',checked);
