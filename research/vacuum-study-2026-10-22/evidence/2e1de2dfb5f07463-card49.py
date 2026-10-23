#!/usr/bin/env python3
"""MAINLINE-049: CARD.md, RESULTS.json, NFI.json and INPUTS.json.

The primary account is FOLD.json: 048's finish and water in place of 040's coating and water, with CHECK-040's rows.
COMPUTE.json, SENS.json and EXTRA.json hold the same constructions under 040's coating and water, kept for comparison."""
import datetime
import hashlib
import json
import os
import re

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

BE = "Be | CR-III 5056 3/8-1.0 | AF163-2U 200 F"
ALB = "AlBeMet AM162 | CR-III 5056 3/8-1.0 | 040's Be scarf and stock"
M200 = "M55J QI | CR-III 5056 3/8-1.0 | AF163-2U 200 F"
MRT = "M55J QI | CR-III 5056 3/8-1.0 | room-temperature cure (PROJECTION)"
MH10 = "M55J QI | HRH-10-3/8-1.5 | AF163-2U 200 F"
MH49 = "M55J QI | HRH-49-1/4-2.1 | AF163-2U 200 F"
K200 = "K13D2U QI | CR-III 5056 3/8-1.0 | AF163-2U 200 F"
KRT = "K13D2U QI | CR-III 5056 3/8-1.0 | room-temperature cure (PROJECTION)"
KH10 = "K13D2U QI | HRH-10-3/8-1.5 | AF163-2U 200 F"
KH49 = "K13D2U QI | HRH-49-1/4-2.1 | AF163-2U 200 F"
K60 = "K13D2U QI at 60% Vf (PROJECTION) | CR-III 5056 3/8-1.0 | room-temperature cure (PROJECTION)"
K60C = "K13D2U QI at 60% Vf (PROJECTION) | CR-III 5056 3/8-1.0 | 50 C cure (PROJECTION)"
SHORT = {BE: "Be SR-200 on 5056, 200 F bond", ALB: "AlBeMet on 5056, 200 F bond", M200: "M55J on 5056, 200 F bond",
         MRT: "M55J on 5056, room-temperature bond", MH10: "M55J on HRH-10, 200 F bond", MH49: "M55J on HRH-49, 200 F bond",
         K200: "K13D2U on 5056, 200 F bond", KRT: "K13D2U on 5056, room-temperature bond",
         KH10: "K13D2U on HRH-10, 200 F bond", KH49: "K13D2U on HRH-49, 200 F bond",
         K60: "K13D2U 60% Vf (PROJECTION) on 5056, room-temperature bond",
         K60C: "K13D2U 60% Vf (PROJECTION) on 5056, 50 C bond"}
ORDER = [BE, K60, K60C, KRT, MRT, ALB, KH49, MH49, KH10, MH10, K200, M200]
CON = {c["key"]: c for c in FD["constructions"]}
OLD_ROWS = C["rows"] + EX["k13_60"]["rows"]
R3 = (15, 20, 30)
VAR = [("MLCCAg", "primary", "Primary"), ("MLCCAg", "water_1mm", "1 mm water"),
       ("MLCCAg", "cure_in_global", "Cure in global and crimp"), ("MLCCAg", "edge_scarf", "Edge/scarf coincidence"),
       ("MLCCAg", "dry_gas", "Dry gas, no drying credit"), ("CCAg", "primary", "Classical CCAg")]


def f(key, R, w="ISA", fl=False, v="primary", fin="MLCCAg"):
    return next(x for x in FD["rows"] if x["construction"] == key and x["variant"] == v and x["finish"] == fin
                and x["R_m"] == R and x["weather"] == w and x["floor"] == fl)


def o(key, R, w="ISA", fl=False):
    lab = CON[key]["label"]
    return next(x for x in OLD_ROWS if x["case"] == lab and x["R_m"] == R and x["weather"] == w and x["floor"] == fl)


def t(x, nd=1):
    if x is None:
        return "none feasible"
    return f"{x / 1000:+.{max(nd, 2) if abs(x) < 1000 else nd}f} t"


def tt(x, nd=1):
    return "n/a" if x is None else f"{x / 1000:.{nd}f} t"


def axes(r):
    return "none" if r["least_axes"] is None else " + ".join(r["least_axes"])


def need(r):
    lp = r["least"]
    if lp is None:
        return "none floats"
    s = f"{lp['gamma']:.3f} (x{lp['gamma_x']:.2f}) / {lp['Q']:.3f} (x{lp['Q_x']:.2f}) / {lp['Fcy_Pa'] / 1e6:.0f} MPa (x{lp['Fcy_x']:.2f})"
    if "film" in r["least_axes"]:
        s += f" / film {lp['film_kg_m2'] * 1000:.0f} g/m2"
    return s


def triple(fn):
    return " / ".join(fn(R) for R in R3)


def simjob_record():
    rec = []
    for name in ("run49", "sens49", "extra49", "fold49"):
        p = f"{LOGS}/{name}-simjob.log"
        if not os.path.exists(p):
            rec.append({"run": name, "log": None})
            continue
        txt = open(p).read()
        rec.append({"run": name, "attempts": len(re.findall(r"^attempt \d+ start", txt, re.M)),
                    "refusals": len(re.findall(r"^attempt \d+ exit 75 ", txt, re.M)),
                    "admitted": re.findall(r"^simjob: ADMITTED .*$", txt, re.M),
                    "ended": re.findall(r"^simjob: ENDED .*$", txt, re.M),
                    "final": re.findall(r"^FINAL .*$", txt, re.M)})
    return rec


