#!/usr/bin/env python3
"""R3-I007 deterministic arithmetic: gas-ship equipment set and trim cycle, P-100.

Selects and prices a propulsion / energy / water-delivery / trim equipment set
for the P-100 100 t-payload mission on the corrected R3-I003 gas hull, and
balances the 100 t load/drop cycle with every term counted once: dry structure,
equipment, payload/expendables, gas (helium mixture), ballonet air, net lift.
Public component data cited per line; unknown masses stay UNKNOWN with
sign-reversal thresholds. Pure stdlib, no environment access, no file writes.
Internal, conditional design hypothesis. No aircraft has been built or flown.
"""

import math

# --- programme anchors (carried, recorded) ---------------------------------
RHO_SL = 1.2250        # kg/m3, sea level (float ledger anchor)
RHO_25 = 0.9569        # kg/m3, 2,500 m working altitude (float ledger anchor)
V = 220_000.0          # m3 displacement (P-100, recorded)
PAYLOAD_T = 100.0      # t, mission water payload (recorded allowance)
M_AIR, M_HE = 28.9644, 4.0026          # g/mol
PURITY = 0.97                            # He volume fraction (I003 assumption)
MIX_FRAC = PURITY * M_HE / M_AIR + (1 - PURITY)   # 0.164045 mixture/air density
HE_MASS_FRAC = PURITY * (M_HE / M_AIR) / MIX_FRAC # 0.8171 He mass fraction

# --- corrected I003 hull (carried, frozen candidate, now landed) -----------
GAS_HULL_T = 23.75     # t envelope+ballonets+suspension+nose+fins+gondola
BALLONET_CAP_M3 = 110_000.0   # 50% of hull volume, installed (2 x 25%)

# --- atmosphere: standard-lapse density between the anchors ----------------
T0, LAPSE = 288.15, 0.0065
def rho_at(z):
    """Density kg/m3, standard lapse layer (z m; anchor-checked)."""
    return RHO_SL * (1 - LAPSE * z / T0) ** 4.2568
def p_at(z):
    """Pressure Pa, standard lapse layer."""
    return 101325.0 * (1 - LAPSE * z / T0) ** 5.2568
assert abs(rho_at(2500) - RHO_25) / RHO_25 < 5e-4

# --- public component data (browsed 2026-10-14) ---------------------------
# PT6A-67B, primary: EASA Type-Certificate Data Sheet No. EASA.IM.E.008
# Issue 06 (2022-02-18), type certificate holder Pratt & Whitney Canada Corp.:
# max continuous power 895 kW, take-off (5 min) 895 kW, dry spec weight
# 234.5 kg (Section 5 Ratings / Section 4 Dimensions and Dry Weight).
# TSFC 0.546 lb/shp/h ~ 0.332 kg/kWh: ESTIMATE from secondary public figures
# (Wikipedia PT6 table); the TCDS carries no fuel-consumption data and no
# primary public source is known - qualified UNKNOWN, sensitivity below.
PT6_KW = 895.0                     # max continuous, EASA TCDS (shaft)
PT6_KG = 234.5                     # dry spec weight, EASA TCDS
PT6_TSFC = 0.546 * 0.4536 / 0.7457 # 0.332 kg/kWh, ESTIMATE (secondary)
N_ENG = 6
# USGS Mineral Commodity Summaries 2026: Grade-A helium base ~$12/m3 (2025),
# $14/m3 (2024); public retail band $28-92/m3.
HE_PRICE_BASE, HE_PRICE_LO, HE_PRICE_HI = 12.0, 28.0, 92.0
# Fire Boss LLC public comparison: scooping SEAT delivers water ~$0.64/gallon.
FIREBOSS_PER_T = 0.64 * 264.172   # $/t (1 t water = 264.17 gal)

# --- selected equipment set (recorded floor lines kept where gas-agnostic) --
SOLAR_T = 2.16
WATER_SET_T = 2.10 + 0.24 + 1.07 + 0.64 + 0.12 + 0.77
SUNDRIES_T = 19.64
PROP_ENG_T = N_ENG * PT6_KG / 1000
PROP_DISC_T = 0.72                   # 6 props ~120 kg, assumed
PROP_MOUNT_T = 1.50                  # gearboxes/nacelles/mounts, allowance
TRIM_SET_T = 3.00                    # ballonet fans/valves/controls, UNKNOWN detail
CRUISE_MS, CD_HULL, ETA_PROP, HOTEL_KW = 30.0, 0.030, 0.80, 200.0
ENDURANCE_H = 6.0

def he_m3_stp(tonnes):
    return tonnes * 1000.0 / (RHO_SL * M_HE / M_AIR)

