#!/usr/bin/env python3
"""R3-I017 deterministic arithmetic: drawn bay/cradle/interface arrangement, P-100.

Replaces the I012 allowance-priced bay set with ONE drawn hardware
arrangement at the proposed x = +/-14 m frame stations (with a chosen
vertical stagger), priced from quantities: plate areas, sections, fittings.
The fixed I012 x = +/-10 m arrangement is re-priced with the SAME method as
the sole comparison - as a labelled SIMPLIFIED SCALAR BEAM (both bay loads
at one midspan point; connecting transverse structure unpriced), so its
spreader figure is member stock under that simplification, NOT an
established physical station saving. Corner envelopes per station, routing
and maintenance corridors; the earlier "conditional" bag-plane occupancy
demonstration is WITHDRAWN (the 40 m bags enter the hemispherical caps,
where the full-circle section bound was nonconservative; membrane shape
UNKNOWN) - occupancy is UNKNOWN under the ideal unobstructed-volume
convention. Member reactions/moments for full bays, the bounded release
mismatch (rate + allowed 2 s start skew) and one-bay-empty states under one
stated loading convention, a declared release law with finite trim response
(net of displaced mixture), and the corrected-ledger rerun (dry mass cancels
from the neutral vent; fuel FAIL cases and economics carried). Carries the
twice-corrected I012 laws: pitch authority is ONE-DIRECTIONAL and
state-specific, bounded by BOTH donor inventory and receiving-bag headroom
(displaced mixture nets x(1-MIX_FRAC)); asymmetric states use their own
gross mass (incl gas) in CoM and heel denominators; the S7 reset is COMPUTED
from the arrival state plus the named operations (species arithmetic) and
asserted against S0; vent accounting is species-consistent (He + air);
transition energy is a listed PARTIAL budget with closure UNKNOWN; the 3 mm
tank plate is selected stock, UNQUALIFIED for flat-panel adequacy. Pure
stdlib; no env access, no writes.
Internal, conditional design hypothesis. No aircraft has been built or flown.
"""

import math

# --- carried corrected-I012/I007 anchors and laws -----------------------------
RHO_SL, RHO_25 = 1.2250, 0.9569
V = 220_000.0                        # recorded displacement anchor (all lift)
V_DRAWN = 217_547.0                  # drawn capsule volume (1.3% below anchor)
MIX_FRAC = 0.164045
HE_MASS_FRAC = 0.8171
LIFT_PER_KM3 = RHO_SL * (1 - MIX_FRAC)
T0, LAPSE = 288.15, 0.0065
def rho_at(z):
    return RHO_SL * (1 - LAPSE * z / T0) ** 4.2568
GAS_HULL_T = 23.75
EQUIP_I007_T = 38.77
FUEL_T = 4.902245704547417           # consumable (exactly 6 h)
TANK_T = 0.50                        # permanent tank
BURN_TPH = 0.8170409507579027
BALLONET_CAP = 110_000.0
N_FLOOR = V - BALLONET_CAP
RHO_AL = 2.70                        # t/m3, 5083/6061 declared
SIG_Y_AL = 276.0                     # MPa, 6061-T6 declared
FS = 1.5                             # loading/allowable factor (quasi-static
SIG_ALLOW = SIG_Y_AL / FS            # 1 g x FS; dynamic/slosh impact named)
HE_PRICE_BASE, HE_PRICE_LO, HE_PRICE_HI = 12.0, 28.0, 92.0
FIREBOSS_PER_T = 0.64 * 264.172
PAYLOAD_T = 100.0
MISMATCH = 0.05
T_DRAIN_S = 9.0 * 60.0    # declared linear-drain bound window (~9 min)
SKEW_S = 2.0              # allowed pair start skew (declared <= 2 s)
RHO_W = 1.000             # t/m3 declared freshwater (head + volume conv.)
# fixed I012 comparison values (twice-corrected successor output; labeled
# carries - authority figures are the corrected ONE-DIRECTION NET law,
# receiver-headroom-bounded where the state bag exceeds 25% of V)
I012 = dict(HW=9.20, REPLACED=2.34, DRY=69.38, LOADED=169.38, N0=165403.0,
            N1=114463.0, VENT_M3=50940.0, VENT_HE_T=8.36, SCOOP=50.9,
            MARGIN=6.60, IDEAL=13.46, MAXBAG=0.480, MAXRESID=2.04,
            AUTH_MINAIR=164.66, AUTH_ONEEMPTY=842.3, AUTH_MISMATCH=730.8,
            MY_MIS=12.5, MY_OBE=250.0, HEEL_BOUND=0.15, HEEL_WORST=2.99)

def lift_of(n):
    return n / 1000.0 * LIFT_PER_KM3
def v_bag(n, z):
    return V - n * RHO_SL / rho_at(z)
def m_air(n, z):
    return rho_at(z) * V / 1000.0 - n * RHO_SL / 1000.0
def fuel_at(t):
    return FUEL_T - BURN_TPH * t

L, R = 110.0, 27.5
LC = 54.9
t_d1, t_d2, t_ex, t_base = 2.65, 3.00, 0.75, 5.75

# --- DECLARED structural-interface assumptions (unqualified parts of the -----
# --- load path; each carries a named sensitivity below) -----------------------
CURTAIN_PLANES = (-21.0, -14.0, -7.0, 0.0, 7.0, 14.0, 21.0)  # midbody x, m
BAG_SPAN_M = 40.0                    # declared ballonet span (each, centred
X_BAG_C = 25.0                       # at x = +/-25); fit is UNKNOWN (the
                                     # former minimum-span bound is withdrawn)
Z_UP, Z_LOW = -19.0, -21.5        # row heights (DIAGONAL: each pair at one z)
Y_BAY = 11.0                         # bay centreline y (both rows)
BAY_L, BAY_W, BAY_H = 3.05, 3.05, 2.85   # OUTSIDE dims of the drawn tank
WALL_T = 0.003                       # m plate - SELECTED STOCK (min-gauge +
                                     # corrosion + handling, declared); flat-
                                     # panel structural adequacy UNKNOWN
PLATE_ALLOW = 90.0                   # MPa weld-affected allowable, declared
BAFFLES = 2
FREEBOARD = 0.06                     # m ullage/vent space
DYNAMIC_UNRESOLVED = ("slosh impact, gust and release-door transient loads "
                      "are NOT modelled (quasi-static 1 g x FS 1.5 only)")

