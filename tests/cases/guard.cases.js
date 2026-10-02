/* The guard: the days and fires the simulated fleet must not touch.
 *
 * Every fixture here is invented — numbers that are no fire, places that are no town —
 * because what is under test is the RULE, not the 2026 list: that a guard which cannot be
 * read fails closed, that a listed fire is never a candidate whatever its status, that a
 * keep-out distance is measured against a fire's outline and not its centroid, and that
 * the window and the distances answer to the file, not to the code. The real file's own
 * pins (its digest, its window, its counts) are held by tests/guard/check.py, which is
 * where a deliberate edit to data/season/2026.guard.json is made to hurt.
 */
import { close, deepEq, describe, eq, it, ok } from '../harness.js';
import {
  dayKind, guardedFire, keepOutsFor, loadGuard, noteKm, pathBlocked, pointBlocked,
} from '../../sim/index.js?v=26282d19';

/* A well-formed guard file, small enough to check by hand. X-prefixed numbers are not
   BCWS fire numbers; the dates are 2030; nothing here is real. */
const DOC = () => ({
  defaultKeepOutKm: 10,
  noFleet: [{ from: '2030-08-08', to: '2030-08-27', basis: 'a state of emergency',
              source: 'https://example.test/window' }],
  fires: [
    { fire: 'X10001', name: 'Alpha', tier: 1, basis: 'loss', keepOutKm: 30,
      source: 'https://example.test/alpha' },
    { fire: 'X10002', name: 'Beta', tier: 2, basis: 'order', keepOutKm: 20,
      source: 'https://example.test/beta' },
    { name: 'The Nameless Fire', tier: 3, basis: 'alert', keepOutKm: 0,
      source: 'https://example.test/nameless' },
  ],
  places: [
    { name: 'A Town', ll: [-120.5, 50.5], date: '2030-09-01', basis: 'order', keepOutKm: 15,
      source: 'https://example.test/town' },
  ],
});
const CTX = { seasonNumbers: ['X10001', 'X10002'] };

/* Normalized fires in the shape app/feeds.js hands the model. */
const fire = (over = {}) => Object.assign(
  { id: 'X19999', name: 'Nowhere', ll: [-120, 50], sizeHa: 100, note: false, ring: null }, over);

