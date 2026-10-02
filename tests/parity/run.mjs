import '../cases/spec-parity.cases.js';
import { runAll } from '../harness.js';
const r = runAll();
for (const suite of r.suites) for (const t of suite.tests) {
  if (t.status === 'fail') console.log(`FAIL ${t.name}\n${t.error}`);
}
console.log(`parity: ${r.pass} passed, ${r.fail} failed`);
process.exitCode = r.fail ? 1 : 0;
