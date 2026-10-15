/* Fire-record identity, the one thing the loader still owes every view.
 *
 * A fire number the way every season file writes it: one capital letter, then digits.
 * It is the join key between the day files' points, their perimeter files and the season
 * record, so a value that could not match a fire is a refusal, not a shrug: normalize
 * (app/feeds.js) keeps an unparseable number only as a display string that can join
 * nothing. Pure arithmetic, like the rest of sim/: no DOM, no fetch, no clock.
 */
export function fireNumber(value) {
  if (typeof value !== "string") return null;
  const n = value.trim().toUpperCase();
  return /^(?:[A-Z][0-9]{5}|[A-Z]{2}[0-9]{4})$/.test(n) ? n : null;
}
