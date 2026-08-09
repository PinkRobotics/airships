#!/usr/bin/env python3
"""Copy the served subset of this repository into the website that deploys it.

    tools/publish.py            copy, reporting what changed
    tools/publish.py --check    change nothing; exit non-zero if the copy has drifted
    tools/publish.py --dest DIR publish somewhere else

WHY A COPY AND NOT A BUILD. There is no build. The modules the browser executes are the
modules in this repository, byte for byte, which is the only version of "you can check our
arithmetic" that survives contact with a skeptic. Publishing is therefore a file copy plus
a cache-busting stamp, and `--check` exists so that a hand-edit made downstream — in the
deployed tree, where it would be invisible here — fails loudly instead of quietly becoming
the truth.

WHAT IS SERVED is decided by dist.manifest, which must classify every top-level entry.
An unclassified entry is an error rather than a default, because both defaults are wrong:
serving something by accident puts test harnesses on a public host, and omitting something
by accident ships a page whose imports 404.

data/live/ is never published from here. It is written on the server by pipeline/live.py
every ten minutes, and the repository's copy of it is always older than the server's.
"""
from __future__ import annotations

import argparse
import filecmp
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_DEST = pathlib.Path('/home/tyler/dev/pink-sites/pinkrobotics/airships')


def read_manifest() -> tuple[set[str], set[str], set[str]]:
    served, excluded, partial = set(), set(), set()
    for raw in (ROOT / 'dist.manifest').read_text().split('\n'):
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        parts = line.split(None, 2)
        if len(parts) < 2:
            continue
        kind, name = parts[0], parts[1]
        if kind == 'served':
            served.add(name)
        elif kind == 'excluded':
            excluded.add(name)
        elif kind == 'PARTIAL':
            partial.add(name)
    return served, excluded, partial


def check_complete(served: set[str], excluded: set[str]) -> list[str]:
    """Every top-level entry must be classified, or publishing is a guess."""
    known = served | excluded
    present = {p.name for p in ROOT.iterdir() if p.name != '.git'}
    return sorted(present - known)


def wanted_files(served: set[str], partial: set[str]):
    """Every file to publish, as (source, path-relative-to-destination)."""
    for name in sorted(served):
        src = ROOT / name
        if src.is_file():
            yield src, pathlib.Path(name)
            continue
        for p in sorted(src.rglob('*')):
            if not p.is_file():
                continue
            rel = p.relative_to(ROOT)
            if any(str(rel).startswith(x + '/') or str(rel) == x for x in partial):
                continue
            if '__pycache__' in rel.parts or rel.name == '.DS_Store':
                continue
            yield p, rel


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--check', action='store_true',
                    help='report drift between this repository and the published copy')
    ap.add_argument('--dest', type=pathlib.Path, default=DEFAULT_DEST)
    args = ap.parse_args()

    served, excluded, partial = read_manifest()
    unclassified = check_complete(served, excluded)
    if unclassified:
        print("dist.manifest does not classify:", ", ".join(unclassified))
        print("Add each as `served` or `excluded` and say why. Publishing stops here.")
        return 2

    files = list(wanted_files(served, partial))
    dest = args.dest

    if args.check:
        missing, differing = [], []
        for src, rel in files:
            tgt = dest / rel
            if not tgt.exists():
                missing.append(str(rel))
            elif not filecmp.cmp(src, tgt, shallow=False):
                differing.append(str(rel))
        stray = []
        for p in dest.rglob('*'):
            rel = p.relative_to(dest)
            if not p.is_file() or str(rel).startswith('data/live/'):
                continue
            if rel not in {r for _, r in files}:
                stray.append(str(rel))
        if missing or differing or stray:
            print(f"published copy has drifted from {ROOT}:")
            for label, items in (('missing', missing), ('differs', differing),
                                 ('not in the manifest', stray)):
                for i in items[:20]:
                    print(f"  {label:20s} {i}")
                if len(items) > 20:
                    print(f"  {label:20s} … and {len(items) - 20} more")
            return 1
        print(f"published copy matches: {len(files)} files")
        return 0

    copied = 0
    for src, rel in files:
        tgt = dest / rel
        if tgt.exists() and filecmp.cmp(src, tgt, shallow=False):
            continue
        tgt.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, tgt)
        copied += 1

    # Anything in the destination that this repository no longer serves, except the live
    # mirror, which belongs to the server.
    removed = 0
    keep = {r for _, r in files}
    for p in sorted(dest.rglob('*'), reverse=True):
        rel = p.relative_to(dest)
        if str(rel).startswith('data/live'):
            continue
        if p.is_file() and rel not in keep:
            p.unlink()
            removed += 1
        elif p.is_dir() and not any(p.iterdir()):
            p.rmdir()

    print(f"published {len(files)} files to {dest}  ({copied} changed, {removed} removed)")
    print("data/live/ left alone — the server owns it")
    return 0


if __name__ == '__main__':
    sys.exit(main())
