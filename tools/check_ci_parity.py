#!/usr/bin/env python3
"""Compare the executable CI gate command with Makefile's check prerequisites.

The main job runs the explicit check prerequisites in order. CI_OUTSIDE_CHECK
names real targets, each run exactly once by a literal make step in an independent,
unconditional job. Unsupported indirection fails. No gate names are copied here.
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


def outside_gates(text):
    logical = re.sub(r"\\\n[ \t]*", " ", text)
    rows = re.findall(r"^CI_OUTSIDE_CHECK[ \t]*:=[ \t]*([^\n]*)", logical, re.M)
    if not rows:
        return []  # Older, unsplit trees retain their original contract.
    if len(rows) != 1:
        raise ValueError('expected one literal CI_OUTSIDE_CHECK assignment')
    gates = validate_gates(rows[0].split('#', 1)[0].split())
    for gate in gates:
        if len(re.findall(r'^' + re.escape(gate) + r':[ \t]*(?:[^=\n]*)$', logical, re.M)) != 1:
            raise ValueError(f'outside gate {gate} must be a real, explicit Makefile target')
    return gates


def check_split(doc, outside):
    # PyYAML's YAML 1.1 loader reads the unquoted GitHub key "on" as True.
    events = doc.get('on', doc.get(True))
    if outside and (not isinstance(events, dict) or set(events) != {'push', 'pull_request'}):
        raise ValueError('split gates require every push and pull_request')
    if outside and any(value not in (None, {}) for value in events.values()):
        raise ValueError('split gates must have unfiltered triggers')
    seen = {gate: [] for gate in outside}
    for job_name, job in doc['jobs'].items():
        for step in job.get('steps', []):
            run = step.get('run', '')
            command = shlex.split(run)
            if 'make' in command and command[0] != 'make':
                raise ValueError('CI make gates require a literal make step')
            if not command or command[0] != 'make':
                continue
            if job_name == 'checks' and step.get('id') == 'check-gates':
                goals = ci_gates(yaml.safe_dump(doc))
            else:
                if command[:2] == ['make', '--keep-going']:
                    goals = validate_gates(command[2:])
                else:
                    goals = validate_gates(command[1:])
                if len(goals) != 1 or goals[0] not in outside:
                    raise ValueError('extra CI make gate outside the checked contract')
                if job_name == 'checks' or 'needs' in job:
                    raise ValueError('outside gates require an independent job beside checks')
                for mapping in (job, step):
                    if 'if' in mapping or mapping.get('continue-on-error', False):
                        raise ValueError('outside gate job and step must be unconditional and fail on error')
            for gate in goals:
                if gate in seen:
                    seen[gate].append(job_name)
    for gate, jobs in seen.items():
        if len(jobs) != 1:
            raise ValueError(f'outside gate {gate} must run exactly once; jobs={jobs}')


def check(root=ROOT):
    text = (root / 'Makefile').read_text()
    local = make_gates(text)
    outside = outside_gates(text)
    if set(local) & set(outside):
        raise ValueError('CI_OUTSIDE_CHECK and check must be disjoint')
    workflow = (root / '.github/workflows/ci.yml').read_text()
    remote = ci_gates(workflow)
    if local != remote:
        missing = [g for g in local if g not in remote]
        extra = [g for g in remote if g not in local]
        raise ValueError(f"CI parity FAIL: missing={missing}, extra={extra}; "
                         f"ordered lists equal={local == remote}")
    check_split(yaml.safe_load(workflow), outside)
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
    print(f"CI parity PASS: {len(gates)} ordered main gates: {' '.join(gates)}")
    print('Independent CI targets: ' + ' '.join(outside_gates((args.root / 'Makefile').read_text())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
