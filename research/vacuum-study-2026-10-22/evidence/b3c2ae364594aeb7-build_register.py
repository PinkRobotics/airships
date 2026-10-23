#!/usr/bin/env python3
"""Build the additive design register; no upstream calculation is executed."""
import copy
import hashlib
import json
import math
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

B=Path(__file__).resolve().parent
def load(path): return json.loads((B/path).read_text())
def save(name,x): (B/name).write_text(json.dumps(x,indent=2,allow_nan=False)+"\n")
def pin(path):
    data=path.read_bytes()
    return dict(path=str(path.resolve()),sha256=hashlib.sha256(data).hexdigest(),bytes=len(data))
intake=load("INTAKE.json")
norm=load("NFI-NORM.json")
fresh=load("NEW-NFI.json")
routing=load("ROUTING.json")["assignments"]
assert set(routing)=={x["uid"] for x in fresh}
base=load("snapshots/baseline030/REGISTER.json")
rows=copy.deepcopy(base["rows"])
new_topics=[
 (87,"T06","Face sheet and panels","Finished minimum gauge, forming and strength retention"),
 (88,"T04","Wrinkling and core Ec","Waviness at the critical wavelength; metric and process transfer"),
 (89,"T11","Thermal","Sun, bond reference temperature and additional pressure/load interaction"),
 (90,"T01","Case and atmosphere","Terrain, weather, altitude floor/ceiling and passive equilibrium requirement"),
 (91,"T14","P3 local buckling","Tensile bending and coupled shell/column/curvature limits"),
 (92,"T18","P3 nodes and joints","Discrete curved-member rolling mechanisms and restraint"),
 (93,"T26","Grounding plan","Ordered evidence route and grounding of the current leads"),
 (94,"T24","Method and provenance","Snapshot completeness and pending follow-on filings"),
]
for number,topic,name,gap in new_topics:
    rows.append(dict(rid=f"R{number:03d}",topic=topic,topic_name=name,gap=gap,
                     unknown=gap,today=[],needed=[],owners=[],states=["QUESTIONABLE","PROJECTION"],
                     directions=["unknown"],check_outcome=None,raised_by_checks=[],
                     source_cards_checked_by=[],sources=[]))
byrid={r["rid"]:r for r in rows}
for r in rows: r["updates_030b"]=[]
for issue in fresh:
    byrid[routing[issue["uid"]]]["updates_030b"].append(copy.deepcopy(issue))

own=[
 ("B001","NFI-030B-BASIS","R083",
  "P2 comparisons use distinct pressure, Poisson and joint-account conventions.",
  "028b uses p0, nu=.0752 and max(J,.05S); 033 uses 1.01p0, nu=.0768 and actual J as its main case. 036's 027 R20 point retains a separate eta=.9 splice law. Keep these bases attached; a changed threshold is not an arithmetic contradiction."),
 ("B002","NFI-030B-FIXED-ASSUMPTIONS","R013",
  "Two adjustable optimisms do not mean two unresolved assumptions.",
  "The R10 nominal scarf already fixes .015 lb/ft2 film, assumes thin stock, transfers 345 MPa tensile yield to compression and uses an unqualified 10 MPa scarf screen. Neither zero strength-slider usage nor stock panel factor one qualifies those inputs."),
 ("B003","NFI-030B-LOAD-AND-MASS-TRANSFER","R089",
  "Weather, extra loads and vacuum bills have not been jointly optimized on every current lead.",
  "031 reoptimizes older seam/film geometry; 037 evaluates 028b's full endpoint and pre-022d P3; 034 estimates service at older geometries. Carry their requirements and evidence, but do not add their margins or copy their bills as validated values for 033/022d. Coating, pads, barriers and fittings require a complete reclosure."),
 ("B004","NFI-030B-SNAPSHOT","R094",
  "Unfiled cards and checks remain pending for 030c.",
  "Coverage is through the recorded final queue intake. No result or check is inferred from a running seat, a brief, an elapsed time or an unfiled artifact."),
 ("B005","NFI-030B-EVIDENCE-LABEL","R079",
  "A demonstrated source-contract correction is not a demonstrated hull capability.",
  "The Zylon directional factor is a demonstrated arithmetic/source mismatch in CHECK-022b/022c. New correction, measured coupon precedent, source absence and projected assembly capability remain distinct in this register."),
 ("B006","NFI-030B-DISCRETE-TRANSFER","R055",
  "The ordered 026b-to-022d fold is a sensitivity, not an exact-frame solution.",
  "Apply the ordered .848 only to the global mode of the held 022d screened lead, with all other modes and masses held. The frequency-4 section/topology differs, so the resulting 1.067 multiplier is QUESTIONABLE. The exact source ratio is also shown; no reoptimization, material qualification or verified nonlinear first loss follows."),
 ("B007","NFI-030B-017B-SUPERSESSION","R083",
  "017b's P3 improvement factors and trend projection use superseded 022c physics.",
  "Retain its directional study as historical evidence, but use 022d for current P3 values and the ordered 026b global sensitivity. Its 1.441 Zylon optimum and projected 14–25 year closure are not current lead predictions. P2's variable scarf, nu=.08 and piecewise gamma also differ from 028b/033."),
]
ownfile=dict(schema=1,card="MAINLINE-030b",tag="QUESTIONABLE; transfers PROJECTION",
             rows=[dict(id=i,title=title,finding=text,status="OPEN",blocks_progress=False)
                   for _,i,_,title,text in own])
