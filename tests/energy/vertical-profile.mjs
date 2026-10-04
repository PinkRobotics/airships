/* Vertical controls, integrated distance and upward-authority counterexamples. */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {CLASSES,MODES,PHASES,planCycle,drawAt,cycleGeometry,altAt,gsAt,verticalProfiles} from '../../sim/index.js?v=68fef878';
import {searchedProfile} from '../../sim/profile.js?v=68fef878';
let count=0,worst=0,where={};
function velocity(p,g,id,x) {
  const a=Math.max(0,x-.001),b=Math.min(1,x+.001);
  return (altAt(g,p,id,b)-altAt(g,p,id,a))/Math.max(1e-9,(b-a)*p.dur[id]*60);
}
for(const c of Object.values(CLASSES))for(const mode of Object.values(MODES))for(const km of [2.550290,15,60])for(const ballast of [0,.95])for(const speedMultiplier of [.5,.75,1,1.25,1.5]) {
 const base=planCycle(c,mode,km,null,{ballastT:c.payloadT*ballast,speedMultiplier});
 for(const options of verticalProfiles()) {
  const p={...base,dur:{...base.dur}},g=cycleGeometry(c,p);
  p.profile=searchedProfile(p,g,km,options);
  let previous=null;
  for(const [id] of PHASES)if(p.dur[id]>0)for(let i=0;i<=2000;i++) {
   const x=i/2000,v=velocity(p,g,id,x),alt=altAt(g,p,id,x);
   if(previous){if(Math.abs(v-previous.v)>worst){worst=Math.abs(v-previous.v);where={class:c.id,mode:mode.id,km,ballast,options,id,x,previous};}if(i===0)assert.ok(Math.abs(alt-previous.alt)<1e-8,'altitude seam');}
   previous={v,alt};
  }
  worst=Math.max(worst,Math.abs(previous.v-velocity(p,g,'SOURCE_APPROACH',0)));
  for(const [id,leg] of Object.entries(p.profile.legs))if(leg.fits) {
   // Simpson integration at segment seams resolves even a very short cruise interval.
   let m=leg.extraDistanceM,offset=0;
   for(const segment of p.profile.phases[id]) {
    const speed=f=>gsAt(g,p,id,(offset+f*segment.seconds)/(p.dur[id]*60))/3.6;
    m+=segment.seconds*(speed(0)+4*speed(.5)+speed(1))/6;
    offset+=segment.seconds;
   }
   assert.ok(Math.abs(m-km*1000)<1e-7,`${c.id}/${id}: integrated distance ${m}`);
  }
  count++;
 }
}
assert.ok(worst<=.1,`vertical speed step ${worst} ${JSON.stringify(where)}`);
const c=CLASSES.P100,m=MODES.balanced;
const options={climbRateMps:2,letdownRateMps:.5,climbAirspeedMps:5,letdownAirspeedMps:5};
for(const speedMultiplier of [.5,.75,1,1.25,1.5]) {
 const p=planCycle(c,m,15,null,{verticalProfile:options,speedMultiplier});
 const s=p.profile.phases.RETURN_TRANSIT.at(-1),before=p.profile.phases.RETURN_TRANSIT.slice(0,-1).reduce((n,s)=>n+s.seconds,0);
 const x=(before+s.seconds/2)/(p.dur.RETURN_TRANSIT*60);
 const got=drawAt(c,m,p,'RETURN_TRANSIT',x);
 assert.ok(Math.abs(got.airV-options.letdownAirspeedMps)<1e-9,'letdown airspeed must be independent of cruise');
}
const steep=planCycle(c,m,15,null,{verticalCd:100,verticalProfile:options});
assert.equal(steep.feasible,false,'climb outrunning surplus cannot be accepted');
assert.ok(steep.bindingLimits.includes('upward authority unavailable'));
const gentle=planCycle(c,m,15,null,{verticalProfile:{...options,climbRateMps:.5,climbAirspeedMps:0,letdownAirspeedMps:0}});
assert.ok(gentle.feasible,'full-delivery profile exists');assert.equal(gentle.deliveredT,c.payloadT);
console.log(`PASS independent vertical controls: ${count} shapes; largest speed step ${worst.toFixed(9)} m/s; full-delivery cycle ${gentle.cycleMin.toFixed(3)} minutes`);
