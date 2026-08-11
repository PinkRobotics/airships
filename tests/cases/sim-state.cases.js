/* stateAt: the phase machine.
 *
 * The map, the instruments and the 3D model all read this one function, so a discontinuity
 * here is visible as a hull teleporting or snapping round at a phase change. That has
 * happened, more than once, which is why the continuity checks below sample either side of
 * every seam and compare the step against the largest step the adjoining phases take
 * INTERNALLY at the same time increment. A seam that moves the ship four times faster than
 * the phase it belongs to is a bug regardless of the absolute number.
 */
import { close, describe, eq, it, ok } from '../harness.js';
import {
  ALT, ALT_DROP_TOP, CLASSES, CLASS_ORDER, MODES, PHASES,
  buildMission, findSource, havKm, resetConfig, setSeed, sourceAltM, stateAt,
} from '../../sim/index.js?v=cae4b374';

/* A fixture with no live data in it: two lakes big enough for any class, one fire between
   them. `null` outlines mean intakePoint returns the centroid, so the geometry is exactly
   reproducible without shipping a polygon. */
const WATER = [
  [-120.30, 50.00, 40000, 0, 'Big Lake', null],
  [-119.80, 50.10, 900, 1, 'Small Reservoir', null],
];
const FIRE = (over) => Object.assign({
  id: 'FIX-1', ll: [-120.05, 50.05], sizeHa: 4000, status: 'Out of Control', note: false, ring: null,
}, over);

/* Forcing a class means supplying its source too: buildMission takes the assignment
   wholesale or not at all, and a forced class with no source is an idle mission. */
function mission(clsId, modeId = 'balanced') {
  resetConfig();
  setSeed(7);
  const fire = FIRE();
  const src = findSource(fire.ll, CLASSES[clsId], WATER);
  if (!src) throw new Error(`fixture: no source for ${clsId}`);
  return buildMission(fire, WATER, modeId, clsId, { src, relaxed: false });
}

/** stateAt in cycle coordinates: `t` seconds into cycle `cyc`, ignoring the hull's offset. */
function at(m, cyc, t) {
  return stateAt(m, (cyc - 1) * m.cycleSec + t - m.offset * m.cycleSec);
}

const TWO_PI = Math.PI * 2;
const wrapAng = a => { let d = a % TWO_PI; if (d > Math.PI) d -= TWO_PI; if (d < -Math.PI) d += TWO_PI; return d; };

/** Position / altitude / heading step between two samples. Heading is compared mod 2pi. */
function step(a, b) {
  return {
    km: havKm(a.ll, b.ll),
    alt: Math.abs(b.alt - a.alt),
    ang: Math.abs(wrapAng(b.bearing - a.bearing)),
  };
}

describe('state · the mission fixture', () => {
  it('builds a real mission from the fixture, not an idle one', () => {
    for (const id of CLASS_ORDER) {
      const m = mission(id);
      ok(!m.idle, `${id}: the fixture produced an idle mission`);
      eq(m.cls.id, id, `${id}: forced class`);
      ok(m.cycleSec > 0, `${id}: cycleSec = ${m.cycleSec}`);
      ok(m.phaseEnds.length === 6, `${id}: ${m.phaseEnds.length} phase ends`);
    }
  });

  it('an unreachable fire is idle and says so', () => {
    resetConfig(); setSeed(7);
    const lost = buildMission(FIRE({ id: 'FIX-2', ll: [-135, 59.9] }), WATER, 'balanced');
    ok(lost.idle, 'a fire 1,000 km from any mapped water is not idle');
    const st = stateAt(lost, 0);
    eq(st.phase, 'NO_SUITABLE_SOURCE', 'idle phase');
    eq(st.water, 0, 'idle water');
  });
});

