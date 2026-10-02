/* The guard: the days and the fires the simulated fleet must not touch.
 *
 * WHY THIS EXISTS. The monitor flies an imagined fleet over real wildfires, and the 2026
 * season it replays includes days and fires where what happened to people is the only fact
 * that matters. The project's rule is that a tragedy is never replayed with a better
 * ending: so there are days the fleet is not simulated at all, fires it never works no
 * matter their status, and distances it keeps from the fires that forced people out. Those
 * decisions are data, not code: they live in data/season/2026.guard.json, written by hand
 * with a source link per entry, and this module is the one place that reads them.
 *
 * WHAT THIS MODULE IS ALLOWED TO DO. Nothing but arithmetic: no DOM, no fetch, no clock.
 * Every function is a function of its arguments. The page loads the guard file and hands
 * the parsed object to loadGuard(); tests hand it invented objects with the same shape, and
 * deliberately broken ones, because a guard that fails open is worse than no guard.
 *
 * THE THREE WAYS A FIRE IS GUARDED (in this order, first match wins):
 *   listed      it is in the guard file, by fire number — or by name, for the rare entry
 *               written before anyone knew its number. The entry's own keep-out wins.
 *   of-note     the day's own data flags it a wildfire of note (`note` on the fire). An
 *               unlisted fire of note gets the file's default distance.
 *   season-note the season record marked it a fire of note then or earlier. The season file
 *               is hindsight, and hindsight is not allowed to send the fleet anywhere —
 *               but it is allowed to refuse. This use only ever subtracts.
 */
import { havKm } from './geo.js?v=26282d19';

/* Dates here are America/Vancouver calendar dates, YYYY-MM-DD, and they ARRIVE as strings:
 * sim/ touches no clock, so the epoch→date conversion (app/dates.js) is the caller's job.
 * The no-fleet window is defined in those dates. */

const DATE = /^\d{4}-\d{2}-\d{2}$/;
const BASES = ["loss", "order", "alert", "new"];

function isDate(s) {
  return typeof s === "string" && DATE.test(s);
}

/**
 * Parse and validate the guard file. Returns a state object; check `.ok` first.
 *
 * @param {object}  doc  the parsed data/season/2026.guard.json
 * @param {object?} ctx  {seasonNumbers?, seasonOfNote?, viewFires?} — the season record's
 *                       fire numbers, the numbers it flags as fires of note, and the fires
 *                       in view, so an entry that resolves to no fire at all can be named.
 *                       Without seasonNumbers the resolution check is skipped (tests).
 */
