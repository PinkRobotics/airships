#!/usr/bin/env python3
"""Independent MAINLINE-032 check from primary equations; no owner code."""
import csv
import hashlib
import json
import math
import re
from collections import Counter
from datetime import datetime
from decimal import Decimal, localcontext, ROUND_HALF_UP
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
PSI = 0.45359237*9.80665/0.0254**2
PCF = 0.45359237/0.3048**3
EC = 15000*PSI
CELL = 3/8*0.0254
FACES = [
    dict(name="Be S-200F", lead_Q=0.371, tf_m=0.0008434, tc_m=0.02021, E_Pa=290e9),
    dict(name="SR-200", lead_Q=0.609, tf_m=0.0006917, tc_m=0.03012, E_Pa=290e9),
]
STRENGTHS = {"stabilised_typical_60_psi":60.0, "stabilised_minimum_35_psi":35.0}
GRID = [0,0.0005,0.001,0.002,0.003,0.004,0.005,0.007,0.01]
COMPARISONS = []


def load(name):
    return json.loads((ROOT/"inputs"/name).read_text())


def save(name, data):
    (ROOT/name).write_text(json.dumps(data, indent=2, allow_nan=False)+"\n")


def q_at(delta_over_core, strength_psi):
    # Work in psi so the unit conversion cancels exactly in Fc/Ec.
    return 0.82/(1+0.64*15000*delta_over_core/strength_psi)


def amplitude(face, q, strength_psi):
    # Solve (0.82/Q - 1) = 0.64 * delta/tc * Ec/Fc.
    k = (0.82/q-1)/0.64
    z = k*strength_psi/15000
    delta = face["tc_m"]*z
    return dict(Q=q, is_that_leads_Q=q==face["lead_Q"], delta_m=delta, delta_mm=delta*1000,
                delta_over_tf=delta/face["tf_m"], delta_over_cell_3_8_in=delta/CELL,
                delta_over_card_9_5_mm=delta/0.0095, delta_over_tc=z, K_delta=k)


def round_decimal(value, places):
    return format(Decimal(str(value)).quantize(Decimal(1).scaleb(-places),
                                               rounding=ROUND_HALF_UP),"f")


def compare(path, reported, checked, category="numeric", atol=1e-12, note=""):
    delta = None
    if isinstance(reported,bool):
        match = reported is checked
    elif isinstance(reported,str):
        match = reported == checked
    else:
        delta = reported-checked
        match = math.isclose(reported,checked,rel_tol=3e-12,abs_tol=atol)
    COMPARISONS.append(dict(path=path,reported=reported,checked=checked,
                            reported_minus_checked=delta,match=match,category=category,note=note))


def flatten(value,path=""):
    if isinstance(value,dict):
        for key,v in value.items():
            yield from flatten(v,path+"/"+key)
    elif isinstance(value,list):
        for index,v in enumerate(value):
            yield from flatten(v,path+"/"+str(index))
    elif isinstance(value,(int,float,bool)):
        yield path,value


