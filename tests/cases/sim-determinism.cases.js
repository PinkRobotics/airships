/* Determinism: what `?seed=N` actually pins, and when.
 *
 * The whole golden-file regime rests on one claim — that a seeded run is reproducible. It
 * is worth stating precisely what that means, because the seed is read at CALL time by the
 * geometry helpers and at BUILD time by everything else, and those are not the same thing.
 */
import { close, deepEq, describe, eq, it, ok } from '../harness.js';
import {
  CLASSES, SEED, buildMission, findSource, hashFrac, havKm,
  resetConfig, segAt, setSeed, stateAt,
} from '../../sim/index.js?v=60a254ea';

const WATER = [
  [-120.30, 50.00, 40000, 0, 'Big Lake', null],
  [-119.80, 50.10, 900, 1, 'Small Reservoir', null],
];
const fire = () => ({ id: 'DET-1', ll: [-120.05, 50.05], sizeHa: 4000, status: 'Out of Control', note: false, ring: null });

function build(seed, clsId = 'P1000') {
  resetConfig();
  setSeed(seed);
  const f = fire();
  const src = findSource(f.ll, CLASSES[clsId], WATER);
  return buildMission(f, WATER, 'balanced', clsId, { src, relaxed: false });
}

/** The parts of a mission a reader would call "the plan". */
const summary = m => ({
  legKm: m.legKm,
  cycleSec: m.cycleSec,
  order: m.order.slice(),
  tph: m.plan.tph,
  eCycleMWh: m.plan.eCycleMWh,
  phaseEnds: m.phaseEnds.slice(),
  seg1: segAt(m, 1).map(p => p.slice()),
});

describe('determinism · the same seed is the same run', () => {
  it('two builds on seed 7 are identical', () => {
    deepEq(summary(build(7)), summary(build(7)), 'seed 7 twice');
  });

  it('and identical again after an unrelated build on another seed', () => {
    const a = summary(build(7));
    build(999, 'P100');
    setSeed(7);
    const b = summary(build(7));
    deepEq(a, b, 'seed 7, then 999, then 7');
  });

  it('the state machine replays exactly', () => {
    const a = build(7), b = build(7);
    for (let i = 0; i < 200; i++) {
      const sa = stateAt(a, a.cycleSec * i / 200), sb = stateAt(b, b.cycleSec * i / 200);
      eq(sa.phase, sb.phase, `sample ${i} phase`);
      eq(sa.ll[0], sb.ll[0], `sample ${i} longitude`);
      eq(sa.ll[1], sb.ll[1], `sample ${i} latitude`);
      eq(sa.bearing, sb.bearing, `sample ${i} heading`);
      eq(sa.water, sb.water, `sample ${i} water`);
    }
  });
});

describe('determinism · different seeds are different runs', () => {
  it('the drop lines move', () => {
    // segAt jitters each cycle's line by hashFrac(fireId + cycle + SEED). Two seeds that
    // produced the same line would mean the seed is not reaching the geometry at all.
    const a = build(7), b = build(8);
    const sa = segAt(a, 1), sb = segAt(b, 1);
    ok(havKm(sa[0], sb[0]) > 1e-4, `line heads coincide: ${JSON.stringify(sa[0])} vs ${JSON.stringify(sb[0])}`);
  });

  it('the flown leg, and therefore the plan, differs', () => {
    const a = build(7), b = build(8);
    ok(Math.abs(a.legKm - b.legKm) > 1e-9, `legKm identical on two seeds: ${a.legKm}`);
    ok(Math.abs(a.cycleSec - b.cycleSec) > 1e-9, `cycleSec identical on two seeds: ${a.cycleSec}`);
  });

  it('several seeds give several distinct plans', () => {
    const seen = new Set();
    for (const s of [1, 2, 3, 4, 5, 6, 7, 8]) seen.add(build(s).legKm.toFixed(9));
    ok(seen.size >= 6, `eight seeds produced only ${seen.size} distinct flown legs`);
  });
});

describe('determinism · seeding before the build is what matters', () => {
  it('a reseed after the build does not move the plan', () => {
    const m = build(7);
    const before = { legKm: m.legKm, cycleSec: m.cycleSec, order: m.order.slice() };
    setSeed(12345);
    deepEq({ legKm: m.legKm, cycleSec: m.cycleSec, order: m.order.slice() }, before,
      'a built mission changed under a later setSeed');
    setSeed(7);
  });

  it('but the drop-line geometry DOES follow a later reseed, and the plan then lags it', () => {
    // segAt reads SEED at call time, so reseeding a live page moves the lines the ships
    // fly to while leaving legKm — and every duration timed against it — on the old seed.
    // Pinned rather than fixed: it only bites if something reseeds mid-run, which the page
    // never does, and changing it would change the golden output.
    const m = build(7);
    const before = segAt(m, 1).map(p => p.slice());
    setSeed(8);
    const after = segAt(m, 1);
    ok(havKm(before[0], after[0]) > 1e-4, 'segAt ignored the reseed');
    setSeed(7);
  });

  it('setSeed stringifies, so 7 and "7" are one seed', () => {
    // The page hands over whatever ?seed= contained, which is always a string. Numbers have
    // to land on the same run or a URL and a console call would disagree.
    setSeed(7);
    eq(SEED, '7', 'setSeed(7) did not store "7"');
    const a = build(7).legKm;
    const b = build('7').legKm;
    eq(a, b, 'the number 7 and the string "7" are different runs');
    setSeed(7);
  });
});

describe('determinism · hashFrac', () => {
  it('is a pure function of its string', () => {
    for (const s of ['', 'a', 'FIX-1|3|7', 'x'.repeat(200)]) {
      eq(hashFrac(s), hashFrac(s), `hashFrac(${JSON.stringify(s)}) is not stable`);
    }
  });

  it('lands in [0, 1) with four decimal places of resolution', () => {
    for (const s of ['a', 'b', 'c', 'FIX-1#1', 'FIX-1@6', 'zzz']) {
      const v = hashFrac(s);
      ok(v >= 0 && v < 1, `hashFrac(${s}) = ${v}`);
      close(v * 10000, Math.round(v * 10000), 1e-9, `hashFrac(${s}) is not a multiple of 1/10000`);
    }
  });

  it('separates strings that differ by one character', () => {
    const seen = new Set();
    for (let i = 0; i < 64; i++) seen.add(hashFrac('FIRE-' + i));
    ok(seen.size >= 60, `64 nearby keys collapsed to ${seen.size} values`);
  });
});
