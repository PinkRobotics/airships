#!/usr/bin/env node
/* The 2026-10-01 energy-model change, measured: every published energy figure before and after,
 * and WHY each one moved, attributed defect by defect.
 *
 *   node research/analysis/energy-model-change.mjs [--old <git-ref|path>] [--out <json>]
 *
 * Nothing in the output is typed. "Old" is research/figures.json as the base commit published it
 * (read with `git show`, or from a file); "new" is the committed research/figures.json, which
 * `make factsheet` regenerates from the live model and `tools/check_figures_fresh.py` keeps
 * honest. The attribution re-prices the SAME flown cycle five times with the counterfactual
 * switches in sim/power.js drawAt — the old rotor physics, the rotors blind to the bag, the
 * generators' nameplate on the bus — walking from the old model's assumptions to the new one's
 * one at a time, so the steps telescope exactly to the published difference.
 *
 * docs/ENERGY-MODEL-2026-10.md is written from the JSON this emits. If the two disagree, this
 * file is right and the document is stale.
 */
import { execFileSync } from 'node:child_process';
import { existsSync, readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..', '..');
const args = process.argv.slice(2);
const opt = (name, dflt) => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : dflt; };
const OLD_REF = opt('--old', '09b9c0e');
const OUT = path.resolve(ROOT, opt('--out', 'research/analysis/energy-model-change.json'));

const S = await import(new URL('../../sim/index.js', import.meta.url));
const { CFG, CLASSES, CLASS_ORDER, MODES, PHASES, TERRAIN_MSL, BUS_CEILING, SHARE_MAX, PLAN_STEPS,
  LETDOWN_FROM, integrateCycle, ledger, planCycle, resetConfig, stateAt } = S;
resetConfig();

const oldText = existsSync(OLD_REF) ? readFileSync(OLD_REF, 'utf8')
  : execFileSync('git', ['show', `${OLD_REF}:research/figures.json`], { cwd: ROOT, encoding: 'utf8' });
const OLD = JSON.parse(oldText);
const NEW = JSON.parse(readFileSync(path.join(ROOT, 'research/figures.json'), 'utf8'));
const r = (x, n = 3) => (Number.isFinite(x) ? Number(x.toFixed(n)) : null);
const pct = (a, b) => (b ? r(100 * (a - b) / Math.abs(b), 1) : null);
const G = 9.81;

/** The descent closure as plan.js struck it BEFORE the change: the generators' nameplate on the
    bus, no ceiling, rotors at a 0.6 share. Replicated here, and checked against what the old
    figures.json published, so the counterfactual flight is the old model's flight and not a
    guess at it. */
function oldClosure(c, p) {
  const busMW = c.battMW + c.genMW;
  const rotorMaxT = Math.pow(busMW * 1e6 * CFG.propEta * Math.sqrt(2 * CFG.rhoAir * c.diskM2), 2 / 3) / G / 1000;
  const rotorCapT = rotorMaxT / 0.6;
  const srcAltM = S.sourceAltM(c);
  let anchorFromAglM = srcAltM;
  for (let a = srcAltM; a <= srcAltM + (c.anchorM || 0); a += 10) {
    if (ledger(c, TERRAIN_MSL + a).surplusT - p.ln2MakeT > rotorCapT) anchorFromAglM = a;
  }
  return { busMW, rotorMaxT, rotorCapT, anchorFromAglM };
}

/** A map-less mission, so stateAt can be integrated over exactly the plan's cycle. */
function synthetic(cls, mode, km) {
  const plan = planCycle(cls, mode, km);
  const m = { cls, mode, plan, offset: 0, legKm: km, oneWayKm: km, wind: null,
    fire: { id: `X-${cls.id}`, ll: [-120.05, 50.05] }, intake: [-120.30, 50.00], delivery: [-120.05, 50.05] };
  m.cycleSec = plan.cycleMin * 60; m.phaseEnds = [];
  let acc = 0;
  for (const [id] of PHASES) { acc += plan.dur[id] * 60; m.phaseEnds.push(acc); }
  return m;
}
function integrateState(m, N = 4000) {
  let draw = 0, regen = 0, letdown = 0;
  const dtH = m.cycleSec / N / 3600;
  for (let i = 0; i < N; i++) {
    const st = stateAt(m, m.cycleSec * (i + 0.5) / N);
    for (const v of Object.values(st.draw)) draw += v * dtH;
    regen += (st.gen.regen || 0) * dtH;
    if (st.phase === 'SOURCE_APPROACH' || (st.phase === 'RETURN_TRANSIT' && st.prog > LETDOWN_FROM)) letdown += (st.draw.rotors || 0) * dtH;
  }
  return { netMWh: draw - regen, letdownMWh: letdown };
}

