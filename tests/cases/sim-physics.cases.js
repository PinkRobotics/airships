/* The four first-order relations, against numbers worked out by hand.
 *
 * Every expected value below is derived in its comment from the equation and the constants
 * in sim/config.js, in SI, so that a reader can check the arithmetic without running
 * anything. Where a test pins behaviour that is known to be wrong, it is marked knownFail
 * with the defect it belongs to.
 */
import { close, describe, eq, it, ok, throws } from '../harness.js';
import {
  BUS_CEILING, CFG, CLASSES, CLASS_ORDER, DEFAULTS, MODES, TERRAIN_MSL, WORK_ALT_MSL,
  airDensity, diskMW, dragMW, ledger, planCycle, pumpMW, resetConfig, setConfig,
} from '../../sim/index.js?v=979323dd';

const P100 = CLASSES.P100, P1000 = CLASSES.P1000, P10000 = CLASSES.P10000;

describe('physics · pumpMW', () => {
  it('P-100: rho g Q h / eta = 1.962 MW', () => {
    // 1000 kg/m3 x 9.81 m/s2 x 0.5 m3/s x 300 m = 1,471,500 W of hydraulic power;
    // divided by the all-in efficiency 0.75 that is 1,962,000 W = 1.962 MW.
    // The head is the class's own hose length now, not one global 250 m — see hoseM.
    resetConfig();
    close(pumpMW(P100), 1.962, 1e-9, 'pumpMW(P-100)');
  });

  it('scales linearly with fill rate: 3 and 15 m3/s at 300 m give 11.77 and 58.86 MW', () => {
    // Every class hangs 300 m over the water, so at a common head the pump power is linear in
    // flow alone. The hoses were briefly 1,100 and 1,350 m — an attempt to keep the big hulls
    // out of the dense air near the surface — which worked and cost 29 MWh a cycle. The
    // descent anchor does that job for 0.11 MWh, so the hoses went back to being hoses.
    resetConfig();
    close(pumpMW(P1000), 1000 * 9.81 * 3 * 300 / 0.75 / 1e6, 1e-9, 'pumpMW(P-1000)');
    close(pumpMW(P10000), 1000 * 9.81 * 15 * 300 / 0.75 / 1e6, 1e-9, 'pumpMW(P-10000)');
    close(pumpMW(P1000), 11.772, 1e-3, 'P-1000 in MW');
    close(pumpMW(P10000), 58.86, 1e-3, 'P-10000 in MW');
  });

  it('reads the live tunables, not the defaults', () => {
    try {
      setConfig({ fillMul: 2 });
      close(pumpMW(P100), 3.924, 1e-9, 'doubling the fill rate doubles pump power');
      resetConfig();
      setConfig({ hoseMul: 2 });
      close(pumpMW(P100), 3.924, 1e-9, 'doubling the hose doubles pump power');
      resetConfig();
      setConfig({ pumpEta: 0.375 });
      close(pumpMW(P100), 3.924, 1e-9, 'halving efficiency doubles pump power');
    } finally { resetConfig(); }
  });
});

describe('physics · dragMW', () => {
  it('P-100 drag at the local working altitude', () => {
    resetConfig();
    // ISA density at 2500 m MSL, frontal disk and 25 m/s airspeed.
    const rho = 1.225 * (1 - 0.0065 * WORK_ALT_MSL / 288.15) ** (9.80665 / (287.0528 * 0.0065) - 1);
    const expected = 0.5 * rho * 0.05 * Math.PI * (55 / 2) ** 2 * 25 ** 3 / 0.70 / 1e6;
    close(dragMW(P100, MODES.balanced), expected, 1e-8, 'local drag power');
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
    const wide = Object.assign({}, P100, { diaM: P100.diaM * 2 });
    close(dragMW(wide, MODES.balanced) / dragMW(P100, MODES.balanced), 4, 1e-12, 'area ratio');
  });
});

