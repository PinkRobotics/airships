/* The invented view is separate from the dated-day and mirror fallback routes. It has no
 * date, and its ground is checked here against the season record: the exercise claims its
 * fires stand far from every real wildfire of note, and the view itself re-derives that
 * claim from the record it ships with rather than trusting the generator's word. */
import { havKm, setSeed } from '../sim/index.js?v=6f3787a9';
import { fetchJSON } from './net.js?v=6f3787a9';
import { S } from './store.js?v=6f3787a9';

export const EXERCISE_MODE = 'Exercise: every fire on this map is invented. The terrain, the lakes and the distances are real.';
export const EXERCISE_NOTE = 'No fire shown here happened. No aircraft flew. The exercise shows how the simulated fleet chooses under load. Its ground was chosen at least 150 km from every wildfire of note in the season record and from every fire in the season evacuation record.';
export const EXERCISE_CLEARANCE_KM = 150;

/* The radius (km) of an area-equivalent disc around a footprint, the conservative bound
 * the generator's own record uses for fires without a drawn outline. */
function radiusKm(sizeHa) {
  return Math.sqrt(Math.max(sizeHa || 0, 10) / Math.PI) / 10;
}

export async function loadExercise(normalize) {
  S.exercise = true; S.day = null; S.daySource = 'exercise'; S.tier = 'exercise';
  S.fetchedAt = null; S.snapshotDate = null; S.usingFallback = false;
  S.unknownDay = null;
  try {
    if (S.seasonNote) throw new Error('the season record did not load');
    const doc = await fetchJSON('data/exercise/exercise.json', 20000);
    if (doc.kind !== 'exercise' || !Number.isInteger(doc.seed) || doc.label !== EXERCISE_MODE || doc.note !== EXERCISE_NOTE)
      throw new Error('the exercise identity or labels are invalid');
    if (!doc.fires?.features?.length || !doc.perimeters?.features)
      throw new Error('the exercise has no fire or outline collection');
    for (const f of doc.fires.features) {
      const p = f.properties;
      if (!p.EXERCISE || !/^EX\d{3}$/.test(p.FIRE_NUMBER) || p.INCIDENT_NAME !== 'Exercise ' + p.FIRE_NUMBER.slice(2))
        throw new Error('an exercise fire is not labelled as invented');
    }
    // The note says the ground was chosen far from every wildfire of note in the season
    // record. Hold that here, from the record itself: centre-to-centre distance minus the
    // discs both sides claim. A scene that no longer clears the sentence it ships with is
    // refused, not shown anyway; the generator's own gate holds the full basis (every
    // captured outline, and the evacuation record) against the committed files.
    const rings = new Map();
    for (const f of doc.perimeters.features) rings.set(f.properties.FIRE_NUMBER, f.geometry?.coordinates?.[0] || null);
    let minKm = Infinity;
    for (const f of doc.fires.features) {
      const ll = f.geometry.coordinates, size = f.properties.CURRENT_SIZE || 0;
      const ring = rings.get(f.properties.FIRE_NUMBER);
      const reach = ring ? Math.max(...ring.map(p => havKm(ll, p))) : radiusKm(size);
      for (const s of S.seasonFires) {
        if (!s.note) continue;
        const km = havKm(ll, s.ll) - reach - radiusKm(s.sizeHa);
        if (km < minKm) minKm = km;
      }
    }
    S.exerciseClearance = { minKm: Math.round(minKm * 10) / 10, limitKm: EXERCISE_CLEARANCE_KM };
    if (minKm < EXERCISE_CLEARANCE_KM - 1e-6)
      throw new Error('an exercise footprint is within ' + EXERCISE_CLEARANCE_KM + ' km of a wildfire of note in the season record');
    setSeed(doc.seed);
    S.recordOnly = false; S.standDown = null; S.perimsOk = true;
    S.dataNote = EXERCISE_NOTE;
    return normalize(doc.fires, doc.perimeters);
  } catch (e) {
    // A clause that ends "..., because": the page's sentences for an empty view are built on it.
    S.recordOnly = true; S.standDown = 'the exercise could not be read (' + e.message + ')';
    S.dataNote = S.standDown; S.perimsOk = false;
    S.exerciseClearance = null;
    return [];
  }
}
