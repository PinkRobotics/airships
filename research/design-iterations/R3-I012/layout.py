#!/usr/bin/env python3
"""R3-I012 deterministic arithmetic: dimensioned payload/trim geometry, P-100.

Turns the corrected R3-I007 aggregate cycle into ONE dimensioned arrangement:
four 25 t water bays in the P-100 gas hull, two diagonal 50 t deliveries on
one declared outing, against the corrected I007 laws (SL bag floor
n >= 110,000 m3, rate-matched D2 exchange, fuel tracked per state as
CONSUMABLE fuel with the 0.5 t tank permanent). For this heavier craft the
D1 neutral vent sits ABOVE the SL floor, so the outing is ONE neutral vent +
lake water at D2 - the floor never binds (it bound I007 only because I007's
D1 neutral lay below it). Per-state mass / vertical-force / moment / CoM
ledger with an asserted force identity, one concrete trim action per
transition, preliminary support/routing hardware, a massless ideal bound,
the schedule/fuel envelope with its off-nominal cases marked fuel FAIL, and
the carried economics. Pure stdlib; no environment access, no file writes.
Internal, conditional design hypothesis. No aircraft has been built or flown.

Successor (consolidated first-review correction): state-specific pitch
authority from the stated 50/50 datum with displaced-mixture netting;
asymmetric states carry their own gross mass (all gas/air/fuel/water) in CoM
and heel; disjoint occupancy and usable bay capacity WITHDRAWN to an ideal
unobstructed-volume bound (UNKNOWN); base reset restores the vented mixture
BY SPECIES (He + air) and the reset state is computed and asserted; the
unsupported ~2 kW transition-power claim is replaced by a bounded preliminary
energy budget with closure UNKNOWN.

Second targeted correction: one-direction authority is bounded by BOTH the
donor bag's air AND the receiving bag's headroom under the declared separate
55,000 m3 per-bag capacity (the donor-only D1-end figure overstated
installed authority); the S7 reset row is COMPUTED from the arrival state
plus the named reset operations (species arithmetic in the lifting-mixture
compartment, derived fuel/payload/ballast, ops-complete clock after the
~45 min pump-out) and the assertions consume those computed inventories;
the 18.9 MJ figure is stated strictly as its listed partial subset
(exchange pump, reset pump-out, D1 trim fan) with reset-air and other
supply work UNKNOWN.
"""

import math

# --- carried corrected-I007 anchors and laws --------------------------------
RHO_SL, RHO_25 = 1.2250, 0.9569      # kg/m3 anchors
V = 220_000.0                        # m3 displacement (recorded)
MIX_FRAC = 0.164045                  # 97/3 He/air mixture-to-air density
HE_MASS_FRAC = 0.8171
LIFT_PER_KM3 = RHO_SL * (1 - MIX_FRAC)   # 1.02404 t per 1000 m3 inventory
T0, LAPSE = 288.15, 0.0065
def rho_at(z):
    return RHO_SL * (1 - LAPSE * z / T0) ** 4.2568
GAS_HULL_T = 23.75                   # I007/I003 gas hull
EQUIP_I007_T = 38.77                 # corrected I007 equipment (incl the
FUEL_T = 4.902245704547417           # 5.40 t fuel+tankage line: consumable
TANK_T = 0.50                        # fuel (exactly 6 h) + permanent tank)
BURN_TPH = 0.8170409507579027        # t/h, corrected I007 (2460 kW x 0.332),
                                     # full precision so the carried envelope
                                     # figures reproduce I007 digit-for-digit
BALLONET_CAP = 110_000.0             # m3, 50% installed (2 x 55,000)
N_FLOOR = V - BALLONET_CAP           # 110,000 m3: SL zero-gauge floor
HE_PRICE_BASE, HE_PRICE_LO, HE_PRICE_HI = 12.0, 28.0, 92.0
FIREBOSS_PER_T = 0.64 * 264.172      # $/t comparator
PAYLOAD_T = 100.0
MISMATCH = 0.05                      # manifold drain-rate mismatch bound
HE_I007_VENT_T = 8.00                # corrected I007's floor-capped vent, t

def lift_of(n):
    return n / 1000.0 * LIFT_PER_KM3
def v_bag(n, z):
    return V - n * RHO_SL / rho_at(z)
def m_air(n, z):
    return rho_at(z) * V / 1000.0 - n * RHO_SL / 1000.0

# --- declared geometry (P-100 capsule, corrected I007 hull) ------------------
L, R = 110.0, 27.5                   # m; axis z=0, nose x=-55, tail x=+55
LC = 54.9                            # cylindrical midbody (surface 19,007 m2)
V_DRAW = math.pi * R**2 * LC + 4 / 3 * math.pi * R**3   # 217,255 m3: drawing
# is 1.3% below the recorded 220,000 m3 displacement anchor; all lift uses
# the recorded anchor V (programme convention), stated here once.
BAY_L, BAY_W, BAY_H = 3.0, 3.0, 2.8  # m shell outside; 25.2 m3 >= 25 m3 water
BAYS = {  # bay centre (x, y, z) m; y+ = port
    "B1-FL": (-10.0,  11.0, -19.0),
    "B2-FR": (-10.0, -11.0, -19.0),
    "B3-AL": ( 10.0,  11.0, -19.0),
    "B4-AR": ( 10.0, -11.0, -19.0),
}
PAIR_D1 = ("B1-FL", "B4-AR")          # diagonal: x- and y-moments cancel
PAIR_D2 = ("B2-FR", "B3-AL")          # the other diagonal
CENT_D1 = tuple((BAYS[PAIR_D1[0]][i] + BAYS[PAIR_D1[1]][i]) / 2
                for i in range(3))    # (0, 0, -19): a diagonal pair's centroid
CENT_D2 = tuple((BAYS[PAIR_D2[0]][i] + BAYS[PAIR_D2[1]][i]) / 2
                for i in range(3))    # (0, 0, -19) - ON AXIS by construction
X_FORE_BAG, X_AFT_BAG = -25.0, 25.0  # ballonet centres (air-transfer lever 50 m)
Z_EQUIP = -22.5                      # gondola/equipment centroid (x=y=0)
X_FUEL = (3.0, -3.0)                 # paired fuel tanks, equal draw

# --- preliminary support/routing hardware (declared assumptions, +/-50%) -----
HW = [
    ("bay shells 4x (25.2 m3, baffled, ~48 kg/m3)", 4 * 1.20),
    ("shared frames + cradles + suspension pick-ups", 1.60),
    ("paired release manifold, doors, valves", 1.40),
    ("water cross-pump + internal piping", 0.35),
    ("ballonet air-transfer ducts + fans", 0.75),
    ("trim controls, wiring, instrumentation", 0.30),
]
HW_T = sum(v for _, v in HW)
REPLACED_T = 2.10 + 0.24             # recorded tanks+pump lines replaced
EQUIP_T = EQUIP_I007_T - REPLACED_T + HW_T
DRY_T = GAS_HULL_T + EQUIP_T         # includes the 5.40 t fuel+tankage line
DRY_EX_FUEL = DRY_T - FUEL_T         # consumable fuel burns off; the 0.50 t
                                    # tank is permanent hardware, stays here
