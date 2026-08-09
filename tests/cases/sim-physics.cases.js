/* The four first-order relations, against numbers worked out by hand.
 *
 * Every expected value below is derived in its comment from the equation and the constants
 * in sim/config.js, in SI, so that a reader can check the arithmetic without running
 * anything. Where a test pins behaviour that is known to be wrong, it is marked knownFail
 * with the defect it belongs to.
 */
import { close, describe, eq, it, knownFail, ok } from '../harness.js';
import {
  CFG, CLASSES, CLASS_ORDER, DEFAULTS, MODES,
  diskMW, dragMW, ledger, planCycle, pumpMW, resetConfig, setConfig,
} from '../../sim/index.js';

const P100 = CLASSES.P100, P1000 = CLASSES.P1000, P10000 = CLASSES.P10000;

describe('physics · pumpMW', () => {
  it('P-100: rho g Q h / eta = 1.635 MW', () => {
    // 1000 kg/m3 x 9.81 m/s2 x 0.5 m3/s x 250 m = 1,226,250 W of hydraulic power;
    // divided by the all-in efficiency 0.75 that is 1,635,000 W = 1.635 MW.
    resetConfig();
    close(pumpMW(P100), 1.635, 1e-9, 'pumpMW(P-100)');
  });

  it('scales linearly with fill rate: 3 and 15 m3/s give 9.81 and 49.05 MW', () => {
    resetConfig();
    close(pumpMW(P1000), 9.81, 1e-9, 'pumpMW(P-1000)');
    close(pumpMW(P10000), 49.05, 1e-9, 'pumpMW(P-10000)');
  });

  it('reads the live tunables, not the defaults', () => {
    try {
      setConfig({ fillMul: 2 });
      close(pumpMW(P100), 3.27, 1e-9, 'doubling the fill rate doubles pump power');
      resetConfig();
      setConfig({ hoseHead: 500 });
      close(pumpMW(P100), 3.27, 1e-9, 'doubling the head doubles pump power');
      resetConfig();
      setConfig({ pumpEta: 0.375 });
      close(pumpMW(P100), 3.27, 1e-9, 'halving efficiency doubles pump power');
    } finally { resetConfig(); }
  });
});

describe('physics · dragMW', () => {
  it('P-100 balanced: 0.933362 MW at 25 m/s', () => {
    // v = 90 km/h / 3.6 = 25 m/s. A = pi (44/2)^2 = 1520.5308 m2 (frontal disc of the hull).
    // P_drag = 0.5 rho Cd A v^3 = 0.5 x 1.10 x 0.05 x 1520.5308 x 15625 = 653,353 W;
    // over propulsive efficiency 0.70 that is 933,362 W.
    resetConfig();
    close(dragMW(P100, MODES.balanced), 0.9333615674, 1e-9, 'dragMW(P-100, balanced)');
  });

  it('is cubic in speed', () => {
    resetConfig();
    const base = dragMW(P100, MODES.balanced);
    try {
      setConfig({ speedMul: 2 });
      close(dragMW(P100, MODES.balanced) / base, 8, 1e-9, 'doubling airspeed is eight times the drag power');
    } finally { resetConfig(); }
    // The mode multipliers land in the same cube: rapid is 1.15x airspeed.
    close(dragMW(P100, MODES.rapid) / base, 1.15 ** 3, 1e-12, 'rapid mode');
    close(dragMW(P100, MODES.endurance) / base, 0.8 ** 3, 1e-12, 'endurance mode');
  });

  it('is quadratic in diameter at equal speed', () => {
    resetConfig();
    // Same cruise speed, area ratio only: a 2x diameter hull is 4x the frontal area.
    const wide = Object.assign({}, P100, { diaM: 88 });
    close(dragMW(wide, MODES.balanced) / dragMW(P100, MODES.balanced), 4, 1e-12, 'area ratio');
  });
});

