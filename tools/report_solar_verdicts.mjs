/* Record the prescribed checks and the captured missions at current solar areas. */
import fs from 'node:fs';
import {CLASSES,MODES,planCycle,selectServedPlan,aeroGeometry} from '../sim/index.js';
const brief=p=>({feasible:p.feasible,releasedT:p.deliveredT,retainedT:p.retainedT,cycleMin:p.cycleMin,suppliedMWh:p.eCycleMWh,tph:p.tph});
const classes=Object.entries(CLASSES).map(([id,c])=>({class:id,solarM2:c.solarM2,footprintM2:aeroGeometry(c).areaM2}));
const prescribed=[];
for(const [id,c] of Object.entries(CLASSES))for(const km of [15,60])for(const basis of ['record','favourable'])prescribed.push({class:id,km,basis,...brief(planCycle(c,MODES.balanced,km,null,{basis}))});
const served=JSON.parse(fs.readFileSync('tests/energy/served-route-distances.json')).missions.map(m=>{
 const s=selectServedPlan(CLASSES[m.class],m.km,null,m.mode);
 return {capture:m.capture,mission:m.mission,class:m.class,km:m.km,requestedMode:m.mode,state:s.state,mode:s.mode,options:s.options,plan:s.plan?brief(s.plan):null};
});
const report={classes,prescribed,served},i=process.argv.indexOf('--json');
if(i>=0)fs.writeFileSync(process.argv[i+1],JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(classes));
console.log(`Prescribed ${prescribed.length} rows; ${prescribed.filter(r=>r.feasible).length} accepted`);
console.log(`Served ${served.length} missions; ${served.filter(r=>r.state==='ready').length} ready`);
