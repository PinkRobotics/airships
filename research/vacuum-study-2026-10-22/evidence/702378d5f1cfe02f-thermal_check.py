"""CHECK-053: independent face balances, rank-two Newton elimination and audits.

Written from the non-code boundary specification and this seat's CHECK-040
derivation. No predecessor/owner executable is read, imported or run.
"""
from pathlib import Path
import json, gzip, math
from functools import lru_cache
import numpy as np
from numpy.polynomial import legendre as L
from numpy.polynomial import Polynomial as P

ROOT = Path(__file__).resolve().parent
SIGMA = 5.670374419e-8
TA = 284.9
RHO = 16.018463373960138
RHO_A = 1.1672683307461802
TC_REF = .02210679007353296
MODELS = ("forced_conduction", "mixed_conduction", "forced_gap", "mixed_gap")
COATS = {r["id"]: r for r in json.loads(
    (ROOT/"intake/inputs/048/COATINGS.json").read_text())}

def dump(name, value):
    (ROOT/name).write_text(json.dumps(value, indent=2, default=lambda v:
        v.tolist() if isinstance(v, np.ndarray) else v.item())+"\n")

@lru_cache(None)
def quadrature(n, scheme, poles):
    if scheme == "midpoint":
        x = (np.arange(n)+.5)*2/n-1
        w = np.full(n, 2/n)
    elif scheme == "split":
        z, wz = L.leggauss(n//2)
        x = np.r_[(z-1)/2, (z+1)/2]
        w = np.r_[wz/2, wz/2]
    else:
        x, w = L.leggauss(n)
    if poles:
        x, w = np.r_[-1, x, 1], np.r_[0, w, 0]
    return x, w/2

def curvature(to, ti, x, w, raw=False, mode="roots"):
    field = (to+ti)/2
    if not raw:
        field = field-(field@w)[:, None]
    coefficients = ((field*w)@L.legvander(x, 6))*(2*np.arange(7)+1)
    coefficients[:, :2] = 0
    values = []
    for c in coefficients:
        poly = P(L.leg2poly(c))
        q = P([1, 0, -1])*poly.deriv(2)-P([0, 1])*poly.deriv()
        if mode == "roots":
            roots = q.deriv().roots()
            points = [-1, 1]+[r.real for r in roots
                if abs(r.imag)<1e-8 and -1<r.real<1]
            values.append(float(max(abs(q(points)))))
        elif mode == "finite721":
            theta = np.linspace(0, np.pi, 721)
            vals = poly(np.cos(theta))
            values.append(float(max(abs(np.diff(vals, 2)))/(np.pi/720)**2))
        else:
            values.append(float(max(abs(q(np.cos(np.linspace(0, np.pi, 1441)))))))
    return np.array(values)

def solve(radius, thickness, model="forced_conduction", alpha=.09, epsilon=.8,
          n=256, scheme="split", poles=True, density=2700.,
          raw_day=False, raw_night=False, curv="roots", profiles=False,
          uniform=False, inner_epsilon=.2, gap_override=None, resistance=0.):
    x, w = quadrature(n, scheme, poles)
    tc = np.atleast_1d(thickness).astype(float)[:, None]
    hf = .0257/(2*radius)*(2+(.4*np.sqrt(RHO_A*4*radius/1.79e-5)
         +.06*(RHO_A*4*radius/1.79e-5)**(2/3))*.71**.4)
    eg = (.2 if model.endswith("_gap") else 0.) if gap_override is None else gap_override
    mixed = model.startswith("mixed")
    result = {"tc_m": tc[:, 0]}
    fields = {}
    for label, sky, sun, raw in (
            ("day", TA if uniform else 275., 0 if uniform else 970., raw_day),
            ("night", TA if uniform else 260., 0., raw_night)):
        incoming = epsilon*SIGMA*((1+x)/2*sky**4+(1-x)/2*TA**4)
        incoming = incoming+alpha*sun*np.maximum(x, 0)
        to = np.full((len(tc), len(x)), TA)
        ti = to.copy()
        for iteration in range(70):
            mean = (ti@w)[:, None]
            j = (ti**4@w)[:, None]
            u_raw = 130*RHO/density/tc+4*eg*SIGMA*mean**3
            u = 1/(1/u_raw+resistance)
            du = 12*eg*SIGMA*mean**2*(u/u_raw)**2
            hn = 1.32*np.maximum(abs(to-TA), .05)**.25
            h = np.maximum(hf, hn) if mixed else np.full_like(to, hf)
            dhflux = np.where((hn>hf)&mixed,
                hn*(1+.25*(abs(to-TA)>.05)), hf)
            f = h*(to-TA)+epsilon*SIGMA*to**4+u*(to-ti)-incoming
            g = u*(ti-to)+inner_epsilon*SIGMA*(ti**4-j)
            a = dhflux+4*epsilon*SIGMA*to**3+u
            d = u+4*inner_epsilon*SIGMA*ti**3-u*u/a
            rhs = (-g-u*f/a)/d
            first = du*(to-ti)*(u/a-1)/d
            second = -4*inner_epsilon*SIGMA/d
            # Solve the two area-moment updates after eliminating local To.
            b11 = 1+first@w
            b12 = second@w
            b21 = (first*ti**3)@w
            b22 = 1+(second*ti**3)@w
            r1 = rhs@w
            r2 = (rhs*ti**3)@w
            det = b11*b22-b12*b21
            z1 = (b22*r1-b12*r2)/det
            z2 = (b11*r2-b21*r1)/det
            dti = rhs-first*z1[:, None]-second*z2[:, None]
            dto = (-f+u*dti-du*(to-ti)*z1[:, None])/a
            to += dto
            ti += dti
            update = max(np.max(abs(dto)), np.max(abs(dti)))
            if update<2e-11:
                break
        else:
            raise RuntimeError(("thermal failed to converge", model, radius, update))
        # Re-evaluate residuals at final state, independent of the stopping test.
        mean = (ti@w)[:, None]
        j = (ti**4@w)[:, None]
        u = 1/(1/(130*RHO/density/tc+4*eg*SIGMA*mean**3)+resistance)
        hn = 1.32*np.maximum(abs(to-TA), .05)**.25
        h = np.maximum(hf, hn) if mixed else np.full_like(to, hf)
        ext = h*(to-TA)+epsilon*SIGMA*to**4-incoming
        qi = inner_epsilon*SIGMA*(ti**4-j)
        result[label+"_gradient_K"] = np.max(abs(to-ti), axis=1)
        result[label+"_curvature_temperature_K"] = curvature(to, ti, x, w, raw, curv)
        result[label+"_max_K"] = np.max(to, axis=1)
        result[label+"_min_K"] = np.min(to, axis=1)
        result[label+"_mean_K"] = ((to+ti)/2)@w
        result[label+"_diagnostics"] = {
            "iterations": iteration+1,
            "update_K": float(update),
            "maximum_energy_residual_W_m2": float(max(
                np.max(abs(ext+u*(to-ti))), np.max(abs(u*(ti-to)+qi)))),
            "global_external_residual_W_m2": float(np.max(abs(ext@w))),
            "net_cavity_W_m2": float(np.max(abs(qi@w))),
            "h_forced_W_m2K": hf,
            "h_min_W_m2K": float(np.min(h)),
            "h_max_W_m2K": float(np.max(h))}
        fields[label] = {"mu": x, "outer_K": to, "inner_K": ti}
    result["gradient_K"] = np.maximum(result["day_gradient_K"], result["night_gradient_K"])
    result["curvature_temperature_K"] = np.maximum(
        result["day_curvature_temperature_K"], result["night_curvature_temperature_K"])
    result["max_outer_K"] = result["day_max_K"]
    result["min_outer_K"] = result["night_min_K"]
    result["swing_K"] = result["max_outer_K"]-result["min_outer_K"]
    result["rise_K"] = result["max_outer_K"]-TA
    if profiles:
        result["profiles"] = fields
    return result

class Compare:
    def __init__(self, name):
        self.file = gzip.open(ROOT/(name+".jsonl.gz"), "wt")
        self.stats = {}
        self.mismatches = []
    def add(self, group, path, own, filed, atol=2e-8, rtol=2e-11):
        own, filed = float(own), float(filed)
        diff = own-filed
        tol = atol+rtol*abs(filed)
        row = dict(group=group, path=path, own=own, filed=filed,
                   difference=diff, tolerance=tol, passed=abs(diff)<=tol)
        self.file.write(json.dumps(row)+"\n")
        s = self.stats.setdefault(group, {"count":0, "passed":0, "maximum_absolute_difference":0.})
        s["count"] += 1
        s["passed"] += int(row["passed"])
        s["maximum_absolute_difference"] = max(s["maximum_absolute_difference"], abs(diff))
        if not row["passed"]:
            self.mismatches.append(row)
    def table(self, group, key, ours, filed, atol=2e-8):
        for field, vals in filed.items():
            if not isinstance(vals, list) or not vals or not isinstance(vals[0], (int, float)):
                continue
            if field not in ours:
                continue
            for i, (a, b) in enumerate(zip(ours[field], vals, strict=True)):
                self.add(group, f"{key}/{field}/{i}", a, b, atol=atol)
    def close(self, name):
        self.file.close()
        dump(name+"-SUMMARY.json", self.stats)
        dump(name+"-MISMATCHES.json", self.mismatches)

def main():
    comp = Compare("THERMAL-COMPARISONS")
    filed = json.loads((ROOT/"owner/SETTLED-THERMAL-TABLES.json").read_text())
    tables = {}
    for model in MODELS:
        tables[model] = {}
        for profile in ("reference040", "MLCCAg"):
            tables[model][profile] = {}
            coat = COATS[profile]
            for radius in (10, 12, 15, 20, 30):
                tc = np.geomspace(.001*radius/10, 1.5*radius/10, 241)
                ans = solve(radius, tc, model, coat["alpha"], coat["epsilon"])
                tables[model][profile][str(radius)] = ans
                comp.table("settled_tables", f"{model}/{profile}/{radius}",
                           ans, filed[model][profile][str(radius)])
        print("thermal tables", model, flush=True)
    dump("THERMAL-INDEPENDENT.json", tables)
    probes = {}
    expected = json.loads((ROOT/"owner/THERMAL-PROBE.json").read_text())
    for model in MODELS:
        ans = solve(10, TC_REF, model, .2, .9, n=128, scheme="gauss",
                    poles=False, density=2640., profiles=True)
        probes[model] = ans
        comp.table("four_historical_R10", model, ans, expected[model])
    dump("FOUR-R10-INDEPENDENT.json", probes)
    references = []
    for row in json.loads((ROOT/"owner/REFERENCE-THERMAL-ROWS.json").read_text()):
        c = COATS[row["profile"]]
        ans = solve(row["radius_m"], TC_REF*row["radius_m"]/10,
            row["model"], c["alpha"], c["epsilon"], profiles=True)
        comp.table("reference_rows", f'{row["model"]}/{row["profile"]}/{row["radius_m"]}',
                   ans, row["values"])
        references.append({k:row[k] for k in ["model","profile","radius_m"]}|{"values":ans})
    dump("REFERENCE-INDEPENDENT.json", references)
    screens = []
    # Original 028b/037 screen geometry, explicitly a separate rigid-shear screen.
    screen_refs = json.loads((ROOT/"owner/SETTLED-FINISH-SCREEN.json").read_text())
    source = json.loads((ROOT/"intake/inputs/037/INPUTS.json").read_text())
    dump("SCREEN-INPUT-SCHEMA.json", source)
    # Full scalar screen factors are audited by the account module; retain all
    # temperatures here without adopting the reported screening outputs.
    for row in screen_refs:
        c = COATS[row["id"]]
        ans = solve(10, TC_REF, row["model"], c["alpha"], c["epsilon"])
        comp.table("finish_temperatures", row["model"]+"/"+row["id"], ans, row["temperatures"])
        screens.append({"model":row["model"],"id":row["id"],"temperatures":ans})
    dump("FINISH-TEMPERATURES-INDEPENDENT.json", screens)
    # Historical physical tables: numerical conventions stated in the reply.
    original = json.loads((ROOT/"intake/inputs/048/THERMAL-TABLES.json").read_text())
    legacy_tables = {}
    for profile, radii in original.items():
        c = COATS[profile]
        legacy_tables[profile] = {}
        for radius_s, target in radii.items():
            ans = solve(float(radius_s), target["tc_m"], "mixed_gap",
                c["alpha"], c["epsilon"], n=128, scheme="gauss", poles=False, curv="grid")
            legacy_tables[profile][radius_s] = ans
            comp.table("historical048_tables", f"{profile}/{radius_s}", ans, target)
        print("historical tables", profile, flush=True)
    dump("HISTORICAL-INDEPENDENT.json", legacy_tables)
    comp.close("THERMAL")
    print(json.dumps(comp.stats, indent=2), flush=True)

if __name__ == "__main__":
    main()
