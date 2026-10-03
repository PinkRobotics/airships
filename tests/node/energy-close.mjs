import {collect,runAll} from '../harness.js';
await import('../cases/energy-closure.cases.js');
const r=runAll();
for(const s of r.suites)for(const t of s.tests)console.log(`${t.status.toUpperCase()} ${t.name}${t.error?' — '+t.error:''}`);
console.log(`${r.pass} passed, ${r.fail} failed; ${r.ms.toFixed(0)} ms`);
process.exitCode=r.fail?1:0;
