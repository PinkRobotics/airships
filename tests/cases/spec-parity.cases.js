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
import { CLASSES, CLASS_ORDER } from '../../sim/index.js';
import { resolveClass } from '../../3d/model/config.js';

/** sim field -> 3D field, for every quantity both files claim to know. */
const SHARED = {
  payloadT: 'payloadTonnes',
  dispM3: 'displacementM3',
  lenM: 'lengthM',
  diskM2: 'publishedDiscAreaM2',
  genMW: 'generatorContinuousPowerMW',
  battMWh: 'batteryEnergyMWh',
  battMW: 'batteryPeakPowerMW',
  cryoMW: 'cryogenicPlantPowerMW',
  // ln2CapT is deliberately NOT compared: the model's tank bank (30/150/700 t) is smaller
  // than the monitor's plan target (50/500/5000 t), and adapter/fable.js documents at
  // length why converting between them by capacity is the only choice that conserves
  // tonnes end to end. A difference with a written reason is not drift.
  solarM2: 'solarAreaM2',
};

describe('the vehicle specification, in both copies', () => {
  for (const id of CLASS_ORDER) {
    const sim = CLASSES[id];
    const viz = resolveClass(id);

    for (const [simKey, vizKey] of Object.entries(SHARED)) {
      const a = sim[simKey];
      const b = viz[vizKey];
      // A field one side does not carry is not a disagreement; a field both carry is.
      if (a === undefined || b === undefined) continue;
      it(`${id}: ${simKey} matches 3d ${vizKey}`, () => {
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
