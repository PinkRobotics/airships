#!/usr/bin/env python3
"""Regenerate energy regions and reject unbound figures with a file and line."""
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parent.parent
FILES={'docs/PHYSICS.md':'physics','sim/README.md':'simulator',
       'docs/ENERGY-CLOSURE-2026-10.md':'closure','docs/ENERGY-MODEL-2026-10.md':'model'}
NUMBER=re.compile(r'(?<![A-Za-z])\d+(?:[.,]\d+)*')
ENERGY=re.compile(r'\b(?:[kMG]?W(?:h)?|Wh/kg|energy|battery|solar|endurance|pump|rotor|thrust|unheld|hold-down)\b',re.I)

def unbound(path,text,region):
    start=f'<!-- energy:{region}:start -->';end=f'<!-- energy:{region}:end -->'
    if text.count(start)!=1 or text.count(end)!=1 or text.index(start)>text.index(end):
        return [f'{path}:1: expected one complete generated energy region']
    extra={"notation"} if path=="docs/PHYSICS.md" else set()
    inside=False;bad=[];table_energy=False
    for line_no,line in enumerate(text.splitlines(),1):
        if line==start or any(line==f"<!-- energy:{r}:start -->" for r in extra):inside=True;continue
        if line==end or any(line==f"<!-- energy:{r}:end -->" for r in extra):inside=False;continue
        if inside:continue
        # All simulator/model/closure figures are owned. The physics preface and hull
        # geometry remain outside this energy gate; energy quantities there still fail.
        if not line.strip():table_energy=False
        if line.startswith('|') and ENERGY.search(line):table_energy=True
        plain=re.sub(r'\([^)]*://[^)]*\)','',line)
        if NUMBER.search(plain) and (path!='docs/PHYSICS.md' or table_energy or ENERGY.search(plain) or re.search(r'cycle.*(?:minutes?|hours?)',plain,re.I)):
            bad.append(f'{path}:{line_no}: unbound energy figure outside a generated region')
    return bad

def first_difference(old,new):
    a=old.splitlines();b=new.splitlines()
    for i,(x,y) in enumerate(zip(a,b),1):
        if x!=y:return i
    return min(len(a),len(b))+1

def selftest():
    marker='<!-- energy:model:start -->\n100 MWh\n<!-- energy:model:end -->\n'
    assert not unbound('sim/README.md',marker,'model')
    assert unbound('sim/README.md',marker+'A cycle costs 123 MWh.\n','model')==['sim/README.md:4: unbound energy figure outside a generated region']
    assert unbound('sim/README.md',marker.replace(':end',':oops'),'model')
    assert unbound('docs/PHYSICS.md',marker+'\n| Energy | Value |\n|---|---|\n| Sample | 123 |\n','model')
    assert first_difference('one\ntwo\n','one\nthree\n')==2
    print('PASS energy document gate self-test: owned, unbound, missing marker and first differing line')

def main():
    if '--self-test' in sys.argv:selftest();return 0
    errors=[]
    for path,region in FILES.items():errors.extend(unbound(path,(ROOT/path).read_text(),region))
    if errors:print('\n'.join(errors));return 1
    checks=[['node',f'research/analysis/{name}.mjs','--check'] for name in
            ['energy-omissions','energy-unheld','energy-descent','energy-close','energy-model-change','energy-profile-details','energy-served-inertia','energy-necessary','energy-zero-sun']]
    checks.insert(0,['node','research/analysis/energy-tables.mjs','--check'])
    checks += [['node','research/analysis/energy-motion.mjs','--check']]
    checks += [['node','tools/gen_energy_pages.mjs','--check']]
    checks += [['python3','tests/energy/hover-floor.py','--check'],['node','tests/energy/replay.mjs']]
    for command in checks:
        result=subprocess.run(command,cwd=ROOT,capture_output=True,text=True)
        if result.returncode:
            print('Energy record check failed: '+' '.join(command))
            output=result.stdout+result.stderr
            location=re.search(r'(research/analysis/[^\n]+:\d+: [^\n]+)',output)
            print(location[1] if location else output);return 1
    result=subprocess.run(['node','research/analysis/energy-documents.mjs','--emit'],cwd=ROOT,capture_output=True,text=True)
    if result.returncode:print('docs/PHYSICS.md:1: energy regeneration failed\n'+result.stderr);return 1
    for path,expected in json.loads(result.stdout).items():
        actual=(ROOT/path).read_text()
        if actual!=expected:errors.append(f'{path}:{first_difference(actual,expected)}: generated energy content is stale; run node research/analysis/energy-documents.mjs')
    if errors:print('\n'.join(errors));return 1
    print('PASS energy documents: generated energy regions and their live model record match; no unbound energy figures')
    return 0
if __name__=='__main__':sys.exit(main())
