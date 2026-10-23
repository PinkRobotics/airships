#!/usr/bin/env python3
"""MAINLINE-018. Does a knockdown apply on the shear-crimp branch?

Own arithmetic. Predecessor scripts are not executed. Geometries are held.
Nothing here is a certification.
"""

from __future__ import annotations

import hashlib
import json
import math
import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ZONE = ZoneInfo("America/Los_Angeles")
ROOT = Path(__file__).resolve().parent
STARTED = sys.argv[1]

R14 = Path(
    "unpublished-local-ref:1a0c61fe133cc91e"
    "/.ship/work/outputs/vacuum-mainline014-balanced-sandwich-1019/RESULTS.json"
)
K09 = Path(
    "unpublished-local-ref:7f7c51a246885c2d"
    "/.ship/work/outputs/vacuum-mainline009b-kc-all-levels-1019/KC-LEVELS.json"
)
CARD = Path(
    "unpublished-local-ref:2f68afa9c74ca674"
    "/.ship/artifacts/vacuum-overnight-briefs-1019/CARD-018-CRIMP-BRANCH-KNOCKDOWN.md"
)
COMMON = Path(
    "unpublished-local-ref:2f68afa9c74ca674"
    "/.ship/artifacts/vacuum-overnight-briefs-1019/COMMON.md"
)
CR = Path("unpublished-local-ref:993e7648efa339d0")
WAGNER = Path("unpublished-local-ref:717949c3dcf7d36e")
EUCASS = Path(
    "unpublished-local-ref:ref-2ea7bf366999327844ca"
)
PINS = {
    CARD: ("d144f70add045e2cb112512bc6d41579d51b679bbd1247186ecce640e32f16c4", 1928),
    COMMON: ("8f359d6c04f84d158ccc232173cb61e86eeede3797fe362d8212066a096f94b5", 5874),
}


def g(x: float) -> str:
    return format(x, ".12g")


def sha_bytes(path: Path) -> tuple[str, int]:
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest(), len(data)


def pin(path: Path) -> dict:
    digest, size = sha_bytes(path)
    return {"path": str(path), "sha256": digest, "bytes": size}


def require_pin(path: Path) -> None:
    expect_sha, expect_bytes = PINS[path]
    digest, size = sha_bytes(path)
    if digest != expect_sha or size != expect_bytes:
        raise SystemExit(f"pin mismatch {path.name} {digest} {size}")


def gamma_optimistic(vc: float) -> float:
    """PROJECTION. Linear bridge between the handbook endpoints.

    0.20 at Vc = 0 (maximum imperfection sensitivity) and 1 at Vc >= 2
    (the unity claim). CR-1457 says this transition is beyond its scope.
    """
    return 0.20 + 0.40 * min(vc, 2.0)


def gamma_conservative(vc: float) -> float:
    """QUESTIONABLE. Hemisphere factor 0.20 at every Vc.

    The crimp exception is withheld. Equation 6.2-13, not a new fit.
    """
    return 0.20


def gamma_handbook_page(vc: float) -> float:
    """Page 6-12 reading: Yd = 1 at Vc >= 2, else 0.20. Not a continuous curve."""
    return 1.0 if vc >= 2.0 else 0.20


def govern(modes: dict, branch: str) -> dict:
    """Least mode.

    On the shear-crimp branch the design global pressure is gamma times the
    bare crimp pressure. That allowable is named core_shear_crimping, which
    is MAINLINE-014's name when the two are equal. Bare crimp stays in the
    mode list. It does not outrank the reduced allowable.
    """
    global_sf = modes["global_buckling"]
    crimp_sf = modes["core_shear_crimping"]
    design = dict(modes)
    names_crimp = (
        branch == "shear_crimping"
        and global_sf <= crimp_sf + 1e-9 * max(crimp_sf, 1e-30)
    )
    if names_crimp:
        design.pop("global_buckling")
        design["core_shear_crimping"] = global_sf
    ordered = sorted(design.items(), key=lambda item: (item[1], item[0]))
    return {
        "modes": modes,
        "bare_crimp_SF": crimp_sf,
        "design_global_SF": global_sf,
        "governing": ordered[0][0],
        "least_SF": ordered[0][1],
        "second_mode": ordered[1][0],
        "second_SF": ordered[1][1],
        "factor_to_SF_1": 1.0 / ordered[0][1],
        "crimp_allowable": "gamma(Vc) * Kc * sigma_0. On the shear-crimp branch this equals gamma(Vc) times the bare crimp stress.",
    }


