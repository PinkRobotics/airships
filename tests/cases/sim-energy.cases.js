/* The two energy models, side by side.
 *
 * The site quotes a cost per cycle and a cost per tonne. Both come from planCycle's
 * phase-by-phase budget. But the cockpit's power bars come from stateAt's per-system draw,
 * and integrating THAT over the same cycle is a second, independent answer to the same
 * question. They do not agree, and the disagreement is not small. That is defect 2, and
 * this file is where it is measured rather than described.
 */
import { close, describe, it, knownFail, ok } from '../harness.js';
import {
  CLASSES, CLASS_ORDER, MODES,
  buildMission, findSource, resetConfig, setSeed, stateAt,
} from '../../sim/index.js?v=0c6ff005';

const WATER = [[-120.30, 50.00, 40000, 0, 'Big Lake', null]];
const FIRE = () => ({ id: 'NRG-1', ll: [-120.05, 50.05], sizeHa: 4000, status: 'Out of Control', note: false, ring: null });

function mission(clsId, modeId = 'balanced') {
  resetConfig();
  setSeed(7);
  const f = FIRE();
  const src = findSource(f.ll, CLASSES[clsId], WATER);
  return buildMission(f, WATER, modeId, clsId, { src, relaxed: false });
}

/** Riemann sum of every draw channel over one cycle, in MWh. N is large enough that the
    sum has converged to well under a percent; doubling it moves the totals by ~0.1%. */
function integrate(m, N = 4000) {
  let draw = 0, gen = 0;
  const dtH = (m.cycleSec / N) / 3600;
  for (let i = 0; i < N; i++) {
    const st = stateAt(m, (m.cycleSec * (i + 0.5)) / N + m.cycleSec - m.offset * m.cycleSec);
    for (const v of Object.values(st.draw)) draw += v * dtH;
    for (const v of Object.values(st.gen)) gen += v * dtH;
  }
  return { drawMWh: draw, genMWh: gen };
}

describe('energy · each model on its own terms', () => {
  it('the planned cycle energy is positive, finite and dominated by nothing negative', () => {
    resetConfig();
    for (const id of CLASS_ORDER) for (const mid of Object.keys(MODES)) {
      const p = planCycleOf(id, mid);
      ok(isFinite(p.eCycleMWh) && p.eCycleMWh > 0, `${id}/${mid}: eCycleMWh = ${p.eCycleMWh}`);
      ok(p.kwhPerTonne > 0 && p.kwhPerTonne < 1e6, `${id}/${mid}: ${p.kwhPerTonne} kWh/t`);
    }
  });

  it('the integrated draw is positive and finite', () => {
    for (const id of CLASS_ORDER) {
      const m = mission(id);
      const { drawMWh, genMWh } = integrate(m, 1200);
      ok(isFinite(drawMWh) && drawMWh > 0, `${id}: integrated draw = ${drawMWh}`);
      ok(isFinite(genMWh) && genMWh > 0, `${id}: integrated generation = ${genMWh}`);
      ok(genMWh < drawMWh, `${id}: generation ${genMWh.toFixed(1)} MWh exceeds draw ${drawMWh.toFixed(1)} MWh — the fleet is meant to run a deficit`);
    }
  });

  it('the integration has converged', () => {
    const m = mission('P1000');
    const coarse = integrate(m, 600).drawMWh;
    const fine = integrate(m, 4800).drawMWh;
    close(fine / coarse, 1, 0.02, 'the Riemann sum is still moving at 600 samples');
  });
});

describe('energy · the two models against each other', () => {
  it('they disagree, and the gap widens with the size of the ship', () => {
    // Measured, so the size of the disagreement is on the record rather than in a comment.
    // On a 19 km leg: P-100 2.1 -> 2.6 MWh (1.23x), P-1000 14.4 -> 26.2 MWh (1.81x),
    // P-10000 90.2 -> 255.5 MWh (2.83x). If a fix lands these numbers all move and this
    // test fails, which is the intended way to find out.
    //
    // The 2026-08-09 resize made the disagreement WORSE on every class, and the mechanism is
    // worth knowing: planCycle's budget shrank, because the letdown term it is dominated by
    // fights a smaller surplus at honest density, while stateAt's rotor draw grew, because
    // the hull is buoyant at the bottom of the cycle where the air is thick and the trim it
    // holds against is 24% bigger than the plan's single ceiling figure. Two models moving
    // in opposite directions is what defect 2 looks like from the outside.
    const ratios = {};
    for (const id of CLASS_ORDER) {
      const m = mission(id);
      const { drawMWh } = integrate(m, 2000);
      ratios[id] = drawMWh / m.plan.eCycleMWh;
      ok(ratios[id] > 1.1, `${id}: the two models agree to within ${((ratios[id] - 1) * 100).toFixed(0)}% ` +
        `(${drawMWh.toFixed(1)} MWh against ${m.plan.eCycleMWh.toFixed(1)} MWh)`);
    }
    ok(ratios.P100 < ratios.P1000 && ratios.P1000 < ratios.P10000,
      `the gap is not monotonic in class: ${JSON.stringify(ratios)}`);
    ok(ratios.P10000 > 2, `the P-10000 gap is only ${ratios.P10000.toFixed(2)}x`);
  });

  knownFail(
    'the planned budget and the integrated draw agree within 25%',
    'defect 2 — two disagreeing power models: planCycle budgets one cycle, stateAt draws another',
    () => {
      for (const id of CLASS_ORDER) {
        const m = mission(id);
        const { drawMWh } = integrate(m, 2000);
        const ratio = drawMWh / m.plan.eCycleMWh;
        ok(ratio > 0.75 && ratio < 1.25,
          `${id}: integrated draw ${drawMWh.toFixed(1)} MWh against a planned ${m.plan.eCycleMWh.toFixed(1)} MWh (${ratio.toFixed(2)}x)`);
      }
    });
});

/* planCycle by class and mode at the fixture's own leg, so the two halves of this file are
   talking about the same flight. */
function planCycleOf(id, mid) {
  return mission(id, mid).plan;
}
