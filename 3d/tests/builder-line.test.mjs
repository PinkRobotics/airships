import test from 'node:test';
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

test('recorded changes name their builder', t => {
  const script = fileURLToPath(new URL('../../tools/check_builder_line.py', import.meta.url));
  const result = spawnSync('python3', [script], { encoding: 'utf8' });
  assert.ifError(result.error);
  assert.equal(result.status, 0, result.stdout + result.stderr);
  const summary = result.stdout.trim();
  if (summary.startsWith('buildercheck: no history;')) {
    t.skip(summary);
    return;
  }
  t.diagnostic(summary);
});