describe('physics · diskMW and its inverse', () => {
  it('P-100 at 1 MN uses the local working-altitude density', () => {
    resetConfig();
    const rho = 1.225 * (1 - 0.0065 * WORK_ALT_MSL / 288.15) ** (9.80665 / (287.0528 * 0.0065) - 1);
    close(diskMW(P100, 1e6), 1e9 / Math.sqrt(2 * rho * 2500) / 0.7 / 1e6, 1e-7, 'local rotor power');
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
    // rotorMaxT (power.js rotorMaxTonnes) inverts diskMW for the share of the DESCENT bus the
    // rotors may take — BUS_CEILING of the battery plus what the nitrogen store returns during
    // the approach (plan.busMW), not battMW + genMW: a generator with no fuel aboard is storage
    // (defect 6). Feeding it back in must return the power it was solved for, or the
    // force-closure argument the whole descent rests on is arithmetic against itself.
    resetConfig();
    for (const id of CLASS_ORDER) {
      const c = CLASSES[id];
      const p = planCycle(c, MODES.balanced, 15);
      ok(p.busMW > c.battMW && p.busMW < c.battMW + c.genMW,
        `${id}: the descent bus ${p.busMW} MW should sit between the battery and the nameplate`);
      const back = diskMW(c, p.rotorMaxT * 1000 * 9.81, p.ledLow.rho);
      close(back / (BUS_CEILING * p.busMW), 1, 1e-12, `${id}: diskMW(rotorMaxT) vs the rotors' share of the bus`);
    }
  });

  it('rotorMaxT matches the hand-computed values', () => {
    // ((0.95 x P_bus x eta x sqrt(2 rho A))^(2/3)) / g, in tonnes, with P_bus the honest descent
    // bus: 31.48 / 154.04 / 1,406.84 MW at the worked example. Before 2026-10-01 the bus was the
    // nameplate 38 / 190 / 1,550 MW with no ceiling, and these read 160.3 / 790.9 / 7,599.7 t.
    resetConfig();
    const want = { P100: 136.6819318, P1000: 664.5193501, P10000: 6884.7755194 }; // prior 95% bus values
    for (const id of CLASS_ORDER) {
      close(planCycle(CLASSES[id], MODES.balanced, 15).rotorMaxT, want[id] / Math.pow(0.95, 2/3) * Math.cbrt(airDensity(TERRAIN_MSL + 300, CFG.rhoSL) / 1.10), 1e-6, `${id} rotorMaxT (t)`);
    }
  });
});

