/* Satellite heat must actually change where the water goes.
 *
 * `planTargets` scores and orders a mission's candidate drop lines. Part of that score is
 * how much 24-hour satellite hotspot temperature sits within 1.2 km of each line. That
 * data used to be read from a global; it is an argument now, so the model can be run and
 * tested with no feed at all.
 *
 * The change came with a trap, and the trap sprang: all three call sites in the
 * application kept calling `planTargets(m)` with no second argument, so the default empty
 * array won and hotspot scoring was silently switched off on the live page. Nothing caught
 * it — the golden files are captured in replay mode, where the sampled fleet happens to
 * carry no heat-derived targets, so every recorded number was identical and wrong.
 *
 * These tests exist so that the argument cannot be dropped again in silence.
 */
import { describe, it, eq, ok } from '../harness.js';
import { buildMission, planTargets, setSeed } from '../../sim/index.js?v=75e59915';

/* A large fire with a big lake to the west. Interior BC coordinates, so the water search
   and the community scoring behave as they do in production. */
const FIRE = {
  id: 'HEATTEST', ll: [-120.05, 50.00], sizeHa: 6000,
  status: 'Out of Control', note: false, ring: null,
};
const WATER = [[-120.30, 50.00, 20000, 0, 'Test Lake', null]];

function freshMission() {
  setSeed('heat-test');
  // No forced class: forcing one also requires supplying the source, and letting the
  // allocator choose exercises the same path the application takes.
  return buildMission(FIRE, WATER, 'balanced');
}

/** Enough detections on one line to dominate its score: the cap is reached at 300 degrees. */
function hotspotsOn(target) {
  const out = [];
  for (let i = 0; i < 20; i++) {
    out.push({ ll: [target[0] + (i - 10) * 0.0004, target[1] + (i - 10) * 0.0002], temp: 340 });
  }
  return out;
}

describe('satellite heat reaches the drop planner', () => {
  it('a mission is built with candidate lines to score', () => {
    const m = freshMission();
    ok(m.targets && m.targets.length >= 2,
      `expected several candidate targets, got ${m.targets ? m.targets.length : 0}`);
    ok(m.order && m.order.length === m.targets.length, 'every target should be ordered');
  });

  it('heat on the last-ranked line promotes it', () => {
    const m = freshMission();
    planTargets(m, []);
    const coldOrder = m.order.slice();
    const lastIdx = coldOrder[coldOrder.length - 1];
    const lastRankCold = coldOrder.indexOf(lastIdx);

    m.heat = true;
    planTargets(m, hotspotsOn(m.targets[lastIdx]));
    const lastRankHot = m.order.indexOf(lastIdx);

    ok(lastRankHot < lastRankCold,
      `the line with 20 hotspots on it went from rank ${lastRankCold} to ${lastRankHot} — `
      + 'heat is not reaching the score');
  });

  it('the recorded reason names the cluster', () => {
    const m = freshMission();
    m.heat = true;
    planTargets(m, hotspotsOn(m.targets[0]));
    ok(m.whyT.some(w => /hottest cluster/.test(w)),
      `no line was credited to the hotspots; reasons were ${JSON.stringify(m.whyT)}`);
  });

  it('heat is ignored unless the mission is flagged as heat-targeted', () => {
    // m.heat says the TARGETS came from detections; without it the hotspots are just
    // weather. Both halves of that condition are load-bearing, so both are pinned.
    const m = freshMission();
    m.heat = false;
    planTargets(m, hotspotsOn(m.targets[0]));
    eq(m.whyT.some(w => /hottest cluster/.test(w)), false,
      'hotspot scoring ran on a mission whose targets are geometric');
  });

  it('no heat is not an error — the planner falls back to geometry', () => {
    const m = freshMission();
    planTargets(m, []);
    ok(m.targets.length > 0, 'a fire with no detections still gets drop lines');
    eq(m.segs.length, m.targets.length, 'every target keeps a segment');
    ok(m.whyT.every(w => typeof w === 'string' && w.length > 0),
      'every chosen line should still record why');
  });
});
