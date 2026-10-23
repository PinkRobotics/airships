"""Independent MAINLINE-035 arithmetic.

Source inputs transcribed from the primary documents listed in EVIDENCE.md.
The owner's executable is neither read nor imported. Owner JSON is opened only
after our results have been calculated, to make a field-by-field comparison.
All values are QUESTIONABLE; transfers are PROJECTIONS, not design allowables.
"""
from pathlib import Path
import json
import math
import numpy as np

ROOT = Path(__file__).resolve().parent


def save(name, data):
    (ROOT / name).write_text(json.dumps(data, indent=2, allow_nan=False) + "\n")


def laminate(E1, E2, nu12, G12, angles, ply):
    """Assemble A/B/D by transforming strain and stress tensors for unit strains."""
    nu21 = nu12 * E2 / E1
    Q = np.array([[E1, nu12 * E2, 0],
                  [nu12 * E2, E2, 0],
                  [0, 0, G12 * (1 - nu12 * nu21)]]) / (1 - nu12 * nu21)
    thickness = ply * len(angles)
    A, B, D = (np.zeros((3, 3)) for _ in range(3))
    for k, angle in enumerate(angles):
        theta = math.radians(angle)
        c, s = math.cos(theta), math.sin(theta)
        rotation = np.array([[c, s], [-s, c]])
        columns = []
        for strain in (np.array([[1., 0], [0, 0]]),
                       np.array([[0., 0], [0, 1]]),
                       np.array([[0., .5], [.5, 0]])):
            local = rotation @ strain @ rotation.T
            stress = Q @ [local[0, 0], local[1, 1], 2 * local[0, 1]]
            global_stress = rotation.T @ np.array(
                [[stress[0], stress[2]], [stress[2], stress[1]]]) @ rotation
            columns.append([global_stress[0, 0], global_stress[1, 1],
                            global_stress[0, 1]])
        transformed = np.array(columns).T
        z0 = -thickness / 2 + k * ply
        z1 = z0 + ply
        A += transformed * (z1 - z0)
        B += transformed * (z1**2 - z0**2) / 2
        D += transformed * (z1**3 - z0**3) / 3
    compliance = np.linalg.inv(A)
    ex, ey, gxy = [1 / (compliance[i, i] * thickness) for i in range(3)]
    nuxy = -compliance[1, 0] / compliance[0, 0]
    nuyx = -compliance[0, 1] / compliance[1, 1]
    assert np.allclose(A, A.T)
    assert np.linalg.eigvalsh(A).min() > 0
    assert abs(nuxy / ex - nuyx / ey) < 1e-18
    assert np.max(np.abs(B)) < 1e-8
    return dict(t_in=thickness, Ex_psi=ex, Ey_psi=ey, nuxy=nuxy,
                nuyx=nuyx, Gxy_psi=gxy), dict(A=A.tolist(), B=B.tolist(), D=D.tolist())


def cylinder(rt):
    # SP-8007 (1968), Eq. 5: coefficient 0.901, not the later 0.902 convention.
    return 1 - .901 * (1 - math.exp(-math.sqrt(rt) / 16))


def sphere(rt, nu=.3, phi=math.pi / 2):
    # SP-8032 Eqs. 3 and 4; phi is cap half-angle. Here phi=90 deg.
    lam2 = math.sqrt(12 * (1 - nu**2)) * rt * (2 * math.sin(phi / 2))**2
    return .14 + 3.2 / lam2


def eye_curve(rr):
    # Reproduce the CARD's stated three-node log interpolation, then compare
    # separately with CR-1457's available analytic 0.75*SP-8007 relationship.
    x = math.log10(rr)
    return float(np.interp(x, [1, 2, 3], [.68, .55, .31]))


def vc(ef, nu, tf, tc, r, gc):
    return 2 * ef * tf * tc / (r * math.sqrt(1 - nu**2) * (tc + tf) * gc)


