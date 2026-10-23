#!/usr/bin/env python3
"""MAINLINE-014b. Metal honeycomb added to the 014 balanced sandwich.

Own arithmetic. The 014 script is not executed. Formulas are the 014 reading
of NASA CR-1457, plus the brief's intracell-dimpling stress. W shear is Gc.
Nothing here is a certification.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import time
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
PSI = 6894.757293168361
KSI = PSI * 1000.0
PCF_TO_KG = 0.45359237 / (0.3048**3)
K_FOAM = 0.50
K_HONEY = 0.33
K_THEORY = 0.82
CELL_M = {
    "1/8": 0.0254 / 8.0,
    "5/32": 0.0254 * 5.0 / 32.0,
    "3/16": 0.0254 * 3.0 / 16.0,
    "1/4": 0.0254 / 4.0,
    "3/8": 0.0254 * 3.0 / 8.0,
}

CARD = Path(
    "unpublished-local-ref:2f68afa9c74ca674"
    "/.ship/artifacts/vacuum-overnight-briefs-1019/CARD-014b-METAL-HONEYCOMB.md"
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
R014 = Path(
    "unpublished-local-ref:1a0c61fe133cc91e"
    "/.ship/work/outputs/vacuum-mainline014-balanced-sandwich-1019/RESULTS.json"
)
PDFS = {
    Path("unpublished-local-ref:951dae7dbde87d65"): (
        "0467f718f7d9d3a175635718573f94f58baea1d753e83db4be8edcba9f374034",
        "https://www.hexcel.com/wp-content/uploads/2025/12/HexWeb_CRIII_DataSheet.pdf",
    ),
    Path("unpublished-local-ref:520d93dc2201e43f"): (
        "5a88084e6f95eb23bab2f7068de6f07d75dc6c093e2c0fc881fe84cf515d94a9",
        "http://plascore.com/wp-content/uploads/dlm_uploads/2025/08/PLA_PAMG-XR1-5052_2023-06-02.pdf",
    ),
    Path("unpublished-local-ref:ad6f653b2469389b"): (
        "cecf9aadb972fddcb296f534dea37f5bfabf6273217ba4343be2a3ae17bb65c3",
        "https://www.hexcel.com/wp-content/uploads/2026/01/HexWebHoneycombAttributesandProperties-1.pdf",
    ),
}
PINS = {
    CARD: ("5eba8ace2bbd32f10f10ca6d110f8990bc0c4b78c1d11acfaca9816cedff6fc2", 1840),
    COMMON: ("8f359d6c04f84d158ccc232173cb61e86eeede3797fe362d8212066a096f94b5", 5874),
    R014: ("0e2d7bf61d20e6ee2316d545ba53d8a850378379ff126a95ce8cae8181df0eb8", 85107),
}

# cell, pcf, Ec ksi, crush psi, L strength psi, L modulus ksi, W strength psi, W modulus ksi.
# CR-III typical columns. Crush is the sheet's crush column.
CRIII_5052 = [
    ("1/8", "3.1", "75", "130", "210", "45.0", "130", "22.0"),
    ("5/32", "2.6", "55", "90", "165", "37.0", "100", "19.0"),
    ("5/32", "3.8", "110", "185", "270", "56.0", "165", "26.4"),
    ("3/16", "2.0", "34", "60", "120", "27.0", "70", "14.3"),
    ("3/16", "3.1", "75", "130", "210", "45.0", "125", "22.0"),
    ("1/4", "1.6", "20", "40", "85", "21.0", "50", "11.0"),
    ("1/4", "2.3", "45", "75", "140", "32.0", "85", "16.2"),
    ("1/4", "3.4", "90", "150", "230", "50.0", "140", "24.0"),
    ("3/8", "1.0", "10", "25", "45", "12.0", "30", "7.0"),
    ("3/8", "1.6", "20", "40", "85", "21.0", "50", "11.0"),
    ("3/8", "2.3", "45", "75", "135", "32.0", "80", "16.2"),
    ("3/8", "3.0", "70", "120", "200", "43.0", "125", "21.2"),
    ("3/8", "3.7", "105", "180", "250", "55.0", "160", "26.0"),
]
CRIII_5056 = [
    ("1/8", "3.1", "97", "170", "250", "45.0", "155", "20.0"),
    ("5/32", "2.6", "70", "120", "200", "37.0", "115", "17.0"),
    ("5/32", "3.8", "140", "235", "335", "57.0", "195", "24.0"),
    ("3/16", "2.0", "45", "75", "140", "27.0", "85", "13.0"),
    ("3/16", "3.1", "97", "170", "265", "45.0", "150", "20.0"),
    ("1/4", "1.6", "30", "50", "90", "20.0", "60", "10.5"),
    ("1/4", "2.3", "58", "100", "180", "32.0", "100", "15.0"),
    ("1/4", "3.4", "115", "200", "290", "50.0", "175", "22.0"),
    ("3/8", "1.0", "15", "35", "55", "15.0", "35", "6.8"),
    ("3/8", "1.6", "30", "50", "90", "20.0", "60", "10.5"),
    ("3/8", "2.3", "58", "100", "170", "32.0", "95", "15.0"),
    ("3/8", "3.0", "92", "160", "245", "43.0", "145", "19.0"),
]
# Plascore typical psi/ksi. No Ec and no crush column. rho is the printed kg/m3.
# bare compressive psi is the crush the brief names. Ec is filled from CR-III 5052.
PLASCORE = [
    ("1/8", "3.1", "50", "310", "225", "50", "123", "26"),
    ("3/16", "2.0", "32", "187", "150", "34", "80", "20"),
    ("3/16", "3.1", "50", "346", "218", "51", "127", "27"),
    ("5/32", "2.6", "42", "242", "150", "38", "100", "24"),
    ("5/32", "3.8", "61", "436", "215", "58", "175", "32"),
    ("1/4", "1.6", "26", "108", "88", "24", "45", "12"),
    ("1/4", "2.3", "37", "218", "130", "32", "95", "18"),
    ("1/4", "3.4", "54", "364", "232", "54", "130", "26"),
    ("3/8", "1.0", "16", "52", "45", "10", "30", "7"),
    ("3/8", "2.3", "37", "197", "145", "30", "77", "16"),
    ("3/8", "3.0", "48", "314", "209", "44", "110", "24"),
    ("3/8", "3.7", "59", "420", "245", "55", "125", "26"),
]
# HFT: stabilised strength, stabilised modulus, L, W. No separate crush column.
HFT = [
    ("1/8", "3.0", "23.0", "350", "195", "19.0", "95", "7.5"),
    ("1/8", "4.0", "46.0", "560", "315", "25.0", "150", "12.0"),
    ("3/16", "2.0", "17.0", "170", "115", "15.0", "60", "5.0"),
    ("3/16", "3.0", "34.0", "365", "200", "19.0", "100", "9.0"),
    ("3/16", "4.0", "44.0", "550", "340", "25.0", "190", "12.0"),
]
HRH49 = [("1/4", "2.1", "25", "130", "85", "2.7", "40", "1.3")]


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


def token_on_line(line: str, [credential] -> bool:
    return re.search(rf"(?<![\d.]){re.escape(token)}(?![\d.])", line) is not None


def assert_row(blob: str, cell: str, pcf: str, tokens: tuple[str, ...], label: str) -> None:
    for line in blob.splitlines():
        if cell in line and token_on_line(line, pcf) and all(token_on_line(line, tok) for tok in tokens):
            return
    raise SystemExit(f"sheet row missing {label} {cell} {pcf} {tokens}")


def verify_sheets() -> None:
    criii = Path("unpublished-local-ref:a1e243c9bdc9acd1").read_text(encoding="utf-8", errors="replace")
    table_i, table_ii = criii.split("Table II:", 1)
    for row in CRIII_5052:
        assert_row(table_i, row[0], row[1], row[2:], "CR-III 5052")
    for row in CRIII_5056:
        assert_row(table_ii, row[0], row[1], row[2:], "CR-III 5056")
    line_316 = next(
        line for line in table_i.splitlines() if "3/16" in line and token_on_line(line, "2.0") and token_on_line(line, "14.3")
    )
    if "13.3" in line_316:
        raise SystemExit("CR-III 3/16-2.0 still shows 13.3")
    plas = Path("unpublished-local-ref:369add5162018f7d").read_text(encoding="utf-8", errors="replace")
    for cell, pcf, rho, bare, lstr, gl, wstr, gw in PLASCORE:
        assert_row(plas, cell, pcf, (rho, bare, lstr, gl, wstr, gw), "Plascore")
    attr = Path("unpublished-local-ref:4c78985542c89b81").read_text(encoding="utf-8", errors="replace")
    for row in HFT:
        assert_row(attr, row[0], row[1], row[2:], "HFT")
    for row in HRH49:
        assert_row(attr, row[0], row[1], row[2:], "HRH-49")
    for path, (expect, _url) in PDFS.items():
        digest, _size = sha_bytes(path)
        if digest != expect:
            raise SystemExit(f"pdf pin mismatch {path.name} {digest}")


def rank_modes(sfs: dict, branch: str) -> list[tuple[str, float]]:
    ordered = sorted(sfs.items(), key=lambda item: (item[1], item[0]))
    if branch == "shear_crimping":
        global_sf = sfs["global_buckling"]
        crimp_sf = sfs["core_shear_crimping"]
        if abs(global_sf - crimp_sf) <= 1e-9 * max(crimp_sf, 1e-30):
            ordered = [item for item in ordered if item[0] != "global_buckling"]
    return ordered


def modes(face: dict, core: dict, tf: float, tc: float, kd: float, biax: float, score_dimple: bool) -> dict:
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
    if core["Ec_Pa"] is not None:
        if core["form"] == "foam":
            uni = K_FOAM * (young * core["Ec_Pa"] * core["Gc_Pa"] / (1.0 - NU * NU)) ** (1.0 / 3.0)
        else:
            uni = K_HONEY * young * math.sqrt(core["Ec_Pa"] * tf / (young * tc))
        sfs["face_wrinkling"] = biax * uni / membrane
    if score_dimple and core.get("s_cell_m"):
        sigma_d = 2.0 * young / (1.0 - NU * NU) * (tf / core["s_cell_m"]) ** 2
        sfs["intracell_dimpling"] = sigma_d / membrane
    ordered = rank_modes(sfs, branch)
    return {
        "h_m": h,
        "tf_m": tf,
        "core_m": tc,
        "Vc": vc,
        "Kc": kc,
        "gamma": gamma,
        "branch": branch,
        "sfs": sfs,
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


def optimize(face: dict, core: dict, kd: float, biax: float, score_dimple: bool) -> dict:
    best = None
    for step in range(1, GRID):
        fraction = step / GRID
        tf, tc = geometry(face, core, fraction)
        ev = modes(face, core, tf, tc, kd, biax, score_dimple)
        if "face_wrinkling" not in ev["sfs"]:
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
        "s_cell_m": core.get("s_cell_m"),
        "ec_source": core.get("ec_source", "sheet"),
        "theoretical": theoretical_column(face, core, ev, biax),
    }


def theoretical_column(face: dict, core: dict, ev: dict, biax: float) -> dict:
    sfs = dict(ev["sfs"])
    tf = ev["tf_m"]
    tc = ev["core_m"]
    young = face["E_Pa"]
    membrane = P_EXT * R / (4.0 * tf)
    if core["form"] == "foam":
        uni = K_THEORY * (young * core["Ec_Pa"] * core["Gc_Pa"] / (1.0 - NU * NU)) ** (1.0 / 3.0)
        basis = "foam CR-1457 form, theoretical coefficient 0.82"
    else:
        uni = K_THEORY * young * math.sqrt(core["Ec_Pa"] * tf / (young * tc))
        basis = "honeycomb form, Hemp theoretical coefficient 0.82"
    sfs["face_wrinkling"] = biax * uni / membrane
    ordered = rank_modes(sfs, ev["branch"])
    return {
        "k": K_THEORY,
        "basis": basis,
        "face_wrinkling": sfs["face_wrinkling"],
        "governing": ordered[0][0],
        "least_SF": ordered[0][1],
        "second_mode": ordered[1][0],
        "second_SF": ordered[1][1],
        "factor_to_SF_1": 1.0 / ordered[0][1],
    }


def scale(rho: float, base_rho: float, base_ec: float, base_gc: float, base_crush: float) -> dict:
    ratio = rho / base_rho
    return {
        "Ec_Pa": base_ec * ratio**2,
        "Gc_Pa": base_gc * ratio**2,
        "crush_Pa": base_crush * ratio**1.5,
    }


def sheet_core(
    name: str,
    family: str,
    cell: str,
    pcf: str,
    rho: float,
    ec_ksi: str,
    crush_psi: str,
    l_psi: str,
    gl_ksi: str,
    w_psi: str,
    gw_ksi: str,
    source: str,
    ec_source: str,
    crush_basis: str,
) -> dict:
    gw = float(gw_ksi)
    gl = float(gl_ksi)
    if gw > gl:
        raise SystemExit(f"W shear is not the lower modulus on {name}")
    if rho <= 0.0 or rho > 64.1:
        raise SystemExit(f"density outside the band {name} {rho}")
    return {
        "name": name,
        "family": family,
        "form": "honeycomb",
        "cell": cell,
        "pcf": float(pcf),
        "rho": rho,
        "s_cell_m": CELL_M[cell],
        "Ec_Pa": float(ec_ksi) * KSI,
        "Gc_Pa": gw * KSI,
        "Gl_Pa": gl * KSI,
        "crush_Pa": float(crush_psi) * PSI,
        "shear_strength_L_Pa": float(l_psi) * PSI,
        "shear_strength_W_Pa": float(w_psi) * PSI,
        "tag": "QUESTIONABLE",
        "source": source,
        "ec_source": ec_source,
        "crush_basis": crush_basis,
        "Gc_direction": "W",
    }


def build_cores() -> list[dict]:
    foam32 = {
        "name": "ROHACELL 31 IG-F",
        "family": "PMI_foam",
        "form": "foam",
        "rho": 32.0,
        "Ec_Pa": 17.0e6,
        "Gc_Pa": 13.0e6,
        "crush_Pa": 0.40e6,
        "tag": "QUESTIONABLE",
        "source": "MAINLINE-014 sourced core, ROHACELL 31 IG-F",
        "ec_source": "sheet",
        "Gc_direction": "isotropic_foam",
    }
    aramid32 = {
        "name": "Hexcel HRH-10-4.8-32",
        "family": "aramid_honeycomb",
        "form": "honeycomb",
        "cell": "4.8 mm",
        "rho": 32.0,
        "s_cell_m": 0.0048,
        "Ec_Pa": 76.0e6,
        "Gc_Pa": 14.0e6,
        "crush_Pa": 1.00e6,
        "tag": "QUESTIONABLE",
        "source": "MAINLINE-014 sourced core, Hexcel HRH-10-4.8-32, W shear",
        "ec_source": "sheet",
        "Gc_direction": "W",
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
            "source": "MAINLINE-014 density scaling: Ec and Gc as rho^2, crush as rho^1.5",
            "ec_source": "projection",
            "Gc_direction": "isotropic_foam",
            **foam,
        })
        honey = scale(rho, 32.0, 76.0e6, 14.0e6, 1.00e6)
        eligible.append({
            "name": f"aramid honeycomb scaled from HRH-10-32 to {rho:g}",
            "family": "aramid_honeycomb",
            "form": "honeycomb",
            "cell": "4.8 mm",
            "rho": rho,
            "s_cell_m": 0.0048,
            "tag": "PROJECTION",
            "source": "MAINLINE-014 density scaling from HRH-10-4.8-32, same 4.8 mm cell",
            "ec_source": "projection",
            "Gc_direction": "W",
            **honey,
        })
    criii_url = PDFS[Path("unpublished-local-ref:951dae7dbde87d65")][1]
    for alloy, rows in (("5052", CRIII_5052), ("5056", CRIII_5056)):
        for cell, pcf, ec, crush, lstr, gl, wstr, gw in rows:
            rho = float(pcf) * PCF_TO_KG
            eligible.append(sheet_core(
                f"Hexcel CR-III {alloy} {cell}-{pcf}",
                "aluminium_honeycomb",
                cell,
                pcf,
                rho,
                ec,
                crush,
                lstr,
                gl,
                wstr,
                gw,
                f"Hexcel HexWeb CR-III data sheet, {alloy} typical, {criii_url}",
                "sheet",
                "CR-III crush column",
            ))
    ec_by_cell = {(cell, pcf): ec for cell, pcf, ec, *_rest in CRIII_5052}
    plas_url = PDFS[Path("unpublished-local-ref:520d93dc2201e43f")][1]
    for cell, pcf, rho_s, bare, lstr, gl, wstr, gw in PLASCORE:
        ec = ec_by_cell[(cell, pcf)]
        eligible.append(sheet_core(
            f"Plascore PAMG-XR1 5052 {cell}-{pcf}",
            "aluminium_honeycomb",
            cell,
            pcf,
            float(rho_s),
            ec,
            bare,
            lstr,
            gl,
            wstr,
            gw,
            f"Plascore PAMG-XR1 5052 typical shear and bare compression, {plas_url}. "
            f"Ec is the Hexcel CR-III 5052 {cell}-{pcf} stabilised modulus {ec} ksi.",
            f"transferred from Hexcel CR-III 5052 {cell}-{pcf} stabilised modulus {ec} ksi",
            "Plascore bare compressive typical; the sheet has no crush column",
        ))
    attr_url = PDFS[Path("unpublished-local-ref:ad6f653b2469389b")][1]
    for cell, pcf, ec, crush, lstr, gl, wstr, gw in HFT:
        eligible.append(sheet_core(
            f"Hexcel HFT fiberglass {cell}-{pcf}",
            "fiberglass_honeycomb",
            cell,
            pcf,
            float(pcf) * PCF_TO_KG,
            ec,
            crush,
            lstr,
            gl,
            wstr,
            gw,
            f"Hexcel attributes brochure, Fibertruss HFT, not carbon, {attr_url}",
            "sheet",
            "HFT stabilised compressive strength; the sheet has no crush column",
        ))
    for cell, pcf, ec, crush, lstr, gl, wstr, gw in HRH49:
        eligible.append(sheet_core(
            f"Hexcel HRH-49 Kevlar {cell}-{pcf}",
            "para_aramid_honeycomb",
            cell,
            pcf,
            float(pcf) * PCF_TO_KG,
            ec,
            crush,
            lstr,
            gl,
            wstr,
            gw,
            f"Hexcel attributes brochure, HRH-49 Kevlar 49 fabric, not carbon, {attr_url}",
            "sheet",
            "HRH-49 stabilised compressive strength; the sheet has no crush column",
        ))
    return eligible


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
    th = row["theoretical"]
    dimple = row["sfs"].get("intracell_dimpling")
    dimple_txt = (
        f" Dimpling SF is {g(dimple)}."
        if dimple is not None
        else " This core has no cell size, so dimpling is not scored."
    )
    return (
        f"{short(row['face'])} ({row['face_tag']}): least SF {g(row['least_SF'])} "
        f"governed by {row['governing']}, second {row['second_mode']} at {g(row['second_SF'])}. "
        f"Core {row['core_name']} at {g(row['core_density_kg_m3'])} kg/m3 ({row['core_tag']}), "
        f"tf {g(row['tf_m'])} m, core depth {g(row['core_m'])} m. "
        f"The factor to reach 1 is {g(row['factor_to_SF_1'])}. "
        f"Theoretical coefficient {g(th['k'])} gives least SF {g(th['least_SF'])} "
        f"by {th['governing']}."
        + dimple_txt
    )


def same_ranking(left: list[dict], right: list[dict]) -> bool:
    if len(left) != len(right):
        return False
    for a, b in zip(left, right):
        if short(a["face"]) != short(b["face"]) or g(a["least_SF"]) != g(b["least_SF"]):
            return False
        if a["governing"] != b["governing"] or a["core_name"] != b["core_name"]:
            return False
    return True


def main() -> None:
    if (ROOT / "RESULTS.json").exists():
        raise SystemExit("RESULTS.json is the measured run. Not recomputing.")
    for path in PINS:
        require_pin(path)
    verify_sheets()
    if abs(20_000 * PSI - 137895145.86336723) > 1e-6:
        raise SystemExit("ksi conversion drifted from MAINLINE-007")
    if abs(187 * PSI - 1289319.6138224835) > 1e-6:
        raise SystemExit("psi conversion drifted from MAINLINE-007")
    r003 = json.loads(R003.read_text(encoding="utf-8"))
    r007 = json.loads(R007.read_text(encoding="utf-8"))
    r007b = json.loads(R007B.read_text(encoding="utf-8"))
    r008 = json.loads(R008.read_text(encoding="utf-8"))
    r014 = json.loads(R014.read_text(encoding="utf-8"))
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
    if abs(biax - 0.6823278038280194) > 1e-12:
        raise SystemExit("biaxial factor left the 014 value")
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
    ident = modes(al, dummy, tf_e, tc_e, KD_HANDBOOK, biax, False)
    sealed = p2e["buckling_SF"]
    if abs(ident["sfs"]["global_buckling"] - sealed) / sealed > 1e-9:
        raise SystemExit(f"classical identity {ident['sfs']['global_buckling']}")
    if ident["branch"] != "stiff_or_moderate_core" or abs(ident["Kc"] - 1.0) > 1e-9:
        raise SystemExit("infinite-G branch failed")

    faces = load_faces(r008)
    wanted = {"SiC", "Be S-200F", "AlBeMet 162", "K13D2U", "M55J", "6061-T6", "CNT-yarn", "graphene"}
    have = {short(face["name"]) for face in faces}
    missing = wanted - have
    if missing or len(faces) != 15:
        raise SystemExit(f"faces {len(faces)} missing {sorted(missing)}")
    eligible = build_cores()
    aramid = next(core for core in eligible if core["name"] == "Hexcel HRH-10-4.8-32")
    be_face = next(face for face in faces if short(face["name"]) == "Be S-200F")
    be_old = optimize(be_face, aramid, KD_HANDBOOK, biax, False)
    be014 = next(
        row for row in r014["optima"] if short(row["face"]) == "Be S-200F" and row["kd"] == KD_HANDBOOK
    )
    for key in ("least_SF", "tf_m", "core_m", "second_SF"):
        if abs(be_old[key] - be014[key]) / abs(be014[key]) > 1e-9:
            raise SystemExit(f"014 regression {key} {be_old[key]} {be014[key]}")
    if be_old["governing"] != be014["governing"] or be_old["second_mode"] != be014["second_mode"]:
        raise SystemExit("014 regression mode mismatch")
    if g(be014["least_SF"]) != "0.685338231171":
        raise SystemExit("014 Be display drifted")
    plas = next(core for core in eligible if core["name"] == "Plascore PAMG-XR1 5052 3/16-2.0")
    if abs(plas["Gc_Pa"] - 137895145.86336723) > 1e-4:
        raise SystemExit("Plascore W shear left the 007 value")
    if abs(plas["crush_Pa"] - 1289319.6138224835) > 1e-4:
        raise SystemExit("Plascore bare compression left the 007 value")
    if abs(plas["Ec_Pa"] / KSI - 34.0) > 1e-9:
        raise SystemExit("Plascore Ec transfer is not 34 ksi")

    origin_path = ROOT / "ORIGIN.json"
    if origin_path.exists():
        origin = json.loads(origin_path.read_text(encoding="utf-8"))
    else:
        origin = {
            "origin_utc": datetime.now(ZONE).isoformat(timespec="microseconds"),
            "origin_monotonic_s": time.monotonic(),
        }
        origin_path.write_text(json.dumps(origin, indent=1) + "\n", encoding="utf-8")

    optima = []
    for face in faces:
        for kd in (KD_HANDBOOK, KD_BRIEF):
            best = None
            per_density = []
            for core in eligible:
                row = optimize(face, core, kd, biax, True)
                row["face"] = face["name"]
                row["face_tag"] = face["tag"]
                row["kd"] = kd
                row["gain_vs_008_P2E"] = row["least_SF"] / face["p2e_least_SF_008"]
                row["p2e_least_SF_008"] = face["p2e_least_SF_008"]
                per_density.append({
                    "core": core["name"],
                    "density": core["rho"],
                    "family": core["family"],
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
    top_q_low = ranked(KD_BRIEF, "QUESTIONABLE")[:3]
    be = next(row for row in optima if short(row["face"]) == "Be S-200F" and row["kd"] == KD_HANDBOOK)
    al6061 = next(row for row in optima if short(row["face"]) == "6061-T6" and row["kd"] == KD_HANDBOOK)

    end_utc = datetime.now(ZONE).isoformat(timespec="microseconds")
    elapsed = time.monotonic() - origin["origin_monotonic_s"]
    results = {
        "schema": 1,
        "card": "MAINLINE-014b",
        "unit": "vacuum-mainline014b-metal-honeycomb-1019",
        "status": "ESTIMATE_PENDING_UNA",
        "tag": "QUESTIONABLE",
        "certification": False,
        "kd_handbook": KD_HANDBOOK,
        "kd_brief": KD_BRIEF,
        "nu_used_for_every_face": NU,
        "crush_target_Pa": P_EXT / 2.0,
        "structural_mass_kg": M_STRUCT,
        "Gc_is_W_shear": True,
        "wrinkling_coefficients": {
            "foam_design": K_FOAM,
            "honeycomb_design": K_HONEY,
            "theoretical": K_THEORY,
            "tag": "QUESTIONABLE",
        },
        "dimpling": "sigma = 2*E_f/(1-nu^2)*(tf/s_cell)^2; SF = sigma/membrane; no extra biaxial factor",
        "checks": {
            "P2E_mass_identity": "PASS",
            "classical_kd_0_2_infinite_G": "PASS",
            "classical_SF": ident["sfs"]["global_buckling"],
            "biaxial_factor": biax,
            "atmosphere_from_007": "PASS",
            "regression_014_Be_on_HRH10_dimpling_off": "PASS",
            "plascore_3_16_2_W_and_bare_match_007": "PASS",
            "sheet_rows_found_in_text": "PASS",
        },
        "optima": optima,
        "best_three_kd_0_20": [short(row["face"]) for row in top],
        "best_three_questionable_kd_0_20": [short(row["face"]) for row in top_q],
        "best_three_kd_0_1407": [short(row["face"]) for row in top_low],
        "kd_0_1407_same_leaders_as_0_20": same_ranking(top, top_low),
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
                "note": "Every face uses nu 0.33. MAINLINE-008 published no Poisson ratio.",
            },
            {
                "id": "NFI-KD-01407",
                "note": "0.1407 replaces handbook gamma 0.20 on the stiff branch only. It is the brief's figure, not a fresh SP-8032 knockdown.",
            },
            {
                "id": "NFI-SCALE",
                "note": "The 014 projections at 16, 8 and 4 kg/m3 stay in the set. Moduli scale as rho^2 and crush as rho^1.5. The scaled aramid keeps the parent 4.8 mm cell.",
            },
            {
                "id": "NFI-013",
                "note": "MAINLINE-013 has not filed. Its cores are not used.",
            },
            {
                "id": "NFI-W-SHEAR",
                "note": "Gc is the W plate-shear modulus, the lower of L and W on every sheet row scored here. Crimping and honeycomb wrinkling use that Gc.",
            },
            {
                "id": "NFI-W-13-3",
                "note": "The attributes brochure text shows 13.3 ksi for CR-III 5052 3/16-2.0 W modulus. The CR-III data sheet prints 14.3 ksi. This card uses 14.3. The brochure's 1/4-3.4 L modulus glyph 50..0 is 50.0 on the data sheet.",
            },
            {
                "id": "NFI-PLASCORE-EC",
                "note": "Plascore PAMG-XR1 5052 prints bare compression and L/W plate shear. It prints no stabilised compressive modulus and no crush column. Ec is the Hexcel CR-III 5052 stabilised modulus at the same cell and nominal pcf. Crush is Plascore's bare compressive typical, which is the 1.29 MPa the brief names at 3/16-2.0. That bare value is not the Hexcel crush-column test.",
            },
            {
                "id": "NFI-DENSITY",
                "note": "Hexcel pcf converts at 0.45359237/0.3048^3. Plascore uses the kg/m3 printed on its sheet, so 2.0 pcf is 32 there and 32.037 on the Hexcel conversion. Rows above 4.0 pcf, and Plascore rows printed above 64 kg/m3, are outside the band and were not scored. HFT at 4.0 pcf converts to 64.074 kg/m3 and is kept.",
            },
            {
                "id": "NFI-CARBON",
                "note": "No carbon-fiber honeycomb sheet located here lists stabilised Ec and both shear moduli in this density band. Hexcel's product list has no carbon honeycomb table. Ultracor UCF-51-3/8-2.0 on MatWeb lists density 0.032 g/cc, compressive yield 1.41 MPa and L shear modulus 0.331 GPa, and omits Ec and W shear, so it is not scored. HFT is fiberglass phenolic. HRH-49 is Kevlar 49 fabric. Neither is carbon.",
            },
            {
                "id": "NFI-HRH36",
                "note": "HRH-36 para-aramid in the attributes brochure has no stabilised compressive modulus. It is not scored. HDC has strengths only. HFT 3/8-4.0 has no stabilised modulus. Preliminary and beam-shear rows were not scored.",
            },
            {
                "id": "NFI-CRUSH-COLUMN",
                "note": "Hexcel CR-III crush is the crush column. HFT and HRH-49 have no crush column, so the stabilised compressive strength is used. Thickness does not enter the crush safety factor. The target is p/2.",
            },
            {
                "id": "NFI-SHEAR-STRENGTH",
                "note": "L and W plate-shear strengths are stored from the sheets. The scored crimp mode uses shear modulus. Shear strength is not a separate mode.",
            },
            {
                "id": "NFI-DIMPLE",
                "note": "Intracell dimpling uses the brief's stress 2*E_f/(1-nu^2)*(tf/s_cell)^2, divided by the same membrane stress as wrinkling. No equibiaxial factor is applied. Cell size is the sheet nominal. Foam is not dimpled. The coefficient 2 is the brief's expression.",
            },
            {
                "id": "NFI-WRINKLE-Q",
                "note": "Honeycomb design coefficient 0.33 is CR-1457 eq 2.2-14. Theoretical 0.82 is Hemp's symmetric anti-plane value, quoted as purely theoretical for honeycomb in NASA/CR-1999-208994. Foam design 0.50 and theoretical 0.82 are the 014 column, kept for the foam cores that remain in the set. The theoretical column is the same geometry, not a new grid.",
            },
            {
                "id": "NFI-HEMISPHERE",
                "note": "Handbook gamma 0.20 is the CR-1457 hemisphere value. A complete sphere has no edge.",
            },
            {
                "id": "NFI-FACTOR",
                "note": "1/least SF is the safety-factor gap. It is the property multiple only when that mode scales in proportion. Wrinkling scales as a square root or a cube root. Dimpling scales as tf cubed.",
            },
            {
                "id": "NFI-014-REGRESSION",
                "note": "With dimpling turned off, Be S-200F on HRH-10-4.8-32 at kd 0.20 recovers the filed 014 least SF, thicknesses and modes. The 014 tree was not rewritten.",
            },
            {
                "id": "NFI-STIFF-BRANCH",
                "note": "A high shear modulus leaves the crimp branch. Gamma then becomes the knockdown 0.20, and global buckling is scored with that factor. For Be S-200F the best aluminium row is CR-III 5056 at 1.6 pcf, least SF 0.668649769509 by global buckling, below the HRH-10 crimp balance 0.685338231171. The 1/4 and 3/8 cells tie. Plascore 3/16-2.0, W shear 20 ksi and transferred Ec 34 ksi, reaches 0.641722323466 by the same mode. The higher W shear does not raise the leading safety factors. 6061-T6 does move, to 0.145930331406 on CR-III 5056 3/8-1.0.",
            },
        ]
    }
    (ROOT / "NFI.json").write_text(json.dumps(nfi, indent=1) + "\n", encoding="utf-8")
    inputs = {
        "pins": [pin(path) for path in (CARD, COMMON, R008, R007, R007B, R003, R014)],
        "pdfs": [
            {"path": str(path), "sha256": digest, "url": url}
            for path, (digest, url) in PDFS.items()
        ],
        "nu": NU,
        "p_ext_Pa": P_EXT,
        "lift_kg": LIFT,
        "pcf_to_kg_m3": PCF_TO_KG,
        "cores_eligible": eligible,
        "faces": [
            {"name": face["name"], "rho": face["rho"], "E_Pa": face["E_Pa"], "sigma_Pa": face["sigma_Pa"], "tag": face["tag"]}
            for face in faces
        ],
        "band": "about 16 to 64 kg/m3; Hexcel rows with pcf <= 4.0; Plascore rows with printed kg/m3 <= 64",
        "not_scored": [
            "Hexcel and Plascore rows above the density band",
            "CR-III preliminary and beam-shear rows, and rows with no modulus",
            "HRH-36, no stabilised modulus",
            "HDC, strengths only",
            "HFT 3/8-4.0, no stabilised modulus",
            "Ultracor UCF-51-3/8-2.0, no Ec and no W shear on the public MatWeb sheet",
            "CarbonCore plastic honeycomb, not carbon fiber, and 80 kg/m3",
        ],
    }
    (ROOT / "INPUTS.json").write_text(json.dumps(inputs, indent=1) + "\n", encoding="utf-8")

    lines = [
        "# MAINLINE-014b metal and carbon honeycomb — ESTIMATE_PENDING_UNA",
        "",
        "QUESTIONABLE. Nothing here is a certification. The float ceiling, pressure, lift, nu 0.33 and the fifteen faces are the MAINLINE-014 set. Knockdowns 0.20 and 0.1407 are re-optimised separately. Gc is the W shear modulus, the lower direction, on every honeycomb row.",
        "",
        "Hexcel CR-III 5052 and 5056 typical rows from 1.0 to 3.8 pcf are the aluminium sheet, including stabilised compressive modulus and the crush column. URL https://www.hexcel.com/wp-content/uploads/2025/12/HexWeb_CRIII_DataSheet.pdf. Plascore PAMG-XR1 5052 rows whose sheet prints 16 to 61 kg/m3 are added. That sheet has no Ec. Ec is transferred from the CR-III 5052 row of the same cell and nominal pcf. Crush there is the bare compressive typical. URL http://plascore.com/wp-content/uploads/dlm_uploads/2025/08/PLA_PAMG-XR1-5052_2023-06-02.pdf. No carbon-fiber honeycomb sheet with stabilised Ec and both shear moduli was found in this band. Hexcel HFT fiberglass and one HRH-49 Kevlar row are the other high-modulus sheets that do print those moduli. They are not carbon. URL https://www.hexcel.com/wp-content/uploads/2026/01/HexWebHoneycombAttributesandProperties-1.pdf. The 014 foam and aramid cores, including the projections, stay in the set.",
        "",
        "Modes are shear-trimmed global buckling, face yield, wrinkling, core shear crimping, core crush at p/2, and intracell dimpling. Dimpling stress is 2*E_f/(1-nu^2)*(tf/s_cell)^2. Honeycomb wrinkling uses design coefficient 0.33. The theoretical coefficient 0.82 is a column on the same geometry. Foam keeps design 0.50 and theoretical 0.82. On the crimp branch, global buckling and crimping are the same pressure and count as one mode.",
        "",
        f"Checks passed. Equal face and core mass at 16 kg/m3 recovers the sealed P2-E thicknesses. Infinite shear modulus at knockdown 0.20 recovers buckling SF {g(sealed)}. With dimpling off, Be S-200F on HRH-10 at 32 kg/m3 recovers the filed 014 least SF {g(be014['least_SF'])}. The Plascore 3/16-2.0 W modulus is 20 ksi and the bare compression is 187 psi, matching MAINLINE-007. Its transferred Ec is 34 ksi.",
        "",
        "Best three at knockdown 0.20, by least safety factor:",
    ]
    for row in top:
        lines.append("")
        lines.append(sentence(row))
    lines.extend(["", "Best three QUESTIONABLE faces at knockdown 0.20:"])
    for row in top_q:
        lines.append("")
        lines.append(sentence(row))
    lines.extend(["", "Best three at knockdown 0.1407, re-optimised:"])
    if same_ranking(top, top_low):
        lines.append("")
        lines.append(
            "The best three faces, cores, least safety factors and governing modes match the knockdown 0.20 ranking. "
            "The QUESTIONABLE three match as well. Where a winner sits on the shear-crimping branch, gamma is 1 "
            "and the knockdown does not enter."
        )
    else:
        for row in top_low:
            lines.append("")
            lines.append(sentence(row))
    if not same_ranking(top_q, top_q_low):
        lines.append("")
        lines.append("QUESTIONABLE faces at knockdown 0.1407:")
        for row in top_q_low:
            lines.append("")
            lines.append(sentence(row))
    lines.extend([
        "",
        (
            "The best three overall stay on Hexcel HRH-10 at 32 kg/m3. "
            "A high-G aluminium row leaves the crimp branch, takes gamma 0.20, and finishes lower. "
            "See NFI-STIFF-BRANCH. "
            f"6061-T6 least SF is {g(al6061['least_SF'])}, governed by {al6061['governing']}, "
            f"on {al6061['core_name']}."
        ),
        "",
        (
            f"Start {origin['origin_utc']}. End {end_utc}. Elapsed {elapsed} s, a measurement. "
            "The 2026-10-20T07:00:00-07:00 deadline is a door check-in."
        ),
        "",
    ])
    (ROOT / "CARD.md").write_text("\n".join(lines), encoding="utf-8")
    print("cores", len(eligible), "faces", len(faces), "elapsed", elapsed)
    print("same1407", same_ranking(top, top_low), "sameQ", same_ranking(top_q, top_q_low))
    for label, rows in (("TOP", top), ("Q", top_q), ("LOW", top_low)):
        for row in rows:
            print(
                label,
                short(row["face"]),
                row["face_tag"],
                g(row["least_SF"]),
                row["governing"],
                row["second_mode"],
                g(row["second_SF"]),
                g(row["tf_m"]),
                g(row["core_m"]),
                g(row["core_density_kg_m3"]),
                row["core_name"],
                g(row["factor_to_SF_1"]),
                row["branch"],
                g(row["theoretical"]["least_SF"]),
                row["theoretical"]["governing"],
                g(row["sfs"].get("intracell_dimpling", float("nan"))),
            )
    print("BE014", g(be014["least_SF"]), "BE", g(be["least_SF"]), "AL", g(al6061["least_SF"]), al6061["governing"], al6061["core_name"])


if __name__ == "__main__":
    main()