LOADED_T = DRY_T + PAYLOAD_T
N0 = LOADED_T / LIFT_PER_KM3 * 1000.0
N_MAX = V * RHO_25 / RHO_SL

print("== R3-I012: dimensioned four-bay payload/trim arrangement, one outing ==")
print(f"geometry: capsule {L}x{R} m, midbody {LC} m; drawn volume {V_DRAW:,.0f} m3 "
      f"(1.3% below the recorded {V:,.0f} anchor, which all lift uses)")
print(f"bays: {BAY_L}x{BAY_W}x{BAY_H} m shells (25.2 m3) at (x,y,z) = "
      + ", ".join(f"{k}{v}" for k, v in BAYS.items()))
y_hull = math.sqrt(R**2 - 19.0**2)
z_hull_y11 = -math.sqrt(R**2 - 11.0**2)
print(f"clearance: hull half-width at bay z: {y_hull:.1f} m vs bay outboard "
      f"{11.0 + BAY_W / 2:.1f} m ({y_hull - 12.5:.1f} m skin clearance); hull "
      f"floor under bay y: {z_hull_y11:.1f} m vs bay bottom "
      f"{-19.0 - BAY_H / 2:.1f} m ({-19.0 - BAY_H / 2 - z_hull_y11:.1f} m)")
occ_m3 = 4 * BAY_L * BAY_W * BAY_H
print(f"occupied volume: the four shell OUTSIDE envelopes alone are "
      f"{occ_m3:.1f} m3 (4 x {BAY_L * BAY_W * BAY_H:.1f}), equipment and "
      f"routes undrawn beyond them; the ledger allocates ALL of V between "
      f"mixture and ballonet with NOTHING reserved - skin clearance is "
      f"necessary, NOT sufficient: disjoint occupancy is UNKNOWN and every "
      f"scalar result below is an IDEAL UNOBSTRUCTED-VOLUME bound (the drawn "
      f"construction is the next unit's work)")
print(f"usable capacity: {BAY_L * BAY_W * BAY_H:.1f} m3 OUTSIDE per bay does "
      f"not prove 25.0 m3 of storable water - walls, baffles and freeboard "
      f"are unpriced here, so usable capacity per bay is UNKNOWN; the ledger "
      f"carries water as MASS (25 t/bay), not as a drawn tank")
print(f"pair centroids: D1 {'+'.join(PAIR_D1)} -> {CENT_D1}; "
      f"D2 {'+'.join(PAIR_D2)} -> {CENT_D2} - both ON the hull centreline, "
      f"so every conserved state has zero nominal pitch/roll moment")
print(f"deliveries: D1 = {'+'.join(PAIR_D1)} via paired manifold (fast drop); "
      f"D2 = {'+'.join(PAIR_D2)} via hose at the scoop rate (rate-matched "
      f"exchange)")

print(f"\n== preliminary hardware (declared assumptions, +/-50%, undrawn) ==")
for name, val in HW:
    print(f"  {name:<48} {val:5.2f} t")
print(f"  TOTAL dimensioned bay/routing hardware {HW_T:5.2f} t replaces the "
      f"recorded tanks+pump {REPLACED_T:.2f} t -> equipment {EQUIP_T:.2f} t "
      f"(corrected I007 {EQUIP_I007_T:.2f}); DRY {DRY_T:.2f} t; "
      f"LOADED {LOADED_T:.2f} t")
margin_hw = lift_of(N_MAX) - LOADED_T
margin_ideal = lift_of(N_MAX) - (LOADED_T - HW_T + REPLACED_T)
print(f"margin at max inventory {lift_of(N_MAX):.2f} t lift: {margin_hw:+.2f} t "
      f"with the dimensioned hardware; massless ideal bound (recorded "
      f"aggregate tanks kept instead) {margin_ideal:+.2f} t - the dimensioned "
      f"set costs {HW_T - REPLACED_T:.2f} t of margin")
print(f"inventory n0 = {N0:,.0f} m3 (SL) -> lift {lift_of(N0):.2f} t balanced "
      f"at departure (full fuel + 100 t); bag {v_bag(N0, 2500) / V:.1%} at "
      f"2,500 m, {v_bag(N0, 0) / V:.1%} at SL; SL floor {N_FLOOR:,.0f} m3 "
      f"(lift at the floor {lift_of(N_FLOOR):.2f} t) would cap total venting "
      f"at {N0 - N_FLOOR:,.0f} m3 - it never binds below (shown)")

# --- declared schedule (times h; corrected-I007 shape, bounded) --------------
t_d1, t_d2, t_ex, t_base = 2.65, 3.00, 0.75, 5.75
def fuel_at(t):
    """Consumable fuel t at time t; the permanent 0.50 t tank never burns."""
    return FUEL_T - BURN_TPH * t

# --- vents: ONE neutral vent at D1; D2 closes with lake water only ----------
# D1 vents exactly to neutral (the post-D1 balanced inventory). For THIS
# craft the neutral sits ABOVE the SL floor, so the vent is legal and the
# floor never binds. An earlier internal sketch also vented D2 down to the
# floor (9.10 t He, a -4.3 t heavy dip mid-exchange): nothing forces it -
# the exchange closes with scooped water at n1 - so the sketch was rejected
# and is recorded in the unit evidence. No helium or bag-capacity reset
# between drops; the bag stays under the 50% cap at every state.
n_after_d1_neutral = (DRY_EX_FUEL + fuel_at(t_d1) + 50.0) / LIFT_PER_KM3 * 1000.0
N1 = max(n_after_d1_neutral, N_FLOOR)
floor_clear_m3 = N1 - N_FLOOR
vent1_m3 = N0 - N1
vent1_mix_t = vent1_m3 * RHO_SL * MIX_FRAC / 1000.0
vent1_he_t = vent1_mix_t * HE_MASS_FRAC
SCOOP_T = lift_of(N1) - DRY_EX_FUEL - fuel_at(t_d2 + t_ex)
SCOOP_D1_PAIR_T = min(SCOOP_T, 50.0)    # into the emptied D1 bays (50 t cap)
SCOOP_TAIL_T = SCOOP_T - SCOOP_D1_PAIR_T  # tail into the emptying D2 bays
# I007 cross-check from the same carried constants: I007's D1 neutral lay
# BELOW its floor, so its vent was floor-capped (it flew +2.29 t light).
n1_i007_neutral = ((GAS_HULL_T + EQUIP_I007_T - FUEL_T) + fuel_at(t_d1) + 50.0) \
    / LIFT_PER_KM3 * 1000.0

