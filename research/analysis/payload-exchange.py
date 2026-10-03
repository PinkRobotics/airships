#!/usr/bin/env python3
"""the payload-exchange study, from first principles. Shares no code with sim/.

ANALYSIS, NOT DESIGN. Every number in payload-exchange.md is a key in payload-exchange.json, written here.

Relations used (and nothing else):
  ISA troposphere   rho(h) = rho_SL (1 - L h/T0)^(g0/(R L) - 1); p(h) = P0 (1 - L h/T0)^(g0/(R L))   [sim/atmosphere.js L23-27; noaa-1976-us-standard-atmosphere]
  lift ledger       lift = disp rho / 1000 t; dry mass target = payload; empty surplus = lift - payload; loaded = lift - 2 payload
  momentum theory   hover P = T^1.5 / sqrt(2 rho A) / eta                                                [Johnson 1994; not in the catalogue]
  Glauert inflow    vi sqrt(V^2 + (vc + vi)^2) = T/(2 rho A); P = T (vc + vi) / eta                     [Glauert 1926 R&M 1111; not in the catalogue]
  lifting line      D_i = L^2 / (q pi b^2 e), span b = hull diameter                                      [Prandtl 1921 NACA TR 116; not in the catalogue]
  broadside drag    D = 0.5 rho C_D S vz^2, S = capsule planform, C_D = 1 (unverified; range 0..2)
  ideal gas         isothermal work to re-establish a vacuum of volume dV against ambient p: W = p dV
  added mass        m_eff = dry + k2 rho Vol, k2 from Munk 1924 NACA TR 184 (not in the catalogue)

Constants are copied from sim/config.js (classes L260-292, CFG L52-62, altitudes L103/L140) and docs/PHYSICS.md.
Phase durations and channel energies of the earlier tree (read-only run, 2026-10-02) and the
baseline's worst-instant records (baseline/first-principles.json, letdown[]) are embedded as DATA, not code.
"""
import json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- class constants (sim/config.js)
CLASSES = {
  'P100':   dict(payloadT=100,   dispM3=220000, lenM=110, diaM=55,  diskM2=2500,   battMW=30,   genMW=8,   cryoMW=6,   solarM2=6000,   anchorBagT=125,   anchorM=350, fillM3s=0.5, cruiseKph=90,  battMWh=20),
  'P1000':  dict(payloadT=1000,  dispM3=2.2e6,  lenM=238, diaM=119, diskM2=12000,  battMW=150,  genMW=40,  cryoMW=30,  solarM2=28000,  anchorBagT=1250,  anchorM=600, fillM3s=3,   cruiseKph=110, battMWh=120),
  'P10000': dict(payloadT=10000, dispM3=2.2e7,  lenM=512, diaM=256, diskM2=160000, battMW=1400, genMW=150, cryoMW=100, solarM2=120000, anchorBagT=12400, anchorM=850, fillM3s=15,  cruiseKph=130, battMWh=2000),
}
ORDER = ['P100', 'P1000', 'P10000']
PUBLISHED_HULL = {'P100': (190, 47), 'P1000': (404, 102), 'P10000': (876, 219)}   # docs/PHYSICS.md: fineness 4, differ from config.js
PROP_ETA = 0.70; ETAS = (0.55, 0.70)                     # Efficiency assumption: 0.70 on ideal induced power, printed at 0.55 and 0.70
CD_ZERO_LIFT = 0.05                                       # config.js Cd on the frontal area
VERTICAL_CD = 1.0; VERTICAL_CD_RANGE = (0.0, 1.0, 2.0)    # unverified broadside coefficient, tested across the declared range
RHO_SL, T0, P0, LAPSE, G0, R = 1.225, 288.15, 101325.0, 0.0065, 9.80665, 287.0528
G = 9.81
TERRAIN_MSL, HOSE_M, DROP_AGL, WORK_ALT_MSL = 1000, 300, 450, 2500
ALT = dict(ground=TERRAIN_MSL, hold=TERRAIN_MSL + HOSE_M, drop=TERRAIN_MSL + DROP_AGL, work=WORK_ALT_MSL)
SOLAR_W_M2, HOTEL_FRAC, PUMP_ETA = 45, 0.02, 0.75
HOIST_M, WINCH_MPS, WINCH_ETA = 15, 5, 0.85
RHO_WATER = 1000.0
LN2_KWH_PER_T = {'optimumCollins_arnaizDelPozo2020': 430.7, 'config_eLN2': 450.0, 'standalone_rimpel2023': 907.0}
CRYO_T_PER_MW = {'floor': 2.0, 'credible': 20.0, 'demonstrated': 65.0}            # mass-budget.json EVIDENCE
BATT_WH_PER_KG = {'floor': 500, 'credible': 300, 'demonstrated': 149}             # battery specific energies from mass-budget.json EVIDENCE
ISOTHERMAL_PUMP_EFF = (0.30, 1.0)                                                  # mass-budget.py assumption, and ideal
ADDED_MASS_K2 = {2: 0.702, 4: 0.860}        # Munk TR 184 table: transverse additional-mass coefficient, fineness 2.00 and 3.99
MEASURED_CL = {                              # planform-basis conversions are this study's own (see md, step 2c)
  'akron_fins_20deg_vol23': 0.405, 'akron_bare_vol23_max': 0.115, 'akron_vol23_to_planform': None,
  'fineness4_finned_35p6deg_vol23_normal': 0.825, 'fineness4_finned_11p6deg_vol23_normal': 0.233,
  'hybridHull_slope_per_deg': 0.0067, 'hybridHull_zeroLiftDeg': -4.2,
}
CL_MEASURED_PLANFORM = (0.14, 0.34)   # from the conversions below (Akron, fins on, 20 deg; fineness-4 finned hull, 35.6 deg); the range this study treats as "measured"
CL_ASSUMED = (0.5, 1.0, 1.5)          # the earlier tree's AERO_CL_VALUES (assumptions, not tests)
E_SPAN = (1.0, 0.7)
TURN_RADIUS_LENGTHS = (1.0, 2.0, 3.0) # assumption: a hull turns no tighter than one to three lengths; no source
REVERSE_THRUST_FACTOR = (0.5, 0.8)    # assumption: power per tonne pushing UP vs pushing down, same disk; no source

