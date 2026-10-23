#!/usr/bin/env python3
"""MAINLINE-007 arithmetic. Own script. Reads pinned inputs, writes RESULTS.json.

Mass, buckling and yield follow MAINLINE-002/003 as restated in COMMON.md.
d is the face separation core_thickness + tf. Both faces and the core use the
external sphere area. kd = 0.2. Nothing here is a certification.
"""
from __future__ import annotations

import hashlib
import json
import math
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STARTED = "2026-10-19T22:45:53-07:00"

# Full-precision atmosphere from sealed MAINLINE-003 RESULTS.json.
P = 95460.83791390515
RHO_AIR = 1.1672683307461802
VOLUME = 4188.790204786391
LIFT = 4889.442150186961
R = 10.0
E = 68.9e9
NU = 0.33
SIGMA = 276e6
KD = 0.2
RHO_AL = 2700.0
SYSTEMS = 100.0
JOINT = 0.05
DENSITIES = (32.0, 16.0, 8.0, 6.0, 4.0, 3.0, 2.0, 1.0)

PINS = {
    "mainline001_card": (
        "evidence/33ee112c1cb1a4b5-CARD.md",
        "33ee112c1cb1a4b5fe2460554b46bd68963cb980f49b06964fe672199132c4d8",
        5667,
    ),
    "mainline001_inputs": (
        "evidence/69d9ef27cb5c86f2-INPUTS.json",
        "69d9ef27cb5c86f2a20399210b65cfb12f911ab1c1c4cb6fdff9cca70ba14c5a",
        15384,
    ),
    "mainline001_results": (
        "evidence/e7b2e4a33ab68eb0-RESULTS.json",
        "e7b2e4a33ab68eb0e195b83cb91faa86a77d7bc5b8970dfa3dd3cbae07a9cde5",
        30175,
    ),
    "mainline002_card": (
        "evidence/63c812f02bde7cf4-CARD.md",
        "63c812f02bde7cf43d029e423b360014f9bb73c233bf33b46e525005378a0f07",
        6977,
    ),
    "mainline002_inputs": (
        "evidence/f7365a5dbdda8ddd-INPUTS.json",
        "f7365a5dbdda8dddb18217e3a352457b372b3d0e2d94d7e692d78e62b48c7928",
        1643,
    ),
    "mainline002_results": (
        "evidence/d728af6ca61595e1-RESULTS.json",
        "d728af6ca61595e116b2b133b23477cecaf54d050486202277f441234c25a2c0",
        13071,
    ),
    "mainline002_nfi": (
        "evidence/b155c07e690eaa66-NFI.json",
        "b155c07e690eaa665db0f27994bcf36986d5ffe168aa7a45cc0ae403ddcd87a8",
        2449,
    ),
    "mainline003_card": (
        "evidence/17dc1e39680f79f6-CARD.md",
        "17dc1e39680f79f6ba2fd9d3ac0ac4fba28dfc4e4c95824e55e544bbcd3f1a3e",
        3907,
    ),
    "mainline003_inputs": (
        "evidence/a697a764919c3211-INPUTS.json",
        "a697a764919c3211bb47caf3b032d3ace7637e85971078a66ef3264beb6abbe9",
        851,
    ),
    "mainline003_results": (
        "evidence/df5d268297e342bd-mainline003.json",
        "df5d268297e342bdce62fb6c4906a128e6c8729c8b56ae7a710ef9fdd73cd0db",
        7995,
    ),
    "mainline003_nfi": (
        "evidence/2090c6e1f4ca8afb-NFI.json",
        "2090c6e1f4ca8afb62ff5a7a0e2efbe8757aa60a79a773be2fae359cdd446e97",
        2978,
    ),
    "una003": (
        "evidence/dcfa7ae3942a9e4f-UNA600-MAINLINE003-REVIEW.md",
        "dcfa7ae3942a9e4f8a43ac06ff5ba62d2249d69414228ea756661cb1f020925b",
        3351,
    ),
    "common": (
        "withheld-source:b528d6a62c81ce0b",
        "8f359d6c04f84d158ccc232173cb61e86eeede3797fe362d8212066a096f94b5",
        5874,
    ),
    "card007": (
        "unpublished-local-ref:eee4da47983eaf06",
        "05791cd102b446c15ddf1b266b08263652ed4f24d54ac2f1206d79f010533b53",
        1640,
    ),
}