describe('guard · loadGuard', () => {
  it('accepts a well-formed file and counts what it holds', () => {
    const G = loadGuard(DOC(), CTX);
    ok(G.ok, `expected ok, got reason: ${G.reason}`);
    eq(G.defaultKeepOutKm, 10, 'the file default');
    eq(G.noFleet.length, 1, 'one window');
    eq(G.fires.length, 3, 'three fire entries');
    eq(G.places.length, 1, 'one place');
    eq(G.byNumber.get('X10001').keepOutKm, 30, 'by number');
    ok(G.byName.has('the nameless fire'), 'by name, lower-cased');
  });

  it('refuses a file that is not an object, or has no default distance', () => {
    for (const doc of [null, undefined, 3, 'x', []]) {
      const G = loadGuard(doc, CTX);
      ok(!G.ok && /not an object/.test(G.reason), `null-shaped doc: ${G.reason}`);
    }
    for (const d of [undefined, 0, -5, '10']) {
      const doc = DOC(); delete doc.defaultKeepOutKm; if (d !== undefined) doc.defaultKeepOutKm = d;
      const G = loadGuard(doc, CTX);
      ok(!G.ok && /defaultKeepOutKm/.test(G.reason), `default ${String(d)}: ${G.reason}`);
    }
  });

  it('refuses a window that is not {from, to, basis, source} in order, with a link', () => {
    const cases = [
      ['from after to', w => { w.from = '2030-09-01'; w.to = '2030-08-01'; }],
      ['not a date', w => { w.from = '2030-8-8'; }],
      ['no basis', w => { delete w.basis; }],
      ['no source', w => { delete w.source; }],
      ['a source that is not a link', w => { w.source = 'see the newspaper'; }],
    ];
    for (const [name, bend] of cases) {
      const doc = DOC(); bend(doc.noFleet[0]);
      const G = loadGuard(doc, CTX);
      ok(!G.ok && /no-fleet window/.test(G.reason), `${name}: ${G.reason}`);
    }
    const doc = DOC(); delete doc.noFleet;
    ok(!loadGuard(doc, CTX).ok, 'noFleet missing is refused');
  });

  it('refuses a fire entry that is incomplete, wrong-typed or duplicated', () => {
    const bend = (f, fn) => { const doc = DOC(); fn(doc.fires[f]); return loadGuard(doc, CTX); };
    const cases = [
      ['tier 4', e => { e.tier = 4; }],
      ['tier missing', e => { delete e.tier; }],
      ['a basis outside the vocabulary', e => { e.basis = 'hunch'; }],
      ['a negative distance', e => { e.keepOutKm = -1; }],
      ['a distance that is not a number', e => { e.keepOutKm = '20'; }],
      ['no name', e => { delete e.name; }],
      ['no number and no name', e => { delete e.fire; delete e.name; }],
      ['a number that is not a string', e => { e.fire = 10001; }],
      ['no source link', e => { e.source = 'trust me'; }],
    ];
    for (const [name, fn] of cases) {
      const G = bend(0, fn);
      ok(!G.ok && /(fire entry|Alpha)/.test(G.reason), `${name}: ${G.reason}`);
    }
    ok(!bend(1, e => { e.fire = 'X10001'; }).ok, 'a number listed twice is refused');
    const doc = DOC();
    doc.fires.push({ name: 'the nameless fire', tier: 3, basis: 'alert', keepOutKm: 0,
                     source: 'https://example.test/two' });
    ok(!loadGuard(doc, CTX).ok, 'a name listed twice is refused');
  });

  it('refuses a listed number that no season record and no view carries (R6)', () => {
    const G = loadGuard(DOC(), { seasonNumbers: ['X10002'] });
    ok(!G.ok && /X10001 .*cannot be resolved/.test(G.reason), G.reason);
    // without seasonNumbers the resolution check is skipped: the guard still loads
    ok(loadGuard(DOC(), {}).ok, 'no season context: the check is skipped, not failed');
    const G2 = loadGuard(DOC(), { seasonNumbers: ['X99999'],
                                  viewFires: [fire({ id: 'X10001' }), fire({ id: 'X10002' })] });
    ok(G2.ok, 'fires in view satisfy resolution even when the season record lacks them');
  });

  it('refuses a place that is not {name, ll, date, basis, keepOutKm, source}', () => {
    const bend = (fn) => { const doc = DOC(); fn(doc.places[0]); return loadGuard(doc, CTX); };
    for (const [name, fn] of [
      ['no coordinates', p => { delete p.ll; }],
      ['one coordinate', p => { p.ll = [-120.5]; }],
      ['coordinates that are not numbers', p => { p.ll = ['-120.5', '50.5']; }],
      ['not a date', p => { p.date = '2030/09/01'; }],
      ['a negative distance', p => { p.keepOutKm = -1; }],
      ['no source link', p => { p.source = 'a book'; }],
    ]) {
      const G = bend(fn);
      ok(!G.ok && /place entry/.test(G.reason), `${name}: ${G.reason}`);
    }
    ok(!bend(p => { delete p.name; }).ok, 'no name is refused');
  });
});

describe('guard · dayKind', () => {
  const G = loadGuard(DOC(), CTX);
  it('stands the fleet down on every date of the window, both ends included', () => {
    for (const d of ['2030-08-08', '2030-08-15', '2030-08-27'])
      deepEq(dayKind(G, d), { fleet: false, reason: `${d} is inside the no-fleet window 2030-08-08 to 2030-08-27` }, d);
  });
  it('flies on every date outside the window', () => {
    for (const d of ['2030-08-07', '2030-08-28', '2030-07-04', '2031-01-01'])
      deepEq(dayKind(G, d), { fleet: true, reason: null }, d);
  });
  it('stands down everywhere when the guard did not load, and says why', () => {
    const bad = loadGuard({ defaultKeepOutKm: 1, noFleet: [] }, {});   // fires: missing
    const k = dayKind(bad, '2030-09-01');
    ok(!k.fleet && /fires is missing/.test(k.reason), k.reason);
    const none = dayKind(null, '2030-09-01');
    ok(!none.fleet && /did not load/.test(none.reason), none.reason);
  });
  it('refuses a date that is not YYYY-MM-DD rather than guessing', () => {
    for (const d of ['2030-8-8', 'not-a-date', 20300808, null])
      ok(!dayKind(G, d).fleet, String(d));
  });
});

