"""MAINLINE-067 ranking. Own arithmetic from pinned files and the sourced table below.

Every inherited or sourced material value is QUESTIONABLE. A value that is not a
product today is PROJECTION. Nothing here is a hull safety factor.
"""
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DELTA = Path(
    "unpublished-local-ref:2f846ae958082233"
    "/.ship/work/outputs/vacuum-record-delta-c-1020/RESULTS.json"
)
FACE_INPUTS = Path(
    "unpublished-local-ref:2f846ae958082233"
    "/.ship/work/outputs/vacuum-mainline064-gamma-sources-1020/model/sources/040--INPUTS.json"
)
LB_PER_FT2 = 0.45359237 / 0.09290304  # kg/m2


def sha256(path):
    data = path.read_bytes()
    return hashlib.sha256(data).hexdigest(), len(data)


def cbrt(x):
    return x ** (1.0 / 3.0)


def two_faces(radius_m):
    """Both faces counted at the outer radius. The inner face is smaller."""
    return 2.0 * 4.0 * math.pi * radius_m * radius_m


def main():
    delta = json.loads(DELTA.read_text())
    pinned = json.loads(FACE_INPUTS.read_text())
    face = pinned["face"]
    core = pinned["core"]
    rho_be = face["rho"]
    e_be = face["E_today_Pa"]
    s_be = face["strength_today_Pa"]
    spec_be = e_be / rho_be
    wr_be = rho_be / cbrt(e_be)
    st_be = rho_be / s_be

    rows = []
    for row in delta["rows"]:
        if row["law"] != "handbook" or row["Q"] != 0.33 or row["gamma"] != 0.2:
            continue
        factor = row["density_factor"]
        rows.append({
            "R_m": row["R_m"],
            "weather": row["weather"],
            "concept_binding": row["concept_binding"],
            "TRL7_binding": row["TRL7_binding"],
            "density_factor": factor,
            "target_density_kg_m3": rho_be / factor,
            "admissible": True,
            "note": "Keeps the programme SR-200 modulus and strength. Handbook gamma 0.20 and Q 0.33.",
        })

    areas = {r: two_faces(r) for r in (20, 30)}
    sheet_m2 = 0.6096 * 1.8288

    faces = [
        {
            "id": "sr200-programme",
            "name": "SR-200 rolled sheet, programme tuple",
            "form": "cross-rolled sheet",
            "rho": rho_be,
            "E_Pa": e_be,
            "sigma_Pa": s_be,
            "sigma_kind": "programme tensile yield transferred to compression",
            "gauge": "Materion page: made to order 0.020 to 0.250 in, maximum 24 by 72 in",
            "sheet_m2": sheet_m2,
            "readiness": "production",
            "admissibility": "admissible with a named limit",
            "limit": "The programme tuple is the hull model's face. It is not a new compression test of a formed shell on CR-III. A partial SAE AMS 7902 extract gives a lower minimum yield.",
            "source": "040 INPUTS face block, copied under MAINLINE-064; Materion product page via environmental-expert; NTRS 19940006718 for the Fenn 1967 in-plane moduli",
        },
        {
            "id": "sr200-sae-minimum",
            "name": "SAE SR200 minimum, sheet specification floor",
            "form": "sheet",
            "rho": 1850.0,
            "E_Pa": 293.0e9,
            "sigma_Pa": 206.8e6,
            "sigma_kind": "minimum tensile yield, not compression",
            "gauge": "same SR-200 product page, 0.020 to 0.250 in",
            "sheet_m2": sheet_m2,
            "readiness": "production",
            "admissibility": "admissible with a named limit",
            "limit": "Total Materia extract of SAE AMS 7902H: compression modulus 293 GPa, tensile yield at least 206.8 MPa. Density is the 1.85 g/cm3 figure, not printed on that extract.",
            "source": "https://www.totalmateria.com/en-us/material/3304540",
        },
        {
            "id": "i220h-block",
            "name": "Materion I-220-H",
            "form": "block, rod or bar, not sheet",
            "rho": 1844.0,
            "E_Pa": 303.0e9,
            "sigma_Pa": 345.0e6,
            "sigma_kind": "minimum tensile yield",
            "gauge": "not a rolled face sheet",
            "sheet_m2": None,
            "readiness": "production, instrument blanks",
            "admissibility": "not admissible",
            "limit": "Not the sheet product form the hull face uses.",
            "source": "MatWeb archive of Materion I-220-H Grade 2 minimums",
        },
        {
            "id": "albemet-162-sheet",
            "name": "AlBeMet AM162 rolled sheet",
            "form": "rolled sheet",
            "rho": 2071.0,
            "E_Pa": 193.0e9,
            "sigma_Pa": 276.0e6,
            "sigma_kind": "minimum tensile yield",
            "gauge": "not stated on the pages read",
            "sheet_m2": None,
            "readiness": "production",
            "admissibility": "admissible with a named limit",
            "limit": "Rolled-sheet minimums. Not a compression allowables of a bonded sandwich face. Gauge and yearly area were not on the pages read.",
            "source": "https://www.lookpolymers.com/pdf/Materion-AlBeMet-AM-162-Rolled-Sheet-Annealed.pdf",
        },
        {
            "id": "cvd-diamond",
            "name": "CVD diamond window",
            "form": "flat or spherical disk, not a hull sheet",
            "rho": 3515.0,
            "E_Pa": 1050.0e9,
            "sigma_Pa": 750.0e6,
            "sigma_kind": "tensile, 500 µm, nucleation side",
            "gauge": "10 to 2000 µm, diameter up to 100 mm",
            "sheet_m2": math.pi * 0.050 ** 2,
            "readiness": "production for small optics",
            "admissibility": "not admissible",
            "limit": "Disks up to 100 mm. The strength is tensile at one thickness, not biaxial compression of a sandwich face.",
            "source": "https://www.diamond-materials.com/en/cvd-diamond/mechanical and the Diamond Materials CVD booklet",
        },
        {
            "id": "boron-epoxy-qi",
            "name": "boron/epoxy quasi-isotropic, textbook typical",
            "form": "quasi-isotropic laminate",
            "rho": 80.3e9 / (3820.0e3 * 9.80665),
            "E_Pa": 80.3e9,
            "sigma_Pa": None,
            "sigma_kind": "not given for the quasi-isotropic laminate",
            "gauge": "a ply stack, not a stated hull gauge",
            "sheet_m2": None,
            "readiness": "coupon; boron/epoxy has been a production laminate",
            "admissibility": "not admissible",
            "limit": "Vasiliev table of typical quasi-isotropic laminates. The extract prints specific modulus 3820. Read as 3820e3 m, which is E over rho g, the density is 2144 kg/m3. Read as 3820 m, the density is a thousand times a composite and the row is unusable. Not a lot certificate.",
            "source": "https://www.sciencedirect.com/topics/engineering/quasi-isotropic-laminate",
        },
        {
            "id": "carbon-epoxy-qi",
            "name": "carbon/epoxy quasi-isotropic, textbook typical",
            "form": "quasi-isotropic laminate",
            "rho": 54.8e9 / (3530.0e3 * 9.80665),
            "E_Pa": 54.8e9,
            "sigma_Pa": None,
            "sigma_kind": "not given for the quasi-isotropic laminate",
            "gauge": "a ply stack, not a stated hull gauge",
            "sheet_m2": None,
            "readiness": "production laminate family, this row is a textbook typical",
            "admissibility": "not admissible",
            "limit": "Same Vasiliev table. Printed specific modulus 3530 is read as 3530e3 m. Ordinary carbon/epoxy, not a high-modulus lot.",
            "source": "https://www.sciencedirect.com/topics/engineering/quasi-isotropic-laminate",
        },
        {
            "id": "m60j-ud",
            "name": "Toray M60J / epoxy, unidirectional, 60% fiber volume",
            "form": "unidirectional coupon, not the biaxial membrane",
            "rho": 0.60 * 1930.0 + 0.40 * 1200.0,
            "E_Pa": 360.0e9,
            "sigma_Pa": 790.0e6,
            "sigma_kind": "unidirectional compressive strength",
            "gauge": "coupon; fiber filament 5 µm",
            "sheet_m2": None,
            "readiness": "production fiber, coupon laminate",
            "admissibility": "not admissible",
            "limit": "The sphere's membrane is biaxial, so a laminate counts at its quasi-isotropic value. This row is the unidirectional upper bound. Composite density uses an assumed resin density of 1200 kg/m3, which is not on the Toray sheet. A quasi-isotropic modulus was not measured here and would be lower.",
            "source": "Toray M60J technical data sheet, composite properties normalized to 60% fiber volume",
        },
        {
            "id": "cnt-yarn-ud",
            "name": "Miralon CNT yarn / cyanate, unidirectional laminate",
            "form": "unidirectional laboratory laminate",
            "rho": 1380.0,
            "E_Pa": 329.0e9,
            "sigma_Pa": None,
            "sigma_kind": "tensile only in the paper; compressive strength not used",
            "gauge": "about 0.19 mm coupons",
            "sheet_m2": None,
            "readiness": "lab",
            "admissibility": "not admissible",
            "limit": "ACS Appl. Nano Mater. 2023, 6, 11260. The paper's best specific modulus is 256 GPa per g/cm3, unidirectional. Not quasi-isotropic and not a compressive face sheet.",
            "source": "https://doi.org/10.1021/acsanm.3c01282",
            "specific_modulus_claim_Pa_per_kg_m3": 256.0e9 / 1000.0,
        },
        {
            "id": "miralon-sheet",
            "name": "Miralon CNT nonwoven sheet",
            "form": "nonwoven sheet",
            "rho": 650.0,
            "E_Pa": None,
            "sigma_Pa": None,
            "sigma_kind": "specific strength cited as 50 to 200 MPa per g/cm3; modulus column was ambiguous and is not used",
            "gauge": "sheet, thickness not taken from that table",
            "sheet_m2": None,
            "readiness": "commercial sheet, not a structural face",
            "admissibility": "not admissible",
            "limit": "Secondary table of manufacturer figures. No compressive biaxial modulus was read cleanly.",
            "source": "TechConnect Briefs 2022, table citing Huntsman Miralon",
        },
        {
            "id": "al-6061-common",
            "name": "aluminium 6061-T6, common brief",
            "form": "sheet or plate",
            "rho": 2700.0,
            "E_Pa": 68.9e9,
            "sigma_Pa": 276.0e6,
            "sigma_kind": "typical tensile yield transferred to compression",
            "gauge": "ordinary mill product",
            "sheet_m2": None,
            "readiness": "production",
            "admissibility": "admissible with a named limit",
            "limit": "COMMON.md's pinned comparison metal. Not a candidate anyone expects to beat beryllium. Included so the ranking has a floor.",
            "source": "COMMON.md aluminium 6061-T6 block",
        },
    ]

    cores = [
        {
            "id": "criii-5056-3/8-1.0",
            "name": "Hexcel CR-III 5056 3/8-1.0",
            "rho": core["rho"],
            "Ec_Pa": core["Ec_Pa"],
            "Gc_Pa": core["Gc_Pa"],
            "Gc_direction": "W",
            "readiness": "production",
            "screen": "baseline",
            "admissibility": "admissible with a named limit",
            "limit": "Datasheet typicals for flat honeycomb. Not an installed core on a 20 to 30 m beryllium sphere.",
            "source": core["source"],
        },
        {
            "id": "hrh10-6.4-24",
            "name": "Hexcel HRH-10 6.4 mm cell, 24 kg/m3",
            "rho": 24.0,
            "Ec_Pa": 41.0e6,
            "Gc_Pa": 9.0e6,
            "Gc_direction": "W",
            "readiness": "production",
            "screen": "heavier and softer than the baseline",
            "admissibility": "admissible with a named limit",
            "limit": "EU datasheet typicals. Lightest hexagonal grade in the table read. Aramid paper, not the hull bond.",
            "source": "https://www.hexcel.com/wp-content/uploads/2025/12/HexWeb_HRH10_DataSheet_eu1.pdf",
        },
        {
            "id": "ucf-51-3/8-2.0",
            "name": "Ultracor UCF-51-3/8-2.0 carbon honeycomb",
            "rho": 32.0,
            "Ec_Pa": None,
            "Gc_Pa": None,
            "Gc_L_Pa": 331.0e6,
            "Gc_direction": "ribbon shear only; W and Ec not on the sheet read",
            "readiness": "production, satellite panels, about 36 by 24 in",
            "screen": "heavier; support index not computed",
            "admissibility": "not admissible",
            "limit": "Ribbon shear modulus and compressive strength are published. Through-thickness modulus is not on the sheet read, so wrinkling support is not ranked.",
            "source": "https://www.lookpolymers.com/pdf/Ultracor-UCF-51-38-20-Honeycomb-Core-Material.pdf",
            "compressive_strength_Pa": 1.41e6,
        },
    ]

    bonds = [
        {
            "id": "af163-2u-0.030",
            "name": "3M AF 163-2U, 0.030 lb/ft2",
            "areal_kg_m2": 0.030 * LB_PER_FT2,
            "flatwise_Pa": 800.0 * 6894.75729,
            "readiness": "production",
            "admissibility": "admissible with a named limit",
            "limit": "Flatwise tensile 800 psi at 75 F is on aluminium skins and 5052 honeycomb, not beryllium on CR-III 5056.",
            "source": "3M Scotch-Weld AF 163-2 technical data sheet, November 2009",
        },
        {
            "id": "af163-2u-0.015",
            "name": "3M AF 163-2U, 0.015 lb/ft2",
            "areal_kg_m2": 0.015 * LB_PER_FT2,
            "flatwise_Pa": None,
            "readiness": "production",
            "admissibility": "admissible with a named limit",
            "limit": "Catalog weight of the unsupported film. Flatwise strength at 0.015 lb/ft2 was not in the rows read. This weight matches the programme's favorable film.",
            "source": "3M Scotch-Weld AF 163-2 technical data sheet, product table",
        },
    ]

    def face_row(item):
        rho, E, sigma = item["rho"], item["E_Pa"], item["sigma_Pa"]
        out = {
            "id": item["id"],
            "name": item["name"],
            "form": item["form"],
            "density_kg_m3": rho,
            "E_Pa": E,
            "compressive_strength_Pa": sigma,
            "strength_kind": item["sigma_kind"],
            "readiness": item["readiness"],
            "admissibility": item["admissibility"],
            "limit": item["limit"],
            "source": item["source"],
            "gauge": item["gauge"],
            "tag": "QUESTIONABLE",
        }
        if item["sheet_m2"]:
            out["piece_m2"] = item["sheet_m2"]
            out["pieces_for_two_faces"] = {
                str(r): areas[r] / item["sheet_m2"] for r in (20, 30)
            }
        if E:
            out["specific_modulus_Pa_per_kg_m3"] = E / rho
            out["specific_modulus_over_beryllium"] = (E / rho) / spec_be
            out["wrinkling_index_rho_over_E_cbrt"] = rho / cbrt(E)
            out["wrinkling_index_improvement_over_beryllium"] = wr_be / (rho / cbrt(E))
        if sigma:
            out["strength_index_rho_over_sigma"] = rho / sigma
            out["strength_index_improvement_over_beryllium"] = st_be / (rho / sigma)
        if "specific_modulus_claim_Pa_per_kg_m3" in item:
            claim = item["specific_modulus_claim_Pa_per_kg_m3"]
            out["paper_specific_modulus_claim_Pa_per_kg_m3"] = claim
            out["paper_specific_modulus_over_beryllium"] = claim / spec_be
        clears = []
        for case in rows:
            factor = case["density_factor"]
            same = (
                E is not None
                and sigma is not None
                and abs(E - e_be) / e_be < 0.02
                and abs(sigma - s_be) / s_be < 0.02
                and rho <= rho_be / factor + 1e-6
            )
            entry = {
                "R_m": case["R_m"],
                "weather": case["weather"],
                "factor": factor,
                "keeps_beryllium_properties_and_clears_density": same,
            }
            if E:
                entry["clears_specific_modulus_index"] = (E / rho) / spec_be >= factor
                entry["clears_wrinkling_index"] = wr_be / (rho / cbrt(E)) >= factor
            if sigma:
                entry["clears_strength_index"] = st_be / (rho / sigma) >= factor
            clears.append(entry)
        out["against_handbook_factors"] = clears
        return out

    face_rows = [face_row(item) for item in faces]

    def core_row(item):
        Ec, Gc = item["Ec_Pa"], item["Gc_Pa"]
        out = {
            "id": item["id"],
            "name": item["name"],
            "density_kg_m3": item["rho"],
            "Ec_Pa": Ec,
            "Gc_Pa": Gc,
            "Gc_direction": item["Gc_direction"],
            "readiness": item["readiness"],
            "screen": item["screen"],
            "admissibility": item["admissibility"],
            "limit": item["limit"],
            "source": item["source"],
            "tag": "QUESTIONABLE",
        }
        if "Gc_L_Pa" in item:
            out["Gc_L_Pa"] = item["Gc_L_Pa"]
        if "compressive_strength_Pa" in item:
            out["compressive_strength_Pa"] = item["compressive_strength_Pa"]
        if Ec and Gc:
            out["wrinkling_support_Pa"] = (Ec * Gc) ** (1.0 / 3.0)
        return out

    core_rows = [core_row(item) for item in cores]
    support_base = core_rows[0]["wrinkling_support_Pa"]
    for row in core_rows:
        if "wrinkling_support_Pa" in row:
            row["support_over_baseline"] = row["wrinkling_support_Pa"] / support_base

    bond_rows = []
    for item in bonds:
        bond_rows.append({
            "id": item["id"],
            "name": item["name"],
            "areal_mass_kg_m2": item["areal_kg_m2"],
            "two_interfaces_kg_m2": 2.0 * item["areal_kg_m2"],
            "flatwise_Pa": item["flatwise_Pa"],
            "over_baseline_0.030": item["areal_kg_m2"] / (0.030 * LB_PER_FT2),
            "readiness": item["readiness"],
            "admissibility": item["admissibility"],
            "limit": item["limit"],
            "source": item["source"],
            "tag": "QUESTIONABLE",
        })

    def rank_key(rows, key, reverse):
        usable = [r for r in rows if key in r and r[key] is not None]
        ordered = sorted(usable, key=lambda r: r[key], reverse=reverse)
        return [r["id"] for r in ordered]

    result = {
        "unit": "vacuum-mainline067-materials-pathway-1020",
        "tag": "QUESTIONABLE / PROJECTION",
        "qualified_hull_SF": None,
        "started": "2026-10-20T17:42:44-07:00",
        "simjob": None,
        "why_no_simjob": "Literature ranking and one arithmetic script. One core, seconds. No sweep.",
        "baseline": {
            "face": "SR-200",
            "density_kg_m3": rho_be,
            "E_today_Pa": e_be,
            "strength_today_Pa": s_be,
            "specific_modulus_Pa_per_kg_m3": spec_be,
            "wrinkling_index_rho_over_E_cbrt": wr_be,
            "strength_index_rho_over_sigma": st_be,
            "core": core["name"],
            "core_density_kg_m3": core["rho"],
            "Ec_Pa": core["Ec_Pa"],
            "Gc_W_Pa": core["Gc_Pa"],
        },
        "face_area_m2": {
            "formula": "2 * 4 * pi * R^2, both faces at the outer radius",
            "R20": areas[20],
            "R30": areas[30],
            "limit": "The inner face is smaller. This area is slightly high.",
        },
        "handbook_cases": rows,
        "ramp_not_used": "063's ramp at Q 0.33 has density factors 1.06 to 1.12 and is not admissible. It is not a clear criterion.",
        "faces": face_rows,
        "face_rank": {
            "specific_modulus_high_better": rank_key(face_rows, "specific_modulus_over_beryllium", True),
            "wrinkling_index_high_improvement_better": rank_key(
                face_rows, "wrinkling_index_improvement_over_beryllium", True
            ),
            "strength_index_high_improvement_better": rank_key(
                face_rows, "strength_index_improvement_over_beryllium", True
            ),
            "membrane_ids": [
                "sr200-programme", "sr200-sae-minimum", "albemet-162-sheet",
                "boron-epoxy-qi", "carbon-epoxy-qi", "al-6061-common",
            ],
            "excluded_from_membrane_rank": {
                "i220h-block": "not sheet",
                "cvd-diamond": "100 mm disks",
                "m60j-ud": "unidirectional upper bound",
                "cnt-yarn-ud": "unidirectional upper bound",
                "miralon-sheet": "no modulus read",
            },
        },
        "cores": core_rows,
        "core_rank": {
            "density_low_better": rank_key(core_rows, "density_kg_m3", False),
            "wrinkling_support_high_better": rank_key(core_rows, "wrinkling_support_Pa", True),
        },
        "bonds": bond_rows,
        "answer": {
            "clears_today_keeping_beryllium_properties": [],
            "statement": (
                "No candidate keeps SR-200's modulus and strength and divides the density "
                "by 1.74 to 1.86. SR-200 leads the wrinkling index. Diamond leads specific "
                "modulus and still fails wrinkling. No core read is lighter than CR-III "
                "3/8-1.0 and stiffer. AF 163-2U at 0.015 lb/ft2 is half the baseline film "
                "and does not clear the face factors. T3 and T7 stay on SR-200 bonded to CR-III."
            ),
        },
        "projection": {
            "tag": "PROJECTION",
            "build_time_density_at_beryllium_stiffness_kg_m3": "993 to 1061, the four handbook targets",
            "credible_trend": (
                "No published metal trend reaches that density at 290 GPa. The closest measured "
                "specific modulus, a unidirectional CNT yarn laminate at 256 GPa per g/cm3, is "
                "still short of 1.74 times SR-200 and is not quasi-isotropic. Diamond already "
                "exceeds the specific-modulus factor as 100 mm disks. That is not a hull-sheet trend."
            ),
        },
    }
    (ROOT / "RESULTS.json").write_text(json.dumps(result, indent=2) + "\n")
    print("wrote", ROOT / "RESULTS.json")
    print("areas", areas)
    print("sheet", sheet_m2, "pieces", {r: areas[r] / sheet_m2 for r in areas})
    print("spec_be", spec_be, "wr_be", wr_be, "st_be", st_be)
    for row in face_rows:
        print(
            row["id"],
            "spec", round(row.get("specific_modulus_over_beryllium") or -1, 3),
            "wr", round(row.get("wrinkling_index_improvement_over_beryllium") or -1, 3),
            "st", round(row.get("strength_index_improvement_over_beryllium") or -1, 3),
        )
    for row in core_rows:
        print(row["id"], "rho", row["density_kg_m3"], "support", row.get("wrinkling_support_Pa"), "over", row.get("support_over_baseline"))
    for row in bond_rows:
        print(row["id"], row["areal_mass_kg_m2"], row["flatwise_Pa"])


if __name__ == "__main__":
    main()
