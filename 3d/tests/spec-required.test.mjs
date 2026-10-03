import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { resolveClass, rawSpec, CLASS_IDS, ALT, MODES } from '../model/config.js?v=47195d1b';
import * as mission from '../anim/mission.js?v=47195d1b';
import { aeroForce } from '../physics/mass.js?v=47195d1b';
import { pumpPowerMW } from '../physics/energy.js?v=47195d1b';
import { createHose } from '../anim/hose.js?v=47195d1b';

const root = fileURLToPath(new URL('../', import.meta.url)).replace(/\/$/, '');
function sourceFiles(dir) {
  return readdirSync(dir, {withFileTypes:true}).flatMap(e => e.isDirectory()
    ? sourceFiles(`${dir}/${e.name}`) : e.name.endsWith('.js') ? [`${dir}/${e.name}`] : []);
}
const keys = [...new Set(CLASS_IDS.flatMap(id => Object.entries(rawSpec(id))
  .filter(([,v]) => typeof v === 'number').map(([k]) => k)))].join('|');
// Property names, rather than only `cls`, catch aliases and quoted bracket reads too.
const fallback = new RegExp(`(?:\\.\\s*(?:${keys})\\b|\\[\\s*['"](?:${keys})['"]\\s*\\]|specNumber\\([^)]*\\))\\s*\\)*\\s*(?:\\|\\||\\?\\?)\\s*[+-]?(?:\\d|\\.\\d)`, 'g');

test('no numeric default on a class field anywhere in 3d JavaScript', () => {
  const errors = [];
  for (const path of sourceFiles(root)) {
    const source = readFileSync(path,'utf8');
    for (const m of source.matchAll(fallback)) {
      errors.push(`${path.slice(root.length + 1)}:${source.slice(0,m.index).split('\n').length}: ${m[0]}`);
    }
  }
  assert.deepEqual(errors, []);
});

test('the fallback detector recognizes aliases, brackets and parenthesized reads', () => {
  for (const source of ['cls.cruiseKph || 90', 'vehicle["cruiseKph"] || 90',
    '(renamed.hoseLengthM) || 250', 'c.hoseDeployMin ?? 4', "specNumber(c, 'cruiseKph') || 90"]) {
    fallback.lastIndex = 0;
    assert.ok(fallback.test(source), source);
  }
});

test('every declared numeric class field rejects a missing or nonfinite override', () => {
  for (const id of CLASS_IDS) for (const [key,value] of Object.entries(rawSpec(id))) {
    if (typeof value !== 'number') continue;
    for (const missing of [undefined, null, NaN, Infinity, '90']) {
      assert.throws(() => resolveClass(id, {[key]:missing}), /required class field/,
        `${id}.${key}=${missing}`);
    }
  }
});

test('a missing spec fails at the animation, drag, pump and hose consumers', () => {
  for (const [key,consume] of [
    ['cruiseKph', c => mission.phaseShape(c,'OUTBOUND_TRANSIT',.5)],
    ['hoseDeployMin', c => mission.phaseDurations(c)],
    ['hoseRetractMin', c => mission.phaseDurations(c)],
    ['anchorCableM', c => mission.anchorAt(c,300)],
    ['nominalDiameterM', c => aeroForce(c,{airspeedMps:25})],
    ['fillRateM3s', c => pumpPowerMW(c)],
    ['hoseLengthM', c => createHose(c,{index:0,p:[0,0,0]})],
  ]) {
    const c = resolveClass('P100'); delete c[key];
    assert.throws(() => consume(c), new RegExp(`required class field ${key}`));
  }
});

test('mission constants and liquid density exports have a single home inside 3d', () => {
  assert.equal(mission.ALT, ALT); assert.equal(mission.MODES, MODES);
  const duplicates = [];
  for (const path of sourceFiles(root)) {
    if (path === `${root}/model/config.js`) continue;
    if (/\b(?:const|let|var)\s+(?:RHO_LN2|RHO_WATER|RHO_WORK|MODES|ALT)\s*=/.test(readFileSync(path,'utf8'))) {
      duplicates.push(path.slice(root.length + 1));
    }
  }
  assert.deepEqual(duplicates, []);
});
