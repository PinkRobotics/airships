"""MAINLINE056: corotational Cauchy DF/J2 return, logarithmic strain.

Normalized DF yield: sqrt((q*q+alpha*alpha*p*p)/(1+alpha*alpha/9))-Y(k).
Associated flow, dk=dLambda. alpha=0 is J2; alpha=3/sqrt(2), nu=0 is
radial return in the Frobenius norm (zero plastic Poisson ratio).
All stresses MPa; strain is dimensionless. No fitted collapse-pressure input.

The corotational logarithmic-strain/Cauchy interface and conversion to PK2
follow the convention documented by CalculiX 2.21 umat_abaqusnl, without
copying its implementation. A numerical consistent tangent dPK2/dGreen is
used, with independent finite-difference verification in verify56.py.
"""
import math

import numpy as np
from numba import njit


@njit(cache=True)
def hardening(k, table):
    """Piecewise linear Y, dY/dk; last slope extrapolation is explicit."""
    i = 0
    while i < len(table) - 2 and k > table[i + 1, 0]:
        i += 1
    h = (table[i + 1, 1] - table[i, 1]) / (table[i + 1, 0] - table[i, 0])
    return table[i, 1] + h * (k - table[i, 0]), h


@njit(cache=True)
def return_log(h, ep0, k0, young, nu, alpha, table):
    """Engineering strain order rr,zz,hoop,2rz; stress rr,zz,hoop,rz."""
    shear = young / (2 * (1 + nu))
    bulk = young / (3 * (1 - 2 * nu))
    e = h - ep0
    tr = e[0] + e[1] + e[2]
    mean = bulk * tr
    s = np.empty(4)
    for j in range(3):
        s[j] = 2 * shear * (e[j] - tr / 3)
    s[3] = shear * e[3]
    q2 = 1.5 * (s[0]**2 + s[1]**2 + s[2]**2 + 2 * s[3]**2)
    a2 = alpha * alpha
    den = 1 + a2 / 9
    trial = math.sqrt(max(0, (q2 + a2 * mean * mean) / den))
    y0, _ = hardening(k0, table)
    dl = 0.0
    if trial > y0 * (1 + 1e-12):
        # Exact simplifications for the two main material choices.
        if alpha == 0:
            rate = 3 * shear
            for i in range(len(table) - 1):
                y, ht = hardening(max(k0, table[i, 0]) + 1e-14, table)
                intercept = y - ht * max(k0, table[i, 0])
                cand = (trial - intercept - ht * k0) / (rate + ht)
                if k0 + cand <= table[i + 1, 0] or i == len(table) - 2:
                    if k0 + cand >= table[i, 0] - 1e-12:
                        dl = max(0, cand)
                        break
        elif abs(a2 - 4.5) < 1e-12 and abs(nu) < 1e-12:
            for i in range(len(table) - 1):
                y, ht = hardening(max(k0, table[i, 0]) + 1e-14, table)
                intercept = y - ht * max(k0, table[i, 0])
                cand = (trial - intercept - ht * k0) / (young + ht)
                if k0 + cand <= table[i + 1, 0] or i == len(table) - 2:
                    if k0 + cand >= table[i, 0] - 1e-12:
                        dl = max(0, cand)
                        break
        else:
            # Monotone scalar consistency equation for associated DF.
            lo = 0.0
            hi = max(1e-6, 10 * trial / young)
            for _ in range(20):
                y, _ = hardening(k0 + hi, table)
                ad = 1 + 3 * shear * hi / (den * y)
                av = 1 + bulk * a2 * hi / (den * y)
                f = math.sqrt((q2 / ad**2 + a2 * mean**2 / av**2) / den) - y
                if f <= 0:
                    break
                hi *= 2
            for _ in range(55):
                dl = (lo + hi) / 2
                y, _ = hardening(k0 + dl, table)
                ad = 1 + 3 * shear * dl / (den * y)
                av = 1 + bulk * a2 * dl / (den * y)
                f = math.sqrt((q2 / ad**2 + a2 * mean**2 / av**2) / den) - y
                if f > 0:
                    lo = dl
                else:
                    hi = dl
            dl = (lo + hi) / 2
    y, _ = hardening(k0 + dl, table)
    ad = 1 + 3 * shear * dl / (den * y)
    av = 1 + bulk * a2 * dl / (den * y)
    sig = s / ad
    mn = mean / av
    for j in range(3):
        sig[j] += mn
    ep = np.empty(4)
    for j in range(3):
        ep[j] = h[j] - ((sig[j] - mn) / (2 * shear) + mn / (3 * bulk))
    ep[3] = h[3] - sig[3] / shear
    return sig, ep, k0 + dl, trial, y


