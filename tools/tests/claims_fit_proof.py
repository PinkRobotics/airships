#!/usr/bin/env python3
"""Plant audit prose and carry drift on a disposable copy; never fetch a feed."""
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]


def run(tree, argv, expected=0):
    result = subprocess.run(argv, cwd=tree, capture_output=True, text=True, timeout=240)
    output = (result.stdout + result.stderr).replace(str(tree), '<fixture>')
    relevant = [line for line in output.splitlines() if any(word in line for word in
                ('claimscheck:', 'ledgercheck:', 'research/claims/', 'Ran ', 'OK', 'FAIL'))]
    print('COMMAND ' + ' '.join(argv) + f' EXIT {result.returncode}', flush=True)
    print('\n'.join(relevant[-12:]), flush=True)
    if expected == 'red':
        assert result.returncode != 0, output
    else:
        assert result.returncode == expected, output
    return output


def main():
    files = subprocess.check_output(['git', 'ls-files', '--cached', '--others',
                                    '--exclude-standard', '-z'], cwd=ROOT).decode().split('\0')
    # Ignored gate inputs are required in disposable mutation trees too.
    files_extra = ['research/claims/' + name for name in
                   ('register.json', 'carry-history.json', 'rule-changes.json', 'accepted-defects.json')]
    files.extend(files_extra)
    with tempfile.TemporaryDirectory(prefix='claims-fit-proof-', dir=os.environ['TMPDIR']) as tmp:
        tree = Path(tmp)
        for rel in files:
            if not rel or rel.startswith(('inputs/', 'series/')) or rel == 'HANDUP.md':
                continue
            src = ROOT / rel
            if src.is_file():
                dst = tree / rel
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
        (tree / '.git').symlink_to(ROOT / '.git', target_is_directory=True)
        for name in sorted((tree / 'research/claims').glob('*.md')):
            original = name.read_bytes()
            try:
                name.write_bytes(original + b'\nThe 52 m hull floats at sea level.\n')
                out = run(tree, ['make', 'ledgercheck'], 'red')
                assert name.relative_to(tree).as_posix() in out and 'No disposition' in out, out
            finally:
                name.write_bytes(original)
            run(tree, ['make', 'ledgercheck'])
            print(f'PAIR {name.relative_to(tree)} RED then restored GREEN', flush=True)
        # Also prove TSV edits and omissions fail the actual make-check member gate.
        for name in ('carry-report.tsv', 'nonclaim-reclassifications.tsv', 'page-defects.tsv'):
            path = tree / 'research/claims' / name
            original = path.read_bytes()
            for mode in ('append', 'missing'):
                try:
                    if mode == 'append':
                        path.write_bytes(original + b'\nThe 52 m hull floats at sea level.\n')
                    else:
                        path.unlink()
                    out = run(tree, ['python3', '-B', 'tools/claims.py', 'check'], 'red')
                    assert name + ': missing or stale audit table' in out, out
                finally:
                    path.write_bytes(original)
        run(tree, ['make', 'claimscheck'])
        records = {p.relative_to(tree).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                   for p in (tree / 'research/analysis/float-claims').glob('*.json')}
        register = tree / 'research/claims/register.json'
        old = register.read_bytes()
        source = tree / 'GOALS.md'
        source.write_text(source.read_text() + '\nVision: 314159 seconds of review.\n')
        run(tree, ['python3', '-B', 'tools/claims.py', 'carry'])
        assert register.read_bytes() != old, 'carry plant did not change the register'
        run(tree, ['make', 'claimscheck'])
        run(tree, ['make', 'ledgercheck'])
        assert records == {p.relative_to(tree).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in (tree / 'research/analysis/float-claims').glob('*.json')}
        before = {p.name: p.read_bytes() for p in (tree / 'research/claims').iterdir() if p.is_file()}
        run(tree, ['python3', '-B', 'tools/claims.py', 'carry'])
        assert before == {p.name: p.read_bytes() for p in (tree / 'research/claims').iterdir() if p.is_file()}
        print('CARRY changed register; claimscheck and ledgercheck GREEN; float records unchanged; second carry byte-identical', flush=True)
    print('All audit plants RED and restorations GREEN; disposable copy removed.', flush=True)


if __name__ == '__main__':
    main()