# ---------------------------------------------------------------- earlier-tree DATA (read-only run, record basis, balanced, still air)
DUR = {  # minutes per phase
  ('P100', 15):   dict(SA=2, WF=3.3333, OUT=11.7647, WR=3.3333, BE=2, RET=11.7647),
  ('P100', 60):   dict(SA=2, WF=3.3333, OUT=47.0588, WR=3.3333, BE=2, RET=47.0588),
  ('P1000', 15):  dict(SA=3, WF=5.5556, OUT=9.6257, WR=5.5556, BE=2, RET=9.6257),
  ('P1000', 60):  dict(SA=3, WF=5.5556, OUT=38.5027, WR=5.5556, BE=2, RET=38.5027),
  ('P10000', 15): dict(SA=5, WF=11.1111, OUT=8.1448, WR=11.1111, BE=2, RET=8.1448),
  ('P10000', 60): dict(SA=5, WF=11.1111, OUT=32.5792, WR=11.1111, BE=2, RET=32.5792),
}
EARLIER = {  # cycle MWh, rotor channel MWh, worst unheld t (record basis)
  ('P100', 15): dict(cycleMWh=8.0422, rotorsMWh=6.6510, worstUnheldT=34.252, feasible=False, worstPhase='RETURN_TRANSIT'),
  ('P100', 60): dict(cycleMWh=19.6874, rotorsMWh=14.6888, worstUnheldT=0.0, feasible=True, worstPhase='SOURCE_APPROACH'),
  ('P1000', 15): dict(cycleMWh=62.4999, rotorsMWh=54.1610, worstUnheldT=868.561, feasible=False, worstPhase='SOURCE_APPROACH'),
  ('P1000', 60): dict(cycleMWh=140.6869, rotorsMWh=113.5462, worstUnheldT=816.828, feasible=False, worstPhase='SOURCE_APPROACH'),
  ('P10000', 15): dict(cycleMWh=697.5856, rotorsMWh=644.9394, worstUnheldT=7389.458, feasible=False, worstPhase='SOURCE_APPROACH'),
  ('P10000', 60): dict(cycleMWh=1111.3329, rotorsMWh=969.2823, worstUnheldT=7273.491, feasible=False, worstPhase='SOURCE_APPROACH'),
}
BASELINE_LEVERS = {('P1000', 15): dict(retainedT=869.190, deliveredT=130.810, kwhPerT=166.835),   # baseline, requirements table
                ('P1000', 60): dict(retainedT=817.441, deliveredT=182.559, kwhPerT=322.902),
                ('P10000', 15): dict(retainedT=7396.778, deliveredT=2603.222, kwhPerT=90.841),
                ('P10000', 60): dict(retainedT=7280.782, deliveredT=2719.218, kwhPerT=164.355)}
BASELINE_INSTANTS = [  # baseline/first-principles.json letdown[], tree A, record basis (trajectory data at the worst instant)
  dict(cls='P100', km=15, phase='RETURN_TRANSIT', x=0.8105, altAgl=883.168, vz=-8.823116, airV=25.0, surplusT=122.557082, bagT=0, rotorBusMW=24.451623, treeUnheldT=34.252145),
  dict(cls='P1000', km=15, phase='SOURCE_APPROACH', x=0.7305, altAgl=518.199, vz=-7.441801, airV=0.0, surplusT=1317.695270, bagT=0, rotorBusMW=134.646536, treeUnheldT=868.561162),
  dict(cls='P1000', km=60, phase='SOURCE_APPROACH', x=0.7305, altAgl=518.199, vz=-7.441801, airV=0.0, surplusT=1300.157252, bagT=0, rotorBusMW=146.774878, treeUnheldT=816.827563),
  dict(cls='P10000', km=15, phase='SOURCE_APPROACH', x=0.6768, altAgl=702.924, vz=-6.461992, airV=0.0, surplusT=12794.900081, bagT=0, rotorBusMW=1291.004612, treeUnheldT=7389.457648),
  dict(cls='P10000', km=60, phase='SOURCE_APPROACH', x=0.6768, altAgl=702.924, vz=-6.461992, airV=0.0, surplusT=12744.413126, bagT=0, rotorBusMW=1311.529499, treeUnheldT=7273.490624),
]
BASELINE_CAP_RHO110 = {'P100': 160.339, 'P1000': 790.861, 'P10000': 7599.734}   # baseline: hover thrust of the full bus at rho 1.10

# ---------------------------------------------------------------- the relations
RHO_EXP = G0 / (R * LAPSE) - 1

def rho_isa(h): return RHO_SL * (1 - LAPSE * h / T0) ** RHO_EXP
def p_isa(h): return P0 * (1 - LAPSE * h / T0) ** (G0 / (R * LAPSE))
def alt_for_rho(rho): return T0 / LAPSE * (1 - (rho / RHO_SL) ** (1 / RHO_EXP))
def planform(lenM, diaM): return diaM * (lenM - diaM) + math.pi * (diaM / 2) ** 2   # capsule, as the earlier tree
def frontal(diaM): return math.pi * (diaM / 2) ** 2
def lift_t(dispM3, h): return dispM3 * rho_isa(h) / 1000

def hover_mw(thrust_t, rho, A, eta=PROP_ETA):
    T = thrust_t * 1000 * G
    return T ** 1.5 / math.sqrt(2 * rho * A) / eta / 1e6 if T > 0 else 0.0

def glauert_mw(thrust_t, rho, A, vc=0.0, V=0.0, eta=PROP_ETA):
    """Rotor power pushing with thrust T while the air comes INTO the disk axially at vc (hold-down in descent)
    and edgewise at V. vc < 0 (climb against hold-down) is priced as level flight: no bound claimed."""
    T = thrust_t * 1000 * G
    if T <= 0: return 0.0
    vc = max(0.0, vc); V = abs(V)
    vh2 = T / (2 * rho * A)
    lo, hi = 0.0, math.sqrt(vh2)
    for _ in range(100):
        vi = (lo + hi) / 2
        if vi * math.sqrt(V * V + (vc + vi) ** 2) > vh2: hi = vi
        else: lo = vi
    return T * (vc + (lo + hi) / 2) / eta / 1e6

def thrust_at_power(mw, rho, A, vc=0.0, V=0.0, eta=PROP_ETA):
    """Inverse of glauert_mw: P eta = 2 rho A vi (vc + vi) sqrt(V^2 + (vc + vi)^2) is increasing in vi; bisect on vi,
    then T = 2 rho A vi sqrt(V^2 + (vc + vi)^2). At V = vc = 0 this is the closed form T = (P eta sqrt(2 rho A))^(2/3)."""
    if mw <= 0: return 0.0
    vc = max(0.0, vc); V = abs(V); Pe = mw * 1e6 * eta
    if V == 0 and vc == 0: return (Pe * math.sqrt(2 * rho * A)) ** (2 / 3) / (1000 * G)
    lo, hi = 0.0, (Pe / (2 * rho * A)) ** (1 / 3) + vc + V
    for _ in range(60):
        vi = (lo + hi) / 2
        if 2 * rho * A * vi * (vc + vi) * math.sqrt(V * V + (vc + vi) ** 2) > Pe: hi = vi
        else: lo = vi
    vi = (lo + hi) / 2
    return 2 * rho * A * vi * math.sqrt(V * V + (vc + vi) ** 2) / (1000 * G)

def disk_for(thrust_t, mw, rho, eta):
    """Disk area that holds thrust_t on mw of power at hover: A = T^3 / (2 rho (P eta)^2)."""
    T = thrust_t * 1000 * G
    return T ** 3 / (2 * rho * (mw * 1e6 * eta) ** 2)

def induced_drag_n(L_n, q, b, e): return L_n ** 2 / (q * math.pi * b * b * e) if q > 0 else float('inf')

def r(x, n=3): return None if x is None else (round(x, n) if isinstance(x, float) else x)

