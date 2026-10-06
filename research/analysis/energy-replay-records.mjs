/* Refresh diagnostics and selected controls without claiming a new optimum.
 * Run the slow energy-feasible.mjs search when a profile shape changes. */
import fs from 'node:fs';
import {CLASSES,MODES,planCycle,energySummary,closureRequirements} from '../../sim/index.js?v=816a54f9';
import {profileDetails} from './energy-profile-details.mjs';
import {writeGenerated} from './energy-output.mjs';
const load=name=>JSON.parse(fs.readFileSync(`research/analysis/${name}.json`));
const save=(name,data)=>writeGenerated(`research/analysis/${name}.json`,JSON.stringify(data,null,2)+'\n');
const requirements=load('energy-requirements');
requirements.rows=requirements.rows.map(r=>closureRequirements(CLASSES[r.class],MODES.balanced,r.km,r.basis));
save('energy-requirements',requirements);
for(const name of ['energy-profiles','energy-feasible']){
 const data=load(name);
 for(const r of data.rows){
  const c=CLASSES[r.class];
  r.asDrawn=energySummary(c,planCycle(c,MODES.balanced,r.km,null,{basis:r.basis}));
  for(const b of [r.best,r.fullDeliveryBest].filter(Boolean)){
   const p=planCycle(c,MODES[b.mode],r.km,null,b.options);
   if(!p.feasible)throw new Error(`selected controls no longer close: ${r.class}/${r.km}/${r.basis}`);
   Object.assign(b,energySummary(c,p));profileDetails(b);
  }
 }
 save(name,data);
}
console.log('Replayed requirements, diagnostic summaries and selected profile controls; no new search claimed.');
