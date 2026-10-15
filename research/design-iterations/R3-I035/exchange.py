"""R3-I035 finite exchange calculator: segregated upper-tank countermass chambers.

Loads the frozen baseline (saved-input assembly) and computes exactly:
  geometry + compartment capacities vs acceptance demands,
  the complete paid hardware bill (stock-formula masses, declared masses),
  total mass / CG from explicit part centres,
  the nominal event programme + eight fixed skew cases (species ledgers),
  boundary states, and honest FAIL/UNKNOWN verdicts.
Stdlib only. Writes exchange.json beside this file. No ancestor import.
"""
import hashlib, json, math, sys
from pathlib import Path

U = Path(__file__).resolve().parent
print("SCIENCE_STARTED", flush=True)
BASE = json.loads((U / "baseline.json").read_text())


def fail(msg):
    print("EXCHANGE_FAIL " + msg, file=sys.stderr, flush=True)
    raise SystemExit(2)


# ---------------------------------------------------------------- geometry
OD = BASE["tanks"]["stock"]["od_m"]
WALL = BASE["tanks"]["stock"]["wall_mm"] / 1000.0
RHO_AL = BASE["tanks"]["stock"]["shell_density_kg_m3"]
C_OUT = BASE["tanks"]["stock"]["head_outer_depth_m"]
C_IN = C_OUT - WALL
R_IN = OD / 2.0 - WALL
R_OUT = OD / 2.0
RHO_STEEL = BASE["supports"]["pipe_stock_steel_kg_m3"]
RHO_W = BASE["water"]["density_t_m3"] * 1000.0  # kg/m3


def head_cap_volume(h):
    """Inner oblate (semi-ellipsoid) cap volume filled to depth h from the apex."""
    h = min(h, C_IN)
    return math.pi * R_IN * R_IN * (h * h / C_IN - h ** 3 / (3 * C_IN ** 2))


def barrel_volume(length):
    return math.pi * R_IN * R_IN * length


def head_surface_area():
    """Exact oblate-dome surface (equatorial radius a, depth c): 2*pi*a^2*(1+(1-e^2)/e*artanh e)."""
    a, c = R_OUT, C_OUT
    e = math.sqrt(1.0 - (c * c) / (a * a))
    return 2 * math.pi * a * a * (1.0 + (1.0 - e * e) / e * math.atanh(e))


UPPER_L = BASE["tanks"]["uppers"]["straight_m"]
LOWER_L = BASE["tanks"]["lowers"]["straight_m"]
DIV_Z = BASE["tanks"]["uppers"]["divider"]["midplane_z_m"]
DIV_H = BASE["tanks"]["uppers"]["divider"]["height_above_bottom_tangent_m"]
DIV_T = 0.006
FB = 0.060  # freeboard rule

# Upper tank z landmarks (world z; centre -19.0)
UP_CENTRE_Z = -19.0
UP_BOT_TAN = UP_CENTRE_Z - UPPER_L / 2.0            # -21.10
UP_TOP_TAN = UP_CENTRE_Z + UPPER_L / 2.0            # -16.90
UP_APEX_IN = UP_TOP_TAN + C_IN                       # -16.603
LOW_CENTRE_Z = -21.5
LOW_BOT_TAN = LOW_CENTRE_Z - LOWER_L / 2.0
LOW_TOP_TAN = LOW_CENTRE_Z + LOWER_L / 2.0
LOW_APEX_IN = LOW_TOP_TAN + C_IN

# Reserve: bottom head + (DIV_H - FB) of barrel, minus internals that sit in it
RES_LIQ_BARREL = DIV_H - FB                          # 0.69 m below divider underside
# Service: from divider top plate face to (apex - FB)
SRV_BOT = DIV_Z + DIV_T                              # liquid can reach plate top
SRV_TOP_Z = UP_APEX_IN - FB
SRV_BARREL_FULL = UP_TOP_TAN - SRV_BOT               # straight portion available
SRV_HEAD_USED = SRV_TOP_Z - UP_TOP_TAN               # head portion used (0.237)
# Lower: head + barrel + head, freeboard into top head
LOW_HEAD_USED = C_IN - FB

