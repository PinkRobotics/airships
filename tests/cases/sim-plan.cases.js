/* planCycle: the function every published figure comes out of.
 *
 * These are invariants rather than magic numbers wherever an invariant exists, because the
 * magic numbers are already pinned byte-for-byte in tests/golden/. What matters here is
 * that the arithmetic cannot silently stop making sense: the books balance, more distance
 * never buys more water, and a tailwind out is a headwind home.
 */
import { close, describe, eq, it, knownFail, ok } from '../harness.js';
import {
  CFG, CLASSES, CLASS_ORDER, MODES,
  planCycle, resetConfig, setConfig,
} from '../../sim/index.js';

const MODE_IDS = Object.keys(MODES);
const KMS = [2, 5, 15, 30, 60, 120, 400];
const BOTTLENECKS = new Set([
  'transit distance',
  'water handling at the source',
  'cryogenic production rate',
  'descent authority',
  'descent ballast — cryogenic capacity',
]);

/** Every (class, mode, distance) combination, with the config at its documented defaults. */
function grid(fn) {
  resetConfig();
  for (const id of CLASS_ORDER) {
    for (const mid of MODE_IDS) {
      for (const km of KMS) fn(planCycle(CLASSES[id], MODES[mid], km), `${id}/${mid}/${km}km`, CLASSES[id], MODES[mid], km);
    }
  }
}

describe('plan · the books balance', () => {
  it('delivered + retained = payload, everywhere', () => {
    grid((p, tag, c) => close(p.deliveredT + p.retainedT, c.payloadT, 1e-9, `${tag}: mass book`));
  });

  it('nothing is negative and nothing is infinite', () => {
    grid((p, tag) => {
      for (const [k, v] of Object.entries(p.dur)) {
        ok(isFinite(v) && v > 0, `${tag}: duration ${k} = ${v}`);
      }
      ok(isFinite(p.cycleMin) && p.cycleMin > 0, `${tag}: cycleMin = ${p.cycleMin}`);
      ok(isFinite(p.eCycleMWh) && p.eCycleMWh > 0, `${tag}: eCycleMWh = ${p.eCycleMWh}`);
      ok(isFinite(p.kwhPerTonne) && p.kwhPerTonne > 0, `${tag}: kwhPerTonne = ${p.kwhPerTonne}`);
      ok(p.deliveredT > 0, `${tag}: deliveredT = ${p.deliveredT}`);
      ok(p.retainedT >= 0, `${tag}: retainedT = ${p.retainedT}`);
      ok(p.ln2MakeT >= 0, `${tag}: ln2MakeT = ${p.ln2MakeT}`);
      ok(p.eBack >= 0, `${tag}: eBack = ${p.eBack}`);
    });
  });

  it('cycleMin is the sum of the six phase durations', () => {
    grid((p, tag) => {
      const sum = Object.values(p.dur).reduce((a, b) => a + b, 0);
      close(p.cycleMin, sum, 1e-9, `${tag}: cycleMin vs phase sum`);
      eq(Object.keys(p.dur).length, 6, `${tag}: six phases`);
    });
  });

  it('the derived rates are consistent with the cycle', () => {
    grid((p, tag) => {
      close(p.tph, p.deliveredT * 60 / p.cycleMin, 1e-9, `${tag}: tonnes per hour`);
      close(p.dropsPerHour, 60 / p.cycleMin, 1e-12, `${tag}: drops per hour`);
      close(p.kwhPerTonne, p.eCycleMWh * 1000 / Math.max(1, p.deliveredT), 1e-9, `${tag}: kWh per tonne`);
    });
  });

  it('the drop-pass count is odd, so the run ends at the far end of the line', () => {
    // BUOYANCY_ESCAPE picks the ship up at sB. An even count would leave it at sA and the
    // map would jump the length of the drop line at the phase seam.
    grid((p, tag) => {
      ok(Number.isInteger(p.passes) && p.passes >= 1, `${tag}: passes = ${p.passes}`);
      eq(p.passes % 2, 1, `${tag}: even pass count ${p.passes}`);
    });
  });

  it('the bottleneck is one of the five named constraints', () => {
    grid((p, tag) => ok(BOTTLENECKS.has(p.bottleneck), `${tag}: unknown bottleneck ${JSON.stringify(p.bottleneck)}`));
  });

  it('descent power never exceeds the bus', () => {
    grid((p, tag, c) => ok(p.downMW <= (c.battMW + c.genMW) * 1.01,
      `${tag}: downMW ${p.downMW.toFixed(1)} against a ${(c.battMW + c.genMW)} MW bus`));
  });
});

