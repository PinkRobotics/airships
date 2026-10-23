#!/usr/bin/env python3
"""MAINLINE-007b. Sourced shear and wrinkling, same geometries as 007 and P2-E.

Formulas are the ones read from NASA CR-1457 (Sullins, Smith, Spier, December
1969), NTRS 19700004831. The sphere section restates Yao (1962) as Plantema
rewrote it. This script does not re-derive that theory. Nothing here is a
certification.
"""
from __future__ import annotations

import json
import math
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PRIOR = ROOT.parent / "vacuum-mainline007-core-trade-1019" / "RESULTS.json"
STARTED = datetime.now().astimezone().isoformat(timespec="seconds")

# NASA CR-1457, equal faces, elastic. Middle-surface separation h = tc + tf.
# sigma_0 = eta * E * h / (R * sqrt(1-nu^2))                         (6.2-2, 6.2-26)
# sigma_crimp = h^2 * Gc / (2 * tf * tc)                              (6.2-6, 6.2-27)
# Vc = sigma_0 / sigma_crimp                                          (6.2-5, 6.2-28)
# Kc = 1 - Vc/4 when Vc <= 2, else 1/Vc                               (6.2-3, 6.2-4)
# gamma = 0.20 for a hemisphere when Vc < 2, else 1                   (6.2-13 and p. 6-12)
# sigma_cr = gamma * Kc * sigma_0                                     (6.2-1, 6.2-25)
# p_cr = 4 * sigma_cr * tf / R                                        (6.2-29)
# Foam wrinkling, Q = 0.50, eta = 1:                                  (2.2-5)
#   sigma_wr = Q * (eta*E*Ec*Gc / (1-nu^2)) ** (1/3)
# Honeycomb lower bound, eta = 1, waviness unknown:                   (2.2-14)
#   sigma_wr = 0.33 * E * sqrt(Ec * tf / (E * tc))
# Equibiaxial interaction, Rx^3 + Ry = 1, Rx = Ry:                    (2.2-6, 2.2-15)


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


def evaluate(tf: float, tc: float, gc: float, ec: float, E: float, nu: float, R: float, p_ext: float) -> dict:
    h = tc + tf
    root = math.sqrt(1.0 - nu * nu)
    sigma_0 = E * h / (R * root)  # eta = 1
    sigma_crimp = h * h * gc / (2.0 * tf * tc)
    vc = sigma_0 / sigma_crimp
    kc, gamma, branch = k_and_gamma(vc)
    sigma_cr = gamma * kc * sigma_0
    p_cr = 4.0 * sigma_cr * tf / R
    p_classical = 0.2 * 4.0 * tf * h * E / (R * R * root)
    membrane = p_ext * R / (4.0 * tf)
    # Advisory crimp from MAINLINE-003: p = 2*Gc*d/R with d = h.
    p_advisory_crimp = 2.0 * gc * h / R
    out = {
        "h_m": h,
        "sigma_0_Pa": sigma_0,
        "sigma_crimp_Pa": sigma_crimp,
        "Vc": vc,
        "Kc": kc,
        "gamma_d": gamma,
        "branch": branch,
        "sigma_cr_Pa": sigma_cr,
        "p_cr_Pa": p_cr,
        "SF_general": p_cr / p_ext,
        "SF_classical_kd_0_2": p_classical / p_ext,
        "SF_ratio_general_over_classical": (p_cr / p_ext) / (p_classical / p_ext),
        "membrane_Pa": membrane,
        "SF_yield_unchanged_needs_sigma": None,
        "advisory_crimp_pressure_Pa": p_advisory_crimp,
        "handbook_crimp_pressure_Pa": 4.0 * sigma_crimp * tf / R,
        "crimp_pressure_ratio_handbook_over_advisory": (h / tc),
        "Gc_for_Vc_equals_2_Pa": sigma_0 * tf * tc / (h * h),
    }
    if ec is not None and gc is not None:
        # Solid or foam core, equation 2.2-5. Not for honeycomb.
        uni = 0.50 * (E * ec * gc / (1.0 - nu * nu)) ** (1.0 / 3.0)
        advisory = 0.50 * (E * ec * gc) ** (1.0 / 3.0)
        factor = biaxial_factor()
        allow = factor * uni
        out["foam_wrinkling"] = {
            "uniaxial_Pa": uni,
            "advisory_uniaxial_Pa": advisory,
            "biaxial_factor": factor,
            "equibiaxial_allowable_Pa": allow,
            "SF_wr_equibiaxial": allow / membrane,
            "SF_wr_advisory_uniaxial": advisory / membrane,
            "SF_ratio_sourced_over_advisory": (allow / membrane) / (advisory / membrane),
        }
    if ec is not None:
        uni_h = 0.33 * E * math.sqrt(ec * tf / (E * tc))
        factor = biaxial_factor()
        allow_h = factor * uni_h
        out["honeycomb_wrinkling"] = {
            "uniaxial_Pa": uni_h,
            "biaxial_factor": factor,
            "equibiaxial_allowable_Pa": allow_h,
            "SF_wr_equibiaxial": allow_h / membrane,
            "note": "Equation 2.2-14. Ec is the core modulus normal to the facings. A stabilised honeycomb compressive modulus is used where that is the sourced number, and it is QUESTIONABLE.",
        }
    return out


