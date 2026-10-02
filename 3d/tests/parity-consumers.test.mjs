import test from 'node:test';
import assert from 'node:assert/strict';
import { CLASS_IDS, resolveClass, ALT, ASSUMPTIONS } from '../model/config.js?v=b7ca2f95';
import { idealDiscThrust, idealDiscPower, buildActuators } from '../control/actuators.js?v=b7ca2f95';
import { build } from '../model/build.js?v=b7ca2f95';
import { createDriver, updateDriver } from '../anim/driver.js?v=b7ca2f95';
import { phaseShape } from '../anim/mission.js?v=b7ca2f95';
import { defaultState } from '../physics/state.js?v=b7ca2f95';
import { pumpPowerMW } from '../physics/energy.js?v=b7ca2f95';
import { templateFor } from '../model/metadata.js?v=b7ca2f95';

for (const id of CLASS_IDS) {
  test(`${id}: driver lines stay stowed at both old and corrected release altitudes`, () => {
    const b = build(id,{tier:0}), d = createDriver(b,{reduced:true});
    const rows = [];
    for (const altitudeM of [250,ALT.drop]) {
      d.snapNext = true;
      updateDriver(d,0,defaultState({...phaseShape(b.cls,'WATER_RELEASE',.5),
        phase:'WATER_RELEASE',phaseProgress:.5,altitudeM}),null,{lowDetail:true});
      assert.ok(d.hoses.every(h => h.deployed === 0));
      assert.equal(d.anchor.deployed,0);
      assert.equal(d._nodes.anchorCable.visible,false);
      assert.equal(d._nodes.waterSurface.visible,false);
      rows.push({altitudeM,hosePaidM:d.hoses[0].deployed*d.hoses[0].headM,
        cablePaidM:d.anchor.deployed*d.anchor.headM,spraySpanM:d._nodes.dropSpray.spanM});
    }
    assert.equal(rows[0].spraySpanM, rows[1].spraySpanM);
    console.log(`${id} release geometry ${JSON.stringify(rows)}`);
    // The same driver reaches the source with the class hose, including every reel.
    d.snapNext = true;
    updateDriver(d,0,defaultState({...phaseShape(b.cls,'WATER_FILL',.1),
      phase:'WATER_FILL',phaseProgress:.1}),null,{lowDetail:true});
    assert.ok(d.hoses.every(h => h.headM === b.cls.hoseLengthM));
    assert.ok(d.hoses.every(h => h.podPos[2] <= -b.cls.hoseLengthM));
    console.log(`${id} source geometry ${JSON.stringify({headM:d.hoses[0].headM,
      surfaceZ:d._nodes.waterSurface.p[2],podZ:d.hoses[0].podPos[2],anchorCableM:d.anchor.headM})}`);
  });
}

test('source altitude, pump, metadata and driver follow a changed class hose together', () => {
  const b = build('P100',{tier:0,overrides:{hoseLengthM:450}}), d = createDriver(b);
  assert.equal(phaseShape(b.cls,'WATER_FILL',.5).altitudeM,450);
  assert.ok(Math.abs(pumpPowerMW(b.cls)/pumpPowerMW(resolveClass('P100'))-1.5) < 1e-12);
  assert.ok(d.hoses.every(h => h.headM === 450));
  assert.match(templateFor('PumpPod_00').desc(b.cls), /450 m/);
});

test('rotor density defaults and actuator construction follow the shared assumption', () => {
  const b = build('P100',{tier:0});
  const previous = ASSUMPTIONS.rhoAir;
  try {
    ASSUMPTIONS.rhoAir = 0.9;
    assert.equal(idealDiscThrust(100,1e6),idealDiscThrust(100,1e6,0.9));
    assert.equal(idealDiscPower(100,1e5),idealDiscPower(100,1e5,0.9));
    const a = buildActuators(b.cls,b.layout).find(a => a.kind === 'primary');
    const perW = (b.cls.batteryPeakPowerMW+b.cls.generatorContinuousPowerMW)*1e6*.78/b.cls.primaryRotorStations;
    assert.equal(a.fMaxN, idealDiscThrust(a.discAreaM2,perW,0.9));
  } finally { ASSUMPTIONS.rhoAir = previous; }
});
