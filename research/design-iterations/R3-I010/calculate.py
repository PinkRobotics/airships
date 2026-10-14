#!/usr/bin/env python3
"""R3-I010 bounded arithmetic: ideal nodes and geometric screens, not qualification.

Only the Python standard library is used. No optimizer, simulation or file writes.
All mass inputs without a cited selected material/component remain assumptions.
"""
import json
from math import ceil, cos, pi, sin, sqrt

P0, T0, RA, RU, G, LAPSE = 101325., 288.15, 287.05, 8.314462618, 9.80665, .0065
MHE, MAIR = .004002602, RU / RA
D0, V0 = 70.57485803146756, 181394.53949136072
VOLUME_RATIO = V0 / (pi * D0**3 / 6)
EQUIPMENT = {"pressure_control": 2000., "propulsion": 3000., "energy": 5000.,
             "avionics": 1000., "local_cradles": 3000., "ground_ballast": 3000.}


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def sub(a, b):
    return tuple(x-y for x, y in zip(a, b))


def norm(a):
    return sqrt(dot(a, a))


def atm(h):
    t = T0 - LAPSE*h
    p = P0*(t/T0)**(G/(RA*LAPSE))
    return p, t, p/(RA*t)


def solve3(columns, target):
    """One nonsingular three-cable balance, using partial-pivot elimination."""
    a = [[columns[j][i] for j in range(3)] + [target[i]] for i in range(3)]
    for i in range(3):
        j = max(range(i, 3), key=lambda j: abs(a[j][i]))
        a[i], a[j] = a[j], a[i]
        assert abs(a[i][i]) > 1e-10
        d = a[i][i]
        a[i] = [x/d for x in a[i]]
        for j in range(3):
            if j != i:
                d = a[j][i]
                a[j] = [a[j][k]-d*a[i][k] for k in range(4)]
    return [a[i][3] for i in range(3)]


def segment_distance(p, q, r, s):
    """Exact minimum over two closed straight segments: interior plus four edges."""
    u, v, w = sub(q, p), sub(s, r), sub(p, r)
    a, b, c, d, e = dot(u, u), dot(u, v), dot(v, v), dot(u, w), dot(v, w)
    candidates = []
    den = a*c-b*b
    if den > 1e-12*a*c:
        t, z = (b*e-c*d)/den, (a*e-b*d)/den
        if 0 <= t <= 1 and 0 <= z <= 1:
            candidates.append((t, z))
    for t in (0., 1.):
        candidates.append((t, max(0., min(1., (e+b*t)/c))))
    for z in (0., 1.):
        candidates.append((max(0., min(1., (b*z-d)/a)), z))
    return min(norm(tuple(w[i]+t*u[i]-z*v[i] for i in range(3)))
               for t, z in candidates)


def sphere_chord(p, q, centre, radius):
    d, w = sub(q, p), sub(p, centre)
    a, b, c = dot(d, d), dot(w, d), dot(w, w)-radius**2
    disc = b*b-a*c
    if disc <= 0:
        return 0.
    lo, hi = max(0., (-b-sqrt(disc))/a), min(1., (-b+sqrt(disc))/a)
    return max(0., hi-lo)*sqrt(a)


def inventory(d, purity=.96):
    external = pi*d**3/6*VOLUME_RATIO
    free = external-100.  # common non-gas volume debit, not extra mass
    p, t, _ = atm(2500.)
    mol = (p+1000.)*.95*free/(RU*t)
    return {"diameter_m": d, "external_m3": external, "free_m3": free,
            "mol": mol, "purity_mole": purity, "helium_kg": mol*purity*MHE,
            "impurity_air_kg": mol*(1-purity)*MAIR, "ballonet_usable_m3": .30*free}


def gas(inv, h, superheat=0.):
    p, ta, rho = atm(h)
    vg = inv["mol"]*RU*(ta+superheat)/(p+1000.)
    vb = inv["free_m3"]-vg
    air = (p+1250.)*vb/(RA*ta)
    return {"altitude_m": h, "ambient_pa": p, "ambient_k": ta, "rho_air": rho,
            "helium_space_m3": vg, "ballonet_air_m3": vb, "ballonet_air_kg": air,
            "ballonet_fraction": vb/inv["free_m3"], "gross_kg": rho*inv["external_m3"],
            "capacity_ok": 0 <= vb <= inv["ballonet_usable_m3"]}


