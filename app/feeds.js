/* The live data: what the page asks for, how it falls back, and how it becomes model input.
 *
 * Three tiers, in order: this site's own mirror of the public feeds (pipeline/live.py),
 * then the public feeds directly, then the dated snapshot committed to this repository.
 * The mirror exists so that traffic to this page does not become traffic to an emergency
 * service. Whichever tier answers is named on the page — the status line never implies
 * live data it does not have.
 */
import { dropSeg, havKm, insideFire, planTargets } from '../sim/index.js';
import { renderDrawer } from './cockpit/panels.js';
import { replanAll } from './fleet.js';
import { renderStatus } from './main.js';
import { FIRES_URL, PERIMS_URL, cachedJSON, fetchJSON, mirrorJSON } from './net.js';
import { S } from './store.js';

/* REPLAY MODE. `?data=snapshot` pins every external input to the dataset bundled with the
 * repository: the fires, their perimeters, the satellite heat, and the wind (still air, and
 * labelled as such — a wind forecast cannot be replayed honestly from a file, so replay mode
 * declines to pretend). With `?seed=` pinning the plan jitter, a run is fully determined.
 *
 * That buys three things: golden-output tests that compare numbers rather than screenshots,
 * a link that shows another person exactly what you were looking at, and a page that works
 * with no network at all. */
export const REPLAY = typeof location !== "undefined" &&
  new URLSearchParams(location.search).get("data") === "snapshot";

export function normalize(firesGJ, perimsGJ) {
  const rings = {};
  for (const f of (perimsGJ && perimsGJ.features) || []) {
    const num = f.properties.FIRE_NUMBER;
    const g = f.geometry; if (!g || !num) continue;
    const polys = g.type === "MultiPolygon" ? g.coordinates : [g.coordinates];
    let best = null, ba = -1;
    for (const p of polys) {
      const r = p[0];
      let a = 0;
      for (let i = 0; i < r.length - 1; i++) a += r[i][0] * r[i + 1][1] - r[i + 1][0] * r[i][1];
      a = Math.abs(a);
      if (a > ba) { ba = a; best = r; }
    }
    if (best) {
      const step = Math.max(1, Math.floor(best.length / 240));
      rings[num] = best.filter((_, i) => i % step === 0);
      if (!rings[num].allRings) rings[num].allRings = polys.map(p => {
        const r = p[0]; const st = Math.max(1, Math.floor(r.length / 160));
        return r.filter((_, i) => i % st === 0);
      });
    }
  }
  const fires = [];
  for (const f of (firesGJ && firesGJ.features) || []) {
    const p = f.properties, g = f.geometry;
    if (!g || p.FIRE_STATUS === "Out") continue;
    fires.push({
      id: p.FIRE_NUMBER || String(p.OBJECTID),
      name: p.INCIDENT_NAME && p.INCIDENT_NAME !== p.FIRE_NUMBER ? p.INCIDENT_NAME : null,
      geo: p.GEOGRAPHIC_DESCRIPTION || null,
      status: p.FIRE_STATUS, cause: p.FIRE_CAUSE || null,
      sizeHa: p.CURRENT_SIZE || 0,
      ignited: p.IGNITION_DATE ? new Date(p.IGNITION_DATE) : null,
      url: p.FIRE_URL || null,
      note: p.FIRE_STATUS === "Fire of Note" || p.FIRE_OF_NOTE_IND === "Y" || p.FIRE_OF_NOTE_IND === "Yes",
      ll: [g.coordinates[0], g.coordinates[1]],
      ring: rings[p.FIRE_NUMBER] || null,
    });
  }
  fires.sort((a, b) => b.sizeHa - a.sizeHa);
  return fires;
}

export async function loadLive() {
  if (REPLAY) {
    const snap = await fetchJSON("data/snapshot.json", 20000);
    S.usingFallback = true; S.fetchedAt = new Date(snap.retrievedAt || Date.now());
    S.snapshotDate = snap.retrievedAt;
    return normalize(snap.fires, snap.perimeters);
  }
  try {
    // Mirror first (45 min covers a few missed refreshes); direct feed only as fallback,
    // still behind the courtesy localStorage cache.
    let fr, pr = null;
    try {
      fr = await mirrorJSON("fires", 45);
      try { pr = await mirrorJSON("perims", 90); } catch (e) { /* fires alone still draw */ }
    } catch (e) {
      fr = await cachedJSON("fires", FIRES_URL, 300000, 15000);
      try { pr = await cachedJSON("perims", PERIMS_URL, 900000, 15000); } catch (e2) {}
    }
    if (!fr.data || !fr.data.features || !fr.data.features.length) throw new Error("empty feed");
    S.usingFallback = false;
    S.fetchedAt = new Date(Date.now() - fr.age);
    return normalize(fr.data, pr && pr.data);
  } catch (e) {
    const snap = await fetchJSON("data/snapshot.json", 20000);
    S.usingFallback = true; S.fetchedAt = new Date(); S.snapshotDate = snap.retrievedAt;
    return normalize(snap.fires, snap.perimeters);
  }
}