print("== R3-I007: gas-ship equipment set and the 100 t trim cycle, P-100 ==")
print(f"atmosphere: standard lapse; rho(1000)={rho_at(1000):.4f} "
      f"rho(2500)={rho_at(2500):.4f} (anchor {RHO_25})")

# --- the inventory law and the forced-ballast identity ---------------------
# Mixture volume at z for inventory n (SL m3): v_mix = n * rho_SL/rho(z)
# (molar conservation; the anchor-to-anchor expansion is exactly rho_SL/rho(z)
# for any temperature profile - temperature cancels).
# At zero gauge and fixed hull volume the ballonet-bag volume is FORCED:
#   v_bag(z) = V - v_mix(z),  m_air(z) = rho(z)*V - n*rho_SL
# so net lift = n*rho_SL*(1-MIX_FRAC), altitude-independent, set by inventory
# alone. Ballonet air mass is NOT a free control - the bag holds exactly what
# the displaced mixture leaves behind, at whatever altitude.
LIFT_PER_KM3 = RHO_SL * (1 - MIX_FRAC)     # t per 1000 m3 inventory
def lift_of(n):
    return n / 1000.0 * LIFT_PER_KM3
def v_bag(n, z):
    return V - n * RHO_SL / rho_at(z)
sp_t = V * 2000.0 * rho_at(2500) * MIX_FRAC / p_at(2500) / 1000.0
print(f"\n== inventory law and the forced-ballast identity ==")
print(f"net lift = n x {LIFT_PER_KM3:.5f} t per 1000 m3 of inventory, "
      f"altitude-independent")
print(f"forced ballast: m_air(z) = rho(z)*V - n*rho_SL -> SL-to-2,500 m climb "
      f"sheds {(RHO_SL-RHO_25)*V/1000:.1f} t of air as the mixture expands; "
      f"bag volume follows the gas, and net lift never moves")
print(f"trim controls, net-t equivalent: venting 1,000 m3 inventory = "
      f"{LIFT_PER_KM3:.4f} t toward heavy (costs {1000*RHO_SL*MIX_FRAC/1000:.3f} t "
      f"mixture = {1000*RHO_SL*MIX_FRAC*HE_MASS_FRAC/1000:.3f} t He); "
      f"superpressure +2 kPa adds only {sp_t:.2f} t of mixture (weak; envelope "
      f"limit UNKNOWN, I006); dynamic thrust with the installed "
      f"{N_ENG*PT6_KW/1000:.1f} MW ~ 10-15 t; mast/anchor at station (recorded "
      f"1.2 MN cable) - unlimited at zero airspeed; carried water (competes "
      f"with payload for lift)")

# --- propulsion sizing -----------------------------------------------------
v23 = V ** (2 / 3)
drag_kn = 0.5 * RHO_SL * CRUISE_MS ** 2 * CD_HULL * v23 / 1000.0
shaft_kw = drag_kn * CRUISE_MS / ETA_PROP            # kN * m/s / eta = kW
cruise_kw = shaft_kw + HOTEL_KW
fuel_kgh = cruise_kw * PT6_TSFC
burn_tph = fuel_kgh / 1000.0               # t/h at cruise: fuel is EXPENDABLE
TANK_T = 0.5                               # permanent tank hardware (never burns)
FUEL_T = fuel_kgh * ENDURANCE_H / 1000.0   # consumable fuel: exactly the 6 h
fuel_t = FUEL_T + TANK_T                   # equipment-table line, same total as
# before; the outing ledger tracks FUEL_T only (targeted-check repair: the
# r3-i007-r1 MEDIUM remainder - fuel_at used to return fuel+tank, counting the
# 0.5 t of tank steel as range)
print(f"\n== propulsion (PT6A-67B, primary EASA TCDS EASA.IM.E.008: "
      f"{PT6_KW:.0f} kW max continuous, {PT6_KG:.1f} kg dry; TSFC "
      f"{PT6_TSFC:.3f} kg/kWh ESTIMATE, secondary) ==")
print(f"cruise drag {drag_kn:.1f} kN at {CRUISE_MS:.0f} m/s (Cd {CD_HULL}, "
      f"V^2/3 {v23:.0f} m2) -> shaft {shaft_kw:.0f} kW + hotel {HOTEL_KW:.0f} "
      f"= {cruise_kw:.0f} kW")
print(f"installed {N_ENG} x {PT6_KW:.0f} kW = {N_ENG*PT6_KW/1000:.2f} MW "
      f"(headwind margin; the recorded 30 MW hover-thrust concept is NOT "
      f"carried - its mass closed only without it)")