save("AUTHORED-NFI.json",ownfile)
for (uid,rowid,rid,_,_),fields in zip(own,ownfile["rows"]):
    issue=dict(uid=uid,report="rpt-ref-39745602983887568501",
               card="MAINLINE-030b",file=str(B/"AUTHORED-NFI.json"),
               row_id=rowid,fields=fields,source_sha256=pin(B/"AUTHORED-NFI.json")["sha256"])
    norm.append(issue);byrid[rid]["updates_030b"].append(issue)

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

ALIASES={
 "028b":"rpt-ref-d907de1e97319ecc3f9a",
 "033":"rpt-ref-5b1ba7a48fcb57c8e35e",
 "022d":"rpt-ref-6c81b0b188ad134a3ea2",
 "031":"rpt-ref-9a0319231d2fe686eb92",
 "034":"rpt-ref-244f32e2449e729d312f",
 "036":"rpt-ref-5f14d083ceae03234596",
 "037":"rpt-ref-8c5de04c9c33dbcf7447",
 "026":"rpt-ref-7ce5b278fa083d87105b",
 "035":"rpt-mainline035-opus-knockdown-tests-1020",
 "026b":"rpt-ref-8befdd4c89803adc44a8",
 "017b":"rpt-ref-6ba73ec8a89453b26832",
 "038":"rpt-ref-536c47263ffe5f46fd19",
 "CHECK035":"rpt-ref-d3afcdc3514000cb6fc2",
 "CHECK036":"rpt-ref-f182f16ed5be422b7811",
}
def source(alias,name): return load("snapshots/"+ALIASES[alias]+"/"+name)
def ref(alias,name,selector):
    p=B/"snapshots"/ALIASES[alias]/name
    return dict(report=ALIASES[alias],file=str(p),sha256=pin(p)["sha256"],selector=selector)

original_p2=source("028b","PROPERTY-CHECKS.json")
p2=[]
for route in ["af015_scarf","af015_scarf_primer5","lab8_eb_eta1"]:
    s=next(x for x in original_p2["searches"] if x["route"]==route and x["joint_screen_enforced"])
    p=s["floating_point"]
    p2.append(dict(id="028b-"+route,R_m=10.,basis="028b p0; nu=.0752; retained joint floor",
        source=ref("028b","PROPERTY-CHECKS.json",f"searches[route={route},joint_screen_enforced=true].floating_point"),
        gamma=p["needed"]["gamma"],Q=p["needed"]["wrinkle"],
        gamma_factor=p["factor_vs_today"]["gamma"],Q_factor=p["factor_vs_today"]["wrinkle"],
        strength_factor=1.,strength_Pa=345e6,E_Pa=290e9,tf_m=p["tf_m"],tc_m=p["tc_m"],
        face_compression_required_Pa=p["face_demand_Pa"],usage=s["least_set"]["min_max_usage"],
        physical_joining_kg=p["masses_kg"]["physical_joining"],payload_kg=0.,
        modes={**p["at_needed"]["six_modes"],"joint_screen":p["at_needed"]["projected_seam_SF"]},
        tag="PROJECTION",overall_installed_hull_SF=None,original_point=p))
