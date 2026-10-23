#!/usr/bin/env python3
# MAINLINE-016: secondary needs-further-investigation rows, at the MAINLINE-009 P2 point.
# Own arithmetic, own script. Every number traces to an input and a formula stated here.
# Tags: QUESTIONABLE = inherited or sourced value; PROJECTION = does not exist today.
import json, math, datetime

started_at = "2026-10-19T23:37:00-07:00"

# ---------- pinned case (COMMON.md, MAINLINE-009 RESULTS.json) ----------
R = 10.0                          # m, external radius
p_ext = 95460.83791390515         # Pa, 500 m ISA
T_air = 284.9                     # K
rho_air = 1.1672683307461802      # kg/m3
V = 4.0/3.0*math.pi*R**3         # displaced volume, m3
lift = 4889.442150186961          # kg, lift-equivalent mass
A = 4*math.pi*R**2                # shell surface area, m3
tf = 0.00027215364631557974       # m, each SiC face (009)
tc = 0.04624190488644608          # m, H35 core (009)
h_sep = tf + tc                   # m, face separation (009: 0.04651405853276166)
E_SiC = 410e9                     # Pa, QUESTIONABLE MatWeb alpha SiC (009 face_source)
rho_SiC = 3100.0                  # kg/m3, QUESTIONABLE MatWeb alpha SiC (009)
sig_c_SiC = 3900e6                # Pa, QUESTIONABLE Saint-Gobain Hexoloy SA (009)
nu = 0.33                         # carried case value (009)
mass_faces = 2120.3898218634963   # kg (009)
mass_core = 2208.1530759247057    # kg (009)
mass_joints_allow = 216.4271448894101  # kg, the 5% allowance (009)
mass_systems = 100.0              # kg (009)
total_mass = 4644.970042677613    # kg (009)
margin_kg = 244.47210750934846    # kg, 5% of lift (009)
SF = {                            # 009 modes at knockdown 0.20 (pinned numbers, not recomputed)
 "global_buckling": 0.23515931324953654, "face_compression": 4.4474749806324665,
 "core_crush": 10.475499920730703, "core_shear_crimping": 1.1763017784546326,
 "face_wrinkling": 0.23516798404427022}
least_SF = SF["global_buckling"]
sig_m = p_ext*R/(4*tf)            # Pa, membrane stress at external pressure (003 formula pR/(4 tf))
sig_crush_core = p_ext/2.0        # Pa, core stress at p_ext (005b model, core stress = p/2)
sig_core_allow = SF["core_crush"]*sig_crush_core  # Pa, H35 compressive strength backed out of 009/005b

# ---------- gas constants and air properties (CODATA / Incropera at 285 K) ----------
R_air = 287.05                    # J/(kg K), QUESTIONABLE textbook
M_air = 0.02897                   # kg/mol
gam = 1.4
mu_air = 1.79e-5                  # Pa s, Incropera, QUESTIONABLE
k_air = 0.0257                    # W/(m K), Incropera, QUESTIONABLE
Pr_air = 0.71
R_v = 461.5                       # J/(kg K) water vapor

# ---------- item 1: holding the vacuum ----------
# (c) 1% lift loss per day allowance
lift_1pct = 0.01*lift                                     # kg
m_air_inside = lift_1pct                                  # kg of air inside at 1% loss (lift loss = rho_i*V)
p_int_1pct = 0.01*p_ext                                   # Pa, isothermal same gas: rho_i/rho_air = p_i/p_ext
Q_allow = V*p_int_1pct/86400.0                            # Pa m3/s throughput to reach it in a day
m_rate_allow = lift_1pct/86400.0                          # kg/s
# choked inflow at p_i ~ 0 (standard gas dynamics; ideal thin hole)
flux_choked = p_ext*math.sqrt(gam/(R_air*T_air))*(2/(gam+1))**((gam+1)/(2*(gam-1)))
A_choked_eq = m_rate_allow/flux_choked                    # m2, equivalent choked hole
# molecular effusion thin aperture: Q = (1/4)*p*vbar*A
vbar = math.sqrt(8*R_air*T_air/math.pi)  # sqrt(8 R_u T/(pi M)) == sqrt(8 R_specific T/pi)
C_mol_area = 0.25*vbar                                    # m3/(s m2) conductance per area
A_mol_eq = Q_allow/(C_mol_area*p_ext)                     # m2 (driving p ~ p_ext while p_i ~ 0)