print(f"fuel {fuel_kgh:.0f} kg/h x {ENDURANCE_H:.0f} h = {FUEL_T:.6f} t "
      f"consumable + {TANK_T:.2f} t permanent tank = {fuel_t:.2f} t line")

# --- equipment table and sizing -------------------------------------------
equipment = [
    ("solar skin (recorded, kept)", SOLAR_T, "recorded floor line"),
    ("water delivery set (recorded, kept)", WATER_SET_T,
     "tanks 2.10 + pump 0.24 + hose 1.07 + cable 0.64 + bag 0.12 + winch 0.77"),
    ("engines 6x PT6A-67B", PROP_ENG_T, "EASA TCDS: 234.5 kg dry each"),
    ("propellers 6x", PROP_DISC_T, "~120 kg composite each, assumed"),
    ("gearboxes/nacelles/mounts", PROP_MOUNT_T, "allowance, undrawn"),
    ("fuel + tankage", fuel_t,
     f"{FUEL_T:.2f} t fuel {ENDURANCE_H:.0f} h at {cruise_kw:.0f} kW + "
     f"{TANK_T:.2f} t tank, permanent"),
    ("ballonet trim set", TRIM_SET_T, "fans/valves/controls, allowance, UNKNOWN"),
    ("sundries and margin (recorded, kept)", SUNDRIES_T, "recorded floor line"),
]
equip_t = sum(v for _, v, _ in equipment)
dry_t = GAS_HULL_T + equip_t
dry_ex_fuel_t = dry_t - FUEL_T     # consumable fuel burns off in flight (tracked
                                    # per state); the 0.5 t tank is permanent
                                    # hardware and stays in this term
loaded_t = dry_t + PAYLOAD_T       # departure sizing: the heaviest state
n_sl = loaded_t / LIFT_PER_KM3 * 1000.0
lift = lift_of(n_sl)
n_max = V * RHO_25 / RHO_SL            # mixture fills hull at 2,500 m
print(f"\n== selected equipment set and sizing ==")
for name, val, basis in equipment:
    print(f"  {name:<38} {val:6.2f} t   {basis}")
print(f"  EQUIPMENT EX-HULL {equip_t:6.2f} t | gas hull (I003) {GAS_HULL_T:.2f} t "
      f"| DRY {dry_t:.2f} t | +payload {PAYLOAD_T:.0f} t | LOADED {loaded_t:.2f} t")
print(f"inventory n = {n_sl:,.0f} m3 (SL) -> net lift {lift:.2f} t, balanced "
      f"loaded (at any altitude in range; bag {v_bag(n_sl,2500)/V:.1%} at "
      f"2,500 m, {v_bag(n_sl,0)/V:.1%} at SL)")
print(f"max-inventory option n = {n_max:,.0f} m3 (hull full at 2,500 m): lift "
      f"{lift_of(n_max):.2f} t -> margin {lift_of(n_max)-loaded_t:+.2f} t")

# --- departure identity (conditional arithmetic, preserved) -----------------
# Full-fuel loaded identity at both anchors. Fuel is NOT permanent trim mass:
# the outing ledger below tracks it burning off (r3-i007-r1 MEDIUM repair).
for label, z, payload in (("loaded, 2,500 m (drop zone, full fuel)", 2500.0, PAYLOAD_T),
                          ("loaded, SL (departure)", 0.0, PAYLOAD_T)):
    vb = v_bag(n_sl, z)
    m_air = rho_at(z) * vb / 1000.0
    m_mix = n_sl * RHO_SL * MIX_FRAC / 1000.0
    disc = rho_at(z) * V / 1000.0
    net = disc - m_mix - m_air
    print(f"  {label:<34} displaced {disc:6.1f} - mixture {m_mix:5.1f} - "
          f"ballonet air {m_air:6.1f} = net {net:6.1f} t vs dry+payload "
          f"{dry_t+payload:6.1f} t (bag {vb/V:5.1%})")

# --- the trim cycle --------------------------------------------------------
GAS_PER_T = MIX_FRAC / (1 - MIX_FRAC)         # t mixture vented per t ballast
HE_PER_T = GAS_PER_T * HE_MASS_FRAC           # t He per t ballast
need = lift - dry_t
n_empty_bal = dry_t / LIFT_PER_KM3 * 1000.0   # empty-balanced inventory
b_empty = v_bag(n_empty_bal, 2500.0)          # bag needed to neutral empty, high
z_empty = next(z for z in range(5000, 9000, 100)
               if v_bag(n_empty_bal, z) <= BALLONET_CAP_M3)