# Displaced volumes inside compartments (m3)
def annulus(r_o, r_i, length):
    return math.pi * (r_o ** 2 - r_i ** 2) * length


SUMP_R_O, SUMP_R_I, SUMP_DEPTH, SUMP_FLOOR_T = 0.175, 0.169, 0.100, 0.006
DN300_R_O, DN300_R_I = 0.162, 0.156
DN100_R_O, DN100_R_I = 0.05715, 0.05415
DN80_R_O, DN80_R_I = 0.04445, 0.04145
DN50_R_O, DN50_R_I = 0.03015, 0.02715
DN300_LEN = DIV_H + C_IN + 0.300                     # sump -> through reserve -> stub
SCOOPI_DownPIPE_L = 0.500

ring_r_o = R_IN
ring_r_i = R_IN - 0.100
stiff_len = max(0.0, R_IN - 0.200)                   # collar OD 0.200 -> ring

reserve_displaced = (
    annulus(SUMP_R_O, SUMP_R_I, SUMP_DEPTH)          # sump cup wall
    + math.pi * SUMP_R_I ** 2 * SUMP_FLOOR_T         # sump floor
    + annulus(DN300_R_O, DN300_R_I, DN300_LEN - 0.300)  # drain pipe inside reserve
)
# divider plate + ring + stiffener webs occupy the divider plane (counts on both sides boundary)
divider_volume = (
    math.pi * R_IN ** 2 * DIV_T
    + annulus(ring_r_o, ring_r_i, DIV_T)
    + 8.0 * (stiff_len * 0.100 * 0.006 + stiff_len * 0.060 * 0.006)
)
baffle_hole_frac = (8 * math.pi * 0.075 ** 2) / (math.pi * R_IN ** 2)
baffle_plate_vol = math.pi * R_IN ** 2 * 0.003 * (1 - baffle_hole_frac)
service_displaced = 2 * baffle_plate_vol + annulus(DN100_R_O, DN100_R_I, SCOOPI_DownPIPE_L) \
    + 0.300 * 0.300 * 0.006                          # 2 baffles + downpipe + splash plate
lower_displaced = 2 * baffle_plate_vol

V_res = head_cap_volume(C_IN) + barrel_volume(RES_LIQ_BARREL) - reserve_displaced
V_srv = barrel_volume(SRV_BARREL_FULL) + head_cap_volume(SRV_HEAD_USED) - service_displaced
V_low = head_cap_volume(C_IN) + barrel_volume(LOWER_L) + head_cap_volume(LOW_HEAD_USED) - lower_displaced

demands = BASE["acceptance_demands_t"]
cap_rows = []
for name, usable, dem in (
    ("upper reserve fresh", V_res, demands["reserve_fresh"]),
    ("upper service (max of D1 fresh / scoop)", V_srv, max(demands["service_D1_fresh"], demands["service_scoop"])),
    ("lower fresh", V_low, demands["lower_fresh"]),
):
    cap_rows.append({
        "compartment": name, "usable_m3": round(usable, 3), "demand_m3": dem,
        "margin_m3": round(usable - dem, 3),
        "verdict": "PASS" if usable >= dem else "FAIL",
    })
capacity_all_pass = all(r["verdict"] == "PASS" for r in cap_rows)

# ---------------------------------------------------------------- mass bill
bill = []
def row(ident, mass_kg, cz, note=""):
    bill.append({"id": ident, "kg": round(mass_kg, 2), "z_cg_m": round(cz, 3), "note": note})
    return mass_kg

shell_area = head_surface_area()
up_shell = math.pi * (R_OUT ** 2 - R_IN ** 2) * UPPER_L * RHO_AL + 2 * shell_area * WALL * RHO_AL
low_shell = math.pi * (R_OUT ** 2 - R_IN ** 2) * LOWER_L * RHO_AL + 2 * shell_area * WALL * RHO_AL
ring_mass = annulus(ring_r_o, ring_r_i, DIV_T) * RHO_AL
stiff_mass = 8.0 * (stiff_len * 0.100 * 0.006 + stiff_len * 0.060 * 0.006) * RHO_AL
plate_mass = math.pi * R_IN ** 2 * DIV_T * RHO_AL
sump_mass = (annulus(SUMP_R_O, SUMP_R_I, SUMP_DEPTH) + math.pi * SUMP_R_I ** 2 * SUMP_FLOOR_T) * RHO_AL
dn300_mass = annulus(DN300_R_O, DN300_R_I, DN300_LEN) * RHO_STEEL
baffle_mass = baffle_plate_vol * RHO_AL

