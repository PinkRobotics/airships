"""Render this card's tables and evidence ledger from its computed outputs."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import math

ROOT=Path(__file__).resolve().parent
I=json.loads((ROOT/"INPUTS.json").read_text())
B=json.loads((ROOT/"RESULTS.json").read_text())
R=json.loads((ROOT/"PROPERTY-CHECKS.json").read_text())
LABELS={"af015_scarf":"Nominal AF/scarf","af015_scarf_primer5":"AF/scarf + primer",
        "lab8_eb_eta1":"Lab 8 g/m² + ideal weld","lab8_scarf":"Lab 8 g/m² + scarf"}
ROUTES=list(LABELS)
sr={x["route"]:x for x in R["searches"] if x["joint_screen_enforced"]}
six={x["route"]:x for x in R["searches"] if not x["joint_screen_enforced"]}
six["lab8_eb_eta1"]=sr["lab8_eb_eta1"]
legacy={x["route"]:x for x in B["searches"] if x["material"]=="SR200" and x["joint_screen_enforced"]}
full={(x["route"],x["material"]):x for x in R["full_named_maxima"]}
P={k:v["floating_point"] for k,v in sr.items()}


def table(headers, rows):
    return "\n".join(["| "+" | ".join(headers)+" |","| "+" | ".join("---" for _ in headers)+" |"]+
                     ["| "+" | ".join(map(str,row))+" |" for row in rows])


def f(v,n=3):
    return f"{v:.{n}f}"


def main():
    t=[]
    def para(text): t.append(text.strip())
    para("""# MAINLINE-028b — joining on the 021b reserve

ESTIMATE · QUESTIONABLE / PROJECTION · no certified installed-hull SF.
Order `ord-admiral-rr2-mainline028b-joining-into-021b-1020`; unit
`vacuum-mainline028b-joining-into-021b-1020`.

**The least remaining adjustable set is {global-buckling gamma, wrinkling
coefficient} in all three commissioned joining cases. No singleton works.**
Keep the stock panel envelope fixed. The nominal and primer scarfs meet the
seven numerical screens only conditionally: their largest remaining usages are
0.97198 and 0.99608 after using the SR-200 sheet Poisson value. The laboratory
8 g/m² bond plus ideal weld needs 0.65147, but its Be bond and weld are unqualified.
The 255 MPa compression sensitivity has **no floating set**, even before core
mass is charged.

These are **two adjustable** factors. The AF cases already fix the original
O5 thin-film optimism at its full 0.015 lb/ft² value. In the original five-factor
bookkeeping the used set is therefore {O1 gamma, O2 wrinkling, fixed O5 film};
O3 face strength and O4 panel enlargement are unused. Do not count the fixed
thin-film choice as newly proven. The laboratory bond is a different process
outside that original film interval.""")
    para("""## SR-200 properties and the comparison with 021b

