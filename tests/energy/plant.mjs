/* Historical test controls replayed with the current hull-centre cable datum. */
/* Reviewer values are oracle values on the reviewed base, not current publications. */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {computePlant,readComparators} from '../../research/analysis/energy-plant.mjs';
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-6,`${a} != oracle ${b}`);
const fixture=JSON.parse(fs.readFileSync(new URL('plant-oracle-controls.json',import.meta.url)));
const record=computePlant({profiles:{oracle:fixture}});
const oracle={P100:[[true,5.049544,0],[true,5.114471,0]],P1000:[[true,26.035382,0],[true,26.465349,0]],P10000:[[true,187.632422,0],[true,188.017148,0]]};
for(const r of record.tables.oracle){
 assert.equal(r.baseline.feasible,true);
 for(const [i,s] of r.sensitivity.entries()){
  const [closes,mwh,gap]=oracle[r.class][i];assert.equal(s.feasible,closes);near(s.cycleMWh,mwh);near(s.worstUnheldT,gap);
  near(s.specificEnergyMWhT*s.recoveryFraction,record.recoveredMWhT);
 }
}
const inputs=readComparators();inputs.liquidAir.specificEnergyMWhT*=1.1;
const planted=computePlant({profiles:{oracle:fixture},comparators:inputs});
let refused=false;
try{near(planted.tables.oracle[1].sensitivity[0].cycleMWh,oracle.P1000[0][1]);}catch{refused=true;}
assert.ok(refused,'planted comparator change must fail the independent oracle');
console.log('RED planted comparator energy: oracle refused changed input');
console.log('GREEN plant energy: three base classes, two ground comparators; recovered work fixed');