per_upper_struct = plate_mass + ring_mass + stiff_mass + sump_mass + 2 * baffle_mass
per_upper_shell = up_shell
per_lower_shell = low_shell

hw = BASE["paid_hardware_per_upper_tank"]
per_upper_fittings_kg = (
    2 * 70.0 + 10.0 + 5.0        # DN300 valves + blank + bleed
    + 2 * 15.0 + 12.0            # reserve draw valves + check
    + 15.0                        # fresh fill valve
    + 15.0 + 12.0                 # scoop fill valve + check
    + 2 * (12.0 + 5.0 + 5.0)      # two vent assemblies
    + 2 * 15.0                    # two DN80 reset drain valves
    + 2 * (2 * 3.0 + 2.0)         # sensors: 2 compartments x (2 level + 1 pressure)
    + 10.0                        # interlocked controller
)
per_upper_fittings_notes = "declared complete-body masses from the frozen baseline"

# nozzle/stub pipe masses (steel, per upper): reserve draw 0.3 + fresh fill ~0.3 + scoop 0.3 + downpipe 0.5 + vents 2 risers
VENT_TOP_Z = -27.8
vent_reserve_len = VENT_TOP_Z - (DIV_Z - 0.10)       # riser from reserve gas space through service to exterior
vent_service_len = VENT_TOP_Z - (UP_APEX_IN - 0.10)
per_upper_pipes = (
    annulus(DN100_R_O, DN100_R_I, 0.300) * 3.0       # draw, fill, scoop stubs
    + annulus(DN100_R_O, DN100_R_I, SCOOPI_DownPIPE_L)
    + annulus(DN50_R_O, DN50_R_I, vent_reserve_len + vent_service_len)
    + annulus(DN80_R_O, DN80_R_I, 0.300) * 2.0       # reset drains
) * RHO_STEEL
vent_hood_kg = 2 * (5.0 + 15.0)                      # 2 penetrations x (hood + flanged collar)
vent_blank_kg = 2 * 2 * (0.300 * 0.300 * 0.006) * RHO_STEEL  # reinforcement blanks, each side, 2 penetrations

# route pipe masses per PAIR (exact node distances)
Y_U = 11.0
scoop_len = 3.0 + Y_U + ( abs(-16.3 - (-23.5)) ) + 0.300 + 4 * (math.pi * 0.300 / 2)
fresh_len = abs(-23.0 - (-21.2)) + (2 * Y_U) + 0.300 + 3 * (math.pi * 0.200 / 2)
scoop_pipe_kg = annulus(DN100_R_O, DN100_R_I, scoop_len) * RHO_STEEL
fresh_len_paid = max(25.0, fresh_len)                 # allowance superseded by actual route, pay additional
fresh_pipe_kg = annulus(0.040, 0.037, fresh_len_paid) * RHO_STEEL  # 80/74 mm
per_pair_pumps = (
    45.0 + 2 * 15.0 + 12.0          # fresh pump + valves + wiring
    + 45.0 + 2 * 15.0 + 12.0 + 10.0 + 12.0  # scoop pump set (per upper, one per pair here)
)

# P-frame per pair (aluminium plate + steel rails/gussets/bolts)
al_plate = 1.000 * 0.800 * 0.010 * 2700.0
rhs_area = 0.100 ** 2 - (0.100 - 2 * 0.006) ** 2
rails = 2 * 1.000 * rhs_area * RHO_STEEL + 2 * 0.800 * rhs_area * RHO_STEEL
gussets = 4 * (0.300 * 0.250 * 0.010) * RHO_STEEL
bolts16 = 8 * 0.35
p_frame = al_plate + rails + gussets + bolts16

# clamps + brackets: exact count for frozen routes (never rounded down)
clamp_len = scoop_len + fresh_len + vent_reserve_len + vent_service_len + DN300_LEN + 0.9
n_clamps = math.ceil(clamp_len / 2.0) + 4 + 6 + 4   # straight spacing + elbows + valves + pumps
bracket_plate = 0.200 * 0.200 * 0.008 * RHO_STEEL
clamp_mass = n_clamps * (2.0 + 1.0 + bracket_plate + 4 * 0.085)

