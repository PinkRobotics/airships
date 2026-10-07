/* Replay the exact decimal requirements and profiles that the document generator prints. */
import fs from 'node:fs';
import assert from 'node:assert/strict';
import {validateFleetDistanceRecord} from '../../research/analysis/fleet-distance-set.mjs';
import {CLASSES,MODES,planCycle,energySummary,REQUIREMENT_UNIT} from '../../sim/index.js?v=31a23fa3';
let checked=0;
const fleet=JSON.parse(fs.readFileSync('research/analysis/energy-fleet-distances.json'));
validateFleetDistanceRecord(fleet);
const feasible=JSON.parse(fs.readFileSync('research/analysis/energy-feasible.json'));
assert.deepEqual(feasible.distances,[fleet.min,fleet.median,fleet.max].map(km=>+km.toFixed(6)),
 'printed search distances must come from the current pinned record');
assert.deepEqual(feasible.distanceSelection.capture,fleet.capture,'printed search capture must match');
for(const key of ['source','min','median','max'])assert.equal(feasible.distanceSelection[key],fleet[key]);
function sameSummary(c,p,row){
 for(const [key,value] of Object.entries(energySummary(c,p)))assert.deepEqual(row[key],value,`stale printed energy field ${key}`);
}

for(const r of JSON.parse(fs.readFileSync('research/analysis/energy-requirements.json')).rows){
 const c=CLASSES[r.class],b=r.ballast,p=r.powerAndThrust;
 sameSummary(c,planCycle(c,MODES.balanced,r.km,null,{basis:r.basis}),r.baseline);
 if(b.feasible)sameSummary(c,planCycle(c,MODES.balanced,r.km,null,{basis:r.basis,ballastT:b.ballastT}),b);
 if(p.feasible)sameSummary(c,planCycle(c,MODES.balanced,r.km,null,{basis:r.basis,requiredBatteryMW:p.requiredBatteryMW,requiredRotorT:p.requiredRotorT}),p.verification);
 if(b.feasible){assert.ok(planCycle(c,MODES.balanced,r.km,null,{basis:r.basis,ballastT:+b.ballastT.toFixed(3)}).feasible);if(b.threshold)assert.ok(b.ballastT>=b.threshold&&b.ballastT-b.threshold<=REQUIREMENT_UNIT);checked++;}
 if(p.feasible){assert.ok(planCycle(c,MODES.balanced,r.km,null,{basis:r.basis,requiredBatteryMW:+p.requiredBatteryMW.toFixed(3),requiredRotorT:+p.requiredRotorT.toFixed(3)}).feasible);
  for(const s of [p.batterySearch,p.rotorSearch])assert.ok(s.printed>=s.threshold&&s.printed-s.threshold<=REQUIREMENT_UNIT);checked++;}
}
for(const path of ['energy-profiles','energy-feasible'])for(const r of JSON.parse(fs.readFileSync(`research/analysis/${path}.json`)).rows){
 sameSummary(CLASSES[r.class],planCycle(CLASSES[r.class],MODES.balanced,r.km,null,{basis:r.basis}),r.asDrawn);
 for(const b of [r.best,r.fullDeliveryBest].filter(Boolean)){
 const p=planCycle(CLASSES[b.class],MODES[b.mode],b.km,null,b.options);
 sameSummary(CLASSES[b.class],p,b);
 assert.ok(p.feasible,`${path}: infeasible row`);assert.ok(Math.abs(p.eCycleMWh-b.cycleMWh)<1e-8);assert.equal(p.deliveredT,b.deliveredT);assert.ok(Math.abs(p.cycleMin-b.cycleMin)<1e-8);
 for(const s of b.sensitivity||[]){const q=planCycle(CLASSES[b.class],MODES[b.mode],b.km,null,{...b.options,[s.parameter]:s.value});assert.equal(q.feasible,s.feasible);assert.ok(Math.abs(q.eCycleMWh-s.cycleMWh)<1e-8);}
 checked++;}
}
console.log('PASS printed requirement/profile replays:',checked);
