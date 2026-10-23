#!/usr/bin/env python3
"""Independent MAINLINE-025 arithmetic; no inherited executable is imported.

Run: TMPDIR=unpublished-local-ref:1ffe4110219d37c0 python3 model.py
All output remains beside this file. Values are conditional screens, not allowables.
"""

from __future__ import annotations

import hashlib
import json
import math
from dataclasses import asdict, dataclass, replace
from pathlib import Path

import numpy as np
import scipy
from scipy.optimize import minimize

HERE = Path(__file__).resolve().parent
SOURCE = Path(
    "unpublished-local-ref:1a0c61fe133cc91e"
    "/.ship/work/outputs/vacuum-mainline011b-p3-global-arcs-1019"
)
R = 10.0
PRESSURE = 95460.8379139
LIFT_MASS = 4889.44215019
FILM_MASS = 97.515
SYSTEMS_MASS = 50.0
NODE_MASS = 0.02
JOINT_FRACTION = 0.05
GLOBAL_K = 0.2
LOCAL_C = 0.6
FILM_STRENGTH = 1.5e9
FILM_THICKNESS = 80e-6
S_MIN, S_MAX, RO_CAP = 0.4, 3.0, 0.25
BASE_S, BASE_RO = 2.04, 0.12368836237368608
BASE_T = 0.0008802990936851718
SP8007_URL = (
    "https://ntrs.nasa.gov/api/citations/20205011530/downloads/"
    "20205011530%20Rev%202FINALa%201-2023.pdf"
)
CMC_URL = "https://ntrs.nasa.gov/api/citations/20210021598/downloads/TM-20210021598.pdf"
EQUILIBRIUM_NOTE = Path(
    "unpublished-local-ref:2f68afa9c74ca674"
    "/.ship/artifacts/vacuum-overnight-briefs-1019/NOTE-P3-EQUILIBRIUM.md"
)
EQUILIBRIUM_SHA = "dc65f9c0d7585fbf3e57e3423fe48896a96425fd9f3abdcf49ce3b7cadaf7d8e"
MODE_NAMES = (
    "compression_extreme", "Euler", "local_shell", "film",
    "global_lattice", "midspan_tension", "nodal_tension",
)


@dataclass(frozen=True)
class Material:
    name: str
    rho: float
    E: float
    Fc: float
    Ft: float | None = None
    status: str = "QUESTIONABLE conditional input"
    axial_force_factor: float = 1.0
    minimum_wall_m: float = 0.0


SIC = Material(
    "SiC inherited", 3100.0, 410e9, 3900e6, None,
    "3900 MPa inherited compression input; component allowable UNKNOWN",
)
CMC = Material(
    "CVI SiC/SiC balanced 0/90 scalar PROJECTION", 2440.0, 272e9, 128e6, 128e6,
    "E/rho/tensile PLS from Sylramic-iBN; Fc is an assumed proxy, not measured compression",
)


def budget(s, rho):
    """Counts are fractional continuum values, matching the stipulated model."""
    vertices = 8 * np.pi * R**2 / (np.sqrt(3) * s**2) + 2
    nodes = NODE_MASS * vertices
    length = (3 * vertices - 6) * s
    tube = (LIFT_MASS - FILM_MASS - SYSTEMS_MASS - nodes) / (1 + JOINT_FRACTION)
    area = tube / (rho * length)
    return vertices, nodes, length, tube, area


def radius_bounds(s, material):
    *_, area = budget(s, material.rho)
    # The lower bound and s/3 cap are explicit inherited 011b search bounds.
    upper = np.minimum(RO_CAP, s / 3)
    if material.minimum_wall_m:
        tw = material.minimum_wall_m
        upper = np.minimum(upper, (area/np.pi + tw**2)/(2*tw))
    return np.sqrt(area / np.pi) * 1.0001, upper


def geometry(s, ro, material, wall=None):
    vertices, nodes, length, tube, area = budget(s, material.rho)
    if wall is None:
        ri = np.sqrt(ro**2 - area / np.pi)
        # Algebraic form avoids loss of digits in thin-wall subtraction.
        wall = area / (np.pi * (ro + ri))
    else:
        ri = ro - wall
        area = np.pi * wall * (ro + ri)
        tube = material.rho * area * length
    inertia = area * (ro**2 + ri**2) / 4
    mean = material.axial_force_factor * PRESSURE * R * s / (2 * area)
    euler = np.pi**2 * material.E * inertia / (area * s**2)
    eta = (s / 1000) * ro * area / inertia
    return dict(
        s=s, ro=ro, ri=ri, wall=wall, area=area, inertia=inertia,
        vertices=vertices, nodes=nodes, length=length, tube=tube,
        mean=mean, euler=euler, eta=eta,
    )


def local_gamma(g, gamma):
    if gamma == "NASA":
        # NASA uses the shell reference/mid-surface radius. The inherited local
        # stress retains ro; this deliberately transfers only the gamma factor.
        ratio = ((g["ro"] + g["ri"]) / 2) / g["wall"]
        return 1 - 0.901 * (1 - np.exp(-np.sqrt(ratio) / 16))
    return np.asarray(gamma)


def compression_capacity(g, Fc):
    se, eta = g["euler"], g["eta"]
    phi = (Fc + (1 + eta) * se) / 2
    # The smaller root, written to avoid cancellation.
    return Fc * se / (phi + np.sqrt(np.maximum(0, phi**2 - Fc * se)))


def tension_capacity(g, Ft):
    """Mean axial stress when the opposite fibre first reaches tensile Ft."""
    se, eta = g["euler"], g["eta"]
    b = se * (eta - 1) + Ft
    radical = np.sqrt(b * b + 4 * Ft * se)
    # For Ft>0; a zero Ft is the onset-of-tension limit.
    if Ft == 0:
        return np.maximum(0, se * (1 - eta))
    denominator = radical + b
    return np.where(
        b >= 0, 2 * Ft * se / np.maximum(denominator, 1e-200),
        (radical - b) / 2,
    )


