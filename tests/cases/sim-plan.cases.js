/* planCycle: the function every published figure comes out of.
 *
 * These are invariants rather than magic numbers wherever an invariant exists, because the
 * magic numbers are already pinned byte-for-byte in tests/golden/. What matters here is
 * that the arithmetic cannot silently stop making sense: the books balance, more distance
 * never buys more water, and a tailwind out is a headwind home.
 */
import { close, describe, eq, it, ok } from '../harness.js';
import {
  BUS_CEILING, CFG, CLASSES, CLASS_ORDER, MODES, PHASES, WORK_ALT_MSL,
  drawAt, FORCE_TOL, LIMIT_STEPS, ledger, planCycle, resetConfig, setConfig,
} from '../../sim/index.js?v=93744380';

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

  it('the rotors never draw more than their share of the honest bus', () => {
    // downMW is the rotors' peak draw over the cycle. The bus it is clamped to is the battery
    // plus what the nitrogen store is returning at that instant (defect 6) — never the
    // generators' nameplate — and the rotors get BUS_CEILING of it. plan.busMW is that bus
    // during the approach, which is where the peak falls on every class at the worked example.
    grid((p, tag, c) => {
      ok(p.downMW <= BUS_CEILING * (c.battMW + c.genMW + c.solarM2 * CFG.solarWPerM2 / 1e6) * (1 + 1e-9),
        `${tag}: downMW ${p.downMW.toFixed(1)} against ${(BUS_CEILING * (c.battMW + c.genMW + c.solarM2 * CFG.solarWPerM2 / 1e6)).toFixed(1)} MW, the most any bus could give the rotors`);
      // The store can return at most genMW: on a long endurance leg the P-100 makes enough
      // nitrogen for the regen to sit at the cap through the approach, and the bus is then the
      // nameplate — reached as a limit, not booked as a source.
      ok(p.busMW >= c.battMW && p.busMW <= c.battMW + c.genMW + c.solarM2 * CFG.solarWPerM2 / 1e6 + 1e-9, `${tag}: descent bus ${p.busMW} MW`);

    });
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

  it('windUsed is false when the wind was not applied', () => {
    resetConfig();
    for (const bearing of [null, undefined]) {
      const p = planCycle(CLASSES.P1000, MODES.balanced, 40, { spd: 40, dir: 270, bearing });
      eq(p.windUsed, false, 'windUsed');
    }
    const north = planCycle(CLASSES.P1000, MODES.balanced, 40, { spd: 40, dir: 270, bearing: 0 });
    eq(north.windUsed, true, 'a zero-degree bearing is present');
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

});

describe('plan · rates', () => {
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

  it('the drawn baseline keeps no ballast and exposes unsupported force', () => {
    for (const id of CLASS_ORDER) {
      const p=planCycle(CLASSES[id],MODES.balanced,15);
      eq(p.retainedT,0,'baseline is not silently redesigned');
      eq(p.feasible,false,'drawn 15 km cycle is unsupported');
      ok(p.bindingLimits.length>0 && p.worst.phase,'reason and location');
    }
  });
  it('explicit retained ballast reduces delivered water and fill duration',()=>{
    const c=CLASSES.P1000,a=planCycle(c,MODES.balanced,60),b=planCycle(c,MODES.balanced,60,null,{ballastT:900});
    eq(b.retainedT,900);eq(b.deliveredT,100);ok(b.dur.WATER_FILL<a.dur.WATER_FILL);
  });
  it('phase and channel ledgers independently sum to net energy',()=>{
    grid((p,tag)=>{
      close(Object.values(p.E).reduce((a,b)=>a+b,0),p.eCycleMWh,1e-8,tag);
      close(Object.values(p.Echan).reduce((a,b)=>a+b,0)-p.eBack,p.eCycleMWh,1e-8,tag);
    });
  });
});

describe('plan · cryogenic bounds', () => {
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
});

// The prescribed profile does not choose retention automatically.
describe('plan · anchor removal', () => {
  it('without an anchor the mass book balances and descent authority binds', () => {
    resetConfig();
    const bare = planCycle({ ...CLASSES.P10000, anchorBagT: 0 }, MODES.balanced, 15);
    close(bare.retainedT, 0, 1, 'the prescribed profile keeps no water automatically');
    close(bare.deliveredT + bare.retainedT, CLASSES.P10000.payloadT, 1e-9, 'the mass book balances');
    eq(bare.bottleneck, 'descent authority', 'the bottleneck names the authority gap');
  });

  it('without an anchor the prescribed cycle is NOT FEASIBLE', () => {
    resetConfig();
    const bare = planCycle({ ...CLASSES.P10000, anchorBagT: 0 }, MODES.balanced, 15);
    eq(bare.feasible, false, 'an unheld hull cannot establish a delivery cycle');
  });

  it('without an anchor unheld mass is reported in every phase except outbound transit', () => {
    resetConfig();
    const cls = { ...CLASSES.P10000, anchorBagT: 0 };
    const bare = planCycle(cls, MODES.balanced, 15);
    for (const [phase] of PHASES) {
      let reported = false;
      for (let i = 0; i <= LIMIT_STEPS; i++) {
        const s = drawAt(cls, MODES.balanced, bare, phase, i / LIMIT_STEPS);
        ok(Number.isFinite(s.unheldT), `${phase}: unheld mass must be reported as a finite quantity`);
        reported ||= Math.abs(s.unheldT) > FORCE_TOL * Math.max(1, Math.abs(s.surplusT));
      }
      eq(reported, phase !== 'OUTBOUND_TRANSIT', `${phase}: unheld mass on the verdict mesh`);
    }
  });
});