def rescore(label: str, vc: float, branch: str, gamma_old: float, sfs: dict, meta: dict) -> dict:
    out = {"label": label, "Vc": vc, "branch": branch, "gamma_filed": gamma_old, **meta}
    curves = {}
    for name, fn in (
        ("optimistic", gamma_optimistic),
        ("conservative", gamma_conservative),
    ):
        gamma = fn(vc)
        modes = dict(sfs)
        modes["global_buckling"] = sfs["global_buckling"] * (gamma / gamma_old)
        scored = govern(modes, branch)
        curves[name] = {"gamma": gamma, "tag": "PROJECTION" if name == "optimistic" else "QUESTIONABLE", **scored}
    out["curves"] = curves
    return out


def sim_vc() -> dict:
    """EUCASS 2023-367 Figure 4, the geometry Sim et al. 2024 analyse.

    Outer radius 42.80 mm, foam 3.10 mm, outer sheet 0.42 mm.
    Inner sheet 0.42 mm (flat) or 0.40 mm (dimple).
    Steel E 210 GPa, nu 0.33. Foam E 0.04 GPa, nu 0. Gc is not stated.
    G = E / (2 * (1 + nu)) = 20 MPa.
    """
    e_face = 210.0e9
    nu = 0.33
    e_core = 0.04e9
    nu_core = 0.0
    gc = e_core / (2.0 * (1.0 + nu_core))
    r_outer = 42.80e-3
    t_outer = 0.42e-3
    t_core = 3.10e-3
    root = math.sqrt(1.0 - nu * nu)
    rows = {}
    for name, t_inner in (("flat", 0.42e-3), ("dimple", 0.40e-3)):
        h = t_core + 0.5 * (t_outer + t_inner)
        t_total = t_outer + t_core + t_inner
        r_mid = r_outer - 0.5 * t_total
        sigma_0 = e_face * h / (r_mid * root)
        sigma_crimp = h * h * gc / ((t_outer + t_inner) * t_core)
        vc = sigma_0 / sigma_crimp
        # sigma_crimp scales with Gc and Vc scales as 1/Gc, so Gc(Vc=2) = Gc * Vc / 2.
        gc_at_vc_2 = gc * vc / 2.0
        rows[name] = {
            "t_outer_m": t_outer,
            "t_inner_m": t_inner,
            "t_core_m": t_core,
            "h_m": h,
            "R_outer_m": r_outer,
            "R_middle_m": r_mid,
            "R_over_tc": r_mid / t_core,
            "sigma_0_Pa": sigma_0,
            "sigma_crimp_Pa": sigma_crimp,
            "Vc": vc,
            "branch_if_handbook": "shear_crimping" if vc > 2.0 else "stiff_or_moderate_core",
            "Gc_for_Vc_eq_2_Pa": gc_at_vc_2,
            "published_kdf_imperfect_over_perfect_fea": 0.22 if name == "flat" else 0.20,
        }
    return {
        "source_geometry": "EUCASS 2023-367 Figure 4, doi 10.13009/EUCASS2023-367",
        "source_kdf": "Sim, Lee, Kim, Park and Lee, Int. J. Aerospace Engineering, 2024, doi 10.1155/2024/8765733",
        "kdf_denominator": "Their own perfect-shell linear buckling load, not the CR-1457 allowable. Numerical, not a test.",
        "Gc_Pa": gc,
        "Gc_basis": "Isotropic conversion G = E/(2*(1+nu)) from the stated foam modulus 0.04 GPa and Poisson 0. The paper does not state Gc.",
        "rows": rows,
    }


