#!/usr/bin/env python3
"""Bound each tracked file and print the largest files; inspect the working tree."""
import argparse
from pathlib import Path
import subprocess

LIMIT = 25 * 1024 * 1024
ROOT = Path(__file__).resolve().parents[1]


def check(root, limit=LIMIT):
    names = subprocess.check_output(['git', '-C', str(root), 'ls-files', '-z']).decode().split('\0')
    sizes = []
    missing = []
    for name in names:
        if not name:
            continue
        try:
            sizes.append(((root / name).lstat().st_size, name))
        except FileNotFoundError:
            missing.append(name)
    sizes.sort(key=lambda item: (-item[0], item[1]))
    print('Largest tracked files (bytes):')
    for size, name in sizes[:10]:
        print(f'{size}\t{name}')
    for name in missing:
        print(f'reposizecheck: FAIL missing tracked file {name}')
    oversized = [(size, name) for size, name in sizes if size > limit]
    for size, name in oversized:
        print(f'reposizecheck: FAIL {name}: {size} bytes exceeds {limit}')
    failed = bool(missing or oversized)
    print(f'reposizecheck: {"FAIL" if failed else "PASS"}; {len(sizes)} tracked files; limit {limit} bytes')
    return int(failed)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--limit', type=int, default=LIMIT, help='Byte limit; smaller limits support fixture tests.')
    args = parser.parse_args()
    if args.limit < 1:
        parser.error('limit must be positive')
    return check(args.root, args.limit)


if __name__ == '__main__':
    raise SystemExit(main())