# --- I. the drawn tank: usable volume vs outside dimensions ------------------
inner = (BAY_L - 2 * WALL_T) * (BAY_W - 2 * WALL_T)
usable_h = BAY_H - 2 * WALL_T - FREEBOARD
baffle_vol = BAFFLES * BAY_L * BAY_H * WALL_T
usable = inner * usable_h - baffle_vol
need = 25.0                          # t fresh water at rho 1.000 t/m3
head_kpa = RHO_W * 1000.0 * 9.81 * BAY_H / 1000.0    # freshwater bottom head
# F1/F8: the earlier p*L/(2*sigma) "pressure thickness" (0.58 mm vs 3 mm
# plate) is WITHDRAWN as a qualification - a membrane/hoop relation does not
# model rectangular flat-panel bending, baffle support or load transfer into
# the saddle, and the head used the air-density anchor. The 3 mm plate is
# SELECTED STOCK, unqualified; no corrected thickness is claimed here.
plate_area = 2 * BAY_L * BAY_W + 2 * BAY_L * BAY_H + 2 * BAY_W * BAY_H
shell_t = plate_area * WALL_T * RHO_AL
baffle_t = BAFFLES * BAY_L * BAY_H * WALL_T * RHO_AL
rim_t = 4 * (2 * (BAY_L + BAY_W)) * 0.0025 * 2.7 / 4  # rim angles ~25 kg set
fitout_t = 0.095   # manway+cover, sump, drain, vent, surge strainers, coating,
                   # wear pads, lugs: declared +/-50%
BAY_T = shell_t + baffle_t + rim_t + fitout_t
BAY_LOADED_T = BAY_T + need

print("== R3-I017: drawn four-bay payload cradles and occupied-volume interfaces ==")
print(f"I. drawn tank: outside {BAY_L}x{BAY_W}x{BAY_H} m, wall {WALL_T*1000:.0f} mm "
      f"5083 plate, {BAFFLES} full baffles {WALL_T*1000:.0f} mm, {FREEBOARD*1000:.0f} mm freeboard")
print(f"   bottom hydrostatic head {head_kpa:.1f} kPa (freshwater, rho "
      f"{RHO_W:.3f} t/m3 declared); plate {WALL_T*1000:.0f} mm 5083 is "
      f"SELECTED STOCK (min-gauge + corrosion + handling, declared) - "
      f"flat-panel bending/support/attachment adequacy WITHDRAWN to UNKNOWN: "
      f"the earlier p*L/(2*sigma) '0.58 mm pressure thickness' is a "
      f"membrane/hoop relation, not a flat-panel check, and is withdrawn; no "
      f"corrected thickness claimed (weld-affected {PLATE_ALLOW:.0f} MPa "
      f"allowable remains a declared sizing datum for the members below)")
print(f"   usable volume {usable:.2f} m3 vs {need:.1f} m3 required (25 t fresh "
      f"water, rho {RHO_W:.3f} t/m3 declared; salt 1.025 would need "
      f"{25/1.025:.1f}) -> "
      f"ullage margin {(usable/need-1)*100:.1f}%")
print(f"   mass from quantities: plates {plate_area:.1f} m2 x {WALL_T*1000:.0f} mm "
      f"= {shell_t:.3f} t + baffles {baffle_t:.3f} + rims {rim_t:.3f} + fitout "
      f"{fitout_t:.3f} (declared +/-50%) = {BAY_T:.3f} t/bay "
      f"({BAY_T/ (BAY_L*BAY_W*BAY_H) * 1000:.0f} kg/m3 vs I012's assumed 48)")
print(f"   {DYNAMIC_UNRESOLVED}")

# --- II. geometry: stations, stagger, corner clearance ledger -----------------
X_STATIONS = (-14.0, 14.0)
BAYS = {  # (x, y, z) centres; diagonal pairs as in I012
    "B1-FL": (X_STATIONS[0], +Y_BAY, Z_UP),
    "B2-FR": (X_STATIONS[0], -Y_BAY, Z_LOW),
    "B3-AL": (X_STATIONS[1], +Y_BAY, Z_LOW),
    "B4-AR": (X_STATIONS[1], -Y_BAY, Z_UP),
}
PAIR_D1 = ("B1-FL", "B4-AR")
PAIR_D2 = ("B2-FR", "B3-AL")
print(f"\nII. arrangement: frames at x = {X_STATIONS} m (proposed stations), "
      f"vertical stagger DIAGONAL - upper row {'+'.join(PAIR_D1)} at z = {Z_UP} m, "
      f"lower row {'+'.join(PAIR_D2)} at z = {Z_LOW} m, both rows at "
      f"y = +/-{Y_BAY} m (each pair at ONE height: release within a pair is "
      f"height-balanced)")
print(f"    both pair centroids remain ON the hull centreline in x and y "
      f"((0, 0, avg-z)) - zero nominal Mx/My is preserved by the stagger "
      f"(stagger moves only z, which enters neither roll nor pitch arms)")
min_rad = 1e9
print(f"    {'bay':<6}{'corner(y,z) m':>22}{'radial r m':>11}{'skin clear m':>13}"
      f"   (per-bay EXTREMA: worst/best)")
for name, (bx, by, bz) in BAYS.items():
    # F10: print each bay's ACTUAL radial extrema over all four corners; the
    # earlier sy*sz>0 sign filter showed intermediate corners for the
    # positive-y bays and omitted their worst corner. The global minimum
    # still accumulates every corner of every bay.
    corners = [(by + sy * BAY_W / 2, bz + sz * BAY_H / 2)
               for sy in (-1, 1) for sz in (-1, 1)]
    rs = [math.hypot(cy, cz) for cy, cz in corners]
    min_rad = min(min_rad, R - max(rs))
    order = sorted(range(4), key=lambda i: -rs[i])   # worst corner first
    for i in (order[0], order[-1]):                  # the bay's extrema
        cy, cz = corners[i]
        print(f"    {name:<6}({cy:>6.2f},{cz:>7.2f})   {rs[i]:>9.2f}  {R - rs[i]:>12.2f}")
y_hull_up = math.sqrt(R**2 - Z_UP**2)
y_hull_low = math.sqrt(R**2 - Z_LOW**2)
print(f"    worst radial skin clearance {min_rad:.2f} m (declared minimum 0.50 m); "
      f"hull half-width {y_hull_up:.1f} m at z={Z_UP}, {y_hull_low:.1f} m at "
      f"z={Z_LOW} vs bay outboard edge {Y_BAY + BAY_W/2:.2f} m -> outboard "
      f"maintenance gaps {y_hull_up - Y_BAY - BAY_W/2:.1f} / "
      f"{y_hull_low - Y_BAY - BAY_W/2:.1f} m (>= 0.9 m scaffold declared)")
print(f"    inboard: both rows at |y| = {Y_BAY} leave |y| < {Y_BAY - BAY_W/2:.2f} m "
      f"open to the keel corridor (below the lower row bottom "
      f"{Z_LOW - BAY_H/2:.1f} m down to the hull floor {-R:.1f} m at y=0) for "
      f"hose, ducts and the winch at z=-22.5; gondola/engines/fuel at x in "
      f"[-3,3] z=-22.5 clear the nearest bay face by "
      f"{abs(X_STATIONS[0]) - BAY_L/2 - 3:.1f} m in x")