print(f"\n== trim cycle: the 100 t drop ==")
print(f"ballast law: at zero gauge the bag can only grow by displacing "
      f"mixture - each m3 of bag growth vents a m3 of mixture and admits a m3 "
      f"of air; net ballast = dV*(rho_air-rho_mix), gas cost {GAS_PER_T:.4f} t "
      f"mixture = {HE_PER_T:.4f} t He per tonne of ballast - ALTITUDE-"
      f"INDEPENDENT (the ratio rho_mix/(rho_air-rho_mix) is the constant "
      f"{MIX_FRAC/(1-MIX_FRAC):.4f}); there is NO free room at any altitude")
print(f"post-drop reconciliation need: {need:.2f} t (lift {lift:.2f} - dry "
      f"{dry_t:.2f}); carried water cannot reduce it (ballast aboard is still "
      f"weight, and it competed with payload for lift)")
print(f"empty-balanced inventory n = {n_empty_bal:,.0f} m3 needs bag "
      f"{b_empty/V:.1%} at 2,500 m vs {BALLONET_CAP_M3/V:.0%} installed -> "
      f"post-drop full venting is CAP-BLOCKED at working altitude")
print(f"  the light ship neutralises by climbing: bag reaches the cap at "
      f"~{z_empty:,} m (mixture expands into the hull) - a high-cruise return "
      f"leg, or reconcile another way (below)")
cap25 = (BALLONET_CAP_M3 - v_bag(n_sl, 2500.0)) * rho_at(2500.0) * (1 - MIX_FRAC) / 1000.0
b_full = v_bag(n_sl, 2500.0) + need * 1000 / (rho_at(2500.0) * (1 - MIX_FRAC))
fab = ((b_full / 2) ** (2 / 3) - (BALLONET_CAP_M3 / 2) ** (2 / 3)) * 4 * math.pi * 0.30 / 1000
print(f"max single drop at 2,500 m with the 50% cap: {cap25:.1f} t; a full "
      f"100 t single drop needs {b_full/V:.0%} ballonet capacity (fabric "
      f"delta {fab:+.2f} t sphere-equiv) - envelope/pressure limits are the "
      f"I006 lane: interface requirement, not designed here")
# --- the SL-return floor (r3-i007-r1 HIGH repair) ---------------------------
# bag(z,n) = V - n*rho_SL/rho(z) GROWS as z falls, so the 50% bag cap binds at
# the LOWEST point of the outing - the sea-level base: bag(SL) = V - n, hence
# n >= N_FLOOR for zero-gauge SL ops. Superpressure cannot relax this (gauge
# compresses the mixture, shrinking v_mix and GROWING the bag). Venting below
# the floor strands the ship at altitude - there is no helium source aloft.
# This one law is what the published cycle ignored.
N_FLOOR = V - BALLONET_CAP_M3
print(f"\n== the SL-return floor (the binding constraint) ==")
print(f"bag(SL) = V - n: the cap binds at the base, not at 2,500 m -> the "
      f"whole outing keeps n >= {N_FLOOR:,.0f} m3 (lift at the floor "
      f"{lift_of(N_FLOOR):.2f} t); venting past the floor strands the ship")

# --- the r3-i007-r1 counterexamples, reproduced from these constants --------
print(f"\n== counterexamples from round r3-i007-r1, reproduced ==")
print(f"(a) both 50 t drops closed by neutral vents (unburned fuel, as "
      f"published): n -> {n_empty_bal:,.0f} m3, bag at 2,500 m "
      f"{b_empty/V:.3%} > {BALLONET_CAP_M3/V:.0%} installed -> FAIL, "
      f"cap-blocked")
print(f"(b) those two vents plus the stated 50 t scooped ballast: lift "
      f"{lift_of(n_empty_bal):.2f} t vs dry {dry_t:.2f} + 50 t = "
      f"{dry_t + 50:.2f} t -> {dry_t + 50 - lift_of(n_empty_bal):.1f} t heavy "
      f"with no vent left (below the floor) and no helium aloft -> FAIL")
print(f"(c) the published return state n_mid carried ONE vent's inventory "
      f"while the helium bill carried TWO - the two-drop story and the return "
      f"state described different outings; repaired below as one ledger")

# --- the corrected outing: ONE conserved ledger -----------------------------
# D1 (zone A, no lake): fast drop closed by the floor-capped vent.
# D2 (zone B, lake): RATE-MATCHED exchange - the hose delivers mission water
# at the scoop pump rate while the tanks refill from the lake, keeping the
# residual inside thrust authority (a fast D2 would swing ~53 t light, several
# times the 10-15 t installed authority). Pump ~1.2 m3/min assumed (Fire
# Boss-class), +/-50%; hover/dip procedure is UNKNOWN ops detail.
t_d1, t_d2, t_ex = 2.65, 3.00, 0.75      # h: D1 done, D2 start, exchange span
t_base = 5.75                            # h: base arrival (0.25 h reserve)
def fuel_at(t):
    """Consumable fuel t at time t; the permanent tank never burns."""
    return FUEL_T - burn_tph * t