inherited = BASE["inherited_charges"]
i017_t = inherited["i017_retained_t"]
retained_kg = (
    (i017_t["fitout_grating_piping_etc"] + i017_t["empty_bay_structure"]
     + i017_t["fasteners"] + i017_t["pickup_fittings_unresolved"]) * 1000.0
    + 4 * 45.0 + 4 * 95.0 + 350.0                    # adapters + fitout allowances x4 tanks + cross-pump
)

# totals: 2 uppers + 2 lowers + 2 pairs + shared
total_struct = 2 * (per_upper_shell + per_upper_struct) + 2 * per_lower_shell
total_fittings = 2 * per_upper_fittings_kg
total_unit_pipes = 2 * (per_upper_pipes + vent_hood_kg + vent_blank_kg)
total_pair = 2 * (scoop_pipe_kg + fresh_pipe_kg + per_pair_pumps + p_frame) + clamp_mass + retained_kg

DRY = total_struct + total_fittings + total_unit_pipes + total_pair
row("upper shell x2", 2 * per_upper_shell, UP_CENTRE_Z, "barrel+2 oblate heads, exact dome area")
row("lower shell x2", 2 * per_lower_shell, LOW_CENTRE_Z, "same")
row("divider plates x2", 2 * plate_mass, DIV_Z, "6 mm plate cut to inner diameter")
row("seating rings x2", 2 * ring_mass, DIV_Z, "100x6 circumferential")
row("T stiffeners x16", 2 * stiff_mass, DIV_Z - 0.05, "8 per divider, 100x6 web + 60x6 flange")
row("sump cups x2", 2 * sump_mass, DIV_Z - SUMP_DEPTH / 2, "350 OD x 6 wall x 100 deep + floor")
row("service baffles x4", 4 * baffle_mass, -18.85, "repartitioned at -19.350/-18.350")
row("lower baffles x4", 4 * baffle_mass, LOW_CENTRE_Z, "retained")
row("DN300 service drains x2", 2 * dn300_mass, -21.5, "sump through reserve + stub")
row("fittings per upper x2", total_fittings, UP_CENTRE_Z, per_upper_fittings_notes)
row("unit pipes/nozzles x2", total_unit_pipes, -20.0, "stubs, downpipe, vents incl hoods/collars/blanks")
row("scoop route DN100 x2", 2 * scoop_pipe_kg, -22.0, "S->P->V->F exact nodes + 300 elbows")
row("fresh route 80/74 x2", 2 * fresh_pipe_kg, -22.7, "reserve->lower inlet exact nodes")
row("pumps/valves/wiring x2 pairs", 2 * per_pair_pumps, -23.5, "fresh 45 kg set + scoop 45 kg set")
row("P-frames x2", 2 * p_frame, -23.5, "plate+rails+gussets+bolts at P")
row("clamps/brackets", clamp_mass, -22.0, f"{n_clamps} clamps exact count")
row("retained I017 lines + adapters + fitout + cross-pump", retained_kg, -20.0, "declared allowances; adapters/attachment C unresolved")
row("DRY TOTAL", DRY, 0.0, "sum of rows above; complete bill conditional on unpriced C duties")

# ---------------------------------------------------------------- fluid states
def centroid_barrel(length):
    return length / 2.0


def fluid_state_table():
    rows = []
    for label, srv, res, low, scoop in (
        ("S0/pre-D1", 25.0, 5.0, 20.0, 0.0),
        ("D1 end", 0.0, 5.0, 20.0, 0.0),
        ("D2 mid s=0.5", 0.0, 2.5, 10.0, 12.725),
        ("D2 end", 0.0, 0.0, 0.0, 25.45),
    ):
        water_t = 2 * (srv + res + low + scoop)
        # fluid CG z (approx: reserve centroid in reserve, service in service, lower in lower)
        z = 0.0
        m_tot = srv + res + low + scoop
        if m_tot > 0:
            z = (srv * (-18.4) + res * (-20.8) + low * (-21.5) + scoop * (-18.4)) / m_tot
        rows.append({"state": label, "per_pair_service_t": srv, "reserve_t": res,
                     "lower_t": low, "scoop_t": scoop, "total_water_t": round(water_t, 3),
                     "fluid_cg_z_m": round(z, 3)})
    return rows