# (a) permeation through faces
# CFRP He permeance 1e-6..1e-5 scc/(m2 s) at 1 atm, QUESTIONABLE NASA composite-cryotank literature
# (Grimsley/Cano class); air through epoxy ~ 50x lower than He, QUESTIONABLE.
scc_mol = 1.0/22414.0                                     # mol per scc
perm_cfrp_band = [(1e-6*scc_mol/101325.0)/50.0, (1e-5*scc_mol/101325.0)/50.0]  # mol/(m2 s Pa)
perm_rows = []
for name, band, note in [
    ("metal_foil_6061", [0.0, 0.0], "N2/O2 solution-diffusion through Al at 285-400 K is nil for barrier purposes (textbook; Ashby)"),
    ("monolithic_SiC", [0.0, 0.0], "sintered >98% dense alpha SiC has no connected porosity; used as a gas barrier (datasheet class)"),
    ("CFRP_quasi_isotropic_epoxy", perm_cfrp_band, "QUESTIONABLE NASA composite cryotank He permeance band /50 for air")]:
    row = {"face": name, "note": note,
           "kg_per_day": [band[0]*A*p_ext*M_air*86400.0, band[1]*A*p_ext*M_air*86400.0]}
    row["pct_of_1pct_budget"] = [100.0*x/lift_1pct for x in row["kg_per_day"]]
    perm_rows.append(row)

# (d) outgassing (interior surfaces: inner face + seam edges), QUESTIONABLE O'Hanlon polymer band
q_og_band = [1e-7, 1e-5]                                  # Pa m3/(s m2)
Q_og = [q_og_band[0]*A, q_og_band[1]*A]                   # Pa m3/s
og_pct_of_budget = [100.0*x/Q_allow for x in Q_og]
# moisture resident in the PVC foam: 0.5..3% of core mass, QUESTIONABLE PVC foam data
moist_band = [0.005*mass_core, 0.03*mass_core]             # kg
p_moist = [m*R_v*T_air/V for m in moist_band]              # Pa if fully released to the void

# (e) pump to hold an internal ceiling
p_ceiling = 1000.0                                        # Pa operational ceiling, owner assumption
vdot_at_ceiling = Q_allow/p_ceiling                       # m3/s volumetric at the ceiling
W_ideal = Q_allow*math.log(p_ext/p_ceiling)               # W isothermal ideal
eff_band = [0.25, 0.40]                                   # QUESTIONABLE Roots+backing wire class
W_real = [W_ideal/eff_band[0], W_ideal/eff_band[1]]
pump_mass_band = [150.0, 400.0]                           # kg QUESTIONABLE catalog class (Roots/screw + backing)
pump_pct_margin = [100.0*x/margin_kg for x in pump_mass_band]

# ---------- item 2: joints and seams ----------
# square panels width w: N = A/w^2 panels, shared seam length L = N*4w/2 = 2A/w
scenarios = [
 ("w4_PROJECTION", 4.0, "4 m panels: no SiC face panel this size exists today (PROJECTION)"),
 ("w2_PROJECTION", 2.0, "2 m panels: standard for Al sheet today, PROJECTION for SiC"),
 ("w0p5_today", 0.5, "0.5 m: Saint-Gobain Hexoloy SA plate size today, QUESTIONABLE"),
 ("w0p25_conservative", 0.25, "0.25 m tiles: conservative producible today, QUESTIONABLE")]
b_doubler = [0.06, 0.12]                                  # m doubler width, optimistic/conservative
t_adh = [0.0002, 0.0003]                                  # m adhesive film
t_splice = [0.0015, 0.0030]                               # m core splice paste
rho_adh = 1250.0; rho_paste = 1100.0                      # QUESTIONABLE epoxy film / paste
seam_rows = []
for name, w, note in scenarios:
    L = 2*A/w
    for i, tagv in enumerate(["optimistic", "conservative"]):
        m_doubler = L*b_doubler[i]*tf*rho_SiC
        m_adh = L*b_doubler[i]*t_adh[i]*rho_adh
        m_splice = L*tc*t_splice[i]*rho_paste
        tot = m_doubler + m_adh + m_splice
        seam_rows.append({"scenario": name, "panel_w_m": w, "bound": tagv, "seam_length_m": L,
            "doubler_kg": m_doubler, "adhesive_kg": m_adh, "core_splice_kg": m_splice,
            "total_kg": tot, "pct_of_5pct_allowance": 100.0*tot/mass_joints_allow,
            "margin_after_kg": margin_kg - (tot - mass_joints_allow), "note": note})

