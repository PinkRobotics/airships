/* The guard: the days and fires the simulated fleet must not touch.
 *
 * Every fixture here is invented — numbers that are no fire, places that are no town —
 * because what is under test is the RULE, not the 2026 list: that a guard which cannot be
 * read fails closed, that a listed fire is never a candidate whatever its status, that a
 * keep-out distance is measured against a fire's outline and not its centroid, and that
 * the window and the distances answer to the file, not to the code. The real file's own
 * pins (its digest, its window, its counts) are held by tests/guard/check.py, which is
 * where a deliberate edit to data/season/2026.guard.json is made to hurt.
 *
 * The derived evacuation record gets the same treatment: an invented record of X-numbers
 * holds the rule that an order takes the default distance and an alert only holds the
 * fire, that the stricter of a hand entry and the record wins and data never loosens the
 * list, that an order area is keep-out ground on its own, and that a record which cannot
 * be read is a refusal with the fleet down — never a quiet "no fires under order".
 */
import * as guardModel from '../../sim/guard.js?v=68694086';
const missionBlocked = (...args) => guardModel.missionBlocked(...args);
import { close, deepEq, describe, eq, it, ok } from '../harness.js';
import {
  dayKind, guardedFire, keepOutsFor, loadEvac, loadGuard, liveEvac, mergeEvac, noteKm,
  pathBlocked, pointBlocked,
} from '../../sim/index.js?v=68694086';

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
    { fire: 'X10006', name: 'The Nameless Fire', tier: 3, basis: 'alert', keepOutKm: 0,
      source: 'https://example.test/nameless' },
  ],
  places: [
    { name: 'A Town', ll: [-120.5, 50.5], date: '2030-09-01', basis: 'order', keepOutKm: 15,
      source: 'https://example.test/town' },
  ],
});
const CTX = { seasonNumbers: ['X10001', 'X10002', 'X10006'] };

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
    eq(G.byNumber.get('X10006').keepOutKm, 0, 'alert by number');
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
    doc.fires.push({ fire: 'X10006', name: 'the nameless fire', tier: 3, basis: 'alert', keepOutKm: 0,
                     source: 'https://example.test/two' });
    ok(!loadGuard(doc, CTX).ok, 'a number listed twice is refused');
  });

  it('refuses a listed number that no season record and no view carries (R6)', () => {
    const G = loadGuard(DOC(), { seasonNumbers: ['X10002'] });
    ok(!G.ok && /X10001 .*cannot be resolved/.test(G.reason), G.reason);
    // without seasonNumbers the resolution check is skipped: the guard still loads
    ok(loadGuard(DOC(), {}).ok, 'no season context: the check is skipped, not failed');
    const G2 = loadGuard(DOC(), { seasonNumbers: ['X99999'],
                                  viewFires: [fire({ id: 'X10001' }), fire({ id: 'X10002' }), fire({ id: 'X10006' })] });
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
  it('holds a listed fire by number, at the entry\'s own distance', () => {
    eq(guardedFire(G, fire({ id: 'X10001', name: 'Alpha' })).why, 'listed', 'by number');
    eq(guardedFire(G, fire({ id: 'X10001', name: 'Alpha' })).keepOutKm, 30, 'tier 1 distance');
    const byName = guardedFire(G, fire({ id: 'X10006', name: 'THE NAMELESS FIRE' }));
    eq(byName.why, 'listed', 'matched by number');
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
    const fires = [fire({ id: 'X10006', name: 'The Nameless Fire' }), fire({ id: 'X10002', name: 'Beta' })];
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

/* ---------- the derived evacuation record: same rules, invented record ------ */

/* Order-area outlines, far from every fixture fire above. RING_A spans roughly
   [-121.4, -121.3] × [50.9, 51.0]; RING_B is a small patch around [-120.15, 50.15]. */
const RING_A = [[-121.4, 50.9], [-121.4, 51.0], [-121.3, 51.0], [-121.3, 50.9], [-121.4, 50.9]];
const RING_B = [[-120.2, 50.1], [-120.2, 50.2], [-120.1, 50.2], [-120.1, 50.1], [-120.2, 50.1]];

const EVAC = () => ({
  season: 2030,
  fires: [
    // on the hand list at 30 km (loss): the record's order must not loosen it
    { fire: 'X10001', everOrder: true, everAlert: false, firstSeen: '2030-08-01',
      lastSeen: '2030-08-09', orderOutlines: [RING_A] },
    // on the hand list at 20 km (order): the record holds only an alert, 0 km
    { fire: 'X10002', everOrder: false, everAlert: true, firstSeen: '2030-08-02',
      lastSeen: '2030-08-03', orderOutlines: [] },
    // in the record only, under an order that published no geometry
    { fire: 'X10003', everOrder: true, everAlert: false, firstSeen: '2030-08-04',
      lastSeen: '2030-08-04', orderOutlines: [] },
    // on the hand list at 5 km: the record's order at the 10 km default tightens it
    { fire: 'X10004', everOrder: true, everAlert: true, firstSeen: '2030-08-05',
      lastSeen: '2030-08-06', orderOutlines: [RING_B] },
    // on the hand list at exactly the default: a tie, and the hand entry keeps its words
    { fire: 'X10005', everOrder: true, everAlert: false, firstSeen: '2030-08-07',
      lastSeen: '2030-08-08', orderOutlines: [RING_A] },
    // in the record only, alert alone: held, and claims no air
    { fire: 'X19999', everOrder: false, everAlert: true, firstSeen: '2030-09-01',
      lastSeen: '2030-09-02', orderOutlines: [] },
  ],
});

/* The hand list of DOC() plus the two entries the precedence cases need: Delta at 5 km
   (the record widens it to the default) and Epsilon at exactly the default (the tie). */
const WITH_EVAC = () => {
  const doc = DOC();
  doc.fires.push({ fire: 'X10004', name: 'Delta', tier: 2, basis: 'order', keepOutKm: 5,
                   source: 'https://example.test/delta' });
  doc.fires.push({ fire: 'X10005', name: 'Epsilon', tier: 2, basis: 'order', keepOutKm: 10,
                   source: 'https://example.test/epsilon' });
  return doc;
};
const CTX4 = { seasonNumbers: ['X10001', 'X10002', 'X10004', 'X10005', 'X10006'] };

describe('guard · loadEvac', () => {
  it('accepts a well-formed record and carries its orders', () => {
    const E = loadEvac(EVAC());
    ok(E.ok, `expected ok, got reason: ${E.reason}`);
    eq(E.byNumber.size, 6, 'one entry per fire');
    eq(E.orders.length, 3, 'one per order outline: X10001, X10004, X10005');
    deepEq(E.orders.map(o => o.who), ["X10001's evacuation order area",
                                      "X10004's evacuation order area",
                                      "X10005's evacuation order area"], 'each names its fire');
    deepEq(E.orders[0].ring, RING_A, 'the outline is carried as given, unsimplified');
    eq(E.byNumber.get('X10003').orderOutlines.length, 0, 'an order with no geometry is fine');
  });
  it('refuses a record that is not what it says', () => {
    const bend = (fn) => { const doc = EVAC(); fn(doc); return loadEvac(doc); };
    for (const [name, fn] of [
      ['not an object', () => null],
      ['an array', () => []],
      ['no fires list', d => { delete d.fires; }],
      ['an entry that is not an object', d => { d.fires[0] = null; }],
      ['a number that is not a string', d => { d.fires[0].fire = 10001; }],
      ['digits with no letter', d => { d.fires[0].fire = '10001'; }],
      ['an empty number', d => { d.fires[0].fire = ''; }],
      ['a number listed twice', d => { d.fires[1].fire = 'X10001'; }],
      ['everOrder as a string', d => { d.fires[0].everOrder = 'true'; }],
      ['under neither an order nor an alert', d => { d.fires[2].everOrder = false; }],
      ['dates out of order', d => { d.fires[0].lastSeen = '2030-07-31'; }],
      ['a date that is not YYYY-MM-DD', d => { d.fires[0].firstSeen = '2030-8-1'; }],
      ['orderOutlines missing', d => { delete d.fires[0].orderOutlines; }],
      ['outlines without ever an order', d => { d.fires[1].orderOutlines = [RING_A]; }],
      ['a ring that is not closed', d => { d.fires[0].orderOutlines = [[[-121.4, 50.9],
        [-121.4, 51.0], [-121.3, 51.0], [-121.3, 50.9]]]; }],
      ['a ring of three points', d => { d.fires[0].orderOutlines = [[[-121.4, 50.9],
        [-121.35, 51.0], [-121.4, 50.9]]]; }],
      ['a ring with a string coordinate', d => { d.fires[0].orderOutlines = [[[-121.4, '50.9'],
        [-121.4, 51.0], [-121.3, 51.0], [-121.3, 50.9], [-121.4, 50.9]]]; }],
    ]) {
      const E = typeof fn === 'function' && fn.length === 1 ? bend(fn) : loadEvac(fn());
      ok(!E.ok, `${name}: expected a refusal`);
      eq(E.byNumber.size, 0, `${name}: a refused record holds nothing`);
      eq(E.orders.length, 0, `${name}: and claims no orders`);
    }
  });
  it('a malformed record stands the guard down and says so in words, not a fleet', () => {
    const broken = loadEvac({ fires: 3 });
    const G = loadGuard(DOC(), { ...CTX4, evac: broken });
    ok(!G.ok && /evacuation record cannot be read/.test(G.reason), G.reason);
    const k = dayKind(G, '2030-09-01');
    ok(!k.fleet && /evacuation record/.test(k.reason), k.reason);
    deepEq(keepOutsFor(G, [fire()]), [], 'no regions are drawn from a refused record');
    eq(guardedFire(G, fire()).why, 'guard-down', 'and every fire answers guard-down');
    ok(!loadGuard(DOC(), { evac: {} }).ok, 'ctx.evac that is not a loadEvac state is refused');
  });
  it('a guard with no evacuation record is the guard it always was', () => {
    const G = loadGuard(DOC(), CTX);
    ok(G.ok && !G.evac, 'no ctx.evac, no evac on the state');
    eq(guardedFire(G, fire({ id: 'X10001', name: 'Alpha' })).why, 'listed', 'unchanged');
  });
});

describe('guard · guardedFire with the evacuation record', () => {
  const G = loadGuard(WITH_EVAC(), { ...CTX4, evac: loadEvac(EVAC()) });
  const read = (over) => {
    const g = guardedFire(G, fire(over));
    return g && [g.why, g.tier, g.basis, g.keepOutKm];
  };
  it('an order takes the default distance; an alert alone holds the fire and claims no air', () => {
    deepEq(read({ id: 'X10003', name: 'Nowhere' }), ['evac', 2, 'order', 10],
           'a fire the record holds under an order, on no hand list');
    deepEq(read({ id: 'X19999', name: 'Nowhere' }), ['evac', 3, 'alert', 0],
           'a fire the record holds under an alert alone');
  });
  it('the stricter of the hand entry and the record wins, and a tie keeps the hand entry', () => {
    deepEq(read({ id: 'X10004', name: 'Delta' }), ['evac', 2, 'order', 10],
           'the record tightened a 5 km hand entry to the default');
    deepEq(read({ id: 'X10001', name: 'Alpha' }), ['listed', 1, 'loss', 30],
           'the record never loosens a 30 km hand entry');
    deepEq(read({ id: 'X10002', name: 'Beta' }), ['listed', 2, 'order', 20],
           'an alert in the record, 0 km, does not loosen a 20 km hand entry');
    deepEq(read({ id: 'X10005', name: 'Epsilon' }), ['listed', 2, 'order', 10],
           'a tie at the default keeps the hand entry, its tier and its words');
  });
  it('the record outranks the day\'s own of-note flag, as the hand list does', () => {
    deepEq(read({ id: 'X19999', note: true }), ['evac', 3, 'alert', 0],
           'held by the record before of-note is even asked');
    deepEq(read({ id: 'X10003', note: true }), ['evac', 2, 'order', 10],
           'same, under an order');
    deepEq(read({ id: 'X18888' }), null, 'a fire in neither record and flagged by nothing is free');
  });
});

describe('guard · keepOutsFor order areas', () => {
  const G = loadGuard(WITH_EVAC(), { ...CTX4, evac: loadEvac(EVAC()) });
  const areas = keepOutsFor(G, [], {}, null);
  it('carries every order outline on every view, whatever is in it', () => {
    eq(areas.length, 3, 'three outlines: X10001, X10004 and X10005');
    ok(areas.every(r => r.kind === 'evac-order' && r.rKm === 0 && r.ring && r.edge),
       'each is its own ground: the outline is the boundary, no buffer');
  });
  it('blocks a point inside an area and a path crossing it, and frees what is outside', () => {
    eq(pointBlocked(areas, [-121.35, 50.95]).who, "X10001's evacuation order area",
       'inside RING_A');
    eq(pointBlocked(areas, [-120.15, 50.15]).who, "X10004's evacuation order area",
       'inside RING_B');
    eq(pointBlocked(areas, [-121.45, 50.95]), null,
       'about 4 km outside the outline is free: the outline itself is the boundary');
    eq(pathBlocked(areas, [-121.6, 50.95], [-121.0, 50.95]).who,
       "X10001's evacuation order area", 'a leg through the area');
    eq(pathBlocked(areas, [-121.6, 51.5], [-121.0, 51.5]), null, 'a leg well north');
  });
  it('a data-order fire in view carries its band beside its order area; an alert claims no air', () => {
    const withFire = keepOutsFor(G, [fire({ id: 'X10003', ll: [-119.5, 49.5] })], {}, null);
    eq(withFire.length, 4, 'the fire\'s own band and three order areas');
    const band = withFire.find(r => r.kind === 'fire');
    deepEq([band.why, band.rKm > 10], ['evac', true],
           'held by the record, at the default plus its radius');
    eq(keepOutsFor(G, [fire({ id: 'X19999' })], {}, null).length, 3,
       'an alert-only fire contributes no band of its own');
  });
});

describe('guard · mergeEvac and liveEvac', () => {
  const seasonDoc = { fires: [{ fire: 'X10003', everOrder: true, everAlert: false,
                                firstSeen: '2030-08-04', lastSeen: '2030-08-05',
                                orderOutlines: [RING_A] }] };
  const season = () => loadEvac(seasonDoc);
  const liveDoc = () => ({ fires: [
    { fire: 'X10003', everOrder: false, everAlert: true, firstSeen: '2030-09-01',
      lastSeen: '2030-09-01', orderOutlines: [] },
    { fire: 'X10050', everOrder: true, everAlert: false, firstSeen: '2030-09-01',
      lastSeen: '2030-09-01', orderOutlines: [RING_B] }] });
  it('unions two records, and only ever widens', () => {
    const m = mergeEvac(season(), loadEvac(liveDoc()));
    ok(m.ok, m.reason);
    const x = m.byNumber.get('X10003');
    deepEq([x.everOrder, x.everAlert], [true, true],
           'the live alert is added; the order the record already held is not rescinded away');
    deepEq([x.firstSeen, x.lastSeen], ['2030-08-04', '2030-09-01'], 'first and last across both');
    eq(m.byNumber.get('X10050').orderOutlines.length, 1, 'a fire only the live copy names is kept');
    eq(m.orders.length, 2, 'RING_A and RING_B');
  });
  it('keeps a ring both records carry identically once, and never narrows', () => {
    const live = liveDoc();
    live.fires[0].everOrder = true;        // a live copy that repeats the order, same outline
    live.fires[0].orderOutlines = [RING_A];
    const m = mergeEvac(season(), loadEvac(live));
    eq(m.byNumber.get('X10003').orderOutlines.length, 1, 'the same outline, once');
    const shrunk = mergeEvac(loadEvac(liveDoc()), season());   // either way round
    eq(shrunk.byNumber.get('X10003').everOrder, true, 'the union is order-independent');
  });
  it('a state that did not load merges with nothing: the refusal stands', () => {
    const bad = loadEvac({ fires: 3 });
    eq(mergeEvac(season(), bad), bad, 'a bad live copy is returned untouched');
    eq(mergeEvac(bad, season()), bad, 'a bad base is returned untouched');
  });
  it('a missing live copy keeps the season record — never "no orders"', () => {
    const r = liveEvac(season(), null);
    deepEq([r.from, r.state.ok, r.state.byNumber.has('X10003')], ['season', true, true],
           'the season state, exactly as it was');
  });
  it('an unreadable live copy is a refusal, not a fallback', () => {
    const r = liveEvac(season(), { fires: 3 });
    deepEq([r.from, r.state.ok], ['unreadable', false], 'the refusal comes back');
    ok(/evacuation record/.test(r.state.reason), r.state.reason);
  });
  it('a good live copy widens the season record and says where it came from', () => {
    const r = liveEvac(season(), liveDoc());
    deepEq([r.from, r.state.ok, r.state.byNumber.has('X10050')], ['live', true, true],
           'merged, from the live copy');
  });
});

describe('guard · identity regressions', () => {
  it('normalises numbers on both sides of the join', () => {
    ok(loadGuard(DOC(), {seasonNumbers:new Set(CTX.seasonNumbers),seasonOfNote:new Set()}).ok, 'set context');
    const doc = DOC(); doc.fires[0].fire = ' x10001 ';
    const g = loadGuard(doc, CTX);
    ok(g.ok, g.reason);
    for (const id of ['X10001', 'x10001', ' X10001 '])
      eq(guardedFire(g, fire({id})).why, 'listed', id);
    const evac = EVAC(); evac.fires[0].fire = ' x10001 ';
    ok(loadEvac(evac).byNumber.has('X10001'), 'evacuation load normalises too');
    eq(guardedFire(g, fire({id:' va1981 '})), null, 'two-letter record identity is valid');
    for (const id of ['12345', 'X1', 'X100001', '', null])
      eq(guardedFire(g, fire({id})).why, 'invalid-fire', String(id));
  });
  it('null refuses in words instead of throwing', () => {
    const r = guardedFire(loadGuard(DOC(), CTX), null);
    eq(r.why, 'invalid-fire'); ok(r.reason.includes('fire number'), r.reason);
  });
  it('has no name fallback and refuses a nameless-number entry', () => {
    const doc = DOC(); delete doc.fires[0].fire;
    ok(!loadGuard(doc, CTX).ok, 'a name alone is not an identity');
    const g = loadGuard(DOC(), CTX);
    ok(!('byName' in g), 'no dead fallback index');
    eq(guardedFire(g, fire({id:'X99999',name:'Alpha'})), null, 'a shared name grants no match');
  });
});

describe('guard · every flown position', () => {
  const region = (ll,rKm=1) => [{kind:'test',who:'invented exclusion',ll,rKm,edge:null,ring:null}];
  const m = () => ({intake:[-120,50],delivery:[-119,50],stations:[[-120,50]],
    targets:[[-119,50]],segs:[[[-119,49.98],[-119,50.02]]],heat:false});
  it('refuses a drop endpoint even when the centre clears', () => {
    const x=m(), rs=region(x.segs[0][1],.2);
    eq(pointBlocked(rs,x.delivery),null,'centre clear');
    ok(missionBlocked(rs,x),'endpoint blocks');
  });
  it('refuses the widest point of the bowed outbound track', () => {
    const x=m(); x.segs=[[x.delivery,x.delivery]];
    const rs=region([-119.5,50.045],.2);
    eq(pathBlocked(rs,x.intake,x.delivery),null,'straight line clear');
    ok(missionBlocked(rs,x),'actual bow blocks');
  });
  it('covers the whole cycle jitter envelope without changing the mission', () => {
    const x=m(), before=JSON.stringify(x), rs=region([-118.996,50.026],.15);
    eq(pointBlocked(rs,x.segs[0][1]),null,'base endpoint clear');
    ok(missionBlocked(rs,x),'future shifted endpoint blocks');
    eq(JSON.stringify(x),before,'no clipping or nudging');
    eq(missionBlocked(region([-122,50]),x),null,'clear mission passes');
  });
});