print(f"    the stagger is CHOSEN (diagonal, each pair at one height) so the "
      f"upper-row saddles tie high on the curtain fan and the lower row "
      f"beneath, layering the pickup points and the two working heights; BOTH "
      f"rows at z={Z_UP} would also fit (worst corner then "
      f"{R - math.hypot(Y_BAY + BAY_W/2, Z_UP - BAY_H/2):.2f} m radial) - stated "
      f"so the stagger is not read as forced by skin fit")

# --- III. member statics (one loading convention) ------------------------------
# Convention: quasi-static 1 g, loads as bay weights at cradle points; members
# simply supported at their pickup points; allowable = 276/1.5 MPa. Dynamic,
# slosh-impact and gust loads are NOT modelled (named above).
W_BAY_KN = BAY_LOADED_T * 9.81           # full bay weight, kN
SADDLE_LEN, SADDLE_SUPP = 3.7, 3.0       # saddle beam length / support span
M_saddle = (W_BAY_KN / SADDLE_SUPP) * SADDLE_SUPP**2 / 8   # kN*m, UDL
S_req_saddle = M_saddle * 1e3 / (SIG_ALLOW * 1e6)          # m^3
def box_S(h, b, t):
    """Section modulus (m^3) and mass (t/m) of a thin-walled box."""
    I = (b * h**3 - (b - 2 * t) * (h - 2 * t)**3) / 12
    return I / (h / 2), (b * h - (b - 2 * t) * (h - 2 * t)) * RHO_AL
SAD_CAND = [(0.20, 0.32, 0.006), (0.20, 0.32, 0.008),
            (0.25, 0.35, 0.008), (0.30, 0.40, 0.010)]
sad_h, sad_b, sad_t = next(d for d in SAD_CAND if box_S(*d)[0] >= S_req_saddle)
SAD_S, sad_mass_pm = box_S(sad_h, sad_b, sad_t)
SADDLE_T = sad_mass_pm * SADDLE_LEN + 0.015   # + wear pads/lugs, t
PICKUP_T = 0.012                          # clevis + bonded socket each, declared
# --- the +/-14 station: saddles tie DIRECTLY into a declared curtain plane ---
# --- the +/-10 comparison: a SIMPLIFIED SCALAR BEAM, labelled as such. The
# single 7.4 m member puts BOTH y=+/-11 bay loads at one midspan point and
# treats the +/-7 and +/-14 planes as simple supports (x=10 sits 3 m from 7
# and 4 m from 14, NOT midway); the real comparison load path - two separated
# saddle loads collected by transverse structure into the planes - is NOT
# drawn and its connecting stock is unpriced. The figure below is member
# stock under that simplification, not an established physical saving.
SPREAD_LEN, SPREAD_SUPP = 7.4, 7.0
P_frame = 2 * W_BAY_KN                    # both bays of one frame station, kN
M_spread = P_frame * SPREAD_SUPP / 4      # both saddles at midspan, kN*m
S_req_spread = M_spread * 1e3 / (SIG_ALLOW * 1e6)
SPR_CAND = [(0.40, 0.70, 0.014), (0.45, 0.80, 0.016), (0.50, 0.90, 0.020)]
spr_h, spr_b, spr_t = next(d for d in SPR_CAND if box_S(*d)[0] >= S_req_spread)
SPR_S, spr_mass_pm = box_S(spr_h, spr_b, spr_t)
SPREAD_T = spr_mass_pm * SPREAD_LEN + 0.06    # + gussets/end fittings, t
print(f"\nIII. member statics (convention: quasi-static 1 g, FS {FS} in the "
      f"{SIG_ALLOW:.0f} MPa allowable; supports = pickup points)")
print(f"    full bay {BAY_LOADED_T:.2f} t = {W_BAY_KN:.0f} kN; saddle beam "
      f"{SADDLE_LEN} m long, {SADDLE_SUPP} m support span, UDL -> M = "
      f"{M_saddle:.0f} kN*m, S req {S_req_saddle*1e6:.0f} cm3 -> box "
      f"{sad_h*1000:.0f}x{sad_b*1000:.0f}x{sad_t*1000:.0f} mm (S {SAD_S*1e6:.0f} "
      f"cm3, {sad_mass_pm*1000:.1f} kg/m) -> {SADDLE_T*1000:.0f} kg/saddle incl "
      f"pads; pickups 2 x {W_BAY_KN/2:.0f} kN each bay")
print(f"    x=+/-14 STATION (chosen): saddles tie directly into the declared "
      f"curtain planes at x = +/-14 (two-ended pickups per bay) - NO auxiliary "
      f"spreader; the load path is saddle -> pickup fitting -> curtain plane -> "
          f"envelope attachment (attachment qualification UNKNOWN)")
print(f"    x=+/-10 COMPARISON (I012's fixed station; SIMPLIFIED SCALAR BEAM, "
      f"not a drawn load path): no curtain plane at 10 -> a transverse "
        f"X-spreader modelled from the +/-7 and +/-14 planes with both "
        f"saddles at midspan (x=10 is 3 m from the 7 plane, 4 m from 14 - "
        f"NOT midway; the separated real pickups need transverse collection "
        f"that is unpriced): P = {P_frame:.0f} kN, M = {M_spread:.0f} kN*m, "
        f"S req {S_req_spread*1e6:.0f} cm3 -> box "
        f"{spr_h*1000:.0f}x{spr_b*1000:.0f}x{spr_t*1000:.0f} mm "
        f"({spr_mass_pm*1000:.0f} kg/m) -> {SPREAD_T*1000:.0f} kg/station of "
        f"MEMBER STOCK under that simplification; TWO stations")
print(f"    the earlier DERIVED {2*SPREAD_T:.2f} t station-SAVING claim is "
        f"WITHDRAWN as an established physical saving: the figure is the "
        f"simplified beam's member stock, conditional on the declared curtain "
        f"planes AND on an undrawn connecting load path (I012's README had "
        f"ASSUMED ~0.4 t; neither number is an established saving); if the "
        f"real planes sat at +/-10 instead, the +/-14 stations would need "
        f"~2 x {SPREAD_T:.2f} t of such members (a {4*SPREAD_T:.1f} t swing); "
        f"I003 carries the curtain as an undrawn 3 t allowance")
R_full = W_BAY_KN / 2
mis_t = 25.0 * MISMATCH            # rate-only endpoint (zero start skew)
# F7: skew-inclusive retained-mass bound under the declared linear law - the
# lagging bay starts SKEW_S late and drains (1-MISMATCH) slower; when the
# leader empties at T_DRAIN_S the laggard still holds
#   25 - (1-MISMATCH)*(25/T)*(T-delta) = 25*(MISMATCH+(1-MISMATCH)*delta/T)
# endpoints through the chosen delivery: delta=0 -> 1.25 t (rate-only);
# delta=2 s -> the bound below. Propagates to moments/authority/trim below.
mis_bound_t = 25.0 * (MISMATCH + (1.0 - MISMATCH) * SKEW_S / T_DRAIN_S)
dW_mis = mis_bound_t * 9.81        # added water at the lagging bay, kN
dR_mis = dW_mis / 2                # F5: symmetric saddle UDL -> each support
                                   # +dW/2; support-to-support DIFFERENCE 0
                                   # (no eccentricity declared; the earlier
                                   # ~8 kN width-lever "end unbalance" is
                                   # withdrawn)
