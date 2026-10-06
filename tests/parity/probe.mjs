// Runtime reproduction for OPEN-QUESTIONS #16; no feeds, browser or generated inputs.
import * as sim from '../../sim/config.js?v=68694086';
import { buildMission, findSource, setSeed, stateAt } from '../../sim/index.js?v=68694086';
import { buildActuators } from '../../3d/control/actuators.js?v=91301eab';
import { planCycle } from '../../sim/plan.js?v=68694086';
import { airDensity } from '../../sim/atmosphere.js?v=68694086';
import { dragMW, pumpMW, ledger } from '../../sim/physics.js?v=68694086';
import * as viz from '../../3d/model/config.js?v=91301eab';
import * as mission from '../../3d/anim/mission.js?v=91301eab';
import * as mass from '../../3d/physics/mass.js?v=91301eab';
import { pumpPowerMW, derivePower } from '../../3d/physics/energy.js?v=91301eab';
import { buildLayout } from '../../3d/model/layout.js?v=91301eab';
import { createHose, updateHose } from '../../3d/anim/hose.js?v=91301eab';

const reads = new Set();
function traced(obj, label) {
  return new Proxy(obj, { get(target, key) {
    if (typeof key === 'string') {
      const frame = new Error().stack.split('\n')[2].replaceAll(process.cwd() + '/', '');
      reads.add(`${label}.${key}=${JSON.stringify(target[key])} ${frame.trim().replace('file://', '')}`);
    }
    return target[key];
  } });
}
for (const id of sim.CLASS_ORDER) {
  const a = sim.CLASSES[id], b = viz.resolveClass(id);
  const model = traced(a, 'sim.' + id), viewer = traced(b, '3d.' + id);
  const mode = traced(sim.MODES.balanced, 'sim.MODES.balanced');
  const plan = planCycle(model, mode, 15);
  const durations = mission.phaseDurations(viewer, traced(mission.MODES.balanced, '3d.MODES.balanced'));
  const release = [0, 1].map(p => mission.phaseShape(viewer, 'WATER_RELEASE', p));
  const transit = mission.phaseShape(viewer, 'OUTBOUND_TRANSIT', .5);
  const aero = mass.aeroForce(viewer, { airspeedMps: a.cruiseKph / 3.6 }, viz.ASSUMPTIONS);
  const power = dragMW(model, sim.MODES.balanced);
  const layout = buildLayout(viewer);
  const actuators = buildActuators(viewer,layout);
  setSeed(7);
  const water = [[-120.30,50,40000,0,'Synthetic lake',null]];
  const fire = {id:'PARITY-FIXTURE',ll:[-120.05,50.05],sizeHa:4000,status:'Out of Control',note:false,ring:null};
  const src = findSource(fire.ll,a,water);
  const m = buildMission(fire,water,'balanced',id,{src,relaxed:false});
  const idx = sim.PHASES.findIndex(([id]) => id === 'WATER_RELEASE');
  const start = m.phaseEnds[idx-1], duration = m.phaseEnds[idx]-start;
  const releaseModelAltM = [0,.5,.99].map(p => stateAt(m,start+duration*p-m.offset*m.cycleSec).alt);
  const hose = createHose(viewer, layout.hoseReels[0]);
  const fullMass = mass.massState(viewer, {waterFraction:1, ln2Fraction:0, fuelFraction:1}, layout);
  const waterPower = [pumpMW(model), pumpPowerMW(viewer)];
  const atDrop = {};
  for (const altitudeM of [250, 450]) {
    const shape = mission.phaseShape(viewer, 'WATER_RELEASE', .5);
    updateHose(hose, 0, {progress:shape.hoseProgress ?? 0, snap:true, reduced:true});
    atDrop[altitudeM] = {hosePaidM:hose.deployed * hose.headM, anchor:mission.anchorAt(viewer, altitudeM, 1, shape.airspeedMps)};
  }
  console.log(JSON.stringify({id, specSim:a, spec3d:viz.rawSpec(id),
    cycleMinutes:mission.phaseTimeline(viewer,mission.MODES.balanced).totalMinutes, flightKph:transit.airspeedMps*3.6, releaseModelAltM, modeFlightKph:Object.fromEntries(Object.values(mission.MODES).map(mode=>[mode.id,mission.phaseShape(viewer,'OUTBOUND_TRANSIT',.5,{modeId:mode.id}).airspeedMps*3.6])), releaseAltM:release.map(s=>s.altitudeM),
    hoseMinutes:[durations.HOSE_DEPLOY,durations.HOSE_RETRACT], sourceAltM:mission.phaseShape(viewer,'WATER_FILL',.5).altitudeM,
    dragReferenceM2:[Math.PI*(a.diaM/2)**2,aero.referenceAreaM2],
    dragPowerMW:[power,aero.dragN*(a.cruiseKph/3.6)/viz.ASSUMPTIONS.propEta/1e6],
    dragRatio:aero.dragN*(a.cruiseKph/3.6)/viz.ASSUMPTIONS.propEta/1e6/power,
    pumpMW:waterPower, modelHoseOverlapsMin:[plan.dur.SOURCE_APPROACH,plan.dur.OUTBOUND_TRANSIT], ln2VolumeM3:mass.ln2VolumeM3(viewer,1), displayedPropulsionMW:derivePower(viewer,transit).propulsionPowerMW,
    rotorCount:[a.rotors,b.primaryRotorStations*b.rotorsPerStation], primaryActuators:actuators.filter(a=>a.kind==='primary').length,
    discAreaM2:[a.diskM2,b.totalDiscAreaM2],
    liftTonnes:[ledger(model,sim.WORK_ALT_MSL).liftT,fullMass.displacedTonnes,b.displacedAirTonnes],
    hoseDefaultM:hose.headM, atDrop}));
}
console.log(JSON.stringify({DEFAULTS:sim.DEFAULTS, ASSUMPTIONS:viz.ASSUMPTIONS, ALT:[sim.ALT,mission.ALT], ALT_DROP_TOP:sim.ALT_DROP_TOP,
  MODES:[sim.MODES,mission.MODES], RHO_WORK:[airDensity(sim.WORK_ALT_MSL,sim.DEFAULTS.rhoSL),viz.RHO_WORK],
  RHO_LN2:[viz.RHO_LN2,mass.RHO_LN2], RHO_WATER:[viz.RHO_WATER,mass.RHO_WATER]}));
console.log('READS\n'+[...reads].sort().join('\n'));
