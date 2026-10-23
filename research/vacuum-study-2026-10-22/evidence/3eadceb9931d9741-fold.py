"""MAINLINE-043: conditional reliability on the two pinned MAINLINE-041 frames."""

import csv
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import brentq

ROOT = Path(__file__).resolve().parent
TAG = "QUESTIONABLE / PROJECTION"
MODULI = [5, 8, 10, 11, 15, 20, 30]
TARGETS = [1e-3, 1e-6]
SCALE = 3.9e9
E = 410e9
RHO = 3100.0
CHECKS = []


def load(name):
    return json.loads((ROOT / name).read_text())


def save(name, obj):
    (ROOT / name).write_text(json.dumps(obj, indent=2, allow_nan=False) + "\n")


def check(name, passed, detail=None):
    CHECKS.append(dict(name=name, passed=bool(passed), detail=detail))
    if not passed:
        raise AssertionError(f"{name}: {detail}")


def close(name, got, expected, rtol=2e-9, atol=1e-10):
    check(name, math.isclose(float(got), float(expected), rel_tol=rtol, abs_tol=atol),
          dict(got=float(got), expected=float(expected)))


def pf(hazard):
    return -np.expm1(-hazard)


def maximum(values, member, count):
    result = np.full(count, -np.inf)
    np.maximum.at(result, member, values)
    return result


def minimum(values, member, count):
    result = np.full(count, np.inf)
    np.minimum.at(result, member, values)
    return result


def risk(stress, size_ratio, m, scale=SCALE):
    h = size_ratio * (stress / scale) ** m
    p = pf(h)
    return dict(
        m=m, assumed_reference_characteristic_Pa=scale,
        member_Pf_min=float(p.min()), member_Pf_max=float(p.max()),
        frame_hazard=float(h.sum()), frame_Pf=float(pf(h.sum())),
    )


def required(stress, size_ratio, m, target):
    htarget = -math.log1p(-target)
    # Normalize before exponentiation to retain comfortable numerical range.
    scale = 1e9 * float(np.sum(size_ratio * (stress / 1e9) ** m) / htarget) ** (1 / m)
    close("inverse reliability requirement", risk(stress, size_ratio, m, scale)["frame_Pf"],
          target, rtol=2e-10, atol=1e-18)
    return scale


def required_m(stress, size_ratio, target):
    htarget = -math.log1p(-target)
    check("all stresses below hypothetical 3.9GPa scale", np.all(stress < SCALE))
    answer = brentq(lambda m: float(np.sum(size_ratio * (stress / SCALE) ** m)) - htarget,
                    0.1, 300, xtol=1e-12)
    close("inverse scatter requirement", risk(stress, size_ratio, answer)["frame_Pf"],
          target, rtol=1e-9, atol=1e-18)
    return answer


source = load("intake/041/RESULTS.json")
prior = load("intake/043/RESULTS.json")
q022d = prior["geometry"]["target_multiplier"]
check("source capacity and probability remain unqualified",
      source["qualified_failure_probability"] is None
      and source["qualified_structural_SF"] is None)

# Reuse only the explicitly stated reference calibration from the frozen 043 projections.
tensile_models = []
for row in prior["tensile_thresholds"]:
    if row["stressed_fraction"] == 1 and row["frame_target"] == 1e-3:
        tensile_models.append(dict(
            grade=row["grade"], m=row["m"], population=row["population"],
            scale=row["assumed_or_derived_coupon_characteristic_Pa"],
            reference=row["reference_effective_size"],
            reference_basis="Frozen 043 assumed/derived bend calibration; same flaw population transfer unqualified",
        ))
for row in prior["cvd_miniature_tube_tensile_only"]:
    tensile_models.append(dict(
        grade=row["grade"], m=row["m"], population="inner_surface",
        scale=row["derived_coupon_characteristic_Pa"], reference=row["reference_area_m2"],
        reference_basis="Miniature CVD coating hoop-tension population, not commercial CVD qualification",
    ))

