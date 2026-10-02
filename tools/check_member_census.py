#!/usr/bin/env python3
"""A green census means the recorded disagreements equal fresh measurements."""
from __future__ import annotations
import argparse
import ast
import copy
import importlib.util
import json
import math
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]


def load_module(name):
    spec=importlib.util.spec_from_file_location(name.replace('-','_'), ROOT/f'research/analysis/{name}.py')
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def changes(recorded, measured, path=''):
    if isinstance(recorded,dict) and isinstance(measured,dict):
        for key in sorted(recorded.keys() | measured.keys()):
            child=f'{path}/{key}'
            if key not in recorded:
                yield f'{child}: new measurement missing from record'
            elif key not in measured:
                yield f'{child}: recorded measurement vanished'
            else:
                yield from changes(recorded[key],measured[key],child)
    elif isinstance(recorded,list) and isinstance(measured,list):
        if len(recorded)!=len(measured):
            yield f'{path}: record has {len(recorded)} entries; measured {len(measured)}'
        for i,(a,b) in enumerate(zip(recorded,measured)):
            yield from changes(a,b,f'{path}/{i}')
    elif any(isinstance(x,float) and not math.isfinite(x) for x in (recorded,measured)):
        yield f'{path}: nonfinite quantity refused'
    elif recorded!=measured or (recorded is None)!=(measured is None):
        yield f'{path}: recorded {recorded!r}; measured {measured!r}'


def geometry_bindings(source):
    """Cap lengths must be reads of the measured drawing, even if a literal matches today."""
    tree=ast.parse(source)
    required={'cap_hoops_length':"f['hoops']['capArcM']",'cap_bars_length':"f['bars']['capArcM']"}
    assignments={}
    for node in ast.walk(tree):
        if isinstance(node,ast.Assign):
            for target in node.targets:
                if isinstance(target,ast.Name) and target.id in required:
                    assignments.setdefault(target.id,[]).append(ast.dump(node.value))
    for name,expression in required.items():
        expected=ast.dump(ast.parse(expression,mode='eval').body)
        if assignments.get(name)!=[expected]:
            yield f'cap-readings.py: {name} must read its measured geometry field; typed or replaced length refused'


def check():
    census=load_module('member-census'); caps=load_module('cap-readings')
    bad=list(geometry_bindings((ROOT/'research/analysis/cap-readings.py').read_text()))
    fresh=census.measure()
    for relative,measured,render in (
        ('research/analysis/member-census.json',fresh,census.markdown),
        ('research/analysis/cap-readings.json',caps.readings(fresh),caps.markdown)):
        path=ROOT/relative
        try:
            recorded=json.loads(path.read_text())
        except (OSError,ValueError) as e:
            bad.append(f'{relative}: record unavailable ({type(e).__name__})');continue
        bad.extend(f'{relative}{item}' for item in changes(recorded,measured))
        md=ROOT/('docs/MEMBER-CENSUS.md' if 'member-census' in relative else 'research/analysis/cap-readings.md')
        if not md.is_file() or md.read_text()!=render(measured):
            bad.append(f'{md.relative_to(ROOT)}: differs from fresh generated text')
    if bad:
        print('CENSUS CHECK FAILED: the published record differs from fresh measurements')
        for item in bad[:30]:print('  '+item)
        if len(bad)>30:print(f'  {len(bad)-30} further differences')
        return 1
    print(f"censuscheck: {fresh['disagreementCount']} disagreements unchanged; five cap readings and both generated notes match")
    print('This is record consistency, not agreement between the drawing and bill or structural approval.')
    return 0


def self_test():
    sample={'disagreements':[{'id':'inner','delta':-2.0}], 'unknown':None, 'count':2}
    assert not list(changes(sample,copy.deepcopy(sample)))
    for label,mutate in (
        ('changed quantity',lambda d:d.update(count=3)),
        ('deleted disagreement',lambda d:d['disagreements'].clear()),
        ('new disagreement',lambda d:d['disagreements'].append({'id':'new','delta':1})),
        ('nonfinite quantity',lambda d:d.update(count=float('nan'))),
        ('unknown replaced by zero',lambda d:d.update(unknown=0))):
        changed=copy.deepcopy(sample);mutate(changed)
        assert list(changes(sample,changed)),label
    source="cap_hoops_length = f['hoops']['capArcM']\ncap_bars_length = f['bars']['capArcM']\n"
    assert not list(geometry_bindings(source))
    assert list(geometry_bindings(source.replace("f['hoops']['capArcM']",'123.0')))
    c=load_module('member-census')
    assert not c.different(100,100+1e-5)
    assert c.different(100,101) and c.different(0,None) and c.different(1,float('nan'))
    print('census self-test: equality accepted; changes, deletion, additions, nonfinite, unknown-to-zero and typed lengths rejected')
    return 0

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--self-test',action='store_true')
    args=ap.parse_args()
    sys.exit(self_test() if args.self_test else check())
