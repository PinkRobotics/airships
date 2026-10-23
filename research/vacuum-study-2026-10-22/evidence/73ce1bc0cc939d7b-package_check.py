"""Build the independent check narrative and verify the delivered evidence."""
from pathlib import Path
import json
import hashlib
import datetime
import csv
import math
from collections import Counter

B=Path(__file__).resolve().parent
D=json.loads((B/"DERIVED.json").read_text())
S=json.loads((B/"SUPPLEMENT.json").read_text())
A=json.loads((B/"ARITHMETIC.json").read_text())
P=json.loads((B/"PROVENANCE.json").read_text())
C=json.loads((B/"owner/COMPUTE.json").read_text())
OWNER_NFI=json.loads((B/"owner/NFI.json").read_text())
NOW=datetime.datetime.now().astimezone().isoformat(timespec="seconds")


def dump(name,x):
    (B/name).write_text(json.dumps(x,indent=2,allow_nan=False)+"\n")


items=[
 dict(id="NFI-CHECK037b-HEX679-SUPPORT",tag="CORRECTION",status="OPEN",
      finding="HexBond 679 was priced using 250 g/m2 resin while its separate 30 g/m2 support was omitted at both interfaces.",
      exact={"owner_increment_kg":444.25534518822144,"corrected_increment_kg":519.6535688743766,
             "omitted_kg":75.39822368615503,"corrected_classical_maximum_minimum_SF":0.9162604110157426},
      disposition="Correction already re-solved in this check; replace the owner's mass line when reconciling the card. It remains rejected.",
      evidence="EVIDENCE.md; DERIVED.json/hexbond_support_correction; primary HexBond 679 p.1"),
 dict(id="NFI-CHECK037b-200F-TRANSFER",tag="QUESTIONABLE",status="OPEN",
      finding="The detailed 200 F cure data use AF 163-2K at 0.060 lb/ft2 on metal, not the 2U 0.015 lb/ft2 Be/honeycomb joint. The family's six-hour guidance is not evidence that all two-to-six-hour cycles qualify the target assembly.",
      exact={"test_cycle_pressure_psi":50,"core_stabilized_typical_compression_psi":60,
             "core_stabilized_minimum_average_compression_psi":35,
             "unbypassed_cure_pressure_SF_typical":1.2,"unbypassed_cure_pressure_SF_minimum_average":.7},
      disposition="Keep the +0.12015 kg route as a process candidate; establish cure, pressure/tooling path, actual bond performance and stress-free temperature on target materials.",
      evidence="3M datasheet pp.15,19; Hexcel CR-III Table II; EVIDENCE.md"),
 dict(id="NFI-CHECK037b-FIELD-EDGE-RESIDUAL",tag="QUESTIONABLE",status="OPEN",
      finding="Zero mean mismatch shear is a homogeneous continuous-field idealization. The 16.092 mm edge length spans only 1.68948 cells; local peaks and the effect of balanced residuals on global/crimp modes are unresolved.",
      exact={"transfer_length_mm":D["residual"][0]["transfer_length_mm"],
             "transfer_length_cells":D["residual"][0]["transfer_length_mm"]/9.525,
             "028b_finite_face_residual_MPa":D["finite_face_compatibility"][1]["face_residual_MPa"]},
      disposition="Retain the calculated factors conditionally. A layer-wise/cell-resolved model and representative cured curved panel are the grounding steps; no debond survival is established by a zero mean shear argument.",
      carries_owner_rows=["NFI-037b-SCREEN-PREMISE","NFI-037b-EDGE-MODEL","NFI-037b-BALANCED-COMPRESSION","NFI-037b-SPLICE","NFI-037b-WAVINESS","NFI-037b-HARDPOINTS"]),
 dict(id="NFI-CHECK037b-FOIL-ALLOWABLE-TRANSFER",tag="QUESTIONABLE",status="OPEN",
      finding="67 GPa/2700 kg/m3 came from a 5056-H14 bulk register, while 227.53 MPa comes from 5052-H39 foil. Neither is a primary allowable for the actual cured 5056-H39 core. The 10 MPa Be scarf limit also remains projected.",
      disposition="Use the present numbers only as model inputs; measure or source the actual foil and bonded-scarf properties.",
      carries_owner_rows=["NFI-037b-FOIL","NFI-037b-SCARF","NFI-037b-028B-SCARF-LEVER"]),
 dict(id="NFI-CHECK037b-CREEP-STATEMENT",tag="QUESTIONABLE",status="OPEN",
      finding="The statement that creep is none in service overstates a finite-duration displacement result. A zero table reading at one condition is not zero creep over all service histories, and no stress-relaxation fraction follows.",
      exact={"reported_180F_creep_in":.0002,"converted_displacement_um":5.08,"duration_h":192},
      disposition="Replace the absolute statement with the measured conditions and preserve the unmeasured relaxation/cyclic-life qualification.",
      carries_owner_rows=["NFI-037b-SUSTAINED-SHEAR","NFI-037b-STRESS-FREE-T"]),
 dict(id="NFI-CHECK037b-INTERLAYER-COUNT",tag="QUESTIONABLE",status="OPEN",
      finding="The inherited rigid screen adds one interlayer compliance while the symmetric edge/global model adds both interfaces. A consistent two-interface version halves the rigid-screen thickness requirement.",
      exact=S["symmetric_interlayer_sensitivity"],
      disposition="State the topology explicitly. Neither 20.619 t nor the symmetric 10.310 t sensitivity can float; no change to the selected route."),
 dict(id="NFI-CHECK037b-DIAGNOSTIC-SCHEMA",tag="QUESTIONABLE",status="OPEN",
      finding="Some rows set feasible=true while named usage exceeds one. Failed rows also contain zero geometry, NaN and Infinity. Several rejected nonmetal solutions have core depths of only 0.016–0.076 mm, outside the supplied core data.",
      disposition="Distinguish local-constraint feasibility from a design inside the named stretch, encode nonfinite values as null plus an infeasibility reason, and keep failed-solve trial coordinates out of build dimensions. Independent broader-envelope searches confirm the rejection."),
 dict(id="NFI-CHECK037b-MASS-ALONE-WORDING",tag="QUESTIONABLE",status="OPEN",
      finding="The glass/aramid rejections involve their specified mechanical properties and the fixed scarf, not density alone. An artificial ideal-property core at the HFT density can pass the broader classical envelope.",
      exact={"HFT_density_kg_m3":32.04,"actual_HFT_classical_maximum_minimum_SF":D["fix_searches"][10]["search"]["full_envelope_max"]["full_min"],
             "ideal_properties_same_density_classical_maximum_minimum_SF":S["ideal_properties_at_HFT_density"]["full_envelope_max"]["full_min"]},
      disposition="Narrow 'mass alone' to the metallic density bounds that were actually proven. No sourced nonmetal candidate becomes feasible.",
      carries_owner_rows=["NFI-037b-NONMETAL-CTE","NFI-037b-RT-PASTE"]),
 dict(id="NFI-CHECK037b-L-PRECISION",tag="ROUNDING",status="OPEN",
      finding="The L-direction branch mixes rounded 103.42 MPa/379.21 kPa inputs with exact-PSI conversions elsewhere. This produces 14 distinct precision differences, repeated twice in the verdict.",
      disposition="Use one stated conversion convention or reduce reported digits. All fourteen values reproduce when the published rounded L inputs are used. W remains governing.",
      evidence="EXACT-DIFFERENCES.csv; SUPPLEMENT.json/rounded_L_replication")
]
for item in items:item["blocking"]=False
dump("NFI.json",dict(unit="vacuum-mainline037b-check-1020",status="OPEN",
                    items=items,retained_owner_rows=[r["id"] for r in OWNER_NFI["items"]],
                    owner_rows_frozen_in="owner/NFI.json",next="none"))

