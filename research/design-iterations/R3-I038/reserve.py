#!/usr/bin/env python3
# R3-I038 external freshwater reserve pair - finite stock/geometry calculator.
# Contract: python3 -I -B research/design-iterations/R3-I038/reserve.py --write
# Produces reserve.json next to this file. stdlib only. No qualification claims:
# every capacity/structural/energy figure is data or UNKNOWN; physical float NOT SHOWN.
import json, math, sys

RHO_5083, RHO_STEEL, RHO_POLY, RHO_WATER, G = 2660.0, 7850.0, 1200.0, 1000.0, 9.81
def ring_area(ro, ri, t):  # annular plate volume
    return math.pi * (ro * ro - ri * ri) * t
def tube_area(od, id_):
    return math.pi * (od * od / 4.0 - id_ * id_ / 4.0)
def hex_area(af):  # regular hexagon, across flats
    return math.sqrt(3.0) / 2.0 * af * af
def rhs_area(w, t):
    return w * w - (w - 2 * t) * (w - 2 * t)
def fillet_sec(leg):
    return 0.5 * leg * leg

# ---------------- inherited tanks (I032 declared geometry; upright barrels) ----------------
INH = {
    "U": {"station": (-14.0, 11.0, -19.0), "station2": (14.0, -11.0, -19.0), "straight": 4.20,
           "z_bot": -21.10, "z_top": -16.90},
    "L": {"station": (-14.0, -11.0, -21.5), "station2": (14.0, 11.0, -21.5), "straight": 3.00,
           "z_bot": -23.00, "z_top": -20.00},
}
OD, PLATE, HEAD_DEPTH, FREEBOARD = 3.05, 0.003, 0.30, 0.06
R_IN = OD / 2.0 - PLATE                      # 1.522 inner radius (straight segment)
A_STRAIGHT = math.pi * R_IN * R_IN           # inner straight-section area 7.2779 m^2
HEAD_STATUS = ("UNKNOWN - oblate-head inner volume, wall stock and displaced volume not "
               "established; straight-segment model only, no apex/tangent shortcut")
shell_a_per_m = tube_area(OD, OD - 2 * PLATE)
baffle_vol = ring_area(R_IN, 0.0, 0.003) - 8 * math.pi * 0.075 * 0.075 * 0.003
inh_rows = []
for tag in ("U", "L"):
    st = INH[tag]
    shell = shell_a_per_m * st["straight"] * RHO_5083
    baf = 2 * baffle_vol * RHO_5083
    inh_rows.append({
        "tank": tag, "straight_shell_kg": round(shell, 3), "baffles_2_kg": round(baf, 3),
        "head_stock_and_volume": HEAD_STATUS,
        "bands_2_kg_declared": round(2 * math.pi * OD * 0.100 * 0.006 * RHO_5083, 3),
        "adapter_kg_declared": 45.0, "fitout_allowance_kg_declared_50pct": 95.0,
        "lower_baffle_planes": "UNKNOWN - preserved, not invented",
    })

# ---------------- new external reserves (frozen construction) ----------------
RES = [{"name": "R1", "c": (-14.0, 7.60, -19.0), "lower": "L2", "upper": "U1"},
       {"name": "R4", "c": (14.0, -7.60, -19.0), "lower": "L3", "upper": "U4"}]
RZ_BOT, RZ_TOP, R_OD, R_WALL = -20.200, -17.800, 1.800, 0.004
R_RI = R_OD / 2.0 - R_WALL                   # 0.896 inner radius
R_STRAIGHT_I = 2.400                          # inner height between flat head inner faces
R_HEAD_T, RING_W, RING_T = 0.012, 0.100, 0.008
RING_RO, RING_RI = R_RI, R_RI - RING_W       # 0.896 / 0.796
STIFF_LEN = RING_RI - 0.100                   # collar OD 0.200 -> r 0.100
FIL6, FIL8 = fillet_sec(0.006), fillet_sec(0.008)