describe('plan · distance', () => {
  it('a longer haul is a longer cycle and less water per hour', () => {
    resetConfig();
    for (const id of CLASS_ORDER) for (const mid of MODE_IDS) {
      let prev = null;
      for (const km of KMS) {
        const p = planCycle(CLASSES[id], MODES[mid], km);
        if (prev) {
          ok(p.cycleMin > prev.cycleMin, `${id}/${mid}: ${km} km is not a longer cycle than the step before it`);
          ok(p.tph < prev.tph, `${id}/${mid}: ${km} km does not lower throughput`);
        }
        prev = p;
      }
    }
  });

  it('transit time is linear in distance once the floor is clear of it', () => {
    // dur.OUTBOUND_TRANSIT is km/gs x 60 x 1/0.85 above a short-leg floor. Doubling a long
    // leg must double the transit; anything else means the ramp factor has moved.
    resetConfig();
    const a = planCycle(CLASSES.P1000, MODES.balanced, 100);
    const b = planCycle(CLASSES.P1000, MODES.balanced, 200);
    close(b.dur.OUTBOUND_TRANSIT / a.dur.OUTBOUND_TRANSIT, 2, 1e-9, 'outbound doubles');
    close(b.dur.RETURN_TRANSIT / a.dur.RETURN_TRANSIT, 2, 1e-9, 'return doubles');
    // The trapezoid costs 1/0.85 over the naive quotient: 100 km at 110 km/h is 54.55 min,
    // not 54.55 x 0.85 = 46.36.
    close(a.dur.OUTBOUND_TRANSIT, 100 / 110 * 60 / 0.85, 1e-9, 'ramp factor');
  });
});

