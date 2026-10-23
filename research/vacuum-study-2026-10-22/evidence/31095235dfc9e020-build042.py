#!/usr/bin/env python3
"""MAINLINE-042: the P2 build route. Shape the build can hold against the shape gamma and Q need.

Own arithmetic, seat ref-55cff924be25afe6f9dd. The P2 point is 028b's nominal AF/scarf point. The gamma map is
015b's live map (Baizhikova 2026 Eq. 3 and Lee 2016 Eq. 23 on t_eq = sqrt3 (core + tf), nu 0.33, lambda_I = 1), re-implemented
here and checked against 015b's published rows. The Q map is 032's CR-1457 Eq. 2.2-12, checked against 032's rows. Route
numbers (forming strain, seam thermal stress, gauge, self-weight, evacuation) are this card's own estimates. Precedent
accuracies enter from LIT-*.json only after this seat verified them at source (PRECEDENTS below). All QUESTIONABLE.
"""
import datetime
import json
import math
import time
from pathlib import Path

T_START = datetime.datetime.now().astimezone().isoformat()
T0C = time.monotonic()
OUT = Path(__file__).resolve().parents[1] / "outputs" / "vacuum-mainline042-build-route-1020"

R, P, L0 = 10.0, 95460.83791390515, 4889.442150186961
A = 4 * math.pi * R ** 2
P028B = {"tf": 0.0007946240669858892, "tc": 0.02323721790601576, "gamma": 0.564164, "Q": 0.434628,
         "faces_kg": 3694.6499941886, "core_kg": 467.7511319586517, "joining_kg": 215.74207996805592,
         "seam_m": 2841.518543919854, "scarf_overlap_m": 0.023838722009576676, "nu_face": 0.0752}
BE = {"E": 290e9, "rho": 1850.0, "cte": 11.3e-6, "sig": 345e6}
CORE = {"Ec": 103421359.3975254, "rho": 16.018463373960138, "Fc60": 60 * 6894.757293168361, "Fc35": 35 * 6894.757293168361,
        "cte_al": 23.6e-6}
NU_MAP = 0.33                                        # 015b's live map convention
BLANK = (0.6096, 1.8288)                             # SR-200 maximum stock (020; 028b)
GAUGE_TOL = 0.1016e-3                                # SR-200 thickness tolerance near this gauge (020)