describe('state · the phases cover the cycle exactly once', () => {
  it('phaseEnds is strictly increasing and ends at the cycle', () => {
    for (const id of CLASS_ORDER) {
      const m = mission(id);
      let prev = 0;
      m.phaseEnds.forEach((e, i) => {
        ok(e > prev, `${id}: phase end ${i} (${e}) does not advance past ${prev}`);
        prev = e;
      });
      close(m.phaseEnds[5], m.cycleSec, 1e-6, `${id}: last phase end vs cycleSec`);
    }
  });

  it('sampling a cycle visits all six phases, in order, once each', () => {
    for (const id of CLASS_ORDER) {
      const m = mission(id);
      const seen = [];
      for (let i = 0; i < 2000; i++) {
        const st = at(m, 1, m.cycleSec * i / 2000);
        eq(st.phase, PHASES[st.idx][0], `${id}: phase name and index disagree`);
        if (!seen.length || seen[seen.length - 1] !== st.idx) seen.push(st.idx);
      }
      eq(seen.join(','), '0,1,2,3,4,5', `${id}: phase sequence was ${seen.join(',')}`);
    }
  });

  it('progress runs 0 to 1 inside each phase', () => {
    for (const id of CLASS_ORDER) {
      const m = mission(id);
      for (let i = 0; i < 600; i++) {
        const st = at(m, 1, m.cycleSec * i / 600);
        ok(st.prog >= 0 && st.prog < 1.0000001, `${id}: prog = ${st.prog} in ${st.phase}`);
      }
    }
  });

  it('the cycle repeats: the same point in cycle 2 and cycle 3 is the same state', () => {
    for (const id of CLASS_ORDER) {
      const m = mission(id);
      for (const f of [0.05, 0.3, 0.62, 0.9]) {
        const a = at(m, 2, m.cycleSec * f), b = at(m, 3, m.cycleSec * f);
        eq(a.phase, b.phase, `${id}: phase at ${f}`);
        close(a.water, b.water, 1e-9, `${id}: water at ${f}`);
        close(a.alt, b.alt, 1e-9, `${id}: altitude at ${f}`);
      }
    }
  });
});

describe('state · water is monotonic where it should be', () => {
  it('the fill only ever adds water, and ends full', () => {
    for (const id of CLASS_ORDER) {
      const m = mission(id);
      const t0 = m.phaseEnds[0], t1 = m.phaseEnds[1];
      let prev = -Infinity;
      for (let i = 0; i <= 400; i++) {
        const w = at(m, 2, t0 + (t1 - t0) * i / 401).water;
        ok(w >= prev - 1e-9, `${id}: water fell during the fill (${prev} -> ${w})`);
        prev = w;
      }
      close(at(m, 2, t1 - 1e-6).water, m.cls.payloadT, m.cls.payloadT * 1e-4, `${id}: the fill does not end full`);
      close(at(m, 2, t0 + 1e-6).water, m.plan.retainedT, m.cls.payloadT * 1e-5, `${id}: the fill does not start at the retained load`);
    }
  });

  it('the drop run only ever sheds water, and ends at the retained load', () => {
    for (const id of CLASS_ORDER) {
      const m = mission(id);
      const t0 = m.phaseEnds[2], t1 = m.phaseEnds[3];
      let prev = Infinity;
      for (let i = 0; i <= 800; i++) {
        const w = at(m, 2, t0 + (t1 - t0) * i / 801).water;
        ok(w <= prev + 1e-9, `${id}: water rose during the drop run (${prev} -> ${w})`);
        prev = w;
      }
      close(at(m, 2, t0 + 1e-6).water, m.cls.payloadT, 1e-6, `${id}: the run does not start full`);
      close(at(m, 2, t1 - 1e-6).water, m.plan.retainedT, m.cls.payloadT * 1e-3, `${id}: the run does not end empty`);
    }
  });

  it('water never leaves the range 0 .. payload, at any point in the cycle', () => {
    for (const id of CLASS_ORDER) {
      const m = mission(id);
      for (let i = 0; i < 1200; i++) {
        const st = at(m, 2, m.cycleSec * i / 1200);
        ok(st.water >= -1e-9 && st.water <= m.cls.payloadT + 1e-6,
          `${id}: ${st.water} t aboard in ${st.phase}`);
      }
    }
  });

  it('the transit legs carry a fixed load: full out, retained home', () => {
    for (const id of CLASS_ORDER) {
      const m = mission(id);
      for (const f of [0.05, 0.5, 0.95]) {
        const out = at(m, 2, m.phaseEnds[1] + (m.phaseEnds[2] - m.phaseEnds[1]) * f);
        const ret = at(m, 2, m.phaseEnds[4] + (m.phaseEnds[5] - m.phaseEnds[4]) * f);
        eq(out.water, m.cls.payloadT, `${id}: outbound at ${f}`);
        eq(ret.water, m.plan.retainedT, `${id}: return at ${f}`);
      }
    }
  });
});