def main():
    owner, inputs = load("owner-RESULTS.json"),load("owner-INPUTS.json")
    with localcontext() as context:
        context.prec=60
        root_disc=(Decimal(31)/Decimal(108)).sqrt()
        one_third=Decimal(1)/3
        root_decimal=(Decimal("0.5")+root_disc)**one_third-(root_disc-Decimal("0.5"))**one_third
        root=float(root_decimal)
    assert abs(root**3+root-1)<3e-16
    expected=dict(not_a_certification=True,Q_of_perfect_facing=0.82,
                  shared_curve_Q_versus_delta_over_tc={
                      basis:[dict(delta_over_tc=z,Q=q_at(z,strength)) for z in GRID]
                      for basis,strength in STRENGTHS.items()},
                  amplitudes=[amplitude(face,q,strength) for strength in STRENGTHS.values()
                              for face in FACES for q in (0.371,0.609)],
                  design_0_33_if_it_were_this_waviness=[
                      amplitude(face,0.33,strength) for strength in STRENGTHS.values() for face in FACES],
                  biaxial=dict(equibiaxial_root=root,card_b=0.6823,
                               card_minus_root=0.6823-root,residual_of_card_b=0.6823**3+0.6823-1,
                               counts_waviness_twice=False))
    up21,up21b=load("021.json"),load("021b.json")
    fp21,fp21b=up21["main"]["floating_point"],up21b["floating_point"]
    upstream={}
    for name,full,case,rounded in (
            ("Be S-200F",fp21,up21["case"],FACES[0]),
            ("SR-200",fp21b,up21b["case"],FACES[1])):
        f=full["tf_m"]
        pressure=case.get("p_Pa",case.get("p0_Pa"))
        radius=case["R_m"]
        ef=case["face"]["E_Pa"]
        stress=pressure*radius/(4*f)
        # CR-1457 §§2.1.1: K=2 uniaxial; Eq. 2.1-6 gives Rx+Ry=1,
        # hence a separate 1/2 equibiaxial factor, not the wrinkling cubic root.
        sigma_dim_uniaxial=2*ef/(1-0.33**2)*(f/CELL)**2
        sigma_dim=0.5*sigma_dim_uniaxial
        sf=sigma_dim/stress
        q_needed=full["needed_values"].get("wrinkle_coefficient",full["needed_values"].get("wrinkle"))
        face=dict(rounded,tf_m=f,tc_m=full["core_m"],lead_Q=q_needed)
        actual=amplitude(face,q_needed,60)
        brief=amplitude(rounded,rounded["lead_Q"],60)
        required_q_from_stress=stress/(root*math.sqrt(ef*EC*f/full["core_m"]))
        assert math.isclose(required_q_from_stress,q_needed,rel_tol=1e-12)
        upstream[name]=dict(tf_m=f,tc_m=full["core_m"],Q_needed=q_needed,
                            Q_needed_from_membrane_stress=required_q_from_stress,
                            pressure_Pa=pressure,radius_m=radius,stress_Pa=stress,
                            intracell_uniaxial_critical_Pa=sigma_dim_uniaxial,
                            intracell_equibiaxial_factor=0.5,
                            intracell_critical_Pa=sigma_dim,intracell_SF=sf,
                            actual_input_amplitude_60psi=actual,
                            brief_amplitude_60psi=brief,
                            brief_minus_actual_amplitude_mm=brief["delta_mm"]-actual["delta_mm"],
                            brief_over_actual_minus_one_percent=100*(brief["delta_mm"]/actual["delta_mm"]-1))
    expected["dimpling"]=dict(cell_m=CELL,card_cell_m=0.0095,filed_SF={
        "Be S-200F 021 rev1":upstream["Be S-200F"]["intracell_SF"],
        "SR-200 021b":upstream["SR-200"]["intracell_SF"]})

    observed_paths=dict(flatten(owner))
    wanted_paths=dict(flatten(expected))
    excluded={"/elapsed_s":"Owner timing is metadata, not independently remeasured by running foreign code."}
    assert set(observed_paths)-set(wanted_paths)==set(excluded)
    assert not set(wanted_paths)-set(observed_paths)
    for path,value in wanted_paths.items():
        note=""
        atol=1e-12
        category="boolean" if isinstance(value,bool) else "numeric"
        if path.startswith("/dimpling/filed_SF/"):
            atol=0.05 if "S-200F" in path else 0.005
            note="Carried safety factor printed to one or two decimals; raw independent upstream value shown."
            category="rounded_upstream"
        compare("RESULTS"+path,observed_paths[path],value,category,atol,note)

    expected_inputs=dict(
        formula=dict(Q_ideal=0.82,K_factor=0.64,eta=1.0,design_Q=0.33),
        core=dict(density_pcf=1.0,density_kg_m3=PCF,cell_m=CELL,card_cell_m=0.0095,
                  Ec_ksi_typical=15.0,Ec_Pa=EC,Fc_stabilised_typical_psi=60.0,
                  Fc_stabilised_minimum_psi=35.0,Fc_typical_Pa=60*PSI,Fc_minimum_Pa=35*PSI,
                  crush_psi_typical=35.0,crush_Pa=35*PSI,bare_typical_psi=55.0,bare_minimum_psi=25.0),
        faces=[dict(f,dimpling_SF_filed=upstream[f["name"]]["intracell_SF"]) for f in FACES],
        flatness_sources=[
            dict(number_read=False),
            dict(flatness_inch_per_radial_foot=0.008,flatness_mm_per_foot=0.008*25.4,face_inch=0.04),
            dict(flatness_mm_per_radial_metre=0.7),
            dict(wave_mm=1.0,per_60_inch_mm=1.5),
            dict(flatness_inch=0.010,local_step_inch=0.003,local_step_mm=0.003*25.4)])
    observed_inputs=dict(flatten(inputs))
    expected_input_paths=dict(flatten(expected_inputs))
    pin_numeric_paths={path:value for path,value in observed_inputs.items() if path.startswith("/pins/")}
    assert set(observed_inputs)-set(expected_input_paths)==set(pin_numeric_paths)
    for path,value in expected_input_paths.items():
        if path.endswith("dimpling_SF_filed"):
            compare("INPUTS"+path,observed_inputs[path],value,"rounded_upstream",
                    0.05 if "/0/" in path else 0.005,
                    "Rounded inherited safety factor; rederived from full pinned geometry.")
        else:
            compare("INPUTS"+path,observed_inputs[path],value,
                    "source_constant_or_conversion",
                    note="Formula/source constants read independently; geometry specified in the pinned brief.")

    # Independent round trips and scaling checks, corresponding to all owner PASS labels.
    all_rows=expected["amplitudes"]+expected["design_0_33_if_it_were_this_waviness"]
    inverse_error=max(abs(q_at(row["delta_over_tc"],60 if index<4 else 35)-row["Q"])
                      for index,row in enumerate(expected["amplitudes"]))
    design_error=max(abs(q_at(row["delta_over_tc"],60 if index<2 else 35)-row["Q"])
                     for index,row in enumerate(expected["design_0_33_if_it_were_this_waviness"]))
    scale_tc=FACES[1]["tc_m"]/FACES[0]["tc_m"]
    scale_fc=35/60
    verification={
        "inverse_returns_Q":max(inverse_error,design_error)<1e-14,
        "amplitude_scales_with_tc":all(math.isclose(amplitude(FACES[1],q,60)["delta_m"]/amplitude(FACES[0],q,60)["delta_m"],scale_tc,rel_tol=1e-14) for q in (0.371,0.609)),
        "amplitude_scales_with_Fc":all(math.isclose(amplitude(f,q,35)["delta_m"]/amplitude(f,q,60)["delta_m"],scale_fc,rel_tol=1e-14) for f in FACES for q in (0.371,0.609)),
        "perfect_facing_Q_0_82":q_at(0,60)==0.82,
        "biaxial_root_on_cubic":abs(root**3+root-1)<3e-16,
        "Ec_matches_014b_15_ksi":math.isclose(EC,103421359.3975254,rel_tol=1e-14),
        "crush_35_psi_matches_014b_and_is_not_Fc":math.isclose(35*PSI,241316.50526089262,rel_tol=1e-14),
    }
    assert set(verification)==set(owner["checks"])
    for key,passed in verification.items():
        compare("RESULTS/checks/"+key,owner["checks"][key],"PASS" if passed else "FAIL","owner_self_check")

    # Directly parse engineering numbers from the CARD's four amplitude lines.
    card=(ROOT/"inputs/owner-CARD.md").read_text()
    report=load("rpt-mainline032-grok-wrinkle-waviness-1020.json")["body"]
    prose=[]
    lines=[line for line in card.splitlines() if line.startswith(("- Be S-200F core","- SR-200 core"))]
    assert len(lines)==4
    pattern=r"Q ([0-9.]+).*?: delta ([0-9.]+) mm, delta/t_f ([0-9.]+), delta/\(3/8 in\) ([0-9.]+), delta/9.5 mm ([0-9.]+)\."
    for index,line in enumerate(lines):
        matches=re.search(pattern,line)
        assert matches,line
        values=matches.groups()
        expected_row=expected["amplitudes"][index]
        for key,literal in zip(["Q","delta_mm","delta_over_tf","delta_over_cell_3_8_in","delta_over_card_9_5_mm"],values):
            places=len(literal.split(".")[1])
            compare(f"CARD/amplitudes/{index}/{key}",literal,round_decimal(expected_row[key],places),"card_display")
        prose.append(dict(location=f"CARD amplitude line {index}",text=line))

    def prose_check(text,phrase,values,label):
        assert phrase in text,(label,phrase)
        for token,value in values:
            places=len(token.partition(".")[2])
            compare(label+"/"+token,token,round_decimal(value,places),"prose_display")
        prose.append(dict(location=label,text=phrase))

    # Report's leading amplitudes and normalized quantities; the source cases are conditional.
    for index in (0,3):
        row=expected["amplitudes"][index]
        for key in ("delta_mm","delta_over_tf","delta_over_cell_3_8_in"):
            [credential]
            prose_check(report,token,[(token,row[key])],f"REPORT lead {index} {key}")
    for index in (4,7):
        row=expected["amplitudes"][index]
        [credential]
        prose_check(report,token,[(token,row["delta_mm"])],f"REPORT minimum {index}")
    for index in (0,1):
        row=expected["design_0_33_if_it_were_this_waviness"][index]
        [credential]
        prose_check(card,token,[(token,row["delta_mm"])],f"CARD projected design {index}")
    prose_check(card,"0.682327803828",[("0.682327803828",root)],"CARD biaxial root")
    prose_check(report,"0.682327803828",[("0.682327803828",root)],"REPORT biaxial root")
    # Scientific-notation root error is checked at the author's stated significant figures.
    compare("CARD/card_minus_root","-2.78038280193e-05",
            format(0.6823-root,".12g"),"prose_display")
    for value,token in ((0.008*25.4,"0.203"),(0.003*25.4,"0.076")):
        prose_check(card,token+" mm",[(token,value)],"CARD unit conversion")
    prose_check(card,"0.33/0.82 is about 0.40",[("0.40",0.33/0.82)],"CARD design ratio")

    lead_ratios=[expected["amplitudes"][j]["delta_over_cell_3_8_in"] for j in (0,3)]
    all_ratios=[row["delta_over_cell_3_8_in"] for row in expected["amplitudes"][:4]]
    assert "The lead amplitudes are 0.0046 to 0.024" in card
    prose_corrections=[
        dict(id="NFI-032-CHECK-LEAD-RANGE",field="CARD lead amplitude / 9.525 mm cell range",
             reported=[0.0046,0.024],checked=[min(lead_ratios),max(lead_ratios)],
             all_four_typical_rows=[min(all_ratios),max(all_ratios)],
             reason="The reported endpoints round the two cross-Q rows; the lead-specific range uses Q .371 on S-200F and Q .609 on SR-200."),
    ]
    # Inelastic reduction is a sensitivity calculation, not a material calibration.
    inelastic={}
    for face in FACES:
        q=face["lead_Q"]
        inelastic[face["name"]]={
            "minimum_eta_for_target_Q_even_at_zero_waviness":(q/0.82)**2,
            "eta_sensitivity_projection":[
                dict(eta=eta,delta_mm_at_60psi=max(0,(0.82*math.sqrt(eta)/q-1)/0.64)*60/15000*face["tc_m"]*1000,
                     target_possible=0.82*math.sqrt(eta)>=q)
                for eta in (1.0,0.9,0.8,0.6,0.5)]}
    # Owner timings are preserved as an observation, without rerunning foreign code.
    owner_wall=(datetime.fromisoformat(owner["ended"])-datetime.fromisoformat(owner["started"])).total_seconds()
    timing=dict(reported_elapsed_s=owner["elapsed_s"],timestamp_difference_s=owner_wall,
                reported_minus_timestamp_difference_s=owner["elapsed_s"]-owner_wall,
                interpretation="Microsecond wall-clock stamps and an elapsed timer need not coincide. Owner execution duration is not independently verified.")
    pins=[]
    for manifest_name in ("pin-audit.json","brief-pins.json","upstream-pins.json"):
        for item in load(manifest_name):
            path=Path(item["path"])
            data=path.read_bytes()
            digest=hashlib.sha256(data).hexdigest()
            match=digest==item["sha256"] and len(data)==item["bytes"]
            pins.append(dict(path=str(path),sha256=digest,bytes=len(data),match=match))
            assert match,path
    for item in json.loads((ROOT/"sources/manifest.json").read_text()):
        if "path" not in item:
            continue
        data=Path(item["path"]).read_bytes()
        assert hashlib.sha256(data).hexdigest()==item["sha256"] and len(data)==item["bytes"]
    mismatches=[row for row in COMPARISONS if not row["match"]]
    result=dict(schema=1,unit="vacuum-mainline032-check-1020",tag="QUESTIONABLE",certification=False,
                started_at=json.loads((ROOT/"WORK.json").read_text())["started_at"],
                calculated_at=datetime.now(ZoneInfo("America/Vancouver")).isoformat(timespec="seconds"),
                method="Primary equations and independently transcribed source constants; no foreign code read, imported or executed.",
                comparison_counts=dict(Counter(x["category"] for x in COMPARISONS)),
                comparison_total=len(COMPARISONS),mismatches=mismatches,
                owner_results_numeric_coverage=dict(total=len(observed_paths),checked=len(wanted_paths),excluded=excluded),
                owner_inputs_numeric_coverage=dict(total=len(observed_inputs),checked=len(expected_input_paths),
                                                   metadata_pin_lengths_verified=len(pin_numeric_paths)),
                relative_tolerance=3e-12,absolute_tolerance=1e-12,
                rounded_upstream_allowance={"9.0":0.05,"4.98":0.005},
                independent=expected,independent_inputs=expected_inputs,
                upstream_recalculation=upstream,verification=verification,
                root_60_digit_decimal=str(root_decimal),core_amplitude_ratio=scale_tc,
                strength_amplitude_ratio=scale_fc,design_over_ideal=0.33/0.82,
                prose_corrections=prose_corrections,inelastic_projection=inelastic,
                timing_observation=timing,source_pins_match=True,
                foreign_scripts_read_or_executed=False)
    save("RESULTS.json",result)
    save("PROSE-CHECK.json",prose)
    save("SOURCE-PINS.json",pins)
    with (ROOT/"NUMERIC-CHECK.csv").open("w",newline="") as stream:
        writer=csv.DictWriter(stream,fieldnames=list(COMPARISONS[0]))
        writer.writeheader();writer.writerows(COMPARISONS)
    print(json.dumps({key:result[key] for key in ("comparison_counts","comparison_total","mismatches",
                     "owner_results_numeric_coverage","upstream_recalculation","prose_corrections",
                     "root_60_digit_decimal","inelastic_projection")},indent=2))
    assert not mismatches


if __name__=="__main__":
    main()