@njit(cache=True)
def log_and_inverse(E):
    """Return log(U), U^-1 and J from the axisymmetric Green strain."""
    c11 = 1 + 2 * E[0]
    c22 = 1 + 2 * E[1]
    c12 = E[3]
    c33 = 1 + 2 * E[2]
    mean = (c11 + c22) / 2
    rad = math.sqrt(((c11 - c22) / 2)**2 + c12**2)
    lm, lp = mean - rad, mean + rad
    if min(lm, c33) <= 1e-12:
        raise ValueError("nonpositive right Cauchy-Green eigenvalue")
    lmean = (math.log(lp) + math.log(lm)) / 4
    vmean = (1 / math.sqrt(lp) + 1 / math.sqrt(lm)) / 2
    if rad > 1e-9 * mean:
        lslope = (math.log(lp) - math.log(lm)) / (4 * rad)
        vslope = (1 / math.sqrt(lp) - 1 / math.sqrt(lm)) / (2 * rad)
    else:
        lslope = 0.5 / mean
        vslope = -0.5 / mean**1.5
    h = np.array([lmean + lslope * (c11 - mean),
                  lmean + lslope * (c22 - mean),
                  0.5 * math.log(c33), 2 * lslope * c12])
    inv = np.array([vmean + vslope * (c11 - mean),
                    vmean + vslope * (c22 - mean),
                    1 / math.sqrt(c33), vslope * c12])
    jac = math.sqrt((c11 * c22 - c12 * c12) * c33)
    return h, inv, jac


@njit(cache=True)
def point(E, ep0, k0, young, nu, alpha, table):
    h, v, jac = log_and_inverse(E)
    sig, ep, k, trial, y = return_log(h, ep0, k0, young, nu, alpha, table)
    a, b, c, d = v
    x, z, t, s = sig
    pk = jac * np.array([a*a*x + 2*a*d*s + d*d*z,
                         d*d*x + 2*b*d*s + b*b*z,
                         c*c*t,
                         a*d*x + (a*b+d*d)*s + b*d*z])
    return pk, ep, k, sig, trial, y, jac


@njit(cache=True)
def evaluate(E, ep0, k0, kinds, props, foam, steel, tangent):
    n = len(E)
    S = np.empty((n, 4))
    ep = np.empty((n, 4))
    kap = np.empty(n)
    sig = np.empty((n, 4))
    extra = np.empty((n, 3))
    D = np.zeros((n, 4, 4))
    for i in range(n):
        kind = kinds[i]
        young, nu, alpha = props[kind]
        table = foam if kind == 0 else steel
        si, ei, ki, ci, tri, yi, ji = point(E[i], ep0[i], k0[i], young, nu, alpha, table)
        S[i], ep[i], kap[i], sig[i] = si, ei, ki, ci
        extra[i] = np.array([tri, yi, ji])
        if tangent:
            for j in range(4):
                de = 1e-7 * max(1.0, abs(E[i, j]))
                plus = E[i].copy()
                minus = E[i].copy()
                plus[j] += de
                minus[j] -= de
                sp = point(plus, ep0[i], k0[i], young, nu, alpha, table)[0]
                sm = point(minus, ep0[i], k0[i], young, nu, alpha, table)[0]
                D[i, :, j] = (sp - sm) / (2 * de)
    return S, D, ep, kap, sig, extra


def baseline_tables(foam_scale=1.0, steel_scale=1.0):
    # Read from EUCASS Fig.3, rounded plot digitization, not a collapse fit.
    # Later high-slope densification cannot be represented with constant E=40.
    # Only the monotone true-plastic-strain part is retained. Its last slope is
    # extrapolated explicitly and its use is tracked, never called source data.
    total_foam = np.array([[0.035, 1.4], [0.10, 1.4], [0.20, 1.42],
                           [0.30, 1.44], [0.40, 1.46], [0.45, 1.60],
                           [0.50, 1.90], [0.55, 2.40], [0.58, 2.96],
                           [0.60, 3.50]])
    foam = total_foam.copy()
    foam[:, 0] -= foam[:, 1] / 40
    foam[0, 0] = 0.0
    foam[:, 1] *= foam_scale
    # Conditional factor-of-ten reading of Fig.5. Literal reading is a
    # separate steel_scale=10 run. No claim that the correction is established.
    total_steel = np.array([[0., 750.], [.025, 792.], [.05, 824.],
                            [.10, 878.], [.15, 916.], [.20, 947.],
                            [.25, 976.], [.30, 1000.], [.375, 1018.]])
    steel = total_steel.copy()
    steel[:, 1] *= steel_scale
    steel[:, 0] = np.maximum(0, total_steel[:, 0] - steel[:, 1] / 210000)
    steel[0, 0] = 0
    # The literal axis makes some early points nonmonotone in plastic strain.
    keep = [0]
    for i in range(1, len(steel)):
        if steel[i, 0] > steel[keep[-1], 0]:
            keep.append(i)
    return foam, steel[keep], total_foam, total_steel