def sbkf(name, angles, ply, tc, g13, g23, gamma, material):
    lam, abd = laminate(*material, angles, ply)
    tf, h, r = lam["t_in"], tc + lam["t_in"], 48.
    ex, ey = lam["Ex_psi"], lam["Ey_psi"]
    nuxy, nuyx = lam["nuxy"], lam["nuyx"]
    ef, nu = math.sqrt(ex * ey), math.sqrt(nuxy * nuyx)
    vi = vc(ef, nu, tf, tc, r, math.sqrt(g13 * g23))
    va = vc(ex, nuxy, tf, tc, r, g13)
    vs = vc(ef, nu, tf, tc, r, g23)
    rr, rt = 2 * r / h, r / (math.sqrt(3) * h)
    sp, cr = cylinder(rt), eye_curve(rr)
    out = dict(id=name, laminate=lam, h_in=h, Vc_iso=vi, Vc_axial=va,
               Vc_soft=vs, Vc_range=[va, vs], R_over_rho=rr, R_over_teq=rt,
               SP8007_at_teq=sp, beat_SP8007=gamma / sp,
               CR1457_cyl_curve=cr, beat_CR1457_curve=gamma / cr)
    extra = dict(id=name, source_lamina_psi=list(material), ply_in=ply,
                 tc_in=tc, R_in=r, G13_psi=g13, G23_psi=g23, gamma_input=gamma,
                 angles=angles, matrices=abd,
                 Vc_axial_reciprocal_nu=vc(ex, nu, tf, tc, r, g13),
                 R_over_rho_finite_homogeneous_faces=r / math.sqrt(h*h/4 + tf*tf/12),
                 R_over_rho_CLT_x=r / math.sqrt(h*h/4 + abd["D"][0][0]/abd["A"][0][0]),
                 R_over_rho_CLT_y=r / math.sqrt(h*h/4 + abd["D"][1][1]/abd["A"][1][1]),
                 CR1457_exact=.75*sp, beat_CR1457_exact=gamma/(.75*sp))
    return out, extra


def transform(corners):
    a, b = [], []
    for (x, y), (u, v) in corners:
        a.extend([[x, y, 1, 0, 0, 0, -u*x, -u*y],
                  [0, 0, 0, x, y, 1, -v*x, -v*y]])
        b.extend([u, v])
    return np.r_[np.linalg.solve(a, b), 1].reshape(3, 3)


def digitize(H, point):
    v = H @ [*point, 1]
    return (v[:2] / v[2]).tolist()


def flatten(value, prefix=""):
    if isinstance(value, dict):
        for k, v in value.items():
            yield from flatten(v, f"{prefix}/{k}")
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from flatten(v, f"{prefix}/{i}")
    elif isinstance(value, (int, float)):
        yield prefix, value


