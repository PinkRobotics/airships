/* The data this page shows: which view it is, what it asks for, how it falls back, and how
 * the files become model input.
 *
 * EVERY VIEW IS A REPLAY OF THE PUBLISHED RECORD. The page queries no wildfire feed, live
 * or mirrored — the Admiral's ruling of 2026-10-14 stopped that, and this code now reads
 * only files this site itself serves:
 *
 *   a dated day   ?day=YYYY-MM-DD — one of the status days in data/season/. A day whose
 *                 files answer their checks is a fleet day; one that cannot be read
 *                 honestly stands the fleet down and says so in words.
 *   the sample    ?data=snapshot, and the default view: the busiest captured day — most
 *                 hulls working, ranked in data/season/2026.activity.json — read from
 *                 the same season day files; there is no second copy of the data.
 *
 * The separate ?view=exercise route loads invented fires through normalize, with no date,
 * and checks its ground against the season record.
 * Whichever tier answered is named on the page — the status line never implies
 * fresher data than it has, and it names the day and the mode in words on every view.
 */
import { fireNumber } from '../sim/index.js?v=7d7bed4f';
import { EXERCISE_MODE, EXERCISE_NOTE, loadExercise } from './exercise.js?v=7d7bed4f';
import { vancouverClock, vancouverDate } from './dates.js?v=7d7bed4f';
import { fetchJSON } from './net.js?v=7d7bed4f';
import { S } from './store.js?v=7d7bed4f';


/* REPLAY MODE. `?data=snapshot` pins every external input to a dated copy bundled with the
 * repository — the busiest captured fleet day in data/season/ (the ranking's defaultDay;
 * the newest day when the ranking cannot be read), with its fires and perimeters and
 * nothing else: no wind (a forecast cannot be replayed honestly from a file, so replay mode
 * declines to pretend) and no satellite heat (not part of a status day). With
 * `?seed=` pinning the plan jitter, a run is fully determined.
 *
 * That buys three things: golden-output tests that compare numbers rather than screenshots,
 * a link that shows another person exactly what you were looking at, and a page that works
 * with no network at all. A ?day= parameter wins over it: a link that names a day is asking
 * for that day, not for the sample. */
const QP = new URLSearchParams(location.search);
export const EXERCISE = QP.get("view") === "exercise";
export const DAY = QP.get("day");
export const REPLAY = QP.get("data") === "snapshot" && !DAY;

export function normalize(firesGJ, perimsGJ) {
  const close = r => {
    if (!r.length) return r;
    const a = r[0], b = r[r.length - 1];
    return a[0] === b[0] && a[1] === b[1] ? r : r.concat([a.slice()]);
  };
  const rings = {}, footprints = {};
  // Drawing may be thinned; clearance always receives every supplied outer part.
  // Separate perimeter features for the same fire also contribute to the footprint.
  for (const f of (perimsGJ && perimsGJ.features) || []) {
    const num = fireNumber(f.properties.FIRE_NUMBER) || f.properties.FIRE_NUMBER;
    const g = f.geometry; if (!g || !num) continue;
    const polys = g.type === "MultiPolygon" ? g.coordinates : [g.coordinates];
    footprints[num] = (footprints[num] || []).concat(polys.map(p => close(p[0].map(q => q.slice()))));
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
      rings[num] = close(best.filter((_, i) => i % step === 0));
      if (!rings[num].allRings) rings[num].allRings = polys.map(p => {
        const r = p[0]; const st = Math.max(1, Math.floor(r.length / 160));
        return close(r.filter((_, i) => i % st === 0));
      });
    }
  }
  const fires = [];
  for (const f of (firesGJ && firesGJ.features) || []) {
    const p = f.properties, g = f.geometry;
    if (!g || p.FIRE_STATUS === "Out") continue;
    fires.push({
      id: fireNumber(p.FIRE_NUMBER) || p.FIRE_NUMBER || null,
      exercise: S.exercise && p.EXERCISE === true,
      name: S.exercise && p.EXERCISE === true ? p.INCIDENT_NAME : fireNumber(p.FIRE_NUMBER),
      geo: p.GEOGRAPHIC_DESCRIPTION || null,
      status: p.FIRE_STATUS, cause: p.FIRE_CAUSE || null,
      sizeHa: p.CURRENT_SIZE || 0,
      ignited: p.IGNITION_DATE ? new Date(p.IGNITION_DATE) : null,
      url: p.FIRE_URL || null,
      note: p.FIRE_STATUS === "Fire of Note" || p.FIRE_OF_NOTE_IND === "Y" || p.FIRE_OF_NOTE_IND === "Yes",
      ll: [g.coordinates[0], g.coordinates[1]],
      ring: rings[fireNumber(p.FIRE_NUMBER) || p.FIRE_NUMBER] || null,
      footprint: footprints[fireNumber(p.FIRE_NUMBER) || p.FIRE_NUMBER] || null,
    });
  }
  fires.sort((a, b) => b.sizeHa - a.sizeHa);
  return fires;
}

