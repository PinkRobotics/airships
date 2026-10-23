"""Verify frozen artifacts and package MAINLINE-043; no scientific solver or queue write."""

from collections import Counter
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


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pin(path):
    return dict(path=str(path.resolve()), sha256=digest(path), bytes=path.stat().st_size)


def check(name, passed, detail=None):
    row = dict(name=name, passed=bool(passed))
    if detail is not None:
        row["detail"] = detail
    checks.append(row)
    if not passed:
        raise RuntimeError(f"Packaging verification failed: {name}: {detail}")


inputs = read("INPUTS.json")
check("26 pinned inputs", len(inputs) == 26)
for index, row in enumerate(inputs):
    path = Path(row["local"])
    check(
        f"input {index + 1} frozen local copy",
        row["verified"] and path.is_file()
        and digest(path) == row["sha256"]
        and path.stat().st_size == row["bytes"],
        str(path),
    )

retrievals = read("web-sources/SOURCES.json")
check(
    "raw retrieval accounting",
    Counter(row["status"] for row in retrievals) == {"saved": 12, "failed": 3},
)
for row in retrievals:
    if row["status"] == "saved":
        path = ROOT / "web-sources" / row["local"]
        check(
            f"saved source {row['local']}",
            digest(path) == row["sha256"] and path.stat().st_size == row["bytes"],
        )

validation = read("VALIDATION.json")
check(
    "210 scientific checks passed",
    validation["passed"] and validation["count"] == len(validation["checks"]) == 210
    and all(row["passed"] for row in validation["checks"]),
)

result = read("RESULTS.json")
check(
    "unqualified values remain null",
    all(
        result[key] is None
        for key in [
            "qualified_frame_failure_probability",
            "qualified_compressive_characteristic_strength_Pa",
            "qualified_compressive_weibull_modulus",
            "lifetime_failure_probability",
        ]
    ),
)
check(
    "rise-8 remains independently unverified",
    result["rise8"]["independently_verified_force_solution"] is False
    and result["rise8"]["geometry_and_forces_independently_reproduced"] is False,
)
check("17 material evidence rows", len(read("SOURCE-DATA.json")["rows"]) == 17)

csv_rows = {}
for beam in result["checked_discrete_beams"]:
    name = f"MEMBERS-{beam['label']}.csv"
    with (ROOT / name).open(newline="") as handle:
        rows = list(csv.DictReader(handle))
    csv_rows[name] = len(rows)
    check(
        f"{name} count and unique member identifiers",
        len(rows) == beam["count"]
        and len({row["member"] for row in rows}) == beam["count"],
    )
    check(
        f"{name} classifications",
        all(row["stress_tag"] == "QUESTIONABLE" and row["probability_tag"] == "PROJECTION"
            for row in rows),
    )
    check(
        f"{name} output correspondence",
        max(float(row["peak_compression_fiber_Pa"]) for row in rows)
        == beam["maxima"]["peak_compression_fiber_Pa"]
        and max(float(row["max_positive_axial_tension_Pa"]) for row in rows)
        == beam["maxima"]["max_positive_axial_tension_Pa"],
    )
check("1680 member rows", sum(csv_rows.values()) == 1680)

jobs = []
source_map = {
    "reliability-01": "development/reliability-01/reliability.py",
    "reliability-02": "development/reliability-02/reliability.py",
    "reliability-final": "development/reliability-03/reliability.py",
    "reliability-verified": "reliability.py",
}
for label, source in source_map.items():
    start = read(f"execution/{label}/START.json")
    end = read(f"execution/{label}/END.json")
    check(
        f"{label} source hash and bytes",
        digest(ROOT / source) == start["source_sha256"]
        and (ROOT / source).stat().st_size == start["source_bytes"],
    )
    if "source_data_sha256" in start:
        check(
            f"{label} material-data hash",
            digest(ROOT / "SOURCE-DATA.json") == start["source_data_sha256"],
        )
    check(
        f"{label} admitted, completed and released",
        end["returncode"] == 0 and end["admitted"] is True
        and end["refused"] is False and end["released"] is True,
    )
    check(
        f"{label} clocks and no task cap",
        datetime.fromisoformat(end["ended_utc"]) >= datetime.fromisoformat(end["started_utc"])
        and end["elapsed_seconds"] > 0 and start["task_time_budget"] is None,
    )
    jobs.append({
        **end,
        "code_snapshot": pin(ROOT / source),
        "start_receipt": pin(ROOT / f"execution/{label}/START.json"),
        "end_receipt": pin(ROOT / f"execution/{label}/END.json"),
    })