def capacities(g, material, gamma=1.0, Ct=0.0):
    mean = g["mean"]
    far = np.ones_like(mean) * 1e6  # finite inactive sentinel for optimization
    tensile = far if material.Ft is None else tension_capacity(g, material.Ft) / mean
    contact = far if material.Ft is None or Ct == 0 else material.Ft / (Ct * mean)
    return np.stack(np.broadcast_arrays(
        compression_capacity(g, material.Fc) / mean,
        g["euler"] / mean,
        LOCAL_C * material.E * g["wall"] / g["ro"] * local_gamma(g, gamma) / mean,
        2 * FILM_STRENGTH * FILM_THICKNESS / (g["s"] * PRESSURE),
        GLOBAL_K * 4 * np.sqrt(1.5) * material.E
        * np.sqrt(g["inertia"] * g["area"]) / (g["s"] * R**2 * PRESSURE),
        tensile, contact,
    ), axis=-1)


def stress_state(g, material, multiplier, Ct=0.0):
    mean = float(g["mean"]) * multiplier
    ratio = mean / float(g["euler"])
    state = dict(
        applied_pressure_multiplier=float(multiplier),
        N_N=float(mean * g["area"]),
        Ne_N=float(g["euler"] * g["area"]),
        N_over_Ne=ratio, mean_compression_Pa=mean,
        nodal_tension_Pa=Ct * mean,
        Ct_assumed=Ct,
        nodal_model_status="UNKNOWN: illustrative sigma_contact_t=Ct*N/A only",
    )
    if ratio >= 1:
        state.update(
            status="FAIL_EULER: N>=Ne; no finite pre-buckling stress estimate",
            bending_Pa=None, maximum_compression_Pa=None,
            opposite_signed_compression_Pa=None, midspan_tension_Pa=None,
            compression_pass=False, midspan_tension_pass=None,
        )
        return state
    bending = mean * float(g["eta"]) / (1 - ratio)
    compression = mean + bending
    opposite = mean - bending
    tension = max(0.0, -opposite)
    state.update(
        status="pre-Euler elastic calculation; other modes may already have failed",
        bending_Pa=bending, maximum_compression_Pa=compression,
        opposite_signed_compression_Pa=opposite, midspan_tension_Pa=tension,
        compression_pass=compression <= material.Fc * (1 + 1e-10),
        midspan_tension_pass=None if material.Ft is None else tension <= material.Ft * (1 + 1e-10),
        contact_tension_pass=None if material.Ft is None else Ct * mean <= material.Ft * (1 + 1e-10),
    )
    return state


def record(s, ro, material, gamma=1.0, Ct=0.0, wall=None):
    g = geometry(s, ro, material, wall=wall)
    cap = capacities(g, material, gamma, Ct)
    least = float(np.min(cap))
    score = {k: float(v) if v < 1e5 else None for k, v in zip(MODE_NAMES, cap)}
    active = [k for k, v in score.items() if v is not None and v <= least * (1 + 2e-6)]
    tube, node = float(g["tube"]), float(g["nodes"])
    total = FILM_MASS + SYSTEMS_MASS + node + tube * (1 + JOINT_FRACTION)
    midr = (ro + float(g["ri"])) / 2
    mean = float(g["mean"])
    max_tube_ignoring_nodes = (LIFT_MASS-FILM_MASS-SYSTEMS_MASS)/(1+JOINT_FRACTION)
    mean_floor = material.axial_force_factor * 4*np.pi*np.sqrt(3)*material.rho*PRESSURE*R**3/max_tube_ignoring_nodes
    result = dict(
        material=asdict(material), local_gamma_rule=gamma,
        member_force_branch=(
            "corrected uniform equilateral-grid equilibrium; topology remains a surrogate"
            if math.isclose(material.axial_force_factor, 1/math.sqrt(3), rel_tol=1e-12) else
            "inherited pRs/2 member demand, retained for comparison"
        ),
        local_gamma_value=float(local_gamma(g, gamma)), global_k=GLOBAL_K,
        Ct=Ct, s_m=float(s), r_o_m=float(ro), r_i_m=float(g["ri"]),
        t_m=float(g["wall"]), A_m2=float(g["area"]), I_m4=float(g["inertia"]),
        node_count=float(g["vertices"]), total_tube_length_m=float(g["length"]),
        m_nodes_kg=node, m_tube_kg=tube, m_joints_kg=JOINT_FRACTION * tube,
        m_film_kg=FILM_MASS, m_systems_kg=SYSTEMS_MASS, total_kg=total,
        float_margin_kg=LIFT_MASS-total, mass_within_float_ceiling=total <= LIFT_MASS+1e-8,
        SF_modes=score, SF_least=least,
        active_modes=active, factor_to_SF1=1 / least,
        eta=float(g["eta"]), mean_compression_Pa=mean, Euler_stress_Pa=float(g["euler"]),
        full_pressure=stress_state(g, material, 1.0, Ct),
        at_limiting_multiplier=stress_state(g, material, least, Ct),
        NASA_radius_over_t=midr/float(g["wall"]), NASA_length_over_radius=s/midr,
        local_shell_t_over_midradius=float(g["wall"])/midr,
        local_shell_thickness_status=(
            "THICK-WALL CAUTION: t/r>=0.1; thin-shell local formula uncalibrated"
            if float(g["wall"])/midr >= .1 else
            "thin-shell applicability remains unvalidated for the curved ceramic/component"
        ),
        NASA_r_over_t_within_1500=midr/float(g["wall"]) < 1500,
        NASA_length_range_caution=s/midr > 5,
        NASA_scope="QUESTIONABLE transfer to curved ceramic/composite struts; no shell-column interaction",
        weakest_link_compression="not inferred from tensile Weibull law",
        geometry_independent_mean_stress_floor_Pa=float(mean_floor),
        geometry_independent_compression_SF_ceiling=float(material.Fc/mean_floor),
        bound_assumptions="ignores all node mass, imperfection and every other failure mode; necessary upper bound only",
        midspan_tension_allowable_status="UNKNOWN / unscored" if material.Ft is None else "conditional assumed Ft",
        on_spacing_bound=bool(abs(s-S_MIN) < 1e-7 or abs(s-S_MAX) < 1e-7),
        on_radius_cap=bool(abs(ro-min(RO_CAP, s/3)) < 1e-7),
        on_minimum_wall=bool(material.minimum_wall_m and abs(float(g["wall"])-material.minimum_wall_m) < 1e-8),
        size_stress_interface=dict(
            total_tube_material_volume_m3=float(g["area"]*g["length"]),
            single_member_material_volume_m3=float(g["area"]*s),
            total_outer_surface_m2=float(2*np.pi*ro*g["length"]),
            total_inner_surface_m2=float(2*np.pi*g["ri"]*g["length"]),
            total_inner_plus_outer_surface_m2=float(2*np.pi*(ro+g["ri"])*g["length"]),
            effective_tensile_volume_m3=None, effective_tensile_surface_m2=None,
            size_adjusted_compression_allowable_Pa=None,
            interpretation=(
                "Geometric extents only, not effective stressed measures. MAINLINE-022b must integrate its "
                "actual positive tensile stress field and calibrated Weibull inputs; no tensile-to-compression transfer. "
                "End faces and node/joint material are not included."
            ),
        ),
    )
    for key, multiplier in (("full_pressure", 1.0), ("at_limiting_multiplier", least)):
        failures = [k for k, v in score.items() if v is not None and v < multiplier*(1-1e-9)]
        result[key]["failed_capacity_modes"] = failures
        result[key]["all_scored_modes_pass"] = not failures
        result[key]["physical_stress_interpretation"] = (
            "Pre-failure surrogate stress state" if not failures else
            "Counterfactual elastic stress calculation: a scored failure mode has already been exceeded"
        )
        tension = result[key]["midspan_tension_Pa"]
        result[key]["unscored_positive_tension"] = bool(material.Ft is None and tension is not None and tension > 0)
        if result[key]["unscored_positive_tension"]:
            result[key]["physical_stress_interpretation"] += "; POSITIVE TENSION HAS NO SCORED ALLOWABLE"
    result["unscored_positive_tension_at_limiting_load"] = result["at_limiting_multiplier"]["unscored_positive_tension"]
    result["stress_screen_scope"] = (
        "UPPER BOUND WITH TENSION UNSCORED: positive tensile stress at the claimed limiting multiplier"
        if result["unscored_positive_tension_at_limiting_load"] else
        "conditional scored modes only; component allowables and local/nodal models remain unvalidated"
    )
    return result


