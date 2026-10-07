/* Historical test controls replayed with the current hull-centre cable datum. */
/* Reviewer cold-readiness oracles on fixed reviewed-base controls, never current figures. */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {computePlant,COLD_READY_NOTE} from '../../research/analysis/energy-plant.mjs';
const fixture=JSON.parse(fs.readFileSync(new URL('plant-oracle-controls.json',import.meta.url)));
const record=computePlant({profiles:{oracle:fixture}});
const oracle={P100:{closes:true,gap:0},P1000:{closes:true,gap:0},P10000:{closes:true,gap:0}};
for(const r of record.tables.oracle){
 assert.equal(r.noLiquid.feasible,oracle[r.class].closes);
 assert.ok(Math.abs(r.noLiquid.worstUnheldT-oracle[r.class].gap)<1e-6);
 assert.equal(r.noLiquid.makeT,0);
 assert.ok(r.noLiquid.cycleMWh<r.baseline.cycleMWh,'zero production also removes plant draw');
 assert.ok(r.coldReady.firstPositiveSampleLN2T>0,'already-cold production at the first positive sample');
}
assert.match(COLD_READY_NOTE,/assumption/);
assert.match(COLD_READY_NOTE,/no startup, standby or restart cost/);
console.log('GREEN no-liquid oracles: all three classes close at fixed controls with the hull-centre cable datum');
