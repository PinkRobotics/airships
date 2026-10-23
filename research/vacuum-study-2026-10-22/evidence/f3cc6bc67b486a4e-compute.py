#!/usr/bin/env python3
"""MAINLINE-009. One combined design point from the filed cards.

The formulas are the ones already used on MAINLINE-007 and MAINLINE-007b.
This script does not re-derive them. Nothing here is a certification.
"""
from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STARTED = datetime.now().astimezone().isoformat(timespec="seconds")

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

# Knockdowns the brief tells this card to carry. 0.20 is the main point.
KD_MAIN = 0.20
KD_PRECISION = 0.90
KD_CONSERVATIVE = 0.1407
PAYLOAD_MARGIN = 0.05
JOINT = 0.05
SYSTEMS = 100.0
# Case Poisson ratio. MAINLINE-008 does not carry a SiC value.
NU_CASE = 0.33


def sha256(path: Path) -> tuple[str, int]:
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest(), len(data)


def load(path: Path) -> dict:
    return json.loads(path.read_text())


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


def assert_close(name: str, got: float, expect: float, rel: float = 1e-9) -> None:
    scale = max(abs(expect), 1e-30)
    err = abs(got - expect) / scale
    if err > rel:
        raise SystemExit(f"{name} rel {err:.3e}: got {got!r} expect {expect!r}")


def g(x: float) -> str:
    return format(float(x), ".12g")


