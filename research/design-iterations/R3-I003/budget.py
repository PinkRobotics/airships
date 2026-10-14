#!/usr/bin/env python3
"""R3-I003 deterministic arithmetic: gas-supported vs evacuated hull at P-100 scale.

Corrected per ord-spock-glm-a-i003-corrections-1014: the 100 t mission payload
now enters every mission case; the hybrid model removes the full 97/3 mixture,
not helium alone; membrane loading is derived from equilibrium in two labelled
directions with no strength claim; the gas-fill/ballonet schedule is explicit,
with ballonet air budgeted exactly once. Prints every number quoted in
README.md. Pure stdlib, no environment access, no file writes. Anchors: air
densities 1.2250 / 0.9569 kg/m3 (sea level / 2,500 m, the programme's own);
molar-mass lift factors computed, not remembered. Internal, conditional design
hypothesis. No aircraft has been built or flown.
"""

import math

RHO_SL = 1.2250        # kg/m3, programme anchor (float ledger)
RHO_25 = 0.9569        # kg/m3, programme anchor (float ledger)
P_ATM = 101325.0       # Pa
M_AIR, M_HE, M_H2 = 28.9644, 4.0026, 2.016  # g/mol, CODATA standard masses

# P-100 class, sim/config.js and research/analysis/mass-budget.json on afb2c2d1
V = 220_000.0          # m3 displacement (recorded)
HULL_A = 19_007.0      # m2 hull surface (recorded)
PAYLOAD_T = 100.0      # t, class allowance (recorded) - enters every mission case
R_CYL = 27.5           # m, capsule cylindrical radius (110 x 55 m class)

# Recorded vacuum baseline, research/analysis/mass-budget.json P100 cases (t)
SHELL_T = {"floor": 111.76, "credible": 165.0, "demonstrated": 255.2}
BARRIER_T = {"floor": 0.82, "credible": 8.24, "demonstrated": 65.6}
EQUIP_EX_T = {"floor": 103.5, "credible": 293.2, "demonstrated": 787.5}
#   EQUIP_EX_T = everything-but-shell-and-barrier, recomputed from the case
#   lines (their everythingButShellT minus the barrier line). The lines include
#   water tanks and plumbing but NOT the 100 t of water itself.
SHELL_MODEL_KGM3 = {"level-1 lattice (M60J, +nodes+film)": 1.306,
                    "level-2 hierarchy, compression-capped": 1.124}

# Gas-envelope design assumptions (all assumed basis; no coupon exists)
FABRIC_NOM, FABRIC_LO, FABRIC_HI = 0.45, 0.35, 0.65   # kg/m2 hull laminate
BALLONET_FRAC, BALLONET_FABRIC = 0.25, 0.30           # x2 ballonets, kg/m2
SUSPENSION_T, NOSE_T, FINS_T, GONDOLA_T = 3.0, 1.0, 3.0, 4.0  # t allowances
PURITY = 0.97                                          # volume fraction He
SUPERPRESSURE_PA = 500.0                               # nominal gauge
# Float-only (demonstrator systems) additions, t: power, fuel, avionics, ballast
FLOAT_KIT_T = 2.5 + 2.0 + 2.0
# Credible-class cryo plant + LN2 tankage lines (recorded), t - descope lever
DESCOPE_T = 132.4

def mix_frac_mass(purity=PURITY):
    """Mixture-to-air density ratio of a purity-volume He / (1-purity) air fill."""
    return purity * M_HE / M_AIR + (1 - purity)

def net_lift_full(rho):
    """Net lift t, whole hull full of mixture at ambient pressure (zero gauge)."""
    return rho * (1 - mix_frac_mass()) * V / 1000

print("== anchors ==")
print(f"molar-mass lift factors: He/air={M_HE/M_AIR:.5f}  H2/air={M_H2/M_AIR:.5f}")
print(f"mixture density ratio, {PURITY:.0%}/{1-PURITY:.0%} He/air by volume: "
      f"{mix_frac_mass():.6f} of ambient air")