vent1_m3 = n_sl - N_FLOOR                # the ONLY vent of the outing
vent1_mix_t = vent1_m3 * RHO_SL * MIX_FRAC / 1000.0
vent1_he_t = vent1_mix_t * HE_MASS_FRAC
scoop_end_t = lift_of(N_FLOOR) - dry_ex_fuel_t - fuel_at(t_d2 + t_ex)
states = [
    ("S0 mast release, SL", 0.00, PAYLOAD_T, 0.0, n_sl, 0.0,
     "none: balanced at departure sizing (full fuel + 100 t water)"),
    ("S1 top of climb", 0.50, PAYLOAD_T, 0.0, n_sl, 2500.0,
     "auto-valves SHED the 59.0 t of ballonet air as the mixture expands "
     "(descent is the reverse); NOT neutral - climb burn leaves the ship "
     "light; the D1 vent sizing absorbs it"),
    ("S2 zone A arrival", 2.50, PAYLOAD_T, 0.0, n_sl, 2500.0,
     "none: cruise lightness grows with burn, inside thrust authority"),
    ("S3 drop 1 done (50 t)", t_d1, 50.0, 0.0, N_FLOOR, 2500.0,
     f"fast drop 50 t (~9 min) with CONCURRENT relief vent; the vent stops at "
     f"the floor: {vent1_m3:,.0f} m3 ({vent1_he_t:.2f} t He); the ship stays "
     f"~2.3 t LIGHT (the floor blocks the last of the reconciliation), held "
     f"down by thrust/pitch on the transit leg"),
    ("S4 zone B arrival", t_d2, 50.0, 0.0, N_FLOOR, 2500.0,
     "none: the light residual grows slowly as fuel burns"),
    ("S4.5 exchange midpoint", t_d2 + t_ex / 2, 25.0, scoop_end_t / 2,
     N_FLOOR, 2500.0,
     "rate-matched: hose out ~ scoop in; residual stays in band"),
    ("S5 exchange done (100 t)", t_d2 + t_ex, 0.0, scoop_end_t, N_FLOOR, 2500.0,
     f"drop 2 delivered at the pump rate while scooping {scoop_end_t:.1f} t "
     f"of lake ballast - closes the floor-blocked residual exactly"),
    ("S6 base arrival, SL", t_base, 0.0, scoop_end_t, N_FLOOR, 0.0,
     "2.0 h return + descent: bag grows to 50.0% AT the cap at base arrival "
     "(the binding point); air valves in freely; light residual on thrust"),
    ("S7 reset, moored", t_base, 0.0, scoop_end_t, N_FLOOR, 0.0,
     f"pump out {scoop_end_t:.1f} t ballast (mast takes ~53 t of its 100 t "
     f"case, recorded 1.2 MN cable); re-add {vent1_m3:,.0f} m3 He "
     f"({vent1_he_t:.2f} t - the ONLY helium purchase); refuel "
     f"{FUEL_T - fuel_at(t_base):.2f} t (to {FUEL_T:.2f} t consumable); "
     f"load 100 t water -> neutral, release"),
]
print(f"\n== the corrected outing: one conserved ledger (fuel tracked per "
      f"state, signed residuals) ==")
print(f"{'state':<24}{'t_h':>5}{'fuel':>6}{'pay':>5}{'scoop':>7}{'n_m3':>8}"
      f"{'bag%':>6}{'lift':>7}{'weight':>8}{'resid':>7}")
maxbag = 0.0
for label, t, payload, scoop, n, z, action in states:
    vb = v_bag(n, z)
    maxbag = max(maxbag, vb)
    hard = dry_ex_fuel_t + fuel_at(t) + payload + scoop
    print(f"{label:<24}{t:>5.2f}{fuel_at(t):>6.2f}{payload:>5.0f}{scoop:>7.1f}"
          f"{n:>8,.0f}{vb / V:>6.1%}{lift_of(n):>7.1f}{hard:>8.1f}"
          f"{lift_of(n) - hard:>+7.2f}")
print(f"residual = lift - (dry ex fuel + fuel + payload + scoop); + light "
      f"(net up), - heavy; the fuel column is CONSUMABLE fuel only - the "
      f"{TANK_T:.2f} t tank is permanent hardware inside 'dry ex fuel'. Max "
      f"bag fraction of the outing: {maxbag / V:.1%} at base "
      f"arrival (SL, N_FLOOR by construction) - exactly AT the installed cap, "
      f"never beyond; residuals within +/-2.6 t vs 10-15 t thrust authority")
