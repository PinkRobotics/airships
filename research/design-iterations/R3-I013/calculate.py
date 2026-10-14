#!/usr/bin/env python3
"""One bounded external suspension layout, with finite assumed supports.

Stdlib only. Selected cold/hot/load cases; no optimizer, FEA or physical claim.
Run from any directory; JSON goes to stdout. SVG drawings are a separate script.
"""
import hashlib
import importlib.util
import json
from math import asinh, ceil, cos, pi, sin, sqrt
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "R3-I010/calculate.py"
SOURCE_SHA = "a61daa351d923e8293751d315e1f56af2432576897e9285341f2c11a7c442c51"
assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == SOURCE_SHA
spec = importlib.util.spec_from_file_location("pressure_corrected_i010", SOURCE)
old = importlib.util.module_from_spec(spec)
spec.loader.exec_module(old)
G = old.G
INV = old.inventory(76.)
BASE = old.build(INV)
GEO = BASE["geometry"]
R = GEO["radius_m"]
AREA = BASE["main_cable_area_m2"]
EA = 50e9 * AREA  # assumed rope secant modulus, not a qualified material
MU = 1440 * AREA + .50  # paid 80mm-OD weather/chafe cover, kg per free metre
ROPE_RADIUS = .040
F_SCALE = 100000.
ACTUATOR_DRAG_AREA, BRACKET_DRAG_AREA = .3, 1.3  # m², no shielding credit
STIFFNESS = (("soft", .5e6, .2e6), ("nominal", 2e6, 1e6), ("firm", 10e6, 5e6))


def add(a, b): return tuple(x+y for x, y in zip(a, b))
def sub(a, b): return tuple(x-y for x, y in zip(a, b))
def mul(a, x): return tuple(x*y for y in a)
def dot(a, b): return sum(x*y for x, y in zip(a, b))
def norm(a): return sqrt(dot(a, a))
def unit(a): return mul(a, 1/norm(a))
def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])


def solve(a, b):
    """Small dense elimination with pivoting; not an optimization routine."""
    a = [list(row)+[v] for row, v in zip(a, b)]
    n = len(b)
    for i in range(n):
        j = max(range(i, n), key=lambda j: abs(a[j][i]))
        a[i], a[j] = a[j], a[i]
        if abs(a[i][i]) < 1e-13: raise ArithmeticError("singular local balance")
        q = a[i][i]
        a[i] = [v/q for v in a[i]]
        for j in range(n):
            if j == i: continue
            q = a[j][i]
            a[j] = [a[j][k]-q*a[i][k] for k in range(n+1)]
    return [row[-1] for row in a]


def newton(fun, x):
    """At most 24 local force/compatibility iterations, with bounded backtracking."""
    x = list(x)
    for iteration in range(24):
        y = fun(x)
        err = max(abs(v) for v in y)
        if err < 2e-10: return x, iteration, err
        columns = []
        for j in range(len(x)):
            h = 2e-6*max(1., abs(x[j]))
            xp, xm = x[:], x[:]
            xp[j] += h; xm[j] -= h
            yp, ym = fun(xp), fun(xm)
            columns.append([(a-b)/(2*h) for a, b in zip(yp, ym)])
        step = solve(list(zip(*columns)), [-v for v in y])
        for fraction in (1., .5, .25, .125, .0625, .03125):
            candidate = [v+fraction*s for v, s in zip(x, step)]
            try: improved = max(abs(v) for v in fun(candidate)) < err
            except (ValueError, ArithmeticError): improved = False
            if improved:
                x = candidate
                break
        else: raise ArithmeticError(f"local compatibility step stalled: {err}")
    raise ArithmeticError("local compatibility iteration bound reached")


def curve(n0, q, s):
    """Integral of N/|N|+N/(EA), N=N0+q*s, in reference arc coordinate."""
    qn = norm(q)
    v = mul(q, 1/qn)
    p = dot(n0, v)
    horizontal = sub(n0, mul(v, p))
    h = norm(horizontal)
    if h < 1e-8:
        assert p > 0 and p+qn*s > 0
        geometric = mul(v, s)
    else:
        geometric = add(mul(horizontal, (asinh((p+qn*s)/h)-asinh(p/h))/qn),
                        mul(v, (sqrt(h*h+(p+qn*s)**2)-sqrt(h*h+p*p))/qn))
    return add(geometric, mul(add(mul(n0, s), mul(q, s*s/2)), 1/EA))


def integral_tension(n0, q, length):
    v = unit(q); qn = norm(q); p = dot(n0, v)
    h = norm(sub(n0, mul(v, p)))
    def primitive(x):
        if h < 1e-8: return x*abs(x)/2
        return (x*sqrt(x*x+h*h)+h*h*asinh(x/h))/2
    return (primitive(p+qn*length)-primitive(p))/qn


def cylinder(bore, od, rod, stroke, barrel, rod_length, fittings):
    """Explicit steel body/rod/caps, oil and fittings; no catalogue capability."""
    a = pi*(od*od-bore*bore)/4
    ar = pi*rod*rod/4
    annulus = pi*bore*bore/4-ar
    oil_volume = pi*bore*bore/4*barrel
    parts = {"barrel": a*barrel*7850, "rod": ar*rod_length*7850,
             "two_caps": 2*pi*od*od/4*.030*7850,
             "contained_oil": oil_volume*850,
             "clevis_lock_valves_and_yoke": fittings}
    hoop = 25e6*((od/2)**2+(bore/2)**2)/((od/2)**2-(bore/2)**2)
    axial = 25e6*(bore/2)**2/((od/2)**2-(bore/2)**2)
    return {"parts_kg": parts, "mass_kg": sum(parts.values()),
            "axial_stiffness_n_m": 1/(barrel/(200e9*a)+rod_length/(200e9*ar)+(oil_volume+.001)/(1.4e9*annulus**2)),
            "assumed_oil_bulk_modulus_pa": 1.4e9,
            "working_pressure_pa": 25e6, "tensile_force_rating_n": 25e6*annulus,
            "inner_hoop_pa": hoop, "closed_end_axial_pa": axial,
            "von_mises_inner_pa": sqrt(((hoop-axial)**2+(axial+25e6)**2+(hoop+25e6)**2)/2),
            "working_steel_pa": 160e6, "rod_area_m2": ar,
            "stroke_m": stroke, "od_m": od, "rod_diameter_m": rod}


MAIN_ACT = cylinder(.125, .155, .075, .6, .85, 1., 25.)
BAG_ACT = cylinder(.063, .079, .035, .4, .60, .70, 10.)
MAIN_COMMAND0, MAIN_MIN, MAIN_MAX = 1.4, 1.1, 1.7
BAG_COMMAND0, BAG_MIN, BAG_MAX = 1.0, .8, 1.2
LEG_LENGTH = sqrt(.35**2+2*.30**2)
LEG_AREA = pi*(.10**2-.084**2)/4
LEG_I = pi*(.10**4-.084**4)/64
K_NORMAL = 4*70e9*LEG_AREA*.35**2/LEG_LENGTH**3
K_TANGENT = 4*70e9*LEG_AREA*.30**2/LEG_LENGTH**3
BRACKET_PARTS = {"four_legs": 4*LEG_LENGTH*LEG_AREA*2700,
                 "spread_plate_1m_by_1m_by_70mm": 1.*1.*.070*2700,
                 "pins_gussets_fasteners": 30., "curved_bedding_shims": 5.}
