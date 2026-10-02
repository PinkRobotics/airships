// Replay the final parity guard against HEAD's 3d source, then restore the working bytes.
// Run alone: this temporarily replaces only modified, tracked 3d/*.js files in this clone.
import { execFileSync, spawnSync } from 'node:child_process';
import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
const cwd = fileURLToPath(new URL('../../', import.meta.url));
const git = (...args) => execFileSync('git',args,{cwd,encoding:'utf8'});
const paths = git('diff','--name-only','HEAD','--','3d').trim().split('\n')
  .filter(p => p.startsWith('3d/') && p.endsWith('.js'));
const saved = paths.map(p => [p,readFileSync(cwd+p)]);
try {
  for (const [p] of saved) writeFileSync(cwd+p,git('show',`HEAD:${p}`));
  console.log(`Starting 3d source: ${git('rev-parse','HEAD').trim()}`);
  const r = spawnSync(process.execPath,['tests/parity/run.mjs'],{cwd,encoding:'utf8'});
  process.stdout.write(r.stdout);
  if (r.status !== 1 || !r.stdout.includes('drag reference area:') ||
      !r.stdout.includes('sim.cruiseKph=110; 3d.cruiseKph=undefined')) {
    throw new Error(`expected demonstrated starting-tree failures, got exit ${r.status}`);
  }
  console.log('EXPECTED RED: parity runner exited 1');
  if (process.argv.includes('--probe')) {
    const p = spawnSync(process.execPath,['tests/parity/probe.mjs'],{cwd,encoding:'utf8'});
    if (p.status !== 0) throw new Error(p.stderr);
    console.log('BASELINE PROBE'); process.stdout.write(p.stdout);
  }
} finally {
  for (const [p,bytes] of saved) writeFileSync(cwd+p,bytes);
}
const restored = spawnSync(process.execPath,['tests/parity/run.mjs'],{cwd,encoding:'utf8'});
process.stdout.write(restored.stdout);
if (restored.status !== 0) throw new Error('restored tree is not green');
console.log('RESTORED: working source passes');
