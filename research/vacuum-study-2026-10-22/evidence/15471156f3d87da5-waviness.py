#!/usr/bin/env python3
"""MAINLINE-032. Q against initial face waviness for the two lead stacks.

The honeycomb formula is NASA CR-1457 equations (2.2-12) and (2.2-13),
read from the page image of printed page 2-33. Elastic eta is 1.
Nothing here is a certification. The 014b, 021 and 022 trees are not run.
"""

from __future__ import annotations

import hashlib
import json
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
ZONE = ZoneInfo("America/Los_Angeles")

# Same psi constant as this seat's 014b honeycomb sheet conversion.
PSI = 6894.757293168361
KSI = PSI * 1000.0

Q_IDEAL = 0.82
K_FACTOR = 0.64
Q_DESIGN = 0.33
Q_TARGETS = (0.371, 0.609)
CARD_B = 0.6823

# Hexcel HexWeb CR-III Table II, 5056, 3/8-1.0. Read from the local
# sheet text extracted for 014b. Modulus and strengths are typical
# except the stabilised minimum, which the sheet also prints.
EC_KSI = 15.0
FC_STAB_TYP_PSI = 60.0
FC_STAB_MIN_PSI = 35.0
CRUSH_PSI = 35.0
CELL_M = 0.0254 * 3.0 / 8.0
CARD_CELL_M = 0.0095

CARD = Path(
    "unpublished-local-ref:2f68afa9c74ca674"
    "/.ship/artifacts/vacuum-overnight-briefs-1019/CARD-032-WRINKLE-WAVINESS.md"
)
COMMON = Path(
    "unpublished-local-ref:2f68afa9c74ca674"
    "/.ship/artifacts/vacuum-overnight-briefs-1019/COMMON.md"
)
PINS = {
    CARD: ("26885739fb2fbeb601fc3c79b9aeb9ac5dc50c1838f76971065abc316d69d21c", 1874),
    COMMON: ("8f359d6c04f84d158ccc232173cb61e86eeede3797fe362d8212066a096f94b5", 5874),
}

FACES = (
    {
        "name": "Be S-200F",
        "lead": "MAINLINE-021 rev1",
        "lead_Q": 0.371,
        "tf_m": 0.8434e-3,
        "tc_m": 20.21e-3,
        "E_Pa": 290.0e9,
        "dimpling_SF_filed": 9.0,
    },
    {
        "name": "SR-200",
        "lead": "MAINLINE-021b",
        "lead_Q": 0.609,
        "tf_m": 0.6917e-3,
        "tc_m": 30.12e-3,
        "E_Pa": 290.0e9,
        "dimpling_SF_filed": 4.98,
    },
)


def g(value: float) -> str:
    return format(value, ".12g")


def sha_bytes(path: Path) -> tuple[str, int]:
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest(), len(data)


def require_pin(path: Path) -> dict:
    digest, size = sha_bytes(path)
    expect_sha, expect_bytes = PINS[path]
    if digest != expect_sha or size != expect_bytes:
        raise SystemExit(f"pin mismatch {path.name} {digest} {size}")
    return {"path": str(path), "sha256": digest, "bytes": size}


def dump(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, indent=1) + "\n", encoding="utf-8")


def biaxial_root() -> float:
    """Real root of r**3 + r - 1 = 0, the equibiaxial case of R_x**3 + R_y = 1."""
    r = 0.7
    for _ in range(80):
        f = r * r * r + r - 1.0
        d = 3.0 * r * r + 1.0
        r = r - f / d
    return r


def k_delta(delta_m: float, tc_m: float, ec_pa: float, fc_pa: float) -> float:
    return delta_m * ec_pa / (tc_m * fc_pa)


def q_of(delta_m: float, tc_m: float, ec_pa: float, fc_pa: float) -> float:
    return Q_IDEAL / (1.0 + K_FACTOR * k_delta(delta_m, tc_m, ec_pa, fc_pa))


def delta_for_q(q: float, tc_m: float, ec_pa: float, fc_pa: float) -> float:
    if not 0.0 < q <= Q_IDEAL:
        raise SystemExit(f"Q outside (0, 0.82]: {q}")
    k = (Q_IDEAL / q - 1.0) / K_FACTOR
    return k * tc_m * fc_pa / ec_pa