print(f"\n== the outing against the corrected-I007 laws ==")
print(f"D1: release 50 t (pair {'+'.join(PAIR_D1)}) -> vent "
      f"{'to neutral' if N1 == n_after_d1_neutral else 'to the floor'}: "
      f"n1 = {N1:,.0f} m3 (vent {vent1_m3:,.0f} m3); bag after "
      f"{v_bag(N1, 2500) / V:.1%} at 2,500 m, {v_bag(N1, 0) / V:.1%} at SL")
print(f"the floor never binds: n1 sits {floor_clear_m3:,.0f} m3 ABOVE the "
      f"{N_FLOOR:,.0f} m3 SL floor (I007's D1 neutral "
      f"{n1_i007_neutral:,.0f} m3 lay {N_FLOOR - n1_i007_neutral:,.0f} m3 "
      f"below its floor, so I007's vent was floor-capped and it flew +2.29 t "
      f"light; the {HW_T - REPLACED_T:.2f} t of hardware mass is exactly what "
      f"lifts this craft's neutral above the floor - the one place it helps)")
print(f"D2: release 50 t (pair {'+'.join(PAIR_D2)}) by rate-matched exchange, "
      f"NO further vent: the hose delivers at the scoop rate while the lake "
      f"refills {SCOOP_T:.1f} t of ballast ({SCOOP_D1_PAIR_T:.1f} t into the "
      f"emptied D1 pair + {SCOOP_TAIL_T:.1f} t tail into the emptying D2 "
      f"pair, both diagonals on-axis); pump ~1.2 m3/min assumed +/-50%, Fire "
      f"Boss-class; hover/dip UNKNOWN")
print(f"total vented {vent1_m3:,.0f} m3 = {vent1_mix_t:.2f} t mixture = "
      f"{vent1_he_t:.2f} t He - ONE neutral vent, {vent1_he_t - HE_I007_VENT_T:+.2f} t "
      f"vs corrected I007's floor-capped {HE_I007_VENT_T:.2f} t; the difference "
      f"is the residual-band choice (full neutral here vs I007's floor-blocked "
      f"+2.29 t light), NOT hardware mass - a neutral vent reconciles the "
      f"weight CHANGE (50 t payload + burn), from which dry mass cancels")
vent_he_v3 = vent1_he_t * 1000.0 / (RHO_SL * 4.0026 / 28.9644)
vent_air_v3 = vent1_m3 - vent_he_v3
print(f"species split of the vent (97/3 He/air by STP volume, consistent "
      f"with the priced He mass): {vent_he_v3:,.0f} m3 He + "
      f"{vent_air_v3:,.0f} m3 air = {vent1_m3:,.0f} m3 of MIXTURE - the base "
      f"reset below restores BOTH constituents; re-adding "
      f"{vent1_m3:,.0f} m3 of pure helium would change the composition")

# --- S7: the reset operation COMPUTED from S6 arrival + named operations -----
# Species arithmetic in the LIFTING-MIXTURE compartment. Declared convention
# (mixing hardware/routing still UNKNOWN): the purchased He and the
# replenishment air enter the mixture space, and the ballonet back-expels
# air through its valves as the mixture volume grows - admitting air to a
# ballonet alone would NOT restore the mixture's air fraction.
HE_VOL_FRAC = 0.97                       # declared 97/3 STP-volume mixture
n_he_s6, n_air_s6 = N1 * HE_VOL_FRAC, N1 * (1.0 - HE_VOL_FRAC)
n_he_s7 = n_he_s6 + vent_he_v3           # + the purchased helium
n_air_s7 = n_air_s6 + vent_air_v3        # + replenishment air to the MIXTURE
N_S7 = n_he_s7 + n_air_s7                # computed; NOT an assigned N0
refuel_t = FUEL_T - fuel_at(t_base)      # named refuel to full consumable
FUEL_S7 = fuel_at(t_base) + refuel_t     # derived reset fuel
pump_out_t = SCOOP_T                     # named pump-out of all scooped ballast
S1_S7 = SCOOP_D1_PAIR_T - min(pump_out_t, SCOOP_D1_PAIR_T)
S2_S7 = SCOOP_TAIL_T - max(pump_out_t - SCOOP_D1_PAIR_T, 0.0)
RELOAD_EACH = PAYLOAD_T / 2.0            # named reload, 50 t per delivery pair
t_s7 = t_base + 45.0 / 60.0              # EARLIEST ops-complete: pump-out only

# --- the ledger: mass, force, moments, CoM -----------------------------------
# P1/P2: water in the D1/D2 pair bays (t); s1/s2: scooped ballast in the
# D1/D2 pair bays (the scoop refills the emptied D1 pair first).
states = [
    ("S0 mast release, SL", 0.00, dict(P1=50.0, P2=50.0, s1=0.0, s2=0.0), N0, 0.0),
    ("S1 top of climb", 0.50, dict(P1=50.0, P2=50.0, s1=0.0, s2=0.0), N0, 2500.0),
    ("S2 zone A arrival", 2.50, dict(P1=50.0, P2=50.0, s1=0.0, s2=0.0), N0, 2500.0),
    ("S3 D1 done (50 t)", t_d1, dict(P1=0.0, P2=50.0, s1=0.0, s2=0.0), N1, 2500.0),
    ("S4 zone B arrival", t_d2, dict(P1=0.0, P2=50.0, s1=0.0, s2=0.0), N1, 2500.0),
    ("S4.5 exchange midpoint", t_d2 + t_ex / 2,
     dict(P1=0.0, P2=25.0, s1=SCOOP_T / 2, s2=0.0), N1, 2500.0),
    ("S5 exchange done (100 t)", t_d2 + t_ex,
     dict(P1=0.0, P2=0.0, s1=SCOOP_D1_PAIR_T, s2=SCOOP_TAIL_T), N1, 2500.0),
    ("S6 base arrival, SL", t_base,
     dict(P1=0.0, P2=0.0, s1=SCOOP_D1_PAIR_T, s2=SCOOP_TAIL_T), N1, 0.0),
    # S7 is the reset operation's CHECKED end state, COMPUTED here from the
    # S6 arrival row plus the named reset operations (species arithmetic in
    # the block above): ballast pumped out, He + air restored to the MIXTURE
    # by species, fuel refilled, 100 t reloaded. Its clock is the EARLIEST
    # ops-complete (~45 min pump-out after S6 arrival; replenishment/load
    # durations UNKNOWN, moored - outside the 6.00 h flight envelope).
    ("S7 reset checked (=S0)", t_s7,
     dict(P1=RELOAD_EACH, P2=RELOAD_EACH, s1=S1_S7, s2=S2_S7, fuel=FUEL_S7),
     N_S7, 0.0),
]
AIR_SPLIT = 0.5   # ballonet air 50/50 fore/aft at neutral (trim datum)
print(f"\n== per-state ledger (fuel, payload, ballast, gas each once; signed "
      f"residuals; moments about the hull centre) ==")