PSI = 6894.757293168361
KSI = 6.894757293168361e6


def sha256(path: Path) -> tuple[str, int]:
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest(), len(data)


def verify_pins() -> dict:
    out = {}
    for name, (path, expect, nbytes) in PINS.items():
        digest, size = sha256(Path(path))
        if digest != expect or size != nbytes:
            raise SystemExit(f"pin mismatch {name}: {digest} {size} != {expect} {nbytes}")
        out[name] = {"path": path, "sha256": digest, "bytes": size}
    return out


def sphere_area() -> float:
    return 4.0 * math.pi * R * R


def denom() -> float:
    return R * R * math.sqrt(1.0 - NU * NU)


def p_buckling(tf: float, separation: float, kd: float = KD) -> float:
    """kd * 4 * tf * (d+tf) * E / (R^2 * sqrt(1-nu^2)). separation is d+tf."""
    return kd * 4.0 * tf * separation * E / denom()


def p_yield(tf: float) -> float:
    return 4.0 * SIGMA * tf / R


def structural_mass() -> float:
    return (LIFT - SYSTEMS) / (1.0 + JOINT)


def tf_max() -> float:
    return structural_mass() / (2.0 * sphere_area() * RHO_AL)


def geometry(tf: float, rho_c: float) -> dict:
    area = sphere_area()
    m_struct = structural_mass()
    m_faces = 2.0 * area * tf * RHO_AL
    m_core = m_struct - m_faces
    if m_core < -1e-9:
        raise ValueError("face mass exceeds the structural budget")
    m_core = max(m_core, 0.0)
    tc = m_core / (area * rho_c)
    separation = tc + tf
    m_sandwich = m_faces + m_core
    m_joints = JOINT * m_sandwich
    total = m_sandwich + m_joints + SYSTEMS
    pb = p_buckling(tf, separation)
    py = p_yield(tf)
    sf_b = pb / P
    sf_y = py / P
    membrane = P * R / (4.0 * tf)
    return {
        "tf_m": tf,
        "core_m": tc,
        "separation_m": separation,
        "rho_core_kg_m3": rho_c,
        "masses_kg": {
            "faces": m_faces,
            "core": m_core,
            "joints": m_joints,
            "systems_payload": SYSTEMS,
            "residual_gas": 0.0,
        },
        "all_mass_kg": total,
        "float_margin_kg": LIFT - total,
        "p_buckling_Pa": pb,
        "p_yield_Pa": py,
        "SF_b": sf_b,
        "SF_y": sf_y,
        "least_SF": min(sf_b, sf_y),
        "governing": (
            "both_equal"
            if abs(sf_b - sf_y) <= 1e-12 * max(sf_b, sf_y, 1.0)
            else "knocked_down_buckling" if sf_b < sf_y else "aluminum_yield"
        ),
        "membrane_stress_Pa": membrane,
        "E_factor": P / pb,
        "strength_factor": membrane / SIGMA,
        "Gc_crimp_Pa": P * R / (2.0 * separation),
        "Ec_times_Gc_Pa2": (2.0 * membrane) ** 3 / E,
        "crush_target_Pa": P / 2.0,
    }


def buckling_split(rho_c: float) -> dict:
    """Closed form. Maximise tf*(tc+tf) on the mass line. See CARD.md."""
    area = sphere_area()
    m_struct = structural_mass()
    tf = m_struct / (2.0 * area * (2.0 * RHO_AL - rho_c))
    row = geometry(tf, rho_c)
    row["rule"] = "max_buckling_SF"
    row["solver"] = "closed_form"
    return row


def equal_sf_separation() -> float:
    """d where SF_b = SF_y. Independent of density. Una: strength does not set E."""
    return SIGMA * R * math.sqrt(1.0 - NU * NU) / (KD * E)