def amplitude_row(q: float, face: dict, ec_pa: float, fc_pa: float, fc_name: str) -> dict:
    delta = delta_for_q(q, face["tc_m"], ec_pa, fc_pa)
    back = q_of(delta, face["tc_m"], ec_pa, fc_pa)
    if abs(back - q) > 1e-12 * q:
        raise SystemExit(f"inverse failed {face['name']} {q} {back}")
    return {
        "face": face["name"],
        "lead": face["lead"],
        "Q": q,
        "is_that_leads_Q": q == face["lead_Q"],
        "Fc_basis": fc_name,
        "delta_m": delta,
        "delta_mm": delta * 1e3,
        "delta_over_tf": delta / face["tf_m"],
        "delta_over_cell_3_8_in": delta / CELL_M,
        "delta_over_card_9_5_mm": delta / CARD_CELL_M,
        "delta_over_tc": delta / face["tc_m"],
        "K_delta": k_delta(delta, face["tc_m"], ec_pa, fc_pa),
        "tag": "QUESTIONABLE",
    }


def curve(ec_pa: float, fc_pa: float, fc_name: str) -> list[dict]:
    rows = []
    for ratio in (0.0, 0.0005, 0.001, 0.002, 0.003, 0.004, 0.005, 0.007, 0.010):
        # Q depends on delta/tc and Fc/Ec only. Core thickness cancels.
        delta = ratio  # metres, with tc = 1 m, so K = ratio * Ec / Fc
        q = q_of(delta, 1.0, ec_pa, fc_pa)
        rows.append({
            "delta_over_tc": ratio,
            "Q": q,
            "Fc_basis": fc_name,
            "tag": "QUESTIONABLE",
        })
    return rows