V, S = "verified at source by this seat", "sub-worker row (LIT-*.json), not re-read"
PRECEDENTS = [
    {"id": "S-II common bulkhead", "diameter_m": 10.06, "verified": V,
     "construction": "2014-T6 Al faces, chem-milled gores 13 mm to 0.79 mm; phenolic honeycomb tapering from about 5 in",
     "tooling": "gores explosively formed (3 blasts each); 12 gores + dollar welded; skins inflated at low pressure and "
                "measured at about 15,000 points; core machined to cutting tables in 0.010 in passes",
     "cure": "aft sheet + core cured in a 'gargantuan autoclave'; skins bonded in preload; ultrasonic checks",
     "shape": "core contour to match the face within 0.010 in (0.254 mm), the largest gap the adhesive bridges "
              "(specified); welding left localized distortion; as-built RMS/peak not published",
     "sources": "SD 71-256 (NTRS 19720008130) printed pp.4-44 to 4-45; NASA SP-4206 pp.213-214"},
    {"id": "S-IVB common bulkhead", "diameter_m": 6.63, "verified": V,
     "construction": "2014-T6 Al faces 0.813/1.4 mm on phenolic fibreglass honeycomb",
     "tooling": "350 putty-pad 'Paleno' blocks to read the fit, then the core sanded by hand",
     "cure": "final bond at 182 C (360 F) in an oversized autoclave; machined on a Niles boring mill",
     "shape": "fit read by putty pads, values unpublished; experimental bonded segments 0 to 0.090 in gap, welded 0 to "
              "0.015 in (Douglas Paper 3817, sub-worker row)",
     "sources": "NASA SP-4206 p.168 (read); Douglas Paper 3817 (sub-worker)"},
    {"id": "Rohr 57 in bonded bulkhead", "diameter_m": 1.448, "verified": V,
     "construction": "2219 Al skins on 1 in HRP honeycomb", "tooling": "stretch-formed, welded gores",
     "cure": "autoclave 350 F, about 200 psi, creep-sizing the skins in the bond cycle (sub-worker detail)",
     "shape": "gores about 0.050 in out of contour after forming; 0.150-0.200 in after chemical milling; extensive hand "
              "forming", "sources": "NTRS 19660014454"},
    {"id": "CCTD 5.5 m composite tank", "diameter_m": 5.5, "verified": V, "construction": "IM7/5320-1 laminate (not sandwich)",
     "tooling": "-", "cure": "out of autoclave: 'no autoclave large enough to cure a 10m cryotank'", "shape": "-",
     "sources": "NTRS 20150021410"},
    {"id": "Ares I common bulkhead", "diameter_m": 5.49, "verified": S,
     "construction": "1.78 mm Al skins on 50.8 mm perforated phenolic honeycomb", "tooling": "robotic FSW tool",
     "cure": "not stated", "shape": "dome-to-ring weld mismatch max 0.041 in", "sources": "NTRS 20120014602, 20100017376"},
    {"id": "Atlas V 5.4 m fairing", "diameter_m": 5.4, "verified": S,
     "construction": "carbon prepreg faces on vented Al honeycomb bent to radius", "tooling": "54 t mould",
     "cure": "out-of-autoclave oven under vacuum bag", "shape": "not published", "sources": "CompositesWorld RUAG tour"},
    {"id": "X-33 LH2 tank", "diameter_m": None, "verified": S,
     "construction": "IM7/977-2 on Korex honeycomb, AF-191", "tooling": "lobes cured separately",
     "cure": "autoclave, 350 F; severe skin-core disbonds after cure; 1999 failure by microcracking and cryopumping",
     "shape": "not published", "sources": "NTRS 20200006023, 20020021989"},
    {"id": "CSO 10.4 m reflector", "diameter_m": 10.4, "verified": V,
     "construction": "1.0 mm Al skin pulled onto machined Al honeycomb, hexagonal panels about 1.15 m",
     "tooling": "honeycomb machined on a curved cutter track; panels pre-strained during cutting",
     "cure": "epoxy", "shape": "skin force bent each prototype panel about 150 um centre-to-edge until pre-strained; "
              "panels 5-10 um rms; dish just under 30 um rms (Serabyn 1991, sub-worker)",
     "sources": "Leighton NSF final report (read); Serabyn et al. 1991 Appl. Opt. 30, 1227"},
    {"id": "ALMA European 12 m antenna", "diameter_m": 12, "verified": V,
     "construction": "0.6 mm electroformed Ni skin on 20 mm Al honeycomb, 120 panels, 5 adjusters each (ESO/ESA, sub-worker)",
     "tooling": "replication from machined steel moulds", "cure": "bonded",
     "shape": "dish 38 um rms as set by the contractor's laser tracker; 55 um at first holography; about 14 um after a "
              "third partial adjustment; panel spec 8 um",
     "sources": "Mangum et al. 2006 PASP, Sect. 5.1.1 (read)"},
    {"id": "SMT/HHT 10 m", "diameter_m": 10, "verified": S, "construction": "CFRP faces on Al honeycomb, 60 panels",
     "tooling": "-", "cure": "-", "shape": "47 um first holography; 14-19 um after panel resets", "sources": "HHT 1997 holography page"},
    {"id": "LMT 50 m", "diameter_m": 50, "verified": S, "construction": "electroformed Ni panels on Al boxes",
     "tooling": "-", "cure": "-", "shape": "segments just below 20 um; overall 98 um rms", "sources": "Hughes et al. SPIE 11445 (2020)"},
    {"id": "IRAM 30 m", "diameter_m": 30, "verified": S, "construction": "Al panels (honeycomb per snippet)", "tooling": "-",
     "cure": "-", "shape": "about 50-60 um; panel errors correlated over 0.3-0.5 m", "sources": "Kramer et al. 2013 IRAM report"},
    {"id": "Sandwich ground radomes", "diameter_m": 23.5, "verified": S,
     "construction": "bolted doubly curved sandwich panels (foam or honeycomb)", "tooling": "-", "cure": "-",
     "shape": "no tolerance published; sizes to 23.5 m (CPI) and 20 m (Comtech)", "sources": "CPI and Comtech data sheets"},
    {"id": "SNO 12 m acrylic sphere", "diameter_m": 12, "verified": V,
     "construction": "122 bonded acrylic panels 5.6 cm", "tooling": "dry-assembled hemispheres on a framework",
     "cure": "room-temperature polymerising adhesive, bonds above 27.5 MPa (sub-worker)",
     "shape": "+/-25 mm specified; 'typically maintained to +/-6 mm'", "sources": "Boger et al. NIM A 449 (2000) p.181"},
    {"id": "Moss LNG sphere, JUNO, JT-60SA lid", "diameter_m": 36.6, "verified": S,
     "construction": "welded Al (Moss), bonded acrylic (JUNO), welded steel (JT-60SA)", "tooling": "jigs",
     "cure": "-", "shape": "Moss under 2 cm; JUNO +/-50 mm (panels within 6 mm); JT-60SA R 8 m +/-8 mm",
     "sources": "Faig ISPRS 1980; JUNO arXiv 2311.17314; JT-60SA poster"},
    {"id": "Solar creep-formed Be honeycomb panel", "diameter_m": None, "verified": V,
     "construction": "brazed all-Be honeycomb, 1 x 2 ft", "tooling": "vacuum-bagged die, 10 ft radius (cylindrical)",
     "cure": "creep formed at 1250 F", "shape": "'conformed to the die within 0.003 inch at room temperature'",
     "sources": "Vogan and Grant, Solar RDR 1550-12 (NTRS 19730016169) Sect. 6.3"},
]
INSPECTION = [
    {"target": "face-core bond", "method": "tap test (manual / automated)", "resolution": "a90/95 43 / 28 mm, 0.5 mm Al skins "
     "on 19 mm Al honeycomb, laboratory (automated better by 15 mm)", "verified": V, "source": "Genest et al. ICAF 2023"},
    {"target": "face-core bond", "method": "vacuum-stress shearography", "resolution": "POD 0.95 at debond diameter equal to "
     "foam thickness (Shuttle SOFI); 0.375 in voids; vendor 15 m2/h hood; ASTM E2581 names metal-faced honeycomb, no size",
     "verified": S, "source": "NTRS 19960028755/19960029100; Dantec"},
    {"target": "face-core bond", "method": "pulse-echo / through-transmission UT", "resolution": "6.35 mm inserts in thin "
     "CFRP; ASTM E2580 flat parallel panels only", "verified": S, "source": "NLR; ASTM E2580-24"},
    {"target": "face-core bond", "method": "flash thermography", "resolution": "E2582 excludes core and far-side bond; "
     "signal lost at face/core-wall ratio 8:1 (CFRP model)", "verified": S, "source": "NTRS 20150001252; ASTM E2582"},
    {"target": "weak or kissing bond", "method": "commercial NDE", "resolution": "fails on weak or kissing bonds", "verified": S,
     "source": "NTRS 20230010345"},
    {"target": "scarf seams", "method": "none found", "resolution": "no scarf-seam NDE source; shearography needs two shear "
     "directions on strip debonds", "verified": S, "source": "LIT-C GAPS"},
    {"target": "global shape", "method": "laser tracker AT960", "resolution": "scale-bar MPE 0.106 mm at 10 m, 0.191 mm at 20 m",
     "verified": V, "source": "Leica AT960 ASME B89.4.19 sheet"},
    {"target": "global shape", "method": "photogrammetry (V-STARS)", "resolution": "0.043-0.091 mm rms on a 13.2 m tool; "
     "1:100,000-1:200,000 claimed", "verified": S, "source": "GSI acceptance test 1997"},
    {"target": "global shape", "method": "terrestrial laser scanner RTC360", "resolution": "1.9 mm at 10 m, 2.9 mm at 20 m",
     "verified": S, "source": "Leica RTC360 sheet"},
    {"target": "waviness", "method": "structured light + photogrammetry; laser line profiler", "resolution": "0.001 in on "
     "8 ft cylinder OML (NASA SBKF); profiler Z repeatability 0.4 um", "verified": S, "source": "NTRS 20180006177; Keyence"},
    {"target": "under load", "method": "stereo DIC; distributed fibre-optic strain", "resolution": "0.003 in (3 sigma) on 8 ft "
     "shells, six systems on 27.5 ft cylinders; 0.65 mm gage pitch, +/-5 microstrain", "verified": S,
     "source": "NTRS 20180006177, 20180006174; Luna ODiSI 6000"},
]


