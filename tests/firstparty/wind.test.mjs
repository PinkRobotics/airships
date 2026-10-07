import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readWind, windForMission, WIND_MAX_AGE_MS } from '../../app/wind.js?v=01e992e3';

const now = Date.parse('2026-10-02T02:30:00Z');
const doc = () => ({ fetchedAt: '2026-10-02T02:20:00Z', data: {
  forecastAt: '2026-10-02T02:00:00Z', lats: [50, 54], lons: [-128, -124],
  vectors: [[10, 20], [30, 20], [10, 40], [30, 40]],
} });
const mission = { intake: [-128, 50], delivery: [-124, 54], bearing: 123 };
test('bilinear wind at mission midpoint, in km/h and meteorological from direction', () => {
  const w = windForMission(readWind(doc(), now), mission);
  assert.equal(w.spd, Math.hypot(20, 30));
  assert.equal(w.bearing, 123);
  assert.ok(Math.abs(w.dir - 213.69006752598) < 1e-9);
});
test('opposing east/west components cancel across north', () => {
  const d = doc(); d.data.vectors = [[-1, -10], [1, -10], [-1, -10], [1, -10]];
  const w = windForMission(readWind(d, now), mission);
  assert.equal(w.dir, 0); assert.equal(w.spd, 10);
});
test('missing, stale, future, malformed wind is refused', () => {
  assert.throws(() => readWind(null, now));
  const stale = doc(); stale.fetchedAt = new Date(now - WIND_MAX_AGE_MS).toISOString();
  assert.throws(() => readWind(stale, now), /stale/);
  const future = doc(); future.fetchedAt = new Date(now + 600001).toISOString();
  assert.throws(() => readWind(future, now), /future/);
  const malformed = doc(); malformed.data.vectors[0][0] = null;
  assert.throws(() => readWind(malformed, now), /malformed/);
  const oldForecast = doc(); oldForecast.data.forecastAt = '2026-10-01T00:00:00Z';
  assert.throws(() => readWind(oldForecast, now), /stale/);
});
test('edge samples work; outside grid is refused instead of extrapolating', () => {
  const g = readWind(doc(), now);
  assert.equal(windForMission(g, { intake: [-124, 54], delivery: [-124, 54] }).spd, 50);
  assert.throws(() => windForMission(g, { intake: [-140, 60], delivery: [-140, 60] }), /outside/);
});


// Stipulated uniform boundary winds; these are test inputs, not observed weather.
import {CLASSES,MODES,planCycle,selectServedPlan,drawAt,bindServedMission,missionReady,planStatusText} from '../../sim/index.js?v=01e992e3';
const controls = {speedMultiplier:1,ballastT:50,basis:'record'};
const legKm = 4.71; // Representative diagnostic leg, not a flown route.
const along = spd => ({spd,dir:270,bearing:90});
const almost = (a,b,tol=1e-9) => assert.ok(Math.abs(a-b)<tol, `${a} != ${b}`);
test('stipulated along_180 refuses the leg, selector, rate and mission activity', () => {
  const p=planCycle(CLASSES.P100,MODES.rapid,legKm,along(180),{...controls,speedMultiplier:1.5});
  assert.equal(p.trackPossible,false);
  assert.equal(p.feasible,false);
  assert.match(p.trackReason,/return.*positive ground speed/);
  assert.equal(p.tph,null);
  almost(p.selectedAirKph,155.25);
  const selected=selectServedPlan(CLASSES.P100,legKm,along(180),'balanced');
  assert.equal(selected.state,'stand-down');
  assert.match(selected.reason,/return.*positive ground speed/);
  assert.equal(selected.plan,null);
  assert.match(planStatusText(selected),/return.*positive ground speed/);
  const mission={cls:CLASSES.P100,legKm,wind:along(180),mode:MODES.balanced};
  bindServedMission(mission);
  assert.equal(missionReady(mission),false);
  assert.match(mission.planReason,/return.*positive ground speed/);
});
test('stipulated along_72 uses physical speed below the old floor and charges selected airspeed', () => {
  const p=planCycle(CLASSES.P100,MODES.rapid,legKm,along(72),controls);
  almost(p.gsRet,31.5);
  almost(p.gsOut,175.5);
  for(const id of ['OUTBOUND_TRANSIT','RETURN_TRANSIT'])
    almost(drawAt(CLASSES.P100,MODES.rapid,p,id,.5).airV*3.6,103.5);
});
test('stipulated tailwind passes the former upper bound without substituting speed', () => {
  const p=planCycle(CLASSES.P100,MODES.rapid,legKm,along(90),controls);
  assert.equal(p.trackPossible,true);
  almost(p.gsOut,193.5);
  almost(p.gsRet,13.5);
  for(const id of ['OUTBOUND_TRANSIT','RETURN_TRANSIT'])
    almost(drawAt(CLASSES.P100,MODES.rapid,p,id,.5).airV*3.6,103.5);
});


