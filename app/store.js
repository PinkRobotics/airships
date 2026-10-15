/* S — the application's state, in one object.
 *
 * Everything mutable that is not owned by a single module lives here, so that "what is
 * the page currently showing" has one answer you can print.
 */
export const S = {
  fires: [], missions: [], standby: [], water: [], outline: [], waterMeta: null,
  usingFallback: false, fetchedAt: null, snapshotDate: null,
  /* The view's day. S.day is the America/Vancouver date this view shows, today included.
   * S.daySource is which route produced it: "live" (the site mirror), "day" (?day=YYYY-MM-DD)
   * or "sample" (?data=snapshot, or the mirror failing). S.recordOnly is true only when the
   * view could not be read honestly (a day with no dated copy, files that failed their
   * checks, an unreadable exercise, nothing readable at all): the fleet stands down and
   * S.standDown carries the reason in words. S.dayList is the season index for the day
   * control; S.unknownDay is set when ?day= named a date no day file exists for;
   * S.seasonFires is the season record's fires as {id, ll, sizeHa, note}, kept for the
   * exercise view's clearance check; S.seasonNote is the words for a season file that did
   * not load. */
  // An exercise has no date; its invented ground is checked against the season record.
  exercise: false,
  day: null, daySource: "live", recordOnly: false, standDown: null,
  unknownDay: null, dayList: null, seasonFires: null, seasonNote: null,
  sel: null, hlClass: null,  // {type, m, f} | null; hlClass dims other classes
  follow: false, filter: "all", modeId: "balanced", exampleCls: "P100",
  battByHull: {},   // storage state survives the 15-minute live-feed rebuilds, keyed by hull
  speed: 5, paused: false, simTime: 0, lastFrame: null,
  windOk: null, windAt: null, windNote: "loading mirror", roads: [], heat: [],
  view: { cx: -124.5, cy: -73.5, k: 14 },  // world: x=lon, y=mercator(lat)
  layers: { terrain: true, hot: true, wind: true, places: true, perims: true, water: true, routes: true, labels: false },
  reduced: matchMedia("(prefers-reduced-motion: reduce)").matches,
};
if (S.reduced) { S.paused = true; }
