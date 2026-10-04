/* Enumerate BOTH declarations before comparing them: a new numeric key needs a partner
 * or a reason here, even when nobody remembered to add it to the old shared-field list.
 * The import boundary keeps 3d standalone; this test is the sanctioned checked-copy seam.
 */
import { describe, it, eq, close, deepEq } from '../harness.js';
import * as sim from '../../sim/config.js?v=1ead4525';
import { ISA, airDensity } from '../../sim/atmosphere.js?v=1ead4525';
import { dragMW, pumpMW, ledger } from '../../sim/physics.js?v=1ead4525';
import * as viz from '../../3d/model/config.js?v=d3e69408';
import * as mission from '../../3d/anim/mission.js?v=d3e69408';
import * as mass from '../../3d/physics/mass.js?v=d3e69408';
import { pumpPowerMW } from '../../3d/physics/energy.js?v=d3e69408';
import { createHose } from '../../3d/anim/hose.js?v=d3e69408';

export const CLASS_PAIRS = {
  payloadT: 'payloadTonnes', dispM3: 'displacementM3', lenM: 'lengthM',
  diaM: 'nominalDiameterM', diskM2: 'publishedDiscAreaM2', genMW: 'generatorContinuousPowerMW',
  battMWh: 'batteryEnergyMWh', battMW: 'batteryPeakPowerMW', cryoMW: 'cryogenicPowerMW',
  ln2CapT: 'ln2TankCapacityTonnes', hoseM: 'hoseLengthM', anchorM: 'anchorCableM',
  anchorBagT: 'anchorBagTonnes', solarM2: 'solarAreaM2', cruiseKph: 'cruiseKph',
  fillM3s: 'fillRateM3s', hoseDeployMin: 'hoseDeployMin', hoseRetractMin: 'hoseRetractMin',
};

// Each exemption is one exact numeric leaf, not a wildcard that could hide a new field.
export const CLASS_EXEMPTIONS = {
  sim: {
    rotors: 'The model counts 4/6/14 rotors while the drawing uses paired rotors at that many stations; reconciling the drawing needs a design decision (#16).',
    minSourceHa: 'Source eligibility belongs to the mission planner, not the standalone drawing.',
    searchKm: 'Water-source search radius belongs to the mission planner, not the standalone drawing.',
    dropKm: 'The host supplies its drop route while the standalone viewer has no geographic route planner.',
  },
  viz: {
    primaryRotorStations: 'The drawing has 4/6/14 stations, each paired, pending the rotor-layout decision in #16.',
    rotorsPerStation: 'Two coaxial rotors per drawn station remain a conceptual layout pending the rotor-count decision in #16.',
    primaryRotorDiameterM: 'Drawn rotor diameter is a layout choice, with its aggregate area separately checked within the existing ten-percent allowance.',
    mediumThrusters: 'Auxiliary thruster count describes the conceptual drawing and has no mission-model field.',
    mediumThrusterDiameterM: 'Auxiliary thruster diameter describes the conceptual drawing and has no mission-model field.',
    localTrimFans: 'Trim fan count describes the conceptual drawing and has no mission-model field.',
    tailSurfaces: 'Tail surface count describes the conceptual drawing and has no mission-model field.',
    waterTanks: 'Water tank count partitions the shared payload for the conceptual drawing.',
    waterTankRings: 'Water tank rings arrange the conceptual drawing without changing payload.',
    dropOutlets: 'Outlet count partitions the discharge in the conceptual drawing.',
    pumpPods: 'Pod count distributes the shared class fill rate among drawn pumps.',
    hoseReels: 'Reel count distributes the drawn hoses without changing their shared length.',
    cryoTrains: 'Train count partitions the shared cryogenic capacity into drawn modules.',
    ln2Tanks: 'Tank count partitions the shared nitrogen capacity into drawn modules.',
    generators: 'Generator count partitions the shared continuous power into drawn modules.',
    batteryModules: 'Module count partitions the shared battery capacity into drawn modules.',
    hvdcBuses: 'Bus count is an illustrative electrical layout without a mission-model field.',
    macroFrameCount: 'Frame count belongs to the conceptual structure drawing.',
    longerons: 'Longeron count belongs to the conceptual structure drawing.',
    structuralSections: 'Section count belongs to the conceptual structure drawing.',
    cellSizeM: 'Representative cell pitch belongs to the conceptual structure drawing.',
    structuralDensity: 'The structure renderer uses this sampling density, not a physical material density.',
    structuralSeed: 'The structure renderer uses this deterministic drawing seed, not a mission input.',
    maintenanceCorridors: 'Corridor count belongs to the conceptual layout.',
    maxPitchRateDegS: 'The renderer caps attitude interpolation without asserting a mission-model pitch limit.',
    maxYawRateDegS: 'The renderer caps attitude interpolation without asserting a mission-model yaw limit.',
    maxRollRateDegS: 'The renderer caps attitude interpolation without asserting a mission-model roll limit.',
    'visualDetail.closeCellModules': 'Close-view module count is a rendering budget.',
    'visualDetail.mediumCellModules': 'Medium-view module count is a rendering budget.',
    'visualDetail.mapTrianglesTarget': 'Map triangle count is a rendering budget.',
    'hull.xMax': 'The resolved hull carries its conceptual drawing profile, not a mission field.',
    'hull.capFrac': 'The resolved hull carries its conceptual drawing profile, not a mission field.',
    'hull.stub': 'The resolved hull carries its numeric pole guard, not a mission field.',
    'hull.topFlat': 'The resolved hull carries its conceptual drawing profile, not a mission field.',
    'hull.bottomFlat': 'The resolved hull carries its conceptual drawing profile, not a mission field.',
    maxRadiusM: 'The drawing solves its radius to conserve volume rather than rounding to the nominal model diameter.',
    diameterM: 'The solved drawing diameter differs slightly from the nominal diameter used for shared drag.',
    finenessRatio: 'The drawing derives fineness from its solved geometry rather than a mission input.',
    volumeM3: 'Numerically integrated hull volume has roundoff and is checked against displacement in the model tests.',
    centroidXFromNoseM: 'The drawing computes its origin from its integrated hull volume.',
    xNose: 'The drawing places the nose relative to its computed origin.',
    xTail: 'The drawing places the tail relative to its computed origin.',
    displacedAirTonnes: 'This derived lift is compared with the evaluated model ledger below, not an independently declared class input.',
    structureAllowanceTonnes: 'This derived dry allowance is compared with the evaluated model ledger below.',
    surplusTonnes: 'This derived empty surplus is compared with the evaluated model ledger below.',
    reserveTonnes: 'This derived laden reserve is compared with the evaluated model ledger below.',
    payloadVolumeM3: 'The drawing converts the shared water payload into volume using one tonne per cubic metre.',
    payloadCubeEdgeM: 'The scale illustration derives its cube edge from the shared payload volume.',
    approxCellCount: 'The structure renderer estimates a cell count from its conceptual pitch.',
    totalDiscAreaM2: 'The drawing derives this from paired rotor geometry and is checked within the existing ten-percent illustration allowance.',
    sectionLengthM: 'The drawing divides the hull into its conceptual structural sections.',

  },
};

