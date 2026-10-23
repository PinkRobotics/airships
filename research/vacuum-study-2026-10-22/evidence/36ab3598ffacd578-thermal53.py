"""MAINLINE-053: newly assembled two-face energy balances.

Upstream programs are inspected as specifications, never imported/executed.
Solve local face temperatures and two global cavity moments simultaneously.
"""
from pathlib import Path
from dataclasses import dataclass, asdict
import json
import numpy as np
from numpy.polynomial import legendre as L

ROOT = Path(__file__).resolve().parent
SIGMA = 5.670374419e-8
TA = 284.9
RHO_AIR = 1.1672683307461802
RHO_CORE = 16.018463373960138
EPS_IN = .20
TC_REFERENCE = .02210679007353296


def write(name, obj):
    (ROOT/name).write_text(json.dumps(obj, indent=2, allow_nan=False)+"\n")


@dataclass(frozen=True)
class Boundary:
    convection: str = "forced"
    gap_emissivity: float = 0.
    solid_density: float = 2700.
    quadrature: str = "split"
    nodes: int = 256
    include_poles: bool = True
    raw_day_projection: bool = False
    raw_night_projection: bool = False
    curvature: str = "roots"
    added_resistance_m2K_W: float = 0.


def quadrature(b):
    if b.quadrature == "midpoint":
        return -1+(np.arange(b.nodes)+.5)*2/b.nodes, np.full(b.nodes, 1/b.nodes)
    if b.quadrature == "split":
        z, w = L.leggauss(b.nodes//2)
        return np.r_[(z-1)/2, (z+1)/2], np.r_[w/4, w/4]
    z, w = L.leggauss(b.nodes)
    return z, w/2


def external_h(radius, temperature, kind):
    reynolds = RHO_AIR*2*(2*radius)/1.79e-5
    forced = .0257/(2*radius)*(2+(.4*reynolds**.5+.06*reynolds**(2/3))*.71**.4)
    delta = temperature-TA
    if kind == "forced":
        return np.full_like(temperature, forced), np.zeros_like(temperature), forced
    natural = 1.32*np.maximum(abs(delta), .05)**.25
    h = np.maximum(forced, natural)
    # Derivative of h(T)*(T-Ta) is h + this term.
    extra = np.where((natural > forced) & (abs(delta) > .05), natural/4, 0.)
    return h, extra, forced


def inverse_local(a, u, d, fo, fi):
    determinant = a*d-u*u
    return (d*fo+u*fi)/determinant, (u*fo+a*fi)/determinant


def solve_state(radius, thickness, alpha, epsilon, sky, solar, boundary):
    tc = np.atleast_1d(thickness).astype(float)
    mu, weights = quadrature(boundary)
    to = np.full((len(tc), len(mu)), TA)
    ti = to.copy()
    trad = np.full(len(tc), TA)
    tmean = trad.copy()
    conduction = 1/(tc/(130*RHO_CORE/boundary.solid_density)
                    + boundary.added_resistance_m2K_W)
    env4 = (1+mu)/2*sky**4+(1-mu)/2*TA**4
    insolation = alpha*solar*np.maximum(mu, 0)
    for iteration in range(60):
        conductance = conduction+4*boundary.gap_emissivity*SIGMA*tmean**3
        du = 12*boundary.gap_emissivity*SIGMA*tmean**2
        u = conductance[:, None]
        h, extra, hf = external_h(radius, to, boundary.convection)
        f = h*(to-TA)+epsilon*SIGMA*(to**4-env4)+u*(to-ti)-insolation
        g = u*(ti-to)+EPS_IN*SIGMA*(ti**4-trad[:, None]**4)
        a = h+extra+4*epsilon*SIGMA*to**3+u
        d = u+4*EPS_IN*SIGMA*ti**3
        # Local inverse applied to residual and each global-moment column.
        vo, vi = inverse_local(a, u, d, f, g)
        b0 = -4*EPS_IN*SIGMA*trad[:, None]**3
        z0o, z0i = inverse_local(a, u, d, np.zeros_like(to), b0)
        b1 = du[:, None]*(to-ti)
        z1o, z1i = inverse_local(a, u, d, b1, -b1)
        measured4 = np.sum(ti**4*weights, axis=1)**.25
        c4 = -weights*(ti/measured4[:, None])**3
        c1 = -weights
        s00 = 1-np.sum(c4*z0i, axis=1)
        s01 = -np.sum(c4*z1i, axis=1)
        s10 = -np.sum(c1*z0i, axis=1)
        s11 = 1-np.sum(c1*z1i, axis=1)
        r0 = -(trad-measured4)+np.sum(c4*vi, axis=1)
        r1 = -(tmean-np.sum(ti*weights, axis=1))+np.sum(c1*vi, axis=1)
        determinant = s00*s11-s01*s10
        change4 = (r0*s11-s01*r1)/determinant
        change1 = (s00*r1-r0*s10)/determinant
        dto = -vo-z0o*change4[:, None]-z1o*change1[:, None]
        dti = -vi-z0i*change4[:, None]-z1i*change1[:, None]
        to += dto
        ti += dti
        trad += change4
        tmean += change1
        last_change = max(float(np.max(abs(dto))), float(np.max(abs(dti))),
                          float(np.max(abs(change4))), float(np.max(abs(change1))))
        if last_change < 3e-11:
            break
    else:
        raise ArithmeticError(("coupled thermal Newton", last_change, asdict(boundary)))
    conductance = conduction+4*boundary.gap_emissivity*SIGMA*tmean**3
    u = conductance[:, None]
    h, _, hf = external_h(radius, to, boundary.convection)
    qi = EPS_IN*SIGMA*(ti**4-trad[:, None]**4)
    outer_residual = h*(to-TA)+epsilon*SIGMA*(to**4-env4)+u*(to-ti)-insolation
    inner_residual = u*(ti-to)+qi
    residual = max(float(np.max(abs(outer_residual))), float(np.max(abs(inner_residual))))
    assert residual < 3e-7, residual
    cavity_relative = float(np.max(abs(np.sum(ti**4*weights, axis=1)-trad**4)/trad**4))
    diagnostic = dict(iterations=iteration+1, update_K=last_change,
                      maximum_energy_residual_W_m2=residual,
                      global_external_residual_W_m2=float(np.max(abs(np.sum(outer_residual*weights, axis=1)))),
                      cavity_relative=cavity_relative, h_forced_W_m2K=hf,
                      h_min_W_m2K=float(h.min()), h_max_W_m2K=float(h.max()))
    pole_to, pole_ti = None, None
    if boundary.include_poles:
        # Re-solve local balances at true extrema without quadrature weight.
        pole_mu = np.array([-1., 1.])
        t = np.repeat(tmean[:, None], 2, axis=1)
        env = (1+pole_mu)/2*sky**4+(1-pole_mu)/2*TA**4
        qsun = alpha*solar*np.maximum(pole_mu, 0)
        for _ in range(30):
            q = EPS_IN*SIGMA*(t**4-trad[:, None]**4)
            dq = 4*EPS_IN*SIGMA*t**3
            out = t+q/u
            ho, ex, _ = external_h(radius, out, boundary.convection)
            res = epsilon*SIGMA*(out**4-env)+ho*(out-TA)+q-qsun
            derivative = (4*epsilon*SIGMA*out**3+ho+ex)*(1+dq/u)+dq
            step = res/derivative
            t -= step
            if np.max(abs(step)) < 3e-11:
                break
        pole_ti = t
        pole_to = t+EPS_IN*SIGMA*(t**4-trad[:, None]**4)/u
    return dict(mu=mu, weights=weights, outer=to, inner=ti,
                pole_outer=pole_to, pole_inner=pole_ti, diagnostic=diagnostic,
                mean_inner_K=tmean, radiative_mean_K=trad,
                conductance_W_m2K=conductance)


def curvature(state, raw=False, method="roots"):
    mu, weights = state["mu"], state["weights"]
    pattern = (state["outer"]+state["inner"])/2
    if not raw:
        pattern = pattern-np.sum(pattern*weights, axis=1)[:, None]
    coeff = (pattern*weights) @ L.legvander(mu, 6)*(2*np.arange(7)+1)
    coeff[:, :2] = 0.
    if method == "grid":
        x = np.cos(np.linspace(0, np.pi, 1441))
        basis = np.stack([(1-x*x)*L.Legendre.basis(j).deriv(2)(x)
                          -x*L.Legendre.basis(j).deriv()(x) for j in range(7)])
        return np.max(abs(coeff@basis), axis=1)
    out = []
    from numpy.polynomial import Polynomial as P
    for c in coeff:
        q = P([1, 0, -1])*P(L.leg2poly(L.legder(c, 2)))-P([0, 1])*P(L.leg2poly(L.legder(c)))
        roots = q.deriv().roots()
        nodes = [-1., 1.]+[float(z.real) for z in roots if abs(z.imag) < 1e-8 and -1 < z.real < 1]
        out.append(float(np.max(abs(q(nodes)))))
    return np.array(out)


def evaluate(radius, thickness, alpha=.2, epsilon=.9, boundary=Boundary(), profiles=False):
    day = solve_state(radius, thickness, alpha, epsilon, 275., 970., boundary)
    night = solve_state(radius, thickness, alpha, epsilon, 260., 0., boundary)
    fields = {}
    for key, state, raw in [("day", day, boundary.raw_day_projection),
                            ("night", night, boundary.raw_night_projection)]:
        outer, inner = state["outer"], state["inner"]
        if boundary.include_poles:
            outer = np.column_stack([outer, state["pole_outer"]])
            inner = np.column_stack([inner, state["pole_inner"]])
        fields[key+"_gradient_K"] = np.max(abs(outer-inner), axis=1)
        fields[key+"_curvature_temperature_K"] = curvature(state, raw, boundary.curvature)
        fields[key+"_max_K"] = outer.max(axis=1)
        fields[key+"_min_K"] = outer.min(axis=1)
        fields[key+"_mean_K"] = np.sum(state["outer"]*state["weights"], axis=1)
    fields.update(tc_m=np.atleast_1d(thickness),
                  gradient_K=np.maximum(fields["day_gradient_K"], fields["night_gradient_K"]),
                  curvature_temperature_K=np.maximum(fields["day_curvature_temperature_K"], fields["night_curvature_temperature_K"]),
                  swing_K=fields["day_max_K"]-fields["night_min_K"],
                  rise_K=fields["day_max_K"]-TA, max_outer_K=fields["day_max_K"],
                  min_outer_K=fields["night_min_K"])
    result = {k: v.tolist() for k, v in fields.items()}
    result.update(day_diagnostics=day["diagnostic"], night_diagnostics=night["diagnostic"])
    if profiles:
        result["profiles"] = {k: {name: state[name].tolist() for name in
                              ["mu", "weights", "outer", "inner", "mean_inner_K",
                               "radiative_mean_K", "conductance_W_m2K"]}
                              for k, state in [("day", day), ("night", night)]}
    return result


MODELS = {
    "forced_conduction": Boundary(),
    "mixed_conduction": Boundary(convection="legacy_mixed"),
    "forced_gap": Boundary(gap_emissivity=.2),
    "mixed_gap": Boundary(convection="legacy_mixed", gap_emissivity=.2),
}


if __name__ == "__main__":
    import sys
    if "--probe" in sys.argv:
        result = {}
        for name, b in MODELS.items():
            b = Boundary(**{**asdict(b), "solid_density": 2640.,
                            "quadrature": "gauss", "nodes": 128,
                            "include_poles": False, "curvature": "grid"})
            result[name] = evaluate(10, TC_REFERENCE, boundary=b, profiles=True)
        write("THERMAL-PROBE.json", result)
        print(json.dumps({name: {k: row[k][0] for k in
                         ["gradient_K", "swing_K", "rise_K", "curvature_temperature_K"]}
                          for name, row in result.items()}, indent=2))