BRACKET_MASS = sum(BRACKET_PARTS.values())
PLATE_THICKNESS, STANDOFF_RADIAL = .07, .42
BRACKET_CG_RADIAL = (BRACKET_PARTS["four_legs"]*.245+
                     BRACKET_PARTS["spread_plate_1m_by_1m_by_70mm"]*.035+
                     BRACKET_PARTS["pins_gussets_fasteners"]*.42)/BRACKET_MASS
PLATE_K = 4*3*70e9*(.25*.07**3/12)/.3**3


def layout():
    rows = []
    for k, low in enumerate(GEO["modules"]):
        phi = k*pi/4
        for j, (f, angle) in enumerate(((.20, 0.), (.75, -pi/10), (.75, pi/10))):
            radial = (f*cos(phi+angle), f*sin(phi+angle), -sqrt(1-f*f))
            skin = mul(radial, R)
            anchor = mul(radial, R+STANDOFF_RADIAL)
            chord = sub(anchor, low)
            tangential = unit(cross((0., 0., 1.), radial))
            second = cross(radial, tangential)
            bases = [add(add(skin,mul(radial,PLATE_THICKNESS)), add(mul(tangential, a*.3), mul(second, b*.3)))
                     for a, b in ((-1,-1), (-1,1), (1,-1), (1,1))]
            rows.append({"id": 3*k+j, "module": k, "kind": "inner" if j == 0 else "outer",
                         "low": low, "skin": skin, "anchor": anchor, "normal": radial,
                         "leg_bases": bases, "chord_m": norm(chord), "unit": unit(chord),
                         "convex_hull_outward_dot_m2": dot(skin, sub(low, skin))})
    return rows


LAYOUT = layout()


def anchor_state(row, ntop, actuator_command, foundation, wind, rho, azimuth):
    """Finite translation AND rotation of curtain foundation plus metal leg compliance."""
    _, kf, kr = foundation
    direction = unit(ntop)
    actual_length = actuator_command+norm(ntop)/MAIN_ACT["axial_stiffness_n_m"]
    # Conservative fixed projected area per exposed station; no aerodynamic shielding credit.
    actuator_drag = .5*rho*wind**2*1.2*ACTUATOR_DRAG_AREA
    bracket_drag = .5*rho*wind**2*1.2*BRACKET_DRAG_AREA
    drag = actuator_drag+bracket_drag
    actuator_force = (actuator_drag*cos(azimuth), actuator_drag*sin(azimuth), -MAIN_ACT["mass_kg"]*G)
    bracket_force = (bracket_drag*cos(azimuth), bracket_drag*sin(azimuth), -BRACKET_MASS*G)
    station_force = add(actuator_force,bracket_force)
    load = sub(station_force, ntop)
    radial = row["normal"]
    metal = add(mul(load, 1/K_TANGENT), mul(radial, dot(load, radial)*(1/K_NORMAL-1/K_TANGENT)))
    lever = mul(radial, STANDOFF_RADIAL)
    plate = mul(load,1/PLATE_K)
    bracket_lever = mul(radial,BRACKET_CG_RADIAL)
    # The priced yoke carries gravity/aerodynamic couple. The finite rotational
    # foundation includes the first-order displaced lever, rather than hiding it.
    def moment_at(theta):
        pin = add(add(lever,plate),add(metal,cross(theta,lever)))
        cg_b = add(add(bracket_lever,plate),add(mul(metal,.5),cross(theta,bracket_lever)))
        return add(add(cross(pin,mul(ntop,-1)),cross(sub(pin,mul(direction,actual_length/2)),actuator_force)),cross(cg_b,bracket_force))
    moment0=moment_at((0.,0.,0.))
    columns=[sub(moment_at(tuple(1. if i==j else 0. for i in range(3))),moment0) for j in range(3)]
    rotation=tuple(solve([[kr*(i==j)-columns[j][i] for j in range(3)] for i in range(3)],moment0))
    moment=moment_at(rotation)
    displacement = add(add(mul(load, 1/kf),add(plate,metal)), cross(rotation, lever))
    a = add(row["anchor"], displacement)
    b = sub(a, mul(direction, actual_length))
    cg_b=add(row["skin"],add(mul(load,1/kf),add(add(bracket_lever,plate),add(mul(metal,.5),cross(rotation,bracket_lever)))))
    return {"upper_pin": a, "lower_pin": b, "displacement": displacement,
            "bracket_cg_m":cg_b,"actuator_cg_m":mul(add(a,b),.5),
            "foundation_translation_m": mul(load,1/kf), "plate_flex_m":mul(load,1/PLATE_K),
            "metal_leg_flex_m":metal,
            "rotation_rad": rotation, "load_n": load, "moment_nm": moment,
            "actuator_drag_n":actuator_drag,"bracket_drag_n":bracket_drag,
            "station_drag_n": drag, "actuator_command_m": actuator_command,
            "actuator_loaded_m": actual_length}


def cable_force_density(row, wind, rho, azimuth):
    w = (cos(azimuth), sin(azimuth), 0.)
    # Declared uniform reference-chord transverse drag; a bounded approximation.
    qdrag = .5*rho*wind**2*1.2*(2*ROPE_RADIUS)*sqrt(max(0., 1-dot(row["unit"], w)**2))
    return (-qdrag*w[0], -qdrag*w[1], MU*G)


def solve_module(k, target, foundation, wind, rho, azimuth, lengths=None):
    rows = LAYOUT[3*k:3*k+3]
    q = [cable_force_density(r, wind, rho, azimuth) for r in rows]
    ideal = old.solve3([r["unit"] for r in rows], target)
    if min(ideal) <= 0: raise ArithmeticError("outside initial positive direction cone")
    guess = [v/F_SCALE for r, t in zip(rows, ideal) for v in mul(r["unit"], t)]
    if lengths is None: guess += [r["chord_m"]-MAIN_COMMAND0 for r in rows]
    else: guess += [MAIN_COMMAND0]*3
    def evaluate(x, details=False):
        ns = [mul(x[3*i:3*i+3], F_SCALE) for i in range(3)]
        ls = x[9:] if lengths is None else lengths
        cmds = [MAIN_COMMAND0]*3 if lengths is None else x[9:]
        residual = []
        records = []
        for i, row in enumerate(rows):
            if ls[i] <= 0: raise ValueError("nonpositive free length")
            nt = add(ns[i], mul(q[i], ls[i]))
            station = anchor_state(row, nt, cmds[i], foundation, wind, rho, azimuth)
            end = add(row["low"], curve(ns[i], q[i], ls[i]))
            residual.extend(sub(end, station["lower_pin"]))
            if details:
                extension = integral_tension(ns[i], q[i], ls[i])/EA
                n_min_at = max(0., min(ls[i], -dot(ns[i], q[i])/dot(q[i], q[i])))
                n_min = norm(add(ns[i], mul(q[i], n_min_at)))
                sample = [add(row["low"], curve(ns[i], q[i], ls[i]*j/16)) for j in range(17)]
                straight = [add(row["low"], mul(sub(end, row["low"]), j/16)) for j in range(17)]
                sag = [sub(p, c) for p, c in zip(sample, straight)]
                imax = max(range(17), key=lambda j: norm(sag[j]))
                cg = mul(tuple(sum((1 if j in (0,16) else 4 if j%2 else 2)*sample[j][axis]
                                   for j in range(17)) for axis in range(3)), 1/48)
                records.append({"id": row["id"], "module": k, "n0_n": ns[i], "ntop_n": nt,
                                "q_n_per_reference_m": q[i], "free_length_m": ls[i],
                                "loaded_arc_m": ls[i]+extension, "extension_m": extension,
                                "minimum_tension_n": n_min, "station": station,
                                "maximum_sampled_sag_m": norm(sag[imax]),
                                "sag_vector_at_max_m": sag[imax], "sag_position_m": sample[imax],
                                "sag_reference_fraction": imax/16, "cg_m": cg,
                                "points": sample, "shape_residual_m": norm(sub(end, station["lower_pin"]))})
        residual.extend(mul(sub(tuple(sum(n[j] for n in ns) for j in range(3)), target), 1/F_SCALE))
        return (records, residual) if details else residual
    x, iterations, error = newton(evaluate, guess)
    records, residual = evaluate(x, True)
    return records, {"iterations": iterations, "endpoint_residual_m": max(r["shape_residual_m"] for r in records),
                     "force_residual_n": norm(mul(residual[-3:], F_SCALE)), "scaled_residual": error}


