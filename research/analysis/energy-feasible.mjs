/* Slow profile generator, deliberately outside make check. Four worker threads at most. */
import fs from 'node:fs';
import {Worker,isMainThread,parentPort,workerData} from 'node:worker_threads';
import {CLASSES,MODES,cheapestFeasible,closureRequirements,PROFILE_SEARCH,planCycle} from '../../sim/index.js?v=01e992e3';
import {profileDetails} from './energy-profile-details.mjs';
import {validateFleetDistanceRecord} from './fleet-distance-set.mjs';
import {writeGenerated} from './energy-output.mjs';
if(!isMainThread){
  const {kind,class:id,km,basis}=workerData,c=CLASSES[id];
  if(kind==='requirement')parentPort.postMessage(closureRequirements(c,MODES.balanced,km,basis));
  else {
    const r=cheapestFeasible(c,km,basis);
    for(const b of [r.best,r.fullDeliveryBest])profileDetails(b);
    parentPort.postMessage({class:id,km,basis,...r});
  }
}else{
  const fleet=JSON.parse(fs.readFileSync('research/analysis/energy-fleet-distances.json'));
  validateFleetDistanceRecord(fleet);
  const distances=[fleet.min,fleet.median,fleet.max].map(x=>+x.toFixed(6));
  const jobs=[];
  for(const id of Object.keys(CLASSES))for(const km of [15,60])for(const basis of ['record','favourable'])jobs.push({kind:'requirement',class:id,km,basis});
  for(const id of Object.keys(CLASSES))for(const km of [...new Set([15,60,...distances])])for(const basis of ['record','favourable'])jobs.push({kind:'profile',class:id,km,basis});
  const results=new Array(jobs.length);let cursor=0;
  async function run(){while(cursor<jobs.length){const i=cursor++,job=jobs[i];results[i]=await new Promise((resolve,reject)=>{
    const w=new Worker(new URL(import.meta.url),{workerData:job});w.once('message',resolve);w.once('error',reject);w.once('exit',code=>{if(code)reject(new Error(`worker exit ${code}`));});
  });console.log(`${i+1}/${jobs.length} ${job.kind} ${job.class}/${job.km}/${job.basis}`);}}
  await Promise.all(Array.from({length:4},run));
  const requirements=results.filter((_,i)=>jobs[i].kind==='requirement');
  const profiles=results.filter((_,i)=>jobs[i].kind==='profile');
  writeGenerated('research/analysis/energy-requirements.json',JSON.stringify({rows:requirements},null,2)+'\n');
  writeGenerated('research/analysis/energy-profiles.json',JSON.stringify({space:PROFILE_SEARCH,rows:profiles.filter(r=>[15,60].includes(r.km))},null,2)+'\n');
  const table={defaultBasis:'record',otherBasis:'favourable',distances,
    distanceSelection:{source:fleet.source,capture:fleet.capture,min:fleet.min,median:fleet.median,max:fleet.max,reason:'Minimum, median and maximum flown legs of the bundled invented exercise, view=exercise and seed=7. The fixed exercise is a route sample, not a service envelope or an incident-day distribution. Rounded to six decimal kilometres and replayed; no interpolation is claimed.'},
    space:PROFILE_SEARCH,rows:profiles.filter(r=>distances.includes(r.km))};
  writeGenerated('research/analysis/energy-feasible.json',JSON.stringify(table,null,2)+'\n');
}