def least_split(rho_c: float) -> dict:
    """Maximise min(SF_b, SF_y).

    SF_b / SF_y = separation / d_eq. Below d_eq, buckling is the lesser factor,
    so the lesser factor is maximised at the buckling peak. Above d_eq, yield
    is the lesser factor and falls as the faces get thinner, so the maximum
    sits on SF_b = SF_y.
    """
    d_eq = equal_sf_separation()
    peak = buckling_split(rho_c)
    if peak["separation_m"] <= d_eq:
        peak["rule"] = "max_least_SF"
        peak["solver"] = "same_as_buckling_peak_because_separation_below_equal_SF"
        return peak
    area = sphere_area()
    m_struct = structural_mass()
    tf = (m_struct - area * rho_c * d_eq) / (area * (2.0 * RHO_AL - rho_c))
    row = geometry(tf, rho_c)
    row["rule"] = "max_least_SF"
    row["solver"] = "SF_b_equals_SF_y"
    return row


def grid_best(rho_c: float, n: int = 8001) -> tuple[dict, dict]:
    hi = tf_max() * (1.0 - 1.0 / n)
    best_b = None
    best_l = None
    for i in range(1, n):
        tf = hi * i / n
        row = geometry(tf, rho_c)
        if best_b is None or row["SF_b"] > best_b["SF_b"]:
            best_b = row
        if best_l is None or row["least_SF"] > best_l["least_SF"]:
            best_l = row
    return best_b, best_l


def assert_close(name: str, got: float, expect: float, rel: float = 1e-9) -> None:
    if expect == 0:
        if abs(got) > rel:
            raise SystemExit(f"{name}: {got} != 0")
        return
    err = abs(got - expect) / abs(expect)
    if err > rel:
        raise SystemExit(f"{name}: {got} vs {expect} rel {err}")


def baseline_checks() -> dict:
    # Inherited P2 baseline: tf=0.0002, core=0.1, separation=0.1002, rho=16.
    # Mass is NOT on the ceiling. Rebuild from thicknesses, not from the solver.
    area = sphere_area()
    tf, tc, rho = 0.0002, 0.1, 16.0
    separation = tc + tf
    m_faces = 2.0 * area * tf * RHO_AL
    m_core = area * tc * rho
    pb = p_buckling(tf, separation)
    py = p_yield(tf)
    assert_close("baseline faces", m_faces, 1357.1680263507908, 1e-12)
    assert_close("baseline core", m_core, 2010.6192983, 1e-9)
    assert_close("baseline buckling Pa", pb, 11701.5583953, 1e-9)
    assert_close("baseline yield Pa", py, 22080.0, 1e-15)
    # P2-A comparison from MAINLINE-003.
    tf_a = 0.0003758936444928841
    pb_a = p_buckling(tf_a, 0.1 + tf_a)
    assert_close("P2-A buckling SF", pb_a / P, 0.23078902511015878, 1e-9)
    # P2-E equal mass at rho 16, from MAINLINE-003.
    tf_e = 0.0003360949703945902
    row_e = geometry(tf_e, 16.0)
    # geometry() spends the ceiling, so core thickness is whatever the ceiling gives,
    # not the 003 core. Check the 003 point by direct formula instead.
    tc_e = 0.1134320525081742
    pb_e = p_buckling(tf_e, tc_e + tf_e)
    assert_close("P2-E buckling SF", pb_e / P, 0.23388557899250978, 1e-9)
    # Solver versus grid.
    for rho in DENSITIES:
        closed_b = buckling_split(rho)
        closed_l = least_split(rho)
        grid_b, grid_l = grid_best(rho)
        # tf* sits near half of tf_max. One sample is about 1.25e-4 of tf*,
        # so a 1e-4 relative match is tighter than the grid can promise.
        step = tf_max() / 8001.0
        tf_err = abs(closed_b["tf_m"] - grid_b["tf_m"])
        if tf_err > step:
            raise SystemExit(f"grid buckling tf@{rho}: off by {tf_err}, step {step}")
        assert_close(f"grid buckling SF@{rho}", closed_b["SF_b"], grid_b["SF_b"], 1e-7)
        # The equal-SF crossing is a knife edge. A uniform tf sample sits off
        # the crossing, so its min(SF_b, SF_y) is below the closed form. The
        # closed form must dominate that sample, and the gap must stay small.
        if closed_l["least_SF"] + 1e-12 < grid_l["least_SF"]:
            raise SystemExit(
                f"grid least beats closed form @{rho}: "
                f"{grid_l['least_SF']} > {closed_l['least_SF']}"
            )
        least_gap = abs(closed_l["least_SF"] - grid_l["least_SF"]) / closed_l["least_SF"]
        if least_gap > 1e-4:
            raise SystemExit(f"grid least SF@{rho} gap {least_gap}")
    return {
        "baseline_buckling_Pa": pb,
        "baseline_match": "PASS",
        "P2A_buckling_SF": pb_a / P,
        "P2A_match": "PASS",
        "P2E_buckling_SF": pb_e / P,
        "P2E_match": "PASS",
        "grid_match": "PASS",
        "inherited_face_mass_implies_rho_al": m_faces / (2.0 * area * tf),
    }


