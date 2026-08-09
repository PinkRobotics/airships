(async () => {
  /* One dump script, two page shapes. The pre-refactor page declared the model at the top
     level of a classic script, so the identifiers resolve bare. The refactored page is an
     ES module and publishes the model at window.AIRSHIPS.sim. Reading both through `Q`
     lets the same script produce comparable output from either, which is the whole point:
     the refactor is only correct if these two dumps are identical. */
  const modular = typeof window.AIRSHIPS !== 'undefined';
  const Q = modular ? window.AIRSHIPS.sim : {
    CLASSES: CLASSES, CLASS_ORDER: CLASS_ORDER, DEFAULTS: DEFAULTS, HULL_NAMES: HULL_NAMES,
    MODES: MODES, ledger: ledger, planCycle: planCycle, stateAt: stateAt,
    narrate: narrate, selftest: selftest,
  };
  const APPSTATE = modular ? window.AIRSHIPS.app : S;
  const ov = document.getElementById('introOv'); if (ov) ov.click();
  await new Promise(r => setTimeout(r, 3000));
  const R = (x, n = 6) => (typeof x === 'number' && isFinite(x) ? +x.toFixed(n) : x);
  const RO = (o, n = 6) => { const q = {}; for (const k of Object.keys(o || {}).sort()) q[k] = R(o[k], n); return q; };

  const out = { version: 1, note: 'golden characterisation dump; seed=7 data=snapshot' };

  // 1. the class table and the tunable defaults
  out.classes = {};
  for (const id of Q.CLASS_ORDER) { const c = Q.CLASSES[id]; const q = {}; 
    for (const k of Object.keys(c).sort()) if (typeof c[k] !== 'function') q[k] = R(c[k]);
    out.classes[id] = q; }
  out.defaults = RO(Q.DEFAULTS);
  out.hullNames = Q.HULL_NAMES;

  // 2. the mass/lift Q.ledger per class, at every altitude the cycle visits. The ledger takes
  // an altitude now, so one row per class would pin the sizing point and nothing else — and
  // the whole point of the change is that lift varies across the cycle.
  out.ledger = {};
  // The source row is per class now: each carries its own hose, so each fills at its own
  // altitude, and that altitude is what decides whether it can drop its whole load.
  for (const id of Q.CLASS_ORDER) {
    const LEDGER_ALTS = { ground: Q.TERRAIN_MSL,
      source: Q.TERRAIN_MSL + Q.sourceAltM(Q.CLASSES[id]),
      drop: Q.TERRAIN_MSL + Q.ALT.drop, work: Q.WORK_ALT_MSL };
    out.ledger[id] = {};
    for (const [where, alt] of Object.entries(LEDGER_ALTS)) {
      out.ledger[id][where] = RO(Q.ledger(Q.CLASSES[id], alt));
    }
  }

  // 3. Q.planCycle over a grid — the numbers the site publishes
  out.plans = [];
  const WINDS = [null, { spd: 40, dir: 270, bearing: 90 }, { spd: 25, dir: 90, bearing: 90 }];
  for (const id of Q.CLASS_ORDER) for (const mode of Object.keys(Q.MODES).sort())
    for (const km of [5, 15, 30, 60, 120]) for (let w = 0; w < WINDS.length; w++) {
      const p = Q.planCycle(Q.CLASSES[id], Q.MODES[mode], km, WINDS[w]);
      out.plans.push({ cls: id, mode, km, wind: w,
        cycleMin: R(p.cycleMin), tph: R(p.tph), eCycleMWh: R(p.eCycleMWh),
        kwhPerTonne: R(p.kwhPerTonne), retainedT: R(p.retainedT), deliveredT: R(p.deliveredT),
        passes: p.passes, downMW: R(p.downMW), ln2MakeT: R(p.ln2MakeT), eBack: R(p.eBack),
        gsOut: R(p.gsOut), gsRet: R(p.gsRet), rotorMaxT: R(p.rotorMaxT),
        bottleneck: p.bottleneck, dur: RO(p.dur), dropsPerHour: R(p.dropsPerHour),
        pumpMW: R(p.pumpMW), dragMW: R(p.dragMW), cryoLimited: p.cryoLimited, battLimited: p.battLimited });
    }

  // 4. the fleet as allocated from the pinned data
  const act = APPSTATE.missions.filter(m => !m.idle);
  out.fleet = act.map(m => ({ name: m.name, cls: m.cls.id, fire: m.fire.id,
    sizeHa: R(m.fire.sizeHa, 3), status: m.fire.status, src: m.water && m.water[4],
    oneWayKm: R(m.oneWayKm), legKm: R(m.legKm), cycleSec: R(m.cycleSec),
    tph: R(m.plan.tph), passes: m.plan.passes, stations: (m.stations || []).length,
    targets: (m.targets || []).length, heat: !!m.heat, offset: R(m.offset) }));
  out.idle = APPSTATE.missions.filter(m => m.idle).length;
  out.uncovered = APPSTATE.uncovered;

  // 5. the state machine, sampled across a full cycle for one hull of each class
  out.states = {};
  for (const id of Q.CLASS_ORDER) {
    const m = act.find(x => x.cls.id === id); if (!m) continue;
    const rows = [];
    for (let i = 0; i < 240; i++) {
      const st = Q.stateAt(m, m.cycleSec * i / 240);
      rows.push({ i, phase: st.phase, prog: R(st.prog, 5),
        lon: R(st.ll[0], 6), lat: R(st.ll[1], 6), bearing: R(st.bearing, 5),
        alt: R(st.alt, 3), water: R(st.water, 4), ln2: R(st.ln2, 4), gs: R(st.gs, 4),
        vert: R(st.vert, 5), massT: R(st.massT, 3), netN: R(st.netN, 0),
        draw: RO(st.draw, 4), gen: RO(st.gen, 4), sub: st.sub, cycleN: st.cycleN });
    }
    out.states[id] = { ship: m.name, fire: m.fire.id, rows };
  }

  // 6. the narrative, at one point per phase
  out.narrative = {};
  { const m = act.find(x => x.cls.id === 'P1000') || act[0];
    for (let i = 0; i < 6; i++) {
      const st = Q.stateAt(m, m.cycleSec * (i + 0.5) / 6);
      out.narrative[st.phase + '@' + R(st.prog, 2)] = Q.narrate(m, st);
    } }

  // 7. the built-in Q.selftest
  out.selftest = Q.selftest();
  return JSON.stringify(out);
})()