describe('guard · guardedFire', () => {
  const G = loadGuard(DOC(), CTX);
  it('holds a listed fire by number or by name, at the entry\'s own distance', () => {
    eq(guardedFire(G, fire({ id: 'X10001', name: 'Alpha' })).why, 'listed', 'by number');
    eq(guardedFire(G, fire({ id: 'X10001', name: 'Alpha' })).keepOutKm, 30, 'tier 1 distance');
    const byName = guardedFire(G, fire({ id: 'X77777', name: 'THE NAMELESS FIRE' }));
    eq(byName.why, 'listed', 'matched by name, case-insensitively');
    eq(byName.keepOutKm, 0, 'tier 3 holds the fire but claims no air');
  });
  it('holds a fire the day itself flags of note, at the file default', () => {
    const g = guardedFire(G, fire({ note: true }));
    deepEq([g.why, g.basis, g.keepOutKm], ['of-note', 'of note', 10], 'unlisted fire of note');
  });
  it('holds a fire the season record marked of note, even unseen that day', () => {
    const g = guardedFire(G, fire({ id: 'X12168' }), { seasonOfNote: ['X12168'] });
    deepEq([g.why, g.keepOutKm], ['season-of-note', 10], 'hindsight may refuse, never send');
    const g2 = guardedFire(G, fire({ id: 'X12168' }));
    eq(g2, null, 'without that context the same fire is free');
  });
  it('the list outranks the day: a listed fire keeps its entry even if flagged of note', () => {
    const g = guardedFire(G, fire({ id: 'X10002', name: 'Beta', note: true }));
    deepEq([g.why, g.keepOutKm], ['listed', 20], 'listed wins');
  });
  it('an unlisted, unflagged fire is not guarded', () => {
    eq(guardedFire(G, fire()), null, 'free to work');
  });
  it('a guard that did not load guards every fire', () => {
    const bad = { ok: false, reason: 'no', fires: [], places: [], byNumber: new Map(), byName: new Map() };
    deepEq(guardedFire(bad, fire()).why, 'guard-down', 'down is down');
  });
});

describe('guard · keepOutsFor', () => {
  const G = loadGuard(DOC(), CTX);
  it('builds a region per guarded fire that carries a distance', () => {
    const r = keepOutsFor(G, [fire({ id: 'X10002', name: 'Beta', ll: [-120, 50], sizeHa: 100 })]);
    eq(r.length, 1, 'one region');
    eq(r[0].kind, 'fire', 'kind');
    close(r[0].rKm, 20 + Math.sqrt(100 * 1e4 / Math.PI) / 1000, 1e-9,
          'no ring: the distance plus the fire\'s own radius');
    ok(!r[0].ring, 'no ring on the region');
  });
  it('measures from the outline when there is one, and samples its edges', () => {
    const ring = [[-121, 50], [-120.5, 50], [-120.5, 50.5], [-121, 50.5], [-121, 50]];
    const r = keepOutsFor(G, [fire({ id: 'X10001', name: 'Alpha', ring, sizeHa: 5000 })]);
    eq(r.length, 1, 'one region');
    eq(r[0].rKm, 30, 'the distance itself, not distance-plus-radius');
    deepEq(r[0].ring, ring, 'the ring is carried');
    ok(r[0].edge.length > 60, `edges sampled about every 2 km (${r[0].edge.length} points)`);
  });
  it('a tier-3 fire is held but claims no air, and a place claims air only on its date', () => {
    const day = '2030-09-01';
    const fires = [fire({ name: 'The Nameless Fire' }), fire({ id: 'X10002', name: 'Beta' })];
    const r = keepOutsFor(G, fires, {}, day);
    eq(r.length, 2, 'the tier-3 fire contributed no region');
    ok(r.some(x => x.kind === 'place' && x.who === 'A Town' && x.rKm === 15), 'the place, on its day');
    eq(keepOutsFor(G, fires, {}, '2030-09-02').length, 1, 'no place on any other date');
  });
  it('an unlisted fire of note is kept out at the default distance', () => {
    const r = keepOutsFor(G, [fire({ note: true, ll: [-120, 50], sizeHa: 10 })]);
    eq(r.length, 1, 'one region');
    close(r[0].rKm, 10 + Math.sqrt(10 * 1e4 / Math.PI) / 1000, 1e-9, 'default plus its radius');
  });
  it('a guard that did not load produces no regions — and the fleet is down anyway', () => {
    deepEq(keepOutsFor({ ok: false }, [fire()]), [], 'nothing');
  });
});

