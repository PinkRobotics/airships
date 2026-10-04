"""Committed test identities, checked against files and actual runner records.

The stamp is deliberately separate: it measures cache content, not which tests run.
Names are compared as multisets so duplicates cannot cover for a missing test.
"""
from collections import Counter
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / 'research/test-inventory.json'
PATTERNS = {'shared': 'tests/cases/*.cases.js', 'node': '3d/tests/*.test.mjs',
            'browser3d': '3d/tests/browser.html'}


def files(section):
    return sorted(p.relative_to(ROOT).as_posix() for p in ROOT.glob(PATTERNS[section]))


def load():
    try:
        inventory = json.loads(INVENTORY.read_text())
        for section in PATTERNS:
            for field in ('files', 'names'):
                values = inventory[section][field]
                if not isinstance(values, list) or not all(isinstance(v, str) for v in values):
                    raise ValueError('identity lists must contain strings')
        return inventory
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise SystemExit(f'test inventory: cannot read research/test-inventory.json ({type(exc).__name__})')


def differences(section, actual, expected=None):
    expected = (expected or load())[section]
    bad = []
    for field in ('files', 'names'):
        want, got = Counter(expected[field]), Counter(actual[field])
        for item in sorted((want - got).elements()):
            bad.append(f'test inventory {section}: missing {field[:-1]} {item}')
        for item in sorted((got - want).elements()):
            bad.append(f'test inventory {section}: unexpected {field[:-1]} {item}')
    return bad


def check_files(section):
    expected = load()[section]
    return differences(section, {'files': files(section), 'names': expected['names']})


def check_record(section, actual):
    bad = differences(section, actual)
    for line in bad:
        print(line, file=sys.stderr)
    if not bad:
        print(f'test inventory {section}: {len(actual["files"])} files, {len(actual["names"])} names match')
    return not bad


def shared_record(rec):
    return {'files': sorted(rec['files']), 'names': sorted(
        s['name'] + ' › ' + t['name'] for s in rec['suites'] for t in s['tests'])}


def console_record(text, section):
    prefix = f'TEST_INVENTORY {section} '
    for line in text.splitlines():
        if prefix in line:
            # Chromium adds its source location after the console message.
            return json.JSONDecoder().raw_decode(line.split(prefix, 1)[1])[0]
    raise ValueError(f'test inventory {section}: runner produced no identity record')


def native_record(text):
    names, seen = [], set()
    for line in text.splitlines():
        event = json.loads(line)
        if event['type'] not in ('test:pass', 'test:fail'):
            continue
        data = event['data']
        if data.get('details', {}).get('type') == 'suite':
            continue
        path = Path(data['file']).resolve().relative_to(ROOT).as_posix()
        seen.add(path)
        names.append(path + ' › ' + data['name'])
    return {'files': sorted(seen), 'names': sorted(names)}


def run_native():
    with tempfile.TemporaryDirectory() as td:
        record = Path(td) / 'native.jsonl'
        result = subprocess.run([
            'node', '--test', '--test-reporter=tap', '--test-reporter-destination=stdout',
            '--test-reporter=./tools/test_inventory_reporter.mjs',
            '--test-reporter-destination=' + str(record), *files('node')],
            cwd=ROOT, capture_output=True, text=True)
        return result, native_record(record.read_text())


def collect_native():
    result, record = run_native()
    if result.returncode:
        raise SystemExit('test inventory generation: Node tests failed\n' + result.stdout + result.stderr)
    return record


def collect_shared():
    code = r"""
import {collect} from './tests/harness.js';
import fs from 'node:fs';
const source=fs.readFileSync('tests/node/run.mjs','utf8');
const files=[];
for(const m of source.matchAll(/await import\('([^']+)'\)/g)) {
  const url=new URL(m[1],new URL('./tests/node/run.mjs',import.meta.url));
  await import(url); files.push(url.pathname.slice(process.cwd().length+1));
}
console.log(JSON.stringify({files:files.sort(), names:collect().flatMap(s=>s.tests.map(t=>s.name+' › '+t.name)).sort()}));
"""
    with tempfile.TemporaryDirectory() as td:
        log = Path(td) / 'modules.log'
        env = dict(os.environ, TEST_INVENTORY_MODULE_LOG=str(log))
        record = json.loads(subprocess.check_output([
            'node', '--import=./tools/test_inventory_boot.mjs', '--input-type=module', '-e', code],
            cwd=ROOT, text=True, env=env))
        record['files'] = sorted(set(log.read_text().splitlines()))
        return record


def collect_browser():
    from browser_scratch import browser_scratch
    from serve import serve_tree
    with browser_scratch() as td, serve_tree(ROOT) as base:
        probe, out = Path(td) / 'inventory.js', Path(td) / 'inventory.json'
        probe.write_text("""(async () => {
          for (let i=0; i<600 && !window.__tests3d; i++) await new Promise(r=>setTimeout(r,100));
          if (!window.__tests3d) throw new Error('3d browser suite never finished');
          if (!/fail=0 skip=0/.test(document.title)) throw new Error('3d browser checks failed or skipped: '+document.title);
          return window.__tests3d;
        })()""")
        result = subprocess.run([sys.executable, str(ROOT / 'tools/js_eval.py'),
                                 base + '3d/tests/browser.html', str(probe), str(out), '4'],
                                capture_output=True, text=True, cwd=ROOT)
        if result.returncode:
            raise SystemExit('test inventory generation: browser probe failed\n' + result.stdout + result.stderr)
        return json.loads(out.read_text())


def generate():
    result = {'shared': collect_shared(), 'node': collect_native(), 'browser3d': collect_browser()}
    for section, record in result.items():
        record['files'].sort(); record['names'].sort()
        if record['files'] != files(section):
            raise SystemExit(f'test inventory generation: {section} runner does not cover {files(section)}')
    return result


def main():
    if sys.argv[1] == '--files':
        bad = [line for section in sys.argv[2:] for line in check_files(section)]
        for line in bad: print(line, file=sys.stderr)
        return int(bool(bad))
    section, logfile = sys.argv[1:]
    bad = check_files(section)
    for line in bad:
        print(line, file=sys.stderr)
    if bad:
        return 1
    try:
        return int(not check_record(section, console_record(Path(logfile).read_text(), section)))
    except (OSError, ValueError, KeyError) as exc:
        print(f'test inventory {section}: invalid runner record: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