describe('physics · diskMW and its inverse', () => {
  it('P-100 at 1 MN of thrust: 19.262853 MW', () => {
    // Actuator-disc induced power: P = T^1.5 / sqrt(2 rho A).
    // T^1.5 = 1e9; sqrt(2 x 1.10 x 2500) = sqrt(5500) = 74.16198; 1e9/74.16198 = 13.484 MW
    // of ideal induced power, over propulsive efficiency 0.70 = 19.2629 MW.
    resetConfig();
    close(diskMW(P100, 1e6), 19.26285321, 1e-7, 'diskMW(P-100, 1 MN)');
  });

  it('non-positive thrust costs nothing', () => {
    eq(diskMW(P100, 0), 0, 'zero thrust');
    eq(diskMW(P100, -5e5), 0, 'negative thrust');
  });

  it('scales as thrust^1.5', () => {
    resetConfig();
    close(diskMW(P100, 4e6) / diskMW(P100, 1e6), 8, 1e-9, 'four times the thrust is eight times the power');
  });

  it('round-trips with rotorMaxT: the thrust planCycle calls the bus limit costs exactly the bus', () => {
    // rotorMaxT (plan.js) inverts diskMW for P = battMW + genMW, converting N to tonnes at
    // 9.81 m/s2. Feeding it back in must return the bus power it was solved for, or the
    // force-closure argument the whole descent rests on is arithmetic against itself.
    resetConfig();
    for (const id of CLASS_ORDER) {
      const c = CLASSES[id];
      const p = planCycle(c, MODES.balanced, 15);
      const bus = c.battMW + c.genMW;
      const back = diskMW(c, p.rotorMaxT * 1000 * 9.81);
      close(back / bus, 1, 1e-12, `${id}: diskMW(rotorMaxT) vs bus`);
    }
  });

  it('rotorMaxT matches the hand-computed values', () => {
    // ((P_bus x eta x sqrt(2 rho A))^(2/3)) / g, in tonnes.
    resetConfig();
    const want = { P100: 160.3391758, P1000: 790.8608228, P10000: 7599.7336651 };
    for (const id of CLASS_ORDER) {
      close(planCycle(CLASSES[id], MODES.balanced, 15).rotorMaxT, want[id], 1e-6, `${id} rotorMaxT (t)`);
    }
  });
});

describe('physics · the buoyancy ledger', () => {
  it('lift is the displaced volume times CFG.rhoSL', () => {
    // 180,000 m3 x 1.225 kg/m3 = 220.5 t for the P-100; 2,205 t and 22,050 t above it.
    resetConfig();
    close(ledger(P100).liftT, 220.5, 1e-9, 'P-100 lift');
    close(ledger(P1000).liftT, 2205, 1e-9, 'P-1000 lift');
    close(ledger(P10000).liftT, 22050, 1e-9, 'P-10000 lift');
  });

  it('the structure allowance is set equal to the payload', () => {
    // Not a mass estimate: the ledger BETS that structure comes in at payload mass. Pinned
    // here because it is the single most consequential assumption in the whole model.
    for (const id of CLASS_ORDER) eq(ledger(CLASSES[id]).dryT, CLASSES[id].payloadT, `${id} dryT`);
  });

  it('reserve = surplus - payload, by construction', () => {
    resetConfig();
    for (const id of CLASS_ORDER) {
      const l = ledger(CLASSES[id]);
      close(l.reserveT, l.surplusT - CLASSES[id].payloadT, 1e-9, `${id} reserve identity`);
      close(l.surplusT, l.liftT - l.dryT, 1e-9, `${id} surplus identity`);
    }
  });

  it('reads CFG.rhoSL live', () => {
    try {
      setConfig({ rhoSL: 1 });
      close(ledger(P100).liftT, 180, 1e-9, 'lift follows the configured sea-level density');
    } finally { resetConfig(); }
  });

  knownFail(
    'lift at the working-band density covers dry mass plus payload',
    'defect 1 — the ledger buys lift at sea level (rhoSL 1.225) while the ships cruise 1500 m up',
    () => {
      // At CFG.rhoAir (1.10 kg/m3, the density the drag model already uses for the working
      // band) the same envelopes displace 198 t / 1,980 t / 19,800 t against 200 / 2,000 /
      // 20,000 t of dry mass plus payload. All three classes are net HEAVY at their own
      // cruise altitude, which contradicts the page's claim that the rotors only push down.
      resetConfig();
      for (const id of CLASS_ORDER) {
        const c = CLASSES[id];
        const liftAtAltitudeT = c.dispM3 * CFG.rhoAir / 1000;
        ok(liftAtAltitudeT >= c.payloadT * 2,
          `${id}: ${liftAtAltitudeT.toFixed(0)} t of lift against ${(c.payloadT * 2).toFixed(0)} t of dry mass plus payload`);
      }
    });
});

describe('physics · constants', () => {
  it('the working-band density is lower than the sea-level density', () => {
    ok(DEFAULTS.rhoAir < DEFAULTS.rhoSL, 'rhoAir < rhoSL');
  });

  it('every efficiency is a fraction', () => {
    for (const k of ['pumpEta', 'propEta', 'rtLN2']) {
      ok(DEFAULTS[k] > 0 && DEFAULTS[k] < 1, `${k} = ${DEFAULTS[k]} is not strictly between 0 and 1`);
    }
  });
});