def reserve_stock():
    rows = []
    def add(item, count, vol_each, rho, note=""):
        m = count * vol_each * rho
        rows.append({"item": item, "count": count, "vol_each_m3": round(vol_each, 9),
                     "density": rho, "mass_kg": round(m, 3), "note": note})
        return m
    add("shell cylinder 1.8 OD x 4 mm x 2.4 m straight", 1, tube_area(R_OD, R_OD - 2 * R_WALL) * 2.4, RHO_5083)
    add("flat head plate 1.8 OD x 12 mm", 2, math.pi * (R_OD / 2) ** 2 * R_HEAD_T, RHO_5083)
    add("seating ring 100x8 at head (ro 0.896/ri 0.796)", 2, ring_area(RING_RO, RING_RI, RING_T), RHO_5083)
    add("T-stiffener web 100x8 x 0.696 m (steel, frozen assumption)", 12, STIFF_LEN * 0.100 * 0.008, RHO_STEEL)
    add("T-stiffener flange 60x8 x 0.696 m (steel, frozen assumption)", 12, STIFF_LEN * 0.060 * 0.008, RHO_STEEL)
    add("drain collar 200/120 x 20 steel annulus", 1, ring_area(0.100, 0.060, 0.020), RHO_STEEL)
    add("drain collar 2 mm insulating annulus (1200 assumed)", 1, ring_area(0.100, 0.060, 0.002), RHO_POLY)
    add("internal baffle at z_R 3 mm, 8x150 holes, solid stock", 1, baffle_like := ring_area(R_RI, 0.0, 0.003) - 8 * math.pi * 0.075 * 0.075 * 0.003, RHO_5083)
    # fillets: continuous 6 mm along each actual seam once
    seams_5083 = (2 * math.pi * R_RI      # shell-head (2)
                  + 2 * math.pi * R_RI    # ring-shell (2)
                  + 2 * math.pi * R_RI    # ring-head (2)
                  + 1 * math.pi * R_RI    # baffle-shell
                  + 1 * math.pi * 0.100)  # drain collar-head
    seams_steel = 12 * 2 * STIFF_LEN + 12 * STIFF_LEN  # web-head both sides, flange-web
    add("fillet 6 mm 5083 seams (shell/head/ring/baffle/collar)", 1, seams_5083 * FIL6, RHO_5083)
    add("fillet 6 mm steel seams (stiffener web/flange)", 1, seams_steel * FIL6, RHO_STEEL)
    return rows, seams_5083, seams_steel

# ---------------- frame per reserve ----------------
def frame_stock():
    rows = []
    def add(item, count, vol_each, rho, note=""):
        m = count * vol_each * rho
        rows.append({"item": item, "count": count, "vol_each_m3": round(vol_each, 9),
                     "density": rho, "mass_kg": round(m, 3), "note": note})
        return m
    A150 = rhs_area(0.150, 0.008); A100 = rhs_area(0.100, 0.006); A75 = rhs_area(0.075, 0.006)
    add("platform rails RHS150x150x8 x 2.400 m", 2, A150 * 2.400, RHO_STEEL)
    add("platform crossrails RHS150x150x8 x 2.100 m", 2, A150 * 2.100, RHO_STEEL,
        "closed tube faces; end joins modelled, no silent intersection removal")
    add("cradle beams RHS150x150x8 x 2.100 m", 2, A150 * 2.100, RHO_STEEL)
    add("cradle polymer pads 2.100x0.150x0.013", 2, 2.100 * 0.150 * 0.013, RHO_POLY, "capacity UNKNOWN")
    brace_len = math.hypot(2.250, 1.875)
    add("legs RHS100x100x6 x 1.875 m", 4, A100 * 1.875, RHO_STEEL)
    add("braces RHS75x75x6 x %.4f m (cyclic corners)" % brace_len, 4, A75 * brace_len, RHO_STEEL,
        "buckling/connection UNKNOWN, axial-only claim refused")
    add("foot plates 350x350x25", 4, 0.350 * 0.350 * 0.025, RHO_STEEL)
    add("receiver plates 350x350x25 (NEW interface datum)", 4, 0.350 * 0.350 * 0.025, RHO_STEEL,
        "receiving structure stock/stiffness/capacity UNKNOWN")
    m20 = (math.pi * 0.010 ** 2 * 0.140 + hex_area(0.030) * 0.013 + hex_area(0.030) * 0.020
           + 2 * ring_area(0.020, 0.011, 0.003) + 0.060 * 0.060 * 0.012)
    add("M20x140 bolt sets (shank+30AF head13+nut20+2 washers+backer)", 32, m20, RHO_STEEL,
        "8/foot at (+/-120,+/-120),(+/-120,0),(0,+/-120); no area pooling")
    add("gusset blanks 250x250x12", 8, 0.250 * 0.250 * 0.012, RHO_STEEL)
    gusset_seam = 8 * 2 * 0.150 + 4 * 2 * 0.075 + 4 * 4 * 0.100
    add("fillet 8 mm frame seams (gussets/braces/feet)", 1, gusset_seam * FIL8, RHO_STEEL)
    # hold-down bands
    band_len = math.pi * (R_OD + 0.004 + 0.006)   # over 2 mm liner, mid-thickness convention
    liner_len = math.pi * (R_OD + 0.002)
    add("hold-down bands 100x6 at z_R +/-0.900", 2, band_len * 0.100 * 0.006, RHO_5083)
    add("band liners 2 mm (1200 assumed)", 2, liner_len * 0.100 * 0.002, RHO_POLY)
    add("band lugs 200x150x12", 4, 0.200 * 0.150 * 0.012, RHO_STEEL)
    m16_120 = (math.pi * 0.008 ** 2 * 0.120 + hex_area(0.024) * 0.010 + hex_area(0.024) * 0.016
               + 2 * ring_area(0.016, 0.009, 0.003))
    add("M16x120 band sets (24AF head10/nut16/2 washers)", 8, m16_120, RHO_STEEL)
    strap_len = 2 * (2.200 + 0.400)               # band z=-18.1/-19.9 to platform -20.300
    add("40x6 vertical strap blanks to platform", 1, strap_len * 0.040 * 0.006, RHO_STEEL,
        "attach at x=+/-1.125, y=y_R midpoint; bending/clearance/load transfer explicit-UNKNOWN")
    add("pump interface plate 600x500x10", 1, 0.600 * 0.500 * 0.010, RHO_STEEL)
    add("M16x120 pump-plate sets", 4, m16_120, RHO_STEEL)
    return rows, brace_len