/* Which tier is on screen. loadView sets it, and the status line in main.js says it out
 * loud; nothing else may write it. It is not declared in store.js because this module is
 * the only thing that knows the answer.
 *
 *   "replay"    the bundled sample — the busiest captured fleet day in the repository
 *   "day"       ?day=YYYY-MM-DD — a dated status day, a fleet day unless its files fail
 *   "none"      nothing answered and there is nothing to show
 *
 * S.dataNote carries the reason in words — "no perimeters (…)", "timed out after 15 s" —
 * so a visitor who wonders why is not left guessing, and so the failures that look
 * identical from outside (a file that hangs and a file that returns nothing) read
 * differently on the page. S.perimsOk says whether the outlines came with the points,
 * because a day can carry one and not the other. */

/* One short phrase for one failure, for the status line. */
function why(e) {
  return (e && e.message) || "unknown error";
}

/* A file that parses but carries no fires is a failure of the SOURCE, not of the transport.
 * BC has active fires every day of the season; an empty collection in August is a broken
 * publisher, not a quiet province. It is treated as unusable rather than shown as
 * "0 fires". */
function usable(gj) {
  return !!(gj && Array.isArray(gj.features) && gj.features.length);
}

/* ---------- the season record ----------------------------------------------------------------- */

/* The season index, the season record, and the busiest-day ranking, read once per view.
 * Everything else in this module waits on them: the day control is built from the index,
 * the default view opens on the ranking's day, and the exercise view holds its invented
 * ground against the record's wildfires of note.
 *
 * A failure here is not a blank page: the words go into S.seasonNote and the view degrades
 * to whatever it can still load honestly. */
let seasonOnce = null;
export function loadSeason() {
  if (seasonOnce) return seasonOnce;
  seasonOnce = (async () => {
    const fail = [];
    let daysIdx = null, seasonDoc = null;
    try { daysIdx = await fetchJSON("data/season/2026.days.json", 20000); }
    catch (e) { fail.push("season index: " + why(e)); }
    try { seasonDoc = await fetchJSON("data/season/2026.json", 30000); }
    catch (e) { fail.push("season record: " + why(e)); }
    /* The ranking is a preference, not a source: unreadable falls back to the newest day
     * quietly — the view still works, it just opens quieter. */
    let activity = null;
    try { activity = await fetchJSON("data/season/2026.activity.json", 20000); }
    catch (e) { activity = null; }
    S.seasonFires = seasonDoc && Array.isArray(seasonDoc.fires)
      ? seasonDoc.fires
        .filter(f => f && typeof f.fire === "string" && Number.isFinite(f.lon) && Number.isFinite(f.lat))
        .map(f => ({ id: f.fire, ll: [f.lon, f.lat], sizeHa: f.hindsightSizeHa || 0,
          note: !!(f.fireOfNote || f.wasFireOfNote) }))
      : [];
    S.dayList = daysIdx && Array.isArray(daysIdx.days)
      ? daysIdx.days.filter(d => d && typeof d.date === "string" && d.fires && d.fires.file && d.perims && d.perims.file)
      : [];
    S.seasonNote = fail.length ? fail.join("; ") : null;
    S.activity = activity && typeof activity.defaultDay === "string" ? activity : null;
  })();
  return seasonOnce;
}