describe('state · continuity across every phase seam', () => {
  /* Cycle 2, not cycle 1: on the very first cycle SOURCE_APPROACH has no previous return
     leg to continue, so it sits at the intake with a default heading. Every later cycle is
     a continuation, and that is the case worth defending. */
  const DT = 0.05;   // seconds either side of the seam

  function interiorScale(m, cyc, from, to) {
    // The largest step the phase takes internally, at the same DT, over 200 sample points.
    let worst = { km: 0, alt: 0, ang: 0 };
    for (let i = 0; i < 200; i++) {
      const t = from + (to - from) * (i / 200);
      const s = step(at(m, cyc, t), at(m, cyc, Math.min(to - 1e-9, t + DT)));
      worst = { km: Math.max(worst.km, s.km), alt: Math.max(worst.alt, s.alt), ang: Math.max(worst.ang, s.ang) };
    }
    return worst;
  }

  it('position, altitude and heading step no harder at a seam than inside the phases it joins', () => {
    for (const id of CLASS_ORDER) {
      const m = mission(id);
      const bounds = [0].concat(m.phaseEnds);
      for (let k = 1; k <= 6; k++) {
        const seam = bounds[k];
        const before = interiorScale(m, 2, bounds[k - 1], seam);
        const after = k === 6
          ? interiorScale(m, 3, 0, m.phaseEnds[0])
          : interiorScale(m, 2, seam, bounds[k + 1]);
        const s = step(at(m, 2, seam - DT / 2), at(m, 2, seam + DT / 2));
        const tag = `${id}: seam ${PHASES[k - 1][0]} -> ${PHASES[k % 6][0]}`;
        // A floor keeps a phase that is genuinely stationary (the fill) from setting an
        // impossible standard for the phase that follows it.
        ok(s.km <= 4 * Math.max(before.km, after.km) + 5e-4,
          `${tag}: jumped ${(s.km * 1000).toFixed(1)} m against interior steps of ` +
          `${(before.km * 1000).toFixed(1)} / ${(after.km * 1000).toFixed(1)} m`);
        ok(s.alt <= 4 * Math.max(before.alt, after.alt) + 0.5,
          `${tag}: altitude jumped ${s.alt.toFixed(2)} m against ${before.alt.toFixed(2)} / ${after.alt.toFixed(2)} m`);
        ok(s.ang <= 4 * Math.max(before.ang, after.ang) + 0.01,
          `${tag}: heading jumped ${s.ang.toFixed(4)} rad against ${before.ang.toFixed(4)} / ${after.ang.toFixed(4)} rad`);
      }
    }
  });

  it('the ship stops before it lets itself down onto the lake', () => {
    /* A bag of several thousand tonnes cannot be dipped from a moving ship — 20 km/h is a bad
     * time and 40 is worse — so the approach closes the last of its track and comes to a dead
     * stop BEFORE it descends into the band where the anchor has to be in the water. It used to
     * do both at once and was still making 30-odd km/h on the way down. */
    for (const id of CLASS_ORDER) {
      const m = mission(id);
      const dur = m.plan.dur.SOURCE_APPROACH * 60;
      const t0 = m.phaseEnds[5];                       // the approach begins where the return ends
      const at2 = (f) => at(m, 2, t0 + dur * f);
      ok(at2(0.35).gs < 1.0, `${id}: still making ${at2(0.35).gs.toFixed(1)} km/h a third in`);
      ok(at2(0.9).gs < 1.0, `${id}: still moving near the water`);
      // And the descent is on the far side of that stop: most of the height goes after 30%.
      const top = at2(0.02).alt, mid = at2(0.30).alt, low = at2(0.98).alt;
      ok(top - mid < (top - low) * 0.25,
        `${id}: dropped ${(top - mid).toFixed(0)} m of ${(top - low).toFixed(0)} before stopping`);
    }
  });

  it('nothing yaws while there is line in the water', () => {
    /* The fill used to turn onto the departure heading over its last third, which fixed a seam
     * and created something worse: an 876 m hull rotating with a hose, a pump pod and an anchor
     * cable all hanging in the lake. That is how lines tangle. The turn lives in the climb-out
     * now, after the pod is clear. */
    for (const id of CLASS_ORDER) {
      const m = mission(id);
      const dur = m.plan.dur.WATER_FILL * 60;
      const t0 = m.phaseEnds[0];
      let yaw = 0, prev = null;
      for (let k = 0; k <= 60; k++) {
        const b = at(m, 2, t0 + dur * (k / 60)).bearing;
        if (prev !== null) {
          let d = Math.abs(b - prev);
          if (d > Math.PI) d = 2 * Math.PI - d;
          yaw += d;
        }
        prev = b;
      }
      ok(yaw * 180 / Math.PI < 5,
        `${id}: turned ${(yaw * 180 / Math.PI).toFixed(1)} degrees with its lines down`);
    }
  });

  it('the altitudes at the seams are the ones config.js names', () => {
    for (const id of CLASS_ORDER) {
      const m = mission(id);
      close(at(m, 2, m.phaseEnds[0] + 1e-6).alt, sourceAltM(m.cls), 1e-3, `${id}: fill is not at the hose altitude`);
      close(at(m, 2, m.phaseEnds[2] + 1e-6).alt, ALT.drop, 1e-3, `${id}: the run does not start at the drop altitude`);
      close(at(m, 2, m.phaseEnds[3] + 1e-6).alt, ALT_DROP_TOP, 1e-3, `${id}: the escape does not start where the run ended`);
      /* THE RETURN LEG MAY NOT FLY INTO THE BAND IT CANNOT HOLD ITSELF IN.
       *
       * Below `plan.anchorFromAglM` the rotors cannot hold this hull down alone and the descent
       * anchor has to be in the water — and a bag cannot be dipped at 130 km/h. So the transit
       * levels off at or above that altitude and the approach, which is the slow phase, flies
       * the rest of the way down. Asserted as the RULE rather than as a number, because the
       * number is a consequence of the class's cable and its buoyancy.
       *
       * Before 2026-08-09 the return descended to hose range at cruise speed regardless, which
       * is what had the animation paying a full cable out into open air 700 m above the lake. */
      const endRet = at(m, 2, m.phaseEnds[5] - 1e-6).alt;
      ok(endRet >= m.plan.anchorFromAglM - 1e-6,
        `${id}: the return ends at ${endRet.toFixed(0)} m, inside the anchor band that starts at `
        + `${m.plan.anchorFromAglM} m`);
      close(endRet, Math.max(sourceAltM(m.cls) + 130, m.plan.anchorFromAglM + 60), 1e-2,
        `${id}: the return does not level off where the profile says`);
      // And the approach is what closes the remaining distance to the water.
      close(at(m, 2, m.phaseEnds[0] - 1e-6).alt, sourceAltM(m.cls), 1.0,
        `${id}: the approach does not finish at the fill altitude`);
    }
  });

  it('the drop run turns one way and keeps turning: no 180-degree flicker', () => {
    // The one case shortest-arc interpolation cannot answer. state.js counts turns instead
    // of interpolating, so the heading must ACCUMULATE monotonically across the whole run
    // rather than flipping end for end between samples.
    for (const id of CLASS_ORDER) {
      const m = mission(id);
      if ((m.plan.passes || 1) < 3) continue;    // nothing to reverse
      const t0 = m.phaseEnds[2], t1 = m.phaseEnds[3];
      let prev = -Infinity, total = 0, last = null;
      for (let i = 0; i <= 3000; i++) {
        const b = at(m, 2, t0 + (t1 - t0) * i / 3001).bearing;
        ok(b >= prev - 1e-6, `${id}: heading went backwards on the line (${prev} -> ${b})`);
        if (last !== null) total += b - last;
        last = b; prev = b;
      }
      close(total, Math.PI * (m.plan.passes - 1), 0.02, `${id}: total turn over ${m.plan.passes} passes`);
    }
  });
});