r33=source("033","RESULTS.json")
t33=r33["tracks"]["explicit_028_bill_with_scarf_screen"]
threshold=next(x for x in t33["thresholds"] if x["mask"]==3)
for radius in [threshold["first_R_m"],15,20,30,50]:
    if radius==threshold["first_R_m"]:
        p=threshold["witness"];usage=1.;selector="tracks.explicit_028_bill_with_scarf_screen.thresholds[mask=3].witness"
    else:
        r=next(x for x in t33["radii"] if x["R_m"]==radius)
        p=r["selected_minimum_needed"];usage=p["root_max_usage"]
        selector=f"tracks.explicit_028_bill_with_scarf_screen.radii[R_m={radius}].selected_minimum_needed"
    p2.append(dict(id=f"033-R{radius:g}",R_m=radius,basis="033 1.01p0; nu=.0768; actual joining",
        source=ref("033","RESULTS.json",selector),gamma=p["properties"]["gamma"],Q=p["properties"]["Q"],
        gamma_factor=p["improvement_factors"]["gamma"],Q_factor=p["improvement_factors"]["Q"],
        strength_factor=p["improvement_factors"]["face_strength"],strength_Pa=p["properties"]["strength_Pa"],
        E_Pa=p["properties"]["E_Pa"],tf_m=p["geometry"]["tf_m"],tc_m=p["geometry"]["tc_m"],
        face_compression_required_Pa=p["properties"]["face_stress_Pa"],usage=usage,
        physical_joining_kg=p["masses_kg"]["actual_joining"],payload_kg=p["masses_kg"]["payload"],
        modes=p["modes"],tag="PROJECTION",overall_installed_hull_SF=None,original_point=p))
graph35=source("CHECK035","DIGITIZATION.json")
hemispheres=[x for x in graph35["points"] if x["id"].startswith("hemisphere_")]
hemisphere_low=min(x["gamma"] for x in hemispheres)
hemisphere_high=max(x["gamma"] for x in hemispheres)
for p in p2:
    p["weather_attachment"]="031 requirements apply; its optimized altitude numbers are for older geometry, not a validated substitution into this point."
    p["loads_attachment"]="037 evaluated 028b full endpoint, not this minimum-usage geometry or the larger 033 points; combined closure remains open."
    p["compression_attachment"]="036 establishes missing qualification, while required face stress here is recomputed from this point's own load/geometry."
    # Checked 032 equation, transferred to these new core thicknesses and Q.
    # These are conditional amplitudes, not measured fabrication capability.
    p["waviness_projection"]={str(psi):p["tc_m"]*(psi*6894.757293168361)/103421359.3975254/.64*(.82/p["Q"]-1)
                               for psi in [35,60]}
    p["gamma_over_different_hemisphere_graph_centers"]=[p["gamma"]/hemisphere_high,p["gamma"]/hemisphere_low]
    p["gamma_over_hemisphere_graph_read_uncertainty_range"]=[p["gamma"]/(hemisphere_high+.01),p["gamma"]/(hemisphere_low-.01)]
    p["hemisphere_comparator"]=dict(source=ref("CHECK035","DIGITIZATION.json","points[hemisphere_low,hemisphere_high]"),
        graph_centers=[hemisphere_low,hemisphere_high],reading_uncertainty=.01,
        scope="Unmatched geometry; Vc and elastic/plastic/thermal reduction unresolved. Numeric comparison, not required qualified improvement or universal record.")

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