def main() -> None:
    prior = load(R007)
    prior_b = load(R007B)
    face_card = load(R008)
    margin_card = load(R006)
    kd_card = load(R004B)
    crush_card = load(R005B)

    p_ext = prior["atmosphere"]["p_ext_Pa"]
    lift = prior["atmosphere"]["lift_kg"]
    radius = prior["atmosphere"]["R_m"]
    e_al = prior["inherited"]["E_Pa"]
    sig_al = prior["inherited"]["sigma_Pa"]
    rho_al = prior["inherited"]["rho_face_kg_m3"]
    nu = prior["inherited"]["nu"]
    if nu != NU_CASE or radius != 10.0:
        raise SystemExit("case constants moved")
    area = 4.0 * math.pi * radius * radius
    root = math.sqrt(1.0 - nu * nu)
    factor_bx = biaxial_factor()
    assert_close("biaxial", factor_bx, prior_b["biaxial_factor"], 1e-15)

    # MAINLINE-007b identity on the rho-32 buckling split. Same formulas.
    row32 = prior["rows"]["32.0"]["max_buckling_SF"]
    roh = next(m for m in prior["materials"] if m["name"] == "ROHACELL 31 IG-F")
    ev32 = evaluate(
        row32["tf_m"], row32["core_m"], roh["Gc_used_for_compare_Pa"],
        roh["Ec_Pa"], e_al, nu, radius, p_ext, "foam",
    )
    assert_close("007b Rohacell SF_general", ev32["SF_general"], 0.10622616861328742)
    assert_close("007b Rohacell SF_wr", ev32["SF_wrinkle"], 0.12449046966262503)
    hexweb = next(m for m in prior["materials"] if m["name"] == "Hexcel HRH-10-4.8-32")
    evh = evaluate(
        row32["tf_m"], row32["core_m"], hexweb["Gc_used_for_compare_Pa"],
        hexweb["Ec_Pa"], e_al, nu, radius, p_ext, "honeycomb",
    )
    assert_close("007b Hexcel SF_general", evh["SF_general"], 0.10701661242194413)
    assert_close("007b Hexcel SF_wr", evh["SF_wrinkle"], 0.05652863640260287)

    # MAINLINE-007 rho-16 buckling peak, margin 0, then MAINLINE-006's own 5 percent
    # P2-E geometry through the same pressure formula. P2-E is the sealed equal
    # face/core split, not the rho-16 peak, so the two thicknesses are not forced equal.
    m0 = (lift - SYSTEMS) / (1.0 + JOINT)
    peak16 = buckling_peak_tf(m0, area, rho_al, 16.0)
    row16 = prior["rows"]["16.0"]["max_buckling_SF"]
    assert_close("007 rho16 tf", peak16, row16["tf_m"], 1e-12)
    ev16 = evaluate(
        row16["tf_m"], row16["core_m"], None, None, e_al, nu, radius, p_ext, "open", sig_al,
    )
    assert_close("007 rho16 SF_b", ev16["SF_classical_0_20"], row16["SF_b"], 1e-12)
    p2e = next(r for r in margin_card["families"]["P2-E"]["rows"] if r["label"] == "5pct")
    ev_p2e = evaluate(
        p2e["geometry"]["tf_m"], p2e["geometry"]["core_m"], None, None,
        e_al, nu, radius, p_ext, "open", sig_al,
    )
    assert_close("006 P2-E 5pct SF_b", ev_p2e["SF_classical_0_20"], p2e["buckling_SF"], 1e-9)
    m_struct = (lift * (1.0 - PAYLOAD_MARGIN) - SYSTEMS) / (1.0 + JOINT)

    # MAINLINE-008 equal-mass SiC on the sealed P2-E separation.
    sic = face_card["candidates_ranked_by_least_SF_P2E"][0]
    if not sic["name"].startswith("SiC") or sic["tag"] != "QUESTIONABLE":
        raise SystemExit("008 rank 1 is not sourced SiC")
    p2e_al = face_card["case"]["rows_from"]["P2-E"]
    tf_sic_held = p2e_al["tf_Al_m"] * rho_al / sic["rho"]
    d_held = p2e_al["d_m"]
    p_b_held = KD_MAIN * 4.0 * tf_sic_held * d_held * (sic["E_GPa"] * 1e9) / (radius * radius * root)
    assert_close("008 SiC P2-E SF_b", p_b_held / p_ext, sic["rows"]["P2-E"]["SF_b"], 1e-12)
    p2e_kd = next(r for r in kd_card["rows"] if r["point_id"] == "P2-E")
    assert_close(
        "004b P2-E central",
        p2e_kd["factors"]["central"]["buckling_SF"],
        0.23388557899250975,
        1e-12,
    )
    if abs(p2e_kd["factors"]["optimistic"]["kd"] - KD_PRECISION) > 1e-15:
        raise SystemExit("004b optimistic knockdown is not 0.90")

    # 006 knee for the sandwich families is the 0 to 5 percent step.
    knee = margin_card["families"]["P2-E"]["knee"]
    if knee["from_label"] != "0" or knee["to_label"] != "5pct":
        raise SystemExit("P2-E knee moved; the 5 percent margin needs a fresh reading")
    p3_block = margin_card["families"]["P3"]
    p3_zero = next(r for r in p3_block["rows"] if r["label"] == "0")
    p3_least = p3_zero["least_SF"]
    film_sf = p3_zero["film_SF"]

    face = {
        "name": sic["name"],
        "tag": sic["tag"],
        "rho": float(sic["rho"]),
        "E": float(sic["E_GPa"]) * 1e9,
        "sigma": float(sic["sigma_c_MPa"]) * 1e6,
        "sigma_basis": sic["sigma_c_basis"],
        "source": sic["source"],
        "flexural_MPa": 380.0,
    }
    materials = [m for m in prior["materials"] if m["name"] != "Schaedler nickel microlattice"]
    survey = []
    for mat in materials:
        kind = wrinkle_kind(mat["family"], mat.get("Ec_Pa"))
        best = best_on_mass_line(
            m_struct, area, face, mat, nu, radius, p_ext, kind, KD_MAIN,
        )
        best["role"] = "sic_candidate"
        survey.append(best)

    complete = [s for s in survey if s["complete"]]
    if not complete:
        raise SystemExit("no sourced core has every mode")
    complete.sort(key=lambda s: (-s["least_SF"], s["density_kg_m3"]))
    winner = complete[0]
    # The unconstrained line crosses Vc=2, where gamma_d jumps from 0.20 to 1.
    # That jump is the discontinuity MAINLINE-007b recorded. It is not the point.
    try:
        crimp_excursion = best_on_mass_line(
            m_struct, area, face, next(m for m in materials if m["name"] == winner["core"]),
            nu, radius, p_ext, wrinkle_kind(
                next(m for m in materials if m["name"] == winner["core"])["family"],
                next(m for m in materials if m["name"] == winner["core"]).get("Ec_Pa"),
            ), KD_MAIN, branch_limit="crimp",
        )
    except SystemExit:
        crimp_excursion = None

    # Does any QUESTIONABLE face, on any complete core, clear every mode?
    sourced_faces = [
        c for c in face_card["candidates_ranked_by_least_SF_P2E"]
        if c["tag"] == "QUESTIONABLE"
    ]
    face_survey = []
    any_clears = False
    best_any = None
    for cand in sourced_faces:
        f = {
            "name": cand["name"],
            "tag": cand["tag"],
            "rho": float(cand["rho"]),
            "E": float(cand["E_GPa"]) * 1e9,
            "sigma": float(cand["sigma_c_MPa"]) * 1e6,
        }
        local = []
        for mat in materials:
            kind = wrinkle_kind(mat["family"], mat.get("Ec_Pa"))
            if kind == "open":
                continue
            row = best_on_mass_line(
                m_struct, area, f, mat, nu, radius, p_ext, kind, KD_MAIN,
            )
            local.append(row)
            if best_any is None or row["least_SF"] > best_any["least_SF"]:
                best_any = row
            if row["least_SF"] >= 1.0 and modes_clear(row, KD_PRECISION):
                any_clears = True
        local.sort(key=lambda s: -s["least_SF"])
        face_survey.append({
            "face": cand["name"],
            "tag": cand["tag"],
            "best_core": local[0]["core"],
            "best_least_SF": local[0]["least_SF"],
            "governing": local[0]["governing"],
            "clears_at_0_20": local[0]["least_SF"] >= 1.0,
        })

    point_modes_090 = modes_at_kd(winner, KD_PRECISION)
    point_modes_cons = modes_at_kd(winner, KD_CONSERVATIVE)
    improvement = improvement_path(winner, point_modes_090, face_survey, any_clears)

    # Zero-margin twin, same face and core and same rule, to show 006's knee
    # is not a repair. Structural mass at margin 0.
    m0 = (lift - SYSTEMS) / (1.0 + JOINT)
    mat_win = next(m for m in materials if m["name"] == winner["core"])
    kind_win = wrinkle_kind(mat_win["family"], mat_win.get("Ec_Pa"))
    at_zero = best_on_mass_line(
        m0, area, face, mat_win, nu, radius, p_ext, kind_win, KD_MAIN,
    )

    doc = {
        "schema": 1,
        "card": "MAINLINE-009",
        "unit": "vacuum-mainline009-combined-point-1019",
        "status": "ESTIMATE",
        "tag": "QUESTIONABLE",
        "certification": "none",
        "started_at": STARTED,
        "ended_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "point": {
            "family": "P2",
            "family_reason": (
                "MAINLINE-006 least safety factor at zero margin is higher for P2-E "
                "than for P1 or P3. The P3 film factor stays above 1 and does not govern. "
                "No filed sandwich family beats P2."
            ),
            "face": face["name"],
            "face_tag": "QUESTIONABLE",
            "face_source": face["source"],
            "sigma_basis": face["sigma_basis"],
            "core": winner["core"],
            "core_tag": "QUESTIONABLE",
            "core_family": winner["core_family"],
            "core_density_kg_m3": winner["density_kg_m3"],
            "core_source": winner["source"],
            "payload_margin": PAYLOAD_MARGIN,
            "payload_reason": (
                "CARD-009 says 5 percent of lift unless MAINLINE-006 shows a better knee. "
                "On P2-E the knee is the 0 to 5 percent step, the steepest drop, not a "
                "different operating margin. Margins above 5 percent cost less safety "
                "factor per kilogram and are a worse trade. The point keeps 5 percent."
            ),
            "knockdown_main": KD_MAIN,
            "knockdown_precision": KD_PRECISION,
            "knockdown_conservative_reference": KD_CONSERVATIVE,
            "geometry_rule": (
                "On the 5 percent mass ceiling, face thickness is the value that "
                "maximises the lesser of the five mode safety factors at knockdown 0.20. "
                "Global buckling in that lesser factor is the NASA CR-1457 handbook "
                "value, gamma_d times Kc, not the classical pressure stacked on top of it. "
                "The 0.90 column is the same geometry with the classical pressure scaled "
                "to 0.90. The handbook does not authorise gamma_d of 0.90."
            ),
        },
        "float": {
            "lift_kg": lift,
            "total_mass_kg": winner["total_mass_kg"],
            "payload_kg": lift - winner["total_mass_kg"],
            "float_margin": (lift - winner["total_mass_kg"]) / lift,
            "above_zero": (lift - winner["total_mass_kg"]) > 0.0,
        },
        "geometry": {
            "tf_m": winner["tf_m"],
            "core_m": winner["core_m"],
            "separation_m": winner["separation_m"],
            "R_m": radius,
            "radius_note": (
                "R is the external 10 m. The handbook middle-surface radius is smaller "
                "by about half the separation. Both the classical and the handbook "
                "pressures use 10 m, as MAINLINE-007b did."
            ),
        },
        "masses_kg": winner["masses_kg"],
        "modes_main_kd_0_20": winner["modes"],
        "modes_precision_kd_0_90": point_modes_090,
        "modes_conservative_kd_0_1407": point_modes_cons,
        "least_SF_main": winner["least_SF"],
        "governing_main": winner["governing"],
        "handbook": {
            "Vc": winner["Vc"],
            "Kc": winner["Kc"],
            "gamma_d": winner["gamma_d"],
            "branch": winner["branch"],
            "SF_classical_0_20": winner["SF_classical_0_20"],
            "SF_general": winner["SF_general"],
        },
        "rejected_crimp_branch": None if crimp_excursion is None else {
            "reason": "Vc>2 flips gamma_d from 0.20 to 1 while Kc is 1/2. MAINLINE-007b records that jump as discontinuous. The point stays on the moderate branch, where gamma_d is the brief's 0.20.",
            "least_SF": crimp_excursion["least_SF"],
            "governing": crimp_excursion["governing"],
            "Vc": crimp_excursion["Vc"],
            "gamma_d": crimp_excursion["gamma_d"],
            "tf_m": crimp_excursion["tf_m"],
            "core_m": crimp_excursion["core_m"],
            "modes": crimp_excursion["modes"],
        },
        "reaches_SF_1_in_every_mode": bool(
            winner["least_SF"] >= 1.0 and min(point_modes_090.values()) >= 1.0
        ),
        "any_sourced_questionable_pair_reaches_1": any_clears,
        "improvement": improvement,
        "zero_margin_same_materials": {
            "least_SF": at_zero["least_SF"],
            "governing": at_zero["governing"],
            "tf_m": at_zero["tf_m"],
            "core_m": at_zero["core_m"],
            "modes": at_zero["modes"],
            "note": "Same face, same core, margin 0. Shown so the knee is not mistaken for a fix.",
        },
        "sic_cores_ranked": [
            {
                "core": s["core"],
                "density_kg_m3": s["density_kg_m3"],
                "complete": s["complete"],
                "least_SF": s["least_SF"],
                "governing": s["governing"],
                "tf_m": s["tf_m"],
                "core_m": s["core_m"],
                "modes": s["modes"],
            }
            for s in sorted(survey, key=lambda s: -(s["least_SF"] or -1.0))
        ],
        "questionable_faces_best_complete_core": face_survey,
        "best_questionable_pair": None if best_any is None else {
            "face": best_any["face"],
            "core": best_any["core"],
            "least_SF": best_any["least_SF"],
            "governing": best_any["governing"],
            "modes": best_any["modes"],
            "tf_m": best_any["tf_m"],
            "core_m": best_any["core_m"],
        },
        "family_evidence": {
            "P2E_least_SF_margin_0": next(
                r["least_SF"] for r in margin_card["families"]["P2-E"]["rows"] if r["label"] == "0"
            ),
            "P1_least_SF_margin_0": next(
                r["least_SF"] for r in margin_card["families"]["P1"]["rows"] if r["label"] == "0"
            ),
            "P3_least_SF_margin_0": p3_least,
            "P3_block_keys": sorted(p3_block.keys()),
            "film_SF_if_present": film_sf,
        },
        "checks": {
            "007b_rohacell": "PASS",
            "007b_hexcel": "PASS",
            "006_p2e_5pct": "PASS",
            "008_sic_p2e": "PASS",
            "004b_p2e_central": "PASS",
            "float_margin_above_zero": winner["float_margin"] > 0.0,
        },
        "crush_model": {
            "sigma_core_Pa": p_ext / 2.0,
            "source_report": "rpt-ref-9dd3721f6f2e5595ab9a",
            "required_Pa_on_005b": crush_card.get("required_core_compressive_Pa", p_ext / 2.0),
        },
        "knockdown_ledger_inputs": {
            "main": KD_MAIN,
            "precision": KD_PRECISION,
            "brief_conservative": KD_CONSERVATIVE,
            "precision_over_main": KD_PRECISION / KD_MAIN,
            "004b_P2E_optimistic_over_conservative": p2e_kd["optimistic_over_conservative"],
            "004b_P2E_sealed_kd": p2e_kd["sealed_sp8032_kd"],
        },
        "formulas": {
            "mass": "(1-margin)*lift = 1.05*(faces+core)+100",
            "classical": "kd*4*tf*h*E/(R^2*sqrt(1-nu^2)), h=tc+tf",
            "handbook": "gamma_d*Kc*sigma_0, NASA CR-1457 6.2, as on MAINLINE-007b",
            "face": "4*sigma*tf/R",
            "crush": "core compressive strength / (p/2)",
            "crimp": "handbook crimp pressure 4*sigma_crimp*tf/R, equation 6.2-6",
            "wrinkle_foam": "0.50*(E*Ec*Gc/(1-nu^2))**(1/3) times equibiaxial factor, equation 2.2-5",
            "wrinkle_honeycomb": "0.33*E*sqrt(Ec*tf/(E*tc)) times the same factor, equation 2.2-14",
            "nu": "0.33 carried from the 6061 case. 008 does not give a SiC Poisson ratio.",
        },
    }
    if not doc["float"]["above_zero"]:
        raise SystemExit("float margin is not above zero")
    (ROOT / "RESULTS.json").write_text(json.dumps(doc, indent=1) + "\n")
    (ROOT / "NFI.json").write_text(json.dumps(nfi(doc, face, mat_win), indent=1) + "\n")
    print(json.dumps({
        "core": winner["core"],
        "tf_m": g(winner["tf_m"]),
        "core_m": g(winner["core_m"]),
        "least": g(winner["least_SF"]),
        "governing": winner["governing"],
        "Vc": None if winner["Vc"] is None else g(winner["Vc"]),
        "gamma_d": winner["gamma_d"],
        "branch": winner["branch"],
        "Kc": None if winner["Kc"] is None else g(winner["Kc"]),
        "modes_020": {k: g(v) for k, v in winner["modes"].items()},
        "modes_090": {k: g(v) for k, v in point_modes_090.items()},
        "modes_1407": {k: g(v) for k, v in point_modes_cons.items()},
        "float_margin": g(doc["float"]["float_margin"]),
        "reaches": doc["reaches_SF_1_in_every_mode"],
        "any_clears": any_clears,
        "improvement": improvement,
        "faces": face_survey,
        "cores": [
            {"core": s["core"], "least": None if s["least_SF"] is None else g(s["least_SF"]),
             "gov": s["governing"], "complete": s["complete"]}
            for s in survey
        ],
        "zero_least": g(at_zero["least_SF"]),
        "best_any": None if best_any is None else {
            "face": best_any["face"], "core": best_any["core"], "least": g(best_any["least_SF"]),
            "gov": best_any["governing"],
        },
        "film": film_sf,
        "p3_keys": sorted(p3_block.keys()),
    }, indent=1))


