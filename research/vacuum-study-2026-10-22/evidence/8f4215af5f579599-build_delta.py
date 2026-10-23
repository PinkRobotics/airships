"""Write DELTA-D-1020.json. Does not touch the claim record."""
import hashlib
import json
from datetime import datetime
from pathlib import Path

UNIT = Path("unpublished-local-ref:2efb64cc99fc234f")
SEAT066 = Path("unpublished-local-ref:3c3be43fc6ac07a9")
RECORD = UNIT / "record" / "CLAIM-RECORD.json"
RUN = json.loads((UNIT / "RUN.json").read_text())
REV066 = json.loads((UNIT.parent / "vacuum-review-d-066-1020" / "RESULTS.json").read_text())
REV067 = json.loads((SEAT066 / "vacuum-review-d-067-1020" / "RESULTS.json").read_text())
NFI066R = json.loads((UNIT.parent / "vacuum-review-d-066-1020" / "NFI.json").read_text())
NFI067R = json.loads((SEAT066 / "vacuum-review-d-067-1020" / "NFI.json").read_text())
NFI066 = json.loads((SEAT066 / "vacuum-mainline066-improvement-vector-1020" / "NFI.json").read_text())

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


def source(report, key, selector=""):
    path = PATHS[key]
    raw = path.read_bytes()
    return {
        "report": report,
        "artifact": str(path),
        "snapshot": str(path),
        "sha256": hashlib.sha256(raw).hexdigest(),
        "bytes": len(raw),
        "selector": selector,
    }


OPEN = "No installed hull safety factor is released. QUESTIONABLE inputs. PROJECTION targets."


def finding(fid, claim, status, sources, qualification=None):
    return {
        "id": fid,
        "kind": "piece_d",
        "claim": claim,
        "numerical_status": status,
        "physical_qualification": "open",
        "qualification": qualification or OPEN,
        "tag": "QUESTIONABLE / PROJECTION",
        "sources": sources,
    }


def change(fid, label, claim, report, sources):
    return {"id": fid, "kind": "filed_change", "label": label, "claim": claim,
            "report": report, "sources": sources}


def nfi(fid, report, key, pointer, row_id, statement):
    src = source(report, key, pointer)
    return {
        "uid": fid,
        "report": report,
        "file": src["artifact"],
        "snapshot": src["snapshot"],
        "source_sha256": src["sha256"],
        "source_json_pointer": pointer,
        "row_id": row_id,
        "fields": {"id": row_id, "status": "open", "statement": statement},
        "register_classification": "QUESTIONABLE / PROJECTION",
    }


def rows(variant, maturity):
    return [row for row in variant["rows"] if row["case"].startswith(maturity + ":")]


def pack(seq, key):
    return ", ".join(f"{row[key]:.6f}" for row in seq)