describe('plan · wind', () => {
  const wind = (spd, dir, bearing) => ({ spd, dir, bearing });

  it('no wind means no wind: both legs fly the airspeed', () => {
    resetConfig();
    const kph = CLASSES.P1000.cruiseKph * MODES.balanced.speed;
    const p = planCycle(CLASSES.P1000, MODES.balanced, 40);
    close(p.gsOut, kph, 1e-12, 'gsOut');
    close(p.gsRet, kph, 1e-12, 'gsRet');
    eq(p.tailOut, 0, 'tailOut');
    eq(p.windUsed, false, 'windUsed');
  });

  it('a wind without a route bearing does not touch the legs', () => {
    resetConfig();
    const still = planCycle(CLASSES.P1000, MODES.balanced, 40);
    const p = planCycle(CLASSES.P1000, MODES.balanced, 40, { spd: 40, dir: 270, bearing: null });
    close(p.gsOut, still.gsOut, 1e-12, 'outbound leg');
    close(p.gsRet, still.gsRet, 1e-12, 'return leg');
    eq(p.tailOut, 0, 'tailOut');
  });

  knownFail(
    'windUsed is false when the wind was not applied',
    'windUsed tests only wind.spd, while the legs also require wind.bearing — the flag can claim a wind the plan ignored',
    () => {
      // Harmless today: mission.js always sets m.wind.bearing before planning, so the two
      // conditions never come apart on the live page. It is still a flag that can lie, and
      // the cockpit reads it to decide whether to say "wind applied".
      resetConfig();
      const p = planCycle(CLASSES.P1000, MODES.balanced, 40, { spd: 40, dir: 270, bearing: null });
      eq(p.windUsed, false, 'windUsed');
    });

  it('a tailwind out is a headwind home: the two ground speeds average to the airspeed', () => {
    resetConfig();
    const kph = CLASSES.P1000.cruiseKph * MODES.balanced.speed;   // 110 km/h
    for (const dir of [0, 45, 90, 180, 270, 315]) {
      for (const bearing of [0, 30, 90, 175, 260]) {
        const p = planCycle(CLASSES.P1000, MODES.balanced, 40, wind(20, dir, bearing));
        // 20 km/h against 110 km/h of airspeed is nowhere near the 0.35x/1.8x clamps.
        close((p.gsOut + p.gsRet) / 2, kph, 1e-9, `dir ${dir} bearing ${bearing}: legs are not symmetric about the airspeed`);
        close(p.gsOut, kph + p.tailOut, 1e-9, `dir ${dir} bearing ${bearing}: gsOut vs the reported tail component`);
      }
    }
  });

  it('a west wind on an eastbound leg is faster out and slower home', () => {
    resetConfig();
    const still = planCycle(CLASSES.P100, MODES.balanced, 30);
    const blown = planCycle(CLASSES.P100, MODES.balanced, 30, wind(40, 270, 90));
    ok(blown.tailOut > 0, `tailOut = ${blown.tailOut}`);
    ok(blown.dur.OUTBOUND_TRANSIT < still.dur.OUTBOUND_TRANSIT, 'outbound is not quicker');
    ok(blown.dur.RETURN_TRANSIT > still.dur.RETURN_TRANSIT, 'return is not slower');
    eq(blown.windUsed, true, 'windUsed');
  });

  it('a storm is clamped to between 0.35x and 1.8x the airspeed', () => {
    resetConfig();
    const kph = CLASSES.P100.cruiseKph * MODES.balanced.speed;    // 90 km/h
    const gale = planCycle(CLASSES.P100, MODES.balanced, 30, wind(400, 270, 90));
    close(gale.gsOut, kph * 1.8, 1e-9, 'tailwind clamp');
    close(gale.gsRet, kph * 0.35, 1e-9, 'headwind clamp');
  });

  it('a crosswind costs nothing in this first-order model', () => {
    // The model takes the along-track component only; there is no drift angle and no
    // penalty for flying one. Pinned so the simplification stays visible.
    resetConfig();
    const still = planCycle(CLASSES.P1000, MODES.balanced, 40);
    const cross = planCycle(CLASSES.P1000, MODES.balanced, 40, wind(60, 90, 0));
    close(cross.cycleMin, still.cycleMin, 1e-9, 'a pure crosswind changes the cycle');
  });
});