describe('physics · the buoyancy ledger', () => {
  it('lift is the displaced volume times the air density AT THE STATED ALTITUDE', () => {
    // 220,000 m3 x 1.225 kg/m3 = 269.5 t for the P-100 at sea level, where it never goes;
    // x 0.956859 = 210.509 t at the 2,500 m it is sized for. The second number is the one
    // that matters and the first is here to show the size of the error the altitude
    // argument removed: 28% of the P-100's lift, and the sign of its net force.
    resetConfig();
    close(ledger(P100, 0).liftT, 269.5, 1e-9, 'P-100 lift at sea level');
    close(ledger(P1000, 0).liftT, 2695, 1e-9, 'P-1000 lift at sea level');
    close(ledger(P10000, 0).liftT, 26950, 1e-9, 'P-10000 lift at sea level');
    close(ledger(P100, WORK_ALT_MSL).liftT, 210.509, 5e-4, 'P-100 lift at 2,500 m');
    for (const id of CLASS_ORDER) {
      const c = CLASSES[id];
      close(ledger(c, WORK_ALT_MSL).liftT, c.dispM3 * airDensity(WORK_ALT_MSL, CFG.rhoSL) / 1000,
        1e-9, `${id}: liftT is rho(h) V`);
    }
  });

  it('refuses to guess the altitude', () => {
    // The whole of defect 1 was a default that silently meant sea level. There is no default
    // now, and a caller that has not decided where it is cannot get a number at all.
    throws(() => ledger(P100), 'a missing altitude');
    throws(() => ledger(P100, null), 'a null altitude');
    throws(() => ledger(P100, NaN), 'a NaN altitude');
  });

  it('the structure allowance is set equal to the payload', () => {
    // Not a mass estimate: the ledger BETS that structure comes in at payload mass. Pinned
    // here because it is the single most consequential assumption in the whole model.
    for (const id of CLASS_ORDER) {
      eq(ledger(CLASSES[id], WORK_ALT_MSL).dryT, CLASSES[id].payloadT, `${id} dryT`);
    }
  });

  it('reserve = surplus - payload, by construction, at any altitude', () => {
    resetConfig();
    for (const id of CLASS_ORDER) for (const h of [0, TERRAIN_MSL, WORK_ALT_MSL]) {
      const l = ledger(CLASSES[id], h);
      close(l.reserveT, l.surplusT - CLASSES[id].payloadT, 1e-9, `${id} at ${h} m: reserve identity`);
      close(l.surplusT, l.liftT - l.dryT, 1e-9, `${id} at ${h} m: surplus identity`);
      eq(l.altMslM, h, `${id}: the ledger reports where it was evaluated`);
    }
  });

  it('lift falls with altitude, and says so', () => {
    resetConfig();
    for (const id of CLASS_ORDER) {
      const low = ledger(CLASSES[id], TERRAIN_MSL), high = ledger(CLASSES[id], WORK_ALT_MSL);
      ok(high.liftT < low.liftT, `${id}: ${high.liftT} t at altitude is not less than ${low.liftT} t at the ground`);
      close(high.liftT / low.liftT, 0.860761, 1e-6, `${id}: 1,500 m of climb costs 14% of the lift`);
    }
  });

  it('reads CFG.rhoSL live, as the anchor of the whole column', () => {
    try {
      setConfig({ rhoSL: 1 });
      close(ledger(P100, 0).liftT, 220, 1e-9, 'lift at sea level follows the configured density');
      close(ledger(P100, WORK_ALT_MSL).liftT, 220 * 0.781109, 1e-4, 'and so does lift at altitude');
    } finally { resetConfig(); }
  });

  it('FAIL-SAFE FLOAT-UP: every class is buoyant fully loaded at its working altitude', () => {
    // Was `knownFail` for defect 1, which is fixed as of 2026-08-09 — see
    // docs/OPEN-QUESTIONS.md #1. The old test asked the weaker question, whether the hull
    // floated at CFG.rhoAir; this asks the requirement the classes were resized to meet.
    //
    // The hull must lift itself, its structure and a full payload of water it CANNOT DROP,
    // in the thinnest air of the cycle, with 5% to spare. 2,200 m3 of displacement per tonne
    // of payload against 0.956859 kg/m3 gives 2.1051 t of lift per 2 t of loaded ship. The
    // margin is identical for all three classes because dry mass is set equal to payload for
    // all three, so no class needs an exception and none is granted one.
    resetConfig();
    for (const id of CLASS_ORDER) {
      const c = CLASSES[id];
      const l = ledger(c, WORK_ALT_MSL);
      const loadedT = l.dryT + c.payloadT;
      ok(l.liftT >= loadedT * 1.05,
        `${id}: ${l.liftT.toFixed(1)} t of lift against ${loadedT.toFixed(1)} t of loaded ship`);
      close(l.liftT / loadedT, 1.05254, 1e-5, `${id}: the stated float-up margin`);
    }
  });

  it('UNPOWERED RECOVERY: the nitrogen tanks can sink an empty hull at ground level', () => {
    // A hull that floats up when it dies has to be able to come back down without rotors,
    // and the binding altitude is the BOTTOM of that descent, not the top: at TERRAIN_MSL
    // the air is 16% denser than at the ceiling and the empty hull is correspondingly more
    // buoyant. Ballast sized for 2,500 m would stall the ship at about 2,065 m for ever.
    resetConfig();
    for (const id of CLASS_ORDER) {
      const c = CLASSES[id];
      const atCeiling = ledger(c, WORK_ALT_MSL).surplusT;
      const atGround = ledger(c, TERRAIN_MSL).surplusT;
      ok(atGround > atCeiling, `${id}: the ground is not the harder case`);
      ok(c.ln2CapT >= atGround,
        `${id}: ${c.ln2CapT} t of LN2 against ${atGround.toFixed(1)} t of surplus at ${TERRAIN_MSL} m`);
      close(c.ln2CapT / atGround, 1.0722, 1e-3, `${id}: the stated ballast margin`);
      close(c.ln2CapT / c.payloadT, 1.55, 1e-12, `${id}: 1.55 payloads of nitrogen`);
    }
  });
});

describe('physics · constants', () => {
  it('the working-band density is lower than the sea-level density', () => {
    ok(DEFAULTS.rhoAir < DEFAULTS.rhoSL, 'rhoAir < rhoSL');
  });

  it('rhoAir does NOT agree with the altitude the ledger works at, and that is tracked', () => {
    // The ledger buys lift at 0.9569 kg/m3 while drag and every rotor calculation still use
    // a flat 1.10, which is ISA at about 990 m. Drag is therefore overstated by 15% and
    // induced power understated by 7%. Both belong to defect 2 — the power model — and this
    // pins the gap so it cannot be forgotten now that the ledger is honest.
    const work = airDensity(WORK_ALT_MSL, DEFAULTS.rhoSL);
    ok(DEFAULTS.rhoAir > work, `rhoAir ${DEFAULTS.rhoAir} is not above the working density ${work}`);
    close(DEFAULTS.rhoAir / work, 1.1496, 1e-4, 'the size of the remaining inconsistency');
  });

  it('every efficiency is a fraction', () => {
    for (const k of ['pumpEta', 'propEta', 'rtLN2']) {
      ok(DEFAULTS[k] > 0 && DEFAULTS[k] < 1, `${k} = ${DEFAULTS[k]} is not strictly between 0 and 1`);
    }
  });
});
