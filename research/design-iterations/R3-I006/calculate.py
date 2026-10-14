#!/usr/bin/env python3
"""R3-I006 bounded paper budget. No solver, file writes or physical qualification."""
import json
from math import ceil, cos, pi, radians, sin, sqrt

P0, T0, RA, RU, G, LAPSE = 101325.0, 288.15, 287.05, 8.314462618, 9.80665, 0.0065
MHE, MAIR = 0.004002602, RU / RA
D = 70.57485803146756
R, AREA = D / 2, pi * D**2
# Frozen I002 gamma=.20, q=.20 at 2da1ca08; its nominal volume is larger.
V_EXTERNAL = 181394.53949136072
LEGACY_DRY = 80336.60235891192 + 12050.490353836787 + 770.2664400613867 + 782.3838973204092 + 4694.303383922455
SOLID_VOLUME = 100.0  # common conservative gas-volume debit; not extra mass
EQUIPMENT = {"pressure_control": 2000., "propulsion": 3000., "energy": 5000.,
             "avionics": 1000., "local_cargo_cradles": 3000., "ground_ballast_provision": 3000.}


def atmosphere(h):
    temperature = T0 - LAPSE * h
    pressure = P0 * (temperature / T0)**(G / (RA * LAPSE))
    return pressure, temperature, pressure / (RA * temperature)


def mixture_molar_mass(purity):
    return purity * MHE + (1 - purity) * MAIR


def inventory(purity=.96, volume_factor=1., dp=1000.):
    external = V_EXTERNAL * volume_factor
    free = external - SOLID_VOLUME
    p, t, _ = atmosphere(2500.)
    # 5% occupied ballonet air at 2500 m; this fixes ONE lifting-gas inventory.
    mol = (p + dp) * .95 * free / (RU * t)
    return {"external_m3": external, "free_m3": free, "mol": mol,
            "helium_kg": mol * purity * MHE, "impurity_air_kg": mol * (1-purity) * MAIR,
            "installed_ballonet_m3": .30 * free, "purity": purity, "dp_pa": dp}


def gas_state(inv, h, superheat=0.):
    p, ta, rho = atmosphere(h)
    tg = ta + superheat
    pg = p + inv["dp_pa"]  # centre reference; hydrostatic head is screened separately
    vg = inv["mol"] * RU * tg / pg
    vb = inv["free_m3"] - vg
    # Four symmetric lobes: centre-reference first-order hydrostatic contributions cancel.
    ma = (pg + 250.) * vb / (RA * ta) if vb >= 0 else None
    return {"h_m": h, "p_air_pa": p, "t_air_k": ta, "t_gas_k": tg,
            "p_helium_centre_pa": pg, "p_ballonet_reference_pa": pg + 250.,
            "helium_space_m3": vg, "occupied_ballonet_m3": vb,
            "ballonet_fraction": vb / inv["free_m3"],
            "ballonet_air_kg": ma, "rho_air": rho,
            "gross_kg": rho * inv["external_m3"],
            "capacity_ok": 0 <= vb <= inv["installed_ballonet_m3"]}