def main():
    record = json.loads(RECORD.read_text())
    if record["version"] != 7:
        raise SystemExit(f"version {record['version']}")
    if record["register"]["rows"][-1]["rid"] != "R120":
        raise SystemExit(record["register"]["rows"][-1]["rid"])
    variants = {item["id"]: item for item in RUN["variants"]}
    for item in variants.values():
        if not all(row["admissible_line"] for row in item["rows"]):
            raise SystemExit(f"left the admissible line: {item['id']}")
    margins = RUN["fixed_geometry_margins"]
    review_rows = [row for row in REV066["rows"] if row["case"].startswith("concept:")]
    if [row["case"] for row in review_rows] != [row["case"] for row in margins]:
        raise SystemExit("case order")
    buck33 = ", ".join(f"{row['buckling_margin_nu_0.33']:.4f}" for row in review_rows)
    bucknu = ", ".join(f"{row['buckling_margin_nu_0.0768']:.4f}" for row in review_rows)
    wr = ", ".join(f"{row['wrinkling_margin']:.4f}" for row in review_rows)
    common = ", ".join(f"{row['buckling_common_nu_P0']:.4f}" for row in margins)
    for a, b in zip(review_rows, margins):
        if abs(a["buckling_margin_nu_0.33"] - b["buckling_common_nu_P0"]) > 5e-5:
            raise SystemExit("common buckling mismatch")
        if abs(a["wrinkling_margin"] - b["wrinkling_P0_sigp_only"]) > 5e-5:
            raise SystemExit("wrinkling mismatch")
    kc = ", ".join(f"{row['kc']:.4f}" for row in margins)
    no_kc_cure = ", ".join(f"{row['buckling_model_p_no_kc_cure']:.4f}" for row in margins)
    kc_only = ", ".join(f"{row['buckling_model_p_kc_no_cure']:.4f}" for row in margins)
    wr_p = ", ".join(f"{row['wrinkling_model_p_sigp_only']:.4f}" for row in margins)
    share = ", ".join(f"{100 * row['thermal_share_of_demand']:.2f}%" for row in margins)
    index_note = REV066["fixes"][-1]["independent"]
    blend = {row["id"]: row["blend_improvement"] for row in REV067["blend_rank"]}
    direct = next(row["fact"] for row in NFI066["open"] if row["id"] == "NFI-066-DIRECT-FOLLOWUP")
    nfi_facts = {row["id"]: row["fact"] for row in NFI066R["rows"]}
    nfi_facts.update({row["id"]: row["fact"] for row in NFI067R["open"]})

    def both(name):
        concept = rows(variants[name], "concept")
        trl = rows(variants[name], "TRL7")
        return (f"concept {pack(concept, 'recomputed_factor')} beside filed {pack(concept, 'filed_066_factor')}; "
                f"TRL7 {pack(trl, 'recomputed_factor')} beside filed {pack(trl, 'filed_066_factor')}")

    control = rows(variants["control"], "concept")
    offset = max(abs(row["recomputed_factor"] - row["filed_066_factor"])
                 for item in variants["control"]["rows"] for row in [item])
    witness = rows(variants["no_kc"], "concept")[1]
    terms = (
        "At 066's four concept optima the model global-buckling and face-wrinkling margins are 1. "
        f"REVIEW-D's COMMON buckling margins at nu 0.33 are {buck33}. This piece's same formula gives {common}. "
        f"Equation 2.2-14 over P0 gives {wr}. "
        f"The buckling gap is kc = 1 - vc/4 while vc is below 2. kc is {kc}. "
        "It is set at model61.py line 106 and model63.py line 113 and multiplies the buckling allowable at "
        "model61.py line 120 and model63.py line 127. "
        f"With kc removed and cure kept, those margins are {no_kc_cure}. "
        f"With kc kept and cure removed, they are {kc_only}. Cure then brings that last step to 1. "
        "Cure is kb*12.3e-6*dtc*tc/(2*tf) at model61.py line 116 and model63.py line 123, and it sits in the buckling denominator. "
        "The wrinkling gap is the pressure adder plus thermal demand. Pressure is P0*max(1.01, QWEATHER)+QWIND "
        "at model61.py line 99 and model63.py line 106. QWIND and QWEATHER are model63.py lines 21-23, with no handbook citation in the file. "
        f"Wrinkling on membrane stress alone at that pressure is {wr_p}. "
        f"grad, bend and cure are {share} of demand and bring the margin to 1. "
        "grad and bend are model61.py lines 110-111 and model63.py lines 117-118, using 11.3e-6. "
        "nu 0.0768 stands as 040's historical SR-200 nu12 scalar proxy. It accounts for the move from the nu 0.33 margins "
        f"{buck33} to the model-nu margins {bucknu}, and it does not bring either set to 1. "
        "Gamma 0.20 and Q 0.33 stand, from CR-1457 as COMMON and knockdown.md state them, with the named hemisphere and waviness limits. "
        "kc, the cure coefficients, 11.3e-6, the 1.01 floor, QWIND and QWEATHER have no equation in the opened model text, "
        "the SOURCE-INDEX bodies, knockdown.md, or COMMON.md. The 040 case source string names pinned 014b. That pin is not in the SOURCE-INDEX and was not opened. "
        "Those four unsourced terms are removed one at a time. BETA stays 1. Vc itself is not replaced."
    )
    fixes = {
        "PD-FIX-D066-BUCKLING": (
            "buckling",
            "UNREVIEWED. FIX-D066-BUCKLING. The filed card stores both margins at 1. "
            f"The review half gives COMMON buckling {buck33} at nu 0.33 and {bucknu} at nu 0.0768, "
            "in the order concept R20 ISA, R20 optimistic, R30 ISA, R30 optimistic. "
            "This piece's fixed-geometry check matches the nu 0.33 column. The margin of 1 does not reproduce on that route."
        ),
        "PD-FIX-D066-WRINKLING": (
            "wrinkling",
            "UNREVIEWED. FIX-D066-WRINKLING. Equation 2.2-14 as 065 states it, over P0, gives "
            f"{wr} at the four concept optima. The model margin is 1. BETA is already 1 on this run, so BETA does not make this gap."
        ),
        "PD-FIX-D066-JOIN": (
            "join-index",
            "UNREVIEWED. FIX-D066-JOIN. The concept R30 ISA slope ratio 77082.7/149950.6 is "
            f"{77082.7 / 149950.6:.6f}. Under density over modulus to that power, against 066's 293.6 GPa and 1850 kg/m3 base, "
            f"the review's independent rank is {index_note}. None of those clears 1.74 or TRL7's 1.61. "
            "067's wrinkling order does not hold on this index. Among quasi-isotropic sheets the SR-200 class still leads."
        ),
    }
    removed = {
        "PD066-NO-KC": ("no-kc", "no_kc", "kc set to 1"),
        "PD066-NO-CURE": ("no-cure", "no_cure", "cure set to 0"),
        "PD066-NO-THERMAL": ("no-thermal", "no_grad_bend", "grad and bend set to 0"),
        "PD066-NO-PRESSURE": ("no-pressure", "no_pressure_augmentation",
                              "pressure set to P0, removing the 1.01 floor, QWEATHER and QWIND"),
    }
    vector = (
        "066's admissible improvement vector is face density only, at gamma 0.20 and Q 0.33 with BETA 1, "
        "on 293.6 GPa, 379.2 MPa and the favorable film. "
        f"Filed concept factors {pack(rows(variants['control'], 'concept'), 'filed_066_factor')} "
        "and filed TRL7 factors "
        f"{pack(rows(variants['control'], 'TRL7'), 'filed_066_factor')}, "
        "order R20 ISA, R20 optimistic, R30 ISA, R30 optimistic. "
        "The joint witnesses are concept 1.862738 at 993.162 kg/m3 and TRL7 1.614325 at 1145.990 kg/m3, both set by R20 optimistic. "
        "Sciences admitted 066 conditionally. Density-only is the best mix found under the stated L1 norm and the tested pairs, "
        "not a proven global minimum. PROBE corrects RUN's modulus-failure labels. "
        "The direct-Python follow-ups are an execution exception and stay apart from this numerical status. "
        "The stored margin of 1 does not reproduce on the independent route."
    )
    base = (
        "UNREVIEWED. The density factors that match the DELTA-C handbook targets are 066's run at 293.6 GPa and 379.2 MPa "
        "with the favorable film. 067 normalizes its material table to 290 GPa and 345 MPa. The two bases are not the same comparison."
    )
    rank = (
        "UNREVIEWED. On 067's membrane table the SAE minimum is above programme SR-200. "
        f"Under density over modulus to the 0.514, the review's improvements are cnt-yarn-ud {blend['cnt-yarn-ud']:.4f}, "
        f"m60j-ud {blend['m60j-ud']:.4f}, cvd-diamond {blend['cvd-diamond']:.4f}, "
        f"sr200-sae-minimum {blend['sr200-sae-minimum']:.4f}, and sr200-programme 1. "
        "None clears the concept factor 1.74 to 1.86. The disks page says up to 120 mm. "
        f"At 120 mm, R20 needs {REV067['diamond_disks_R20']['at_120_mm']:,.0f} disks. Diamond is not a hull face."
    )
    meet = (
        "No 067 candidate in a hull-face product form meets 066's filed density vector at gamma 0.20 and Q 0.33. "
        "T3 and T7 stay on SR-200 bonded to CR-III 5056 3/8-1.0. UD coupons are the wrong form. "
        f"The unreviewed removal of kc still leaves a concept R20 optimistic factor of {witness['recomputed_factor']:.6f} "
        f"({witness['recomputed_density_kg_m3']:.3f} kg/m3). Nothing was bought."
    )
    state = (
        "Programme state, UNREVIEWED as a restatement. Today's admissible line is gamma 0.20 and Q 0.33. "
        "The improvement vector is 066's density-only joint witness, concept 1.862738 and TRL7 1.614325, "
        "with Sciences' limit that the L1 search is not a global-minimum proof. "
        "No real hull-face sheet in 067 meets that vector. "
        "Of the unsourced terms, kc moves the concept R20 optimistic witness the most. "
        "Cure, the grad and bend stress, and the pressure adder move it less, and every recomputed row stays at gamma 0.20 with Vc below 2. "
        "T3 has to measure wrinkling of this coupon before any Q above 0.33. "
        "T7 has to measure this sandwich shell before any gamma above 0.20. "
        "A sourced equation for kc, cure, the thermal stress, or the pressure adder would let that term stand."
    )
    control_claim = (
        f"The DELTA-C face-density search, repeated here with no term removed, matches 066's filed factors within {offset:.6f}. "
        f"Concept {pack(control, 'recomputed_factor')} beside filed {pack(control, 'filed_066_factor')}. "
        "Gamma stays 0.20 and Vc stays below 2. This is the method check for the four removals. It is not a new physical result."
    )
    run_src = [source(ORDER, "run", "/variants"), source(ORDER, "script", "")]
    term_src = [
        source(ORDER, "m61", "L21,L99,L106,L110,L111,L116,L120,L123"),
        source(ORDER, "m63", "L21,L23,L106,L113,L117,L118,L123,L127,L130"),
        source(ORDER, "run", "/fixed_geometry_margins"),
        source(ORDER, "inputs040", "/face/nu_basis"),
        source(ORDER, "knock", ""),
        source(ORDER, "common", ""),
        source(ORDER, "index", ""),
        source("rpt-ref-2684c4730353c185b7d6", "rev066", "/rows"),
    ]
    findings = [
        finding("PD066-TERMS", terms, "unreviewed", term_src),
        finding("PD066-CONTROL", control_claim, "reproduced", run_src,
                OPEN + " The offset is the SLSQP witness in 066 against this binary search."),
    ]
    changes = [
        change("PD066-TERMS", "margin-terms", terms, ORDER, term_src),
        change("PD066-CONTROL", "search-check", control_claim, ORDER, run_src),
    ]
    for fid, (label, text) in fixes.items():
        srcs = [source("rpt-ref-2684c4730353c185b7d6", "rev066", "/fixes"),
                source(ORDER, "run", "/fixed_geometry_margins")]
        findings.append(finding(fid, text, "unreviewed", srcs))
        changes.append(change(fid, label, text, "rpt-ref-2684c4730353c185b7d6", srcs))
    for fid, (label, name, what) in removed.items():
        text = (f"UNREVIEWED. Face-density factors with {what}. Gamma 0.20, Q 0.33, BETA 1, Vc below 2. "
                f"{both(name)}. simjob-20261020t183403-e1930b66c51e exited 0.")
        findings.append(finding(fid, text, "unreviewed", run_src))
        changes.append(change(fid, label, text, ORDER, run_src))
    vector_src = [
        source("rpt-ref-b1e4952922b441a54267", "r066", "/density_only"),
        source("rpt-sciences-g6-mainline066-admission-limits-1020", "adm", "/body"),
        source("rpt-ref-2684c4730353c185b7d6", "rev066", "/payload_match_max_abs_kg"),
    ]
    findings.append(finding(
        "PD066-VECTOR", vector, "reproduced", vector_src,
        OPEN + " Sciences' three limits sit beside this status. Shared-model reproduction is not an independent derivation. "
        + direct))
    changes.append(change("PD066-VECTOR", "066-vector", vector,
                           "rpt-ref-b1e4952922b441a54267", vector_src))
    base_src = [source("rpt-ref-ffca8829d86cfae49814", "rev067", "/fixes"),
                source("rpt-ref-b1e4952922b441a54267", "r066", "/base")]
    findings.append(finding("PD-FIX-D067-BASE", base, "unreviewed", base_src))
    changes.append(change("PD-FIX-D067-BASE", "two-bases", base, "rpt-ref-ffca8829d86cfae49814", base_src))
    rank_src = [source("rpt-ref-ffca8829d86cfae49814", "rev067", "/blend_rank")]
    findings.append(finding("PD-FIX-D067-RANK", rank, "unreviewed", rank_src))
    changes.append(change("PD-FIX-D067-RANK", "067-rank", rank, "rpt-ref-ffca8829d86cfae49814", rank_src))
    meet_src = [source("rpt-ref-3b692c8042e522b38b95", "r067", ""),
                source(ORDER, "run", "/variants")]
    findings.append(finding("PD067-MEET", meet, "unreviewed", meet_src))
    changes.append(change("PD067-MEET", "materials", meet, ORDER, meet_src))
    state_src = [source(ORDER, "run", "/variants"),
                 source("rpt-sciences-g6-mainline066-admission-limits-1020", "adm", "/body")]
    findings.append(finding("PD-STATE", state, "unreviewed", state_src))
    changes.append(change("PD-STATE", "programme-state", state, ORDER, state_src))

    carried = [
        ("PD-NFI-PAIRS", "NFI-D066-PAIRS", "rev066n", "rpt-ref-2684c4730353c185b7d6"),
        ("PD-NFI-MODULUS-CAPS", "NFI-D066-MODULUS-CAPS", "rev066n", "rpt-ref-2684c4730353c185b7d6"),
        ("PD-NFI-OPTIMISTIC", "NFI-D066-OPTIMISTIC", "rev066n", "rpt-ref-2684c4730353c185b7d6"),
        ("PD-NFI-VC", "NFI-D066-VC", "rev066n", "rpt-ref-2684c4730353c185b7d6"),
        ("PD-NFI-ABOVE-BILL", "NFI-D066-ABOVE-BILL", "rev066n", "rpt-ref-2684c4730353c185b7d6"),
        ("PD-NFI-SHARED", "NFI-D066-SHARED-MODEL", "rev066n", "rpt-ref-2684c4730353c185b7d6"),
        ("PD-NFI-UNOPENED", "NFI-D-UNOPENED-SOURCES", "rev067n", "rpt-ref-ffca8829d86cfae49814"),
        ("PD-NFI-SAE-YIELD", "NFI-D-SAE-YIELD", "rev067n", "rpt-ref-ffca8829d86cfae49814"),
        ("PD-NFI-DIAMOND", "NFI-D-DIAMOND-BOOKLET", "rev067n", "rpt-ref-ffca8829d86cfae49814"),
        ("PD-NFI-BLEND", "NFI-D-BLEND-IS-LOCAL", "rev067n", "rpt-ref-ffca8829d86cfae49814"),
    ]
    nfi_rows = []
    for fid, old, key, report in carried:
        text = f"Carried, not demonstrated again. {old}: {nfi_facts[old]}"
        findings.append(finding(fid, text, "unreviewed", [source(report, key, "")]))
        nfi_rows.append(nfi(fid, report, key, "", old, text))
    limits = (
        "Sciences admitted 066 conditionally, and no 067 admission has been filed. "
        "Density-only is the best mix found under the stated L1 norm and the tested pairs, not a proven global minimum. "
        "PROBE corrects RUN's modulus-failure labels. Bracket artifacts are not mix improvements, and optimizer nulls do not prove physical impossibility. "
        "The direct-Python follow-ups are an execution exception kept apart from numerical status."
    )
    findings.append(finding("PD-NFI-LIMITS", limits, "unreviewed",
                            [source("rpt-sciences-g6-mainline066-admission-limits-1020", "adm", "/body")]))
    nfi_rows.append(nfi("PD-NFI-LIMITS", "rpt-sciences-g6-mainline066-admission-limits-1020",
                        "adm", "/body", "NFI-D-066-LIMITS", limits))
    direct_claim = "Carried apart from numerical status. " + direct
    findings.append(finding("PD-NFI-DIRECT", direct_claim, "unreviewed",
                            [source("rpt-ref-b1e4952922b441a54267", "n066", "")]))
    nfi_rows.append(nfi("PD-NFI-DIRECT", "rpt-ref-b1e4952922b441a54267",
                        "n066", "", "NFI-066-DIRECT-FOLLOWUP", direct_claim))
    pin = ("The 040 case source string names pinned 014b and pinned 016 for the block that holds the 1.01 pressure floor. "
           "014b is not in the model's SOURCE-INDEX and was not opened. COMMON.md states neither the 1.01 floor nor the wind formula. "
           "The pressure-augmentation recompute is the consequence of that open pin, not a finding that the floor is false.")
    findings.append(finding("PD-NFI-014B", pin, "unreviewed",
                            [source(ORDER, "inputs040", "/case/source"), source(ORDER, "common", "")]))
    nfi_rows.append(nfi("PD-NFI-014B", ORDER, "inputs040", "/case/source", "NFI-D-014B-UNOPENED", pin))

    known = {item["id"] for item in record["findings"]}
    new_ids = [item["id"] for item in findings]
    if len(new_ids) != len(set(new_ids)) or known & set(new_ids):
        raise SystemExit("finding id collision")
    if len(nfi_rows) != len({row["uid"] for row in nfi_rows}):
        raise SystemExit("nfi uid collision")
    register = {
        "rid": "R121",
        "topic": "Piece D",
        "topic_name": "Margin terms, the density vector, and the materials that meet it",
        "gap": "Which model term makes the margin of 1, and whether a real face meets the density vector",
        "unknown": "The four removed-term recomputes are unreviewed. Pin 014b was not opened. No 067 admission is filed.",
        "today": [item["claim"] for item in changes],
        "needed": [
            "Leave the removed-term rows unreviewed until a later piece.",
            "A sourced equation would let kc, cure, the thermal stress, or the pressure adder stand.",
            "T3 for an installed Q and T7 for an installed gamma on SR-200 bonded to CR-III.",
        ],
        "owners": [
            "rpt-ref-b1e4952922b441a54267",
            "rpt-ref-3b692c8042e522b38b95",
            "rpt-ref-2684c4730353c185b7d6",
            "rpt-ref-ffca8829d86cfae49814",
            "rpt-sciences-g6-mainline066-admission-limits-1020",
        ],
        "states": ["QUESTIONABLE", "PROJECTION"],
        "directions": [
            "Carry gamma 0.20 and Q 0.33. The filed density vector stands beside the unreviewed removals. No hull-face candidate meets it."
        ],
        "check_outcome": "Margin terms named. Four unsourced terms recomputed unreviewed on the admissible line. Sciences' 066 limits carried. No qualified hull safety factor.",
        "sources": [],
        "finding_ids": new_ids,
    }
    delta = {
        "id": "DELTA-D-1020",
        "expected_version": 7,
        "at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "meaning": "Append Piece D, 066, 067, both review halves, the 066 admission, and the unreviewed removals of kc, cure, thermal stress and the pressure adder. Do not rebuild version 7.",
        "append_findings": findings,
        "append_changes": changes,
        "append_register_rows": [register],
        "append_nfi_rows": nfi_rows,
        "append_grounding_routes": [{
            "id": "PD-T3-T7",
            "statement": "T3 still has to measure elastic wrinkling of this SR-200 / CR-III coupon before any Q above 0.33. T7 still has to measure this sandwich shell before any gamma above 0.20.",
            "status": "open",
        }],
    }
    dest = UNIT / "DELTA-D-1020.json"
    dest.write_text(json.dumps(delta, indent=2, ensure_ascii=False) + "\n")
    print(f"findings {len(findings)} changes {len(changes)} nfi {len(nfi_rows)}")
    print(f"wrote {dest}")


if __name__ == "__main__":
    main()