def sphere_interval(low, high, centre, radius):
    d, w = sub(high, low), sub(low, centre)
    a, b, c = dot(d, d), dot(w, d), dot(w, w)-radius*radius
    discriminant = b*b-a*c
    if discriminant <= 0: return None
    lo, hi = max(0., (-b-sqrt(discriminant))/a), min(1., (-b+sqrt(discriminant))/a)
    return (lo, hi) if lo < hi else None


def guides():
    rows = []
    for i, hanger in enumerate(GEO["hangers"]):
        for b, centre in enumerate(GEO["bag_centres"]):
            if b == hanger["bag"]: continue
            intersection = sphere_interval(hanger["low"], hanger["top"], centre, GEO["bag_radius_m"]+.14)
            if intersection is None: continue
            lo = max(0., intersection[0]*hanger["length_m"]-2.)
            hi = min(hanger["length_m"], intersection[1]*hanger["length_m"]+2.)
            length = hi-lo
            parts = {"aluminium_240mm_od_2mm_wall": pi*(.24**2-.236**2)/4*length*2700,
                     "one_metre_rings": (ceil(length)+1)*.50,
                     "1p5m_cable_saddles": (ceil(length/1.5)+1)*2.,
                     "two_flexible_bag_cuffs": 24., "end_collars_and_joints": 10.}
            rows.append({"hanger": i, "foreign_bag": b, "start_m": lo, "end_m": hi,
                         "length_m": length, "diameter_m": .24, "parts_kg": parts,
                         "mass_kg": sum(parts.values()), "clamp_spacing_m": 1.5})
    assert len(rows) == 8
    return rows


GUIDES = guides()
GUIDE_MASS = sum(r["mass_kg"] for r in GUIDES)
HANGER_MAX_L = max(h["length_m"] for h in GEO["hangers"])
HANGER_SIZE_A = (1.5*(BASE["bag_supported_mass_bound_kg"]/32+max(r["mass_kg"] for r in GUIDES))*G /
                 (150e6-1.5*1440*HANGER_MAX_L*G))
HANGER_D = ceil(sqrt(4*HANGER_SIZE_A/pi)*1000)/1000
HANGER_A = pi*HANGER_D**2/4
HANGER_EA = 50e9*HANGER_A
HYDRAULIC_PARTS = {"eight_main_pump_reservoir_control_sets": 8*(20.+10.+5.),
                   "main_dual_lines_144m": 144*.8,
                   "main_line_oil_144m_8mm_bore_pair": 144*2*pi*.008**2/4*850,
                   "four_bag_pump_control_sets": 4*(15.+5.),
                   "bag_dual_lines_160m": 160*.5,
                   "bag_line_oil_160m_6mm_bore_pair": 160*2*pi*.006**2/4*850}


def construction(lengths):
    masses = dict(BASE["mass_kg"])
    for key in ("main_cables", "lower_envelope_seals_and_chafe", "routing_sleeves_liners_boots", "bag_hangers"):
        del masses[key]
    masses.update({"external_main_ropes_and_80mm_covers": sum(lengths)*MU,
                   "24_standoffs_and_spread_plates": 24*BRACKET_MASS,
                   "24_main_length_adjusters": 24*MAIN_ACT["mass_kg"],
                   "32_bag_length_adjusters": 32*BAG_ACT["mass_kg"],
                   "hydraulic_controls_lines_and_oil": sum(HYDRAULIC_PARTS.values()),
                   "eight_rigid_hanger_pass_through_liners": GUIDE_MASS,
                   "bag_hangers_and_70mm_clamp_envelope": sum(h["length_m"] for h in GEO["hangers"])*(HANGER_A*1440+.2)})
    result = dict(BASE)
    result["mass_kg"] = masses
    result["construction_kg"] = sum(masses.values())
    return result


def budgets(hull):
    return {name: [old.budget(INV, hull, h, p) for h in (0., 2500.)]
            for name, p in (("M20", 3000.), ("P100", 100000.))}


