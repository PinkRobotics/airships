#!/usr/bin/env python3
"""Published shell calculations, with paper terms separated from project primitives.

Akhmeteli & Gavrilin, Eng 2021, doi:10.3390/eng2040030, equations (7)-(9),
Discussion p.489. Jenett, Gregg & Cheung, NTRS 20190001133, equations (29),
(30), (33), section IV.D pp.8-9, section VI and Tables 1-2 p.12.
Inputs are supplied by the caller from the source records; no target mass enters sizing.
"""
import importlib.util
import math
from pathlib import Path


def project_primitives():
    spec = importlib.util.spec_from_file_location(
        "reproduction_cell", Path(__file__).with_name("vacuum-cell.py"))
    cell = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cell)
    return cell


def akhmeteli(radius_m, face_ratio, core_ratio, face_density, core_density,
              air_density, face_modulus):
    """Paper's final geometry, not its earlier analytical optimum or an FEA rerun."""
    r, h1, h3 = radius_m, face_ratio * radius_m, core_ratio * radius_m
    if min(r, h1, h3, face_density, core_density, air_density, face_modulus) <= 0 or 2*h1+h3 >= r:
        raise ValueError("invalid sandwich geometry/material")
    volume = lambda x: 4 * math.pi * x**3 / 3
    # The paper's term, not the project's: Eq.(7), thin-layer mass balance.
    thin_mass = 4 * math.pi * r**2 * (2*h1*face_density + h3*core_density)
    # The paper's term, not the project's: resolve that balance into concentric
    # layer volumes for the OUTER radius specified in Discussion p.489. Eq.(7)
    # neglects these finite-thickness corrections; retain both, never fit q.
    outer_face = (volume(r) - volume(r-h1)) * face_density
    core = (volume(r-h1) - volume(r-h1-h3)) * core_density
    inner_face = (volume(r-h1-h3) - volume(r-2*h1-h3)) * face_density
    mass = outer_face + core + inner_face
    displaced = volume(r) * air_density
    # Eq.(9) is the paper's semi-empirical sandwich term, not the project's
    # classical homogeneous-sphere buckling primitive. No substitution of the
    # project's monolithic knockdown (0.2), nor a claim to reproduce eigenvalue 2.65.
    critical_pressure = 2 * face_modulus * h1 * (h3+h1) / r**2
    return dict(shell_mass_kg=mass, payload_kg=displaced-mass,
                thin_shell_mass_kg=thin_mass, thin_payload_kg=displaced-thin_mass,
                displaced_air_kg=displaced, outer_face_kg=outer_face,
                core_kg=core, inner_face_kg=inner_face,
                paper_sandwich_critical_pressure_Pa=critical_pressure)


def euler_load(cell, section, length_m, modulus_Pa):
    """Reuse the project's pinned Euler primitive at the PAPER'S modulus.

    _ship_sigma_euler binds T700 in its interface. Linear modulus rescaling is
    exact, not an empirical fit; do not mutate its material table. ship_section's
    kgPerM is likewise T700-specific and is never used for paper mass.
    """
    return (cell._ship_sigma_euler(section, length_m) * section["A"]
            * modulus_Pa / cell.MATERIALS["T700_LAM"]["E"])


def jenett(radius_m, pressure_Pa, air_density, modulus_Pa, material_density,
           thickness_ratio=0.1, pitch_ratio=0.1, tube_radius_wall_ratio=10.0,
           member_count=None):
    """Run IV.D's local sizing; Table 2 mass needs an unstated member inventory.

    Figure 4's regular octahedron is interpreted with pitch as axial diagonal,
    four 45-degree members under the top load, pinned strut ends. These are
    explicit diagnostic conventions, not extra claims about the Table 2 code.
    member_count must count full equivalent struts, with sharing/boundaries
    resolved; the paper prints voxels, not this input. None stays unavailable.
    """
    if min(radius_m, pressure_Pa, air_density, modulus_Pa, material_density,
           thickness_ratio, pitch_ratio) <= 0 or tube_radius_wall_ratio <= 1:
        raise ValueError("invalid lattice inputs")
    cell = project_primitives()
    t = radius_m * thickness_ratio
    pitch = t * pitch_ratio
    # The paper's term, not the project's: Eq.(33) and IV.D, uniform shell
    # stress -> force on t^2 -> (t/pitch)^2 cells sharing it.
    stress = pressure_Pa * radius_m / (2*t)
    cell_force = stress * pitch**2
    # The paper's geometry, with the explicit interpretation described above.
    length = pitch / math.sqrt(2)
    member_force = cell_force / (4 / math.sqrt(2))
    # Solve IV.D's Euler sizing by scaling an actual project tube section.
    # At fixed tube r/wall ratio, Euler load scales with tube radius^4.
    unit = cell.ship_section(2000.0, 1000.0 / tube_radius_wall_ratio)
    tube_radius = (member_force / euler_load(cell, unit, length, modulus_Pa))**0.25
    section = cell.ship_section(2000*tube_radius, 1000*tube_radius/tube_radius_wall_ratio)
    member_mass = section["A"] * length * material_density
    displaced = 4 * math.pi * radius_m**3 * air_density / 3
    if member_count is not None and (not math.isfinite(member_count) or member_count < 0):
        raise ValueError("invalid member count")
    mass = None if member_count is None else member_mass * member_count
    return dict(radius_m=radius_m, shell_thickness_m=t, pitch_m=pitch,
                shell_stress_Pa=stress, cell_force_N=cell_force, member_force_N=member_force,
                member_length_m=length, tube_radius_m=tube_radius,
                member_euler_load_N=euler_load(cell, section, length, modulus_Pa),
                member_mass_kg=member_mass, displaced_air_kg=displaced,
                shell_mass_kg=mass, net_lift_kg=None if mass is None else displaced-mass,
                missing_inputs=["Table 2 equivalent strut count per radius, including shared edges and boundary truncation",
                                "Table 2 pitch-to-member-length convention and Euler effective-length factor"]
                if member_count is None else [])