import {readFileSync} from 'node:fs';
const cross = spd => ({spd,dir:0,bearing:90});
test('saved forecast magnitude on a representative crosswind route uses triangle timing', () => {
  const capture=JSON.parse(readFileSync(new URL('./fixtures/wind-response.json',import.meta.url)))[0];
  const spd=capture.hourly.wind_speed_850hPa[0], dir=capture.hourly.wind_direction_850hPa[0];
  const w={spd,dir,bearing:(dir+90)%360}; // Rotate representative track; no incident reconstruction.
  const p=planCycle(CLASSES.P100,MODES.rapid,legKm,w,controls);
  const speed=Math.sqrt(103.5**2-spd**2);
  almost(p.gsOut,speed);almost(p.gsRet,speed);
  almost(p.gsOut,91.538844264,1e-6);
  almost(p.cycleMin,13.897366,1e-6);
  almost(p.tph*24,5180.837776,1e-6);
  assert.match(p.windBasis,/one pressure-level wind vector per route; straight level legs; no shear, turns, gusts or vertical air motion/);
  for(const id of ['OUTBOUND_TRANSIT','RETURN_TRANSIT'])
    almost(drawAt(CLASSES.P100,MODES.rapid,p,id,.5).airV*3.6,103.5);
});
test('stipulated cross_120 and equality refuse the selected slower track', () => {
  for(const spd of [120,103.5]){
    const p=planCycle(CLASSES.P100,MODES.rapid,legKm,cross(spd),controls);
    assert.equal(p.trackPossible,false);
    assert.match(p.trackReason,/crosswind.*selected airspeed/);
    assert.equal(p.tph,null);
  }
});
test('stipulated sub-airspeed pure crosswind lowers both ground speeds equally', () => {
  const p=planCycle(CLASSES.P100,MODES.rapid,legKm,cross(36),controls);
  almost(p.gsOut,Math.sqrt(103.5**2-36**2));almost(p.gsRet,p.gsOut);
  assert.ok(p.gsOut<103.5);
});
test('zero wind leaves every numeric field identical to the still-air plan', () => {
  const still=planCycle(CLASSES.P100,MODES.rapid,legKm,null,controls);
  const zero=planCycle(CLASSES.P100,MODES.rapid,legKm,cross(0),controls);
  const numbers = value => Array.isArray(value)?value.flatMap(numbers):value&&typeof value==='object'
    ?Object.keys(value).sort().flatMap(k=>numbers(value[k])):typeof value==='number'?[value]:[];
  assert.deepEqual(numbers(zero),numbers(still));
});


test('searched profile carries both wind components and charges the full air vector', () => {
  const options={...controls,verticalProfile:{climbRateMps:2,letdownRateMps:2,climbAirspeedMps:5,letdownAirspeedMps:5}};
  const p=planCycle(CLASSES.P100,MODES.rapid,50,cross(36),options);
  for(const id of ['OUTBOUND_TRANSIT','RETURN_TRANSIT']){
    const leg=p.profile.legs[id];almost(Math.abs(leg.crosswindMps),10);
    const segments=p.profile.phases[id],level=segments.find(s=>s.from===s.to);
    assert.ok(level);
    almost(level.airspeedMps,Math.sqrt(103.5**2-36**2)/3.6);
    const before=segments.slice(0,segments.indexOf(level)).reduce((n,s)=>n+s.seconds,0);
    const progress=(before+level.seconds/2)/(p.dur[id]*60);
    almost(drawAt(CLASSES.P100,MODES.rapid,p,id,progress).airV*3.6,103.5);
  }
});
test('stipulated wind at selected airspeed cannot gain round-trip progress from rounding', () => {
  const V=CLASSES.P100.cruiseKph*MODES.rapid.speed;
  for(const dir of [3,13,30,45,90,180,270]) {
    const p=planCycle(CLASSES.P100,MODES.rapid,legKm,{spd:V,dir,bearing:90},controls);
    assert.equal(p.trackPossible,false,`stipulated direction ${dir}`);
    assert.match(p.trackReason,/crosswind|ground speed|wind magnitude/);
    assert.equal(p.tph,null);
  }
});
test('nonzero wind with unsupported whole-phase dilation is refused with a reason', () => {
  const p=planCycle(CLASSES.P100,MODES.rapid,legKm,along(36),{...controls,movingPhaseRateMultiplier:.5});
  assert.equal(p.trackPossible,false);
  assert.match(p.trackReason,/whole-phase dilation.*no represented track/);
  assert.equal(p.tph,null);
});


test('stipulated along_36 changes ceiling through timing, as the weather boundary states', () => {
  const still=planCycle(CLASSES.P100,MODES.rapid,legKm,null,controls);
  const windy=planCycle(CLASSES.P100,MODES.rapid,legKm,along(36),controls);
  almost(still.altitudeGeometry.altTop,646.9258312020461);
  almost(windy.altitudeGeometry.altTop,557.3965844402276);
  assert.ok(windy.dur.OUTBOUND_TRANSIT<still.dur.OUTBOUND_TRANSIT);
  assert.ok(windy.altitudeGeometry.altTop<still.altitudeGeometry.altTop);
  const physics=readFileSync(new URL('../../docs/PHYSICS.md',import.meta.url),'utf8');
  const bullet=physics.slice(physics.indexOf('- **Weather.**'),physics.indexOf('- **Turbulence and gust loading.**'));
  assert.match(bullet,/wind triangle/);
  assert.match(bullet,/timing[\s\S]*profile/);
  assert.doesNotMatch(bullet,/unaffected by wind|clamped/);
});