def case(hull, ballast, h, wind, foundation, lengths=None, hot=0., azimuth=0.):
    """Settled trim with fixed total onboard water; shape-dependent distributed loads."""
    s = old.gas(INV, h, hot)
    b = old.budget(INV, hull, h, 3000., superheat=hot)
    assert b["capacity_ok"]
    excess = b["margin_kg"]-ballast
    fixed = 15000.+hull["cradle"]["over_3000kg_allowance_kg"]+3000.
    total_module = fixed+ballast
    hull_drag = .8*.5*s["rho_air"]*wind**2*pi*38**2
    station_drag = 24*.5*s["rho_air"]*wind**2*1.2*(ACTUATOR_DRAG_AREA+BRACKET_DRAG_AREA)
    reference_lengths = lengths or [r["chord_m"]-MAIN_COMMAND0 for r in LAYOUT]
    cable_drag = sum(norm(cable_force_density(r, wind, s["rho_air"], azimuth)[:2])*l
                     for r,l in zip(LAYOUT, reference_lengths))
    total_drag = hull_drag+station_drag+cable_drag
    w = (cos(azimuth), sin(azimuth), 0.)
    depth, mr = GEO["thrust_depth_m"], GEO["module_radius_m"]
    amplitudes = mul(w, -total_drag*depth/(4*G*mr))
    all_rows, all_checks = [], []
    # This bounded fixed point couples distributed moments to water trim; no family search.
    for trim_iteration in range(10):
        all_rows, all_checks, modules = [], [], []
        for k in range(8):
            phi = k*pi/4
            wk = ballast/8+amplitudes[0]*cos(phi)+amplitudes[1]*sin(phi)
            mk = fixed/8+wk
            weight = (mk+excess/8)*G
            hk = total_drag*weight/((total_module+excess)*G)
            ring = hull["ballast_system"]["inward_reaction_per_module_n"]
            target = (hk*w[0]+ring*cos(phi), hk*w[1]+ring*sin(phi), weight)
            rows, checks = solve_module(k, target, foundation, wind, s["rho_air"], azimuth,
                                        None if lengths is None else lengths[3*k:3*k+3])
            all_rows.extend(rows); all_checks.append(checks)
            modules.append({"module": k, "water_kg": wk, "physical_mass_kg": mk,
                            "horizontal_thrust_n": hk, "vertical_down_thrust_n": excess*G/8,
                            "target_n": target})
        # External hardware/cables are charged in mass. Their spatial moments also matter.
        extra_moment = (0., 0., 0.)
        for row in all_rows:
            original = LAYOUT[row["id"]]
            station = row["station"]
            cg_act = station["actuator_cg_m"]
            force_act = (station["actuator_drag_n"]*w[0], station["actuator_drag_n"]*w[1], -MAIN_ACT["mass_kg"]*G)
            extra_moment = add(extra_moment, cross(cg_act, force_act))
            extra_moment = add(extra_moment, cross(station["bracket_cg_m"], (station["bracket_drag_n"]*w[0],station["bracket_drag_n"]*w[1],-BRACKET_MASS*G)))
            extra_moment = add(extra_moment, cross(row["cg_m"], mul(row["q_n_per_reference_m"], -row["free_length_m"])))
        thrust_moment = (-depth*total_drag*w[1], depth*total_drag*w[0], 0.)
        updated = (-(extra_moment[1]+thrust_moment[1])/(4*G*mr),
                   (extra_moment[0]+thrust_moment[0])/(4*G*mr), 0.)
        error = norm(sub(updated, amplitudes))
        if error < 1e-7: break
        amplitudes = updated
    else: raise ArithmeticError("distributed moment/trim iteration bound reached")
    moments = add(extra_moment, thrust_moment)
    for row, centre in zip(modules, GEO["modules"]):
        moments = add(moments, cross(centre, (0.,0.,-row["physical_mass_kg"]*G)))
    shaft=[]
    for row in modules:
        resultant=sqrt(row["horizontal_thrust_n"]**2+row["vertical_down_thrust_n"]**2)
        axial=wind*row["horizontal_thrust_n"]/resultant if resultant else 0.
        induced=(sqrt(axial*axial+2*resultant/(s["rho_air"]*pi*2**2))-axial)/2
        shaft.append(resultant*(axial+induced)/.7/1000)
    moved_water=.5*sum(abs(row["water_kg"]-ballast/8) for row in modules)
    return {"altitude_m": h, "wind_ms": wind, "wind_azimuth_deg": azimuth*180/pi,
            "gas_superheat_k": hot, "foundation": foundation[0],
            "foundation_translation_n_m": foundation[1], "foundation_rotation_nm_rad": foundation[2],
            "budget": b, "fixed_water_ballast_kg": ballast, "vertical_downforce_n": excess*G,
            "hull_drag_n": hull_drag, "station_drag_n": station_drag, "cable_drag_n": cable_drag,
            "total_drag_n": total_drag, "modules": modules, "lines": all_rows,
            "settled_water_shift_kg":moved_water,"optimistic_parallel_transfer_time_s":moved_water/(1000*.04),
            "total_shaft_proxy_kw":sum(shaft),"maximum_module_shaft_proxy_kw":max(shaft),
            "shaft_proxy_qualification":"axial-momentum tilt proxy with assumed0.70 loss factor; no rated propulsion or energy claim",
            "minimum_tension_n": min(r["minimum_tension_n"] for r in all_rows),
            "maximum_upper_tension_n": max(norm(r["ntop_n"]) for r in all_rows),
            "maximum_rope_extension_m": max(r["extension_m"] for r in all_rows),
            "maximum_sampled_sag_m": max(r["maximum_sampled_sag_m"] for r in all_rows),
            "actuator_command_range_m": [min(r["station"]["actuator_command_m"] for r in all_rows), max(r["station"]["actuator_command_m"] for r in all_rows)],
            "stroke_ok": all(MAIN_MIN <= r["station"]["actuator_command_m"] <= MAIN_MAX for r in all_rows),
            "water_module_limits_ok": all(0 <= r["water_kg"] <= BASE["cradle"]["water_capacity_each_kg"] and 0 < r["physical_mass_kg"] <= 25000 for r in modules),
            "checks": {"trim_iterations": trim_iteration+1, "trim_amplitude_change_kg": error,
                       "node_force_residual_n": max(c["force_residual_n"] for c in all_checks),
                       "endpoint_residual_m": max(c["endpoint_residual_m"] for c in all_checks),
                       "whole_moment_residual_nm": moments,
                       "whole_vertical_residual_n": (b["gross_kg"]-b["total_kg"]-ballast)*G-excess*G}}


def reference():
    lengths = [r["chord_m"]-MAIN_COMMAND0 for r in LAYOUT]
    for iteration in range(6):
        hull = construction(lengths)
        bs = budgets(hull)
        ballast = min(b["margin_kg"] for b in bs["M20"])
        ref = case(hull, ballast, 0., 0., STIFFNESS[1])
        updated = [r["free_length_m"] for r in ref["lines"]]
        change = abs(sum(updated)-sum(lengths))*MU
        lengths = updated
        if change < 1e-7: break
    else: raise ArithmeticError("mass/reference calibration bound reached")
    hull = construction(lengths)
    ballast = min(b["margin_kg"] for b in budgets(hull)["M20"])
    return hull, ballast, lengths, ref, {"iterations": iteration+1, "last_mass_change_kg": change}


def bag_state(h, hot=0.):
    s = old.gas(INV, h, hot)
    rho_b = (s["ambient_pa"]+1250)/(old.RA*s["ambient_k"])
    rho_g = (INV["helium_kg"]+INV["impurity_air_kg"])/s["helium_space_m3"]
    gradient = (rho_b-rho_g)*G
    extrema = [250-gradient*(c[2]+sign*GEO["bag_radius_m"])
               for c in GEO["bag_centres"] for sign in (-1,1)]
    inside_air = s["ballonet_air_m3"]-BASE["pressure_system"]["inside_duct_air_m3"]
    helium_tube_volume = sum(r["length_m"]*pi*.24**2/4 for r in GUIDES)
    equivalent = (3*(inside_air+helium_tube_volume)/(16*pi))**(1/3) if inside_air >= 0 else None
    return {"gas": s, "common_datum_z_m": 0., "common_datum_dp_pa": 250.,
            "gradient_pa_m": gradient, "design_envelope_dp_min_pa": min(extrema),
            "design_envelope_dp_max_pa": max(extrema), "positive_full_envelope": min(extrema)>0,
            "lobe_air_m3_total": inside_air, "equivalent_equal_occupied_radius_m": equivalent,
            "occupied_radius_is_not_shape_solution": True, "helium_pass_through_volume_bound_m3": helium_tube_volume,
            "apparent_lobe_air_kg": max(0.,inside_air)*(rho_b-rho_g),
            "density_ballonet_kg_m3": rho_b, "density_lifting_kg_m3": rho_g,
            "capacity_ok": s["capacity_ok"] and s["ballonet_air_m3"] >= BASE["pressure_system"]["rigid_air_m3_upper_bound"]}


