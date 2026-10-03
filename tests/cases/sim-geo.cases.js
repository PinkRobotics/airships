/* Geometry, distance and easing.
 *
 * Small functions, but the map, the flown-leg estimate and every heading on the page are
 * built out of them, so the reference values below are real great-circle distances between
 * real places rather than round numbers chosen to make the test pass.
 */
import { close, describe, eq, it, ok } from '../harness.js';
import {
  CITIES, R_EARTH, bez, bezBearing, easeSm, easeTrap, havKm, lerpAng, moveToward, trackBearing,
} from '../../sim/index.js?v=acbad6ee';

const city = name => {
  const c = CITIES.find(q => q[2] === name);
  if (!c) throw new Error(`fixture: no city named ${name}`);
  return [c[0], c[1]];
};

const TWO_PI = Math.PI * 2;
const wrap = a => { let d = a % TWO_PI; if (d > Math.PI) d -= TWO_PI; if (d < -Math.PI) d += TWO_PI; return d; };
const deg = r => r * 180 / Math.PI;

describe('geo · havKm', () => {
  it('matches published great-circle distances between BC cities', () => {
    // Spherical earth, R = 6371 km. These agree with the usual published figures to well
    // under a kilometre; the ellipsoid correction at this latitude is smaller than that.
    close(havKm(city('Vancouver'), city('Kelowna')), 270.30, 0.05, 'Vancouver - Kelowna');
    close(havKm(city('Vancouver'), city('Kamloops')), 253.02, 0.05, 'Vancouver - Kamloops');
    close(havKm(city('Kelowna'), city('Kamloops')), 106.20, 0.05, 'Kelowna - Kamloops');
    close(havKm(city('Prince George'), city('Vancouver')), 516.57, 0.05, 'Prince George - Vancouver');
  });

  it('a degree of latitude is 111.19 km anywhere', () => {
    // R x pi/180. The model uses 110.57 for local metric conversions, which is the WGS84
    // value near 50 N; the difference is deliberate and lives in targets.js, not here.
    for (const lat of [0, 30, 49, 60, 80]) {
      close(havKm([-120, lat], [-120, lat + 1]), R_EARTH * Math.PI / 180, 1e-6, `at ${lat} N`);
    }
  });

  it('a degree of longitude shrinks with the cosine of latitude', () => {
    const atEquator = havKm([0, 0], [1, 0]);
    close(havKm([0, 60], [1, 60]) / atEquator, Math.cos(60 * Math.PI / 180), 1e-5, 'at 60 N');
  });

  it('is zero on itself and symmetric', () => {
    const a = city('Kelowna'), b = city('Nelson');
    eq(havKm(a, a), 0, 'distance to self');
    close(havKm(a, b), havKm(b, a), 1e-12, 'symmetry');
  });

  it('obeys the triangle inequality on a sample of the city list', () => {
    for (let i = 0; i < 12; i++) {
      const a = [CITIES[i][0], CITIES[i][1]];
      const b = [CITIES[(i + 5) % CITIES.length][0], CITIES[(i + 5) % CITIES.length][1]];
      const c = [CITIES[(i + 11) % CITIES.length][0], CITIES[(i + 11) % CITIES.length][1]];
      ok(havKm(a, c) <= havKm(a, b) + havKm(b, c) + 1e-9,
        `${CITIES[i][2]} -> ${CITIES[(i + 11) % CITIES.length][2]} via ${CITIES[(i + 5) % CITIES.length][2]}`);
    }
  });
});

describe('geo · moveToward', () => {
  it('goes nowhere on zero, and all the way on the full distance', () => {
    const a = city('Kamloops'), b = city('Kelowna');
    const d = havKm(a, b);
    close(havKm(moveToward(a, b, 0), a), 0, 1e-12, 'zero step');
    close(havKm(moveToward(a, b, d), b), 0, 1e-9, 'full step lands on the target');
  });

  it('interpolates linearly in degrees, which is not the same as linearly in kilometres', () => {
    // Honest about what it is: a lon/lat lerp with a kilometre-shaped argument. Over the
    // ~20 km hops it is used for the difference is metres, which is why it survives.
    const a = [-120, 50], b = [-119, 51];
    const mid = moveToward(a, b, havKm(a, b) / 2);
    close(mid[0], -119.5, 1e-12, 'longitude midpoint');
    close(mid[1], 50.5, 1e-12, 'latitude midpoint');
  });

  it('returns a copy when the two points coincide', () => {
    const a = [-120, 50];
    const r = moveToward(a, a.slice(), 5);
    ok(r !== a, 'returned the same array');
    eq(r[0], a[0], 'longitude'); eq(r[1], a[1], 'latitude');
  });
});