# ---------------- circuits and routes ----------------
DN100_A, DN80_A, DN50_A, DN300_A = (tube_area(0.1143, 0.1083), tube_area(0.0889, 0.0829),
                                    tube_area(0.0603, 0.0543), tube_area(0.324, 0.312))
PIPE80_A = tube_area(0.080, 0.074)
M16_80 = (math.pi * 0.008 ** 2 * 0.080 + hex_area(0.024) * 0.010 + hex_area(0.024) * 0.016
          + 2 * ring_area(0.016, 0.009, 0.003))
M12_80 = (math.pi * 0.006 ** 2 * 0.080 + hex_area(0.018) * 0.008 + hex_area(0.018) * 0.012
          + 2 * ring_area(0.014, 0.007, 0.003))
CLAMP_KG = 2.0 + 1.0 + 0.200 * 0.200 * 0.008 * RHO_STEEL + 4 * M12_80 * RHO_STEEL

def circuit_rows():
    rows = []
    def add(item, count, mass_each, note=""):
        rows.append({"item": item, "count": count, "mass_each_kg": round(mass_each, 4),
                     "mass_kg": round(count * mass_each, 3), "note": note})
    add("DN100 draw stub 0.300 m", 1, DN100_A * 0.300 * RHO_STEEL)
    add("DN100 fill stub 0.300 m", 1, DN100_A * 0.300 * RHO_STEEL)
    add("DN80 reset-drain stub 0.300 m", 1, DN80_A * 0.300 * RHO_STEEL)
    add("DN100 isolation valves 15 kg (declared device)", 3, 15.0)   # 2 draw + 1 fill
    add("DN100 check valve 12 kg (declared device)", 1, 12.0)
    add("DN80 drain valve 15 kg (declared device)", 1, 15.0)
    flange = ring_area(0.110, 0.058, 0.020) * RHO_STEEL
    add("DN100 flanges OD220/ID116/20 (4 conn x 2 mating)", 8, flange)
    add("M16x80 flange bolt sets", 64, M16_80 * RHO_STEEL)
    add("3 mm annular seals (1200 assumed)", 4, ring_area(0.110, 0.058, 0.003) * RHO_POLY)
    # vent line: stub 0.3 + x+0.3 + y+1.1 + down 10.0 to z=-27.8
    vent_len = 0.300 + 0.300 + 1.100 + (RZ_TOP - (-27.800))
    add("DN50 vent line %.3f m incl bends (centreline)" % vent_len, 1, vent_len * DN50_A * RHO_STEEL,
        "3 bends; hood/cuff/blanks separately")
    add("P/V assembly 12 kg", 1, 12.0); add("trap 5 kg", 1, 5.0); add("drain 5 kg", 1, 5.0)
    add("exterior hood 5 kg", 1, 5.0); add("flanged cuff 15 kg", 1, 15.0)
    add("vent blanks 300x300x6", 2, 0.300 * 0.300 * 0.006 * RHO_STEEL)
    add("pump 45 kg 20 kg/s @0.2 MPa (unqualified assumption)", 1, 45.0)
    add("pump valves 15 kg", 2, 15.0); add("pump wiring/drive 12 kg", 1, 12.0)
    return rows, vent_len