def hanger_axial(free_length, lower_tension, guide):
    linear_mass = HANGER_A*1440+.2
    guide_mass = guide["mass_kg"] if guide else 0.
    midpoint = (guide["start_m"]+guide["end_m"])/(2*GEO["hangers"][guide["hanger"]]["length_m"]) if guide else .5
    top_tension = lower_tension+linear_mass*free_length*G+guide_mass*G
    extension = (lower_tension*free_length+linear_mass*G*free_length**2/2+
                 guide_mass*G*free_length*(1-midpoint))/HANGER_EA
    return top_tension, extension


def hanger_reference_lengths():
    state = bag_state(0.)
    fixed = BASE["bag_supported_mass_bound_kg"]-BASE["bag_apparent_capacity_kg"]
    tension = (state["apparent_lobe_air_kg"]+fixed)*G/32
    kband = 4*5e9*(.25*BASE["bag_cradle_band_mm"]/1000)/(2*pi*GEO["bag_radius_m"])
    result = []
    for i, hanger in enumerate(GEO["hangers"]):
        guide = next((g for g in GUIDES if g["hanger"] == i), None)
        lo, hi = 0., hanger["length_m"]
        for _ in range(45):
            length = (lo+hi)/2
            upper, extension = hanger_axial(length, tension, guide)
            required = (length+extension+tension/kband+(upper+BAG_ACT["mass_kg"]*G)/2e6+
                        BAG_COMMAND0+upper/BAG_ACT["axial_stiffness_n_m"])
            if required > hanger["length_m"]: hi = length
            else: lo = length
        result.append((lo+hi)/2)
    return result


HANGER_FREE_LENGTHS = hanger_reference_lengths()


def hangers(h, hot, foundation, contact=False):
    """Finite hanger/band compliance and one declared bounded cuff-contact load.

    Contact: +x uniform pressure cap on each liner, equal opposite force on its
    foreign bag. Natural pendulum stiffness and finite cradle bands close four
    bag horizontal balances; no imaginary fixed lateral bag anchor. Small-slope
    string response bounds the liner's possible bending demand, not a coupled
    shell/contact solution.
    """
    state = bag_state(h, hot)
    kf = foundation[1]
    kband = 4*5e9*(.25*BASE["bag_cradle_band_mm"]/1000)/(2*pi*GEO["bag_radius_m"])
    bag_fixed = BASE["bag_supported_mass_bound_kg"]-BASE["bag_apparent_capacity_kg"]
    lower_tension = (state["apparent_lobe_air_kg"]+bag_fixed)*G/32
    liner_q = max(abs(state["design_envelope_dp_min_pa"]), abs(state["design_envelope_dp_max_pa"]))* .24 if contact else 0.
    loads, stiffness, source, foreign = [], [0.]*4, [0.]*4, [0.]*4
    for i, hanger in enumerate(GEO["hangers"]):
        guide = next((g for g in GUIDES if g["hanger"] == i), None)
        _, extension = hanger_axial(HANGER_FREE_LENGTHS[i], lower_tension, guide)
        length = HANGER_FREE_LENGTHS[i]+extension
        # Preserve the paid rigid liner's physical span; the rope slides through
        # saddles/boots as the upper adjuster and finite cradle pad move.
        a, b = (guide["start_m"]-lower_tension/kband,
                guide["end_m"]-lower_tension/kband) if guide else (0.,0.)
        if guide: assert 0 <= a < b <= length
        force = liner_q*(b-a)
        r0 = force*(1-(a+b)/(2*length))
        effective_k = 1/(length/lower_tension+1/kf+1/kband)
        forcing = effective_k*(force/kf+r0*length/lower_tension)
        owner = hanger["bag"]
        stiffness[owner] += effective_k
        source[owner] += forcing
        if guide: foreign[guide["foreign_bag"]] += force
        loads.append((length, guide, a, b, force, r0, effective_k, forcing))
    centres_x = [(source[b]-foreign[b])/stiffness[b] for b in range(4)]
    rows, balances = [], [-v for v in foreign]
    for i, (hanger, load) in enumerate(zip(GEO["hangers"], loads)):
        length, guide, a, b, force, r0, keff, forcing = load
        bottom_force = forcing-keff*centres_x[hanger["bag"]]
        top_force = force-bottom_force
        x0 = centres_x[hanger["bag"]]+bottom_force/kband
        xL = top_force/kf
        balances[hanger["bag"]] += bottom_force
        # Tube gravity is a load on its host hanger, not equalized onto all bags.
        top_tension, elastic = hanger_axial(HANGER_FREE_LENGTHS[i], lower_tension, guide)
        def x_at(z):
            return x0+(xL-x0)*z/length+r0*z/lower_tension-(liner_q/(2*lower_tension))*max(0.,z-a)**2+(liner_q/(2*lower_tension))*max(0.,z-b)**2
        def slope_at(z):
            return (xL-x0+r0*length/lower_tension)/length-(liner_q/lower_tension)*max(0.,z-a)+(liner_q/lower_tension)*max(0.,z-b)
        # Exact integrals of the piecewise-linear slope squared.
        knots = sorted(set((0., a, b, length)))
        geometric_excess = sum((v-u)*(slope_at(u)**2+slope_at(u)*slope_at(v)+slope_at(v)**2)/6
                               for u,v in zip(knots,knots[1:]))
        top_drop = (top_tension+BAG_ACT["mass_kg"]*G)/kf
        band_rise = lower_tension/kband
        vertical_span = length-geometric_excess
        command = (hanger["length_m"]-top_drop-band_rise-vertical_span-
                   top_tension/BAG_ACT["axial_stiffness_n_m"])
        base_low = hanger["low"]
        pts = [(base_low[0]+x_at(length*j/16),base_low[1],base_low[2]+band_rise+vertical_span*j/16)
               for j in range(17)]
        curvature_error = (liner_q/lower_tension)*(length/16)**2/8 if guide else 0.
        # A liner following the string bound has curvature <=q/T; beam coupling remains unresolved.
        liner_bend_stress = 70e9*.12*liner_q/lower_tension if guide else 0.
        clamp_reaction = liner_q*1.5 if guide else 0.
        rows.append({"id": i, "bag": hanger["bag"], "points": pts, "host_guide": guide,
                     "lower_vertical_tension_n": lower_tension, "upper_vertical_tension_n": top_tension,
                     "bottom_horizontal_reaction_n": bottom_force, "top_horizontal_reaction_n": top_force,
                     "bottom_cradle_displacement_m": bottom_force/kband, "top_foundation_displacement_m": top_force/kf,
                     "elastic_extension_m": elastic, "geometric_excess_m": geometric_excess,
                     "free_length_m": HANGER_FREE_LENGTHS[i], "band_vertical_extension_m": band_rise,
                     "top_drop_m": top_drop, "actuator_command_m": command, "stroke_ok": BAG_MIN <= command <= BAG_MAX,
                     "maximum_abs_slope": max(abs(slope_at(z)) for z in knots),
                     "curvature_error_m": curvature_error, "liner_following_stress_pa": liner_bend_stress,
                     "clamp_side_reaction_n": clamp_reaction})
    shifted = [add(c,(x,0.,0.)) for c,x in zip(GEO["bag_centres"],centres_x)]
    bag_gap = min(norm(sub(a,b))-2*GEO["bag_radius_m"] for i,a in enumerate(shifted) for b in shifted[:i])
    hull_gap = min(R-norm(c)-GEO["bag_radius_m"] for c in shifted)
    # Equal gas/fabric distribution between four lobes; include actual moving air mass.
    first_moment = sum(centres_x)*(state["lobe_air_m3_total"]*state["density_ballonet_kg_m3"]+bag_fixed)/4
    return {"contact": "one_sided_pressure_cap_plus_x" if contact else "no_lateral_cuff_force",
            "state": state, "cradle_band_assumed_modulus_pa": 5e9, "cradle_lateral_stiffness_n_m": kband,
            "bag_centre_shift_x_m": centres_x, "bag_centres": shifted,
            "minimum_bag_envelope_gap_m": bag_gap, "minimum_bag_to_hull_gap_m": hull_gap,
            "bag_horizontal_balance_residual_n": max(abs(v) for v in balances),
            "maximum_hanger_slope": max(r["maximum_abs_slope"] for r in rows),
            "linear_slope_screen_ok": max(r["maximum_abs_slope"] for r in rows) <= .2,
            "all_bag_actuator_strokes_ok": all(r["stroke_ok"] for r in rows),
            "bag_actuator_command_range_m": [min(r["actuator_command_m"] for r in rows),max(r["actuator_command_m"] for r in rows)],
            "additional_water_trim_cos_amplitude_kg": -first_moment/(4*GEO["module_radius_m"]),
            "liner_following_strength_screen_ok": max(r["liner_following_stress_pa"] for r in rows)*1.5 <= 100e6,
            "rows": rows}