describe('geo · bez', () => {
  const p0 = [-120, 50], p1 = [-119.5, 50.4], p2 = [-119, 50.1];

  it('starts at p0 and ends at p2', () => {
    eq(bez(p0, p1, p2, 0)[0], p0[0], 'start longitude');
    eq(bez(p0, p1, p2, 0)[1], p0[1], 'start latitude');
    close(bez(p0, p1, p2, 1)[0], p2[0], 1e-12, 'end longitude');
    close(bez(p0, p1, p2, 1)[1], p2[1], 1e-12, 'end latitude');
  });

  it('at t = 0.5 is (p0 + 2 p1 + p2) / 4', () => {
    const m = bez(p0, p1, p2, 0.5);
    close(m[0], (p0[0] + 2 * p1[0] + p2[0]) / 4, 1e-12, 'longitude');
    close(m[1], (p0[1] + 2 * p1[1] + p2[1]) / 4, 1e-12, 'latitude');
  });

  it('degenerates to a straight line when the control point is the midpoint', () => {
    const mid = [(p0[0] + p2[0]) / 2, (p0[1] + p2[1]) / 2];
    for (const t of [0.1, 0.25, 0.5, 0.75, 0.9]) {
      const q = bez(p0, mid, p2, t);
      close(q[0], p0[0] + (p2[0] - p0[0]) * t, 1e-12, `longitude at t=${t}`);
      close(q[1], p0[1] + (p2[1] - p0[1]) * t, 1e-12, `latitude at t=${t}`);
    }
  });

  it('never leaves the convex hull of its three points', () => {
    const lo = Math.min(p0[1], p1[1], p2[1]), hi = Math.max(p0[1], p1[1], p2[1]);
    for (let i = 0; i <= 100; i++) {
      const q = bez(p0, p1, p2, i / 100);
      ok(q[1] >= lo - 1e-12 && q[1] <= hi + 1e-12, `latitude ${q[1]} outside [${lo}, ${hi}]`);
    }
  });
});

describe('geo · bearings', () => {
  it('trackBearing reads clockwise from north', () => {
    close(trackBearing([-120, 50], [-120, 51]), 0, 1e-9, 'due north');
    close(trackBearing([-120, 50], [-120, 49]), 180, 1e-9, 'due south');
    // Not 90 and 270: this is the INITIAL great-circle bearing, and a rhumb line due east
    // along 50 N starts 0.38 degrees north of east. That difference is real, not slop.
    close(trackBearing([-120, 50], [-119, 50]), 89.61697, 1e-4, 'due east');
    close(trackBearing([-120, 50], [-121, 50]), 270.38303, 1e-4, 'due west');
    for (let i = 0; i < 36; i++) {
      const b = trackBearing([-120, 50], [-120 + Math.sin(i) * 0.3, 50 + Math.cos(i) * 0.3]);
      ok(b >= 0 && b < 360, `bearing out of range: ${b}`);
    }
  });

  it('bezBearing on a straight segment points along it', () => {
    // Radians, clockwise from north, with longitude scaled by cos(lat) so the angle is the
    // one a map reader sees rather than the one raw degrees would give.
    const north = bezBearing([-120, 50], [-120, 50.5], [-120, 51], 0.5, 50);
    close(deg(north), 0, 1e-9, 'due north');
    const east = bezBearing([-120, 50], [-119.5, 50], [-119, 50], 0.5, 50);
    close(deg(east), 90, 1e-9, 'due east');
    const sw = bezBearing([-120, 50], [-120.5, 49.5], [-121, 49], 0.5, 50);
    ok(deg(sw) > -180 && deg(sw) < -90, `south-west came out as ${deg(sw)} degrees`);
  });

  it('bezBearing agrees with trackBearing over a short straight hop', () => {
    // 46.97 degrees against 46.92: bezBearing is the flat-earth angle at one stated
    // latitude, trackBearing the initial great-circle bearing. Over a 12 km hop they differ
    // by 0.06 degrees, which is the scale of the approximation the map is drawn with.
    const a = [-120, 50], b = [-119.9, 50.06];
    const mid = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2];
    const bz = (deg(bezBearing(a, mid, b, 0.5, 50)) + 360) % 360;
    close(bz, trackBearing(a, b), 0.1, 'bezBearing vs trackBearing');
  });
});

