/* planCycle: the function every published figure comes out of.
 *
 * These are invariants rather than magic numbers wherever an invariant exists, because the
 * magic numbers are already pinned byte-for-byte in tests/golden/. What matters here is
 * that the arithmetic cannot silently stop making sense: the books balance, more distance
 * never buys more water, and a tailwind out is a headwind home.
 */
import { close, describe, eq, it, knownFail, ok } from '../harness.js';
import {
  CFG, CLASSES, CLASS_ORDER, MODES, WORK_ALT_MSL,
  ledger, planCycle, resetConfig, setConfig,
} from '../../sim/index.js?v=b5da402b';

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

  it('the mode ordering has flipped five times and is not load-bearing', () => {
    // SIX flips now. Every one of them has been a side effect of a change made for some other
    // reason, and not one has been a decision about how the ship should be flown — which is
    // the finding this test exists to carry.
    //
    // Two terms pull against each other. Drag rises with the square of airspeed, so rapid pays
    // most for the legs; the letdown rides the return leg's duration, so endurance pays most
    // for the descent. Whichever is bigger decides the order.
    //
    // It was drag (slower is cheaper), then the letdown (balanced cheapest, briefly, when the
    // descent balance moved to the dense air at the lake), then drag again when the long hose
    // cut the letdown, then balanced again when the hoses came off. The anchor has now taken
    // the letdown down to 3% of the cycle, so drag wins: endurance is cheapest.
    //
    // The SEVENTH flip nearly was not one. Cutting rtLN2 from 0.50 to 0.20 on 2026-08-09 took
    // away most of the nitrogen credit, and the credit scales with return-leg duration, so it
    // was worth most to endurance. That closed the gap from 18% to 5.8% and left the ordering
    // intact by 0.5%. Balanced and endurance are now within one part in two hundred, which is
    // to say the mode dial is very nearly free.
    //
    // The flip that produced these numbers is worth naming, because it was an ACCOUNTING fix
    // and not a physics one. The nitrogen recovery used to be netted against the pump bill
    // under a max(0, ...); the longer a mode's return leg, the more nitrogen it made, and the
    // more of its own recovery it therefore threw away. Endurance was being charged for the
    // thing it was best at. Splitting the two lines moved it from dearest to cheapest.
    //
    // So the ordering is pinned as an observation, not claimed as a property. It remains a
    // downstream symptom of defect 3's unexplained window and should be expected to move
    // again when that is fixed.
    resetConfig();
    const p = m => planCycle(CLASSES.P10000, m, 60);
    const r = p(MODES.rapid), b = p(MODES.balanced), e = p(MODES.endurance);
    ok(e.eCycleMWh < b.eCycleMWh && b.eCycleMWh < r.eCycleMWh,
      `slower should be cheaper per cycle now: ${r.eCycleMWh.toFixed(1)} / `
      + `${b.eCycleMWh.toFixed(1)} / ${e.eCycleMWh.toFixed(1)} MWh`);
    close(r.eCycleMWh, 125.2, 0.2, 'rapid');
    close(b.eCycleMWh, 118.5, 0.2, 'balanced');
    close(e.eCycleMWh, 118.0, 0.2, 'endurance');
  });

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

  it('the fill is the DELIVERED load over flow, not the payload', () => {
    // Retained ballast never leaves the tanks, so the pumps only replace what was dropped.
    // This read `payloadT / flow` while retention was inert and the two were the same number;
    // since the descent balance moved to the lake (2026-08-09) they differ, and the version
    // that agrees with the mass book is the delivered one. The P-100 still retains nothing,
    // so its fill is unchanged and pins the simple case.
    resetConfig();
    const p1k = planCycle(CLASSES.P1000, MODES.balanced, 15);
    close(p1k.dur.WATER_FILL, p1k.deliveredT / 3 / 60, 1e-9, 'P-1000 fill');
    const p100 = planCycle(CLASSES.P100, MODES.balanced, 15);
    eq(p100.retainedT, 0, 'the P-100 should still retain nothing');
    close(p100.dur.WATER_FILL, 100 / 0.5 / 60, 1e-9, 'P-100 fill');
  });
});

