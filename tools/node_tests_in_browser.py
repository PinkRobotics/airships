#!/usr/bin/env python3
"""Run the node unit tests in a browser, on a machine that has no node.

    python3 tools/node_tests_in_browser.py            # run them
    python3 tools/node_tests_in_browser.py --keep     # leave the harness in place to debug

WHY THIS EXISTS. `make test-node` prints "SKIPPED — no node here" and says the tests are not
optional, which is honest and completely useless: this repository is developed on a machine
without node, so those three files are only ever executed by CI, and a break in them is
discovered by a red badge minutes after a push. That has now happened twice — a pump figure
pinned at 1.635 MW after the head moved to 300 m, and a test asserting `rtLN2 = 0.50` after
the round trip was cut to 0.20 for exceeding the exergy of liquid nitrogen. Both were found
by CI. Both should have been found here.

Nothing about `3d/tests/*.test.mjs` actually needs node. They import three things node
provides — `node:test`, `node:assert`, `node:assert/strict` — and everything else from the
library, which is browser code. So this shims those three specifiers with an import map and
runs the same files, unmodified, in the Chromium that is already the toolchain.

WHAT THIS IS NOT. It is not a replacement for the CI job. The shim implements the assertions
the suite actually uses and nothing else; `node --test` remains the authority, and an
assertion helper added to a test tomorrow may need adding here too — it will fail loudly as
`A.foo is not a function` rather than passing silently. Treat a green run here as "CI will
probably be green", which is exactly the signal that was missing.

CHECK THE COUNT. The first version of this file ran 22 of 103 tests and reported green,
because it reset the registry between files while the cached shim module kept pushing into
the original array. A harness that under-reports is worse than no harness, so the count it
prints is compared against `EXPECTED_MIN` below — if the suite grows, that number moves with
it, deliberately and in a diff.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
TESTS = ROOT / '3d' / 'tests'
HARNESS = TESTS / '.node-tests-in-browser.html'

# Only what the suite uses. Deliberately not a faithful node:assert — a missing helper should
# blow up as a TypeError naming itself, not quietly report a pass.
SHIM_TEST = (
    "data:text/javascript,"
    "const R=[];"
    "export default function test(n,f){R.push({n,f})};"
    "export {test};"
    "export function describe(n,f){f()};"
    "export function it(n,f){R.push({n,f})};"
    "globalThis.__R=R;"
)
SHIM_ASSERT = (
    "data:text/javascript,"
    "const fail=(m)=>{throw new Error(String(m||'assertion failed'))};"
    "const A={"
    "ok(v,m){if(!v)fail(m||'not ok')},"
    "equal(a,b,m){if(a!==b)fail((m||'')+' :: '+a+' !== '+b)},"
    "strictEqual(a,b,m){A.equal(a,b,m)},"
    "notStrictEqual(a,b,m){if(a===b)fail(m)},"
    "deepEqual(a,b,m){if(JSON.stringify(a)!==JSON.stringify(b))fail((m||'')+' :: '+JSON.stringify(a))},"
    "deepStrictEqual(a,b,m){A.deepEqual(a,b,m)},"
    "notEqual(a,b,m){if(a===b)fail(m)},"
    "match(s,re,m){if(!re.test(s))fail((m||'')+' :: '+s)},"
    "throws(f,e,m){let t=false;try{f()}catch(x){t=true};if(!t)fail(m||'did not throw')},"
    "doesNotThrow(f,m){try{f()}catch(x){fail((m||'threw')+' :: '+x.message)}},"
    "fail(m){fail(m)}};"
    "export default A;"
    "export const ok=A.ok,equal=A.equal,strictEqual=A.strictEqual,deepEqual=A.deepEqual,"
    "deepStrictEqual=A.deepStrictEqual,notEqual=A.notEqual,match=A.match,throws=A.throws,"
    "doesNotThrow=A.doesNotThrow;"
)

# What `node --test 3d/tests/*.test.mjs` reports. A harness that runs a subset and says green is
# worse than none: the first version of this file ran 22 and passed. Raise this when the suite
# grows — in a diff, on purpose.
EXPECTED_MIN = 101   # was 103: the thruster retirement (2026-08-13) folded three
                     # blower-behaviour tests into one absence guard (net -2)

# The host div is on screen and sized, because the viewer stops rendering when it is not
# intersecting and several of these tests build a real scene.
HARNESS_HTML = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>node tests, in a browser</title>
<meta name="robots" content="noindex,nofollow">
<script type="importmap">
{"imports":{"node:test":"%(t)s","node:assert":"%(a)s","node:assert/strict":"%(a)s"}}
</script></head>
<body><div id="host" style="width:640px;height:400px;opacity:.35"></div><pre id="out">PENDING</pre>
<script type="module">
const out = document.getElementById('out');
const files = %(files)s;
const lines = []; let pass = 0, fail = 0;
try {
  // The shim module is CACHED, so its registry array is created once and every file pushes
  // into the same one. Resetting globalThis.__R between files therefore reads an empty array
  // while the tests pile up in the original — which silently ran 22 of 103 and reported green.
  // Take a slice of the shared registry instead.
  for (const f of files) {
    const from = (globalThis.__R || []).length;
    try { await import(f); }
    catch (e) { lines.push('LOADFAIL ' + f + ': ' + e.message); fail++; continue; }
    for (const t of globalThis.__R.slice(from)) {
      try { await t.f(); pass++; }
      catch (e) { fail++; lines.push('FAIL [' + f.slice(2) + '] ' + t.n + ': ' + e.message); }
    }
  }
  out.textContent = 'RESULT pass=' + pass + ' fail=' + fail + '\\n' + lines.join('\\n');
} catch (e) { out.textContent = 'HARNESSERROR ' + e.message; }
</script></body></html>
"""