print(f"net lift, hull full of mixture, zero gauge: SL {net_lift_full(RHO_SL):.2f} t"
      f"   2500m {net_lift_full(RHO_25):.2f} t")
print(f"gas-support concession vs vacuum: mixture mass = {mix_frac_mass():.2%} of "
      f"displaced air at any altitude ({RHO_SL*mix_frac_mass()*V/1000:.2f} t at SL, "
      f"{RHO_25*mix_frac_mass()*V/1000:.2f} t at 2500 m, both constituents)")
print(f"hydrogen instead ({PURITY:.0%} purity): "
      f"+{RHO_SL*PURITY*(M_HE-M_H2)/M_AIR*V/1000:.1f} t SL   "
      f"+{RHO_25*PURITY*(M_HE-M_H2)/M_AIR*V/1000:.1f} t at 2500 m")

print("\n== gas hull (Option A) component budget, P-100 envelope ==")
env_nom = HULL_A * FABRIC_NOM / 1000
ball_v = V * BALLONET_FRAC
ball_r = (3 * ball_v / (4 * math.pi)) ** (1/3)
ball_a = 2 * 4 * math.pi * ball_r * ball_r
ball_t = ball_a * BALLONET_FABRIC / 1000
gas_hull = env_nom + ball_t + SUSPENSION_T + NOSE_T + FINS_T + GONDOLA_T
rows = [
    ("envelope laminate", env_nom, f"{HULL_A:.0f} m2 x {FABRIC_NOM} kg/m2 (range {FABRIC_LO}-{FABRIC_HI})"),
    ("ballonets 2x25%", ball_t, f"2 x sphere-equiv r={ball_r:.1f} m, {ball_a:.0f} m2 x {BALLONET_FABRIC} kg/m2"),
    ("suspension/septum", SUSPENSION_T, "allowance, undrawn"),
    ("nose + mooring", NOSE_T, "allowance, undrawn"),
    ("fins + actuators", FINS_T, "allowance, undrawn"),
    ("gondola + systems", GONDOLA_T, "allowance, undrawn"),
]
for name, val, basis in rows:
    print(f"  {name:<22} {val:6.2f} t   {basis}")
print(f"  {'GAS HULL TOTAL':<22} {gas_hull:6.2f} t")
print(f"  fabric range: {(HULL_A*FABRIC_LO)/1000:.2f}-{(HULL_A*FABRIC_HI)/1000:.2f} t "
      f"-> hull total {gas_hull-(FABRIC_NOM-FABRIC_LO)*HULL_A/1000:.2f}-"
      f"{gas_hull+(FABRIC_HI-FABRIC_NOM)*HULL_A/1000:.2f} t")
print(f"  vs recorded vacuum shell+barrier: "
      + ", ".join(f"{k} {SHELL_T[k]+BARRIER_T[k]:.1f} t" for k in SHELL_T))

print("\n== membrane loading (equilibrium derivation, no strength claim) ==")
print("closed cylindrical section, radius r: equilibrium of a half-cylinder gives")
print("hoop N = p*r; axial (closed ends) N = p*r/2. Dished caps ~ spherical:")
print("both directions ~ p*r_cap/2. Class radius r = {r} m:".format(r=R_CYL))
for p in (SUPERPRESSURE_PA, 2 * SUPERPRESSURE_PA):
    print(f"  p = {p:.0f} Pa gauge: hoop {p*R_CYL/1000:.2f} kN/m, "
          f"axial/cap {p*R_CYL/2000:.2f} kN/m")
print("  laminate working line-strength and seam reduction: UNKNOWN (no coupon)")
print("  -> no strength margin asserted; sizing rests on assumed areal density only")