# Every inherited optimism remains in RESULTS history; current named choices
# and their evidence category are separately made explicit below.
optimisms=[]
for p in p2:
    factors=[
      ("P2-O1","gamma",p["gamma_factor"],"No compatible elastic sphere at lead geometry. CHECK-035 S-II graph centers about .21–.22 +/- .01, unknown Vc/reduction; cylinder and other marine tests are different precedent.","G1"),
      ("P2-O2","wrinkling Q",p["Q_factor"],"Handbook/measurement precedent only; no Be/core/bond wavelength-specific qualification.","G5"),
      ("P2-O3","face strength",p["strength_factor"],"Tensile minimum exists; no qualified thin formed-sheet compressive minimum. Required stress stays explicit.","G4"),
      ("P2-O4","panel enlargement",1.,"No enlargement chosen; stock dimensions at thin gauges are unconfirmed.","G4"),
      ("P2-O5","bond areal mass reduction",18.3091036364 if "lab8" in p["id"] else 2.,
       "Laboratory cell-edge deposition on other adherends." if "lab8" in p["id"] else "Commercial .015 film weight; installed Be/Al-core strength and complete process mass unqualified.","G3"),
      ("P2-J","joint capacity",None,"30:1/10MPa assumed screen, or ideal weld retention; no qualified installed joint.","G3"),
      ("P2-W","weather and clearance",None,"031 hydrostatic model precedent; mission/site requirements remain a decision.","G0"),
      ("P2-L","coating and load introduction",None,"037 conditional estimates; combined current-geometry mass and capacity not established.","G6"),
      ("P2-V","sealed service",None,"034 24-hour planning candidate; assembly gas-load measurement required.","G7"),
    ]
    for oid,name,factor,evidence,route in factors:
        optimisms.append(dict(lead=p["id"],id=oid,name=name,factor=factor,tag="PROJECTION",
                              evidence_category="none" if oid in ["P2-J","P2-L","P2-V"] else "precedent",
                              evidence_state=evidence,grounding_route=route))
optimisms+= [
 dict(lead="P3-022d-screened",id="P3-F",name="complete Zylon membrane",
      factor=p3["film_specific_strength_factor_vs_Kapton_design"],tag="PROJECTION",
      evidence_state="Fibre precedent; no qualified complete gas-tight 0/90 membrane at this effective specific design strength.",grounding_route="G8"),
 dict(lead="P3-022d-screened",id="P3-C",name="SiC compression",
      factor=p3["assumed_compression_vs_380MPa_flexural_proxy"],tag="PROJECTION",
      evidence_state="3.9 GPa typical bulk crush versus a 380 MPa flexural proxy is a numeric comparison, not equivalent allowables. Full-size compression remains unknown.",grounding_route="G9"),
 dict(lead="P3-022d-screened",id="P3-G",name="global lattice knockdown",
      factor=None,value=.2,tag="PROJECTION",
      evidence_state="026b frequency4 ratio .848429 motivates ordered .848 global sensitivity; neither calibrates k=.2 nor solves the current frame.",grounding_route="G2"),
 dict(lead="P3-022d-screened",id="P3-local",name="local cylinder-to-arc gamma",
      factor=None,value=p3["gamma"],tag="PROJECTION",
      evidence_state="NASA cylinder relation transferred to a curved ceramic member; coupled shell/column behavior unqualified.",grounding_route="G2"),
 dict(lead="P3-022d-screened",id="P3-J",name="joint multiplier and rigidity",
      factor=p3["target_multiplier"]**2,tag="PROJECTION",
      evidence_state="Lambda-squared joint mass is corrected. Actual SiC bond, adhesive mass, bearing, moment and anti-roll capacities remain unknown.",grounding_route="G2"),
 dict(lead="P3-022d-screened",id="P3-T",name="tensile-bending ceiling",
      factor=None,value_Pa=15.586e6,tag="PROJECTION",
      evidence_state="Assumed screen; zero tension at this selected limit, but no full-size probabilistic qualification.",grounding_route="G9"),
 dict(lead="P3-022d-screened",id="P3-M",name="manufactured arc and loaded membrane shape",
      factor=None,tag="PROJECTION",evidence_state="No combined qualified production geometry; fractional node counts and cap shape are surrogates.",grounding_route="G2"),
]
for item in optimisms:
    if "evidence_category" not in item:
        item["evidence_category"]="precedent" if item["id"] in ["P3-F","P3-C","P3-G","P3-local"] else "none"

