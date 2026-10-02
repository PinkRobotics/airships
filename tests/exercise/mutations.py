#!/usr/bin/env python3
"""Five required negative controls, always restoring the exact original bytes.

Run after the ordinary gate. A mutation must fail its targeted check; restoration must
pass that same check. Run sequentially: these temporary edits are intentionally visible
to the local browser. Do not run alongside another gate or a working editor.
"""
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[2]


def change_json(fn):
    def change(raw):
        doc=json.loads(raw);fn(doc)
        return (json.dumps(doc,indent=2)+'\n').encode()
    return change


def move_near_guard(doc):
    g=json.loads((ROOT/'data/season/2026.guard.json').read_text())
    s=json.loads((ROOT/'data/season/2026.json').read_text())
    f=next(f for f in s['fires'] if f['fire']==g['fires'][0]['fire'])
    # ~89 km north of a guard entry, below the mandatory 150 km clearance.
    doc['fires']['features'][0]['geometry']['coordinates']=[f['lon'],f['lat']+.8]


def replace(old,new):
    def change(raw):
        assert raw.count(old)==1, 'mutation anchor must be unique'
        return raw.replace(old,new)
    return change


CASES=[
    ('real-looking number','data/exercise/exercise.json','invented_identity',change_json(lambda d:d['fires']['features'][0]['properties'].update(FIRE_NUMBER='K51234'))),
    ('within 100 km of guard','data/exercise/exercise.json','geography',change_json(move_near_guard)),
    ('remove EXERCISE chip','app/main.js','page_labels',replace(b'<b>EXERCISE</b>',b'<b></b>')),
    ('remove exercise from fires heading','app/cockpit/tables.js','page_labels',replace(b'Exercise fires',b'Fires')),
    ('change seed without regeneration','data/exercise/exercise.json','regenerated_bytes',change_json(lambda d:d.update(seed=d['seed']+1))),
]


def run(check):
    cmd=[sys.executable,'tests/exercise/check.py',check]
    print('$ python3 tests/exercise/check.py '+check,flush=True)
    r=subprocess.run(cmd,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    print(r.stdout,end='',flush=True);print('exit',r.returncode,flush=True)
    return r.returncode


def main():
    for name,rel,check,mutate in CASES:
        p=ROOT/rel;original=p.read_bytes()
        print('\nMUTATION: '+name,flush=True)
        try:
            p.write_bytes(mutate(original))
            red=run(check)
        finally:
            p.write_bytes(original)
        assert p.read_bytes()==original, 'restoration changed bytes'
        assert red!=0, 'mutation escaped the gate'
        print('RESTORED: exact original bytes',flush=True)
        assert run(check)==0, 'restored gate did not pass'
    print('\nmutations: 5 red, 5 restored green',flush=True)

if __name__=='__main__':main()
