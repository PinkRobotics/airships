/* Historical test controls replayed with the current hull-centre cable datum. */
/* Independent arithmetic and labelled reference values from the rotor pre-review. */
import assert from 'node:assert/strict';
import fs from 'node:fs';
const referenceCases=JSON.parse(fs.readFileSync(new URL('./rotor-reference.json',import.meta.url))).cases;
import {computeAreaSensitivity} from '../../research/analysis/energy-rotor-area.mjs';
import {S} from '../../research/analysis/energy-rotor-common.mjs';
const result=computeAreaSensitivity(referenceCases);
const oracles={P100:[1256.637061,153.058701,121.697402,1.410474],P1000:[6107.256119,754.950431,602.753952,1.401740],P10000:[79443.024228,7254.654725,5744.629308,1.419162]};
const near=(a,b,t=1e-6)=>assert(Math.abs(a-b)<t,`${a} != ${b}`);
for(const r of result.geometry){
 const c=S.CLASSES[r.class],A=r.stations*Math.PI*r.diameterM*r.diameterM/4;
 const cap=area=>((S.BUS_CEILING*(c.battMW+c.genMW)*1e6*S.CFG.propEta)**2*2*r.rho*area)**(1/3)/9.81/1000;
 near(r.footprintM2,A,1e-8);near(r.pricedCapT,cap(c.diskM2),1e-8);near(r.footprintCapT,cap(A),1e-8);
 near(r.sameThrustHoverPowerRatio,Math.sqrt(c.diskM2/A),1e-12);
 const reference=oracles[r.class];[r.footprintM2,r.pricedCapT,r.footprintCapT,r.sameThrustHoverPowerRatio].forEach((v,i)=>near(v,reference[i]));
}
const p=result.profiles.find(r=>r.dataset==='energy-profiles'&&r.class==='P100'&&r.km===15&&r.basis==='record');
assert(p.baseline.feasible&&!p.footprint.feasible&&!p.footprintCredit.feasible);
near(p.footprint.cycleMWh,7.179606);near(p.footprint.worst.unheldT,9.070433);near(p.footprintCredit.worst.unheldT,2.296146);
assert.match(result.scope,/fixed controls/);assert.match(result.credit.scope,/stipulated sensitivity input/);
console.log('PASS rotor area: three independent footprints, caps and power ratios; labelled probe oracles; fixed-control failure retained');