ground=[
 dict(id="G0",rank=0,route="Choose mission requirements",status="DECISION",
      evidence="031 and its check; 037",target="Weather envelope, terrain-relative clearance, altitude ceiling/control, coating, bond reference temperature, airspeed and mooring wind."),
 dict(id="G1",rank=1,route="Imperfect sandwich-sphere analysis and calibrated shape evidence",status="029 pending unless superseded in final intake",
      evidence="030 priority 1; CHECK-035 finds no compatible elastic sphere datum at lead geometry, without claiming universal absence",target="P2 gamma at each actual joined geometry, followed by appropriate measured validation."),
 dict(id="G2",rank=2,route="Discrete P3 frame with actual nodes and film coupling",status="026 and026b filed; exact current frame and new nonlinear first loss unresolved",
      evidence="030 priority 2; 026/check; 026b; 022d",target="Use current3.184m member geometry, integer topology, anti-roll/moment stiffness, complete mass and local/material interaction. Ordered global sensitivity1.067 is not a solved frame."),
 dict(id="G3",rank=3,route="Weighed curved sealed sandwich/joint article",status="EVIDENCE REQUIRED",
      evidence="030 priority 3; 028b/check; 036; 034",target="Scarf/face-core capacity and stiffness, actual primer/splice/seal mass, thermal cycling, leak paths and shape."),
 dict(id="G4",rank=4,route="Finished thin-sheet specification and compression evidence",status="EVIDENCE REQUIRED",
      evidence="030 priority 4; 036",target="Minimum gauge, raw dimensions, orthotropic post-form properties and about 300 MPa effective compression at the scarf leads. Any external contact is a separate authorized task."),
 dict(id="G5",rank=5,route="Matched wrinkle coupon and wavelength-resolved metrology",status="EVIDENCE REQUIRED",
      evidence="030 priority 5; 032/check; 032b",target="Core/bond weakest flatwise capacity, Q, critical wavelength and as-built zero-to-peak component on the actual Be/core assembly."),
 dict(id="G6",rank=6,route="Thermal and hardpoint closure on the chosen hull",status="EVIDENCE REQUIRED",
      evidence="037",target="Coating mass, assembly stress-free temperature, wind pressure map and pad load path; charge pads/coating and reclose each selected hull."),
 dict(id="G7",rank=7,route="Assembly gas-load and evacuation test",status="EVIDENCE REQUIRED",
      evidence="034",target="Every cell/bore vented, installed seam/port leaks, conditioning inventory, pressure and lift debit, monitoring endurance."),
 dict(id="G8",rank=8,route="Complete P3 membrane process and barrier qualification",status="EVIDENCE REQUIRED",
      evidence="024/check; 022b/c check; 022d; 034",target="Two-direction strength, full barrier/attachment mass, biaxial creep, seams and loaded shape; no fibre-only payload credit."),
 dict(id="G9",rank=9,route="Full-size curved-tube material and joint evidence",status="EVIDENCE REQUIRED",
      evidence="025/check; 026; 022d",target="Compression/tension populations, contact fields, manufacturing and failure probability; preserve null allowables until established."),
]
plan38=source("038","TEST-PLAN.json")
physical_map={"G1":["T7"],"G2":["T6","T8"],"G3":["T2"],"G4":["T1"],
              "G5":["T3"],"G6":["T2","T9"],"G7":["T9"],"G8":["T4"],"G9":["T5","T6"]}
for g in ground:
    g["original_030_priority"]=g["rank"] if 1<=g["rank"]<=5 else None
    g["physical_tests_038"]=physical_map.get(g["id"],[])
for item in optimisms:
    item["physical_tests_038"]=physical_map.get(item["grounding_route"],[])

report_ids={x["id"] for x in intake["reports"]}
pending=[]
for name,term in [("029 gamma FE","mainline029"),("026b frame bays","mainline026b"),
                  ("038 grounding plan","mainline038"),("039 stiffened sandwich","mainline039"),
                  ("017b improvement directions","mainline017b"),
                  ("CHECK-026","check026"),("CHECK-035","check035")]:
    present=any(term in rid or (term.startswith("check") and "mainline"+term[5:]+"-check" in rid)
                or (term.startswith("check") and "check-mainline"+term[5:] in rid) for rid in report_ids)
    pending.append(dict(item=name,status="FILED" if present else "PENDING",match=term,
                        next="Fold into this register if filed before cutoff; otherwise 030c."))

checks=copy.deepcopy(load("snapshots/baseline030/CHECK-VERDICTS.json"))
existing_checks={x["check_id"] for x in checks}
for report in intake["reports"]:
    rid=report["id"]
    if "check" in rid.lower() and rid not in existing_checks:
        checks.append(dict(check_id=rid,at=report["at"],
            verdict=("REVISE source readings and conclusions; 112 comparable derived fields reproduce" if rid==ALIASES["CHECK035"] else
                     "Administrative filing notice; no new scientific check" if not report["artifacts"] else
                     "Source-reported check with explicit limitations; see full statement and findings"),
            statement=report["body"],
            findings=[x for x in fresh if x["report"]==rid],
            files=[x["snapshot"] for x in report["artifacts"] if x.get("snapshot")]))