# ---------------------------------------------------------------- step 1: the problem per class
def problem(name, c):
    S, b = planform(c['lenM'], c['diaM']), c['diaM']
    Lp, Dp = PUBLISHED_HULL[name]
    out = dict(payloadT=c['payloadT'], dispM3=c['dispM3'], dryMassTargetT=c['payloadT'],
               hull=dict(config=dict(lenM=c['lenM'], diaM=c['diaM'], fineness=c['lenM'] / c['diaM'], planformM2=S, spanM=b, aspectRatio=b * b / S,
                                     frontalM2=frontal(c['diaM']), capsuleVolumeM3=math.pi*(c['diaM']/2)**2*(c['lenM']-c['diaM'])+4/3*math.pi*(c['diaM']/2)**3),
                         published=dict(lenM=Lp, diaM=Dp, fineness=Lp / Dp, planformM2=planform(Lp, Dp), spanM=Dp, aspectRatio=Dp * Dp / planform(Lp, Dp),
                                        ellipsoidVolumeM3=math.pi / 6 * Lp * Dp ** 2)),
               busMW=c['battMW'] + c['genMW'], batteryPlusSolarMW=c['battMW'] + c['solarM2'] * SOLAR_W_M2 / 1e6, diskM2=c['diskM2'],
               altitudes={})
    for key, h in ALT.items():
        rho = rho_isa(h); L = c['dispM3'] * rho / 1000
        out['altitudes'][key] = dict(mslM=h, aglM=h - TERRAIN_MSL, rho=rho, pressurePa=p_isa(h), liftT=L, emptySurplusT=L - c['payloadT'],
                                     loadedSurplusT=L - 2 * c['payloadT'], emptySurplusOverPayload=(L - c['payloadT']) / c['payloadT'])
    out['hull']['config']['volumeOverDesign'] = out['hull']['config']['capsuleVolumeM3'] / c['dispM3']
    rho_bal_e, rho_bal_l = c['payloadT'] * 1000 / c['dispM3'], 2 * c['payloadT'] * 1000 / c['dispM3']
    out['balance'] = dict(emptyRho=rho_bal_e, emptyAltMslM=alt_for_rho(rho_bal_e), loadedRho=rho_bal_l, loadedAltMslM=alt_for_rho(rho_bal_l))
    return out

# ---------------------------------------------------------------- the cycle sketch (this study's own, simplified; durations are earlier-tree data)
def cycle_sketch(name, c, km, keptT=0.0, disp=None, lenM=None, diaM=None, two_way=False, aero_cl=None, e_span=1.0, cd_vert=VERTICAL_CD,
                 eta=PROP_ETA, reverse_factor=1.0, steps=120, use_surrogate=True):
    """Integrates rotor hold-down (and lift, if two_way) along a simplified cycle: BE climb to work altitude, RET cruise,
    letdown to the hold altitude over the last 28% of RET plus SOURCE_APPROACH, WATER_FILL at hover with the bag, OUT cruise
    loaded, WATER_RELEASE at hover. Returns the rotor energy, peaks and the worst unheld force (sign: + = too light)."""
    P = c['payloadT']; disp = disp or c['dispM3']; lenM = lenM or c['lenM']; diaM = diaM or c['diaM']
    S, Af, A = planform(lenM, diaM), frontal(diaM), c['diskM2']
    d = DUR[(name, km)]; V_cr = c['cruiseKph'] / 3.6
    bus = c['battMW'] + c['genMW']; hotel = c['genMW'] * HOTEL_FRAC
    pumpMW = RHO_WATER * G * HOSE_M * c['fillM3s'] / PUMP_ETA / 1e6
    surrogate = thrust_at_power(bus, rho_isa(ALT['hold']), A, eta=eta) if use_surrogate else float('inf')
    reach = c['anchorM'] - diaM / 2
    moved = P - keptT                        # tonnes filled and released each cycle
    fill_min, rel_min = d['WF'] * moved / P, d['WR'] * moved / P
    phases = []  # (minutes, fn(s) -> (alt_msl, V, vz, water_t, bag_t, pumps_on))
    phases.append(('BE', d['BE'], lambda s: (ALT['drop'] + s * (ALT['work'] - ALT['drop']), V_cr / 2, (ALT['work'] - ALT['drop']) / (d['BE'] * 60), keptT, 0.0, False)))
    phases.append(('RET_cruise', 0.72 * d['RET'], lambda s: (ALT['work'], V_cr, 0.0, keptT, 0.0, False)))
    t_let = 0.28 * d['RET'] + d['SA']
    def letdown(s):
        alt = ALT['work'] - s * (ALT['work'] - ALT['hold']); V = V_cr * (1 - s); vz = -(ALT['work'] - ALT['hold']) / (t_let * 60)
        bag = c['anchorBagT'] if (alt - TERRAIN_MSL <= reach and V <= 2.0) else 0.0
        return (alt, V, vz, keptT, bag, False)
    phases.append(('LETDOWN', t_let, letdown))
    phases.append(('WF', fill_min, lambda s: (ALT['hold'], 0.0, 0.0, keptT + s * moved, c['anchorBagT'], True)))
    phases.append(('OUT', d['OUT'], lambda s: (ALT['hold'] + s * (ALT['work'] - ALT['hold']) if s < 0.3 else ALT['work'], V_cr, 0.0, P, 0.0, False)))
    phases.append(('WR', rel_min, lambda s: (ALT['drop'], 0.0, 0.0, P - s * moved, 0.0, False)))
    E = 0.0; peakMW = 0.0; worst = dict(unheldT=0.0); worst_up = dict(unheldT=0.0); per_phase = {}
    for pid, minutes, fn in phases:
        if minutes <= 0: continue
        Eph = 0.0; dt = minutes * 60 / steps
        for i in range(steps):
            s = (i + 0.5) / steps
            alt, V, vz, water, bag, pumps = fn(s)
            rho = rho_isa(alt); q = 0.5 * rho * V * V
            surplus = disp * rho / 1000 - P - water
            drag_t = 0.5 * rho * cd_vert * S * vz * abs(vz) / (1000 * G)      # + when climbing (acts down), - when descending (acts up)
            aero_t = aero_cl * q * S / (1000 * G) if (aero_cl and V > 0) else 0.0
            bag = min(bag, max(0.0, surplus - drag_t))                         # excess water is dumped, never a bag that pulls the hull under (as the earlier tree)
            need = surplus - bag - drag_t                                      # what the rotors (and aero) must hold DOWN; < 0 = must LIFT
            nonrotor = hotel + q * CD_ZERO_LIFT * Af * V / eta / 1e6 + (pumpMW if pumps else 0.0)
            induced_mw = 0.0
            if need > 0:
                held_aero = min(aero_t, need)
                if held_aero > 0: induced_mw = induced_drag_n(held_aero * 1000 * G, q, diaM, e_span) * V / eta / 1e6
                avail = max(0.0, bus - nonrotor - induced_mw)
                cap = min(thrust_at_power(avail, rho, A, max(0.0, -vz), V, eta), surrogate)
                rotor = min(need - held_aero, cap)
                mw = glauert_mw(rotor, rho, A, max(0.0, -vz), V, eta) + induced_mw
                unheld = need - held_aero - rotor
                if unheld > worst['unheldT']: worst = dict(unheldT=unheld, phase=pid, s=round(s, 3), altAgl=alt - TERRAIN_MSL, V=V, vz=vz, needT=need, rotorT=rotor, aeroT=held_aero, availMW=avail)
            elif two_way:
                avail = max(0.0, bus - nonrotor)
                cap = min(thrust_at_power(avail * reverse_factor, rho, A, max(0.0, vz), V, eta), surrogate)
                rotor = min(-need, cap)
                mw = glauert_mw(rotor, rho, A, max(0.0, vz), V, eta) / reverse_factor
                unheld = -need - rotor
                if unheld > worst_up['unheldT']: worst_up = dict(unheldT=unheld, phase=pid, s=round(s, 3), altAgl=alt - TERRAIN_MSL, needT=need, rotorT=rotor, availMW=avail)
            else:
                mw = 0.0
                if -need > worst_up['unheldT']: worst_up = dict(unheldT=-need, phase=pid, s=round(s, 3), altAgl=alt - TERRAIN_MSL, needT=need, note='heavy; the drawn rotors provide no upward authority')
            total = mw + nonrotor
            peakMW = max(peakMW, total)
            Eph += mw * dt / 3600
        per_phase[pid] = dict(minutes=minutes, rotorMWh=Eph)
        E += Eph
    cycle_min = sum(p[1] for p in phases)
    return dict(rotorMWh=E, peakBusMW=peakMW, worstUnheldDownT=worst, worstUnheldUpT=worst_up, perPhase=per_phase, cycleMin=cycle_min,
                deliveredT=moved, surrogateCapT=surrogate if use_surrogate else None)

