#!/usr/bin/env python3
"""MAINLINE-035: measured sandwich-shell knockdowns against Vc and R/rho, and the lead points' gamma needs.

Checker seat ref-55cff924be25afe6f9dd, own arithmetic. Inputs are the stated numbers in LIT-A..D.json (four research
sub-workers; each number carries its source location) plus this seat's own reading of CR-1457 Fig. 6.2-3. Face moduli of
the SBKF laminates are computed here by classical lamination theory (the sources give lamina values only). Every value is
QUESTIONABLE; nothing here is a certification.
"""
import json
import math
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = Path(__file__).resolve().parents[1] / "outputs" / "vacuum-mainline035-sandwich-knockdown-tests-1020"


# ---- classical lamination theory --------------------------------------------------------------------
def q_matrix(E1, E2, nu12, G12):
    nu21 = nu12 * E2 / E1
    d = 1 - nu12 * nu21
    return np.array([[E1 / d, nu12 * E2 / d, 0], [nu12 * E2 / d, E2 / d, 0], [0, 0, G12]])


def qbar(Q, deg):
    t = math.radians(deg)
    c, s = math.cos(t), math.sin(t)
    T = np.array([[c * c, s * s, 2 * s * c], [s * s, c * c, -2 * s * c], [-s * c, s * c, c * c - s * s]])
    R = np.diag([1, 1, 2])
    return np.linalg.inv(T) @ Q @ R @ T @ np.linalg.inv(R)


def laminate(layup, tply, E1, E2, nu12, G12):
    Q = q_matrix(E1, E2, nu12, G12)
    A = sum(qbar(Q, th) * tply for th in layup)
    t = tply * len(layup)
    a = np.linalg.inv(A)
    Ex, Ey = 1 / (a[0, 0] * t), 1 / (a[1, 1] * t)
    nuxy = -a[0, 1] / a[0, 0]
    return {"t_in": t, "Ex_psi": Ex, "Ey_psi": Ey, "nuxy": nuxy, "nuyx": nuxy * Ey / Ex, "Gxy_psi": 1 / (a[2, 2] * t)}


def vc_line(E, nu, tf, tc, R, Gc):
    """The line's Vc = sigma0/sigma_crimp = 2*E*tf*tc / (R*sqrt(1-nu^2)*(tc+tf)*Gc), equal faces."""
    return 2 * E * tf * tc / (R * math.sqrt(1 - nu * nu) * (tc + tf) * Gc)


def sp8007(r_over_teq):
    phi = math.sqrt(r_over_teq) / 16
    return 1 - 0.901 * (1 - math.exp(-phi))


def sp8032_sphere(r_over_teq, nu=0.3):
    lam = 2 * (3 * (1 - nu * nu)) ** 0.25 * math.sqrt(r_over_teq)
    return 0.14 + 3.2 / lam ** 2


def cr1457_cyl(r_over_rho):
    """CR-1457 Fig. 4.2-3 design curve, eye-read by the B researcher: 0.68 @10, 0.55 @100, 0.31 @1000; log-linear between."""
    x = math.log10(r_over_rho)
    pts = [(1.0, 0.68), (2.0, 0.55), (3.0, 0.31)]
    if x <= 1: return 0.68
    if x >= 3: return 0.31 + (x - 3) * (0.31 - 0.55)
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


