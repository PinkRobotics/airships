"""MAINLINE-043. All outputs QUESTIONABLE/PROJECTION, never qualification.

No FE equilibrium is solved here. Recover forces from this seat's pinned 026b
displacements, then evaluate explicit stress/Weibull hypotheses. Run by simjob.
"""
from pathlib import Path
import csv
import json
import math
import numpy as np

ROOT = Path(__file__).resolve().parent
E = 410e9
NU = .14
CHECKS = []


def save(name, data):
    (ROOT / name).write_text(json.dumps(data, indent=2, allow_nan=False) + "\n")


def check(name, got, expected, rtol=2e-8, atol=1e-7):
    error = abs(got - expected)
    passed = error <= atol + rtol * abs(expected)
    CHECKS.append(dict(name=name, got=float(got), expected=float(expected),
                       error=float(error), passed=bool(passed)))
    if not passed:
        raise AssertionError(CHECKS[-1])


def prob(hazard):
    return -math.expm1(-hazard)


def scale(mean, modulus):
    return mean / math.gamma(1 + 1 / modulus)


def risk(stress, characteristic, modulus, size_ratio=1., count=433):
    h = size_ratio * (stress / characteristic) ** modulus
    return dict(member_hazard=h, member_Pf=prob(h),
                frame_hazard=count*h, frame_Pf=prob(count*h))


def need(stress, modulus, target, count=433, size_ratio=1.):
    return stress * (count * size_ratio / -math.log1p(-target)) ** (1 / modulus)


def needed_m(stress, characteristic, target, count=433, size_ratio=1.):
    if characteristic <= stress:
        return None
    return math.log(count*size_ratio / -math.log1p(-target)) / math.log(characteristic/stress)


