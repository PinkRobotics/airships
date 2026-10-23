#!/usr/bin/env python3
"""Seal the completed 030c package and atomically file exactly one report."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import os
import subprocess
from intake import B, load, save, pin

W = B.parents[3]
assert W.name == "ref-ed3515d83349998d6b1b"
OUT = W / ".ship/outbox"
RID = "rpt-1228-mainline030c-design-register-1020"
target = OUT / (RID + ".json")
assert not target.exists(), "One report only; never overwrite an existing filing."
assert (B / "SNAPSHOT-FROZEN.json").exists()
for script in ("build_register.py", "write_docs.py", "validate_packet.py"):
    subprocess.run(["python3", str(B / script)], check=True,
                   env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
v = load(B / "VALIDATION.json")
assert v["all_pass"]
r = load(B / "RESULTS.json")
end = datetime.now(timezone.utc)
start = datetime.fromisoformat(load(B / "START.json")["started_at"])
ending = {"ended_at": end.isoformat(), "elapsed_seconds": (end - start).total_seconds(),
          "timing": "measurement only; no time budget or phase cap",
          "own_simulation_jobs_launched": 0, "own_live_jobs": 0,
          "out_of_band_contact": False, "other_seat_restore_or_wake": False,
          "next_job": "none; stop and file"}
save(B / "END.json", ending)
r["measurement_end"] = ending
save(B / "RESULTS.json", r)
save(B / "ARTIFACT-GUIDE.json", {
    "current_morning_read": "CARD.md",
    "complete_issue_register": ["REGISTER.md", "REGISTER.json", "NFI.json"],
    "all_030b_source_records": "baseline030b/",
    "new_source_records": "snapshots/",
    "original_source_fields": "Preserved verbatim; historical conclusions do not override current 030c annotations.",
    "source_snapshot": "SNAPSHOT-FROZEN.json",
    "validation": "VALIDATION.json",
    "qualified_installed_hull_SF": None,
    "qualified_frame_failure_probability": None,
    "qualified_hull_life_days": None,
})
excluded = {"MANIFEST.json", "REPORT.json", "FILING-RECEIPT.json"}
artifacts = [pin(p) for p in sorted(B.rglob("*"))
             if p.is_file() and "__pycache__" not in p.parts
             and not (p.parent == B and p.name in excluded)]
manifest = {"schema": 1, "unit": r["unit"], "sealed_at": end.isoformat(),
            "snapshot_at": r["snapshot_at"],
            "excludes_root_files": sorted(excluded),
            "excludes_directories": ["__pycache__"],
            "artifacts": artifacts, "files": len(artifacts),
            "bytes": sum(x["bytes"] for x in artifacts)}
save(B / "MANIFEST.json", manifest)
body = """QUESTIONABLE / PROJECTION. MAINLINE-030c incorporates 16 reports through 04:03:32 PDT, preserving all 94 prior rows and 711 findings: 98 rows, 961 attributed findings total.

P2 uses 040's whole bill with 028b/037b construction. R10 does not float (ISA endpoint −109.649 kg); first ISA floats occur at R12–15. R30 requires least optimism: usage .601233/.789568 for ISA/optimistic weather, conditional SF 1. Both-weather closes nowhere. Coating+primer (assumed 0.20 kg/m²) and retained water are the largest assumed debits.

CHECK-037b reproduces the principal fix numbers; rejected HexBond 679 gains 75.398 kg of omitted support. Cure/process qualification remains open.

041's direct f5 witnesses replace the transferred 1.067 shortcut: SF 1.143285/1.083205 at 5%/019 reserves; local sensitivities 1.033223/.978132. 043 leaves frame failure probability null.

029 establishes no collapse gamma; weak endpoints 78.627/90.722 kPa remain below 95.461 kPa. CHECK-037's ten mass corrections and 84 missing thermal fields are retained.

039's former O5 becomes O6. CHECK-039 reaches .699692 at fixed lift and SF 1 with +1127.071 kg. 042 build gaps and 044 unqualified life remain explicit.

Optimism/corrections ledgers and ground-first routes are preserved. First tests: compression/specification, weighed curved scarf (F1 extension), same-batch wrinkle.

[withheld: private task or principal quotation; scientific result/status retained elsewhere]