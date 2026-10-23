import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
R=json.loads((ROOT/"RESULTS.json").read_text())
data={x["id"]:x for x in R["models"]}
fig,axes=plt.subplots(1,2,figsize=(12,4.9),sharey=True,layout="constrained")
groups=[
    [("R10_af015_scarf_catalog_E_full","AF015 + scarf","#1864ab"),
     ("R10_af015_scarf_primer5_catalog_E_full","AF015 + primer + scarf","#e67700"),
     ("R10_lab8_eb_eta1_catalog_E_full","Light bond + ideal weld","#087f5b")],
    [("R20_027_full","027 original elastic inputs","#1864ab"),
     ("R20_handbook_elastic","Sheet handbook scalar elasticity","#c92a2a")]]
for ax,items,title in zip(axes,groups,["R10 — catalog E=290 GPa","R20 — inherited 027 joining"]):
    for key,label,color in items:
        points=data[key]["points"]
        ax.plot([p["Fcy_Pa"]/1e6 for p in points],[p["least_SF"] for p in points],
                marker="o",markersize=3,lw=1.8,color=color,label=label)
        t=data[key]["threshold"]["Fcy_Pa"]/1e6
        ax.scatter([t],[1],marker="x",s=55,color=color,zorder=6)
    ax.axhline(1,color="#444",linestyle="--",lw=1)
    ax.axvline(345,color="#999",linestyle=":",lw=1)
    ax.axvline(379.2,color="#999",linestyle=":",lw=1)
    ax.set(title=title,xlabel="Assumed effective compression strength (MPa)",xlim=(250,402))
    ax.grid(alpha=.15)
    ax.legend(loc="lower right",fontsize=8)
axes[0].set(ylabel="Maximum modeled safety factor",ylim=(.68,1.30))
fig.suptitle("MAINLINE-036 · PROJECTION — no qualified thin-sheet biaxial allowable",fontsize=12)
fig.supxlabel("Full projected buckling/wrinkling envelope. × = SF1 threshold.\nDotted lines: 345 MPa tensile proxy; 379.2 MPa historical thicker-sheet compression.",fontsize=9)
fig.savefig(ROOT/"compression-sensitivity.png",dpi=180)
fig.savefig(ROOT/"compression-sensitivity.pdf")
print("Saved compression-sensitivity.png and .pdf")
