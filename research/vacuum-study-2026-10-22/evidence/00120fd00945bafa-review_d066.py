"""REVIEW-D on MAINLINE-066. Own arithmetic.

Does not import or run model61.py, model63.py, or rank.py.
Buckling is COMMON's P2 equation. Wrinkling is equation 2.2-14
as 065 stated it: Q times the square root, with Q = 0.33.
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
P_ISA = 95460.8379139
L10 = 4889.44215019
NU_COMMON = 0.33
NU_BE = 0.0768
E = 293.6e9
EC = 103421359.3975254
RHO_F = 1850.0
RHO_C = 16.018463373960138
Q = 0.33
GAMMA = 0.20
STRENGTH = 379.2e6
FILM = 0.07323641454574575
ALPHA = 77082.7 / 149950.6

OWN066 = Path(
    "unpublished-local-ref:2f846ae958082233"
    "/.ship/work/outputs/vacuum-mainline066-improvement-vector-1020/RESULTS.json"
)
DELTA = Path(
    "unpublished-local-ref:2f846ae958082233"
    "/.ship/work/outputs/vacuum-record-delta-c-1020/RESULTS.json"
)
OWN067 = Path(
    "unpublished-local-ref:4fe47543de57daa1"
    "/.ship/work/outputs/vacuum-mainline067-materials-pathway-1020/RESULTS.json"
)


def margin_buckling(tf, tc, R, nu):
    sep = tc + tf
    den = math.sqrt(1.0 - nu * nu)
    p_allow = GAMMA * 4.0 * tf * sep * E / (R * R * den)
    return p_allow / P_ISA, p_allow


def margin_wrinkling(tf, tc, R):
    sigma = Q * math.sqrt(EC * E * tf / tc)
    p_allow = 4.0 * sigma * tf / R
    return p_allow / P_ISA, p_allow


def margin_yield(tf, R):
    p_allow = 4.0 * STRENGTH * tf / R
    return p_allow / P_ISA, p_allow


def main():
    src = json.loads(OWN066.read_text())
    delta = json.loads(DELTA.read_text())
    mat = json.loads(OWN067.read_text())
    handbook = {
        (row["R_m"], row["weather"]): row
        for row in delta["rows"]
        if row["law"] == "handbook"
    }

    rows = []
    max_diff = 0.0
    for name, row in src["base"]["rows"].items():
        level, radius, weather = name.split(":")
        R = float(radius)
        tf = row["point"]["geometry"]["tf_m"]
        tc = row["point"]["geometry"]["tc_m"]
        area = 4.0 * math.pi * R * R
        faces = 2.0 * tf * RHO_F * area
        core = tc * RHO_C * area
        two_films = 2.0 * FILM * area
        lift = L10 * (R / 10.0) ** 3
        payload = (
            row["point"]["lift_kg"]
            - row["point"]["mass_before_growth_kg"]
            - row["point"]["growth_total_kg"]
        )
        bill = (
            row["point"]["bill_faces_kg"]
            + row["point"]["bill_core_kg"]
            + row["point"]["bill_joining_kg"]
        )
        drow = handbook[(int(radius), weather)]
        theirs = row["point"]["payload_kg"]
        ref = drow["recomputed_concept_kg" if level == "concept" else "recomputed_TRL7_kg"]
        diff = theirs - ref
        max_diff = max(max_diff, abs(diff))
        b33, pb33 = margin_buckling(tf, tc, R, NU_COMMON)
        bbe, _ = margin_buckling(tf, tc, R, NU_BE)
        w, pw = margin_wrinkling(tf, tc, R)
        y, py = margin_yield(tf, R)
        rows.append({
            "case": name,
            "lift_independent_kg": lift,
            "lift_reported_kg": row["point"]["lift_kg"],
            "lift_difference_kg": lift - row["point"]["lift_kg"],
            "payload_identity_difference_kg": payload - theirs,
            "faces_independent_kg": faces,
            "faces_reported_kg": row["point"]["bill_faces_kg"],
            "faces_difference_kg": faces - row["point"]["bill_faces_kg"],
            "core_independent_kg": core,
            "core_reported_kg": row["point"]["bill_core_kg"],
            "core_difference_kg": core - row["point"]["bill_core_kg"],
            "two_films_kg": two_films,
            "joining_reported_kg": row["point"]["bill_joining_kg"],
            "mass_above_bill_kg": row["point"]["mass_before_growth_kg"] - bill,
            "delta_c_payload_kg": ref,
            "reported_payload_kg": theirs,
            "payload_minus_delta_c_kg": diff,
            "buckling_margin_nu_0.33": b33,
            "buckling_margin_nu_0.0768": bbe,
            "wrinkling_margin": w,
            "yield_margin": y,
            "reported_binding": row["point"]["binding"],
            "card_margin": 1.0,
        })

    arith = []
    for row in src["density_only"]:
        arith.append({
            "case": row["case"],
            "ln_factor": math.log(row["factor"]),
            "reported_l1": row["l1"],
            "density_1850_over_factor": 1850.0 / row["factor"],
            "reported_density": row["density_kg_m3"],
        })
    modulus = []
    for row in src["modulus_closure"]:
        modulus.append({
            "case": row["case"],
            "ln_factor": math.log(row["factor"]),
            "reported_l1": row["l1"],
            "E_GPa": 293.6 * row["factor"],
            "reported_E_GPa": row["E_GPa"],
        })
    gamma = {
        key: (None if factor is None else 0.2 * factor)
        for key, factor in src["gamma_alone"].items()
    }

    ranking = []
    for face in mat["faces"]:
        if not face.get("E_Pa"):
            continue
        ratio = (RHO_F / face["density_kg_m3"]) * (face["E_Pa"] / E) ** ALPHA
        ranking.append({
            "id": face["id"],
            "index_rho_over_E_to_0.514": ratio,
            "membrane": face["id"] in mat["face_rank"]["membrane_ids"],
            "specific_modulus_over_beryllium_in_067": face.get("specific_modulus_over_beryllium"),
            "wrinkling_improvement_in_067": face.get("wrinkling_index_improvement_over_beryllium"),
        })
    ranking.sort(key=lambda item: item["index_rho_over_E_to_0.514"], reverse=True)

    out = {
        "unit": "vacuum-review-d-066-1020",
        "tag": "QUESTIONABLE",
        "qualified_hull_SF": None,
        "started": "2026-10-20T18:11:10-07:00",
        "simjob": None,
        "why_no_simjob": "Spot checks of the load-bearing rows. One core, seconds. The owner's model was not run.",
        "route": {
            "buckling": "p = 0.20 * 4 * tf * (tc + tf) * E / (R^2 * sqrt(1 - nu^2))",
            "nu_common": NU_COMMON,
            "wrinkling": "sigma = 0.33 * sqrt(Ec * E * tf / tc); p = 4 * sigma * tf / R",
            "wrinkling_source": "065's statement of NASA CR-1457 equation 2.2-14, Q = 0.33",
            "yield": "p = 4 * strength * tf / R",
            "applied_pressure_Pa": P_ISA,
            "index": "rho / E^0.514, with 0.514 = 77082.7 / 149950.6",
            "owner_code": "not read and not run",
        },
        "payload_match_max_abs_kg": max_diff,
        "rows": rows,
        "arithmetic": {
            "density_only": arith,
            "modulus_closure": modulus,
            "realized_gamma_0.20_times_factor": gamma,
            "modulus_to_density_ratio": ALPHA,
        },
        "join_ranking_high_better": ranking,
        "fixes": [
            {
                "id": "FIX-D066-BUCKLING",
                "case": "four concept geometries",
                "field": "global_buckling margin",
                "card": 1.0,
                "independent_nu_0.33": "1.63, 1.69, 1.63, 1.69 in case order",
            },
            {
                "id": "FIX-D066-WRINKLING",
                "case": "four concept geometries",
                "field": "face_wrinkling margin",
                "card": 1.0,
                "independent": "1.06, 1.09, 1.07, 1.10 in case order",
            },
            {
                "id": "FIX-D066-JOIN",
                "case": "concept R 30 ISA index",
                "field": "067 ranking under rho/E^0.514",
                "card": "067's wrinkling order, diamond at 0.81",
                "independent": "diamond 1.013, CNT yarn 1.421, M60J 1.254, programme SR-200 0.994",
            },
        ],
    }
    (ROOT / "RESULTS.json").write_text(json.dumps(out, indent=2) + "\n")
    print("max_diff", max_diff)
    for row in rows:
        if row["case"].startswith("concept"):
            print(
                row["case"],
                "buck33", round(row["buckling_margin_nu_0.33"], 4),
                "buckBe", round(row["buckling_margin_nu_0.0768"], 4),
                "wr", round(row["wrinkling_margin"], 4),
                "y", round(row["yield_margin"], 4),
                "films", round(row["two_films_kg"], 1),
                "join", round(row["joining_reported_kg"], 1),
                "above", round(row["mass_above_bill_kg"], 1),
                "dPay", row["payload_minus_delta_c_kg"],
            )
    print("rank")
    for item in ranking:
        print(item["id"], round(item["index_rho_over_E_to_0.514"], 4), "membrane", item["membrane"])


if __name__ == "__main__":
    main()