def geometry(inv):
    r = (3*inv["external_m3"]/(4*pi))**(1/3)
    modules, cables = [], []
    for k in range(8):
        phi = k*pi/4
        low = (.5*r*cos(phi), .5*r*sin(phi), -r-3.)
        modules.append(low)
        for f, delta in ((.20, 0.), (.85, -pi/10), (.85, pi/10)):
            top = (f*r*cos(phi+delta), f*r*sin(phi+delta), r*sqrt(1-f*f))
            length = norm(sub(top, low))
            cables.append({"module": k, "top": top, "low": low, "length_m": length,
                           "unit": tuple(x/length for x in sub(top, low))})
    # Four separated spherical design envelopes; occupied folded shapes are UNKNOWN.
    rb = (3*(inv["ballonet_usable_m3"]+50.)/(16*pi))**(1/3)
    a = (2*rb+.5)/(2*sqrt(2))
    centres = ((a,a,a), (a,-a,-a), (-a,a,-a), (-a,-a,a))
    hangers = []
    for b, centre in enumerate(centres):
        for j in range(8):
            angle = (j+.5)*pi/4
            low = (centre[0]+rb/sqrt(2)*cos(angle),
                   centre[1]+rb/sqrt(2)*sin(angle), centre[2]+rb/sqrt(2))
            top = (low[0], low[1], sqrt(r*r-low[0]**2-low[1]**2))
            assert top[2] > low[2]
            hangers.append({"bag": b, "top": top, "low": low, "length_m": top[2]-low[2]})
    # Common four-blower discharge manifold under the hull, then four branch ducts.
    # The shared manifold is necessary for an aggregate one-blower-out flow claim.
    ducts = []
    manifold = (0.,0.,-r-.5)
    for centre in centres:
        port = (centre[0],centre[1],centre[2]-rb)
        points = [manifold]
        if centre[2] > 0:
            # Priced 20-degree azimuthal dogleg avoids the inward main cable.
            angle = pi/9
            points.append((.75*(port[0]*cos(angle)-port[1]*sin(angle)),
                           .75*(port[0]*sin(angle)+port[1]*cos(angle)),
                           manifold[2]+.75*(port[2]-manifold[2])))
        points.append(port)
        length = sum(norm(sub(q,p)) for p,q in zip(points,points[1:]))
        ducts.append({"points":points,"length_m":length+2.+.5*(len(points)-2)})
    return {"radius_m": r, "module_radius_m": .5*r, "thrust_depth_m": r+3,
            "modules": modules, "cables": cables, "bag_radius_m": rb,
            "bag_centres": centres, "bag_outer_extent_m": norm(centres[0])+rb,
            "hangers": hangers, "ducts": ducts}


def cradle():
    # Eight 3.2 x 3.2 x 3.8 m frames; 3 m diameter x 3.6 m water bladders.
    b, h, wall = .15, .30, .006
    area = b*h-(b-2*wall)*(h-2*wall)
    ix = (b*h**3-(b-2*wall)*(h-2*wall)**3)/12
    iy = (h*b**3-(h-2*wall)*(b-2*wall)**3)/12
    span, spacing, plate = 3.2, .8, .016
    load = 1.5*25000.*G
    pressure = load/span**2
    beam_stress = (pressure*spacing*span**2/8)/(ix/(h/2))
    plate_stress = (pressure*spacing**2/8)*6/plate**2
    frame_length = 8*span+4*3.8+3*span
    # Four X-braced sides. One diagonal carries a selected 0.1 g lateral load per side.
    diag = sqrt(span**2+3.8**2)
    brace_t = 1.5*.1*25000*G*diag/span
    brace_a = brace_t/150e6
    sling_length = sqrt(2*(span/2)**2+2.**2)
    sling_t = load/(4*(2/sling_length))
    sling_a = sling_t/150e6
    water_t = ceil((1.5*1000*G*3.6*1.5/(30e6*.6))/.0001)*.0001
    water_area = 2*pi*1.5*3.6+2*pi*1.5**2
    parts = {"frames": 8*frame_length*area*2700,
             "floor_plates": 8*span**2*plate*2700,
             "frame_joints_floor_brackets": 8*(8*10+10*5),
             "side_braces": 8*8*diag*brace_a*1440,
             "brace_terminations": 8*16*5,
             "lower_slings": 8*4*sling_length*sling_a*1440,
             "lower_sling_fittings": 8*8*12,
             "water_bladders_and_10pct_laps": 8*water_area*water_t*1400*1.10,
             "water_ports": 8*4*2}
    return {"parts_kg": parts, "total_kg": sum(parts.values()),
            "over_3000kg_allowance_kg": max(0., sum(parts.values())-3000.),
            "water_capacity_each_kg": pi*1.5**2*3.6*1000,
            "module_mass_limit_kg": 25000., "water_bladder_mm": water_t*1000,
            "frame_section_mm": [300,150,6], "frame_length_each_m": frame_length,
            "beam_stress_mpa": beam_stress/1e6, "plate_stress_mpa": plate_stress/1e6,
            "column_euler_div4_kn": pi*pi*70e9*iy/3.8**2/4/1000,
            "column_limit_load_kn": load/4/1000,
            "beam_deflection_mm": 5*pressure*spacing*span**4/(384*70e9*ix)*1000,
            "lower_sling_kn": sling_t/1000, "lower_sling_length_m": sling_length,
            "brace_kn": brace_t/1000,
            "scalar_ok": max(beam_stress, plate_stress) <= 100e6 and
                         pi*pi*70e9*iy/3.8**2/4 >= load/4}