def cable_lobe_crossings(rb, outer_r):
    """Line/sphere intersections expose the routing debit; they do not model fabric contact."""
    a=rb/sqrt(2)
    centres=((a,a,a),(a,-a,-a),(-a,a,-a),(-a,-a,a))
    chords=[]
    for k in range(16):
        ang=k*pi/8
        group=(k//2+.25)*pi/4
        upper=(outer_r/sqrt(2)*cos(ang), outer_r/sqrt(2)*sin(ang), outer_r/sqrt(2))
        lower=(4*cos(group),4*sin(group),-outer_r-5)
        d=tuple(lower[j]-upper[j] for j in range(3))
        length2=sum(q*q for q in d)
        for centre in centres:
            rel=tuple(upper[j]-centre[j] for j in range(3))
            b=sum(rel[j]*d[j] for j in range(3))
            cc=sum(q*q for q in rel)-rb*rb
            disc=b*b-length2*cc
            if disc>0:
                lo=max(0,(-b-sqrt(disc))/length2)
                hi=min(1,(-b+sqrt(disc))/length2)
                if hi>lo:
                    chords.append((hi-lo)*sqrt(length2))
    return len(chords),sum(chords)


def structure(inv, wind=5., skin_floor=.001, ballonet_floor=.00025,
              working_stress=80e6, seam_efficiency=.70):
    """Sized demands are screening loads; curtain/skin load sharing remains UNKNOWN."""
    sl = gas_state(inv, 0.)
    rho_g = (inv["helium_kg"] + inv["impurity_air_kg"]) / sl["helium_space_m3"]
    qwind = .5 * sl["rho_air"] * wind**2
    drag = .8 * qwind * pi * R**2
    head = (sl["rho_air"] - rho_g) * G * R
    p_peak = inv["dp_pa"] + head + 1.5 * qwind
    p_min = inv["dp_pa"] - head - 1.5 * qwind
    # 1.5 is the selected limit manoeuvre/load multiplier, not a substitute for fabric factor 4.
    w_limit, h_limit = 1.5 * 200000. * G, 1.5 * drag
    n_pressure = p_peak * R / 2.
    n_global = n_pressure + (w_limit + h_limit) / (2 * pi * R)
    effective = working_stress * seam_efficiency
    thickness = ceil(max(skin_floor, n_global / effective) / .0001 - 1e-12) * .0001
    # Anchors lie on the common LOADED sphere; unloaded R still bounds pressure demand and area.
    loaded_r=(3*inv["external_m3"]/(4*pi))**(1/3)
    ra, za = loaded_r / sqrt(2), loaded_r / sqrt(2)
    horizontal = sqrt(ra**2 + 4**2 - 2 * ra * 4 * cos(radians(11.25)))
    vertical = za + loaded_r + 5.
    cable_length = sqrt(horizontal**2 + vertical**2)
    cosine = vertical / cable_length
    # Four windward cables have >=.20 horizontal projection. Adding this demand to
    # gravity is a conservative individual strength screen, not a positive-tension solution.
    cable_tension = w_limit / (16 * cosine) + h_limit / (4 * .20)
    cable_area = cable_tension / 150e6  # assumed effective working stress, including terminations
    pin_d = ceil(max(.05, sqrt(2 * cable_tension / (pi * 100e6))) / .005) * .005
    seam_length = 32 * pi * R + 2 * pi * R * (1 + 2 / sqrt(2))
    # Add 20 m3 geometrical lobe volume to cover air volume excluded by cable sleeves.
    # This space holds helium; it is distinct from the common 100 m3 non-gas debit.
    rb = (3 * (inv["installed_ballonet_m3"]+20.) / (4 * 4 * pi))**(1/3)
    ab = 4 * 4 * pi * rb**2
    rho_b = (sl["p_helium_centre_pa"] + 250) / (RA * T0)
    pb = 250 + (rho_b - rho_g) * G * rb
    tb = max(ballonet_floor, pb * rb / (2 * 30e6 * .60))
    # 80 t apparent internal load bound, 32 hangers, <=60 m each, vertical cosine >=.70.
    hanger_tension = 1.5 * 80000 * G / (32 * .70)
    crosses,chord_length=cable_lobe_crossings(rb,loaded_r)
    sleeve_length=chord_length+4*crosses
    sleeve_d=max(.12,sqrt(4*cable_area/pi)+.06)
    masses = {
        "envelope_load_fabric": AREA * thickness * 1400,
        "envelope_seam_overlaps": seam_length * .30 * thickness * 1400,
        "barrier_weather_layer": AREA * .10,
        "anchor_doublers": 16 * 25 * thickness * 1400,
        "load_curtains": 16 * (5 * 8 / 2) * max(.002, 2*thickness) * 1400,
        "main_suspension_cables": 16 * cable_length * cable_area * 1440,
        "pins_fittings_seals_chafe": 32 * 25 * (pin_d / .05)**3 + 16 * 10 + 200,
        "ballonet_membranes": ab * tb * 1400,
        "ballonet_seams_cradle_doublers": .25 * ab * tb * 1400,
        "ballonet_hangers": 32 * 60 * hanger_tension / 150e6 * 1440,
        # Flexible pressure barriers contact sacrificial cable liners; NO compression-tube credit.
        "cable_sleeves_liners_boots": sleeve_length*(pi*sleeve_d*.001*1400+1.)+2*crosses*8.,
    }
    return {"mass_kg": masses, "dry_kg": sum(masses.values()), "wind_ms": wind,
            "drag_sl_kn": drag/1000, "shaft_power_sl_mw": drag*wind/.7/1e6,
            "head_pa": head, "p_peak_pa": p_peak, "p_min_pa": p_min,
            "pressure_line_kn_m": n_pressure/1000, "global_line_kn_m": n_global/1000,
            "skin_mm": thickness*1000, "working_line_kn_m": effective*thickness/1000,
            "patch_line_kn_m": (n_global+cable_tension/20)/1000,
            "doubled_patch_capacity_kn_m": 2*effective*thickness/1000,
            "loaded_radius_m": loaded_r, "cable_length_m": cable_length, "cable_cosine": cosine,
            "cable_horizontal_tangent": horizontal/vertical,
            "cable_kn": cable_tension/1000, "cable_equiv_diameter_mm": sqrt(4*cable_area/pi)*1000,
            "pin_diameter_mm": pin_d*1000,
            "ballonet_radius_m": rb, "ballonet_area_m2": ab, "ballonet_peak_dp_pa": pb,
            "ballonet_min_dp_pa": 500-pb, "ballonet_mm": tb*1000,
            "ballonet_tetra_extent_m": rb*(1+sqrt(1.5)),
            "cable_lobe_crossings":crosses, "cable_lobe_chord_m":chord_length,
            "sleeve_length_m":sleeve_length, "sleeve_diameter_m":sleeve_d,
            "sleeve_air_volume_debit_m3":chord_length*pi*sleeve_d**2/4,
            "ballonet_working_line_kn_m": tb*30e6*.6/1000,
            "ballonet_demand_kn_m": pb*rb/2/1000,
            "membrane_screen_ok": effective*thickness >= n_global,
            "positive_pressure_screen_ok": p_min > 0}


def budget(inv, hull, h, payload=3000., equipment_extra=0.):
    gas = gas_state(inv, h)
    assert gas["capacity_ok"], "No physical budget outside the installed gas capacity"
    equipment = sum(EQUIPMENT.values()) + equipment_extra
    gases = inv["helium_kg"] + inv["impurity_air_kg"] + gas["ballonet_air_kg"]
    total = hull["dry_kg"] + equipment + payload + gases
    # Necessary whole-system screen: all horizontal force is assumed to reach the
    # underhung modules. This is not sufficient to prove individual cable tensions.
    dry_suspended = sum(hull["mass_kg"][k] for k in (
        "main_suspension_cables", "pins_fittings_seals_chafe", "ballonet_hangers",
        "ballonet_membranes", "ballonet_seams_cradle_doublers", "load_curtains",
        "cable_sleeves_liners_boots"))
    apparent_ballonet = max(0., gas["ballonet_air_kg"] -
                           (inv["helium_kg"]+inv["impurity_air_kg"])/gas["helium_space_m3"]*gas["occupied_ballonet_m3"])
    suspended = equipment + payload + dry_suspended + apparent_ballonet
    drag = hull["drag_sl_kn"] * 1000 * gas["rho_air"] / atmosphere(0.)[2]
    return {"h_m": h, "dry_t": hull["dry_kg"]/1000, "equipment_t": equipment/1000,
            "payload_t": payload/1000, "helium_t": inv["helium_kg"]/1000,
            "impurity_air_t": inv["impurity_air_kg"]/1000,
            "ballonet_air_t": gas["ballonet_air_kg"]/1000,
            "total_t": total/1000, "gross_t": gas["gross_kg"]/1000,
            "margin_t": (gas["gross_kg"]-total)/1000,
            "suspended_screen_t": suspended/1000,
            "suspension_capacity_screen_ok": suspended <= 200000.,
            "horizontal_equilibrium_necessary_ok": drag <= suspended*G*hull["cable_horizontal_tangent"],
            "gas_capacity_ok": gas["capacity_ok"]}


def pressure_control(inv):
    rows=[]
    for h in (0., 2500.):
        s=gas_state(inv,h)
        beta_g=-LAPSE/s["t_air_k"]+G/(RA*s["t_air_k"])*s["p_air_pa"]/s["p_helium_centre_pa"]
        beta_b=-LAPSE/s["t_air_k"]+G/(RA*s["t_air_k"])*s["p_air_pa"]/s["p_ballonet_reference_pa"]
        # Include compression of air already inside, and rate the blower at ambient inlet density.
        internal_flow=(s["helium_space_m3"]*beta_g+s["occupied_ballonet_m3"]*beta_b)*1.0
        internal_flow+=s["helium_space_m3"]*10/(3600*s["t_air_k"])
        inlet_flow=internal_flow*s["p_ballonet_reference_pa"]/s["p_air_pa"]
        rows.append({"h_m":h,"air_flow_m3s":inlet_flow,"ballonet_exit_volume_flow_m3s":internal_flow})
    return {"schedule":rows,"one_blower_out_flow_m3s":24.,
            "three_blower_power_kw":3*8*2000/.65/1000,
            "altitude_superheat_before_zero_ballonet_k":atmosphere(2500.)[1]*(1/.95-1)}


def main():
    inv=inventory(); hull=structure(inv)
    budgets=[budget(inv,hull,h,payload) for payload in (3000.,100000.) for h in (0.,2500.)]
    legacy_gas=81060*(V_EXTERNAL-SOLID_VOLUME)*mixture_molar_mass(.96)/(RU*T0)
    legacy={"dry_t":LEGACY_DRY/1000,"gas_t":legacy_gas/1000,"equipment_t":17.,"payload_t":3.,
            "gross_t":atmosphere(0.)[2]*V_EXTERNAL/1000,
            "margin_t":(atmosphere(0.)[2]*V_EXTERNAL-LEGACY_DRY-20000-legacy_gas)/1000}
    variations={}
    for name, kwargs in (("skin_floor_0p5mm",{"skin_floor":.0005}),
                         ("skin_floor_2mm",{"skin_floor":.002}),
                         ("working_stress_halved",{"working_stress":40e6}),
                         ("seam_efficiency_0p5",{"seam_efficiency":.5}),
                         ("ballonet_floor_0p5mm",{"ballonet_floor":.0005}),
                         ("wind_10ms_resized",{"wind":10.}),
                         ("wind_20ms_resized",{"wind":20.}),
                         ("wind_30ms_resized",{"wind":30.})):
        sh=structure(inv,**kwargs)
        variations[name]={"structure":sh,"budgets":[budget(inv,sh,2500.,p) for p in (3000.,100000.)]}
    pure=inventory(purity=1.)
    smaller=inventory(volume_factor=.99)  # RECHARGED case; separate conserved inventory
    variations["pure_helium_recharged"]={"budgets":[budget(pure,structure(pure),2500.,p) for p in (3000.,100000.)]}
    variations["one_pct_volume_loss_recharged"]={"budgets":[budget(smaller,structure(smaller),2500.,p) for p in (3000.,100000.)]}
    deformed=dict(inv, external_m3=.99*inv["external_m3"], free_m3=.99*inv["external_m3"]-SOLID_VOLUME)
    variations["one_pct_volume_loss_same_inventory"]={"budgets":[budget(deformed,hull,2500.,p) for p in (3000.,100000.)]}
    variations["extra_equipment_30t"]={"budgets":[budget(inv,hull,2500.,p,30000.) for p in (3000.,100000.)]}
    # Conservation, capacity and counterfactual accounting checks, not structural tests.
    s0,s1=gas_state(inv,0.),gas_state(inv,2500.)
    for s in (s0,s1):
        assert s["capacity_ok"]
        assert abs(s["helium_space_m3"]+s["occupied_ballonet_m3"]-inv["free_m3"])<1e-8
        assert abs(s["p_helium_centre_pa"]*s["helium_space_m3"]/(RU*s["t_gas_k"])-inv["mol"])<1e-8
    assert s0["ballonet_air_kg"] > s1["ballonet_air_kg"]
    for b in budgets:
        mass=sum(b[k] for k in ("dry_t","equipment_t","payload_t","helium_t","impurity_air_t","ballonet_air_t"))
        assert abs(b["total_t"]-mass)<1e-10
        assert abs(b["gross_t"]-mass-b["margin_t"])<1e-10
    assert abs((budgets[0]["margin_t"]-budgets[2]["margin_t"])-97)<1e-10
    assert budgets[1]["margin_t"]>0>budgets[3]["margin_t"]
    assert hull["ballonet_tetra_extent_m"] < (3*V_EXTERNAL/(4*pi))**(1/3)
    assert hull["sleeve_air_volume_debit_m3"] <= 20.
    assert hull["cable_lobe_crossings"] == 20
    assert hull["ballonet_working_line_kn_m"] >= hull["ballonet_demand_kn_m"]
    assert hull["doubled_patch_capacity_kn_m"] >= hull["patch_line_kn_m"]
    assert max(x["air_flow_m3s"] for x in pressure_control(inv)["schedule"])<24
    assert not gas_state(inv,2500.,15.)["capacity_ok"]
    assert not variations["wind_30ms_resized"]["structure"]["positive_pressure_screen_ok"]
    print(json.dumps({"inventory":inv,"states":[s0,s1],"structure":hull,"budgets":budgets,
                      "legacy_matched":legacy,"pressure_control":pressure_control(inv),
                      "sensitivities":variations,"checks":"PASS: bookkeeping and stated scalar screens only"},indent=2))


if __name__ == "__main__":
    main()