describe('plan · modes', () => {
  it('rapid transits fastest, endurance slowest', () => {
    resetConfig();
    for (const id of CLASS_ORDER) {
      const r = planCycle(CLASSES[id], MODES.rapid, 60);
      const b = planCycle(CLASSES[id], MODES.balanced, 60);
      const e = planCycle(CLASSES[id], MODES.endurance, 60);
      ok(r.dur.OUTBOUND_TRANSIT < b.dur.OUTBOUND_TRANSIT, `${id}: rapid is not quicker than balanced`);
      ok(b.dur.OUTBOUND_TRANSIT < e.dur.OUTBOUND_TRANSIT, `${id}: balanced is not quicker than endurance`);
      ok(r.tph > b.tph && b.tph > e.tph, `${id}: throughput does not fall from rapid to endurance`);
    }
  });

  it('flying faster costs more per leg: transit energy goes as the square of airspeed', () => {
    // Drag power is cubic in speed and the leg is inversely proportional to it, so the
    // energy to cover a fixed distance goes as v^2. Rapid is 1.15x airspeed, endurance
    // 0.8x, so the outbound leg costs (1.15/0.8)^2 = 2.07 times as much in rapid.
    resetConfig();
    for (const id of CLASS_ORDER) {
      const legE = m => { const p = planCycle(CLASSES[id], m, 60); return p.dragMW * p.dur.OUTBOUND_TRANSIT / 60; };
      const r = legE(MODES.rapid), b = legE(MODES.balanced), e = legE(MODES.endurance);
      ok(r > b && b > e, `${id}: outbound energy ${r.toFixed(2)} / ${b.toFixed(2)} / ${e.toFixed(2)} MWh`);
      close(r / e, (1.15 / 0.8) ** 2, 1e-9, `${id}: rapid against endurance`);
    }
  });

  it('the total cycle energy is NOT monotonic in mode, because the cryogenic share is not', () => {
    // Worth stating because it is the opposite of what the mode names suggest. Endurance
    // runs the cryo plant at full share and a longer cycle, so on the P-10000 at 60 km the
    // rapid cycle (249.2 MWh) costs more than the balanced one (245.8) and less than the
    // endurance one (253.6). A reader comparing modes should compare per tonne, not per cycle.
    resetConfig();
    const e = m => planCycle(CLASSES.P10000, m, 60).eCycleMWh;
    ok(e(MODES.rapid) > e(MODES.balanced), 'rapid is no longer dearer than balanced on the P-10000');
    ok(e(MODES.endurance) > e(MODES.rapid), 'endurance is no longer the dearest cycle on the P-10000');
  });
});

describe('plan · the tunables reach the plan', () => {
  it('speedMul shortens the transit legs', () => {
    resetConfig();
    const before = planCycle(CLASSES.P1000, MODES.balanced, 100).dur.OUTBOUND_TRANSIT;
    try {
      setConfig({ speedMul: 2 });
      close(planCycle(CLASSES.P1000, MODES.balanced, 100).dur.OUTBOUND_TRANSIT, before / 2, 1e-9, 'twice the airspeed, half the leg');
    } finally { resetConfig(); }
  });

  it('fillMul shortens the fill', () => {
    resetConfig();
    const before = planCycle(CLASSES.P1000, MODES.balanced, 100).dur.WATER_FILL;
    try {
      setConfig({ fillMul: 4 });
      close(planCycle(CLASSES.P1000, MODES.balanced, 100).dur.WATER_FILL, before / 4, 1e-9, 'four times the pump, a quarter of the fill');
    } finally { resetConfig(); }
  });

  it('the fill is payload over flow: 1,000 t at 3 m3/s is 5.56 minutes', () => {
    resetConfig();
    close(planCycle(CLASSES.P1000, MODES.balanced, 15).dur.WATER_FILL, 1000 / 3 / 60, 1e-9, 'P-1000 fill');
    close(planCycle(CLASSES.P100, MODES.balanced, 15).dur.WATER_FILL, 100 / 0.5 / 60, 1e-9, 'P-100 fill');
  });
});

