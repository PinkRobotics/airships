from pathlib import Path
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

ROOT=Path(__file__).resolve().parent
def read(name):return json.loads((ROOT/name).read_text())
ar=read("ARITHMETIC.json");su=read("SUPPLEMENT.json");tr=read("TOLERANCE-ROOTS.json")
fig,axes=plt.subplots(2,2,figsize=(12,8),layout="constrained")
for label,title,color in [
    ("S1-be-sphere-d16","Be sphere, 16.057 mm","#364fc7"),
    ("C3-be-cap2500-d16","Be 5 m cap, 16.057 mm","#1098ad"),
    ("S2-be-sphere-d9","Be sphere, 9.318 mm","#e8590c")]:
    r=read(f"fe-runs/{label}.json")
    axes[0,0].plot([-p["pole_dz_mm"] for p in r["path"]],[p["p_kPa"] for p in r["path"]],label=title,color=color)
axes[0,0].axhline(95.4608379139,color="#555555",ls="--",lw=1,label="Operating pressure")
axes[0,0].set(xlabel="Inward pole displacement (mm)",ylabel="Pressure (kPa)",title="Independent elastic equilibrium paths")
axes[0,0].legend(fontsize=8,loc="lower right")
for material,color in [("Be","#364fc7"),("5052-O","#e8590c")]:
    rows=[x for x in su["caps"] if x["material"]==material]
    axes[0,1].plot([x["diameter_m"] for x in rows],[(x["limit_ratio"]-1)*100 for x in rows],"o-",label=material,color=color)
axes[0,1].axhline(0,color="#777",lw=1)
axes[0,1].set(xlabel="Cap diameter (m)",ylabel="Pressure maximum difference (%)",title="Cap versus its matching full sphere")
axes[0,1].legend()
keys=["elastic_pressure_maximum_at_operating","outer_face_345MPa","core_W_typ_35psi","core_W_min_25psi"]
own=[5.823329047943682,1.2710684884226882,2.3773352438995956,1.8027456952092222]
ind=[tr[k]["amplitude_mm"] for k in keys]
x=np.arange(4)
axes[1,0].bar(x-.18,own,.36,color="#b0b8c4",label="Card interpolation")
axes[1,0].bar(x+.18,ind,.36,color="#364fc7",label="Independent direct solve")
axes[1,0].set(xticks=x,xticklabels=["Elastic peak","Face yield","Core typical","Core minimum"],ylabel="Dimple amplitude (mm)",title="Conditional dimple thresholds")
axes[1,0].legend(fontsize=8)
rig=ar["rig"][1:]
axes[1,1].plot([0,2,5,10],[r["gamma_Be_exact"] for r in rig],"o--",color="#b0b8c4",label="Be reference")
axes[1,1].plot([0,2,5,10],[r["gamma_5052_article"] for r in rig],"o-",color="#364fc7",label="Proposed 5052-O article")
axes[1,1].set(xlabel="Water head above pole (m)",ylabel="Gamma reachable",title="Rig reach with the article's denominator")
axes[1,1].legend(fontsize=8)
for ax in axes.flat:
    ax.grid(axis="y",alpha=.18)
    ax.spines["right"].set_visible(False);ax.spines["top"].set_visible(False)
fig.suptitle("CHECK055: numerical agreement and corrections\nConditional elastic models; no qualified physical capacity",fontsize=14)
fig.savefig(ROOT/"CHECK055-FIGURE.pdf")
fig.savefig(ROOT/"CHECK055-FIGURE.png",dpi=150)
print("Wrote CHECK055-FIGURE.pdf and .png")
