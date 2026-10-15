/* S — the application's state, in one object.
 *
 * Everything mutable that is not owned by a single module lives here, so that "what is
 * the page currently showing" has one answer you can print.
 */
export const S = {
  fires: [], missions: [], standby: [], water: [], outline: [], waterMeta: null,
  usingFallback: false, snapshotDate: null,
  /* The moment the record on screen was captured — the day file's own fetchedAt, set by
   * feeds.js when it loads a view. It is not a page event: nothing was fetched live, and
   * the mode sentence quotes this time as the record's, not ours. */
  fetchedAt: null,
  /* The view's day. S.day is the America/Vancouver date this view shows. S.daySource is
   * which route produced it: "day" (?day=YYYY-MM-DD) or "sample" (?data=snapshot, or the
   * no-parameter default — every view is a replay of the published record, and nothing is
   * fetched from any agency). S.recordOnly is true only when the view could not be read
   * honestly (a day with no dated copy, files that failed their checks, an unreadable
   * exercise, nothing readable at all): the fleet stands down and S.standDown carries the
   * reason in words. S.dayList is the season index for the day control; S.unknownDay is
   * set when ?day= named a date no day file exists for; S.seasonFires is the season
   * record's fires as {id, ll, sizeHa, note}, kept for the exercise view's clearance
   * check; S.seasonNote is the words for a season file that did not load. S.activity is
   * the busiest-day ranking the default view opens by (2026.activity.json), or null when
   * it did not load — the default then falls back to the newest day. */
  // An exercise has no date; its invented ground is checked against the season record.
  exercise: false,
  day: null, daySource: "sample", recordOnly: false, standDown: null,
  unknownDay: null, dayList: null, seasonFires: null, seasonNote: null, activity: null,
  sel: null, hlClass: null,  // {type, m, f} | null; hlClass dims other classes
  follow: false, filter: "all", modeId: "balanced", exampleCls: "P100",
  battByHull: {},   // storage state survives rebuilds, keyed by hull
  speed: 5, paused: false, simTime: 0, lastFrame: null,
  // The mirror is gone; the wind line is a still-air note naming the view. heat stays as
  // an (always empty) array because the sim's mission builder reads S.heat.
  windOk: false, windAt: null, windNote: "", roads: [], heat: [],
  view: { cx: -124.5, cy: -73.5, k: 14 },  // world: x=lon, y=mercator(lat)
  layers: { terrain: true, places: true, perims: true, water: true, routes: true, labels: false },
  reduced: matchMedia("(prefers-reduced-motion: reduce)").matches,
};
if (S.reduced) { S.paused = true; }