# ---------- item 3: thermal ----------
S_sol = 970.0                                             # W/m2 clear-sky at 500 m, QUESTIONABLE ASHRAE class
sig_SB = 5.670374419e-8
T_sky_day = 275.0; T_sky_night = 260.0                    # K, QUESTIONABLE atmospheric radiation (Bliss class)
coat = {"coated": (0.20, 0.90), "bare_SiC": (0.70, 0.85)} # QUESTIONABLE thermal-control handbook bands
def h_conv(vwind):
    Re = rho_air*vwind*(2*R)/mu_air
    Nu = 2 + (0.4*Re**0.5 + 0.06*Re**(2.0/3.0))*Pr_air**0.4   # Whitaker sphere, Incropera
    return Nu*k_air/(2*R)
def solve_Tface(alpha, eps, vwind, S, T_sky):
    T_env = 0.5*(T_sky + T_air)
    def resid(T):
        return alpha*S*math.pi*R**2 - eps*sig_SB*(T**4 - T_env**4)*4*math.pi*R**2 \
               - h_conv(vwind)*(T - T_air)*4*math.pi*R**2
    lo, hi = 200.0, 500.0
    for _ in range(200):
        mid = 0.5*(lo+hi)
        if resid(mid) > 0: lo = mid
        else: hi = mid
    return 0.5*(lo+hi)
thermal_env = []
for cname, (al, ep) in coat.items():
    for vwind, wl in [(2.0, "wind 2 m/s"), (10.0, "wind 10 m/s")]:
        Td = solve_Tface(al, ep, vwind, S_sol, T_sky_day)
        Tn = solve_Tface(al, ep, vwind, 0.0, T_sky_night)
        thermal_env.append({"case": cname+" "+wl, "T_face_day_K": Td, "T_face_night_K": Tn,
            "dT_day_K": Td - T_air, "dT_night_K": Tn - T_air})
# radiative-only bound (no convection) worst case, bare in full sun
T_rad_bound = solve_Tface(0.70, 0.85, 1e-9, S_sol, T_sky_day)
# core through-thickness time constant
a_core = 0.030/(38.0*1300.0)                              # m2/s, k=0.030 rho=38 cp=1300 QUESTIONABLE DIAB class
tau_core = tc**2/(math.pi**2*a_core)
# CTE mismatch face/core: sandwich shear-lag (Zenkert, Handbook of Sandwich Construction)
alpha_SiC = 4.5e-6                                        # 1/K QUESTIONABLE MatWeb alpha SiC
alpha_PVC = 60e-6                                         # 1/K QUESTIONABLE PVC foam class
Gc_H35 = 12e6                                             # Pa QUESTIONABLE DIAB H35 nominal shear modulus
lam = math.sqrt(Gc_H35/(E_SiC*tf*tc))                     # 1/m
tau_strength_H35 = [0.40e6, 0.55e6]                       # Pa QUESTIONABLE DIAB H35 shear strength band
cte_rows = []
for dT in [10.0, 30.0, 60.0]:
    d_eps = (alpha_PVC - alpha_SiC)*dT
    tau_max = d_eps*E_SiC*tf*lam
    cte_rows.append({"dT_face_core_K": dT, "differential_strain": d_eps,
        "tau_max_Pa": tau_max, "SF_vs_0p40MPa": 0.40e6/tau_max, "SF_vs_0p55MPa": 0.55e6/tau_max})
# thermal geometric imperfection, top-bottom asymmetry dT_v
therm_imperfection = [{"dT_vertical_K": dTv, "w_thermal_m": alpha_SiC*dTv*R/2}
                      for dTv in [5.0, 10.0, 20.0]]
# property loss: H35 service temperature
core_limit_K = [343.0, 353.0]                             # 70-80 C QUESTIONABLE DIAB H series

# ---------- item 4: loads beyond uniform pressure ----------
weather = []
for name, dp in [("diurnal_1hPa", 100.0), ("synoptic_3pct", 0.03*p_ext), ("extreme_storm_low_10pct", -0.10*p_ext)]:
    p_case = p_ext + dp
    weather.append({"case": name, "p_case_Pa": p_case, "pct_of_p_ext": 100.0*dp/p_ext,
        "crush_SF_at_case": least_SF*p_ext/p_case, "lift_margin_kg_at_case": margin_kg*p_case/p_ext})