# fresh route: outlet(x_R,y_R,z=-20.212) -> (x_R,y_R,-21.5) -> (x_R,y_R,-23.0) -> (x_L,y_L,-23.0)
#   -> ascent 3.3 to lower apex -19.700 -> DN100 stub 0.3 (lower TOP inlet)
def fresh_route(res):
    x_r, y_r, _ = res["c"]; x_l, y_l, _ = INH["L"]["station"] if res["lower"] == "L2" else INH["L"]["station2"]
    segs = [abs(-20.212 - (-21.500)), abs(-21.500 - (-23.000)), abs(y_r - y_l), abs(-23.000 - (-19.700))]
    poly = sum(segs) + 0.300
    bends = 2                                   # at (x_R,y_R,-23.0) and (x_L,y_L,-23.0)
    centre80 = sum(segs) - bends * (2 * 0.200 - math.pi * 0.200 / 2.0)
    clamps = sum(max(1, math.ceil(s / 2.0)) for s in segs) + 1 + bends + 2 + 1 + 2  # runs+stub+elbows+valves/check+pump+reducers
    return {"pair": res["name"] + "->" + res["lower"], "segments_m": [round(s, 3) for s in segs],
            "stub_dn100_m": 0.300, "reducers_0.200m_frusta": 2, "elbows_r0.200": bends,
            "pipe80_centreline_m": round(centre80, 3),
            "pipe80_kg": round(centre80 * PIPE80_A * RHO_STEEL, 3),
            "stub_kg": round(DN100_A * 0.300 * RHO_STEEL, 3),
            "reducer_kg": round(2 * 0.200 * math.pi * ((0.1143 + 0.080) / 2) * 0.003 * RHO_STEEL, 3),
            "water_inventory_kg_when_filled": round(centre80 * math.pi * 0.037 ** 2 * RHO_WATER, 3),
            "clamps": clamps, "clamp_assembly_kg": round(clamps * CLAMP_KG, 3),
            "lengths_non_negative": all(s >= 0 for s in segs)}

def scoop_route(res):
    x_u, y_u, _ = INH["U"]["station"] if res["upper"] == "U1" else INH["U"]["station2"]
    segs = [3.000, abs(y_u - 0.0), abs(-23.500 - (-16.300))]
    bends = 3
    centre = sum(segs) - bends * (2 * 0.300 - math.pi * 0.300 / 2.0)
    clamps = sum(max(1, math.ceil(s / 2.0)) for s in segs) + 1 + bends + 1
    return {"service": res["upper"], "segments_S_P_V_F_m": [round(s, 3) for s in segs],
            "stub_m": 0.300, "elbows_r0.300": bends, "pipe114_centreline_m": round(centre, 3),
            "pipe_kg": round(centre * DN100_A * RHO_STEEL, 3),
            "stub_kg": round(DN100_A * 0.300 * RHO_STEEL, 3),
            "water_inventory_kg_when_filled": round(centre * math.pi * 0.05415 ** 2 * RHO_WATER, 3),
            "clamps": clamps, "clamp_assembly_kg": round(clamps * CLAMP_KG, 3),
            "pump_set_kg_declared": 94.0, "P_equipment_frames": "retained, separately paid",
            "lengths_non_negative": all(s >= 0 for s in segs)}

