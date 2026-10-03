import {runAll} from '../harness.js';
await import('../cases/energy-profile.cases.js');
const r=runAll();
for(const s of r.suites)for(const t of s.tests)console.log(`${t.status.toUpperCase()} ${t.name}${t.error?' '+t.error:''}`);
process.exitCode=r.fail?1:0;