def kept_to_close(name, c, km, **kw):
    """Smallest water kept aboard at which the sketch holds every instant (unheld <= 1 t), by bisection on 0..payload."""
    lo, hi = 0.0, c['payloadT']
    if cycle_sketch(name, c, km, keptT=hi, **kw)['worstUnheldDownT']['unheldT'] > 1.0: return None
    if cycle_sketch(name, c, km, keptT=lo, **kw)['worstUnheldDownT']['unheldT'] <= 1.0: return 0.0
    for _ in range(16):
        mid = (lo + hi) / 2
        if cycle_sketch(name, c, km, keptT=mid, **kw)['worstUnheldDownT']['unheldT'] > 1.0: lo = mid
        else: hi = mid
    return hi

# ---------------------------------------------------------------- step 2: the routes
def route_a(name, c, prob):
    hold = prob['altitudes']['hold']; rho, S, A, bus = hold['rho'], prob['hull']['config']['planformM2'], c['diskM2'], prob['busMW']
    Se = hold['emptySurplusT']
    out = dict(label='rotor hold-down as drawn', emptySurplusT=Se, byEta={})
    for eta in ETAS:
        cap_local, cap_110 = thrust_at_power(bus, rho, A, eta=eta), thrust_at_power(bus, 1.10, A, eta=eta)
        need_local = hover_mw(Se, rho, A, eta)
        A_need = disk_for(Se, bus, rho, eta)
        out['byEta'][str(eta)] = dict(hoverPowerNeededMW_local=need_local, hoverPowerNeededMW_rho110=hover_mw(Se, 1.10, A, eta),
                                      powerOverBus=need_local / bus, thrustCapT_fullBus_local=cap_local, thrustCapT_fullBus_rho110=cap_110,
                                      hoverDeficitT_local=Se - cap_local, closesAtHover=Se <= cap_local,
                                      diskNeededM2_fullBus=A_need, diskNeededOverDrawn=A_need / A, diskNeededOverPlanform=A_need / S,
                                      diskNeededOverPublishedPlanform=A_need / prob['hull']['published']['planformM2'],
                                      inducedVelocityAtNeedMps=math.sqrt(Se * 1000 * G / (2 * rho * A)))
    # the empty-hull hold through the sketch (energy if the bus could supply it is not meaningful; print the clipped sketch)
    for km in (15, 60):
        sk = cycle_sketch(name, c, km)
        out[f'sketch{km}'] = dict(rotorMWh=sk['rotorMWh'], worstUnheldT=sk['worstUnheldDownT']['unheldT'], worstPhase=sk['worstUnheldDownT'].get('phase'),
                                  earlierRotorsMWh=EARLIER[(name, km)]['rotorsMWh'], earlierWorstUnheldT=EARLIER[(name, km)]['worstUnheldT'])
    return out

def route_b(name, c, prob):
    hold = prob['altitudes']['hold']; rho, A, bus, P = hold['rho'], c['diskM2'], prob['busMW'], c['payloadT']
    Se = hold['emptySurplusT']
    out = dict(label='water kept aboard', byKm={})
    hover_bound = {str(eta): max(0.0, Se - thrust_at_power(bus, rho, A, eta=eta)) for eta in ETAS}
    out['keptAtHover_fullBusT'] = hover_bound
    for km in (15, 60):
        J = EARLIER[(name, km)]; nonrotor = J['cycleMWh'] - J['rotorsMWh']
        rows = {}
        for eta in ETAS:
            kept = kept_to_close(name, c, km, eta=eta)
            if kept is None: rows[str(eta)] = dict(closes=False); continue
            sk = cycle_sketch(name, c, km, keptT=kept, eta=eta)
            delivered = P - kept
            E = nonrotor + sk['rotorMWh']
            rows[str(eta)] = dict(closes=True, keptT=kept, keptFraction=kept / P, deliveredT=delivered, deliveredFraction=delivered / P,
                                  cycleMWh=E, rotorMWh=sk['rotorMWh'], nonRotorMWh_earlier=nonrotor, peakBusMW=sk['peakBusMW'],
                                  kwhPerDeliveredT=E * 1000 / delivered if delivered > 0 else None,
                                  minutesAdded=-(DUR[(name, km)]['WF'] + DUR[(name, km)]['WR']) * kept / P)
        lever = BASELINE_LEVERS.get((name, km))
        rows['earlierLever'] = dict(retainedT=lever['retainedT'], deliveredT=lever['deliveredT'], kwhPerDeliveredT=lever['kwhPerT']) if lever else dict(retainedT=0.0, note='baseline: no ballast lever needed or no ballast can repair the loaded trajectory (P-100)')
        rows['keptRangeT'] = dict(low=hover_bound['0.7'], sketch=rows['0.7'].get('keptT'), high=lever['retainedT'] if lever else J['worstUnheldT'])
        out['byKm'][str(km)] = rows
    return out

