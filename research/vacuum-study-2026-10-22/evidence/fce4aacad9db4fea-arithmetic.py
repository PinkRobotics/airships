#!/usr/bin/python3
"""Owner arithmetic for vacuum-mainline-estimates-owner3000-1019.

Ordinary closed forms only. Every numeric input is QUESTIONABLE.
The sandwich collapse expression is an owner extrapolation of the
monocoque identity, not a published sandwich theorem.
"""
from __future__ import annotations

import json
import math
import os
import time
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
ORIGIN_MONO = 2077365.589951272
PHASE1_EARLY_ELAPSED = 430.5604903032072


def now():
    return (
        datetime.now(ZoneInfo("America/Los_Angeles")).isoformat(timespec="microseconds"),
        time.monotonic(),
    )


def q(value, units, source, why, nfi, point="common"):
    return {
        "point_id_or_common": point,
        "value": value,
        "units": units,
        "QUESTIONABLE_tag": "QUESTIONABLE",
        "source_reference_or_explicit_assumption_basis": source,
        "why_optimistic_or_uncertain": why,
        "NFI_id": nfi,
    }


def main():
    utc0, mono0 = now()
    # Atmosphere constants. Primary pressure and density are recomputed here.
    h = 500.0
    T0 = 288.15
    p0 = 101325.0
    lapse = 0.0065
    g0 = 9.80665
    Rspec = 287.053
    T = T0 - lapse * h
    exponent = g0 / (lapse * Rspec)
    p_ext = p0 * (T / T0) ** exponent
    rho = p_ext / (Rspec * T)
    rho_charter = 1.167
    p_sealevel = 101325.0

    E = 68.9e9
    rho_al = 2700.0
    nu = 0.33
    kd = 0.2
    p_int = 0.0
    R = 10.0
    V = (4.0 / 3.0) * math.pi * R**3
    area = 4.0 * math.pi * R**2
    lift = rho * V
    lift_charter = rho_charter * V

    # Monocoque identity: Zoelly must match 4/R^2*sqrt(D*S) for a solid wall.
    def zoelly(Emod, thickness, radius, poisson):
        return (
            2.0
            * Emod
            * (thickness / radius) ** 2
            / math.sqrt(3.0 * (1.0 - poisson**2))
        )

    def shell_from_DS(Emod, thickness, radius, poisson):
        D = Emod * thickness**3 / (12.0 * (1.0 - poisson**2))
        S = Emod * thickness
        return 4.0 / radius**2 * math.sqrt(D * S)

    ident_a = zoelly(E, 0.001, R, nu)
    ident_b = shell_from_DS(E, 0.001, R, nu)
    if abs(ident_a - ident_b) / ident_a > 1e-12:
        raise SystemExit("monocoque identity failed")

    # P1 simple isotropic shell.
    t1 = 0.0007
    m1_shell = rho_al * area * t1
    j1 = 0.10
    m1_joint = j1 * m1_shell
    m1_sys = 200.0
    m1_gas = 0.0
    m1 = m1_shell + m1_joint + m1_sys + m1_gas
    p1_cl = zoelly(E, t1, R, nu)
    p1 = kd * p1_cl
    sf1 = p1 / p_ext
    mar1 = (lift - m1) / lift

    # P2 sandwich sphere. d is face-center distance.
    tf = 0.0002
    core_t = 0.10
    rho_core = 16.0
    d = core_t + tf
    D2 = E * tf * d**2 / (2.0 * (1.0 - nu**2))
    S2 = E * 2.0 * tf
    p2_cl = 4.0 / R**2 * math.sqrt(D2 * S2)
    p2_closed = 4.0 * E * tf * d / (R**2 * math.sqrt(1.0 - nu**2))
    if abs(p2_cl - p2_closed) / p2_cl > 1e-12:
        raise SystemExit("sandwich closed form mismatch")
    p2 = kd * p2_cl
    m2_face = rho_al * area * 2.0 * tf
    m2_core = rho_core * area * core_t
    m2_sand = m2_face + m2_core
    j2 = 0.05
    m2_joint = j2 * m2_sand
    m2_sys = 100.0
    m2_gas = 0.0
    m2 = m2_sand + m2_joint + m2_sys + m2_gas
    sf2 = p2 / p_ext
    mar2 = (lift - m2) / lift

    # P3 frame plus membrane. Equal-triangle continuum, not an integer mesh.
    s = 1.0
    ro = 0.020
    tw = 0.001
    ri = ro - tw
    A = math.pi * (ro**2 - ri**2)
    I = math.pi / 4.0 * (ro**4 - ri**4)
    p_euler = 2.0 * math.pi**2 * E * I / (R * s**3)
    sigma_allow = 1.5e9
    t_film = 80e-6
    rho_film = 970.0
    p_film = 2.0 * sigma_allow * t_film / s
    if p_euler <= p_film:
        govern = "pinned_euler_member"
        p3 = p_euler
        prop3 = "Young_modulus_of_6061-T6_frame"
        holds3 = "R, s, tube radii, film, knockdown not applied, nu unused"
        scaling3 = "p_euler = (2*pi^2*I/(R*s^3))*E, linear in E"
    else:
        govern = "local_film_membrane"
        p3 = p_film
        prop3 = "film_tensile_allowable"
        holds3 = "t_film, s, R, frame section"
        scaling3 = "p_film = (2*t_film/s)*sigma_allow, linear in sigma_allow"
    sf3 = p3 / p_ext
    tri = math.sqrt(3.0) / 4.0 * s**2
    n_tri = area / tri
    n_edge = 1.5 * n_tri
    n_node = n_edge - n_tri + 2.0
    if abs((n_node - n_edge + n_tri) - 2.0) > 1e-9:
        raise SystemExit("euler characteristic failed")
    node_mass = 0.02
    m3_frame = n_edge * rho_al * A * s
    m3_film = rho_film * area * t_film
    m3_nodes = n_node * node_mass
    m3_sys = 50.0
    m3_gas = 0.0
    m3 = m3_frame + m3_film + m3_nodes + m3_sys + m3_gas
    mar3 = (lift - m3) / lift

    def factor_block(sf, prop, holds, scaling, collapse, baseline_name, baseline):
        if sf >= 1.0:
            return {
                "required": False,
                "property": "NOT_APPLICABLE_SF_AT_LEAST_ONE",
                "improvement_factor": None,
                "scaling": "not required",
                "held_fixed": holds,
            }
        factor = p_ext / collapse
        # Linear models: factor equals 1/SF because collapse was defined as the pressure used in SF.
        if abs(factor - (1.0 / sf)) > 1e-9:
            raise SystemExit("factor scaling mismatch")
        return {
            "required": True,
            "property": prop,
            "improvement_factor": factor,
            "equals_one_over_SF_because_linear": True,
            "scaling": scaling,
            "held_fixed": holds,
            "baseline_name": baseline_name,
            "baseline_value": baseline,
            "target_value": baseline * factor,
        }

    f1 = factor_block(
        sf1,
        "Young_modulus_of_6061-T6",
        "R, t, nu, knockdown, all masses, p_ext",
        "p_collapse = kd*2*(t/R)^2/sqrt(3*(1-nu^2))*E, linear in E",
        p1,
        "E",
        E,
    )
    f2 = factor_block(
        sf2,
        "Young_modulus_of_6061-T6_faces",
        "R, tf, d, nu, knockdown, core, all masses, p_ext; shear omitted",
        "p_collapse = kd*4*tf*d/(R^2*sqrt(1-nu^2))*E, linear in E",
        p2,
        "E",
        E,
    )
    f3 = factor_block(
        sf3,
        prop3,
        holds3,
        scaling3,
        p3,
        "E" if govern.startswith("pinned") else "sigma_allow",
        E if govern.startswith("pinned") else sigma_allow,
    )

    # Sensitivities. Same stated geometry except the named change.
    sens = []
    for pid, mass in (("P1", m1), ("P2", m2), ("P3", m3)):
        mar_c = (lift_charter - mass) / lift_charter
        sens.append({
            "id": f"S-RHO-{pid}",
            "change": "replace computed ISA density with charter 1.167 kg/m3",
            "primary": False,
            "float_margin": mar_c,
            "crush_SF_unchanged": True,
            "label": "QUESTIONABLE historical charter density; pressure case unchanged",
        })
    for pid, pcol in (("P1", p1), ("P2", p2), ("P3", p3)):
        sens.append({
            "id": f"S-SL-{pid}",
            "change": "replace p_ext with 101325 Pa",
            "primary": False,
            "label": "NON_PRIMARY sea-level comparison. Not the ordered 500 m case.",
            "crush_SF": pcol / p_sealevel,
        })
    # Alternate sandwich core thickness, still an explicit single point, not a search.
    core_alt = 0.16
    d_alt = core_alt + tf
    p2_alt_cl = 4.0 * E * tf * d_alt / (R**2 * math.sqrt(1.0 - nu**2))
    p2_alt = kd * p2_alt_cl
    m2_alt = (
        rho_al * area * 2.0 * tf
        + rho_core * area * core_alt
    )
    m2_alt = m2_alt + j2 * m2_alt + m2_sys + m2_gas
    sens.append({
        "id": "S-P2-CORE-0.16m",
        "change": "P2 core thickness 0.10 m to 0.16 m; other P2 inputs fixed",
        "primary": False,
        "collapse_pressure_Pa": p2_alt,
        "crush_SF": p2_alt / p_ext,
        "all_mass_kg": m2_alt,
        "float_margin": (lift - m2_alt) / lift,
        "label": "QUESTIONABLE single alternate. Shear still omitted.",
    })

    inputs = []
    def add(iid, point, quantity, spec):
        row = {"input_id": iid, "quantity": quantity}
        row.update(spec)
        row["point_id_or_common"] = point
        inputs.append(row)

    src_isa = (
        "Recomputed from ISO 2533 troposphere model. Constants g0=9.80665 m/s^2, "
        "R=287.053 J/(kg K), lapse=0.0065 K/m, T0=288.15 K, p0=101325 Pa as listed "
        "on https://www.foehnwall.at/meteo/isa.html . Wikipedia ISA names ISO 2533:1975. "
        "Not copied from that page's 500 m table."
    )
    src_al = (
        "ASM matweb 6061-T6, https://asm.matweb.com/search/specificmaterial.asp?bassnum=ma6061t6 : "
        "density 2.7 g/cc AA typical; modulus 68.9 GPa AA typical average of tension and compression; "
        "Poisson 0.33 estimated on that page from similar alloys."
    )
    src_kd = (
        "Owner choice of 0.2 from the published statement that a knockdown for spherical shells "
        "under equi-biaxial compression is typically as small as 0.2: "
        "https://www.researchgate.net/publication/44276253_Knockdown_Factors_for_Buckling_of_Cylindrical_and_Spherical_Shells_Subject_to_Reduced_Biaxial_Membrane_Stress . "
        "Not an evaluation of the NASA SP-8032 curve."
    )
    add("I-H", "common", "altitude", q(h, "m", src_isa, "Geometric height used as geopotential.", "NFI-ISA"))
    add("I-T0", "common", "ISA sea-level temperature", q(T0, "K", src_isa, "Dry standard; no humidity.", "NFI-ISA"))
    add("I-P0", "common", "ISA sea-level pressure", q(p0, "Pa", src_isa, "Standard constant, not the crush case.", "NFI-ISA"))
    add("I-LAPSE", "common", "tropospheric lapse", q(lapse, "K/m", src_isa, "Constant lapse assumed through 500 m.", "NFI-ISA"))
    add("I-G", "common", "standard gravity", q(g0, "m/s^2", src_isa, "Constant g, no height correction.", "NFI-ISA"))
    add("I-RSPEC", "common", "specific gas constant", q(Rspec, "J/(kg K)", src_isa, "Dry air.", "NFI-ISA"))
    add("I-PINT", "common", "residual internal pressure", q(p_int, "Pa", "Owner assumption: perfect vacuum, the evacuated-hull case.", "Optimistic for gas mass and pessimistic for pressure difference. A real hull holds some gas.", "NFI-GAS"))
    add("I-E", "common", "6061-T6 Young modulus", q(E, "Pa", src_al, "Typical value, not a design allowable, not corrected to 284.9 K.", "NFI-AL"))
    add("I-RHO-AL", "common", "6061-T6 density", q(rho_al, "kg/m^3", src_al, "Typical 2.7 g/cc converted as 2700 kg/m^3.", "NFI-AL"))
    add("I-NU", "common", "6061-T6 Poisson ratio", q(nu, "1", src_al, "Page marks this estimated, not measured for this sheet.", "NFI-AL"))
    add("I-KD", "P1", "spherical knockdown", q(kd, "1", src_kd, "Severe typical value, not an optimistic upper knockdown, and not fitted at this R/t.", "NFI-KD"))
    add("I-KD", "P2", "spherical knockdown", q(kd, "1", src_kd + " Applied to the sandwich extrapolation by owner assumption.", "Sandwich imperfection factor is not established by that citation.", "NFI-SAND"))
    add("I-R", "common", "external radius", q(R, "m", "Owner choice of a common demonstrator scale.", "Walls are assumed inside this radius, so displaced volume is not reduced.", "NFI-GEOM"))
    add("I-T1", "P1", "shell thickness", q(t1, "m", "Owner choice of a thin machined/spun wall.", "R/t is far above ordinary fabrication. Optimistic mass.", "NFI-GEOM"))
    add("I-J1", "P1", "joint mass fraction of shell", q(j1, "1", "Owner allowance.", "Optimistic small joint mass. Not a joint design.", "NFI-MASS"))
    add("I-SYS1", "P1", "systems and payload", q(m1_sys, "kg", "Owner allowance for a small package.", "May be low for a real vehicle.", "NFI-MASS"))
    add("I-GAS1", "P1", "residual gas mass", q(m1_gas, "kg", "Follows p_int=0.", "Zero only if the vacuum is perfect.", "NFI-GAS"))
    add("I-TF", "P2", "one face thickness", q(tf, "m", "Owner choice.", "Two faces. Thin sheet, optimistic.", "NFI-SAND"))
    add("I-CORE-T", "P2", "core thickness", q(core_t, "m", "Owner choice.", "Thick light core. No shear check.", "NFI-SAND"))
    add("I-RHO-CORE", "P2", "core density", q(rho_core, "kg/m^3", "Owner assumption for a very light honeycomb or foam class. No datasheet pinned.", "Optimistic mass. Real core at this density may lack shear stiffness.", "NFI-CORE"))
    add("I-J2", "P2", "joint mass fraction of sandwich", q(j2, "1", "Owner allowance.", "Optimistic.", "NFI-MASS"))
    add("I-SYS2", "P2", "systems and payload", q(m2_sys, "kg", "Owner allowance.", "May be low.", "NFI-MASS"))
    add("I-GAS2", "P2", "residual gas mass", q(m2_gas, "kg", "Follows p_int=0.", "Zero only if the vacuum is perfect.", "NFI-GAS"))
    add("I-S", "P3", "member spacing", q(s, "m", "Owner choice.", "Continuum of equal triangles, not a built geodesic.", "NFI-FRAME"))
    add("I-RO", "P3", "tube outer radius", q(ro, "m", "Owner choice.", "Section is assumed constant on every member.", "NFI-FRAME"))
    add("I-TW", "P3", "tube wall thickness", q(tw, "m", "Owner choice.", "Local tube crippling is not checked.", "NFI-FRAME"))
    add("I-SIG", "P3", "film tensile allowable", q(sigma_allow, "Pa", "Owner assumption in the range of a strong polymer film. No datasheet pinned.", "Optimistic allowable.", "NFI-FILM"))
    add("I-TFILM", "P3", "film thickness", q(t_film, "m", "Owner choice.", "Sagged area not added.", "NFI-FILM"))
    add("I-RHO-FILM", "P3", "film density", q(rho_film, "kg/m^3", "Owner assumption near polyethylene density.", "Not tied to the allowable. Inconsistent material pairing is possible.", "NFI-FILM"))
    add("I-NODE", "P3", "mass per node", q(node_mass, "kg", "Owner allowance.", "Optimistic hardware.", "NFI-MASS"))
    add("I-SYS3", "P3", "systems and payload", q(m3_sys, "kg", "Owner allowance.", "May be low.", "NFI-MASS"))
    add("I-GAS3", "P3", "residual gas mass", q(m3_gas, "kg", "Follows p_int=0.", "Zero only if the vacuum is perfect.", "NFI-GAS"))
    add("I-RHO-CHARTER", "common", "charter air density", q(rho_charter, "kg/m^3", "CHARTER.md historical ordered density 1.167. Sensitivity only.", "Superseded as the primary density by the recomputed ISA value. Sea-level survival in that charter is not applied.", "NFI-CHARTER"))
    add("I-P-SL", "common", "sea-level pressure comparison", q(p_sealevel, "Pa", "Same 101325 Pa constant, used only in a labelled ref-3bd6c432813f5781289e sensitivity.", "Must not replace p_ext at 500 m.", "NFI-CHARTER"))
    add("I-CORE-ALT", "P2", "alternate core thickness", q(core_alt, "m", "Single stated sensitivity, not a searched optimum.", "Still omits shear.", "NFI-SAND"))

    def point(pid, family, geom, equations, mats, masses, margin, pcol, pcl, sf, factor, extra):
        return {
            "point_id": pid,
            "construction_family": family,
            "geometry_scale_and_residual_pressure": geom,
            "model_equations_and_source_ids": equations,
            "material_and_other_input_ids": mats,
            "displaced_volume_m3": V,
            "lift_basis": "supported mass rho_air*V_external at computed ISA density; p_int=0",
            "lift_equivalent_mass_kg": lift,
            "all_mass_breakdown_kg": masses,
            "all_mass_kg": sum(masses.values()),
            "float_margin": margin,
            "collapse_pressure_estimate_Pa": pcol,
            "classical_or_mode_pressure_Pa": pcl,
            "external_pressure_at_500m_Pa": p_ext,
            "crush_safety_factor": sf,
            "pressure_convention": "p_int=0 so differential equals external. SF = p_collapse/p_ext(500 m ISA). p_collapse already includes the knockdown where one is applied.",
            "if_SF_below1_property_to_improve": factor["property"],
            "improvement_factor_relative_to_stated_baseline": factor["improvement_factor"],
            "scaling_or_calculation_for_factor": factor,
            "float_note": (
                "margin=(lift-all_mass)/lift. "
                + (
                    "Negative margin: structural density and the stated allowances set the mass. Reducing the dominating material density raises margin at fixed geometry."
                    if margin < 0
                    else "Margin is positive at the stated allowances. It falls if those allowances or densities rise."
                )
            ),
            "NFI_ids": extra["nfi"],
            "extra": extra,
        }

    points = [
        point(
            "P1",
            "simple_shell",
            "Complete sphere, external radius 10 m, thickness 0.0007 m, p_int=0.",
            "Zoelly p_cl=2*E*(t/R)^2/sqrt(3*(1-nu^2)); p_collapse=kd*p_cl. Identity 4/R^2*sqrt(D*S) checked.",
            ["I-E", "I-RHO-AL", "I-NU", "I-KD", "I-R", "I-T1", "I-J1", "I-SYS1", "I-GAS1", "I-PINT"],
            {"shell": m1_shell, "joints": m1_joint, "systems_payload": m1_sys, "residual_gas": m1_gas},
            mar1,
            p1,
            p1_cl,
            sf1,
            f1,
            {"nfi": ["NFI-ISA", "NFI-AL", "NFI-KD", "NFI-GEOM", "NFI-MASS", "NFI-GAS"], "mode": "knocked_down_zoelly"},
        ),
        point(
            "P2",
            "sandwich",
            "Complete sphere, external radius 10 m, two faces 0.0002 m, core 0.10 m, p_int=0.",
            "Owner extrapolation: D=E*tf*d^2/(2*(1-nu^2)), S=E*2*tf, p_cl=4/R^2*sqrt(D*S), p_collapse=kd*p_cl. d=core+tf. Core shear, wrinkling and core crush omitted.",
            ["I-E", "I-RHO-AL", "I-NU", "I-KD", "I-R", "I-TF", "I-CORE-T", "I-RHO-CORE", "I-J2", "I-SYS2", "I-GAS2", "I-PINT"],
            {"faces": m2_face, "core": m2_core, "joints": m2_joint, "systems_payload": m2_sys, "residual_gas": m2_gas},
            mar2,
            p2,
            p2_cl,
            sf2,
            f2,
            {"nfi": ["NFI-ISA", "NFI-AL", "NFI-SAND", "NFI-CORE", "NFI-GEOM", "NFI-MASS", "NFI-GAS"], "mode": "knocked_down_owner_sandwich"},
        ),
        point(
            "P3",
            "frame_membrane",
            "Complete sphere, external radius 10 m, spacing 1 m, tube 0.020 m outer by 0.001 m wall, film 80e-6 m, p_int=0.",
            "Equilibrium N=p*R/2. Owner tributary: F=N*s. Pinned Euler p_euler=2*pi^2*E*I/(R*s^3). Film p_film=2*sigma*t_film/s. Collapse is the lesser. No extra knockdown.",
            ["I-E", "I-RHO-AL", "I-R", "I-S", "I-RO", "I-TW", "I-SIG", "I-TFILM", "I-RHO-FILM", "I-NODE", "I-SYS3", "I-GAS3", "I-PINT"],
            {"frame": m3_frame, "film": m3_film, "nodes": m3_nodes, "systems_payload": m3_sys, "residual_gas": m3_gas},
            mar3,
            p3,
            {"p_euler": p_euler, "p_film": p_film},
            sf3,
            f3,
            {
                "nfi": ["NFI-ISA", "NFI-AL", "NFI-FRAME", "NFI-FILM", "NFI-GEOM", "NFI-MASS", "NFI-GAS"],
                "mode": govern,
                "n_triangles": n_tri,
                "n_edges": n_edge,
                "n_nodes": n_node,
                "tube_area_m2": A,
                "tube_I_m4": I,
            },
        ),
    ]

    nfis = [
        {"NFI_id": "NFI-ISA", "linked_inputs_or_points": "common atmosphere", "questionable_assumption_or_gap": "Dry constant-g geopotential formula; geometric height substituted.", "direction_of_further_investigation": "Pin ISO 2533 or ICAO Doc 7488 table at 500 m and a humidity case.", "how_it_affects_margin_or_SF": "Density moves float margin. Pressure moves every SF inversely."},
        {"NFI_id": "NFI-AL", "linked_inputs_or_points": "I-E I-RHO-AL I-NU", "questionable_assumption_or_gap": "Room-temperature typical properties, Poisson estimated.", "direction_of_further_investigation": "MMPDS allowables at about 285 K.", "how_it_affects_margin_or_SF": "E scales collapse linearly in all three models. Density scales metallic mass."},
        {"NFI_id": "NFI-KD", "linked_inputs_or_points": "P1 I-KD", "questionable_assumption_or_gap": "0.2 is a cited severe typical knockdown, not a curve at R/t.", "direction_of_further_investigation": "Evaluate NASA SP-8032 at this complete-sphere geometry.", "how_it_affects_margin_or_SF": "SF scales directly with the knockdown. It does not change mass."},
        {"NFI_id": "NFI-SAND", "linked_inputs_or_points": "P2", "questionable_assumption_or_gap": "Collapse formula extrapolates the monocoque D-S identity. Shear, wrinkling and core crush are omitted.", "direction_of_further_investigation": "Replace with a published sandwich-sphere formula that includes core shear.", "how_it_affects_margin_or_SF": "Shear would lower collapse pressure. The omission is optimistic for SF."},
        {"NFI_id": "NFI-CORE", "linked_inputs_or_points": "I-RHO-CORE", "questionable_assumption_or_gap": "16 kg/m^3 has no pinned datasheet.", "direction_of_further_investigation": "Pin a honeycomb or foam sheet at the thickness used.", "how_it_affects_margin_or_SF": "Core density scales core mass and can erase the float margin. It does not enter the reported collapse formula."},
        {"NFI_id": "NFI-FRAME", "linked_inputs_or_points": "P3", "questionable_assumption_or_gap": "Tributary width equals spacing, members are pinned, mesh is a real-valued equal triangulation, tube crippling ignored.", "direction_of_further_investigation": "Integer geodesic, end fixity, imperfection knockdown and local crippling.", "how_it_affects_margin_or_SF": "Euler pressure scales with I and E and inversely with s^3. Mass scales with edge count and area."},
        {"NFI_id": "NFI-FILM", "linked_inputs_or_points": "P3 film", "questionable_assumption_or_gap": "Allowable, density and thickness are not one published film. Pocket radius set equal to spacing.", "direction_of_further_investigation": "Pin one film datasheet and a local pocket test.", "how_it_affects_margin_or_SF": "Film pressure scales with allowable and thickness. Film mass scales with density and thickness."},
        {"NFI_id": "NFI-GEOM", "linked_inputs_or_points": "all points", "questionable_assumption_or_gap": "External volume ignores skin intrusion and member protrusion.", "direction_of_further_investigation": "Define inner and outer mould lines.", "how_it_affects_margin_or_SF": "Volume error moves lift linearly."},
        {"NFI_id": "NFI-MASS", "linked_inputs_or_points": "joints nodes systems", "questionable_assumption_or_gap": "Allowances are round owner numbers.", "direction_of_further_investigation": "Replace with a parts list.", "how_it_affects_margin_or_SF": "Each kilogram reduces margin by 1/lift."},
        {"NFI_id": "NFI-GAS", "linked_inputs_or_points": "I-PINT and gas masses", "questionable_assumption_or_gap": "Perfect vacuum.", "direction_of_further_investigation": "State a hold pressure and the pump mass.", "how_it_affects_margin_or_SF": "Residual gas adds mass and reduces differential pressure."},
        {"NFI_id": "NFI-CHARTER", "linked_inputs_or_points": "sensitivity only", "questionable_assumption_or_gap": "Charter density and sea-level survival belong to the historical note.", "direction_of_further_investigation": "Do not let them replace the 500 m case.", "how_it_affects_margin_or_SF": "Shown only as labelled sensitivities."},
    ]

    atmo = {
        "T_K": T,
        "exponent": exponent,
        "p_ext_Pa": p_ext,
        "rho_kg_m3": rho,
        "lift_kg": lift,
        "volume_m3": V,
        "area_m2": area,
        "identity_relative_error": abs(ident_a - ident_b) / ident_a,
    }
    utc1, mono1 = now()
    elapsed1 = mono1 - ORIGIN_MONO
    out = {
        "schema": 1,
        "status": "ESTIMATE_PENDING_UNA",
        "unit": "vacuum-mainline-estimates-owner3000-1019",
        "atmosphere": atmo,
        "points": points,
        "inputs": inputs,
        "NFI": nfis,
        "sensitivities": sens,
        "phase2_write_utc": utc1,
        "phase2_write_monotonic_s": mono1,
        "phase2_write_elapsed_s": elapsed1,
        "phase1_early_elapsed_s": PHASE1_EARLY_ELAPSED,
        "checks": {
            "monocoque_identity": "PASS",
            "sandwich_closed_form": "PASS",
            "euler_characteristic": "PASS",
            "linear_factor_matches_pressure_ratio": "PASS",
        },
    }
    (ROOT / "RESULTS.json").write_text(json.dumps(out, indent=1) + "\n")
    (ROOT / "INPUTS.json").write_text(json.dumps(inputs, indent=1) + "\n")
    (ROOT / "POINTS.json").write_text(json.dumps(points, indent=1) + "\n")
    (ROOT / "NFI.json").write_text(json.dumps(nfis, indent=1) + "\n")
    (ROOT / "SENSITIVITIES.json").write_text(json.dumps(sens, indent=1) + "\n")
    print(json.dumps({
        "elapsed": elapsed1,
        "T": T,
        "exponent": exponent,
        "p_ext": p_ext,
        "rho": rho,
        "lift": lift,
        "P1": {"mass": m1, "margin": mar1, "p_cl": p1_cl, "p": p1, "sf": sf1, "factor": f1["improvement_factor"]},
        "P2": {"mass": m2, "margin": mar2, "p_cl": p2_cl, "p": p2, "sf": sf2, "factor": f2["improvement_factor"]},
        "P3": {"mass": m3, "margin": mar3, "p_euler": p_euler, "p_film": p_film, "sf": sf3, "mode": govern, "factor": f3["improvement_factor"]},
        "S_core": sens[-1],
    }, indent=1))


if __name__ == "__main__":
    main()