def closest_segments(p, q, r, s):
    u,v,w = sub(q,p),sub(s,r),sub(p,r)
    a,b,c,d,e = dot(u,u),dot(u,v),dot(v,v),dot(u,w),dot(v,w)
    den = a*c-b*b
    candidates=[]
    if den > 1e-12*a*c:
        t,z=(b*e-c*d)/den,(a*e-b*d)/den
        if 0 <= t <= 1 and 0 <= z <= 1: candidates.append((t,z))
    for t in (0.,1.): candidates.append((t,max(0.,min(1.,(e+b*t)/c))))
    for z in (0.,1.): candidates.append((max(0.,min(1.,(b*z-d)/a)),z))
    t,z=min(candidates,key=lambda tz: norm(add(w,sub(mul(u,tz[0]),mul(v,tz[1])))))
    pa,pb=add(p,mul(u,t)),add(r,mul(v,z))
    return norm(sub(pa,pb)),pa,pb,t,z


def point_segment(p, a, b):
    d=sub(b,a);t=max(0.,min(1.,dot(sub(p,a),d)/dot(d,d)))
    return norm(sub(p,add(a,mul(d,t))))


def paths(main, bag, foundation):
    result=[]
    for row in main["lines"]:
        length=row["free_length_m"]
        ss=[.5+(length-.65)*j/16 for j in range(17)]
        pts=[add(LAYOUT[row["id"]]["low"],curve(row["n0_n"],row["q_n_per_reference_m"],s)) for s in ss]
        err=norm(row["q_n_per_reference_m"])*(1/row["minimum_tension_n"]+1/EA)*((length-.65)/16)**2/8
        # The secant foundation law uses small rotations. Bound omitted second-order pin geometry.
        support_error=STANDOFF_RADIAL*norm(row["station"]["rotation_rad"])**2/2
        err+=support_error
        result.append({"label":f'main-{row["id"]}',"kind":"main","id":row["id"],"points":pts,"radius":ROPE_RADIUS,"error":err,"reference_s":ss})
        station=row["station"];direction=unit(sub(station["upper_pin"],station["lower_pin"]))
        result.append({"label":f'actuator-{row["id"]}',"kind":"station","id":row["id"],
                       "points":[add(station["lower_pin"],mul(direction,.15)),sub(station["upper_pin"],mul(direction,.15))],"radius":.12,"error":support_error})
        for j,base in enumerate(LAYOUT[row["id"]]["leg_bases"]):
            # Base follows finite foundation translation/rotation to first order.
            displacement=add(add(station["foundation_translation_m"],station["plate_flex_m"]),
                             cross(station["rotation_rad"],sub(base,LAYOUT[row["id"]]["skin"])))
            result.append({"label":f'leg-{row["id"]}-{j}',"kind":"station","id":row["id"],
                           "points":[add(base,displacement),station["upper_pin"]],"radius":.05,"error":support_error})
        original=LAYOUT[row["id"]]
        root=add(original["skin"],station["foundation_translation_m"])
        # Circumscribed capsule encloses the full1m-square plate; own bedding is intentional.
        n=original["normal"]
        result.append({"label":f'plate-{row["id"]}',"kind":"station","id":row["id"],
                       "points":[root,add(root,mul(n,PLATE_THICKNESS))],"radius":sqrt(.5**2+.5**2),"error":support_error+norm(station["plate_flex_m"])})
    for row in bag["rows"]:
        result.append({"label":f'hanger-{row["id"]}',"kind":"hanger","id":row["id"],
                       "points":row["points"],"radius":.14 if row["host_guide"] else .035,"error":row["curvature_error_m"]})
        original=GEO["hangers"][row["id"]]
        pin=add(original["top"],(row["top_foundation_displacement_m"],0.,-row["top_drop_m"]))
        low=row["points"][-1];direction=unit(sub(pin,low))
        result.append({"label":f'bag-actuator-{row["id"]}',"kind":"bag_station","id":row["id"],
                       "points":[add(low,mul(direction,.1)),sub(pin,mul(direction,.1))],"radius":.07,"error":0.})
    duct_d=BASE["pressure_system"]["duct_diameter_m"]
    rho_b=bag["state"]["density_ballonet_kg_m3"]
    q=(pi*duct_d*.001*2700+1+rho_b*pi*duct_d**2/4)*G
    ei=70e9*pi*(duct_d**4-(duct_d-.002)**4)/64
    # The existing paid 4m supports have declared finite secant stiffness, not fixed anchors.
    duct_k=foundation[1]/5
    duct_bound=q*4/duct_k+5*q*4**4/(384*ei)
    for i,duct in enumerate(GEO["ducts"]):
        for j,(a,b) in enumerate(zip(duct["points"],duct["points"][1:])):
            low=add(a,mul(unit(sub(b,a)),3.)) if j==0 else a
            result.append({"label":f'duct-{i}-{j}',"kind":"duct","id":i,
                           "points":[low,b],"radius":duct_d/2+.03,"error":duct_bound})
    for p in result:
        p["aabb"]=[(min(v[j] for v in p["points"])-p["radius"]-p["error"],max(v[j] for v in p["points"])+p["radius"]+p["error"]) for j in range(3)]
    return result,duct_bound


