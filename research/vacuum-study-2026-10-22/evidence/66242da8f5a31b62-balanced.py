#!/usr/bin/env python3
"""MAINLINE-014. Balanced sandwich at the float ceiling, every mode at once.

Own arithmetic. Predecessor scripts are not executed. Formulas are the
MAINLINE-002 mass rules, the MAINLINE-007b reading of NASA CR-1457, and the
MAINLINE-007 crush target p/2. Nothing here is a certification.
"""

from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
ZONE = ZoneInfo("America/Los_Angeles")
R = 10.0
NU = 0.33
SYSTEMS = 100.0
JOINT = 0.05
P_EXT = 95460.83791390515
LIFT = 4889.442150186961
KD_HANDBOOK = 0.20
KD_BRIEF = 0.1407
AREA = 4.0 * math.pi * R * R
M_STRUCT = (LIFT - SYSTEMS) / (1.0 + JOINT)
GRID = 8000

CARD = Path(
    "unpublished-local-ref:2f68afa9c74ca674"
    "/.ship/artifacts/vacuum-overnight-briefs-1019/CARD-014-BALANCED-SANDWICH.md"
)
COMMON = Path(
    "unpublished-local-ref:2f68afa9c74ca674"
    "/.ship/artifacts/vacuum-overnight-briefs-1019/COMMON.md"
)
R008 = Path(
    "unpublished-local-ref:b5eced3bc27be18f"
    "/.ship/work/outputs/vacuum-mainline008-material-gap-1019/RESULTS.json"
)
R007 = Path(
    "unpublished-local-ref:7f7c51a246885c2d"
    "/.ship/work/outputs/vacuum-mainline007-core-trade-1019/RESULTS.json"
)
R007B = Path(
    "unpublished-local-ref:7f7c51a246885c2d"
    "/.ship/work/outputs/vacuum-mainline007b-shear-wrinkle-1019/RESULTS.json"
)
R003 = Path(
    "unpublished-local-ref:1a0c61fe133cc91e"
    "/.ship/work/outputs/vacuum-mainline003-p2-targets-owner1200-1019/RESULTS.json"
)
PINS = {
    CARD: ("5bc728f0b189a4a6844379d495cbba85db4d1b3516f9bb0c9ce86946f19b0a39", 2104),
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


def biaxial_factor() -> float:
    lo, hi = 0.0, 1.0
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if mid**3 + mid > 1.0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def require_pin(path: Path) -> None:
    expect_sha, expect_bytes = PINS[path]
    digest, size = sha_bytes(path)
    if digest != expect_sha or size != expect_bytes:
        raise SystemExit(f"pin mismatch {path.name} {digest} {size}")


def modes(face: dict, core: dict, tf: float, tc: float, kd: float, biax: float) -> dict:
    h = tc + tf
    root = math.sqrt(1.0 - NU * NU)
    young = face["E_Pa"]
    sigma_0 = young * h / (R * root)
    sigma_crimp = h * h * core["Gc_Pa"] / (2.0 * tf * tc)
    vc = sigma_0 / sigma_crimp
    if vc <= 2.0:
        kc = 1.0 - vc / 4.0
        gamma = kd
        branch = "stiff_or_moderate_core"
    else:
        kc = 1.0 / vc
        gamma = 1.0
        branch = "shear_crimping"
    membrane = P_EXT * R / (4.0 * tf)
    sfs = {
        "global_buckling": (4.0 * gamma * kc * sigma_0 * tf / R) / P_EXT,
        "face_yield": (4.0 * face["sigma_Pa"] * tf / R) / P_EXT,
        "core_shear_crimping": (4.0 * sigma_crimp * tf / R) / P_EXT,
        "core_crush": core["crush_Pa"] / (P_EXT / 2.0),
    }
    wrinkle = None
    if core["Ec_Pa"] is not None:
        if core["form"] == "foam":
            uni = 0.50 * (young * core["Ec_Pa"] * core["Gc_Pa"] / (1.0 - NU * NU)) ** (1.0 / 3.0)
        else:
            uni = 0.33 * young * math.sqrt(core["Ec_Pa"] * tf / (young * tc))
        wrinkle = biax * uni / membrane
        sfs["face_wrinkling"] = wrinkle
    ordered = sorted(sfs.items(), key=lambda item: (item[1], item[0]))
    # On the crimp branch the handbook global pressure is the crimp pressure.
    if branch == "shear_crimping":
        global_sf = sfs["global_buckling"]
        crimp_sf = sfs["core_shear_crimping"]
        if abs(global_sf - crimp_sf) <= 1e-9 * max(crimp_sf, 1e-30):
            ordered = [item for item in ordered if item[0] != "global_buckling"]
    return {
        "h_m": h,
        "tf_m": tf,
        "core_m": tc,
        "Vc": vc,
        "Kc": kc,
        "gamma": gamma,
        "branch": branch,
        "sfs": sfs,
        "face_wrinkling": wrinkle,
        "governing": ordered[0][0],
        "least_SF": ordered[0][1],
        "second_mode": ordered[1][0],
        "second_SF": ordered[1][1],
    }


def geometry(face: dict, core: dict, fraction: float) -> tuple[float, float]:
    core_mass = fraction * M_STRUCT
    face_mass = (1.0 - fraction) * M_STRUCT
    tc = core_mass / (AREA * core["rho"])
    tf = face_mass / (2.0 * AREA * face["rho"])
    return tf, tc


def optimize(face: dict, core: dict, kd: float, biax: float) -> dict:
    best = None
    for step in range(1, GRID):
        fraction = step / GRID
        tf, tc = geometry(face, core, fraction)
        ev = modes(face, core, tf, tc, kd, biax)
        if ev["face_wrinkling"] is None:
            raise SystemExit("eligible core missing wrinkling")
        key = (ev["least_SF"], ev["second_SF"])
        if best is None or key > best["key"]:
            best = {"key": key, "fraction": fraction, "ev": ev}
    ev = best["ev"]
    root = math.sqrt(1.0 - NU * NU)
    d_bal = (face["sigma_Pa"] / face["E_Pa"]) * R * root / kd
    return {
        "core_mass_fraction": best["fraction"],
        "tf_m": ev["tf_m"],
        "core_m": ev["core_m"],
        "h_m": ev["h_m"],
        "d_balance_m": d_bal,
        "h_over_d_balance": ev["h_m"] / d_bal,
        "Vc": ev["Vc"],
        "Kc": ev["Kc"],
        "gamma": ev["gamma"],
        "branch": ev["branch"],
        "sfs": ev["sfs"],
        "governing": ev["governing"],
        "least_SF": ev["least_SF"],
        "second_mode": ev["second_mode"],
        "second_SF": ev["second_SF"],
        "factor_to_SF_1": 1.0 / ev["least_SF"],
        "core_name": core["name"],
        "core_family": core["family"],
        "core_form": core["form"],
        "core_density_kg_m3": core["rho"],
        "core_tag": core["tag"],
    }


def scale(rho: float, base_rho: float, base_ec: float, base_gc: float, base_crush: float) -> dict:
    ratio = rho / base_rho
    return {
        "Ec_Pa": base_ec * ratio**2,
        "Gc_Pa": base_gc * ratio**2,
        "crush_Pa": base_crush * ratio**1.5,
    }


def build_cores() -> tuple[list[dict], list[dict]]:
    """Eligible cores, then aluminium honeycomb rows that have no Ec."""
    foam32 = {
        "name": "ROHACELL 31 IG-F",
        "family": "PMI_foam",
        "form": "foam",
        "rho": 32.0,
        "Ec_Pa": 17.0e6,
        "Gc_Pa": 13.0e6,
        "crush_Pa": 0.40e6,
        "tag": "QUESTIONABLE",
        "source": "MAINLINE-007 ROHACELL 31 IG-F, sourced",
    }
    aramid32 = {
        "name": "Hexcel HRH-10-4.8-32",
        "family": "aramid_honeycomb",
        "form": "honeycomb",
        "rho": 32.0,
        "Ec_Pa": 76.0e6,
        "Gc_Pa": 14.0e6,
        "crush_Pa": 1.00e6,
        "tag": "QUESTIONABLE",
        "source": "MAINLINE-007 Hexcel HRH-10-4.8-32, W shear, sourced",
    }
    eligible = [foam32, aramid32]
    for rho in (16.0, 8.0, 4.0):
        foam = scale(rho, 32.0, 17.0e6, 13.0e6, 0.40e6)
        eligible.append({
            "name": f"PMI foam scaled from ROHACELL 31 IG-F to {rho:g}",
            "family": "PMI_foam",
            "form": "foam",
            "rho": rho,
            "tag": "PROJECTION",
            "source": "density scaling from ROHACELL 31 IG-F: Ec and Gc as rho^2, crush as rho^1.5",
            **foam,
        })
        honey = scale(rho, 32.0, 76.0e6, 14.0e6, 1.00e6)
        eligible.append({
            "name": f"aramid honeycomb scaled from HRH-10-32 to {rho:g}",
            "family": "aramid_honeycomb",
            "form": "honeycomb",
            "rho": rho,
            "tag": "PROJECTION",
            "source": "density scaling from HRH-10-4.8-32: Ec and Gc as rho^2, crush as rho^1.5",
            **honey,
        })
    partial = [
        {
            "name": "Plascore PAMG-XR1 5052 3/16-2.0",
            "family": "aluminium_honeycomb",
            "form": "honeycomb",
            "rho": 32.0,
            "Ec_Pa": None,
            "Gc_Pa": 137895145.86336723,
            "crush_Pa": 1289319.6138224835,
            "tag": "QUESTIONABLE",
            "source": "MAINLINE-007, W shear. No compressive modulus on the sheet.",
        },
        {
            "name": "Plascore PAMG-XR1 5052 3/8-1.0",
            "family": "aluminium_honeycomb",
            "form": "honeycomb",
            "rho": 16.0,
            "Ec_Pa": None,
            "Gc_Pa": 48263301.05217853,
            "crush_Pa": 358527.3792447548,
            "tag": "QUESTIONABLE",
            "source": "MAINLINE-007, W shear. No compressive modulus on the sheet.",
        },
    ]
    return eligible, partial


def load_faces(doc: dict) -> list[dict]:
    faces = []
    for row in doc["candidates_ranked_by_least_SF_P2E"]:
        faces.append({
            "name": row["name"],
            "rho": float(row["rho"]),
            "E_Pa": float(row["E_GPa"]) * 1.0e9,
            "sigma_Pa": float(row["sigma_c_MPa"]) * 1.0e6,
            "tag": row["tag"],
            "source": row["source"],
            "p2e_least_SF_008": float(row["rows"]["P2-E"]["least_SF"]),
            "p2e_limiting_008": row["rows"]["P2-E"]["limiting_figure"],
        })
    return faces


def short(name: str) -> str:
    table = {
        "SiC (monolithic alpha SiC, Hexoloy SA type)": "SiC",
        "CNT-yarn composite quasi-isotropic": "CNT-yarn",
        "Graphene composite quasi-isotropic": "graphene",
        "CFRP quasi-isotropic M55J/epoxy": "M55J",
        "Beryllium S-200F": "Be S-200F",
        "CFRP quasi-isotropic K13D2U pitch/epoxy": "K13D2U",
        "Boron/epoxy quasi-isotropic": "boron/epoxy",
        "AlBeMet 162 (AM162, HIP)": "AlBeMet 162",
        "CFRP quasi-isotropic T700/epoxy": "T700",
        "Al-Li 2195-T8": "Al-Li 2195",
        "Ti-6Al-4V (annealed)": "Ti-6Al-4V",
        "6061-T6 (baseline)": "6061-T6",
        "7075-T6": "7075-T6",
        "Mg AZ31B": "Mg AZ31B",
        "Metallic glass Vitreloy 1 (Zr41.2Ti13.8Cu12.5Ni10Be22.5)": "Vitreloy 1",
    }
    return table.get(name, name)


def sentence(row: dict) -> str:
    return (
        f"{short(row['face'])} ({row['face_tag']}): least SF {g(row['least_SF'])} "
        f"governed by {row['governing']}, second {row['second_mode']} at {g(row['second_SF'])}. "
        f"Core {row['core_density_kg_m3']:g} kg/m3 {row['core_form']} ({row['core_tag']}), "
        f"tf {g(row['tf_m'])} m, core depth {g(row['core_m'])} m. "
        f"The factor 1/least SF is {g(row['factor_to_SF_1'])}."
    )


def main() -> None:
    for path in PINS:
        require_pin(path)
    r003 = json.loads(R003.read_text(encoding="utf-8"))
    r007 = json.loads(R007.read_text(encoding="utf-8"))
    r007b = json.loads(R007B.read_text(encoding="utf-8"))
    r008 = json.loads(R008.read_text(encoding="utf-8"))
    p2e = next(row for row in r003["rows"] if row["point_id"] == "P2-E")
    tf_e = p2e["geometry"]["tf_m"]
    tc_e = p2e["geometry"]["core_m"]
    if abs(r007["atmosphere"]["p_ext_Pa"] - P_EXT) > 0.0:
        raise SystemExit("007 pressure drifted")
    if abs(r007["atmosphere"]["lift_kg"] - LIFT) / LIFT > 1e-15:
        raise SystemExit("007 lift drifted")
    biax = biaxial_factor()
    if abs(biax - r007b["biaxial_factor"]) > 1e-12:
        raise SystemExit(f"biaxial factor {biax}")
    al = {"name": "6061-T6", "rho": 2700.0, "E_Pa": 68.9e9, "sigma_Pa": 276e6}
    tf_m, tc_m = geometry(al, {"rho": 16.0}, 0.5)
    if abs(tf_m - tf_e) / tf_e > 1e-12 or abs(tc_m - tc_e) / tc_e > 1e-12:
        raise SystemExit(f"P2-E mass identity failed {tf_m} {tc_m}")
    dummy = {
        "name": "infinite",
        "form": "foam",
        "rho": 16.0,
        "Ec_Pa": None,
        "Gc_Pa": 1.0e30,
        "crush_Pa": 1.0e30,
    }
    ident = modes(al, dummy, tf_e, tc_e, KD_HANDBOOK, biax)
    sealed = p2e["buckling_SF"]
    if abs(ident["sfs"]["global_buckling"] - sealed) / sealed > 1e-9:
        raise SystemExit(f"classical identity {ident['sfs']['global_buckling']}")
    if ident["branch"] != "stiff_or_moderate_core" or abs(ident["Kc"] - 1.0) > 1e-9:
        raise SystemExit("infinite-G branch failed")

    origin_path = ROOT / "ORIGIN.json"
    if origin_path.exists():
        origin = json.loads(origin_path.read_text(encoding="utf-8"))
    else:
        origin = {
            "origin_utc": datetime.now(ZONE).isoformat(timespec="microseconds"),
            "origin_monotonic_s": __import__("time").monotonic(),
        }
        origin_path.write_text(json.dumps(origin, indent=1) + "\n", encoding="utf-8")

    faces = load_faces(r008)
    wanted = {"SiC", "Be S-200F", "AlBeMet 162", "K13D2U", "M55J", "6061-T6", "CNT-yarn", "graphene"}
    have = {short(face["name"]) for face in faces}
    missing = wanted - have
    if missing:
        raise SystemExit(f"missing faces {sorted(missing)}")
    eligible, partial = build_cores()
    optima = []
    for face in faces:
        for kd in (KD_HANDBOOK, KD_BRIEF):
            best = None
            per_density = []
            for core in eligible:
                row = optimize(face, core, kd, biax)
                row["face"] = face["name"]
                row["face_tag"] = face["tag"]
                row["kd"] = kd
                row["gain_vs_008_P2E"] = row["least_SF"] / face["p2e_least_SF_008"]
                row["p2e_least_SF_008"] = face["p2e_least_SF_008"]
                row["p2e_limiting_008"] = face["p2e_limiting_008"]
                per_density.append({
                    "density": core["rho"],
                    "form": core["form"],
                    "tag": core["tag"],
                    "least_SF": row["least_SF"],
                    "governing": row["governing"],
                })
                key = (row["least_SF"], row["second_SF"])
                if best is None or key > (best["least_SF"], best["second_SF"]):
                    best = row
            best["per_density"] = per_density
            optima.append(best)

    def ranked(kd: float, tag: str | None) -> list[dict]:
        rows = [row for row in optima if row["kd"] == kd and (tag is None or row["face_tag"] == tag)]
        return sorted(rows, key=lambda row: row["least_SF"], reverse=True)

    top = ranked(KD_HANDBOOK, None)[:3]
    top_q = ranked(KD_HANDBOOK, "QUESTIONABLE")[:3]
    top_low = ranked(KD_BRIEF, None)[:3]
    be = next(row for row in optima if short(row["face"]) == "Be S-200F" and row["kd"] == KD_HANDBOOK)
    albe = next(row for row in optima if short(row["face"]) == "AlBeMet 162" and row["kd"] == KD_HANDBOOK)
    k13 = next(row for row in optima if short(row["face"]) == "K13D2U" and row["kd"] == KD_HANDBOOK)

    end_utc = datetime.now(ZONE).isoformat(timespec="microseconds")
    elapsed = __import__("time").monotonic() - origin["origin_monotonic_s"]
    results = {
        "schema": 1,
        "card": "MAINLINE-014",
        "unit": "vacuum-mainline014-balanced-sandwich-1019",
        "status": "ESTIMATE_PENDING_UNA",
        "tag": "QUESTIONABLE",
        "certification": False,
        "kd_handbook": KD_HANDBOOK,
        "kd_brief": KD_BRIEF,
        "nu_used_for_every_face": NU,
        "crush_target_Pa": P_EXT / 2.0,
        "structural_mass_kg": M_STRUCT,
        "checks": {
            "P2E_mass_identity": "PASS",
            "classical_kd_0_2_infinite_G": "PASS",
            "classical_SF": ident["sfs"]["global_buckling"],
            "biaxial_factor": biax,
            "atmosphere_from_007": "PASS",
        },
        "scaling": {
            "exponent_moduli": 2,
            "exponent_crush": 1.5,
            "bases": ["ROHACELL 31 IG-F at 32 kg/m3", "Hexcel HRH-10-4.8-32"],
            "tag": "PROJECTION",
            "mainline_013": "not filed",
        },
        "partial_cores_excluded": [
            {"name": row["name"], "reason": "no sourced Ec, wrinkling unscored"} for row in partial
        ],
        "optima": optima,
        "best_three_kd_0_20": [short(row["face"]) for row in top],
        "best_three_questionable_kd_0_20": [short(row["face"]) for row in top_q],
        "best_three_kd_0_1407": [short(row["face"]) for row in top_low],
        "strength_limited_gains_vs_008_P2E": {
            "Be S-200F": be["gain_vs_008_P2E"],
            "AlBeMet 162": albe["gain_vs_008_P2E"],
            "K13D2U": k13["gain_vs_008_P2E"],
        },
        "measurements": {
            "origin_utc": origin["origin_utc"],
            "end_utc": end_utc,
            "elapsed_s": elapsed,
        },
    }
    (ROOT / "RESULTS.json").write_text(json.dumps(results, indent=1) + "\n", encoding="utf-8")

    nfi = {
        "rows": [
            {
                "id": "NFI-NU",
                "note": "Every face uses nu 0.33 from the aluminium case. MAINLINE-008 published no Poisson ratio. CFRP, SiC and beryllium are not aluminium.",
            },
            {
                "id": "NFI-KD-01407",
                "note": "0.1407 replaces the handbook gamma 0.20 on the stiff branch only. It is the brief's single figure, not a fresh SP-8032 knockdown at the optimum thickness.",
            },
            {
                "id": "NFI-SCALE",
                "note": "Densities 16, 8 and 4 have no fully sourced core in MAINLINE-007. Ec and Gc scale as rho^2 and crush strength as rho^1.5 from the 32 kg/m3 sourced row. PROJECTION.",
            },
            {
                "id": "NFI-013",
                "note": "MAINLINE-013 has not filed. Its cores are not used.",
            },
            {
                "id": "NFI-ALHC",
                "note": "Both Plascore aluminium honeycombs lack Ec. Wrinkling is unscored, so they are excluded from the optimum.",
            },
            {
                "id": "NFI-CRUSH",
                "note": "Core crush is compressive strength over p/2. Thickness does not enter. The target is the MAINLINE-007 reading of about p/2.",
            },
            {
                "id": "NFI-HEMISPHERE",
                "note": "Handbook gamma 0.20 is the CR-1457 hemisphere value. A complete sphere has no edge. MAINLINE-007b already recorded that the 0.20 rests on meager tests.",
            },
            {
                "id": "NFI-FACTOR",
                "note": "1/least SF is the safety-factor gap. It is the property multiple only when that mode scales in proportion to the named property. Wrinkling scales as a cube root or a square root.",
            },
        ]
    }
    (ROOT / "NFI.json").write_text(json.dumps(nfi, indent=1) + "\n", encoding="utf-8")
    inputs = {
        "pins": [pin(path) for path in (CARD, COMMON, R008, R007, R007B, R003)],
        "nu": NU,
        "p_ext_Pa": P_EXT,
        "lift_kg": LIFT,
        "cores_eligible": eligible,
        "cores_partial": partial,
        "faces": [
            {"name": face["name"], "rho": face["rho"], "E_Pa": face["E_Pa"], "sigma_Pa": face["sigma_Pa"], "tag": face["tag"]}
            for face in faces
        ],
    }
    (ROOT / "INPUTS.json").write_text(json.dumps(inputs, indent=1) + "\n", encoding="utf-8")

    lines = [
        "# MAINLINE-014 balanced sandwich — ESTIMATE_PENDING_UNA",
        "",
        "QUESTIONABLE. Not a certification. The float ceiling is the MAINLINE-002 sandwich mass rule at margin 0: joints are 5 percent of the sandwich and systems are 100 kg. External pressure is 95460.83791390515 Pa and lift is 4889.442150186961 kg. Every face uses nu 0.33.",
        "",
        "Global buckling is the NASA CR-1457 shear trim from MAINLINE-007b. On the stiff branch gamma is the knockdown, 0.20 or 0.1407. On the shear-crimping branch gamma stays 1. Face yield is 4*sigma*tf/R. Wrinkling is the CR-1457 foam form or the honeycomb form, with the equibiaxial factor. Core shear crimping is the handbook pressure. Core crush is strength over p/2. The least safety factor is the minimum of those five.",
        "",
        f"Checks passed. Equal face and core mass at 16 kg/m3 recovers the sealed P2-E thicknesses. Infinite shear modulus at knockdown 0.20 recovers buckling SF {g(sealed)}. The biaxial factor is {g(biax)}.",
        "",
        "Sourced cores are ROHACELL 31 IG-F and Hexcel HRH-10 at 32 kg/m3. Densities 16, 8 and 4 scale Ec and Gc as rho squared and crush as rho to the 1.5, tagged PROJECTION. MAINLINE-013 has not filed. Aluminium honeycomb has no Ec and is excluded.",
        "",
        "Best three at knockdown 0.20, by least safety factor:",
    ]
    for row in top:
        lines.append("")
        lines.append(sentence(row))
    lines.extend([
        "",
        "Best three QUESTIONABLE faces, excluding PROJECTION faces:",
    ])
    for row in top_q:
        lines.append("")
        lines.append(sentence(row))
    lines.extend([
        "",
        "Best three at knockdown 0.1407, re-optimised rather than scaled:",
    ])
    for row in top_low:
        lines.append("")
        lines.append(sentence(row))
    al6061 = next(row for row in optima if short(row["face"]) == "6061-T6" and row["kd"] == KD_HANDBOOK)
    lines.extend([
        "",
        (
            "The 0.1407 rows match the 0.20 rows on the winners. Those optima sit on the shear-crimping branch, "
            "where the handbook sets gamma to 1, so the knockdown does not enter the safety factor."
        ),
        "",
        (
            f"Against the sealed-geometry MAINLINE-008 P2-E least safety factor, the optimised gain is "
            f"{g(be['gain_vs_008_P2E'])} for Be S-200F, {g(albe['gain_vs_008_P2E'])} for AlBeMet 162 "
            f"and {g(k13['gain_vs_008_P2E'])} for K13D2U. "
            f"The robotics estimate of roughly 1.7 for beryllium is high: the computed gain is {g(be['gain_vs_008_P2E'])}. "
            "Shear crimping binds before the yield-buckling depth, so that depth is not the optimum. "
            f"6061-T6 stays at least SF {g(al6061['least_SF'])}, crimp against wrinkling, "
            f"on a projected {al6061['core_density_kg_m3']:g} kg/m3 honeycomb."
        ),
        "",
        (
            f"Start {origin['origin_utc']}. End {end_utc}. Elapsed {elapsed} s, a measurement. "
            "The 2026-10-20T07:00:00-07:00 deadline is a door check-in."
        ),
        "",
    ])
    (ROOT / "CARD.md").write_text("\n".join(lines), encoding="utf-8")
    print("faces", len(faces), "optima", len(optima))
    print("top20", [(short(row["face"]), g(row["least_SF"]), row["governing"], row["core_form"], row["core_density_kg_m3"], row["core_tag"], g(row["factor_to_SF_1"]), g(row["second_SF"]), row["second_mode"]) for row in top])
    print("topQ", [(short(row["face"]), g(row["least_SF"]), row["governing"]) for row in top_q])
    print("top1407", [(short(row["face"]), g(row["least_SF"]), row["governing"], row["core_form"], row["core_density_kg_m3"]) for row in top_low])
    watch = {"CNT-yarn", "Be S-200F", "graphene", "K13D2U", "AlBeMet 162", "SiC", "M55J", "6061-T6"}
    for row in optima:
        if row["kd"] == KD_HANDBOOK and short(row["face"]) in watch:
            print(
                short(row["face"]),
                row["face_tag"],
                row["branch"],
                g(row["least_SF"]),
                row["governing"],
                g(row["second_SF"]),
                row["second_mode"],
                row["core_form"],
                row["core_density_kg_m3"],
                g(row["h_over_d_balance"]),
                {name: g(value) for name, value in row["sfs"].items()},
            )
    print("gains", g(be["gain_vs_008_P2E"]), g(albe["gain_vs_008_P2E"]), g(k13["gain_vs_008_P2E"]))
    print("be", g(be["h_over_d_balance"]), be["branch"], g(be["tf_m"]), g(be["core_m"]))
    print("elapsed", elapsed)


if __name__ == "__main__":
    main()