def wrinkle_kind(family: str, ec) -> str:
    if "foam" in family:
        return "foam"
    if "honeycomb" in family and ec is not None:
        return "honeycomb"
    return "open"


def core_thickness(tf: float, m_struct: float, area: float, rho_f: float, rho_c: float) -> float:
    m_faces = 2.0 * area * tf * rho_f
    m_core = m_struct - m_faces
    return m_core / (area * rho_c)


def buckling_peak_tf(m_struct: float, area: float, rho_f: float, rho_c: float) -> float:
    return m_struct / (2.0 * area * (2.0 * rho_f - rho_c))


def evaluate(tf, tc, gc, ec, E, nu, R, p_ext, kind, sigma=None) -> dict:
    h = tc + tf
    root = math.sqrt(1.0 - nu * nu)
    membrane = p_ext * R / (4.0 * tf)
    sf_classical = {
        KD_MAIN: (KD_MAIN * 4.0 * tf * h * E / (R * R * root)) / p_ext,
        KD_PRECISION: (KD_PRECISION * 4.0 * tf * h * E / (R * R * root)) / p_ext,
        KD_CONSERVATIVE: (KD_CONSERVATIVE * 4.0 * tf * h * E / (R * R * root)) / p_ext,
    }
    out = {
        "tf_m": tf,
        "core_m": tc,
        "separation_m": h,
        "membrane_Pa": membrane,
        "SF_classical_0_20": sf_classical[KD_MAIN],
        "SF_classical_0_90": sf_classical[KD_PRECISION],
        "SF_classical_0_1407": sf_classical[KD_CONSERVATIVE],
        "SF_face": None if sigma is None else (4.0 * sigma * tf / R) / p_ext,
        "Vc": None,
        "Kc": None,
        "gamma_d": None,
        "branch": None,
        "SF_general": None,
        "SF_crimp": None,
        "SF_wrinkle": None,
    }
    if gc is not None and tc > 0.0:
        sigma_0 = E * h / (R * root)
        sigma_crimp = h * h * gc / (2.0 * tf * tc)
        vc = sigma_0 / sigma_crimp
        kc, gamma, branch = k_and_gamma(vc)
        sigma_cr = gamma * kc * sigma_0
        p_cr = 4.0 * sigma_cr * tf / R
        p_crimp = 4.0 * sigma_crimp * tf / R
        out.update({
            "Vc": vc,
            "Kc": kc,
            "gamma_d": gamma,
            "branch": branch,
            "SF_general": p_cr / p_ext,
            "SF_crimp": p_crimp / p_ext,
        })
    if kind == "foam" and ec is not None and gc is not None:
        uni = 0.50 * (E * ec * gc / (1.0 - nu * nu)) ** (1.0 / 3.0)
        out["SF_wrinkle"] = biaxial_factor() * uni / membrane
    elif kind == "honeycomb" and ec is not None and tc > 0.0:
        uni_h = 0.33 * E * math.sqrt(ec * tf / (E * tc))
        out["SF_wrinkle"] = biaxial_factor() * uni_h / membrane
    return out


