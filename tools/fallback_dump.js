/* Static reference scene: the invented exercise, with its own deterministic seed.
 * Only settled allocation output belongs here, never wall-clock phase or feed age. */
(() => {
  const A = window.AIRSHIPS, S = A.app, SIM = A.sim;
  const { CLASSES, CLASS_ORDER, HULL_NAMES, REFERENCE_CLASS, srcName, missionReady, auditServedPlan } = SIM;
  if (S.planning?.state !== 'settled') throw new Error('fallback cycle figures unavailable: planning has not settled');
  for(const m of S.missions) if(missionReady(m)) auditServedPlan(m.cls,m.legKm,m.wind,m.selection,m.mode.id);
  const r = (x, n) => (Number.isFinite(x) ? Number(x.toFixed(n)) : null);
  const fname = f => f.name || f.geo || f.id;
  // The page's own rule (app/feeds.js), guard first: a fire the guard holds is never a
  // candidate for the fleet, so it never reaches the top-fires table this dump feeds.
  const needsShip = f => !f.guarded && f.status === "Out of Control";

  // The fixed demonstration fleet, from the model's own constants.
  const fleet = CLASS_ORDER.map(id => ({
    id, name: CLASSES[id].name, count: HULL_NAMES[id].length,
    payloadT: CLASSES[id].payloadT, lenM: CLASSES[id].lenM, diaM: CLASSES[id].diaM,
  }));

  // The roster exactly as the snapshot allocation left it: hull, class, fire, rate —
  // grouped in the missions array's own order, which is renderRoster's order (the
  // allocator builds the fleet biggest class first).
  const rosterOrder = [];
  for (const m of S.missions)
    if (m.cls && !rosterOrder.includes(m.cls.id)) rosterOrder.push(m.cls.id);
  const roster = rosterOrder.map(id => ({
    cls: CLASSES[id].name, count: HULL_NAMES[id].length,
    ships: S.missions.filter(m => m.cls && m.cls.id === id).map(m => ({
      hull: m.name || null,
      fire: m.idle ? null : fname(m.fire),
      tph: m.idle ? null : Math.round(m.plan.tph),
    })),
  }));

  // The top-fires panel's own selection rule: largest fires needing a hull, first eight.
  const topFires = S.fires.filter(needsShip).slice()
    .sort((a, b) => b.sizeHa - a.sizeHa).slice(0, 8).map(f => ({
      name: fname(f), id: f.id, sizeHa: Math.round(f.sizeHa), status: f.status,
      hull: f.mission && !f.mission.idle ? f.mission.name : null,
      tph: S.missions.some(m=>m.fire===f&&missionReady(m)) ? Math.round(S.missions.filter(m=>m.fire===f&&missionReady(m)).reduce((n,m)=>n+m.plan.tph,0)) : null,
    }));

  // boot()'s own opening pick, reproduced: a REFERENCE_CLASS ship on the largest fire
  // that class was given, ties on fire number; any flying ship if no P-100 flies.
  const larger = (m, best) => !best || m.fire.sizeHa > best.fire.sizeHa ||
    (m.fire.sizeHa === best.fire.sizeHa && m.fire.id < best.fire.id);
  let pick = null, anyShip = null;
  for (const m of S.missions) {
    if (m.idle) continue;
    if (larger(m, anyShip)) anyShip = m;
    if (m.cls.id === REFERENCE_CLASS && larger(m, pick)) pick = m;
  }
  pick = pick || anyShip;
  const example = pick && {
    hull: pick.name, cls: pick.cls.name,
    fire: fname(pick.fire), fireId: pick.fire.id,
    fireHa: Math.round(pick.fire.sizeHa), fireStatus: pick.fire.status,
    source: srcName(pick), sourceHa: Math.round(pick.water[2]),
    legKm: r(pick.legKm, 1), cycleMin: Math.round(pick.plan.cycleMin),
    mode: pick.mode.label.toLowerCase(), requestedT: pick.cls.payloadT, keptT: Math.round(pick.plan.retainedT),
    releasedT: Math.round(pick.plan.deliveredT), tph: Math.round(pick.plan.tph),
  };

  return {
    generated: { by: 'tools/fallback_dump.js via tools/gen_fallback.py',
                 inputs: 'data/exercise/exercise.json; invented fires; seed from the file' },
    day: S.day,                     // the day the view shows (America/Vancouver)
    snapshotAt: S.snapshotDate,     // when that day's files were captured (UTC)
    tier: S.tier,
    // The page's own sentences, in the ruling's fixed words (R7), read from the DOM so the
    // static block and the running page can never disagree about what day this is.
    mode: (document.getElementById('modeNote') || {}).textContent || '',
    guard: (document.getElementById('guardNote') || {}).textContent || '',
    fires: {
      active: S.fires.length,
      outOfControl: S.fires.filter(f => f.status === "Out of Control").length,
      ofNote: S.fires.filter(f => f.note).length,
      needingShip: S.fires.filter(needsShip).length,
      guarded: S.fires.filter(f => f.guarded).length,
    },
    uncovered: S.uncovered,
    flying: S.missions.filter(m => !m.idle).length,
    fleet, roster, topFires, example,
  };
})()