export const CONSTANT_EXEMPTIONS = {
  sim: {
    'DEFAULTS.hoseMul': 'The host applies its hose multiplier before passing state; standalone specs use nominal hose length.',
    'DEFAULTS.speedMul': 'The host applies its speed dial before passing state; standalone specs use nominal speed.',
    'DEFAULTS.fillMul': 'The host applies its fill dial before passing state; standalone specs use nominal flow.',
    'DEFAULTS.cryoMul': 'The host applies its cryogenic dial before passing state; standalone specs use nominal capacity.',
    'DEFAULTS.exampleKm': 'The standalone timeline accepts distance as an argument rather than owning the host distance dial.',
    VZ_MAX: 'The eleven-phase standalone illustration has its own vertical choreography; host flight limits arrive in host state.',
    'ISA.P0': 'The viewer needs a density ratio anchored to rhoSL, not absolute ISA pressure.',
    'ISA.TROPOPAUSE': 'The viewer derives density only at its declared work altitude, not at arbitrary ISA altitudes.',
    'ISA.FLOOR': 'The viewer derives density only at its declared work altitude, not at arbitrary ISA altitudes.',
  },
  viz: {
    'ASSUMPTIONS.eLN2Range.0': 'The lower exploratory slider bound is viewer UI, not a model assumption.',
    'ASSUMPTIONS.eLN2Range.1': 'The upper exploratory slider bound is viewer UI, not a model assumption.',
    'ASSUMPTIONS.rtLN2Range.0': 'The lower exploratory slider bound is viewer UI, not a model assumption.',
    'ASSUMPTIONS.rtLN2Range.1': 'The upper exploratory slider bound is viewer UI, not a model assumption.',
    G: 'The sim uses literal 9.81 in its force and pump equations, checked here through evaluated pump power.',
    RHO_LN2: 'The sim accounts for nitrogen in tonnes, while only the viewer packages its liquid volume.',
    RHO_WATER: 'The sim uses literal 1000 in its pump equation, checked here through evaluated pump power.',
    'PACKAGING.generatorMWPerM3': 'Generator packaging density sizes conceptual boxes, not mission performance.',
    'PACKAGING.batteryKWhPerM3': 'Battery packaging density sizes conceptual boxes, not mission performance.',
    'PACKAGING.cryoMWPerM3': 'Cryogenic packaging density sizes conceptual boxes, not mission performance.',
    'HULL_DEFAULT.xMax': 'This is a hull drawing profile parameter, not a mission assumption.',
    'HULL_DEFAULT.capFrac': 'This is a hull drawing profile parameter, not a mission assumption.',
    'HULL_DEFAULT.stub': 'This keeps drawn pole geometry finite without altering nominal model dimensions.',
    'HULL_DEFAULT.topFlat': 'This is a hull drawing profile parameter, not a mission assumption.',
    'HULL_DEFAULT.bottomFlat': 'This is a hull drawing profile parameter, not a mission assumption.',
    TRIM_FAN_DEPTH_RATIO: 'Duct depth is a conceptual drawing proportion.',
    DUCT_SEAL_OF_DIAMETER: 'Duct seal depth is a conceptual drawing proportion.',
    HULL_BAND_LIFT: 'Band offset prevents overlapping drawn surfaces.',
    ANCHOR_MAX_DIP_MPS: 'The bag motion safety gate is viewer choreography, separately covered by anchor parity tests.',
  },
};