export function loadGuard(doc, ctx = {}) {
  const bad = (reason) => ({ ok: false, reason, fires: [], places: [], noFleet: [] });
  if (!doc || typeof doc !== "object" || Array.isArray(doc)) return bad("the guard file is not an object");
  if (typeof doc.defaultKeepOutKm !== "number" || !(doc.defaultKeepOutKm > 0))
    return bad("defaultKeepOutKm is missing or not a positive distance");

  if (!Array.isArray(doc.noFleet)) return bad("noFleet is missing");
  const noFleet = [];
  for (const w of doc.noFleet) {
    if (!w || typeof w !== "object" || !isDate(w.from) || !isDate(w.to) || w.from > w.to
        || typeof w.basis !== "string" || !w.basis || typeof w.source !== "string"
        || !/^https?:\/\//.test(w.source))
      return bad(`a no-fleet window is not {from, to, basis, source} with a link`);
    noFleet.push({ from: w.from, to: w.to, basis: w.basis, source: w.source });
  }

  if (!Array.isArray(doc.fires)) return bad("fires is missing");
  const seasonNumbers = ctx.seasonNumbers ? new Set(ctx.seasonNumbers) : null;
  const viewIds = new Set((ctx.viewFires || []).map((f) => f.id));
  const viewNames = new Set((ctx.viewFires || []).map((f) => (f.name || "").toLowerCase()));
  const byNumber = new Map(), byName = new Map(), fires = [];
  for (const e of doc.fires) {
    if (!e || typeof e !== "object") return bad("a fire entry is not an object");
    const hasNumber = e.fire != null;
    if (hasNumber && typeof e.fire !== "string") return bad(`a fire entry's number is not a string`);
    if (!hasNumber && typeof e.name !== "string") return bad("a fire entry with no number has no name");
    if (typeof e.name !== "string" || !e.name) return bad("a fire entry has no name");
    if (![1, 2, 3].includes(e.tier)) return bad(`${e.name}: tier must be 1, 2 or 3`);
    if (!BASES.includes(e.basis)) return bad(`${e.name}: basis must be one of ${BASES.join(", ")}`);
    if (typeof e.keepOutKm !== "number" || e.keepOutKm < 0) return bad(`${e.name}: keepOutKm is not a distance`);
    if (typeof e.source !== "string" || !/^https?:\/\//.test(e.source))
      return bad(`${e.name}: no source link`);
    if (hasNumber) {
      if (byNumber.has(e.fire)) return bad(`${e.fire}: listed twice`);
      byNumber.set(e.fire, e);
    } else if (byName.has(e.name.toLowerCase())) {
      return bad(`${e.name}: listed twice by name`);
    } else byName.set(e.name.toLowerCase(), e);
    if (seasonNumbers && hasNumber && !seasonNumbers.has(e.fire) && !viewIds.has(e.fire))
      return bad(`${e.fire} (${e.name}) is in no season record and no view: it cannot be resolved`);
    fires.push(e);
  }

  if (!Array.isArray(doc.places)) return bad("places is missing");
  const places = [];
  for (const p of doc.places) {
    if (!p || typeof p !== "object" || typeof p.name !== "string" || !p.name
        || !isDate(p.date) || typeof p.keepOutKm !== "number" || p.keepOutKm < 0
        || !Array.isArray(p.ll) || p.ll.length !== 2
        || typeof p.ll[0] !== "number" || typeof p.ll[1] !== "number"
        || !BASES.includes(p.basis) || typeof p.source !== "string"
        || !/^https?:\/\//.test(p.source))
      return bad(`a place entry is not {name, ll, date, basis, keepOutKm, source}`);
    places.push(p);
  }

  return {
    ok: true, reason: null, doc,
    defaultKeepOutKm: doc.defaultKeepOutKm, noFleet, fires, places, byNumber, byName,
    seasonOfNote: ctx.seasonOfNote ? new Set(ctx.seasonOfNote) : null,
  };
}

/** Is the fleet simulated on this date? A guard state that failed to load stands the fleet
 *  down everywhere, and says why in words — the caller owes the page that sentence. */
export function dayKind(G, date) {
  if (!G || !G.ok) return { fleet: false, reason: G && G.reason ? G.reason : "the guard file did not load" };
  if (!isDate(date)) return { fleet: false, reason: `${date} is not a date` };
  for (const w of G.noFleet)
    if (date >= w.from && date <= w.to)
      return { fleet: false, reason: `${date} is inside the no-fleet window ${w.from} to ${w.to}` };
  return { fleet: true, reason: null };
}

/** Why a fire in view is guarded, or null if it is not. `fire` is a normalized fire: id,
 *  name, note (the day's own of-note flag), ring and sizeHa carry the geometry. */
export function guardedFire(G, fire, ctx = {}) {
  if (!G || !G.ok) return { why: "guard-down", tier: null, basis: null, keepOutKm: 0 };
  let e = fire.id && G.byNumber.get(fire.id) || null;
  if (!e && fire.name) e = G.byName.get(fire.name.toLowerCase()) || null;
  if (e) return { why: "listed", tier: e.tier, basis: e.basis, keepOutKm: e.keepOutKm, entry: e };
  if (fire.note)
    return { why: "of-note", tier: null, basis: "of note", keepOutKm: G.defaultKeepOutKm };
  // Coerced rather than trusted: a caller handing an array here (a test, a future page)
  // would otherwise crash on .has, and a crash in this function is a refusal that forgot
  // to say so. Sets pass through untouched.
  const season = ctx.seasonOfNote instanceof Set ? ctx.seasonOfNote
    : new Set(ctx.seasonOfNote || G.seasonOfNote || []);
  if (fire.id && season.has(fire.id))
    return { why: "season-of-note", tier: null, basis: "of note", keepOutKm: G.defaultKeepOutKm };
  return null;
}

/** The fires' own radius, in km, the way the model draws them (targets.js insideFire). */
function fireRadiusKm(fire) {
  return Math.sqrt(Math.max(fire.sizeHa || 0, 10) * 1e4 / Math.PI) / 1000;
}

/* A perimeter edge is generalised, so a single edge can run for kilometres: sample each
   edge at ~2 km so "within X of the outline" is measured against the line, not only the
   vertices. Pure arithmetic on lon/lat; good to well inside the 25 km scales here. */
function ringPoints(ring, stepKm = 2) {
  const pts = [];
  for (let i = 0; i < ring.length - 1; i++) {
    const a = ring[i], b = ring[i + 1];
    const d = havKm(a, b);
    const n = Math.max(1, Math.ceil(d / stepKm));
    for (let k = 0; k < n; k++) pts.push([a[0] + (b[0] - a[0]) * k / n, a[1] + (b[1] - a[1]) * k / n]);
  }
  pts.push(ring[ring.length - 1]);
  return pts;
}

function insideRing(ring, pt) {
  let inside = false;
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    if (((ring[i][1] > pt[1]) !== (ring[j][1] > pt[1])) &&
        (pt[0] < (ring[j][0] - ring[i][0]) * (pt[1] - ring[i][1]) / (ring[j][1] - ring[i][1]) + ring[i][0]))
      inside = !inside;
  }
  return inside;
}

/**
 * The keep-out regions for one view: every guarded fire in it that carries a distance, and
 * every place entry whose date this is. A guarded fire with keepOutKm 0 guards against
 * being worked but claims no air. A fire flagged of note by the day itself and missing from
 * the file gets the default distance (R4's default rule).
 *
 * @param {object}  G     the guard state
 * @param {Array}   fires the normalized fires in view
 * @param {object?} ctx   {seasonOfNote?}
 * @param {string?} date  the view's date, for place entries
 */
export function keepOutsFor(G, fires, ctx = {}, date = null) {
  if (!G || !G.ok) return [];
  const out = [];
  for (const f of fires) {
    const g = guardedFire(G, f, ctx);
    if (!g || !(g.keepOutKm > 0)) continue;
    const region = { kind: "fire", who: f.id || f.name, why: g.why, rKm: g.keepOutKm,
                     ll: f.ll, edge: null, ring: null };
    if (f.ring && f.ring.length > 2) {
      region.ring = f.ring;
      region.edge = ringPoints(f.ring);
    } else {
      region.rKm = g.keepOutKm + fireRadiusKm(f);
    }
    out.push(region);
  }
  if (date)
    for (const p of G.places)
      if (p.date === date && p.keepOutKm > 0)
        out.push({ kind: "place", who: p.name, why: "place", rKm: p.keepOutKm,
                   ll: p.ll.slice(), edge: null, ring: null });
  return out;
}

/** Is this point inside a keep-out region? Returns the region (for the message) or null. */
export function pointBlocked(regions, pt) {
  for (const r of regions) {
    if (r.ring && insideRing(r.ring, pt)) return r;
    const pts = r.edge || [r.ll];
    for (let i = 0; i < pts.length; i++)
      if (havKm(pts[i], pt) <= r.rKm) return r;
  }
  return null;
}

/** Does the straight path a→b enter a keep-out region? Sampled every `stepKm` (the drawn
 *  track bows a few percent off the straight leg; the dispatch check that calls this keeps
 *  a margin, and the page-level gate samples the ships' own positions besides). */
export function pathBlocked(regions, a, b, stepKm = 1) {
  const d = havKm(a, b), n = Math.max(2, Math.ceil(d / stepKm) + 1);
  for (let k = 0; k < n; k++) {
    const pt = [a[0] + (b[0] - a[0]) * k / (n - 1), a[1] + (b[1] - a[1]) * k / (n - 1)];
    const hit = pointBlocked(regions, pt);
    if (hit) return hit;
  }
  return null;
}

/** The distance the layers-panel note names: the widest keep-out among entries that exist
 *  because people were forced out (a loss, an order). Falls back to the file default. */
export function noteKm(G) {
  let km = G && G.ok ? G.defaultKeepOutKm : 0;
  for (const e of (G && G.fires) || [])
    if ((e.basis === "loss" || e.basis === "order") && e.keepOutKm > km) km = e.keepOutKm;
  for (const p of (G && G.places) || [])
    if ((p.basis === "loss" || p.basis === "order") && p.keepOutKm > km) km = p.keepOutKm;
  return km;
}