def main():
    im7generic = (20e6, 1.25e6, .36, .77e6)
    im7design = (20.4e6, 1.33e6, .345, .77e6)
    definitions = [
        ("CTA8.1", [45, -45, 0, 90, 0, -45, 45], .0052, .25, 29500., 12000., .87, im7generic),
        ("CTA8.2", [60, -60, 0, 0, -60, 60], .00694, .2, 45000., 20000., .775, im7design),
        ("CTA8.2B", [60, -60, 0, 0, -60, 60], .00694, .2, 45000., 20000., .721, im7design),
        ("CTA8.3", [30, -30, 90, 90, -30, 30], .0054, .2, 45000., 20000., .864, im7design),
    ]
    nominal, expanded = [], []
    for item in definitions:
        row, extra = sbkf(*item)
        nominal.append(row)
        expanded.append(extra)
    # Independent tensor-rotation checks for the quasi-isotropic laminates.
    for row in nominal[1:]:
        l = row["laminate"]
        assert math.isclose(l["Ex_psi"], l["Ey_psi"], rel_tol=1e-12)
        assert math.isclose(l["Gxy_psi"], l["Ex_psi"]/(2*(1+l["nuxy"])), rel_tol=1e-12)
    multipliers = [nominal[i]["beat_SP8007"] for i in [0, 2, 3]]
    lo, hi = min(multipliers), max(multipliers)
    leads = []
    for name, h, need, Vc in [("021 rev1", .0210568, .59532, 1.06106),
                              ("021b", .03081, .46823, .886182)]:
        rr, rt = 20 / h, 10 / (math.sqrt(3) * h)
        cyl, sph = cylinder(rt), sphere(rt)
        old = .49 + (.42 - .49) * math.log(rr / 410) / math.log(1050 / 410)
        leads.append(dict(id=name, R_over_rho=rr, R_over_teq=rt, SP8007_cyl=cyl,
                          SP8032_sphere=sph, CR1457_cyl_curve=eye_curve(rr),
                          CR1457_hemisphere_design=.2,
                          old_sandwich_cylinders_interpolated=old,
                          need_over_old_cylinders=need / old,
                          transfer=dict(direct_cylinder_record=[.721, .87],
                              sbkf_beat_on_SP8007_at_lead_cylinder=[lo*cyl, hi*cyl],
                              sbkf_beat_on_SP8032_at_lead_sphere=[lo*sph, hi*sph],
                              measured_sandwich_hemisphere_SII=[.22, .24]),
                          need_over_SII_hemisphere=[need/.24, need/.22],
                          need_over_sphere_transfer=[need/(hi*sph), need/(lo*sph)]))
    reproduction = dict(sbkf=nominal, leads=leads)
    save("REPRODUCED.json", reproduction)

    # Figure 6.2-3: four native-pixel corners, projective transformation.
    corners = [((384, 1494), (0, 0)), ((1361, 1473), (500, 0)),
               ((358, 517), (0, 1)), ((1335, 491), (500, 1))]
    H = transform(corners)
    points = [
        ("hemisphere_low", (848, 1279), 240, .22),
        ("hemisphere_high", (847, 1267), 240, .24),
        ("ellipsoid_room_low_left", (843, 1113), 240, .39),
        ("ellipsoid_room_high_left", (859, 925), 240, .58),
        ("ellipsoid_thermal_low", (862, 1092), 245, .41),
        ("ellipsoid_thermal_high", (857, 896), 245, .61),
        ("ellipsoid_room_low_right", (1311, 1031), 480, .46),
        ("ellipsoid_room_high_right", (1297, 520), 480, .99)]
    read = []
    for label, pixel, owner_r, owner_g in points:
        rr, g = digitize(H, pixel)
        read.append(dict(id=label, pixel=list(pixel), R_over_rho=rr, gamma=g,
                         owner_R_over_rho=owner_r, owner_gamma=owner_g,
                         gamma_delta=g-owner_g, R_over_rho_delta=rr-owner_r,
                         read_uncertainty_gamma=.01, read_uncertainty_R_over_rho=5))
    # Check transform also reproduces interior grid crossings, not just corners.
    grid_checks = []
    for pixel, expected in [((960, 1091), (300, .4)),
                            ((768, 1291), (200, .2)),
                            ((564, 902), (100, .6))]:
        rr, g = digitize(H, pixel)
        grid_checks.append(dict(pixel=list(pixel), expected=list(expected), got=[rr, g]))
        assert abs(rr-expected[0]) < 3 and abs(g-expected[1]) < .005
    save("DIGITIZATION.json", dict(source="sources/cr1457-p355.png",
                                   image_pixels=[1849, 2400], corners=corners,
                                   homography=H.tolist(), points=read,
                                   grid_checks=grid_checks,
                                   note="Pixel precision is audit information; report rounded graph reads, not specimen precision."))
    # Fig. 4.2-3 uses a logarithmic x axis. Eleven cylinder points are stated
    # explicitly in the text on p. 4-9; the CARD lists only ten.
    cyl_corners = [((464,1497),(1,0)), ((1441,1494),(3,0)),
                   ((462,523),(1,1)), ((1440,521),(3,1))]
    HC = transform(cyl_corners)
    cyl_pixels = [
        ("FPL1830_low",(1451,1090)), ("FPL1830_high",(1491,1068)),
        ("Baker_omitted",(992,903)), ("Baker_180",(1071,969)),
        ("Baker_270_high",(1155,823)), ("Baker_270_mid",(1153,931)),
        ("Baker_270_low",(1153,941)), ("Baker_410",(1250,1019)),
        ("PE227_high",(965,756)), ("PE227_mid",(965,883)),
        ("PE227_low",(965,906))]
    cyl_reads = []
    for name, pixel in cyl_pixels:
        logrr, g = digitize(HC, pixel)
        cyl_reads.append(dict(id=name, pixel=list(pixel), R_over_rho=10**logrr,
                              gamma=g, read_uncertainty_gamma=.01,
                              read_uncertainty_R_relative=.05))
    cone_reads = []
    for name, pixel in [("Baker_cone_low", (1088,999)), ("Baker_cone_high", (1088,939))]:
        logrr, g = digitize(HC, pixel)
        cone_reads.append(dict(id=name, pixel=list(pixel), R_over_rho=10**logrr,
                               gamma=g, read_uncertainty_gamma=.01,
                               read_uncertainty_R_relative=.05))
    save("DIGITIZATION-CYLINDERS.json", dict(source="sources/cr1457-p188.png",
         corners=cyl_corners, homography=HC.tolist(), points=cyl_reads,
         count=11, cones=cone_reads,
         note="Eleven cylinders; the two separately recorded cones are excluded from cylinder interpolation."))
    cyl_by_id = {p["id"]: p for p in cyl_reads}
    baker, fpl = cyl_by_id["Baker_410"], cyl_by_id["FPL1830_low"]
    for l, need in zip(leads, [.59532, .46823]):
        old_revised = baker["gamma"] + (fpl["gamma"]-baker["gamma"]) * (
            math.log(l["R_over_rho"]/baker["R_over_rho"]) /
            math.log(fpl["R_over_rho"]/baker["R_over_rho"]))
        expanded.append(dict(id=l["id"], sphere_to_cylinder=l["SP8032_sphere"]/l["SP8007_cyl"],
                             sphere_nu033=sphere(l["R_over_teq"], nu=.33),
                             full_sphere_angle_extrapolation=sphere(l["R_over_teq"], phi=math.pi),
                             CR1457_exact=.75*l["SP8007_cyl"],
                             revised_need_over_SII_center=[need/read[1]["gamma"], need/read[0]["gamma"]],
                             revised_need_over_SII_read_envelope=[need/(read[1]["gamma"]+.01),
                                                                 need/(read[0]["gamma"]-.01)],
                             revised_old_cylinder_interpolation=old_revised,
                             revised_need_over_old_cylinders=need/old_revised,
                             old_interpolation_input_uncertainty_gamma=.01,
                             all_transfers_are_projections=True))
    sensitivity = []
    # Geometry/material variations already reported in the CTA8.1 primary source.
    for name, ply, props in [
        ("CTA8.1_assumed_E_measured_ply", .005679, im7generic),
        ("CTA8.1_pretest_fitted_E_nominal_ply", .0052, (21.7434e6, 1.35896e6, .36, .77e6)),
        ("CTA8.1_posttest_zero_strain_E_measured_ply", .005679, (20.662e6, 1.25e6, .36, .77e6))]:
        a, e = sbkf(name, definitions[0][1], ply, .25, 29500., 12000., .87, props)
        sensitivity.append(a)
    save("SOURCE-CORRECTIONS.json", dict(rows=expanded, CTA81_sensitivity=sensitivity))

    # Only now read owner numeric output. This does not invoke the owner code.
    owner = json.loads((ROOT / "intake/owner/RESULTS-ANALYSIS.json").read_text())
    ov = dict(flatten(owner))
    comparisons = []
    for field, checked in flatten(reproduction):
        claimed = ov[field]
        comparisons.append(dict(field=field, card_value=claimed, checker_value=checked,
                                delta=checked-claimed,
                                pass_same_convention=math.isclose(checked, claimed, rel_tol=1e-11, abs_tol=1e-12)))
    assert all(r["pass_same_convention"] for r in comparisons)
    save("NUMERIC-COMPARISON.json", dict(count=len(comparisons), comparisons=comparisons,
         note="Pass means same arithmetic conventions only. Source and inference fixes are separate."))

    fair_test = [73213, 70907, 69172, 73468, 64848]
    auxiliary = dict(
        fairing_eigenvalue_overprediction_percent=[
            [100*(a/t-1) for a,t in zip(pred, fair_test)]
            for pred in [[80912,74245,75248,82318,80283],[79471,72928,72884,82319,79471]]],
        d7935_test_over_prediction=[
            [t/p for t,p in zip([38.13,30.27,21.24],pred)]
            for pred in [[50.06,37.99,26.20],[53.78,39.85,27.79]]],
        muc_test_over_eigenvalue=1/1.0849,
        cta82_test_over_linear=708095/913912,
        cta82b_test_over_combined_linear=704880/977283,
        cta83_test_over_combined_linear=432000/499246,
        cta83_source_stated_ratio=.864,
        cta83_ratio_using_stated_loads_beat_SP8007=(432000/499246)/nominal[3]["SP8007_at_teq"],
        cta83_posttest_tare_error_percent=100*(431600/432000-1),
        cta81_test_over_pretest_nonlinear=856900/864600,
        cta81_posttest_nonlinear_error_percent=100*(845000/856900-1),
        yang_test_over_real_geometry_linear=12.44/91.09,
        yang_test_over_real_geometry_nonlinear=12.44/11.87,
        yang_nonlinear_error_on_test_percent=100*(11.87/12.44-1),
        optimistic_gamma_021=.20+.40*1.06106,
        optimistic_gamma_021b=.20+.40*.886182,
        need_over_optimistic_021=.59532/(.20+.40*1.06106),
        nominal_sbkf_optimistic_gamma=[.2+.4*nominal[i]["Vc_iso"] for i in [0,2,3]],
        kazimi_test_over_theory=[17/30.5,27/30.5],
        fpl_lateral_pressure_test_over_theory=[
            t/p for t,p in zip([60,52.5,52.5,52.5,52.5],[55.2,45.2,52.6,45.2,47.6])],
        fpl_lateral_pressure_midpoint_note=(
            "CR-1457 uses 52.5 psi for specimens 2–5 as the midpoint of reported 50–55 psi onset, "
            "not four independently resolved failure pressures."),
    )
    save("AUXILIARY.json", auxiliary)
    inputs_verified = []
    for name, path, locator in [
        ("021 rev1", "021-RESULTS.json", ["main", "floating_point"]),
        ("021b", "021b-RESULTS.json", ["floating_point"])]:
        source = json.loads((ROOT / "intake/lead-points" / path).read_text())
        fp = source
        for key in locator:
            fp = fp[key]
        r, tf, tc, g = (fp[k] for k in ["R_m", "tf_m", "core_m", "core_Gc_Pa"])
        E, nu, p = 290e9, .33, 95460.83791390515
        h = tf + tc
        value = vc(E, nu, tf, tc, r, g)
        kc = 1 - value / 4
        perfect_pressure = 4*E*tf*h / (r*r*math.sqrt(1-nu*nu))
        need = p / (perfect_pressure*kc)
        assert math.isclose(value, fp["Vc"], rel_tol=1e-12)
        assert math.isclose(need, fp["needed_values"]["gamma"], rel_tol=1e-12)
        inputs_verified.append(dict(id=name, tf_m=tf, tc_m=tc, E_Pa=E,
                                    nu=nu, Gc_Pa=g, p_Pa=p, R_m=r,
                                    h_m=h, Vc=value, Kc=kc,
                                    perfect_pressure_Pa=perfect_pressure,
                                    gamma_needed=need, R_over_rho=2*r/h,
                                    R_over_teq=r/(math.sqrt(3)*h),
                                    passed=True))
    save("LEAD-INPUT-CHECK.json", inputs_verified)
    print(json.dumps(dict(numeric_comparisons=len(comparisons), all_same_convention_pass=True,
                          hemisphere_gamma=[x["gamma"] for x in read[:2]],
                          sphere_cylinder_ratio=[r["sphere_to_cylinder"] for r in expanded[-2:]])))


if __name__ == "__main__":
    main()