print(f"    load cases on the chosen members (reactions per pickup): full bays "
          f"{R_full:.0f} kN; bounded release mismatch ({mis_bound_t:.2f} t "
          f"retained at the lagging bay, rate + 2 s skew): +{dR_mis:.1f} kN at "
          f"EACH of that bay's two pickups (symmetric UDL -> equal dW/2 "
          f"reactions, total +{dW_mis:.1f} kN, support-to-support difference 0 "
          f"- the earlier ~8 kN width-lever end-unbalance figure is WITHDRAWN); "
          f"one bay empty: its "
          f"saddle falls to shell weight (~{BAY_T*9.81:.0f} kN total), the full "
          f"pairmate unchanged {R_full:.0f} kN - endpoint interface loads are "
          f"these same reactions into curtain fittings (qualification UNKNOWN, "
          f"bonds/certificates UNRESOLVED - fitting hardware priced, attachment "
          f"not)")

# --- IV. priced hardware set (every load-path part a line or declared) --------
HW = [
    ("drawn bay shells 4x (plates+baffles+rims+fitout)", 4 * BAY_T),
    ("cradle saddles 4x (box {sad} mm, pads, lugs)".format(
        sad=f"{sad_h*1000:.0f}x{sad_b*1000:.0f}x{sad_t*1000:.0f}"), 4 * SADDLE_T),
    ("pickup fittings 8x (clevis + bonded socket)", 8 * PICKUP_T),
    ("bay tie rods (pair spacing/orientation)", 0.05),
    ("isolation valves+actuators 4x DN300 (declared +/-50%)", 4 * 0.035),
    ("D1 bottom door sets 2x (hinges, locks, actuators, decl.)", 2 * 0.080),
    ("matched orifice plates + positioners 4x", 0.06),
    ("internal piping DN300 Al ~30 m + supports", 0.41),
    ("water cross-pump (carried)", 0.35),
    ("ballonet air ducts + fans (carried)", 0.75),
    ("trim controls, wiring, instrumentation (carried)", 0.30),
    ("fasteners, bonds, lugs at interfaces (declared)", 0.10),
    ("keel corridor grating + handrails (declared)", 0.20),
]
HW_T = sum(v for _, v in HW)
REPLACED_T = 2.34
EQUIP_T = EQUIP_I007_T - REPLACED_T + HW_T
DRY_T = GAS_HULL_T + EQUIP_T
DRY_EX_FUEL = DRY_T - FUEL_T
LOADED_T = DRY_T + PAYLOAD_T
N0 = LOADED_T / LIFT_PER_KM3 * 1000.0
N_MAX = V * RHO_25 / RHO_SL
margin_hw = lift_of(N_MAX) - LOADED_T
margin_ideal = lift_of(N_MAX) - (LOADED_T - HW_T + REPLACED_T)
print(f"\nIV. priced hardware set (derived; declared lines marked +/-50%)")
for name, val in HW:
    print(f"    {name:<52} {val:5.2f} t")
print(f"    TOTAL drawn set {HW_T:5.2f} t vs I012's allowance set "
      f"{I012['HW']:.2f} t ({HW_T - I012['HW']:+.2f} t: thin-plate drawn tanks "
      f"and saddle beams replace lumped 48 kg/m3 shells + a 1.60 t frame "
      f"allowance) -> equipment {EQUIP_T:.2f} t, DRY {DRY_T:.2f} t, LOADED "
      f"{LOADED_T:.2f} t; margin at max inventory {margin_hw:+.2f} t "
      f"(I012 {I012['MARGIN']:+.2f}; massless ideal bound {margin_ideal:+.2f} t)")

# --- V. corrected-ledger rerun (dry mass cancels from the neutral vent) -------
n_after_d1_neutral = (DRY_EX_FUEL + fuel_at(t_d1) + 50.0) / LIFT_PER_KM3 * 1000.0
N1 = max(n_after_d1_neutral, N_FLOOR)
vent_m3 = N0 - N1
vent_he_t = vent_m3 * RHO_SL * MIX_FRAC / 1000.0 * HE_MASS_FRAC
vent_identity = (LOADED_T - (DRY_EX_FUEL + fuel_at(t_d1) + 50.0)) \
    / LIFT_PER_KM3 * 1000.0
SCOOP_T = lift_of(N1) - DRY_EX_FUEL - fuel_at(t_d2 + t_ex)
# floor-crossover: the D1 neutral touches the SL floor when dry mass drops to
# dry_star (below it, the vent is floor-capped again as in I007)
dry_ex_star = N_FLOOR / 1000 * LIFT_PER_KM3 - 50.0 - fuel_at(t_d1)
dry_star = dry_ex_star + FUEL_T
hw_star = dry_star - GAS_HULL_T - (EQUIP_I007_T - REPLACED_T)
print(f"\nV. ledger rerun on the drawn set (states as I012; identities shown)")
print(f"    n0 = {N0:,.0f} m3 (SL); D1 neutral n1 = {N1:,.0f} m3 "
      f"({N1 - N_FLOOR:,.0f} m3 above the SL floor - I012 cleared "
      f"{I012['N1'] - N_FLOOR:,.0f}: the LIGHTER drawn set lowers n1 toward the "
      f"floor; the floor re-binds below DRY = {dry_star:.2f} t, i.e. a drawn "
      f"set under {hw_star:.2f} t (ours is {HW_T:.2f} t)")
print(f"    vent = n0 - n1 = {vent_m3:,.0f} m3 = {vent_he_t:.2f} t He; identity: "
      f"vent = (50 t D1 delivery + burn to D1)/1.02405 = {vent_identity:,.0f} m3 "
      f"- DRY MASS CANCELS (the drawn set changes the vent only through the "
      f"crossover, not in size); scoop {SCOOP_T:.1f} t likewise dry-independent")

