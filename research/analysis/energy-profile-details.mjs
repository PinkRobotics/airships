import {writeGenerated} from './energy-output.mjs';
/* Fast replay of selected rows; it performs no search. */
import fs from 'node:fs';
import {CLASSES,MODES,planCycle} from '../../sim/index.js?v=b3bc1c96';
import {omittedInertia} from './energy-motion.mjs';
export function profileDetails(b){
 if(!b)return;
 const c=CLASSES[b.class],m=MODES[b.mode],p=planCycle(c,m,b.km,null,b.options);
 if(!p.feasible)throw new Error('selected profile no longer closes');
 b.inertia=omittedInertia(c,m,p);
 b.sensitivity=['verticalCd','rotorEfficiency','clMax'].flatMap(key=>(key==='verticalCd'?[0,1,2]:key==='rotorEfficiency'?[.55,.70]:[.5,1,1.5]).map(value=>{
  const q=planCycle(c,m,b.km,null,{...b.options,[key]:value});
  return {parameter:key,value,feasible:q.feasible,worst:q.worst,cycleMin:q.cycleMin,cycleMWh:q.eCycleMWh};
 }));
}
if(process.argv[1]?.endsWith('energy-profile-details.mjs'))for(const name of ['energy-profiles','energy-feasible']){
 const path=`research/analysis/${name}.json`,data=JSON.parse(fs.readFileSync(path));
 for(const row of data.rows)for(const b of [row.best,row.fullDeliveryBest])profileDetails(b);
 writeGenerated(path,JSON.stringify(data,null,2)+'\n');
 console.log('Replayed profile details:',name);
}
