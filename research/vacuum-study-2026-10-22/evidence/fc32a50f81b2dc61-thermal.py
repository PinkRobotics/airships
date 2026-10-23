#!/usr/bin/env python3
"""Independent vector implementation of 037's thermal equations."""
import json
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss, Legendre

B = Path(__file__).resolve().parent
SIG = 5.670374419e-8
TA = 284.9
RHO = 1.1672683307461802
K = 130*16.018463373960138/2700
ALPHA = 11.3e-6


def zones(radius, tc, solar, sky, n=64, midpoint=False, fixed_iterations=None, solid_density=2700):
    tc = np.atleast_1d(tc).astype(float)
    if midpoint:
        mu = -1+(np.arange(n)+.5)*2/n
        weights = np.full(n, 2/n)
    else:
        mu, weights = leggauss(n)
    hforced = (2+(.4*np.sqrt(RHO*2*2*radius/1.79e-5)
                  + .06*(RHO*2*2*radius/1.79e-5)**(2/3))*.71**.4)*.0257/(2*radius)
    ti = np.full((len(tc), n), TA)
    env4 = .5*(1+mu)*sky**4+.5*(1-mu)*TA**4
    absorbed = .2*solar*np.maximum(mu, 0)
    error = np.inf
    limit = fixed_iterations or 500
    for iteration in range(limit):
        mean4 = (ti**4 @ weights/2)[:, None]
        mean = (ti @ weights/2)[:, None]
        u = (130*16.018463373960138/solid_density)/tc[:, None]+.2*4*SIG*mean**3
        candidate = ti.copy()
        for _ in range(12):
            qi = .2*SIG*(candidate**4-mean4)
            dqi = .8*SIG*candidate**3
            to = candidate+qi/u
            dto = 1+dqi/u
            dt = to-TA
            hn = 1.32*np.maximum(np.abs(dt), .05)**.25
            h = np.maximum(hforced, hn)
            dhdt = np.where((hn > hforced) & (np.abs(dt) > .05), h*.25, 0)
            residual = .9*SIG*(to**4-env4)+h*dt+qi-absorbed
            derivative = (3.6*SIG*to**3+h+dhdt)*dto+dqi
            change = residual/derivative
            candidate -= change
            if np.max(np.abs(change)) < 1e-10:
                break
        error = float(np.max(np.abs(candidate-ti)))
        ti = candidate
        if fixed_iterations is None and error < 2e-9:
            break
    else:
        if fixed_iterations is None:
            raise ArithmeticError(f"Thermal fixed point not converged: {error}")
    mean4 = (ti**4 @ weights/2)[:, None]
    mean = (ti @ weights/2)[:, None]
    u = (130*16.018463373960138/solid_density)/tc[:, None]+.2*4*SIG*mean**3
    to = ti+.2*SIG*(ti**4-mean4)/u
    residual = .9*SIG*(to**4-env4)+np.maximum(hforced, 1.32*np.maximum(abs(to-TA), .05)**.25)*(to-TA)+.2*SIG*(ti**4-mean4)-absorbed
    return mu, weights, to, ti, dict(iterations=iteration+1, fixed_point_error_K=error,
                                    max_energy_residual_W_m2=float(np.max(abs(residual))))


def evaluate(radius, tc, n=64, midpoint=False, fixed_iterations=None, legacy_project=False,solid_density=2700):
    mu, w, out, inside, diag = zones(radius, tc, 970, 275, n, midpoint, fixed_iterations,solid_density)
    _, _, night, _, diagn = zones(radius, tc, 0, 260, n, midpoint, fixed_iterations,solid_density)
    temp = (out+inside)/2
    # Removing the mean before quadrature prevents a constant temperature from
    # acquiring spurious degree 2..6 curvature in a midpoint integration.
    residual = temp if legacy_project else temp-(temp@w/2)[:, None]
    coeffs = np.stack([(2*j+1)/2*(residual*Legendre.basis(j)(mu))@w for j in range(2, 7)], axis=1)
    angles = np.linspace(0, np.pi, 1441)
    x = np.cos(angles)
    second = np.stack([(1-x*x)*Legendre.basis(j).deriv(2)(x)-x*Legendre.basis(j).deriv()(x)
                       for j in range(2, 7)])
    ktemp = np.max(np.abs(coeffs@second), axis=1)
    return dict(tc_m=np.atleast_1d(tc).tolist(),
                gradient_K=np.max(np.abs(out-inside), axis=1).tolist(),
                swing_K=(np.max(out, axis=1)-np.min(night, axis=1)).tolist(),
                rise_K=(np.max(out, axis=1)-TA).tolist(),
                curvature_temperature_K=ktemp.tolist(),
                max_outer_K=np.max(out, axis=1).tolist(),
                min_outer_K=np.min(night, axis=1).tolist(),
                day_diagnostics=diag, night_diagnostics=diagn)


if __name__ == "__main__":
    table = {}
    for r in [10, 12, 15, 20, 30]:
        tc = np.geomspace(.001*r/10, 1.5*r/10, 241)
        table[str(r)] = evaluate(r, tc, n=128)
    base_tc = .022106790073532958
    checks = dict(source_037_midpoint_25=evaluate(10, [base_tc], n=37, midpoint=True,
                                                fixed_iterations=25, legacy_project=True,solid_density=2640),
                  converged_64=evaluate(10, [base_tc], n=64,solid_density=2640),
                  converged_128=evaluate(10, [base_tc], n=128,solid_density=2640),
                  common_2700_128=evaluate(10,[base_tc],n=128))
    (B/"THERMAL-TABLE.json").write_text(json.dumps(table, indent=2)+"\n")
    (B/"THERMAL-CHECK.json").write_text(json.dumps(checks, indent=2)+"\n")
    print(json.dumps(checks, indent=2))