# --- S7: the reset operation COMPUTED from S6 arrival + named operations ---
# (twice-corrected I012 law, inherited): lifting He and lifting air derived
# SEPARATELY by species arithmetic in the lifting-mixture compartment (air
# admitted to a ballonet alone would not restore mixture air); ballonet air
# stays a separate derived inventory; fuel/payload/ballast derived from their
# named reset operations. The assertions below consume these computed values.
vent_he_v3 = vent_he_t * 1000.0 / (RHO_SL * 4.0026 / 28.9644)
vent_air_v3 = vent_m3 - vent_he_v3
HE_VF = 0.97                       # declared 97/3 STP-volume mixture
n_he_s6, n_air_s6 = N1 * HE_VF, N1 * (1.0 - HE_VF)
n_he_s7 = n_he_s6 + vent_he_v3     # + purchased He (the only He buy)
n_air_s7 = n_air_s6 + vent_air_v3  # + replenishment air to the MIXTURE
N_S7 = n_he_s7 + n_air_s7          # computed; NOT an assigned N0
refuel_t = FUEL_T - fuel_at(t_base)
FUEL_S7 = fuel_at(t_base) + refuel_t
PUMP_OUT_T = SCOOP_T               # named pump-out of all scooped ballast
SC_S7 = SCOOP_T - PUMP_OUT_T       # derived: all ballast gone
RELOAD_EACH = PAYLOAD_T / 2.0      # named reload, 50 t per delivery pair
t_s7 = t_base + 45.0 / 60.0        # EARLIEST ops-complete (pump-out only)
states = [
    ("S0 mast release, SL", 0.00, dict(P1=50.0, P2=50.0), N0, 0.0),
    ("S1 top of climb", 0.50, dict(P1=50.0, P2=50.0), N0, 2500.0),
    ("S2 zone A arrival", 2.50, dict(P1=50.0, P2=50.0), N0, 2500.0),
    ("S3 D1 done (50 t)", t_d1, dict(P1=0.0, P2=50.0), N1, 2500.0),
    ("S4 zone B arrival", t_d2, dict(P1=0.0, P2=50.0), N1, 2500.0),
    ("S4.5 exchange mid", t_d2 + t_ex / 2, dict(P1=0.0, P2=25.0), N1, 2500.0),
    ("S5 exchange done", t_d2 + t_ex, dict(P1=0.0, P2=0.0), N1, 2500.0),
    ("S6 base arrival, SL", t_base, dict(P1=0.0, P2=0.0), N1, 0.0),
    # S7: the reset operation's CHECKED end state, COMPUTED from the S6
    # arrival row plus the named reset operations (species arithmetic in the
    # block above): ballast pumped out, He + air restored to the MIXTURE by
    # species, fuel refilled, 100 t reloaded. Its clock is the EARLIEST
    # ops-complete (~45 min pump-out after S6; replenishment/load durations
    # UNKNOWN, moored - outside the 6.00 h flight envelope).
    ("S7 reset checked (=S0)", t_s7,
     dict(P1=RELOAD_EACH, P2=RELOAD_EACH, fuel=FUEL_S7, sc=SC_S7), N_S7, 0.0),
]
AIR_SPLIT = 0.5
print(f"    {'state':<24}{'t_h':>5}{'fuel':>6}{'pay':>5}{'air_t':>7}{'n_m3':>8}"
      f"{'bag%':>6}{'lift':>7}{'weight':>8}{'resid':>7}")
maxbag = 0.0
maxres = -99.0
w_hist, n_hist = [], []
for label, t, w, n, z in states:
    fuel = w["fuel"] if "fuel" in w else fuel_at(t)
    p1, p2 = w["P1"], w["P2"]
    air = m_air(n, z)
    disc = rho_at(z) * V / 1000.0
    lift = disc - air - n * RHO_SL * MIX_FRAC / 1000.0
    if "sc" in w:                      # explicit override (the reset state)
        sc = w["sc"]
    elif t <= t_d2:                    # scoop ramps through the D2 exchange only
        sc = 0.0
    else:
        scoop_full = lift_of(N1) - DRY_EX_FUEL - fuel_at(t_d2 + t_ex)
        sc = min((t - t_d2) / t_ex, 1.0) * scoop_full
    w_tot = DRY_EX_FUEL + fuel + p1 + p2 + sc
    w_hist.append(w_tot)
    n_hist.append(n)
    resid = lift - w_tot
    if abs(resid) < 1e-6:
        resid = 0.0
    vb = v_bag(n, z)
    maxbag = max(maxbag, vb / V)
    maxres = max(maxres, resid)
    assert abs((disc - air - n * RHO_SL * MIX_FRAC / 1000.0 - DRY_EX_FUEL
                - fuel - p1 - p2 - sc) - resid) < 1e-9, label
    print(f"    {label:<24}{t:>5.2f}{fuel:>6.2f}{p1 + p2:>5.0f}{air:>7.1f}"
          f"{n:>8,.0f}{vb / V:>6.1%}{lift:>7.1f}{w_tot:>8.1f}{resid:>+7.2f}")
print(f"    max bag {maxbag:.1%} at base arrival (cap margin "
      f"{(BALLONET_CAP/V) - maxbag:.1%}; I012 {I012['MAXBAG']:.1%} - the lighter "
      f"set lifts n1's slack: LESS cap margin, LESS floor clearance); residuals "
      f"light-side max {maxres:+.2f} t (I012 {I012['MAXRESID']:+.2f})")
# twice-corrected I012 checked reset (inherited): the assertions CONSUME the
# computed reset inventories - a missing species addition, short refuel or
# missed reload breaks them; they never compare an assigned target to itself.
# Explicit tolerances: inventory/species m3 STP, composition relative, weight t.
assert abs(N_S7 - N0) < 1.0, "reset inventory must reproduce S0"
assert abs(n_he_s7 / N_S7 - HE_VF) < 1e-3, "reset composition 97/3"
assert abs(n_he_s7 - N0 * HE_VF) < 5.0, "lifting He restored"
assert abs(n_air_s7 - N0 * (1.0 - HE_VF)) < 5.0, "lifting air restored"
assert abs(w_hist[-1] - w_hist[0]) < 1e-6, "reset weight must equal S0"
assert abs(n_hist[-1] - n_hist[0]) < 1.0, "reset ledger row must equal S0"
print(f"    reset (S7, checked, COMPUTED): species arithmetic on the arrival "
      f"mixture + the two named replenishments ({vent_he_v3:,.0f} m3 STP He "
      f"purchased + {vent_air_v3:,.0f} m3 STP air to the MIXTURE compartment) "
      f"-> n_S7 = {N_S7:,.0f} m3, asserted = S0's n0 at 97/3 with both species "
      f"asserted; fuel {FUEL_S7:.2f} t (arrival + {refuel_t:.2f} t refuel), "
      f"ballast pumped out, 100 t reloaded; ops complete no earlier than "
      f"t = {t_s7:.2f} h (~45 min pump-out; replenishment/load durations "
      f"UNKNOWN, moored)")