def teq(tf, tc):
    return math.sqrt(3) * (tc + tf)


def beta0(t):
    return math.sqrt(t / R) / (12 * (1 - NU_MAP ** 2)) ** 0.25


def eq3_kd(d_over_t):
    return 0.45 + 0.51 * math.exp(-3.88 * d_over_t)


def eq3_inv(kd):
    return None if kd <= 0.45 else -math.log((kd - 0.45) / 0.51) / 3.88


def lee_kd(d_over_t):
    return 0.068 + 0.25 / (0.28 + d_over_t)


def lee_inv(kd):
    return 0.25 / (kd - 0.068) - 0.28


def dimple(tf, tc, kd):
    """015b map at one shell: matched amplitude (Eq. 3) and Lee amplitude, mm, with single-dimple RMS (k = 1), mm."""
    t = teq(tf, tc)
    b = beta0(t)
    e3 = eq3_inv(kd)
    le = lee_inv(kd)
    return {"t_eq_mm": t * 1e3, "R_over_t": R / t, "width_m": R * b,
            "eq3_amp_mm": e3 * t * 1e3 if e3 is not None else None,
            "eq3_rms_mm": e3 * t * b / math.sqrt(8) * 1e3 if e3 is not None else None,
            "eq3_d_over_t": e3, "eq3_in_fit": (e3 is not None and e3 >= 0.07),
            "lee_amp_mm": le * t * 1e3, "lee_rms_k1_mm": le * t * b / math.sqrt(8) * 1e3,
            "lee_rms_k5_mm": 5 * le * t * b / math.sqrt(8) * 1e3, "lee_d_over_t": le,
            "lee_in_fem_range": le >= 0.15, "lee_in_ode_range": le >= 0.2}