ledger=copy.deepcopy(load("snapshots/baseline030/LEDGER.json")["rows"])
corrections=[
 ("CHECK-036 reproduces thresholds and corrects a legacy film label",[ALIASES["036"],ALIASES["CHECK036"]],
  "4945 comparisons and150 threshold/sensitivity points pass. R20 sheet-scalar threshold381.612–381.639MPa. OldR20 .015lb/ft2 label conflicts with governing.146472829kg/m2=.030; calculations use.030. Historical379.2MPa at1.96mm confirmed, still not matched finished thin-sheet qualification."),
 ("CHECK-035 revises graph readings and narrows absence claims",[ALIASES["035"],ALIASES["CHECK035"]],
  "S-II centers .209242/.221511 (about +/- .01), not .22/.24. Add eleventh cylinder point; use analytic CR1457 curve. CTA8.3 printed .864 versus load ratio .865305 unresolved. Other marine/foam-core tests exist; no compatible elastic sphere at recoverable moderateVc is established, and unprecedented control is not proven."),
 ("026b global transfer moves the current P3 screen", [ALIASES["026b"],ALIASES["022d"]],
  "Ordered .848 times1.258252476558=1.066998100121; exact frequency4 ratio gives1.067537780749. Global alone moves; mass and other modes held. QUESTIONABLE cross-geometry sensitivity."),
 ("026b new nonlinear first-loss fields remain null",[ALIASES["026b"]],
  "Raw nearest-zero crossings5.082444/2.218113 can skip an unstable family. No verified first-instability claim, no retry or new numerical work performed here."),
 ("026b rise and mass conventions remain explicit",[ALIASES["026b"]],
  "Rise8 retains538.899kN mean compression and4.248GPa elastic bending. Frequency4 sag uncharged; frequency2 carries187.938kg. No uniform mass-budget comparison."),
 ("017b P3 numerical leads superseded by022d",[ALIASES["017b"],ALIASES["022d"]],
  "Retain trends/directions and all15NFIs, not old1.441 Zylon optimum or its14–25year closure as current predictions. P2 comparisons use variable scarf and piecewise gamma."),
 ("Combined032/032b check repairs metrology attribution",["rpt-ref-7427b639691bfaf71f29"],
  "533 comparisons pass; Woody3micrometres is template adjustment, .008in coupon faces identified, Rion near-wavelength measured evidence added for carbon/Nomex. Be modal gap remains."),
 ("038 turns ground-first list into physical test sequence",[ALIASES["038"]],
  "First compression/specification, weighed sealed scarf, same-batch wrinkle screens; nine test families. Prices projected, no quotes; newest P3 target must use selected022d reserve, not frozen022c."),
 ("028b replaces panel enlargement with stock scarf and fixed thin film",
  ["rpt-ref-d907de1e97319ecc3f9a","rpt-ref-aae116a5fcd787ed9abc"],
  "Two remaining adjustable factors; fixed O5 is still consumed. Nominal gamma/Q=2.820818×/1.317054× at p0."),
 ("P2 R10 results must keep pressure and accounting bases",
  [ALIASES["028b"],ALIASES["033"]],
  "028b passes at p0; 033 includes +1% pressure and fails at R10 with the scarf screen. Threshold actual bill10.350852m; floor10.358194m."),
 ("Thin-sheet compression remains unqualified", [ALIASES["036"]],
  "Current maker345MPa is tensile. Current scarf demand about300MPa; 036 older027 R20 needs about382MPa under its own different joint/elastic assumptions."),
 ("Zylon 0/90 source contract halves old film factors",
  ["rpt-ref-f6de390e1555b4ca8e78",ALIASES["022d"]],
  "Old022c cap5%/019 fixed-geometry factors .746876/.708523. 022d charges both plies and reoptimizes; selected screened1.258252."),
 ("Joint capacities and mass must use claimed multiplier",
  ["rpt-ref-f4daf73c940b6f527d37","rpt-ref-f6de390e1555b4ca8e78",ALIASES["022d"]],
  "Old joint sized at lambda1 had no pressure reserve. New sleeve/wrap mass scales lambda²; its own capacity equals target, still unqualified."),
 ("P3 tensile bending and local/column interaction",["rpt-ref-f6de390e1555b4ca8e78",ALIASES["022d"]],
  "022d includes Ft15.586MPa projection; current screened lead has no tensile stress at target. Coupled instability stays open."),
 ("P3 screened lead replaces out-of-band maxima",[ALIASES["022d"],"rpt-ref-490f8e9228d526b69dc8"],
  "Half-wave/member=1 at3.170759m spacing; not validated continuum. Two-way C4 remains unqualified."),
 ("Discrete frame result is not an installed safety factor",[ALIASES["026"]],
  "6.465222 elastic eigenvalue versus6.127640; mechanisms for free pins;61.40kg overrun; local/material screens precede elastic limits."),
 ("Altitude benefit requires weather/terrain choice",[ALIASES["031"],"rpt-ref-be337d7d2ce1259d0aff"],
  "Optimistic100m floor55.341kg headroom, nominalSF1.036553. P3 altitude passes remain out of half-wave band; do not adopt them as the current P3 lead."),
 ("Thermal, wind and mooring screens add required mass and choices",[ALIASES["037"]],
  "Coated/bond-reference shear can be1.678 or.917; bare.388.70-knot screen.998442, nominal pads8.65/33.14kg. No uncharged pad fixes."),
 ("Vacuum service differs from gas-only life",[ALIASES["034"]],
  "Ground-evacuated sealed24h at30–50kg estimated; preserve100kg. Outgassing is phase transfer, ingress adds mass. Zylon complete bill91.624–111.624kg at older geometry."),
 ("Frame material names refer to fittings",[ALIASES["034"]],
  "Both Kapton/Ti and Zylon/CFRP P3 frames are SiC tubes. Titanium and CFRP designate end fittings, not tube material."),
 ("035 arithmetic is separate from physical comparability",[ALIASES["035"],ALIASES["CHECK035"]],
  "112 comparable derived fields reproduce. Corrected S-II readings, unknownVc/plasticity, anisotropic SBKF denominator and extra experimental leads prevent universal absence or transferable sphere-penalty claims."),
 ("032 lead-only amplitude/cell prose corrected",["rpt-ref-a30a669ed3e245f1473b"],
  "Lead-only range .00684754923–.01604921437; .0046–.024 spans four cases. Fc is weakest of core compression/tension/bond;35psi is minimum average."),
 ("032b compares distinct measurement quantities",["rpt-mainline032b-grok-measured-flatness-1020"],
  ".001651mm aluminium cell depth is precedent; .024mm reflector RMS and .2032mm whole-panel RMS are not the critical wrinkle component."),
 ("015b tolerance correction retains extra source qualifications",
  ["rpt-ref-a5374575ee8867fc8d2e"],
  "Old/live RMS2.6112627; actual-gamma RMS .139344/.654416mm. Rounded021b gamma changes amplitude.379%, not only fourth digit; k-span is conditional."),
 ("028 legacy reoptimization contained unstated eta=.9",
  ["rpt-ref-68dff0680696fe9b4cb4"],
  "Without hidden screen, legacy stock/four-metre SF .792549/.914222 rather than .750851/.844536. Nominal scarf result stands."),
 ("020 grade, modulus and doubler supply corrections",
  ["rpt-ref-35706d7a2ae7e951590b"],
  "Use product-specific SR200 strength/290GPa basis; doubling material changes historical supply/cost. Do not treat a source transfer as compression admission."),
 ("024 original sag and pump accounts incomplete",
  ["rpt-ref-7d6892c4e55be16ad523",ALIASES["034"]],
  "Original cap rise alone charged no sag volume.022c/d charge sag;034 separates systems choices and extra membrane mass."),
 ("027 P3 member-force convention flagged",
  ["rpt-ref-7b45cb6b4d7f92067f8b"],
  "Inherited pRs/2 is not triangular pRs/(2sqrt3); global/film unchanged, member scores conditional."),
 ("025 property edition and missing sag carried",
  ["rpt-ref-a8b77f7de2ffc56af7b4"],
  "CurrentSA table430GPa versus carried410GPa has negligible reported governing effect; no qualified compression; original025 excludes sag."),
 ("030 half-wave coefficient and duplicate source pointer confirmed",
  ["rpt-ref-490f8e9228d526b69dc8"],
  "Printed1.06 rounds1.06066 under thin-radius convention; no conclusion changes.362 unique rows,363 pointers because N023 has two subjects."),
]
for title,by,effect in corrections:
    ledger.append(dict(correction=title,by=by,effect_on_lead=effect,lead_relevant=True,
                       register_version="030b",tag="QUESTIONABLE / PROJECTION"))