describe('state · the vertical duty', () => {
  it('is never positive: the rotors only ever hold the hull down', () => {
    for (const id of CLASS_ORDER) for (const mid of Object.keys(MODES)) {
      const m = mission(id, mid);
      for (let i = 0; i < 1500; i++) {
        const st = at(m, 2, m.cycleSec * i / 1500);
        ok(st.vert <= 0, `${id}/${mid}: vert = ${st.vert} in ${st.phase} at prog ${st.prog.toFixed(3)}`);
        ok(st.vert >= -1, `${id}/${mid}: vert = ${st.vert} exceeds full authority`);
      }
    }
  });

  it('rotor draw stays inside the bus', () => {
    for (const id of CLASS_ORDER) {
      const m = mission(id);
      const bus = (m.cls.battMW + m.cls.genMW) * 0.95;
      for (let i = 0; i < 900; i++) {
        const st = at(m, 2, m.cycleSec * i / 900);
        ok((st.draw.rotors || 0) <= bus + 1e-9,
          `${id}: rotors drawing ${st.draw.rotors} MW of a ${bus} MW ceiling in ${st.phase}`);
      }
    }
  });

  it('mass and net force agree with the water aboard', () => {
    for (const id of CLASS_ORDER) {
      const m = mission(id);
      for (let i = 0; i < 300; i++) {
        const st = at(m, 2, m.cycleSec * i / 300);
        close(st.massT, m.plan.led.dryT + st.water + st.ln2, 1e-9, `${id}: massT`);
        /* THE NET INCLUDES THE ANCHOR, and that is the point of the field. The bag is the
         * largest single force on the hull whenever it is in use — 12,400 t against a
         * 21,000 t P-10000 — and a net line of buoyancy minus weight reported a ship
         * straining upward at the exact moment a bucket of lake water was holding it down. */
        close(st.netN, st.buoyN - st.weightN - st.anchorN, 1e-6, `${id}: netN`);
        ok(st.anchorN >= 0, `${id}: the anchor pulls down, never up`);
        ok(st.anchorT <= m.plan.anchorT + 1e-9, `${id}: more water in the bag than it holds`);
        close(st.weightN, st.massT * 1000 * 9.81, 1e-6, `${id}: weightN`);
      }
    }
  });
});