def modes_from(ev: dict, crush_sf: float | None) -> dict:
    global_sf = ev["SF_general"] if ev["SF_general"] is not None else ev["SF_classical_0_20"]
    return {
        "global_buckling": global_sf,
        "face_compression": ev["SF_face"],
        "core_crush": crush_sf,
        "core_shear_crimping": ev["SF_crimp"],
        "face_wrinkling": ev["SF_wrinkle"],
    }


def best_on_mass_line(m_struct, area, face, mat, nu, radius, p_ext, kind, kd_for_global, branch_limit="moderate") -> dict:
    rho_c = float(mat["density_kg_m3"])
    rho_f = face["rho"]
    tf_hi = m_struct / (2.0 * area * rho_f) * (1.0 - 1e-6)
    # Keep a token core. The mass line's far end is all face.
    n = 40001
    best = None
    gc = mat.get("Gc_used_for_compare_Pa")
    ec = mat.get("Ec_Pa")
    crush = mat.get("compressive_strength_Pa")
    crush_sf = None if crush is None else crush / (p_ext / 2.0)
    for i in range(1, n):
        tf = tf_hi * i / n
        tc = core_thickness(tf, m_struct, area, rho_f, rho_c)
        if tc <= 0.0:
            continue
        ev = evaluate(tf, tc, gc, ec, face["E"], nu, radius, p_ext, kind, face["sigma"])
        if branch_limit == "moderate" and ev["branch"] == "shear_crimping":
            continue
        if branch_limit == "crimp" and ev["branch"] != "shear_crimping":
            continue
        modes = modes_from(ev, crush_sf)
        # Global column used in the lesser factor is the main-point column.
        if kd_for_global == KD_PRECISION:
            modes["global_buckling"] = ev["SF_classical_0_90"]
        present = {k: v for k, v in modes.items() if v is not None}
        complete = len(present) == 5
        if not present:
            continue
        gov = min(present, key=present.get)
        least = present[gov]
        if not complete:
            gov = "incomplete:" + gov
        if best is None or least > best["least_SF"]:
            masses = masses_of(tf, tc, area, rho_f, rho_c)
            best = {
                "face": face["name"],
                "core": mat["name"],
                "core_family": mat["family"],
                "density_kg_m3": rho_c,
                "source": mat.get("source"),
                "tag": mat.get("tag"),
                "complete": complete,
                "tf_m": tf,
                "core_m": tc,
                "separation_m": tc + tf,
                "least_SF": least,
                "governing": gov,
                "modes": modes,
                "masses_kg": masses,
                "total_mass_kg": masses["total"],
                "float_margin": masses["float_margin"],
                "Vc": ev["Vc"],
                "Kc": ev["Kc"],
                "gamma_d": ev["gamma_d"],
                "branch": ev["branch"],
                "SF_classical_0_20": ev["SF_classical_0_20"],
                "SF_general": ev["SF_general"],
                "SF_wrinkle": ev["SF_wrinkle"],
                "kind": kind,
            }
    if best is None:
        raise SystemExit(f"no geometry for {mat['name']}")
    return best