print("\n== connected gas-fill / ballonet schedule (nominal paper schedule) ==")
P_25 = P_ATM * RHO_25 / RHO_SL          # Pa; isothermal atmosphere, labelled
mix_25_t = RHO_25 * mix_frac_mass() * V / 1000
lift_25 = net_lift_full(RHO_25)
lift_sl_full = net_lift_full(RHO_SL)
v_mix_sl = V * P_25 / P_ATM             # same inventory, no venting
v_ball_sl = V - v_mix_sl
ball_air_sl_t = v_ball_sl * RHO_SL / 1000
lift_sl_novent = (RHO_SL * V - mix_25_t * 1000 - ball_air_sl_t * 1000) / 1000
vent_v = V * (P_ATM / P_25 - 1)
vent_t = vent_v * RHO_25 * mix_frac_mass() / 1000
print(f"atmosphere model: isothermal (assumption), P(2500m) = {P_25:.0f} Pa = "
      f"{P_25/P_ATM:.4f} of SL")
print(f"design point, 2500 m: mixture fills hull ({V:.0f} m3), ballonets empty;")
print(f"  mixture mass {mix_25_t:.2f} t, net lift {lift_25:.2f} t")
print(f"same inventory at SL, no venting: mixture {v_mix_sl:.0f} m3 "
      f"({v_mix_sl/V:.1%} of hull), ballonet air {v_ball_sl:.0f} m3 = "
      f"{ball_air_sl_t:.2f} t")
print(f"  (occupancy {v_ball_sl/V:.1%} of hull vs {2*BALLONET_FRAC:.0%} installed")
print(f"  capacity; ballonet air budgeted exactly once, here - it is ambient air")
print(f"  in ambient air and contributes zero net lift)")
print(f"  -> net lift at SL, no-vent state: {lift_sl_novent:.2f} t, equal to the")
print(f"  design point (constant-inventory gas ship)")
print(f"SL full-hull bound (first departure, or helium topped up at base):")
print(f"  net lift {lift_sl_full:.2f} t with ballonets EMPTY (no SL trim authority);")
print(f"  climbing to 2500 m must vent {vent_v:.0f} m3 = {vent_t:.2f} t of mixture")
print(f"  (irreversible per cycle; base helium logistics UNKNOWN). After any")
print(f"  climb-descent cycle the recoverable SL state is the no-vent state")
print(f"  unless helium is re-added.")
print(f"superpressure {SUPERPRESSURE_PA:.0f} Pa gauge costs "
      f"{mix_25_t*SUPERPRESSURE_PA/P_25:.2f} t of lift at the design point;")
print(f"  main tables are zero-gauge; sensitivity row below")

print("\n== vehicle cases: dry vehicle / payload / net lift (payload INCLUDED) ==")
dry = {"mission @floor": gas_hull + EQUIP_EX_T["floor"],
       "mission @credible": gas_hull + EQUIP_EX_T["credible"],
       "mission @demonstrated": gas_hull + EQUIP_EX_T["demonstrated"],
       "float-only systems": gas_hull + FLOAT_KIT_T}
for name, d in dry.items():
    pay = 0.0 if name == "float-only systems" else PAYLOAD_T
    print(f"  {name:<22} dry {d:7.2f} t + payload {pay:5.1f} t = {d+pay:7.2f} t")
    print(f"      net lift 2500m        {lift_25:7.2f} t -> margin "
          f"{lift_25-d-pay:+8.2f} t")
    if pay:
        print(f"      net lift SL full-hull {lift_sl_full:7.2f} t -> margin "
              f"{lift_sl_full-d-pay:+8.2f} t (bound, first departure)")
        print(f"      net lift SL no-vent   {lift_sl_novent:7.2f} t -> margin "
              f"{lift_sl_novent-d-pay:+8.2f} t (recoverable SL state)")
    else:
        print(f"      payload-free float bound only: SL full-hull "
              f"{lift_sl_full-d:+.2f} t, SL no-vent {lift_sl_novent-d:+.2f} t")