def route_c(name, c, prob):
    hold = prob['altitudes']['hold']; rho, A, bus, P = hold['rho'], c['diskM2'], prob['busMW'], c['payloadT']
    Se = hold['emptySurplusT']; L_n = Se * 1000 * G
    S, b, Af = prob['hull']['config']['planformM2'], c['diaM'], frontal(c['diaM'])
    Sp, bp = prob['hull']['published']['planformM2'], PUBLISHED_HULL[name][1]
    hotel = c['genMW'] * HOTEL_FRAC
    V_cr = c['cruiseKph'] / 3.6
    speeds = [15, 20, 25, 30, 35] + ([round(V_cr, 2)] if V_cr > 35 else [])
    out = dict(label='approach flown at airspeed (hull as a lifting body at negative incidence)', emptySurplusT=Se, bySpeed={}, favourable={}, record={})
    for V in speeds:
        q = 0.5 * rho * V * V
        row = dict(qPa=q, clNeeded_configPlanform=L_n / (q * S), clNeeded_publishedPlanform=L_n / (q * Sp),
                   zeroLiftDragMW=q * CD_ZERO_LIFT * Af * V / PROP_ETA / 1e6)
        for e in E_SPAN:
            Di = induced_drag_n(L_n, q, b, e); Dip = induced_drag_n(L_n, q, bp, e)
            row[f'inducedPowerMW_e{e}'] = Di * V / PROP_ETA / 1e6
            row[f'inducedPowerMW_publishedSpan_e{e}'] = Dip * V / PROP_ETA / 1e6
            row[f'liftOverInducedDrag_e{e}'] = L_n / Di
            row[f'totalPowerMW_e{e}'] = row[f'inducedPowerMW_e{e}'] + row['zeroLiftDragMW'] + hotel
            row[f'closesOnBus_e{e}'] = row[f'totalPowerMW_e{e}'] <= bus
        # record basis at this airspeed: rotors edgewise alone, whole bus, no aero
        avail = max(0.0, bus - hotel - row['zeroLiftDragMW'])
        cap = thrust_at_power(avail, rho, A, 0.0, V)
        row['record_rotorThrustAtBusT'] = cap; row['record_unheldT'] = Se - cap
        row['record_surrogateCapT'] = thrust_at_power(bus, rho, A); row['record_closes'] = (Se <= min(cap, row['record_surrogateCapT']))
        # measured-C_L split: aero at C_L, rotors with the rest of the bus
        for cl in CL_MEASURED_PLANFORM + CL_ASSUMED:
            aero = min(Se, cl * q * S / (1000 * G))
            Pi = induced_drag_n(aero * 1000 * G, q, b, 1.0) * V / PROP_ETA / 1e6
            avail2 = max(0.0, bus - hotel - row['zeroLiftDragMW'] - Pi)
            rot = min(thrust_at_power(avail2, rho, A, 0.0, V), row['record_surrogateCapT'])
            row[f'split_cl{cl}'] = dict(aeroT=aero, inducedPowerMW_e1=Pi, rotorT=rot, unheldT=Se - aero - rot, closesLevelFlight=(Se - aero - rot) <= 0)
        out['bySpeed'][str(V)] = row
    # minimum speed for the aero alone at measured C_L, and the power there
    for cl in CL_MEASURED_PLANFORM + CL_ASSUMED:
        Vmin = math.sqrt(2 * L_n / (rho * cl * S)); q = 0.5 * rho * Vmin ** 2
        rowc = dict(VminMps=Vmin, VminOverCruise=Vmin / V_cr, zeroLiftDragMW=q * CD_ZERO_LIFT * Af * Vmin / PROP_ETA / 1e6)
        for e in E_SPAN:
            rowc[f'inducedPowerMW_e{e}'] = induced_drag_n(L_n, q, b, e) * Vmin / PROP_ETA / 1e6
            rowc[f'totalPowerMW_e{e}'] = rowc[f'inducedPowerMW_e{e}'] + rowc['zeroLiftDragMW'] + hotel
            rowc[f'closesOnBus_e{e}'] = rowc[f'totalPowerMW_e{e}'] <= bus
        out['favourable'][f'cl{cl}'] = rowc
    # the hand-over
    h = HOSE_M - c['diaM'] / 2; Rmax = math.sqrt(max(0.0, c['anchorM'] ** 2 - h * h))
    k2 = ADDED_MASS_K2[2]; m_eff = c['payloadT'] * 1000 + k2 * rho * c['dispM3']
    hand = dict(cableBelowAttachmentM=h, cableM=c['anchorM'], circleRadiusMaxM=Rmax, addedMassK2_fineness2=k2, effectiveMassT=m_eff / 1000,
                circles={})
    V_use = out['favourable']['cl0.34']['VminMps']
    for nL in TURN_RADIUS_LENGTHS:
        Rt = nL * c['lenM']
        row = dict(radiusM=Rt, radiusOverCableReach=Rt / Rmax if Rmax > 0 else None, reachable=Rt <= Rmax, cableAngleFromVerticalDeg=math.degrees(math.atan2(Rt, h)),
                   turnRateDegPerS=math.degrees(V_use / Rt), secondsPerCircle=2 * math.pi * Rt / V_use, bankForTurnDeg=math.degrees(math.atan(V_use ** 2 / (G * Rt))),
                   centripetalForceT=m_eff * V_use ** 2 / Rt / (1000 * G), endSideslipDeg=math.degrees(math.atan((V_use / Rt) * c['lenM'] / 2 / V_use)),
                   pendulumDropM=c['anchorM'] * (1 - math.cos(math.atan2(Rt, h))), pendulumSpeedMps=math.sqrt(2 * G * c['anchorM'] * (1 - math.cos(math.atan2(Rt, h)))),
                   bagOrbitSpeedIfConicalMps=V_use * min(1.0, Rt / max(Rt, 1e-9)) * (h / c['anchorM']))
        hand['circles'][f'{nL:g}L'] = row
    hand['speedUsedMps'] = V_use
    hand['headWind'] = {f'cl{cl}': out['favourable'][f'cl{cl}']['VminMps'] for cl in CL_MEASURED_PLANFORM + CL_ASSUMED}
    # the hover interval after the stop, no bag: unheld, rise
    cap_h = thrust_at_power(bus, rho, A); unh = Se - cap_h
    vt = math.sqrt(2 * max(unh, 0) * 1000 * G / (rho * VERTICAL_CD * S)) if unh > 0 else 0.0
    hand['hoverInterval'] = dict(unheldT_fullBus=unh, closesAtHoverWithoutBag=unh <= 0, initialAccelMps2=max(unh, 0) * 1000 * G / m_eff,
                                 terminalRiseMps_CD1=vt, riseIn60sM=min(vt * 60, 0.5 * (max(unh, 0) * 1000 * G / m_eff) * 3600),
                                 withBagAtHoverT=Se - cap_h - c['anchorBagT'], closesAtHoverWithBag=(Se - cap_h - c['anchorBagT']) <= 0,
                                 cablePayoutS=h / WINCH_MPS, hoistS=HOIST_M / WINCH_MPS)
    out['handOver'] = hand
    # the sketch with aero at the measured and assumed C_L (helps only while V > 0)
    for km in (15, 60):
        rows = {}
        for cl in (CL_MEASURED_PLANFORM[1], CL_ASSUMED[1]):
            sk = cycle_sketch(name, c, km, aero_cl=cl)
            kept = kept_to_close(name, c, km, aero_cl=cl)
            rows[f'cl{cl}'] = dict(worstUnheldT_noWaterKept=sk['worstUnheldDownT']['unheldT'], worstPhase=sk['worstUnheldDownT'].get('phase'),
                                   keptToCloseT=kept, rotorMWh=sk['rotorMWh'])
        out[f'sketch{km}'] = rows
    return out