# ---------------- reserve enclosed geometry (stock payment only) ----------------
datum_z = RZ_TOP - FREEBOARD                   # -17.860
enclosed = math.pi * R_RI ** 2 * (R_STRAIGHT_I - FREEBOARD)
disp_bottom_ring = ring_area(RING_RO, RING_RI, RING_T)
disp_baffle = ring_area(R_RI, 0.0, 0.003) - 8 * math.pi * 0.075 * 0.075 * 0.003
disp_collar = ring_area(0.100, 0.060, 0.020) + ring_area(0.100, 0.060, 0.002)
top_ring_above_datum = True                    # top ring z -17.808..-17.800 above -17.860
geometric_net = enclosed - disp_bottom_ring - disp_baffle - disp_collar
capacity = {"enclosed_to_freeboard_datum_m3": round(enclosed, 4),
            "displacements_subtracted_once_m3": {"bottom_ring": round(disp_bottom_ring, 6),
                                                 "baffle": round(disp_baffle, 6),
                                                 "drain_collar_and_insulator": round(disp_collar, 6),
                                                 "top_ring": "above datum, not displaced",
                                                 "nozzle_penetrations": "UNKNOWN"},
            "geometric_net_m3": round(geometric_net, 4),
            "acceptance_demand_m3": 5.0,
            "status": "UNKNOWN - vent/overflow inlet unestablished, flat-bottom deadwater and "
                      "penetration volumes unknown; NO usable-volume or margin claim"}

# ---------------- events, centroids, wrenches ----------------
def liquid_cz(kind, tonnes):
    v = tonnes  # m3 at 1000 kg/m3
    if v <= 0: return None
    h = v / A_STRAIGHT if kind != "R" else v / (math.pi * R_RI ** 2)
    z0 = {"U": INH["U"]["z_bot"], "L": INH["L"]["z_bot"], "R": RZ_BOT}[kind]
    note = "straight-segment vertical fill; head contribution UNKNOWN" if kind != "R" \
        else "flat-head vertical cylinder, exact"
    return {"volume_m3": round(v, 4), "fill_height_m": round(h, 4),
            "centroid_z": round(z0 + h / 2.0, 4), "model": note}