/* The newest dated day in the repository — the default view's fallback when the ranking
 * could not be read. Null when the index is down. */
export function latestDay() {
  const days = S.dayList.map(d => d.date).slice().sort();
  return days.length ? days[days.length - 1] : null;
}

/* The day the default view opens on: the busiest captured fleet day — the one with the
 * most hulls left a feasible plan, measured by tools/gen_activity.py over each day's
 * published record and held as data (2026.activity.json's defaultDay; ties went to the
 * newest date when it was measured). A ranking that did not load, or names a day the
 * index does not hold, falls back to the newest day: a quiet default beats none. */
export function bestReplayDay() {
  const ranked = S.activity && S.activity.defaultDay;
  if (ranked && S.dayList.some(x => x.date === ranked)) return ranked;
  return latestDay();
}

/* Set the view's mode once its date is known. Everything downstream — the fleet, the map,
 * the panels — reads S.recordOnly. A forcedWhy (the day's own files failed, an unknown
 * date, nothing could be read) stands the fleet down, and the reason in words is owed to
 * the visitor. */
function setView(date, forcedWhy) {
  S.day = typeof date === "string" ? date : vancouverDate(Date.now());
  S.recordOnly = !!forcedWhy;
  S.standDown = forcedWhy || null;
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

/* Load one dated day (fires + perimeters) and set the view to it. Returns the normalized
 * fires. Throws only in ways the caller has decided how to say. */
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
  return normalize(fres.data, perims && perims.data);
}

/* The built-in sample: the busiest captured day in the repository, whichever route asked
 * for it (?data=snapshot, or a plain visit). If no season day can be read — the index is
 * down — the committed snapshot is the last resort, dated by its own retrievedAt. */
async function loadSample(tier, notes) {
  const date = bestReplayDay();
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
    return normalize(snap.fires, snap.perimeters);
  } catch (e) {
    notes.push("snapshot: " + why(e));
  }
  S.usingFallback = true; S.tier = "none"; S.fetchedAt = null;
  S.dataNote = notes.join("; "); S.perimsOk = false;
  setView(null, "nothing could be read: " + notes.join("; "));
  return [];
}

export async function loadView() {
  await loadSeason();
  if (EXERCISE) return loadExercise(normalize);

  /* A dated status day, checked against the index before it is trusted. */
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
      // A day file that fails its own checks is not flown around, and the visitor is told
      // which check failed rather than being handed a silent blank map.
      S.tier = "none"; S.usingFallback = true; S.fetchedAt = null; S.perimsOk = false;
      S.dataNote = why(e); S.fires = [];
      setView(d.date, "the day's own files failed their checks (" + why(e) + ")");
      return [];
    }
  }

  // The default view is the bundled sample: the busiest captured fleet day in the
  // repository, dated on the page and replayed, never called live.
  return await loadSample("replay", []);
}

export function needsShip(f) {
  // The demonstration responds only to fires actually out of control; held and
  // under-control fires stay on the map with no simulated allocation.
  if (!f) return false;
  return f.status === "Out of Control";
}

/* The mode sentence, in the words the ruling fixed (only the braces are filled). One
 * place writes it so the status line, the tests and the fallback generator all quote the
 * same source. */
