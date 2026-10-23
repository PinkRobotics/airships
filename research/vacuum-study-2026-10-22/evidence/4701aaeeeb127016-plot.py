"""Scientific comparison figure; numerical data come from PROPERTY-CHECKS.json."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

root=Path(__file__).resolve().parent
r=json.loads((root/"PROPERTY-CHECKS.json").read_text())
ids=["af015_scarf","af015_scarf_primer5","lab8_eb_eta1","lab8_scarf"]
labels=["AF + scarf","AF + scarf\n+ primer","Lab + ideal\nweld","Lab + scarf"]
joined={x["route"]:x for x in r["searches"] if x["joint_screen_enforced"]}
six={x["route"]:x for x in r["searches"] if not x["joint_screen_enforced"]}
six["lab8_eb_eta1"]=joined["lab8_eb_eta1"]
full={(x["route"],x["material"]):x for x in r["full_named_maxima"]}
plt.rcParams.update({"font.size":11,"axes.spines.top":False,"axes.spines.right":False,
                     "axes.titleweight":"bold","svg.fonttype":"none"})
fig,axes=plt.subplots(1,2,figsize=(13,5.7))
x=np.arange(4); w=.35
colors=["#346991","#c56638"]
for ax in axes:
    ax.set_axisbelow(True)
    ax.yaxis.grid(True,alpha=.18)
    ax.axhline(1,color="#31383f",ls="--",lw=1.3)
    ax.set_xticks(x,labels)
    ax.set_ylim(0,1.36)
u6=[six[k]["least_set"]["min_max_usage"] for k in ids]
u7=[joined[k]["least_set"]["min_max_usage"] for k in ids]
bars1=axes[0].bar(x-w/2,u6,w,color=colors[0],label="Six continuum modes")
bars2=axes[0].bar(x+w/2,u7,w,color=colors[1],label="Seam screen enforced")
axes[0].set_title("Required adjustable optimism")
axes[0].set_ylabel("Largest log-share of allowed improvement")
axes[0].text(3.65,1.105,"Allowed limit = 1",ha="right",fontsize=9)
axes[0].legend(loc="upper left",frameon=False,fontsize=10)
s1=[full[(k,"SR200")]["least_SF"] for k in ids]
s2=[full[(k,"S200F255_sensitivity")]["least_SF"] for k in ids]
bars3=axes[1].bar(x-w/2,s1,w,color=colors[0],label="SR-200, full named endpoints")
bars4=axes[1].bar(x+w/2,s2,w,color=colors[1],label="255 MPa sensitivity")
axes[1].set_title("Best SF at full named endpoints")
axes[1].set_ylabel("Least of the seven numerical screens")
axes[1].legend(loc="upper left",frameon=False,fontsize=9)
for bars,ax in [(bars1,axes[0]),(bars2,axes[0]),(bars3,axes[1]),(bars4,axes[1])]:
    ax.bar_label(bars,fmt="%.3f",padding=3,fontsize=9)
fig.suptitle("Joining on the 019/021b reserve · stock envelope fixed",fontsize=16,fontweight="bold")
fig.text(.055,.07,"SR-200 scalar sheet model: E = 290 GPa, ν = 0.0752. AF's fixed thin-film optimism is excluded from the left-axis usage.",
         fontsize=10,color="#343d48")
fig.text(.055,.035,"Laboratory bond and ideal weld are projections. Unmeasured bond and local seam modes leave installed-hull SF unknown.",
         fontsize=10,color="#343d48")
fig.tight_layout(rect=(0,.12,1,.93),w_pad=3)
for suffix in ("png","svg"):
    fig.savefig(root/f"joining-021b-comparison.{suffix}",dpi=170,bbox_inches="tight")
plt.close(fig)
