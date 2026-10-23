#!/usr/bin/env python3
"""Independent scalar pressure/mass checks; exported, non-interactive figure."""
import hashlib
import json
from decimal import Decimal, getcontext
from pathlib import Path

ROOT = Path(__file__).resolve().parent
I = json.loads((ROOT / "INPUTS.json").read_text())
O = json.loads((ROOT / "RESULTS.json").read_text())
getcontext().prec = 40
D = lambda x: Decimal(str(x))
pi = D("3.141592653589793238462643383279502884197")
R = D(I["case"]["radius_m"])
A = 4*pi*R**2
p = D(I["case"]["p0_Pa"])
L = D(I["case"]["lift0_kg"])
E = D(I["face"]["E_Pa"])
rho = D(I["face"]["rho"])
nu = D(I["case"]["nu"])
root = (1-nu**2).sqrt()
b = D(O["biaxial_factor"])
checks = []
for name, result in O["scenarios"].items():
    sc = I["scenarios"][name]
    for family, pt in result["points"].items():
        co = I["cores"][family]
        t, c = D(pt["tf_m"]), D(pt["core_m"])
        G, Ec = D(co["Gc_Pa"]), D(co["Ec_Pa"])
        h = t+c
        vc = 2*E*t*c/(R*root*h*G)
        pressure_crimp = 2*G*h*h/(R*c)
        if vc > 2:
            pressure_global = pressure_crimp
        else:
            pressure_global = 4*D(".2")*E*t*h/(R*R*root)*(1-vc/4)
        pressures = {
            "global_buckling": pressure_global,
            "face_compression": 4*D(I["face"]["sigma_Pa"])*t/R,
            "core_crush": 2*D(co["crush_Pa"]),
            "core_shear_crimping": pressure_crimp,
            "face_wrinkling": 4*b*D(".33")*(E*Ec*t/c).sqrt()*t/R,
            "intracell_dimpling": 8*E*t**3/(R*(1-nu**2)*D(co["s_cell_m"])**2),
        }
        errors = {k: abs(float(v/p)-pt["modes"][k]) for k,v in pressures.items()}
        assert max(errors.values()) < 1e-9
        # Accounted physical mass is compared with day lift directly, without M.
        m_struct = 2*A*t*rho + A*c*D(co["rho"])
        length = 2*A/D(sc["panel_width_m"])
        bstrip = D(sc["strip_width_m"])
        metal = length*2*bstrip*t*rho
        local_adh = length*2*bstrip*D(sc["seam_adhesive_m"])*D(sc["rho_adhesive_kg_m3"])
        core_splice = length*c*D(sc["core_splice_width_m"])*D(sc["rho_splice_kg_m3"])
        film = 2*A*D(sc["bondfilm_lb_ft2"])*D(".45359237")/D(".3048")**2
        joint_total = metal+local_adh+core_splice+film
        sy = result["budgets"][family]["systems"]
        day_lift = L*(1-D(sc["pressure_swing_fraction"])-D(".378")*D(sc["water_vapour_Pa"])/p)*D("284.9")/(D("284.9")+D(sc["temperature_rise_K"]))
        extra = A*D(sc["water_film_m"])*D(1000)+D(sc["contamination_kg"])+D(sc["payload_kg"])+L*D(".01")
        accounted = m_struct+max(joint_total,D(".05")*m_struct)+max(D(sy["total_kg"]),D(100))+extra
        slack = float(day_lift-accounted)
        assert slack > -1e-7
        checks.append(dict(scenario=name, family=family, decimal_pressure_max_absolute_error=max(errors.values()),
                           day_mass_slack_kg=slack, scalar_mass_and_pressure="PASS"))

for pin in I["pins"]:
    raw = Path(pin["path"]).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == pin["sha256"], pin["path"]
validation = json.loads((ROOT/"VALIDATION.json").read_text())
validation["independent_decimal_checks"] = checks
validation["input_pins_reverified"] = len(I["pins"])
(ROOT/"VALIDATION.json").write_text(json.dumps(validation,indent=2)+"\n")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
fig, (ax, bar) = plt.subplots(1,2,figsize=(12,4.6),gridspec_kw={"width_ratios":[1.2,1]})
colors = {"aramid":"#125e89","aluminium":"#c76524"}
L0 = float(L)
for family, color in colors.items():
    ax.plot([x["margin_kg"]/L0*100 for x in O["curve"]],
            [x[family] for x in O["curve"]], color=color, label="Be / "+family, lw=2)
    for scenario, result in O["scenarios"].items():
        ax.scatter(result["margin_pct"], result["points"][family]["least_SF"],color=color,s=40,zorder=5)
ax.axhline(1,color="#7b2626",ls="--",lw=1,label="SF = 1")
ax.axvline(5,color="#666",ls=":",lw=1)
for name, result in O["scenarios"].items():
    ax.axvline(result["margin_pct"],color="#999",alpha=.55,lw=.8)
    ax.text(result["margin_pct"]+.6,.94,name,rotation=90,va="top",fontsize=8)
ax.set(xlabel="Reserve (% of reference lift)",ylabel="Re-optimised least factor",
       title="Both pinned families, kd = 0.20",xlim=(0,94),ylim=(0,1.05))
ax.legend(loc="upper center",fontsize=8)
ax.grid(alpha=.15)
names = ["optimistic","conservative"]
groups = [
    ("systems_excess_kg","Systems","#6d7789"),
    ("joints_and_bondfilm_excess_kg","Joints and bonds","#8063a3"),
    ("retained_water_kg","Water","#4194b5"),
    ("contamination_kg","Contamination","#8b7445"),
    ("temperature_pressure_loss_kg","Temperature + pressure","#cc8a3f"),
    ("humidity_loss_kg","Humidity","#d1b464"),
    ("internal_gas_kg","Internal air","#659077"),
]
bottom = [0.,0.]
for key, label, color in groups:
    vals = [O["scenarios"][n]["budgets"]["aluminium"]["lines"][key] for n in names]
    bar.bar(names,vals,bottom=bottom,color=color,label=label,width=.55)
    bottom = [a+b for a,b in zip(bottom,vals)]
for j, n in enumerate(names):
    bar.text(j,bottom[j]+60,f'{bottom[j]:,.0f} kg',ha="center",fontsize=9)
bar.axhline(.05*L0,color="#333",ls=":",lw=1)
bar.set(ylabel="Required reserve (kg)",title="Common budget; zero payload",ylim=(0,4900))
bar.legend(loc="upper left",fontsize=7)
bar.grid(axis="y",alpha=.15)
fig.suptitle("MAINLINE-019 | Scenario estimates, not a qualified design",fontsize=13)
fig.text(.02,.01,"QUESTIONABLE inputs; panel fabrication PROJECTION. Branch rule inherited unchanged. No site or leak measurements.",fontsize=8,color="#555")
fig.tight_layout(rect=(0,.05,1,.94))
fig.savefig(ROOT/"margin-budget.png",dpi=180)
plt.close(fig)
print(json.dumps(dict(status="PASS",independent_scalar_cases=len(checks),pins=len(I["pins"]),figure=str(ROOT/"margin-budget.png"))))
