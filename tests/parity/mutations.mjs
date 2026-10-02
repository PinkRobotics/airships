// Bounded break-the-code checks. Each file mutation is restored in finally; sim/ is never written.
import { readFileSync, writeFileSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const root = fileURLToPath(new URL('../../', import.meta.url));
const parity = ['tests/parity/run.mjs'];
const required = ['--test','3d/tests/spec-required.test.mjs'];
let count = 0;
function run(args, expected, name) {
  const r = spawnSync(process.execPath,args,{cwd:root,encoding:'utf8'});
  const output = r.stdout + r.stderr;
  if (r.error || r.status !== 1 || !output.includes(expected)) {
    throw new Error(`${name}: expected exit 1 containing ${expected}; got ${r.status}\n${output}`);
  }
  console.log(`RED ${++count} ${name}: exit ${r.status}; ${expected}`);
}
function change(name,path,from,to,expected,args=parity) {
  const full = root+path, before = readFileSync(full,'utf8');
  if (!before.includes(from)) throw new Error(`mutation target not found: ${name}`);
  try { writeFileSync(full,before.replace(from,to)); run(args,expected,name); }
  finally { writeFileSync(full,before); }
}
function modelMutation(name,mutation,expected) {
  // In-memory mutation exercises the sim side without touching the other worker's files.
  run(['--input-type=module','-e',
    `const m = await import('./sim/config.js?v=a67fca39'); ${mutation}; await import('./tests/parity/run.mjs');`],expected,name);
}
modelMutation('new sim scalar','m.CLASSES.P100.unreviewed = 17','unpaired sim.unreviewed');
modelMutation('new sim numeric table','m.CLASSES.P100.unreviewed = {row:[17,18]}','unpaired sim.unreviewed.row.0');
modelMutation('missing sim partner','delete m.CLASSES.P100.cruiseKph','missing numeric partner: sim.cruiseKph=undefined');
change('unreasoned exemption','tests/cases/spec-parity.cases.js',
  "'Source eligibility belongs to the mission planner, not the standalone drawing.'", "''", 'unpaired sim.minSourceHa');
const config='3d/model/config.js';
change('new viewer scalar',config,'    payloadTonnes: 100,','    unreviewed: 17,\n    payloadTonnes: 100,','unpaired 3d.unreviewed');
change('new viewer numeric table',config,'    payloadTonnes: 100,','    unreviewed: {row:[17,18]},\n    payloadTonnes: 100,','unpaired 3d.unreviewed.row.0');
change('new resolved viewer number',config,'  c.sectionLengthM =','  c.unreviewed = 17;\n  c.sectionLengthM =','unpaired 3d.unreviewed');
change('new exported viewer number',config,'export const G = 9.81;','export const G = 9.81;\nexport const UNREVIEWED = 17;','unpaired 3d.UNREVIEWED');
change('missing viewer partner',config,'    cruiseKph: 90,','', 'missing numeric partner: sim.cruiseKph=90');
change('wrong scalar',config,'    batteryEnergyMWh: 20,','    batteryEnergyMWh: 21,','sim.battMWh / 3d.batteryEnergyMWh');
change('wrong table value',config,'speed: 1.15','speed: 1.16','sim.MODES / 3d.MODES');
change('new table member',config,"speed: 1.15","unreviewed: 17, speed: 1.15",'sim.MODES / 3d.MODES');
change('ignored mode speed','3d/anim/mission.js', "specNumber(cls, 'cruiseKph') * mode.speed / 3.6", "specNumber(cls, 'cruiseKph') / 3.6", 'rapid flight speed');
change('copied rotor density','3d/control/actuators.js', 'rho = ASSUMPTIONS.rhoAir', 'rho = 1.10', 'not ok 5 - rotor density', ['--test','3d/tests/parity-consumers.test.mjs']);
change('wrong drag derivation','3d/physics/mass.js',"Math.PI * (specNumber(cls, 'nominalDiameterM') / 2) ** 2",'Math.pow(cls.displacementM3, 2 / 3)','drag reference area:');
change('rounded working density',config,'export const RHO_WORK = RHO_SL * Math.pow','export const RHO_WORK = 0.95686; const unusedDensity = RHO_SL * Math.pow','sim.RHO_WORK / 3d.RHO_WORK');
change('wrong drop altitude',config,'drop: 450','drop: 250','sim.ALT / 3d.ALT');
change('old hose consumer','3d/anim/hose.js','opts.headM ?? sourceAltM(cls)','opts.headM ?? 250','eq: 250 !== 300');
change('silent spec default','3d/anim/mission.js',"const kph = specNumber(cls, 'cruiseKph');",'const kph = cls.cruiseKph || 90;','not ok 1 - no numeric default',required);
change('disabled runtime validation',config,'throw new Error(`${cls.id}: required class field','return value; throw new Error(`${cls.id}: required class field','Missing expected exception',required);
change('duplicated density declaration','3d/physics/mass.js','RHO_WORK, ASSUMPTIONS, RHO_LN2, RHO_WATER, G, specNumber','RHO_WORK, ASSUMPTIONS, RHO_WATER, G, specNumber','not ok 5 - mission constants and liquid density exports', ['--input-type=module','-e',
  `import {readFileSync,writeFileSync} from 'node:fs'; const p='3d/physics/mass.js'; let s=readFileSync(p,'utf8'); s=s.replace("export { RHO_LN2, RHO_WATER }", "export const RHO_LN2 = 807;\\nexport { RHO_WATER }"); writeFileSync(p,s); await import('./3d/tests/spec-required.test.mjs');`]);
for (const args of [parity,required]) {
  const r = spawnSync(process.execPath,args,{cwd:root,encoding:'utf8'});
  if (r.status !== 0) throw new Error(`restored tree is not green\n${r.stdout}${r.stderr}`);
}
console.log(`RESTORED: ${count}/${count} mutations caught; parity and required-spec suites green`);
