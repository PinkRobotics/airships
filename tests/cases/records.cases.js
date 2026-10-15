/* Fire-record identity: the join key between the day files' points, their perimeter files
 * and the season record. Every value here is invented — numbers that are no fire — because
 * what is under test is the SHAPE: one capital letter then five digits, or two capital
 * letters then four, the way every season file writes its fire numbers. A value that could
 * not match a fire is null, never a shrug and never a thrown error, because normalize
 * (app/feeds.js) keeps an unparseable number only as a display string that can join
 * nothing.
 */
import { describe, eq, it } from '../harness.js';
import { fireNumber } from '../../sim/index.js?v=6f3787a9';

describe('records · fireNumber', () => {
  it('accepts the two published shapes, normalised', () => {
    eq(fireNumber('X10001'), 'X10001', 'one letter, five digits');
    eq(fireNumber(' x10001 '), 'X10001', 'trimmed and uppercased');
    eq(fireNumber('va1981'), 'VA1981', 'two letters, four digits');
    eq(fireNumber(' VA1981 '), 'VA1981', 'two-letter shape normalised too');
  });
  it('refuses everything that could not join a fire', () => {
    for (const bad of ['12345', 'X1', 'X1000', 'X100001', 'X1000A', 'VAA1981', 'va198',
                       'X 1001', 'X-1001', '', '   ', 'Fire 123', 'X10001 ' + '.5'])
      eq(fireNumber(bad), null, String(bad));
  });
  it('refuses non-strings and never throws', () => {
    for (const bad of [null, undefined, 10001, {}, [], true])
      eq(fireNumber(bad), null, String(bad));
    eq(fireNumber('X10001').length, 6, 'an accepted number is six characters');
  });
});