def grid(material, gamma=1.0, Ct=0.0, ns=131, nr=4000):
    spacing = np.linspace(S_MIN, S_MAX, ns)[:, None]
    low, high = radius_bounds(spacing, material)
    if np.any(high <= low):
        raise ValueError("minimum wall eliminates part of the spacing grid; revise feasible-domain handling")
    fraction = np.linspace(0, 1, nr)[None, :]
    radii = low + fraction * (high - low)
    g = geometry(spacing, radii, material)
    scores = capacities(g, material, gamma, Ct).min(axis=-1)
    indices = np.argmax(scores, axis=1)
    row_scores = scores[np.arange(ns), indices]
    ranked = np.argsort(-row_scores, kind="stable")
    best = int(ranked[0])
    result = record(float(spacing[best, 0]), float(radii[best, indices[best]]), material, gamma, Ct)
    seeds = []
    for i in ranked:
        s = float(spacing[i, 0])
        if not seeds or all(abs(s-v[0]) >= 0.12 for v in seeds):
            seeds.append([s, float(fraction[0, indices[i]]), float(row_scores[i])])
        if len(seeds) >= 5:
            break
    result["grid"] = dict(ns=ns, nr=nr, ds_m=(S_MAX-S_MIN)/(ns-1), radial_grid="linear fraction of per-s radius interval")
    return result, seeds


def optimize(material, gamma=1.0, Ct=0.0, ns=131, nr=2001):
    coarse, seeds = grid(material, gamma, Ct, ns, nr)
    runs, candidates = [], [coarse]

    def unpack(x):
        low, high = radius_bounds(x[0], material)
        return x[0], low + x[1] * (high-low)

    def constraint(x):
        s, ro = unpack(x)
        return capacities(geometry(s, ro, material), material, gamma, Ct) - x[2]

    for seed in seeds:
        fit = minimize(
            lambda x: -x[2], seed, method="SLSQP",
            bounds=((S_MIN, S_MAX), (0.0, 1.0), (0.0, 100.0)),
            constraints=[dict(type="ineq", fun=constraint)],
            options=dict(ftol=2e-12, maxiter=180),
        )
        s, ro = unpack(fit.x)
        candidate = record(float(s), float(ro), material, gamma, Ct)
        residual = float(np.min(constraint(fit.x)))
        runs.append(dict(
            success=bool(fit.success), iterations=int(fit.nit),
            SF=candidate["SF_least"], solver_objective=float(fit.x[2]),
            min_constraint_residual=residual, message=str(fit.message),
        ))
        # Rank by directly evaluated feasible physical score, never by epigraph z.
        candidates.append(candidate)
    best = max(candidates, key=lambda v: v["SF_least"])
    # A contact- or film-limited objective can have a radius plateau. Avoid
    # presenting an arbitrary tensile/Euler-critical point from that plateau.
    low, high = radius_bounds(best["s_m"], material)
    radii = np.append(np.linspace(low, high, 5001), best["r_o_m"])
    mode_grid = capacities(geometry(best["s_m"], radii, material), material, gamma, Ct)
    ordered_modes = np.sort(mode_grid, axis=-1)
    eligible = ordered_modes[:, 0] >= best["SF_least"]*(1-1e-12)
    if np.any(eligible):
        second = np.where(eligible, ordered_modes[:, 1], -np.inf)
        ro = float(radii[int(np.argmax(second))])
        best = record(best["s_m"], ro, material, gamma, Ct)
    best["optimization"] = dict(
        method="deterministic full-domain grid plus five separated SLSQP epigraph starts",
        coarse_grid=coarse["grid"], coarse_SF=coarse["SF_least"],
        continuous_gain=best["SF_least"]-coarse["SF_least"], starts=runs,
        plateau_tie_break="within relative1e-12 of best score, maximize second-smallest capacity at fixed best spacing",
        interpretation="numerical maximum found in bounded surrogate; not a certified global optimum",
    )
    return best