def state(name, per_pair, per_pair_b=None):
    # per_pair = (service fresh, reserve, lower, scoop) tonnes; second value for asymmetric states
    pp_b = per_pair if per_pair_b is None else per_pair_b
    parts = []
    for i, res in enumerate(RES):
        per_pair_now = (per_pair if i == 0 else pp_b)
        x_r, y_r, z_r = res["c"]
        rrows, _, _ = reserve_stock(); frows, _ = frame_stock(); crows, _ = circuit_rows()
        m_res = sum(r["mass_kg"] for r in rrows) / 1000.0
        m_frame = sum(r["mass_kg"] for r in frows) / 1000.0
        m_circ = sum(r["mass_kg"] for r in crows) / 1000.0
        fr = fresh_route(res); sr = scoop_route(res)
        x_u, y_u, _ = INH["U"]["station"] if res["upper"] == "U1" else INH["U"]["station2"]
        x_l, y_l, _ = INH["L"]["station"] if res["lower"] == "L2" else INH["L"]["station2"]
        # (tonnes, x, y, z) - dry masses at declared centres
        parts += [
            (m_res, x_r, y_r, z_r, "reserve dry %s" % res["name"]),
            (m_frame, x_r, y_r, -20.95, "frame+plates %s (component CG approx at frame mid, "
             "individual part centres in bill)" % res["name"]),
            (m_circ, x_r, y_r, -19.0, "reserve circuit hardware %s" % res["name"]),
            (fr["pipe80_kg"] / 1000.0 + fr["stub_kg"] / 1000.0 + fr["reducer_kg"] / 1000.0, x_r, (y_r + y_l) / 2.0, -21.9, "fresh route pipe %s" % res["name"]),
            (fr["clamp_assembly_kg"] / 1000.0, x_r, (y_r + y_l) / 2.0, -22.3, "fresh clamps %s" % res["name"]),
            (sr["pipe_kg"] / 1000.0 + sr["stub_kg"] / 1000.0, x_u, y_u / 2.0, -21.0, "scoop route %s" % res["upper"]),
            (sr["clamp_assembly_kg"] / 1000.0, x_u, y_u / 2.0, -22.5, "scoop clamps %s" % res["upper"]),
            (0.094, x_u, 0.0, -23.5, "scoop pump set %s (declared 94 kg)" % res["upper"]),
            (0.008, x_r, y_r, z_r, "instruments reserve"),
            (0.008, x_l, y_l, -21.5, "instruments lower"),
            (0.008, x_u, y_u, -19.0, "instruments upper"),
            (0.010, x_r, y_r, z_r, "interlocked controller (same-frame pair)"),
        ]
        # inherited tank dry stock (straight+baffles only; heads UNKNOWN)
        for tag, st in (("U", (x_u, y_u)), ("L", (x_l, y_l))):
            row = next(r for r in inh_rows if r["tank"] == tag)
            m = (row["straight_shell_kg"] + row["baffles_2_kg"]) / 1000.0
            parts.append((m, st[0], st[1], INH[tag]["z_bot"] + INH[tag]["straight"] / 2.0,
                          "inherited %s straight shell+2 baffles (heads UNKNOWN)" % tag))
            parts.append(((row["bands_2_kg_declared"] + row["adapter_kg_declared"]) / 1000.0, st[0], st[1],
                          INH[tag]["z_bot"] + INH[tag]["straight"] / 2.0, "bands+adapter %s (declared)" % tag))
            parts.append((0.095, st[0], st[1], INH[tag]["z_bot"] + INH[tag]["straight"] / 2.0,
                          "fitout allowance %s (declared +/-50%%)" % tag))
        # liquid - unpartitioned upper barrel holds svc+scoop as ONE fill
        svc, resv, low, scp = per_pair_now
        for tonnes, kind, (xx, yy) in ((svc + scp, "U", (x_u, y_u)),
                                        (resv, "R", (x_r, y_r)), (low, "L", (x_l, y_l))):
            if tonnes > 0:
                cz = liquid_cz(kind, tonnes)
                parts.append((tonnes, xx, yy, cz["centroid_z"], "liquid %s" % kind))
        # fresh-route water inventory during D2 (both circuits flowing)
        if name.startswith("D2") and (per_pair_now[1] > 0 or per_pair_now[2] > 0):
            parts.append((fr["water_inventory_kg_when_filled"] / 1000.0, x_r, (y_r + y_l) / 2.0, -21.9,
                          "fresh-route pipe water (filled during D2)"))
    M = sum(p[0] for p in parts)
    Fz = -M * 1000.0 * G
    # r x F with F=(0,0,-mg):  Mx = y*Fz = -m g y ;  My = -x*Fz = +m g x
    Mx = -sum(p[0] * 1000.0 * G * p[2] for p in parts)
    My = sum(p[0] * 1000.0 * G * p[1] for p in parts)
    return {"state": name, "per_pair_commanded_t": list(per_pair),
            "total_mass_t": round(M, 4), "wrench_at_origin_N_and_Nm":
            {"Fx": 0.0, "Fy": 0.0, "Fz": round(Fz, 1), "Mx": round(Mx, 1), "My": round(My, 1), "Mz": 0.0},
            "support_note": "aggregate six-component wrench retained; individual foot/band/receiver "
                            "reactions UNKNOWN - no equal split, no rigid support, receiver stiffness C"}

NOMINAL = [("before_D1", (25.0, 5.0, 20.0, 0.0)), ("D1_complete", (0.0, 5.0, 20.0, 0.0))]
for s in (0.0, 0.25, 0.5, 0.75, 1.0):
    NOMINAL.append(("D2_s=%.2f" % s, (0.0, round(5.0 * (1 - s), 4), round(20.0 * (1 - s), 4), round(25.45 * s, 4))))
states = [state(n, pp) for n, pp in NOMINAL]
# inherited D1 intermediate + switch states (one service empty while opposite still full, both orders)
states.append(state("D1_one_empty_A", (0.0, 5.0, 20.0, 0.0), (25.0, 5.0, 20.0, 0.0)))
states.append(state("D1_one_empty_B", (25.0, 5.0, 20.0, 0.0), (0.0, 5.0, 20.0, 0.0)))
sw = state("switch_not_confirmed", (0.0, 5.0, 20.0, 0.0))
sw["note"] = "inventory identical to D1_complete; isolators/positive blank not yet verified - " \
             "scoop admission barred until confirmed; verification duty/energy UNKNOWN"
states.append(sw)

