/* The CI runner.
 *
 * Same assertions as tests/browser/index.html: the cases register themselves with the
 * harness at import time, and this file re-emits them into node:test so that a failure
 * lands in the place CI already knows how to read.
 *
 *   node --test tests/node/run.mjs        (node 18+; no dependencies, no install step)
 *   node tests/node/run.mjs               (also works — node:test runs standalone)
 *
 * Outcomes are decided by harness.runTest, not by node, so that "known failure" means the
 * same thing in both runners: a test expected to fail against an open defect, which is
 * reported as an error the moment it starts passing.
 */
import { describe as nodeDescribe, it as nodeIt } from 'node:test';
import { collect, runTest } from '../harness.js';

await import('../cases/sim-atmosphere.cases.js');
await import('../cases/sim-physics.cases.js');
await import('../cases/sim-plan.cases.js');
await import('../cases/sim-state.cases.js');
await import('../cases/sim-energy.cases.js');
await import('../cases/sim-determinism.cases.js');
await import('../cases/sim-config.cases.js');
await import('../cases/sim-geo.cases.js');
await import('../cases/spec-parity.cases.js');
await import('../cases/anchor-parity.cases.js');
await import('../cases/sim-heat.cases.js');
await import('../cases/guard.cases.js');

const suites = collect();
if (!suites.length) throw new Error('no tests were collected — check the import list in tests/node/run.mjs');

const tally = { pass: 0, fail: 0, known: 0 };
const ran = [];

for (const suite of suites) {
  nodeDescribe(suite.name, () => {
    for (const test of suite.tests) {
      nodeIt(test.name, () => {
        ran.push(suite.name + ' › ' + test.name);
        const r = runTest(test);
        tally[r.status]++;
        if (r.status === 'fail') {
          const e = new Error(r.error);
          e.stack = r.stack || e.stack;
          throw e;
        }
        if (r.status === 'known') {
          // Not a failure: an expected one. Recorded on stderr so the log still says which
          // defects the suite is currently carrying.
          process.stderr.write(`  known failure (${r.known}): ${suite.name} › ${test.name}\n`);
        }
      });
    }
  });
}

process.on('exit', () => {
  console.log('TEST_INVENTORY shared ' + JSON.stringify({names: ran.sort()}));
  process.stderr.write(
    `\nharness: ${tally.pass} passed, ${tally.fail} failed, ${tally.known} known-failing ` +
    `across ${suites.length} suites\n`);
});