def masses_of(tf, tc, area, rho_f, rho_c) -> dict:
    faces = 2.0 * area * tf * rho_f
    core = area * tc * rho_c
    joints = JOINT * (faces + core)
    total = faces + core + joints + SYSTEMS
    lift = 4889.442150186961
    return {
        "faces": faces,
        "core": core,
        "joints": joints,
        "systems_kg": SYSTEMS,
        "residual_gas": 0.0,
        "total": total,
        "payload_kg": lift - total,
        "float_margin": (lift - total) / lift,
    }


def modes_at_kd(row: dict, kd: float) -> dict:
    """Other modes do not use the classical knockdown. Global buckling does.

    At 0.20 the stated global mode is already the handbook value stored on the
    row. At 0.90 and at 0.1407 the stated global mode is the classical pressure
    at that knockdown. Handbook gamma_d stays 0.20 on the moderate branch.
    """
    modes = dict(row["modes"])
    if kd == KD_MAIN:
        return modes
    scale = kd / KD_MAIN
    modes["global_buckling"] = row["SF_classical_0_20"] * scale
    return modes


def modes_clear(row: dict, kd_precision: float) -> bool:
    if row["least_SF"] is None or row["least_SF"] < 1.0:
        return False
    return min(modes_at_kd(row, kd_precision).values()) >= 1.0


