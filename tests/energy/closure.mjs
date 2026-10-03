/* Independent force, power and verdict equations, adapted from claude-fable-5-1. */
import { loadTree, norm, planInfo, sum } from './model.mjs';
const { S, which } = await loadTree();
S.resetConfig();
const N = +(process.env.N || 1000);
const CFG = S.CFG, G = 9.81, ETA = CFG.propEta, CD = CFG.Cd, RHO_ROTOR = CFG.rhoAir;
const HOIST_M = 15, WINCH_ETA = 0.85;             // both trees' named constants (power.js)
const planform = c => c.diaM * (c.lenM - c.diaM) + Math.PI * (c.diaM / 2) ** 2;
const frontal = c => Math.PI * (c.diaM / 2) ** 2;
function glauertMW(c, thrustN, V, vc, rho) {              // independent momentum-theory price
  if (thrustN <= 0) return 0;
  const vh2 = thrustN / (2 * rho * c.diskM2);
  if (V === 0 && vc === 0) return thrustN * Math.sqrt(vh2) / ETA / 1e6;
  let lo = 0, hi = Math.sqrt(vh2);
  for (let k = 0; k < 80; k++) { const m = (lo + hi) / 2; if (m * Math.sqrt(V * V + (vc + m) ** 2) > vh2) hi = m; else lo = m; }
  return thrustN * (vc + (lo + hi) / 2) / ETA / 1e6;
}
const zeroLiftMW = (c, rho, V) => 0.5 * rho * CD * frontal(c) * V ** 3 / ETA / 1e6;
const inducedMW = (c, rho, V, forceN) => (V <= 0 || forceN <= 0) ? 0 : forceN * forceN / (0.5 * rho * V * V * Math.PI * c.diaM ** 2 * 1) * V / ETA / 1e6;
const winds = [null, { spd: 40, dir: 270, bearing: 90 }, { spd: 25, dir: 90, bearing: 90 }];
const KNOWN = new Set(['hotel', 'winch', 'pumps', 'cryo', 'prop', 'rotors']);
const viol = {}; const worst = {};
const note = (k, rel, ex) => { viol[k] = (viol[k] || 0) + 1; if (!worst[k] || rel > worst[k].rel) worst[k] = { rel, ...ex }; };
let plans = 0, instants = 0, feasiblePlans = 0, rotorUp = 0, bagInstants = 0, aeroInstants = 0;
const mismatches = [], channelsSeen = {}, fansRatio = {};
let hoistWorst = { rel: 0 };
for (const c of Object.values(S.CLASSES)) for (const m of Object.values(S.MODES)) for (const km of [5, 15, 30, 60, 120]) for (const wind of winds) for (const basis of ['record', 'favourable']) {
  const tag = `${c.id}/${m.id}/${km}/wind${wind?.spd || 0}/${basis}`;
  const p = S.planCycle(c, m, km, wind, { basis });
  const pi = planInfo(which, p); plans++;
  const bagCap = Math.min(p.anchorT, c.anchorBagT) + 1e-9, reach = c.anchorM - c.diaM / 2;
  let scanOk = true, scanWorst = 0, scanWhere = '', maxBag = 0;
  for (const [id] of S.PHASES) for (let i = 0; i <= N; i++) {
    const x = i / N, raw = S.drawAt(c, m, p, id, x), s = norm(which, raw); instants++;
    const ex = { tag, phase: id, x };
    const sur = s.surplusT, tolF = 1e-6 * Math.max(1, Math.abs(sur));
    // sum
    const owners = s.bagT + s.rotorT + s.aeroT + s.vdragDownT + s.inertiaDownT + s.unheldT;
    const dSum = Math.abs(owners - sur); if (dSum > tolF) note('sum', dSum / Math.max(1, Math.abs(sur)), { ...ex, owners, sur });
    // bag
    if (s.bagT > 0) {
      bagInstants++; maxBag = Math.max(maxBag, s.bagT);
      if (s.bagT > bagCap) note('bagCap', s.bagT / bagCap - 1, { ...ex, bag: s.bagT, cap: bagCap });
      if (s.alt > reach + 1e-9) note('bagReach', s.alt - reach, { ...ex, alt: s.alt, reach });
      if (raw.gs / 3.6 > 2 + 1e-9) note('bagMoving', raw.gs / 3.6 - 2, { ...ex, gsMps: raw.gs / 3.6 });
      if (!(id === 'SOURCE_APPROACH' || id === 'WATER_FILL' || (id === 'RETURN_TRANSIT' && x > 0.94))) note('bagPhase', 1, { ...ex, bag: s.bagT });
    }
    if (s.bagT < -1e-9) note('bagNegative', -s.bagT, ex);
    // rotor cap and direction
    if (Math.abs(s.rotorT) > s.rotorCapT * (1 + 1e-9) + 1e-9) note('rotorCap', Math.abs(s.rotorT) / s.rotorCapT - 1, { ...ex, rotor: s.rotorT, cap: s.rotorCapT });
    if (s.rotorT < -1e-9) rotorUp++;
    // aero cap, zero airspeed, record basis
    const rhoTree = s.rho;                 // the tree's density convention for q
    const clMax = p.clMax ?? 1;
    const aeroCapMine = basis === 'favourable' ? clMax * 0.5 * rhoTree * s.airV ** 2 * planform(c) / (1000 * G) : 0;
    if (s.aeroT < -1e-9) note('aeroNegative', -s.aeroT, ex);
    if (s.aeroT > 0) aeroInstants++;
    if (s.aeroT > aeroCapMine * (1 + 1e-9) + 1e-9) note('aeroCap', aeroCapMine > 0 ? s.aeroT / aeroCapMine - 1 : s.aeroT, { ...ex, aero: s.aeroT, capMine: aeroCapMine, capTree: s.aeroCapT });
    if (s.airV === 0 && s.aeroT > 1e-12) note('aeroAtZeroV', s.aeroT, ex);
    if (basis === 'record' && s.aeroT > 1e-12) note('aeroOnRecord', s.aeroT, ex);
    // rotor price
    const vc = s.rotorT >= 0 ? Math.max(0, -s.vz) : Math.max(0, s.vz);
    const priceMine = glauertMW(c, Math.abs(s.rotorT) * 1000 * G, s.airV, vc, s.rho);
    const dPrice = Math.abs(priceMine - s.rotorsMW) / Math.max(1e-9, priceMine);
    if (dPrice > 1e-6) note('rotorPrice', dPrice, { ...ex, mine: priceMine, tree: s.rotorsMW });
    // propulsion law at the actual airspeed
    const propMine = zeroLiftMW(c, rhoTree, s.airV) + inducedMW(c, rhoTree, s.airV, s.aeroT * 1000 * G);
    const dProp = Math.abs(propMine - s.draw.prop) / Math.max(1e-9, propMine);
    if (dProp > 1e-6) note('propLaw', dProp, { ...ex, mine: propMine, tree: s.draw.prop, V: s.airV });
    // channels outside the named consumers
    for (const k of Object.keys(s.draw)) { channelsSeen[k] = (channelsSeen[k] || 0) + 1; if (!KNOWN.has(k)) { const r = s.draw[k] / p.dragMW; fansRatio[`${id}:${k}`] = r; } }
    // bus
    const over = s.gross - s.busMW; if (over > 1e-6) { note('bus', over, { ...ex, gross: s.gross, bus: s.busMW, flagged: (s.limits || []).join('+') }); scanOk = false; }
    if (Math.abs(s.unheldT) > tolF) { scanOk = false; if (Math.abs(s.unheldT) > Math.abs(scanWorst)) { scanWorst = s.unheldT; scanWhere = `${id}@${x}`; } }
  }
  // hoist energy vs the largest bag mass lifted HOIST_M
  const hoistExpect = maxBag * 1000 * G * HOIST_M / WINCH_ETA / 3.6e9;
  const hoistRel = Math.abs((p.anchorHoistMWh || 0) - hoistExpect) / Math.max(1e-12, hoistExpect);
  if (maxBag > 0 && hoistRel > hoistWorst.rel) hoistWorst = { rel: hoistRel, tag, hoistMWh: p.anchorHoistMWh, expect: hoistExpect, maxBagT: maxBag };
  if (pi.feasible) feasiblePlans++;
  if (pi.feasible !== scanOk) mismatches.push({ tag, planFeasible: pi.feasible, scanFeasible: scanOk, scanWorst, scanWhere, modelWorst: pi.worstT, modelWhere: `${pi.worstPhase}@${pi.worstProg}` });
}
console.log(JSON.stringify({ tree: which, N, plans, instants, feasiblePlans, rotorUpInstants: rotorUp, bagInstants, aeroInstants,
  violations: viol, worst, channelsSeen, phaseKeyedConsumers: fansRatio, hoistWorst, verdictMismatches: mismatches }, null, 1));

if(Object.keys(viol).length||mismatches.length||Object.keys(fansRatio).length)process.exitCode=1;