v_gust = 20.0
q_dyn = 0.5*rho_air*v_gust**2                             # Pa
F_drag = 0.47*q_dyn*math.pi*R**2                          # N, Cd sphere 0.47 textbook
gust_factor = 1.4                                         # QUESTIONABLE ASCE class
F_mooring = F_drag*gust_factor
A_patch = 0.0707                                          # m2 hardpoint patch r=0.15 m, owner assumption
p_patch = F_mooring/A_patch
SF_patch = sig_core_allow/p_patch
A_spread_needed = F_mooring/(sig_core_allow/1.5)          # m2 spreader at SF 1.5 on core
fitting_mass_est = 6*8.0                                  # kg 6 hardpoints x 8 kg, owner assumption
virt_mass = 0.5*rho_air*V                                 # kg added air mass, potential flow
# ground handling: distributed cradle contact pressure target
p_cradle_ok = 250e3                                       # Pa target <= half core strength, owner assumption

# ---------- item 5: altitude and climate (ideal gas; MAINLINE-012 unfiled, derived here) ----------
# rho = p/(R_air*T) => dL/L = dp/p - dT/T at fixed V (500 m fixed altitude case)
climate = []
for name, dT, dp in [("hot_summer_afternoon", 25.1, 0.0), ("cold_winter_dawn", -11.9, 0.0),
                     ("synoptic_high_2pct", 0.0, 0.02*p_ext), ("synoptic_low_2pct", 0.0, -0.02*p_ext)]:
    dLL = dp/p_ext - dT/T_air
    climate.append({"case": name, "dT_K": dT, "dp_Pa": dp, "dL_over_L": dLL,
        "lift_kg": lift*(1.0+dLL), "margin_kg": margin_kg + lift*dLL})
water_rows = []
for film_mm in [0.1, 1.0]:
    m_film = A*film_mm*1e-3*1000.0
    water_rows.append({"film_mm": film_mm, "mass_kg": m_film, "pct_of_margin": 100.0*m_film/margin_kg})

# ---------- checks ----------
checks = {
 "membrane_stress_vs_009_face_SF": "PASS" if abs(sig_c_SiC/SF["face_compression"]/sig_m - 1) < 1e-3 else "FAIL",
 "core_allow_backout_vs_crush": "PASS" if abs(sig_core_allow/1e6 - 0.500) < 0.005 else "FAIL",
 "volume_and_area": "PASS" if abs(V - 4188.7902047863905) < 1e-6 and abs(A - 1256.6370614359173) < 1e-6 else "FAIL",
 "separation": "PASS" if abs(h_sep - 0.04651405853276166) < 1e-12 else "FAIL",
}