describe('state · ground speed', () => {
  it('is never negative, and only the fill is a true stop', () => {
    for (const id of CLASS_ORDER) {
      const m = mission(id);
      for (let i = 0; i < 1200; i++) {
        const st = at(m, 2, m.cycleSec * i / 1200);
        ok(st.gs >= 0, `${id}: gs = ${st.gs} in ${st.phase}`);
        ok(st.gs < m.plan.gsOut * 3 + 10, `${id}: gs = ${st.gs} in ${st.phase} is beyond anything planned`);
      }
      eq(at(m, 2, m.phaseEnds[0] + (m.phaseEnds[1] - m.phaseEnds[0]) / 2).gs, 0, `${id}: the fill is not a station hold`);
    }
  });

  it('the transit legs reach the planned ground speeds', () => {
    for (const id of CLASS_ORDER) {
      const m = mission(id);
      const out = at(m, 2, m.phaseEnds[1] + (m.phaseEnds[2] - m.phaseEnds[1]) * 0.5);
      const ret = at(m, 2, m.phaseEnds[4] + (m.phaseEnds[5] - m.phaseEnds[4]) * 0.5);
      close(out.gs, m.plan.gsOut, 1e-9, `${id}: outbound cruise`);
      close(ret.gs, m.plan.gsRet, 1e-9, `${id}: return cruise`);
    }
  });
});

describe('state · a dead hull', () => {
  it('freezes at the moment the bus died and draws nothing', () => {
    const m = mission('P1000');
    m.dead = true;
    m.deadAt = m.cycleSec * 1.5;
    const a = stateAt(m, m.cycleSec * 1.5);
    const b = stateAt(m, m.cycleSec * 40);
    eq(a.phase, b.phase, 'the phase moved after death');
    close(a.ll[0], b.ll[0], 1e-12, 'longitude moved after death');
    close(a.ll[1], b.ll[1], 1e-12, 'latitude moved after death');
    eq(b.gs, 0, 'ground speed');
    eq(Object.keys(b.draw).length, 0, 'something is still drawing power');
    eq(b.stopped, true, 'stopped flag');
  });
});