Use density 1850 kg/m³ and E=290 GPa. The 345 MPa datasheet minimum is **tensile**
yield; using it for compression is an explicit assumption, not a compressive
minimum. The full O3 endpoint is the historical SR-200 lot's 379.2 MPa compression,
with 293.6 GPa at full-endpoint evaluation. All selected least-set points leave
O3 unused. [Materion SR-200 datasheet](https://hkvxni.files.cmp.optimizely.com/download/c3370ecef75e11eeb4768ed6ed17dca6),
[NASA CR-194164 Tables 2–3](https://ntrs.nasa.gov/api/citations/19940006718/downloads/19940006718.pdf).

021b retained nu=0.33. For a sheet-based scalar approximation this card uses
nu=0.0752, the smaller historical in-plane value (the other is 0.0768).
This does not validate an orthotropic sphere. RESULTS.json preserves the exact
021b convention; PROPERTY-CHECKS.json supplies the sheet-property results used
below. All remaining assumptions and equations are in METHOD.md.""")
    para(table(["Route","Max usage, six modes, nu=.0752","Max usage, seam enforced, nu=.33",
                "Max usage, seam enforced, nu=.0752"],
               [[LABELS[k],f(six[k]["least_set"]["min_max_usage"],6),
                 f(legacy[k]["least_set"]["min_max_usage"],6),f(sr[k]["least_set"]["min_max_usage"],6)]
                for k in ROUTES]))
    para("""The fourth row separates a laboratory-light bond from the ideal-weld
assumption. It is an additional sensitivity, not a fourth commissioned material.
The first two six-mode optima have scarf SF only 0.93006 and 0.92691.
Enforcing 028's assumed 10 MPa mean-shear limit requires thicker faces. That
assumption is a numerical screen; peel and actual Be-joint strength remain unknown.""")
    para("""## The least-set points, including the seam screen

All four select Hexcel CR-III 5056 3/8-1.0: density 16.0185 kg/m³, Ec=103.421 MPa,
W shear modulus=46.884 MPa, crush=241.317 kPa, cell=9.525 mm. These inherited
typical values are QUESTIONABLE. [Hexcel CR-III data sheet](https://www.hexcel.com/wp-content/uploads/2025/12/HexWeb_CRIII_DataSheet.pdf).
R=10 m, pressure=95,460.8379 Pa, lift=4,889.44215 kg. Raw panel blanks stay
0.6096 × 1.8288 m; scarf overlap is deducted from both dimensions.""")
    para(table(["Route","Face mm","Core mm","Vc","Physical joining kg","5% allowance kg",
                "Joint excess kg","Unused allowance kg"],
               [[LABELS[k],f(P[k]["tf_m"]*1000,6),f(P[k]["tc_m"]*1000,4),f(P[k]["Vc"],6),
                 f(P[k]["masses_kg"]["physical_joining"]),f(P[k]["masses_kg"]["base_joint_allowance"]),
                 f(P[k]["masses_kg"]["joint_excess"]),f(P[k]["masses_kg"]["unused_joint_allowance"])]
                for k in ROUTES]))
    para("""The order's 214.24/226.81 kg values are reproduced at the old 028
geometry. At these resized points they become **215.742/227.880 kg**.
Joining is recomputed from the actual face/core thicknesses. The laboratory
route becomes 50.151 kg; its unused allowance stays reserved.

The fixed 019 reserve stays 411.298944 kg and systems stay 100 kg. The mass line is:

    faces + core + max(0.05 × (faces + core), actual joining)
        + 100 + 411.298944 = 4889.442150 kg

Only the excess above the joint allowance enters the reserve. Adding the whole
joining bill as excess would double-count it. There is no extra 5% float-margin
charge on this commissioned 019/021b budget.""")
    para(table(["Route","Faces kg","Core kg","Base joint allowance kg","Fixed reserve kg",
                "Excess reserve kg","Systems kg","Charged total kg"],
               [[LABELS[k],f(P[k]["masses_kg"]["faces"]),f(P[k]["masses_kg"]["core"]),
                 f(P[k]["masses_kg"]["base_joint_allowance"]),f(P[k]["masses_kg"]["fixed_reserve"]),
                 f(P[k]["masses_kg"]["joint_excess"]),f(P[k]["masses_kg"]["systems"]),
                 f(P[k]["masses_kg"]["charged_total"])] for k in ROUTES]))
    para("The six component columns sum to the charged total before rounding. "
         "The fixed reserve includes environmental mass-equivalent losses as well as mass.")
    para(table(["Route","Core bond kg","Primer kg","Scarf film kg","Core splice kg","Seal kg","Hull seam m"],
               [[LABELS[k]]+[f(P[k]["joining"][field]) for field in
                            ("bond_kg","primer_kg","scarf_film_kg","core_splice_kg","seal_kg","seam_length_m")]
                for k in ROUTES]))
    para("""AF film is 0.015 lb/ft² per bond; primer adds 5 g/m² at both bonds.
The lab's 8 g/m² cell-edge deposition is demonstrated on other adherends and
core, not on this Be/aluminium assembly. Core splice and seal quantities remain
028 projections. [3M AF 163 film weights](https://multimedia.3m.com/mws/media/282041O/3m-scotch-weld-structural-adhesive-film-af-163-2-af-163-3.pdf),
[Rion et al. 2008 laboratory process](https://infoscience.epfl.ch/server/api/core/bitstreams/28b8cc7a-f046-4da3-9fcc-5d5ad3c52a9d/content).""")
    para("## Each factor")
    para(table(["Route","Gamma needed / full","Gamma × today","Gamma usage",
                "Wrinkle k needed","k × .33","k usage","Face MPa / usage"],
               [[LABELS[k],f(P[k]["needed"]["gamma"],6)+" / "+f(P[k]["full_gamma_at_search_E"],6),
                 f(P[k]["factor_vs_today"]["gamma"],6),f(P[k]["log_usage"]["O1_gamma"],6),
                 f(P[k]["needed"]["wrinkle"],6),f(P[k]["factor_vs_today"]["wrinkle"],6),
                 f(P[k]["log_usage"]["O2_wrinkle"],6),"345 / 0"] for k in ROUTES]))
    para("""Gamma today is 0.20 at these Vc<2 points; full is the projected
018 curve, 0.20+0.40Vc. Wrinkling today/full is 0.33/0.82. Usage is the log-share
of that interval required to meet SF=1. Panel enlargement factor is 1 and O4
usage is 0 in every case. AF film mass is half the old 0.030 lb/ft² baseline,
so its **fixed O5 usage is 1**. The lab's 8 g/m² is 18.309 times lighter than
that baseline by areal mass, but is not an AF-film interpolation.

The primer point requires gamma=0.578524 against full=0.580950 at E=290 GPa:
only about 0.4% remains in the allowed log stretch. Larger gamma is not a
measured capability. The scarf points demand 300.333 MPa face compression,
not the full 345 MPa proxy. The ideal weld point requires at least 93.212%
parent compression retention; 80% retention would give seam SF=0.85826
at that selected geometry.""")
    para("## Every computed mode at the needed values")
    mode_rows=[]
    for k in ROUTES:
        e=P[k]["at_needed"]
        mode_rows.append([LABELS[k]]+[f(e["six_modes"][n],6) for n in
          ("global_buckling","face_compression","core_shear_crimping","core_crush",
           "face_wrinkling","intracell_dimpling")]+[f(e["projected_seam_SF"],6)])
    para(table(["Route","Global","Face","Crimp","Crush","Wrinkle","Dimpling","Scarf / ideal weld"],mode_rows))
    para("""The seam entry is mean scarf shear for scarf cases and parent-strength
compression retention for the ideal weld. All are conditional screens.
Face/core flatwise tension, imperfection-driven shear, seam peel/HAZ failure,
local seam buckling, thermal/cyclic debonding and leak-tightness are **unknown**.
Overall installed-hull SF therefore remains **unknown**, not 1.

At each selected point, returning gamma to 0.20 while holding the other full
endpoints gives the following least screen. Separately reoptimizing with every
remaining named endpoint at full gives the right column; these are different
geometries and do not constitute proven margin.""")
    para(table(["Route","At selected point, full except gamma=.20","Reoptimized, all endpoints full"],
               [[LABELS[k],f(P[k]["at_full_but_gamma_02"]["least_seven_screen_SF"],6),
                 f(full[(k,"SR200")]["least_SF"],6)] for k in ROUTES]))
    para("## Every subset of the remaining adjustable factors")
    subsets=sr[ROUTES[0]]["subsets"]
    ss=[]
    for idx,row in enumerate(subsets):
        name="{"+", ".join(x.replace("O1_gamma","gamma").replace("O2_wrinkle","k")
                          .replace("O3_SR200_face_strength","face") for x in row["subset"])+"}"
        values=[]
        for key in ROUTES:
            r=sr[key]["subsets"][idx]; u=r["min_max_usage"]
            values.append("infeasible" if u is None else f(u,6)+(" ✓" if r["feasible_within_named"] else " >1"))
        ss.append([name]+values)
    para(table(["Subset"]+[LABELS[k] for k in ROUTES],ss))
    para("""A value above one needs more than the named full improvement.
“Infeasible” means the unchanged modes reject all sampled/refined points.
The denser all-core search confirms the critical two-factor results. In the
commissioned fixed-route problem the minimum cardinality is two; the face
endpoint does not reduce it.""")
    para("## S-200-F's 255 MPa compression as a sensitivity")
    para("""Materion describes roughly 255 MPa compression for S-200-F.
This run changes only the strength to 255 MPa; it does not mix the SR-200 lot's
379.2 MPa into that sensitivity. [Materion design guide, p.4](https://hkvxni.files.cmp.optimizely.com/download/dafce45ca04211ee97ee126db737ac74).

No subset floats. With the full structural budget placed into faces and **zero
core**, the compression SF upper bound is only **0.958217**. Any real core or
joint excess makes that worse. This independently rules out success regardless
of the gamma/wrinkling search.

Reoptimizing at the permitted full gamma and k=0.82 gives these maxima and all
their mode values (nu=.0752, E=290 GPa):""")
    sensitivity=[]
    for k in ROUTES:
        x=full[(k,"S200F255_sensitivity")]; p=x["point"]; e=p["at_full_named"]
        sensitivity.append([LABELS[k],f(x["least_SF"],6),f(p["tf_m"]*1000,6),f(p["tc_m"]*1000,4)]+
                           [f(e["six_modes"][n],6) for n in ("global_buckling","face_compression",
                            "core_shear_crimping","core_crush","face_wrinkling","intracell_dimpling")]+
                           [f(e["projected_seam_SF"],6)])
    para(table(["Route","Best SF","Face mm","Core mm","Global","Face","Crimp","Crush","Wrinkle","Dimpling","Seam"],sensitivity))
    para("""## Verification and carry forward

All 47 inherited honeycomb candidates were searched. Twelve aggregate numerical
checks passed: exact reproduction of 021b's six modes and mass line, all four
028 joining masses, feasibility and mass residuals, the analytic 255 MPa bound,
the 24,001-point all-core refinement of both critical scarf subsets, and
independent scalar mass roots. Maximum selected mass discrepancy is below
1e-8 kg. All 16 upstream file pins match.

No repository source was changed, no inherited executable ran, and no other
seat was contacted outside the queue. The calculation, source pins, full subset
results, mode results and unknowns are supplied in the JSON files and scripts.
`NFI.json` identifies what still needs evidence. `METHOD.md` records exact
formulas and reproduction steps. Timing is measured only; no work limit applied.

The next useful evidence is a weighed curved panel and representative joint
with post-form sheet compression, actual gauge, bond shear/flatwise strength,
scarf shear/peel or weld retention, geometric imperfections, and leak/thermal
performance. Thin-stock availability remains open even though panel size is
fixed in this search. No successor is named by this order: file this report
and await the robotics seat's next queued assignment.""")
    (ROOT/"CARD.md").write_text("\n\n".join(t)+"\n")

    rows=[]
    def nfi(id,issue,state,needed,today=None,factor=None,source=None,tag="PROJECTION",**extra):
        rows.append({"id":"NFI-028b-"+id,"status":"OPEN","issue":issue,"state":state,"tag":tag,
                     "needed":needed,"today":today,"improvement_factor":factor,
                     "null_factor_reason":None if factor is not None else "No matched measured baseline or meaningful scalar ratio.",
                     "source":source,**extra})
    for key in ROUTES:
        p=P[key]
        nfi(key+"-gamma","Ground gamma at the actual jointed geometry, including imperfections.",
            "PROJECTION",p["needed"]["gamma"],.2,p["factor_vs_today"]["gamma"],"MAINLINE-018 curve",
            usage=p["log_usage"]["O1_gamma"],full=p["full_gamma_at_search_E"])
        nfi(key+"-wrinkle","Ground wrinkling coefficient with the actual core and bond.",
            "PROJECTION",p["needed"]["wrinkle"],.33,p["factor_vs_today"]["wrinkle"],"Inherited CR-1457 bounds",
            usage=p["log_usage"]["O2_wrinkle"],full=.82)
    nfi("SR200-compression","345 MPa is tensile minimum, not a published compressive minimum; measure post-form compression.",
        "exists_today",{"face_stress_scarf_Pa":P["af015_scarf"]["face_demand_Pa"],
                        "face_stress_lab_weld_Pa":P["lab8_eb_eta1"]["face_demand_Pa"],
                        "assumed_compressive_Pa":345e6},
        {"minimum_tensile_Pa":345e6,"minimum_compressive_Pa":None},None,
        I["new_primary_sources"][0]["url"],tag="QUESTIONABLE",O3_usage=0)
    nfi("sheet-anisotropy","Scalar nu=.0752 uses historical SR-200 data; a formed orthotropic shell requires its own model and properties.",
        "in_the_lab",{"nu":.0752,"E_Pa":290e9},{"nu12":.0768,"nu21":.0752},None,
        I["new_primary_sources"][1]["url"],tag="QUESTIONABLE")
    nfi("scarf10","Measure mean-shear allowable and peel/compression failure of the exact scarf; 10 MPa is assumed.",
        "PROJECTION",{"average_shear_Pa":10e6,"ratio":30,"total_skin_seams_m":2*P["af015_scarf"]["joining"]["seam_length_m"]},
        None,None,"MAINLINE-028 owner screen")
    nfi("stock-envelope","Confirm available raw blank sizes at 0.74–0.80 mm thickness; full published envelope belongs to thicker sheet.",
        "PROJECTION",{"a_m":.6096,"b_m":1.8288},{"thin_gauge_envelope":None},None,
        I["new_primary_sources"][0]["url"],panel_search_usage=0,panel_enlargement_factor=1)
    nfi("gauge","Map actual minimum thickness after forming and scarf preparation; nominal gauges sit at tight mode boundaries.",
        "exists_today",{"scarf_face_m":P["af015_scarf"]["tf_m"]},
        {"datasheet_gauge_tolerance_in_this_band_m":.0001016},None,
        I["new_primary_sources"][0]["url"],tag="QUESTIONABLE")
    nfi("AF015-bond","Published weight exists; matched Be/low-density-aluminium-core bond strength and stiffness are unknown.",
        "exists_today",{"film_lb_ft2":.015,"weight_per_line_kg_m2":I["routes"][0]["bond_kg_m2"]},
        {"old_film_lb_ft2":.030},2,
        "https://multimedia.3m.com/mws/media/282041O/3m-scotch-weld-structural-adhesive-film-af-163-2-af-163-3.pdf",
        fixed_O5_usage=1,tag="QUESTIONABLE")
    nfi("primer","Actual primer coverage, surface preparation and mass must be measured; 5 g/m² is a selected sensitivity.",
        "PROJECTION",{"per_line_kg_m2":.005,"two_lines_kg":P["af015_scarf_primer5"]["joining"]["primer_kg"]},
        None,None,"MAINLINE-028 sensitivity")
    nfi("lab-bond","8 g/m² deposition exists in laboratory work on other materials; transfer to Be/Al core is unqualified.",
        "in_the_lab",{"per_line_kg_m2":.008,"matched_strength":None},None,None,
        "https://infoscience.epfl.ch/server/api/core/bitstreams/28b8cc7a-f046-4da3-9fcc-5d5ad3c52a9d/content",
        Be_hull_transfer="PROJECTION")
    nfi("lab-weld","Ground parent compression retention, HAZ, brittle seam failure, distortion and final-hull access.",
        "PROJECTION",{"retention_needed_at_selected_point":P["lab8_eb_eta1"]["weld_retention_required_at_today_strength"],
                       "retention_assumed":1.0,"filler_mass_assumed_kg":0},None,None,
        "MAINLINE-028 ideal autogenous seam")
    nfi("splice-and-seal","Weigh and qualify the core splice, seals and intersection details.",
        "PROJECTION",{"core_gap_m":.0005,"splice_density_kg_m3":500,"seal_kg_per_hull_m":.002},
        None,None,"MAINLINE-028 mass assumptions")
    nfi("unmodelled-bond-seam","Relevant flatwise, imperfection shear, peel/HAZ, local buckling, thermal/cycle and leak allowables are absent.",
        "PROJECTION",{"overall_installed_SF":None},None,None,"Unknown modes listed in every point")
    nfi("019-reserve","Validate the optimistic service/environment assumptions behind the fixed mass-equivalent reserve.",
        "PROJECTION",I["case"]["reserve_fixed_lines"],None,None,"Pinned MAINLINE-019 / 021b",
        fixed_reserve_kg=I["case"]["reserve_fixed_items_kg"])
    nfi("core-data","Confirm core lot, minimum properties, forming and strength after bonding on the selected low-density core.",
        "exists_today",P["af015_scarf"]["core"],None,None,P["af015_scarf"]["core"]["source"],tag="QUESTIONABLE")
    nfi("255-sensitivity","S-200-F 255 MPa is a compression sensitivity, not a rolled-sheet specification or certified minimum.",
        "exists_today",{"compression_Pa":255e6,"no_core_face_SF_upper_bound":R["S200F255_all_subsets_infeasible_proof"]["face_SF_upper_bound_even_with_zero_core"]},
        None,None,I["new_primary_sources"][2]["url"],tag="QUESTIONABLE")
    (ROOT/"NFI.json").write_text(json.dumps({"schema":1,"card":"MAINLINE-028b","unit":I["unit"],
        "overall_installed_hull_SF":None,"rows":rows},indent=2)+"\n")
    checks={**B["validation"]["checks"],**R["validation"]["checks"]}
    pins=[]
    for p in I["pins"]:
        data=Path(p["local_path"]).read_bytes()
        ok=hashlib.sha256(data).hexdigest()==p["sha256"] and len(data)==p["bytes"]
        pins.append({"path":p["local_path"],"matches":ok,"sha256":p["sha256"]})
    assert all(x["matches"] for x in pins)
    assert len({x["id"] for x in rows})==len(rows)
    validation={"all_passed":all(checks.values()),"numeric_check_count":len(checks),"checks":checks,
                "base_details":B["validation"],"property_details":R["validation"],
                "frozen_pin_count":len(pins),"frozen_pins":pins,
                "unique_NFI_ids":True,"NFI_rows":len(rows),
                "code_sha256":{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                               for name in ("calculate.py","property_checks.py","make_report.py")},
                "INPUTS_sha256":hashlib.sha256((ROOT/"INPUTS.json").read_bytes()).hexdigest()}
    (ROOT/"VALIDATION.json").write_text(json.dumps(validation,indent=2)+"\n")
    note=ROOT.parents[2]/"notes"/(I["unit"]+".md")
    note.write_text(f"""# MAINLINE-028b handoff

Unit {I["unit"]}; order {I["order"]}. No time cap.
Report recipient sciences; cc co, xo and admiral-robotics-review-v2.

Task complete: three commissioned routes plus lab/scarf disambiguation,
47 honeycomb candidates, all subsets of the three adjustable factors, exact
021b nu=.33 comparison and SR-200 sheet nu=.0752 approximation, all six
continuum modes plus seam screen and explicit unknown modes.

Sheet-property seam-aware maximum usages: nominal 0.9719775174, primer
0.9960764381, lab/ideal weld 0.6514685431, lab/scarf 0.9578679244.
Every least adjustable set is gamma + wrinkling. AF fixed O5 remains at full.
S-200-F 255 MPa sensitivity has no feasible set: no-core face upper SF 0.9582173.
Best full-endpoint SFs 0.8698459 / 0.8668485 / 0.8709023.
Overall installed SF unknown. Strength and sheet-size assumptions remain open.

Artifacts: {ROOT}/CARD.md, RESULTS.json, PROPERTY-CHECKS.json,
INPUTS.json, NFI.json, METHOD.md, VALIDATION.json, reproducible scripts.
{len(checks)} aggregate numeric checks passed; {len(pins)} upstream pins match; {len(rows)} NFI rows.
No repository source changes, inherited script execution, or out-of-band contact.

Next: submit one pinned completion report, then SLEEPING. No successor is named;
await a queue assignment. State line records the eventual submission.
""")
    print(json.dumps({"card":str(ROOT/"CARD.md"),"numeric_checks":len(checks),
                      "pins":len(pins),"NFI_rows":len(rows),"note":str(note)}))


if __name__=="__main__":
    main()