const out = {
  generated: { by: 'research/analysis/energy-model-change.mjs', oldFigures: `${OLD_REF}:research/figures.json`,
    newFigures: 'research/figures.json', worked: NEW.worked, planSteps: PLAN_STEPS },
  summary: {
    what: 'One energy model: planCycle\'s budget is the integral of the same drawAt the instruments show (sim/power.js). '
      + 'Rotor power is Glauert momentum theory with the airspeed and the rate of descent in it; the anchor is credited '
      + 'before the rotors; the letdown is read out of the flown descent with no window constant; the generators are '
      + 'LN2 storage bounded by what the cryo plant made, not a source.',
    defects: { 2: 'forward flight in the rotor model, and one model', 3: 'the min(6, 0.2 x return) window and the 1.12 stretch',
      6: 'generators as storage, honest bus', 14: 'the anchor credited before the rotors', 15: 'hold-down priced over the whole flown descent' },
  },
  classes: {},
  modeOrderingP10000At60km: null,
  sensitivityP10000: {},
};

for (const id of CLASS_ORDER) {
  const c = CLASSES[id];
  const o = OLD.classes[id], n = NEW.classes[id];
  const p = planCycle(c, MODES.balanced, CFG.exampleKm);
  if (r(p.eCycleMWh, 3) !== n.cycle.eCycleMWh) throw new Error(`${id}: research/figures.json is stale (${n.cycle.eCycleMWh} vs ${p.eCycleMWh}); run make factsheet first`);
  const oc = oldClosure(c, p);
  if (r(oc.rotorCapT, 1) !== o.descent.rotorCapT || oc.anchorFromAglM !== o.descent.anchorFromAglM)
    throw new Error(`${id}: the replicated old closure (${oc.rotorCapT}, ${oc.anchorFromAglM}) does not match the old figures (${o.descent.rotorCapT}, ${o.descent.anchorFromAglM})`);

  // The flown cycle, re-priced step by step from the old model's assumptions to the new one's.
  const oldGeom = { ...p, anchorFromAglM: oc.anchorFromAglM };
  const step = (plan, opts) => integrateCycle(c, MODES.balanced, plan, PLAN_STEPS, opts);
  const s1 = step(oldGeom, { hover: true, anchorCredit: false, nameplateBus: true });
  const s2 = step(oldGeom, { anchorCredit: false, nameplateBus: true });
  const s3 = step(oldGeom, { nameplateBus: true });
  const s4 = step(oldGeom, {});
  const s5 = step(p, {});
  if (Math.abs(s5.eCycleMWh - p.eCycleMWh) > 1e-9) throw new Error(`${id}: the last step is not the published plan`);
  const steps = [
    { step: 0, label: 'the old budget as published', eCycleMWh: r(o.cycle.eCycleMWh, 3), defect: null },
    { step: 1, label: 'ONE model: the budget becomes the integral of the flown cycle, still with hover-priced rotors, '
        + 'blind to the bag, on the nameplate bus (defects 3 and 15: hold-down priced wherever the ship is, no window, no 1.12 stretch)',
      eCycleMWh: r(s1.eCycleMWh), defect: '3+15', letdownMWh: r(s1.letdownMWh), downMW: r(s1.downMW, 1) },
    { step: 2, label: 'rotor power by Glauert momentum theory: airspeed through the disks, rate of descent in the axial term (defect 2)',
      eCycleMWh: r(s2.eCycleMWh), defect: '2', letdownMWh: r(s2.letdownMWh), downMW: r(s2.downMW, 1) },
    { step: 3, label: 'the anchor credited before the rotors (defect 14)', eCycleMWh: r(s3.eCycleMWh), defect: '14',
      letdownMWh: r(s3.letdownMWh), downMW: r(s3.downMW, 1) },
    { step: 4, label: 'the bus the rotors are clamped to is the battery plus what the nitrogen store returns, not the nameplate (defect 6, the clamp)',
      eCycleMWh: r(s4.eCycleMWh), defect: '6', letdownMWh: r(s4.letdownMWh), downMW: r(s4.downMW, 1) },
    { step: 5, label: 'the descent closure struck on the same honest bus: rotorMaxT falls, the altitude where the rotors stop managing alone rises, and the hold altitude with it (defect 6, the closure)',
      eCycleMWh: r(s5.eCycleMWh), defect: '6', letdownMWh: r(s5.letdownMWh), downMW: r(s5.downMW, 1) },
  ];
  for (let i = 1; i < steps.length; i++) {
    steps[i].deltaMWh = r(steps[i].eCycleMWh - steps[i - 1].eCycleMWh);
    steps[i].deltaPctOfOld = pct(steps[i].eCycleMWh, steps[0].eCycleMWh) - (i > 1 ? pct(steps[i - 1].eCycleMWh, steps[0].eCycleMWh) : 0);
    steps[i].deltaPctOfOld = r(steps[i].deltaPctOfOld, 1);
  }
  const solarMWh = c.solarM2 * CFG.solarWPerM2 / 1e6 * p.cycleMin / 60;
  const bare = planCycle({ ...c, anchorBagT: 0 }, MODES.balanced, CFG.exampleKm);
  const agree = integrateState(synthetic(c, MODES.balanced, CFG.exampleKm));
  const moved = (key, oldV, newV, dp, defect, why) => ({ key, old: oldV, new: newV,
    changePct: typeof oldV === 'number' && typeof newV === 'number' ? pct(newV, oldV) : null, defect, why });

  out.classes[id] = {
    published: [
      moved('cycle.eCycleMWh', o.cycle.eCycleMWh, n.cycle.eCycleMWh, 3, '2, 3, 6, 14, 15', 'the budget is now the integral of the flown cycle; see attribution'),
      moved('cycle.kwhPerTonne', o.cycle.kwhPerTonne, n.cycle.kwhPerTonne, 2, '2, 3, 6, 14, 15', 'eCycleMWh over the same delivered tonnes'),
      moved('energy.deficitPerCycleMWh', o.energy.deficitPerCycleMWh, n.energy.deficitPerCycleMWh, 2, '2, 3, 6, 14, 15', 'the cycle grew; solar did not'),
      moved('energy.hoursOnBattery', o.energy.hoursOnBattery, n.energy.hoursOnBattery, 1, '2, 3, 6, 14, 15', 'battery over the deficit, times the cycle'),
      moved('energy.cyclesOnBattery', o.energy.cyclesOnBattery, n.energy.cyclesOnBattery, 1, '2, 3, 6, 14, 15', 'battery over the deficit'),
      moved('energy.downMW', o.energy.downMW, n.energy.downMW, 1, '15, 14, 6',
        'was the anchor-assisted hold-down at the fill altitude; is now the rotors\' peak draw over the flown cycle, which falls in the approach before the bag is in'),
      moved('energy.ledgerMWh.letdown -> energy.letdownMWh', o.energy.ledgerMWh.letdown, n.energy.letdownMWh, 3, '3, 15',
        'was downMW x min(6, 0.2 x return)/60; is the rotor energy integrated over the return leg\'s descent and the approach'),
      moved('energy.ledgerMWh.anchor -> energy.anchorHoistMWh', o.energy.ledgerMWh.anchor, n.energy.anchorHoistMWh, 3, '-',
        'the same m g h / eta, now priced as winch power in the integral (delivered at the winch speed)'),
      moved('descent.rotorCapT', o.descent.rotorCapT, n.descent.rotorCapT, 1, '6', 'rotorMaxT on BUS_CEILING x (battMW + regen during the approach), over SHARE_MAX'),
      moved('descent.anchorFromAglM', o.descent.anchorFromAglM, n.descent.anchorFromAglM, 0, '6',
        'the altitude below which the rotors cannot hold the hull alone, on the honest bus; capped at the cable top'),
      moved('descent.battLimited', o.descent.battLimited, n.descent.battLimited, 0, '3, 6',
        'now means the bus clamp held the rotors during the letdown (letdownClipMin > 0); the 0.92 threshold is gone'),
      moved('cycle.bottleneck', o.cycle.bottleneck, n.cycle.bottleneck, 0, '6', 'follows battLimited'),
      moved('cycle.cycleMin', o.cycle.cycleMin, n.cycle.cycleMin, 2, '-', 'durations are kinematic and did not move; the 1.12 stretch never fired at the worked example'),
      moved('cycle.tph', o.cycle.tph, n.cycle.tph, 0, '-', 'delivered tonnes and cycle minutes did not move'),
    ],
    ledgerOld: o.energy.ledgerMWh,
    ledgerNew: { byPhase: n.energy.ledgerMWh, byChannel: n.energy.ledgerByChannelMWh },
    attribution: { steps, telescopes: r(steps[steps.length - 1].eCycleMWh - steps[0].eCycleMWh) === r(n.cycle.eCycleMWh - o.cycle.eCycleMWh) },
    oldClosureReplicated: { busMW: oc.busMW, rotorMaxT: r(oc.rotorMaxT, 1), rotorCapT: r(oc.rotorCapT, 1), anchorFromAglM: oc.anchorFromAglM },
    newClosure: { busMW: r(p.busMW, 2), rotorMaxT: r(p.rotorMaxT, 1), rotorCapT: r(p.rotorMaxT / SHARE_MAX, 1), anchorFromAglM: p.anchorFromAglM,
      busCeiling: BUS_CEILING, shareMax: SHARE_MAX, letdownClipMin: r(p.letdownClipMin, 2), rotorClipMWh: r(p.rotorClipMWh, 3) },
    agreement: { integratedStateAtMWh: r(agree.netMWh), budgetMWh: r(p.eCycleMWh), ratio: r(agree.netMWh / p.eCycleMWh, 5),
      letdownIntegratedMWh: r(agree.letdownMWh), letdownBudgetMWh: r(p.letdownMWh) },
    solar: { perCycleMWh: r(solarMWh, 3), deficitPerCycleMWh: r(p.eCycleMWh - solarMWh, 2) },
    theBagsTrade: {
      note: 'What the bag buys is water, not energy: a bare hull keeps lake water aboard as ballast and is heavier on every phase.',
      withBag: { eCycleMWh: r(p.eCycleMWh), kwhPerTonne: r(p.kwhPerTonne, 2), deliveredT: r(p.deliveredT, 1), retainedT: r(p.retainedT, 1) },
      withoutBag: { eCycleMWh: r(bare.eCycleMWh), kwhPerTonne: r(bare.kwhPerTonne, 2), deliveredT: r(bare.deliveredT, 1), retainedT: r(bare.retainedT, 1), bottleneck: bare.bottleneck },
    },
  };
}

