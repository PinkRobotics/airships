"""Verify and pin the fold supplement without modifying prior scientific artifacts."""

import csv
from datetime import datetime
import hashlib
import json
from pathlib import Path
import re
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
checks = []


def read(name):
    return json.loads((ROOT / name).read_text())


def write(name, value):
    (ROOT / name).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def pin(path):
    data = path.read_bytes()
    return dict(path=str(path.resolve()), sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))


def check(name, passed):
    checks.append(dict(name=name, passed=bool(passed)))
    if not passed:
        raise RuntimeError(name)


inputs = read("INPUTS.json")
check("26 inputs", len(inputs) == 26)
for i, entry in enumerate(inputs):
    actual = pin(Path(entry["local"]))
    check(f"input-{i + 1}", actual["sha256"] == entry["sha256"] and actual["bytes"] == entry["bytes"])

prior_manifest = read("intake/043/MANIFEST.json")
prior_checks = []
for entry in prior_manifest["files"]:
    actual = pin(Path(entry["path"]))
    passed = actual["sha256"] == entry["sha256"] and actual["bytes"] == entry["bytes"]
    prior_checks.append(dict(path=entry["path"], passed=passed))
check("all 96 original 043 artifacts remain unchanged",
      len(prior_checks) == 96 and all(row["passed"] for row in prior_checks))
prior_report = read("intake/043/REPORT.json")
for entry in prior_report["artifacts"]:
    actual = pin(Path(entry["path"]))
    check(f"original reported pin {Path(entry['path']).name}",
          actual["sha256"] == entry["sha256"] and actual["bytes"] == entry["bytes"])
write("PRIOR-FREEZE-CHECK.json", dict(passed=True, count=len(prior_checks), checks=prior_checks))

validation = read("VALIDATION.json")
check("843 scientific checks pass",
      validation["passed"] and validation["count"] == len(validation["checks"]) == 843
      and all(row["passed"] for row in validation["checks"]))
start = read("execution/fold-01/START.json")
end = read("execution/fold-01/END.json")
for entry in start["source_pins"]:
    actual = pin(Path(entry["path"]))
    check(f"execution pin {Path(entry['path']).name}",
          actual["sha256"] == entry["sha256"] and actual["bytes"] == entry["bytes"])
check("one job admitted and released",
      end["returncode"] == 0 and end["admitted"] and end["released"] and not end["refused"])
check("no task or phase cap", start["task_time_limit"] is None and start["phase_time_limit"] is None)
check("final stdout validation count", read("execution/fold-01/stdout.txt")["validation_count"] == 843)

results = read("RESULTS.json")
check("qualified probabilities remain null",
      results["actual_frame_failure_probability"] is None
      and results["actual_lifetime_failure_probability"] is None
      and all(row["actual_frame_failure_probability"] is None for row in results["points"]))
check("no new FE claim", results["new_FE_equilibrium_solve"] is False)
csv_counts = {}
for point in results["points"]:
    reserve = point["reserve"]
    for case in point["load_cases"]:
        name = f"MEMBERS-f5-{reserve}-{case['label']}.csv"
        with (ROOT / name).open(newline="") as handle:
            rows = list(csv.DictReader(handle))
        csv_counts[name] = len(rows)
        check(f"{name} membership and classification",
              len(rows) == 750 and len({row["member"] for row in rows}) == 750
              and all(row["tag"] == "QUESTIONABLE / PROJECTION" for row in rows))
        check(f"{name} source correspondence",
              max(float(row["peak_compression_Pa"]) for row in rows) == case["max_compression_Pa"])
check("six states contain 4500 member rows", len(csv_counts) == 6 and sum(csv_counts.values()) == 4500)
nfi = read("NFI.json")
check("eight nonblocking fold dispositions",
      len(nfi["items"]) == 8 and not nfi["stops_other_work"]
      and all(row["stops_other_work"] is False for row in nfi["items"]))
for name in ["CARD.md", "METHOD.md"]:
    text = (ROOT / name).read_text()
    check(f"{name} classifications", "QUESTIONABLE / PROJECTION" in text)
    links = [s for s in re.findall(r"\]\(([^)]+)\)", text) if not s.startswith(("https://", "http://"))]
    check(f"{name} local links", all((ROOT / link).is_file() for link in links))

[withheld: private task or principal quotation; scientific result/status retained elsewhere]