coverage=dict(baseline_rows=len(base["rows"]),baseline_unique_source_rows=362,
              baseline_source_pointers=sum(len(r["sources"]) for r in base["rows"]),
              new_upstream_source_rows=len(fresh),authored_rows=len(own),
              total_unique_source_rows=len(norm),register_rows=len(rows),
              upstream_primary_nfi_files=len(load("NEW-NFI-SOURCES.json")),
              original_rows_preserved=True,source_rows_complete=True)
original_norm=load("snapshots/baseline030/NFI-NORM.json")
assert norm[:362]==original_norm
for old,current in zip(base["rows"],rows):
    assert all(current[k]==v for k,v in old.items()),old["rid"]
all_refs=[x["uid"] for r in rows for x in r["sources"]]+[x["uid"] for r in rows for x in r["updates_030b"]]
assert set(all_refs)=={x["uid"] for x in norm}
assert len(norm)==len({(x["report"],x["file"],x["row_id"]) for x in norm})
assert all(x["matches"] for r in intake["reports"] for x in r["artifacts"])

save("REGISTER.json",dict(schema=2,tag="QUESTIONABLE / PROJECTION",rows=rows,
                         source_files=base["source_files"],coverage=coverage))
save("NFI.json",dict(schema=2,unit=B.name,tag="QUESTIONABLE / PROJECTION",
                    blocks_progress=False,overall_installed_hull_SF=None,
                    rows=norm,auxiliary_source_documents="NEW-NFI-SOURCES.json",
                    note="Source fields, including source-specific resolution/disposition, preserved. No issue closes solely by being merged."))