def solve_sf_b_equals_one() -> dict:
    lo, hi = 0.05, 64.0
    # SF_b at the buckling split falls as density rises.
    if buckling_split(lo)["SF_b"] < 1.0 or buckling_split(hi)["SF_b"] > 1.0:
        raise SystemExit("SF_b = 1 is outside the bracket")
    for _ in range(80):
        mid = 0.5 * (lo + hi)
        if buckling_split(mid)["SF_b"] > 1.0:
            lo = mid
        else:
            hi = mid
    rho = 0.5 * (lo + hi)
    row = buckling_split(rho)
    return {"rho_core_kg_m3": rho, "at_split": "max_buckling_SF", **{k: row[k] for k in (
        "tf_m", "core_m", "separation_m", "SF_b", "SF_y", "least_SF", "governing",
        "membrane_stress_Pa", "E_factor", "strength_factor")}}


def least_sf_peak() -> dict:
    # Sample the named set and a continuous log range. Report the argmax.
    samples = []
    rho = 0.25
    while rho <= 64.0 * 1.0000001:
        row = least_split(rho)
        samples.append((rho, row["least_SF"], row["SF_b"], row["SF_y"], row["solver"]))
        rho *= 1.05
    named = [(rho, least_split(rho)["least_SF"]) for rho in DENSITIES]
    best = max(samples, key=lambda item: item[1])
    # Monotonic check: least SF should fall as density rises, so the peak is the low end.
    rising = sum(1 for a, b in zip(samples, samples[1:]) if b[1] > a[1] + 1e-12)
    return {
        "on_named_set_peak_rho_kg_m3": max(named, key=lambda item: item[1])[0],
        "on_named_set": [{"rho": rho, "least_SF": sf} for rho, sf in named],
        "continuous_peak_rho_kg_m3": best[0],
        "continuous_peak_least_SF": best[1],
        "continuous_samples": len(samples),
        "samples_where_next_is_higher": rising,
        "reading": (
            "On the sampled range 0.25 to 64 kg/m3 the maximised lesser safety factor "
            "falls as density rises. There is no interior peak. On the named densities "
            "it is highest at 1 kg/m3. It remains below 1."
        ),
    }