checks=A+S["checks"]
mismatches=[r for r in checks if not r["match"]]
all_differences=mismatches+[dict(
    path="fixes/2/HexBond679_total_mass_increment_kg",owner=C["fixes"][2]["mass_change_kg"],
    independent=D["hexbond_support_correction"]["corrected_increment_kg"],
    independent_minus_owner=D["hexbond_support_correction"]["missing_mass_kg"],
    kind="omitted supported-film mass")]
dump("FINDINGS.json",dict(numerical_path_differences=mismatches,
                        source_mass_correction=all_differences[-1],
                        interpretation="16 numerical path differences = 14 distinct L-rounding values plus 2 verdict repeats; one separate material-mass omission",
                        nfi_rows=[x["id"] for x in items]))

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

lines=[
"CHECK-037b independently reproduces the owner's principal numbers. One product-mass omission and the limits of the proposed cure change require correction or carry-forward. All findings are nonblocking. ESTIMATE / QUESTIONABLE; no installed-hull qualification is claimed.",
"",
f"Order `{summary['order']}`; owner report `{summary['owner_report']}`. The 27 supplied non-code pins match. Five executable artifacts were excluded without reading or running them. This package contains the checker's own arithmetic and source evidence.",
"",
"| Requested check | Independent result | Assessment |",
"|---|---:|---|",
f"| Rigid-screen core force / first wall-yield force | {D['screen_equilibrium']['cure_250F']['ratio']:.12f} | Reproduces 47×; 702.760 versus 14.921 kN/m |",
f"| Wall stress, uniform / doubled single wall | {D['residual'][0]['wall_stress_MPa']:.9f} / {D['residual'][0]['wall_stress_doubled_single_MPa']:.9f} MPa | Reproduces 102–122 MPa |",
f"| Free-edge W factors, typical / minimum average | {D['residual'][0]['SF_edge_typ']:.10f} / {D['residual'][0]['SF_edge_min']:.10f} | Reproduces 1.17 / 0.83 |",
f"| Added face compression at 028b lead | {S['verdict']['face_compression_at_028b_lead_MPa']:.10f} MPa | Reproduces 4.4 MPa; 037's different geometry gives 4.16244 MPa |",
f"| Fixed 30:1 scarf, usage / gamma required | {D['fix_searches'][0]['search']['best']['u_raw']:.10f} / {D['fix_searches'][0]['search']['best']['gamma_need']:.10f} | Reproduces 1.052 / 0.618 |",
f"| 037 scarf stress-free ceiling | {D['037_scarf_ceiling_C']:.10f} °C | Reproduces 54 °C |",
f"| 200 °F cycle, minimum-average W factor | {D['residual'][2]['SF_edge_min']:.10f} | Conditional model value |",
f"| 200 °F scarf ratio / old-geometry joining increment | {D['constants']['scarf_ratios'][1]:.10f}:1 / {D['fix_searches'][6]['mass_change_at_original_lead_kg']:.10f} kg | Reproduces 30.34:1 / +0.12 kg |",
f"| Reoptimized low-cure usage / gamma / Q | {D['fix_searches'][6]['search']['best']['u_raw']:.10f} / {D['fix_searches'][6]['search']['best']['gamma_need']:.10f} / {D['fix_searches'][6]['search']['best']['Q_need']:.10f} | Inside the named stretch |",
"",
"The correction is in the rejected HexBond 679 alternative. Its 250 g/m² resin comes with a separate 30 g/m² support. Counting both interfaces changes its mass increment from **444.2553451882 to 519.6535688744 kg**, a **75.3982236862 kg** increase. Re-solving gives maximum minimum factor 0.9162604110 even with the broader classical gamma/wrinkle envelope; rejection stands. [Primary product sheet](https://www.hexcel.com/wp-content/uploads/2025/12/HexBond679TDSv12.pdf).",
"",
"The +0.12015 kg AF cure/scarf route remains a candidate. The 200 °F family cure guidance and the actual 2K metal-joint tests do not qualify the light 2U Be/honeycomb construction. The 50 psi test cure also needs an established tooling/load path for the low-density core. EVIDENCE.md and the cure-transfer NFI preserve that distinction. [3M datasheet](https://multimedia.3m.com/mws/media/282041O/3m-scotch-weld-structural-adhesive-film-af-163-2-af-163-3.pdf).",
"",
"All 17 alternatives were checked with an independent face-thickness search and analytic piecewise mass balance. The values below are the owner's conditional model, with full precision in DERIVED.json. An infeasible trial point is not a build geometry.",
"",
"| Case | Usage at least local-feasible point | Best minimum factor with gamma=1, Q=.82 |",
"|---|---:|---:|",
]
for r in D["fix_searches"]:
    sr=r["search"];best=sr.get("best")
    usage=f"{best['u_raw']:.9g}" if best else "no local-feasible point"
    mx=sr.get("full_envelope_max",{}).get("full_min")
    envelope=f"{mx:.9f}" if mx is not None else "interface mass exceeds budget"
    lines.append(f"| {r['index']}: {r['name'].replace('|','/')} | {usage} | {envelope} |")