def pressure_system(inv, geo):
    rows = []
    for h in (0.,2500.):
        s = gas(inv, h)
        p, t = s["ambient_pa"], s["ambient_k"]
        bg = -LAPSE/t+G/(RA*t)*p/(p+1000)
        ba = -LAPSE/t+G/(RA*t)*p/(p+1250)
        internal = s["helium_space_m3"]*(bg+10/(3600*t))+s["ballonet_air_m3"]*ba
        rows.append({"altitude_m": h, "internal_flow_m3s": internal,
                     "inlet_flow_m3s": internal*(p+1250)/p})
    # Three operating plus one reserve; rating quantized in 2 m3/s increments.
    rating = 2*ceil(max(row["inlet_flow_m3s"] for row in rows)/3/2)
    diameter = sqrt(4*rating/(pi*12.))
    length = sum(c["length_m"] for c in geo["ducts"])
    parts = {"four_blowers": 4*250*rating/8,
             "eight_air_valves": 8*40*(rating/8)**(2/3),
             "two_emergency_helium_valves": 2*40*(rating/8)**(2/3),
             "duct_1mm_aluminium_and_rings": length*(pi*diameter*.001*2700+1.),
             "duct_supports_and_bag_ports": ceil(length/4)*10+4*15,
             "common_discharge_manifold_isolation": 250.,
             "sensors": 120., "limiters": 80., "mounts": 160.}
    inside_length = sum(sphere_chord(p,q,(0.,0.,0.),geo["radius_m"])
                        for c in geo["ducts"] for p,q in zip(c["points"],c["points"][1:]))
    outside_volume = (length-inside_length)*pi*diameter**2/4+10.
    for row in rows:
        p,t,_ = atm(row["altitude_m"])
        beta_air = -LAPSE/t+G/(RA*t)*p/(p+1250)
        extra = outside_volume*beta_air
        row["external_air_compression_m3s"] = extra
        row["internal_flow_m3s"] += extra
        row["inlet_flow_m3s"] += extra*(p+1250)/p
    assert max(row["inlet_flow_m3s"] for row in rows) <= 3*rating
    return {"flow": rows, "blower_each_m3s": rating, "one_out_m3s": 3*rating,
            "three_blower_power_kw": 3*rating*2000/.65/1000,
            "duct_diameter_m": diameter, "duct_length_m": length,
            # Conservative non-collapsible air volume; all ducts/tails counted inside.
            "rigid_air_m3_upper_bound": length*pi*diameter**2/4+10.,
            "inside_duct_air_m3":inside_length*pi*diameter**2/4,
            "external_pressure_air_m3":outside_volume,
            "parts_kg": parts, "mass_kg": sum(parts.values()),
            "over_2000kg_allowance_kg": max(0., sum(parts.values())-2000.)}