def gamma_for_amplitude(tf, tc, amp_m):
    t = teq(tf, tc)
    x = amp_m / t
    return {"amp_mm": amp_m * 1e3, "d_over_t": x, "eq3_kd": eq3_kd(x), "eq3_in_fit": x >= 0.07, "lee_kd": lee_kd(x),
            "lee_in_fem_range": x >= 0.15}


def waviness_for_Q(Q, tc, Fc):
    K = (0.82 / Q - 1) / 0.64
    return K * tc * Fc / CORE["Ec"]


def Q_for_waviness(d, tc, Fc):
    return 0.82 / (1 + 0.64 * d * CORE["Ec"] / (tc * Fc))


def main():
    res = {"schema": 1, "card": "MAINLINE-042", "unit": "vacuum-mainline042-build-route-1020", "tag": "QUESTIONABLE",
           "certification": False, "started_local": T_START,
           "measured_times": {"job_started_local": "2026-10-20T03:09:06-07:00 (WORKING state line)",
                              "this_run_local": T_START}}
    # 1. reproduce 015b's published rows (live map)
    chk = {}
    be = dimple(0.000693223, 0.041550, 0.9)
    chk["015b_Be_kd0.9"] = {"mine": [be["eq3_amp_mm"], be["eq3_rms_mm"], be["lee_amp_mm"], be["lee_rms_k1_mm"]],
                            "filed": [2.360, 0.0395, 1.499, 0.0251]}
    d021 = dimple(0.000843448, 0.020213, 0.5953179642995181)
    chk["015b_021"] = {"mine": [d021["t_eq_mm"], d021["eq3_amp_mm"], d021["eq3_rms_mm"], d021["lee_amp_mm"]],
                       "filed": [36.47, 11.801, 0.1393, 7.079]}
    d021b = dimple(0.000691748, 0.030118, 0.46822856667720764)
    chk["015b_021b"] = {"mine": [d021b["t_eq_mm"], d021b["eq3_amp_mm"], d021b["eq3_rms_mm"], d021b["lee_amp_mm"]],
                        "filed": [53.36, 45.819, 0.6544, 18.392]}
    # 032's rows (60 psi): S-200F on 20.21 mm core at Q 0.371; SR-200 on 30.12 mm at Q 0.609
    chk["032_S200F"] = {"mine": waviness_for_Q(0.371, 0.020213, CORE["Fc60"]) * 1e3, "filed": 0.152868766846}
    chk["032_SR200"] = {"mine": waviness_for_Q(0.609, 0.030118, CORE["Fc60"]) * 1e3, "filed": 0.0652229064039}
    res["reproduce"] = chk
    # 2. the P2 point (028b)
    tf, tc = P028B["tf"], P028B["tc"]
    need = dimple(tf, tc, P028B["gamma"])
    res["gamma_need_028b"] = need
    res["gamma_table"] = {f"{kd}": dimple(tf, tc, kd) for kd in (0.2, 0.3, 0.4, 0.468, 0.5, 0.564164, 0.6, 0.7, 0.8, 0.9)}
    res["amplitude_table"] = [gamma_for_amplitude(tf, tc, a * 1e-3) for a in
                              (0.5, 1, 2, 3, 5, 7.5, 9.32, 10, 12.5, 16.06, 20, 25, 30, 40, 50, 75, 100)]
    res["Q_need_028b"] = {"waviness_mm_60psi": waviness_for_Q(P028B["Q"], tc, CORE["Fc60"]) * 1e3,
                          "waviness_mm_35psi": waviness_for_Q(P028B["Q"], tc, CORE["Fc35"]) * 1e3}
    res["Q_table"] = [{"waviness_mm": d * 1e3, "Q_60psi": Q_for_waviness(d, tc, CORE["Fc60"]),
                       "Q_35psi": Q_for_waviness(d, tc, CORE["Fc35"])}
                      for d in (0.005e-3, 0.01e-3, 0.02e-3, 0.024e-3, 0.034e-3, 0.05e-3, 0.075e-3, 0.1e-3, 0.129e-3,
                                0.15e-3, 0.2e-3, 0.2032e-3, 0.287e-3, 0.3e-3, 0.5e-3)]
    # 3. route numbers
    a, b = BLANK
    o = P028B["scarf_overlap_m"]
    per_skin = A / ((a - o) * (b - o))
    eps_m = P * R / 2 * (1 - P028B["nu_face"]) / (2 * BE["E"] * tf)          # membrane strain at the 028b point
    route = {
        "blanks_per_skin": per_skin, "blanks_total": 2 * per_skin, "coincident_seam_m": P028B["seam_m"],
        "flat_blank_corner_sag_mm": (a ** 2 + b ** 2) / 4 / (2 * R) * 1e3,
        # forming: a strip of width w on a sphere: edge fibres follow small circles, strain spread w^2/(8 R^2);
        # a disc of radius r forced flat-to-sphere (plane stress): rim hoop strain r^2/(8 R^2) (Foppl-type estimate)
        "forming_strain_strip_w": (a ** 2) / (8 * R ** 2), "forming_strain_disc_halfdiag": ((a ** 2 + b ** 2) / 4) / (8 * R ** 2),
        "forming_strain_small_blank_0.305x0.610": ((0.3048 ** 2 + 0.6096 ** 2) / 4) / (8 * R ** 2),
        "Be_elastic_strain_at_345MPa": BE["sig"] / BE["E"],
        "forming_stress_strip_MPa": BE["E"] * (a ** 2) / (8 * R ** 2) / 2 / 1e6,
        "face_bending_strain_flat_to_R": tf / (2 * R), "face_bending_stress_MPa": BE["E"] * tf / (2 * R) / 1e6,
        # a seam strip heated in situ while the shell stays cold
        "seam_hot_cure_stress_MPa_per_100K": BE["E"] * BE["cte"] * 100 / (1 - P028B["nu_face"]) / 1e6,
        "Be_Al_core_cte_mismatch_strain_per_100K": (CORE["cte_al"] - BE["cte"]) * 100,
        "membrane_strain": eps_m,
        "gauge_tol_fraction": GAUGE_TOL / tf,
        "gauge_low_patch_radial_mm_upper": eps_m * GAUGE_TOL / tf * R * 1e3,
        "areal_mass_kg_m2": (P028B["faces_kg"] + P028B["core_kg"] + P028B["joining_kg"]) / A,
        "self_weight_Pa": (P028B["faces_kg"] + P028B["core_kg"] + P028B["joining_kg"]) / A * 9.80665,
        "sea_level_overload": 101325.0 / P - 1,
    }
    D_s = BE["E"] * tf * (tc + tf) ** 2 / (2 * (1 - P028B["nu_face"] ** 2))
    q = route["self_weight_Pa"]
    # S-II-style inflation of a closed 0.8 mm Be skin at 1/2 psi: membrane stress, tension against bending at the dimple scale
    p_infl = 0.5 * 6894.757293168361
    D_face = BE["E"] * tf ** 3 / (12 * (1 - P028B["nu_face"] ** 2))
    k_dimple = 1 / need["width_m"]
    route["inflation"] = {"p_Pa": p_infl, "skin_stress_MPa": p_infl * R / (2 * tf) / 1e6, "tension_N_per_m": p_infl * R / 2,
                          "face_bending_D_Nm": D_face, "bending_term_D_k2_N_per_m": D_face * k_dimple ** 2,
                          "tension_over_bending": (p_infl * R / 2) / (D_face * k_dimple ** 2)}
    route["D_sandwich_Nm"] = D_s
    route["self_weight_span_deflection_mm"] = {f"{L} m": 5 * q * L ** 4 / (384 * D_s) * 1e3 for L in (1, 2, 3, 5)}
    res["route"] = route
    # 4. precedent shape classes through the same maps (values verified at source by this seat; see CARD)
    dimple_cases = {"Rohr 57 in gores after stretch forming (0.050 in)": 0.050 * 25.4e-3,
                    "Rohr gores after chemical milling (0.150 in)": 0.150 * 25.4e-3,
                    "Rohr gores after chemical milling (0.200 in)": 0.200 * 25.4e-3,
                    "S-II core-to-face fit limit (0.010 in)": 0.010 * 25.4e-3,
                    "gauge-low patch under load (upper, this card)": route["gauge_low_patch_radial_mm_upper"] * 1e-3,
                    "reflector class, 3 x 50 um whole-surface rms": 0.15e-3}
    res["precedent_dimples"] = {k: gamma_for_amplitude(tf, tc, v) for k, v in dimple_cases.items()}
    wav_cases = {"CSO panel 10 um rms (x sqrt2)": 10e-6 * math.sqrt(2),
                 "Woody 1994 installed 24 um rms (x sqrt2; 032b)": 24e-6 * math.sqrt(2),
                 "Nobeyama new-antenna panels 21 um rms (x sqrt2)": 21e-6 * math.sqrt(2),
                 "Nobeyama older panels 60 um rms (x sqrt2)": 60e-6 * math.sqrt(2),
                 "von Hoerner vendor honeycomb 0.2032 mm rms (x sqrt2; 032b)": 0.2032e-3 * math.sqrt(2),
                 "ER-1001 cell dimple depth 0.001651 mm (032b)": 0.001651e-3,
                 "3/8 in cell one-cell rise projection 0.01524 mm (032b)": 0.01524e-3}
    res["precedent_waviness"] = {k: {"amp_mm": v * 1e3, "Q_60psi": Q_for_waviness(v, tc, CORE["Fc60"]),
                                     "Q_35psi": Q_for_waviness(v, tc, CORE["Fc35"])} for k, v in wav_cases.items()}
    # 5. face-core disbond that buckles as a circular plate at the 028b face stress (inner face: vented core, no
    #    pressure holding it); equal biaxial compression, clamped lambda 14.682, simply supported 4.198
    sig = P * R / 2 / (2 * tf)
    Df = BE["E"] * tf ** 3 / (12 * (1 - P028B["nu_face"] ** 2))
    res["disbond_critical_diameter_mm"] = {"face_stress_MPa": sig / 1e6,
                                           "clamped": 2 * math.sqrt(14.682 * Df / (sig * tf)) * 1e3,
                                           "simply_supported": 2 * math.sqrt(4.198 * Df / (sig * tf)) * 1e3}
    # 6. cure envelope and coverage arithmetic
    res["envelope"] = {"sphere_volume_m3": 4 / 3 * math.pi * R ** 3, "largest_autoclave_volume_m3_ASC": 2321.0,
                       "largest_autoclave_diameter_m_Spirit": 30 * 0.3048, "panel_envelope_m": [BLANK[0] + 0.1, BLANK[1] + 0.1],
                       "cure_dT_K_AF163_250F_to_service": (250 - 32) / 1.8 + 273.15 - 284.9,
                       "cure_dT_K_AF163_200F_to_service": (200 - 32) / 1.8 + 273.15 - 284.9,
                       "Be_Al_mismatch_strain_250F": (CORE["cte_al"] - BE["cte"]) * ((250 - 32) / 1.8 + 273.15 - 284.9),
                       "Be_Al_mismatch_strain_200F": (CORE["cte_al"] - BE["cte"]) * ((200 - 32) / 1.8 + 273.15 - 284.9),
                       "film_mass_per_10gm2_both_lines_kg": 2 * A * 0.010}
    res["coverage"] = {"bond_area_m2_two_lines": 2 * A, "scarf_seam_m_two_skins": 2 * P028B["seam_m"],
                       "shearography_hours_at_15m2h_vendor": 2 * A / 15.0,
                       "photogrammetry_relative_1_to_100k_at_20m_mm": 20.0 / 1e5 * 1e3,
                       "photogrammetry_relative_1_to_200k_at_20m_mm": 20.0 / 2e5 * 1e3}
    # 7. precedent and inspection rows carried into RESULTS (verified = read at source by this seat)
    res["precedents"] = PRECEDENTS
    res["inspection"] = INSPECTION
    res["ended_local"] = datetime.datetime.now().astimezone().isoformat()
    res["elapsed_s"] = time.monotonic() - T0C
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "RESULTS.json").write_text(json.dumps(res, indent=1))
    for k, v in chk.items():
        print(k, v)
    print("need at 028b:", {k: (round(v, 4) if isinstance(v, float) else v) for k, v in need.items()})
    print("Q need:", res["Q_need_028b"])
    for r in res["amplitude_table"]:
        print(f"  amp {r['amp_mm']:7.2f} mm  d/t {r['d_over_t']:.4f}  Eq3 {r['eq3_kd']:.4f} (fit {r['eq3_in_fit']})  "
              f"Lee {r['lee_kd']:.4f} (FEM {r['lee_in_fem_range']})")
    for r in res["Q_table"]:
        print(f"  wav {r['waviness_mm']:.4f} mm  Q60 {r['Q_60psi']:.4f}  Q35 {r['Q_35psi']:.4f}")
    print({k: (round(v, 6) if isinstance(v, float) else v) for k, v in route.items()})


if __name__ == "__main__":
    main()
