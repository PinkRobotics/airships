/* The standard atmosphere, against the published ISA table.
 *
 * This module exists because the buoyancy ledger got its density wrong by a whole kilometre
 * of altitude, so the tests that matter most are the ones that check the numbers against
 * something outside this repository. ISO 2533:1975 tabulates density at every 50 m; the
 * values pinned below are read off that table, not out of this implementation.
 */
import { close, describe, it, ok, throws } from '../harness.js';
import {
  ISA, RHO_SL_ISA, airDensity, altitudeForDensity, densityRatio,
  isaPressurePa, isaTemperatureK,
} from '../../sim/index.js?v=173e4858';

describe('atmosphere · against the ISO 2533 table', () => {
  it('density at 0, 1,000, 2,000, 2,500 and 3,000 m', () => {
    // ISO 2533:1975, kg/m3. The last of these is the top of the band the fleet works in;
    // 2,500 m is the altitude the hulls are sized at, so its value sets every displacement
    // in sim/config.js and is the single most load-bearing number in this file.
    close(airDensity(0), 1.225000, 5e-7, '0 m');
    close(airDensity(1000), 1.111643, 5e-7, '1,000 m');
    close(airDensity(2000), 1.006490, 5e-7, '2,000 m');
    close(airDensity(2500), 0.956859, 5e-7, '2,500 m');
    close(airDensity(3000), 0.909122, 5e-7, '3,000 m');
  });

  it('temperature is the lapse rate and nothing else', () => {
    // 288.15 K at sea level, 6.5 K per km down. 271.90 K at the working altitude, which is
    // -1.25 C: cold enough that a stuck water valve is a plausible failure and warm enough
    // that the standard atmosphere is the right reference to use.
    close(isaTemperatureK(0), 288.15, 1e-12, 'sea level');
    close(isaTemperatureK(2500), 271.90, 1e-12, '2,500 m');
    close(isaTemperatureK(11000), 216.65, 1e-9, 'tropopause');
  });

  it('pressure at the tabulated altitudes', () => {
    // ISO 2533:1975, Pa.
    close(isaPressurePa(0), 101325, 1e-9, 'sea level');
    close(isaPressurePa(2500), 74682.5, 0.1, '2,500 m');
    close(isaPressurePa(11000), 22632.0, 0.1, 'tropopause');
  });

  it('density is pressure over R T at every altitude, which is the only equation here', () => {
    // The three functions are not three models. If this ever fails, one of them has grown a
    // fudge factor.
    for (let h = -2000; h <= 11000; h += 250) {
      close(airDensity(h), isaPressurePa(h) / (ISA.R * isaTemperatureK(h)), 1e-12, `${h} m`);
    }
  });

  it('the sea-level density is derived, not asserted', () => {
    close(RHO_SL_ISA, ISA.P0 / (ISA.R * ISA.T0), 1e-15, 'RHO_SL_ISA');
    close(RHO_SL_ISA, 1.225, 4e-7, 'the familiar 1.225 kg/m3');
  });
});

describe('atmosphere · shape and inverse', () => {
  it('density falls monotonically with altitude', () => {
    let prev = Infinity;
    for (let h = -2000; h <= 11000; h += 100) {
      const r = airDensity(h);
      ok(r < prev, `density did not fall at ${h} m: ${r} against ${prev}`);
      prev = r;
    }
  });

  it('the ratio is dimensionless and anchored at sea level', () => {
    close(densityRatio(0), 1, 1e-15, 'ratio at sea level');
    close(densityRatio(2500), 0.781109, 5e-7, 'ratio at 2,500 m');
    // Scaling the anchor scales the whole column, which is what CFG.rhoSL is for.
    close(airDensity(2500, 2.45) / airDensity(2500, 1.225), 2, 1e-12, 'a doubled anchor');
  });

  it('altitudeForDensity inverts airDensity', () => {
    for (const h of [-1500, 0, 300, 1000, 2500, 5000, 10500]) {
      close(altitudeForDensity(airDensity(h)), h, 1e-8, `round trip at ${h} m`);
    }
  });

  it('states the break-even altitudes the ledger turns on', () => {
    // A hull displacing 2,200 m3 per tonne of payload carries 2 t of loaded ship per tonne.
    // It goes neutral where the air is 2000/2200 = 0.90909 kg/m3, and neutral EMPTY where it
    // is 0.45455. The first of those is the number the resize exists to put above the cruise
    // ceiling: 3,000 m against a 2,500 m ceiling, 500 m of altitude in hand. Before the
    // resize it was 2,000/1,800 = 1.1111 kg/m3, which is 1,005 m — below the drop run.
    close(altitudeForDensity(2000 / 2200), 3000.33, 0.01, 'loaded break-even');
    close(altitudeForDensity(2000 / 1800), 1004.87, 0.01, 'the break-even the resize replaced');
    ok(altitudeForDensity(2000 / 2200) > 2500, 'the loaded hull goes heavy below its own ceiling');
  });
});

describe('atmosphere · the guard rails', () => {
  it('refuses an altitude outside the layer rather than extrapolating', () => {
    throws(() => airDensity(11001), 'above the tropopause');
    throws(() => airDensity(-2001), 'below the tabulated floor');
    throws(() => airDensity(NaN), 'NaN');
    throws(() => airDensity(undefined), 'a missing argument');
    throws(() => isaTemperatureK('1000'), 'a string');
  });

  it('refuses a density that is not a positive number', () => {
    throws(() => altitudeForDensity(0), 'zero');
    throws(() => altitudeForDensity(-1), 'negative');
    throws(() => altitudeForDensity(NaN), 'NaN');
    throws(() => altitudeForDensity(4), 'denser than anything in the layer');
  });

  it('names the altitude in the error, so a bad caller is findable', () => {
    let msg = '';
    try { airDensity(20000); } catch (e) { msg = String(e.message || e); }
    ok(msg.includes('20000'), `the error did not name the altitude: ${JSON.stringify(msg)}`);
  });
});