def material_table() -> list:
    """Sourced cores. SI values are the script's conversions from the cited column.

    Plascore psi and ksi are converted by 6894.757293168361 Pa/psi. Where the
    sheet's own MPa cell disagrees with that conversion, both are kept and the
    psi column is the one used. Honeycomb has no isotropic G. The W modulus is
    the smaller plate-shear modulus and is the one compared with the crimp target.
    """
    def pcf_row(name, density, comp_psi, g_l_ksi, g_w_ksi, source, note, ec_mpa=None):
        return {
            "name": name,
            "family": "aluminium_honeycomb",
            "density_kg_m3": density,
            "compressive_strength_Pa": comp_psi * PSI,
            "compressive_strength_source_column": f"{comp_psi} psi typical bare",
            "Ec_Pa": None if ec_mpa is None else ec_mpa * 1e6,
            "Gc_L_Pa": g_l_ksi * KSI,
            "Gc_W_Pa": g_w_ksi * KSI,
            "Gc_used_for_compare_Pa": g_w_ksi * KSI,
            "tag": "QUESTIONABLE",
            "source": source,
            "note": note,
        }

    return [
        {
            "name": "ROHACELL 31 IG-F",
            "family": "PMI_foam",
            "density_kg_m3": 32.0,
            "compressive_strength_Pa": 0.4e6,
            "Ec_Pa": 17e6,
            "Ec_column": "compressive modulus ISO 844, 17 MPa",
            "Gc_Pa": 13e6,
            "Gc_used_for_compare_Pa": 13e6,
            "shear_strength_Pa": 0.4e6,
            "tag": "QUESTIONABLE",
            "source": "Evonik ROHACELL IG-F product information, April 2022, https://cdn.sanity.io/files/dorbplvp/production/ed045b3e26f3de6b4faf1533d03ca5c1b66f8ae0.pdf",
            "note": "Nominal density 32 kg/m3 with a printed tolerance of plus or minus 7. Typical values, not a design allowable.",
        },
        {
            "name": "Divinycell H35",
            "family": "PVC_foam",
            "density_kg_m3": 38.0,
            "compressive_strength_Pa": 0.5e6,
            "Ec_Pa": 40e6,
            "Gc_Pa": 12e6,
            "Gc_used_for_compare_Pa": 12e6,
            "shear_strength_Pa": 0.4e6,
            "tag": "QUESTIONABLE",
            "source": "DIAB Divinycell H, H Oct 2012 rev9 SI, nominal column, via https://www.castrocompositesshop.com/en/index.php?controller=attachment&id_attachment=1020",
            "note": "Nearest listed PVC to 32 kg/m3, not a 32 kg/m3 product. An October 2012 rev7 sheet prints compressive strength 0.45 MPa for the same grade. Nominal is used. Minimum printed compressive strength on rev9 is 0.3 MPa.",
        },
        pcf_row(
            "Plascore PAMG-XR1 5052 3/16-2.0",
            32.0, 187.0, 34.0, 20.0,
            "Plascore PAMG-XR1 5052 datasheet rev 4.6.2021, http://plascore.com/wp-content/uploads/dlm_uploads/2025/08/PLA_PAMG-XR1-5052_2023-06-02.pdf",
            "The sheet's MPa cell beside the 100 psi bare-compression minimum prints 0.55, which is not 100 psi. Typical 187 psi converts to 1.289 MPa and the sheet prints 1.29. No compressive modulus column. Plate shear, not an isotropic G.",
        ),
        {
            "name": "Hexcel HRH-10-4.8-32",
            "family": "aramid_honeycomb",
            "density_kg_m3": 32.0,
            "compressive_strength_Pa": 1.00e6,
            "compressive_strength_column": "bare typical 1.00 MPa; stabilised typical 1.05 MPa",
            "Ec_Pa": 76e6,
            "Ec_column": "stabilised compressive modulus 76 MPa",
            "Gc_L_Pa": 30e6,
            "Gc_W_Pa": 14e6,
            "Gc_used_for_compare_Pa": 14e6,
            "tag": "QUESTIONABLE",
            "source": "Hexcel HexWeb HRH-10 datasheet, https://www.hexcel.com/wp-content/uploads/2025/12/HexWeb_HRH10_DataSheet_eu1.pdf",
            "note": "Aramid/phenolic honeycomb, 4.8 mm cell, 32 kg/m3. Stabilised modulus is not the continuum Ec of the wrinkling formula. W modulus is the smaller plate-shear modulus.",
        },
        pcf_row(
            "Plascore PAMG-XR1 5052 3/8-1.0",
            16.0, 52.0, 10.0, 7.0,
            "Plascore PAMG-XR1 5052 datasheet rev 4.6.2021, http://plascore.com/wp-content/uploads/dlm_uploads/2025/08/PLA_PAMG-XR1-5052_2023-06-02.pdf",
            "Lightest 5052 row on that sheet, 1.0 pcf. No compressive modulus column. Bare typical compression 52 psi.",
        ),
        {
            "name": "Hexcel HRH-10-6.4-24",
            "family": "aramid_honeycomb",
            "density_kg_m3": 24.0,
            "compressive_strength_Pa": 0.55e6,
            "Ec_Pa": 41e6,
            "Gc_L_Pa": 21e6,
            "Gc_W_Pa": 9e6,
            "Gc_used_for_compare_Pa": 9e6,
            "tag": "QUESTIONABLE",
            "source": "Hexcel HexWeb HRH-10 datasheet, https://www.hexcel.com/wp-content/uploads/2025/12/HexWeb_HRH10_DataSheet_eu1.pdf",
            "note": "Nearest listed aramid honeycomb below 32 kg/m3. 24 kg/m3, not 16. Bare typical compression 0.55 MPa. Stabilised modulus 41 MPa.",
        },
        {
            "name": "Schaedler nickel microlattice",
            "family": "microlattice",
            "density_kg_m3": 0.9,
            "compressive_strength_Pa": None,
            "Ec_Pa": None,
            "Gc_Pa": None,
            "tag": "QUESTIONABLE",
            "exists": "PROJECTION of a usable core is not claimed. The solid exists at this density in the paper.",
            "source": "T. A. Schaedler et al., Science 334, 962-965 (2011), doi:10.1126/science.1211649",
            "note": "Open abstract: density at or above 0.9 mg/cm3, recovery after compression beyond 50 percent strain, Young's modulus scales as density squared. No numeric modulus, shear modulus or compressive strength was in the abstract. Those values are not invented here.",
        },
    ]