print(f"transients: the D1 release and its vent run concurrently "
      f"(instantaneous residual <= ~5 t for <= 2 min, declared bound); the D2 "
      f"exchange is rate-matched end to end (2.6 t light -> 1.3 -> 0); a FAST "
      f"D2 would swing {lift_of(N_FLOOR) - (dry_ex_fuel_t + fuel_at(t_d2 + t_ex)):.0f} t "
      f"light - beyond authority, which is why D2 is an exchange")
print(f"gas and fuel conserved: one vent {vent1_m3:,.0f} m3 = {vent1_mix_t:.2f} t "
      f"mixture = {vent1_he_t:.2f} t He; fuel burned {FUEL_T - fuel_at(t_base):.6f} t "
      f"of {FUEL_T:.6f} t consumable ({TANK_T:.2f} t tank permanent, never "
      f"burns); reserve at base {fuel_at(t_base):.6f} t = 0.25 h; every tonne "
      f"of post-vent burn closes with BALLAST (1.00 t scoop per t), not "
      f"helium")

# --- delivery economics (the retained FAIL, from the same sequence) ---------
he_cycle = vent1_he_t
m3_cycle = he_m3_stp(he_cycle)
print(f"\n== delivery economics (retained FAIL, derived from the ledger) ==")
print(f"helium vented per 100 t airborne delivery: {he_cycle:.2f} t He = "
      f"{m3_cycle:,.0f} m3 STP ({m3_cycle / 100:,.0f} m3 per delivered tonne) - "
      f"ONE floor-capped vent; the published 16.0 t bill attached two vents "
      f"to a one-vent return state (r3-i007-r1 HIGH, repaired)")
for label, price in (("USGS base 2025", HE_PRICE_BASE),
                     ("retail low", HE_PRICE_LO), ("retail high", HE_PRICE_HI)):
    per_t = m3_cycle / 100.0 * price
    print(f"  ${price:>3.0f}/m3 ({label:<14}): ${per_t:,.0f} per delivered tonne "
          f"(${m3_cycle * price / 1e6:.2f}M per 100 t cycle)")
ratio = m3_cycle / 100.0 * HE_PRICE_BASE / FIREBOSS_PER_T
rev_price = FIREBOSS_PER_T / (m3_cycle / 100.0)
print(f"public comparator: scooping SEAT (Fire Boss) ~${FIREBOSS_PER_T:.0f}/t "
      f"delivered -> helium-trimmed airdrop is {ratio:.1f}x that cost at the "
      f"USGS base price")
print(f"sign-reversal helium price ${rev_price:.2f}/m3 = "
      f"{HE_PRICE_BASE / rev_price:.0f}x below the USGS base - no public helium "
      f"price is near it")
print(f"jet fuel per outing {FUEL_T - fuel_at(t_base):.2f} t: under $15k at any "
      f"plausible price, <1% of the {m3_cycle * HE_PRICE_BASE / 1e6:.2f}M helium "
      f"bill - fuel mass is not the economic constraint; the fuel ENVELOPE "
      f"(zero slack) is schedule-critical, not cost-critical")
print(f"on-board capture rejected by scalar arithmetic: "
      f"{vent1_m3 * RHO_SL / rho_at(2500):,.0f} m3 of vented mixture at 2,500 "
      f"m; at 200 bar ~{vent1_m3 * RHO_SL / rho_at(2500) * p_at(2500) / 101325 / 200:.0f} "
      f"m3 of pressure-tube volume - hundreds of tonnes of vessels (real-gas "
      f"compressibility ignored, errs light); capture would also strand the "
      f"floor-blocked states")
print(f"helium-free alternatives (stated, not selected): (a) surface transfer "
      f"- release at a moored/anchor station, mast takes the load (recorded "
      f"cable+winch+hose kept) - mission changes from airdrop to crane/hose, "
      f"ops UNKNOWN; (b) heavy-leg aerodynamic lift - non-rigid hull CL limit "
      f"UNKNOWN (I006 interface); (c) ~64-72% ballonet capacity (mass+volume, "
      f"I006) - removes the two-pass constraint, not the helium law")