describe('plan · the mechanisms the copy describes', () => {
  it('retained descent ballast is zero for every class, mode and distance', () => {
    // The page describes retaining water as descent ballast. It never happens: rotorMaxT /
    // 0.6 alone exceeds the buoyant surplus for all three classes, so the max() in plan.js
    // always clamps to zero and "descent ballast" is inert. Pinned deliberately — if this
    // test starts failing, either the class table or the ballast rule has moved and the
    // copy on the site has to change with it.
    grid((p, tag) => eq(p.retainedT, 0, `${tag}: retainedT`));
  });

  it('at the worked example the cryogenic plant makes under 7% of the ballast asked of it', () => {
    // ln2NeedT is 80% of the buoyant surplus, capped by the tanks. What the plant can make
    // on one return leg at the distance the site quotes is one to two orders of magnitude
    // smaller, so the nitrogen store is decorative in the MASS budget. It is not inert in
    // the energy budget: eCryo and eBack are both non-zero.
    resetConfig();
    for (const id of CLASS_ORDER) for (const mid of MODE_IDS) {
      const c = CLASSES[id];
      const p = planCycle(c, MODES[mid], CFG.exampleKm);
      const needT = Math.min((c.dispM3 * CFG.rhoSL / 1000 - c.payloadT) * 0.8, c.ln2CapT);
      ok(p.cryoLimited, `${id}/${mid}: cryoLimited is false at the worked example`);
      ok(p.ln2MakeT < needT * 0.07,
        `${id}/${mid}: made ${p.ln2MakeT.toFixed(1)} t of the ${needT.toFixed(0)} t asked for`);
      ok(p.eBack > 0, `${id}/${mid}: no nitrogen energy returned`);
    }
  });

  it('only one combination anywhere on the grid ever fills its nitrogen tanks', () => {
    // A P-100 in endurance mode on a 400 km leg: 313 minutes of return at full cryo share
    // makes the whole 50 t the tanks hold. Every other class, mode and distance in the grid
    // is cryo-limited. Stated exactly so that "the plant cannot keep up" stays a measured
    // claim rather than a slogan.
    const unlimited = [];
    grid((p, tag) => { if (!p.cryoLimited) unlimited.push(tag); });
    eq(unlimited.join(' | '), 'P100/endurance/400km', `cryo-satisfied combinations: ${unlimited.join(' | ')}`);
  });

  it('the letdown window uses min(6, return x 0.2), and both branches occur in the grid', () => {
    // E.letdown = downMW x min(6, RETURN_TRANSIT x 0.2) / 60. Nothing in the model says
    // where either number came from. Defect 3, tracked. Under about 50 km the 0.2 branch
    // is active; above it the flat six minutes is. This pins which, so a change cannot
    // pass unnoticed.
    resetConfig();
    const win = p => Math.min(6, p.dur.RETURN_TRANSIT * 0.2);
    const near = planCycle(CLASSES.P10000, MODES.balanced, CFG.exampleKm);
    const far = planCycle(CLASSES.P10000, MODES.balanced, 120);
    close(win(near), near.dur.RETURN_TRANSIT * 0.2, 1e-12, 'the short leg should use the 0.2 branch');
    close(win(near), 1.824, 0.01, 'the worked example letdown window, minutes');
    eq(win(far), 6, 'the long leg should be capped at six minutes');
  });

  it('that window sets over half the P-10000 worked-example cycle energy', () => {
    // 82.5 MWh per cycle at 15 km, of which 43.6 MWh is the letdown term. Change the 0.2
    // and the headline number moves by tens of percent.
    resetConfig();
    const p = planCycle(CLASSES.P10000, MODES.balanced, CFG.exampleKm);
    close(p.eCycleMWh, 82.5, 0.1, 'the published P-10000 cycle energy');
    const letdownMWh = p.downMW * Math.min(6, p.dur.RETURN_TRANSIT * 0.2) / 60;
    ok(letdownMWh / p.eCycleMWh > 0.5,
      `the letdown is only ${(100 * letdownMWh / p.eCycleMWh).toFixed(0)}% of the cycle`);
  });

  knownFail(
    'the letdown term is a minor share of cycle energy',
    'defect 3 — an unexplained min(6, ...) window sets over half of the P-10000 cycle energy',
    () => {
      resetConfig();
      const c = CLASSES.P10000;
      const p = planCycle(c, MODES.balanced, CFG.exampleKm);
      const letdownMWh = p.downMW * Math.min(6, p.dur.RETURN_TRANSIT * 0.2) / 60;
      ok(letdownMWh / p.eCycleMWh < 0.15,
        `letdown is ${(100 * letdownMWh / p.eCycleMWh).toFixed(0)}% of the cycle energy`);
    });
});