# --- VI. occupancy: ideal unobstructed-volume convention (fit UNKNOWN) --------
# F2/F3: the earlier "conservative bag-plane envelope" (plane at z=-3.1 m,
# 14.1 m separation, 26.3 m sufficient span, fit "conditional") is WITHDRAWN.
# The scalar ledger allocates ALL of V between lifting mixture and ballonet
# air (mixture + v_bag = V identically) with NOTHING reserved for the four
# tank envelopes or equipment - placing tanks below the bag plane does NOT
# reserve them from mixture volume. And the span bound itself used the FULL
# midbody circle R across spans that enter the hemispherical caps, where the
# section is smaller: each declared 40 m bag at x = +/-25 covers |x| 5..45,
# but the midbody ends at LC/2 = 27.45 m, so ~17.6 m of the bag sits in the
# caps (25 + 26.3/2 > LC/2 puts even the proposed minimum span into them).
# Membrane shape/drape is UNKNOWN regardless. Physical disjoint occupancy and
# bag-plane fit under the drawn capsule are UNKNOWN, not conditionally closed.
bag_envelope_m3 = 4 * BAY_L * BAY_W * BAY_H
print(f"\nVI. occupancy (ideal unobstructed-volume convention; fit WITHDRAWN)")
print(f"    the ledger allocates ALL of V between mixture and ballonet with "
      f"NOTHING reserved: the four tank OUTSIDE envelopes alone are "
      f"{bag_envelope_m3:.1f} m3 (4 x {BAY_L*BAY_W*BAY_H:.1f}), equipment and "
      f"routes undrawn beyond them - every scalar result here is an IDEAL-"
      f"UNOBSTRUCTED-VOLUME bound (twice-corrected I012 convention), and tanks "
      f"placed below the bag plane are NOT thereby reserved from mixture")
print(f"    the bag-plane fit demonstration is WITHDRAWN: each declared "
      f"{BAG_SPAN_M:.0f} m bag at x = +/-{X_BAG_C:.0f} covers |x| "
      f"{X_BAG_C - BAG_SPAN_M/2:.0f}..{X_BAG_C + BAG_SPAN_M/2:.0f}, but the "
      f"midbody ends at LC/2 = {LC/2:.2f} m, so "
      f"{(X_BAG_C + BAG_SPAN_M/2) - LC/2:.1f} m of it sits in the smaller "
      f"hemispherical-cap sections - the earlier bound used the full circle R "
      f"throughout and its z=-3.1 m plane / 14.1 m separation / 26.3 m "
      f"sufficient span are NOT established; membrane shape and drape over "
      f"structure are UNKNOWN (I006/I010 do not establish the P-100 "
      f"interface); physical disjoint occupancy is UNKNOWN")
print(f"    declared interface data retained: stations between the columns "
      f"(|x| < {X_BAG_C - BAG_SPAN_M/2:.0f}) and outboard of "
      f"+/-{(X_BAG_C + BAG_SPAN_M/2):.0f} see no bag on the declared span - "
      f"gondola, fuel tanks (x=+/-3), winch sit in that bag-free zone (a "
      f"placement statement on declared data, not an occupancy proof)")

# --- VII. moments, reactions, finite trim (twice-corrected-I012 laws) --------
mx_mis = mis_bound_t * Y_BAY            # roll (y-arm), skew-inclusive bound
my_mis = mis_bound_t * abs(X_STATIONS[0])   # pitch (x-arm)
mx_obe = 25.0 * Y_BAY
my_obe = 25.0 * abs(X_STATIONS[0])
LEVER = 50.0
def auth_net(n, z):
    """One-direction ballonet PITCH authority, twice-corrected I012 law
    (inherited): bounded by BOTH the donor bag's air AND the receiving bag's
    headroom under the separate 55,000 m3 per-bag capacity (the receiver
    bound governs whenever the state bag exceeds 25% of V); displaced
    mixture nets x (1 - MIX_FRAC). State-specific, never a craft constant."""
    v_donor = v_bag(n, z) * AIR_SPLIT
    v_move = min(v_donor, BALLONET_CAP / 2.0 - v_donor)
    return v_move * rho_at(z) / 1000.0 * LEVER * (1.0 - MIX_FRAC)
def gross_at(t, water, n, z):
    mix = n * RHO_SL * MIX_FRAC / 1000.0
    return DRY_EX_FUEL + fuel_at(t) + water + mix + m_air(n, z)
# the three disturbance datums on the I017 masses (own inventories)
t_obe = 2.575
n_obe = (DRY_EX_FUEL + fuel_at(t_obe) + 75.0) / LIFT_PER_KM3 * 1000.0
DATUMS17 = [
    ("min air (n0 @2500)", 2.50, 100.0, N0, 0.0, 0.0),
    ("D1-end mismatch", t_d1, 50.0 + mis_bound_t, N1, my_mis, mx_mis),
    ("one bay empty mid-D1", t_obe, 75.0, n_obe, my_obe, mx_obe),
]
FAN_TPM = 1.0   # t/min declared +/-50%, UNKNOWN real capability
# F6: required transfer carries the SAME (1-MIX_FRAC) netting the authority
# law uses (the earlier demand/50 m figure understated the transfer); the
# transfer is additionally bounded by the receiving-bag headroom (inherited).
t_resp_mis = my_mis / (LEVER * (1.0 - MIX_FRAC)) / FAN_TPM
print(f"\nVII. moments, reactions, finite trim (twice-corrected-I012 laws)")
print(f"    bounded release mismatch {mis_bound_t:.2f} t at (x=+/-14, "
      f"y=+/-11) - +/-{MISMATCH:.0%} rate WITH the allowed {SKEW_S:.0f} s pair "
      f"start skew under the declared linear drain (endpoints: {mis_t:.2f} t "
      f"rate-only at zero skew, {mis_bound_t:.2f} t at the allowed skew): roll "
      f"{mx_mis:.1f} t*m (I012's rate-only 13.8), pitch {my_mis:.1f} t*m "
      f"(I012 12.5 rate-only - the 14 m station grows the pitch arm 40%); "
      f"one bay empty: roll "
      f"{mx_obe:.0f} t*m (= I012), pitch {my_obe:.0f} t*m (I012 250, +40%)")
print(f"    {'datum':<24}{'n_m3':>9}{'air_t':>7}{'gross':>8}"
      f"{'pitch_dem':>10}{'auth_net':>9}{'covers':>8}")
for label, t, water, n, pd_, _rd in DATUMS17:
    g_ = gross_at(t, water, n, 2500.0)
    an_ = auth_net(n, 2500.0)
    print(f"    {label:<24}{n:>9,.0f}{m_air(n, 2500.0):>7.1f}{g_:>8.1f}"
          f"{pd_:>10.1f}{an_:>9.1f}"
          f"{'yes' if an_ > pd_ else 'NO':>8}")
print(f"    authority is the corrected ONE-DIRECTION NET law, bounded by BOTH "
      f"donor inventory AND receiving-bag headroom under the separate "
      f"{BALLONET_CAP/2:,.0f} m3 per-bag capacity (donor bag at the 50/50 "
      f"datum, displaced mixture nets x(1-{MIX_FRAC:.6f}); the receiver bound "
      f"governs at datums whose bag exceeds 25% of V - the D1-end datum here) "
      f"- the whole-inventory figure is withdrawn I012 law and is not used "
      f"here; the earlier donor-only {1548.8:.1f} t*m at the mismatch datum "
      f"was NOT an installed capacity and is superseded by the bounded row "
      f"above; I012 twice-corrected values at the same datums: "
      f"{I012['AUTH_MINAIR']:.2f} min-air / {I012['AUTH_MISMATCH']:.1f} "
      f"mismatch / {I012['AUTH_ONEEMPTY']:.1f} one-empty")