def ballast_system(geo):
    # 100 mm bore water hose with 5 mm wall and a separate 30 kN messenger.
    # Eight equal sagged spans attach at the main apices, not at crate corners.
    span = 2*geo["module_radius_m"]*sin(pi/8)
    sag = 2.
    length = span+8*sag*sag/(3*span)  # parabolic length approximation
    ring_length, branches = 8*length, 8*7.
    hose_area = pi*(.11**2-.10**2)/4
    fluid_a = pi*.10**2/4
    messenger_a = 30000./150e6
    parts = {"hose": (ring_length+branches)*hose_area*950,
             "fixed_hose_water": (ring_length+branches)*fluid_a*1000,
             "ring_messengers": ring_length*messenger_a*1440,
             "eight_pumps": 8*20., "sixteen_valves": 16*8.,
             "fittings": 16*5., "controls": 80., "mounts": 8*15.,
             "ground_tackle_allowance": 600.}
    linear_mass = hose_area*950+fluid_a*1000+messenger_a*1440
    horizontal = linear_mass*G*length/span*span**2/(8*sag)
    return {"parts_kg": parts, "mass_kg":sum(parts.values()),
            "over_3000kg_allowance_kg":max(0.,sum(parts.values())-3000.),
            "span_m":span,"sag_m":sag,"ring_hose_length_m":ring_length,
            "branch_hose_length_m":branches,"hose_od_m":.11,
            "inward_reaction_per_module_n":2*horizontal*sin(pi/8),
            "messenger_service_tension_kn":sqrt(horizontal**2+(linear_mass*G*length/2)**2)/1000,
            "eight_pump_power_kw":8*1000*G*.005*20/.65/1000,
            "all_pump_flow_m3s":8*.005}