# --- matched before/after budget ------------------------------------------
print(f"\n== matched before/after: recorded floor set -> selected (t) ==")
before = [
    ("vacuum shell + barrier", 111.76 + 0.82, "gas hull (I003)", GAS_HULL_T),
    ("cryo plant + LN2 (emergency ballast)", 12.0 + 7.75, "ballonet trim set", TRIM_SET_T),
    ("battery 20 MWh", 40.0, "fuel + tankage 6 h", fuel_t),
    ("motors+drives+rotors (30 MW)", 1.88 + 1.88 + 13.25,
     "engines+props+mounts", PROP_ENG_T + PROP_DISC_T + PROP_MOUNT_T),
    ("solar skin", 2.16, "solar skin (kept)", SOLAR_T),
    ("water delivery set", 4.94, "water delivery set (kept)", WATER_SET_T),
    ("sundries and margin", 19.64, "sundries and margin (kept)", SUNDRIES_T),
]
for old_n, old_v, new_n, new_v in before:
    print(f"  {old_n:<34} {old_v:6.2f} -> {new_n:<26} {new_v:6.2f} ({new_v-old_v:+7.2f})")
b_tot, n_tot = (sum(v for _, v, _, _ in before), sum(v for _, _, _, v in before))
print(f"  {'TOTAL structure+equipment':<34} {b_tot:6.2f} -> {'':<26} {n_tot:6.2f} "
      f"({n_tot-b_tot:+7.2f})")
print(f"  loaded vehicle: {GAS_HULL_T+103.5+100:.2f} t (I003 floor case, missed "
      f"2,500 m lift by 51.27 t) -> {loaded_t:.2f} t vs lift {lift:.2f} t "
      f"balanced, {lift_of(n_max):.2f} t at max inventory: the MASS budget "
      f"closes")

# --- sensitivity and sign-reversal ----------------------------------------
margin = lift_of(n_max) - loaded_t
print(f"\n== sensitivity (margin at max inventory {margin:+.2f} t) ==")
cd_fuel = (0.5 * RHO_SL * CRUISE_MS**2 * 0.010 * v23 / 1000 * CRUISE_MS
           / ETA_PROP) * PT6_TSFC * ENDURANCE_H / 1000
sens = [
    ("all fabric lines at hi range (I003)", -3.80),
    ("sundries +50% (kept recorded line)", -9.82),
    ("trim set 3.0 -> 9.0 t (undrawn)", -6.00),
    ("endurance 6 -> 12 h", -FUEL_T),
    ("Cd 0.030 -> 0.040 (fuel)", -cd_fuel),
    ("TSFC estimate +20% (no primary source)", -FUEL_T * 0.20),
    ("inventory at balance sizing, not max", lift - lift_of(n_max)),
]
for name, delta in sens:
    print(f"  {name:<40} {delta:+7.2f} t -> margin {margin+delta:+8.2f} t")
print(f"  r3-i007-r1 MEDIUM, restated: all 6 h burnt = {burn_tph*6:.6f} t; "
      f"neutralising that BY VENTING would cost {burn_tph*6*HE_PER_T:.6f} t He, "
      f"but the corrected cycle is floor-capped - post-vent burn closes with "
      f"water ballast at 1.00 t per t, no helium cost")
# --- schedule/fuel envelope (targeted-check repair) --------------------------
# The 6.00 h nominal schedule (5.75 h + 0.25 h reserve) buys EXACTLY the
# consumable fuel: zero slack. A timing slip dt is covered only while
# burn_tph*dt <= reserve. The two published off-nominal cases exceed it and
# are marked fuel FAIL / outside the accepted nominal envelope (the earlier
# "+/-0.45 t, 1:1" line wrongly assumed fuel existed to absorb them).
reserve_t = fuel_at(t_base)
dt33 = 33.0 / 60.0                       # published band: climb +10, exchange +23
short33 = burn_tph * (t_base + dt33) - FUEL_T
cover33 = burn_tph * (t_base + dt33 + 0.25)
pump_lo = 0.6                             # m3/min at -50%
ex_nom_min = t_ex * 60.0                  # 45 min nominal exchange
t_a = scoop_end_t / pump_lo               # scoop time alone at the low rate
t_fix = t_a
for _ in range(8):                        # burn during the overtime must itself
    t_fix = t_a + burn_tph * (t_fix - ex_nom_min) / 60.0 / pump_lo  # be scooped
dt_lo = (t_fix - ex_nom_min) / 60.0
short_lo = burn_tph * (t_base + dt_lo) - FUEL_T
cover_lo = burn_tph * (t_base + dt_lo + 0.25)
print(f"  schedule/fuel envelope (targeted-check repair): {FUEL_T:.6f} t "
      f"consumable buys EXACTLY the 6.00 h nominal outing incl. the 0.25 h "
      f"reserve ({reserve_t:.6f} t at base) - ZERO slack; a slip dt is "
      f"covered only while dt <= 15 min")
