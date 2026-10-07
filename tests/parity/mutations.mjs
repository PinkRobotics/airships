// Bounded break-the-code checks. Every mutation is made in a disposable copy of sim/, 3d/ and tests/
// under TMPDIR, made once per run and removed at the end (also on SIGINT, SIGTERM and SIGHUP), and the
// runners execute there. No tracked file is written, so an interrupted run leaves the tree as it was.
// Within the copy each mutated file is still restored in finally, so the mutations stay independent.
// The closing green check runs on the real tree and only reads it.
import { readFileSync, writeFileSync, mkdtempSync, cpSync, rmSync, statSync } from 'node:fs';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const root = fileURLToPath(new URL('../../', import.meta.url));
if (!process.env.TMPDIR) throw new Error('Set TMPDIR to project scratch before testing');
const scratch = mkdtempSync(join(process.env.TMPDIR, 'parity-mutations-'));
const copy = scratch + '/';
function cleanup() { rmSync(scratch, { recursive: true, force: true }); }
process.on('exit', cleanup);   // also runs after a thrown error and after the handlers below
// spawnSync blocks the event loop, so run() yields to it after every child: a signal is then handled
// within one child's run time (tens of milliseconds) and ends the process through the exit hook above.
const yieldToLoop = () => new Promise(resolve => setImmediate(resolve));
const signalCodes = { SIGINT: 130, SIGTERM: 143, SIGHUP: 129 };
for (const [name, code] of Object.entries(signalCodes)) {
  process.on(name, () => process.exit(code));
}
// Ctrl-C or a cancelled job signals the whole process group, so a child usually dies first. A child
// ended by a signal is an interrupt, never a caught or missed mutation.
function interrupted(r) {
  if (!r.signal) return;
  console.error(`interrupted: a child run ended by ${r.signal}`);
  process.exit(signalCodes[r.signal] ?? 1);
}
const { version } = JSON.parse(readFileSync(new URL('../../sim/version.json', import.meta.url), 'utf8'));
if (typeof version !== 'string' || !/^[0-9a-f]{8}$/.test(version)) {
  throw new Error('sim/version.json must contain an eight-digit hexadecimal version stamp');
}
const configURL = `./sim/config.js?v=${version}`;
// Only source the runners import or scan: directories, .js, .mjs and .json under these three trees.
for (const dir of ['sim', '3d', 'tests']) {
  cpSync(root + dir, copy + dir, { recursive: true,
    filter: src => statSync(src).isDirectory() || /\.(m?js|json)$/.test(src) });
}
const parity = ['tests/parity/run.mjs'];
const required = ['--test','3d/tests/spec-required.test.mjs'];
let count = 0;
async function run(args, expected, name) {
  const r = spawnSync(process.execPath,args,{cwd:copy,encoding:'utf8'});
  interrupted(r);
  const output = r.stdout + r.stderr;
  if (r.error || r.status !== 1 || !output.includes(expected)) {
    throw new Error(`${name}: expected exit 1 containing ${expected}; got ${r.status}\n${output}`);
  }
  console.log(`RED ${++count} ${name}: exit ${r.status}; ${expected}`);
  await yieldToLoop();
}
async function change(name,path,from,to,expected,args=parity) {
  const full = copy+path, before = readFileSync(full,'utf8');
  if (!before.includes(from)) throw new Error(`mutation target not found: ${name}`);
  try { writeFileSync(full,before.replace(from,to)); await run(args,expected,name); }
  finally { writeFileSync(full,before); }
}
async function modelMutation(name,mutation,expected) {
  // In-memory mutation exercises the sim side; the copy's modules are imported, never the real tree's.
  await run(['--input-type=module','-e',
    `const m = await import(${JSON.stringify(configURL)}); ${mutation}; await import('./tests/parity/run.mjs');`],expected,name);
}
await modelMutation('new sim scalar','m.CLASSES.P100.unreviewed = 17','unpaired sim.unreviewed');
await modelMutation('new sim numeric table','m.CLASSES.P100.unreviewed = {row:[17,18]}','unpaired sim.unreviewed.row.0');
await modelMutation('missing sim partner','delete m.CLASSES.P100.cruiseKph','missing numeric partner: sim.cruiseKph=undefined');
await change('unreasoned exemption','tests/cases/spec-parity.cases.js',
  "'Source eligibility belongs to the mission planner, not the standalone drawing.'", "''", 'unpaired sim.minSourceHa');