# ---------------------------------------------------------------- event programme
T = BASE["mission"]["D2_window_s"]
CKPTS = BASE["skew_cases"]["checkpoints_s"]
PAIRS = ("A", "B")
res_total, low_total, out_total, scoop_total = 5000.0, 20000.0, 25000.0, 25450.0


def run_case(leader, eps, delta):
    rates = {}
    for pair in PAIRS:
        lead = (pair == leader)
        e = eps if lead else -eps
        d = 0.0 if lead else delta
        f = 1.0 + e
        rates[pair] = {
            "start_delay_s": d, "fresh_mult": f, "scoop_mult": 1.0 - e,
            "r_res": (out_total / 5.0) * f / T, "r_low": (out_total * 4.0 / 5.0) * f / T,
            "r_out": out_total * f / T, "r_scoop": scoop_total * (1.0 - e) / T,
        }
    bps = set(CKPTS) | {0.0, T}
    rows = []
    verdicts = []
    for pair in PAIRS:
        r = rates[pair]
        bps |= {r["start_delay_s"], min(T, r["start_delay_s"] + T / r["fresh_mult"]),
                min(T, r["start_delay_s"] + T / r["scoop_mult"])}
    for t in sorted(b for b in bps if 0 <= b <= T):
        snap = {"t_s": round(t, 3)}
        for pair in PAIRS:
            r = rates[pair]
            dt = max(0.0, t - r["start_delay_s"])
            out = min(out_total, r["r_out"] * dt)
            delivered_from_res = min(res_total, r["r_res"] * dt)
            delivered_from_low = min(low_total, r["r_low"] * dt)
            scoop = min(scoop_total, r["r_scoop"] * dt)
            res_left = res_total - delivered_from_res
            low_left = low_total - delivered_from_low
            snap[pair] = {
                "out_t": round(out / 1000.0, 4), "reserve_left_t": round(res_left / 1000.0, 4),
                "lower_left_t": round(low_left / 1000.0, 4), "scoop_t": round(scoop / 1000.0, 4),
            }
        rows.append(snap)
    for pair in PAIRS:
        r = rates[pair]
        fin_fresh = min(out_total, r["r_out"] * (T - r["start_delay_s"]))
        fin_scoop = min(scoop_total, r["r_scoop"] * (T - r["start_delay_s"]))
        for kind, fin, target in (("fresh delivery", fin_fresh, out_total), ("scoop receipt", fin_scoop, scoop_total)):
            if fin < target - 1e-9:
                verdicts.append({"pair": pair, "kind": kind,
                                 "delivered_kg": round(fin, 1), "target_kg": target,
                                 "short_kg": round(target - fin, 1),
                                 "symbolic_completion_s": "start+" + str(round(T / (r["fresh_mult"] if kind == "fresh delivery" else r["scoop_mult"]), 2)),
                                 "verdict": "TIMING FAIL (unfinished at T; not a permitted extension)"})
    return {"leader": leader, "eps": eps, "delta_s": delta, "rates": rates,
            "breakpoints": rows, "unfinished": verdicts}


cases = [run_case(l, e, d) for l in ("A", "B") for e in (0.05, -0.05) for d in (0.0, 2.0)]
nominal = run_case("A", 0.0, 0.0)

# boundary states: D1 one-empty/other-full; switch-not-confirmed
boundary = [
    {"case": "D1 one upper service empty / other full", "mass_delta_t": 25.0,
     "moment_My_t_m_about_x0": 2 * 14.0 * 25.0, "verdict": "asymmetric load recorded; support/trim adequacy UNKNOWN"},
    {"case": "switch not confirmed (service retains residual fresh, scoop inhibited)",
     "mass_delta_t": None, "verdict": "residual/contamination/duration UNKNOWN; no silent extension"},
]