def main() -> None:
    prior = json.loads(PRIOR.read_text())
    E = prior["inherited"]["E_Pa"]
    nu = prior["inherited"]["nu"]
    p_ext = prior["atmosphere"]["p_ext_Pa"]
    R = prior["atmosphere"]["R_m"]
    sigma = prior["inherited"]["sigma_Pa"]
    factor = biaxial_factor()
    # Identity: infinite shear restores the kd = 0.2 classical pressure.
    ident = evaluate(0.000336094970395, 0.113432052508, 1e30, None, E, nu, R, p_ext)
    if abs(ident["SF_ratio_general_over_classical"] - 1.0) > 1e-9:
        raise SystemExit(f"infinite-G identity failed: {ident['SF_ratio_general_over_classical']}")
    if abs(ident["Kc"] - 1.0) > 1e-9:
        raise SystemExit("infinite-G Kc is not 1")
    # P2-E sealed match at kd = 0.2.
    if abs(ident["SF_classical_kd_0_2"] - 0.23388557899250978) / 0.23388557899250978 > 1e-9:
        raise SystemExit(f"P2-E classical mismatch {ident['SF_classical_kd_0_2']}")

    geometries = {
        "P2-E": {
            "source": "MAINLINE-003 equal face and core mass, rho 16 kg/m3",
            "tf_m": 0.0003360949703945902,
            "core_m": 0.1134320525081742,
            "SF_b_sealed": 0.23388557899250978,
            "SF_y": 4.0 * sigma * 0.0003360949703945902 / R / p_ext,
        }
    }
    for rho, block in prior["rows"].items():
        for split in ("max_buckling_SF", "max_least_SF"):
            row = block[split]
            geometries[f"rho_{rho}_{split}"] = {
                "source": "MAINLINE-007 closed form",
                "tf_m": row["tf_m"],
                "core_m": row["core_m"],
                "SF_b_007": row["SF_b"],
                "SF_y": row["SF_y"],
                "least_SF_007": row["least_SF"],
                "governing_007": row["governing"],
            }

    materials = []
    for mat in prior["materials"]:
        materials.append({
            "name": mat["name"],
            "family": mat["family"],
            "density_kg_m3": mat["density_kg_m3"],
            "Gc_Pa": mat.get("Gc_used_for_compare_Pa"),
            "Ec_Pa": mat.get("Ec_Pa"),
            "tag": mat["tag"],
            "source": mat["source"],
        })

    # Which geometry each material is judged on. Same attachment as 007, plus P2-E
    # for the 16 kg/m3 honeycomb and for every core on the P2-E shape as a
    # what-if only when the density is the inherited 16.
    def geos_for(mat):
        named = min((32.0, 16.0, 8.0, 6.0, 4.0, 3.0, 2.0, 1.0), key=lambda rho: abs(rho - mat["density_kg_m3"]))
        names = [f"rho_{named}_{split}" for split in ("max_buckling_SF", "max_least_SF")]
        if abs(mat["density_kg_m3"] - 16.0) < 1e-9 or named == 16.0:
            names.insert(0, "P2-E")
        return names

    comparisons = []
    for mat in materials:
        if mat["Gc_Pa"] is None:
            comparisons.append({"material": mat["name"], "skipped": "no sourced shear modulus"})
            continue
        for gname in geos_for(mat):
            geo = geometries[gname]
            # Honeycomb uses 2.2-14, foam uses 2.2-5. Pass Ec only into the matching branch.
            ec_for_foam = mat["Ec_Pa"] if mat["family"] in ("PMI_foam", "PVC_foam") else None
            ev = evaluate(geo["tf_m"], geo["core_m"], mat["Gc_Pa"], ec_for_foam, E, nu, R, p_ext)
            if mat["family"] in ("PMI_foam", "PVC_foam"):
                ev.pop("honeycomb_wrinkling", None)
            elif mat["Ec_Pa"] is not None:
                honey = evaluate(geo["tf_m"], geo["core_m"], mat["Gc_Pa"], mat["Ec_Pa"], E, nu, R, p_ext)
                ev["honeycomb_wrinkling"] = honey["honeycomb_wrinkling"]
            else:
                ev.pop("honeycomb_wrinkling", None)
                ev.pop("foam_wrinkling", None)
            sf_y = geo["SF_y"]
            sf_g = ev["SF_general"]
            least = min(sf_g, sf_y)
            old_least = geo.get("least_SF_007", min(geo.get("SF_b_sealed", ev["SF_classical_kd_0_2"]), sf_y))
            comparisons.append({
                "material": mat["name"],
                "family": mat["family"],
                "density_kg_m3": mat["density_kg_m3"],
                "geometry": gname,
                "Gc_Pa": mat["Gc_Pa"],
                "Ec_Pa": mat["Ec_Pa"],
                "SF_y": sf_y,
                "SF_general": sf_g,
                "SF_classical": ev["SF_classical_kd_0_2"],
                "SF_ratio_general_over_classical": ev["SF_ratio_general_over_classical"],
                "least_of_general_and_yield": least,
                "least_007": old_least,
                "least_ratio": least / old_least,
                "Vc": ev["Vc"],
                "Kc": ev["Kc"],
                "gamma_d": ev["gamma_d"],
                "branch": ev["branch"],
                "crimp_pressure_ratio_handbook_over_advisory": ev["crimp_pressure_ratio_handbook_over_advisory"],
                "foam_wrinkling": ev.get("foam_wrinkling"),
                "honeycomb_wrinkling": ev.get("honeycomb_wrinkling"),
            })

    # G threshold at every 007 geometry, no material required.
    thresholds = []
    for gname, geo in geometries.items():
        dummy = evaluate(geo["tf_m"], geo["core_m"], 1e6, None, E, nu, R, p_ext)
        thresholds.append({
            "geometry": gname,
            "tf_m": geo["tf_m"],
            "core_m": geo["core_m"],
            "Gc_for_Vc_equals_2_Pa": dummy["Gc_for_Vc_equals_2_Pa"],
            "SF_classical": dummy["SF_classical_kd_0_2"],
        })

    doc = {
        "schema": 1,
        "card": "MAINLINE-007b",
        "unit": "vacuum-mainline007b-shear-wrinkle-1019",
        "status": "ESTIMATE",
        "tag": "QUESTIONABLE",
        "certification": "none",
        "started_at": STARTED,
        "ended_at": datetime.now().astimezone().isoformat(timespec="seconds"),
        "source": {
            "document": "NASA CR-1457, Manual for Structural Stability Analysis of Sandwich Plates and Shells, R. T. Sullins, G. F. Smith, E. E. Spier, General Dynamics, December 1969",
            "url": "https://ntrs.nasa.gov/citations/19700004831",
            "sphere_basis": "Section 6.2 restates J. C. Yao, Journal of the Aerospace Sciences, March 1962, as reformulated by F. J. Plantema, Sandwich Construction, Wiley, 1966. The equations used are the handbook's, read from the NTRS PDF.",
            "equations": ["6.2-2", "6.2-3", "6.2-4", "6.2-5", "6.2-6", "6.2-13", "6.2-25", "6.2-26", "6.2-27", "6.2-28", "6.2-29", "2.2-5", "2.2-6", "2.2-14", "2.2-15"],
        },
        "biaxial_factor": factor,
        "identity_infinite_G": "PASS",
        "P2E_classical_match": "PASS",
        "radius_note": "R is the external 10 m used by MAINLINE-007. The handbook's R is the middle-surface radius, smaller by h/2. That shift is not inside the reported ratios.",
        "knockdown_note": "gamma_d = 0.20 is the handbook value for hemispheres when Vc < 2. It is the same number as kd. On that branch the safety-factor ratio is Kc. A complete sphere has no edge. The handbook says the 0.20 rests on meager tests.",
        "comparisons": comparisons,
        "Gc_at_crimp_boundary": thresholds,
        "prior_results": str(PRIOR),
    }
    (ROOT / "RESULTS.json").write_text(json.dumps(doc, indent=1) + "\n")
    brief = []
    for row in comparisons:
        if row.get("skipped"):
            brief.append(row)
            continue
        brief.append({
            "material": row["material"],
            "geometry": row["geometry"],
            "Vc": row["Vc"],
            "Kc": row["Kc"],
            "branch": row["branch"],
            "SF_classical": row["SF_classical"],
            "SF_general": row["SF_general"],
            "ratio": row["SF_ratio_general_over_classical"],
            "least_ratio": row["least_ratio"],
            "SF_y": row["SF_y"],
            "wr_ratio": None if not row["foam_wrinkling"] else row["foam_wrinkling"]["SF_ratio_sourced_over_advisory"],
            "hc_SF": None if not row["honeycomb_wrinkling"] else row["honeycomb_wrinkling"]["SF_wr_equibiaxial"],
        })
    print(json.dumps({"biaxial_factor": factor, "rows": brief, "G_boundary_P2E": thresholds[0]}, indent=1))


if __name__ == "__main__":
    main()