print(f"  +33 min case (the published climb +10/exchange +23 band): "
      f"fuel_at(6.30 h) = {fuel_at(t_base + dt33):.6f} t -> SHORT "
      f"{short33:.6f} t -> fuel FAIL / outside the accepted nominal envelope; "
      f"covering it with the reserve held needs {cover33:.6f} t "
      f"(+{cover33 - FUEL_T:.6f} t fuel, ~+0.05 t tank; margin "
      f"{margin - (cover33 - FUEL_T) - 0.05:+.2f} t) - priced, NOT taken")
print(f"  -50% pump case (0.6 m3/min, reciprocal rate + burn coupling): "
      f"exchange {t_fix:.6f} min (45 nominal; scoop alone {t_a:.6f} min), "
      f"base arrival {t_base + dt_lo:.6f} h, fuel_at there "
      f"{fuel_at(t_base + dt_lo):.6f} t -> SHORT {short_lo:.6f} t -> fuel "
      f"FAIL / outside the envelope (the committed code printed "
      f"+0.096068 t here because the tank rode in the fuel); covering it "
      f"needs {cover_lo:.6f} t (+{cover_lo - FUEL_T:.6f} t fuel, ~+0.06 t "
      f"tank; margin {margin - (cover_lo - FUEL_T) - 0.06:+.2f} t) - priced, "
      f"NOT taken; the extra {burn_tph * dt_lo:.6f} t of exchange burn is "
      f"scooped ballast, not helium (floor-capped)")
print(f"sign-reversal on equipment growth: +{margin:.1f} t total - any two "
    f"large sensitivity lines consume it")

# --- verdict ---------------------------------------------------------------
print(f"\n== verdict ==")
print(f"MASS: closes. Equipment {equip_t:.1f} t ex-hull (recorded floor "
      f"103.5 t); dry {dry_t:.1f} t; loaded {loaded_t:.1f} t vs lift "
      f"{lift_of(n_max):.2f} t at 2,500 m with max inventory.")
print(f"TRIM: closes as ONE conserved outing (r3-i007-r1 repaired): the SL bag "
      f"floor caps venting at a single {vent1_m3:,.0f} m3 vent ({vent1_he_t:.2f} t "
      f"He); D1 fast drop closed by it; D2 rate-matched lake exchange; return "
      f"on {scoop_end_t:.1f} t scooped ballast; base refill {vent1_m3:,.0f} m3 "
      f"He; max bag {maxbag/V:.1%} at base arrival; residuals +/-2.6 t vs "
      f"10-15 t authority. A full 100 t single drop still needs {b_full/V:.0%} "
      f"ballonet capacity (I006 interface, not designed here).")
print(f"ECONOMICS (retained FAIL): {he_cycle:.2f} t He per 100 t delivered = "
      f"${m3_cycle*HE_PRICE_BASE/100:,.0f}/t at the USGS base vs "
      f"~${FIREBOSS_PER_T:.0f}/t public comparator ({ratio:.1f}x; repaired "
      f"from the published two-vent bill); reversal needs ${rev_price:.2f}/m3 "
      f"helium. Surface-transfer mode is the helium-free fallback (mission "
      f"change, ops UNKNOWN).")
print(f"SCHEDULE (targeted-check repair): the 6.00 h nominal envelope "
      f"(5.75 h + 0.25 h reserve) has ZERO consumable-fuel slack; both "
      f"off-nominal cases are fuel FAIL / outside the accepted envelope - the "
      f"+33 min published band (short {short33:.6f} t) and the -50% pump "
      f"({t_fix:.3f} min exchange, {t_base + dt_lo:.6f} h base, short "
      f"{short_lo:.6f} t); covering fuel is priced (+{cover33 - FUEL_T:.2f} / "
      f"+{cover_lo - FUEL_T:.2f} t with tank growth), NOT taken - the nominal "
      f"outing and its economics stand on the declared 6 h / +15 min envelope "
      f"only")
print(f"weakest assumptions: the D2 rate-matched exchange (pump ~1.2 m3/min, "
      f"hover/dip at a lake) is an UNKNOWN ops procedure that the second "
      f"delivery now depends on, and its -50% case now also breaks the fuel "
      f"envelope (FAIL above, not absorbed); the TSFC is a secondary-sourced "
      f"estimate (no "
      f"primary public source; fuel scales with it), and propeller/mount "
      f"masses plus the 3.0 t trim set are allowances, not drawings "
      f"({PROP_DISC_T+PROP_MOUNT_T+TRIM_SET_T:.1f} t combined); next design "
      f"change: price the ballonet trim set and enlarged-capacity option with "
      f"the envelope/pressure-control lane (whose current R3-I006 envelope "
      f"does not establish the P-100 bag interface), then re-run the cycle "
      f"economics at the retail helium band")