def beam_members(label, ro, wall):
    """Recover axial, bending, transverse shear and torque without matrix assembly."""
    root = ROOT / "intake/own026b/runs" / label
    data = np.load(root / "STATIC.npz")
    xyz, chains, u = data["points"], data["chains"], data["u"].reshape(-1, 6)
    elem = np.column_stack([chains[:, :-1].ravel(), chains[:, 1:].ravel()])
    delta = xyz[elem[:, 1]] - xyz[elem[:, 0]]
    lengths = np.linalg.norm(delta, axis=1)
    ex = delta/lengths[:, None]
    axes = np.eye(3)[np.argmin(np.abs(ex), axis=1)]
    ez = np.cross(ex, axes)
    ez /= np.linalg.norm(ez, axis=1)[:, None]
    ey = np.cross(ez, ex)
    rot = np.stack([ex, ey, ez], axis=1)
    a = np.einsum("eij,ej->ei", rot, u[elem[:, 0], :3])
    b = np.einsum("eij,ej->ei", rot, u[elem[:, 1], :3])
    ra = np.einsum("eij,ej->ei", rot, u[elem[:, 0], 3:])
    rb = np.einsum("eij,ej->ei", rot, u[elem[:, 1], 3:])
    ri = ro-wall
    area = math.pi*(ro*ro-ri*ri)
    inertia = math.pi*(ro**4-ri**4)/4
    axial_N = E*area/lengths*(a[:, 0]-b[:, 0])
    torque = E*inertia/(1+NU)/lengths*(ra[:, 0]-rb[:, 0])
    dv, dw = a[:, 1]-b[:, 1], a[:, 2]-b[:, 2]
    vy = 12*E*inertia/lengths**3*dv + 6*E*inertia/lengths**2*(ra[:, 2]+rb[:, 2])
    vz = 12*E*inertia/lengths**3*dw - 6*E*inertia/lengths**2*(ra[:, 1]+rb[:, 1])
    mya = -6*E*inertia/lengths**2*dw + E*inertia/lengths*(4*ra[:, 1]+2*rb[:, 1])
    myb = -6*E*inertia/lengths**2*dw + E*inertia/lengths*(2*ra[:, 1]+4*rb[:, 1])
    mza = 6*E*inertia/lengths**2*dv + E*inertia/lengths*(4*ra[:, 2]+2*rb[:, 2])
    mzb = 6*E*inertia/lengths**2*dv + E*inertia/lengths*(2*ra[:, 2]+4*rb[:, 2])
    moments = np.stack([np.hypot(mya, mza), np.hypot(myb, mzb)], axis=1)
    axial = axial_N/area
    bend = moments*ro/inertia
    comp = axial[:, None]+bend
    tension_signed = bend-axial[:, None]
    shear = np.hypot(vy, vz)
    # Thin circular tube beam shear estimate. Sum separate maxima conservatively;
    # no stress concentration, contact, membrane attachment or shell shear included.
    tau = 2*shear/area + np.abs(torque)*ro/(2*inertia)
    least_c = axial-bend.max(axis=1)
    positive_principal_cap = tau*tau/(np.hypot(least_c/2, tau)+least_c/2)
    assert np.all(least_c > 0)
    n, m = chains.shape[0], chains.shape[1]-1
    lengths2 = lengths.reshape(n, m)
    mean_N = (axial_N.reshape(n, m)*lengths2).sum(axis=1)/lengths2.sum(axis=1)
    main_xyz = xyz[chains[:, [0, -1]]]
    arc = 10*np.arccos(np.clip(np.einsum("ij,ij->i", main_xyz[:, 0], main_xyz[:, 1])/100, -1, 1))
    peak = lambda arr: arr.reshape(n, -1).max(axis=1)
    rows = []
    for i in range(n):
        rows.append(dict(member=i, node_a=int(chains[i, 0]), node_b=int(chains[i, -1]),
                         arc_length_m=float(arc[i]), volume_m3=float(area*arc[i]),
                         mean_compression_N=float(mean_N[i]),
                         peak_axial_compression_Pa=float(peak(axial)[i]),
                         peak_bending_stress_Pa=float(peak(bend)[i]),
                         peak_compression_fiber_Pa=float(peak(comp)[i]),
                         max_signed_axial_tension_Pa=float(peak(tension_signed)[i]),
                         max_positive_axial_tension_Pa=max(0., float(peak(tension_signed)[i])),
                         peak_bending_moment_Nm=float(peak(moments)[i]),
                         joint_end_bending_moment_Nm=float(max(moments.reshape(n,m,2)[i,0,0],
                                                               moments.reshape(n,m,2)[i,-1,1])),
                         peak_shear_N=float(peak(shear)[i]),
                         peak_torque_Nm=float(peak(np.abs(torque))[i]),
                         beam_shear_stress_estimate_Pa=float(peak(tau)[i]),
                         positive_principal_tension_cap_Pa=float(peak(positive_principal_cap)[i])))
    for row in rows:
        for mult, suffix in [(1., "operating"), (1.2582524765581682, "target_q")]:
            demand=mult*row["peak_compression_fiber_Pa"]
            row["hypothesis_m10_whole_member_3p9GPa_Pf_"+suffix]=risk(demand,3.9e9,10)["member_Pf"]
            row["hypothesis_m10_coupon_1cm3_3p9GPa_Pf_"+suffix]=risk(
                demand,3.9e9,10,row["volume_m3"]/1e-6)["member_Pf"]
    prior = json.loads((root/"RESULTS.json").read_text())
    for key, got in [
        ("max_axial_compression_Pa", axial.max()),
        ("max_end_bending_stress_Pa", bend.max()),
        ("max_combined_compressive_fiber_stress_Pa", comp.max()),
        ("max_tensile_fiber_stress_Pa", tension_signed.max()),
        ("max_end_bending_moment_Nm", moments.max())]:
        check(label+"/"+key, got, prior["static"][key])
    check(label+"/mean_force", mean_N.mean(), prior["static"]["member_mean_compression_N"]["mean"])
    with (ROOT/f"MEMBERS-{label}.csv").open("w") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    summary = dict(label=label, count=n, ro_m=ro, wall_m=wall, area_m2=area,
                   inertia_m4=inertia, total_volume_m3=float(area*arc.sum()),
                   mean_arc_m=float(arc.mean()), mean_force_N=float(mean_N.mean()),
                   maxima={key:max(row[key] for row in rows) for key in rows[0] if key not in ("member","node_a","node_b")})
    # Actual per-member nonuniform demands, with uniform peak stress in each tube
    # as an upper-hazard envelope only under the assumed monotone scalar law.
    summary["hypothetical_compression"] = []
    for modulus in [8, 10, 20]:
        for q in [1., 1.2582524765581682]:
            h = np.array([(q*row["peak_compression_fiber_Pa"]/3.9e9)**modulus for row in rows])
            hvol = h*np.array([row["volume_m3"]/1e-6 for row in rows])
            summary["hypothetical_compression"].append(dict(
                m=modulus, q=q, characteristic_Pa=3.9e9,
                whole_member_calibration=dict(frame_hazard=float(h.sum()),frame_Pf=prob(float(h.sum())),
                    min_member_Pf=prob(float(h.min())),max_member_Pf=prob(float(h.max()))),
                coupon_1cm3_calibration=dict(frame_hazard=float(hvol.sum()),frame_Pf=prob(float(hvol.sum())),
                    min_member_Pf=prob(float(hvol.min())),max_member_Pf=prob(float(hvol.max())))))
    return summary


