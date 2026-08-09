#!/usr/bin/env python3
"""Semantic diff of two golden dumps. Reports WHAT changed, not that bytes differ.
Usage: gdiff.py baseline.json candidate.json [--tol 1e-9]"""
import json, sys

a = json.load(open(sys.argv[1])); b = json.load(open(sys.argv[2]))
TOL = float(sys.argv[sys.argv.index('--tol') + 1]) if '--tol' in sys.argv else 0.0
diffs = []

def walk(pa, pb, path):
    if type(pa) is not type(pb) and not (isinstance(pa, (int, float)) and isinstance(pb, (int, float))):
        diffs.append(f"{path}: type {type(pa).__name__} -> {type(pb).__name__}"); return
    if isinstance(pa, dict):
        for k in sorted(set(pa) | set(pb)):
            if k not in pa: diffs.append(f"{path}.{k}: ADDED = {json.dumps(pb[k])[:120]}")
            elif k not in pb: diffs.append(f"{path}.{k}: REMOVED")
            else: walk(pa[k], pb[k], f"{path}.{k}")
    elif isinstance(pa, list):
        if len(pa) != len(pb):
            diffs.append(f"{path}: length {len(pa)} -> {len(pb)}")
        for i in range(min(len(pa), len(pb))): walk(pa[i], pb[i], f"{path}[{i}]")
    elif isinstance(pa, (int, float)) and not isinstance(pa, bool):
        if pa != pb and (TOL == 0 or abs(pa - pb) > TOL * max(1.0, abs(pa))):
            diffs.append(f"{path}: {pa} -> {pb}")
    elif pa != pb:
        diffs.append(f"{path}: {json.dumps(pa)[:80]} -> {json.dumps(pb)[:80]}")

walk(a, b, '')
if not diffs:
    print("IDENTICAL — every simulation output matches the baseline")
else:
    print(f"{len(diffs)} DIFFERENCES:")
    for d in diffs[:120]: print("  " + d)
    if len(diffs) > 120: print(f"  ... and {len(diffs)-120} more")
sys.exit(1 if diffs else 0)
