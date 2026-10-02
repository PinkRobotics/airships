/* The data this page shows: which view it is, what it asks for, how it falls back, and how
 * the feeds become model input.
 *
 * A VIEW IS ONE OF THREE KINDS, and the guard decides which (data/season/2026.guard.json,
 * read through sim/guard.js — the ruling is data, not code):
 *
 *   a dated day   ?day=YYYY-MM-DD — one of the status days in data/season/, loaded through
 *                 the same code path as live data. A day inside a no-fleet window is shown
 *                 as the record alone: the fires and their outlines as published, nothing
 *                 of the fleet. Any other dated day is a fleet day.
 *   the sample    ?data=snapshot, and the live mirror's failure fallback: the latest fleet
 *                 day in the repository, read from the same season day files — there is no
 *                 second copy of the data, and 8 August 2026 is not reachable with a fleet
 *                 by any route.
 *   live          this site's own mirror of the public feeds (pipeline/live.py), when it is
 *                 fresh. Live is a fleet view unless today, in Vancouver, is inside a
 *                 no-fleet window.
 *
 * The mirror exists so that traffic to this page does not become traffic to an emergency
 * service. Whichever tier answered is named on the page — the status line never implies
 * live data it does not have, and it names the day and the mode in words on every view.
 */
import { dropSeg, dayKind, guardedFire, havKm, insideFire, loadGuard, noteKm, planTargets, pointBlocked } from '../sim/index.js?v=26282d19';
import { renderDrawer } from './cockpit/panels.js?v=26282d19';
import { vancouverClock, vancouverDate } from './dates.js?v=26282d19';
import { replanAll } from './fleet.js?v=26282d19';
import { renderStatus } from './main.js?v=26282d19';
import { fetchJSON, mirrorJSON } from './net.js?v=26282d19';
import { S } from './store.js?v=26282d19';
import { windForMission, readWind, WIND_MAX_AGE_MS } from './wind.js?v=26282d19';

/* REPLAY MODE. `?data=snapshot` pins every external input to a dated copy bundled with the
 * repository — now the latest fleet day in data/season/, with its fires and perimeters and
 * nothing else: no wind (a forecast cannot be replayed honestly from a file, so replay mode
 * declines to pretend) and no satellite heat (a live layer, not part of a status day). With
 * `?seed=` pinning the plan jitter, a run is fully determined.
 *
 * That buys three things: golden-output tests that compare numbers rather than screenshots,
 * a link that shows another person exactly what you were looking at, and a page that works
 * with no network at all. A ?day= parameter wins over it: a link that names a day is asking
 * for that day, not for the sample. */
const QP = new URLSearchParams(location.search);
export const DAY = QP.get("day");
export const REPLAY = QP.get("data") === "snapshot" && !DAY;

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

/* Which tier is on screen. loadLive sets it, and the status line in main.js says it out
 * loud; nothing else may write it. It is not declared in store.js because this module is
 * the only thing that knows the answer.
 *
 *   "replay"    ?data=snapshot — the visitor asked for the bundled sample (a fleet day)
 *   "day"       ?day=YYYY-MM-DD — a dated status day, record-only or fleet as the guard says
 *   "mirror"    this site's server-side copy of the public feeds
 *   "snapshot"  the bundled sample; the mirror failed
 *   "none"      nothing answered and there is nothing to show
 *
 * A refresh that fails with a good picture already on screen changes none of this: the tier
 * and the fetch time stay as they were, because they describe the data the visitor is
 * looking at, and the growing age is what tells them the page has stopped updating.
 *
 * S.dataNote carries the reason in words — "mirror is 63 min old, past its 45 min gate",
 * "timed out after 15 s" — so a visitor who wonders why is not left guessing, and so the
 * two failures that look identical from outside (a feed that hangs and a feed that returns
 * nothing) read differently on the page. S.perimsOk says whether the outlines came with the
 * points, because a live tier can answer with one and not the other. */

/* One short phrase for one failure, for the status line. */
function why(e) {
  return (e && e.message) || "unknown error";
}