print(f"    coverage, per state: the mismatch pitch {my_mis:.1f} t*m is "
      f"covered at its own datum; the one-bay-empty pitch {my_obe:.0f} t*m is "
      f"covered at the neutral one-empty datum (larger air) but EXCEEDS the "
      f"min-air one-direction bound - same structure as corrected I012 "
      f"(250 vs {I012['AUTH_MINAIR']:.2f}), and the ratio "
      f"{my_obe / auth_net(N0, 2500.0):.2f} here vs "
      f"{I012['MY_OBE'] / I012['AUTH_MINAIR']:.2f} there: the 14 m arm grows "
      f"the demand, the lighter kit grows the min-air air inventory - net "
      f"marginally LESS exposed; recovery at the min-air datum (concurrent "
      f"vent, thrust, ballast) UNKNOWN; transient response NOT established")
print(f"    release law (declared): orifice drain is sqrt-head, front-loaded; "
      f"BOUND modelled as linear over ~9 min with rate mismatch +/-5% and door "
      f"opening <= 5 s with <= 2 s pair start skew - NO free perfect "
      f"simultaneous release; valve spec UNQUALIFIED (matched orifices are a "
      f"declared tolerance, not a purchased spec)")
print(f"    finite trim: countering pitch {my_mis:.1f} t*m needs "
      f"{t_resp_mis:.3f} t of air shifted over the 50 m lever net of the "
      f"{MIX_FRAC:.6f} mixture fraction ({my_mis:.1f}/50/(1-{MIX_FRAC:.6f}) - "
      f"the earlier /50 figure understated it; additionally bounded by the "
      f"receiving bag's headroom, inherited) -> {t_resp_mis * 60:.0f} s at the "
      f"declared {FAN_TPM} t/min (drain ~9 min; fan energy falls under the "
      f"corrected-I012 PARTIAL budget - 3.92 MJ per t at 1.5 kPa/40% covers "
      f"the LISTED subset only, reset-air and other work UNKNOWN, closure "
      f"UNKNOWN); STATIC capacity shown, transient "
      f"control NOT proven (fan capability, gust coupling, slosh unmodelled)")
for label, t, water, n, pd_, rd_ in DATUMS17:
    if not rd_:
        continue
    g_ = gross_at(t, water, n, 2500.0)
    pend = g_ * 25.0
    print(f"    roll at '{label}': pendulum {pend:,.0f} t*m/rad ({g_:.1f} t "
          f"STATE gross x 25 m) -> heel {math.degrees(rd_ / pend):.2f} deg "
          f"(I012 corrected {I012['HEEL_BOUND']:.2f} bound / "
          f"{I012['HEEL_WORST']:.2f} one-empty; rigid hull; envelope heel "
          f"limit UNKNOWN, I006)")

# --- VIII. carried schedule/fuel envelope + economics -------------------------
reserve_t = fuel_at(t_base)
short33 = BURN_TPH * (t_base + 0.55) - FUEL_T
pump_lo = 0.6
t_a = SCOOP_T / pump_lo
t_fix = t_a
for _ in range(8):
    t_fix = t_a + BURN_TPH * (t_fix - t_ex * 60) / 60.0 / pump_lo
short_lo = BURN_TPH * (t_base + (t_fix - t_ex * 60) / 60.0) - FUEL_T
m3_stp = vent_he_t * 1000.0 / (RHO_SL * 4.0026 / 28.9644)
ratio = m3_stp / 100.0 * HE_PRICE_BASE / FIREBOSS_PER_T
print(f"\nVIII. carried envelope and economics (unchanged laws, restated)")
print(f"    fuel: zero slack - 4.902246 t consumable buys exactly 6.00 h with "
      f"the 0.204260 t reserve; +33 min -> SHORT {short33:.6f} t; -50% pump "
      f"(scoop {SCOOP_T:.1f} t alone {t_a:.6f} min, coupled {t_fix:.6f} min, "
      f"base {t_base + (t_fix - t_ex*60)/60.0:.6f} h) -> SHORT {short_lo:.6f} t; "
      f"both fuel FAIL / outside the 6.00 h / +15 min envelope; covering priced, "
      f"NOT taken (unselected extra fuel/tank capacity remains a scenario)")
print(f"    economics: {vent_he_t:.2f} t He = {m3_stp:,.0f} m3 STP per 100 t -> "
      f"${m3_stp/100*HE_PRICE_BASE:,.0f}/t at the USGS base = {ratio:.1f}x the "
      f"$169/t SEAT comparator; reversal ${FIREBOSS_PER_T/(m3_stp/100):.2f}/m3; "
      f"retained FAIL (I012 8.36 t / 35.1x - unchanged, dry mass cancels)")

# --- IX. sensitivity (named lines incl. geometric-volume) ----------------------
print(f"\nIX. sensitivity (margin at max inventory {margin_hw:+.2f} t)")
for name, delta in [
        ("fitout/valves/doors +50% (declared lines)", -(4 * fitout_t + 4 * 0.035 + 2 * 0.08) * 0.5),
        ("curtain planes actually at +/-10 (delta reverses)", -2 * SPREAD_T),
        ("curtain misaligned +/-3.5 m (spreader 10.5 m x2)", -2 * (spr_mass_pm * 10.5 + 0.06)),
        ("plate 3 -> 5 mm (handling/corrosion doubling)", -(plate_area * 0.002 * RHO_AL) * 4),
        ("occupancy/bag fit (withdrawn, UNKNOWN)", 0.0),
        ("I007 sundries +50% (carried)", -9.82),
        ("endurance 6 -> 12 h (carried)", -FUEL_T),
        (f"lift on {V_DRAWN:,.0f} m3 not the anchor (DRAWN-VOLUME)",
         -(V - V_DRAWN) / 1000.0 * RHO_25 / RHO_SL * LIFT_PER_KM3),
]:
    if name.startswith("occupancy"):
        print(f"    {name:<46} UNKNOWN (not a mass line)")
    else:
        print(f"    {name:<46} {delta:+7.2f} t -> margin {margin_hw + delta:+7.2f} t")
n_max_drawn = V_DRAWN * RHO_25 / RHO_SL   # mixture ceiling on the capsule
dv_loss = lift_of(N_MAX) - lift_of(n_max_drawn)
floor_drawn = V_DRAWN - BALLONET_CAP
print(f"    DRAWN-VOLUME detail: every lift above uses the recorded "
      f"{V:,.0f} m3 anchor; the drawn capsule is {V_DRAWN:,.0f} m3 "
      f"({(V_DRAWN/V-1)*100:.1f}%). Mixture lift is hull-independent "
      f"(lift = n x {LIFT_PER_KM3:.5f} t per km3), so n0, the {vent_m3:,.0f} m3 "
      f"vent and the {SCOOP_T:.1f} t scoop do NOT change on the capsule; what "
      f"changes is the ceiling - max inventory {n_max_drawn:,.0f} m3 -> max lift "
      f"{lift_of(n_max_drawn):.2f} t ({-dv_loss:.2f} t vs anchor) - and the SL "
      f"floor drops to {floor_drawn:,.0f} m3, which n1 clears by "
      f"{N1 - floor_drawn:,.0f} m3 (MORE than the anchor's {N1-N_FLOOR:,.0f}: "
      f"the cap, not the hull volume, binds); displacement is NOT silently "
      f"added - this is the named geometric-volume sensitivity and it alone "
      f"consumes {dv_loss:.2f} t of margin")

