#!/usr/bin/env python3
"""Version-stamp the SITE's own modules — `sim/` and `app/` — the way 3d/ stamps itself.

WHY THIS EXISTS, and it is not hypothetical. The pages are served through a CDN that caches
JavaScript for four hours. `3d/` has been safe from that since it started stamping every import
with `?v=<hash>`; `sim/` and `app/` were not stamped at all, so a deploy did not take effect for
up to four hours — and worse, a visitor could be served a MIXED graph, with new `app/` code
calling old `sim/` code, which is a failure mode with no symptom except wrong numbers. It was
found by deploying a change and watching the live page report `anchorFromAglM` as undefined while
the file on the origin plainly had it.

WHY IT IS A SECOND TOOL RATHER THAN A WIDER FIRST ONE. `3d/scripts/stamp-version.py` is a
faithful port of `stamp-version.mjs` and the two must stay identical — that parity is itself a
check. It also deliberately refuses to stamp specifiers that resolve OUTSIDE `3d/`, on the
grounds that versioning another owner's URLs is not its business. This tool is that other owner.
The two trees hash separately, so a change to the model does not invalidate the 3D library's
cache and vice versa.

    python3 tools/stamp_site.py            # stamp
    python3 tools/stamp_site.py --check    # exit 1 if anything is stale
    python3 tools/stamp_site.py --strip    # remove the stamps
"""
import hashlib
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OWNED = ("sim", "app")
SKIP_DIRS = {"node_modules", "assets", ".git", "3d", "data", "pipeline", "tools", "docs"}

check = "--check" in sys.argv
strip = "--strip" in sys.argv


def walk(dir_, suffixes):
    out = []
    if not dir_.exists():
        return out
    for p in sorted(dir_.iterdir()):
        if p.name in SKIP_DIRS or p.name.startswith('.'):
            continue
        if p.is_dir():
            out += walk(p, suffixes)
        elif p.suffix in suffixes:
            out.append(p)
    return out


STAMP = re.compile(r"(\.m?js)\?v=[A-Za-z0-9_.-]+(['\"])")
# `from './x.js'` and `import('./x.js')`, the same two forms the 3D stamper handles.
SPEC = re.compile(r"(from\s*|import\s*\(\s*)(['\"])(\.{0,2}/?[^'\"?]+\.m?js)(?:\?[^'\"]*)?(['\"])")
# `<script type="module" src="./app/main.js">`, which the 3D tool never needed: its pages import
# the library from inline modules, and this one is the entry point of the whole application.
SRC = re.compile(r"(<script[^>]*\ssrc=)([\"'])([^\"'?]+\.m?js)(?:\?[^\"']*)?([\"'])")


def owned(path):
    """Is this file one of ours? Only sim/ and app/ are hashed and only they are stamped INTO."""
    try:
        rel = path.resolve().relative_to(ROOT)
    except ValueError:
        return False
    return rel.parts and rel.parts[0] in OWNED


def targets_owned(page, spec):
    """Does this relative specifier, resolved from `page`, land in sim/ or app/?

    normpath rather than resolve, so a symlinked checkout does not change the answer — and so
    this agrees with the 3D stamper about what resolution means."""
    return owned(Path(os.path.normpath(page.parent / spec)))


def strip_stamp(s):
    return STAMP.sub(r"\1\2", s)


modules = [p for p in walk(ROOT / "sim", {".js"}) + walk(ROOT / "app", {".js"})]

h = hashlib.sha256()
for p in sorted(modules, key=str):
    h.update(strip_stamp(p.read_text()).encode())
VERSION = h.hexdigest()[:8]


def stamp_source(page, src):
    q = "" if strip else f"?v={VERSION}"

    def one(m):
        if not targets_owned(page, m.group(3)):
            return m.group(0)
        return f"{m.group(1)}{m.group(2)}{m.group(3)}{q}{m.group(4)}"

    def one_src(m):
        if not targets_owned(page, m.group(3)):
            return m.group(0)
        return f"{m.group(1)}{m.group(2)}{m.group(3)}{q}{m.group(4)}"

    return SRC.sub(one_src, SPEC.sub(one, src))


# Anything in the repository may import the model — the page, the concept page, the lab, the
# test runners. All of them get stamped, because a stale specifier anywhere is a page that can
# be served a graph from two different generations.
pages = walk(ROOT, {".html"}) + walk(ROOT, {".js", ".mjs"})

changed, stale = 0, []
for p in sorted(set(pages), key=str):
    src = p.read_text()
    out = stamp_source(p, src)
    if out == src:
        continue
    changed += 1
    if check:
        stale.append(str(p.relative_to(ROOT)))
    else:
        p.write_text(out)

if not check and not strip:
    (ROOT / "sim" / "version.json").write_text(json.dumps(
        {"version": VERSION,
         "note": "sim/ + app/ content hash. tools/stamp_site.py stamps every import with it."},
        indent=2) + "\n")

if check:
    if stale:
        print(f"stamp-site: {len(stale)} file(s) are not stamped at {VERSION}:", file=sys.stderr)
        for f in stale[:12]:
            print(f"  {f}", file=sys.stderr)
        sys.exit(1)
    print(f"stamp-site: every import is stamped at ?v={VERSION}")
else:
    print(f"stamp-site: {changed} file(s) stamped at ?v={VERSION}")