def improvement_path(winner, modes_090, face_survey, any_clears) -> dict:
    short = {k: v for k, v in winner["modes"].items() if v is not None and v < 1.0}
    short_090 = {k: v for k, v in modes_090.items() if v is not None and v < 1.0}
    if not short and not short_090:
        return {"needed": False, "text": "The sourced point reaches 1 in every mode at both knockdowns."}
    # Smallest single-mode factor on the main point.
    gov = min(short, key=short.get) if short else min(short_090, key=short_090.get)
    sf = (short or short_090)[gov]
    factor = 1.0 / sf
    nearest = face_survey[0]
    # Runner-up face by all-mode least SF, if the survey is sorted by the caller.
    ranked = sorted(face_survey, key=lambda r: -r["best_least_SF"])
    return {
        "needed": True,
        "any_sourced_pair_clears": any_clears,
        "governing_mode": gov,
        "SF": sf,
        "factor_on_that_allowable": factor,
        "also_short_at_0_20": short,
        "also_short_at_0_90": short_090,
        "nearest_face_class": ranked[0]["face"] if ranked else None,
        "nearest_face_least_SF": ranked[0]["best_least_SF"] if ranked else None,
        "nearest_face_core": ranked[0]["best_core"] if ranked else None,
        "wrinkle_stress_factor": None if "face_wrinkling" not in short and "face_wrinkling" not in short_090 else (
            1.0 / min(short.get("face_wrinkling", 1e9), short_090.get("face_wrinkling", 1e9))
        ),
        "wrinkle_Ec_Gc_product_factor_if_foam": None if winner["kind"] != "foam" or (
            "face_wrinkling" not in short and "face_wrinkling" not in short_090
        ) else (
            1.0 / min(short.get("face_wrinkling", 1e9), short_090.get("face_wrinkling", 1e9))
        ) ** 3,
        "note": nearest["face"],
    }