describe('plan · the mechanisms the copy describes', () => {
  it('the drop is ONE run, flown slowly, not repeated passes', () => {
    /* It used to shuttle: three passes for a P-10000, an odd count so the run still ended at
     * the far end. Every turn is an 876 m hull reversing over the fire it is dropping on, and
     * the water lands on the same line either way — the turns were pure overhead, 4.3 minutes
     * of a 49.8 minute cycle. One pass, flown at the rate the sprayers meter: about 22 km/h. */
    resetConfig();
    grid((p, tag, c) => {
      eq(p.passes, 1, `${tag}: passes`);
      // The run lasts as long as it takes to lay the water, and never less than one line.
      const dump = p.deliveredT / (c.fillM3s * CFG.fillMul) / 60;
      ok(p.dur.WATER_RELEASE >= dump - 1e-9,
        `${tag}: ${p.dur.WATER_RELEASE.toFixed(2)} min of run for ${dump.toFixed(2)} min of water`);
      const runKph = c.dropKm / p.dur.WATER_RELEASE * 60;
      ok(runKph < c.cruiseKph * 0.5,
        `${tag}: laying water at ${runKph.toFixed(0)} km/h is not a crawl`);
    });
  });

  it('no class retains descent ballast, because the lake holds the ship down', () => {
    // THE HISTORY MATTERS, because this test has asserted three different things.
    //
    // The page has always described retaining water as descent ballast. For most of this
    // model's life it never happened: the balance was struck at the ceiling, where the air is
    // thinnest, and the rotors always won. Struck where the letdown actually ends — 1,200 m
    // lower, 16% denser, the hull 24% more buoyant — the two larger classes were 49 t and
    // 1,056 t short and had to keep water back, at a tenth of the delivered figure.
    //
    // The descent anchor pays that instead. A bag of lake water on a cable, winched clear of
    // the surface, is ballast that costs 0.11 MWh and is given straight back. Retention is
    // zero again, and this time the whole payload is still delivered.
    resetConfig();
    grid((p, tag) => eq(p.retainedT, 0, `${tag}: retainedT`));
  });

  it('take the anchor away and the water goes back in the tanks', () => {
    // The guard against the above being a tautology, and the reason the retention code is not
    // dead. Give the P-10000 no bag and it is 1,056 t short at the source again, exactly as it
    // was before the anchor existed, and it pays in delivery.
    resetConfig();
    const bare = planCycle({ ...CLASSES.P10000, anchorBagT: 0 }, MODES.balanced, 15);
    close(bare.retainedT, 1056, 1, 'the shortfall comes straight back');
    close(bare.deliveredT + bare.retainedT, CLASSES.P10000.payloadT, 1e-9, 'the mass book balances');
    eq(bare.bottleneck, 'descent authority', 'and the bottleneck says so');
  });

  it('the anchor does the descent and the rotors only trim it', () => {
    // Ordering matters and is a design decision, not an accident. The bag goes first and takes
    // everything it holds — 12,400 t of the P-10000's 13,722 t — leaving the rotors 10% of
    // their capability, which is trim rather than lift. Sizing the bag to cover only what the
    // rotors could not manage would run the whole letdown at full bus power for nothing.
    resetConfig();
    const p = planCycle(CLASSES.P10000, MODES.balanced, 15);
    close(p.anchorT, 12400, 0.5, 'the whole bag goes in');
    ok(!p.battLimited, 'the rotors should not be saturated with the anchor deployed');
    const holdT = p.ledLow.surplusT - p.ln2MakeT;
    const rotorShare = (holdT - p.anchorT) / (p.rotorMaxT / 0.6);
    ok(rotorShare < 0.15, `the rotors should be left doing trim, not lift — ${(rotorShare * 100).toFixed(1)}%`);
    // The P-100 carries one too, though its descent closes on rotors alone (x1.94 headroom).
    // Not because it needs holding down, but because a bucket is cheaper than thrust on every
    // class: 1.773 -> 1.253 MWh for the same delivered water, a 29% saving on a class that
    // does not need the mechanism at all. The largest class saves 49% AND delivers 1,056 t
    // more, because without the bag it cannot get all of its water down to the fire.
    const small = planCycle(CLASSES.P100, MODES.balanced, 15);
    close(small.anchorT, 125, 0.5, 'the P-100 uses its bag as well');
    close(small.eCycleMWh, 1.253, 5e-3, 'and saves 29% of its cycle energy doing it');
  });

  it('the descent balance is struck at the source, not at the ceiling', () => {
    // The defect this replaced, kept as a measurement so it cannot come back quietly. The
    // ratio is rotorMaxT/0.6 over the surplus that has to be pushed down: above 1 the rotors
    // can do it alone. At the ceiling all three look comfortable; at the lake, where the
    // letdown actually ends, two of them are below 1.0 and need the anchor.
    resetConfig();
    const ceiling = { P100: 2.4182, P1000: 1.1928, P10000: 1.1462 };
    const lake = { P100: 1.9444, P1000: 0.9591, P10000: 0.9216 };
    for (const id of CLASS_ORDER) {
      const p = planCycle(CLASSES[id], MODES.balanced, 15);
      close((p.rotorMaxT / 0.6) / p.led.surplusT, ceiling[id], 1e-3, `${id}: headroom at the ceiling`);
      close((p.rotorMaxT / 0.6) / p.ledLow.surplusT, lake[id], 1e-3, `${id}: headroom at the lake`);
    }
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
      const needT = Math.min(ledger(c, WORK_ALT_MSL).surplusT * 0.8, c.ln2CapT);
      ok(p.cryoLimited, `${id}/${mid}: cryoLimited is false at the worked example`);
      ok(p.ln2MakeT < needT * 0.07,
        `${id}/${mid}: made ${p.ln2MakeT.toFixed(1)} t of the ${needT.toFixed(0)} t asked for`);
      ok(p.eBack > 0, `${id}/${mid}: no nitrogen energy returned`);
    }
  });

  it('no combination anywhere on the grid ever makes the nitrogen it is asked for', () => {
    // One used to: a P-100 in endurance mode on a 400 km leg, 313 minutes of return at full
    // cryo share, made the whole 50 t its tanks then held. The 2026-08-09 resize took that
    // away from both ends. The tanks now hold 155 t, sized by unpowered recovery rather than
    // picked, so the cap no longer binds before the plant does; and the target is 80% of the
    // surplus, 88.4 t, against the 69.6 t that leg can make. Every class, mode and distance
    // in the grid is now cryo-limited, so `cryoLimited` carries no information at all —
    // defect 5, unchanged and if anything more complete.
    const unlimited = [];
    grid((p, tag) => { if (!p.cryoLimited) unlimited.push(tag); });
    eq(unlimited.join(' | '), '', `cryo-satisfied combinations: ${unlimited.join(' | ')}`);
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
    close(win(near), 1.629, 0.01, 'the worked example letdown window, minutes');
    eq(win(far), 6, 'the long leg should be capped at six minutes');
  });

  it('the letdown is no longer the largest term, and the anchor is why', () => {
    // For the life of this model the biggest line in the published energy budget was an
    // unexplained window. It is a minor term now — 1.42 MWh of a 45.87 MWh cycle — while the
    // anchor's own cost, lifting 12,400 t of lake water the 15 m it takes to break the surface,
    // is 0.6 MWh and buys a 34.5 MWh reduction in rotor work. That ratio is the entire argument
    // for the mechanism.
    resetConfig();
    const p = planCycle(CLASSES.P10000, MODES.balanced, CFG.exampleKm);
    close(p.eCycleMWh, 45.87, 0.05, 'the published P-10000 cycle energy');
    const letdownMWh = p.downMW * Math.min(6, p.dur.RETURN_TRANSIT * 0.2) / 60;
    const returnMWh = p.dragMW * 0.55 * p.dur.RETURN_TRANSIT / 60;
    ok(letdownMWh < returnMWh, `the letdown ${letdownMWh.toFixed(2)} should now be under the `
      + `return leg ${returnMWh.toFixed(2)} MWh`);
    close(p.anchorT * 1000 * 9.81 * 15 / 0.85 / 3.6e9, 0.596, 5e-3, 'the anchor lift energy');
  });

  it('the letdown term is a minor share of cycle energy', () => {
    // THIS WAS A KNOWN FAILURE UNTIL 2026-08-09, and it came off the way the mechanism is
    // supposed to work: the defect stopped mattering, the test started passing, the suite
    // reported that as a hard failure, and the marker had to go.
    //
    // Defect 3 is that `min(6, t_ret x 0.2)` has no stated justification, and it used to set
    // 45% of the P-10000's cycle — an unexplained constant deciding the headline number. The
    // descent anchor did not explain it. It made it small: rotor power goes as thrust^1.5, so
    // moving 12,400 t of the hold onto a bag of lake water cut `downMW` from 1,748 to 52 MW
    // and the term from 35.9 MWh to 1.4, which is 3.1% of the cycle.
    //
    // The 6 and the 0.2 are still unjustified and defect 3 is still open in
    // docs/OPEN-QUESTIONS.md. What changed is that they no longer move a published figure by
    // more than a few percent, so they are a wart rather than a load-bearing guess.
    resetConfig();
    const p = planCycle(CLASSES.P10000, MODES.balanced, CFG.exampleKm);
    const letdownMWh = p.downMW * Math.min(6, p.dur.RETURN_TRANSIT * 0.2) / 60;
    ok(letdownMWh / p.eCycleMWh < 0.05,
      `letdown is ${(100 * letdownMWh / p.eCycleMWh).toFixed(1)}% of the cycle energy`);
  });
});
