#!/usr/bin/env python3
"""Faithful port of stamp-version.mjs for machines without node (this box has none).

Same algorithm, same regexes, same output: the version is sha256 over the STRIPPED contents
of every module (sorted by absolute path), truncated to 8 hex chars; every relative .js/.mjs
specifier that resolves into this tree — in the modules and in every HTML page of the
repository that imports it — is stamped `?v=<version>`; version.json is rewritten. Running
either stamper after the other is a no-op — if it is not, one of them has drifted and THAT
is the bug to fix. See stamp-version.mjs for the full rationale.

    python3 scripts/stamp-version.py            # stamp
    python3 scripts/stamp-version.py --check    # fail if the stamp is stale
    python3 scripts/stamp-version.py --strip    # remove the stamps
"""
import hashlib
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
SITE = ROOT.parent

check = "--check" in sys.argv
strip = "--strip" in sys.argv

SKIP_DIRS = {"node_modules", "assets", ".git"}


def walk(dir_, suffixes):
    out = []
    for p in sorted(dir_.iterdir()):
        if p.name in SKIP_DIRS:
            continue
        if p.is_dir():
            out += walk(p, suffixes)
        elif p.suffix in suffixes:
            out.append(p)
    return out


# JS side: `walkFiles(ROOT).filter((p) => !p.includes('scripts/'))` on the absolute path.
modules = [p for p in walk(ROOT, {".js", ".mjs"}) if "scripts/" not in str(p)]

STAMP = re.compile(r"(\.m?js)\?v=[A-Za-z0-9_.-]+(['\"])")
SPEC = re.compile(r"(from\s*|import\s*\(\s*)(['\"])(\.{1,2}/[^'\"?]+\.m?js)(?:\?[^'\"]*)?(['\"])")


def targets_tree(page, spec):
    """Does this relative specifier, resolved from `page`, land inside the module tree?

    Only those get stamped. A page may import this tree and someone else's modules in the
    same block — `model-lab/` may import `sim/` — and rewriting the other owner's URLs
    would version files they have deliberately left unversioned.

    normpath, not resolve: node's path.resolve does not follow symlinks either, and the two
    stampers have to agree about which files they own."""
    target = Path(os.path.normpath(page.parent / spec))
    return target == ROOT or ROOT in target.parents


def imports_tree(page):
    return any(targets_tree(page, m.group(3)) for m in SPEC.finditer(page.read_text()))


# HTML entry points are DISCOVERED by resolving their import specifiers, not listed by path.
# The list was `walk(ROOT)` plus a literal <site>/airships/model-lab/index.html — the path the
# lab page had inside the private website repository. Nothing is at that path here, so the lab
# was neither stamped nor checked: it imported `?v=41bc1f51` while the tree hashed to
# `f3cb948e`, and `--check` still exited 0. Resolving the specifier finds the page wherever it
# is, which is the only form of this list that a later move cannot silently empty.
html_entries = [p for p in walk(SITE, {".html"}) if imports_tree(p)]

# JS entry points OUTSIDE the tree that import into it — cell/explorer.js was the first.
# Without this, a module in another owner's tree holds unversioned ../3d/ specifiers, and a
# CDN serves it a stale graph for exactly as long as its cache pleases: the renderer fix of
# 2026-08-11 would have been invisible behind Cloudflare. Discovery is by resolving
# specifiers, same as the HTML entries and for the same reason. (Mirrored in the .mjs.)
def inside_tree(p: Path) -> bool:
    q = Path(os.path.normpath(p))
    return q == ROOT or ROOT in q.parents


js_entries = [p for p in walk(SITE, {".js", ".mjs"})
              if not inside_tree(p) and imports_tree(p)]


def strip_stamp(s):
    return STAMP.sub(r"\1\2", s)


h = hashlib.sha256()
for p in sorted(modules, key=lambda q: str(q)):
    h.update(strip_stamp(p.read_text()).encode())
VERSION = h.hexdigest()[:8]


def stamp_source(page, src):
    def one(m):
        if not targets_tree(page, m.group(3)):
            return m.group(0)
        q = "" if strip else f"?v={VERSION}"
        return f"{m.group(1)}{m.group(2)}{m.group(3)}{q}{m.group(4)}"
    return SPEC.sub(one, src)


changed, stale = 0, []
for p in modules + html_entries + js_entries:
    src = p.read_text()
    out = stamp_source(p, src)
    if out == src:
        continue
    changed += 1
    if check:
        stale.append(str(p.relative_to(SITE)))
    else:
        p.write_text(out)

# Foreign pages that import the tree unversioned are REPORTED, never edited.
foreign = []
FOREIGN = re.compile(r"3d/index\.js(?!\?v=)")
for p in walk(SITE, {".html"}):
    if ROOT in p.parents or p in html_entries:
        continue
    if FOREIGN.search(p.read_text()):
        foreign.append(str(p.relative_to(SITE)))
if foreign:
    print(f"stamp: NOTE — unversioned 3d/ imports (can be served a stale graph):\n  "
          + "\n  ".join(foreign), file=sys.stderr)

if not check and not strip:
    (ROOT / "version.json").write_text(json.dumps(
        {"version": VERSION, "note": "Pin dynamic imports to this. See scripts/stamp-version.mjs."},
        indent=2) + "\n")

if check:
    if stale:
        print(f"stamp: {len(stale)} file(s) are not stamped at {VERSION}:", file=sys.stderr)
        for f in stale[:12]:
            print(f"  {f}", file=sys.stderr)
        sys.exit(1)
    print(f"stamp: all module URLs carry ?v={VERSION}")
else:
    print(f"stamp: removed version queries from {changed} file(s)" if strip
          else f"stamp: {changed} file(s) stamped at ?v={VERSION}")