describe('guard · pointBlocked and pathBlocked', () => {
  const G = loadGuard(DOC(), CTX);
  const ll = [-120, 50];
  const circle = keepOutsFor(G, [fire({ id: 'X10002', name: 'Beta', ll, sizeHa: 10 })]);
  it('blocks a point inside the distance and frees one outside it', () => {
    close(20 + Math.sqrt(10 * 1e4 / Math.PI) / 1000, 20.178, 0.01, 'the region radius');
    eq(pointBlocked(circle, [-120, 50]).who, 'X10002', 'at the fire');
    eq(pointBlocked(circle, [-120, 50 + 0.1]).who, 'X10002', '11 km north is inside');
    eq(pointBlocked(circle, [-120, 50 + 0.4]), null, '44 km north is outside');
  });
  const ring = [[-121, 50], [-120.5, 50], [-120.5, 50.5], [-121, 50.5], [-121, 50]];
  const outline = keepOutsFor(G, [fire({ id: 'X10001', name: 'Alpha', ring, sizeHa: 5000 })]);
  it('blocks the interior of an outline however far its vertices are', () => {
    const centre = [-120.75, 50.25];
    eq(pointBlocked(outline, centre).who, 'X10001', 'deep inside, >25 km from any vertex');
  });
  it('blocks outside an outline within the distance, frees beyond it', () => {
    ok(pointBlocked(outline, [-120.4, 50.25]), 'about 7 km east of the edge: inside 30');
    eq(pointBlocked(outline, [-119.4, 50.25]), null, 'about 43 km east: outside 30');
    eq(pointBlocked(outline, [-121.6, 49.9]), null, 'far to the southwest');
  });
  it('blocks a path that crosses a region, either way round, and frees one that skirts it', () => {
    const through = pathBlocked(outline, [-122, 50.25], [-119.5, 50.25]);
    ok(through && through.who === 'X10001', 'a leg through the outline');
    eq(pathBlocked(outline, [-119.5, 50.25], [-122, 50.25]).who, 'X10001', 'symmetric');
    eq(pathBlocked(outline, [-122, 49], [-119.5, 49]), null, 'a leg well south');
    ok(pathBlocked(circle, [-120, 49.9], [-120, 50.1]), 'a pickup-to-fire leg over the point');
    eq(pathBlocked(circle, [-120, 51], [-119, 51]), null, 'a leg far north');
  });
  it('an empty region list blocks nothing', () => {
    eq(pathBlocked([], ll, [-119, 50]), null, 'free air');
    eq(pointBlocked([], ll), null, 'free point');
  });
});

describe('guard · noteKm', () => {
  it('names the widest distance among entries that forced people out, else the default', () => {
    eq(noteKm(loadGuard(DOC(), CTX)), 30, 'loss 30 over order 20 and a place at 15');
    const doc = DOC(); doc.defaultKeepOutKm = 40;
    eq(noteKm(loadGuard(doc, CTX)), 40, 'the default, when it is the widest');
    const quiet = DOC();
    quiet.fires = [{ fire: 'X10003', name: 'Gamma', tier: 3, basis: 'alert', keepOutKm: 5,
                     source: 'https://example.test/gamma' }];
    quiet.places = [];
    eq(noteKm(loadGuard(quiet, { seasonNumbers: ['X10003'] })), 10, 'an alert claims no widening');
    eq(noteKm(null), 0, 'no guard, no promise of distance');
  });
});
