/* Prove the anchor-removal assertions by altering module responses in owned scratch.
 * No model file is edited. Each child process has a fresh, independent module graph.
 */
import {mkdtempSync, writeFileSync, rmSync} from 'node:fs';
import {join, resolve} from 'node:path';
import {spawnSync} from 'node:child_process';

if (!process.env.TMPDIR) throw new Error('Set TMPDIR to project scratch before testing');
const scratch = mkdtempSync(join(process.env.TMPDIR, 'anchor-mutations-'));
const loader = join(scratch, 'loader.mjs');
writeFileSync(loader, `
export async function load(url, context, nextLoad) {
  const out = await nextLoad(url, context);
  const mutation = process.env.ANCHOR_MUTATION;
  let old, replacement;
  if (mutation === 'verdict' && new URL(url).pathname.endsWith('/sim/plan.js')) {
    old = 'feasible: I.feasible'; replacement = 'feasible: true';
  }
  if (mutation === 'reported-mass' && new URL(url).pathname.endsWith('/sim/power.js')) {
    old = 'owners, unheldT,'; replacement = 'owners, unheldT: 0,';
  }
  if (!old) return out;
  const source = String(out.source);
  if (source.split(old).length !== 2) throw new Error('Mutation target must occur once');
  return {...out, source: source.replace(old, replacement)};
}
`);
const run = `
import {collect, runTest} from './tests/harness.js';
await import('./tests/cases/sim-plan.cases.js');
const suite = collect().find(s => s.name === 'plan · anchor removal');
if (!suite || suite.tests.length !== 3) throw new Error('Expected all three anchor assertions');
let failures = 0;
for (const test of suite.tests) {
  const r = runTest(test);
  console.log(r.status.toUpperCase() + ' ' + r.name + (r.error ? ': ' + r.error : ''));
  failures += r.status === 'fail';
}
process.exitCode = failures ? 1 : 0;
`;
const probes = [
  ['', 0, 'green before'],
  ['verdict', 1, 'red: infeasible verdict replaced by true'],
  ['reported-mass', 1, 'red: instantaneous unheld mass hidden'],
  ['', 0, 'green restored'],
];
try {
  for (const [mutation, expected, label] of probes) {
    const p = spawnSync(process.execPath,
      ['--no-warnings', '--experimental-loader', loader, '--input-type=module', '-e', run],
      {cwd: resolve('.'), env: {...process.env, ANCHOR_MUTATION: mutation}, encoding: 'utf8'});
    console.log(label + ': exit ' + p.status);
    process.stdout.write(p.stdout || '');
    if (p.status !== expected) throw new Error('Anchor mutation did not produce its required verdict');
    if (mutation === 'verdict' && !p.stdout.includes('FAIL without an anchor the prescribed cycle is NOT FEASIBLE'))
      throw new Error('Verdict mutation did not fail the verdict assertion');
    if (mutation === 'reported-mass' && !p.stdout.includes('FAIL without an anchor unheld mass is reported'))
      throw new Error('Unheld-mass mutation did not fail the reporting assertion');
    if (p.stderr) throw new Error('Unexpected child diagnostic: ' + p.stderr);
  }
  console.log('PASS anchor-removal mutation proofs: both independent assertions reject their counterexamples');
} finally {
  rmSync(scratch, {recursive: true, force: true});
}