const config='3d/model/config.js';
await change('new viewer scalar',config,'    payloadTonnes: 100,','    unreviewed: 17,\n    payloadTonnes: 100,','unpaired 3d.unreviewed');
await change('new viewer numeric table',config,'    payloadTonnes: 100,','    unreviewed: {row:[17,18]},\n    payloadTonnes: 100,','unpaired 3d.unreviewed.row.0');
await change('new resolved viewer number',config,'  c.sectionLengthM =','  c.unreviewed = 17;\n  c.sectionLengthM =','unpaired 3d.unreviewed');
await change('new exported viewer number',config,'export const G = 9.81;','export const G = 9.81;\nexport const UNREVIEWED = 17;','unpaired 3d.UNREVIEWED');
await change('missing viewer partner',config,'    cruiseKph: 90,','', 'missing numeric partner: sim.cruiseKph=90');
await change('wrong scalar',config,'    batteryEnergyMWh: 20,','    batteryEnergyMWh: 21,','sim.battMWh / 3d.batteryEnergyMWh');
await change('wrong table value',config,'speed: 1.15','speed: 1.16','sim.MODES / 3d.MODES');
await change('new table member',config,"speed: 1.15","unreviewed: 17, speed: 1.15",'sim.MODES / 3d.MODES');
await change('ignored mode speed','3d/anim/mission.js', "specNumber(cls, 'cruiseKph') * mode.speed / 3.6", "specNumber(cls, 'cruiseKph') / 3.6", 'rapid flight speed');
await change('copied rotor density','3d/control/actuators.js', 'rho = ASSUMPTIONS.rhoAir', 'rho = 1.10', 'not ok 5 - rotor density', ['--test','3d/tests/parity-consumers.test.mjs']);
await change('wrong drag derivation','3d/physics/mass.js',"Math.PI * (specNumber(cls, 'nominalDiameterM') / 2) ** 2",'Math.pow(cls.displacementM3, 2 / 3)','drag reference area:');
await change('rounded working density',config,'export const RHO_WORK = RHO_SL * Math.pow','export const RHO_WORK = 0.95686; const unusedDensity = RHO_SL * Math.pow','sim.RHO_WORK / 3d.RHO_WORK');
await change('wrong drop altitude',config,'drop: 450','drop: 250','sim.ALT / 3d.ALT');
await change('old hose consumer','3d/anim/hose.js','opts.headM ?? sourceAltM(cls)','opts.headM ?? 250','eq: 250 !== 300');
await change('silent spec default','3d/anim/mission.js',"const kph = specNumber(cls, 'cruiseKph');",'const kph = cls.cruiseKph || 90;','not ok 1 - no numeric default',required);
await change('disabled runtime validation',config,'throw new Error(`${cls.id}: required class field','return value; throw new Error(`${cls.id}: required class field','Missing expected exception',required);
await change('duplicated density declaration','3d/physics/mass.js','RHO_WORK, ASSUMPTIONS, RHO_LN2, RHO_WATER, G, specNumber','RHO_WORK, ASSUMPTIONS, RHO_WATER, G, specNumber','not ok 5 - mission constants and liquid density exports', ['--input-type=module','-e',
  `import {readFileSync,writeFileSync} from 'node:fs'; const p='3d/physics/mass.js'; let s=readFileSync(p,'utf8'); s=s.replace("export { RHO_LN2, RHO_WATER }", "export const RHO_LN2 = 807;\\nexport { RHO_WATER }"); writeFileSync(p,s); await import('./3d/tests/spec-required.test.mjs');`]);
cleanup();
for (const args of [parity,required]) {
  const r = spawnSync(process.execPath,args,{cwd:root,encoding:'utf8'});
  interrupted(r);
  if (r.status !== 0) throw new Error(`restored tree is not green\n${r.stdout}${r.stderr}`);
}
console.log(`RESTORED: ${count}/${count} mutations caught; parity and required-spec suites green`);
