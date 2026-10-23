"""Read-only helpers for native histories and conditional boundary calculations."""
import csv, json, math, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
P0=95.46083791390515
def summary(name):
    return json.loads((ROOT/"runs"/name/"SUMMARY.json").read_text())
def path(name):
    rows=list(csv.DictReader((ROOT/"runs"/name/"PATH.csv").open()))
    for r in rows:
        for k in ["p_kPa","max_mises_MPa","max_peeq","inner_mises_MPa","outer_mises_MPa"]:
            r[k]=float(r[k])
    return rows
def at_pressure(name,p):
    rows=path(name)
    if not rows or rows[-1]["p_kPa"]<p-1e-4:
        return None
    for hi in rows:
        if abs(hi["p_kPa"]-p)<1e-4:
            return dict(hi,interpolation="native target increment, printed-time rounding <0.0001 kPa")
    lo=dict(p_kPa=0.,max_mises_MPa=0.,max_peeq=0.,inner_mises_MPa=0.,outer_mises_MPa=0.)
    for hi in rows:
        if hi["p_kPa"]>p:
            f=(p-lo["p_kPa"])/(hi["p_kPa"]-lo["p_kPa"])
            return dict(p_kPa=p,interpolation="linear between native increments",
                        **{k:lo[k]+f*(hi[k]-lo[k]) for k in ["max_mises_MPa","max_peeq","inner_mises_MPa","outer_mises_MPa"]})
        lo=hi
    return None
def py_estimate(row,y=None):
    y=row["yield_MPa"] if y is None else y
    v=row["first_yield_estimates"].get(str(float(y)))
    if v and v.get("inside_native_bracket",True):return v["p_kPa"]
    b=row["first_yield_bracket_kPa"]
    return sum(b)/2 if b else None
def criterion(row,endpoint_divisor=1.):
    y=py_estimate(row)
    # If yield was not reached on the converged path, endpoint governs the
    # requested minimum. Do not relabel the endpoint as an observed yield.
    return min(row["endpoint_kPa"]/endpoint_divisor,y if y is not None else math.inf)
def rms_factor(w,R=10000.):
    from scipy.integrate import quad
    beta=w/R
    integ=quad(lambda x:math.exp(-2*x*x)*math.sin(beta*x),0,min(math.pi/beta,12),
               epsabs=1e-14,epsrel=1e-12)[0]
    return math.sqrt(beta*integ/2)
def sampled_boundary(points,target):
    """Return crossing estimate AND its tested amplitude bracket."""
    points=sorted(points)
    if not points or points[0][0]!=0:
        return dict(status="missing_zero")
    if points[0][1]<target:
        return dict(status="no_admissible_amplitude_even_zero",amplitude_mm=None,
                    perfect_capacity_kPa=points[0][1],target_kPa=target)
    for (a,p),(b,q) in zip(points,points[1:]):
        if p>=target and q<target:
            return dict(status="sampled_crossing",amplitude_mm=a+(target-p)*(b-a)/(q-p),
                        bracket_mm=[a,b],bracket_capacity_kPa=[p,q],target_kPa=target)
    return dict(status="not_bracketed",last_point=points[-1],target_kPa=target)
def sweep_rows():
    rows=[]
    for listname in ["SWEEP.json","CONTROLS.json"]:
        for job in json.loads((ROOT/listname).read_text()):
            if not job["name"].startswith(("sweep-","perfect-")):continue
            p=ROOT/"runs"/job["name"]/"SUMMARY.json"
            if p.exists():rows.append(json.loads(p.read_text()))
    for n in ["p128-a0-y345","p128-a1-W-y345","p128-a1-L-y345"]:
        rows.append(summary(n))
    return rows
