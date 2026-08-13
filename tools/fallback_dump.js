/* Everything the static fallback block quotes, read out of the running page itself.
 *
 * The block baked into index.html between the FALLBACK markers is what a crawler or a
 * no-script visitor gets instead of "loading…". Its numbers must not be typed by hand:
 * they come from this dump, taken from the page running the bundled snapshot replay
 * (`?seed=7&data=snapshot` — the same pinned run the golden tests compare). Everything
 * read here is settled at rebuildMissions() and is deterministic under that URL; nothing
 * time-dependent (phases, clocks, ages) may be added, or `gen_fallback.py --check`
 * stops being reproducible.
 */
(() => {
  const A = window.AIRSHIPS, S = A.app, SIM = A.sim;
  const { CLASSES, CLASS_ORDER, HULL_NAMES, REFERENCE_CLASS, srcName } = SIM;
  const r = (x, n) => (Number.isFinite(x) ? Number(x.toFixed(n)) : null);
  const fname = f => f.name || f.geo || f.id;
  const needsShip = f => f.status === "Out of Control" || f.status === "Fire of Note";

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
      tph: f.mission && !f.mission.idle ? Math.round(f.mission.plan.tph) : null,
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
    deliveredT: Math.round(pick.plan.deliveredT), tph: Math.round(pick.plan.tph),
  };

  return {
    generated: { by: 'tools/fallback_dump.js via tools/gen_fallback.py',
                 inputs: 'data/snapshot.json replayed at seed=7' },
    snapshotAt: S.snapshotDate,
    tier: S.tier,
    fires: {
      active: S.fires.length,
      outOfControl: S.fires.filter(f => f.status === "Out of Control").length,
      ofNote: S.fires.filter(f => f.note).length,
      needingShip: S.fires.filter(needsShip).length,
    },
    flying: S.missions.filter(m => !m.idle).length,
    fleet, roster, topFires, example,
  };
})()