/* A feed that parses but carries no fires is a failure of the SOURCE, not of the transport,
 * and the next tier may well have the fires. BC has active fires every day of the season;
 * an empty collection in August is a broken publisher, not a quiet province. It is treated
 * as unusable rather than shown as "0 fires" — but only after every tier has been asked. */
function usable(gj) {
  return !!(gj && Array.isArray(gj.features) && gj.features.length);
}

/* ---------- the season record and the guard -------------------------------------------------- */

/* The season index, the season record and the guard file, read once per view. Everything
 * else in this module waits on them: which fires the fleet may work, and whether it flies
 * at all, are the guard's call — and a guard that cannot be read stands the fleet down
 * (R6) rather than being skipped.
 *
 * A failure here is not a blank page: the words go into S.seasonNote and the view degrades
 * to whatever it can still load honestly. The season record's numbers are handed to
 * loadGuard only when the record actually loaded, so a missing season file degrades the
 * hindsight checks without taking the guard itself down. */
let seasonOnce = null;
export function loadSeason() {
  if (seasonOnce) return seasonOnce;
  seasonOnce = (async () => {
    const fail = [];
    let daysIdx = null, guardDoc = null, seasonDoc = null;
    try { daysIdx = await fetchJSON("data/season/2026.days.json", 20000); }
    catch (e) { fail.push("season index: " + why(e)); }
    try { guardDoc = await fetchJSON("data/season/2026.guard.json", 20000); }
    catch (e) { fail.push("guard file: " + why(e)); }
    try { seasonDoc = await fetchJSON("data/season/2026.json", 30000); }
    catch (e) { fail.push("season record: " + why(e)); }
    const seasonNumbers = new Set(), seasonOfNote = new Set();
    if (seasonDoc && Array.isArray(seasonDoc.fires))
      for (const f of seasonDoc.fires) {
        if (typeof f.fire !== "string") continue;
        seasonNumbers.add(f.fire);
        if (f.fireOfNote || f.wasFireOfNote) seasonOfNote.add(f.fire);
      }
    S.seasonNumbers = seasonNumbers;
    S.seasonOfNote = seasonOfNote;
    S.dayList = daysIdx && Array.isArray(daysIdx.days)
      ? daysIdx.days.filter(d => d && typeof d.date === "string" && d.fires && d.fires.file && d.perims && d.perims.file)
      : [];
    // loadGuard never throws: a malformed or missing file becomes {ok:false, reason} in
    // words, and every caller below reads that as "the fleet stands down".
    S.guard = loadGuard(guardDoc, seasonDoc ? { seasonNumbers, seasonOfNote } : {});
    S.seasonNote = fail.length ? fail.join("; ") : null;
  })();
  return seasonOnce;
}

/* R3 on one line: mark every guarded fire in view. f.guarded is the reason object exactly
 * when the fleet may never work that fire; needsShip, the map, the tables and the cockpit
 * all read it, so the reason shown is the reason enforced. */
export function applyGuard(fires) {
  for (const f of fires) f.guarded = guardedFire(S.guard, f, { seasonOfNote: S.seasonOfNote });
  return fires;
}

/* Is this date inside a no-fleet window? (dayKind answers the same question with the
 * reason attached; this is the boolean for choosing which sentence the page says.) */
function inWindow(G, date) {
  return !!(G && G.ok && (G.noFleet || []).some(w => date >= w.from && date <= w.to));
}

/* The newest dated day the guard allows a fleet on. ?data=snapshot and the mirror's
 * failure fallback both resolve to this, so the bundled sample is always a fleet day and
 * the old 8 August snapshot is never shown with a fleet. Null when no day qualifies — a
 * guard that failed to load says no to every date. */
export function latestFleetDay() {
  const days = S.dayList.map(d => d.date).slice().sort();
  for (let i = days.length - 1; i >= 0; i--)
    if (dayKind(S.guard, days[i]).fleet) return days[i];
  return null;
}

/* Set the view's mode once its date is known. Everything downstream — the fleet, the map,
 * the panels — reads S.recordOnly. A forcedWhy (R6: the guard file unreadable, the day's
 * own files failed, nothing could be read) stands the fleet down whatever the calendar
 * says, and the reason in words is owed to the visitor. */