def build(inv, skin_floor=.001, bag_floor=.00025, fabric_work=80e6, seam=.70):
    geo, s = geometry(inv), gas(inv, 0.)
    cr, pressure, ballast = cradle(), pressure_system(inv, geo), ballast_system(geo)
    r, rn = geo["radius_m"], inv["diameter_m"]/2
    rho_g = (inv["helium_kg"]+inv["impurity_air_kg"])/s["helium_space_m3"]
    head = (s["rho_air"]-rho_g)*G*rn
    drag5 = .8*.5*s["rho_air"]*25*pi*rn**2
    peak = 1000+head+1.5*.5*s["rho_air"]*25
    line = peak*rn/2+(1.5*300000*G+1.5*drag5)/(2*pi*rn)
    thickness = ceil(max(skin_floor, line/(fabric_work*seam))/.0001-1e-12)*.0001
    seam_length = 32*pi*rn+2*pi*rn*(1+2/sqrt(2))
    # Size each main line for a 25 t module, 1.5 limit load, H/W=.06.
    # Two fixed wind azimuths exercise the sector symmetry; no search/optimizer.
    normalized = []
    for angle in (0., pi/8):
        for k in range(8):
            us = [c["unit"] for c in geo["cables"][3*k:3*k+3]]
            normalized += solve3(us, (.06*cos(angle), .06*sin(angle), 1.))
    assert min(normalized) > 0
    max_length = max(c["length_m"] for c in geo["cables"])
    cable_a = max(normalized)*1.5*25000*G/(150e6-1.5*1440*max_length*G)
    cable_t = 150e6*cable_a
    cable_d = sqrt(4*cable_a/pi)
    pin_d = .005*ceil(max(.05, sqrt(2*cable_t/(pi*100e6)))/.005)
    rb = geo["bag_radius_m"]
    bag_area = 16*pi*rb**2
    rho_b = (P0+1250)/(RA*T0)
    # All connected bags share the z=0 datum; their centres are not local datums.
    # Uniform-density hydrostatic approximation: dp(z)=250-gradient*z.
    bag_gradient = (rho_b-rho_g)*G
    bag_z_min = min(c[2]-rb for c in geo["bag_centres"])
    bag_z_max = max(c[2]+rb for c in geo["bag_centres"])
    bag_peak = 250-bag_gradient*bag_z_min
    bag_min = 250-bag_gradient*bag_z_max
    bag_t = ceil(max(bag_floor, bag_peak*rb/(2*30e6*.6))/.00005-1e-12)*.00005
    apparent_capacity = (rho_b-rho_g)*inv["ballonet_usable_m3"]
    # Each of four closed meridian cradle bands per bag has two upper support legs.
    band_length = 4*4*2*pi*rb
    bag_fixed_mass = (bag_area*bag_t*1400+4*32*pi*rb*.10*bag_t*1400+
                      32*(5+.5*bag_t*1400)+64*5)
    # Include the supported fabric/fittings and the bands' own thickness-dependent mass.
    band_den = 32/sqrt(2)*.25*fabric_work*seam-1.5*G*band_length*.25*1400
    band_t = ceil((1.5*G*(apparent_capacity+bag_fixed_mass)/band_den)/.0001)*.0001
    supported_bag_mass = apparent_capacity+bag_fixed_mass+band_length*.25*band_t*1400
    hanger_t = 1.5*supported_bag_mass*G/32
    hanger_a = hanger_t/(150e6-1.5*1440*max(c["length_m"] for c in geo["hangers"])*G)
    hanger_d = sqrt(4*hanger_a/pi)
    sleeve_d = max(.12, cable_d+.06)
    paths = [("main", c["top"], c["low"], None, sleeve_d) for c in geo["cables"]]
    paths += [("hanger", c["top"], c["low"], c["bag"], sleeve_d) for c in geo["hangers"]]
    paths += [("duct",q,p,b,pressure["duct_diameter_m"]+.06)
              for b,c in enumerate(geo["ducts"]) for p,q in zip(c["points"],c["points"][1:])]
    chords = []
    for kind, p, q, own_bag, diameter in paths:
        for b, centre in enumerate(geo["bag_centres"]):
            if b == own_bag:
                continue  # intentional bag attachment has its own cradle fitting
            chord = sphere_chord(p, q, centre, rb+diameter/2)
            if chord > 0:
                chords.append({"kind": kind, "bag": b, "length_m": chord,"diameter_m":diameter})
    chord_length = sum(row["length_m"] for row in chords)
    sleeve_length = chord_length+4*len(chords)
    # Finite centreline clearance; same-module joints capture the final 0.5 m.
    separations, contacts = [], []
    shortened = []
    for c in geo["cables"]:
        low = tuple(c["low"][i]+.5*c["unit"][i] for i in range(3))
        shortened.append((c["top"], low))
    finite_paths = [(p,q,sleeve_d,None) for p,q in shortened]
    finite_paths += [(c["top"],c["low"],sleeve_d,None) for c in geo["hangers"]]
    for b,c in enumerate(geo["ducts"]):
        for j,(p,q) in enumerate(zip(c["points"],c["points"][1:])):
            direction = sub(q,p)
            low = tuple(p[i]+3*direction[i]/norm(direction) for i in range(3)) if j==0 else p
            finite_paths.append((q,low,pressure["duct_diameter_m"]+.06,b))
    for i, (p, q,di,own_i) in enumerate(finite_paths):
        for j, (u, v,dj,own_j) in enumerate(finite_paths[:i]):
            if own_i is not None and own_i == own_j:
                continue  # intentional same-duct elbow
            distance = segment_distance(p, q, u, v)
            # Conservatively apply the sleeve outer radius over every cable segment.
            clearance = distance-(di+dj)/2
            separations.append(clearance)
            if clearance < 0:
                contacts.append({"a": i, "b": j, "surface_gap_m": clearance})
    masses = {
        "envelope_fabric": pi*inv["diameter_m"]**2*thickness*1400,
        "envelope_seam_laps": seam_length*.30*thickness*1400,
        "barrier_weather": pi*inv["diameter_m"]**2*.10,
        "main_anchor_doublers": 24*25*thickness*1400,
        "main_load_curtains": 24*(5*8/2)*max(.002,2*thickness)*1400,
        "main_cables": sum(c["length_m"] for c in geo["cables"])*cable_a*1440,
        "main_pin_fittings": 48*25*(pin_d/.05)**3,
        "lower_envelope_seals_and_chafe": 24*(10+10),
        "bag_membranes": bag_area*bag_t*1400,
        "bag_32_gore_laps": 4*32*pi*rb*.10*bag_t*1400,
        "bag_cradle_bands": band_length*.25*band_t*1400,
        "bag_cradle_fittings_doublers": 32*(5+.5*bag_t*1400),
        "bag_hangers": sum(c["length_m"] for c in geo["hangers"])*hanger_a*1440,
        "bag_hanger_fittings": 64*5,
        "bag_anchor_doublers_curtains": 32*(4*thickness*1400+4*.002*1400),
        "routing_sleeves_liners_boots": sum((c["length_m"]+4)*(pi*c["diameter_m"]*.001*1400+
                                      (4. if c["kind"]=="duct" else 1.))+
                                      (40. if c["kind"]=="duct" else 16.) for c in chords),
        "cradle_construction_over_3t": cr["over_3000kg_allowance_kg"],
        "pressure_hardware_over_2t": pressure["over_2000kg_allowance_kg"],
        "ballast_hardware_over_3t": ballast["over_3000kg_allowance_kg"],
    }
    return {"mass_kg": masses, "construction_kg": sum(masses.values()),
            "geometry": geo, "cradle": cr, "pressure_system": pressure,"ballast_system":ballast,
            "skin_mm": thickness*1000, "head_pa": head, "peak_pressure_pa": peak,
            "pressure_line_kn_m": peak*rn/2/1000, "global_line_kn_m": line/1000,
            "skin_working_line_kn_m": thickness*fabric_work*seam/1000,
            "doubled_patch_demand_kn_m": (line+cable_t/20)/1000,
            "doubled_patch_capacity_kn_m": 2*thickness*fabric_work*seam/1000,
            "main_cable_area_m2": cable_a, "main_cable_diameter_mm": cable_d*1000,
            "main_working_tension_kn": cable_t/1000, "main_pin_mm": pin_d*1000,
            "bag_mm": bag_t*1000, "bag_area_m2": bag_area, "bag_peak_dp_pa": bag_peak,
            "bag_min_dp_pa": bag_min,
            "bag_pressure_reference": {"datum_z_m": 0., "datum_dp_pa": 250.,
                                       "gradient_pa_m": bag_gradient,
                                       "z_min_m": bag_z_min, "z_max_m": bag_z_max,
                                       "everywhere_positive_on_design_envelopes": bag_min > 0},
            "bag_cradle_band_mm": band_t*1000,
            "bag_hanger_diameter_mm": hanger_d*1000,
            "bag_apparent_capacity_kg": apparent_capacity,
            "bag_supported_mass_bound_kg":supported_bag_mass,
            "routing": {"sleeve_diameter_m": sleeve_d, "crossings": chords,
                        "chord_length_m": chord_length, "sleeve_length_m": sleeve_length,
                        "excluded_air_m3": sum(c["length_m"]*pi*c["diameter_m"]**2/4 for c in chords),
                        "minimum_cable_surface_gap_m": min(separations),
                        "cable_contacts": contacts}}