def main() -> None:
    require_pin(CARD)
    require_pin(COMMON)
    r14 = json.loads(R14.read_text())
    k09 = json.loads(K09.read_text())
    wanted = {
        "Be S-200F / HRH-10": ("Beryllium S-200F", "Hexcel HRH-10-4.8-32"),
        "K13D2U / HRH-10": ("CFRP quasi-isotropic K13D2U pitch/epoxy", "Hexcel HRH-10-4.8-32"),
        "AlBeMet 162 / HRH-10": ("AlBeMet 162 (AM162, HIP)", "Hexcel HRH-10-4.8-32"),
    }
    rows = []
    for label, (face, core) in wanted.items():
        matches = [
            row
            for row in r14["optima"]
            if row["face"] == face and row["core_name"] == core and row["kd"] == 0.2
        ]
        if len(matches) != 1:
            raise SystemExit(f"{label} matches {len(matches)}")
        row = matches[0]
        if row["branch"] != "shear_crimping":
            raise SystemExit(f"{label} branch {row['branch']}")
        if abs(row["sfs"]["global_buckling"] - row["sfs"]["core_shear_crimping"]) > 1e-9:
            raise SystemExit(f"{label} global and crimp differ under the filed gamma")
        rows.append(
            rescore(
                label,
                row["Vc"],
                row["branch"],
                row["gamma"],
                row["sfs"],
                {
                    "source": "MAINLINE-014 optima, kd 0.2, geometry held",
                    "tf_m": row["tf_m"],
                    "core_m": row["core_m"],
                    "Kc": row["Kc"],
                    "filed_least_SF": row["least_SF"],
                    "filed_governing": row["governing"],
                    "margin": 0.0,
                    "face_tag": row["face_tag"],
                    "core_tag": row["core_tag"],
                },
            )
        )
    design = k09["levels_design_Q_0.50"]["0.20"]
    sic = rescore(
        "SiC / Divinycell H35",
        k09["fix"]["Vc"],
        k09["fix"]["branch"],
        k09["fix"]["gamma_d"],
        design["modes"],
        {
            "source": "MAINLINE-009b design Q 0.50 at knockdown 0.20, geometry held",
            "tf_m": k09["geometry"]["tf_m"],
            "core_m": k09["geometry"]["core_m"],
            "Kc": k09["fix"]["Kc"],
            "filed_least_SF": design["least_SF"],
            "filed_governing": design["governing"],
            "margin": 0.05,
            "wrinkle_Q": 0.5,
            "note": "Already on the moderate branch. A flat 0.20 curve does not move it.",
        },
    )
    rows.append(sic)
    sim = sim_vc()
    # Plausible foam shear cannot cross Vc = 2: threshold is tens of times E.
    for name, row in sim["rows"].items():
        if row["Vc"] <= 2.0:
            raise SystemExit(f"Sim {name} Vc unexpectedly <= 2")
    wagner = WAGNER.read_text(errors="replace").lower()
    if "sandwich" in wagner:
        raise SystemExit("Wagner extract contains sandwich; re-read before claiming none")
    ended = datetime.now(ZONE).isoformat(timespec="seconds")
    results = {
        "schema": 1,
        "card": "MAINLINE-018",
        "unit": "vacuum-mainline018-crimp-branch-kd-1019",
        "status": "ESTIMATE",
        "tag": "QUESTIONABLE",
        "certification": "none",
        "started_at": STARTED,
        "ended_at": ended,
        "question": "Does a knockdown apply on the shear-crimp branch?",
        "answer": "The handbook applies gamma 1 for Vc >= 2 and says a continuous transition is beyond its scope. Two estimate curves are scored here. The optimistic curve keeps gamma 1 on that branch. The conservative curve keeps 0.20. Neither is a test fit.",
        "handbook": {
            "document": "NASA CR-1457, Sullins, Smith and Spier, 1969",
            "url": "https://ntrs.nasa.gov/citations/19700004831",
            "local_extract": str(CR),
            "theory": "Section 6.2. Yao, Journal of the Aerospace Sciences, March 1962, ref 6-1, reformulated by Plantema, Sandwich Construction, Wiley, 1966, ref 6-2.",
            "step": "Section 6.2.2, page 6-12. Vc < 2: Yd = 0.20 for hemispheres and 0.35 for ellipsoids and torispheres. Vc >= 2: Yd = 1 for those domes.",
            "kc_boundary": "Kc is 1 - Vc/4 for Vc <= 2 and 1/Vc for Vc > 2. Both give 1/2 at Vc = 2, so Kc is continuous. Yd is not.",
            "implementation_note": "MAINLINE-014 puts the gamma step on Vc > 2, with the Kc inequality. Page 6-12 puts Yd = 1 at Vc >= 2. No rescored row is exactly Vc = 2.",
            "why_unity": "Page 6-7. Sensitivity decreases as Vc goes from 0 to 2. Weak-core constructions are said not to be influenced by initial imperfections, so a knockdown of unity can be applied. A continuous transitional knockdown is beyond the scope of the handbook.",
            "dome_tests": "Section 6.2.1.2. Data very scarce. Gonzalez and Patton, North American Rockwell report SDL 468, May 1964, ref 6-4, Saturn S-II 55-inch bulkheads. Recommended 0.20 except where shear crimping occurs. The method is called best-available and not very reliable.",
            "cylinder_weak_core": "Section 4.2, Figs 4.2-4 and 4.2-5, refs 4-2 (March and Kuenzi, FPL 1830, revised December 1957) and 4-11 (Hexcel Products status summary, 25 July 1963). Axial compression, not external pressure. All but one test exceed the gamma-1 prediction. The exception is 0.86 of predicted. Individual Vc values are not tabulated. Class is Vc >= 2. Section 2.3 says no knockdown is required because crimping is insensitive, and that neglecting face bending is conservative and can be considerable.",
            "transfer": "QUESTIONABLE. Cylinder axial tests and a theory claim are not a sphere series at Vc > 2.",
        },
        "curves": {
            "optimistic": {
                "gamma": "0.20 + 0.40 * min(Vc, 2)",
                "at_0": 0.20,
                "at_and_above_2": 1.0,
                "tag": "PROJECTION",
                "source": "Handbook endpoints on page 6-7. The linear bridge is not in the handbook.",
                "multiplies_crimp_branch": False,
            },
            "conservative": {
                "gamma": "0.20",
                "tag": "QUESTIONABLE",
                "source": "Equation 6.2-13 extended onto Vc >= 2. The crimp exception is withheld.",
                "multiplies_crimp_branch": True,
                "how": "Design pressure is gamma(Vc) * Kc * (4*tf/R) * sigma_0. On the crimp branch that equals gamma times the bare crimp pressure. Bare crimp, face, crush and wrinkling are not otherwise changed. gamma replaces kd. It is not stacked on 0.20, 0.90 or 0.1407.",
            },
            "not_scored": "The handbook step itself is the discontinuous rule, not one of the two continuous curves. A third curve at 0.86 is not scored. That 0.86 is one axial cylinder, not a sphere fit.",
        },
        "tests": {
            "sim_2024": sim,
            "wagner_2020": {
                "doi": "10.1016/j.ijpvp.2019.104015",
                "extract": str(WAGNER),
                "sandwich_rows": "none. The extract has no occurrence of sandwich. Table 3 is monocoque spherical shells, including PVC and aluminium. No sandwich Vc is computed from it.",
                "carried_from_004b": "Equation 7 about 0.2 for elastic monocoque shells, deep-dome bound 0.21, Krenzke and Kiernan KDF 0.11 to 0.90. QUESTIONABLE if transferred onto this sandwich.",
            },
            "sp_8032": "Monocoque doubly curved shells. The monograph PDF was not retrieved. The cap rho = 0.14 + 3.2/lambda^2 is not a sandwich Vc curve. QUESTIONABLE transfer, already filed on MAINLINE-004.",
            "sp_8007": "CR-1457 ref 4-4 is NASA SP-8007, September 1965, Buckling of Thin-Walled Circular Cylinders. The monograph was not opened. It is a cylinder document. No sandwich-sphere Vc series was taken from it.",
            "plantema": "Not opened. Used only as CR-1457 ref 6-2 and ref 4-12.",
            "imperfection_analyses": "No separate sandwich-sphere gamma(Vc) analysis with a DOI was opened. The sourced sensitivity statement is CR-1457 page 6-7. Sim 2024 is a numerical dimple study and does not report Vc.",
        },
        "rescore": rows,
        "p3": "PENDING-011b. Not scored.",
        "cnt": "Not the point.",
        "geometry": "Held. No thickness search.",
    }
    (ROOT / "RESULTS.json").write_text(json.dumps(results, indent=1) + "\n")
    inputs = {
        "schema": 1,
        "card": "MAINLINE-018",
        "pins": [pin(path) for path in (CARD, COMMON, CR, WAGNER, EUCASS, R14, K09)],
        "brief_pins_checked": "CARD-018 and COMMON.md match the wake pins.",
        "glm_partial": "ref-c713c40ee838487ac6d3 has no vacuum-mainline018-crimp-branch-kd-1019 directory.",
    }
    (ROOT / "INPUTS.json").write_text(json.dumps(inputs, indent=1) + "\n")
    nfi = {
        "schema": 1,
        "card": "MAINLINE-018",
        "open": [
            {
                "NFI_id": "NFI-CRIMP-UNITY",
                "gap": "No sandwich-sphere test series at Vc > 2 was read. Unity rests on the handbook's imperfection claim plus axial cylinder tests, one of which reached 0.86 of the prediction.",
                "tag": "QUESTIONABLE",
            },
            {
                "NFI_id": "NFI-SIM-GC",
                "gap": "Sim 2024 does not state Gc. Vc uses G = E/2 from the stated foam modulus and Poisson 0. Their 0.20 and 0.22 are imperfect-over-perfect finite-element ratios, not tests against CR-1457.",
                "tag": "QUESTIONABLE",
            },
            {
                "NFI_id": "NFI-CONTINUOUS",
                "gap": "The optimistic line is a projection. The handbook declined to publish a transitional knockdown.",
                "tag": "PROJECTION",
            },
            {
                "NFI_id": "NFI-P3-PENDING-011b",
                "gap": "P3 lattice buckling and member bending remain unscored.",
                "tag": "QUESTIONABLE",
            },
        ],
    }
    (ROOT / "NFI.json").write_text(json.dumps(nfi, indent=1) + "\n")
    print(ended)
    for row in rows:
        print(row["label"], "Vc", g(row["Vc"]))
        for name, curve in row["curves"].items():
            print(
                " ",
                name,
                "gamma",
                g(curve["gamma"]),
                "least",
                g(curve["least_SF"]),
                curve["governing"],
                "second",
                curve["second_mode"],
                g(curve["second_SF"]),
            )
    for name, row in sim["rows"].items():
        print(
            "sim",
            name,
            "Vc",
            g(row["Vc"]),
            "R/tc",
            g(row["R_over_tc"]),
            "Gc_at_2_GPa",
            g(row["Gc_for_Vc_eq_2_Pa"] / 1e9),
        )


if __name__ == "__main__":
    main()