print(f"{'state':<24}{'t_h':>5}{'fuel':>6}{'pay':>5}{'scoop':>7}{'air_t':>7}"
      f"{'n_m3':>8}{'bag%':>6}{'lift':>7}{'weight':>8}{'resid':>7}{'Mx':>6}{'My':>6}")
maxbag = 0.0
rows = []
for label, t, w, n, z in states:
    fuel = w["fuel"] if "fuel" in w else fuel_at(t)   # S7: derived reset fuel
    p1, p2, s1, s2 = w["P1"], w["P2"], w["s1"], w["s2"]
    air = m_air(n, z)
    hard = DRY_EX_FUEL + fuel + p1 + p2 + s1 + s2 + air + n * RHO_SL * MIX_FRAC / 1000.0
    # moments about the hull centre: water rides at its PAIR CENTROID (both
    # (0,0,-19)); fuel equal-draw from +/-3 m tanks; equipment/gas hull on
    # axis; buoyancy at 0 by symmetry; ballonet air at the 50/50 datum.
    # Mx = ROLL (y-terms); My = PITCH (x-terms) - labels kept consistent with
    # the asymmetric section below, which uses both explicitly.
    mx = ((p1 + s1) * CENT_D1[1] + (p2 + s2) * CENT_D2[1])
    my = ((p1 + s1) * CENT_D1[0] + (p2 + s2) * CENT_D2[0]
          + air * AIR_SPLIT * (X_FORE_BAG + X_AFT_BAG))
    vb = v_bag(n, z)
    maxbag = max(maxbag, vb)
    disc = rho_at(z) * V / 1000.0
    lift = disc - air - n * RHO_SL * MIX_FRAC / 1000.0
    w_tot = DRY_EX_FUEL + fuel + p1 + p2 + s1 + s2
    resid = lift - w_tot
    if abs(resid) < 1e-6:   # S3/S5 are neutral by construction; kill float
        resid = 0.0         # noise so the sign of a printed zero is not read
    # force identity, asserted every state: the two ways of writing the
    # balance agree exactly (guards the chimera class of error).
    assert abs((disc - hard) - (lift - w_tot)) < 1e-9, label
    com_x, com_y = (mx / hard if hard else 0.0), (my / hard if hard else 0.0)
    rows.append((label, t, fuel, p1 + p2, s1 + s2, air, n, vb / V, lift,
                 w_tot, resid, mx, my, com_x, com_y))
    print(f"{label:<24}{t:>5.2f}{fuel:>6.2f}{p1 + p2:>5.0f}{s1 + s2:>7.1f}"
          f"{air:>7.1f}{n:>8,.0f}{vb / V:>6.1%}{lift:>7.1f}{w_tot:>8.1f}"
          f"{resid:>+7.2f}{mx:>6.0f}{my:>6.0f}")
print(f"residual = lift - (dry ex fuel + fuel + payload + scoop); + light, "
      f"- heavy; fuel column = CONSUMABLE fuel only (the {TANK_T:.2f} t tank "
      f"is permanent inside dry ex fuel; force identity asserted every "
      f"state). Mx (roll, y-terms) / My (pitch, x-terms) are water+air "
      f"(t*m) about the hull centre: ZERO every state by construction - "
      f"both pair centroids sit on the centreline, fuel draws equally from "
      f"+/-3 m, air holds the 50/50 datum; real moments live in the "
      f"mismatch/worst-case section below")
print(f"max bag fraction of the outing: {maxbag / V:.1%} at base arrival (SL) "
      f"- UNDER the installed 50% TOTAL cap with "
      f"{(BALLONET_CAP_M3_SPARE := BALLONET_CAP - maxbag) / V:.1%} spare; the "
      f"total cap never binds (nor does the SL floor, cleared by "
      f"{floor_clear_m3:,.0f} m3) - the separate {BALLONET_CAP / 2:,.0f} m3 "
      f"PER-BAG capacity still bounds one-direction transfer authority "
      f"(asymmetric section); residuals all light-side, max "
      f"{max(r[10] for r in rows):+.2f} t, within +/-2.6 t vs 10-15 t thrust "
      f"authority")
# the reset operation is CHECKED, not narrated: the assertions CONSUME the
# computed reset inventories - a missing species addition, short refuel or
# missed reload breaks them; they never compare an assigned target to
# itself. Explicit tolerances: inventory/species in m3 STP, composition
# relative, weight in t (source conventions: STP-volume species split of the
# declared 97/3 mixture, carried lift anchors).
assert abs(N_S7 - N0) < 1.0, "reset inventory must reproduce S0"
assert abs(n_he_s7 / N_S7 - HE_VOL_FRAC) < 1e-3, "reset composition 97/3"
assert abs(n_he_s7 - N0 * HE_VOL_FRAC) < 5.0, "lifting He restored"
assert abs(n_air_s7 - N0 * (1.0 - HE_VOL_FRAC)) < 5.0, "lifting air restored"
assert abs(rows[-1][9] - rows[0][9]) < 1e-6, "reset weight must equal S0"
assert abs(rows[-1][6] - rows[0][6]) < 1.0, "reset ledger row must equal S0"
mast_light = lift_of(N0) - (DRY_EX_FUEL + fuel_at(t_base))
print(f"base reset (S7, checked, COMPUTED): pump out {SCOOP_T:.1f} t of scooped "
      f"ballast -> {lift_of(N1) - (DRY_EX_FUEL + fuel_at(t_base)):.1f} t "
      f"light; restore the vented mixture BY SPECIES into the mixture "
      f"compartment - re-add {vent_he_v3:,.0f} m3 STP He ({vent1_he_t:.2f} t, "
      f"the only helium purchase) AND re-admit {vent_air_v3:,.0f} m3 STP of "
      f"air (free from atmosphere; the admission path's hardware/routing is "
      f"UNKNOWN and its energy is NOT in the partial budget below) -> "
      f"computed n_S7 = {N_S7:,.0f} m3, asserted equal to S0's n0 at the "
      f"declared 97/3 composition -> {mast_light:.1f} t light on the mast vs "
      f"the recorded 1.2 MN cable (122 t) - within, {122.4 - mast_light:.1f} "
      f"t to spare; refuel {refuel_t:.2f} t (to {FUEL_S7:.2f} t consumable, "
      f"derived); load 100 t -> the S7 row above is COMPUTED from these "
      f"operations and reproduces S0 exactly (asserted); ops complete no "
      f"earlier than t = {t_s7:.2f} h (~45 min pump-out after S6 arrival; "
      f"replenishment/load durations UNKNOWN, moored - outside the 6.00 h "
      f"flight envelope), neutral, release")