def tests(baseline, proxy, native, proxy_native):
    results = []

    def check(name, observed, expected, tolerance):
        ok = bool(abs(observed-expected) <= tolerance)
        results.append(dict(name=name, observed=observed, expected=expected, tolerance=tolerance, passed=ok))
        if not ok:
            raise AssertionError(results[-1])

    check("baseline exact point least SF", baseline["SF_least"], 1.2255279468805444, 2e-12)
    check("380 MPa conditional proxy exact point SF", proxy["SF_least"], .26224593555973924, 2e-12)
    check("011b 131x4000 grid baseline recovery", native["SF_least"], 1.2255279468805444, 2e-11)
    check("011b 131x4000 grid proxy recovery", proxy_native["SF_least"], .26224593555973924, 2e-11)
    check("baseline total float mass", baseline["total_kg"], LIFT_MASS, 2e-9)
    g = geometry(BASE_S, BASE_RO, SIC)
    check("annulus I identity", float(g["inertia"]), math.pi*(BASE_RO**4-float(g["ri"])**4)/4, 1e-18)
    compression_factor = baseline["SF_modes"]["compression_extreme"]
    at_compression = stress_state(g, SIC, compression_factor)
    check("Perry root equals separately evaluated compressive extreme", at_compression["maximum_compression_Pa"], SIC.Fc, .02)
    check("baseline has zero midspan tension", baseline["full_pressure"]["midspan_tension_Pa"], 0.0, 0.0)
    euler_factor = baseline["SF_modes"]["Euler"]
    pole = stress_state(g, SIC, euler_factor*(1+1e-12))
    if not pole["status"].startswith("FAIL_EULER"):
        raise AssertionError("post-Euler call was not refused")
    results.append(dict(name="explicit N>=Ne failure", passed=True, status=pole["status"]))
    m = replace(SIC, Ft=100e6)
    tensile_factor = float(tension_capacity(g, m.Ft)/g["mean"])
    check("tension capacity equals tensile-face root", stress_state(g, m, tensile_factor)["midspan_tension_Pa"], m.Ft, .05)
    corrected = geometry(BASE_S, BASE_RO, replace(SIC, axial_force_factor=1/math.sqrt(3)))
    check("triangular force correction at fixed section", float(corrected["mean"]/g["mean"]), 1/math.sqrt(3), 1e-14)
    check("geometry cancellation N/A", float(g["mean"]),
          4*math.pi*math.sqrt(3)*SIC.rho*PRESSURE*R**3/float(g["tube"]), .0001)
    wall_case = replace(SIC, minimum_wall_m=.004)
    _, ro_wall = radius_bounds(2.0, wall_case)
    check("minimum-wall radius bound identity", float(geometry(2.0, ro_wall, wall_case)["wall"]), .004, 1e-14)
    return results


def compact_row(row):
    return (
        f"| {row['material']['Fc']/1e6:g} | {row['local_gamma_rule']} | "
        f"{row['local_gamma_value']:.6f} | {row['SF_least']:.9f} | "
        f"{row['s_m']:.6f} | {row['r_o_m']*1000:.6f} | {row['t_m']*1000:.6f} | "
        f"{', '.join(row['active_modes'])} |"
    )


