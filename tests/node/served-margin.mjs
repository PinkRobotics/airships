/* A physically closing threshold is not an operational reserve. */
import assert from 'node:assert/strict';
import * as S from '../../sim/index.js';
const cls=S.CLASSES.P10000,km=3;
// Contact geometry can move a fixed numerical fixture away from its boundary.
// Find the physical boundary on this model; reserve rejection stays independent.
const at=ballastT=>S.planCycle(cls,S.MODES.rapid,km,null,{speedMultiplier:1.25,ballastT,basis:'record'});
let lo=0,hi=cls.payloadT*.95;
assert.equal(at(lo).feasible,false);assert.equal(at(hi).feasible,true);
for(let i=0;i<45;i++){const mid=(lo+hi)/2;if(at(mid).feasible)hi=mid;else lo=mid;}
const candidate={controls:{mode:'rapid',options:{speedMultiplier:1.25,ballastT:hi}},source:{kind:'regression fixture'}};
const threshold=S.planCycle(cls,S.MODES.rapid,km,null,{...candidate.controls.options,basis:'record'});
assert.equal(threshold.feasible,true,'fixture closes at the unchanged physical tolerance');
assert.equal(S.selectServedPlan(cls,km,null,'balanced',[candidate]).state,'stand-down','a closing plan without reserve must not be served');
assert.equal(S.hasOperatingMargin(threshold),false);
assert.equal(S.SERVED_RELATIVE_MARGIN,.05);
assert.equal(S.CONTROL_RELATIVE_MARGIN,.10);
const withReserve=minimum=>{
 let lo=candidate.controls.options.ballastT,hi=cls.payloadT*.95;
 for(let i=0;i<45;i++){const mid=(lo+hi)/2;const plan=at(mid);
  if(Object.values(plan.operatingMargins).every(r=>r.relativeMargin>=minimum))hi=mid;else lo=mid;}
 return {...candidate,controls:{...candidate.controls,options:{...candidate.controls.options,ballastT:hi}}};
};
const reserved=withReserve(.15),belowTarget=withReserve(.075);
assert.ok(Object.values(at(belowTarget.controls.options.ballastT).operatingMargins).some(r=>r.relativeMargin<.10));
const selected=S.selectServedPlan(cls,km,null,'balanced',[belowTarget,reserved]);
assert.equal(selected.options.ballastT,reserved.controls.options.ballastT,'route selection also prefers the target reserve over lower-cost minimum-only controls');
assert.equal(S.selectServedPlan(cls,km,null,'balanced',[belowTarget]).state,'ready','the serving floor remains five percent when the target is unavailable');
assert.equal(selected.state,'ready');
assert.equal(S.hasOperatingMargin(selected.plan),true);
assert.equal(S.auditServedPlan(cls,km,null,selected),true);
const forged={...selected,plan:threshold};
const altered=structuredClone(selected);altered.plan.operatingMargins['bus power'].relativeMargin+=.1;
assert.throws(()=>S.auditServedPlan(cls,km,null,altered),/reserve differs/);
assert.throws(()=>S.auditServedPlan(cls,km,null,forged));
assert.equal(S.selectServedPlan(cls,km,null,'balanced',[{...candidate,controls:{...candidate.controls,options:{speedMultiplier:1.25,ballastT:0}}}]).state,'stand-down');
for(const r of Object.values(selected.plan.operatingMargins))assert.ok(r.relativeMargin>=S.SERVED_RELATIVE_MARGIN);
console.log('PASS served reserve: the base threshold is physically feasible and refused; ready replay carries every stated reserve');
