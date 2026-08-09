/* stateAt: where a mission is and what it is doing at a given moment in its cycle.
 *
 * The phase state machine. Everything the map draws, the instruments read and the 3D
 * model animates comes from this one function, so that no two surfaces can disagree
 * about what the ship is doing.
 */
import { ALT, ALT_DROP_TOP, CFG, PHASES, VZ_MAX } from './config.js';
import { bez, bezBearing, easeSm, easeTrap, lerpAng } from './geo.js';
import { diskMW, pumpMW } from './physics.js';
import { arrivalCurve, segAt, stationFor, tIdx } from './targets.js';

export function stateAt(m, tRaw) {
  if (m.idle) return { phase: "NO_SUITABLE_SOURCE", label: "idle — no suitable mapped source", ll: m.fire.ll, water: 0, ln2: 0, prog: 0, alt: 0, bearing: 0, idx: -1 };
  // A hull whose storage reached zero is frozen at the moment the bus died: the picture
  // (position, phase, tanks) holds, but nothing draws power and nothing moves.
  const stopped = !!(m.dead && tRaw >= m.deadAt);
  if (stopped) tRaw = m.deadAt;
  const t = ((tRaw + m.offset * m.cycleSec) % m.cycleSec + m.cycleSec) % m.cycleSec;
  let idx = m.phaseEnds.findIndex(e => t < e);
  if (idx < 0) idx = PHASES.length - 1;
  const start = idx ? m.phaseEnds[idx - 1] : 0;
  const dur = Math.max(1e-6, m.phaseEnds[idx] - start);
  const prog = (t - start) / dur;
  const id = PHASES[idx][0];
  const cls = m.cls, plan = m.plan, led = plan.led;
  // this cycle's drop line and the S-curve built on it: outbound flies to the line's start,
  // the run paints the line, escape and return leave from its end
  const cycN = Math.floor((tRaw + m.offset * m.cycleSec) / m.cycleSec) + 1;
  const ti = tIdx(m, cycN);
  const seg = segAt(m, cycN);
  const sA = seg[0], sB = seg[1];
  const ikN = stationFor(m, cycN), ikX = stationFor(m, cycN + 1);
  const mid2 = [(ikN[0] + sA[0]) / 2, (ikN[1] + sA[1]) / 2];
  const dX = sA[0] - ikN[0], dY = sA[1] - ikN[1];
  const cO = [mid2[0] - dY * 0.09, mid2[1] + dX * 0.09];
  const cR = [(ikX[0] + sB[0]) / 2 + dY * 0.09, (ikX[1] + sB[1]) / 2 - dX * 0.09];
  m.curDelivery = sA; m.curCtlOut = cO; m.curCtlRet = cR; m.curSeg = seg; m.curTi = ti;
  m.curIk = ikN; m.curIkNext = ikX;
  m.curPass = m.order ? Math.floor((cycN - 1) / m.order.length) : 0;
  let ll, bearing = 0, alt = ALT.cruise, water = 0, ln2 = 0, sub = "", draw = { hotel: cls.genMW * 0.02 };
  const B = (p0, c, p2, tt) => { ll = bez(p0, c, p2, tt); bearing = bezBearing(p0, c, p2, tt, ll[1]); };
  const sm = easeSm(prog), tz = easeTrap(prog);
  // Distance the escape climb covers, as a fraction of the return leg: mean speed (the dial's
  // vEsc profile integrates to vEsc/2.5) times its duration, over the one-way distance. The
  // return picks up exactly where it leaves off, so map motion and needle never disagree.
  const escF = Math.max(0.01, Math.min(0.15,
    (plan.gsRet * 0.85 / 2.5) * (plan.dur.BUOYANCY_ESCAPE / 60) / Math.max(1, m.legKm || m.oneWayKm)));
  // A ship does not climb to 1,500 m on a two-minute hop. The working ceiling is whatever the
  // shorter leg can actually reach at a sane climb rate — without this a P-1000 on a short run
  // was diving at 44 m/s to make the profile fit, which is a lie the altitude dial then tells.
  const altTop = Math.min(ALT.cruise, ALT.source +
    VZ_MAX * 0.30 * 60 * Math.min(plan.dur.OUTBOUND_TRANSIT, plan.dur.RETURN_TRANSIT));
  switch (id) {
    case "SOURCE_APPROACH": {
      const wMW = pumpMW(cls) * 0.06;              // winch scales with the class, not a constant
      // The flown tail of the previous cycle's return curve, hose paying out on the way in.
      //
      // It must be THE SAME CURVE the return actually flew. Rebuilding the control point from
      // THIS cycle's geometry gave the approach a different arc from the one the ship was on,
      // so the hull jumped and swung through the seam — a phase change that looked like a
      // manoeuvre when all that really happens here is the hose starting to pay out.
      if (m.segs && cycN > 1) B(...arrivalCurve(m, cycN), 0.96 + sm * 0.04);
      else ll = ikN.slice();
      alt = ALT.source + 130 * (1 - sm);
      ln2 = plan.ln2MakeT * (1 - prog * 0.3);
      sub = "hose paying out";
      water = plan.retainedT;
      draw.prop = plan.dragMW * 0.3; draw.winch = wMW;
      break;
    }
    case "WATER_FILL": {
      ll = ikN.slice(); alt = ALT.source;
      // HEADING THROUGH THE HOLD. A station-keeping ship has no track to take a bearing from,
      // and leaving it at the default sent the hull snapping to due north on the way into the
      // fill and snapping again on the way out — the worst seam on the page. It holds the
      // heading it arrived on, then turns onto the departure heading over the last third of
      // the fill, so the outbound leg begins already pointing where it is going.
      const bIn = bezBearing(...arrivalCurve(m, cycN), 1, ll[1]);
      const bOut = bezBearing(ikN, cO, sA, 0, ll[1]);
      bearing = lerpAng(bIn, bOut, easeSm(Math.max(0, (prog - 0.65) / 0.35)));
      water = plan.retainedT + plan.deliveredT * prog;
      ln2 = plan.ln2MakeT * 0.7 * (1 - prog);
      draw.pumps = plan.pumpMW;
      // What holds the ship down while filling: retained water and LN2 ballast, the water
      // column standing in the hose, and rotor trim on the small residual the force-closure
      // guarantees is within reach. A dangling pod is not an anchor, and none is needed.
      sub = "hose column + rotor trim";
      break;
    }
    case "OUTBOUND_TRANSIT": {
      B(ikN, cO, sA, tz);
      alt = tz < 0.3 ? ALT.source + (altTop - ALT.source) * easeSm(tz / 0.3)
          : tz > 0.75 ? altTop - (altTop - ALT.drop) * easeSm((tz - 0.75) / 0.25)
          : altTop;
      // Turn onto the line before reaching it: the drop run starts already tracking the
      // heading it will fly, instead of the hull snapping 90 degrees at the phase change.
      if (prog > 0.88) {
        const kxo = Math.cos(ll[1] * Math.PI / 180);
        bearing = lerpAng(bearing, Math.atan2((sB[0] - sA[0]) * kxo, sB[1] - sA[1]),
          easeSm((prog - 0.88) / 0.12));
      }
      water = cls.payloadT; draw.prop = plan.dragMW;
      if (prog < 0.18) { sub = "hose winding up"; draw.winch = pumpMW(cls) * 0.06; }
      break;
    }
    case "WATER_RELEASE": {
      // Multiple passes shuttle the line: out, back, out … always an odd count, so the
      // final pass delivers the ship to sB where BUOYANCY_ESCAPE picks it up.
      const nP = plan.passes || 1;
      const k = Math.min(nP - 1e-9, prog * nP), pi = Math.floor(k), pf = k - pi;
      // Each pass eases in and out, so the ship never reverses at speed: it slows into the
      // turn, comes about, and accelerates back down the line. Water goes out with DISTANCE
      // covered rather than with the clock, so nothing is dumped while the hull is turning.
      const e = easeSm(pf);
      const t = pi % 2 ? 1 - e : e;
      ll = [sA[0] + (sB[0] - sA[0]) * t, sA[1] + (sB[1] - sA[1]) * t];
      alt = ALT.drop + (prog > 0.85 ? (prog - 0.85) / 0.15 * 130 : 0);   // already lifting off the line
      water = cls.payloadT - plan.deliveredT * ((pi + e) / nP);
      // Heading is the line's, reversed on alternate passes and swung through the turn rather
      // than snapped — the ship is barely moving there, which is when a hull that size turns.
      const kx = Math.cos(ll[1] * Math.PI / 180);
      const segB = Math.atan2((sB[0] - sA[0]) * kx, sB[1] - sA[1]);
      // A 180° reversal is the one case shortest-arc interpolation cannot answer: the two
      // directions are exactly equal, so floating-point noise in (a + π) − a picks one per
      // sample and the hull flickers end for end. Count the turns instead and always swing
      // the same way — the heading accumulates, which is also what a rate-limited camera
      // wants to follow.
      const tw = 0.12;
      let turns = pi, frac = 0;
      if (pi < nP - 1 && pf > 1 - tw) frac = (pf - (1 - tw)) / (2 * tw);
      else if (pi > 0 && pf < tw) { turns = pi - 1; frac = (pf + tw) / (2 * tw); }
      bearing = segB + Math.PI * (turns + easeSm(frac));
      if (prog > 0.5) sub = "buoyancy building — escape climb imminent";
      draw.fans = plan.dragMW * 0.5; draw.prop = plan.dragMW * 0.4;
      break;
    }
    case "BUOYANCY_ESCAPE":
      // The cork. It leaves the line barely moving and accelerates the whole way up: 10% of
      // the return curve is covered here, on a squared profile, not the 2% that made the
      // most dramatic phase of the cycle look like a hover.
      // How far along the return curve the climb actually carries the ship, derived from the
      // speed the dial is showing rather than picked: average escape speed x duration, as a
      // fraction of the leg. A hand-chosen fraction had the map moving at 300 km/h while the
      // needle read 120.
      B(sB, cR, ikX, escF * Math.pow(prog, 1.7));
      // Comes off the line still pointing down it, and turns onto the homeward curve as it
      // rises — the climb and the turn are one movement, not a snap followed by a climb.
      if (prog < 0.35) {
        const kxe = Math.cos(ll[1] * Math.PI / 180);
        const lineB = Math.atan2((sB[0] - sA[0]) * kxe, sB[1] - sA[1]) +
          Math.PI * ((plan.passes || 1) - 1);
        bearing = lerpAng(lineB, bearing, easeSm(prog / 0.35));
      }
      alt = ALT_DROP_TOP + (altTop * 0.55 - ALT_DROP_TOP) * sm;
      water = plan.retainedT;
      draw.fans = plan.dragMW * 0.12;
      sub = prog < 0.28 ? "rotors feathering — buoyancy has it" : "arresting the climb";
      break;
    case "RETURN_TRANSIT": {
      B(sB, cR, ikX, escF + tz * (0.96 - escF));   // ends short: the approach flies the rest in
      const a0 = altTop * 0.55;
      alt = tz < 0.3 ? a0 + (altTop - a0) * easeSm(tz / 0.3)
          : tz > 0.7 ? altTop - (altTop - ALT.source - 130) * easeSm((tz - 0.7) / 0.3)
          : altTop;
      water = plan.retainedT;
      ln2 = plan.ln2MakeT * Math.min(1, prog / 0.85);
      draw.prop = plan.dragMW * 0.55;
      if (prog < 0.85) draw.cryo = cls.cryoMW * CFG.cryoMul * m.mode.cryoShare;
      if (prog > 0.72) sub = "descending to hose range";
      else if (prog < 0.30) sub = "holding the ceiling, empty";
      break;
    }
  }
  // speed fraction and accel sense for the transit legs (drives the rotor tilt display)
  let vf = 0, acc = 0;
  if (id === "OUTBOUND_TRANSIT" || id === "RETURN_TRANSIT") {
    const aE = 0.15;
    vf = Math.min(prog / aE, 1, (1 - prog) / aE);
    acc = prog < aE ? 1 : prog > 1 - aE ? -1 : 0;
  } else if (id === "WATER_RELEASE" || id === "BUOYANCY_ESCAPE") vf = 0.5;
  const massT = led.dryT + water + ln2;
  /* THE VERTICAL DUTY — one number, read by the 3D model, the schematic avatar and the power
     ledger, so none of them can disagree about which way the rotors are pushing.
     Never positive: the hull is buoyant at every point in the cycle, so the rotors only ever
     hold it DOWN, and climbing means RELAXING that hold. Magnitude is the physics — surplus
     lift now over the most there can be, empty — times a per-phase multiplier.
     `share` is how much of that surplus the rotors carry rather than aero trim: 12% holding
     station or cruising level, up to 60% when they are actively driving the hull down. */
  const reserveT = Math.max(1, led.liftT - led.dryT);
  const netFrac = Math.min(1, Math.max(0, led.liftT - massT) / reserveT);
  let hold = 1, share = 0.12;
  if (id === "OUTBOUND_TRANSIT") {
    hold = prog < 0.10 ? 1 - 0.75 * easeSm(prog / 0.10)
      : prog < 0.34 ? 0.25 + 0.55 * ((prog - 0.10) / 0.24) : 0.8;
  } else if (id === "WATER_RELEASE") {
    share = 0.12 + 0.33 * (1 - water / Math.max(1, cls.payloadT));
  } else if (id === "BUOYANCY_ESCAPE") {
    hold = prog < 0.28 ? 1 - 0.94 * (prog / 0.28)
      : 0.06 + 0.94 * Math.pow((prog - 0.28) / 0.72, 1.5);
    share = 0.12 + 0.33 * Math.max(0, (prog - 0.28) / 0.72);
  } else if (id === "RETURN_TRANSIT") {
    hold = prog < 0.30 ? 1 - 0.2 * (prog / 0.30)
      : prog > 0.72 ? 0.8 + 0.2 * ((prog - 0.72) / 0.28) : 0.8;
    share = prog > 0.72 ? 0.12 + 0.48 * ((prog - 0.72) / 0.28) : 0.12;
  } else if (id === "SOURCE_APPROACH") {
    share = 0.12 + 0.48 * Math.max(0, 1 - prog / 0.35);   // easing out of the letdown
  }
  const vert = -hold * netFrac;
  if (!stopped) {
    draw.rotors = Math.min((cls.battMW + cls.genMW) * 0.95,
      diskMW(cls, Math.abs(vert) * reserveT * 1000 * 9.81 * share));
  }
  const buoyN = led.liftT * 1000 * 9.81;
  const weightN = massT * 1000 * 9.81;
  // Instantaneous ground speed, km/h — the dial's needle, not the plan's out/back averages.
  // Phase SEAMS carry speed across: the outbound ends at the drop-run speed, the return ends
  // at the approach's entry speed, the escape hands off to the return — nothing except the
  // fill (a true station-hold) passes through zero.
  let gs = 0;
  const vRun = cls.dropKm * (plan.passes || 1) / Math.max(0.05, plan.dur.WATER_RELEASE) * 60;
  const vApp = Math.max(6, plan.gsOut * 0.3);
  const aE2 = 0.15;
  const vEsc = plan.gsRet * 0.85;      // what the escape climb has built by the time it ends
  if (id === "OUTBOUND_TRANSIT") {
    // Arrives ON the line, not past it: the run's first pass starts from rest, so the
    // outbound decelerates to meet it.
    gs = prog < aE2 ? plan.gsOut * (prog / aE2)
       : prog > 1 - aE2 ? plan.gsOut * ((1 - prog) / aE2)
       : plan.gsOut;
  } else if (id === "RETURN_TRANSIT") {
    gs = prog < aE2 ? vEsc + (plan.gsRet - vEsc) * (prog / aE2)
       : prog > 1 - aE2 ? vApp + (plan.gsRet - vApp) * ((1 - prog) / aE2)
       : plan.gsRet;
  } else if (id === "WATER_RELEASE") {
    // The needle reads what the ship is ACTUALLY doing on the line: the derivative of the
    // eased shuttle, so it falls to nothing at each turn and averages out to the run speed.
    const nP = plan.passes || 1;
    const kk = Math.min(nP - 1e-9, prog * nP);
    const pff = kk - Math.floor(kk);
    gs = vRun * 6 * pff * (1 - pff);
  } else if (id === "BUOYANCY_ESCAPE") gs = vEsc * Math.pow(prog, 1.5);
  else if (id === "SOURCE_APPROACH") gs = Math.max(2, vApp * (1 - sm));
  // Generation: the solar skin, plus the nitrogen store handing energy back while ballast
  // converts to water during the fill. That is ALL a hull generates — the bus otherwise
  // spends storage, and every cycle runs a deficit until an energy import chain exists.
  const gen = { solar: cls.solarM2 * 200 / 1e6 };
  if (id === "WATER_FILL") gen.regen = plan.eBack / Math.max(0.02, plan.dur.WATER_FILL / 60);
  if (stopped) { draw = {}; sub = "power exhausted — safe shutdown"; gs = 0; vf = 0; acc = 0; }
  return { idx, phase: id, label: PHASES[idx][1], prog, ll, bearing, alt, water, ln2, sub,
    draw, gen, gs, stopped, massT, buoyN, weightN, netN: buoyN - weightN, vf, acc, vert,
    cyclePos: t, cycleN: cycN };
}

/* The Mind's trace: last / now / next / plan, from the state machine and real numbers. */
