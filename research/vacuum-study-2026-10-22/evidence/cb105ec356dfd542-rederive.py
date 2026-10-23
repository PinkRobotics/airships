#!/usr/bin/env python3
"""MAINLINE-009b. Restate the filed P2 point with K_c at every knockdown.

Geometry, materials and the moderate branch stay where MAINLINE-009 left them.
This script does not search thicknesses and does not score the P3 frame.
"""
from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STARTED = datetime.now().astimezone().isoformat(timespec="seconds")

SEAT = Path("unpublished-local-ref:7a5bf1cec24b249e")
OURS = SEAT / "ref-1a533823b6613bf7ff73/.ship/work/outputs"
R009 = OURS / "vacuum-mainline009-combined-point-1019/RESULTS.json"
WRINKLE = OURS / "vacuum-mainline009-combined-point-1019/WRINKLE-COLUMN.json"
P3 = OURS / "vacuum-mainline009-combined-point-1019/P3-PENDING.json"
R007 = OURS / "vacuum-mainline007-core-trade-1019/RESULTS.json"
R008 = (
    SEAT
    / "ref-454ea8a33cb537f77738/.ship/work/outputs"
    / "vacuum-mainline008-material-gap-1019/RESULTS.json"
)

KD_MAIN = 0.20
KD_PRECISION = 0.90
KD_CONSERVATIVE = 0.1407
NU = 0.33


def sha256(path: Path) -> tuple[str, int]:
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest(), len(data)


def load(path: Path) -> dict:
    return json.loads(path.read_text())


def assert_close(name: str, got: float, expect: float, rel: float = 1e-12) -> None:
    scale = max(abs(expect), 1e-30)
    err = abs(got - expect) / scale
    if err > rel:
        raise SystemExit(f"{name} rel {err:.3e}: got {got!r} expect {expect!r}")


def g(x: float) -> str:
    return format(float(x), ".12g")


def biaxial_factor() -> float:
    lo, hi = 0.0, 1.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if mid**3 + mid > 1.0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def k_and_gamma(vc: float) -> tuple[float, float, str]:
    if vc <= 2.0:
        return 1.0 - vc / 4.0, 0.20, "stiff_or_moderate_core"
    return 1.0 / vc, 1.0, "shear_crimping"