def route_d(name, c, prob):
    P = c['payloadT']; rho_w = prob['altitudes']['work']['rho']
    disp2 = 1.5 * P * 1000 / rho_w
    scale = (disp2 / c['dispM3']) ** (1 / 3); lenM, diaM = c['lenM'] * scale, c['diaM'] * scale
    S2, A, bus = planform(lenM, diaM), c['diskM2'], prob['busMW']
    out = dict(label='hull balanced at half load, rotors pushing both ways', dispM3=disp2, dispChange=disp2 / c['dispM3'] - 1,
               hullAreaChange=(disp2 / c['dispM3']) ** (2 / 3) - 1, allowedWallMassPerM3Change=c['dispM3'] / disp2 - 1,
               lenM=lenM, diaM=diaM, planformM2=S2, sizedAtMslM=ALT['work'], surpluses={}, byEta={})
    for key, h in ALT.items():
        rho = rho_isa(h); L = disp2 * rho / 1000
        out['surpluses'][key] = dict(liftT=L, emptySurplusT=L - P, loadedSurplusT=L - 2 * P)
    Se_hold, Sl_work = out['surpluses']['hold']['emptySurplusT'], out['surpluses']['work']['loadedSurplusT']
    for eta in ETAS:
        row = dict(downThrustT_emptyAtHold=Se_hold, downHoverMW=hover_mw(Se_hold, rho_isa(ALT['hold']), A, eta),
                   downCapT_fullBus=thrust_at_power(bus, rho_isa(ALT['hold']), A, eta=eta),
                   upThrustT_loadedAtWork=-Sl_work, upHoverMW_ideal=hover_mw(-Sl_work, rho_w, A, eta),
                   upHoverMW_reverseRange=[hover_mw(-Sl_work, rho_w, A, eta) / f for f in REVERSE_THRUST_FACTOR],
                   upEdgewiseMW_atCruise=glauert_mw(-Sl_work, rho_w, A, 0.0, c['cruiseKph'] / 3.6, eta))
        row['closesDownAtHover'] = Se_hold <= row['downCapT_fullBus']
        row['closesUpAtHover_ideal'] = row['upHoverMW_ideal'] + c['genMW'] * HOTEL_FRAC <= bus
        out['byEta'][str(eta)] = row
    for km in (15, 60):
        J = EARLIER[(name, km)]; nonrotor = J['cycleMWh'] - J['rotorsMWh']
        rows = {}
        for f in (1.0,) + REVERSE_THRUST_FACTOR:
            sk = cycle_sketch(name, c, km, disp=disp2, lenM=lenM, diaM=diaM, two_way=True, reverse_factor=f)
            E = nonrotor + sk['rotorMWh']
            rows[f'reverse{f}'] = dict(rotorMWh=sk['rotorMWh'], cycleMWh=E, kwhPerDeliveredT=E * 1000 / P, peakBusMW=sk['peakBusMW'],
                                      worstUnheldDownT=sk['worstUnheldDownT']['unheldT'], worstUnheldUpT=sk['worstUnheldUpT']['unheldT'],
                                      closes=sk['worstUnheldDownT']['unheldT'] <= 1 and sk['worstUnheldUpT']['unheldT'] <= 1, perPhase=sk['perPhase'])
        out[f'sketch{km}'] = rows
    # failure case: loaded, rotors stop at the working altitude
    heavy = -Sl_work; rho_mid = rho_isa((ALT['work'] + TERRAIN_MSL) / 2)
    vt = math.sqrt(2 * heavy * 1000 * G / (rho_mid * VERTICAL_CD * S2))
    t_fall = (ALT['work'] - TERRAIN_MSL) / vt
    out['failureCase'] = dict(heavyT=heavy, terminalSinkMps_CD1=vt, terminalSinkMps_CD2=vt / math.sqrt(2), terminalSinkMps_CD0p5=vt * math.sqrt(2),
                              secondsToGroundAtTerminal=t_fall, dumpRateNeededM3s=heavy / t_fall, dumpRateOverDrawnFill=heavy / t_fall / c['fillM3s'],
                              note='fail-safe float-up is given up: a loaded ship with stopped rotors is heavy. See docs/DECISIONS.md, section "Buoyancy is evaluated where the ship is, and the hulls are sized for the worst of it".')
    out['ifRotorsNotReversible'] = dict(upwardActuatorNeededT=heavy, atPowerMW_eta07=hover_mw(heavy, rho_w, A, 0.70), note='The drawn rotors provide no upward thrust. This route needs upward authority, so the class record changes.')
    return out

def route_e(name, c, prob):
    hold = prob['altitudes']['hold']; rho, p, A, bus = hold['rho'], hold['pressurePa'], c['diskM2'], prob['busMW']
    Se = hold['emptySurplusT']; cap = thrust_at_power(bus, rho, A)
    out = dict(label='variable displacement (sealed cells change volume)', ambientPressurePa=p)
    for tag, dL in (('fullExchange', Se), ('toRotorCap', max(0.0, Se - cap))):
        dV = dL * 1000 / rho
        W = p * dV / 3.6e9
        row = dict(liftRemovedT=dL, volumeChangeM3=dV, volumeFraction=dV / c['dispM3'], idealWorkMWh=W,
                   electricalMWh_eff030=W / ISOTHERMAL_PUMP_EFF[0])
        for km in (15, 60):
            d = DUR[(name, km)]
            row[f'meanPowerInFillMW_{km}'] = W / (d['WF'] / 60); row[f'meanPowerInFillMW_eff030_{km}'] = W / ISOTHERMAL_PUMP_EFF[0] / (d['WF'] / 60)
            cyc = sum(d.values())
            row[f'meanPowerOverCycleMW_{km}'] = W / (cyc / 60); row[f'meanPowerOverCycleMW_eff030_{km}'] = W / ISOTHERMAL_PUMP_EFF[0] / (cyc / 60)
            row[f'cyclesPer24h_{km}'] = 24 * 60 / cyc
            J = EARLIER[(name, km)]; E = J['cycleMWh'] - J['rotorsMWh'] + W / ISOTHERMAL_PUMP_EFF[0]
            row[f'cycleMWh_eff030_{km}'] = E; row[f'kwhPerDeliveredT_eff030_{km}'] = E * 1000 / c['payloadT']
            row[f'minutesAddedIfBusLimited_{km}'] = max(0.0, W / ISOTHERMAL_PUMP_EFF[0] / bus * 60 - d['WF'])
        out[tag] = row
    out['closedBy'] = 'sealed cells with no valve (research/analysis/air-ballast.md, retraction 2026-08-10); reopenable only as a design decision'
    return out

def route_f(name, c, prob):
    hold = prob['altitudes']['hold']; rho, A, bus, P = hold['rho'], c['diskM2'], prob['busMW'], c['payloadT']
    Se = hold['emptySurplusT']
    out = dict(label='ballast made on board by the cryogenic plant', plantMW=c['cryoMW'], tonnesPerHourAtDrawnPlant={k: c['cryoMW'] / (v / 1000) for k, v in LN2_KWH_PER_T.items()}, byKm={})
    gap_hover = {str(eta): max(0.0, Se - thrust_at_power(bus, rho, A, eta=eta)) for eta in ETAS}
    for km in (15, 60):
        d = DUR[(name, km)]; J = EARLIER[(name, km)]
        window_h = (d['OUT'] + d['WR'] + 0.72 * d['RET']) / 60
        rows = dict(makingWindowMin=window_h * 60, gapT=dict(hover_eta07=gap_hover['0.7'], hover_eta055=gap_hover['0.55'], earlierWorstUnheldT=J['worstUnheldT']))
        for gtag, Gt in (('hover_eta07', gap_hover['0.7']), ('earlierWorst', J['worstUnheldT'])):
            if Gt <= 0: rows[gtag] = dict(ballastT=0.0, note='no gap at this bound'); continue
            rr = dict(ballastT=Gt)
            for k, e in LN2_KWH_PER_T.items():
                Emwh = Gt * e / 1000
                rr[k] = dict(energyPerCycleMWh=Emwh, hoursAtDrawnPlant=Emwh / c['cryoMW'], powerToMakeInWindowMW=Emwh / window_h,
                             powerOverBus=Emwh / window_h / bus, plantMassT_range=[Emwh / window_h * m for m in CRYO_T_PER_MW.values()],
                             plantMassOverDryTarget_floor=Emwh / window_h * CRYO_T_PER_MW['floor'] / P,
                             tonnesMadeByDrawnPlantPerCycle=c['cryoMW'] * window_h / (e / 1000),
                             cycleMWh=J['cycleMWh'] - J['rotorsMWh'] + Emwh, kwhPerDeliveredT=(J['cycleMWh'] - J['rotorsMWh'] + Emwh) * 1000 / P,
                             minutesAddedAtDrawnPlant=max(0.0, Emwh / c['cryoMW'] * 60 - window_h * 60))
            rows[gtag] = rr
        out['byKm'][str(km)] = rows
    return out