print("\n== minimum demonstrator (24 m x 48 m capsule, own scale) ==")
dD, dL = 24.0, 48.0
dV = math.pi * (dD/2)**2 * (dL-dD) + (4/3)*math.pi*(dD/2)**3
dA = math.pi*dD*(dL-dD) + math.pi*dD**2
d_env = dA * FABRIC_NOM / 1000
d_ball = dA * 0.30 * BALLONET_FABRIC / 1000
d_kit = 0.6 + 0.4 + 0.5   # gondola/power/avionics allowance, t
d_lift = net_lift_full(RHO_SL) * dV / V
print(f"  V={dV:.0f} m3  A={dA:.0f} m2  envelope {d_env:.2f} t + ballonets "
      f"{d_ball:.2f} t + kit {d_kit:.1f} t = {d_env+d_ball+d_kit:.2f} t "
      f"vs lift {d_lift:.2f} t -> +{d_lift-d_env-d_ball-d_kit:.2f} t at SL")
print(f"  (payload-free static bound at SL; no altitude schedule claimed)")

print("\n== Option B: partial-vacuum hybrid (full-mixture model, corrected) ==")
m_mix_sl = RHO_SL * mix_frac_mass() * V / 1000
print(f"model: reducing internal pressure by fraction f removes the {PURITY:.0%}/"
      f"{1-PURITY:.0%}")
print(f"mixture in proportion - BOTH constituents; the remaining (1-f) gas keeps")
print(f"the {PURITY:.0%}/{1-PURITY:.0%} proportions. gain(f) = f * {m_mix_sl:.2f} t "
      f"(full mixture mass at SL; the previous")
print(f"tip counted displaced helium only, 36.1 t - superseded)")
print(f"shell(f) = M_vac * f^(2/3) (buckling-governed, vacuum-cell.md); "
      f"ratio(f) = ratio(1) * f^(-1/3), so ratio(f) >= ratio(1) for f <= 1:")
for k in SHELL_T:
    print(f"    recorded shell {k}: {SHELL_T[k]/m_mix_sl:.2f}x the gain at f=1")
for name, dens in SHELL_MODEL_KGM3.items():
    print(f"    modelled {name}: {dens*V/1000/m_mix_sl:.2f}x the gain")
print(f"  no vacuum fraction pays for any recorded or modelled shell, under this")
print(f"  one stated model")
cross = m_mix_sl * 1000 / V
print(f"  crossover: full-vacuum shell <= {m_mix_sl:.2f} t = {cross:.6f} kg/m3 "
      f"(best recorded 0.508 = {0.508/cross:.2f}x above; "
      f"best modelled 1.124 = {1.124/cross:.2f}x above)")

print("\n== sensitivity (mission @floor, design point 2500 m, payload included) ==")
base = lift_25 - dry["mission @floor"] - PAYLOAD_T
print(f"  base margin: {base:+.2f} t")
sens = [
    ("helium purity 97 -> 95%", -RHO_25*0.02*(1-M_HE/M_AIR)*V/1000),
    ("fabric 0.45 -> 0.65 kg/m2", -(FABRIC_HI-FABRIC_NOM)*HULL_A/1000),
    ("superpressure 0 -> 500 Pa", -mix_25_t*SUPERPRESSURE_PA/P_25),
    ("equipment floor -> credible", EQUIP_EX_T["floor"]-EQUIP_EX_T["credible"]),
    ("hydrogen instead of helium", RHO_25*PURITY*(M_HE-M_H2)/M_AIR*V/1000),
    ("SL full-hull bound vs design point", lift_sl_full-lift_25),
]
for name, delta in sens:
    print(f"  {name:<38} {delta:+8.2f} t  -> margin {base+delta:+8.2f} t")

print("\n== next-change bound (conditional, NOT a credit in the tables above) ==")
d_cred = dry["mission @credible"] - DESCOPE_T
print(f"  credible-class dry vehicle minus cryo plant + LN2 ({DESCOPE_T} t): "
      f"{d_cred:.2f} t; with payload {d_cred+PAYLOAD_T:.2f} t")
print(f"  margin 2500m {lift_25-d_cred-PAYLOAD_T:+.2f} t; SL full-hull "
      f"{lift_sl_full-d_cred-PAYLOAD_T:+.2f} t - dropping those two lines alone")
print(f"  does NOT close the mission; required replacement trim/control equipment")
print(f"  is unpriced (UNKNOWN)")
