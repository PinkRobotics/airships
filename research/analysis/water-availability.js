/* OPEN-QUESTIONS #13: how often does the mission actually exist?
 *
 * The concept is a shuttle between a fire and a lake, and until now no figure anywhere in this
 * project said what fraction of real fires have a lake worth shuttling to. The monitor answers
 * it for whatever is burning today. Twenty seasons is the only version of the question that
 * bounds a market.
 *
 * Run through tools/js_eval.py against the live page, so every throughput is computed by the
 * model's own planCycle and every distance is checked against its own sim/water.js. This
 * project has been bitten enough times by a second copy of a calculation, and an analysis
 * that disagreed with the simulator would be worse than useless.
 *
 *   make water-availability
 *
 * Two structural notes, both of which are also findings.
 *
 * `findSource(ll, cls, water, minHa, maxKm)` reads `cls` for NOTHING except the defaults of
 * those last two arguments. Override both and the class is inert. So the sweep below is
 * indexed by adequacy threshold, not by class, and the three classes are mapped onto it
 * afterwards: the first draft of this file computed every number three times and got three
 * identical answers.
 *
 * And `findSource` does not return the nearest source — see nearestAdequate() below.
 */
(async () => {
  const S = window.AIRSHIPS.sim;
  const { CLASSES, CLASS_ORDER, MODES, findSource, planCycle, havKm } = S;
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

  /* NEAREST IS NOT WHAT findSource RETURNS, and finding that out is half of this analysis.
   *
   * `findSource` scores candidates as `d / min(12, (area/minHa)^0.35)` — it deliberately
   * flies past a qualifying pond to reach a lake, which is the right operational behaviour
   * and the wrong measurement for "how far is the water". Worse, the trade depends on the
   * search radius: widen it and a bigger, further body can win, so the same fire gets a
   * different answer at 25 km and at 300 km. The first draft of this file cross-checked the
   * two against each other and found 27 disagreements, which is exactly what that is.
   *
   * So the two questions are computed separately. This function answers "where is the
   * nearest water that qualifies" by pure distance. It mirrors sim/water.js's distance rule
   * exactly — closest approach to the simplified outline where one exists, centroid
   * otherwise — and the cross-check below proves it, by requiring the two to agree to
   * floating point whenever they pick the SAME body.
   */
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
      note: 'Distance is to the closest approach of the water body, not its centroid.',
    },
    classes: {},
    thresholdSweep: {},
    geometry: {},
    crossCheck: {},
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

  for (const id of CLASS_ORDER) {
    const cls = CLASSES[id];
    const t = cls.minSourceHa;
    const sw = out.thresholdSweep[t];
    if (!sw) throw new Error(`no sweep for minSourceHa=${t} on ${id}`);

    const km = [], ha = [], tph = [];
    let inSearch = 0, inSearchHa = 0, servedHa = 0;
    fires.forEach((f, i) => {
      const d = nearest[t][i];
      if (d === null) return;
      km.push(d); ha.push(f[2]); servedHa += f[2];
      tph.push(planCycle(cls, MODES.balanced, d).tph);
      if (d <= cls.searchKm) { inSearch++; inSearchHa += f[2]; }
    });

    // Delivered tonnage is what a fleet is bought for, so the fleet-level rate is weighted by
    // how much land each fire actually burned, not by how many fires there were. The two
    // differ, and the count-weighted figure is the flattering one.
    const wSum = ha.reduce((a, b) => a + b, 0);
    out.classes[id] = {
      minSourceHa: t,
      searchKm: cls.searchKm,
      servedWithinFarKm: { fires: km.length, pctFires: pct(km.length, fires.length),
                           pctHa: pct(servedHa, totalHa) },
      servedWithinClassSearchKm: { fires: inSearch, pctFires: pct(inSearch, fires.length),
                                   pctHa: pct(inSearchHa, totalHa) },
      distanceKm: { byFire: sw.byFire, byHectare: sw.byHectare },
      throughputTph: {
        atWorkedExample15km: r(planCycle(cls, MODES.balanced, 15).tph, 1),
        atMedianByFire: r(planCycle(cls, MODES.balanced, sw.byFire.p50).tph, 1),
        atMedianByHectare: r(planCycle(cls, MODES.balanced, sw.byHectare.p50).tph, 1),
        meanOverFires: r(tph.reduce((a, b) => a + b, 0) / tph.length, 1),
        meanOverHectares: r(tph.reduce((s, v, i) => s + v * ha[i], 0) / wSum, 1),
      },
    };
  }

  /* Two things at once.
   *
   * THE PROOF that nearestAdequate() computes the same distance the model does: run both at
   * the class's own settings, and wherever they choose the SAME body require the kilometres
   * to agree to floating point. Selection may differ; arithmetic may not.
   *
   * THE FINDING: how much further the model's size preference flies than the nearest
   * qualifying water. That detour is a deliberate operational choice — a fleet drawing a
   * full payload every few minutes should not be working a pond — and nobody has priced it.
   */
  for (const id of CLASS_ORDER) {
    const cls = CLASSES[id];
    let sameBody = 0, kmMismatch = 0, modelFurther = 0, bothFound = 0, existenceGap = 0;
    const detour = [], detourHa = [];
    fires.forEach((f) => {
      const ll = [f[0], f[1]];
      const near = nearestAdequate(ll, cls.minSourceHa, cls.searchKm);
      const chosen = findSource(ll, cls, water);
      if (!near || !chosen) { if (!!near !== !!chosen) existenceGap++; return; }
      bothFound++;
      if (near.idx === chosen.idx) {
        sameBody++;
        if (Math.abs(near.km - chosen.km) > 1e-9) kmMismatch++;
      }
      if (chosen.km > near.km + 1e-9) modelFurther++;
      detour.push(chosen.km - near.km);
      detourHa.push(f[2]);
    });
    out.crossCheck[id] = {
      bothFound,
      sameBodyChosen: sameBody,
      kmMismatchWhenSameBody: kmMismatch,          // must be 0
      existenceGap,                                 // must be 0
      modelFlewFurtherThanNearest: modelFurther,
      pctModelFlewFurther: pct(modelFurther, bothFound),
      detourKm: quantiles(detour),
      detourKmByHectare: quantiles(detour, detourHa),
    };
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
    const drawTph = planCycle(cls, MODES.balanced, 15).tph;
    const minBodyM3 = cls.minSourceHa * 10000 * 1.0;      // 1 m of drawdown, as a yardstick
    out.geometry[id] = {
      hullLenM: cls.lenM,
      hullStationDiscHa: r(hullDiscHa),
      configMinSourceHa: cls.minSourceHa,
      conservatismVsHullDisc: r(cls.minSourceHa / hullDiscHa),
      anchorBagT: cls.anchorBagT,
      anchorBagDiameterM: r(bagD),
      depthToSubmergeBagM: r(bagD * 1.5),        // submerge it, and keep it off the bottom
      drawTonnesPer12h: r(drawTph * 12, 0),
      drawdownMetresPer12hOnMinBody: r(drawTph * 12 / minBodyM3, 4),
      qualifyingBodiesInBC: water.filter(w => w[2] >= cls.minSourceHa).length,
    };
  }

  return out;
})()
