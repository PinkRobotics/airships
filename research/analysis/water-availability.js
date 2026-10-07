/* Mapped shore proximity and generated drafting-station geometry are separate measures.
 * Dated points and final perimeters are geographic inputs only: no historical mission is
 * built or dispatched. Diagnostic rates at shore distances remain explicitly unsupported.
 * The source policy and station distances use the simulator's own generator. Planned legs
 * are recorded only for the separate invented exercise, when that view is loaded.
 * Regenerate with tools/js_eval.py, as in series/regen.sh; no network input is refreshed.
 */
(async () => {
  const S = window.AIRSHIPS.sim;
  const { CLASSES, CLASS_ORDER, MODES, findSource, sourceStations, planCycle, havKm, legKmFor, stationFor } = S;
  const {acceptedLogistics} = await import('./research/analysis/accepted-logistics.js');
  const water = window.AIRSHIPS.app.water;

  const doc = await (await fetch('data/fire-history-bc.json')).json();
  const fires = doc.fires;                       // [lon, lat, ha, year, verts, ring|null]

  // Beyond this a leg is not a mission on any class — a P-100 at 90 km/h spends 6.7 hours
  // round-tripping 300 km to deliver 100 t. It is the "no water" boundary, stated rather
  // than left as the class's own searchKm, which differs 24x across the three and would
  // make the three answers incomparable.
  const FAR_KM = 300;
  const THRESHOLDS = [10, 50, 100, 500, 1000, 5000];
  const PERIM_SAMPLES = 12;

  const pct = (n, d) => (d ? Number((100 * n / d).toFixed(2)) : null);
  const r = (x, n = 2) => (Number.isFinite(x) ? Number(x.toFixed(n)) : null);

  function quantiles(vals, weights) {
    // Weighted quantiles, used for both count (weight 1) and hectares (weight = size).
    if (!vals.length) return {};
    const idx = vals.map((v, i) => i).sort((a, b) => vals[a] - vals[b]);
    const tot = idx.reduce((s, i) => s + (weights ? weights[i] : 1), 0);
    const out = {};
    let acc = 0, k = 0;
    for (const q of [0.1, 0.25, 0.5, 0.75, 0.9]) {
      while (k < idx.length - 1 && acc + (weights ? weights[idx[k]] : 1) < q * tot) {
        acc += weights ? weights[idx[k]] : 1;
        k++;
      }
      out[`p${Math.round(q * 100)}`] = r(vals[idx[k]]);
    }
    return out;
  }

  // Keep the original closest mapped outline-vertex/centroid measure unchanged.
  // It is mapped shore proximity, not a drafting station or operational availability.
  function nearestAdequate(ll, minHa, maxKm) {
    let best = null, bestKm = Infinity;
    for (let i = 0; i < water.length; i++) {
      const w = water[i];
      if (w[2] < minHa) continue;
      const dLat = Math.abs(w[1] - ll[1]) * 111;
      if (dLat - (w.spanKm || 0) > maxKm) continue;
      let d;
      if (w[5] && w[5].length) {
        d = Infinity;
        for (const q of w[5]) { const dd = havKm(q, ll); if (dd < d) d = dd; }
      } else d = havKm([w[0], w[1]], ll);
      if (d > maxKm) continue;
      if (d < bestKm) { bestKm = d; best = i; }
    }
    return best === null ? null : { idx: best, km: bestKm };
  }

  // ONE PASS. For every fire and every adequacy threshold, the distance to the nearest body
  // that qualifies — and, for the big fires, the distance from the worst-served point on the
  // perimeter, because a 40,000 ha fire is not a point and the far edge is the honest number
  // for a campaign fire.
  const nearest = {};             // threshold -> [km|null per fire]
  const worstEdge = {};           // threshold -> [km|null per fire, only where a ring exists]
  for (const t of THRESHOLDS) { nearest[t] = []; worstEdge[t] = []; }

  for (const f of fires) {
    const ll = [f[0], f[1]];
    for (const t of THRESHOLDS) {
      const s = nearestAdequate(ll, t, FAR_KM);
      nearest[t].push(s ? s.km : null);
      if (!f[5] || !s) { worstEdge[t].push(null); continue; }
      const ring = f[5];
      const step = Math.max(1, Math.floor(ring.length / PERIM_SAMPLES));
      let worst = s.km, missed = false;
      for (let i = 0; i < ring.length; i += step) {
        const e = nearestAdequate(ring[i], t, FAR_KM);
        if (!e) { missed = true; break; }
        if (e.km > worst) worst = e.km;
      }
      worstEdge[t].push(missed ? null : worst);
    }
  }

  const totalHa = fires.reduce((a, f) => a + f[2], 0);

  const out = {
    generated: { by: 'research/analysis/water-availability.js', fireData: doc.generated },
    input: {
      fires: fires.length,
      totalHa: r(totalHa, 0),
      years: doc.counts ? `${Math.min(...Object.keys(doc.counts.years).map(Number))}-` +
             `${Math.max(...Object.keys(doc.counts.years).map(Number))}` : null,
      firesWithPerimeter: fires.filter(f => f[5]).length,
      waterBodies: water.length,
      farKm: FAR_KM,
      note: 'The legacy distance and threshold tables measure mapped shore proximity (outline vertices, centroid without an outline). Station geometry is separate; no historical dispatch is constructed.',
    },
    classes: {},
    thresholdSweep: {},
    geometry: {},
    crossCheck: {},
    stationGeometry: {},
  };

  for (const t of THRESHOLDS) {
    const km = [], ha = [];
    let miss = 0, missHa = 0;
    fires.forEach((f, i) => {
      const d = nearest[t][i];
      if (d === null) { miss++; missHa += f[2]; return; }
      km.push(d); ha.push(f[2]);
    });
    const we = worstEdge[t].filter(v => v !== null);
    out.thresholdSweep[t] = {
      qualifyingBodies: water.filter(w => w[2] >= t).length,
      firesServed: km.length,
      pctFiresServed: pct(km.length, fires.length),
      pctHaServed: pct(totalHa - missHa, totalHa),
      unservedFires: miss,
      byFire: quantiles(km),
      byHectare: quantiles(km, ha),
      worstPerimeterEdge: we.length ? quantiles(we) : null,
    };
  }

  // Six owned workers keep regeneration bounded; output order is input order.
  // Every worker imports the same selector as the pages, with no approximation.
  const jobs = CLASS_ORDER.flatMap(id => {
    const legs = fires.flatMap((f, i) => nearest[CLASSES[id].minSourceHa][i] === null ? [] :
      [{fire:i, ha:f[2], km:nearest[CLASSES[id].minSourceHa][i]}]);
    return Array.from({length:Math.ceil(legs.length/300)}, (_, i) =>
      ({class:id, legs:legs.slice(i*300,(i+1)*300)}));
  });
  const results = new Array(jobs.length);
  let next = 0;
  await Promise.all(Array.from({length:Math.min(6,jobs.length)}, async () => {
    const worker = new Worker('./research/analysis/logistics-worker.js', {type:'module'});
    try {
      while (next < jobs.length) {
        const index = next++;
        results[index] = await new Promise((resolve,reject) => {
          worker.onmessage = ({data}) => data.error ? reject(Error(data.error)) : resolve(data.rows);
          worker.onerror = event => reject(Error(event.message || 'logistics worker failed'));
          worker.postMessage(jobs[index]);
        });
      }
    } finally {worker.terminate();}
  }));
  const planRows = Object.fromEntries(CLASS_ORDER.map(id => [id,
    results.flatMap((rows,i) => jobs[i].class === id ? rows : [])]));

  for (const id of CLASS_ORDER) {
    const cls = CLASSES[id];
    const t = cls.minSourceHa;
    const sw = out.thresholdSweep[t];
    if (!sw) throw new Error(`no sweep for minSourceHa=${t} on ${id}`);

    const km = [], ha = [], accepted = [], byFire = [];
    let inSearch = 0, inSearchHa = 0, servedHa = 0;
    fires.forEach((f, i) => {
      const d = nearest[t][i];
      if (d === null) return;
      km.push(d); ha.push(f[2]); servedHa += f[2];
      const row = planRows[id][byFire.length];
      byFire.push(row);
      if (row.tph !== null) accepted.push(row);
      if (d <= cls.searchKm) { inSearch++; inSearchHa += f[2]; }
    });

    // Delivered tonnage is what a fleet is bought for, so the fleet-level rate is weighted by
    // how much land each fire actually burned, not by how many fires there were. The two
    // differ, and the count-weighted figure is the flattering one.
    const wSum = accepted.reduce((a, b) => a + b.ha, 0);
    const workedExample = acceptedLogistics(cls, 15);
    const medianByFire = acceptedLogistics(cls, sw.byFire.p50);
    const medianByHectare = acceptedLogistics(cls, sw.byHectare.p50);
    out.classes[id] = {
      minSourceHa: t,
      searchKm: cls.searchKm,
      servedWithinFarKm: { fires: km.length, pctFires: pct(km.length, fires.length),
                           pctHa: pct(servedHa, totalHa) },
      servedWithinClassSearchKm: { fires: inSearch, pctFires: pct(inSearch, fires.length),
                                   pctHa: pct(inSearchHa, totalHa) },
      distanceKm: { byFire: sw.byFire, byHectare: sw.byHectare },
      acceptedPlans: {workedExample, medianByFire, medianByHectare, byFire},
      logisticsService: {acceptedFires: accepted.length,
        notServedFires: fires.length - accepted.length,
        standDowns: byFire.filter(p => p.state === 'stand-down').length,
        unavailable: byFire.filter(p => p.state === 'unavailable').length,
        note: 'Means include accepted legs only; geometric water access is counted separately.'},
      throughputTph: {
        atWorkedExample15km: r(workedExample.tph, 1),
        atMedianByFire: r(medianByFire.tph, 1),
        atMedianByHectare: r(medianByHectare.tph, 1),
        meanOverFires: r(accepted.reduce((a, b) => a + b.tph, 0) / accepted.length, 1),
        meanOverHectares: r(accepted.reduce((s, v) => s + v.tph * v.ha, 0) / wSum, 1),
      },
    };
  }

  function nearestStation(ll, cls, maxKm) {
    let best = null;
    for (let i = 0; i < water.length; i++) {
      const w = water[i];
      if (w[2] < cls.minSourceHa) continue;
      if (Math.abs(w[1] - ll[1]) * 111 - (w.spanKm || 0) > maxKm) continue;
      const stations = sourceStations(w, ll, maxKm);
      if (!stations.length) continue;
      const km = Math.min(...stations.map(st => havKm(st, ll)));
      if (!best || km < best.km) best = { idx: i, km };
    }
    return best;
  }

  // Distances from dated points only. This loop never builds a fire mission.
  for (const id of CLASS_ORDER) {
    const cls = CLASSES[id], nearestKm = [], nearestHa = [], selectedKm = [], selectedHa = [];
    let sameBody = 0, kmMismatch = 0, modelFurther = 0, bothFound = 0, existenceGap = 0;
    let inSearch = 0, selected = 0, beyondRadius = 0;
    const detour = [], detourHa = [];
    for (const f of fires) {
      const ll = [f[0], f[1]], far = nearestStation(ll, cls, FAR_KM);
      if (far) { nearestKm.push(far.km); nearestHa.push(f[2]); }
      const near = far && far.km <= cls.searchKm ? far : null;
      if (near) inSearch++;
      const chosen = findSource(ll, cls, water);
      if (chosen) {
        selected++; selectedKm.push(chosen.km); selectedHa.push(f[2]);
        if (chosen.stations.some(st => havKm(st, ll) > cls.searchKm)) beyondRadius++;
      }
      if (!near || !chosen) { if (!!near !== !!chosen) existenceGap++; continue; }
      bothFound++;
      if (near.idx === chosen.idx) {
        sameBody++;
        if (Math.abs(near.km - chosen.km) > 1e-9) kmMismatch++;
      }
      if (chosen.km > near.km + 1e-9) modelFurther++;
      detour.push(chosen.km - near.km); detourHa.push(f[2]);
    }
    if (kmMismatch || existenceGap || beyondRadius) throw new Error('station qualification mismatch on ' + id);
    out.stationGeometry[id] = {
      nearestWithinFarKm: nearestKm.length,
      nearestWithinClassSearchKm: inSearch,
      pctWithinClassSearchKm: pct(inSearch, fires.length),
      nearestDistanceKm: { byFire: quantiles(nearestKm), byHectare: quantiles(nearestKm, nearestHa) },
      selectedSources: selected, noSelectedSource: fires.length - selected,
      selectedStationKm: { byFire: quantiles(selectedKm), byHectare: quantiles(selectedKm, selectedHa) },
      selectionsOfferingOutOfRadiusStation: beyondRadius,
    };
    out.crossCheck[id] = {
      metric: 'nearest generated station versus size-weighted station selection, within the class radius',
      bothFound, sameBodyChosen: sameBody, kmMismatchWhenSameBody: kmMismatch, existenceGap,
      modelFlewFurtherThanNearest: modelFurther, pctModelFlewFurther: pct(modelFurther, bothFound),
      detourKm: quantiles(detour), detourKmByHectare: quantiles(detour, detourHa),
    };
  }

  // Actual planned legs belong to the invented exercise alone. Every row names a model
  // mission, and is geometric planning evidence, never historical-fire or flight evidence.
  const exercise = window.AIRSHIPS.app;
  out.plannedExercise = { note: 'Invented exercise only; no aircraft flew. Empty unless this generator runs on the exercise view.', rows: [] };
  if (exercise.exercise) {
    out.plannedExercise.rows = exercise.missions.filter(m => m.water && m.cls).map(m => {
      const n = Math.max(1, m.order?.length || m.targets.length);
      return { hull: m.name, incident: m.fire.id, class: m.cls.id, source: m.water[4],
        nearestStationKm: r(Math.min(...m.stations.map(st => havKm(m.fire.ll, st)))),
        cycleStationKm: quantiles(Array.from({length:n}, (_,i) => havKm(m.fire.ll, stationFor(m,i+1)))),
        meanPlannedLegKm: r(legKmFor(m)), state: m.planState };
    });
    out.plannedExercise.meanLegKm = quantiles(out.plannedExercise.rows.map(m => m.meanPlannedLegKm));
  }

  // What the ship's own dimensions demand of a water body, as opposed to what config.js
  // asserts. A hull holding station over open water needs a disc it fits inside; the anchor
  // bag needs enough water under it to submerge in. The first is derivable and the shipped
  // threshold turns out to be far more conservative than it. The second is NOT derivable
  // from this dataset at all, because the Freshwater Atlas carries area and not depth.
  for (const id of CLASS_ORDER) {
    const cls = CLASSES[id];
    const hullDiscHa = Math.PI * Math.pow(cls.lenM / 2, 2) / 10000;
    // A collapsible bucket fills as roughly a cylinder as deep as it is wide; that is the
    // shape a Bambi bucket takes and the least depth-hungry credible one.
    const bagD = Math.cbrt(4 * cls.anchorBagT / Math.PI);
    const drawTph = out.classes[id].acceptedPlans.workedExample.tph;
    const minBodyM3 = cls.minSourceHa * 10000 * 1.0;      // 1 m of drawdown, as a yardstick
    out.geometry[id] = {
      hullLenM: cls.lenM,
      hullStationDiscHa: r(hullDiscHa),
      configMinSourceHa: cls.minSourceHa,
      conservatismVsHullDisc: r(cls.minSourceHa / hullDiscHa),
      anchorBagT: cls.anchorBagT,
      anchorBagDiameterM: r(bagD),
      depthToSubmergeBagM: r(bagD * 1.5),        // submerge it, and keep it off the bottom
      drawTonnesPer12h: drawTph === null ? null : r(drawTph * 12, 0),
      drawdownMetresPer12hOnMinBody: drawTph === null ? null : r(drawTph * 12 / minBodyM3, 4),
      qualifyingBodiesInBC: water.filter(w => w[2] >= cls.minSourceHa).length,
    };
  }

  return out;
})()