def nfi(doc: dict, face: dict, mat: dict) -> list:
    modes = doc["modes_main_kd_0_20"]
    return [
        {
            "id": "NFI-KD-PRECISION",
            "value": "knockdown on classical sphere buckling",
            "optimistic": 0.90,
            "optimistic_source": "Wagner 2020 Table 3, Krenzke and Kiernan, reliable upper, outside this lambda. MAINLINE-004b.",
            "main_point": 0.20,
            "main_source": "Inside the sandwich data. Sim 2024 foam-core 0.20 to 0.22. Wagner 2020 central about 0.2.",
            "conservative": 0.1407,
            "conservative_source": "CARD-009 names SP-8032's 0.1407. MAINLINE-004b P2-E sealed value is 0.140725695373. Its own optimism ratio against that sealed value is near 6.4. This ledger does not replace that ratio.",
            "factor_precision_gap": 0.90 / 0.20,
            "factor_meaning": "0.90/0.20 = 4.5, the precision gap CARD-009 asks this ledger to carry.",
            "direction": "Knockdown tests on sandwich spheres at lambda near 66, the regime of these rows.",
        },
        {
            "id": "NFI-FACE-STRENGTH",
            "value": "SiC face compressive strength",
            "optimistic": 3900e6,
            "optimistic_source": face["source"],
            "conservative": 380e6,
            "conservative_source": "Hexoloy SA flexural strength, the figure MAINLINE-008 says governs a bending or tension path.",
            "factor": 3900.0 / 380.0,
            "stated_mode_uses": "compressive 3900 MPa, because the stated mode is face compression",
            "SF_if_flexural_were_used": modes["face_compression"] * 380.0 / 3900.0,
            "direction": "A compressive allowable for the sintered face, and a check that the sphere stress stays membrane compression.",
        },
        {
            "id": "NFI-FACE-MODULUS",
            "value": "SiC Young's modulus and density",
            "optimistic": {"E_Pa": face["E"], "rho": face["rho"]},
            "conservative": "no second sourced pair on MAINLINE-008",
            "factor": None,
            "tag": "QUESTIONABLE",
            "direction": "A batch modulus and density for the face sheet that would actually be built.",
        },
        {
            "id": "NFI-NU",
            "value": "Poisson ratio inside the buckling and foam-wrinkling formulas",
            "optimistic": 0.33,
            "conservative": 0.33,
            "factor": 1.0,
            "source": "Carried from the 6061 case. MAINLINE-008 does not give a SiC Poisson ratio.",
            "direction": "Use the face sheet's Poisson ratio. Buckling pressure scales as 1/sqrt(1-nu^2).",
        },
        {
            "id": "NFI-CORE",
            "value": mat["name"],
            "optimistic": {
                "density_kg_m3": mat["density_kg_m3"],
                "Ec_Pa": mat.get("Ec_Pa"),
                "Gc_Pa": mat.get("Gc_used_for_compare_Pa"),
                "compressive_Pa": mat.get("compressive_strength_Pa"),
            },
            "conservative": "Divinycell rev9 prints a minimum compressive strength of 0.3 MPa against the nominal 0.5 MPa used here. Other cores on MAINLINE-007 are typical columns, not allowables.",
            "factor_divinycell_compression": 0.5 / 0.3,
            "tag": "QUESTIONABLE",
            "direction": "Design allowables for Ec, Gc and compressive strength at the thickness this point uses.",
        },
        {
            "id": "NFI-CRUSH-MODEL",
            "value": "core compressive stress",
            "optimistic": "p/2",
            "conservative": "p/2",
            "factor": 1.0,
            "source": "MAINLINE-005b. The brief's example, not a solved contact problem.",
            "direction": "A core stress from the face-to-face load path, including local bending.",
        },
        {
            "id": "NFI-HANDBOOK-GAMMA",
            "value": "NASA CR-1457 gamma_d",
            "optimistic": 0.90,
            "main": 0.20,
            "conservative": 0.1407,
            "factor": 4.5,
            "note": "On the moderate-core branch gamma_d is 0.20 and the handbook safety factor is Kc times the classical kd=0.20 pressure. gamma_d of 0.90 is not a handbook value. It is the MAINLINE-004b precision direction, applied only to the classical pressure.",
            "direction": "Tests that separate face-modulus knockdown from core-shear flexibility on a complete sphere.",
        },
        {
            "id": "NFI-WRINKLE-BIAX",
            "value": "equibiaxial factor on the flat-plate interaction Rx^3+Ry=1",
            "optimistic": doc["modes_main_kd_0_20"]["face_wrinkling"],
            "factor_formula": "constant 0.682327803828, already inside the stated wrinkling safety factor",
            "conservative": "the same interaction",
            "direction": "A sphere-face wrinkling test. The interaction is a flat-plate equation.",
        },
        {
            "id": "NFI-MASS",
            "value": "payload margin",
            "optimistic": 0.0,
            "main_point": 0.05,
            "conservative": 0.05,
            "factor": "zero margin raises the structural budget by (lift-100)/(0.95*lift-100), about 5 percent, which does not close a wrinkling gap of several times",
            "source": "CARD-009 default, kept because MAINLINE-006's P2-E knee is that same 0 to 5 percent step.",
            "direction": "MAINLINE-012's equal-margin geometry, when that card is the newer input.",
        },
    ]


if __name__ == "__main__":
    main()