def budget(inv, construction, h, payload, extra_equipment=0., superheat=0.):
    s = gas(inv, h, superheat)
    if not s["capacity_ok"] or s["ballonet_air_m3"] < construction["pressure_system"]["rigid_air_m3_upper_bound"]:
        return {"altitude_m": h, "capacity_ok": False, "margin_kg": None}
    # Air inside the hull is already in Vb. Charge the outside manifold/tails separately;
    # no buoyancy credit is taken for any outside equipment or its displaced volume.
    outside_air = (s["ambient_pa"]+1250)/(RA*s["ambient_k"])*construction["pressure_system"]["external_pressure_air_m3"]
    total = (construction["construction_kg"]+17000+extra_equipment+payload+
             inv["helium_kg"]+inv["impurity_air_kg"]+s["ballonet_air_kg"]+outside_air)
    return {"altitude_m": h, "construction_kg": construction["construction_kg"],
            "equipment_kg": 17000+extra_equipment, "payload_kg": payload,
            "helium_kg": inv["helium_kg"], "impurity_air_kg": inv["impurity_air_kg"],
            "ballonet_air_kg": s["ballonet_air_kg"], "gross_kg": s["gross_kg"],
            "external_pressure_air_kg":outside_air,
            "total_kg": total, "margin_kg": s["gross_kg"]-total, "capacity_ok": True}


