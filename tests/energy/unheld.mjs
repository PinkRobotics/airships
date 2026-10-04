/* Independent completeness and numeric replay of the printed phase table. */
import fs from 'node:fs';
import assert from 'node:assert/strict';
import {CLASSES,MODES,PHASES,planCycle,drawAt,FORCE_TOL,LIMIT_STEPS} from '../../sim/index.js?v=93744380';
const data=JSON.parse(fs.readFileSync('research/analysis/energy-unheld.json'));
assert.equal(data.rows.length,12);let count=0;
for(const r of data.rows){
 const c=CLASSES[r.class],m=MODES.balanced,p=planCycle(c,m,r.km,null,{basis:r.basis});
 assert.equal(p.feasible,r.feasible);
 for(const [phase] of PHASES){
  // Independent 20,001-point probe plus golden-section refinement. It does
  // not consume the model's extrema or repeat the generator's verdict mesh.
  const M=20000, f=x=>drawAt(c,m,p,phase,x).unheldT;
  let bi=0,bv=f(0);
  for(let i=1;i<=M;i++){const v=f(i/M);if(Math.abs(v)>Math.abs(bv)){bi=i;bv=v;}}
  let a=Math.max(0,bi-1)/M,b=Math.min(M,bi+1)/M;
  const ratio=(Math.sqrt(5)-1)/2;
  for(let k=0;k<200&&b-a>1e-12;k++){
   const x=b-ratio*(b-a),y=a+ratio*(b-a);
   if(Math.abs(f(x))>Math.abs(f(y)))b=y;else a=x;
  }
  const x=(a+b)/2,refined=f(x),peak=Math.max(Math.abs(bv),Math.abs(refined));
  const probe=drawAt(c,m,p,phase,Math.abs(refined)>Math.abs(bv)?x:bi/M);
  const fails=peak>FORCE_TOL*Math.max(1,Math.abs(probe.surplusT));
  const records=r.phases.filter(s=>s.phase===phase);assert.equal(records.length,fails?1:0,`${r.class}/${r.km}/${r.basis}: missing or extra ${phase}`);
  for(const row of records){
   const s=drawAt(c,m,p,phase,row.progress);
   assert.equal(s.unheldT,row.unheldT);assert.equal(s.airV,row.airspeedMps);assert.equal(s.vz,row.verticalSpeedMps);assert.deepEqual(s.limits,row.limits);
   assert.ok(peak<=Math.abs(row.unheldT)+1e-6,`${r.class}/${r.km}/${r.basis} ${phase}: phase peak understated (${row.unheldT} vs refined ${peak})`);
   count++;
  }
 }
}
const named=planCycle(CLASSES.P100,MODES.endurance,15,null,{basis:'favourable'});
assert.equal(named.feasible,false);assert.ok(Math.abs(named.worst.unheldT-2.041455599)<1e-8);
console.log(`PASS unheld table: ${data.rows.length} rows, ${count} failing phases; named case stays infeasible, ${named.worst.unheldT.toFixed(9)} t unheld.`);
