/* Historical test controls replayed with the current hull-centre cable datum. */
/* Independent separated shaft-power equations and labelled pre-review oracle. */
/* Source-derived stipulated sensitivity inputs, never measured properties of these rotors. */
import assert from 'node:assert/strict';
import fs from 'node:fs';
const referenceCases=JSON.parse(fs.readFileSync(new URL('./rotor-reference.json',import.meta.url))).cases;
import {shaftPower,computePowerSensitivity} from '../../research/analysis/energy-rotor-power.mjs';
import {S} from '../../research/analysis/energy-rotor-common.mjs';
const near=(a,b,t=1e-6)=>assert(Math.abs(a-b)<t,`${a} != ${b}`);
for(const id of ['P100','P10000']){
 const c=S.CLASSES[id],p=S.planCycle(c,S.MODES.rapid,15,null,{basis:'record',ballastT:.35*c.payloadT});
 const s=S.drawAt(c,S.MODES.rapid,p,'OUTBOUND_TRANSIT',.23075),got=shaftPower(c,s);
 const T=s.owners.rotorT*9810,rho=s.led.rho,A=c.diskM2,V=Math.abs(s.airV),vc=Math.max(0,-s.vz),vh2=T/(2*rho*A);
 // Independent fixed-point solution of Glauert inflow; no production inducedMW call.
 let v=Math.sqrt(vh2);
 for(let i=0;i<1000;i++)v=(v+vh2/Math.sqrt(V*V+(vc+v)**2))/2;
 const mechanical=T*vc/1e6,induced=1.15*T*v/1e6,profile=rho*A*(707*.3048)**3*(.0849/8)*.0085/1e6;
 near(got.mechanicalMW,mechanical,1e-10);near(got.inducedMW,induced,1e-10);near(got.profileMW,profile,1e-10);
 near(got.shaftMW,mechanical+induced+profile,1e-10);
}
const data=computePowerSensitivity(referenceCases);
const r=data.profiles.find(q=>q.dataset==='energy-profiles'&&q.class==='P100'&&q.km===15&&q.basis==='record'&&q.kind==='best');
near(r.lowThrust.rotorT,0);near(r.lowThrust.originalMW,0,1e-12);near(r.lowThrust.comparisonMW,2.426608);
near(r.originalTotalMWh,4.998060);near(r.comparisonDemandMWh,5.470556);
const full=data.profiles.find(q=>q.dataset==='energy-profiles'&&q.class==='P100'&&q.km===15&&q.basis==='record'&&q.kind==='fullDeliveryBest');
near(full.originalTotalMWh,41.563751);near(full.comparisonDemandMWh,40.694612);assert(full.comparisonDemandMWh<full.originalTotalMWh);
const large=data.profiles.find(q=>q.dataset==='energy-profiles'&&q.class==='P10000'&&q.km===60&&q.basis==='record'&&q.kind==='best');
near(large.comparisonDemandMWh,529.508695);assert(large.comparisonDemandMWh>large.originalTotalMWh);
const median=data.profiles.find(q=>q.dataset==='served-reference-median'&&q.class==='P10000');
near(median.originalTotalMWh,141.162194);near(median.comparisonDemandMWh,162.910058);
const zero={led:{rho:1},owners:{rotorT:0},airV:0,vz:0};assert(shaftPower(S.CLASSES.P100,zero).shaftMW>0);
assert.match(data.inputs.scope,/stipulated sensitivity inputs/i);
console.log('PASS separated rotor power: independent shaft equations for two classes, low-thrust oracle, increases and decrease, nonzero spinning-blade power at zero thrust');