function setView(date, forcedWhy) {
  S.day = typeof date === "string" ? date : vancouverDate(Date.now());
  const k = dayKind(S.guard, S.day);
  S.recordOnly = !k.fleet || !!forcedWhy;
  S.recordWindow = !forcedWhy && inWindow(S.guard, S.day);
  S.standDown = S.recordOnly ? (forcedWhy || k.reason) : null;
}

/* One day's files, checked against the season index before they are trusted (R6: a day
 * file that fails its own checks stands the fleet down, never "fly anyway"). The index
 * pins each file's sha256, byte count and fetchedAt; the page compares the fetchedAt and
 * the feature count always, and the digest too wherever crypto.subtle exists — which is
 * every context this page is normally read in (https, localhost). */
async function fetchDayFile(rel, pin) {
  const url = "data/season/" + rel;
  const ctl = new AbortController();
  const t = setTimeout(() => ctl.abort(), 20000);
  let text = "";
  try {
    const r = await fetch(url, { signal: ctl.signal });
    if (!r.ok) throw new Error("HTTP " + r.status);
    text = await r.text();
  } catch (e) {
    throw new Error(rel + " did not answer (" + ((e && e.message) || e) + ")");
  } finally { clearTimeout(t); }
  let doc = null;
  try { doc = JSON.parse(text); } catch (e) { /* checked below */ }
  if (!doc || typeof doc !== "object" || !doc.data || !Array.isArray(doc.data.features))
    throw new Error(rel + " is not a day document");
  if (pin.count != null && doc.data.features.length !== pin.count)
    throw new Error(rel + " carries " + doc.data.features.length + " features; the season index pins " + pin.count);
  if (pin.fetchedAt && doc.fetchedAt !== pin.fetchedAt)
    throw new Error(rel + " was fetched at " + doc.fetchedAt + "; the season index pins " + pin.fetchedAt);
  if (pin.sha256 && typeof crypto !== "undefined" && crypto.subtle) {
    const dig = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
    const hex = Array.from(new Uint8Array(dig), b => b.toString(16).padStart(2, "0")).join("");
    if (hex !== pin.sha256) throw new Error(rel + " does not match the digest pinned in the season index");
  }
  return doc;
}

/* Load one dated day (fires + perimeters) and set the view to it. Returns the normalized,
 * guard-marked fires. Throws only in ways the caller has decided how to say. */
async function loadDayView(d, tier, notes) {
  const fres = await fetchDayFile(d.fires.file, d.fires);
  if (!usable(fres.data)) throw new Error(d.fires.file + " carries no fires");
  let perims = null;
  try { perims = await fetchDayFile(d.perims.file, d.perims); }
  catch (e) { notes.push("no perimeters (" + why(e) + ")"); }
  S.usingFallback = true; S.tier = tier;
  S.fetchedAt = new Date(fres.fetchedAt);
  S.snapshotDate = fres.fetchedAt;
  S.dataNote = notes.join("; ");
  S.perimsOk = !!(perims && usable(perims.data));
  S.unknownDay = null;
  setView(d.date, null);
  return applyGuard(normalize(fres.data, perims && perims.data));
}

/* The built-in sample: the latest fleet day in the repository, whichever route asked for
 * it (?data=snapshot, or the live mirror failing). If no season day can be read — the
 * index or the guard is down — the committed snapshot is the last resort, dated by its own
 * retrievedAt and shown as the guard rules its day: its day is 8 August 2026, inside the
 * window, so the fleet stays down by the guard's own rule and not by accident. */
async function loadSample(tier, notes) {
  const date = latestFleetDay();
  if (date) {
    const d = S.dayList.find(x => x.date === date);
    S.daySource = "sample";
    try { return await loadDayView(d, tier, notes); }
    catch (e) { notes.push("season day " + date + ": " + why(e)); }
  }
  try {
    const snap = await fetchJSON("data/snapshot.json", 20000);
    S.usingFallback = true; S.tier = tier; S.daySource = "sample";
    S.fetchedAt = new Date(snap.retrievedAt || Date.now());
    S.snapshotDate = snap.retrievedAt;
    S.perimsOk = true; S.unknownDay = null;
    notes.push("shown from the committed snapshot; the season days could not be read");
    S.dataNote = notes.join("; ");
    setView(vancouverDate(S.fetchedAt.getTime()), null);
    return applyGuard(normalize(snap.fires, snap.perimeters));
  } catch (e) {
    notes.push("snapshot: " + why(e));
  }
  S.usingFallback = true; S.tier = "none"; S.fetchedAt = null;
  S.dataNote = notes.join("; "); S.perimsOk = false;
  setView(null, "nothing could be read: " + notes.join("; "));
  return [];
}

