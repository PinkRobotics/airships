/* The two copies of the vehicle specification must agree.
 *
 * `sim/config.js` holds the assumptions the published numbers are computed from. The 3D
 * library carries its own copy in `3d/model/config.js`, because it is meant to be usable
 * on its own and cannot import the model.
 *
 * That is a duplication this project otherwise refuses to accept, and it has already
 * failed once: a respec of the P-10000's battery and disc area on 2026-08-08 was applied
 * to `sim/` and only half-applied to the 3D copy, so the model lab computed the hull's
 * descent authority from a 650 MW bus while the page computed it from 1,550 MW — and the
 * documentation said the two agreed. It was found by review, not by a test, which is why
 * this file exists.
 *
 * A number that appears in both files must be identical. If a divergence is ever
 * deliberate, the right move is to delete the field from one side, not to loosen this.
 */
import { describe, it, eq } from '../harness.js';
import { CLASSES, CLASS_ORDER, DEFAULTS } from '../../sim/index.js?v=bdd5b410';
import { ASSUMPTIONS, resolveClass } from '../../3d/model/config.js?v=7439a398';

/** sim field -> 3D field, for every quantity both files claim to know. */
const SHARED = {
  payloadT: 'payloadTonnes',
  dispM3: 'displacementM3',
  lenM: 'lengthM',
  // Both anchor rules compute first contact from the hull's radius, so the two files have to
  // publish the same diameter — see anchor-parity.cases.js.
  diaM: 'nominalDiameterM',
  diskM2: 'publishedDiscAreaM2',
  genMW: 'generatorContinuousPowerMW',
  battMWh: 'batteryEnergyMWh',
  battMW: 'batteryPeakPowerMW',
  cryoMW: 'cryogenicPowerMW',
  // ln2CapT used to be excluded, because the two files disagreed for a written reason: the
  // 3D bank held 30/150/700 t against the monitor's 50/500/5000 t plan target, and
  // adapter/fable.js divides by the 3D figure so that tonnes conserve end to end. Both
  // numbers were arbitrary. The 2026-08-09 resize gave the tank a REQUIREMENT — hold enough
  // nitrogen to sink an empty hull at ground level with no rotors — so there is one right
  // answer now and no reason for two. The exclusion is deleted rather than loosened.
  ln2CapT: 'ln2TankCapacityTonnes',
  // The descent anchor and the hose it works alongside. Both files draw and compute from these,
  // so both files have to agree about them — this is the pair that would otherwise let the 3D
  // show a bag of one size while the model sizes the descent around another.
  hoseM: 'hoseLengthM',
  anchorM: 'anchorCableM',
  anchorBagT: 'anchorBagTonnes',
  solarM2: 'solarAreaM2',
};

/* Tunables both files carry, sim CFG key -> 3D ASSUMPTIONS key. Same rule as the specs above:
 * a number in both files must be identical. These two were added on 2026-08-09 because the old
 * 200 W/m2 solar figure existed in FIVE places and the nitrogen round trip in two, and both were
 * wrong in every copy — a duplicated constant is wrong everywhere or nowhere, and the only
 * defence is a test that reads both. */
const SHARED_ASSUMPTIONS = {
  eLN2: 'eLN2',
  rtLN2: 'rtLN2',
  pumpEta: 'pumpEta',
  propEta: 'propEta',
  Cd: 'Cd',
  rhoAir: 'rhoAir',
  rhoSL: 'rhoSL',
  solarWPerM2: 'solarWPerM2',
};

describe('the shared assumptions, in both copies', () => {
  for (const [simKey, vizKey] of Object.entries(SHARED_ASSUMPTIONS)) {
    it(`${simKey} matches 3d ASSUMPTIONS.${vizKey}`, () => {
      const a = DEFAULTS[simKey], b = ASSUMPTIONS[vizKey];
      if (typeof a !== 'number') throw new Error(`sim DEFAULTS.${simKey} is ${a}`);
      if (typeof b !== 'number') throw new Error(`3d ASSUMPTIONS.${vizKey} is ${b}`);
      eq(b, a, `${simKey}: sim says ${a}, 3d says ${b}`);
    });
  }

  it('the nitrogen store cannot return more work than the liquid holds', () => {
    // LN2 exergy at 1 bar against a 288 K ambient is 173.4 kWh/t (Arnaiz-del-Pozo 2020), so
    // rtLN2 * eLN2 * 1000 must stay under it. This is not a tuning bound, it is the second law,
    // and the model published rtLN2 = 0.50 (225 kWh/t) until 2026-08-09.
    const recoveredKWhPerT = DEFAULTS.rtLN2 * DEFAULTS.eLN2 * 1000;
    if (recoveredKWhPerT > 173.4) {
      throw new Error(`recovers ${recoveredKWhPerT.toFixed(1)} kWh/t from a liquid holding 173.4`);
    }
  });

  it('the solar skin does not out-convert the sun', () => {
    // 264 W/m2 day-averaged incident (NRCan, BC interior July). Anything above about a quarter
    // of that is claiming a conversion efficiency nobody has ever demonstrated.
    if (DEFAULTS.solarWPerM2 > 264 * 0.30) {
      throw new Error(`${DEFAULTS.solarWPerM2} W/m2 needs ${(DEFAULTS.solarWPerM2 / 264 * 100).toFixed(0)}% conversion`);
    }
  });
});

describe('the vehicle specification, in both copies', () => {
  for (const id of CLASS_ORDER) {
    const sim = CLASSES[id];
    const viz = resolveClass(id);

    for (const [simKey, vizKey] of Object.entries(SHARED)) {
      const a = sim[simKey];
      const b = viz[vizKey];
      it(`${id}: ${simKey} matches 3d ${vizKey}`, () => {
        // A MISSPELLED FIELD MUST FAIL, NOT SKIP. The first version of this file skipped
        // any pair where either side was undefined, on the reasoning that a field only one
        // side carries is not a disagreement. The effect was that `cryogenicPlantPowerMW`,
        // which does not exist — the field is `cryogenicPowerMW` — quietly compared nothing
        // at all. A guard with a typo in it is worse than no guard, because it reports
        // green. Every name in SHARED must resolve on both sides.
        eq(a !== undefined, true, `sim/config.js has no field "${simKey}"`);
        eq(b !== undefined, true, `3d/model/config.js has no field "${vizKey}"`);
        eq(b, a, `sim says ${a}, the 3D model says ${b} — one of them is illustrating a `
          + 'vehicle the other is not computing');
      });
    }

    it(`${id}: the 3D rotor diameter reproduces the published disc area`, () => {
      // The 3D file chooses a rotor diameter so that stations x rotors x disc area lands
      // on the number the page publishes. If the page's figure moves and the diameter does
      // not, the illustration shows a rotor that cannot do what the text claims.
      const area = viz.primaryRotorStations * viz.rotorsPerStation
        * Math.PI * (viz.primaryRotorDiameterM / 2) ** 2;
      const err = Math.abs(area - sim.diskM2) / sim.diskM2;
      eq(err < 0.10, true,
        `${id}: ${viz.primaryRotorStations}x${viz.rotorsPerStation} rotors of `
        + `${viz.primaryRotorDiameterM} m give ${Math.round(area)} m2, but the page `
        + `publishes ${sim.diskM2} m2 (${(err * 100).toFixed(1)}% out)`);
    });
  }
});
