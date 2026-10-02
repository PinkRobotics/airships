#!/usr/bin/env python3
"""Compare the executable CI gate command with Makefile's check prerequisites.

The deliberately narrow contract is one explicit prerequisite list and one unconditional
CI step containing a literal make command. Unsupported indirection fails, rather than
silently interpreting a different list. No gate names are copied into this checker.
"""
import argparse
from pathlib import Path
import re
import shlex
import sys

import yaml

ROOT = Path(__file__).resolve().parent.parent
GATE = re.compile(r"[a-z][a-z0-9-]*\Z")


def validate_gates(gates):
    if not gates or any(not GATE.fullmatch(g) for g in gates):
        raise ValueError("gate list must contain explicit target names")
    if len(gates) != len(set(gates)):
        raise ValueError("duplicate gate in list")
    return gates


def make_gates(text):
    logical = re.sub(r"\\\n[ \t]*", " ", text)
    rows = re.findall(r"^check:[ \t]*([^\n]*)", logical, re.M)
    if len(rows) != 1:
        raise ValueError("expected exactly one explicit check: prerequisite list")
    return validate_gates(rows[0].split("#", 1)[0].split())


def ci_gates(text):
    doc = yaml.safe_load(text)
    job = doc["jobs"]["checks"]
    steps = [s for s in job["steps"] if s.get("id") == "check-gates"]
    if len(steps) != 1:
        raise ValueError("expected one checks/check-gates step")
    step = steps[0]
    for mapping in (job, step):
        if "if" in mapping or mapping.get("continue-on-error", False):
            raise ValueError("gate job and step must be unconditional and fail on error")
    command = shlex.split(step["run"])
    if command[:2] != ["make", "--keep-going"]:
        raise ValueError("check-gates must run make --keep-going followed by literal gates")
    return validate_gates(command[2:])


def check(root=ROOT):
    local = make_gates((root / "Makefile").read_text())
    remote = ci_gates((root / ".github/workflows/ci.yml").read_text())
    if local != remote:
        missing = [g for g in local if g not in remote]
        extra = [g for g in remote if g not in local]
        raise ValueError(f"CI parity FAIL: missing={missing}, extra={extra}; "
                         f"ordered lists equal={local == remote}")
    return local


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=ROOT)
    args = ap.parse_args()
    try:
        gates = check(args.root)
    except (OSError, ValueError, KeyError, TypeError, yaml.YAMLError) as exc:
        print(f"CI parity: {exc}", file=sys.stderr)
        return 1
    print(f"CI parity PASS: {len(gates)} ordered gates: {' '.join(gates)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