def notes(out):
    b = out["baseline_exact_point"]
    n = out["optimized_SiC_nasa_3900"]
    p = out["proxy_380_exact_point"]
    text = [
        "# MAINLINE-025 independent numerical screen", "",
        "All physical conclusions are QUESTIONABLE; mixed-material CMC cases are PROJECTION. "
        "The compression allowable of a finished ceramic arc, and the node tensile model, remain UNKNOWN. "
        "The script imports no inherited executable. It uses closed-form identities and its own search implementation.", "",
        "## Reconstruction and stress meaning", "",
        f"The stipulated 011b point gives SF={b['SF_least']:.12f}; the 380 MPa proxy point gives "
        f"{p['SF_least']:.12f}. The original 131-spacing by 4000-radius grid independently recovers both. "
        "The latter is an assumed compression-proxy case, not a measured compression failure prediction. "
        "The continuous ideal-local result is1.227314390995, slightly above the inherited grid maximum; "
        "the difference is search discretization.", "",
        f"At full pressure the SiC baseline mean compression is {b['full_pressure']['mean_compression_Pa']/1e6:.6f} MPa. "
        f"The geometric imperfection adds {b['full_pressure']['bending_Pa']/1e6:.6f} MPa at one face and subtracts it at the other; "
        f"the two faces remain at {b['full_pressure']['maximum_compression_Pa']/1e6:.6f} and "
        f"{b['full_pressure']['opposite_signed_compression_Pa']/1e6:.6f} MPa compression. "
        "There is zero midspan tensile stress in this assumed loading model. Node/contact tension is a separate unverified load path.", "",
        "For load multiplier λ, σ=λN₀/A, σ_E=π²EI/(As²), η=(s/1000)r_o A/I, "
        "σ_b=ση/(1−σ/σ_E), σ_c,max=σ+σ_b and σ_t,max=max(0,σ_b−σ). "
        "N≥N_E returns FAIL_EULER with no post-pole stress. "
        "The smaller root of σ_c,max=F_c reproduces geometric Perry capacity; it is a conditional elastic extreme-stress limit. "
        "Flexural strength is never silently substituted for a measured F_c. "
        "Tension and node limits use separately declared F_t.", "",
        "## Fixed assumptions and equations", "",
        "R=10 m; p=95,460.8379139 Pa; lift ceiling=4,889.44215019 kg; "
        "film=97.515 kg; systems=50 kg; V=8πR²/(√3s²)+2; nodes=0.02V kg; "
        "tube length=(3V−6)s; tube budget=(lift−film−systems−nodes)/1.05; joints=0.05 tube. "
        "Area is tube budget/(ρ total length); r_i²=r_o²−A/π; I=A(r_o²+r_i²)/4 exactly. "
        "The dimensions are constrained to 0.4≤s≤3 m, "
        "sqrt(A/π)×1.0001≤r_o≤min(0.25 m,s/3), retaining the inherited s/3 bound. "
        "Mass, Euler and imperfection all retain s as member length; exact spherical arc length, discrete node counts, "
        "fixture design and fabrication tolerances are unresolved.", "",
        "The global pressure is k_g 4√(3/2)E√(IA)/(sR²), with k_g=0.2 fixed. "
        "Local critical mean stress is γ_local×0.6Et/r_o. Euler is pinned-end π²EI/s². "
        "Film pressure is 2×1.5 GPa×80 µm/s. These modes are independent minima, without a combined local/global/column interaction. "
        "Joint mass is only the assigned fraction, with no demonstrated bearing/bond/load-path capacity. "
        "Every mass-limited optimized row has zero nominal float margin; it does not reserve useful payload or extra defect tolerance.", "",
        "## Geometry-independent compression ceiling", "",
        "Because (3V−6)s²=8√3πR², the inherited load gives "
        "N/A=4√3πρpR³/M_tube. The radius and spacing cancel except for spacing-dependent node mass. "
        "Ignoring all node mass makes M_tube≤(lift−film−systems)/1.05 and sets an optimistic lower bound "
        "on mean compression. Perry bending and all other modes can only reduce the resulting F_c/(N/A) ceiling. "
        f"For SiC the floor is {b['geometry_independent_mean_stress_floor_Pa']/1e6:.6f} MPa. "
        "This explains why geometry changes cannot rescue a low assumed compression limit within this mass/load model.", "",
        "## Local-shell knockdown", "",
        f"[NASA SP-8007 Rev.2]({SP8007_URL}), report pp.23–25, Eqs.9–10, gives "
        "γ=1−0.901(1−exp(−√(r/t)/16)), r/t<1500, for isotropic cylinders. "
        "The report cautions about L/r>5 and uncaptured shell/column interaction. "
        "Here r=(r_o+r_i)/2 enters γ while the inherited 0.6Et/r_o formula is retained. "
        "Curvature, ceramic manufacture and the long-strut range make the transfer QUESTIONABLE. "
        "The numerical formula is still evaluated outside r/t<1500 and every row carries an explicit range flag; "
        "no extrapolated row becomes an established allowable.", "",
        f"At the original point NASA γ={out['fixed_gamma_sensitivity'][-1]['local_gamma_value']:.9f}, "
        f"giving least SF={out['fixed_gamma_sensitivity'][-1]['SF_least']:.9f}. "
        f"Reoptimizing the conditional 3900 MPa case gives SF={n['SF_least']:.9f}, "
        f"s={n['s_m']:.9f} m, r_o={n['r_o_m']*1000:.6f} mm, t={n['t_m']*1000:.6f} mm.", "",
        "## Conditional SiC reoptimization", "",
        "| Assumed F_c MPa | Local rule | γ at optimum | Least SF | s m | r_o mm | t mm | Active modes |",
        "|---:|---|---:|---:|---:|---:|---:|---|",
    ]
    text.extend(compact_row(row) for row in out["SiC_conditional_scan"])
    text += [
        "", "No row in this table establishes the assumed F_c. Low values and 380 MPa are scenario inputs. "
        "A tensile weakest-link or Weibull extrapolation is not used as a compression law.", "",
        "## CMC scalar screening", "",
        f"[NASA CMC dataset]({CMC_URL}): E=272 GPa, ρ=2440 kg/m³, tensile PLS=128 MPa, UTS=357 MPa "
        "for the selected CVI balanced 0/90 Sylramic-iBN material supplied by the parent research. "
        "The calculation uses F_t=128 MPa as a no-cracking tensile proxy. "
        "F_c=128 MPa is a no-cracking proxy, 300 MPa an assumption, and 580 MPa an optimistic mixed-material ceiling "
        "from a different Honeywell Hi-Nicalon material. No case is a same-lot orthotropic tube allowable. "
        "A single E cannot resolve laminate bending, shear, off-axis and interlaminar failure.", "",
        "| Assumed F_c MPa | Local rule | γ at optimum | Least SF | s m | r_o mm | t mm | Active modes |",
        "|---:|---|---:|---:|---:|---:|---:|---:|---|",
    ]
    text.extend(compact_row(row) for row in out["CMC_reoptimized"])
    text += [
        "", "The JSON also contains a strict material swap at the frozen SiC s/r_o/t "
        "(mass changes), and a mass-limited same-s/r_o swap (wall thickness is recomputed). "
        "This distinguishes a fixed physical component from a fixed pair of search coordinates.", "",
        "## Contact and tension sensitivities", "",
        "At each declared point the JSON reports C_t in {0,0.02,0.05,0.1,0.2} with "
        "σ_contact,t=C_t N/A. This is an illustrative multiplier, UNKNOWN as a node model. "
        "The all-compression midspan result cannot establish that a real node has no tensile stress. "
        "F_t in {50,100,200,380} MPa is another declared sensitivity; 380 MPa remains a flexural proxy. "
        "The optimized contact cases change both s and r_o, whereas fixed cases preserve the baseline geometry.", "",
        "An additional reliability sensitivity uses F_t=15.586 MPa and 7.192 MPa supplied by the parallel reliability calculation. "
        "Those are explicitly hypothetical whole-array uniform tensile-field screens at Pf=10⁻⁶, "
        "with assumed Weibull moduli 10/8, 380 MPa mean bend strength and 40/20 mm bend spans. "
        "Applying them to the unknown contact stress through C_t is a PROJECTION, not a calibrated contact reliability calculation "
        "and never a compression allowable. Fixed results cover C_t={0.005,0.01,0.02,0.05}; the 15.586 MPa branch is also reoptimized.", "",
        "## Borrowed wall-thickness screens", "",
        "Minimum walls of 2 mm and 4 mm are pure geometric sensitivity constraints borrowed from a different SiSiC construction "
        "example; they are not stated manufacturing limits for Hexoloy SA. The JSON reports both increased mass at the baseline "
        "outer diameter and mass-limited reoptimization to a smaller diameter. E=410 GPa and ρ=3100 kg/m³ are held fixed. "
        "A wall constraint restricts r_o≤(A/π+t_min²)/(2t_min), with exact annulus area. "
        "The original F_t=None 4 mm optimum is ONLY AN UPPER BOUND WITH TENSION UNSCORED: at its limiting multiplier "
        f"{out['borrowed_minimum_wall_reoptimized'][-1]['SF_least']:.9f}, the model has "
        f"{out['borrowed_minimum_wall_reoptimized'][-1]['at_limiting_multiplier']['midspan_tension_Pa']/1e9:.6f} GPa "
        "midspan tensile stress. This is not a complete stress screen. Its mid-radius/thickness ratio is "
        f"{out['borrowed_minimum_wall_reoptimized'][-1]['NASA_radius_over_t']:.6f}, outside a genuinely thin-shell regime; "
        "the local-shell expression is uncalibrated and inactive there. Record-level flags identify every unscored "
        "positive tensile stress at the limiting load, and a top-level index lists those rows.", "",
        "Additional 2 mm and 4 mm cases impose F_t=15.586 MPa (uniform-field illustrative reliability screen) "
        "or F_t=380 MPa (typical bend-strength proxy, not an allowable), with the NASA local rule. "
        "Neither tensile proxy is calibrated to the nonuniform component stress field. Their results are:", "",
        "| Minimum wall mm | Assumed F_t MPa | Least SF | s m | r_o mm | Tensile stress at limit MPa | Active modes |",
        "|---:|---:|---:|---:|---:|---:|---|",
        *[
            f"| {r['material']['minimum_wall_m']*1000:g} | {r['material']['Ft']/1e6:g} | "
            f"{r['SF_least']:.9f} | {r['s_m']:.6f} | {r['r_o_m']*1000:.6f} | "
            f"{r['at_limiting_multiplier']['midspan_tension_Pa']/1e6:.6f} | {', '.join(r['active_modes'])} |"
            for r in out["borrowed_minimum_wall_tension_constrained"]
        ],
        "",
        "## Corrected equilateral equilibrium and inherited demand", "",
        "There is a distinct inherited load-path inconsistency. Each of the three triangular-grid member families has length "
        "density 2/(√3s). Because the direction factors sum to Σcos²θ=3/2, membrane force per width is "
        "N_x=(√3/s)N_member. Sphere equilibrium N_x=pR/2 therefore gives "
        "N_member=pRs/(2√3), while the inherited point uses pRs/2. The inherited Et=2EA/(√3s) is consistent with the former rule. "
        "The pinned NOTE-P3-EQUILIBRIUM confirms this correction by membrane, node and tributary-load equilibrium. "
        "The corrected branch changes only the member-force factor to 1/√3, leaving global and film expressions unchanged. "
        "Uniform triangular topology and the smeared global model remain surrogate assumptions requiring discrete-model review. "
        "The inherited calculation is retained. Compression, Euler and local pressure factors improve by √3 at fixed geometry; "
        "geometry-dependent reoptimization is reported for every requested compression scenario. "
        "At the original SiC geometry the two mean demands are "
        f"{out['dual_demand_summary']['fixed_original_equilateral_mean_Pa']/1e9:.9f} and "
        f"{out['dual_demand_summary']['fixed_original_inherited_mean_Pa']/1e9:.9f} GPa. "
        "The film-sag volume/lift charge is owned by 024/022b and is not added to this inherited mass budget.", "",
        "| Material | Assumed F_c MPa | Reoptimized SF, inherited demand | Reoptimized SF, corrected equilateral demand |",
        "|---|---:|---:|---:|",
        *[
            f"| {row['material']} | {row['Fc_Pa']/1e6:g} | {row['inherited_SF']:.9f} | {row['equilateral_SF']:.9f} |"
            for row in out["dual_demand_summary"]["reoptimized_comparison"]
        ],
        "",
        "The next table freezes the original physical s/r_o/t for each material, so the two mean stresses are the same "
        "for SiC and CMC, while mass changes with density. F_t is an independent input: unscored for the SiC compression "
        "scenarios and 128 MPa for CMC. The JSON separately provides fixed search coordinates with a recalculated mass-limited "
        "wall, avoiding confusion between a physical material swap and a refitted member.", "",
        "| Material | Assumed F_c MPa | Fixed geometry SF, inherited demand | Fixed geometry SF, corrected equilateral demand |",
        "|---|---:|---:|---:|",
        *[
            f"| {row['material']} | {row['Fc_Pa']/1e6:g} | {row['inherited_SF']:.9f} | {row['equilateral_SF']:.9f} |"
            for row in out["dual_demand_summary"]["fixed_physical_comparison"]
        ],
        "",
        "## Size/stressed-measure interface for 022b", "",
        "Every row exposes total and single-member tube material volume, outer/inner surface area, the signed full-pressure "
        "and limiting-load stress state, and the force branch. Those geometric extents are not Weibull effective volume or area. "
        "Effective tensile measures and size-adjusted compression allowance remain null: 022b must integrate the actual positive "
        "tensile stress field with calibrated inputs. Compression stays a separately declared conditional F_c. "
        "Node/joint material and tube end faces are not included in these tube surface measures.", "",
        "## Search verification and forward carry", "",
        "The inherited 0.02 m / 4000-radius search is labeled grid reproduction. Continuous results use "
        "a full-domain grid followed by five separated SLSQP epigraph starts and direct recomputation of each score. "
        "A doubled spacing grid and 4000-radius grid are reported separately for selected SiC/CMC cases. "
        "These establish numerical resolution for this surrogate, not proof of a global structural optimum. "
        "A flat optimum in radius is resolved by maximizing the second-lowest capacity at the chosen spacing, "
        "within 10⁻¹² relative tolerance on the primary score. Such a radius is not a unique geometry prediction. "
        "Self-checks cover original point/grid recovery, float closure, exact annulus inertia, compressive/tensile roots, "
        "and refusal to extrapolate through the Euler pole. Repository tests were not run for this outputs-only analytic script.", "",
        "Verified starting state: original arithmetic reproduced, stress signs separated, and all requested bounded sensitivity families "
        "computed independently. Learned: the inherited mean compression is about 1.43 GPa, so tensile coupon size scaling alone "
        "does not resolve compression capacity; local knockdown consumes much of the original small structural margin. "
        "Deferred: calibrated ceramic/CMC compression data, probabilistic component reliability, actual nodal stresses, "
        "orthotropic shell/column interaction and manufacturing. Next: use these conditional tables to choose the necessary "
        "component/connection tests and numerical shell analysis; do not certify the vehicle from this surrogate.", "",
    ]
    return "\n".join(text)