{
  const q = m => planCycle(CLASSES.P10000, m, 60);
  const rp = q(MODES.rapid), b = q(MODES.balanced), e = q(MODES.endurance);
  out.modeOrderingP10000At60km = {
    note: 'The eighth flip. Old values are the pins the test carried at the base commit (tests/cases/sim-plan.cases.js); new values are computed.',
    old: { rapid: 158.0, balanced: 143.1, endurance: 133.4, cheapest: 'endurance' },
    new: { rapid: r(rp.eCycleMWh, 3), balanced: r(b.eCycleMWh, 3), endurance: r(e.eCycleMWh, 3),
      cheapest: [['rapid', rp], ['balanced', b], ['endurance', e]].sort((x, y) => x[1].eCycleMWh - y[1].eCycleMWh)[0][0],
      rotorsMWh: { rapid: r(rp.Echan.rotors), balanced: r(b.Echan.rotors), endurance: r(e.Echan.rotors) },
      propMWh: { rapid: r(rp.Echan.prop), balanced: r(b.Echan.prop), endurance: r(e.Echan.prop) },
      cryoMWh: { rapid: r(rp.Echan.cryo || 0), balanced: r(b.Echan.cryo || 0), endurance: r(e.Echan.cryo || 0) } },
  };
}
for (const k of Object.keys(NEW.sensitivity)) {
  out.sensitivityP10000[k] = { old: OLD.sensitivity[k] || null, new: NEW.sensitivity[k] };
}

writeFileSync(OUT, JSON.stringify(out, null, 2) + '\n');
console.log(`wrote ${path.relative(ROOT, OUT)}`);
for (const id of CLASS_ORDER) {
  const c = out.classes[id];
  const e = c.published.find(x => x.key === 'cycle.eCycleMWh');
  console.log(`${id}: eCycleMWh ${e.old} -> ${e.new} (${e.changePct > 0 ? '+' : ''}${e.changePct}%); agreement ${c.agreement.ratio}`);
  for (const s of c.attribution.steps.slice(1)) console.log(`   step ${s.step} [${s.defect}] ${s.eCycleMWh} MWh (${s.deltaMWh >= 0 ? '+' : ''}${s.deltaMWh}, ${s.deltaPctOfOld >= 0 ? '+' : ''}${s.deltaPctOfOld}% of old)`);
}
