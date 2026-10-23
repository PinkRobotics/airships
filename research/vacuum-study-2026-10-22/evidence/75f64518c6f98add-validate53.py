"""Custody, consistency and execution-record checks for delivery."""
from pathlib import Path
from datetime import datetime
from collections import Counter
import ast
import csv
import gzip
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
checks = []


def strict(text):
    def reject(token):
        raise ValueError("Nonfinite JSON [credential]
    return json.loads(text, parse_constant=reject)


def read(name):
    return strict((ROOT/name).read_text())


def save(name, data):
    (ROOT/name).write_text(json.dumps(data, indent=2, allow_nan=False)+"\n")


def check(name, passed, **detail):
    checks.append(dict(check=name, passed=bool(passed), **detail))


def pin(path):
    data = path.read_bytes()
    return dict(path=str(path), bytes=len(data), sha256=hashlib.sha256(data).hexdigest())


pins = []
for item in read("INPUT-PINS.json"):
    frozen = pin(ROOT/item["snapshot"])
    original = pin(Path(item["path"]))
    frozen_ok = all(frozen[k] == item[k] for k in ["bytes", "sha256"])
    live_ok = all(original[k] == item[k] for k in ["bytes", "sha256"])
    pins.append(dict(snapshot=item["snapshot"], original=item["path"],
                     frozen_matches=frozen_ok, live_matches=live_ok,
                     expected_sha256=item["sha256"], actual_live_sha256=original["sha256"]))
    check("frozen input pin", frozen_ok, path=item["snapshot"])
save("PIN-VALIDATION.json", pins)
for item in read("SOURCE-PINS.json"):
    measured = pin(Path(item["path"]))
    check("retrieved source pin", all(measured[k] == item[k] for k in ["bytes", "sha256"]),
          path=item["relative"])
for item in read("SOURCE-INTAKE.json"):
    if item["status"] == "retrieved":
        measured = pin(ROOT/item["path"])
        check("source retrieval bytes and digest",
              all(measured[k] == item[k] for k in ["bytes", "sha256"]), path=item["path"])
        check("retrieved PDF signature", (ROOT/item["path"]).read_bytes().startswith(b"%PDF"),
              path=item["path"])

for path in sorted(ROOT.glob("*.json")):
    if path.name in ["VALIDATION.json", "MANIFEST.json", "TIMING.json"]:
        continue
    strict(path.read_text())
    check("strict output JSON", True, file=path.name)
for path in sorted(ROOT.glob("*.py")):
    ast.parse(path.read_text(), filename=str(path))
    check("own script syntax", True, file=path.name)

result = read("RESULTS.json")
check("all scientific comparisons pass",
      result["thermal_comparisons"] == result["thermal_comparisons_passed"] == 118499
      and result["accounting_audit_failed"] == 0
      and result["owner_boundary_reply_comparisons_passed"] == 46)
check("all accounting audit rows pass", all(r["passed"] for r in read("ACCOUNT-AUDIT.json")))
check("all independent thermal invariants pass", all(r["passed"] for r in read("THERMAL-INVARIANTS.json")))
check("all direct thermal guards pass", all(r["passed"] for r in read("DIRECT-THERMAL-CHECKS.json")))
check("all owner boundary reply rows pass", all(r["passed"] for r in read("BOUNDARY-REPLY-COMPARISONS.json")))
check("local energy residual", result["maximum_energy_residual_W_m2"] < 1e-7,
      residual_W_m2=result["maximum_energy_residual_W_m2"])
check("global external energy residual", result["maximum_global_external_residual_W_m2"] < 1e-7,
      residual_W_m2=result["maximum_global_external_residual_W_m2"])
check("cavity conservation", result["maximum_cavity_relative_residual"] < 1e-10,
      relative_residual=result["maximum_cavity_relative_residual"])
for name in ["THERMAL-REPRODUCTION-DIFFERENCES.json", "ACCOUNT-AUDIT-DIFFERENCES.json",
             "ENDPOINT-FLOAT-CHANGES.json", "LEAST-SET-CHANGES.json", "LEAST-TIED-SET-CHANGES.json"]:
    check("no unaccounted differences", read(name) == [], file=name)
for filename, count in [("THERMAL-TABLES.csv", 9640), ("THERMAL-REFERENCE.csv", 40),
                        ("PAYLOAD-AND-BOND.csv", 360), ("SUBSET-ENDPOINTS.csv", 5760),
                        ("RESIZED-CONSEQUENCES.csv", 288)]:
    with (ROOT/filename).open() as stream:
        rows = list(csv.DictReader(stream))
    check("CSV delivery count", len(rows) == count, file=filename, count=len(rows), expected=count)
with gzip.open(ROOT/"THERMAL-REPRODUCTION.jsonl.gz", "rt") as stream:
    ledger_count = sum(1 for line in stream if strict(line))
check("compressed comparison ledger count", ledger_count == 118499, count=ledger_count)

jobs = []
for directory in sorted((ROOT/"execution").iterdir()):
    if not directory.is_dir():
        continue
    attempts = [strict(path.read_text()) for path in sorted(directory.glob("attempt-*.json"))]
    if not attempts:
        continue
    check("job final success", attempts[-1]["returncode"] == 0, label=directory.name)
    for j, record in enumerate(attempts):
        check("unchanged authorized resource request",
              record["resources"] == dict(cores=1, memory="1G", timeout_seconds=7200),
              label=directory.name, attempt=j+1)
        check("execution streams exist", Path(record["stdout"]).is_file() and Path(record["stderr"]).is_file(),
              label=directory.name, attempt=j+1)
        jobs.append(dict(label=directory.name, attempt=j+1, started=record["started"],
                         finished=record["finished"], elapsed_seconds=record["elapsed_seconds"],
                         returncode=record["returncode"]))
        if record["returncode"] == 75:
            check("refusal has a recorded retry", j+1 < len(attempts), label=directory.name, attempt=j+1)
            if j+1 < len(attempts):
                nxt = attempts[j+1]
                gap = (datetime.fromisoformat(nxt["started"])-datetime.fromisoformat(record["finished"])).total_seconds()
                check("refusal retry same command", record["argv"] == nxt["argv"],
                      label=directory.name, attempt=j+1)
                check("refusal retry at least one minute apart", gap >= 60,
                      label=directory.name, attempt=j+1, gap_seconds=gap)
    required = {
        "thermal-tables": ["thermal53.py", "settle_thermal53.py"],
        "account-audit": ["thermal53.py", "account53.py", "consequences53.py"],
        "scientific-figures": ["plot53.py"],
    }.get(directory.name, ["account53.py"] if directory.name.startswith("account-") else ["thermal53.py"])
    old_pins = {Path(r["path"]).name: r for r in attempts[-1]["source_pins"]}
    for name in required:
        check("executed scientific source matches delivered source",
              pin(ROOT/name)["sha256"] == old_pins[name]["sha256"], label=directory.name, file=name)

# Relative artifact links are checked after final TIMING/MANIFEST paths are created.
deferred = {"TIMING.json", "MANIFEST.json", "VALIDATION.json"}
for doc in ["CARD.md", "METHOD.md", "SPECIFICATION.md"]:
    for target in re.findall(r"\[[^]]*\]\(([^)]+)\)", (ROOT/doc).read_text()):
        if "://" not in target and target not in deferred:
            check("local document link exists", (ROOT/target).exists(), doc=doc, target=target)
check("NFI qualifications retained", read("NFI.json")["count_new"] == 9
      and len(read("NFI.json")["inherited_registers"]) == 6
      and read("NFI.json")["installed_hull_SF"] is None)
check("figure reviewed", read("VISUAL-REVIEW.json")["passed"])
check("no installed qualification claimed", result["installed_hull_SF"] is None
      and result["physical_boundary_qualification"] == "OPEN")

now = datetime.now().astimezone()
started = datetime.fromisoformat(read("START.json")["started"])
save("TIMING.json", dict(started=started.isoformat(), completed=now.isoformat(),
                          elapsed_wall_seconds=(now-started).total_seconds(), no_time_budget=True,
                          simjob_attempts=len(jobs), job_families=len({r["label"] for r in jobs}),
                          returncode_counts=dict(Counter(str(r["returncode"]) for r in jobs)),
                          sum_simjob_attempt_elapsed_seconds=sum(r["elapsed_seconds"] for r in jobs),
                          sum_elapsed_note="Sum of attempt durations; overlapping jobs mean this is not whole-task wall time or CPU usage.",
                          jobs=jobs))
validation = dict(at=now.isoformat(), checks=len(checks), passed=sum(r["passed"] for r in checks),
                  failed=sum(not r["passed"] for r in checks),
                  frozen_inputs=len(pins), frozen_inputs_match=sum(r["frozen_matches"] for r in pins),
                  live_inputs_unchanged=sum(r["live_matches"] for r in pins),
                  live_input_drift=[r for r in pins if not r["live_matches"]],
                  source_files=len(read("SOURCE-PINS.json")), results=checks)
save("VALIDATION.json", validation)
print(json.dumps({k: v for k, v in validation.items() if k != "results"}, indent=2))
for row in checks:
    if not row["passed"]:
        print(json.dumps(row))
raise SystemExit(1 if validation["failed"] else 0)
