import { test } from 'node:test';
import assert from 'node:assert/strict';
import { readWind, windForMission, WIND_MAX_AGE_MS } from '../../app/wind.js?v=eae942b2';

const now = Date.parse('2026-10-02T02:30:00Z');
const doc = () => ({ fetchedAt: '2026-10-02T02:20:00Z', data: {
  forecastAt: '2026-10-02T02:00:00Z', lats: [50, 54], lons: [-128, -124],
  vectors: [[10, 20], [30, 20], [10, 40], [30, 40]],
} });
const mission = { intake: [-128, 50], delivery: [-124, 54], bearing: 123 };
test('bilinear wind at mission midpoint, in km/h and meteorological from direction', () => {
  const w = windForMission(readWind(doc(), now), mission);
  assert.equal(w.spd, Math.hypot(20, 30));
  assert.equal(w.bearing, 123);
  assert.ok(Math.abs(w.dir - 213.69006752598) < 1e-9);
});
test('opposing east/west components cancel across north', () => {
  const d = doc(); d.data.vectors = [[-1, -10], [1, -10], [-1, -10], [1, -10]];
  const w = windForMission(readWind(d, now), mission);
  assert.equal(w.dir, 0); assert.equal(w.spd, 10);
});
test('missing, stale, future, malformed wind is refused', () => {
  assert.throws(() => readWind(null, now));
  const stale = doc(); stale.fetchedAt = new Date(now - WIND_MAX_AGE_MS).toISOString();
  assert.throws(() => readWind(stale, now), /stale/);
  const future = doc(); future.fetchedAt = new Date(now + 600001).toISOString();
  assert.throws(() => readWind(future, now), /future/);
  const malformed = doc(); malformed.data.vectors[0][0] = null;
  assert.throws(() => readWind(malformed, now), /malformed/);
  const oldForecast = doc(); oldForecast.data.forecastAt = '2026-10-01T00:00:00Z';
  assert.throws(() => readWind(oldForecast, now), /stale/);
});
test('edge samples work; outside grid is refused instead of extrapolating', () => {
  const g = readWind(doc(), now);
  assert.equal(windForMission(g, { intake: [-124, 54], delivery: [-124, 54] }).spd, 50);
  assert.throws(() => windForMission(g, { intake: [-140, 60], delivery: [-140, 60] }), /outside/);
});