describe('geo · lerpAng', () => {
  it('is the identity at t = 0', () => {
    for (const a of [-3, -1, 0, 0.7, 2, 6]) for (const b of [-2, 0.4, 3]) {
      eq(lerpAng(a, b, 0), a, `lerpAng(${a}, ${b}, 0)`);
    }
  });

  it('takes the short way round: 350 degrees to 10 degrees passes through north', () => {
    const a = 350 * Math.PI / 180, b = 10 * Math.PI / 180;
    const half = lerpAng(a, b, 0.5);
    close(deg(wrap(half)), 0, 1e-9, 'the halfway heading is not north');
    ok(half > a, 'it turned the long way, anticlockwise through 180');
    close(deg(lerpAng(a, b, 1)) - 350, 20, 1e-9, 'the full turn is 20 degrees, not 340');
  });

  it('never turns further than 180 degrees, for any pair', () => {
    for (let i = 0; i < 200; i++) {
      const a = (i * 0.137) * TWO_PI - 5, b = (i * 0.311) * TWO_PI - 3;
      const swept = lerpAng(a, b, 1) - a;
      ok(Math.abs(swept) <= Math.PI + 1e-12, `swept ${deg(swept)} degrees from ${deg(a)} to ${deg(b)}`);
      close(wrap(lerpAng(a, b, 1) - b), 0, 1e-9, 'it did not arrive at b');
    }
  });

  it('is linear in t along the arc it chose', () => {
    const a = 2.9, b = -2.9;                       // across the +/- pi discontinuity
    const full = lerpAng(a, b, 1) - a;
    for (const t of [0, 0.25, 0.5, 0.75, 1]) close(lerpAng(a, b, t) - a, full * t, 1e-12, `t=${t}`);
    ok(Math.abs(full) < Math.PI, `it went the long way: ${deg(full)} degrees`);
  });

  it('at exactly 180 degrees the direction is arbitrary, which is why state.js counts turns instead', () => {
    // b - a = pi to the last bit: the two ways round are exactly equal in length, and which
    // one comes out depends on how (a + pi) - a rounded. The magnitude is still right, and
    // the WATER_RELEASE reversal — the only place a real 180 happens — does not call this
    // function at all. sim-state.cases.js asserts that reversal never flickers.
    for (const a of [0, 1, 2.5, -4, 7.3]) {
      const swept = lerpAng(a, a + Math.PI, 1) - a;
      close(Math.abs(swept), Math.PI, 1e-9, `magnitude of a ${a} rad reversal`);
    }
  });
});

describe('geo · easing', () => {
  it('easeTrap covers exactly the distance, start to finish', () => {
    eq(easeTrap(0), 0, 'at the start');
    close(easeTrap(1), 1, 1e-12, 'at the end');
    close(easeTrap(0.5), 0.5, 1e-12, 'symmetric about the middle');
  });

  it('easeTrap is monotone and inside [0, 1]', () => {
    let prev = -1;
    for (let i = 0; i <= 1000; i++) {
      const d = easeTrap(i / 1000);
      ok(d >= prev - 1e-12, `went backwards at p=${i / 1000}`);
      ok(d >= -1e-12 && d <= 1 + 1e-12, `out of range at p=${i / 1000}: ${d}`);
      prev = d;
    }
  });

  it('easeTrap really is a trapezoid: constant rate through the middle', () => {
    // 15% ramp each end by default, so between p = 0.15 and p = 0.85 the distance covered
    // per unit of p is constant at 1/0.85.
    const rate = (easeTrap(0.6) - easeTrap(0.4)) / 0.2;
    close(rate, 1 / 0.85, 1e-12, 'cruise rate');
    close((easeTrap(0.8) - easeTrap(0.5)) / 0.3, 1 / 0.85, 1e-12, 'still cruising');
    ok((easeTrap(0.05) - easeTrap(0)) / 0.05 < rate, 'the ramp in is not slower than the cruise');
  });

  it('easeTrap takes a ramp fraction', () => {
    close(easeTrap(0.5, 0.5), 0.5, 1e-12, 'a pure triangle is still symmetric');
    close(easeTrap(1, 0.5), 1, 1e-12, 'and still arrives');
  });

  it('easeSm is smoothstep', () => {
    eq(easeSm(0), 0, 'at 0');
    eq(easeSm(1), 1, 'at 1');
    close(easeSm(0.5), 0.5, 1e-12, 'at the middle');
    close(easeSm(0.25), 0.15625, 1e-12, 'at a quarter');
    let prev = -1;
    for (let i = 0; i <= 200; i++) { const v = easeSm(i / 200); ok(v >= prev, 'not monotone'); prev = v; }
  });
});
