#!/usr/bin/env python3
"""Real-tree mutations, confined to disposable copies under explicit TMPDIR."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import claims


def main():
    scratch = os.environ.get('TMPDIR')
    if not scratch:
        raise SystemExit('Set TMPDIR to the lane scratch directory first.')
    with tempfile.TemporaryDirectory(prefix='claims-mutations-', dir=scratch) as directory:
        root = Path(directory)
        # Copy the complete local dependency tree: model contexts, generated-region
        # producers, records and captures. No network and no agency requests.
        names = subprocess.check_output(['git','ls-files','-c','-o','--exclude-standard','-z'],cwd=ROOT,text=True).split('\0')
        files = sorted({name for name in names if name and not name.startswith(('series/','inputs/')) and name != 'HANDUP.md'})
        for name in files:
            rel=Path(name)
            if not (ROOT/rel).is_file():
                continue
            (root/rel).parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(ROOT/rel,root/rel)
        # Region adapters require measured tracked producers. A disposable index is
        # sufficient; there is no commit, remote or branch change in the worker tree.
        subprocess.run(['git','init','-q',str(root)],check=True,capture_output=True)
        subprocess.run(['git','add','-f','--',*files],cwd=root,check=True,capture_output=True)
        def run():
            p = subprocess.run([sys.executable, '-B', str(root / 'tools/claims.py'), 'check', '--root', str(root)],
                               capture_output=True, text=True, timeout=180)
            return p.returncode, p.stdout + p.stderr
        status, output = run()
        if status:
            raise SystemExit('Baseline is not green: ' + output)
        rows = []
        def probe(name, path, mutate, required):
            target = root / path
            original = target.read_bytes()
            try:
                target.write_text(mutate(original.decode()))
                status, output = run()
                assert status == 1, (name, status)
                assert all(text in output for text in required), (name, required, output)
                messages = [line for line in output.splitlines() if line.startswith('claimscheck: ') and any(text in line for text in required)]
                rows.append(dict(mutation=name, file=path, red_exit=status, messages=messages[:8]))
                print(name + ': RED exit 1')
                for line in messages[:3]:
                    print(line)
            finally:
                target.write_bytes(original)
            status, output = run()
            assert status == 0, (name, 'restore', output)
            rows[-1]['restored_exit'] = status
            print(name + ': restored GREEN exit 0')
        probe('bound page number', 'concept/index.html', lambda s: s.replace('0.45 kWh/kg', '0.46 kWh/kg', 1),
              ['old=0.45 new=0.46 key=assumptions.eLN2', 'UNREGISTERED'])
        probe('new page number', 'concept/index.html', lambda s: s.replace('</body>', '<p>Capacity 314159 tonnes.</p></body>', 1),
              ['UNREGISTERED', '314159'])
        def delete_entry(s):
            data = json.loads(s)
            target = next(e for e in data['entries'] if e['owner'] and e['owner'].get('key') == 'assumptions.eLN2')
            data['entries'].remove(target)
            return json.dumps(data)
        probe('register entry deleted', 'research/claims/register.json', delete_entry, ['UNREGISTERED', 'value=0.45'])
        probe('known defect changed but listed', 'research/reports/README.md', lambda s: s.replace('by half in a single day', 'by seventy in a single day', 1),
              ['known defect no longer reproduces', 'old=half new=seventy'])
        def move_model(s):
            data = json.loads(s)
            data['assumptions']['eLN2'] = 0.55
            return json.dumps(data)
        probe('model figure moved', 'research/figures.json', move_model,
              ['"key":"assumptions.eLN2"', '"observed":"0.45"', '"expected":0.55'])
        def a11y(s):
            match = re.search(r'<p\b[^>]*>(?:(?!</p>).)*?0\.45 kWh/kg(?:(?!</p>).)*?</p>', s, re.S)
            assert match
            para = match[0].replace('0.45 kWh/kg', '', 1)
            para = para.replace('<p', '<p aria-label="0.45 kWh/kg"', 1)
            return s[:match.start()] + para + s[match.end():]
        probe('number moved into accessibility only', 'concept/index.html', a11y,
              ['UNREGISTERED aria-label value=0.45', 'key=assumptions.eLN2'])
        current = claims.extract(root,root/'dist.manifest')['occurrences']
        spans = [o for o in current if o['surface']=='model-span' and o['file']=='ship/index.html']
        if spans:
            key=spans[0]['raw']
            probe('unknown model span key', 'ship/index.html',
                  lambda s:s.replace('data-n="'+key+'"','data-n="claimsMissingKey"',1),
                  ['UNREGISTERED','claimsMissingKey'])
        # Direct rule plants isolate semantic refusals from ordinary drift errors.
        semantic=[]
        water=dict(raw='175',text='The model is delivering 175 t/h.',block='The model is delivering 175 t/h.',context='',before='The model is delivering ',after=' t/h.')
        if claims.water_basis_issue(water,'classes.P100.cycle.tph') is not None:
            semantic.append(dict(mutation='delivering release key',red_kind=claims.water_basis_issue(water,'classes.P100.cycle.tph')['kind']))
            water['text']='The model requests 175 t; released water is not suppression.'
            assert claims.water_basis_issue(water,'classes.P100.cycle.tph') is None
            semantic[-1]['restored']='GREEN';print('delivering release key: RED water-basis; restored GREEN')
        try:
            from claims_rules import Context
        except ImportError:
            Context = None
        if Context is not None and hasattr(Context,'reference_issue'):
            reference_file=root/'research/reports/reference-fixture.md'
            reference_file.write_text('# 1. Scope\n\nSee §2.\n')
            occ=dict(file='research/reports/reference-fixture.md',raw='2',after='.')
            assert Context(root,[occ['file']]).reference_issue(occ)['kind']=='broken-reference'
            reference_file.write_text('# 1. Scope\n\n# 2. Next\n\nSee §2.\n')
            assert Context(root,[occ['file']]).reference_issue(occ) is None
            reference_file.unlink()
            semantic.append(dict(mutation='broken section reference',red_kind='broken-reference',restored='GREEN'))
            print('broken section reference: RED broken-reference; restored GREEN')
        claims.write_json(ROOT / 'research/claims/mutation-evidence.json', dict(
            command='python3 -B research/claims/mutation_proof.py', baseline_exit=0,
            method='Disposable complete dependency tree and index; one mutation at a time, restore bytes and rerun after each.', mutations=rows, semantic_plants=semantic))
    print('All mutations were RED and every restoration GREEN; scratch copy discarded.')


if __name__ == '__main__':
    main()