# --- asymmetric intermediate states, explicitly not concealed ----------------
# Each state is DEFINED (own time, water, inventory, altitude) and carries
# its OWN gross mass - dry ex fuel + fuel + water + mixture + ballonet air -
# in the CoM and heel denominators. The fixed 169.38 t departure load is NOT
# a state denominator (first-review finding: it understates every flying
# state's gross by the gas mass it carries at that moment).
mis_t = 25.0 * MISMATCH
LEVER = X_AFT_BAG - X_FORE_BAG
MIX_RHO_STP = RHO_SL * MIX_FRAC      # t per STP m3 of mixture (0.2010)

def gross_state(t, water, n, z):
    fuel = fuel_at(t)
    mix = n * MIX_RHO_STP / 1000.0
    air = m_air(n, z)
    return DRY_EX_FUEL + fuel + water + mix + air, fuel, mix, air

def auth_pitch_state(n, z):
    """One-direction ballonet PITCH authority at a state, bounded by BOTH
    the donor bag's air AND the receiving bag's headroom under the declared
    separate 55,000 m3 per-bag capacity (both bags at the same P,T from the
    50/50 datum). The donor half alone would exceed the receiver cap
    whenever the state's total bag fraction is above 25% of V, so the
    receiver bound governs there; the displaced lifting mixture still nets
    the transfer down by (1 - rho_mix/rho_air) = (1 - MIX_FRAC). The earlier
    whole-inventory figure (air x 50 m) overstated this and is withdrawn."""
    v_donor = v_bag(n, z) * AIR_SPLIT     # donor bag volume at this state, m3
    v_move = min(v_donor, BALLONET_CAP / 2.0 - v_donor)  # headroom bounds it
    m_move = v_move * rho_at(z) / 1000.0  # transferable air, t
    one_way = m_move * LEVER
    return one_way, one_way * (1.0 - MIX_FRAC)

# the three datums where a disturbance actually meets the bags: the
# minimum-air cruise datum (n0 at 2,500 m, S1/S2); the end-of-D1 mismatch
# bound (n1); and a neutral one-bay-empty mid-D1 state (own inventory).
t_obe = t_d1 - 0.075                 # 2.575 h: B1 released, B4 + D2 pair full
water_obe = 75.0
n_obe = (DRY_EX_FUEL + fuel_at(t_obe) + water_obe) / LIFT_PER_KM3 * 1000.0
DATUMS = [
    ("S2 cruise (min air)", 2.50, 100.0, N0, 2500.0,
     0.0, 0.0),                       # no disturbance: datum for authority only
    ("D1-end +/-5% mismatch", t_d1, 50.0 + mis_t, N1, 2500.0,
     mis_t * 10.0, mis_t * 11.0),     # B1 retains 1.25 t: pitch 12.5, roll 13.75
    ("one bay empty, mid-D1", t_obe, water_obe, n_obe, 2500.0,
     250.0, 275.0),                   # B4 alone at (+10,-11): pitch/roll
]
air_min = min(r[5] for r in rows)
one_way_min, net_min = auth_pitch_state(N0, 2500.0)
print(f"\n== asymmetric intermediate release states (defined, not concealed) ==")
print(f"design bound: paired manifolds drain both bays at matched rates; "
      f"worst +/-{MISMATCH:.0%} mismatch of 25 t = {mis_t:.2f} t retained at "
      f"the released bay -> pitch {mis_t * 10.0:.1f} t*m (x-arm 10 m), roll "
      f"{mis_t * 11.0:.1f} t*m (y-arm 11 m)")
print(f"absolute worst (one bay fully drained, pairmate full - manifold "
      f"failure, not the design case): 25 t off-diagonal -> pitch 250 t*m, "
      f"roll 275 t*m")
print(f"{'state':<24}{'water':>7}{'n_m3':>9}{'fuel':>7}{'mix':>6}{'air':>7}"
      f"{'gross':>8}{'pitch_dem':>10}{'roll_dem':>10}{'CoM(p,r) m':>14}"
      f"{'auth_1way':>10}{'auth_net':>9}")
for label, t, water, n, z, pitch_d, roll_d in DATUMS:
    g_, fu_, mi_, ai_ = gross_state(t, water, n, z)
    one_way, net = auth_pitch_state(n, z)
    disp = (pitch_d / g_ if pitch_d else 0.0, roll_d / g_ if roll_d else 0.0)
    print(f"{label:<24}{water:>7.2f}{n:>9,.0f}{fu_:>7.2f}{mi_:>6.1f}{ai_:>7.1f}"
          f"{g_:>8.1f}{pitch_d:>10.1f}{roll_d:>10.1f}"
          f"  ({disp[0]:.3f},{disp[1]:.3f}){one_way:>9.1f}{net:>9.1f}")
print(f"CoM displacement = water moment / THAT STATE'S gross (all carried "
      f"gas/air/fuel/water; mixture centroid and 50/50 air datum sit on the "
      f"centreline, so gas contributes denominator, not numerator)")
print(f"pitch authority is helium-free but ONE-DIRECTIONAL and state-"
      f"specific: at the declared 50/50 datum the transfer is bounded by "
      f"BOTH the donor bag's air AND the RECEIVING bag's headroom under the "
      f"separate {BALLONET_CAP / 2:,.0f} m3 per-bag capacity (same P,T), "
      f"and the displaced mixture nets it down by (1 - {MIX_FRAC:.6f}). "
      f"Donor-bound datums: minimum-air S1/S2 ({air_min:.2f} t air) "
      f"{one_way_min:.2f} t*m one-way, {net_min:.2f} t*m net (the earlier "
      f"{air_min * LEVER:.2f} t*m whole-inventory figure is WITHDRAWN); "
      f"one-bay-empty mid-D1 {auth_pitch_state(n_obe, 2500.0)[0]:.1f} / "
      f"{auth_pitch_state(n_obe, 2500.0)[1]:.1f} t*m. Receiver-bound: the "
      f"D1-end datum's bag is {v_bag(N1, 2500.0) / V:.1%} of V, so moving "
      f"the whole donor half would put {v_bag(N1, 2500.0) / V:.0%} of V in "
      f"one bag against its 25% of V cap - headroom caps the transfer at "
      f"{BALLONET_CAP / 2.0 - v_bag(N1, 2500.0) * AIR_SPLIT:,.0f} m3 (vs "
      f"{v_bag(N1, 2500.0) * AIR_SPLIT:,.0f} m3 of donor air) -> "
      f"{auth_pitch_state(N1, 2500.0)[0]:.1f} / "
      f"{auth_pitch_state(N1, 2500.0)[1]:.1f} t*m; the donor-only "
      f"1757.0/1468.8 t*m D1-end figure was NOT an installed-capacity "
      f"bound and is withdrawn")