save("REGISTER-COVERAGE.json",coverage)
save("CHECK-VERDICTS.json",checks)
save("LEDGER.json",dict(schema=2,baseline_rows=88,rows=ledger))
save("OPTIMISM-LEDGER.json",dict(schema=1,tag="PROJECTION",rows=optimisms,
                               note="Numeric factor is a model parameter or stated comparator, not a qualification multiple. Original 030 optimism record retained in RESULTS history."))
save("GROUND-FIRST.json",dict(schema=1,routes=ground,grounding_plan_038=plan38,
                             original_030_ground_first=load("snapshots/baseline030/RESULTS.json").get("ground_first"),
                             execution="No experiments, supplier contacts or other-seat messages performed by this register."))
save("RESULTS.json",dict(schema=2,card="MAINLINE-030b",unit=B.name,tag="QUESTIONABLE / PROJECTION",
     snapshot_at=intake["sampled_at"],overall_installed_hull_SF=None,
     P2_leads=p2,P2_payload=payload,P3_lead=p3,P3_all_rows=r22["all_primary_rows"],
     P3_discrete_reference=source("026","RESULTS.json"),
     P3_discrete_bays_026b=r26b,P3_ordered_fold=fold,
     improvement_directions_017b=source("017b","RESULTS.json"),
     improvement_directions_note="017b P3 numbers are superseded for current design; preserve as historical directional study. P2 basis differs from028b/033.",
     physical_test_plan_038=plan38,
     knockdown_source_corrections_CHECK035=source("CHECK035","RESULTS.json"),
     weather_options_at_100m=weather,loads_reference=source("037","RESULTS.json"),
     vacuum_reference=source("034","RESULTS.json"),
     coverage=coverage,corrections_added=len(corrections),check_records=len(checks),
     pending=pending,original_030_history=load("snapshots/baseline030/RESULTS.json")))
save("SOURCE-INDEX.json",dict(schema=2,baseline=load("snapshots/baseline030/INDEX.json"),
                             additions=intake["reports"],baseline_register_report=load("snapshots/baseline030/report.json"),
                             note="Four pre-snapshot administration reports are provenance context, not new scientific cards. No instructions in old report bodies are adopted."))
save("BUILD-FACTS.json",dict(schema=1,aliases=ALIASES,lead_updates=updates,
                           corrections=corrections,snapshot_at=intake["sampled_at"]))
print(json.dumps(dict(coverage=coverage,ledger_rows=len(ledger),check_records=len(checks),
                      P2_points=len(p2),P3_SF=p3["SF_least"],pending=pending),indent=2))