export function needsShip(f) {
  // The demonstration responds only to fires that are actually out of control (fires of
  // note included — they are the marquee incidents). Held and under-control fires stay on
  // the map as monitored-only: crews have them; the imagined fleet does not pile on.
  return f.status === "Out of Control" || f.status === "Fire of Note";
}

export async function fetchWind() {
  if (REPLAY) { S.windOk = false; renderStatus(); return; }   // still air, stated on the page
  const act = S.missions.filter(m => !m.idle);
  if (!act.length) return;
  try {
    const lats = act.map(m => ((m.intake[1] + m.delivery[1]) / 2).toFixed(3)).join(",");
    const lons = act.map(m => ((m.intake[0] + m.delivery[0]) / 2).toFixed(3)).join(",");
    // hourly product: a 20-minute cache is already generous
    const wr = await cachedJSON("wind:" + act.length + ":" + lats.slice(0, 24),
      "https://api.open-meteo.com/v1/forecast?latitude=" + lats +
      "&longitude=" + lons + "&hourly=wind_speed_850hPa,wind_direction_850hPa" +
      "&forecast_hours=1&wind_speed_unit=kmh&timezone=UTC", 1200000, 15000);
    let d = wr.data;
    if (!Array.isArray(d)) d = [d];
    act.forEach((m, i) => {
      const hh = d[i] && d[i].hourly;
      if (hh && hh.wind_speed_850hPa && hh.wind_speed_850hPa[0] != null)
        m.wind = { spd: hh.wind_speed_850hPa[0], dir: hh.wind_direction_850hPa[0], bearing: m.bearing };
    });
    S.windOk = true; S.windAt = new Date();
  } catch (e) { S.windOk = false; }
  // S.heat must be passed: planTargets scores candidate lines partly on how hot the
  // satellite detections along them are, and it takes that data as an argument so the
  // model can run with no feed. Omitting it silently reverts to geometry-only scoring.
  for (const mm of S.missions) if (!mm.idle) planTargets(mm, S.heat);
  replanAll(); renderStatus();
}

export async function fetchHeat() {
  // The same CWFIS detections the heat overlay draws, as readable points: when a fire has
  // them, its drop lines aim at the hottest well-separated detections instead of geometry.
  if (REPLAY) {
    try {
      const snap = await fetchJSON("data/snapshot-heat.json", 20000);
      S.heat = (snap.features || []).map(f => ({ ll: f.geometry.coordinates, temp: f.properties.temp || 0 }));
    } catch (e) { S.heat = []; }
    applyHeat();
    return;
  }
  try {
    // Mirror first; the direct CWFIS query (attribute filter, not a geometry BBOX — the
    // layer's native-CRS envelope over-selects) only as fallback behind its 30-min cache.
    let hr;
    try { hr = await mirrorJSON("heat", 90, 25000); }
    catch (e) {
      hr = await cachedJSON("heat",
        "https://cwfis.cfs.nrcan.gc.ca/geoserver/public/wfs?service=WFS&version=2.0.0&request=GetFeature" +
        "&typeNames=public%3Ahotspots_last24hrs&outputFormat=application%2Fjson&srsName=EPSG:4326" +
        "&CQL_FILTER=lat%20BETWEEN%2047.5%20AND%2060.6%20AND%20lon%20BETWEEN%20-140%20AND%20-113.3" +
        "&sortBy=temp%20D&count=6000&propertyName=geometry,temp", 1800000, 25000);
    }
    S.heat = (hr.data.features || []).map(f => ({ ll: f.geometry.coordinates, temp: f.properties.temp || 0 }));
  } catch (e) { S.heat = []; }
  applyHeat();
}

export function applyHeat() {
  if (!S.heat || !S.heat.length) return;
  for (const m of S.missions) {
    if (m.idle) continue;
    const f = m.fire;
    const radKm = Math.sqrt(Math.max(f.sizeHa, 10) * 1e4 / Math.PI) / 1000 + 3;
    const cand = [];
    for (const h of S.heat) {
      if (Math.abs(h.ll[1] - f.ll[1]) * 111 > radKm) continue;
      if (havKm(h.ll, f.ll) > radKm) continue;
      if (insideFire(f, h.ll) || havKm(h.ll, f.ll) < radKm * 0.6) cand.push(h);
    }
    if (!cand.length) continue;
    cand.sort((a, b) => b.temp - a.temp);
    const sepKm = Math.max(0.3, m.cls.dropKm * 0.45);
    const picks = [];
    for (const h of cand) {
      if (picks.every(q => havKm(q, h.ll) > sepKm)) picks.push(h.ll.slice());
      if (picks.length >= 8) break;
    }
    if (picks.length >= 1) {
      m.targets = picks;
      m.segs = picks.map(t => dropSeg(m, t, true));
      m.heat = true;
      planTargets(m, S.heat);
    }
  }
  renderDrawer();
}