print(f"coverage, stated per state: the +/-5% mismatch ({mis_t * 10.0:.1f} "
      f"t*m pitch) sits within net authority at its own datum "
      f"({auth_pitch_state(N1, 2500.0)[1]:.0f} t*m there, receiver-bounded); "
      f"the "
      f"one-bay-empty pitch demand 250 t*m EXCEEDS the {net_min:.0f} t*m "
      f"minimum-air bound, so at THAT datum ballonet transfer alone does "
      f"not cover it - while at the neutral one-empty mid-D1 datum the "
      f"inventory is larger and net authority is "
      f"{auth_pitch_state(n_obe, 2500.0)[1]:.0f} t*m (covered). Release and "
      f"vent timing set the actual state; this is NOT a universal transient "
      f"failure claim, and recovery for the fault case at the min-air "
      f"datum (concurrent vent, thrust, ballast) is UNKNOWN")
for label, t, water, n, z, pitch_d, roll_d in DATUMS:
    if not roll_d:
        continue
    g_, _, _, _ = gross_state(t, water, n, z)
    pend = g_ * 25.0
    print(f"roll at '{label}': no bag authority (bags on the centreline); "
          f"pendulum W*h ~ {pend:,.0f} t*m/rad ({g_:.1f} t state gross x 25 m "
          f"keel depth) -> equilibrium heel "
          f"{math.degrees(roll_d / pend):.2f} deg (rigid-hull assumption; "
          f"envelope heel limit UNKNOWN, I006)")
print(f"between deliveries: pair D1 empty is a balanced diagonal - zero "
      f"moment, CoM on axis; the scoop refills the SAME diagonal (D1 pair) "
      f"first, tail into D2 - both stay on-axis through the exchange; the "
      f"symmetric ideal does NOT conceal these intermediates: they are the "
      f"bound and worst case above")

# --- transients and trim actions ---------------------------------------------
resid_s4 = lift_of(N1) - (DRY_EX_FUEL + fuel_at(t_d2) + 50.0)
print(f"\n== trim action per transition (one concrete each) ==")
for a in [
    "S0->S1 climb: auto-valves SHED ~59 t of ballonet air as the mixture "
    "expands (fans trim the rate; descent is the reverse); NOT neutral at "
    "top: +0.41 t light from climb burn",
    "S1->S2 cruise: none (lightness grows with burn, inside authority)",
    f"S2->S3 D1: paired-manifold fast drop of {'+'.join(PAIR_D1)} (~9 min) "
    f"CONCURRENT with relief vent {vent1_m3:,.0f} m3 to NEUTRAL (release and "
    f"vent rate-matched; declared transient bound: residual <= ~5 t for "
    f"<= 2 min); mismatch moments within one-direction ballonet authority "
    f"at that datum (asymmetric section); transition energy bounded in the "
    f"budget below, closure UNKNOWN",
    "S3->S4 transit: none (fuel burns from paired centreline tanks, "
    "equal draw - no moment)",
    f"S4->S5 D2: rate-matched exchange - hose delivers pair "
    f"{'+'.join(PAIR_D2)} at the scoop rate while the lake refills "
    f"{SCOOP_T:.1f} t of ballast (D1 pair first); NO vent - the neutral sits "
    f"{floor_clear_m3:,.0f} m3 above the floor, so the exchange closes with "
    f"water alone and the residual stays in band end to end",
    f"S5->S6 return + descent: valve air in freely as the mixture contracts; "
    f"light residual on thrust; bag {v_bag(N1, 2500) / V:.1%} -> "
    f"{v_bag(N1, 0) / V:.1%} at base arrival - UNDER the 50% cap throughout",
    f"S6->S7 reset: pump out {SCOOP_T:.1f} t (cross-pump at the scoop rate, "
    f"~45 min), restore the vented mixture BY SPECIES into the mixture "
    f"compartment ({vent_he_v3:,.0f} m3 STP He purchased + {vent_air_v3:,.0f} "
    f"m3 STP air; admission hardware/routing UNKNOWN), refuel "
    f"{FUEL_T - fuel_at(t_base):.2f} t, load 100 t water; the S7 row is "
    f"COMPUTED from these operations and reproduces S0 (asserted); ops "
    f"complete no earlier than t = {t_s7:.2f} h (~45 min pump-out after S6 "
    f"arrival; moored, outside the 6.00 h flight envelope)",
]:
    print(f"  {a}")
print(f"transients: release/vent concurrent at D1 (declared bound <= ~5 t "
      f"for <= 2 min); exchange rate-matched at D2 end to end (residual "
      f"path ~ +0.3 -> +0.1 -> 0.0 t); a FAST D2 (instant 50 t release, no "
      f"concurrent scoop) would swing ~{resid_s4 + 50.0:.0f} t light vs "
      f"10-15 t authority - which is why D2 is an exchange; impossible "
      f"transitions (fast D2, vent below the floor, bag beyond 50%) stay "
      f"FAIL/UNKNOWN, never averaged away")

# --- bounded preliminary transition-energy budget (closure UNKNOWN) ----------
# Replaces the unsupported "~2 kW" line of the first candidate. Declared
# heads/efficiencies +/-50%; no qualified pump/fan map exists, so this is an
# order-of-magnitude budget, not a closure. The inherited fixed burn is kept
# distinct: it EXCLUDES this demand, and no new fuel-FALSE case is claimed.
G_MS2 = 9.81
ex_head_m, ex_eff = 10.0, 0.50         # exchange: lake lift + routing head
ex_work_mj = SCOOP_T * 1000.0 * G_MS2 * ex_head_m / 1e6
ex_elec_mj = ex_work_mj / ex_eff
ex_kw = ex_elec_mj / (t_ex * 3600.0) * 1e3
rs_head_m, rs_eff = 5.0, 0.50          # reset ballast pump-out head
rs_elec_mj = SCOOP_T * 1000.0 * G_MS2 * rs_head_m / 1e6 / rs_eff
rs_kw = rs_elec_mj / (t_ex * 3600.0) * 1e3
fan_dp_kpa, fan_eff, trim_air_t = 1.5, 0.40, 1.0   # trim transfer, D1 window
fan_vol = trim_air_t * 1000.0 / RHO_25  # kg / (kg/m3) = m3 at 2,500 m
fan_elec_mj = fan_vol * fan_dp_kpa * 1e3 / 1e6 / fan_eff
tot_elec_mj = ex_elec_mj + rs_elec_mj + fan_elec_mj
fuel_equiv_t = tot_elec_mj / 0.30 / 43.0 / 1000.0  # gen 30%, 43 MJ/kg
print(f"\n== transition energy: bounded preliminary budget, closure UNKNOWN ==")
print(f"D2 exchange pump: {SCOOP_T:.1f} t at {ex_head_m:.0f} m declared head "
      f"= {ex_work_mj:.2f} MJ hydraulic -> {ex_elec_mj:.2f} MJ electrical at "
      f"{ex_eff:.0%} ({ex_kw:.1f} kW mean over {t_ex * 60:.0f} min)")