def route_g(name, c, prob, routes):
    """Pairs, for this class at 15 km on the drawn bus."""
    P = c['payloadT']; b = routes['b']['byKm']['15']; cc = routes['c']; f = routes['f']['byKm']['15']; e = routes['e']
    gap_h = routes['b']['keptAtHover_fullBusT']['0.7']
    pairs = {}
    pairs['a+b'] = dict(closes=b['0.7']['closes'], keptT=b['0.7'].get('keptT'), deliveredT=b['0.7'].get('deliveredT'), condition='slow letdown, whole bus on the rotors; the drawn letdown needs the earlier lever', vehicleChange=False)
    pairs['b+c'] = dict(closes=True, keptT=gap_h, deliveredT=P - gap_h, condition=f'C_L {CL_MEASURED_PLANFORM[1]} on the planform at {cc["favourable"]["cl0.34"]["VminMps"]:.1f} m/s shown, and a hand-over that holds the hull through the hover interval with {gap_h:.0f} t of water aboard', vehicleChange=False)
    pairs['c+bag'] = dict(closes=False, condition='the hover interval before the bag holds has no actuator: see routes.c.handOver.hoverInterval', vehicleChange=False)
    made = f['earlierWorst']['config_eLN2']['tonnesMadeByDrawnPlantPerCycle'] if 'config_eLN2' in f.get('earlierWorst', {}) else 0.0
    pairs['a+f'] = dict(closes=made >= EARLIER[(name, 15)]['worstUnheldT'], ballastMadePerCycleT=made, gapT=EARLIER[(name, 15)]['worstUnheldT'], condition='drawn plant, config specific energy, making window of the cycle', vehicleChange=False)
    pairs['b+f'] = dict(closes=True, keptT=max(0.0, b['keptRangeT']['high'] - made), deliveredT=P - max(0.0, b['keptRangeT']['high'] - made), condition='the plant replaces the tonnes it can make per cycle', vehicleChange=False)
    pairs['a+d'] = dict(closes=routes['d']['sketch15']['reverse1.0']['closes'], deliveredT=P, condition='vehicle change: smaller hull, reversible rotors, float-up given up', vehicleChange=True)
    pairs['a+e'] = dict(closes=True, volumeFraction=e['toRotorCap']['volumeFraction'], electricalMWh=e['toRotorCap']['electricalMWh_eff030'], condition='vehicle change: cells that change volume every cycle (closed by the sealed-cell decision)', vehicleChange=True)
    return pairs

# ---------------------------------------------------------------- baseline reproduction
def reproduce_baseline():
    rows = []
    for e in BASELINE_INSTANTS:
        c = CLASSES[e['cls']]; S, A = planform(c['lenM'], c['diaM']), c['diskM2']
        vz = e['vz']; vc = abs(vz) if vz < 0 else 0.0
        drag = 0.5 * 1.10 * VERTICAL_CD * S * vz * vz / (1000 * G)
        avail = thrust_at_power(e['rotorBusMW'], 1.10, A, vc, e['airV'])
        need = e['surplusT'] + (drag if vz < 0 else -drag) - e['bagT']
        mine = need - avail
        rows.append(dict(cls=e['cls'], km=e['km'], phase=e['phase'], x=e['x'], altAgl=e['altAgl'], vz=vz, airV=e['airV'], surplusT=e['surplusT'],
                         dragT_rho110=drag, availThrustT=avail, unheldMine=mine, unheldTree=e['treeUnheldT'], diffT=mine - e['treeUnheldT'],
                         rangeAtCd=[need - avail - drag * (1 - cd) for cd in VERTICAL_CD_RANGE]))
    return rows