def compare_materials(rows_by_rho: dict, materials: list) -> list:
    out = []
    for mat in materials:
        # Compare with the buckling-optimal row at the nearest named density.
        named = min(DENSITIES, key=lambda rho: abs(rho - mat["density_kg_m3"]))
        row = rows_by_rho[named]["max_buckling_SF"]
        gc = mat.get("Gc_used_for_compare_Pa")
        ec = mat.get("Ec_Pa")
        crush = mat.get("compressive_strength_Pa")
        item = {
            "material": mat["name"],
            "material_density_kg_m3": mat["density_kg_m3"],
            "compared_with_named_density_kg_m3": named,
            "split": "max_buckling_SF",
            "density_offset_kg_m3": mat["density_kg_m3"] - named,
            "crush_target_Pa": row["crush_target_Pa"],
            "compressive_strength_Pa": crush,
            "crush_margin": None if crush is None else crush / row["crush_target_Pa"],
            "Gc_target_Pa": row["Gc_crimp_Pa"],
            "Gc_Pa": gc,
            "crimp_margin": None if not gc else gc / row["Gc_crimp_Pa"],
            "Ec_Gc_target_Pa2": row["Ec_times_Gc_Pa2"],
            "Ec_Gc_Pa2": None if ec is None or gc is None else ec * gc,
            "wrinkle_margin": None if ec is None or gc is None else (ec * gc) / row["Ec_times_Gc_Pa2"],
        }
        out.append(item)
    return out


def public_row(row: dict) -> dict:
    keep = (
        "rule", "solver", "tf_m", "core_m", "separation_m", "rho_core_kg_m3",
        "masses_kg", "all_mass_kg", "float_margin_kg", "p_buckling_Pa", "p_yield_Pa",
        "SF_b", "SF_y", "least_SF", "governing", "membrane_stress_Pa", "E_factor",
        "strength_factor", "Gc_crimp_Pa", "Ec_times_Gc_Pa2", "crush_target_Pa",
    )
    return {k: row[k] for k in keep}