# ---------------- eight D2 command cases ----------------
T_WINDOW = 2700.0
def case(leader, eps_sign, lag):
    eps = 0.05 * eps_sign
    out = {"leader": leader, "rate_error": eps, "lag_s": lag, "pairs": {}}
    for pair in ("A", "B"):
        lead = (pair == leader)
        rate_f = 1 + (eps if lead else -eps)
        delay = 0.0 if lead else lag
        # internal 1:4 reserve:lower split is source accounting; command targets per pair
        res = {}
        for circuit, target in (("fresh", 25000.0), ("scoop", 25450.0)):
            rate = target / T_WINDOW * rate_f
            delivered = min(max(0.0, rate * (T_WINDOW - delay)), target)
            short = target - delivered
            res[circuit] = {"command_target_kg": target, "delivered_kg": round(delivered, 1),
                            "shortfall_kg": round(short, 1),
                            "status_at_T": "PASS(clamped)" if short <= 1e-9 else "FAIL"}
        out["pairs"][pair] = res
    tf = sum(p["fresh"]["shortfall_kg"] for p in out["pairs"].values())
    out["total_fresh_shortfall_kg"] = round(tf, 1)
    return out
cases = []
for leader in ("A", "B"):
    for es in (+1, -1):
        for lag in (0.0, 2.0):
            cases.append(case(leader, es, lag))

# ---------------- bill assembly ----------------
res_rows, seams5083, seamssteel = reserve_stock()
frame_rows, brace_len = frame_stock()
circ_rows, vent_len = circuit_rows()
bill_new = {
    "per_reserve_total_kg": round(sum(r["mass_kg"] for r in res_rows), 3),
    "per_frame_total_kg": round(sum(r["mass_kg"] for r in frame_rows), 3),
    "per_circuit_total_kg": round(sum(r["mass_kg"] for r in circ_rows), 3),
    "counts": {"reserves": 2, "frames": 2, "reserve_circuits": 2, "fresh_routes": 2, "scoop_routes": 2,
               "M20_sets_total": 64, "M16_sets_total": 8 * 2 + 64 + 8, "M12_sets_total":
               sum(fresh_route(r)["clamps"] + scoop_route(r)["clamps"] for r in RES) * 4},
    "rules": ["every stock item from fixed selected stock at declared densities",
              "collars/flanges/seals/penetrations paid individually; unpriced fittings remain C",
              "no scrap credit; both stiffener interfaces charged at full length",
              "old divider sump/through-reserve drain ABSENT: no numeric old-bill saving claimed - "
              "their complete old mass was never established"],
}

ledger = {
    "rule": "NEW ledger from fixed construction and accepted saved inputs; NEVER a subtraction "
            "from the I035 8.991 t figure; I035 outputs are withdrawn/archival",
    "new_computed_t_per_pair": round((bill_new["per_reserve_total_kg"] + bill_new["per_frame_total_kg"]
                                      + bill_new["per_circuit_total_kg"]) / 1000.0, 4),
    "new_routes_t_per_pair": round((fresh_route(RES[0])["pipe80_kg"] + fresh_route(RES[0])["stub_kg"]
                                    + fresh_route(RES[0])["reducer_kg"] + fresh_route(RES[0])["clamp_assembly_kg"]
                                    + scoop_route(RES[0])["pipe_kg"] + scoop_route(RES[0])["stub_kg"]
                                    + scoop_route(RES[0])["clamp_assembly_kg"]) / 1000.0, 4),
    "inherited_straight_stock_t_per_pair": round((inh_rows[0]["straight_shell_kg"] + inh_rows[0]["baffles_2_kg"]
                                                  + inh_rows[1]["straight_shell_kg"] + inh_rows[1]["baffles_2_kg"]) / 1000.0, 4),
    "i017_conditional_rows_shown_separately": True,
    "qualified_retirement_t": 0.0,
    "conditional_comparison": "only where a rowwise common-duty match exists (see duty table); "
                              "no-retirement bound retains all previously charged duties",
    "no_qualified_total_while_C_unpriced": True,
}

C_UNRESOLVED = [
    "inherited oblate-head steel stock and inner volume (both pairs)",
    "lower-tank baffle planes (UNKNOWN in sources; not invented)",
    "receiving structure: receiver plates' counterpart stock, stiffness, capacity, bolt procurement",
    "flat-head structural adequacy; frame weld capacities; brace buckling; band/strap load transfer",
    "vent/overflow inlet height -> true usable volume of every tank",
    "nozzle penetration displacements; unpriced fittings (collars/seals beyond enumerated)",
    "DN300 service double-isolation/blank/bleed mounts and service drain valve hardware",
    "gas/ballonet occupation of the envelope region the reserves+frames occupy (UNKNOWN)",
    "cleaning/verification energy and reset transition energy beyond the 18.9 MJ listed subset",
    "external S-interface connection and P equipment frame mounts",
]