function leaves(obj, prefix = '', out = {}) {
  if (typeof obj === 'number') out[prefix] = obj;
  else if (obj && typeof obj === 'object') {
    for (const [k, v] of Object.entries(obj)) leaves(v, prefix ? `${prefix}.${k}` : k, out);
  }
  return out;
}
const at = (obj, path) => path.split('.').reduce((v, k) => v?.[k], obj);

/** Return all errors, so the initial red run lists missing partners and wrong values together. */
export function parityErrors(a, b, pairs, exemptions) {
  const errors = [], covered = { sim: new Set(), viz: new Set() };
  for (const [ak, bk] of pairs) {
    const av = at(a, ak), bv = at(b, bk);
    const al = leaves(av, ak), bl = leaves(bv, bk);
    for (const k of Object.keys(al)) covered.sim.add(k);
    for (const k of Object.keys(bl)) covered.viz.add(k);
    if (!Object.keys(al).length || !Object.keys(bl).length) {
      errors.push(`missing numeric partner: sim.${ak}=${JSON.stringify(av)}; 3d.${bk}=${JSON.stringify(bv)}`);
    } else {
      try { deepEq(bv, av, `sim.${ak} / 3d.${bk}`); } catch (e) { errors.push(e.message); }
    }
  }
  for (const [side, obj] of [['sim', a], ['viz', b]]) {
    for (const key of Object.keys(leaves(obj))) {
      if (covered[side].has(key)) continue;
      const reason = exemptions[side]?.[key];
      if (typeof reason !== 'string' || !reason.trim()) errors.push(`unpaired ${side === 'viz' ? '3d' : 'sim'}.${key}`);
    }
  }
  return errors;
}
function assertParity(...args) {
  const errors = parityErrors(...args);
  if (errors.length) throw new Error(errors.join('\n'));
}

const constantsA = { ...sim, CLASSES: undefined, CFG: undefined, ISA,
  RHO_WORK: airDensity(sim.WORK_ALT_MSL, sim.DEFAULTS.rhoSL) };
const constantsB = { ...viz, ...mission };
const constantPairs = [
  ...['eLN2','rtLN2','pumpEta','propEta','Cd','rhoAir','rhoSL','solarWPerM2']
    .map(k => [`DEFAULTS.${k}`, `ASSUMPTIONS.${k}`]),
  ['DEFAULTS.rhoSL','RHO_SL'], ['DEFAULTS.rhoAir','RHO_AIR'],
  ...['ALT','ALT_DROP_TOP','TERRAIN_MSL','WORK_ALT_MSL','MODES','RHO_WORK'].map(k => [k,k]),
  ...['T0','LAPSE','G0','R'].map(k => [`ISA.${k}`,`ISA.${k}`]),
];

