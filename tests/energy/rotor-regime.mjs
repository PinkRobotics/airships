/* Historical test controls replayed with the current hull-centre cable datum. */
/* The pre-review reference uses midpoint samples of the original force/velocity trace. */
/* Source-derived stipulated sensitivity inputs, never measured properties of these rotors. */
import assert from 'node:assert/strict';
import fs from 'node:fs';
const referenceCases=JSON.parse(fs.readFileSync(new URL('./rotor-reference.json',import.meta.url))).cases;
import {computeRegimeSensitivity,vrsScreen} from '../../research/analysis/energy-rotor-regime.mjs';
import {S} from '../../research/analysis/energy-rotor-common.mjs';
const data=computeRegimeSensitivity(referenceCases),near=(a,b,t=1e-6)=>assert(Math.abs(a-b)<t,`${a} != ${b}`);
const r=data.profiles.find(q=>q.dataset==='energy-profiles'&&q.class==='P100'&&q.km===15&&q.basis==='record');
const phase=id=>r.phases.find(p=>p.phase===id);
// Labelled pre-review reference values, not current published figures.
near(phase('WATER_RELEASE').screenMinutes,.141917);near(phase('BUOYANCY_ESCAPE').screenMinutes,.756000);
near(r.totalScreenMinutes,.897917);near(phase('BUOYANCY_ESCAPE').footprintScreenMinutes,.437600);
near(r.risingRotorMWh,1.149363);near(r.risingFractionOfRotorMWh,.282771);
const sample=phase('BUOYANCY_ESCAPE').peakRising;
near(sample.vz,8.513568);near(sample.airV,6.631212);near(sample.vh,11.534067);
// Independent substitution by hand into the published boundary equations.
const x=sample.airV/sample.vh,z=-sample.vz/sample.vh,b=1-(x/.95)**2;
const upper=(-.45-1.5)/2+(-.45+1.5)/2*b**.2;
const lower=(-.45-1.5)/2-(-.45+1.5)/2*b**1.5;
near(sample.x,x,1e-12);near(sample.z,z,1e-12);near(sample.upper,upper,1e-12);near(sample.lower,lower,1e-12);
near(z,-.738124);near(x,.574924);near(lower,-1.239874);near(upper,-.495771);assert(z>lower&&z<upper);
const avoids=data.profiles.find(q=>q.dataset==='energy-profiles'&&q.class==='P10000'&&q.km===60&&q.basis==='record');
assert.equal(avoids.totalScreenMinutes,0);assert(avoids.phases.every(p=>p.screenMinutes===0));
const state={thrustN:1,led:{rho:1},airV:0,vz:1};
assert.equal(vrsScreen({...state,thrustN:0},S.CLASSES.P100),null);
assert.equal(vrsScreen({...state,airV:100},S.CLASSES.P100).inside,false);
assert.equal(vrsScreen({...state,vz:-1},S.CLASSES.P100).inside,false);
assert.match(data.inputs.scope,/stipulated sensitivity inputs/i);
console.log('PASS rotor regime: phase/reference totals, hand-substituted escape sample, no-crossing profile and excluded states');
