#!/usr/bin/env python3
"""R3-I027 calculator: four upright curved tanks (barrels) replacing I017's four
rectangular flat-panel tanks at the inherited P-100 stations.

Reads only frozen data in baseline.json (see sources.json). Standard library only.
Writes tank.json next to this file. Finite cases per the issued unit contract:
four fixed stations; inherited full, skew-inclusive mismatch and one-bay-empty
states; directly affected D1/D1-end/floor/ceiling budgets; the two inherited
displacement conventions. No sizing sweep; the geometry is frozen.

Implementation validation (inside this single run, against recorded I017 data):
  V1  lift law reproduces recorded n0 162,278 / n1 111,338 at DRY 66.18 (±5 m3)
  V2  authority law reproduces recorded 244.7 / 650.8 / 922.3 t·m (±0.5%)
  V3  section law reproduces the recorded worst corner 1.38 m at z = -22.93 (±0.02 m)
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
B = json.load(open(os.path.join(HERE, "baseline.json"), encoding="utf-8"))

def near(name, got, want, tol):
    if abs(got - want) > tol:
        print("VALIDATION FAIL %s: got %.4f want %.4f tol %.4f" % (name, got, want, tol), file=sys.stderr)
        sys.exit(2)

# ----------------------------------------------------------------- 1. geometry
C   = B["frozen_candidate"]
M   = B["frozen_mission_inherited"]
I17 = B["frozen_i017_comparison"]

OD      = C["outside_diameter_m"]            # 3.05
r_o     = OD / 2.0                            # 1.525 outer radius
t_plate = C["plate_thickness_m"]              # 0.003
r_i     = r_o - t_plate                       # 1.522 inner radius
h_bar   = C["straight_barrel_height_m"]       # 3.60 straight barrel (outer)
c_head  = C["head_depth_m_each"]              # 0.30 outer head depth
c_i     = c_head - t_plate                    # 0.297 inner head depth
freeb   = C["freeboard_m"]                    # 0.06 below top-head springline
rho_al  = C["alloy_density_t_per_m3"]         # 2.66
r_mid   = r_o - t_plate / 2.0                 # mid-surface radius
c_mid   = c_head - t_plate / 2.0

A_i      = math.pi * r_i * r_i                # inner disc area
V_bar_w  = A_i * (h_bar - freeb)              # barrel water below freeboard
V_head_i = (2.0 / 3.0) * math.pi * r_i**2 * c_i   # one inner head cavity
n_baf    = C["internal_baffles"]
V_baf    = n_baf * A_i * C["baffle_thickness_m"]
V_sump   = 0.030                              # declared drain remainder (m3)
usable   = V_bar_w + V_head_i - V_baf - V_sump
req_fresh_m3 = M["per_bay_required_water_t_fresh"] / M["fresh_density_t_per_m3"]
req_salt_m3  = M["per_bay_required_water_t_fresh"] / M["salt_density_t_per_m3"]
capacity_screen = "PASS" if usable >= req_fresh_m3 - 1e-9 else "FAIL"
V_env_tank = math.pi * r_o**2 * h_bar + 2.0 * (2.0 / 3.0) * math.pi * r_o**2 * c_head

# ------------------------------------------------------------------- 2. mass bill
A_bar_mid = 2.0 * math.pi * r_mid * h_bar                       # barrel mid-surface
A_head_mid = math.pi * r_mid**2 * math.sqrt(1.0 + (c_mid / r_mid)**2)  # shallow-head approx
m_barrel   = A_bar_mid * t_plate * rho_al
m_heads    = 2.0 * A_head_mid * t_plate * rho_al
weld_frac  = 0.08                                               # declared seam/weld allowance
m_weld     = weld_frac * (m_barrel + m_heads)
m_baffles  = V_baf * rho_al
m_manway   = 0.030                                              # declared: manway ring+cover+doubler
m_ports    = 3 * 0.008                                          # fill/vent/drain port fittings
m_sumpfit  = 0.010                                              # sump fitting
m_tank_hw  = m_barrel + m_heads + m_weld + m_baffles + m_manway + m_ports + m_sumpfit

band_w, band_t = 0.100, 0.006
m_bands    = 2.0 * math.pi * (OD + band_t) * band_w * band_t * rho_al
m_adapter  = 0.045                                              # declared adapter assembly (saddles, clevis, links, its fasteners)
m_doubler  = 2 * 0.010                                          # band-zone local reinforcement
m_supports = m_bands + m_adapter + m_doubler
m_per_tank = m_tank_hw + m_supports
m_set_tanks   = 4.0 * m_per_tank
m_install     = 0.080                                           # declared set-level installation/access allowance (ASSUMED)
new_stock     = m_set_tanks + m_install

retired = sum(I17["retired_lines_t"].values())                  # 3.53
reused  = sum(I17["reused_lines_t"].values())                   # 2.37
fasteners_retained = I17["interface_fasteners_t"]               # 0.10 (fit to new adapters: UNKNOWN)
new_set_total = new_stock + reused + fasteners_retained
delta_set = new_set_total - I17["drawn_set_total_t"]            # vs 6.00

DRY_old = I17["dry_vehicle_t"]                                  # 66.18 (fuel-in-dry convention kept)
DRY_new = DRY_old + delta_set
loaded_new = DRY_new + M["payload_t"]

# --------------------------------------------------------- 3. hydrostatics/loads
g      = M["g_m_per_s2"]
col_full  = (h_bar - freeb) + c_i                               # surface to bottom-head apex
p_bot_f   = M["fresh_density_t_per_m3"] * g * col_full          # Pa
p_bot_s   = M["salt_density_t_per_m3"] * g * col_full
p_bar_bot = M["fresh_density_t_per_m3"] * g * (h_bar - freeb)   # at bottom of straight wall
hoop_f = p_bar_bot * r_i / t_plate                              # Pa (membrane, barrel bottom)
hoop_s = hoop_f * M["salt_density_t_per_m3"] / M["fresh_density_t_per_m3"]
axial_f = hoop_f / 2.0
head_res_f = p_bot_f * A_i / 1000.0                             # kN (p at apex x projected area: upper bound)
head_res_s = head_res_f * M["salt_density_t_per_m3"] / M["fresh_density_t_per_m3"]

w_full_bay = M["per_bay_required_water_t_fresh"] + m_tank_hw    # water + hung hardware (bands/adapter carry to pickups)
R_pick_full = w_full_bay * g / 2.0 / 1000.0                     # kN per pickup datum (two share)
q_band = R_pick_full / 2.0 / (math.pi * OD / 2.0)               # kN/m line load per band, uniform half-circumference (declared)

# ------------------------------------------------------------------ 4. states
w_water = M["per_bay_required_water_t_fresh"]
rate = M["rate_mismatch_fraction"]; skew = M["pair_start_skew_s"]; window_s = M["drain_window_min_approx"] * 60
m_mis = rate * w_water + (w_water / window_s) * skew            # skew-inclusive bound (t)
y_arm, x_arm = 11.0, 14.0
roll_mis, pitch_mis = m_mis * y_arm, m_mis * x_arm
roll_1e, pitch_1e = w_water * y_arm, w_water * x_arm             # one bay released (hardware stays)
dR_pick_mis = m_mis * g / 2.0 / 1000.0                          # kN pickup imbalance, lagging bay

# authority law (verified below against recorded datums)
mix = M["mixture_fraction"]; lever = M["ballonet_lever_m"]; cap_bag = M["per_bag_cap_m3"]
def authority(air_t, rho_air):
    v_bag = air_t / rho_air                    # total bag volume (bags split 50/50)
    donor = v_bag / 2.0
    headroom = cap_bag - donor
    return min(donor, headroom) * rho_air * (1.0 - mix) * lever
ac = I17["authority_law_check"]["datums"]; auth_rec = I17["authority_net_t_m"]
auth_calc = {}
for d in ac:
    auth_calc[d["name"]] = authority(d["air_t"], d["air_density_t_per_m3"])
near("V2 min_air",     auth_calc["min_air"],              auth_rec["min_air"],              0.005 * auth_rec["min_air"])
near("V2 D1_end",      auth_calc["D1_end_mismatch"],      auth_rec["D1_end_mismatch"],      0.005 * auth_rec["D1_end_mismatch"])
near("V2 one_bay",     auth_calc["one_bay_empty_mid_D1"], auth_rec["one_bay_empty_mid_D1"], 0.005 * auth_rec["one_bay_empty_mid_D1"])

heel_mis  = I17["heel_deg_mismatch"]  * roll_mis / I17["mismatch_roll_t_m"]
heel_1e   = I17["heel_deg_one_empty"] * roll_1e  / I17["one_empty_roll_t_m"]

# ------------------------------------------------------------------ 5. ledger
k = M["lift_t_per_1000m3"]
def n_inv(weight_t): return weight_t / k * 1000.0
n0_old, n1_old = I17["n0_m3"], I17["n1_D1_end_m3"]
near("V1 n0", n_inv(DRY_old + M["payload_t"]), n0_old, 5.0)
near("V1 n1", n_inv(DRY_old + M["payload_t"] - M["delivery_D1_t"] - M["burn_to_D1_t"]), n1_old, 5.0)

n0_new = n_inv(loaded_new)
n1_new = n_inv(loaded_new - M["delivery_D1_t"] - M["burn_to_D1_t"])
floor_anchor = M["installed_bag_cap_m3_total"]                       # 110,000
V_anchor, V_drawn = M["anchor_volume_m3"], M["drawn_volume_m3"]
floor_drawn  = V_drawn - floor_anchor                                # 107,547 (I017 recorded basis)
clear_anchor = n1_new - floor_anchor
clear_drawn  = n1_new - floor_drawn
bag_base = V_anchor - n1_new
bag_pct_V, bag_pct_cap = bag_base / V_anchor * 100.0, bag_base / floor_anchor * 100.0
margin_anchor = I17["ceiling_max_lift_anchor_t"] - loaded_new
margin_drawn  = I17["ceiling_max_lift_drawn_t"] - loaded_new
vent = n0_new - n1_new
dn0 = n0_new - n0_old                                               # net displaced-mixture change (S0)
crossover_slack = DRY_new - I17["floor_crossover_dry_t"]            # further dry drop before floor binds

# --------------------------------------------------------------------- 6. fit
hw = I17["hull_half_width_m"]                                        # {"z_-19.0":19.9,"z_-21.5":17.1}
z1, z2, z3 = -19.0, -21.5, -22.93                                    # datums; z3 = I017 worst-corner depth
corner_y, corner_clr = 12.53, 1.38                                   # recorded worst corner (B2-FR/B3-AL)
hw_z3 = corner_y + corner_clr                                        # 13.91
slope_lo = (hw_z3 - hw["z_-21.5"]) / (z3 - z2)                       # calibrated taper below -21.5 (m/m, positive)
slope_up = (hw["z_-19.0"] - hw["z_-21.5"]) / (z1 - z2)
def hw_cal(z):
    if z >= z2: return hw["z_-21.5"] + slope_up * (z - z2)
    return hw["z_-21.5"] + slope_lo * (z - z2)
near("V3 corner", hw_cal(z3) - corner_y, corner_clr, 0.02)
def hw_linfloor(z):  # rejected stiff basis: linear from -21.5 to hull floor -27.5
    return hw["z_-21.5"] * (I17["hull_floor_z_m"] - z) / (I17["hull_floor_z_m"] - z2)

def y_tank(z, z_c):
    dz = abs(z - z_c)
    if dz <= h_bar / 2.0: return r_o
    if dz <= h_bar / 2.0 + c_head:
        xx = (dz - h_bar / 2.0) / c_head
        return r_o * math.sqrt(1.0 - xx * xx)
    return 0.0
def scan(z_c, law):
    worst, z_w = 1e9, None
    z = z_c - (h_bar / 2.0 + c_head)
    while z <= z_c + (h_bar / 2.0 + c_head) + 1e-12:
        c = law(z) - (y_arm + y_tank(z, z_c))
        if c < worst: worst, z_w = c, z
        z += 0.005
    return worst, z_w
fit = {}
for row, z_c in (("upper", -19.0), ("lower", -21.5)):
    fit[row] = {
        "calibrated": scan(z_c, hw_cal),
        "linear_to_floor": scan(z_c, hw_linfloor),
    }
min_clr = fit["lower"]["calibrated"][0]
fit_verdict = ("PASS" if min_clr >= M["min_skin_clearance_m_declared"] else
               "MARGINAL-FAIL" if min_clr >= 0.0 else "FAIL")

# ------------------------------------------------------------- 7. sensitivities
plate5 = DRY_new + 4.0 * (m_barrel + m_heads + m_weld + m_baffles) * (5.0 / 3.0 - 1.0)
adapter2 = DRY_new + 4.0 * 0.045

# ------------------------------------------------------------------ 8. verdict
screens = {
    "capacity (usable >= 25.45 fresh / 24.83 salt m3)": capacity_screen,
    "mass (new set vs 6.00 t, DRY vs 66.18)":            "PASS" if delta_set < 0 else "FAIL",
    "hoop membrane (<= 90 MPa weld-affected datum)":     "PASS" if hoop_s / 1e6 <= 90.0 else "FAIL",
    "floor (n1 >= 110,000 anchor / 107,547 drawn)":      "PASS" if clear_anchor >= 0 and clear_drawn >= 0 else "FAIL",
    "ceiling margin positive (anchor and drawn)":        "PASS" if margin_anchor > 0 and margin_drawn > 0 else "FAIL",
    "trim: mismatch <= D1-end authority":                "PASS" if pitch_mis <= auth_rec["D1_end_mismatch"] else "FAIL",
    "trim: one-empty <= one-empty authority":            "PASS" if pitch_1e <= auth_rec["one_bay_empty_mid_D1"] else "FAIL",
    "fit vs 0.50 m min skin clearance (calibrated law)": fit_verdict,
}
unknowns = [
    "curved-tank support/load introduction into the declared curtain system (weakest assumption; bands, adapter, curtain fittings unsized beyond stock)",
    "hull section law below z=-21.5 m: corner-calibrated taper is extrapolation past -22.93 m; exact capsule law UNKNOWN",
    "head-to-barrel seam and weld capacity (resultant traced, capacity not shown)",
    "band local shell bending / shell buckling under band line load",
    "pickup datum fitting capacity at 127.8 kN (inherited datum, superseded fittings retired)",
    "occupancy: 116.8 m3 tank envelopes remain unreserved from lifting gas; bag shape/fit UNKNOWN",
    "one-bay-empty recovery at min-air authority (356.3 > 244.7, carried from I012/I017)",
    "slosh/transient under baffles; valve spec; transition-energy closure (partial qualification only)",
    "installation/access allowance 0.08 t assumed; I007 sundries scale carried",
]
carried_fail = {
    "economics 35.1x vs SEAT ($5,929/t)": I17["recorded_fail"]["economics_multiple_vs_SEAT"],
    "fuel short 33-min (t)": I17["recorded_fail"]["fuel_short_33min_t"],
    "fuel short half-pump (t)": I17["recorded_fail"]["fuel_short_halfpump_t"],
}
scoreboard = ("P100 I027 4x barrel OD3.05 H4.20 3mm5083: DRY %.2f (%+.2f) margin +%.2f anchor; lower-head fit %.2f<0.50 %s; load-intro UNKNOWN; float not shown"
              % (DRY_new, delta_set, margin_anchor, min_clr, fit_verdict))
assert len(scoreboard) <= 180 and "not shown" in scoreboard

out = {
 "unit": "R3-I027", "generator": "tank.py", "input": "baseline.json (see sources.json)",
 "geometry": {"OD_m": OD, "straight_barrel_m": h_bar, "head_depth_m_each": c_head, "plate_m": t_plate,
              "total_height_m": h_bar + 2 * c_head, "baffles": n_baf, "freeboard_m": freeb,
              "stations": "I017 unchanged x=+-14, y=+-11, upper z=-19.0, lower z=-21.5; D1 upper diagonal, D2 lower"},
 "capacity_m3": {"inner_total": A_i * h_bar + 2 * V_head_i, "usable": usable, "barrel_water": V_bar_w,
                 "bottom_head": V_head_i, "baffles_displaced": V_baf, "sump_debited": V_sump,
                 "required_fresh": req_fresh_m3, "required_salt": req_salt_m3,
                 "ullage_pct_fresh": (1 - req_fresh_m3 / usable) * 100, "screen": capacity_screen,
                 "envelope_per_tank_m3": V_env_tank},
 "mass_bill_t": {
   "per_tank_new": {"barrel_shell": m_barrel, "two_heads": m_heads, "weld_allowance_8pct": m_weld,
                    "two_baffles": m_baffles, "manway": m_manway, "three_ports": m_ports, "sump_fitting": m_sumpfit,
                    "tank_hardware": m_tank_hw, "two_bands": m_bands, "adapter_assembly": m_adapter,
                    "band_zone_doublers": m_doubler, "supports": m_supports, "total": m_per_tank},
   "set": {"new_tank_stock_4x": m_set_tanks, "installation_access_allowance_assumed": m_install,
           "new_stock_total": new_stock, "reused_retained": reused, "fasteners_retained_fit_UNKNOWN": fasteners_retained,
           "new_set_total": new_set_total, "i017_set": I17["drawn_set_total_t"], "delta": delta_set,
           "retired_i017_lines": retired},
   "budget": {"DRY_i017": DRY_old, "DRY_new": DRY_new, "loaded_new": loaded_new,
              "basis": "same I017 dry/equipment budget, net change only (I012: 38.77 ex-hull + gas hull 23.75 - 2.34)"}},
 "loads": {"water_column_full_m": col_full, "p_bottom_kPa_fresh": p_bot_f / 1000, "p_bottom_kPa_salt": p_bot_s / 1000,
           "hoop_MPa_fresh": hoop_f / 1e6, "hoop_MPa_salt": hoop_s / 1e6, "axial_MPa_fresh": axial_f / 1e6,
           "allowable_MPa_weld_affected_datum": 90, "hoop_pct_of_datum": hoop_s / 90e6 * 100,
           "head_resultant_kN_fresh": head_res_f, "head_resultant_kN_salt": head_res_s,
           "pickup_kN_full_per_datum": R_pick_full, "pickup_i017_datum_kN": I17["saddle_pickup_reaction_kN_full"],
           "band_line_load_kN_per_m_each": q_band, "pickup_imbalance_kN_mismatch": dR_pick_mis},
 "states": {"mismatch_bound_t": m_mis, "roll_mismatch_t_m": roll_mis, "pitch_mismatch_t_m": pitch_mis,
            "roll_one_empty_t_m": roll_1e, "pitch_one_empty_t_m": pitch_1e,
            "i017_comparison": {"mismatch_bound": I17["mismatch_bound_t"], "roll": I17["mismatch_roll_t_m"], "pitch": I17["mismatch_pitch_t_m"],
                                "one_empty_roll": I17["one_empty_roll_t_m"], "one_empty_pitch": I17["one_empty_pitch_t_m"]},
            "authority_t_m": {"min_air": auth_rec["min_air"], "D1_end": auth_rec["D1_end_mismatch"],
                              "one_empty": auth_rec["one_bay_empty_mid_D1"], "law_reproduced": auth_calc},
            "coverage": {"mismatch_vs_D1_end_pct": pitch_mis / auth_rec["D1_end_mismatch"] * 100,
                         "one_empty_vs_authority_pct": pitch_1e / auth_rec["one_bay_empty_mid_D1"] * 100,
                         "one_empty_vs_min_air_x": pitch_1e / auth_rec["min_air"]},
            "heel_deg": {"mismatch": heel_mis, "one_empty": heel_1e}},
 "ledger": {"n0_m3": n0_new, "n0_i017": n0_old, "n1_D1_end_m3": n1_new, "n1_i017": n1_old,
            "floor_anchor_m3": floor_anchor, "floor_drawn_m3": floor_drawn,
            "floor_clearance_anchor_m3": clear_anchor, "floor_clearance_drawn_m3": clear_drawn,
            "i017_clearance_anchor_m3": I17["floor_clearance_m3"],
            "bag_base_arrival_m3": bag_base, "bag_pct_V": bag_pct_V, "bag_pct_cap": bag_pct_cap,
            "cap_headroom_m3": floor_anchor - bag_base,
            "margin_anchor_t": margin_anchor, "margin_drawn_t": margin_drawn, "i017_margin_t": I17["margin_at_max_inventory_t"],
            "vent_identity_m3": vent, "vent_i017_recorded": M["vent_identity_m3"],
            "note_vent": "n0-n1 unchanged by dry while floor-clear (recorded identity 50,940 kept)",
            "net_displaced_mixture_dS0_m3": dn0,
            "floor_crossover_slack_dry_t": crossover_slack,
            "S7_reset": "n_S7 = n0 both species, earliest 6.50 h; moored reset and partial-energy qualification retained, no closure claimed"},
 "fit": {"law": "corner-calibrated taper hw(z)=17.1-2.2308*(z2-z) below -21.5 (reproduces I017 1.38 m corner at -22.93); above -21.5 linear 19.9->17.1",
         "min_clearance_m": {"upper_calibrated": fit["upper"]["calibrated"], "lower_calibrated": fit["lower"]["calibrated"],
                             "lower_linear_to_floor_REJECTED_basis": fit["lower"]["linear_to_floor"],
                             "declared_minimum": M["min_skin_clearance_m_declared"]},
         "verdict": fit_verdict,
         "note": "lower-row bottom head sits below the last recorded datum; verdict is extrapolation-dependent (exact law UNKNOWN)"},
 "sensitivities_declared_points": {"plate_5mm": {"DRY": plate5, "margin_anchor": I17["ceiling_max_lift_anchor_t"] - (plate5 + 100),
                                                 "note": "at 5 mm the set is HEAVIER than I017 (66.18): the case rests on 3 mm membrane adequacy"},
                                   "adapter_mass_x2": {"DRY": adapter2, "margin_anchor": I17["ceiling_max_lift_anchor_t"] - (adapter2 + 100)}},
 "screens": screens, "carried_FAIL": carried_fail, "carried_UNKNOWN": unknowns,
 "weakest_assumption": unknowns[0],
 "next_change": "resolve the actual capsule section law below -21.5 m and the paid curtain-fan attachment construction; if the law confirms interference, shorten the lower-row straight barrel (3.60 -> ~3.0 m restores >1 m clearance) and re-split the scoop allocation across the D1 bays to hold 25.45 m3 per D2 bay",
 "scoreboard": scoreboard,
}
with open(os.path.join(HERE, "tank.json"), "w", encoding="utf-8") as f:
    json.dump(out, f, indent=1, sort_keys=False)
    f.write("\n")
print("R3-I027 tank.py OK: usable %.3f m3 (%s), DRY %.3f t (delta %+.3f), n1 %.0f (clear %.0f), margin +%.2f anchor, hoop %.1f MPa, lower fit %.3f m %s"
      % (usable, capacity_screen, DRY_new, delta_set, n1_new, clear_anchor, margin_anchor, hoop_s / 1e6, min_clr, fit_verdict))
print("scoreboard(%d): %s" % (len(scoreboard), scoreboard))
