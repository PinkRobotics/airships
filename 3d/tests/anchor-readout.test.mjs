import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import test from 'node:test';
import {CLASSES, MODES, planCycle, drawAt, WINCH_MPS} from '../../sim/index.js';

const panel = readFileSync('app/cockpit/panels.js', 'utf8');
test('the cockpit labels the cable flag as deployment and installed length separately', () => {
  assert.equal(panel.includes('"anchor deployment", "hose deployment"'), true,
    'the two deployment indicators need percentage labels');
  assert.equal(panel.includes('100, v => fmt(v) + "%"'), true,
    'the deployment reading visibly carries its percentage unit');
  assert.equal(panel.includes('m installed cable'), true, 'the constant cable length is installed');
  assert.equal(/(?:line out|m of cable)/i.test(panel), false, 'a flag cannot claim metres out');
  assert.equal(/anchorCableOut[^\n]*\*[^\n]*anchorM/.test(panel), false,
    'deployment must not be multiplied into a measured length');
});

test('the transition probe remains a flag and the panel never displays it as winch metres', () => {
  for (const cls of Object.values(CLASSES)) {
    const plan = planCycle(cls, MODES.balanced, 60, null, {basis: 'record'});
    const seconds = plan.dur.SOURCE_APPROACH * 60;
    const at = t => drawAt(cls, MODES.balanced, plan, 'SOURCE_APPROACH', t / seconds);
    let lo = 0, hi = seconds;
    assert.ok(at(hi).anchor.cableP > 0);
    for (let i = 0; i < 60; i++) {
      const mid = (lo + hi) / 2;
      if (at(mid).anchor.cableP > 0) hi = mid; else lo = mid;
    }
    const before = at(hi - 0.01).anchor.cableP, after = at(hi + 0.01).anchor.cableP;
    assert.ok((after - before) * cls.anchorM / 0.02 > WINCH_MPS,
      'this deliberately coarse state is still a deployment flag');
    assert.equal(panel.includes('gGen.set((st.anchorCableOut || 0) * 100, hoseOut * 100)'), true,
      'the flag transition must be displayed in percent');
  }
});