def main() -> None:
    results_path = ROOT / "RESULTS.json"
    if results_path.exists():
        raise SystemExit("RESULTS.json exists; not restamping")
    t0 = time.monotonic()
    started = datetime.now(ZONE)
    pins = {"card": require_pin(CARD), "common": require_pin(COMMON)}
    ec = EC_KSI * KSI
    fc_typ = FC_STAB_TYP_PSI * PSI
    fc_min = FC_STAB_MIN_PSI * PSI
    crush = CRUSH_PSI * PSI
    # 014b stored this core's stabilised modulus and the crush column.
    if abs(ec - 103421359.3975254) > 1e-6:
        raise SystemExit(f"Ec drifted from the 014b sheet value {ec}")
    if abs(crush - 241316.50526089262) > 1e-6:
        raise SystemExit(f"crush drifted from the 014b sheet value {crush}")
    root = biaxial_root()
    if abs(root ** 3 + root - 1.0) > 1e-15:
        raise SystemExit("biaxial root is not on R^3 + R = 1")
    # Same absolute delta must scale between the two cores with tc alone.
    d_a = delta_for_q(0.371, FACES[0]["tc_m"], ec, fc_typ)
    d_b = delta_for_q(0.371, FACES[1]["tc_m"], ec, fc_typ)
    if abs(d_b / d_a - FACES[1]["tc_m"] / FACES[0]["tc_m"]) > 1e-12:
        raise SystemExit("amplitude did not scale with core thickness")
    if abs(delta_for_q(0.371, FACES[0]["tc_m"], ec, fc_min) / d_a - fc_min / fc_typ) > 1e-12:
        raise SystemExit("amplitude did not scale with flatwise strength")
    if abs(q_of(0.0, 1.0, ec, fc_typ) - Q_IDEAL) > 1e-15:
        raise SystemExit("perfect facing is not Q 0.82")

    bases = (("stabilised_typical_60_psi", fc_typ), ("stabilised_minimum_35_psi", fc_min))
    amplitudes = []
    for fc_name, fc in bases:
        for face in FACES:
            for q in Q_TARGETS:
                amplitudes.append(amplitude_row(q, face, ec, fc, fc_name))
    design_inversion = []
    for fc_name, fc in bases:
        for face in FACES:
            row = amplitude_row(Q_DESIGN, face, ec, fc, fc_name)
            row["tag"] = "PROJECTION"
            row["why"] = (
                "Q 0.33 is CR-1457 eq 2.2-14, an empirical lower bound from tests. "
                "This row is the amplitude that would make eq 2.2-12 equal 0.33. "
                "The handbook does not identify 0.33 with a measured wave."
            )
            design_inversion.append(row)

    elapsed = time.monotonic() - t0
    ended = datetime.now(ZONE)
    origin = {
        "origin_utc": started.isoformat(timespec="microseconds"),
        "origin_monotonic_s": t0,
    }
    inputs = {
        "unit": "vacuum-mainline032-wrinkle-waviness-1020",
        "tag": "QUESTIONABLE",
        "pins": pins,
        "formula": {
            "source": "NASA CR-1457 eq 2.2-12 and 2.2-13, printed page 2-33",
            "url": "https://ntrs.nasa.gov/api/citations/19700004831/downloads/19700004831.pdf",
            "citation": "https://ntrs.nasa.gov/citations/19700004831",
            "statement": (
                "sigma_wr = 0.82 * (Ec*tf/(eta*Ef*tc))**0.5 * (eta*Ef) / (1 + 0.64*K_delta); "
                "K_delta = delta*Ec/(tc*Fc); elastic eta = 1. "
                "That is Q = 0.82 / (1 + 0.64*K_delta) in sigma = b*Q*sqrt(Ef*Ec*tf/tc)."
            ),
            "Q_ideal": Q_IDEAL,
            "K_factor": K_FACTOR,
            "eta": 1.0,
            "design_Q_equation": "2.2-14",
            "design_Q": Q_DESIGN,
            "biaxial_equation": "2.2-15",
            "biaxial_statement": "R_x**3 + R_y = 1. Equal compression gives r**3 + r = 1.",
            "figures_from": "MIL-HDBK-23, as named on the CR-1457 page",
        },
        "core": {
            "name": "Hexcel CR-III 5056 3/8-1.0",
            "url": "https://www.hexcel.com/wp-content/uploads/2025/12/HexWeb_CRIII_DataSheet.pdf",
            "table": "Table II, test data at 0.625 inch thickness",
            "density_pcf": 1.0,
            "density_kg_m3": 16.018463373960138,
            "cell_m": CELL_M,
            "card_cell_m": CARD_CELL_M,
            "Ec_ksi_typical": EC_KSI,
            "Ec_Pa": ec,
            "Fc_stabilised_typical_psi": FC_STAB_TYP_PSI,
            "Fc_stabilised_minimum_psi": FC_STAB_MIN_PSI,
            "Fc_typical_Pa": fc_typ,
            "Fc_minimum_Pa": fc_min,
            "crush_psi_typical": CRUSH_PSI,
            "crush_Pa": crush,
            "bare_typical_psi": 55.0,
            "bare_minimum_psi": 25.0,
            "Fc_choice": (
                "Flatwise core compression is the stabilised column. "
                "The crush column is the post-crush plateau and is not Fc. "
                "Flatwise tension and the beryllium bond are not on the sheet."
            ),
            "tag": "QUESTIONABLE",
        },
        "faces": list(FACES),
        "flatness_sources": [
            {
                "name": "SAE AMS7902H",
                "url": "https://doi.org/10.4271/AMS7902H",
                "what": "Hot-rolled beryllium sheet and plate, three flatness classes in section 3.5.5.",
                "number_read": False,
                "tag": "QUESTIONABLE",
            },
            {
                "name": "Flatiron stock 3/8-cell panel",
                "url": "https://www.flatironpanelproducts.com/wp-content/uploads/2020/02/Flatiron-Stock-AHP04038-Data-Sheet-2-11-2020.pdf",
                "flatness_inch_per_radial_foot": 0.008,
                "flatness_mm_per_foot": 0.008 * 25.4,
                "face_inch": 0.040,
                "note": "Panel bow on faces thicker than either lead face. Not the wrinkle-wave amplitude.",
                "tag": "QUESTIONABLE",
            },
            {
                "name": "Honylite balanced aluminum honeycomb",
                "url": "https://www.honylite.com/materials/strength-flatness-inserts",
                "flatness_mm_per_radial_metre": 0.7,
                "note": "Long-wave panel tolerance. Not delta.",
                "tag": "QUESTIONABLE",
            },
            {
                "name": "QC Facades honeycomb guarantee",
                "url": "https://qcfacades.com/wp-content/uploads/2019/05/190101_Honeycomb-Flatness-Guarantee.pdf",
                "wave_mm": 1.0,
                "per_60_inch_mm": 1.5,
                "note": "Architectural panel. Much larger than the amplitudes below.",
                "tag": "QUESTIONABLE",
            },
            {
                "name": "Indy Honeycomb finished-core flatness",
                "url": "https://indyhoneycomb.com/wp-content/uploads/2023/04/IHSS-N1_C.pdf",
                "flatness_inch": 0.010,
                "local_step_inch": 0.003,
                "local_step_mm": 0.003 * 25.4,
                "note": "Core blanket under hold-down, before a beryllium face is bonded.",
                "tag": "QUESTIONABLE",
            },
        ],
        "other_sources": [
            {
                "name": "Norris, Ericksen and March, FPL Report 1810",
                "url": "https://www.fpl.fs.usda.gov/documnts/fplr/fplr1810.pdf",
                "note": (
                    "Initial irregularities are resolved into Fourier components. "
                    "The component nearest the critical wavelength grows. "
                    "The card names Kommers as the third author. This report's third author is March. "
                    "Kommers was not located on this report."
                ),
            },
            {
                "name": "Norris, Boller and Voss, FPL Report 1810-A",
                "url": "https://ir.library.oregonstate.edu/downloads/2f75rc704",
                "note": (
                    "Honeycomb supplement. Cell size influences the length of the waves "
                    "into which the facings wrinkle. Report 1810's waves had amplitude "
                    "proportional to core thickness."
                ),
            },
        ],
    }
    results = {
        "unit": "vacuum-mainline032-wrinkle-waviness-1020",
        "tag": "QUESTIONABLE",
        "not_a_certification": True,
        "started": started.isoformat(timespec="microseconds"),
        "ended": ended.isoformat(timespec="microseconds"),
        "elapsed_s": elapsed,
        "Q_of_perfect_facing": Q_IDEAL,
        "shared_curve_Q_versus_delta_over_tc": {
            "stabilised_typical_60_psi": curve(ec, fc_typ, "stabilised_typical_60_psi"),
            "stabilised_minimum_35_psi": curve(ec, fc_min, "stabilised_minimum_35_psi"),
        },
        "amplitudes": amplitudes,
        "design_0_33_if_it_were_this_waviness": design_inversion,
        "biaxial": {
            "equation": "R_x**3 + R_y = 1",
            "equibiaxial_root": root,
            "card_b": CARD_B,
            "card_minus_root": CARD_B - root,
            "residual_of_card_b": CARD_B ** 3 + CARD_B - 1.0,
            "counts_waviness_twice": False,
            "why": (
                "K_delta is inside the uniaxial stress. Equation 2.2-15 then "
                "multiplies that stress by the load ratio. For equal compression "
                "the ratio is the root above. The cards' b is that root rounded "
                "to 0.6823. The exponent sits on x on the printed page. Equal "
                "components make R_x**3 + R_y and R_x + R_y**3 the same equation."
            ),
            "tag": "QUESTIONABLE",
        },
        "dimpling": {
            "cell_m": CELL_M,
            "card_cell_m": CARD_CELL_M,
            "filed_SF": {
                "Be S-200F 021 rev1": 9.0,
                "SR-200 021b": 4.98,
            },
            "note": (
                "Those safety factors are the filed 021 rows, not recomputed here. "
                "Equation 2.2-12 does not put a one-cell dimple into Q. "
                "FPL 1810-A says the cell size changes the wrinkle wavelength, "
                "so the two modes are not shown to be independent."
            ),
            "tag": "QUESTIONABLE",
        },
        "checks": {
            "inverse_returns_Q": "PASS",
            "amplitude_scales_with_tc": "PASS",
            "amplitude_scales_with_Fc": "PASS",
            "perfect_facing_Q_0_82": "PASS",
            "biaxial_root_on_cubic": "PASS",
            "Ec_matches_014b_15_ksi": "PASS",
            "crush_35_psi_matches_014b_and_is_not_Fc": "PASS",
        },
    }
    nfi = {
        "open": [
            {
                "id": "fc-is-the-lower-of-three",
                "tag": "QUESTIONABLE",
                "note": (
                    "Fc is the lower of flatwise compression, flatwise tension and "
                    "the face-to-core bond. The sheet prints stabilised compression, "
                    "60 psi typical and 35 psi minimum. It does not print flatwise "
                    "tension or a beryllium bond. A weaker bond lowers the allowed amplitude "
                    "in proportion. The crush column, 35 psi, is not that peak."
                ),
            },
            {
                "id": "sheet-thickness",
                "tag": "QUESTIONABLE",
                "note": (
                    "Table II says the test thickness is 0.625 inch. The lead cores "
                    "are 20.21 mm and 30.12 mm. Ec is typical only. No minimum modulus is printed."
                ),
            },
            {
                "id": "eta",
                "tag": "QUESTIONABLE",
                "note": (
                    "The page says elastic cases use eta = 1, and inelastic cases use section 9. "
                    "The map uses eta = 1. The 021 faces sit at compression safety factor about 1, "
                    "so a plasticity factor may apply. It is not in this Q map."
                ),
            },
            {
                "id": "wavelength-versus-cell",
                "tag": "QUESTIONABLE",
                "note": (
                    "Section 2.2.2 does not print the critical half-wavelength. "
                    "FPL 1810-A says cell size changes that wavelength. "
                    "Delta over the 9.525 mm cell is an amplitude ratio, not a separation of modes."
                ),
            },
            {
                "id": "shop-flatness-is-not-delta",
                "tag": "QUESTIONABLE",
                "note": (
                    "AMS7902H defines three flatness classes. The class numbers were not read. "
                    "Bonded-panel numbers found here are long-wave bows or an architectural wave. "
                    "Hexcel's design note that a large cell telegraphs into a thin face gives no depth. "
                    "None of those is the Fourier component in equation 2.2-13."
                ),
            },
            {
                "id": "biaxial-on-a-shell",
                "tag": "QUESTIONABLE",
                "note": (
                    "Equation 2.2-15 is recommended for biaxial compression. "
                    "The foam section bases its interaction on flat plates of large aspect ratio. "
                    "The honeycomb page does not show a biaxial waviness test. The hull radius is 10 m."
                ),
            },
            {
                "id": "design-0-33-is-not-a-measured-wave",
                "tag": "PROJECTION",
                "note": (
                    "Inverting equation 2.2-12 at Q 0.33 is stored so the design value "
                    "can be seen as an amplitude. The handbook selected 0.33 from a test plot."
                ),
            },
            {
                "id": "kommers",
                "tag": "QUESTIONABLE",
                "note": (
                    "The card names Norris, Ericksen and Kommers. "
                    "FPL Report 1810 is Norris, Ericksen and March. Kommers was not found on it."
                ),
            },
        ]
    }
    dump(ROOT / "INPUTS.json", inputs)
    dump(results_path, results)
    dump(ROOT / "NFI.json", nfi)
    dump(ROOT / "ORIGIN.json", origin)
    card = render_card(results, inputs)
    (ROOT / "CARD.md").write_text(card, encoding="utf-8")
    print(g(elapsed))
    print("root", g(root))
    for row in amplitudes:
        if row["Fc_basis"] != "stabilised_typical_60_psi":
            continue
        if not row["is_that_leads_Q"]:
            continue
        print(
            row["face"],
            g(row["Q"]),
            g(row["delta_mm"]),
            g(row["delta_over_tf"]),
            g(row["delta_over_cell_3_8_in"]),
            g(row["delta_over_card_9_5_mm"]),
        )