def free_port() -> int:
    with socket.socket() as s:
        s.bind(('127.0.0.1', 0))
        return s.getsockname()[1]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--keep', action='store_true', help='leave the harness file in place')
    ap.add_argument('--chrome', default='chromium')
    args = ap.parse_args()

    if shutil.which('node'):
        print('note: node is installed here — `make test-node` is the authority, this is the '
              'fallback for machines without it.')

    files = sorted(p.name for p in TESTS.glob('*.test.mjs'))
    if not files:
        print('node_tests_in_browser: no 3d/tests/*.test.mjs found', file=sys.stderr)
        return 1
    HARNESS.write_text(HARNESS_HTML % {
        't': SHIM_TEST, 'a': SHIM_ASSERT,
        'files': '[' + ','.join(f'"./{f}"' for f in files) + ']',
    })

    port = free_port()
    server = subprocess.Popen([sys.executable, str(ROOT / 'tools' / 'serve.py'), '--port', str(port)],
                              stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, cwd=ROOT)
    profile = tempfile.mkdtemp(prefix='node-shim-', dir=pathlib.Path.home() / 'tmp'
                               if (pathlib.Path.home() / 'tmp').is_dir() else None)
    try:
        time.sleep(1.5)
        # swiftshader, unsafe explicitly allowed: several of these build a real GL scene and a
        # headless runner has no GPU. --dump-dom rather than a screenshot because the answer is
        # text, and the virtual time budget is what lets the whole suite finish before the dump.
        proc = subprocess.run(
            [args.chrome, '--headless', '--no-sandbox', '--use-gl=angle',
             '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
             f'--user-data-dir={profile}', '--virtual-time-budget=45000', '--dump-dom',
             f'http://127.0.0.1:{port}/3d/tests/{HARNESS.name}'],
            capture_output=True, text=True, timeout=300)
    finally:
        server.terminate()
        shutil.rmtree(profile, ignore_errors=True)
        if not args.keep:
            HARNESS.unlink(missing_ok=True)

    m = re.search(r'<pre id="out">([\s\S]*?)</pre>', proc.stdout)
    if not m:
        print('node_tests_in_browser: the harness produced no result — run with --keep and open '
              f'it at http://127.0.0.1:PORT/3d/tests/{HARNESS.name}', file=sys.stderr)
        return 1
    body = m.group(1).strip()
    print(body)
    head = body.split('\n', 1)[0]
    ran = sum(int(n) for n in re.findall(r'(?:pass|fail)=(\d+)', head))
    if ran < EXPECTED_MIN:
        print(f'\nnode_tests_in_browser: only {ran} of {EXPECTED_MIN} tests ran. The harness is '
              'not seeing the whole suite — fix that before trusting this result.', file=sys.stderr)
        return 1
    if not head.startswith('RESULT') or ' fail=0' not in head:
        print('\nnode_tests_in_browser: CI runs these on every push and will fail the same way.',
              file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