def clearance(main, bag, foundation):
    ps,duct_bound=paths(main,bag,foundation)
    best={"gap_bound_m":float("inf")};main_best={"gap_bound_m":float("inf")}
    for i,a in enumerate(ps):
        for b in ps[:i]:
            if a["id"]==b["id"] and ({a["kind"],b["kind"]} <= {"main","station"} or
                                      {a["kind"],b["kind"]} <= {"hanger","bag_station"} or a["kind"]==b["kind"]=="duct"):
                continue  # one connected actuator/standoff assembly or a single intentional duct elbow
            lower=sqrt(sum(max(0.,lo1-hi2,lo2-hi1)**2 for (lo1,hi1),(lo2,hi2) in zip(a["aabb"],b["aabb"])))
            interesting=max(best["gap_bound_m"],main_best["gap_bound_m"]) if a["kind"]==b["kind"]=="main" else best["gap_bound_m"]
            if lower > max(interesting,0.): continue
            for ia,(p,q) in enumerate(zip(a["points"],a["points"][1:])):
                for ib,(r,s) in enumerate(zip(b["points"],b["points"][1:])):
                    distance,pa,pb,ta,tb=closest_segments(p,q,r,s)
                    gap=distance-a["radius"]-b["radius"]-a["error"]-b["error"]
                    record={"gap_bound_m":gap,"a":a["label"],"b":b["label"],"point_a_m":pa,"point_b_m":pb,
                            "centreline_separation_m":distance,"radii_m":[a["radius"],b["radius"]],"curve_and_support_allowance_m":a["error"]+b["error"]}
                    if a["kind"]==b["kind"]=="main":
                        for pth,index,t,key in ((a,ia,ta,"a"),(b,ib,tb,"b")):
                            ss=pth["reference_s"][index]*(1-t)+pth["reference_s"][index+1]*t
                            row=main["lines"][pth["id"]];original=LAYOUT[pth["id"]]
                            exact=add(original["low"],curve(row["n0_n"],row["q_n_per_reference_m"],ss))
                            chord=add(original["low"],mul(sub(row["station"]["lower_pin"],original["low"]),ss/row["free_length_m"]))
                            record[f"reference_s_{key}_m"]=ss;record[f"sag_vector_{key}_m"]=sub(exact,chord)
                        if gap < main_best["gap_bound_m"]:main_best=record
                    if gap < best["gap_bound_m"]:best=record
    external=[p for p in ps if p["kind"]=="main" or (p["kind"]=="station" and p["label"].startswith("actuator"))]
    hull_gap=min(point_segment((0.,0.,0.),a,b)-R-p["radius"]-p["error"] for p in external for a,b in zip(p["points"],p["points"][1:]))
    bag_gap=min(point_segment(c,a,b)-GEO["bag_radius_m"]-p["radius"]-p["error"] for p in external for a,b in zip(p["points"],p["points"][1:]) for c in bag["bag_centres"])
    return {"all_represented_paths":best,"main_to_main":main_best,"main_actuator_to_hull_gap_m":hull_gap,
            "main_actuator_to_design_bags_gap_m":bag_gap,"duct_support_displacement_bound_m":duct_bound,
            "positive_capsule_clearance":best["gap_bound_m"]>0 and hull_gap>0 and bag_gap>0,
            "exclusions":"0.5m lower reference-coordinate apex capture; own connected rope/actuator/standoff assembly; standoff-to-own-skin bedding; same-duct elbows and first3m common manifold; designated bag cuffs and own hanger-to-bag attachments. Rotors, folding surfaces and flexible ballast/lower slings are not certified by this capsule check."}


def hardware_screens(cases):
    reactions = [r for c in cases for r in c["lines"]]
    maximum_n = max(norm(r["ntop_n"]) for r in reactions)
    loads = [norm(r["station"]["load_n"]) for r in reactions]
    moments = [norm(r["station"]["moment_nm"]) for r in reactions]
    # Four elastic legs distribute the concurrent force; add a conservative couple term.
    leg_peak = 0.
    for row in reactions:
        original = LAYOUT[row["id"]]
        vectors = [unit(sub(original["anchor"],b)) for b in original["leg_bases"]]
        gram = [[sum(v[i]*v[j] for v in vectors) for j in range(3)] for i in range(3)]
        dual = solve(gram, row["station"]["load_n"])
        leg_peak = max(leg_peak, max(abs(dot(v,dual)) for v in vectors)+norm(row["station"]["moment_nm"])/(2*.3))
    plate_stress = 1.5*(max(loads)/4+max(moments)/(.6*4))*.3/(.25*.07**2/6)
    max_bag_force = max(r["upper_vertical_tension_n"] for c in cases for r in c["hangers"]["rows"])
    max_power = sum(norm(r["ntop_n"])*.005/.65 for r in max(cases,key=lambda c: sum(norm(r["ntop_n"]) for r in c["lines"]))["lines"])
    return {"main_rope_limit_demand_n": 1.5*maximum_n, "main_rope_working_capacity_n": 150e6*AREA,
            "main_rope_strength_ok": 1.5*maximum_n <= 150e6*AREA,
            "main_adjuster_limit_demand_n": 1.5*maximum_n, "main_adjuster_tensile_capacity_n": MAIN_ACT["tensile_force_rating_n"],
            "main_adjuster_force_ok": 1.5*maximum_n <= MAIN_ACT["tensile_force_rating_n"],
            "main_adjuster_rod_stress_pa": 1.5*maximum_n/MAIN_ACT["rod_area_m2"],
            "main_adjuster_25mpa_von_mises_pa": MAIN_ACT["von_mises_inner_pa"],
            "maximum_foundation_displacement_m": max(norm(r["station"]["displacement"]) for r in reactions),
            "maximum_foundation_rotation_rad": max(norm(r["station"]["rotation_rad"]) for r in reactions),
            "maximum_station_load_n": max(loads), "maximum_station_moment_nm": max(moments),
            "leg_limit_axial_stress_pa": 1.5*leg_peak/LEG_AREA,
            "leg_euler_over_four_n": pi*pi*70e9*LEG_I/LEG_LENGTH**2/4,
            "leg_limit_force_n": 1.5*leg_peak,
            "plate_limit_strip_stress_pa": plate_stress,
            "metal_working_stress_pa": 100e6,
            "metal_scalar_ok": 1.5*leg_peak/LEG_AREA <= 100e6 and plate_stress <= 100e6,
            "bag_hanger_limit_force_n": 1.5*max_bag_force,
            "bag_hanger_working_capacity_n": 150e6*HANGER_A,
            "bag_adjuster_tensile_capacity_n": BAG_ACT["tensile_force_rating_n"],
            "bag_adjuster_force_ok": 1.5*max_bag_force <= BAG_ACT["tensile_force_rating_n"],
            "simultaneous_main_adjustment_power_at_5mm_s_kw": max_power/1000,
            "simultaneous_bag_adjustment_power_at_5mm_s_kw":max(sum(r["upper_vertical_tension_n"] for r in c["hangers"]["rows"]) for c in cases)*.005/.65/1000,
            "power_rating_and_rate_are_unqualified": True,
            "curtain_double_patch_strip_demand_kn_m": BASE["global_line_kn_m"]+1.5*max(loads)/20/1000+1.5*max(moments)/(.6*20)/1000,
            "curtain_double_patch_strip_capacity_kn_m": BASE["doubled_patch_capacity_kn_m"],
            "local_bearing_joint_buckling_shape_and_dynamic_response": "UNKNOWN"}