def modules(inv, build, payload, fixed_ballast, h, wind, azimuth=0., superheat=0.):
    """Fixed onboard ballast; equal vertical thrust plus mass-proportional horizontal thrust.

    Positive excess requires DOWN thrust; negative excess requires powered UP lift.
    Neither is hidden in the buoyancy margin. Equipment stays equally distributed.
    """
    s, geo = gas(inv, h, superheat), build["geometry"]
    b = budget(inv, build, h, payload, superheat=superheat)
    assert b["capacity_ok"]
    excess = b["margin_kg"]-fixed_ballast
    # 2 t pressure allowance and all its overrun are mounted to the envelope.
    fixed_module = (15000+build["cradle"]["over_3000kg_allowance_kg"]+
                    build["ballast_system"]["over_3000kg_allowance_kg"])
    water = fixed_ballast + (payload if payload == 100000 else 0.)
    fixed_module += 0. if payload == 100000 else payload
    mass = fixed_module+water
    drag = .8*.5*s["rho_air"]*wind**2*pi*(inv["diameter_m"]/2)**2
    # Uniform dry masses and vertical thrust have zero first moment. Redistribute water.
    amplitude = -drag*geo["thrust_depth_m"]/(4*G*geo["module_radius_m"])
    rows, residuals = [], []
    total_shaft, max_shaft, max_sag = 0., 0., 0.
    for k, centre in enumerate(geo["modules"]):
        phi = k*pi/4
        wk = water/8+amplitude*cos(phi-azimuth)
        mk = fixed_module/8+wk
        weight = (mk+excess/8)*G
        hk = drag*weight/((mass+excess)*G)
        ring_reaction = build["ballast_system"]["inward_reaction_per_module_n"]
        target = (hk*cos(azimuth)+ring_reaction*cos(phi),
                  hk*sin(azimuth)+ring_reaction*sin(phi), weight)
        cs = geo["cables"][3*k:3*k+3]
        tensions = solve3([c["unit"] for c in cs], target)
        residual = norm(tuple(sum(t*c["unit"][i] for t,c in zip(tensions,cs))-target[i]
                              for i in range(3)))
        residuals.append(residual)
        resultant = sqrt(hk*hk+(excess*G/8)**2)
        # Ideal actuator disk with 4 m rotor; eta=.70 is an assumed overall loss factor.
        axial_speed = wind*hk/resultant if resultant else 0.
        induced = (sqrt(axial_speed**2+2*resultant/(s["rho_air"]*pi*2**2))-axial_speed)/2
        power = resultant*(axial_speed+induced)/.70
        total_shaft += power
        max_shaft = max(max_shaft, power)
        if min(tensions) > 0:
            for t,c in zip(tensions,cs):
                qperp = build["main_cable_area_m2"]*1440*G*sqrt(1-c["unit"][2]**2)
                max_sag = max(max_sag,qperp*c["length_m"]**2/(8*t))
        rows.append({"module": k, "water_kg": wk, "physical_mass_kg": mk,
                     "horizontal_thrust_kn": hk/1000, "vertical_down_thrust_kn": excess*G/8/1000,
                     "cable_tensions_kn": [t/1000 for t in tensions],
                     "shaft_proxy_kw":power/1000 if wk>=0 and mk>0 and min(tensions)>=0 else None})
    moment = G*sum(row["physical_mass_kg"]*(centre[0]*cos(azimuth)+centre[1]*sin(azimuth))
                   for row,centre in zip(rows,geo["modules"]))+drag*geo["thrust_depth_m"]
    feasible = all(0 <= row["water_kg"] <= build["cradle"]["water_capacity_each_kg"]
                     and 0 < row["physical_mass_kg"] <= 25000 for row in rows)
    positive = all(t >= 0 for row in rows for t in row["cable_tensions_kn"])
    rn = inv["diameter_m"]/2
    peak = 1000+build["head_pa"]+1.5*.5*s["rho_air"]*wind**2
    global_line = peak*rn/2+(1.5*300000*G+1.5*drag)/(2*pi*rn)
    return {"altitude_m": h, "wind_ms": wind, "wind_azimuth_deg": azimuth*180/pi,
            "gas_superheat_k":superheat,
            "fixed_ballast_kg": fixed_ballast, "module_mass_kg": mass, "drag_kn": drag/1000,
            "vertical_downforce_kn": excess*G/1000, "rows": rows,
            "min_tension_kn": min(t for row in rows for t in row["cable_tensions_kn"]),
            "max_tension_kn": max(t for row in rows for t in row["cable_tensions_kn"]),
            "nonnegative_tensions": positive, "water_and_module_capacity_ok": feasible,
            "force_residual_n": max(residuals), "pitch_residual_nm": moment,
            # Do not publish fictitious power for a negative-mass/tension construction.
            "shaft_proxy_total_kw": total_shaft/1000 if feasible and positive else None,
            "shaft_proxy_max_each_kw": max_shaft/1000 if feasible and positive else None,
            "straight_cable_sag_estimate_m": max_sag if feasible and positive else None,
            "global_line_demand_kn_m":global_line/1000,
            "membrane_scalar_ok":global_line/1000 <= build["skin_working_line_kn_m"],
            "positive_pressure_ok": 1000-build["head_pa"]-1.5*.5*s["rho_air"]*wind**2 > 0}