def main():
    L = []
    a = L.append
    fins = FD["finishes"]
    k60 = FD["k60"]
    wf = FD["water_fractions"]
    sup = C["supply"]
    faces = C["faces"]
    tf_rows = FD["thermal_factors"]
    own = FD["thermal_factors_own_geometry"]
    dry = FD["dry_gas_pressure_at_primary_geometry"]
    em = {(e["construction"], e["R_m"]): e["k_E"] for e in FD["E_multiplier_to_float"]}
    em0 = {(e["face"], e["core"], e["R_m"]): e["k_E"] for e in SE["E_multiplier_to_float"]}
    edge_f = [e for e in FD["edge_vs_cure"] if e["construction"] == MRT]
    edge_f60 = [e for e in FD["edge_vs_cure"] if e["construction"] == K60]
    edge_0 = {round(e["cure_K"], 2): e for e in SE["edge_vs_cure"]}

    def tfac(fin, key):
        return next(x for x in tf_rows if x["finish"] == fin and x["construction"] == key)

    def ownf(key, R):
        return next((x for x in own if x["construction"] == key and x["R_m"] == R), None)
    # facts used in the text
    k30 = f(K60, 30)
    b30 = f(BE, 30)
    fib_frac = FD["supply_inputs"]["face_fibre_fraction"]["K13D2U QI"]
    k_face30 = k30["least"]["faces_kg"]
    k_fib30 = k_face30 * fib_frac
    be_face30 = b30["least"]["faces_kg"]
    alb_face30 = f(ALB, 30)["faces_at_all_endpoint_kg"]
    alb_be30 = alb_face30 * FD["supply_inputs"]["albemet_be_fraction"]
    pitch, be_world = sup["pitch_capacity_t"], sup["be_world_t_2024"]
    any_sourced_float = any(f(k, R, w, fl)["least"] is not None for k in (ALB, M200, MRT, MH10, MH49, K200, KRT, KH10, KH49)
                            for R in R3 for w in ("ISA", "optimistic") for fl in (False, True))
    k60_floats_all = all(f(k, R, w, fl)["least"] is not None for k in (K60, K60C) for R in R3
                         for w in ("ISA", "optimistic") for fl in (False, True))
    be_two_axes = all(f(BE, R, w, fl)["least_axes"] == ["gamma", "Q"] for R in R3 for w in ("ISA", "optimistic")
                      for fl in (False, True))
    mm_float = {k: [(R, w) for R in R3 for w in ("ISA", "optimistic") if f(k, R, w, v="water_1mm")["least"] is not None]
                for k in ORDER}
    mm_only_r30 = all(R == 30 for v in mm_float.values() for R, _ in v)
    cig_lost = [(k, R, w) for k in ORDER for R in R3 for w in ("ISA", "optimistic")
                if f(k, R, w)["least"] is not None and f(k, R, w, v="cure_in_global")["least"] is None]
    es_lost = [(k, R, w) for k in ORDER for R in R3 for w in ("ISA", "optimistic")
               if f(k, R, w)["least"] is not None and f(k, R, w, v="edge_scarf")["least"] is None]

    def cost(v, keys, fin="MLCCAg"):
        d = [f(k, R, w)["endpoint_all_kg"] - f(k, R, w, v=v, fin=fin)["endpoint_all_kg"] for k in keys for R in R3
             for w in ("ISA", "optimistic") if f(k, R, w)["endpoint_all_kg"] is not None
             and f(k, R, w, v=v, fin=fin)["endpoint_all_kg"] is not None]
        return min(d), max(d)
    cig = cost("cure_in_global", [BE, K60, K60C])
    cig_rest = cost("cure_in_global", [k for k in ORDER if k not in (BE, K60, K60C, M200, K200)])
    esb = cost("edge_scarf", [BE])
    esc = cost("edge_scarf", [K60, K60C, KRT, MRT, KH10, KH49, MH10, MH49])
    dgc = cost("dry_gas", [BE, K60, K60C, KRT, MRT, ALB])
    ccg = cost("primary", [k for k in ORDER if k not in (M200, K200)], fin="CCAg")
    aramid_dry_infeasible = all(f(k, R, w, v="dry_gas")["endpoint_all_kg"] is None for k in (KH10, KH49, MH10, MH49)
                                for R in R3 for w in ("ISA", "optimistic"))
    dry_ar = [d for d in dry if "HRH" in d["construction"]]
    usage_be = [f(BE, R)["least_usage"] for R in R3]
    usage_k = [f(K60, R)["least_usage"] for R in R3]
    gb = [f(BE, R)["least"]["tf_m"] * 1e3 for R in R3]
    fc60 = [f(K60, R)["least"]["Fcy_Pa"] / 1e6 for R in R3]

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

    # ------------------------------------------------------------------ 1. faces
    a("## 1. The faces")
    a("")
    a("| Face | Density, kg/m3 | E (QI) | Poisson | Compression today -> full | CTE | Minimum gauge | Water uptake | Basis |")
    a("|---|---|---|---|---|---|---|---|---|")
    a("| Be SR-200 (040) | 1850 | 290 GPa | 0.0768 | 345 -> 379.2 MPa | 11.3 ppm/K | n/a | none charged | 040's inputs |")
    for k, fc in faces.items():
        ff = fc["face"]
        wtxt = "none charged" if k == "AlBeMet AM162" else f"{wf['face_cfrp'] * 100:.2f}% (PROJECTION)"
        a(f"| {k} | {ff['rho']:.0f} | {ff['E_today_Pa'] / 1e9:.1f} GPa | {fc['nu']:.3f} | "
          f"{ff['strength_today_Pa'] / 1e6:.0f} -> {ff['strength_full_Pa'] / 1e6:.0f} MPa | {fc['alpha'] * 1e6:.2f} ppm/K | "
          f"{fc['tf_min'] * 1e3:.3f} mm | {wtxt} | {'; '.join(f'{kk}: {vv}' for kk, vv in fc['basis'].items())} |")
    a(f"| K13D2U QI at 60% Vf (PROJECTION) | {faces['K13D2U QI']['face']['rho']:.0f} | {k60['E_QI_Pa'] / 1e9:.1f} GPa | "
      f"{k60['nu_QI']:.3f} | 220 -> {220 / (1 - k60['nu_QI']):.0f} MPa | as K13D2U QI | as K13D2U QI | "
      f"{wf['face_cfrp'] * 100:.2f}% (PROJECTION) | E1 = 935 GPa fibre x {k60['translation']:.3f} (Toray's M55J lamina/fibre ratio) |")
    a("")
    a("Notes on the faces:")
    a("- **M55J:** the quasi-isotropic modulus, compression and CTE are Rock West's calculated plate values; it says "
      "tested values are \"coming soon\". Toray's UD composite gives Xc 890 MPa at E1 338 GPa (60% Vf).")
    a("- **K13D2U:** the modulus is [0/+-60] laminate theory on Tuttle's measured lamina (E1 410, E2 5.56, G12 4.10 "
      "GPa, nu12 0.39; one specimen each, Vf unstated). No K13D2U compression strength was found; the 220 MPa is 014b's.")
    a("- **The full compression** for CFRP is the equal-biaxial reading of a fibre-strain limit, uniaxial/(1-nu). It "
      "is this seat's PROJECTION; a metal's equal-biaxial yield equals its uniaxial yield.")
    a("- **AlBeMet:** rolled-sheet minimum and typical tensile yield stand in for compression; no compressive yield "
      "is printed. It is 62 wt% beryllium.")
    a("- **CFRP water:** the P75S/954-3 pitch/cyanate quasi-isotropic laminate at 55% RH saturation (0.18%, the highest "
      "of three such laminates; Brand and Derby). EX-1515's own sheet gives 0.04% on P75 at 85% RH; a 954-3 sheet "
      "column gives 0.704%, an epoxy T300/5208 0.92% at 75% RH.")
    a("")

    # ------------------------------------------------------------------ 2. construction
    a("## 2. The construction")
    a("")
    h10, h49 = C["cores"]["HRH-10-3/8-1.5"], C["cores"]["HRH-49-1/4-2.1"]
    a("**Cores:**")
    a("- **CR-III 5056 3/8-1.0:** 040's core, 16 kg/m3, W shear modulus 46.9 MPa. Material water 0.1% (048's "
      "assumption).")
    a(f"- **HRH-10-3/8-1.5 (Nomex):** 24 kg/m3, W {h10['core']['Gc_Pa'] / 1e6:.1f} MPa, Ec {h10['core']['Ec_Pa'] / 1e6:.1f} "
      f"MPa. Material water {wf['core']['HRH-10-3/8-1.5'] * 100:.1f}%, Hexcel's HRH-10 pickup after 95% RH at 120 F "
      "for 120 h.")
    a(f"- **HRH-49-1/4-2.1 (Kevlar):** 33.6 kg/m3, W {h49['core']['Gc_Pa'] / 1e6:.2f} MPa, Ec {h49['core']['Ec_Pa'] / 1e6:.0f} "
      f"MPa. Material water {wf['core']['HRH-49-1/4-2.1'] * 100:.1f}%, HRH-36's pickup in the same test (PROJECTION); "
      "Kevlar 49 yarn holds 3.5% at 55% RH.")
    a("")
    a("No in-plane CTE is printed for any honeycomb, so each core's thickness-direction CTE stands in (PROJECTION): "
      "5056 23.6, Nomex 34.9 and HRH-49 4.86 ppm/K. A UCF carbon core has no sourced compressive modulus and is not run.")
    a("")
    a("**Material water by construction (before the bake's 90% removal):** faces "
      f"{wf['face_cfrp'] * 100:.2f}% for CFRP and none for metal; core as above; AF163-2U face-core film "
      f"{wf['face_core_film'] * 100:.1f}% (048's WVR); CFRP seam film {wf['seam_cfrp'] * 100:.2f}% (FM-300 at 49 C and "
      f"70% RH, NASA CR-3387); metal seam polymers {wf['seam_metal'] * 100:.0f}%, primer {wf['primer'] * 100:.0f}% and "
      f"finish {wf['finish'] * 100:.0f}% (048's assumptions). At R 30 the bake leaves "
      f"{f(BE, 30)['endpoint_all_bill_kg']['absorbed_water']:.1f} kg aboard for beryllium, "
      f"{f(K60, 30)['endpoint_all_bill_kg']['absorbed_water']:.1f} kg for the projection and "
      f"{min(f(k, 30)['endpoint_all_bill_kg']['absorbed_water'] for k in (KH10, KH49, MH10, MH49)):.0f}-"
      f"{max(f(k, 30)['endpoint_all_bill_kg']['absorbed_water'] for k in (KH10, KH49, MH10, MH49)):.0f} kg on the aramid "
      "cores.")
    a("")
    a("**037b's method for each pair.** The faces are bonded with AF163-2U at 200 F (366.5 K), as in 040. Aramid walls "
      "are soft, so their K_biax is small and they pass the free-edge screen at 200 F. On 5056, CFRP needs a bond "
      "stress-free at or below 50 C. The free-edge factor on minimum W strength, under the multilayer finish, at each "
      "construction's R 20 all-four endpoint geometry (040's paint in brackets):")
    a("")
    a("| Bond stress-free at | M55J on 5056 | K13D2U 60% Vf on 5056 | Free-edge shear (M55J) | Balanced face compression (M55J) | Cell wall (M55J) |")
    a("|---|---|---|---|---|---|")
    for e, e6 in zip(edge_f, edge_f60):
        old = edge_0.get(round(e["cure_K"], 2))
        a(f"| {e['cure_K'] - 273.15:.0f} C | {e['edge_SF']:.3f}" + (f" ({old['edge_SF']:.3f})" if old else "")
          + f" | {e6['edge_SF']:.3f} | {e['tau_Pa'] / 1e3:.0f} kPa | {e['cure_compression_Pa'] / 1e6:.1f} MPa | {e['wall_SF']:.2f} |")
    a("")
    a(f"Beryllium on the same core passes at 200 F ({tfac('MLCCAg', BE)['current_edge_SF']:.3f} under the multilayer "
      "finish, as in 048).")
    a("")
    seam = C["seam_cfrp"]
    a(f"**CFRP seams.** A co-cured scarf with FM 300-2M film: {seam['seam_film'] * 1000:.0f} g/m2 over the scarf faces "
      f"(beryllium's is 70), and a {seam['seam_screen'] / 1e6:.1f} MPa average-shear screen from co-cured wide-area lap "
      "shear on CFRP. That test failed in the laminate, so the screen is a lower bound. 040's 30.34:1 ratio and stock "
      "panel are kept (PROJECTION for CFRP). The screen does not bind for CFRP. At the R 30 all-four endpoint the seams "
      f"cost {f(K60, 30)['endpoint_all_joining']['total'] / 1000:.2f} t for the projection, "
      f"{f(KRT, 30)['endpoint_all_joining']['total'] / 1000:.2f} t for K13D2U and "
      f"{f(MRT, 30)['endpoint_all_joining']['total'] / 1000:.2f} t for M55J, against beryllium's "
      f"{f(BE, 30)['endpoint_all_joining']['total'] / 1000:.2f} t.")
    a("")

    # ------------------------------------------------------------------ 3. thermal factors
    a("## 3. The finish's thermal factors on each face")
    a("")
    a("048's screen asks for an 037 day factor of at least 1.678 and a full-cycle factor of at least 1. Both are 037's "
      "rigid-face shear at 037's source geometry (R 10, tf 0.80 mm, tc 22.1 mm), rescored here with each face's modulus "
      "and expansion mismatch and each core's stiffness and typical W strength. The edge factor is 037b's compliant "
      "screen at the construction's own bond temperature. The last column is the full-cycle factor at the construction's "
      "own all-four endpoint geometry, R 15 / 20 / 30, from the converged multilayer table.")
    a("")
    a("| Construction | Multilayer CCAg: day / full cycle / edge | Classical CCAg: day / full cycle / edge | 040 paint: day / full cycle / edge | Own geometry, full cycle |")
    a("|---|---|---|---|---|")
    for k in ORDER:
        cells = []
        for fin in ("MLCCAg", "CCAg", "reference040"):
            x = tfac(fin, k)
            mark = "" if (x["day_at_least_1_6775"] and x["cycle_at_least_1"]) else " (fails)"
            cells.append(f"{x['legacy_037_day_SF']:.2f} / {x['legacy_037_full_cycle_SF']:.3f} / {x['current_edge_SF']:.3f}{mark}")
        og = " / ".join("n/a" if ownf(k, R) is None else f"{ownf(k, R)['full_cycle_SF']:.2f}" for R in R3)
        a(f"| {SHORT[k]} | {cells[0]} | {cells[1]} | {cells[2]} | {og} |")
    a("")
    a("\"(fails)\" marks a day or full-cycle factor below the screen; the edge factor is screened in the account itself. "
      "The day and cycle factors depend only on the face and core, not on the bond temperature.")
    a("")

    # ------------------------------------------------------------------ 4. account
    a("## 4. The account")
    a("")
    a("The bill is 040's, with 048's finish and water: faces, core, actual joining (or 040's retained 5% floor), the "
      "multilayer finish, 10 g/m2 primer, the 70 kn pad, the gas charge, 100 kg systems, the 0.1 kg/m2 exterior film, "
      "the bake's residual material water, contamination and 031's weather headroom. Usage is 040's common "
      "logarithmic ceiling. Multipliers are on today's gamma 0.20, Q 0.33 and compression.")
    a("")
    a("| Construction | R | Weather | Least set | Usage | Gamma / Q / compression needed | All-four endpoint, actual / floor | Under 040's coating, actual | Faces at endpoint |")
    a("|---|---|---|---|---|---|---|---|---|")
    for k in ORDER:
        for R in R3:
            for w in ("ISA", "optimistic"):
                ra, rf, ro = f(k, R, w), f(k, R, w, True), o(k, R, w)
                a(f"| {SHORT[k]} | {R} | {w} | {axes(ra)} | "
                  f"{'n/a' if ra['least_usage'] is None else format(ra['least_usage'], '.3f')} | {need(ra)} | "
                  f"{t(ra['endpoint_all_kg'])} / {t(rf['endpoint_all_kg'])} | {t(ro['endpoint_all_kg'])} | "
                  f"{tt(ra['faces_at_all_endpoint_kg'])} |")
    a("")
    a("\"none feasible\" means no geometry passes every screen. For CFRP on 5056 at 200 F, the free-edge screen fails "
      "at every geometry. Floor rows that float have the same least set as the actual rows; their usage is in "
      "RESULTS.json.")
    a("")

    # ------------------------------------------------------------------ 5. CHECK-040 rows
    a("## 5. CHECK-040's rows and the alternatives")
    a("")
    a("All-four endpoint at ISA with actual joining; where a least set floats, it follows with its usage. Optimistic "
      "weather is in RESULTS.json for every construction.")
    a("")
    a("| Construction | R | " + " | ".join(v[2] for v in VAR) + " |")
    a("|---|---|" + "---|" * len(VAR))
    for k in ORDER:
        for R in R3:
            cells = []
            for fin, v, _ in VAR:
                r = f(k, R, v=v, fin=fin)
                s = t(r["endpoint_all_kg"])
                if r["least"] is not None:
                    s += f"; {axes(r)} {r['least_usage']:.3f}"
                cells.append(s)
            a(f"| {SHORT[k]} | {R} | " + " | ".join(cells) + " |")
    a("")
    a("For the two floating constructions in optimistic weather:")
    a("")
    a("| Construction | R | " + " | ".join(v[2] for v in VAR) + " |")
    a("|---|---|" + "---|" * len(VAR))
    for k in (BE, K60):
        for R in R3:
            cells = []
            for fin, v, _ in VAR:
                r = f(k, R, "optimistic", v=v, fin=fin)
                s = t(r["endpoint_all_kg"])
                if r["least"] is not None:
                    s += f"; {axes(r)} {r['least_usage']:.3f}"
                cells.append(s)
            a(f"| {SHORT[k]} | {R} | " + " | ".join(cells) + " |")
    a("")

    # ------------------------------------------------------------------ 6. E multipliers
    a("## 6. What would float the measured faces")
    a("")
    a("The face-modulus multiplier at which the build floats with all four optimisms at their endpoints (ISA, actual "
      "joining), R 15 / 20 / 30; 040's coating in brackets:")
    for k, fk, ck in ((KRT, "K13D2U QI", "CR-III 5056 3/8-1.0"), (MRT, "M55J QI", "CR-III 5056 3/8-1.0"),
                      (ALB, "AlBeMet AM162", "CR-III 5056 3/8-1.0"), (MH49, "M55J QI", "HRH-49-1/4-2.1"),
                      (KH49, "K13D2U QI", "HRH-49-1/4-2.1")):
        nv = " / ".join("none" if em.get((k, R)) is None else f"x{em[(k, R)]:.2f}" for R in R3)
        ov = " / ".join("none" if em0.get((fk, ck, R)) is None else f"x{em0[(fk, ck, R)]:.2f}" for R in R3)
        a(f"- **{SHORT[k]}:** {nv} ({ov}).")
    a("")
    a("\"none\" means no multiplier up to x8 floats it: shear crimping binds, and modulus does not lift crimping.")
    a("")

    # ------------------------------------------------------------------ 7. bill
    a("## 7. The bill at R 30")
    a("")
    a(f"All-four endpoint, ISA, actual joining, in tonnes. The lift is {f(BE, 30)['lift_kg'] / 1000:.1f} t.")
    a("")
    keys7 = (BE, K60, KRT, MRT, ALB)
    lines7 = [("faces", "Faces"), ("core", "Core"), ("charged_joining", "Joining"), ("coating", "Finish"),
              ("structural_primer", "Primer"), ("mooring_pad", "70 kn pad"), ("gas", "Gas"), ("systems", "Systems"),
              ("water", "Exterior water"), ("absorbed_water", "Material water after the bake"),
              ("contamination", "Contamination"), ("weather_headroom", "Weather headroom")]
    a("| Line | " + " | ".join(SHORT[k] for k in keys7) + " |")
    a("|---|" + "---|" * len(keys7))
    for kk, lab in lines7:
        a(f"| {lab} | " + " | ".join(f"{f(k, 30)['endpoint_all_bill_kg'][kk] / 1000:.3f}" for k in keys7) + " |")
    a("| Payload | " + " | ".join(f"{f(k, 30)['endpoint_all_kg'] / 1000:+.3f}" for k in keys7) + " |")
    a("")

    # ------------------------------------------------------------------ method
    a("## Method and checks")
    a("")
    a("This seat's own code, all pinned:")
    a("- **model49.py:** 040's model.py with the face, core, bond, seam, core conductivity, finish, primer and material "
      "water as inputs, and CHECK-040's cure-in-global switch. 048's water and pressure terms are ported verbatim.")
    a("- **thermal49.py:** 040's thermal.py with the core conductivity, the finish optics and 048's day-or-night "
      "convention as inputs.")
    a("- **laminate.py**, **acct49.py**, **src49.py**, **run49.py** (040's coating), **sens49.py** and **extra49.py** "
      "(040's coating), **fold49.py** (048's finish and water, and CHECK-040's rows) and **card49.py**.")
    a("")
    a("040's model and data were copied into base040/ with their sha256 pins and not changed. Every sourced value is "
      "drawn from the sourcing files by property and product, and asserted.")
    a("")
    a("**Checks:**")
    a("- **040:** all 12 heavy-pad, vented rows at R 15-30, ISA and optimistic, actual and floor. Least set and usage "
      "within 2e-8, endpoint within 1e-3 kg.")
    a(f"- **048:** {nc[0]} beryllium rows bit for bit. They cover both finishes, all three drying routes, both joining "
      "conventions, both weathers, dry exterior and R 10-15. 048's beryllium finish screen is reproduced to 1e-9.")
    a(f"- **CHECK-040:** all 26 cure-in-global and edge/scarf rows, and both 1 mm rows (-594.989 and -820.787 kg), "
      f"within {w40:.4f} kg.")
    a("- **Thermal tables:** 048's multilayer and classical tables at R 15, and 040's table, reproduced exactly.")
    a("- **The laminate code:** returns an isotropic lamina unchanged, and a T300-like quasi-isotropic modulus of "
      "54.7 GPa.")
    a("")
    a("**How the runs were made.** The standing simjob order and COMMON.md's two new lines ask for heavy runs to go "
      "through simjob, retrying a refusal unchanged. Removing exactly those two lines from COMMON.md gives back its "
      "dispatched sha256.")
    a("- **Before they were read:** run49 and a first fold run had gone bare (05:33 to 05:45, 13 threads, about 1 GB).")
    a("- **The pinned results:** every one comes from runs through simjob, retried at least a minute apart after "
      "memory-pressure refusals. The scope records are in RESULTS.json.")
    a("- **Bare and simjob runs agree:** they give identical numbers.")
    a("")
    a("## Then")
    a("")
    a("Stop and file. The robotics seat sends the next job. NFI.json carries the open rows. A checker runs behind this "
      "card.")
    text = "\n".join(L) + "\n"
    with open(os.path.join(HERE, "CARD.md.tmp"), "w") as fh:
        fh.write(text)
    os.replace(os.path.join(HERE, "CARD.md.tmp"), os.path.join(HERE, "CARD.md"))

    # ------------------------------------------------------------------ RESULTS.json
    now = datetime.datetime.now().astimezone().isoformat()

    def brief(r):
        return {"construction": r["construction"], "finish": r["finish"], "variant": r["variant"], "R_m": r["R_m"],
                "weather": r["weather"], "floor": r["floor"], "least_axes": r["least_axes"], "least_usage": r["least_usage"],
                "least": None if r["least"] is None else {k: v for k, v in r["least"].items() if k != "bill_kg"},
                "endpoint_all_kg": r["endpoint_all_kg"], "endpoint_028b_kg": r["endpoint_028b_kg"],
                "endpoint_today_kg": r["endpoint_today_kg"], "faces_at_all_endpoint_kg": r["faces_at_all_endpoint_kg"],
                "endpoint_all_binding": r["endpoint_all_binding"], "endpoint_all_geometry": r["endpoint_all_geometry"],
                "endpoint_all_bill_kg": r["endpoint_all_bill_kg"], "endpoint_all_vacuum": r["endpoint_all_vacuum"]}
    results = {
        "schema": 1, "card": "MAINLINE-049", "unit": "vacuum-mainline049-be-free-p2-1020", "orders": ORDERS,
        "status": "ESTIMATE", "tag": "QUESTIONABLE / PROJECTION", "certification": "none",
        "job_started_at": JOB_STARTED, "job_ended_at": now, "card_written_at": now,
        "times_are": "measurements only, never limits",
        "runs": {"fold49": {"started": FD["started"], "ended": FD["ended"], "elapsed_s": FD["elapsed_s"]},
                 "run49": {"started": C["started"], "ended": C["ended"], "elapsed_s": C["elapsed_s"]},
                 "sens49_elapsed_s": SE["elapsed_s"], "extra49_elapsed_s": EX["elapsed_s"],
                 "simjob": simjob_record(),
                 "bare_runs_before_the_order_was_read": "run49 (05:33-05:45) and the first fold49 run (05:35-05:41) ran "
                                                        "outside simjob; both were repeated through simjob with identical "
                                                        "numbers"},
        "common_amendment": FD["common_amendment"],
        "answer": {
            "sourced_be_free_floats": any_sourced_float,
            "projection_floats": "K13D2U QI at 60% Vf on CR-III 5056, bond stress-free at or below 50 C",
            "projection_least_R30_ISA": {"axes": k30["least_axes"], "usage": k30["least_usage"],
                                         **{k: v for k, v in k30["least"].items() if k != "bill_kg"}},
            "projection_all_four_endpoints_kg": {R: f(K60, R)["endpoint_all_kg"] for R in R3},
            "beryllium_least_axes": {R: f(BE, R)["least_axes"] for R in R3},
            "beryllium_usage_ISA": dict(zip(R3, usage_be)), "projection_usage_ISA": dict(zip(R3, usage_k)),
            "sourced_shortfalls_kg": {SHORT[k]: {R: f(k, R)["endpoint_all_kg"] for R in R3} for k in (KRT, ALB, MRT)},
            "water_1mm_floats": {SHORT[k]: v for k, v in mm_float.items() if v},
            "cure_in_global_cost_kg": {"floating": cig, "others": cig_rest}, "edge_scarf_cost_beryllium_kg": esb, "dry_gas_cost_5056_kg": dgc,
            "classical_ccag_difference_kg": ccg, "aramid_dry_gas_infeasible": aramid_dry_infeasible,
            "supply_R30": {"projection_faces_t": k_face30 / 1000, "projection_fibre_t": k_fib30 / 1000,
                           "pitch_capacity_t": pitch, "beryllium_faces_t": be_face30 / 1000, "be_world_t": be_world,
                           "albemet_beryllium_t": alb_be30 / 1000},
            "easier_to_ground": "beryllium's optimisms (two, smaller, sourced face); the CFRP's case is supply"},
        "rows_folded": [brief(r) for r in FD["rows"]],
        "rows_040_coating": OLD_ROWS,
        "E_multiplier_to_float": {"folded": FD["E_multiplier_to_float"], "040_coating": SE["E_multiplier_to_float"]},
        "edge_vs_cure": {"folded": FD["edge_vs_cure"], "040_coating": SE["edge_vs_cure"]},
        "thermal_factors": FD["thermal_factors"], "thermal_factors_own_geometry": own,
        "dry_gas_pressure_at_primary_geometry": dry, "checks": {"040": C["checks"], "048": FD["checks_048"],
                                                                "CHECK-040": FD["checks_040"],
                                                                "thermal_tables_max_abs_K": FD["thermal_table_checks_max_abs_K"],
                                                                "finish_screen_Be": FD["thermal_screen_check_Be_MLCCAg"]},
        "finishes": fins, "water_fractions": wf, "k60": k60, "constructions": FD["constructions"],
        "endpoint_bills_040_coating": EX["endpoint_bills"]}
    with open(os.path.join(HERE, "RESULTS.json.tmp"), "w") as fh:
        json.dump(results, fh, indent=1, default=float)
    os.replace(os.path.join(HERE, "RESULTS.json.tmp"), os.path.join(HERE, "RESULTS.json"))

    # ------------------------------------------------------------------ NFI.json
    items = [
        ("NFI-049-K13-VF", "PROJECTION", "The floating case rests on K13D2U at a 60% fibre fraction: E1 585 GPa by "
         "Toray's M55J lamina/fibre ratio, against Tuttle's measured 410 GPa at an unstated fraction (one specimen).",
         "A measured K13D2U lamina and quasi-isotropic laminate modulus at 55-60% Vf."),
        ("NFI-049-K13-XC", "QUESTIONABLE", "No K13D2U compression strength was found. The 220 MPa quasi-isotropic figure "
         f"is 014b's inherited value; the floating least set needs {min(fc60):.0f}-{max(fc60):.0f} MPa in equal-biaxial "
         "compression.", "Uniaxial and biaxial compression tests on quasi-isotropic K13D2U laminates at face gauge."),
        ("NFI-049-BIAXIAL", "PROJECTION", "CFRP's full compression is uniaxial/(1-nu), the equal-biaxial reading of a "
         "fibre-strain limit; transverse and shear ply failure, microbuckling and thin-ply effects are not modelled.",
         "Biaxial compression of a curved quasi-isotropic panel."),
        ("NFI-049-COLD-CURE", "QUESTIONABLE", "CFRP on 5056 passes 037b's free-edge screen only for a bond stress-free at "
         f"or below 50 C ({e200['edge_SF']:.2f} at 200 F under the multilayer finish). No source gives honeycomb bond data "
         "for such cures, and the free-edge model is 037b's derivation.",
         "A cold-curing film or paste on 5056 honeycomb with CFRP skins: flatwise, climbing drum and residual strain."),
        ("NFI-049-FINISH", "PROJECTION", "The multilayer CCAg/ITO optics are a class-level NASA transfer, unqualified on "
         "beryllium (048) and on CFRP, where deposition, adhesion over a -0.4 ppm/K laminate and matrix outgassing are "
         f"open. On the 60% Vf face, 048's full-cycle screen reads {t60['legacy_037_full_cycle_SF']:.3f} at 037's source "
         f"geometry (fails) and {min(ownf(K60, R)['full_cycle_SF'] for R in R3):.2f} at its own geometry.",
         "Measured optics, adhesion and thermal cycling of the finish on the chosen face."),
        ("NFI-049-WATER-UPTAKE", "PROJECTION", "Material water uses transferred uptakes. The CFRP face uses 0.18%, a "
         "pitch/cyanate laminate at 55% RH; other sources give 0.04-0.70% for cyanate and about 0.9% for epoxy. The aramid "
         "cores use 95% RH, 120 h pickups (4.4% and 3.4%); the CFRP seam film uses FM-300's 1.67% hot-wet estimate. The "
         "bake's 90% removal is 048's acceptance target, and DuPont says Nomex needs at least 100 C to dry fully against "
         "048's 70 C bake.", "Weighed uptake and bake-out of the chosen face, core and films."),
        ("NFI-049-ONE-MM", "QUESTIONABLE", "With CHECK-040's 1 mm of exterior water only R 30 floats: beryllium on gamma, "
         "Q and film, the 60% Vf projection on gamma, Q and the face tuple.",
         "A measured retained-water film for the hull's finish and attitude."),
        ("NFI-049-CHK040-MODELS", "QUESTIONABLE", "Cure compression in the global and crimp demand and edge/scarf "
         "coincidence are carried as rows. CHECK-040's rigid-face transfer alternatives, which remove every beryllium "
         "float, were not rerun for the beryllium-free faces.", "Grounding of the compliant-core transfer (037b, CHECK-037b)."),
        ("NFI-049-M55J-QI", "QUESTIONABLE", "M55J's quasi-isotropic modulus, compression and CTE are a vendor's calculated "
         "plate values; tested values are announced as coming.", "Tested M55J quasi-isotropic laminate properties."),
        ("NFI-049-ARAMID", "PROJECTION", "Aramid cores use their thickness-direction CTE in plane, a measured Nomex wall "
         "modulus with paper density and strength, a projected Kevlar fabric wall, and a minimum shear strength scaled "
         "from CR-III's ratio. They do not float because crimping binds, which none of these changes; without drying "
         "credit their water also breaks the service pressure.", "In-plane CTE and wall data for low-density aramid cores."),
        ("NFI-049-SEAM", "PROJECTION", "The CFRP seam is a co-cured scarf with 146 g/m2 FM 300-2M film over the scarf "
         "faces, a 17.3 MPa screen (co-cured lap shear, laminate failure) and 040's stock panel and ratio. Larger CFRP "
         "panels would reduce seam mass.", "A co-cured CFRP scarf on a curved panel, and the panel size a CFRP gore allows."),
        ("NFI-049-ALBEMET", "QUESTIONABLE", "AlBeMet's compressive yield is not printed; its tensile yield stands in. It is "
         "62 wt% beryllium and does not float.", "AlBeMet sheet compression data."),
        ("NFI-049-SUPPLY", "QUESTIONABLE", "No K13D2U or M55J tonnage or price was found; the pitch-fibre share uses the "
         "three-producer capacity of 1,400 t/yr.", "Producer capacity for K13D2U and M55J."),
        ("NFI-049-BE-GAUGE", "QUESTIONABLE", f"Beryllium's least-point faces are {gb[0]:.2f} / {gb[1]:.2f} / {gb[2]:.2f} mm "
         "at R 15 / 20 / 30. SR-200's full 609.6 x 1828.8 mm stock is listed from 1.50 mm (020); thinner stock comes in "
         "smaller, unspecified sizes, which 040's joining does not charge.", "A supplier gauge map for SR-200 below 1.5 mm."),
        ("NFI-049-DENSITY-CTE", "PROJECTION", "Laminate densities use a 1.2 g/cm3 resin; K13D2U's quasi-isotropic CTE is "
         "taken as M55J's calculated value.", "Measured laminate densities and CTEs."),
        ("NFI-049-THERMAL", "PROJECTION", "Aramid-core conductivity in vacuum is the wall's conductivity times solidity.",
         "A vacuum conductance measurement of the core."),
        ("NFI-049-HM-DAMAGE", "QUESTIONABLE", "High-modulus pitch laminates are brittle (fibre strain under 0.4%); 045's "
         "damage-tolerance findings apply and are not rescored here.",
         "Impact and compression-after-impact tests on K13D2U/5056 sandwich."),
    ]
    nfi = {"schema": 1, "card": "MAINLINE-049", "unit": "vacuum-mainline049-be-free-p2-1020", "tag": "QUESTIONABLE",
           "status": "OPEN", "items": [{"id": i, "tag": tg, "claim": cl, "needed_to_ground": nd} for i, tg, cl, nd in items]}
    with open(os.path.join(HERE, "NFI.json.tmp"), "w") as fh:
        json.dump(nfi, fh, indent=1)
    os.replace(os.path.join(HERE, "NFI.json.tmp"), os.path.join(HERE, "NFI.json"))

    # ------------------------------------------------------------------ INPUTS.json
    def pin(path, role):
        data = open(path, "rb").read()
        return {"path": path, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data), "role": role}
    pins = [dict(v, role="input read; " + k) for k, v in FD["pins"].items()]
    for name in ("sens49.py", "card49.py", "simretry.sh", "COMPUTE.json", "SENS.json", "EXTRA.json", "FOLD.json"):
        pins.append(pin(os.path.join(HERE, name), "this card's own code or intermediate"))
    inputs = {"schema": 1, "card": "MAINLINE-049", "unit": "vacuum-mainline049-be-free-p2-1020", "orders": ORDERS,
              "pins": pins, "common_amendment": FD["common_amendment"],
              "sources_used": C["sources_used"] | EX["sources_used"] | FD["sources_used"],
              "reports_used": ["rpt-ref-b10363665c6202d8ef75",
                               "rpt-ref-2092a3e39c7141afde61", "rpt-ref-593068c3ed82fd458128",
                               "rpt-ref-3e02218a03708a878faa",
                               "rpt-mainline014b-grok-metal-honeycomb-1019", "rpt-mainline014-grok-balanced-sandwich-1019",
                               "rpt-ref-d6eac96dde8db1968e86"]}
    with open(os.path.join(HERE, "INPUTS.json.tmp"), "w") as fh:
        json.dump(inputs, fh, indent=1)
    os.replace(os.path.join(HERE, "INPUTS.json.tmp"), os.path.join(HERE, "INPUTS.json"))
    print(len(text), "bytes card;", len(items), "NFI;", len(pins), "pins")


if __name__ == "__main__":
    main()
