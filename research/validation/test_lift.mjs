import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { test } from 'node:test';
import { grossLiftKg, ledger } from '../../sim/physics.js?v=1ead4525';
// Follow the stamped imports so the live density dial is the ledger's singleton.
const source = readFileSync(new URL('../../sim/physics.js', import.meta.url), 'utf8');
const dep = async file => import(new URL(source.match(new RegExp(`from '(\\./${file}\\.js[^']*)'`))[1],
  new URL('../../sim/physics.js', import.meta.url)));
const { CFG, CLASSES, setConfig, resetConfig } = await dep('config');
const { airDensity } = await dep('atmosphere');
const state = { pressurePa: 101325, temperatureK: 288.15 };

test('vacuum class lift remains bit-identical over the altitude/density domain', () => {
  try {
    for (const rhoSL of [0.5, 1, 1.225, 1.3, 2]) {
      setConfig({ rhoSL });
      for (let altitude = -2000; altitude <= 11000; altitude += 13) {
        for (const cls of Object.values(CLASSES)) {
          const rho = airDensity(altitude, CFG.rhoSL);
          const liftT = cls.dispM3 * rho / 1000;
          assert.deepEqual(ledger(cls, altitude), { rho, altMslM: altitude, liftT,
            dryT: cls.payloadT, reserveT: liftT-cls.payloadT-cls.payloadT,
            surplusT: liftT-cls.payloadT });
        }
      }
    }
  } finally { resetConfig(); }
});

test('state, gas and purity change lift in the expected directions', () => {
  const lift = gas => grossLiftKg(1000, state, gas);
  assert(lift('vacuum') > lift('hydrogen'));
  assert(lift('hydrogen') > lift('helium'));
  assert.equal(grossLiftKg(1000, state, 'helium', 0), 0);
  assert.equal(grossLiftKg(1000, state, 'helium', 0.5), lift('helium')/2);
  assert.equal(grossLiftKg(1000, { ...state, pressurePa: 202650 }, 'hydrogen'), 2*lift('hydrogen'));
  for (const purity of [-1, 1.01, NaN, Infinity]) assert.throws(() => grossLiftKg(1, state, 'helium', purity));
  assert.throws(() => grossLiftKg(1, state, 'typo'));
  assert.throws(() => grossLiftKg(1, { ...state, temperatureK: 0 }));
  assert.throws(() => grossLiftKg(1, { ...state, airDensityKgM3: NaN }));
});