def main() -> None:
    pins = verify_pins()
    checks = baseline_checks()
    rows = {}
    for rho in DENSITIES:
        b = buckling_split(rho)
        least = least_split(rho)
        same = abs(b["tf_m"] - least["tf_m"]) / b["tf_m"] < 1e-9
        rows[str(rho)] = {
            "max_buckling_SF": public_row(b),
            "max_least_SF": public_row(least),
            "splits_coincide": same,
        }
    materials = material_table()
    by_rho = {rho: rows[str(rho)] for rho in DENSITIES}
    ended = datetime.now().astimezone().isoformat()
    doc = {
        "schema": 1,
        "card": "MAINLINE-007",
        "unit": "vacuum-mainline007-core-trade-1019",
        "status": "ESTIMATE",
        "tag": "QUESTIONABLE",
        "started_at": STARTED,
        "ended_at": ended,
        "certification": "none",
        "atmosphere": {
            "p_ext_Pa": P,
            "rho_air_kg_m3": RHO_AIR,
            "volume_m3": VOLUME,
            "lift_kg": LIFT,
            "R_m": R,
            "p_int_Pa": 0.0,
        },
        "inherited": {
            "E_Pa": E,
            "nu": NU,
            "sigma_Pa": SIGMA,
            "sigma_tag": "QUESTIONABLE",
            "sigma_transfer": "TRANSFERRED_FROM_TENSILE_YIELD",
            "sigma_source": "MAINLINE-002 INPUTS.json, ASM MatWeb 6061-T6 sheet, AA typical tensile yield",
            "rho_face_kg_m3": RHO_AL,
            "kd": KD,
            "joint_fraction_of_sandwich": JOINT,
            "systems_kg": SYSTEMS,
        },
        "formulas": {
            "area_m2": "4*pi*R^2, used for both faces and the core",
            "structural_mass_kg": "(lift - systems) / 1.05",
            "face_mass_kg": "2 * area * tf * 2700",
            "core_mass_kg": "area * core_thickness * rho_core",
            "separation_m": "core_thickness + tf",
            "p_buckling_Pa": "kd*4*tf*separation*E/(R^2*sqrt(1-nu^2))",
            "p_yield_Pa": "4*sigma*tf/R",
            "SF": "limit pressure / external pressure",
            "membrane_Pa": "p*R/(4*tf)",
            "Gc_crimp_Pa": "p*R/(2*separation), from p = 2*Gc*d/R with d = separation",
            "Ec_Gc_Pa2": "(2*membrane)^3 / E_face, from sigma_wr = 0.5*(E_face*Ec*Gc)^(1/3) set equal to membrane stress",
            "crush_Pa": "p/2, the brief's 'about p/2', not an equilibrium solution",
            "buckling_tf_m": "M_struct / (2*area*(2*rho_face - rho_core))",
            "equal_SF_separation_m": "sigma*R*sqrt(1-nu^2)/(kd*E)",
            "kd_scaling": "p_buckling and SF_b scale in direct proportion to kd. E_factor scales as 1/kd. Yield, membrane stress, the crimp modulus, the wrinkling product and the crush target do not depend on kd.",
        },
        "checks": checks,
        "equal_SF_separation_m": equal_sf_separation(),
        "tf_max_all_faces_m": tf_max(),
        "all_face_membrane_Pa": P * R / (4.0 * tf_max()),
        "all_face_SF_y": p_yield(tf_max()) / P,
        "yield_cannot_reach_1_on_the_ceiling": p_yield(tf_max()) / P < 1.0,
        "sf_b_reaches_1": solve_sf_b_equals_one(),
        "least_SF_peak": least_sf_peak(),
        "rows": rows,
        "materials": materials,
        "material_comparison": compare_materials(by_rho, materials),
        "pins": pins,
    }
    (ROOT / "RESULTS.json").write_text(json.dumps(doc, indent=1) + "\n")
    print(json.dumps({
        "ended": ended,
        "sf_b_1_rho": doc["sf_b_reaches_1"]["rho_core_kg_m3"],
        "sf_b_1": doc["sf_b_reaches_1"]["SF_b"],
        "sf_y_there": doc["sf_b_reaches_1"]["SF_y"],
        "all_face_SF_y": doc["all_face_SF_y"],
        "all_face_membrane_MPa": doc["all_face_membrane_Pa"] / 1e6,
        "d_eq": doc["equal_SF_separation_m"],
        "peak": doc["least_SF_peak"]["reading"],
        "named_least": doc["least_SF_peak"]["on_named_set"],
        "checks": checks,
    }, indent=1))


if __name__ == "__main__":
    main()