lines+= [
"",
"The broader-envelope factors in that table are mathematical rejection checks, not evidence that gamma=1 is attainable. The nominal 250 °F case still exceeds its named stretch even though its broader-envelope factor exceeds one.",
"",
f"Verification covers **{summary['checks']:,} arithmetic, source-transfer and presentation comparisons**: {summary['matches']:,} match the stated tolerances. The {summary['numerical_path_differences']} numerical path differences comprise fourteen distinct L-direction rounding differences and their two verdict repetitions. Exact entries are in EXACT-DIFFERENCES.csv and FINDINGS.json. At 250 °F, L typical is 1.234372058379 from exact printed-unit conversion versus 1.234374796304 filed; L minimum is 1.009940775037 versus 1.009947412566. All reproduce with the owner's rounded L inputs. W still governs.",
"",
f"All **{summary['numeric_compute_leaves']} numeric compute fields** are accounted for, including metadata and failed-solve sentinels. Source-register transfers are not mislabeled as physical verification. The completed searches, mass residuals and periodic-cell equilibrium are recorded separately.",
"",
"Nine check NFIs preserve the HexBond correction, low-cure product/process transfer, field/edge/residual idealizations, foil/scarf property transfer, the absolute creep statement, the one-versus-two interlayer convention, failed-solve output semantics, the overly broad 'mass alone' wording and L precision. The owner's thirteen NFIs remain retained in owner/NFI.json. None is treated as a stop-work condition.",
"",
"METHOD.md gives the derivations and search domain. EVIDENCE.md identifies primary documents and transfer limits. ARITHMETIC.json, DERIVED.json and SUPPLEMENT.json contain the independent record; PROVENANCE.json and MANIFEST.json pin the package. No other seat was restored, awakened or contacted. The completion is a single queue report to sciences, cc co, xo and the robotics seat. No successor was assigned.",
]
(B/"CARD.md").write_text("\n".join(lines)+"\n")

