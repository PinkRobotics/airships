#!/usr/bin/env python3
"""Seal the validated register, rescan canonical filings, and submit once."""
import hashlib
import json
import subprocess
from datetime import datetime,timezone
from pathlib import Path
from zoneinfo import ZoneInfo
from intake import B,Q,load,save,pin

ROOT=B.parents[3]
RID="rpt-ref-e999413f5ed23130ebf6"
SEAT="ref-3f7ec48b84b54a049007"
outbox=ROOT/".ship/outbox"
tmp=outbox/(RID+".json.tmp")
final=outbox/(RID+".json")
assert not final.exists() and not tmp.exists(),"Report must be filed once"
assert load(B/"VALIDATION.json")["passed"]
index=load(B/"SOURCE-INDEX.json")
known={"rpt-1228-mainline030c-design-register-1020",RID}
for group in ("baseline","additions","additions_030c","additions_030d"):
    known.update(x["id"] for x in index[group])
cutoff=datetime.fromisoformat("2026-10-20T04:03:32-07:00")

def scan():
    new=[]
    paths=set(Q.glob("rpt-*mainline*.json"))|set(Q.glob("rpt-*check0*-1020.json"))
    for p in paths:
        r=load(p)
        if r.get("kind")!="report" or r["id"] in known:continue
        at=datetime.fromisoformat(r.get("ingested",r["at"]).replace("Z","+00:00"))
        if at<cutoff:continue
        if "mainline" not in ((r.get("unit") or "")+(r.get("body") or "")).lower():continue
        new.append(r["id"])
    for r in load(B/"INTAKE.json")["reports"]:
        a=pin(Path(r["report_path"]))
        assert a["sha256"]==r["report_sha256"] and a["bytes"]==r["report_bytes"],r["id"]
    return sorted(new)

unfolded=scan()
assert not unfolded,{"new_reports_require_fold":unfolded}
coverage=load(B/"REGISTER-COVERAGE.json")
validation=load(B/"VALIDATION.json")
save(B/"SNAPSHOT-FROZEN.json",dict(
    at=datetime.now(timezone.utc).isoformat(),intake_sampled_at=load(B/"INTAKE.json")["sampled_at"],
    since=cutoff.isoformat(),new_canonical_reports=coverage["new_canonical_reports"],
    known_report_ids=sorted(known-{RID}),unfolded_reports=[],
    rule="Every discovered mainline/check canonical report is incorporated. Partial filings stay pending; later filings require a new register/addendum."))
save(B/"END.json",dict(
    unit="vacuum-mainline030d-design-register-1020",work_complete=True,
    at=datetime.now(timezone.utc).isoformat(),coverage=coverage,
    source_validation_passed=True,validation_checks=validation["checks"],
    own_live_jobs=[],out_of_band_contact=False,next="none",
    qualification="All scientific conclusions remain QUESTIONABLE / PROJECTION; installed SF, life and Pf unknown."))
for p in B.glob("*.json"):
    if p.name=="MANIFEST.json":continue
    json.loads(p.read_text(),parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
required=[
 "CARD.md","REGISTER.md","REGISTER.json","RESULTS.json","NFI.json",
 "LEDGER.md","LEDGER.json","OPTIMISM-LEDGER.md","OPTIMISM-LEDGER.json",
 "GROUND-FIRST.md","GROUND-FIRST.json","P2-048-ACCOUNT.json",
 "P3-RELIABILITY.json","P3-052-ACCOUNT.json","P2-WEATHER-050.json","DAMAGE-AND-LIFE.json","BERYLLIUM-SUPPLY.json",
 "PARTIAL-FILINGS.json","PENDING.json","CHANGES.json","CHECK-VERDICTS.json",
 "REPORTS.md","SOURCE-INDEX.json","INPUTS.json","METHOD.md","VALIDATION.json",
 "BASELINE-PINS.json","BRIEF-PINS.json","INTAKE.json","NEW-NFI.json",
 "NEW-NFI-SOURCES.json","AUTHORED-NFI.json","ROUTING.json","REGISTER-COVERAGE.json",
 "SOURCE-DRIFT.json","SUPPLEMENTAL-ORDERS.json","SNAPSHOT-FROZEN.json","END.json",
 "intake.py","normalize.py","build_register.py","write_docs.py","validate_packet.py","seal_and_file.py"]
assert all((B/name).stat().st_size>0 for name in required)
paths=[p for p in sorted(B.rglob("*")) if p.is_file() and p!=B/"MANIFEST.json"
       and not p.name.endswith(".tmp") and "__pycache__" not in p.parts]
save(B/"MANIFEST.json",dict(
    unit="vacuum-mainline030d-design-register-1020",
    at=datetime.now(timezone.utc).isoformat(),artifact_count=len(paths),
    artifacts=[pin(p) for p in paths]))
# A late arrival reopens only this unpublished packet, never a filed report.
unfolded=scan()
if unfolded:
    (B/"SNAPSHOT-FROZEN.json").unlink()
    raise SystemExit("New reports require incorporation: "+", ".join(unfolded))
body=f"""QUESTIONABLE / PROJECTION. MAINLINE-030d preserves all 98 prior rows and 961 findings, both ledgers and the ground-first list. It folds {coverage['new_canonical_reports']} new reports: 104 rows and {coverage['total_attributed_findings']} attributed findings.

048's bill separates finish, primer, exterior water and material water. Cure-included R10 ISA bake endpoint is +118.695 kg; least G+Q+film usage 0.842794. All 432 new 1 mm cases fail to float. Classical CCAg's cited source is alpha 0.08/normal epsilon 0.72 on Kapton; modeled 0.09/0.65 remains unqualified.

CHECK-043 corrects the proof claim: member Euler ratio 0.375 does not demonstrate buckling. Pf1e-6 requires 8.53751/8.39866 GPa under the member-scale hypothesis. Rise8 is 5446.291 kg total, 5039.558 kg tubes.

CHECK-044 identifies AF163-2K .060 and requires 3.414034 kg old-plate credit for +36.661200 kg; without it, +40.075234 kg.

CHECK-045 corrects the 55 mm growth threshold, Perry factor and frame/trajectory claims; improved wall/tear witnesses remain below SF1.

044/045/046 mass and SF effects are recorded against both leads with geometry limits. R30 endpoint's 102.231 t Be is 23.610% of 020's historical 433 t output.

052 conditionally closes ground-serviced P3 at R10 ISA/R12 optimistic; R10 requires 5.343 GPa effective ply strength. No tested onboard-dry package closes. Its P2 comparison now includes cure.

050 finds no sampled R10–30 closure on the declared 10% hot profile and distinguishes fixed hulls from weather-specific designs. Partial CHECK-048 and 051 remain pending.

[withheld: private task or principal quotation; scientific result/status retained elsewhere]