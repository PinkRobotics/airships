#!/usr/bin/env python3
"""Run the node unit tests in a browser, on a machine that has no node.

    python3 tools/node_tests_in_browser.py            # run them
    python3 tools/node_tests_in_browser.py --keep     # leave the harness in place to debug

This fallback runs browser-compatible 3D suites with a small import-map shim for
node:test and node:assert. Suites requiring filesystem access are named as skipped;
a browser cannot enumerate and read the source tree as Node does. The full check
requires Node, and `make test-node` with Node installed always runs every suite.

Only the assertion helpers used by these tests are implemented. An unsupported
helper or an unexpected import failure fails the run rather than silently passing.

The committed inventory pins files and actual test names, including the shared
cases run by tests/browser/run.py. The explicit Node-only exclusions remain
visible. Regenerate deliberately with tools/gen_test_status.py --inventory;
review its diff when adding, renaming or retiring a test.
"""
from __future__ import annotations

import argparse
import html
import json
import pathlib
import re
import shutil
import subprocess
import sys
from browser_scratch import browser_scratch
from serve import serve_tree
from test_inventory import check_files, check_record, console_record, load

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

# Explicit exclusions only: new import failures remain failures. These source scans
# use recursive directory enumeration and synchronous reads, which a browser lacks.
NODE_ONLY = {
    'builder-line.test.mjs': 'requires node:child_process and Git history; run make buildercheck',
    'spec-required.test.mjs': 'requires node:fs directory enumeration and synchronous source-file reads',
}
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
const lines = []; const ran = [], loaded = []; let pass = 0, fail = 0;
try {
  // The shim module is CACHED, so its registry array is created once and every file pushes
  // into the same one. Resetting globalThis.__R between files therefore reads an empty array
  // while the tests pile up in the original — which silently ran 22 of 103 and reported green.
  // Take a slice of the shared registry instead.
  for (const f of files) {
    const from = (globalThis.__R || []).length;
    try { await import(f); loaded.push('3d/tests/' + f.slice(2)); }
    catch (e) { lines.push('LOADFAIL ' + f + ': ' + e.message); fail++; continue; }
    for (const t of globalThis.__R.slice(from)) {
      ran.push('3d/tests/' + f.slice(2) + ' › ' + t.n);
      try { await t.f(); pass++; }
      catch (e) { fail++; lines.push('FAIL [' + f.slice(2) + '] ' + t.n + ': ' + e.message); }
    }
  }
  out.textContent = 'RESULT pass=' + pass + ' fail=' + fail + '\\n' + lines.join('\\n')
    + '\\nTEST_INVENTORY node ' + JSON.stringify({files: loaded, names: ran});
} catch (e) { out.textContent = 'HARNESSERROR ' + e.message; }
</script></body></html>
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--keep', action='store_true', help='leave the harness file in place')
    ap.add_argument('--chrome', default='chromium')
    args = ap.parse_args()

    if shutil.which('node'):
        print('note: node is installed here — `make test-node` is the authority, this is the '
              'fallback for machines without it.')

    bad = check_files('shared') + check_files('node')
    for line in bad:
        print(line, file=sys.stderr)
    if bad:
        return 1
    shared = subprocess.run([sys.executable, str(ROOT / 'tests/browser/run.py')], cwd=ROOT)
    if shared.returncode:
        return 1
    files = sorted(p.name for p in TESTS.glob('*.test.mjs'))
    if not files:
        print('node_tests_in_browser: no 3d/tests/*.test.mjs found', file=sys.stderr)
        return 1
    for name in files:
        if name in NODE_ONLY:
            print(f'SKIP 3d/tests/{name}: {NODE_ONLY[name]} (run with Node).')
    files = [name for name in files if name not in NODE_ONLY]
    HARNESS.write_text(HARNESS_HTML % {
        't': SHIM_TEST, 'a': SHIM_ASSERT,
        'files': '[' + ','.join(f'"./{f}"' for f in files) + ']',
    })

    try:
        with browser_scratch(args.chrome) as profile, serve_tree(ROOT) as base:
            # swiftshader, unsafe explicitly allowed: several of these build a real GL scene and a
            # headless runner has no GPU. --dump-dom rather than a screenshot because the answer is
            # text, and the virtual time budget is what lets the whole suite finish before the dump.
            proc = subprocess.run(
                [args.chrome, '--headless', '--no-sandbox', '--use-gl=angle',
                 '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
                 f'--user-data-dir={profile}', '--virtual-time-budget=45000', '--dump-dom',
                 f'{base}3d/tests/{HARNESS.name}'],
                capture_output=True, text=True, timeout=300)
    finally:
        if not args.keep:
            HARNESS.unlink(missing_ok=True)

    m = re.search(r'<pre id="out">([\s\S]*?)</pre>', proc.stdout)
    if not m:
        print('node_tests_in_browser: the harness produced no result — run with --keep and open '
              f'it at http://127.0.0.1:PORT/3d/tests/{HARNESS.name}', file=sys.stderr)
        return 1
    body = html.unescape(m.group(1)).strip()
    print(body.split("\nTEST_INVENTORY ", 1)[0])
    head = body.split('\n', 1)[0]
    expected = load()
    excluded = {'3d/tests/' + name for name in NODE_ONLY}
    expected['node']['files'] = [p for p in expected['node']['files'] if p not in excluded]
    expected['node']['names'] = [n for n in expected['node']['names']
                                 if n.split(' › ', 1)[0] not in excluded]
    from test_inventory import differences
    try:
        bad = differences('node', console_record(body, 'node'), expected)
    except (ValueError, KeyError) as exc:
        bad = [f'test inventory fallback: invalid runner record: {exc}']
    for line in bad:
        print(line, file=sys.stderr)
    if bad:
        return 1
    print(f"test inventory fallback: {len(expected['node']['files'])} files, "
          f"{len(expected['node']['names'])} names match; named Node-only suites excluded")
    if not head.startswith('RESULT') or ' fail=0' not in head:
        print('\nnode_tests_in_browser: browser-compatible tests failed; see diagnostics above.',
              file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