export async function loadLive() {
  await loadSeason();

  /* A dated status day, through the same code path as live data. */
  if (DAY) {
    S.daySource = "day";
    if (!S.dayList.length) {
      S.tier = "none"; S.usingFallback = true; S.fetchedAt = null; S.perimsOk = false;
      S.dataNote = "the season index did not load" + (S.seasonNote ? " (" + S.seasonNote + ")" : "");
      S.fires = [];
      setView(DAY, "the season index did not load, so no dated day can be read");
      return [];
    }
    const d = S.dayList.find(x => x.date === DAY);
    if (!d) {
      S.tier = "none"; S.usingFallback = true; S.fetchedAt = null; S.perimsOk = false;
      S.dataNote = ""; S.fires = [];
      S.unknownDay = DAY;
      setView(DAY, "no dated copy of " + DAY + " is in this repository");
      return [];
    }
    try {
      return await loadDayView(d, "day", []);
    } catch (e) {
      // R6: a day file that fails its own checks is not flown around, and the visitor is
      // told which check failed rather than being handed a silent blank map.
      S.tier = "none"; S.usingFallback = true; S.fetchedAt = null; S.perimsOk = false;
      S.dataNote = why(e); S.fires = [];
      setView(d.date, "the day's own files failed their checks (" + why(e) + ")");
      return [];
    }
  }

  if (REPLAY) return await loadSample("replay", []);

  // Live: our own mirror first. Every mirror failure is recorded before anything falls back.
  const notes = [];
  let got = null, perims = null;
  try {
    const fr = await mirrorJSON("fires", 45);
    if (usable(fr.data)) {
      got = fr;
      try { perims = await mirrorJSON("perims", 90); }
      catch (e) { notes.push("no perimeters (" + why(e) + ")"); }
    } else notes.push("mirror carried no fires");
  } catch (e) { notes.push("mirror: " + why(e)); }

  if (got) {
    S.usingFallback = false; S.tier = "mirror"; S.daySource = "live";
    S.fetchedAt = new Date(Date.now() - got.age);
    S.dataNote = notes.join("; ");
    // "Perimeters arrived" has to mean outlines are on the map, not merely that the layer
    // answered: an empty collection draws nothing and must not be described as perimeters.
    S.perimsOk = usable(perims && perims.data);
    S.unknownDay = null;
    // R2: live is a fleet view unless today, in Vancouver, is inside a no-fleet window.
    setView(null, null);
    return applyGuard(normalize(got.data, perims && perims.data));
  }

  // A refresh that failed with a good live picture already on screen keeps that picture
  // AND its provenance — it really did come from the mirror, at the time it says — and the
  // age in the status line goes on growing, the honest signal that the page has stopped
  // being able to update itself. Switching to the sample mid-view would be a mode change
  // the visitor did not ask for.
  if (S.daySource === "live" && S.fires.length) {
    S.dataNote = notes.join("; ");
    return S.fires;
  }

  // The mirror did not answer: the latest fleet day in the repository, dated on the page
  // and never called live.
  return await loadSample("snapshot", notes.concat(["mirror unavailable"]));
}

export function needsShip(f) {
  // The guard decides first (R3): a fire that was a wildfire of note, or that led to
  // evacuation orders or alerts, is never a candidate whatever its status — those fires are
  // about people, and the page does not replay them with a fleet in the picture. Beyond
  // that, the demonstration responds only to fires actually out of control; held and
  // under-control fires stay on the map as monitored-only: crews have them.
  if (f.guarded) return false;
  return f.status === "Out of Control";
}

