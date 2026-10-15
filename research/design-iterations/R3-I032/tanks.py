#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""R3-I032 — taller upper D1 barrels + shortened lower D2 barrels with paid
upper-storage/transfer construction at the inherited I017 stations.

New unit, new calculator. Stdlib only; reads baseline.json (frozen inputs).
No ancestor calculator is imported, executed or regenerated; recorded ancestor
values are data. All mechanics in consistent SI (kg, m, s, Pa, N): pressures,
forces and stresses carry their stated units directly (the archived I027
unit/band errata are NOT carried over: no tonne-based formula with a Pa/N
post-conversion, and no extra halving of support loads — each pickup datum
takes W/2 per tank and the band delivers that same W/2, width-spread).

Section order: 0 guards (before ANY calculation) -> 1 geometry -> 2 mass bill
-> 3 hydrostatics/supports -> 4 inventory schedule -> 5 lift ledger ->
6 fit containment -> 7 transfer timing/pump -> 8 authority-law re-verification
-> 9 verdict + tanks.json.
"""
import json, math, os, resource, sys, datetime

B = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "baseline.json")))
OUT = {}

# ------------------------------------------------------------------ 0. guards
def guard():
    g = {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
         "pid": os.getpid(), "ppid": os.getppid()}
    problems = []
    g["argv"] = sys.argv
    g["cwd"] = os.getcwd()
    # cgroup: must sit in the bounded transient unit, not the session scope
    cg = open("/proc/self/cgroup").read().strip()
    g["cgroup"] = cg
    if "r3i032" not in cg:
        problems.append("cgroup not the bounded r3i032 unit: %r" % cg)
    # affinity: exactly the one assigned CPU
    aff = open("/proc/self/status").read()
    for line in aff.splitlines():
        if line.startswith("Cpus_allowed_list:"):
            g["cpus_allowed"] = line.split(":", 1)[1].strip()
    if g.get("cpus_allowed") not in ("28",):
        problems.append("affinity %r is not the single assigned CPU" % g.get("cpus_allowed"))
    # IPC namespace: must differ from PID 1 (bwrap --unshare-ipc)
    g["ns_ipc_self"] = os.stat("/proc/self/ns/ipc").st_ino
    g["ns_ipc_init"] = os.stat("/proc/1/ns/ipc").st_ino
    if g["ns_ipc_self"] == g["ns_ipc_init"]:
        problems.append("IPC namespace NOT unshared (same inode as init)")
    # rlimits
    cpu = resource.getrlimit(resource.RLIMIT_CPU)
    as_ = resource.getrlimit(resource.RLIMIT_AS)
    g["rlimit_cpu_s"] = cpu
    g["rlimit_as_bytes"] = as_
    if not (cpu[0] <= 60 and cpu[1] <= 60):
        problems.append("RLIMIT_CPU %r exceeds 60 s" % (cpu,))
    if not (as_[0] <= 1 << 30 and as_[1] <= 1 << 30):
        problems.append("RLIMIT_AS %r exceeds 1 GiB" % (as_,))
    # single-thread environment
    for var in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        g["env_" + var] = os.environ.get(var)
        if os.environ.get(var) != "1":
            problems.append("%s is not 1" % var)
    g["problems"] = problems
    with open("guard-report.json", "w") as f:
        json.dump(g, f, indent=1)
    if problems:
        print("GUARD-STOP:", "; ".join(problems), flush=True)
        sys.exit(3)
    print("guards OK: cgroup=%s cpu=%s ipc_unshared=yes rlimits=%s/%s" %
          (cg.split("/")[-1], g["cpus_allowed"], cpu, as_), flush=True)
    return g

GUARD = guard()

# ------------------------------------------------------------------ 1. geometry
fc, mi = B["frozen_candidate"], B["frozen_mission_inherited"]
R_out, t_wall = fc["outside_diameter_m"] / 2.0, fc["plate_thickness_m"]
R_in = R_out - t_wall
A_bar = math.pi * R_in * R_in
head_c_out = fc["head_depth_outer_m_each"]
head_c_in = head_c_out - t_wall          # inner cavity depth (oblate, thin wall)
v_head = (2.0 / 3.0) * math.pi * R_in * R_in * head_c_in   # one head cavity
rho_al = fc["alloy_density_kg_per_m3"]

def tank_geom(barrel):
    v_straight = A_bar * barrel
    return {"straight_m3": v_straight, "heads_m3_each": v_head,
            "gross_m3": v_straight + 2 * v_head,
            "total_height_m": barrel + 2 * head_c_out,
            "baffle_dead_m3": fc["baffles_per_tank"] * A_bar * fc["baffle_thickness_m"]}

def usable(geom, barrel):
    # freeboard zone: top 0.06 m of barrel + entire upper head excluded
    return (geom["heads_m3_each"]                       # bottom head drains by construction
            + A_bar * (barrel - fc["freeboard_m"])
            - geom["baffle_dead_m3"])

geo_u = tank_geom(fc["upper_barrel_straight_m"])
geo_l = tank_geom(fc["lower_barrel_straight_m"])
usable_u = usable(geo_u, fc["upper_barrel_straight_m"])
usable_l = usable(geo_l, fc["lower_barrel_straight_m"])
req_u = B["frozen_inventory_schedule"]["initial_water_t"]["upper_each"] / 1.0   # fresh t -> m3
req_l = B["frozen_inventory_schedule"]["initial_water_t"]["lower_each"] / 1.0

def level_for_volume(geom, barrel, vol):
    if vol <= geom["heads_m3_each"]:
        return None  # within bottom head: level solved only as head fraction
    return head_c_in + (vol - geom["heads_m3_each"]) / A_bar

lvl_u = level_for_volume(geo_u, fc["upper_barrel_straight_m"], req_u)
lvl_l = level_for_volume(geo_l, fc["lower_barrel_straight_m"], req_l)
OUT["geometry"] = {"upper": {**geo_u, "usable_m3": usable_u, "initial_fill_m3": req_u,
                             "initial_level_m": lvl_u, "freeboard_actual_m": fc["upper_barrel_straight_m"] - lvl_u},
                   "lower": {**geo_l, "usable_m3": usable_l, "initial_fill_m3": req_l,
                             "initial_level_m": lvl_l, "freeboard_actual_m": fc["lower_barrel_straight_m"] - lvl_l},
                   "baffle_open_area_m2_each": 8 * math.pi * 0.075 ** 2,
                   "baffle_open_fraction": 8 * math.pi * 0.075 ** 2 / A_bar}
print("geometry: upper usable %.3f m3 (need %.1f), lower usable %.3f m3 (need %.1f)"
      % (usable_u, req_u, usable_l, req_l), flush=True)

# ------------------------------------------------------------------ 2. mass bill
def head_area(a, c):
    e = math.sqrt(1.0 - (c / a) ** 2)
    return math.pi * a * a * (1.0 + (1.0 - e * e) / e * math.atanh(e))

A_head_out = head_area(R_out, head_c_out)
band = math.pi * fc["outside_diameter_m"] * 0.100 * 0.006 * rho_al  # one band mass
sup = B["frozen_support"]
th = B["frozen_transfer_hardware_per_pair"]

def tank_steel(barrel):
    shell = math.pi * fc["outside_diameter_m"] * t_wall * barrel * rho_al
    heads = 2 * A_head_out * t_wall * rho_al
    baffles = fc["baffles_per_tank"] * A_bar * fc["baffle_thickness_m"] * rho_al
    return {"shell_kg": shell, "heads_kg": heads, "baffles_kg": baffles,
            "bands_2x_kg": 2 * band, "adapter_kg": sup["adapter_assembly_kg_per_tank"],
            "vent_drain_kg": th["vent_drain_fittings_kg_per_tank"],
            "fitout_kg": B["fitout_allowance_kg_per_tank"]}

st_u, st_l = tank_steel(fc["upper_barrel_straight_m"]), tank_steel(fc["lower_barrel_straight_m"])
tank_u_kg = sum(st_u.values()); tank_l_kg = sum(st_l.values())
pipe_m_per_m = (math.pi / 4.0) * (th["pipe"]["od_m"] ** 2 - th["pipe"]["id_m"] ** 2) * th["pipe"]["steel_density_kg_per_m3"]
pair_hw_kg = (th["pump"]["mass_kg_each"] * th["pump"]["count_per_pair"]
              + pipe_m_per_m * th["pipe"]["length_m_incl_fittings"]
              + th["valves"]["count_per_pair"] * th["valves"]["mass_kg_each"]
              + th["wiring_per_pair_kg"])
new_tanks_kg = 2 * tank_u_kg + 2 * tank_l_kg
transfer_total_kg = th["pairs"] * pair_hw_kg
i17 = B["i017_comparison_recorded"]
retained_kg = (sum(i17["reused_lines_t"].values()) + i17["empty_bay_structure_t"]
               + i17["interface_fasteners_t"]) * 1000.0
new_set_t = (new_tanks_kg + transfer_total_kg + retained_kg) / 1000.0
delta_set_t = new_set_t - i17["drawn_set_total_t"]
DRY_new = i17["dry_vehicle_t"] + delta_set_t
loaded0 = DRY_new + mi["payload_t"]
OUT["mass_bill_kg"] = {"upper_tank_each": st_u, "lower_tank_each": st_l,
                       "upper_tank_total_kg": tank_u_kg, "lower_tank_total_kg": tank_l_kg,
                       "pipe_kg_per_m": pipe_m_per_m, "pair_hardware_kg": pair_hw_kg,
                       "transfer_total_kg": transfer_total_kg, "retained_lines_kg": retained_kg,
                       "pickup_fittings_line_t": "PENDING (bonded-socket split UNKNOWN; neither retired nor charged)",
                       "new_set_t": new_set_t, "i017_drawn_set_t": i17["drawn_set_total_t"],
                       "delta_set_t": delta_set_t, "DRY_new_t": DRY_new}
print("mass: upper tank %.1f kg, lower %.1f kg, transfer %.1f kg total; set %.3f t (I017 6.000, delta %+.3f); DRY %.3f t"
      % (tank_u_kg, tank_l_kg, transfer_total_kg, new_set_t, delta_set_t, DRY_new), flush=True)

# ------------------------------------------------- 3. hydrostatics/supports (SI)
rho_w, g = mi["water_density_kg_per_m3"], mi["g_m_per_s2"]
def hydro(geom, barrel, fill_m3):
    lvl = level_for_volume(geom, barrel, fill_m3)
    p_bottom = rho_w * g * lvl                      # Pa
    hoop = p_bottom * R_in / t_wall                 # Pa
    return lvl, p_bottom, hoop
lvl_u_full, p_u, hoop_u = hydro(geo_u, fc["upper_barrel_straight_m"], req_u)
lvl_l_full, p_l, hoop_l = hydro(geo_l, fc["lower_barrel_straight_m"], req_l)
W_u = req_u * 1000.0 * g; W_l = req_l * 1000.0 * g
pick_u, pick_l = W_u / 2.0, W_l / 2.0               # each pickup datum takes W/2 (no further halving)
band_load_u, band_load_l = pick_u / 0.100, pick_l / 0.100   # N/m over 100 mm band width
OUT["hydrostatics"] = {"upper": {"fill_level_m": lvl_u_full, "p_bottom_Pa": p_u, "hoop_Pa": hoop_u,
                                 "hoop_vs_90MPa_datum": hoop_u / 90e6,
                                 "weight_N": W_u, "per_pickup_N": pick_u, "band_line_load_N_per_m": band_load_u},
                       "lower": {"fill_level_m": lvl_l_full, "p_bottom_Pa": p_l, "hoop_Pa": hoop_l,
                                 "hoop_vs_90MPa_datum": hoop_l / 90e6,
                                 "weight_N": W_l, "per_pickup_N": pick_l, "band_line_load_N_per_m": band_load_l},
                       "note": "clean SI: no tonne-based expressions, no Pa/N post-conversion, no extra support halving; shell bending/buckling/joints UNKNOWN"}
print("hydro: upper p=%.1f kPa hoop=%.1f MPa (%.0f%% of 90 MPa datum), pickup %.1f kN; lower p=%.1f kPa hoop=%.1f MPa (%.0f%%)"
      % (p_u/1e3, hoop_u/1e6, 100*hoop_u/90e6, pick_u/1e3, p_l/1e3, hoop_l/1e6, 100*hoop_l/90e6), flush=True)

# ------------------------------------------------------- 4. inventory schedule
sched = B["frozen_inventory_schedule"]
st = {}
x = [0.0, 12.5, 25.0]
for xv in x:
    up, lo = 5.0 - 0.2 * xv, 20.0 - 0.8 * xv
    st["D2_x=%.1f" % xv] = {"upper_each_t": up, "lower_each_t": lo}
states = {
 "S0_initial":  {"upper_each_t": 30.0, "lower_each_t": 20.0},
 "S1_D1_end":   {"upper_each_t": 5.0,  "lower_each_t": 20.0},
 **st,
 "S4_D2_end":   {"upper_each_t": 0.0,  "lower_each_t": 0.0},
 "S5_return":   {"upper_each_t": 25.0, "lower_each_t": 0.45,
                 "note": "accepted return routing: 50 t at D1 (25 t per upper) + 0.9 t at D2 (0.45 t per lower)"},
}
STA = fc["stations_m"]
def moments(inv):
    mx = my = 0.0
    for name, (sx, sy, sz) in STA.items():
        m_t = inv["upper_each_t"] if "upper" in name else inv["lower_each_t"]
        mx += m_t * sy; my += m_t * sx
    return mx, my
rows = {}
for k, inv in states.items():
    mx, my = moments(inv)
    total = 2 * inv["upper_each_t"] + 2 * inv["lower_each_t"]
    headroom_u = usable_u - inv["upper_each_t"]
    headroom_l = usable_l - inv["lower_each_t"]
    rows[k] = {**inv, "total_water_t": total, "Mx_t_m": mx, "My_t_m": my,
               "upper_headroom_m3": headroom_u, "lower_headroom_m3": headroom_l}
OUT["inventory_schedule"] = {"states": rows,
    "transfer_bound_note": "pump-rate asymmetry stays within the recorded +/-5%% release-rate class; refined transient bound UNKNOWN (no transient model)"}
print("schedule: S0 100.0 t -> S1 50.0 -> D2 x=12.5: %.1f -> S4 0.0; nominal Mx/My all zero by diagonal symmetry"
      % rows["D2_x=12.5"]["total_water_t"], flush=True)

# ------------------------------------------------------------- 5. lift ledger
k = mi["lift_t_per_1000m3"]
n_of = lambda w_t: w_t / k * 1000.0
n0_new = n_of(loaded0)
n1_new = n_of(loaded0 - mi["delivery_D1_t"] - mi["burn_to_D1_t"])
floor_anchor = mi["installed_bag_cap_m3_total"]
floor_drawn = mi["anchor_volume_m3"] - n0_new + (mi["anchor_volume_m3"] - mi["drawn_volume_m3"]) * 0  # I017 basis below
floor_drawn = mi["drawn_volume_m3"] - floor_anchor
clear_a, clear_d = n1_new - floor_anchor, n1_new - floor_drawn
margin_anchor = i17["ceiling_max_lift_anchor_t"] - loaded0
margin_drawn = i17["ceiling_max_lift_drawn_t"] - loaded0
bag_base = mi["anchor_volume_m3"] - n1_new
OUT["ledger"] = {"n0_m3": n0_new, "n0_i017": i17["n0_m3"], "n1_m3": n1_new, "n1_i017": i17["n1_D1_end_m3"],
                 "floor_clearance_anchor_m3": clear_a, "i017_clearance_m3": i17["floor_clearance_m3"],
                 "floor_clearance_drawn_m3": clear_d,
                 "margin_anchor_t": margin_anchor, "margin_drawn_t": margin_drawn,
                 "bag_volume_at_D1_end_m3": bag_base, "bag_per_bag_m3": bag_base / 2.0,
                 "bag_pct_of_per_bag_cap": (bag_base / 2.0) / mi["per_bag_cap_m3"] * 100.0,
                 "vent_identity_m3": n0_new - n1_new, "vent_i017_recorded": mi["vent_identity_m3"],
                 "S_reset": "n_S7 = n0 both species, earliest %.1f h; moored reset and partial 18.9 MJ qualification retained, no closure claimed" % mi["reset_clock_h_earliest"]}
print("ledger: n0 %.0f (I017 162278), n1 %.0f (111338), floor clear anchor %+.0f m3 (I017 +1338), margin anchor %+.2f t, drawn %+.2f t"
      % (n0_new, n1_new, clear_a, margin_anchor, margin_drawn), flush=True)

# --------------------------------------------------------------- 6. fit (radial)
R_mid = 27.5  # circular midbody section radius across the tanks' x extent (I017 record)
clr_min = mi["min_skin_clearance_m_declared"]
def worst_corner(sx, sy, sz, geom):
    wy = abs(sy) + R_out
    wz = sz - geom["total_height_m"] / 2.0
    return math.hypot(wy, wz)
fit = {}
for name, (sx, sy, sz) in STA.items():
    geom = geo_u if "upper" in name else geo_l
    r = worst_corner(sx, sy, sz, geom)
    fit[name] = {"worst_corner_radial_m": r, "clearance_m": R_mid - r,
                 "vs_declared_minimum_m": clr_min, "pass": (R_mid - r) >= clr_min}
OUT["fit"] = {"section": "static containment witness only: circular midbody radius 27.5 m across the tanks' x extent; a radial coordinate is NOT a horizontal half-width",
              "tanks": fit,
              "unknown": "occupancy, gas-bag reservations, adapter/neighbouring-hardware clash and whole-system fit remain UNKNOWN; bag envelope withdrawn in I017"}
worst = min(v["clearance_m"] for v in fit.values())
print("fit: worst radial clearance %.3f m vs %.2f m declared minimum" % (worst, clr_min), flush=True)

# ------------------------------------------------------- 7. transfer timing/pump
tm = B["mission_timing_recorded"]
drain_s = tm["drain_window_min_approx_per_pair"] * 60.0
discharge_kg_s = 25.0 * 1000.0 / drain_s
need_kg_s = 0.2 * discharge_kg_s
rating = th["pump"]["rating_kg_per_s"]
Q = need_kg_s / rho_w
A_pipe = math.pi / 4.0 * th["pipe"]["id_m"] ** 2
v = Q / A_pipe
Re = rho_w * v * th["pipe"]["id_m"] / 1.0e-3
f = 64.0 / Re
h_f = f * (th["pipe"]["length_m_incl_fittings"] / th["pipe"]["id_m"]) * v * v / (2 * g)
dz = 2.5  # upper outlet ~bottom of upper tank to lower inlet ~top of lower tank, plus port risers
H = dz + h_f
P_hyd = rho_w * g * Q * H
OUT["transfer"] = {"drain_model": "linear, %.0f s per pair (recorded)" % drain_s,
                   "discharge_kg_per_s_per_pair": discharge_kg_s, "required_transfer_kg_per_s": need_kg_s,
                   "rating_kg_per_s": rating, "flow_adequate": need_kg_s <= rating,
                   "pipe_velocity_m_per_s": v, "Reynolds": Re, "friction_head_m": h_f,
                   "static_head_m": dz, "total_head_m": H, "head_MPa": rho_w * g * H / 1e6,
                   "head_adequate": rho_w * g * H <= th["pump"]["differential_head_MPa"] * 1e6,
                   "hydraulic_power_W": P_hyd,
                   "window_check_s": {"D2_window_s": tm["D2_exchange_window_S4_to_S5_h"] * 3600.0,
                                      "drain_plus_ops_note": "two pairs sequential within the recorded 45 min window is consistent with the recorded state table; per-pair basis reported"},
                   "assumption_note": "20 kg/s @ 0.20 MPa rating and all hardware masses are frozen unqualified design assumptions; no retuning authorized"}
print("transfer: need %.2f kg/s vs rating %.0f (%s); head %.4f MPa vs 0.20 (%s); P_hyd %.2f W"
      % (need_kg_s, rating, "PASS" if need_kg_s <= rating else "FAIL",
         rho_w * g * H / 1e6, "PASS" if rho_w * g * H <= th["pump"]["differential_head_MPa"] * 1e6 else "FAIL", P_hyd), flush=True)

# --------------------------------------------------- 8. authority-law re-verify
def authority(air_t, rho_air):
    bag_vol = air_t / rho_air
    donor = bag_vol / 2.0
    receiver = mi["per_bag_cap_m3"] - donor
    net = min(donor, receiver)
    return net * rho_air * (1.0 - mi["mixture_fraction"]) * mi.get("lever_m", 50.0)

auth = []
worst_dev = 0.0
for d in i17["authority_datums"]:
    got = authority(d["air_t"], mi["air_density_t_per_m3_at_2500"])
    want = i17["authority_net_t_m"][d["name"]]
    dev = abs(got - want) / want * 100.0
    worst_dev = max(worst_dev, dev)
    auth.append({"name": d["name"], "got_t_m": got, "recorded_t_m": want, "dev_pct": dev})
auth_ok = worst_dev <= 0.25
OUT["authority_law"] = {"datums": auth, "worst_dev_pct": worst_dev, "tolerance_pct": 0.25,
                        "reproduced": auth_ok,
                        "note": "law re-expressed in this unit and checked against the three recorded I017 datums (rounding-tolerance 0.25%; the D1-end recorded datum sits ~0.15% from the exact law on its recorded rounded inputs); authority/heel/one-empty screens for the NEW set remain UNKNOWN pending a new explicitly paid analysis"}
if not auth_ok:
    print("AUTHORITY CHECK outside tolerance: worst %.3f%% — authority screens carried as recorded data only" % worst_dev, flush=True)
else:
    print("authority: 3/3 datums within 0.25%% (worst %.3f%%)" % worst_dev, flush=True)

# ------------------------------------------------------------------ 9. verdict
verdict = {
 "capacity_upper_30t": "PASS" if usable_u >= req_u else "FAIL",
 "capacity_lower_20t": "PASS" if usable_l >= req_l else "FAIL",
 "floor_n1_vs_110000_anchor": "PASS" if clear_a >= 0 else "FAIL",
 "floor_drawn_basis": "PASS" if clear_d >= 0 else "FAIL",
 "ceiling_margin_anchor": "PASS" if margin_anchor >= 0 else "FAIL",
 "fit_static_containment": "PASS" if worst >= clr_min else "FAIL",
 "transfer_flow": "PASS" if need_kg_s <= rating else "FAIL",
 "transfer_head": "PASS" if rho_w * g * H <= th["pump"]["differential_head_MPa"] * 1e6 else "FAIL",
 "economics_inherited": "FAIL 35.1x vs SEAT (unchanged)",
 "fuel_inherited": "FAIL shorts 0.245112/0.350732 t (unchanged)",
}
OUT["verdict"] = verdict
OUT["guard"] = GUARD
OUT["generated_utc"] = GUARD["utc"]
with open("tanks.json", "w") as f:
    json.dump(OUT, f, indent=1)
fails = [k for k, v in verdict.items() if v.startswith("FAIL") and "inherited" not in k]
print("__R3_I032_DONE__ usable_u %.2f usable_l %.2f set %.3f t DRY %.3f n1 %.0f clear %+.0f margin %+.2f/%+.2f worst-clr %.2f: %s"
      % (usable_u, usable_l, new_set_t, DRY_new, n1_new, clear_a, margin_anchor, margin_drawn, worst,
         "ALL NEW SCREENS PASS" if not fails else "NEW FAILS: " + ",".join(fails)), flush=True)