validation=[]
def require(name,ok,detail=None):
    validation.append(dict(check=name,pass_=bool(ok),detail=detail))

require("all supplied non-code pins initially matched",all(r["match"] for r in P["checks"]))
frozen=0
for r in P["checks"]:
    if "frozen_path" in r:
        data=(B/r["frozen_path"]).read_bytes();frozen+=1
        require("frozen pin "+r["frozen_path"],len(data)==r["bytes"] and hashlib.sha256(data).hexdigest()==r["sha256"])
require("five executable paths explicitly excluded",len(P["excluded_executables"])==5)
require("no excluded executable was copied",all(not any(f.name==Path(r["path"]).name
          for f in (B/"owner").iterdir()) for r in P["excluded_executables"]))
require("all numerical compute leaves accounted for",not S["unaccounted"])
require("16 expected L-precision paths only",len(mismatches)==16 and
        all("SF_edge_L_" in r["path"] or "bond_free_core_edge/L_" in r["path"] for r in mismatches))
require("14 rounded-L replication checks pass",all(r["match"] for r in S["checks"] if r["path"].startswith("rounded_L/")))
require("all other independent comparisons pass",all(r["match"] for r in checks
        if r["path"] not in {x["path"] for x in mismatches}))
require("baseline mass balance closes",abs(D["baseline"]["mass_residual_kg"])<1e-7)
for r in D["fix_searches"]:
    for key in ["search","without_residual"]:
        if r[key].get("best"):
            p=r[key]["best"]
            require(f"case {r['index']} {key} mass",abs(p["mass_residual_kg"])<1e-7)
            require(f"case {r['index']} {key} local constraints",p["others_min"]>=1-2e-9)
require("all rejected alternatives fail broader classical envelope",
        all(D["fix_searches"][i]["search"]["full_envelope_max"]["full_min"]<1
            for i in [2,8,10,11,12,13,14,15,16]))
require("5.5 mm interlayer mass rejects without geometry",
        not D["fix_searches"][9]["search"]["feasible"])
require("corrected HexBond still rejected",D["hexbond_support_correction"]["corrected_search"]["full_envelope_max"]["full_min"]<1)
require("periodic cell forces equilibrate",max(abs(x) for x in S["periodic_cell_equilibrium"]["force_balance"])<1e-12)
require("all nine NFIs nonblocking",len(items)==9 and all(not x["blocking"] for x in items))
require("all thirteen owner NFIs retained",len(OWNER_NFI["items"])==13)
rows=list(csv.DictReader((B/"EXACT-DIFFERENCES.csv").open()))
require("17 exact difference rows: 16 precision plus mass",len(rows)==17)
require("source evidence files have measured download hashes",
        all(not r.get("path") or (len((Path.cwd()/r["path"]).read_bytes())==r["bytes"] and
            hashlib.sha256((Path.cwd()/r["path"]).read_bytes()).hexdigest()==r["sha256"])
            for r in json.loads((B/"sources/RETRIEVALS.json").read_text())))

dump("VALIDATION.json",dict(status="PASS" if all(r["pass_"] for r in validation) else "FAIL",
                           checks=len(validation),passed=sum(r["pass_"] for r in validation),
                           frozen_files_reverified=frozen,results=validation))
if not all(r["pass_"] for r in validation):
    print(json.dumps([r for r in validation if not r["pass_"]],indent=2))
    raise SystemExit(1)
manifest=[]
for f in sorted(B.rglob("*")):
    if f.is_file() and f.name!="MANIFEST.json" and "__pycache__" not in f.parts:
        data=f.read_bytes()
        manifest.append(dict(path=str(f.relative_to(B)),sha256=hashlib.sha256(data).hexdigest(),bytes=len(data)))
dump("MANIFEST.json",dict(schema=1,unit=summary["unit"],files=manifest,
                          file_count=len(manifest),total_bytes=sum(x["bytes"] for x in manifest),
                          excluded=["MANIFEST.json (self)","__pycache__/ (local interpreter cache)"]))
print(json.dumps(dict(status="PASS",validation_checks=len(validation),package_files=len(manifest),
                      package_bytes=sum(r["bytes"] for r in manifest),summary=summary),indent=2))