def adverse_screens(hull, ballast, lengths, ref):
    """Six formal direction/trim screens; no feasible loaded curve is asserted."""
    rows=[]
    fixed=15000+hull["cradle"]["over_3000kg_allowance_kg"]+3000
    for h in (0.,2500.):
        rho=old.atm(h)[2]
        excess=old.budget(INV,hull,h,3000)["margin_kg"]-ballast
        for wind in (10.,20.,30.):
            hull_drag=.8*.5*rho*wind**2*pi*38**2
            station_drag=24*.5*rho*wind**2*1.2*(ACTUATOR_DRAG_AREA+BRACKET_DRAG_AREA)
            cable_drags=[-cable_force_density(r,wind,rho,0)[0]*l for r,l in zip(LAYOUT,lengths)]
            total_drag=hull_drag+station_drag+sum(cable_drags)
            distributed_moment=sum((r["station"]["actuator_cg_m"][2]*ACTUATOR_DRAG_AREA+r["station"]["bracket_cg_m"][2]*BRACKET_DRAG_AREA)*.5*rho*wind**2*1.2+
                                   r["cg_m"][2]*drag for r,drag in zip(ref["lines"],cable_drags))
            amplitude=-(GEO["thrust_depth_m"]*total_drag+distributed_moment)/(4*G*GEO["module_radius_m"])
            waters=[];tensions=[];module_masses=[]
            for k in range(8):
                phi=k*pi/4
                wk=ballast/8+amplitude*cos(phi);mk=fixed/8+wk
                weight=(mk+excess/8)*G
                hk=total_drag*weight/((fixed+ballast+excess)*G)
                ring=BASE["ballast_system"]["inward_reaction_per_module_n"]
                target=(hk+ring*cos(phi),ring*sin(phi),weight)
                tensions+=old.solve3([r["unit"] for r in LAYOUT[3*k:3*k+3]],target)
                waters.append(wk);module_masses.append(mk)
            peak=1000+BASE["head_pa"]+1.5*.5*rho*wind**2
            strip=peak*38/2+(1.5*300000*G+1.5*total_drag)/(2*pi*38)
            rows.append({"altitude_m":h,"wind_ms":wind,"minimum_formal_chord_tension_n":min(tensions),
                         "minimum_water_kg":min(waters),"maximum_module_kg":max(module_masses),
                         "directions_ok":min(tensions)>=0,
                         "water_module_limits_ok":min(waters)>=0 and max(waters)<=BASE["cradle"]["water_capacity_each_kg"] and max(module_masses)<=25000,
                         "membrane_strip_kn_m":strip/1000,"membrane_strip_ok":strip/1000<=BASE["skin_working_line_kn_m"],
                         "positive_outer_pressure":1000-BASE["head_pa"]-1.5*.5*rho*wind**2>0,
                         "loaded_shape":"NOT SOLVED; prior adverse failures not superseded by a chord diagnostic"})
    return rows


def pressure_flow(h, hot):
    s=old.gas(INV,h,hot)
    p,t=s["ambient_pa"],s["ambient_k"]
    gas_gradient=-old.LAPSE/(t+hot)+G/(old.RA*t)*p/(p+1000)
    air_gradient=-old.LAPSE/t+G/(old.RA*t)*p/(p+1250)
    internal=(s["helium_space_m3"]*(gas_gradient+10/(3600*(t+hot)))+
              (s["ballonet_air_m3"]+BASE["pressure_system"]["external_pressure_air_m3"])*air_gradient)
    inlet=internal*(p+1250)/p
    return {"altitude_m":h,"gas_superheat_k":hot,"descent_m_s":1.,"additional_gas_cooling_k_h":10.,
            "internal_flow_m3_s":internal,"ambient_inlet_flow_m3_s":inlet,
            "one_blower_out_capacity_m3_s":BASE["pressure_system"]["one_out_m3s"],
            "flow_capacity_screen_ok":inlet<=BASE["pressure_system"]["one_out_m3s"]}


if __name__ == "__main__":
    hull, ballast, lengths, ref, convergence = reference()
    selected = [(f,h,w,0.,0.) for f in STIFFNESS for h in (0.,2500.) for w in (0.,5.)]
    selected += [(STIFFNESS[1],h,w,10.,0.) for h in (0.,2500.) for w in (0.,5.)]
    selected += [(STIFFNESS[1],h,5.,0.,pi/8) for h in (0.,2500.)]
    rows=[]
    for f,h,w,hot,angle in selected:
        c=case(hull,ballast,h,w,f,lengths,hot,angle)
        bag=hangers(h,hot,f)
        c["hangers"]=bag
        c["clearance"]=clearance(c,bag,f)
        assert c["checks"]["node_force_residual_n"] < 1e-5
        assert c["checks"]["endpoint_residual_m"] < 1e-8
        assert max(abs(v) for v in c["checks"]["whole_moment_residual_nm"]) < 1e-3
        assert c["checks"]["whole_vertical_residual_n"] == 0
        rows.append(c)
    contacts=[hangers(h,t,STIFFNESS[1],True) for h,t in ((0.,0.),(2500.,0.),(0.,10.),(2500.,10.))]
    hot_limit=old.atm(2500.)[1]*((INV["free_m3"]-BASE["pressure_system"]["rigid_air_m3_upper_bound"])/(.95*INV["free_m3"])-1)
    assert not bag_state(2500.,15.)["capacity_ok"]
    assert all(c["hangers"]["state"]["helium_pass_through_volume_bound_m3"] < 50 for c in rows)
    output={"calculator_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "source_calculator_sha256":SOURCE_SHA,"corrected_source_commit":"89e8a7ddd4c79871072075145f5ad24b36a0157e",
            "inventory":INV,"construction":hull["mass_kg"],"construction_kg":hull["construction_kg"],
            "construction_change_from_i010_kg":hull["construction_kg"]-BASE["construction_kg"],
            "budgets":budgets(hull),"fixed_water_ballast_kg":ballast,"layout":LAYOUT,
            "main_adjuster":MAIN_ACT,"bag_adjuster":BAG_ACT,"standoff_parts_each_kg":BRACKET_PARTS,
            "main_command_min_nominal_max_m":[MAIN_MIN,MAIN_COMMAND0,MAIN_MAX],
            "bag_command_min_nominal_max_m":[BAG_MIN,BAG_COMMAND0,BAG_MAX],
            "main_free_lengths_m":lengths,"bag_free_lengths_m":HANGER_FREE_LENGTHS,
            "main_cable_area_m2":AREA,"main_cable_modulus_pa":50e9,"bag_hanger_diameter_m":HANGER_D,
            "additional_drag_area_per_station_m2":{"actuator":ACTUATOR_DRAG_AREA,"bracket":BRACKET_DRAG_AREA},
            "hydraulic_parts_kg":HYDRAULIC_PARTS,"guides":GUIDES,
            "pressure_system":BASE["pressure_system"],"ballast_system":BASE["ballast_system"],
            "cold_hot_pressure_flow":[pressure_flow(h,t) for h in (0.,2500.) for t in (0.,10.)],
            "reference_checks":convergence,"hardware_screens":hardware_screens(rows),
            "cases":rows,"contact_screens":contacts,"adverse_screens":adverse_screens(hull,ballast,lengths,ref),
            "rigid_duct_hot_limit_k":hot_limit,"same_inventory_hot_15k":bag_state(2500.,15.),
            "checks":"PASS: selected arithmetic and main-line force/compatibility checks. Physical design UNKNOWN/FAIL at bag pressure/contact; P100 buoyant mission FAIL."}
    print(json.dumps(output,indent=2))