results = {
 "schema": 1, "card": "MAINLINE-016", "unit": "ref-81587374594cae9c1e2e-nfi-1019",
 "status": "ESTIMATE", "tag": "QUESTIONABLE", "certification": "none",
 "started_at": started_at,
 "base_point": {"report": "rpt-ref-d5b4aaa267b71d82fe25",
   "R_m": R, "tf_m": tf, "core_m": tc, "A_m2": A, "V_m3": V, "p_ext_Pa": p_ext, "T_K": T_air,
   "rho_air": rho_air, "lift_kg": lift, "margin_kg": margin_kg,
   "least_SF_main": least_SF, "modes_main_kd_0_20": SF,
   "membrane_stress_MPa": sig_m/1e6, "core_stress_at_ext_MPa": sig_crush_core/1e6,
   "H35_compressive_allow_MPa_backed_out": sig_core_allow/1e6},
 "item1_vacuum": {
   "lift_1pct_kg_per_day": lift_1pct, "p_int_at_1pct_Pa": p_int_1pct,
   "Q_allow_Pa_m3_s": Q_allow, "m_rate_allow_kg_s": m_rate_allow,
   "A_choked_equivalent_mm2": A_choked_eq*1e6, "A_molecular_equivalent_mm2": A_mol_eq*1e6,
   "choked_flux_kg_s_m2": flux_choked,
   "permeation": perm_rows,
   "outgassing_Q_Pa_m3_s": Q_og, "outgassing_pct_of_budget": og_pct_of_budget,
   "moisture_kg_band": moist_band, "moisture_pressure_if_released_Pa": p_moist,
   "deploy_pumpdown_kWh": p_ext*V*math.log(p_ext/p_ceiling)/3.6e6,
   "pump": {"ceiling_Pa": p_ceiling, "vdot_m3_s": vdot_at_ceiling,
            "W_ideal": W_ideal, "W_real_band_W": W_real, "mass_band_kg": pump_mass_band,
            "pct_of_margin": pump_pct_margin}},
 "item2_seams": seam_rows,
 "item3_thermal": {
   "environment": thermal_env,
   "T_rad_only_bound_K": T_rad_bound,
   "core_tau_s": tau_core,
   "cte_mismatch_shear_lag": {"lambda_per_m": lam, "rows": cte_rows},
   "thermal_imperfection": therm_imperfection,
   "core_service_limit_K": core_limit_K},
 "item4_loads": {
   "weather": weather,
   "gust": {"v_m_s": v_gust, "q_Pa": q_dyn, "q_pct_of_p_ext": 100*q_dyn/p_ext,
            "F_drag_N": F_drag, "F_mooring_N": F_mooring,
            "patch_p_kPa": p_patch/1e3, "SF_patch": SF_patch,
            "spreader_m2_needed": A_spread_needed, "fittings_est_kg": fitting_mass_est,
            "added_air_mass_kg": virt_mass, "cradle_target_kPa": p_cradle_ok/1e3}},
 "item5_climate": {"law": "rho = p/(R_air*T); dL/L = dp/p - dT/T at fixed V; MAINLINE-012 unfiled, derived",
   "rows": climate, "surface_water": water_rows},
 "checks": checks,
}
ended_at = datetime.datetime.now().astimezone().isoformat()
results["ended_at"] = ended_at
with open("RESULTS.json", "w") as f:
    json.dump(results, f, indent=1)
print("checks:", checks)
print("Q_allow %.2f Pa m3/s | choked %.2f mm2 | molecular %.2f mm2" % (Q_allow, A_choked_eq*1e6, A_mol_eq*1e6))
print("perm CFRP pct budget:", perm_rows[2]["pct_of_1pct_budget"])
print("pump: ideal %.0f W real %.0f-%.0f W mass %g-%g kg (%.0f-%.0f%% margin)" % (W_ideal, W_real[0], W_real[1], pump_mass_band[0], pump_mass_band[1], pump_pct_margin[0], pump_pct_margin[1]))
for r in seam_rows: print("seam %-22s %-12s L=%7.0f m tot=%8.1f kg %6.0f%% of allowance" % (r["scenario"], r["bound"], r["seam_length_m"], r["total_kg"], r["pct_of_5pct_allowance"]))
print("thermal env:")
for t in thermal_env: print("  %-28s day %.1f K (%+.1f) night %.1f K (%+.1f)" % (t["case"], t["T_face_day_K"], t["dT_day_K"], t["T_face_night_K"], t["dT_night_K"]))
print("rad-only bound %.1f K | core tau %.0f s" % (T_rad_bound, tau_core))
for c in cte_rows: print("cte dT=%4.0f K tau=%6.0f kPa SF(0.40)=%.2f SF(0.55)=%.2f" % (c["dT_face_core_K"], c["tau_max_Pa"]/1e3, c["SF_vs_0p40MPa"], c["SF_vs_0p55MPa"]))
print("imperfection:", [(r["dT_vertical_K"], round(r["w_thermal_m"]*1e3,3)) for r in therm_imperfection], "mm")
print("gust: q=%.0f Pa F_moor=%.0f N patch %.0f kPa SF=%.2f spreader %.3f m2" % (q_dyn, F_mooring, p_patch/1e3, SF_patch, A_spread_needed))
for c in climate: print("climate %-24s dL/L %+.4f margin %8.1f kg" % (c["case"], c["dL_over_L"], c["margin_kg"]))
for w in water_rows: print("water %.1f mm -> %.0f kg (%.0f%% margin)" % (w["film_mm"], w["mass_kg"], w["pct_of_margin"]))
print("outgassing pct budget: %.2f-%.2f | moisture p: %.0f-%.0f Pa vs 1%% ceiling %.0f Pa" % (og_pct_of_budget[0], og_pct_of_budget[1], p_moist[0], p_moist[1], p_int_1pct))