/* The mode sentence, in the words the ruling fixed (R7: only the braces are filled). One
 * place writes it so the status line, the tests and the fallback generator all quote the
 * same source. The record-day sentence names the window in the guard file's own dates. */
export function modeWords() {
  if (S.unknownDay)
    return S.unknownDay + " has no dated copy in this repository: nothing is shown for that " +
      "day, and no fleet is simulated for it.";
  const date = S.day || vancouverDate(Date.now());
  const time = S.fetchedAt ? vancouverClock(S.fetchedAt.getTime()) : "an unstated time";
  if (S.recordOnly) {
    const open = date + ": the fires as British Columbia published them at " + time + ". ";
    if (S.recordWindow)
      return open + "No fleet is simulated for 8 to 27 August 2026. The province was under a " +
        "state of emergency, and this page does not replay those days with a different ending.";
    return open + "No fleet is simulated for this view: " + S.standDown + ".";
  }
  // "Live" only when the mirror answered; every dated view is a replay of its day.
  const lead = S.daySource === "live" ? "Live " + date : "Replay of " + date;
  return lead + ": the fires as British Columbia published them at " + time + ". The fleet is " +
    "simulated and never flew. Its drops are water released, not water arrived, and nothing " +
    "here says any fire would have burned differently.";
}

/* The guard note (R7), in the words the ruling fixed: the layers panel carries it beside
 * the data note, and the cockpit gives a guarded fire this same reason — never "queued",
 * never "the allocator gave this fire no ship", because neither is true. */
export function guardNoteWords() {
  return "The simulated fleet never works a fire that was a wildfire of note or led to an " +
    "evacuation order or alert, and it keeps " + noteKm(S.guard) + " km from those that " +
    "forced people out. The list and its sources are in data/season/2026.guard.json.";
}

export async function fetchWind() {
  clearTimeout(fetchWind._expiry);
  const act = S.missions.filter(m => !m.idle);
  // Clear the previous forecast even on a failed refresh: stale wind is still air.
  for (const m of act) m.wind = null;
  S.windOk = false; S.windAt = null;
  // The wind mirror describes today's air. A dated day has no forecast to replay honestly
  // and no fleet to carry one, so day and sample views fly in still air, labelled as such.
  S.windNote = S.daySource === "live" ? "mirror unavailable"
    : S.recordOnly ? "no fleet is simulated" : "a dated day replays no forecast";
  if (S.daySource !== "live" || !act.length) { renderStatus(); return; }
  try {
    const grid = readWind(await fetchJSON("data/live/wind.json?ts=" +
      Math.floor(Date.now() / 300000), 12000));
    const winds = act.map(m => windForMission(grid, m));
    act.forEach((m, i) => { m.wind = winds[i]; });
    S.windOk = true; S.windAt = new Date(grid.fetchedAt); S.windNote = "";
    fetchWind._expiry = setTimeout(fetchWind, Math.max(1, Math.min(
      grid.fetchedAt + WIND_MAX_AGE_MS, grid.forecastAt + 2 * 3600000) - Date.now() + 1));
  } catch (e) { S.windNote = why(e); }
  // S.heat must be passed: planTargets scores candidate lines partly on how hot the
  // satellite detections along them are, and it takes that data as an argument so the
  // model can run with no feed. Omitting it silently reverts to geometry-only scoring.
  for (const mm of S.missions) if (!mm.idle) planTargets(mm, S.heat);
  replanAll(); renderStatus();
}

export async function fetchHeat() {
  // The satellite detections the heat overlay draws are a live layer. A status day is the
  // published record of one date and carries none, so day and sample views load no heat —
  // and yesterday's detections must never guide missions on another day's fires anyway.
  if (S.daySource !== "live") { S.heat = []; applyHeat(); return; }
  try {
    const hr = await mirrorJSON("heat", 90, 25000);
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
      // R4: a hotspot line inside a keep-out distance is never aimed at. The geometry
      // targets stand and the heat simply does not refine this mission.
      if (S.regions.length && picks.some(p => pointBlocked(S.regions, p))) continue;
      m.targets = picks;
      m.segs = picks.map(t => dropSeg(m, t, true));
      m.heat = true;
      planTargets(m, S.heat);
    }
  }
  renderDrawer();
}