# ---- the SBKF articles (stated values from LIT-A; G12 generic, as CTA8.1's paper assumed) -----------------
LAM_8552 = dict(E1=20.4e6, E2=1.33e6, nu12=0.345, G12=0.77e6)       # TM-20205008667 Table 4; G12 generic
LAM_GENERIC = dict(E1=20.0e6, E2=1.25e6, nu12=0.36, G12=0.77e6)      # CTA8.1 paper, generic IM7/8552
SBKF = [
    {"id": "CTA8.1", "src": "NTRS 20180002092 (Schultz et al. 2018)", "layup": [45, -45, 0, 90, 0, -45, 45], "tply": 0.0052,
     "lam": LAM_GENERIC, "tc": 0.25, "G13": 29500.0, "G23": 12000.0, "R": 48.0, "gamma": 0.87,
     "basis": "test / perfect-shell linear eigenvalue (stated 0.87)", "mode": "global buckling"},
    {"id": "CTA8.2", "src": "NASA/TM-20210024095", "layup": [60, -60, 0, 0, -60, 60], "tply": 0.00694, "lam": LAM_8552,
     "tc": 0.2, "G13": 45000.0, "G23": 20000.0, "R": 48.0, "gamma": 0.775,
     "basis": "test / linear eigenvalue (stated 77.5%)", "mode": "core crush and shear at a ring, before global buckling (not a buckling datum)"},
    {"id": "CTA8.2B", "src": "NASA/TM-20210024081", "layup": [60, -60, 0, 0, -60, 60], "tply": 0.00694, "lam": LAM_8552,
     "tc": 0.2, "G13": 45000.0, "G23": 20000.0, "R": 48.0, "gamma": 0.721,
     "basis": "test / linear eigenvalue, combined load (stated 72.1%)", "mode": "global buckling"},
    {"id": "CTA8.3", "src": "NASA/TM-20210024768", "layup": [30, -30, 90, 90, -30, 30], "tply": 0.0054, "lam": LAM_8552,
     "tc": 0.2, "G13": 45000.0, "G23": 20000.0, "R": 48.0, "gamma": 0.864,
     "basis": "test / linear eigenvalue, combined load (stated 86.4%)", "mode": "global buckling"},
]
LEADS = [
    {"id": "021 rev1", "Vc": 1.06106, "gamma": 0.59532, "h_m": 0.0210568, "R_m": 10.0},
    {"id": "021b", "Vc": 0.886182, "gamma": 0.46823, "h_m": 0.03081, "R_m": 10.0},
]
SII_HEMI = {"R_over_rho": 240.0, "gamma": (0.22, 0.24), "src": "CR-1457 Fig. 6.2-3 (p. 6-9), eye-read by this seat"}
SII_ELL = [(240, 0.39), (240, 0.58), (245, 0.41), (245, 0.61), (480, 0.46), (480, 0.99)]
# CR-1457 Fig. 4.2-3 (PDF p. 188): pre-1969 sandwich cylinders, axial, non weak-core; eye-read by the B researcher and by
# this seat from the page image. ref 4-2 = FPL 1830, ref 4-10 = Baker 1968, ref 4-28 = FPL PE-227.
CR1457_CYL_PTS = [(1050, 0.42, "FPL 1830"), (1300, 0.44, "FPL 1830"), (180, 0.545, "Baker 1968"), (270, 0.69, "Baker 1968"),
                  (270, 0.58, "Baker 1968"), (270, 0.57, "Baker 1968"), (410, 0.49, "Baker 1968"),
                  (105, 0.76, "FPL PE-227"), (105, 0.63, "FPL PE-227"), (105, 0.61, "FPL PE-227")]


def old_cyl_at(r_over_rho):
    """Log-linear interpolation between the two nearest bracketing old-cylinder points above R/rho 400 (Baker 410, FPL 1050)."""
    x0, y0, x1, y1 = 410.0, 0.49, 1050.0, 0.42
    t = (math.log10(r_over_rho) - math.log10(x0)) / (math.log10(x1) - math.log10(x0))
    return y0 + t * (y1 - y0)