check(
    "final stdout agrees with validation count",
    read("execution/reliability-verified/stdout.txt")["validation_count"] == validation["count"],
)

nfi = read("NFI.json")
check(
    "16 open nonblocking qualification questions",
    len(nfi["items"]) == 16
    and len({row["id"] for row in nfi["items"]}) == 16
    and all(row["status"] == "open" and row["stops_other_work"] is False
            for row in nfi["items"])
    and nfi["requires_immediate_reply"] is False,
)
for name in ["CARD.md", "METHOD.md", "SOURCES.md", "PROOF.md"]:
    text = (ROOT / name).read_text()
    check(f"{name} classification", "QUESTIONABLE / PROJECTION" in text)
    local_links = [
        link for link in re.findall(r"\]\(([^)]+)\)", text)
        if not link.startswith(("https://", "http://", "#"))
    ]
    check(f"{name} local links", all((ROOT / link).is_file() for link in local_links))

write("EXECUTION.json", {
    "unit": "vacuum-mainline043-sic-frame-reliability-1020",
    "execution_kind": "scientific postprocessing of frozen input data",
    "new_finite_element_or_nonlinear_solve": False,
    "task_time_limit": None,
    "phase_time_limit": None,
    "technical_watchdog": "ordinary simjob launcher default; no task or phase cap imposed",
    "cores_per_job": 1,
    "requested_memory_per_job": "1G",
    "gpu_requested": False,
    "jobs": jobs,
    "all_four_admitted_and_released": True,
    "total_job_elapsed_seconds": sum(row["elapsed_seconds"] for row in jobs),
    "outstanding_jobs": [],
    "scientific_checks_passed": validation["count"],
    "development_note": (
        "01 used an incorrect four-point RBSC reference; 02 corrected the documented three-point "
        "reference. The third run added member probabilities and bow sensitivities; the fourth "
        "refined and independently checked quadrature. Only top-level scientific results are current."
    ),
    "csv_packaging_annotation": "Constant QUESTIONABLE/PROJECTION columns added after final run; numerical values unchanged.",
})

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

now = datetime.now(ZoneInfo("America/Vancouver")).isoformat()
write("PACKAGE-CHECK.json", {
    "at": now,
    "passed": all(row["passed"] for row in checks),
    "count": len(checks),
    "scope": "Frozen input/source pins, execution provenance, output structure and qualifications; not a material qualification test.",
    "checks": checks,
})
timing = read("TIMING.json")
timing.update(
    ended_at=now,
    elapsed_seconds=(datetime.fromisoformat(now) - datetime.fromisoformat(timing["started_at"])).total_seconds(),
    ended_event="Analysis and artifact packaging complete; queue filing follows.",
    scientific_job_elapsed_seconds=sum(row["elapsed_seconds"] for row in jobs),
)
write("TIMING.json", timing)

files = [
    path for path in sorted(ROOT.rglob("*"))
    if path.is_file() and path.name != "MANIFEST.json" and "__pycache__" not in path.parts
]
write("MANIFEST.json", {
    "unit": "vacuum-mainline043-sic-frame-reliability-1020",
    "tag": "QUESTIONABLE / PROJECTION",
    "created_at": now,
    "excludes": ["MANIFEST.json (self)", "queue report and state file outside artifact root"],
    "files": [pin(path) for path in files],
})
print(json.dumps({
    "packaging_checks_passed": len(checks),
    "scientific_checks_passed": validation["count"],
    "member_rows": sum(csv_rows.values()),
    "manifest_files": len(files),
    "timing": timing,
}, indent=2))