# --- X. verdict + drawing ------------------------------------------------------
print(f"\nX. verdict")
print(f"    GEOMETRY/OCCUPANCY: fit UNKNOWN (ideal-volume convention). Drawn tanks "
      f"3.05x3.05x2.85 m (usable {usable:.1f} m3 >= 25.0) at x=+/-14, "
      f"y=+/-11, upper row z={Z_UP} / lower z={Z_LOW} (diagonal, each pair at "
      f"one height); worst radial skin clearance {min_rad:.2f} m; corridors "
      f"and gondola clearances stated; the bag-plane fit demonstration is "
      f"WITHDRAWN (the earlier z=-3.1 m plane / 14.1 m separation / 26.3 m "
      f"sufficient-span bound used the full midbody circle into the caps - "
      f"~17.6 m of each declared {BAG_SPAN_M:.0f} m bag sits in the smaller "
      f"hemispherical-cap sections); every volume here is an IDEAL "
      f"UNOBSTRUCTED-VOLUME bound; physical disjoint occupancy, membrane "
      f"shape/drape and the I006/I010 interfaces UNKNOWN")
print(f"    LOAD PATH: priced under the SIMPLIFIED SCALAR BEAM model ({HW_T:.2f} t "
      f"vs I012's {I012['HW']:.2f} t allowance, {HW_T-I012['HW']:+.2f} t); "
      f"member stock {2*SPREAD_T:.2f} t total is the SIMPLIFIED-BEAM quantity "
      f"- the earlier claim that the x=+/-14 stations DERIVE {2*SPREAD_T:.2f} t "
      f"of station saving vs the fixed +/-10 arrangement is WITHDRAWN (a "
      f"derived difference needs member statics under the same declared "
      f"method at both arrangements, not the scalar simplification); member "
      f"M/S shown for full/mismatch/one-empty under the simplification; "
      f"envelope/curtain attachment qualification and bonds UNRESOLVED "
      f"(UNKNOWN)")
print(f"    TRIM: nominal zero-moment preserved; coverage per state under the "
      f"twice-corrected one-direction law bounded by donor inventory AND "
      f"receiver headroom - mismatch pitch {my_mis:.1f} t*m covered at its "
      f"datum ({auth_net(N1, 2500.0):.0f} t*m), one-bay-empty "
      f"{my_obe:.0f} t*m covered at the neutral one-empty datum "
      f"({auth_net(n_obe, 2500.0):.0f}) but EXCEEDING the min-air bound "
      f"({auth_net(N0, 2500.0):.0f}) - recovery there UNKNOWN, transient "
      f"control NOT proven; finite response {t_resp_mis*60:.0f} s "
      f"({t_resp_mis:.2f} t netted transfer) vs 9 min "
      f"drain at DECLARED fan rate; quasi-static only")
print(f"    MASS/MARGIN: DRY {DRY_T:.2f} t, margin {margin_hw:+.2f} t (I012 "
      f"{I012['MARGIN']:+.2f}); the lighter set trades floor clearance "
      f"({N1-N_FLOOR:,.0f} m3, was {I012['N1']-N_FLOOR:,.0f}) and cap margin "
      f"({(BALLONET_CAP/V)-maxbag:.1%}, was {(BALLONET_CAP/V)-I012['MAXBAG']:.1%}) "
      f"- the crossover to a floor-bound vent sits at DRY = {dry_star:.2f} t, "
      f"a drawn set under {hw_star:.2f} t (ours is {HW_T:.2f} t)")
print(f"    ECONOMICS/FUEL (carried, retained): vent {vent_he_t:.2f} t He "
      f"(dry-independent), {ratio:.1f}x SEAT FAIL; zero-slack envelope, both "
      f"off-nominal cases fuel FAIL ({short33:.6f} / {short_lo:.6f} t short)")
print(f"    weakest assumption: the declared curtain-plane stations (I003 "
      f"carries the suspension as an undrawn 3 t allowance) - the saddle load "
      f"path hangs on them and the member stock here is scalar-beam only; "
      f"next geometry change (one): draw the curtain fan itself - station "
      f"spacing, run angles and fitting loads from the envelope seam pattern - "
      f"which converts the member statics and the attachment UNKNOWN into "
      f"a drawn interface, then re-run the bag occupancy at the real ballonet "
      f"gore count")

print(f"\n== drawing (elevation at y=0 plane + section at x=+14 m; scales noted) ==")
for line in [
    "side elevation, keel zone only (x: nose left; z from hull centre; 1 char ~ 2.8 m)",
    "",
    "        ballonet bags above (plane NOT established) ---- full hull above ----",
    "  x=-21   x=-14          x=0               x=+14   x=+21   curtain planes",
    "    |    [B1-FL]      +----------+      [B4-AR]    |",
    "    |    z=-19 port   | gondola  |      z=-19 stbd |    (upper row: port",
    "    |    +saddle+     | x in [-3,3]      +saddle+  |     fore, stbd aft)",
    "    |    [B2-FR]      | fuel 2x  |      [B3-AL]    |",
    "    |    z=-21.5 stbd +----------+     z=-21.5 port|    (lower row swapped)",
    "    |         \\____ keel corridor ____/            |",
    "  ~~|~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~|~~  hull floor -27.5",
    "         hose/ducts/winch at z=-22.5 in the corridor",
    "",
    "section at x=+14 m (bow view; y+ = port/left; 1 char ~ 1.7 m)",
    "",
    "          z=0  ____________________",
    "          _,--'   (bags above - plane NOT established)   '--._",
    "       _,-'                                              '-,_",
    "     ,'          [B3-AL] y=+11, z=-21.5 (port LOW here)     ',",
    "    |             \\____/  3.05 m                            |",
    f"    |             | 25 t |   worst corner radial {min_rad:.2f} m     |",
    f"    |              \\____/    (y={Y_BAY + BAY_W/2:.2f}, z={Z_LOW - BAY_H/2:.2f})            |",
    "     ',        saddle -> pickup -> curtain plane x=+14      ,'",
    "       '-,_      [B4-AR] y=-11, z=-19.0 (stbd HIGH here) _,-'",
    "           '--..___ corridor |y|<9.5 to floor ___..--'",
    "                   keel: hose, ducts, winch (z=-22.5)",
]:
    print(line)
