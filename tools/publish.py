#!/usr/bin/env python3
"""Copy the served subset of this repository into the website that deploys it.

    tools/publish.py --dest DIR            copy, reporting what changed
    tools/publish.py --dest DIR --check    change nothing; exit non-zero if the copy has drifted
    AIRSHIPS_SITE_DEST=DIR tools/publish.py [--check]    the same, destination from the environment

WHERE IT PUBLISHES is never built in. DIR is the published copy: the `airships/` directory
of the website tree that deploys these pages. Name it with `--dest`, or once per shell in
AIRSHIPS_SITE_DEST; `--dest` wins when both are given, and with neither the tool stops and
says so. A public repository has no business knowing where one maintainer keeps a website,
and a default that points at somebody's machine is wrong on every other one. (This is not
AIRSHIPS_PUBLISH_DEST: that one belongs to pipeline/live.py and names where the live-data
mirror is pushed, a directory this tool must never be aimed at.)

PUBLISHING PRUNES. Every file in DIR that the manifest does not list is removed, so that a
page deleted here stops being served. That makes a wrong DIR destructive, and the tool
therefore refuses two shapes outright: a DIR that is this repository, sits inside it or
contains it; and a DIR that already holds files but is not a published copy (it has no
index.html beside a sim/version.json). An empty or missing DIR is created. `--check` writes
nothing and only needs DIR to exist.

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
import os
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DEST_ENV = 'AIRSHIPS_SITE_DEST'


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


def resolve_dest(arg: pathlib.Path | None, check: bool) -> pathlib.Path:
    """The published copy: `--dest`, else the environment, and never a guess.

    Raises ValueError with a message fit to print. The refusals are here rather than at the
    point of writing because publishing prunes, and the prune is the dangerous half."""
    raw = str(arg) if arg is not None else os.environ.get(DEST_ENV, '').strip()
    if not raw:
        raise ValueError(
            f'no destination. Pass --dest DIR, or set {DEST_ENV}, to the directory that '
            'holds the published copy\n(the airships/ directory of the website tree). '
            'There is no built-in default.')
    dest = pathlib.Path(raw).expanduser()
    real = dest.resolve()
    if real == ROOT or ROOT in real.parents or real in ROOT.parents:
        raise ValueError(
            f'{dest} is this repository, inside it, or contains it. The published copy '
            'lives in the website tree,\nand publishing removes every file the manifest '
            'does not list.')
    if check:
        if not dest.is_dir():
            raise ValueError(f'{dest} is not a directory, so there is no published copy '
                             'to compare against.')
        return dest
    if dest.exists():
        if not dest.is_dir():
            raise ValueError(f'{dest} exists and is not a directory.')
        published = (dest / 'index.html').is_file() and (dest / 'sim' / 'version.json').is_file()
        # The live mirror may arrive before the first publish: the server owns data/live/,
        # and a directory holding only that is as good as empty.
        foreign = any(q.is_file() and not str(q.relative_to(dest)).startswith('data/live/')
                      for q in dest.rglob('*'))
        if foreign and not published:
            raise ValueError(
                f'{dest} holds files but is not a published copy of this site (no '
                'index.html beside a sim/version.json).\nPublishing removes every file '
                'the manifest does not list, so it will not start there.')
    return dest


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--check', action='store_true',
                    help='report drift between this repository and the published copy')
    ap.add_argument('--dest', type=pathlib.Path, default=None, metavar='DIR',
                    help=f'the published copy; defaults to ${DEST_ENV}, and to nothing else')
    args = ap.parse_args()

    try:
        dest = resolve_dest(args.dest, args.check)
    except ValueError as e:
        print(f'publish.py: {e}', file=sys.stderr)
        return 2

    served, excluded, partial = read_manifest()
    unclassified = check_complete(served, excluded)
    if unclassified:
        print("dist.manifest does not classify:", ", ".join(unclassified))
        print("Add each as `served` or `excluded` and say why. Publishing stops here.")
        return 2

    files = list(wanted_files(served, partial))

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