def reference_bend(m, kind="four"):
    # SA manufacturer dimensions, assumed (unpublished for this batch) 40/20 spans.
    if kind == "four":
        b,h,outer,inner = .004,.003,.040,.020
    else:
        # RBSC's documented 30 mm 3-point span and 4 x 3 mm section.
        b,h,outer,inner = .004,.003,.030,0.
    longitudinal = inner+(outer-inner)/(m+1)
    return dict(Vref_m3=b*h*longitudinal/(2*(m+1)),
                Aref_m2=(b+h/(m+1))*longitudinal)


def stress_integral(ro, ri, length, axial, bow, constant_moment_stress, m, sign,
                    nx=128, nt=512, nr=8):
    """Exact-annulus quadrature for longitudinal normal stress, not full multiaxial failure."""
    x,w = np.polynomial.legendre.leggauss(nx)
    z = (x+1)/2
    wx = w/2
    qr,wr = np.polynomial.legendre.leggauss(nr)
    radius = ri+(qr+1)/2*(ro-ri)
    wr = wr/2*(ro-ri)*radius
    theta = 2*math.pi*(np.arange(nt)+.5)/nt
    bending = bow*np.sin(math.pi*z)+constant_moment_stress
    # Stress sign convention: tension positive.
    sigma = -axial+bending[:,None,None]*(radius[None,:,None]/ro)*np.cos(theta)[None,None,:]
    sigma = np.maximum(sign*sigma,0.)
    peak = max(0., sign*(-axial)+(bow+constant_moment_stress))
    if peak == 0:
        return dict(peak_Pa=0., effective_volume_m3=0., effective_area_m2=0.)
    normalized = (sigma/peak)**m
    ve = float(length*2*math.pi/nt*np.einsum("i,j,ijk->", wx,wr,normalized))
    se = 0.
    for rad in [ri,ro]:
        s = np.maximum(sign*(-axial+bending[:,None]*(rad/ro)*np.cos(theta)[None,:]),0.)
        se += length*rad*2*math.pi/nt*float(np.einsum("i,ij->",wx,(s/peak)**m))
    return dict(peak_Pa=peak,effective_volume_m3=ve,effective_area_m2=se)

[withheld: private task or principal quotation; scientific result/status retained elsewhere]


if __name__ == "__main__":
    main()