scoreboard = {
    "usable_capacity": "UNKNOWN (all six tanks; vent inlet/deadwater/heads unresolved)",
    "fresh_delivery_8cases": "FAIL class: lagging pair short by construction (see cases); "
                             "unfinished at T is FAIL, never extension",
    "economics": "inherited FAIL 35.1x vs SEAT ($5929/t) - unchanged by this unit",
    "fuel": "inherited FAIL shorts 0.245112 t (33-min) / 0.350732 t (half-pump) - unchanged",
    "structure": "UNKNOWN - no welded-joint, flat-head, frame or receiver capacity claim",
    "physical_float": "NOT SHOWN",
    "weakest_assumption": "the external reserves + receiving structure are installable without "
                          "consuming unreserved bag/equipment space or envelope capacity",
    "one_later_hypothesis_unissued": "paid shared same-frame collection beam (not adopted here)",
}

out = {
    "unit": "R3-I038", "calculator": "reserve.py", "mode": "finite stock/geometry; no qualifications",
    "deltas_from_I035": "divider system absent: one unpartitioned upper service barrel; one independent "
                        "external reserve per upper barrel; reserve fresh never passes through the scoop chamber; "
                        "the 0.45 t-per-lower relocation stays upstairs (location, not mass)",
    "densities": {"5083": RHO_5083, "steel": RHO_STEEL, "polymer_assumed": RHO_POLY, "water": RHO_WATER},
    "reserve_stock_rows": res_rows, "frame_stock_rows": frame_rows, "circuit_rows": circ_rows,
    "inherited_tank_rows": inh_rows, "head_status": HEAD_STATUS,
    "reserve_enclosed_geometry": capacity,
    "fresh_routes": [fresh_route(r) for r in RES], "scoop_routes": [scoop_route(r) for r in RES],
    "vents": {"service": "top stub +0.300 x, +1.800 y, down to -27.800",
              "reserve": "top stub +0.300 x, +1.100 y, down to -27.800",
              "reserve_line_m_and_kg": [vent_len, round(vent_len * DN50_A * RHO_STEEL, 3)],
              "lower_duties": "charged independently; hood 5 / cuff 15 / 2 blanks per vent included"},
    "bill": bill_new, "ledger": ledger, "C_unresolved": C_UNRESOLVED,
    "states_and_wrenches": states,
    "d2_eight_cases": cases,
    "events_command_law": "per pair (service fresh, reserve, lower, scoop): before D1 (25,5,20,0); "
                          "D1 complete (0,5,20,0); D2 fraction s (0,5(1-s),20(1-s),25.45s); complete (0,0,0,25.45); "
                          "no reserve transfer during D1; both service chambers empty+isolated/blanked/verified "
                          "before scoop admission; 1:4 reserve:lower split frozen; clamp by command target",
    "i017_conditional_duty_rows": "carried in baseline.json category_1; qualified retirement ZERO",
    "scoreboard": scoreboard,
    "assumptions_declared": [
        "T-stiffeners, frame, fasteners, routes: steel 7850 (stiffener material frozen assumption)",
        "polymer density 1200 (pads/seals/liners/insulator); M12 hardware 18AF/8/12, washer 28/14/3 (derived pattern)",
        "band/liner lengths at mid-thickness circumferences; elbow centreline = arc, corner replaced (declared)",
        "pipe water counted in state mass during D2 (filled); priming volume before D2 UNKNOWN",
        "fresh pump 45 kg 20 kg/s @0.2 MPa is an unqualified device assumption",
        "route endpoints frozen per design freeze; frame/pipe CGs at segment/assembly centres",
    ],
}

def main():
    if "--write" in sys.argv:
        here = "/".join(__file__.split("/")[:-1])
        path = here + "/reserve.json"
        data = json.dumps(out, indent=1, sort_keys=False) + "\n"
        with open(path, "w") as f:
            f.write(data)
        print("wrote %s (%d bytes)" % (path, len(data.encode())))
    else:
        print(json.dumps({"summary": scoreboard, "bill": bill_new, "ledger": ledger}, indent=1))

if __name__ == "__main__":
    main()