print(f"reset pump-out: {SCOOP_T:.1f} t at {rs_head_m:.0f} m head -> "
      f"{rs_elec_mj:.2f} MJ electrical ({rs_kw:.1f} kW mean)")
print(f"D1 trim fans: {trim_air_t:.0f} t air over {fan_dp_kpa:.1f} kPa "
      f"declared -> {fan_elec_mj:.2f} MJ electrical at {fan_eff:.0%}")
print(f"LISTED transitions total {tot_elec_mj:.1f} MJ electrical "
      f"({tot_elec_mj / 3.6:.1f} kWh) ~ {fuel_equiv_t:.4f} t fuel equivalent "
      f"at a 30% generator - a PARTIAL budget: only the D2 exchange pump, "
      f"the reset water pump-out and the D1 trim fan are listed; reset-air "
      f"admission, helium handling and every other supply/transition work "
      f"are UNKNOWN and NOT included - vs the {FUEL_T:.2f} t fixed burn, "
      f"which EXCLUDES it; heads/efficiencies declared +/-50%, no qualified "
      f"pump/fan map, supply allocation undrawn: energy closure UNKNOWN, "
      f"and this is missing accounting, NOT a demonstrated fuel shortage - "
      f"both off-nominal fuel-FAIL cases below stand unchanged")

# --- schedule/fuel envelope (the corrected I007 law, this craft) -------------
reserve_t = fuel_at(t_base)
dt33 = 33.0 / 60.0
short33 = BURN_TPH * (t_base + dt33) - FUEL_T
cover33 = BURN_TPH * (t_base + dt33 + 0.25)
pump_lo = 0.6
ex_nom_min = t_ex * 60.0
t_a = SCOOP_T / pump_lo
t_fix = t_a
for _ in range(8):
    t_fix = t_a + BURN_TPH * (t_fix - ex_nom_min) / 60.0 / pump_lo
dt_lo = (t_fix - ex_nom_min) / 60.0
short_lo = BURN_TPH * (t_base + dt_lo) - FUEL_T
cover_lo = BURN_TPH * (t_base + dt_lo + 0.25)
print(f"\n== schedule/fuel envelope (carried corrected-I007 law) ==")
print(f"{FUEL_T:.6f} t consumable buys EXACTLY the 6.00 h nominal outing "
      f"incl. the 0.25 h reserve ({reserve_t:.6f} t at base; the "
      f"{TANK_T:.2f} t tank is permanent) - ZERO slack; a slip dt is "
      f"covered only while dt <= 15 min")
print(f"+33 min case (carried published band, climb +10/exchange +23): "
      f"fuel_at(6.30 h) = {fuel_at(t_base + dt33):.6f} t -> SHORT "
      f"{short33:.6f} t -> fuel FAIL / outside the accepted nominal envelope; "
      f"covering with the reserve held needs {cover33:.6f} t "
      f"(+{cover33 - FUEL_T:.6f} t fuel, ~+0.05 t tank) - priced, NOT taken")
print(f"-50% pump case (0.6 m3/min, reciprocal rate + burn coupling): "
      f"exchange {t_fix:.6f} min (45 nominal; scoop alone {t_a:.6f} min), "
      f"base arrival {t_base + dt_lo:.6f} h -> SHORT {short_lo:.6f} t -> "
      f"fuel FAIL / outside the envelope; covering needs {cover_lo:.6f} t "
      f"(+{cover_lo - FUEL_T:.6f} t fuel, ~+0.06 t tank) - priced, NOT "
      f"taken; the extra burn is scooped ballast, not helium")

# --- economics (carried law, this craft's numbers) ---------------------------
m3_stp = vent1_he_t * 1000.0 / (RHO_SL * 4.0026 / 28.9644)
print(f"\n== economics from the same ledger (retained FAIL) ==")
print(f"helium vented per 100 t: {vent1_he_t:.2f} t = {m3_stp:,.0f} m3 STP "
      f"({m3_stp / 100:,.0f} m3 per delivered tonne) - ONE neutral vent; "
      f"{vent1_he_t - HE_I007_VENT_T:+.2f} t vs corrected I007's "
      f"{HE_I007_VENT_T:.2f} t floor-capped vent = the residual-band choice, "
      f"not hardware mass (dry mass cancels from a neutral vent); hardware "
      f"mass costs MARGIN ({margin_ideal - margin_hw:.2f} t) and lifts the "
      f"neutral above the floor - it does not change the vent")
for label, price in (("USGS base 2025", HE_PRICE_BASE),
                     ("retail low", HE_PRICE_LO), ("retail high", HE_PRICE_HI)):
    print(f"  ${price:>3.0f}/m3 ({label:<14}): ${m3_stp / 100 * price:,.0f} per "
          f"delivered tonne (${m3_stp * price / 1e6:.2f}M per 100 t cycle)")
ratio = m3_stp / 100.0 * HE_PRICE_BASE / FIREBOSS_PER_T
rev = FIREBOSS_PER_T / (m3_stp / 100.0)
print(f"comparator: scooping SEAT ~${FIREBOSS_PER_T:.0f}/t -> {ratio:.1f}x at "
      f"the USGS base; reversal ${rev:.2f}/m3; jet fuel "
      f"{FUEL_T - fuel_at(t_base):.2f} t/outing <$15k, <1% of the "
      f"{m3_stp * HE_PRICE_BASE / 1e6:.2f}M helium bill")

# --- sensitivity and verdict --------------------------------------------------
print(f"\n== sensitivity (margin at max inventory {margin_hw:+.2f} t) ==")
for name, delta in [
        ("hardware masses +50% (undrawn)", -HW_T * 0.5),
        ("I007 fabric lines hi range (carried)", -3.80),
        ("I007 sundries +50% (carried)", -9.82),
        ("I007 trim set 3 -> 9 t (carried)", -6.00),
        ("endurance 6 -> 12 h", -FUEL_T),
        ("TSFC +20% (secondary estimate)", -FUEL_T * 0.20),
        ("balance sizing, not max inventory", -(lift_of(N_MAX) - lift_of(N0)))]:
    print(f"  {name:<40} {delta:+7.2f} t -> margin {margin_hw + delta:+7.2f} t")
print(f"sign-reversal: the hardware set reaching {HW_T + margin_hw:.1f} t "
      f"(+{margin_hw / HW_T * 100:.0f}% over estimate) alone zeroes the "
      f"closure; any one large carried I007 line plus hardware +50% breaks "
      f"it - thinner than I007's, honestly")
