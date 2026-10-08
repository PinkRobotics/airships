"""Execute the real fallback dump against delayed planning and a virtual clock.

The clock starts at the producer's 18-second navigation sample. A loaded
planner completes later; no wall-clock sleep or CPU saturation is needed in
the fast gate. Real Chromium contention is checked separately before landing.
"""
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[2]
HARNESS = r"""
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

const source = fs.readFileSync(process.argv[2], 'utf8');
const scenario = process.argv[3];
async function capture({handleAt = 0, settleAt = 0, readyAt = 0,
                        invalid = false} = {}) {
  let now = 18000, ticks = 0;
  const cls = {id: 'P100', name: 'P-100', payloadT: 100, lenM: 52, diaM: 20};
  const fire = {id: 'EXTEST', name: 'Invented test fire', sizeHa: 40,
                status: 'Out of Control'};
  const plan = {tph: 87, cycleMin: 49, retainedT: 29, deliveredT: 71};
  const mission = {name: 'Test hull', cls, fire, legKm: 19.3, wind: null,
                   selection: {}, water: [0, 0, 34], mode: {id: 'test', label: 'Test'}};
  fire.mission = mission;
  const state = {missions: [mission], fires: [fire], planning: {},
                 day: 'exercise', snapshotDate: null, tier: 'exercise', uncovered: 0};
  const sim = {CLASSES: {P100: cls}, CLASS_ORDER: ['P100'],
               HULL_NAMES: {P100: ['Test hull']}, REFERENCE_CLASS: 'P100',
               FEASIBILITY_SCOPE: 'Conditional test fixture',
               srcName: () => 'Test lake', diagnosticNotes: () => [],
               missionReady: m => !m.idle && !!m.plan,
               auditServedPlan: () => {if (invalid) throw new Error('invalid served plan');}};
  const window = {};
  function progress() {
    state.ready = now >= readyAt;
    state.planning.state = now >= settleAt ? 'settled' : 'pending';
    mission.idle = now < settleAt;
    mission.plan = now >= settleAt ? plan : null;
    if (now >= handleAt) window.AIRSHIPS = {app: state, sim};
  }
  progress();
  const context = {window, performance: {now: () => now},
    document: {querySelector: () => ({innerHTML: 'Test diagnostic'}),
               getElementById: id => ({textContent: id})},
    setTimeout(callback, delay) {
      if (++ticks > 1000) throw new Error('regression callback limit');
      queueMicrotask(() => {now += delay; progress(); callback();});
    }};
  const value = await vm.runInNewContext(source, context, {timeout: 2000});
  return {value: JSON.stringify(value), now, ticks};
}

if (scenario === 'loaded') {
  const baseline = await capture();
  const loaded = await capture({settleAt: 23000, readyAt: 23000});
  assert.ok(loaded.now >= 23000, 'must wait beyond the 18-second sample');
  assert.equal(loaded.value, baseline.value, 'settled figures must be unchanged');
} else if (scenario === 'late-handle') {
  const result = await capture({handleAt: 20000, settleAt: 26000, readyAt: 26000});
  assert.ok(result.now >= 26000);
  assert.equal(result.value, (await capture()).value);
} else if (scenario === 'not-ready') {
  const result = await capture({readyAt: 23000});
  assert.ok(result.now >= 23000, 'settled planning alone is not page readiness');
} else if (scenario === 'never-ready') {
  await assert.rejects(capture({settleAt: Infinity, readyAt: Infinity}),
                       /readiness deadline exceeded/);
} else if (scenario === 'invalid-plan') {
  await assert.rejects(capture({settleAt: 23000, readyAt: 23000, invalid: true}),
                       /invalid served plan/);
} else {
  throw new Error('unknown scenario');
}
console.log(scenario + ': PASS');
"""


class FallbackReadiness(unittest.TestCase):
    def check(self, scenario):
        result = subprocess.run(
            ['node', '--input-type=module', '-', str(ROOT / 'tools/fallback_dump.js'), scenario],
            input=HARNESS, text=True, capture_output=True, timeout=10,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_loaded_planning_finishes_after_navigation_sample(self):
        self.check('loaded')

    def test_read_handle_arrives_after_navigation_sample(self):
        self.check('late-handle')

    def test_settled_planning_still_requires_page_readiness(self):
        self.check('not-ready')

    def test_never_ready_page_refuses_instead_of_emitting_partial_figures(self):
        self.check('never-ready')

    def test_invalid_served_plan_remains_an_error_after_readiness(self):
        self.check('invalid-plan')


if __name__ == '__main__':
    unittest.main()