def render_card(results: dict, inputs: dict) -> str:
    lines = [
        "# MAINLINE-032. Face waviness that makes the lead Q real.",
        "",
        "QUESTIONABLE. Not a certification. The formula is NASA CR-1457 equation (2.2-12), printed page 2-33, https://ntrs.nasa.gov/citations/19700004831. With elastic eta equal to 1,",
        "",
        "sigma_wr = 0.82 * sqrt(E_f * E_c * t_f / t_c) / (1 + 0.64 * K_delta)",
        "",
        "K_delta = delta * E_c / (t_c * F_c)",
        "",
        "The card's Q is 0.82 / (1 + 0.64 * K_delta). A perfect facing has Q 0.82. Equation (2.2-14) is the design value 0.33 when the amplitude is unknown. Figures 2.2-6 and 2.2-7 are taken from MIL-HDBK-23, as that page says.",
        "",
        "F_c and E_c are Hexcel CR-III 5056 3/8-1.0, Table II, https://www.hexcel.com/wp-content/uploads/2025/12/HexWeb_CRIII_DataSheet.pdf. Stabilised compressive modulus 15 ksi typical. Stabilised compressive strength 60 psi typical and 35 psi minimum. The crush column is 35 psi and is not F_c. Flatwise tension and the beryllium bond are not on the sheet. The sheet's test thickness is 0.625 inch.",
        "",
        "Q depends on delta/t_c and on F_c/E_c. It does not depend on face thickness except when the same amplitude is written as delta/t_f. The two cores therefore share one curve and differ in absolute amplitude by 30.12/20.21.",
        "",
        "## Amplitudes at the stabilised typical 60 psi",
        "",
        "Delta is the zero-to-peak amplitude in equation (2.2-13).",
        "",
    ]
    for row in results["amplitudes"]:
        if row["Fc_basis"] != "stabilised_typical_60_psi":
            continue
        mark = "lead Q" if row["is_that_leads_Q"] else "cross Q"
        lines.append(
            f"- {row['face']} core {g(next(f['tc_m'] for f in FACES if f['name']==row['face'])*1e3)} mm, "
            f"Q {g(row['Q'])} ({mark}): delta {g(row['delta_mm'])} mm, "
            f"delta/t_f {g(row['delta_over_tf'])}, "
            f"delta/(3/8 in) {g(row['delta_over_cell_3_8_in'])}, "
            f"delta/9.5 mm {g(row['delta_over_card_9_5_mm'])}."
        )
    lines += [
        "",
        "At the stabilised minimum, 35 psi, every amplitude above scales by 35/60. A weaker bond would scale them down again. The 60 psi numbers are an upper amplitude only if F_c really is 60 psi.",
        "",
        "The filed dimpling margins, not recomputed, are 9.0 on the S-200F row and 4.98 on the SR-200 row. The lead amplitudes are 0.0046 to 0.024 of the 9.525 mm cell. Equation (2.2-12) does not fold a one-cell dimple into Q. FPL Report 1810-A (Norris, Boller and Voss) says the cell size changes the wrinkle wavelength, so the modes are not shown to be separate. https://ir.library.oregonstate.edu/downloads/2f75rc704",
        "",
        "FPL Report 1810 (Norris, Ericksen and March) treats the initial wave as Fourier components, and the component near the critical wavelength is the one that grows. https://www.fpl.fs.usda.gov/documnts/fplr/fplr1810.pdf. The card names Kommers. That report's third author is March.",
        "",
        "## Shop flatness",
        "",
        "These are not delta. Flatiron's 3/8-cell stock panel, faces 0.040 inch, holds 0.008 inch per radial foot (0.203 mm per foot). https://www.flatironpanelproducts.com/wp-content/uploads/2020/02/Flatiron-Stock-AHP04038-Data-Sheet-2-11-2020.pdf. Honylite states 0.7 mm per radial metre on a balanced aluminum honeycomb panel. https://www.honylite.com/materials/strength-flatness-inserts. QC Facades states a wave of 1 mm. https://qcfacades.com/wp-content/uploads/2019/05/190101_Honeycomb-Flatness-Guarantee.pdf. Indy Honeycomb's finished core, before bonding, allows 0.010 inch overall and a local step of 0.003 inch (0.076 mm). https://indyhoneycomb.com/wp-content/uploads/2023/04/IHSS-N1_C.pdf. SAE AMS7902H, the hot-rolled beryllium sheet specification, defines three flatness classes. The class numbers were not read. https://doi.org/10.4271/AMS7902H. Hexcel describes telegraphing of a large cell into a thin face and prints no depth.",
        "",
        "A per-foot bow of 0.203 mm is larger than the Q 0.609 amplitudes and near the Q 0.371 amplitude on the thinner core. That comparison is a PROJECTION if the whole bow is treated as the wrinkle component. It is not that component.",
        "",
        "## Biaxial",
        "",
        f"Equation (2.2-15) is R_x cubed plus R_y equals 1. Equal compression solves at {g(results['biaxial']['equibiaxial_root'])}. The cards use b = 0.6823. The difference is {g(results['biaxial']['card_minus_root'])}. Waviness stays inside the uniaxial stress. Multiplying by b does not count it twice. The interaction is the handbook's recommendation for flat plates. Transfer to the 10 m hull is QUESTIONABLE.",
        "",
        "## Design 0.33",
        "",
        "PROJECTION. If equation (2.2-12) at Q 0.33 were the whole of the design knockdown, the 60 psi amplitudes would be "
        + g(next(r["delta_mm"] for r in results["design_0_33_if_it_were_this_waviness"] if r["face"] == "Be S-200F" and r["Fc_basis"] == "stabilised_typical_60_psi"))
        + " mm on the 20.21 mm core and "
        + g(next(r["delta_mm"] for r in results["design_0_33_if_it_were_this_waviness"] if r["face"] == "SR-200" and r["Fc_basis"] == "stabilised_typical_60_psi"))
        + " mm on the 30.12 mm core. The handbook selected 0.33 from tests, not from a measured wave. 0.33/0.82 is about 0.40, the knockdown the page calls approximately 0.4.",
        "",
        f"Start {results['started']}. End {results['ended']}. Elapsed {g(results['elapsed_s'])} s. A measurement of this script. The order's 07:00 field is a door check-in.",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    main()
