#!/usr/bin/env python3
"""R3-I031 - mechanically captured tapered-pot socket cartridge (frozen construction).

Standard library only; one process, one thread. Reads baseline.json (frozen inputs
and frozen rules, sha-pinned by sources.json) and writes cartridge.json. The
construction, every material record and every screen formula were frozen BEFORE the
first execution; a FAIL below is a physical result, not a defect, and nothing is
tuned after it.
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(HERE, "baseline.json")) as f:
    B = json.load(f)

INH = B["inherited"]
FAMS = INH["families"]
MAT = INH["materialLedger"]
CON = INH["constants"]
ACC = B["i028Accepted"]
GEO = B["i031Rules"]["geometry"]
HW = B["i031Rules"]["hardware"]
LOADS = B["i031Rules"]["loads"]
COMP = B["i031Rules"]["compliance"]

ALPHA_DEG = GEO["coneHalfAngleDeg"]
ALPHA = math.radians(ALPHA_DEG)
TAN = math.tan(ALPHA)
SIN = math.sin(ALPHA)
COS = math.cos(ALPHA)

E_TI = MAT["terminationMetal"]["EPa"]
RHO_TI = MAT["terminationMetal"]["rhoKgM3"]
SIG_Y_TI = MAT["terminationMetal"]["sigmaYPa"]
E_AL = MAT["alBody"]["EPa"]
RHO_AL = MAT["alBody"]["rhoKgM3"]
SIG_W_AL = MAT["alBody"]["sigmaWPa"]
E_RES = LOADS["E_resinPa"]
RHO_RES = MAT["potResin"]["rhoKgM3"]
TAU_RES = MAT["potResin"]["designShearPa"]
P_RES = LOADS["resinDesignBearingPa"]
E_CORD = MAT["cord"]["EPa"]

FITTING = CON["FITTING"]
ASSM = HW["assemblyShareOnIncrement"]
MACH = HW["machiningFraction"]
AREAS = HW["tensileAreasMm2"]


def frustum_volume(l, ri1, ri2, ro1, ro2):
    """Exact integral of pi(ro^2-ri^2)dz with both radii linear in z."""
    return math.pi * l * ((ro1 * ro1 + ro1 * ro2 + ro2 * ro2)
                          - (ri1 * ri1 + ri1 * ri2 + ri2 * ri2)) / 3.0


def hex_part(af_mm, h_mm, hole_dia_mm):
    """Hex prismatic volume minus a round hole, mm^3."""
    return 0.8660254037844386 * af_mm * af_mm * h_mm \
        - math.pi / 4.0 * hole_dia_mm * hole_dia_mm * h_mm


def washer_vol(od_mm, id_mm, t_mm):
    return math.pi / 4.0 * (od_mm * od_mm - id_mm * id_mm) * t_mm


def family_calc(name, f):
    d_mm = {"d60": 14.0, "d180/11": 23.0}[name]
    d = d_mm / 1000.0
    bolt_nom_mm = {"d60": 6.0, "d180/11": 10.0}[name]
    bore_mm = f["boreMm"]
    grip_od_mm = f["bodyOdMm"]
    ends = f["ends"]
    r0 = bore_mm / 2.0
    rL = 1.25 * d_mm                      # chamber clear radius (2.5d dia)
    L_cone = (rL - r0) / TAN              # cone length until it daylights
    front_wall = (grip_od_mm - bore_mm) / 2.0
    x_hand = 3.0 * d_mm - 2.0 * front_wall  # cone dia where OD rule caps at 3d
    od_ch = 3.0 * d_mm
    od_fl = 4.0 * d_mm
    t_fl = 0.5 * d_mm
    t_cap = 0.5 * d_mm
    bc = 3.5 * d_mm
    L_ch = 2.0 * d_mm
    bolt_clear_mm = bolt_nom_mm + 0.6
    stud_clear_mm = d_mm + 0.6
    L_body = L_cone + L_ch + t_fl

    # --- body volume (Al), exact frustum segments, minus 4 bolt holes in flange
    z_hand = (x_hand - bore_mm) / (2.0 * TAN)   # axial station where cone dia = x_hand
    v_seg1 = frustum_volume(z_hand, bore_mm / 2.0, x_hand / 2.0,
                            grip_od_mm / 2.0, od_ch / 2.0)
    v_seg2 = frustum_volume(L_cone - z_hand, x_hand / 2.0, rL, od_ch / 2.0, od_ch / 2.0)
    v_chamber = math.pi / 4.0 * (od_ch ** 2 - (2.5 * d_mm) ** 2) * L_ch
    v_flange_gross = math.pi / 4.0 * (od_fl ** 2 - (2.5 * d_mm) ** 2) * t_fl
    v_holes = 4.0 * math.pi / 4.0 * bolt_clear_mm ** 2 * t_fl
    v_body = v_seg1 + v_seg2 + v_chamber + v_flange_gross - v_holes
    m_body = v_body * 1e-9 * RHO_AL

    # --- cap (Al): 4d x 0.5d minus 4 bolt clearance holes and stud clearance hole
    v_cap = (math.pi / 4.0 * (od_fl ** 2 - stud_clear_mm ** 2) * t_cap
             - 4.0 * math.pi / 4.0 * bolt_clear_mm ** 2 * t_cap)
    m_cap = v_cap * 1e-9 * RHO_AL

    # --- pot resin: cone frustum minus embedded cord cylinder over the cone length
    v_pot_gross = math.pi * L_cone * (r0 * r0 + r0 * rL + rL * rL) / 3.0
    v_cord_emb = math.pi / 4.0 * f["diaMm"] ** 2 * L_cone
    m_pot = (v_pot_gross - v_cord_emb) * 1e-9 * RHO_RES

    # --- cap bolt stack (Ti): hex head + shank; nuts; 2 washers per bolt
    af = 1.6 * bolt_nom_mm
    head_h = 0.65 * bolt_nom_mm
    nut_h = 0.8 * bolt_nom_mm
    L_bolt = t_fl + t_cap + nut_h + 0.4 * bolt_nom_mm
    v_bolt = hex_part(af, head_h, 0.0) + math.pi / 4.0 * bolt_nom_mm ** 2 * (L_bolt - head_h)
    v_bnut = hex_part(1.6 * bolt_nom_mm, nut_h, 0.85 * bolt_nom_mm)
    v_bwas = washer_vol(2.0 * bolt_nom_mm, 1.1 * bolt_nom_mm, 0.2 * bolt_nom_mm)
    m_bolts = 4.0 * (v_bolt + v_bnut + 2.0 * v_bwas) * 1e-9 * RHO_TI

    # --- interior load nut (Ti, 1.5d engagement) + bearing washer (Ti)
    v_iln = hex_part(1.6 * d_mm, 1.5 * d_mm, 0.85 * d_mm)
    v_bear = washer_vol(1.5 * d_mm, 1.1 * d_mm, 0.1 * d_mm)
    m_iln = (v_iln + v_bear) * 1e-9 * RHO_TI

    # --- stud: new overall length rule, mass prorated on the same blank
    ext_mm = {"d60": 3.0, "d180/11": 14.0}[name]  # inherited stud - inherited body length
    L_stud_new = 1.5 * d_mm + t_cap + ext_mm
    L_stud_old = {"d60": 79.0, "d180/11": 127.0}[name]
    m_stud_new = f["perEndKg"]["studKg"] * L_stud_new / L_stud_old

    # --- isolation stock
    m_iso_new = HW["newIsolationPerEndKg"][name]

    # --- before (accepted I028) per-end masses
    accp = ACC["perEnd"][name]
    m_albody_old = accp["alBodyKg"]
    m_mach_old = MACH * m_albody_old
    m_resin_old = accp["resinKg"]
    m_stud_old = accp["studKg"]

    m_mach_new = MACH * (m_body + m_cap)
    removed = m_albody_old + m_mach_old + m_resin_old + m_stud_old
    added = (m_body + m_cap + m_pot + m_bolts + m_iln + m_stud_new
             + m_iso_new + m_mach_new)
    inc_per_end = added - removed

    # --- loads and screens
    T0 = f["T0kN"] * 1000.0
    Tfit = f["TfitkN"] * 1000.0
    a_lat = math.pi * (r0 + rL) * math.hypot(L_cone, rL - r0)  # lateral frustum area, mm^2
    s_lat = math.hypot(L_cone, rL - r0)

    def cone_pressure(T):
        return (T / SIN) / (a_lat * 1e-6)  # Pa

    p_fit = cone_pressure(Tfit)
    p_0 = cone_pressure(T0)

    # hoop: along the cone p is uniform; r/t rises to the chamber entrance
    hoop_pts = []
    n_scan = 400
    for i in range(n_scan + 1):
        x = bore_mm + (2.5 * d_mm - bore_mm) * i / n_scan
        od = min(max(grip_od_mm, x + 2.0 * front_wall), od_ch)
        t = (od - x) / 2.0
        hoop_pts.append((x, cone_pressure(Tfit) * (x / 2.0) / t))
    hoop_max = max(hoop_pts, key=lambda pt: pt[1])
    hoop_chamber = cone_pressure(Tfit) * (1.25 * d_mm) / (0.25 * d_mm)  # exactly 5p

    # body axial stress at fitting demand
    Dden = (2.5 * d_mm) ** 2 - bore_mm ** 2

    def T_carried(x_mm, T):
        return T * (x_mm * x_mm - bore_mm * bore_mm) / Dden

    def A_wall(x_mm):
        od = min(max(grip_od_mm, x_mm + 2.0 * front_wall), od_ch)
        return math.pi / 4.0 * (od * od - x_mm * x_mm)  # mm^2

    ax_pts = [(T_carried(x, Tfit) / A_wall(x)) for x in
              (bore_mm + (2.5 * d_mm - bore_mm) * i / n_scan for i in range(n_scan + 1))]
    sig_ax_max = max(ax_pts) * 1e6  # N/mm^2 -> Pa

    # cap bending (radial-strip frozen screen)
    r_w = 0.75 * d_mm
    a_bc = 1.75 * d_mm
    M_cap_fit = Tfit * (a_bc - r_w) / (2.0 * math.pi * r_w)      # N*mm/mm
    sig_cap_fit = 6.0 * M_cap_fit / t_cap ** 2                    # N/mm^2
    M_cap_0 = T0 * (a_bc - r_w) / (2.0 * math.pi * r_w)
    sig_cap_0 = 6.0 * M_cap_0 / t_cap ** 2

    area_key = {"d60": "M14", "d180/11": "M23"}[name]
    bolt_area_key = {"d60": "M6", "d180/11": "M10"}[name]
    a_stud = AREAS[area_key] * 1e-6
    a_bolt = AREAS[bolt_area_key] * 1e-6
    sig_bolt = (Tfit / 4.0) / a_bolt
    sig_bolt_bear = (Tfit / 4.0) / (bolt_nom_mm * 1e-3 * t_fl * 1e-3)
    head_seat_area = math.pi / 4.0 * ((af + 0.4) ** 2 - bolt_clear_mm ** 2) * 1e-6
    sig_head_seat = (Tfit / 4.0) / head_seat_area
    sig_stud = Tfit / a_stud
    tau_strip = Tfit / (math.pi * 0.85 * d_mm * 1.5 * d_mm * 1e-6)
    washer_area = math.pi / 4.0 * ((1.5 * d_mm) ** 2 - stud_clear_mm ** 2) * 1e-6
    sig_washer = Tfit / washer_area
    tau_embed = Tfit / (math.pi * f["diaMm"] * 1e-3 * L_cone * 1e-3)

    screens = {
        "coneBearingResin": {"demandPa": p_fit, "limitPa": P_RES,
                             "utilisation": p_fit / P_RES, "verdict": "PASS" if p_fit <= P_RES else "FAIL"},
        "coneBearingAl": {"demandPa": p_fit, "limitPa": SIG_W_AL,
                          "utilisation": p_fit / SIG_W_AL, "verdict": "PASS" if p_fit <= SIG_W_AL else "FAIL"},
        "hoop": {"demandPa": hoop_max[1], "atConeDiaMm": hoop_max[0],
                 "atChamberEntrancePa": hoop_chamber, "limitPa": SIG_W_AL,
                 "utilisation": hoop_max[1] / SIG_W_AL,
                 "verdict": "PASS" if hoop_max[1] <= SIG_W_AL else "FAIL"},
        "bodyAxial": {"demandPa": sig_ax_max, "limitPa": SIG_W_AL,
                      "utilisation": sig_ax_max / SIG_W_AL,
                      "verdict": "PASS" if sig_ax_max <= SIG_W_AL else "FAIL"},
        "capBending": {"demandPa": sig_cap_fit * 1e6, "demandAtT0Pa": sig_cap_0 * 1e6,
                       "limitPa": SIG_W_AL,
                       "utilisation": sig_cap_fit * 1e6 / SIG_W_AL,
                       "verdict": "PASS" if sig_cap_fit * 1e6 <= SIG_W_AL else "FAIL"},
        "capBendingAtT0": {"demandPa": sig_cap_0 * 1e6, "limitPa": SIG_W_AL,
                           "utilisation": sig_cap_0 * 1e6 / SIG_W_AL,
                           "verdict": "PASS" if sig_cap_0 * 1e6 <= SIG_W_AL else "FAIL"},
        "boltTension": {"demandPa": sig_bolt, "limitPa": SIG_Y_TI,
                        "utilisation": sig_bolt / SIG_Y_TI,
                        "verdict": "PASS" if sig_bolt <= SIG_Y_TI else "FAIL"},
        "boltBearingAl": {"demandPa": sig_bolt_bear, "limitPa": SIG_W_AL,
                          "utilisation": sig_bolt_bear / SIG_W_AL,
                          "verdict": "PASS" if sig_bolt_bear <= SIG_W_AL else "FAIL"},
        "headSeatBearing": {"demandPa": sig_head_seat, "limitPa": SIG_W_AL,
                            "utilisation": sig_head_seat / SIG_W_AL,
                            "verdict": "PASS" if sig_head_seat <= SIG_W_AL else "FAIL"},
        "studTension": {"demandPa": sig_stud, "limitPa": SIG_Y_TI,
                        "utilisation": sig_stud / SIG_Y_TI,
                        "verdict": "PASS" if sig_stud <= SIG_Y_TI else "FAIL"},
        "loadNutStrip": {"demandPa": tau_strip, "limitPa": 0.6 * SIG_Y_TI,
                         "utilisation": tau_strip / (0.6 * SIG_Y_TI),
                         "verdict": "PASS" if tau_strip <= 0.6 * SIG_Y_TI else "FAIL"},
        "washerBearingCap": {"demandPa": sig_washer, "limitPa": SIG_W_AL,
                             "utilisation": sig_washer / SIG_W_AL,
                             "verdict": "PASS" if sig_washer <= SIG_W_AL else "FAIL"},
        "cordEmbedShear": {"demandPa": tau_embed, "limitPa": TAU_RES,
                           "utilisation": tau_embed / TAU_RES,
                           "verdict": "PASS" if tau_embed <= TAU_RES else "FAIL"},
    }
    unknowns = {
        "stationPitchEnvelope": "UNKNOWN - no station spacing in the record; body grows "
                                + "from {} to {} mm".format(f["bodyLenMm"], round(L_body, 1)),
        "adjustmentTakeUp": "UNKNOWN - retained adjustment travel not established",
        "contactSeating": "UNKNOWN - excluded from compliance",
        "potCreepUnderConfinement": "UNKNOWN - no confined creep data",
        "resinCrushBeyondAssumedLimit": "UNKNOWN beyond the ASSUMED 80 MPa record",
        "flangeRingBending": "bounded by the cap screen analogy; not separately solved",
    }

    # --- series compliance rebuild
    E_cA_c = E_CORD * f["sectionM2"]

    def antideriv_seg1(x, a, c):
        # d/dx = (x^2 - a^2)/(x + c), since (x+c)(x-c) + (c^2 - a^2) = x^2 - a^2
        return x * x / 2.0 - c * x + (c * c - a * a) * math.log(x + c)

    K = od_ch ** 2
    rk = od_ch

    def antideriv_seg2(x, a):
        return -x + (K - a * a) / (2.0 * rk) * math.log((rk + x) / (rk - x))

    xh = x_hand
    a2 = bore_mm
    AINT1 = antideriv_seg1(xh, a2, front_wall) - antideriv_seg1(bore_mm, a2, front_wall)
    AINT2 = antideriv_seg2(2.5 * d_mm, a2) - antideriv_seg2(xh, a2)
    # lengths in mm and areas in mm^2 against E in Pa: raw quotient carries m^2/mm
    # = 1e3 x m, hence the 1e3 factor below (verified against T*L/(E*A) directly)
    delta_seg1 = T0 * AINT1 / (E_AL * 2.0 * TAN * Dden * math.pi * front_wall) * 1e3
    delta_seg2 = T0 * AINT2 / (E_AL * 2.0 * TAN * Dden * math.pi / 4.0) * 1e3
    a_ch = math.pi / 4.0 * (od_ch ** 2 - (2.5 * d_mm) ** 2)
    a_fl = v_flange_gross / t_fl - v_holes / t_fl
    delta_ch_fl = T0 * (L_ch / (E_AL * a_ch) + t_fl / (E_AL * a_fl)) * 1e3
    delta_body = delta_seg1 + delta_seg2 + delta_ch_fl

    lC_body = delta_body * E_cA_c / T0
    r_m = (r0 + rL) / 2.0 / 1000.0
    a_lat_m2 = a_lat * 1e-6
    k_r = E_RES * a_lat_m2 * COS / r_m
    k_z = k_r * TAN * TAN
    delta_pot = T0 / k_z
    lC_pot = delta_pot * E_cA_c / T0

    a_bt = math.pi / 4.0 * (grip_od_mm ** 2 - bore_mm ** 2) * 1e-6
    ti_body_term = (f["bodyLenMm"] / 1000.0) * (E_CORD / E_TI) * f["sectionM2"] / a_bt
    eo_term = f["lSerM"] - ti_body_term
    stud_term = eo_term * L_stud_new / L_stud_old
    lser_new = lC_body + lC_pot + stud_term
    dl_ser = lser_new - f["lSerM"]
    l_eff_new = f["lEffM"] + 2.0 * dl_ser
    l_eff_mean_new = f["lEffMeanM"] + 2.0 * dl_ser
    ratio = l_eff_new / f["lEffM"]
    slack_new_declared = {k: v * ratio for k, v in f["slackN5DeclaredMm"].items()}
    slack_chord_historical = f["slackN5ChordBasisMm"]
    eta_new = f["meanCordM"] / l_eff_mean_new
    T_at_ext = T0 * f["lEffM"] / l_eff_new
    takeup_both_ends = T0 * 2.0 * dl_ser / E_cA_c

    compliance = {
        "lSerOldM": f["lSerM"], "lSerNewM": lser_new, "deltaLserM": dl_ser,
        "lCBodyM": lC_body, "lCPotWedgeM": lC_pot, "studTermM": stud_term,
        "tiBodyTermM": ti_body_term, "everythingElseTermM": eo_term,
        "potWedgeKzNPerM": k_z, "potDeltaAtT0M": delta_pot,
        "bodyDeltaAtT0M": delta_body,
        "lEffOldM": f["lEffM"], "lEffNewM": l_eff_new, "denominatorRatio": ratio,
        "etaOld": f["etaDrawnMeanCord"], "etaNew": eta_new,
        "T0AtUnchangedExtensionN": T_at_ext,
        "bothEndTakeupToRestoreT0M": takeup_both_ends,
        "n5FirstSlackDeclaredModelNewMm": slack_new_declared,
        "n5FirstSlackChordBasisMm": slack_chord_historical,
        "note": "chord-basis tables carried UNCHANGED as historical comparators; full n=2..12 class bounds, centroid/no-transfer sensitivity and global stability UNCOMPUTED/UNKNOWN; coupled eigen margin not recomputed (dependent UNKNOWN)",
    }

    geometry = {
        "d_mm": d_mm, "bore_mm": bore_mm, "grip_od_mm": grip_od_mm,
        "cone_length_mm": L_cone, "x_handover_mm": x_hand,
        "chamber_clear_dia_mm": 2.5 * d_mm, "chamber_od_mm": od_ch,
        "flange_od_mm": od_fl, "flange_thk_mm": t_fl, "cap_od_mm": od_fl,
        "cap_thk_mm": t_cap, "bolt_circle_mm": bc, "chamber_len_mm": L_ch,
        "body_total_len_mm": L_body, "old_body_len_mm": f["bodyLenMm"],
        "cone_lateral_area_mm2": a_lat, "cone_slant_mm": s_lat,
        "min_wall_over_grip_mm": front_wall,
        "wall_at_chamber_entrance_mm": 0.25 * d_mm,
    }

    bill_per_end = {
        "removed": {"alBodyI028": m_albody_old, "machiningOnOldBody": m_mach_old,
                    "oldStudBlank": m_stud_old, "oldResinPot": m_resin_old,
                    "total": removed},
        "new": {"conicalBody": m_body, "cap": m_cap, "potResin": m_pot,
                "capBoltStack": m_bolts, "interiorLoadNutAndWasher": m_iln,
                "newStudBlank": m_stud_new, "newIsolationSeal": m_iso_new,
                "machiningOnNewAl": m_mach_new, "total": added},
        "retained": {"cord": "retained once", "clips": "retained once",
                     "anchorBlocks": "retained once", "doublerPads": "retained once",
                     "attachmentBolts4550": "retained once",
                     "exteriorJamNut": accp["nutKg"],
                     "isolationProvision0025": ACC["isolationPerEndKg"]},
        "increment": inc_per_end,
        "ends": ends,
        "incrementFamilyKg": inc_per_end * ends,
    }

    return {
        "geometry": geometry,
        "perEndBill": bill_per_end,
        "screens": screens,
        "unknowns": unknowns,
        "compliance": compliance,
        "pressures": {"p_fit_Pa": p_fit, "p_T0_Pa": p_0,
                      "cone_normal_at_fit_N": Tfit / SIN},
    }


out = {"unit": "R3-I031", "basis": B["basis"], "families": {}}
inc_hardware_t = 0.0
for name in ("d60", "d180/11"):
    res = family_calc(name, FAMS[name])
    out["families"][name] = res
    inc_hardware_t += res["perEndBill"]["incrementFamilyKg"] / 1000.0

asm_share_t = ASSM * inc_hardware_t
inc_total_t = inc_hardware_t + asm_share_t
veh = ACC["vehicle"]
sockets_new = veh["socketsLineT"] + inc_hardware_t
subtotal_new = veh["subtotalT"] + inc_total_t
sl_new = veh["marginSLT"] - inc_total_t
m2500_new = veh["margin2500T"] - inc_total_t
x15_new = 0.5 * (sockets_new + INH["billTiEra"]["anchorBlocksT"]
                 + INH["billTiEra"]["doublerPadsT"]
                 + INH["billTiEra"]["attachmentBoltsT"]) * 1.05
stacked_sl = sl_new - x15_new

out["vehicle"] = {
    "before": veh,
    "incrementHardwareT": inc_hardware_t,
    "assemblyShareT": asm_share_t,
    "incrementTotalT": inc_total_t,
    "socketsLineT": sockets_new,
    "spokesLineT": veh["spokesLineT"],
    "subtotalT": subtotal_new,
    "marginSLT": sl_new,
    "margin2500T": m2500_new,
    "x15IncrementT": x15_new,
    "stackedX15SLT": stacked_sl,
    "sf12": "historical FAIL preserved; substitution into the separately sized d60+d20 construction UNCOMPUTED/UNKNOWN",
    "verdictSL": "PASS" if sl_new >= 0 else "FAIL",
    "verdict2500": "PASS" if m2500_new >= 0 else "FAIL",
}

out["verdict"] = {
    "overall": "FAIL" if (out["vehicle"]["verdictSL"] == "FAIL"
                          or any(s["verdict"] == "FAIL"
                                 for fam in out["families"].values()
                                 for s in fam["screens"].values()))
    else "conditional candidate",
    "note": "a heavier or inadequate construction is a valid same-day FAIL; the frozen construction is not enlarged after seeing this",
}

with open(os.path.join(HERE, "cartridge.json"), "w") as f:
    json.dump(out, f, indent=1, sort_keys=True)
    f.write("\n")
print("R3-I031 written: overall", out["verdict"]["overall"],
      "| increment %.3f t | SL %+.1f t | 2500m %+.1f t" % (inc_total_t, sl_new, m2500_new))
