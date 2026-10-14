#!/usr/bin/env python3
"""R3-I003 deterministic arithmetic: gas-supported vs evacuated hull at P-100 scale.

Prints every number quoted in README.md. Pure stdlib, no environment access, no
file writes. Anchors: air densities 1.2250 / 0.9569 kg/m3 (sea level / 2,500 m,
the programme's own anchors); molar-mass lift factors computed, not remembered.
Internal, conditional design hypothesis. No aircraft has been built or flown.
"""

import math

RHO_SL = 1.2250        # kg/m3, programme anchor (float ledger)
RHO_25 = 0.9569        # kg/m3, programme anchor (float ledger)
P_ATM = 101325.0       # Pa
M_AIR, M_HE, M_H2 = 28.9644, 4.0026, 2.016  # g/mol, CODATA standard masses

# P-100 class, sim/config.js and research/analysis/mass-budget.json on afb2c2d1
V = 220_000.0          # m3 displacement (recorded)
HULL_A = 19_007.0      # m2 hull surface (recorded)
PAYLOAD_T = 100.0      # t, class allowance (recorded)

# Recorded vacuum baseline, research/analysis/mass-budget.json P100 cases (t)
SHELL_T = {"floor": 111.76, "credible": 165.0, "demonstrated": 255.2}
BARRIER_T = {"floor": 0.82, "credible": 8.24, "demonstrated": 65.6}
EQUIP_EX_T = {"floor": 103.5, "credible": 293.2, "demonstrated": 787.5}
#   EQUIP_EX_T = everything-but-shell-and-barrier, recomputed from the case
#   lines (their everythingButShellT minus the barrier line).
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

def he_net(rho, purity=PURITY, gauge=0.0):
    """Net helium lift kg/m3: mixture density minus air, gauge pressure folded in."""
    he_frac_mass = purity * M_HE / M_AIR + (1 - purity)
    internal = rho * he_frac_mass * (1 + gauge / P_ATM)
    return rho - internal

def h2_net(rho, purity=PURITY):
    h2_frac_mass = purity * M_H2 / M_AIR + (1 - purity)
    return rho - rho * h2_frac_mass

print("== anchors ==")
print(f"molar-mass lift factors: He/air={M_HE/M_AIR:.5f}  H2/air={M_H2/M_AIR:.5f}")
print(f"helium net lift, purity {PURITY:.0%}: SL {he_net(RHO_SL):.4f}  "
      f"2500m {he_net(RHO_25):.4f} kg/m3 (pure He: "
      f"{RHO_SL*(1-M_HE/M_AIR):.4f} / {RHO_25*(1-M_HE/M_AIR):.4f})")
print(f"hydrogen net lift, purity {PURITY:.0%}: SL {h2_net(RHO_SL):.4f} kg/m3 "
      f"(+{(h2_net(RHO_SL)-he_net(RHO_SL))*V/1000:.1f} t vs He at P-100)")
print(f"superpressure {SUPERPRESSURE_PA:.0f} Pa costs "
      f"{RHO_SL*(M_HE/M_AIR)*(SUPERPRESSURE_PA/P_ATM)*V/1000:.2f} t of lift at P-100 SL")

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

print("\n== vehicle totals and margins (helium, purity 97%) ==")
lift_sl = he_net(RHO_SL) * V / 1000
lift_25 = he_net(RHO_25) * V / 1000
cases = {"mission @floor": gas_hull + EQUIP_EX_T["floor"],
         "mission @credible": gas_hull + EQUIP_EX_T["credible"],
         "mission @demonstrated": gas_hull + EQUIP_EX_T["demonstrated"],
         "float-only systems": gas_hull + FLOAT_KIT_T}
print(f"  lift: SL {lift_sl:.1f} t   2500m {lift_25:.1f} t   (payload target {PAYLOAD_T:.0f} t)")
for name, veh in cases.items():
    print(f"  {name:<22} vehicle {veh:7.1f} t   margin SL {lift_sl-veh:+7.1f} t   "
          f"margin 2500m {lift_25-veh:+7.1f} t")

print("\n== minimum demonstrator (24 m x 48 m capsule, own scale) ==")
dD, dL = 24.0, 48.0
dV = math.pi * (dD/2)**2 * (dL-dD) + (4/3)*math.pi*(dD/2)**3
dA = math.pi*dD*(dL-dD) + math.pi*dD**2
d_env = dA * FABRIC_NOM / 1000
d_ball = dA * 0.30 * BALLONET_FABRIC / 1000
d_kit = 0.6 + 0.4 + 0.5   # gondola/power/avionics allowance, t
d_lift = he_net(RHO_SL) * dV / 1000
print(f"  V={dV:.0f} m3  A={dA:.0f} m2  envelope {d_env:.2f} t + ballonets {d_ball:.2f} t "
      f"+ kit {d_kit:.1f} t = {d_env+d_ball+d_kit:.2f} t vs lift {d_lift:.2f} t "
      f"-> margin +{d_lift-d_env-d_ball-d_kit:.2f} t at SL")

print("\n== Option B: partial-vacuum hybrid closure ==")
he_mass_sl = RHO_SL * (M_HE / M_AIR) * V / 1000  # t of helium displaced by full vacuum
print(f"  max lift gain of hard vacuum over ambient He: {he_mass_sl*PURITY:.1f} t "
      f"(displaced He mass, purity {PURITY:.0%})")
print(f"  buckling-governed shell mass scales as f^(2/3) (vacuum-cell.md); "
      f"ratio shell/gain at f=1:")
for k in SHELL_T:
    print(f"    recorded shell {k}: {SHELL_T[k]/(he_mass_sl*PURITY):.2f}x the gain")
for name, dens in SHELL_MODEL_KGM3.items():
    print(f"    modelled {name}: {dens*V/1000/(he_mass_sl*PURITY):.2f}x the gain")
print(f"  ratio(f) = ratio(1) * f^(-1/3), monotonically >= ratio(1) for f<=1: "
      f"no vacuum fraction pays for any recorded or modelled shell")
print(f"  crossover needs a full-vacuum shell <= {he_mass_sl*PURITY:.1f} t "
      f"= {he_mass_sl*PURITY*1000/V:.3f} kg/m3 "
      f"(best recorded bound 0.508, best modelled 1.124 kg/m3)")

print("\n== sensitivity (P-100, mission @floor, SL margin) ==")
base = lift_sl - cases["mission @floor"]
sens = [
    ("helium purity 97 -> 95%", -RHO_SL*0.02*(1-M_HE/M_AIR)*V/1000),
    ("fabric 0.45 -> 0.65 kg/m2", -(FABRIC_HI-FABRIC_NOM)*HULL_A/1000),
    ("superpressure 500 -> 1000 Pa", -RHO_SL*(M_HE/M_AIR)*(500/P_ATM)*V/1000),
    ("working altitude SL -> 2500 m", lift_25-lift_sl),
    ("equipment floor -> credible", -EQUIP_EX_T["credible"]+EQUIP_EX_T["floor"]),
    ("hydrogen instead of helium", (h2_net(RHO_SL)-he_net(RHO_SL))*V/1000),
]
for name, delta in sens:
    print(f"  {name:<32} {delta:+8.1f} t  -> margin {base+delta:+8.1f} t")