# fluid moments vs inherited authority (comparison bounded)
Mx_S0 = 2 * (50.0 * 11.0) + 2 * (20.0 * -11.0)   # water only, x=±14 ignored (symmetric), y moments
Mx_D2 = 2 * (25.45 * 11.0)                        # scoop upstairs at y=+11/-11 pairs
My_S0 = 2 * 50.0 * 14.0 + 2 * 20.0 * -14.0
My_D2 = 2 * 25.45 * 14.0
trim = {
    "fluid_Mx_t_m_S0": round(Mx_S0, 2), "fluid_Mx_t_m_D2_end": round(Mx_D2, 2),
    "fluid_My_t_m_S0": round(My_S0, 2), "fluid_My_t_m_D2_end": round(My_D2, 2),
    "changed_z_of_0.9t_scoop": "0.45 t per pair moves from lower z=-21.5 to service z~ -18.4 (+3.1 m each)",
    "authority_datums_t_m": BASE["inherited_mission_data"]["authority_datums_t_m"],
    "verdict": "fluid moment deltas computed; trim adequacy vs donor AND receiver-bounded authority UNKNOWN "
               "(pickup identities/stiffness not supplied by the I032 baseline; W/2 at pickups is a declared ideal convention only)",
}

result = {
    "unit": "R3-I035",
    "kind": "finite exchange calculation output",
    "baseline_sha256": hashlib.sha256((U / "baseline.json").read_bytes()).hexdigest(),
    "geometry": {
        "inner_radius_m": round(R_IN, 4), "inner_head_depth_m": round(C_IN, 4),
        "V_reserve_usable_m3": round(V_res, 3), "V_service_usable_m3": round(V_srv, 3),
        "V_lower_usable_m3": round(V_low, 3),
        "freeboard_applied": {"reserve_below_divider_m": FB, "service_below_inner_apex_m": FB, "lower_below_inner_apex_m": FB},
        "displaced_charged": {"reserve_m3": round(reserve_displaced, 4), "service_m3": round(service_displaced, 4),
                              "lower_m3": round(lower_displaced, 4), "divider_boundary_m3": round(divider_volume, 4)},
    },
    "capacity": cap_rows,
    "capacity_verdict": ("ALL PASS (geometric fit of frozen inventories)" if capacity_all_pass
                         else "FAIL present: " + "; ".join(r["compartment"] for r in cap_rows if r["verdict"] == "FAIL")),
    "mass_bill_kg": bill,
    "dry_total_t": round(DRY / 1000.0, 3),
    "dry_verdict": "conditional: unpriced C duties (adapter attachment, old-frame brackets, S-to-scoop link) keep the complete bill UNKNOWN",
    "fluid_states": fluid_state_table(),
    "events_nominal": nominal,
    "skew_cases": cases,
    "skew_summary": [f"leader={c['leader']} eps={c['eps']:+.2f} delta={c['delta_s']}s: "
                     + ("; ".join(f"{v['pair']} {v['kind']} short {v['short_kg']} kg" for v in c["unfinished"]) or "complete within T")
                     for c in cases],
    "boundary_cases": boundary,
    "trim": trim,
    "inherited_FAILs": {"economics": "35.1x vs SEAT", "fuel_shortfalls_t": [0.245112, 0.350732]},
    "unknowns": BASE["unknown_where_unproved"] + [
        "divider both-direction pressure difference / shell load transfer / local band reactions",
        "vent P/V ratings and atmospheric termination",
        "switch event actuation/drainage/contamination/duration",
        "scoop route S-to-existing-scoop-equipment connection (paid unresolved C)",
        "anti-slosh/transient adequacy of repartitioned baffles",
    ],
    "no_physical_float": "no favourable screen or physical float is claimed anywhere in this unit",
    "weakest_assumption": "whether the fixed divider and independent plumbing leave enough usable capacity while carrying "
                          "concurrent service pressure and full pickup loads",
    "next_design_hypothesis_unissued": "one fully paid EXTERNAL small reserve tank replacing the 5 t internal freshwater "
                                       "reserve, returning the lost upper-barrel volume to scoop service; separate frozen unit required",
}
(U / "exchange.json").write_text(json.dumps(result, indent=1) + "\n")
print("SCIENCE_COMPLETED exchange.json bytes=" + str(len(json.dumps(result, indent=1) + "\n")), flush=True)