# ---------------------------------------------------------------- main
def main():
    out = dict(meta=dict(label='ANALYSIS, NOT DESIGN', date='2026-10-02', script='research/analysis/payload-exchange.py',
                         note='Nothing here says the ship flies, and nothing says it cannot be made to.'),
               constants=dict(PROP_ETA=PROP_ETA, ETAS=ETAS, CD_ZERO_LIFT=CD_ZERO_LIFT, VERTICAL_CD=VERTICAL_CD, VERTICAL_CD_RANGE=VERTICAL_CD_RANGE,
                              ISA=dict(RHO_SL=RHO_SL, T0=T0, P0=P0, LAPSE=LAPSE, G0=G0, R=R), G=G, ALT=ALT, SOLAR_W_M2=SOLAR_W_M2, HOTEL_FRAC=HOTEL_FRAC,
                              PUMP_ETA=PUMP_ETA, LN2_KWH_PER_T=LN2_KWH_PER_T, CRYO_T_PER_MW=CRYO_T_PER_MW, BATT_WH_PER_KG=BATT_WH_PER_KG,
                              ISOTHERMAL_PUMP_EFF=ISOTHERMAL_PUMP_EFF, ADDED_MASS_K2=ADDED_MASS_K2, CL_MEASURED_PLANFORM=CL_MEASURED_PLANFORM,
                              CL_ASSUMED=CL_ASSUMED, E_SPAN=E_SPAN, TURN_RADIUS_LENGTHS=TURN_RADIUS_LENGTHS, REVERSE_THRUST_FACTOR=REVERSE_THRUST_FACTOR,
                              measuredSources=MEASURED_CL),
               earlierData=dict(durationsMin={f'{k[0]}/{k[1]}': v for k, v in DUR.items()}, cycles={f'{k[0]}/{k[1]}': v for k, v in EARLIER.items()},
                               levers={f'{k[0]}/{k[1]}': v for k, v in BASELINE_LEVERS.items()}, capT_rho110=BASELINE_CAP_RHO110),
               classes={})
    # measured C_L conversions to a planform basis (Akron: length 239.3 m, dia 40.5 m, volume 184,000 m3; fineness-4 model: 1 m x 0.25 m)
    akron_vol23 = 184000 ** (2 / 3); akron_plan = planform(239.3, 40.5)
    f4_vol = math.pi / 6 * 1.0 * 0.25 ** 2; f4_plan = math.pi / 4 * 1.0 * 0.25
    out['constants']['measuredSources']['akron_vol23_to_planform'] = akron_vol23 / akron_plan
    out['constants']['clConversions'] = dict(
        akron_fins_20deg_planform=0.405 * akron_vol23 / akron_plan, akron_bare_max_planform=0.115 * akron_vol23 / akron_plan,
        fineness4_35p6deg_lift_vol23=0.825 * math.cos(math.radians(35.62)) - 0.038 * math.sin(math.radians(35.62)),
        fineness4_35p6deg_lift_planform=(0.825 * math.cos(math.radians(35.62)) - 0.038 * math.sin(math.radians(35.62))) * f4_vol ** (2 / 3) / f4_plan,
        fineness4_11p6deg_lift_planform=(0.233 * math.cos(math.radians(11.62)) - 0.0325 * math.sin(math.radians(11.62))) * f4_vol ** (2 / 3) / f4_plan,
        hybridHull_12deg_cl=0.0067 * (12 + 4.2), note='conversions are this study\'s own arithmetic; planforms are capsule/ellipse estimates of the test bodies')
    for name in ORDER:
        c = CLASSES[name]
        prob = problem(name, c)
        routes = {}
        routes['a'] = route_a(name, c, prob)
        routes['b'] = route_b(name, c, prob)
        routes['c'] = route_c(name, c, prob)
        routes['d'] = route_d(name, c, prob)
        routes['e'] = route_e(name, c, prob)
        routes['f'] = route_f(name, c, prob)
        routes['g'] = route_g(name, c, prob, routes)
        batt = {k: c['battMWh'] * 1000 / v for k, v in BATT_WH_PER_KG.items()}
        out['classes'][name] = dict(problem=prob, routes=routes, batteryMassT=batt, batteryMassOverDryTarget={k: v / c['payloadT'] for k, v in batt.items()})
        h = prob['altitudes']
        print(f"\n== {name}: disp {c['dispM3']:,.0f} m3, planform {prob['hull']['config']['planformM2']:,.0f} m2 (published {prob['hull']['published']['planformM2']:,.0f}), bus {prob['busMW']} MW")
        for k in ('ground', 'hold', 'drop', 'work'):
            print(f"   {k:<7} {h[k]['mslM']} m MSL rho {h[k]['rho']:.5f} lift {h[k]['liftT']:10.1f} t empty surplus {h[k]['emptySurplusT']:9.1f} t ({h[k]['emptySurplusOverPayload']:.3f} payload) loaded {h[k]['loadedSurplusT']:8.1f} t")
        print(f"   balance: empty hull floats at {prob['balance']['emptyAltMslM']:,.0f} m MSL, loaded at {prob['balance']['loadedAltMslM']:,.0f} m MSL")
        a = routes['a']['byEta']['0.7']; a55 = routes['a']['byEta']['0.55']
        print(f"   (a) hover need {a['hoverPowerNeededMW_local']:.1f} MW ({a['powerOverBus']:.2f} bus); cap {a['thrustCapT_fullBus_local']:.1f} t (eta .55: {a55['thrustCapT_fullBus_local']:.1f}); disk needed {a['diskNeededM2_fullBus']:,.0f} m2 = {a['diskNeededOverPlanform']:.2f} planform (eta .55: {a55['diskNeededOverPlanform']:.2f})")
        for km in ('15', '60'):
            b = routes['b']['byKm'][km]['0.7']
            print(f"   (b) {km} km: kept {b.get('keptT', float('nan')):.1f} t -> delivered {b.get('deliveredT', float('nan')):.1f} t, {b.get('cycleMWh', float('nan')):.1f} MWh, {b.get('kwhPerDeliveredT') or float('nan'):.1f} kWh/t; range {routes['b']['byKm'][km]['keptRangeT']}")
        cf = routes['c']['favourable']
        print(f"   (c) Vmin at C_L .34: {cf['cl0.34']['VminMps']:.1f} m/s, power {cf['cl0.34']['totalPowerMW_e1.0']:.1f}/{cf['cl0.34']['totalPowerMW_e0.7']:.1f} MW (e 1/.7) vs bus; hover interval unheld {routes['c']['handOver']['hoverInterval']['unheldT_fullBus']:.1f} t; 2L circle cable angle {routes['c']['handOver']['circles']['2L']['cableAngleFromVerticalDeg']:.0f} deg, pendulum {routes['c']['handOver']['circles']['2L']['pendulumSpeedMps']:.0f} m/s")
        d = routes['d']
        print(f"   (d) disp {d['dispM3']:,.0f} m3 ({d['dispChange']*100:+.1f}%), down {d['byEta']['0.7']['downThrustT_emptyAtHold']:.0f} t / {d['byEta']['0.7']['downHoverMW']:.0f} MW, up {d['byEta']['0.7']['upThrustT_loadedAtWork']:.0f} t / {d['byEta']['0.7']['upHoverMW_ideal']:.0f} MW; 15 km {d['sketch15']['reverse1.0']['cycleMWh']:.1f} MWh closes {d['sketch15']['reverse1.0']['closes']}; failure sink {d['failureCase']['terminalSinkMps_CD1']:.1f} m/s, dump {d['failureCase']['dumpRateNeededM3s']:.1f} m3/s")
        e = routes['e']
        print(f"   (e) full exchange {e['fullExchange']['volumeFraction']*100:.1f}% of hull, ideal {e['fullExchange']['idealWorkMWh']:.1f} MWh, in the fill {e['fullExchange']['meanPowerInFillMW_15']:.0f} MW ideal")
        f = routes['f']['byKm']['15']
        if 'earlierWorst' in f and 'config_eLN2' in f['earlierWorst']:
            print(f"   (f) {f['earlierWorst']['ballastT']:.0f} t of LN2 per cycle: {f['earlierWorst']['config_eLN2']['energyPerCycleMWh']:.0f} MWh, {f['earlierWorst']['config_eLN2']['powerToMakeInWindowMW']:.0f} MW in the window vs plant {c['cryoMW']} MW; drawn plant makes {f['earlierWorst']['config_eLN2']['tonnesMadeByDrawnPlantPerCycle']:.1f} t per cycle")
    out['baselineReproduction'] = reproduce_baseline()
    print("\n== baseline reproduction (record basis, rho 1.10, C_D 1) ==")
    for rw in out['baselineReproduction']:
        print(f"   {rw['cls']:>6}/{rw['km']:>2} {rw['phase']}@{rw['x']:.4f}: unheld mine {rw['unheldMine']:9.2f} vs tree {rw['unheldTree']:9.2f} (diff {rw['diffT']:+.4f}); C_D 0/1/2: {[round(x,1) for x in rw['rangeAtCd']]}")
    out['ranking'] = [
        dict(rank=1, route='b', name='water kept aboard', why='closes every class on the drawn vehicle and bus at a price in delivered tonnes; no new mechanism; the price is bounded by routes.b.byKm.*.keptRangeT'),
        dict(rank=2, route='d', name='hull balanced at half load, rotors both ways', why='closes the force balance for all classes on the drawn bus with full delivery, but changes the vehicle and gives up fail-safe float-up; the one next analysis'),
        dict(rank=3, route='c', name='approach at airspeed', why='closes the moving legs for the P-100 and, at measured C_L, the P-1000; the hand-over to the bag has no coherent form at the drawn cable and hull lengths'),
        dict(rank=4, route='e', name='variable displacement', why='ideal work is affordable only for the partial exchange; it asks sealed cells to change volume every cycle; closed by a reopenable design decision'),
        dict(rank=5, route='a', name='rotor hold-down as drawn', why='the disk needed is a multiple of the hull planform on the two larger classes'),
        dict(rank=6, route='f', name='cryogenic ballast', why='the energy and plant mass to make the ballast inside the cycle exceed the bus and the dry mass on every class with a gap'),
    ]
    out['nextAnalysis'] = 'route d: the half-load hull with two-way rotors, opened on its failure case (routes.*.d.failureCase) before anything else'
    json.dump(out, open(os.path.join(HERE, 'payload-exchange.json'), 'w'), indent=1, default=lambda x: r(x))
    # The corrected geometry sentence is generated from the same calculation.
    docpath = os.path.join(HERE, 'payload-exchange.md')
    if os.path.exists(docpath):
        from pathlib import Path
        import re
        volumes = [f"{out['classes'][name]['problem']['hull']['config']['capsuleVolumeM3']:,.0f}" for name in ['P100', 'P1000', 'P10000']]
        sentence = 'The configured hull is a capsule, with a cylinder and hemispherical ends.\n'
        sentence += f'Its volumes are {volumes[0]}, {volumes[1]} and {volumes[2]} m³, computed from the configured lengths and diameters\n'
        sentence += '[`*.problem.hull.config.capsuleVolumeM3`].'
        text = Path(docpath).read_text()
        text = re.sub(r'(?<=<!-- payload-capsule:start -->)\n.*?\n(?=<!-- payload-capsule:end -->)', '\n'+sentence+'\n', text, flags=re.S)
        Path(docpath).write_text(text)

    print(f"\nwrote {os.path.join(HERE, 'payload-exchange.json')}")

if __name__ == '__main__':
    main()