print(f"\n== verdict ==")
print(f"GEOMETRY: closes as an IDEAL UNOBSTRUCTED-VOLUME bound only. Four "
      f"bays at (x,y,z) = (+/-10, +/-11, -19) m in two frames; "
      f"{y_hull - 12.5:.1f} m lateral and "
      f"{-19.0 - BAY_H / 2 - z_hull_y11:.1f} m vertical skin clearance "
      f"(necessary, not sufficient); diagonal deliveries (D1 = "
      f"{'+'.join(PAIR_D1)}, D2 = {'+'.join(PAIR_D2)}) put both pair "
      f"centroids on the centreline - every conserved state is zero-moment. "
      f"Disjoint occupancy and usable bay capacity are UNKNOWN: the ledger "
      f"reserves NO volume for the {occ_m3:.1f} m3 of shell envelopes, "
      f"equipment or routes, and 25.2 m3 outside does not price the internal "
      f"walls - the drawn construction is the next unit's work")
print(f"TRIM/CAPACITY: closes under the corrected-I007 laws for the NOMINAL "
      f"cycle. ONE neutral vent {vent1_m3:,.0f} m3 ({vent1_he_t:.2f} t He) "
      f"at D1; D2 closes with {SCOOP_T:.1f} t of scooped lake water, no "
      f"second vent, no resets; the SL floor never binds (cleared "
      f"{floor_clear_m3:,.0f} m3); max bag {maxbag / V:.1%} at base arrival "
      f"- UNDER the 50% cap; residuals light-side, max "
      f"{max(r[10] for r in rows):+.2f} t; the +/-5% mismatch sits within "
      f"state-specific one-direction ballonet authority (bounded by donor "
      f"inventory AND receiving-bag headroom; receiver-bound at the D1-end "
      f"datum); the one-bay-empty "
      f"pitch demand 250 t*m EXCEEDS the {net_min:.0f} t*m minimum-air "
      f"one-direction bound, so recovery for that fault case at that datum "
      f"is UNKNOWN (state-dependent, larger air inventories do cover it); "
      f"transient response is NOT established anywhere - static capacity is "
      f"not transient control; fast-D2 and below-floor transitions stay "
      f"FAIL/UNKNOWN; transition-energy closure UNKNOWN (bounded budget "
      f"above, distinct from the fixed burn).")
print(f"FUEL/SCHEDULE (carried law): zero slack - the 6.00 h / +15 min "
      f"envelope only; +33 min and -50%-pump cases fuel FAIL "
      f"(short {short33:.6f} / {short_lo:.6f} t), covering priced not taken.")
print(f"ECONOMICS (retained FAIL): {m3_stp / 100 * HE_PRICE_BASE:,.0f} $/t at "
      f"the USGS base = {ratio:.1f}x the comparator; the dimensioned "
      f"arrangement's helium bill is set by the reconciled weight (payload + "
      f"burn), not by its own hardware mass - what the 6.86 t of hardware "
      f"costs is {margin_ideal - margin_hw:.2f} t of margin and, in exchange, "
      f"the floor-freedom that makes the single neutral vent legal.")
print(f"carried unresolved: D2 exchange ops (pump rate, hover/dip) UNKNOWN "
      f"and load-bearing (its -50% case is fuel FAIL); transition-energy "
      f"closure UNKNOWN (bounded budget, distinct from the fixed burn); "
      f"disjoint occupancy and usable bay capacity UNKNOWN (this unit "
      f"withdraws them to an ideal-volume bound); one-bay-empty trim "
      f"recovery at the minimum-air datum UNKNOWN; TSFC secondary; 5.2 t "
      f"I007 allowances undrawn; this hardware set is +/-50% undrawn; "
      f"I006/I010 not established P-100 interfaces (envelope heel/pressure "
      f"limits UNKNOWN).")
print(f"weakest assumption: the {HW_T:.1f} t hardware set (undrawn, +/-50%) - "
      f"it thins the mass margin to {margin_hw:+.2f} t with sign-reversal at "
      f"{HW_T + margin_hw:.1f} t; next geometry change (one, a proposal to "
      f"DERIVE, not a result): draw the x = +/-14 m frame stations with "
      f"staggered z fairing the cradle loads into the main suspension "
      f"curtains - the ~0.4 t frame saving quoted in the first candidate "
      f"was an assumption, to be replaced by a quantity-derived mass; then "
      f"re-price the shells from a drawn tank (usable capacity) and re-run "
      f"the mismatch bound with a real valve spec")

# --- the drawing -------------------------------------------------------------
print(f"\n== drawing (side elevation and section; scale noted per view) ==")
for line in [
    "side elevation (x: nose -55 left, tail +55 right; hull axis z=0; 1 char ~ 2.8 m)",
    "",
    "        fore ballonet (55k m3 max)         aft ballonet (55k m3 max)",
    "     .--------------------------.      .--------------------------.",
    "   .'                            '....'                           '.",
    f"  (  mixture 97/3 He/air, inventory n0 = {N0:,.0f} m3 STP (drawn)      )",
    "   '.                            '----'                           .'|",
    "     '--------------------------'      '--------------------------' |",
    "             |cradle|                       |cradle|                |",
    "     [B1-FL] [B2-FR]             [B3-AL] [B4-AR]      winch/hose    |",
    "       x=-10    z=-19               x=+10   z=-19        z=-22.5     |",
    "  ________________________________._______________________________|",
    "  |<--- midbody 54.9 m ---------->|<-- nose 27.5 + tail 27.5 m --->|",
    "        gondola + equipment (x~0, z=-22.5): 6 engines, paired fuel",
    "        tanks x=+/-3, trim controls; suspension curtains carry the",
    "        bay frames at x=+/-10 m down to the keel",
    "",
    "section at x=+/-10 m (bow view; y+ = port/left; 1 char ~ 1.7 m)",
    "",
    "            z=0  __________________",
    "            _,--'                  '--._",
    "        _,-'      mixture / bag          '-,_",
    f"     _,-'   (bag {v_bag(N0, 2500) / V:.1%} departing -> {v_bag(N1, 2500) / V:.1%} post-D1 of V at 2,500 m,  '-,_",
    f"   ,'          55k m3 cap/side; {v_bag(N1, 0) / V:.1%} max at SL - under the 50% cap)   ',",
    "  |          _,  z=-19:  [B?-L]      [B?-R]          |   y=+/-11 m",
    "  |        ,'  \\____/          \\____/        ',",
    "  |       | 25 t  |    22 m     |  25 t |        |   hull R=27.5 m",
    "  |       | water |<----------->| water |        |",
    "   ',      \\____/                \\____/      ,'",
    "     '-,_        cradles to keel          _,-'",
    "         '--..____ gondola ____..--'   z=-22.5 (engines/fuel/trim)",
    "                   | suspension curtains to hull skin",
]:
    print(line)