def main() -> None:
    filed = load(R009)
    prior = load(R007)
    faces = load(R008)
    wrinkle = load(WRINKLE)
    pending = load(P3)

    p_ext = prior["atmosphere"]["p_ext_Pa"]
    radius = prior["atmosphere"]["R_m"]
    nu = prior["inherited"]["nu"]
    if nu != NU or radius != 10.0:
        raise SystemExit("case constants moved")
    sic = next(
        row for row in faces["candidates_ranked_by_least_SF_P2E"]
        if row["name"].startswith("SiC")
    )
    divinycell = next(m for m in prior["materials"] if m["name"] == "Divinycell H35")
    hexcel = next(m for m in prior["materials"] if m["name"] == "Hexcel HRH-10-4.8-32")
    hex_row = next(
        row for row in filed["sic_cores_ranked"]
        if row["core"] == "Hexcel HRH-10-4.8-32"
    )

    tf = filed["geometry"]["tf_m"]
    tc = filed["geometry"]["core_m"]
    h = tc + tf
    E = sic["E_GPa"] * 1e9
    sigma = sic["sigma_c_MPa"] * 1e6
    gc = divinycell["Gc_used_for_compare_Pa"]
    ec = divinycell["Ec_Pa"]
    crush = divinycell["compressive_strength_Pa"]
    root = math.sqrt(1.0 - nu * nu)

    sigma_0 = E * h / (radius * root)
    sigma_crimp = h * h * gc / (2.0 * tf * tc)
    vc = sigma_0 / sigma_crimp
    kc, gamma, branch = k_and_gamma(vc)
    if branch != "stiff_or_moderate_core" or gamma != 0.20:
        raise SystemExit("the filed point left the moderate branch")

    def classical(kd: float) -> float:
        return (kd * 4.0 * tf * h * E / (radius * radius * root)) / p_ext

    # Handbook pressure is gamma_d * Kc * (4*tf/R) * sigma_0.
    # On this branch gamma_d is 0.20, so at kd=0.20 the ratio to classical is Kc.
    # Kc does not contain kd, so the same Kc multiplies every classical level.
    stated = {kd: kc * classical(kd) for kd in (KD_MAIN, KD_PRECISION, KD_CONSERVATIVE)}
    handbook_020 = gamma * kc * (4.0 * sigma_0 * tf / radius) / p_ext

    assert_close("Vc", vc, filed["handbook"]["Vc"])
    assert_close("Kc", kc, filed["handbook"]["Kc"])
    assert_close("classical 0.20", classical(KD_MAIN), filed["handbook"]["SF_classical_0_20"])
    assert_close("handbook 0.20", handbook_020, filed["handbook"]["SF_general"])
    assert_close("stated 0.20", stated[KD_MAIN], handbook_020)
    assert_close("Kc identity", handbook_020 / classical(KD_MAIN), kc)
    assert_close(
        "0.1407/0.90",
        classical(KD_CONSERVATIVE) / classical(KD_PRECISION),
        KD_CONSERVATIVE / KD_PRECISION,
    )
    assert_close("omitted 0.90", classical(KD_PRECISION), filed["modes_precision_kd_0_90"]["global_buckling"])
    assert_close(
        "omitted 0.1407",
        classical(KD_CONSERVATIVE),
        filed["modes_conservative_kd_0_1407"]["global_buckling"],
    )
    if round(stated[KD_PRECISION], 3) != 1.058:
        raise SystemExit(f"0.90 product does not round to 1.058: {stated[KD_PRECISION]}")
    if round(stated[KD_CONSERVATIVE], 3) != 0.165:
        raise SystemExit(f"0.1407 product does not round to 0.165: {stated[KD_CONSERVATIVE]}")
    if not (stated[KD_CONSERVATIVE] < stated[KD_MAIN] < stated[KD_PRECISION]):
        raise SystemExit("restated column is not linear in knockdown")

    membrane = p_ext * radius / (4.0 * tf)
    face = (4.0 * sigma * tf / radius) / p_ext
    crush_sf = crush / (p_ext / 2.0)
    crimp_sf = (4.0 * sigma_crimp * tf / radius) / p_ext
    bx = biaxial_factor()
    uni_design = 0.50 * (E * ec * gc / (1.0 - nu * nu)) ** (1.0 / 3.0)
    wrinkle_design = bx * uni_design / membrane
    assert_close("face", face, filed["modes_main_kd_0_20"]["face_compression"])
    assert_close("crush", crush_sf, filed["modes_main_kd_0_20"]["core_crush"])
    assert_close("crimp", crimp_sf, filed["modes_main_kd_0_20"]["core_shear_crimping"])
    assert_close("wrinkle design", wrinkle_design, filed["modes_main_kd_0_20"]["face_wrinkling"])
    assert_close("separation", h, filed["geometry"]["separation_m"])

    foam_rows = {}
    for label, q in (("design_0.50", 0.50), ("band_0.78", 0.78), ("compare_0.82", 0.82), ("band_0.91", 0.91)):
        uni = q * (E * ec * gc / (1.0 - nu * nu)) ** (1.0 / 3.0)
        sf_w = bx * uni / membrane
        assert_close(label, sf_w, wrinkle["foam"]["rows"][label]["SF_wrinkle"])
        foam_rows[label] = {"Q": q, "SF_wrinkle": sf_w}

    # Least factor at each knockdown, design Q and comparison Q.
    # Wrinkling scales with Q. Handbook buckling does not.
    levels = {}
    for kd, key in (
        (KD_MAIN, "0.20"),
        (KD_PRECISION, "0.90"),
        (KD_CONSERVATIVE, "0.1407"),
    ):
        base = {
            "global_buckling": stated[kd],
            "face_compression": face,
            "core_crush": crush_sf,
            "core_shear_crimping": crimp_sf,
        }
        by_q = {}
        for q_label, q in (("design_0.50", 0.50), ("compare_0.82", 0.82)):
            modes = dict(base)
            modes["face_wrinkling"] = foam_rows[{"design_0.50": "design_0.50", "compare_0.82": "compare_0.82"}[q_label]]["SF_wrinkle"]
            gov = min(modes, key=modes.get)
            by_q[q_label] = {
                "Q": q,
                "modes": modes,
                "least_SF": modes[gov],
                "governing": gov,
            }
        levels[key] = by_q

    # Design point at Q=0.50, kd=0.20: buckling remains a hair under wrinkling.
    design_least = levels["0.20"]["design_0.50"]
    if design_least["governing"] != "global_buckling":
        raise SystemExit("design governing mode moved")
    assert_close("design least", design_least["least_SF"], filed["least_SF_main"])
    if levels["0.90"]["design_0.50"]["governing"] != "face_wrinkling":
        raise SystemExit("0.90 lesser factor must stay design wrinkling")
    if levels["0.1407"]["design_0.50"]["governing"] != "global_buckling":
        raise SystemExit("0.1407 lesser factor must be the restated global")
    if levels["0.90"]["compare_0.82"]["governing"] != "face_wrinkling":
        raise SystemExit("0.90 at Q=0.82 must still be wrinkling")
    if levels["0.1407"]["compare_0.82"]["governing"] != "global_buckling":
        raise SystemExit("0.1407 at Q=0.82 must still be the restated global")

    gap = (0.82 / 0.50) ** 3
    product = 1.0 / wrinkle_design ** 3
    # The filed improvement path stores the product factor at this thickness.
    assert_close("product factor", product, filed["improvement"]["wrinkle_Ec_Gc_product_factor_if_foam"], 1e-9)

    # Honeycomb row, same mass line, not the point. Coefficient 0.33 is 2.2-14.
    # 0.8 is the leading factor of 2.2-12, used here inside 2.2-14. QUESTIONABLE.
    h_tf = hex_row["tf_m"]
    h_tc = hex_row["core_m"]
    h_ec = hexcel["Ec_Pa"]
    h_membrane = p_ext * radius / (4.0 * h_tf)
    honey = {}
    for label, coeff in (("design_0.33", 0.33), ("equation_2_2_12_0.80", 0.8)):
        uni_h = coeff * E * math.sqrt(h_ec * h_tf / (E * h_tc))
        sf_w = bx * uni_h / h_membrane
        stored = wrinkle["honeycomb"]["hexcel_HRH-10-4.8-32_on_the_filed_mass_line"][label]
        assert_close(label, sf_w, stored["SF_wrinkle"])
        honey[label] = {
            "coefficient": coeff,
            "SF_wrinkle": sf_w,
            "global_buckling_handbook": hex_row["modes"]["global_buckling"],
            "least_of_buckling_and_wrinkle": min(sf_w, hex_row["modes"]["global_buckling"]),
        }

    old_misread = classical(KD_PRECISION) / handbook_020
    assert_close("old misread", old_misread, (KD_PRECISION / KD_MAIN) / kc)

    out = {
        "schema": 1,
        "card": "MAINLINE-009b",
        "unit": "vacuum-mainline009-combined-point-1019",
        "status": "ESTIMATE",
        "tag": "QUESTIONABLE",
        "certification": "none",
        "started_at": STARTED,
        "ended_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "does_not_restart": "Face, core, thicknesses and the moderate branch stay at the filed MAINLINE-009 point.",
        "fix": {
            "defect": "MAINLINE-009 stated classical global buckling at 0.90 and 0.1407, with Kc omitted. The 0.1407 factor then exceeded the 0.20 handbook factor.",
            "rule": "stated global SF(kd) = Kc * classical SF(kd). Kc and Vc do not depend on kd. gamma_d stays 0.20 on the moderate branch.",
            "Vc": vc,
            "Kc": kc,
            "gamma_d": gamma,
            "branch": branch,
            "sigma_0_Pa": sigma_0,
            "sigma_crimp_Pa": sigma_crimp,
        },
        "geometry": filed["geometry"],
        "float": filed["float"],
        "omitted_kc_global": {
            "0.90": classical(KD_PRECISION),
            "0.1407": classical(KD_CONSERVATIVE),
            "ratio_equals": KD_CONSERVATIVE / KD_PRECISION,
        },
        "stated_global": {
            "0.20": stated[KD_MAIN],
            "0.90": stated[KD_PRECISION],
            "0.1407": stated[KD_CONSERVATIVE],
            "rounded_0.90": round(stated[KD_PRECISION], 3),
            "rounded_0.1407": round(stated[KD_CONSERVATIVE], 3),
            "order_after_fix": "0.165 < 0.235 < 1.058",
        },
        "knockdown_gap_0.90_over_0.20": KD_PRECISION / KD_MAIN,
        "old_column_0.90_classical_over_0.20_handbook": old_misread,
        "levels_design_Q_0.50": {k: levels[k]["design_0.50"] for k in levels},
        "levels_compare_Q_0.82": {k: levels[k]["compare_0.82"] for k in levels},
        "foam": {
            "design_Q": 0.50,
            "comparison_Q": 0.82,
            "theoretical_band": [0.78, 0.91],
            "theoretical_source": wrinkle["foam"]["theoretical_source"],
            "rows": foam_rows,
            "precision_gap_Ec_Gc": gap,
            "product_factor_at_Q_0.50": product,
            "product_factor_at_Q_0.82": product / gap,
        },
        "honeycomb_not_the_point": honey,
        "reaches_SF_1_in_every_mode": False,
        "p3": {
            "mark": "PENDING-011b",
            "scored": False,
            "rows": pending["rows"],
        },
        "later_cards": {
            "011b_report": None,
            "013_report": None,
            "014_report": "rpt-mainline014-grok-balanced-sandwich-1019",
            "009c": "Due now because 014 has filed. 011b and 013 have not. This card does not absorb 014.",
        },
        "sources": {
            path.name: {"sha256": sha256(path)[0], "bytes": sha256(path)[1]}
            for path in (R009, WRINKLE, P3, R007, R008)
        },
    }
    (ROOT / "KC-LEVELS.json").write_text(json.dumps(out, indent=1) + "\n")
    print(json.dumps({
        "Kc": g(kc),
        "Vc": g(vc),
        "global_0.20": g(stated[KD_MAIN]),
        "global_0.90": g(stated[KD_PRECISION]),
        "global_0.1407": g(stated[KD_CONSERVATIVE]),
        "least_0.90_design": g(levels["0.90"]["design_0.50"]["least_SF"]),
        "gov_0.90_design": levels["0.90"]["design_0.50"]["governing"],
        "least_0.1407_design": g(levels["0.1407"]["design_0.50"]["least_SF"]),
        "gov_0.1407_design": levels["0.1407"]["design_0.50"]["governing"],
        "least_0.20_Q82": g(levels["0.20"]["compare_0.82"]["least_SF"]),
        "least_0.90_Q82": g(levels["0.90"]["compare_0.82"]["least_SF"]),
        "least_0.1407_Q82": g(levels["0.1407"]["compare_0.82"]["least_SF"]),
        "gap": g(gap),
        "old_misread": g(old_misread),
        "product_082": g(product / gap),
    }, indent=1))


if __name__ == "__main__":
    main()
