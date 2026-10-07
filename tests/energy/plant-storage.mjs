/* The reviewer numbers are oracle values, not current published requirements. */
import assert from 'node:assert/strict';
import {computeStorage,storageBalance} from '../../research/analysis/energy-storage.mjs';
import {CLASSES,CFG,ledger,TERRAIN_MSL} from '../../sim/index.js?v=bef16258';
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-6,`${a} != oracle ${b}`);
const record=computeStorage();
const oracle={P100:1.602812,P1000:0.574884,P10000:0.507716};
for(const r of record.rows){
 const c=CLASSES[r.class];
 // Independent unit conversion: net watts -> daily kWh -> kg -> tonnes -> capacity share.
 const watts=c.solarM2*CFG.solarWPerM2-c.genMW*.02*1e6;
 const tDay=watts/1000*24/CFG.eLN2/1000;
 near(r.maximumFixedLossPctCapacityDay,100*tDay/c.ln2CapT);
 near(r.maximumFixedLossPctCapacityDay,oracle[r.class]);
}
// Hand balance for the reviewed smaller class at the published lower ground-tank rate.
// Reviewer crossing times are labelled oracle values, rounded to the printed precision.
const small=record.rows.find(r=>r.class==='P100'),cls=CLASSES.P100;
const smallMake=(cls.solarM2*CFG.solarWPerM2-cls.genMW*.02*1e6)*24/(CFG.eLN2*1e6);
const target=ledger(cls,TERRAIN_MSL).surplusT,rate=.0024; // Ground DAGT input, PDF page 2.
const net=smallMake-cls.ln2CapT*rate;
const fixedByHand=target/net,proportionalByHand=-Math.log(1-target*rate/smallMake)/rate;
near(small.sensitivity[1].fixed.days,fixedByHand);
near(small.sensitivity[1].proportional.days,proportionalByHand);
assert.ok(Math.abs(fixedByHand-68.436)<.0005,'reviewer lower-rate fixed days oracle');
assert.ok(Math.abs(proportionalByHand-62.675)<.0005,'reviewer lower-rate proportional days oracle');
// Hand-computable reservoir: make 10 t/day, capacity 100 t, target 50 t, loss 1%/day.
const hand=storageBalance(10,100,50,.01);
near(hand.fixed.netTDay,9);near(hand.fixed.days,50/9);
near(hand.proportional.equilibriumT,1000);
near(hand.proportional.days,-Math.log(.95)/.01);
// Integrate independently with a small time step, then measure the target crossing.
let mass=0,days=0;const dt=1e-4;
while(mass<50){mass+=(10-.01*mass)*dt;days+=dt;}
assert.ok(Math.abs(days-hand.proportional.days)<2*dt);
const p=record.rows.find(r=>r.class==='P1000');
assert.equal(p.sensitivity[0].fixed.days,null);assert.equal(p.sensitivity[0].proportional.days,null);
const lower=p.sensitivity[1];assert.ok(lower.fixed.days>0&&lower.proportional.days>0);
assert.equal(storageBalance(10,100,101,0).fixed.days,null,'capacity must be respected');
assert.equal(storageBalance(10,100,50,.1).fixed.days,null,'equality allows no positive fixed accumulation');
assert.equal(storageBalance(10,100,100,.1).proportional.days,null,'asymptote is not a finite crossing');
console.log('GREEN solar storage: three loss-limit oracles, hand balance, independent integration and both crossing cases');
