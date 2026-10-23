#!/usr/bin/env python3
from check_model import *
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fixed=read("FIXED-CHECK.json");a=read("ACCOUNTS-CHECK.json")
radii=[10,12,15,20,30]
plt.rcParams.update({"font.size":10,"axes.spines.top":False,"axes.spines.right":False})
fig,axes=plt.subplots(1,2,figsize=(11,4.6))
for i,R in enumerate(radii):
    row=next(x for x in fixed["boundaries"] if x["R_m"]==R and x["z_m"]==100)
    family=next(x for x in a["direct_family_boundaries"] if x["R_m"]==R and x["z_m"]==100)
    axes[0].plot([row["conservative_cold_offset_K"],row["worst_P_RH_upper_offset_K"]],[i,i],
        lw=7,color="#245b78",solid_capstyle="round",label="One fixed build" if i==0 else None)
    axes[0].scatter([family["checker_direct_offset_K"]],[i],marker=">",s=80,color="#b56b16",
        label="Reoptimized family upper limit" if i==0 else None)
    water=next(x["checker"] for x in a["dew_accounts"] if x["checker"]["R_m"]==R and x["checker"]["case"]=="clear_saturated")
    axes[1].barh(i,water["total_water_capacity_kg_m2"],height=.38,color="#cbd8df",
        label="Total water capacity at night density" if i==0 else None)
    axes[1].scatter(water["deposit_kg_m2"],i,color="#a53730" if i==0 else "#245b78",s=48,zorder=3,
        label="12-hour deposit (red exceeds capacity)" if i==0 else None)
    axes[1].annotate(f"{water['dry_start_payload_kg']:+,.0f} kg",
        (max(water["total_water_capacity_kg_m2"],water["deposit_kg_m2"])+.015,i),va="center",fontsize=9)
for ax in axes:
    ax.set_yticks(range(5),[f"R {R} m" for R in radii])
    ax.invert_yaxis();ax.grid(axis="x",alpha=.2);ax.set_axisbelow(True)
    ax.legend(loc="lower left",bbox_to_anchor=(0,1.02),frameon=False,fontsize=8)
axes[0].set_xlabel("ISA temperature offset at 100 m (K)")
axes[0].set_title("Common pressure/RH envelope",loc="left",pad=48,fontweight="bold")
axes[1].set_xlabel("Water per whole-sphere area (kg/m²)")
axes[1].set_xlim(0,1.)
axes[1].set_title("Saturated-clear night, initially dry",loc="left",pad=48,fontweight="bold")
fig.text(.5,.015,"Independent CHECK050 • QUESTIONABLE inputs / PROJECTION results • installed-hull capability remains unqualified",
    ha="center",fontsize=8,color="#555555")
fig.tight_layout(rect=(0,.04,1,.94))
fig.savefig(B/"CHECK-HEADLINES.png",dpi=180)
fig.savefig(B/"CHECK-HEADLINES.pdf")
print("figure saved",flush=True)