def record(d):
    inv = inventory(d)
    hull = build(inv)
    cases = {}
    for name,payload in (("M20",3000.),("P100",100000.)):
        budgets = [budget(inv,hull,h,payload) for h in (0.,2500.)]
        ballast = max(0.,min(b["margin_kg"] for b in budgets))
        equilibria = [modules(inv,hull,payload,ballast,h,wind,angle)
                      for h in (0.,2500.) for wind in (0.,5.,10.,20.,30.)
                      for angle in ((0.,pi/8) if wind == 5 else (0.,))]
        cases[name] = {"budgets":budgets,"fixed_water_ballast_kg":ballast,
                       "equilibria":equilibria,
                       "same_ballast_hot_10k":modules(inv,hull,payload,ballast,2500.,5.,superheat=10.)}
    hot_limit = atm(2500.)[1]*((inv["free_m3"]-hull["pressure_system"]["rigid_air_m3_upper_bound"])/
                             (.95*inv["free_m3"])-1)
    return {"inventory":inv,"gas_states":[gas(inv,h) for h in (0.,2500.)],
            "construction":hull,"cases":cases,"rigid_duct_hot_limit_k":hot_limit,
            "unballasted_M20_5ms":modules(inv,hull,3000.,0.,0.,5.)}


def main():
    records = {"matched_70p575":record(D0),"candidate_76":record(76.)}
    inv = records["candidate_76"]["inventory"]
    hull = records["candidate_76"]["construction"]
    variants = {}
    for label,kwargs in (("skin_floor_2mm",{"skin_floor":.002}),
                         ("fabric_work_halved",{"fabric_work":40e6}),
                         ("seam_efficiency_0p5",{"seam":.5}),
                         ("bag_floor_0p5mm",{"bag_floor":.0005})):
        changed = build(inv,**kwargs)
        variants[label] = {"skin_mm":changed["skin_mm"],"construction_kg":changed["construction_kg"],
                           "budgets":[budget(inv,changed,2500.,p) for p in (3000.,100000.)]}
    variants["equipment_plus_30t"] = [budget(inv,hull,2500.,p,30000.) for p in (3000.,100000.)]
    pure = inventory(76.,1.)
    variants["pure_helium_recharged"] = [budget(pure,build(pure),2500.,p) for p in (3000.,100000.)]
    variants["same_inventory_hot_10k"] = [budget(inv,hull,2500.,p,superheat=10.) for p in (3000.,100000.)]
    variants["same_inventory_hot_15k"] = gas(inv,2500.,15.)
    for result in records.values():
        inventory_, structure_ = result["inventory"], result["construction"]
        for s in result["gas_states"]:
            assert s["capacity_ok"]
            assert abs(s["helium_space_m3"]+s["ballonet_air_m3"]-inventory_["free_m3"]) < 1e-7
            n = (s["ambient_pa"]+1000)*s["helium_space_m3"]/(RU*s["ambient_k"])
            assert abs(n-inventory_["mol"]) < 1e-7
        for case in result["cases"].values():
            for b in case["budgets"]:
                mass = sum(b[k] for k in ("construction_kg","equipment_kg","payload_kg","helium_kg","impurity_air_kg","ballonet_air_kg","external_pressure_air_kg"))
                assert abs(b["total_kg"]-mass) < 1e-7
                assert abs(b["gross_kg"]-mass-b["margin_kg"]) < 1e-7
            for eq in case["equilibria"]:
                assert eq["force_residual_n"] < 1e-6
                assert abs(eq["pitch_residual_nm"]) < 1e-6
            assert all(eq["nonnegative_tensions"] for eq in case["equilibria"] if eq["wind_ms"] <= 5)
            assert all(not eq["nonnegative_tensions"] for eq in case["equilibria"] if eq["wind_ms"] >= 20)
        assert abs(result["cases"]["M20"]["budgets"][0]["margin_kg"]-
                   result["cases"]["P100"]["budgets"][0]["margin_kg"]-97000) < 1e-7
        assert structure_["cradle"]["scalar_ok"]
        assert structure_["routing"]["excluded_air_m3"] <= 50
        assert structure_["geometry"]["bag_outer_extent_m"] < structure_["geometry"]["radius_m"]
        assert structure_["skin_working_line_kn_m"] >= structure_["global_line_kn_m"]
    assert not variants["same_inventory_hot_15k"]["capacity_ok"]
    print(json.dumps({"records":records,"sensitivities":variants,
                      "checks":"PASS: arithmetic, ideal-node balances and selected scalar bounds only"},indent=2))


if __name__ == "__main__":
    main()
