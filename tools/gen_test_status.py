#!/usr/bin/env python3
"""Generate current test counts and known-failure descriptions from registered cases."""
from pathlib import Path
import json, re, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]

def status():
    code=r"""
import fs from 'node:fs';
import {collect} from './tests/harness.js';
const source=fs.readFileSync('tests/node/run.mjs','utf8');
for(const match of source.matchAll(/await import\('([^']+)'\)/g))
  await import(new URL(match[1],new URL('./tests/node/run.mjs',import.meta.url)));
const suites=collect(),tests=suites.flatMap(s=>s.tests);
console.log(JSON.stringify({tests:tests.length,suites:suites.length,knownFailing:tests.filter(t=>t.known!==null).length}));
"""
    return json.loads(subprocess.check_output(['node','--input-type=module','-e',code],cwd=ROOT,text=True))

def region(text,name,body,begin,end=None):
    start=f'<!-- test-status:{name}:start -->'
    finish=f'<!-- test-status:{name}:end -->'
    rendered=start+'\n'+body+'\n'+finish+'\n'
    if start in text:
        a=text.index(start);b=text.index(finish,a)+len(finish)
        if text[b:b+1]=='\n':b+=1
    else:
        a=text.index(begin);b=text.index(end,a) if end else len(text)
    return text[:a]+rendered+text[b:]

def outputs(s):
    out={'research/test-status.json':json.dumps(s,indent=2)+'\n'}
    known=s['knownFailing'];tests=s['tests'];suites=s['suites']
    p='tests/README.md';text=(ROOT/p).read_text()
    body=f'The registered suites contain **{known} known-failing markers**.\nThe corrected wind flag runs as an ordinary assertion in `cases/sim-plan.cases.js`.\nThe force ledger and phase-integral checks run in `cases/sim-energy.cases.js`.\nThese counts describe registered tests, not an execution result.'
    out[p]=region(text,'markers',body,'The following markers are defined in the case files:')
    p='docs/OPEN-QUESTIONS.md';text=(ROOT/p).read_text()
    body=f'The current suites contain {known} known-failing markers. The corrected wind flag is an ordinary assertion; item 17 records its closure.'
    out[p]=region(text,'markers',body,'One `knownFail` marker is left','Item 1 had another.')
    p='research/reports/02-paper.md';text=(ROOT/p).read_text()
    body=f'- `make test` registers {tests} tests in {suites} suites, with {known} known-failing markers. Corrected defects run as ordinary assertions.'
    text=text.replace('<!-- test-status:paper:start -->\n','').replace('<!-- test-status:paper:end -->\n','')
    a=text.index('- `make test` ');b=text.index('- `make test-node` ',a)
    out[p]=text[:a]+body+'\n'+text[b:]
    p='research/reports/03-diligence.md';text=(ROOT/p).read_text()
    row=f'| `tests/` | {tests} registered tests in {suites} suites, plus {len(json.loads((ROOT/'research/test-inventory.json').read_text())['node']['names'])} native Node tests. **{known} known-failing markers**; corrected defects run as ordinary assertions. |'
    text,n=re.subn(r'^\| `tests/` \|[^\n]*',lambda m:row,text,flags=re.M)
    assert n==1
    text,n=re.subn(r'`make test` runs \d+ tests (?:including two deliberate failures|with \d+ known-failing markers) and',
                    f'`make test` runs {tests} tests with {known} known-failing markers and',text)
    assert n==1
    out[p]=text
    return out

def main():
    if '--inventory' in sys.argv:
        from test_inventory import INVENTORY, generate, differences, load
        inventory = generate()
        if '--check' in sys.argv:
            bad = [line for section, record in inventory.items()
                   for line in differences(section, record, load())]
            for line in bad: print(line)
            if bad: return 1
        else:
            INVENTORY.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + '\n')
        print('test inventory: ' + ', '.join(f"{s}: {len(r['files'])} files / {len(r['names'])} names"
                                           for s, r in inventory.items()))
        return 0
    s=status();generated=outputs(s);bad=[]
    for name,text in generated.items():
        p=ROOT/name
        if '--check' in sys.argv:
            if not p.exists() or p.read_text()!=text:bad.append(name)
        else:p.write_text(text)
    if bad:
        print('test status is stale: '+', '.join(bad));return 1
    print(f"test status: {s['tests']} registered tests in {s['suites']} suites; {s['knownFailing']} known-failing markers")
    return 0

if __name__=='__main__':sys.exit(main())
