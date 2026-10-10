#!/usr/bin/env python3
"""Materialize missing claims records from their reviewed Git source, offline."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
OUTPUTS = ('register.json', 'carry-history.json', 'rule-changes.json', 'accepted-defects.json')


def restore(root):
    directory = root / 'research/claims'
    source = json.loads((directory / 'restore-source.json').read_text())
    if (source.get('version') != 1 or
            not re.fullmatch(r'[0-9a-f]{40}', source.get('commit', '')) or
            set(source.get('files', {})) != set(OUTPUTS)):
        raise ValueError('invalid claims restoration source')
    missing = []
    for name in OUTPUTS:
        target = directory / name
        if target.is_symlink():
            raise ValueError(f'{name}: refusing a symlink')
        if target.exists():
            if not target.is_file():
                raise ValueError(f'{name}: existing path is not a file')
            continue
        pin = source['files'][name]
        result = subprocess.run(
            ['git', '-C', str(root), 'show', source['commit'] + ':research/claims/' + name],
            capture_output=True, check=False)
        if result.returncode:
            raise ValueError('pinned source unavailable; use a Git clone with the source commit (see claims README)')
        data = result.stdout
        if len(data) != pin['bytes'] or hashlib.sha256(data).hexdigest() != pin['sha256']:
            raise ValueError(f'{name}: pinned bytes/hash mismatch')
        missing.append((target, data))
    # Validate every source before writing any record. An exclusive hard link preserves
    # another contributor's local output if it appears during restoration.
    for target, data in missing:
        with tempfile.NamedTemporaryFile(dir=directory, prefix='.claimsrestore-') as output:
            output.write(data)
            output.flush()
            os.fsync(output.fileno())
            try:
                os.link(output.name, target)
            except FileExistsError:
                raise ValueError(f'{target.name}: appeared during restoration; left untouched')
        print(f'claimsrestore: restored {target.name} ({len(data)} bytes)')
    if not missing:
        print('claimsrestore: existing local records left untouched')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        restore(args.root.resolve())
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'claimsrestore: FAIL ({type(exc).__name__}): {str(exc).replace(str(args.root.resolve()), "<root>")}', file=sys.stderr)
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