describe('numeric declarations have partners in both directions', () => {
  it('class IDs agree', () => deepEq(viz.CLASS_IDS, sim.CLASS_ORDER));
  it('all exported numeric constants and table entries are paired or reasoned', () =>
    assertParity(constantsA, constantsB, constantPairs, CONSTANT_EXEMPTIONS));
  for (const id of sim.CLASS_ORDER) {
    it(`${id}: every numeric class field is paired or reasoned`, () =>
      assertParity(sim.CLASSES[id], viz.rawSpec(id), Object.entries(CLASS_PAIRS), CLASS_EXEMPTIONS));
    it(`${id}: resolved numeric fields also need partners or reasons`, () =>
      assertParity(sim.CLASSES[id], viz.resolveClass(id), Object.entries(CLASS_PAIRS), CLASS_EXEMPTIONS));
  }
});

describe('derived results and actual consumers agree', () => {
  it('liquid densities have one declaration inside 3d', () => {
    eq(mass.RHO_LN2, viz.RHO_LN2); eq(mass.RHO_WATER, viz.RHO_WATER);
  });
  for (const id of sim.CLASS_ORDER) {
    const a = sim.CLASSES[id];
    it(`${id}: selected mode controls the animated speed`, () => {
      const b = viz.resolveClass(id);
      for (const mode of Object.values(sim.MODES)) {
        eq(mission.phaseShape(b,'OUTBOUND_TRANSIT',.5,{modeId:mode.id}).airspeedMps,
          a.cruiseKph*mode.speed/3.6, `${mode.id} flight speed`);
      }
    });
    it(`${id}: frontal-area drag agrees at every mode speed`, () => {
      const b = viz.resolveClass(id);
      for (const mode of Object.values(sim.MODES)) {
        const v = a.cruiseKph * mode.speed / 3.6;
        const rhoAir = ledger(a, sim.WORK_ALT_MSL).rho;
        const aero = mass.aeroForce(b, {airspeedMps:v}, {...viz.ASSUMPTIONS,rhoAir});
        close(aero.referenceAreaM2, Math.PI*(a.diaM/2)**2, 1e-9, 'drag reference area');
        close(aero.dragN*v/viz.ASSUMPTIONS.propEta/1e6, dragMW(a, mode), 1e-9, 'drag MW');
      }
    });
    it(`${id}: evaluated source, pump, hose timing and cruise match the declared model`, () => {
      const b = viz.resolveClass(id), d = mission.phaseDurations(b);
      eq(mission.phaseShape(b,'OUTBOUND_TRANSIT',.5).airspeedMps, a.cruiseKph/3.6);
      eq(mission.phaseShape(b,'WATER_FILL',.5).altitudeM, sim.sourceAltM(a));
      eq(d.HOSE_DEPLOY, a.hoseDeployMin); eq(d.HOSE_RETRACT, a.hoseRetractMin);
      eq(d.WATER_FILL, a.payloadT/a.fillM3s/60);
      eq(d.OUTBOUND_TRANSIT, 15/a.cruiseKph*60);
      close(pumpPowerMW(b), pumpMW(a), 1e-12, 'pump MW');
      eq(createHose(b,{index:0,p:[0,0,0]}).headM, a.hoseM);
    });
    it(`${id}: release and escape share the model's altitude endpoints`, () => {
      const b = viz.resolveClass(id);
      eq(mission.phaseShape(b,'WATER_RELEASE',0).altitudeM, sim.ALT.drop);
      eq(mission.phaseShape(b,'WATER_RELEASE',1).altitudeM, sim.ALT_DROP_TOP);
      eq(mission.phaseShape(b,'BUOYANCY_ESCAPE',0).altitudeM, sim.ALT_DROP_TOP);
    });
    it(`${id}: working-density mass and resolved lift use the model ledger`, () => {
      const b = viz.resolveClass(id), led = ledger(a, sim.WORK_ALT_MSL);
      const m = mass.massState(b,{waterFraction:1,ln2Fraction:0,fuelFraction:1});
      close(m.displacedTonnes, led.liftT, 1e-9);
      close(b.displacedAirTonnes, led.liftT, 1e-9);
      close(b.reserveTonnes, led.reserveT, 1e-9);
      eq(b.structureAllowanceTonnes, led.dryT);
      close(b.surplusTonnes, led.surplusT, 1e-9);
    });
    it(`${id}: unresolved paired-rotor drawing keeps its stated counts and area allowance`, () => {
      const b = viz.resolveClass(id);
      eq(b.primaryRotorStations, a.rotors); eq(b.rotorsPerStation, 2);
      eq(Math.abs(b.totalDiscAreaM2-a.diskM2)/a.diskM2 < .10, true);
    });
  }
  it('nitrogen recovery and solar assumptions stay below their physical ceilings', () => {
    eq(sim.DEFAULTS.rtLN2*sim.DEFAULTS.eLN2*1000 <= 173.4, true);
    eq(sim.DEFAULTS.solarWPerM2 <= 264*.30, true);
  });
});