points = []
all_comparison_rows = []
for reserve, witness in source["best_closure_by_reserve"].items():
    section = witness["section"]
    geo = witness["geometry"]
    count = geo["members"]
    lengths = np.asarray(geo["member_arc_lengths_m"])
    sample = ROOT / "intake/041" / witness["source_sample"]
    response = json.loads(sample.read_text())
    with np.load(sample.with_name("arrays.npz")) as arrays:
        values = {key: arrays[key].copy() for key in arrays.files}
    member = values["subelement_member"].astype(int)
    N, M = values["subelement_N"], values["subelement_M"]
    area, inertia = section["area_m2"], section["inertia_m4"]
    ro, wall = section["r_o_m"], section["wall_m"]
    ri = ro - wall
    qscreen = witness["least_screened_SF"]
    volume = area * lengths
    surface = 2 * math.pi * (ro + ri) * lengths
    inner = 2 * math.pi * ri * lengths
    length_at_segment = lengths[member]
    euler_force = math.pi**2 * E * inertia / length_at_segment**2
    euler_multiplier = euler_force / N

    check(f"{reserve} complete frequency-5 topology",
          count == 750 and geo["nodes"] == 252 and geo["faces"] == 500
          and count == 3 * geo["nodes"] - 6)
    check(f"{reserve} 24 segments per member",
          len(N) == 18000 and len(M) == len(N)
          and np.all(np.bincount(member, minlength=count) == 24))
    check(f"{reserve} compressive inputs", np.all(N > 0))
    close(f"{reserve} section area", math.pi * (ro**2 - ri**2), area)
    close(f"{reserve} section inertia", math.pi * (ro**4 - ri**4) / 4, inertia)
    close(f"{reserve} sample and closure gyration",
          response["section"]["gyration_m"], section["gyration_m"])
    close(f"{reserve} sample ratio A/I",
          inertia / response["section"]["inertia_m4"],
          area / response["section"]["area_m2"])
    close(f"{reserve} total arc length", lengths.sum(), geo["total_arc_m"])
    close(f"{reserve} tube mass", RHO * volume.sum(), witness["mass_kg"]["tube"])
    close(f"{reserve} Euler screen", euler_multiplier.min(), witness["modes"]["euler"])
    close(f"{reserve} axial compression screen", SCALE / (N / area).max(),
          witness["modes"]["compression_axial"])
    close(f"{reserve} unamplified FE-only extreme", (N / area + M * ro / inertia).max(),
          witness["operating_FE_extreme_compression_Pa"])
    close(f"{reserve} joint peak moment", values["joint_M"].max(),
          witness["joint_end_peak_moment_Nm"])
    close(f"{reserve} joint peak torque", values["joint_T"].max(),
          witness["joint_end_peak_torsion_Nm"])
    close(f"{reserve} joint peak axial", values["joint_N"].max(),
          witness["joint_end_peak_compression_N"])
    check(f"{reserve} member force grouping",
          np.allclose(maximum(N, member, count), values["member_max_N"], rtol=1e-11))
    check(f"{reserve} member moment grouping",
          np.allclose(maximum(M, member, count), values["member_max_M"], rtol=1e-11))

    geometry = dict(
        frequency=5, members=count, joints=252, cells=500, end_interfaces=1500,
        ro_m=ro, ri_m=ri, wall_m=wall, area_m2=area, inertia_m4=inertia,
        member_arc_min_m=float(lengths.min()), member_arc_mean_m=float(lengths.mean()),
        member_arc_max_m=float(lengths.max()), total_arc_m=float(lengths.sum()),
        member_volume_min_m3=float(volume.min()), member_volume_mean_m3=float(volume.mean()),
        member_volume_max_m3=float(volume.max()), frame_volume_m3=float(volume.sum()),
        frame_surface_both_m2=float(surface.sum()), frame_inner_surface_m2=float(inner.sum()),
        tube_mass_kg=witness["mass_kg"]["tube"],
        mean_member_volume_over_022d= float(volume.mean() / prior["geometry"]["member_volume_m3"]),
        frame_volume_over_022d=float(volume.sum() / prior["geometry"]["rounded_frame_volume_m3"]),
        frame_surface_over_022d=float(surface.sum() / prior["geometry"]["rounded_frame_surface_both_m2"]),
    )
    cases = []
    for label, q in [("operating", 1.0), ("own_screen", qscreen), ("common_022d_q", q022d)]:
        amplification = 1 / (1 - q / euler_multiplier)
        check(f"{reserve}/{label} pre-Euler projection", np.all(amplification > 0))
        axial = q * N / area
        bending = q * (M + N * length_at_segment / 1000) * ro / inertia * amplification
        extreme = axial + bending
        signed_tension = bending - axial
        peak = maximum(extreme, member, count)
        tension = np.maximum(maximum(signed_tension, member, count), 0)
        bend_max = maximum(bending, member, count)
        axial_max = maximum(axial, member, count)
        least_compression = minimum(axial - bending, member, count)
        critical_bow = inertia / (area * ro) * (1 - q / euler_multiplier) - M / N
        if label == "own_screen":
            close(f"{reserve} source target compression", extreme.max(),
                  witness["required_SiC_extreme_compression_at_screened_limit_Pa"])
            close(f"{reserve} source target positive longitudinal tension", tension.max(),
                  witness["max_tension_at_screened_limit_Pa"])

        ratios = {"whole_member": np.ones(count), "coupon_100cm3": volume / 1e-4,
                  "coupon_1cm3": volume / 1e-6}
        risks, inverse = [], []
        for calibration, size_ratio in ratios.items():
            for m in MODULI:
                item = risk(peak, size_ratio, m)
                item.update(calibration=calibration,
                            uniform_global_peak_frame_Pf=risk(np.full(count, peak.max()), size_ratio, m)["frame_Pf"])
                check(f"{reserve}/{label}/{calibration}/{m} envelope ordering",
                      item["frame_Pf"] <= item["uniform_global_peak_frame_Pf"] + 1e-15)
                risks.append(item)
                for target in TARGETS:
                    req = required(peak, size_ratio, m, target)
                    req_uniform = required(np.full(count, peak.max()), size_ratio, m, target)
                    inverse.append(dict(
                        calibration=calibration, m=m, frame_target=target,
                        required_common_characteristic_Pa=req,
                        factor_over_assumed_3p9GPa=req / SCALE,
                        uniform_global_peak_required_characteristic_Pa=req_uniform,
                        common_scale_assumption=(
                            "Each member has the same complete-member scale despite unequal lengths"
                            if calibration == "whole_member" else "One common coupon reference scale with each member's actual volume"
                        ),
                    ))
        scatter = []
        for calibration, ratio in ratios.items():
            for target in TARGETS:
                scatter.append(dict(
                    calibration=calibration, frame_target=target,
                    required_m_at_assumed_3p9GPa=required_m(peak, ratio, target),
                ))
        case = dict(
            label=label, pressure_multiplier=q,
            screened_capacity_exceeded=bool(q > qscreen + 1e-9),
            stress_model="041 FE moment plus L/1000 bow, both magnified by member Euler denominator",
            max_axial_Pa=float(axial.max()), max_bending_Pa=float(bending.max()),
            min_member_peak_compression_Pa=float(peak.min()), max_compression_Pa=float(peak.max()),
            min_section_longitudinal_compression_Pa=float(least_compression.min()),
            max_positive_longitudinal_tension_Pa=float(tension.max()),
            minimum_initial_bow_to_longitudinal_tension_m=float(critical_bow.min()),
            compression_hypotheses=risks, required_characteristics=inverse, required_scatter=scatter,
            actual_frame_failure_probability=None,
        )
        cases.append(case)
        csv_name = f"MEMBERS-f5-{reserve}-{label}.csv"
        rows = []
        h_whole = (peak / SCALE)**10
        h_coupon = volume / 1e-6 * h_whole
        for i in range(count):
            rows.append(dict(
                tag=TAG, reserve=reserve, load_case=label, member=i,
                q=q, arc_length_m=float(lengths[i]), volume_m3=float(volume[i]),
                surface_both_m2=float(surface[i]), peak_compression_Pa=float(peak[i]),
                peak_axial_Pa=float(axial_max[i]), peak_bending_Pa=float(bend_max[i]),
                minimum_longitudinal_compression_Pa=float(least_compression[i]),
                positive_longitudinal_tension_Pa=float(tension[i]),
                hypothesis_m10_whole_member_3p9GPa_Pf=float(pf(h_whole[i])),
                hypothesis_m10_coupon_1cm3_3p9GPa_Pf=float(pf(h_coupon[i])),
            ))
        with (ROOT / csv_name).open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        for calibration in ["whole_member", "coupon_1cm3"]:
            hypothesis = next(row for row in risks if row["m"] == 10 and row["calibration"] == calibration)
            all_comparison_rows.append(dict(
                point=f"041-f5-{reserve}", load=label, q=q, members=count,
                peak_compression_Pa=float(peak.max()),
                stress_envelope="each member's own peak", **hypothesis,
            ))

    tensile = []
    for model in tensile_models:
        sizes = {"volume": volume, "both_surfaces": surface, "inner_surface": inner}
        reference_ratio = sizes[model["population"]] / model["reference"]
        for fraction in [1, .01, .0001]:
            weights = reference_ratio * fraction
            caps = {
                str(target): model["scale"] * (-math.log1p(-target) / weights.sum())**(1 / model["m"])
                for target in TARGETS
            }
            for target in TARGETS:
                close(f"{reserve} tensile cap inverse",
                      risk(np.full(count, caps[str(target)]), weights, model["m"], model["scale"])["frame_Pf"],
                      target, rtol=2e-10, atol=1e-18)
            scenarios = []
            for stress in [0., 10e6, 25e6, 50e6, 100e6]:
                scenarios.append(dict(stress_Pa=stress,
                    **risk(np.full(count, stress), weights, model["m"], model["scale"])))
            tensile.append(dict(
                **model, stressed_fraction=fraction, frame_effective_size=float(sizes[model["population"]].sum()*fraction),
                positive_tension_caps_Pa=caps, scenarios=scenarios,
                interpretation="Uniform positive tension over an assumed effective fraction; not a measured contact field",
            ))
    allocation = [
        dict(frame_target=p, independent_member_Pf=-math.expm1(math.log1p(-p) / count),
             union_bound_member_Pf=p/count) for p in TARGETS
    ]
    points.append(dict(
        name=f"041-f5-{reserve}", reserve=reserve, tag=TAG, geometry=geometry,
        source_sample=witness["source_sample"], source_screened_multiplier=qscreen,
        source_local_peak_sensitivity=witness["local_max_compression_sensitivity_SF"],
        source_qualification="Projected axial-local/global-k0.2 screens, not certified reliability or capacity",
        force_source="Pinned owner's FE force arrays; independently postprocessed, no independent FE equilibrium solve",
        sample_reference_area_m2=response["section"]["area_m2"],
        force_transfer_to_final_area="A and I scaled together at fixed gyration; owner scaling identity retained",
        joint_actual_end_demands=dict(
            peak_N_at_operating=float(values["joint_N"].max()),
            peak_M_at_operating=float(values["joint_M"].max()),
            peak_T_at_operating=float(values["joint_T"].max()),
            mass_kg=witness["mass_kg"]["joint"],
            scalar_joint_reserve_above_screen=0,
            resolved_contact_and_rotational_reliability=False,
        ),
        load_cases=cases, tensile_hypotheses=tensile, allocations=allocation,
        proof_example=dict(
            factor_over_source_screen=1.25,
            q=1.25*qscreen,
            peak_joint_axial_force_N=1.25*qscreen*float(values["joint_N"].max()),
            exceeds_source_screen=True, ready_protocol=False,
        ),
        actual_member_failure_probabilities=None, actual_frame_failure_probability=None,
        qualified_compressive_strength_Pa=None, lifetime_failure_probability=None,
    ))

# Freeze the previous 022d values verbatim in the comparison; don't replace its stress model.
for case in ["operating_source_bow", "target_source_bow"]:
    for row in prior["compression_hypotheses"]:
        if row["case"] == case and row["m"] == 10 and row["basis"] == "assumed_scale_3.9GPa" and row["calibration"] in ["whole_member", "coupon_1cm3"]:
            all_comparison_rows.append(dict(
                point="022d-selected", load=case,
                q=1 if case.startswith("operating") else q022d,
                members=433, peak_compression_Pa=row["stress_Pa"],
                calibration=row["calibration"], stress_envelope="identical member peak; frozen 043",
                m=10, frame_Pf=row["frame_Pf"], member_Pf_min=row["member_Pf"],
                member_Pf_max=row["member_Pf"],
            ))

[withheld: private task or principal quotation; scientific result/status retained elsewhere]