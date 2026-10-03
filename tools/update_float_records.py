#!/usr/bin/env python3
"""Replay the reviewed float dispositions and freeze dated blocks by text hash.

Run intentionally after reviewing a candidate tree; never a gate prerequisite. Unknown
new text outside dated records is refused unless its hash is in the reviewed catalogue.
Existing record entries retain their dispositions; their informative locations are refreshed.
Energy blocks qualify only inside paired markers that their checked generator reproduces.
"""
import json
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
import check_float_ledger as gate
import float_claims as claims
from float_regions import region

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT/'tools/float_dispositions.json'
GENERATOR = 'research/analysis/energy-documents.mjs'


def write(path, value):
    rel=path.relative_to(ROOT).as_posix()
    old=subprocess.run(['git','show','HEAD:'+rel],cwd=ROOT,capture_output=True,text=True)
    indent=2 if old.returncode==0 and old.stdout.splitlines()[1].startswith('  ') else 1
    body=json.dumps(value,ensure_ascii=False,indent=indent)+'\n'
    if not path.exists() or path.read_text()!=body:path.write_text(body)


def retire_reviewed(shards, by_key, catalogue):
    """Replace an edited live block only by an explicit old/new hash review.

    A second run has nothing to retire. Dated history cannot be replaced by this
    mechanism; new dated corrections remain separate blocks.
    """
    reviewed = {(e['file'], e['key']) for e in catalogue['entries']}
    old_keys, new_keys = set(), set()
    retired = 0
    for item in catalogue.get('replacements', []):
        old = (item['file'], item['oldKey'])
        new = (item['file'], item['newKey'])
        if old == new or old in old_keys or new in new_keys:
            raise SystemExit('Duplicate or unchanged reviewed replacement: ' + str(item))
        old_keys.add(old); new_keys.add(new)
        if new not in reviewed or not 8 <= len(item.get('reason', '')) <= 240:
            raise SystemExit('Replacement requires a reviewed new hash and reason: ' + str(item))
        if old in by_key:
            # Historical catalogue entries also apply to future trees where the
            # old block is still present; only a missing old block is retired.
            continue
        entries = [(d, e) for d in shards.values() for e in d['entries']
                   if (e['file'], e['key']) == old]
        if not entries:
            continue
        if new not in by_key:
            raise SystemExit('Reviewed replacement text is absent: ' + str(new))
        for doc, entry in entries:
            if entry.get('class') == 'history':
                raise SystemExit('Dated history cannot be replaced: ' + str(old))
            doc['entries'].remove(entry)
            retired += 1
    return retired


def main():
    ledger=json.loads((ROOT/claims.LEDGER_PATH).read_text())
    hits=gate.inventory(ledger)
    shards={p:json.loads(p.read_text()) for p in claims.RECORD.glob('*.json') if p.name not in ('dated-blocks.json','widened.json','deferred-list.json')}
    known={(e['file'],e['key']):e for d in shards.values() for e in d['entries']}
    by_key={}
    for h in hits:
        if h.get('pointer') is not None:continue
        h['key']=claims.key_of(h['sentence'])
        by_key.setdefault((h['file'],h['key']),h)
    catalogue=json.loads(CATALOG.read_text())
    retired=retire_reviewed(shards,by_key,catalogue)
    known={(e['file'],e['key']):e for d in shards.values() for e in d['entries']}
    missing=set(known)-set(by_key)
    if missing:raise SystemExit('Existing text changed; review rather than reclassify: '+str(sorted(missing)))
    for k,e in known.items():e['line']=by_key[k]['line']
    dated_entries=[]
    new_entries=[]
    reviewed={(e['file'],e['key']):e for e in catalogue['entries']}
    for k,disposition in reviewed.items():
        if k in known:
            known[k].clear();known[k].update(disposition,line=by_key[k]['line'])
    files=set()
    for k,h in sorted(by_key.items()):
        if any(p.fullmatch(h['file']) for p,_ in gate.ALLOWLIST):
            if k not in known:
                date='20'+re.search(r'(\d{2}-\d{2}-\d{2})',h['file'])[1]
                dated_entries.append(dict(file=h['file'],key=h['key'],line=h['line'],
                    **{'class':'history'},date=date,
                    reason='Frozen block of this dated working or audit record; retained as history, not a current float endorsement.'))
            continue
        if k in known or h['status']=='ALLOW' or h['file']==claims.DEFERRED_PATH:continue
        if k not in reviewed:raise SystemExit('New block needs review: '+str(k))
        new_entries.append(dict(reviewed[k],line=h['line']))
        files.add(h['file'])
    # Hash catalogue remains the review authority for new live text. No blanket class.
    energy_moved=0
    for d in shards.values():
        for e in d['entries']:
            if e.get('class')=='generated' and not e.get('gate'):
                e['gate']='censuscheck'
            if e.get('class')!='deferred' or e.get('owner')!='energy-model':continue
            body=(ROOT/e['file']).read_text()
            matched=None
            for marker in re.findall(r'^<!-- energy:([^\n]+):start -->$',body,re.M):
                start=f'<!-- energy:{marker}:start -->';end=f'<!-- energy:{marker}:end -->'
                try:_,lo,hi=region(body,start,end)
                except ValueError:continue
                if lo <= e['line'] <= hi:matched=dict(start=start,end=end);break
            if matched:
                e.update(**{'class':'generated'},region=matched,generator=GENERATOR,
                         gate='energydoccheck',verifier='tools/check_energy_docs.py',
                         reason='Exact energy region is freshly regenerated and compared by energydoccheck, which make check runs; no structural float endorsement.')
                e.pop('owner',None);energy_moved+=1
            elif 'Generated by' in e['reason']:
                e['reason']='This generated energy analysis has no exact paired region markers or --emit region contract; it remains unreviewed by the float record.'
            elif 'mixed prose' in e['reason']:
                e['reason']='Mixed payload-exchange prose has no paired generated region; its separate analysis checks do not qualify it for the generated-region class.'
    for p,d in shards.items():write(p,d)
    write(claims.RECORD/'dated-blocks.json',dict(schema=claims.SCHEMA,
        files=sorted({e['file'] for e in dated_entries}),entries=dated_entries))
    # New entries for an already owned file go in its existing shard.
    widened=[]
    for e in new_entries:
        owner=next((p for p,d in shards.items() if e['file'] in d['files']),None)
        if owner:
            shards[owner]['entries'].append(e)
        else:widened.append(e)
    for p,d in shards.items():write(p,d)
    write(claims.RECORD/'widened.json',dict(schema=claims.SCHEMA,
        files=sorted({e['file'] for e in widened}),entries=widened))
    hits=gate.inventory(ledger)
    errors=claims.apply(hits,ledger)
    failed=[h for h in hits if h['status']=='FAIL']
    if errors or failed:
        for h in failed:print(h['file'],h['line'],h['reason'])
        for e in errors:print(e)
        return 1
    claims.write_deferred(hits)
    print(f'float records: {len(dated_entries)} frozen dated blocks; {len(new_entries)} new dispositions; {retired} reviewed live replacements; {energy_moved} energy entries qualify by region')
    print('deferred by owner: '+json.dumps(claims.deferred_counts(hits),sort_keys=True))
    return 0

if __name__=='__main__':sys.exit(main())
