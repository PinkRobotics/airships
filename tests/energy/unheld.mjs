/* Independent completeness and numeric replay of the printed phase table. */
import fs from 'node:fs';
import assert from 'node:assert/strict';
import {CLASSES,MODES,PHASES,planCycle,drawAt,FORCE_TOL,LIMIT_STEPS} from '../../sim/index.js';
const data=JSON.parse(fs.readFileSync('research/analysis/energy-unheld.json'));
assert.equal(data.rows.length,12);let count=0;
for(const r of data.rows){
 const c=CLASSES[r.class],m=MODES.balanced,p=planCycle(c,m,r.km,null,{basis:r.basis});
 assert.equal(p.feasible,r.feasible);
 for(const [phase] of PHASES){
  let fails=false;
  for(let i=0;i<=LIMIT_STEPS;i++){
   const s=drawAt(c,m,p,phase,i/LIMIT_STEPS);
   fails ||= Math.abs(s.unheldT)>FORCE_TOL*Math.max(1,Math.abs(s.surplusT));
  }
  const records=r.phases.filter(s=>s.phase===phase);assert.equal(records.length,fails?1:0,`${r.class}/${r.km}/${r.basis}: missing or extra ${phase}`);
  for(const row of records){
   const s=drawAt(c,m,p,phase,row.progress);
   assert.equal(s.unheldT,row.unheldT);assert.equal(s.airV,row.airspeedMps);assert.equal(s.vz,row.verticalSpeedMps);assert.deepEqual(s.limits,row.limits);
   for(let i=0;i<=LIMIT_STEPS;i++)assert.ok(Math.abs(drawAt(c,m,p,phase,i/LIMIT_STEPS).unheldT)<=Math.abs(row.unheldT)+1e-9,'phase peak understated');
   count++;
  }
 }
}
const named=planCycle(CLASSES.P100,MODES.endurance,15,null,{basis:'favourable'});
assert.equal(named.feasible,false);assert.ok(Math.abs(named.worst.unheldT-1.686282096)<1e-8);
console.log(`PASS unheld table: ${data.rows.length} rows, ${count} failing phases; named case stays infeasible, ${named.worst.unheldT.toFixed(9)} t unheld.`);