export function modeWords() {
  // An exercise that did not load shows nothing, and says so instead of describing a map.
  if (S.exercise)
    return S.recordOnly ? "No exercise is shown, because " + nothingWhy() + ". No fleet is simulated."
      : EXERCISE_MODE;
  if (S.unknownDay)
    return S.unknownDay + " has no dated copy in this repository: nothing is shown for that " +
      "day, and no fleet is simulated for it.";
  // Nothing was read at all: there is no record on screen for the record sentence to name.
  if (S.tier === "none")
    return "No fire data is shown, because " + nothingWhy() + ". No fleet is simulated.";
  const date = S.day || vancouverDate(Date.now());
  const time = S.fetchedAt ? vancouverClock(S.fetchedAt.getTime()) : "an unstated time";
  if (S.recordOnly)
    return date + ": the fires as British Columbia published them at " + time + ". " +
      "No fleet is simulated for this view: " + S.standDown + ".";
  // Every view this page can show is a replay of one day's published record.
  return "Replay of " + date + ": the fires as British Columbia published them at " + time + ". The fleet is " +
    "simulated and never flew. Its drops are water released, not water arrived, and " +
    "nothing here says any fire would have burned differently.";
}

/* True when no fire record is on screen at all: a day this repository holds no copy of, or
 * a view where nothing could be read. Every sentence that describes "the record" asks this
 * first, because an empty map has no record to describe. */
export function nothingShown() {
  // The exercise has one stand-down, in exercise.js: it could not be read.
  return S.exercise ? S.recordOnly : !!S.unknownDay || S.tier === "none";
}

/* Why nothing is shown, as a clause that ends a sentence. */
export function nothingWhy() {
  return S.unknownDay ? "this repository holds no dated copy of " + S.unknownDay
    : S.standDown || "nothing could be read";
}

/* What the view calls itself outside the map: the header strip, the tab title and the
 * description tags. Written here, from the same state as the chip and the mode sentence,
 * so that a view with no fleet never promises one and an empty view never names a record.
 * The static head in index.html names no one view: a link preview and a reader without
 * scripts gets it on every address. */
/* The first-visit screen's phrases that name the view. It opens only where a fleet is
 * simulated, so there are two cases: the exercise, a dated replay. */
export function introWords() {
  if (S.exercise)
    return { tap: "Invented fires · a simulated fleet", mapHead: "The map · exercise",
      mapBody: "Every fire is invented. Real terrain and lakes; a simulated fleet. Drag, zoom, select an exercise fire.",
      fires: "the invented exercise fires" };
  return { tap: "BC fires of " + S.day + " · a simulated fleet drawn over them", mapHead: "The map · " + S.day,
    mapBody: "The real BC fires of " + S.day + ", as published. The moving ships are simulated. Drag, zoom, click anything for its record.",
    fires: "the fires of " + S.day };
}

export function viewLabels() {
  const site = "Pink Robotics fleet monitor";
  const mode = modeWords();
  if (S.exercise && !S.recordOnly)
    return { fires: "exercise · invented fires", fleet: "simulated fleet",
      title: "Exercise · invented fires · " + site,
      ogTitle: "Exercise: invented fires, real terrain, a simulated fleet.",
      description: mode, ogDescription: mode };
  if (nothingShown()) {
    const what = S.exercise ? "exercise unavailable"
      : S.unknownDay ? "no dated copy of " + S.unknownDay : "no fire data";
    const What = what[0].toUpperCase() + what.slice(1);
    return { fires: what, fleet: "no fleet simulated", title: What + " · " + site,
      ogTitle: What + ". Nothing is shown.", description: mode, ogDescription: mode };
  }
  const fires = "BC fires of " + S.day;
  if (S.recordOnly)
    return { fires, fleet: "no fleet simulated",
      title: fires + " · no fleet simulated · " + site,
      ogTitle: "The fires of " + S.day + ", as published. No fleet is simulated.",
      description: mode, ogDescription: mode };
  return { fires, fleet: "simulated fleet", title: fires + " · simulated fleet · " + site,
    ogTitle: "The fires of " + S.day + ". A simulated fleet. Arithmetic you can check.",
    description: mode, ogDescription: mode };
}

/* The scene note: what this view's own data is, where a view has something to say beyond
 * its mode sentence. The exercise carries its note here (what is invented, and the ground
 * it was chosen on); every other view's mode sentence already says what is on screen. */
export function sceneNoteWords() {
  return S.exercise && !S.recordOnly ? EXERCISE_NOTE : "";
}