def main():
    rows = []
    for a in SBKF:
        L = laminate(a["layup"], a["tply"], **a["lam"])
        tf, tc, R = L["t_in"], a["tc"], a["R"]
        h = tc + tf
        E_iso = math.sqrt(L["Ex_psi"] * L["Ey_psi"])
        nu_iso = math.sqrt(L["nuxy"] * L["nuyx"])
        Gc_iso = math.sqrt(a["G13"] * a["G23"])
        vcs = [vc_line(E_iso, nu_iso, tf, tc, R, Gc_iso),                       # isotropic-equivalent
               vc_line(L["Ex_psi"], L["nuxy"], tf, tc, R, a["G13"]),             # axial face, axial core shear
               vc_line(E_iso, nu_iso, tf, tc, R, min(a["G13"], a["G23"]))]       # softer core direction
        r_rho, r_teq = 2 * R / h, R / (math.sqrt(3) * h)
        rows.append({**{k: a[k] for k in ("id", "src", "layup", "tply", "tc", "G13", "G23", "R", "gamma", "basis", "mode")},
                     "laminate": L, "h_in": h, "Vc_iso": vcs[0], "Vc_axial": vcs[1], "Vc_soft": vcs[2],
                     "Vc_range": [min(vcs), max(vcs)], "R_over_rho": r_rho, "R_over_teq": r_teq,
                     "SP8007_at_teq": sp8007(r_teq), "beat_SP8007": a["gamma"] / sp8007(r_teq),
                     "CR1457_cyl_curve": cr1457_cyl(r_rho), "beat_CR1457_curve": a["gamma"] / cr1457_cyl(r_rho)})
    leads = []
    buck = [r for r in rows if "not a buckling" not in r["mode"]]
    beats = [r["beat_SP8007"] for r in buck]
    for p in LEADS:
        r_rho, r_teq = 2 * p["R_m"] / p["h_m"], p["R_m"] / (math.sqrt(3) * p["h_m"])
        cyl, sph = sp8007(r_teq), sp8032_sphere(r_teq)
        leads.append({**p, "R_over_rho": r_rho, "R_over_teq": r_teq, "SP8007_cyl": cyl, "SP8032_sphere": sph,
                      "CR1457_cyl_curve": cr1457_cyl(r_rho), "CR1457_hemisphere_design": 0.20,
                      "old_sandwich_cylinders_interpolated": old_cyl_at(r_rho),
                      "need_over_old_cylinders": p["gamma"] / old_cyl_at(r_rho),
                      "transfer": {
                          "direct_cylinder_record": [min(r["gamma"] for r in buck), max(r["gamma"] for r in buck)],
                          "sbkf_beat_on_SP8007_at_lead_cylinder": [min(beats) * cyl, max(beats) * cyl],
                          "sbkf_beat_on_SP8032_at_lead_sphere": [min(beats) * sph, max(beats) * sph],
                          "measured_sandwich_hemisphere_SII": list(SII_HEMI["gamma"])},
                      "need_over_SII_hemisphere": [p["gamma"] / SII_HEMI["gamma"][1], p["gamma"] / SII_HEMI["gamma"][0]],
                      "need_over_sphere_transfer": [p["gamma"] / (max(beats) * sph), p["gamma"] / (min(beats) * sph)]})
    res = {"schema": 1, "card": "MAINLINE-035", "unit": "vacuum-mainline035-sandwich-knockdown-tests-1020",
           "questionable": True, "certification": False, "sbkf": rows, "leads": leads,
           "SII_hemispheres": SII_HEMI, "SII_ellipsoids_eye_read": SII_ELL, "CR1457_cylinder_points_eye_read": CR1457_CYL_PTS,
           "curves": {"018_optimistic": "0.20 + 0.40*min(Vc, 2), PROJECTION", "018_conservative": "0.20",
                      "CR1457_step_sphere": "0.20 below Vc 2, 1 at and above",
                      "CR1457_cylinder_design": "0.68 @ R/rho 10, 0.55 @ 100, 0.31 @ 1000 (eye-read)"}}
    (OUT / "RESULTS-ANALYSIS.json").write_text(json.dumps(res, indent=1, default=float))

    # ---- charts: two panels, one y-scale each (gamma) ----
    ink, ink2, grid, surf = "#0b0b0b", "#52514e", "#d9d8d4", "#fcfcfb"
    c_cyl, c_hemi, c_ell = "#2a78d6", "#eb6834", "#1baf7a"
    plt.rcParams.update({"font.size": 10, "axes.edgecolor": ink2, "axes.labelcolor": ink, "xtick.color": ink2,
                         "ytick.color": ink2, "font.family": "DejaVu Sans"})
    fig, axes = plt.subplots(1, 2, figsize=(13, 6.6), facecolor=surf)
    # (a) gamma vs Vc
    ax = axes[0]
    ax.set_facecolor(surf)
    v = np.linspace(0, 3, 601)
    ax.plot(v, 0.2 + 0.4 * np.minimum(v, 2), color=ink2, lw=2, ls="--", label="018 optimistic curve (PROJECTION)")
    ax.plot(v, np.full_like(v, 0.2), color=ink2, lw=2, ls=":", label="018 conservative, 0.20")
    ax.plot(v, np.where(v < 2, 0.2, 1.0), color="#8a8984", lw=1.2, ls="-", label="CR-1457 sphere step")
    for r in rows:
        mk = "o" if "not a buckling" not in r["mode"] else "x"
        ax.errorbar(r["Vc_iso"], r["gamma"], xerr=[[r["Vc_iso"] - r["Vc_range"][0]], [r["Vc_range"][1] - r["Vc_iso"]]],
                    fmt=mk, ms=8, color=c_cyl, mec=surf if mk == "o" else c_cyl, mew=1.5, elinewidth=1.5, capsize=0, zorder=4)
        off = {"CTA8.1": (10, 8), "CTA8.3": (-48, 8), "CTA8.2": (12, 3), "CTA8.2B": (10, -12)}[r["id"]]
        ax.annotate(r["id"], (r["Vc_iso"], r["gamma"]), xytext=off, textcoords="offset points", fontsize=8.5, color=ink2)
    for p in leads:
        ax.plot(p["Vc"], p["gamma"], marker="*", ms=15, color=ink, mec=surf, mew=1.2, ls="none", zorder=5)
        ax.annotate(f"{p['id']} needs {p['gamma']:.3f}", (p["Vc"], p["gamma"]), xytext=(8, -14), textcoords="offset points",
                    fontsize=9, color=ink)
    ax.plot([], [], "o", color=c_cyl, ms=8, label="SBKF sandwich cylinders, axial (measured; x = core failure)")
    ax.plot([], [], "*", color=ink, ms=12, label="P2 lead points (needed)")
    ax.set_xlim(0, 3); ax.set_ylim(0, 1.05)
    ax.set_xlabel("Vc = sigma0 / sigma_crimp (line definition)"); ax.set_ylabel("knockdown gamma (test / prediction with core shear)")
    ax.set_title("(a) Measured gamma against Vc", color=ink, loc="left", fontsize=11)
    ax.grid(True, color=grid, lw=0.8); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.legend(loc="upper left", bbox_to_anchor=(0, -0.13), fontsize=8.2, frameon=False, ncol=1)
    ax.text(1.25, 0.23, "no measured point at Vc 0.9 to 2\nin any shell form", fontsize=8.5, color=ink2, va="bottom")
    # (b) gamma vs R/rho
    ax = axes[1]
    ax.set_facecolor(surf)
    xr = np.logspace(1, np.log10(2000), 200)
    xc = xr[xr <= 1000]
    ax.plot(xc, [cr1457_cyl(x) for x in xc], color=ink2, lw=2, label="CR-1457 sandwich cylinder design curve (eye-read, to R/rho 1000)")
    ax.plot(xr, [sp8007(x / (2 * math.sqrt(3))) for x in xr], color=ink2, lw=1.4, ls="-.",
            label="SP-8007 cylinder at R/t_eq = (R/rho)/(2*sqrt3)")
    ax.plot(xr, [sp8032_sphere(x / (2 * math.sqrt(3))) for x in xr], color=ink2, lw=1.4, ls=":", label="SP-8032 sphere, same t_eq")
    ax.axhline(0.2, color="#8a8984", lw=1.2, label="CR-1457 hemisphere design 0.20")
    for r in rows:
        mk = "o" if "not a buckling" not in r["mode"] else "x"
        ax.plot(r["R_over_rho"], r["gamma"], mk, ms=8, color=c_cyl, mec=surf if mk == "o" else c_cyl, mew=1.5, zorder=4)
    ax.errorbar([SII_HEMI["R_over_rho"]], [sum(SII_HEMI["gamma"]) / 2], yerr=[[0.01], [0.01]], fmt="^", ms=9, color=c_hemi,
                mec=surf, mew=1.2, elinewidth=1.5, capsize=0, zorder=4, label="Saturn S-II sandwich hemispheres (measured, 2)")
    ax.plot([x for x, _ in SII_ELL], [y for _, y in SII_ELL], "s", ms=7, color=c_ell, mec=surf, mew=1.2, zorder=4,
            label="Saturn S-II sandwich ellipsoids (measured)")
    ax.plot([x for x, _, _ in CR1457_CYL_PTS], [y for _, y, _ in CR1457_CYL_PTS], "D", ms=6.5, color=c_cyl, mfc=surf,
            mec=c_cyl, mew=1.6, zorder=4, label="Pre-1969 sandwich cylinders, axial (CR-1457 Fig. 4.2-3, measured)")
    ax.annotate("FPL 1830", (1050, 0.42), xytext=(-18, -16), textcoords="offset points", fontsize=8.5, color=ink2)
    ax.plot([], [], "o", color=c_cyl, ms=8, label="SBKF sandwich cylinders (measured)")
    for p in leads:
        ax.plot(p["R_over_rho"], p["gamma"], marker="*", ms=15, color=ink, mec=surf, mew=1.2, ls="none", zorder=5)
        ax.annotate(f"{p['id']}", (p["R_over_rho"], p["gamma"]), xytext=(6, 6), textcoords="offset points", fontsize=9, color=ink)
    ax.annotate("S-II hemispheres", (SII_HEMI["R_over_rho"], 0.23), xytext=(-112, 4), textcoords="offset points", fontsize=8.5, color=ink2)
    ax.annotate("SBKF cylinders", (397, 0.80), xytext=(-95, 4), textcoords="offset points", fontsize=8.5, color=ink2)
    ax.set_xscale("log"); ax.set_xlim(10, 2000); ax.set_ylim(0, 1.05)
    ax.set_xlabel("R / rho  (rho = h/2, sandwich radius of gyration)"); ax.set_ylabel("knockdown gamma")
    ax.set_title("(b) Measured gamma against R/rho, cylinders and domes", color=ink, loc="left", fontsize=11)
    ax.grid(True, which="both", color=grid, lw=0.6); ax.set_axisbelow(True)
    for s in ("top", "right"): ax.spines[s].set_visible(False)
    ax.legend(loc="upper left", bbox_to_anchor=(0, -0.13), fontsize=8.2, frameon=False, ncol=1)
    fig.suptitle("MAINLINE-035: the sandwich-shell knockdown record against the P2 lead's needs (QUESTIONABLE)",
                 color=ink, fontsize=12, x=0.01, ha="left")
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(OUT / "gamma-map.png", dpi=150, facecolor=surf)
    for r in rows:
        print(f"{r['id']:8s} tf {r['laminate']['t_in']:.4f} in  Ex {r['laminate']['Ex_psi']/1e6:.2f} Ey {r['laminate']['Ey_psi']/1e6:.2f} Msi"
              f"  Vc iso {r['Vc_iso']:.3f} [{r['Vc_range'][0]:.3f}, {r['Vc_range'][1]:.3f}]  R/rho {r['R_over_rho']:.0f}"
              f"  R/teq {r['R_over_teq']:.1f}  SP8007 {r['SP8007_at_teq']:.3f}  gamma {r['gamma']:.3f}  beat {r['beat_SP8007']:.2f}"
              f"  CR1457cyl {r['CR1457_cyl_curve']:.3f}")
    for p in leads:
        print(json.dumps({k: (round(v, 4) if isinstance(v, float) else v) for k, v in p.items() if k != "transfer"}))
        print("   transfer", json.dumps({k: [round(x, 3) for x in v] for k, v in p["transfer"].items()}))
        print("   need/SII", [round(x, 2) for x in p["need_over_SII_hemisphere"]], "need/sphere-transfer",
              [round(x, 2) for x in p["need_over_sphere_transfer"]])


if __name__ == "__main__":
    main()