def main():
    inherited = json.loads((SOURCE/"INPUTS.json").read_text())
    assert inherited["constants"]["p_ext_Pa"] == PRESSURE
    assert inherited["materials"]["SiC-alpha-Hexoloy-SA"]["E_Pa"] == SIC.E
    source_pins = {
        name: hashlib.sha256((SOURCE/name).read_bytes()).hexdigest()
        for name in ("CARD.md", "INPUTS.json", "RESULTS.json", "arcs.py")
    }
    equilibrium_sha = hashlib.sha256(EQUILIBRIUM_NOTE.read_bytes()).hexdigest()
    if equilibrium_sha != EQUILIBRIUM_SHA:
        raise AssertionError("equilibrium note pin changed")
    baseline = record(BASE_S, BASE_RO, SIC)
    proxy_material = replace(SIC, Fc=380e6, status="380 MPa flexural number used only as conditional assumed compression proxy")
    proxy = record(1.38, .21924454143380107, proxy_material)
    native, _ = grid(SIC)
    proxy_native, _ = grid(proxy_material)
    verification = tests(baseline, proxy, native, proxy_native)
    local_rules = [0.3, 0.5, 0.7, 1.0, "NASA"]
    scans = []
    for fc in (100e6, 200e6, 380e6, 1000e6, 3900e6):
        material = replace(SIC, Fc=fc, status=f"QUESTIONABLE assumed F_c={fc/1e6:g} MPa; not component compression data")
        for gamma in local_rules:
            scans.append(optimize(material, gamma))
    cmc = []
    for fc in (128e6, 300e6, 580e6):
        material = replace(CMC, Fc=fc, status=(
            "PROJECTION: Fc128 no-cracking proxy, not measured compression" if fc == 128e6 else
            "PROJECTION: Fc300 assumed compression input" if fc == 300e6 else
            "PROJECTION: Fc580 optimistic mixed Hi-Nicalon compression with Sylramic-iBN E/rho"
        ))
        for gamma in (1.0, "NASA"):
            cmc.append(optimize(material, gamma))
    contact = []
    for ft in (50e6, 100e6, 200e6, 380e6):
        material = replace(SIC, Ft=ft, status="conditional tensile input; Fc3900 retained, not a component allowable")
        for ct in (0, .02, .05, .1, .2):
            contact.append(record(BASE_S, BASE_RO, material, "NASA", ct))
    contact_optimized = [
        optimize(replace(SIC, Ft=100e6), "NASA", ct) for ct in (0, .02, .05, .1, .2)
    ]
    ctc = [
        optimize(replace(CMC, Fc=580e6), "NASA", ct) for ct in (0, .02, .05, .1, .2)
    ]
    reliability_fixed = [
        record(BASE_S, BASE_RO, replace(SIC, Ft=ft, status="PROJECTION: hypothetical tensile Weibull/contact transfer"), "NASA", ct)
        for ft in (7.192e6, 15.586e6) for ct in (.005, .01, .02, .05)
    ]
    reliability_reoptimized = [
        optimize(replace(SIC, Ft=15.586e6, status="PROJECTION: hypothetical tensile Weibull/contact transfer"), "NASA", ct)
        for ct in (.005, .01, .02, .05)
    ]
    walls_fixed, walls_reoptimized, walls_tension = [], [], []
    for wall in (.002, .004):
        scenario = replace(SIC, minimum_wall_m=wall, status="QUESTIONABLE pure geometry constraint, not SA manufacturing limit")
        walls_fixed.append(record(BASE_S, BASE_RO, scenario, "NASA", wall=wall))
        for gamma in (1.0, "NASA"):
            walls_reoptimized.append(optimize(scenario, gamma))
        for ft in (15.586e6, 380e6):
            constrained = replace(
                scenario, Ft=ft,
                status="PROJECTION: borrowed minimum wall plus illustrative tensile screen; not component allowable",
            )
            row = optimize(constrained, "NASA")
            if row["at_limiting_multiplier"]["midspan_tension_Pa"] > ft*(1+1e-8):
                raise AssertionError("wall scenario exceeded explicitly scored tensile limit")
            if row["unscored_positive_tension_at_limiting_load"]:
                raise AssertionError("scored wall tensile limit marked unscored")
            walls_tension.append(row)
    unscored4 = walls_reoptimized[-1]
    if not unscored4["unscored_positive_tension_at_limiting_load"]:
        raise AssertionError("4 mm unscored-tension bound was not flagged")
    verification.append(dict(
        name="4 mm tensile omission exposed",
        passed=True, tensile_Pa=unscored4["at_limiting_multiplier"]["midspan_tension_Pa"],
    ))
    verification.append(dict(
        name="four explicit wall/tension cases respect their limiting tensile proxy",
        passed=True, rows=len(walls_tension),
    ))
    dual_materials = [
        replace(SIC, Fc=fc, status="QUESTIONABLE conditional compression input; no component allowable")
        for fc in (100e6, 200e6, 380e6, 1000e6, 3900e6)
    ] + [
        replace(CMC, Fc=fc, status=(
            "PROJECTION CMC assumed compression; Ft128 independent" if fc != 580e6 else
            "PROJECTION mixed-material CMC compression ceiling; Ft128 independent"
        ))
        for fc in (128e6, 300e6, 580e6)
    ]
    all_triangular_cases = [replace(m, axial_force_factor=1/math.sqrt(3)) for m in dual_materials]
    all_triangular_optima = [optimize(m, "NASA") for m in all_triangular_cases]
    # Preserve the earlier three-row branch and its order for existing consumers.
    triangular_cases = [all_triangular_cases[i] for i in (4, 5, 7)]
    triangular_reoptimized = [all_triangular_optima[i] for i in (4, 5, 7)]
    dual_fixed, dual_mass_limited = [], []
    dual_optimized_comparison, dual_fixed_comparison = [], []
    for material, corrected in zip(dual_materials, all_triangular_optima):
        physical_pair = []
        for force in (1.0, 1/math.sqrt(3)):
            branch = replace(material, axial_force_factor=force)
            physical = record(BASE_S, BASE_RO, branch, "NASA", wall=BASE_T)
            physical_pair.append(physical)
            dual_fixed.append(physical)
            dual_mass_limited.append(record(BASE_S, BASE_RO, branch, "NASA"))
        inherited_optimum = next(
            r for r in scans+cmc
            if r["material"]["rho"] == material.rho and r["material"]["Fc"] == material.Fc
            and r["local_gamma_rule"] == "NASA"
        )
        label = "SiC" if material.rho == SIC.rho else "CMC"
        dual_optimized_comparison.append(dict(
            material=label, Fc_Pa=material.Fc,
            inherited_SF=inherited_optimum["SF_least"], equilateral_SF=corrected["SF_least"],
        ))
        dual_fixed_comparison.append(dict(
            material=label, Fc_Pa=material.Fc,
            inherited_SF=physical_pair[0]["SF_least"], equilateral_SF=physical_pair[1]["SF_least"],
        ))
        for mode in ("compression_extreme", "Euler", "local_shell"):
            ratio = physical_pair[1]["SF_modes"][mode] / physical_pair[0]["SF_modes"][mode]
            if abs(ratio-math.sqrt(3)) > 2e-12:
                raise AssertionError("fixed-geometry member-force scaling differs from sqrt3")
        if abs(physical_pair[0]["SF_modes"]["global_lattice"]-physical_pair[1]["SF_modes"]["global_lattice"]) > 2e-12:
            raise AssertionError("global pressure changed with member force branch")
    verification.append(dict(
        name="eight dual-demand fixed geometries recover sqrt3 member-mode scaling with unchanged global pressure",
        passed=True, material_scenarios=len(dual_materials),
    ))
    equilateral_refined = optimize(all_triangular_cases[3], "NASA", ns=261, nr=4000)
    equilateral_difference = equilateral_refined["SF_least"]-all_triangular_optima[3]["SF_least"]
    if abs(equilateral_difference) > 1e-8:
        raise AssertionError("corrected-equilateral Fc1000 optimum failed refinement agreement")
    equilateral_refined["comparison_SF"] = all_triangular_optima[3]["SF_least"]
    equilateral_refined["comparison_difference"] = equilateral_difference
    verification.append(dict(
        name="corrected equilateral Fc1000 refined search agreement",
        passed=True, SF_difference=equilateral_difference, tolerance=1e-8,
    ))
    convergence = []
    for material, gamma in (
        (SIC, 1.0), (SIC, "NASA"), (proxy_material, "NASA"), (replace(CMC, Fc=580e6), "NASA")
    ):
        refined = optimize(material, gamma, ns=261, nr=4000)
        convergence.append(refined)
    nasa3900 = next(r for r in scans if r["material"]["Fc"] == 3900e6 and r["local_gamma_rule"] == "NASA")
    output = dict(
        schema=1, unit="vacuum-mainline025-sic-arc-reality-1020", status="QUESTIONABLE",
        source_sha256=source_pins, dependencies=dict(numpy=np.__version__, scipy=scipy.__version__),
        equilibrium_note_pin=dict(path=str(EQUILIBRIUM_NOTE), sha256=equilibrium_sha, matches=True),
        baseline_exact_point=baseline, proxy_380_exact_point=proxy,
        reproduction_original_grid=native, proxy_reproduction_original_grid=proxy_native,
        fixed_gamma_sensitivity=[record(BASE_S, BASE_RO, SIC, gamma) for gamma in local_rules],
        fixed_Fc_sensitivity=[
            record(BASE_S, BASE_RO, replace(SIC, Fc=fc), gamma)
            for fc in (100e6, 200e6, 380e6, 1000e6, 3900e6) for gamma in (1.0, "NASA")
        ],
        SiC_conditional_scan=scans, optimized_SiC_nasa_3900=nasa3900,
        CMC_fixed_physical_geometry=[
            record(BASE_S, BASE_RO, replace(CMC, Fc=fc), gamma, wall=BASE_T)
            for fc in (128e6, 300e6, 580e6) for gamma in (1.0, "NASA")
        ],
        CMC_same_spacing_radius_mass_limited=[
            record(BASE_S, BASE_RO, replace(CMC, Fc=fc), gamma)
            for fc in (128e6, 300e6, 580e6) for gamma in (1.0, "NASA")
        ],
        CMC_reoptimized=cmc, fixed_contact_tensile_sensitivity=contact,
        SiC_contact_reoptimized_Ft100=contact_optimized,
        CMC_contact_reoptimized_Fc580_Ft128=ctc,
        hypothetical_Weibull_contact_fixed=reliability_fixed,
        hypothetical_Weibull_contact_reoptimized_Ft15_586=reliability_reoptimized,
        borrowed_minimum_wall_fixed_OD=walls_fixed,
        borrowed_minimum_wall_reoptimized=walls_reoptimized,
        borrowed_minimum_wall_tension_constrained=walls_tension,
        equilateral_force_fixed=[record(BASE_S, BASE_RO, m, "NASA") for m in triangular_cases],
        equilateral_force_reoptimized=triangular_reoptimized,
        SiC_equilateral_conditional_scan=all_triangular_optima[:5],
        CMC_equilateral_conditional_scan=all_triangular_optima[5:],
        equilateral_Fc1000_refined_search=equilateral_refined,
        fixed_physical_geometry_dual_demand=dual_fixed,
        fixed_search_coordinates_dual_demand_mass_limited=dual_mass_limited,
        dual_demand_summary=dict(
            fixed_original_inherited_mean_Pa=dual_fixed[0]["mean_compression_Pa"],
            fixed_original_equilateral_mean_Pa=dual_fixed[1]["mean_compression_Pa"],
            reoptimized_comparison=dual_optimized_comparison,
            fixed_physical_comparison=dual_fixed_comparison,
            Ft_independent=True,
            film_sag_charge="not added here; 024/022b owns the changed film geometry and lift accounting",
        ),
        convergence_refined_runs=convergence,
        baseline_stress_load_sweep=[
            stress_state(geometry(BASE_S, BASE_RO, SIC), SIC, lam)
            for lam in (0, .5, 1, baseline["SF_least"], 2, 5, 5.1704150978555, 6)
        ],
        source_references=dict(SP8007=SP8007_URL, CMC=CMC_URL),
        verification=verification,
    )
    unscored_index = []
    for family, values in output.items():
        rows = values if isinstance(values, list) else [values]
        for i, row in enumerate(rows):
            if isinstance(row, dict) and row.get("unscored_positive_tension_at_limiting_load"):
                unscored_index.append(dict(
                    family=family, row_index=i, SF_least=row["SF_least"],
                    tensile_at_limit_Pa=row["at_limiting_multiplier"]["midspan_tension_Pa"],
                    status="UPPER BOUND WITH TENSION UNSCORED",
                ))
    output["unscored_positive_tension_at_limit"] = dict(
        present=bool(unscored_index), rows=unscored_index,
        interpretation="These rows do not provide a complete stress screen, even if all scored modes pass.",
    )
    for row in convergence:
        matched = next((x for x in scans+cmc
                  if x["material"]["Fc"] == row["material"]["Fc"]
                  and x["material"]["rho"] == row["material"]["rho"]
                  and x["local_gamma_rule"] == row["local_gamma_rule"]), None)
        row["comparison_SF"] = None if matched is None else matched["SF_least"]
        row["comparison_difference"] = None if matched is None else row["SF_least"]-matched["SF_least"]
    (HERE/"model-results.json").write_text(json.dumps(output, indent=2, allow_nan=False)+"\n")
    (HERE/"model-notes.md").write_text(notes(output)+"\n")
    print(json.dumps({
        "checks_passed": len(verification), "original_SF": baseline["SF_least"],
        "proxy380_SF": proxy["SF_least"], "NASA_fixed_SF": output["fixed_gamma_sensitivity"][-1]["SF_least"],
        "NASA_optimized_SF": nasa3900["SF_least"],
        "CMC_optimized": [
            dict(Fc_MPa=x["material"]["Fc"]/1e6, gamma=x["local_gamma_rule"], SF=x["SF_least"])
            for x in cmc
        ],
        "outputs": ["model.py", "model-results.json", "model-notes.md"],
    }, indent=2))


if __name__ == "__main__":
    main()
