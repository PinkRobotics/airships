#!/usr/bin/env python3
"""Reproduce the analysis JSON and resolve every cited numeric key."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[2]
A=ROOT/'research/analysis'

def expand(text):
    m=re.search(r'\{([^{}]*)\}',text)
    if not m:return [text.strip()]
    return [v for part in m[1].split(',') for v in expand(text[:m.start()]+part.strip()+text[m.end():])]

def resolve(value, path, trail=()):
    if not path:return [trail]
    if path.startswith('.'):
        return resolve(value,path[1:],trail)
    if path.startswith('['):
        m=re.match(r'\[(\*|\d+)\]',path)
        if not m:return []
        indices=range(len(value)) if m[1]=='*' else [int(m[1])]
        if not isinstance(value,list):return []
        return [out for i in indices if i<len(value) for out in resolve(value[i],path[m.end():],trail+(str(i),))]
    if path.startswith('*'):
        if not isinstance(value,dict):return []
        groups=[resolve(v,path[1:],trail+(k,)) for k,v in value.items()]
        return [p for g in groups for p in g] if all(groups) else []
    if not isinstance(value,dict):return []
    for key in sorted(value,key=len,reverse=True):
        if path==key or path.startswith(key+'.') or path.startswith(key+'['):
            return resolve(value[key],path[len(key):],trail+(key,))
    return []

def keys_check(doc,data):
    count=0;previous=[];errors=[]
    for m in re.finditer(r'`([^`]+)`',doc):
        token=m[1].replace('\n','').replace(' ', '')
        if not re.match(r'(?:P100|\*\.|classes\.|constants\.|baseline|earlier|ranking$|nextAnalysis$|\.+[A-Za-z])',token):continue
        if token.startswith('P100') or token.startswith('*.'):token='classes.'+token
        for path in expand(token):
            paths=[]
            if path.startswith('.'):
                for prior in previous:
                    for n in range(len(prior),0,-1):
                        cur=data
                        try:
                            for k in prior[:n]:cur=cur[int(k)] if isinstance(cur,list) else cur[k]
                        except (KeyError,IndexError,TypeError):continue
                        paths=resolve(cur,path.lstrip('.'),prior[:n])
                        if paths:break
                    if paths:break
            else:paths=resolve(data,path)
            if not paths:errors.append(f'line {doc[:m.start()].count(chr(10))+1}: unresolved key {path}')
            else:previous=paths;count+=len(paths)
    if errors:raise ValueError('\n'.join(errors))
    if count<300:raise ValueError(f'only {count} keys checked; expected the complete study')
    return count

def main():
    with tempfile.TemporaryDirectory(prefix='payload-exchange-',dir=os.environ['TMPDIR']) as tmp:
        copy=Path(tmp)/'payload-exchange.py';shutil.copy2(A/'payload-exchange.py',copy)
        shutil.copy2(A/'payload-exchange.md',Path(tmp)/'payload-exchange.md')
        r=subprocess.run(['python3',str(copy)],capture_output=True,text=True)
        if r.returncode:raise ValueError(r.stderr)
        if (Path(tmp)/'payload-exchange.json').read_bytes()!=(A/'payload-exchange.json').read_bytes():raise ValueError('payload-exchange.json is stale; regenerate the analysis')
        if (Path(tmp)/'payload-exchange.md').read_bytes()!=(A/'payload-exchange.md').read_bytes():raise ValueError('payload-exchange.md capsule sentence is stale')
    n=keys_check((A/'payload-exchange.md').read_text(),json.loads((A/'payload-exchange.json').read_text()))
    print(f'PASS payload-exchange: JSON reproduces byte for byte; {n} cited keys resolve.')
if __name__=='__main__':main()
