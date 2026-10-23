import json
import math
from datetime import datetime
from zoneinfo import ZoneInfo
from rederive import OUT, OWNER, model, score, LIFT


def write_json(name,data):
    (OUT/name).write_text(json.dumps(data,indent=2)+"\n")


def run():
    rows=[
        ("GRID-EXTREMUM","REVISE","The +1329.818726 kg and 0.689107645 values are correct at the filed grid points, but are not the best attainable values under the same continuous model.",
         "CONSTRUCTIVE-POINTS.json: +1127.071353 kg at least SF 1.000001080; fixed-mass least SF 0.699691806. Two starts converge.",
         "Label the old results as attained grid values. Append the constructive designs, report the continuous search domain, and refine around the adequacy boundary. Do not assert a global optimum."),
        ("HEAVY-DOME-GATE","QUESTIONABLE","The handbook's .425 recommendation is represented as applying only for psi about 28 or more.",
         "SOURCE-CHECK.md: IDH p4.1.012 supplies no numeric psi gate. CR-62257 p181 describes only a central accurately machined region and stronger surrounding support.",
         "Attribute psi>=28 to the model author, disclose calibration nu=.33/.35 and design versus as-built geometry, and seek a demonstrated transfer before calling it handbook credit."),
        ("BAY-CLAMPING","PROJECTION","gamma_s>=10 and equal-area circular-cap mapping are used to grant clamped-cap behavior to triangular sandwich bays.",
         "SUPPLEMENTARY.json: composite gamma_s 10.400178 versus isolated-member EI/(a Dskin) 3.196840. Circumscribed-circle substitution gives panel SF .390794 versus .710384.",
         "Validate translational and rotational edge restraint, joint compliance, triangular geometry and shear-flexible skin together. Compare multiple bay/frame stiffness ratios including below and above 10; replace the abrupt gate with validated behavior."),
        ("COUPLED-MODES-AND-LAYOUT","PROJECTION","The global wavelength cutoff leaves intermediate frame/bay modes unverified; the continuum length is not the actual 026 frame length.",
         "SUPPLEMENTARY.json: 3.427772 m unrestricted minimum versus 4.08 m cutoff; global SF 1.055069 versus 1.118206. 026 arc length 2161.451 m versus continuum 2133.882 m; unchanged Be tubes add 8.093 kg.",
         "Use a discrete, coupled frame/bay model covering the intervening wavelengths, eccentric constitutive coupling, real joint locations and arc lengths. Retain the continuum model as a screen."),
        ("SEAM-OPERATING-POINT","REVISE","The narrative says Q, scarf and tubes must move after adding the O5 mass deficit.",
         "EXTENDED-ARITHMETIC.json: at the owner's +1329.818726 kg point, wrinkle/scarf/tube-local SF are 1.059449/1.109144/1.055118 using today's assumptions.",
         "Separate fixed-mass failures from mass-added feasibility. Keep the seam-dependent finite-search result qualified by its model and search domain; no impossibility theorem was proved."),
        ("SOURCE-RATIOS","REVISE","The source's printed plain-Ti .33 ratio and literal .14 at a sphere are repeated as checked values.",
         "SOURCE-CHECK.md: 317/917=.345692475; SP-8032's .14+3.2/lambda^2 is greater than .14 for finite lambda. The filed C2b cap factor is .601013192, not the rounded-lambda .603.",
         "Record numerator, denominator, exact calculation and printed source value separately. Describe .14 as the large-lambda limit and use the full-precision bay factor."),
        ("STA8p1-MODEL-IDENTITY","REVISE","LIT-STIFF treats the 759,000 and 754,000 lb predictions as conflicting source values.",
         "STA8.1 PDF p4 distinguishes geometry refinement from the additional nonuniform-loading refinement. Relative errors against 743,000 lb are 2.153% and 1.480%.",
         "Assign separate model identities to the two predictions. Flag the intermediate model's incorrect 1.5% prose label. Clarify total versus web stiffener height instead of declaring an unexplained geometry contradiction."),
        ("THERMAL-JOINT-EQUILIBRIUM","QUESTIONABLE","SiC tube capacity uses the thermal compression envelope while line force and sleeve mass use only mechanical compression.",
         "SUPPLEMENTARY.json: 55.521 kN mechanical versus 63.974 kN compression envelope; difference 8.454 kN. This does not affect the Be-on-Be thermal comparison.",
         "Build signed hot/cold equilibrium cases and propagate member forces through sleeve, bond, core-line and peel calculations. Do not combine incompatible hot-face and cold-tube envelopes as one physical load case."),
        ("INPUT-COMPLETENESS","REVISE","Several numeric choices are recoverable but missing from the supplied inputs or compact geometry.",
         "METHOD.md: fillet density 1250 kg/m3 inferred from mass. SUPPLEMENTARY.json: calibration nu=.33/.35. Four gs5 compact rows omit shape and required psi-based recovery.",
         "Publish these inputs and each chosen section's shape with units and provenance. Keep all independent check limitations visible. Preserve measured elapsed values; their microsecond timestamp differences are harmless."),
        ("ALLOWABLES-AND-ASSEMBLY","QUESTIONABLE","Unity in the scored factors does not close material, bond, peel, residual-stress or thin-wall validation.",
         "The reconstruction retains 345 MPa tensile-as-compression, historical 379.2 MPa endpoint, typical core values, 10 MPa scarf, r/t=300 tube local rule and ideal composite action. A pin-ended Euler screen is 8.675 at the filed Be O5 point, but is not a full frame test.",
         "Keep an explicit unscored-mode/load-case ledger and ground formed-gauge compression, core at lines, scarf/bond/peel and imperfect thin tubes at representative boundaries. Do not convert the conditional mass-added point into a hull qualification.")
    ]
    nfi=[dict(id=f"C039-{i:02d}",topic=t,status=s,objection=o,evidence=e,proposed_fix=f,disposition="Record for owner revision; check completed")
         for i,(t,s,o,e,f) in enumerate(rows,1)]
    write_json("NFI.json",dict(schema=1,unit="vacuum-mainline039-check-1020",rows=nfi,
                              asks="none",standing="none",next="none"))
    a=json.loads((OUT/"ARITHMETIC.json").read_text())
    e=json.loads((OUT/"EXTENDED-ARITHMETIC.json").read_text())
    s=json.loads((OUT/"SUPPLEMENTARY.json").read_text())
    pins=json.loads((OUT/"INPUTS.json").read_text())
    cc=json.loads((OUT/"CONTINUOUS-CHECK.json").read_text())
    cp=json.loads((OUT/"CONSTRUCTIVE-POINTS.json").read_text())
    checks=[]
    def check(name,condition,evidence):
        checks.append(dict(check=name,passed=bool(condition),evidence=evidence))
    check("Owner/upstream/assignment pin integrity",pins["all_pins_match"],f'{pins["pin_count"]} comparisons')
    check("Detailed arithmetic",not a["mismatches"] and not a["uncovered_numeric_fields"],a["numeric_comparisons"])
    check("Extended arithmetic",not e["summary"]["mismatches"],e["summary"]["comparisons"])
    check("Compact-record missing shapes disclosed",len(e["summary"]["unreconstructed_fields"])==4,
          e["summary"]["unreconstructed_fields"])
    check("Nominal 028b reconstructed from seam and mass equalities",all(x["ok"] for x in s["nominal_checks"]),len(s["nominal_checks"]))
    check("Record-dome psi arithmetic",all(abs(v["psi"]-v["filed"])<1e-11 for v in s["psi_calibration"].values()),
          "Four ratios; nu choices explicitly inferred")
    check("Optimization convergence from two starts",all(v["success"] for v in cc),
          [dict(mode=v["mode"],start=v["start"],iterations=v["iterations"],min_constraint=v["min_constraint"]) for v in cc])
    for mode in ["mass","float"]:
        points=[x for x in cc if x["mode"]==mode]
        check(f"{mode} agreement between starts",abs(points[0]["mass_shift_kg"]-points[1]["mass_shift_kg"])<1e-6
              and abs(points[0]["least_SF"]-points[1]["least_SF"])<1e-8,"Independent initial points")
    for point in cp:
        v=point["design"]
        recomputed=model("C2b",2.04,v["tf_mm"]/1000,v["tc_mm"]/1000,v["lattice_kg"],v["shape"],10)
        sf=score(recomputed,True,True)
        check(point["mode"]+" original branch rules",recomputed["adequate"] and recomputed["cap_regime"] and not recomputed["heavy"],
              dict(gamma_s=recomputed["gamma_s"],lambda_p=recomputed["lam_panel"],psi=recomputed["psi"]))
        if point["mode"]=="mass":
            check("Constructive unity point",min(sf.values())>=1 and recomputed["masses"]["total"]-LIFT<1127.072,
                  dict(least_SF=min(sf.values()),extra_mass_kg=recomputed["masses"]["total"]-LIFT))
        else:
            check("Constructive fixed-mass point",abs(recomputed["masses"]["total"]-LIFT)<1e-6 and min(sf.values())>.69969,
                  dict(least_SF=min(sf.values()),mass_kg=recomputed["masses"]["total"]))
    full=json.loads((OWNER/"RUNS.json").read_text())
    result=json.loads((OWNER/"RESULTS.json").read_text())
    headline_count=0
    for concept in full["concepts"]:
        key=f'{concept["concept"]}@{concept["a_m"]}'
        for group,field in [("least_SF_today","best_today"),("least_SF_today_O5","best_today_O5")]:
            if field in concept:
                check(f"headline {group} {key}",abs(result["headline"][group][key]-concept[field]["least_SF"])<5.1e-5,"four-decimal presentation")
                headline_count+=1
        for cat,v in concept["lift_shift_kg"].items():
            check(f"headline mass {key} {cat}",abs(result["headline"]["lift_shift_kg"][key][cat]-v["shift_kg"])<=.051,"one-decimal presentation")
            headline_count+=1
        if concept["concept"]!="baseline":
            diff=full["concepts"][0]["lift_shift_kg"]["at_028b_values"]["shift_kg"]-concept["lift_shift_kg"]["at_028b_values"]["shift_kg"]
            check(f"headline reserve delta {key}",abs(result["headline"]["reserve_change_vs_028b_at_its_values_kg"][key]-diff)<=.051,"baseline-subtracted difference")
            headline_count+=1
    check("Recorded elapsed times",all(abs(v["difference_s"])<1e-5 for v in s["elapsed"]),s["elapsed"])
    check("026 member mass using its reported arc length",abs(s["diagnostics"]["026_layout"]["member_mass_from_area_and_reported_arc_length_kg"]-
                                                           s["diagnostics"]["026_layout"]["filed_026_member_mass_kg"])<1e-8,
          "Geometry length is source input; annular area and mass recomputed")
    assert all(c["passed"] for c in checks)
    validation=dict(schema=1,checked_at=datetime.now(ZoneInfo("America/Vancouver")).isoformat(),
                    status="PASS computational checks; REVISE interpretation and optimization claims",
                    numeric_field_comparisons=a["numeric_comparisons"]+e["summary"]["comparisons"]+len(s["nominal_checks"]),
                    headline_comparisons=headline_count,checks=checks,
                    limitations=["No owner source code read or executed; independent equations only.",
                                 "No independent global optimality or impossibility proof.",
                                 "The new unity point uses the same unvalidated cap, adequacy and material assumptions.",
                                 "Experimental metadata and material inputs are provenance, not new measurements.",
                                 "Four compact psi fields were used to recover missing shape and are not independent checks.",
                                 "Pineda and S-II measurement extraction inherited from pinned CHECK-035."])
    write_json("VALIDATION.json",validation)
    print(json.dumps(dict(checks=len(checks),passed=True,numeric_fields=validation["numeric_field_comparisons"],
                          headline_comparisons=headline_count,NFI=len(nfi)),indent=2))


if __name__=="__main__":
    run()
