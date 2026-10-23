import json,math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from check45 import ROOT,growth

load=lambda name:json.loads((ROOT/name).read_text())
c=load("inputs/owner/COMPUTE.json");f=load("FRAME-RESULTS.json")["radial_planar"]
l=load("LEAK-RESULTS.json")
plt.rcParams.update({"font.size":9,"axes.titlesize":11,"axes.labelsize":9,
 "font.family":"DejaVu Sans","axes.spines.top":False,"axes.spines.right":False})
fig,axs=plt.subplots(1,3,figsize=(15,4.8),layout="constrained")
navy="#234464";teal="#008782";orange="#c06c27"
ax=axs[0]
diam=np.linspace(28,180,1000)
for edge,color,title in [("clamped",navy,"Clamped"),("ss",teal,"Simply supported")]:
    depths=[growth(d/2000,edge) for d in diam]
    ax.plot(diam,[v*1000 if v is not None else np.nan for v in depths],color=color,label=title)
for text,key,dy in [("Fluid","fluid rho v2",-10),("Shi","Shi-calibrated k rho v2",5),("All energy","all energy to the panel",5)]:
    row=c["p2"]["threats"][6]["readings"][key]
    x=row["crushed_diameter_m"]*1000;y=row["depth_m"]*1000
    ax.scatter(x,y,color=orange,zorder=5,s=30)
    ax.annotate(text,(x,y),xytext=(7,dy),textcoords="offset points",color=orange,fontsize=8)
ax.axhline(23.237218,color="#9a9a9a",ls=":",lw=1)
ax.set(xlim=(25,180),ylim=(.08,30),yscale="log",xlabel="Crushed diameter (mm)",ylabel="Dent depth (mm)",
       title="P2 growth thresholds reproduce")
ax.legend(loc="lower right",frameon=False,fontsize=8)
ax.grid(alpha=.15,which="both")

ax=axs[1];labels=[];tensions=[];colors=[]
for key,section in f.items():
    for i,row in enumerate(section["cases"]):
        labels.append(key+"-"+str(i+1));tensions.append(row["tension_max_Pa"]/1e6);colors.append(navy if key=="f4" else teal)
ax.bar(np.arange(len(labels)),tensions,color=colors,width=.7)
ax.axhspan(160,320,color=orange,alpha=.12,label="Cited 160–320 MPa range")
ax.axhline(947.133864,color=orange,lw=1,ls="--",label="Filed selected-case maximum")
ax.set_xticks(np.arange(len(labels)),labels,rotation=60,ha="right",fontsize=7)
ax.set(ylabel="Peak tensile stress (MPa)",ylim=(0,1150),
       title="Additional member removals matter")
ax.legend(loc="upper right",frameon=False,fontsize=7)
ax.grid(axis="y",alpha=.15)

ax=axs[2]
for drag,color in [(.47,navy),(.2,teal)]:
    xs=[];ys=[]
    for row in l["holes"]:
        xs.append(row["hole_m"]*1000);ys.append(-row[f"p2_cd{drag}"]["v_end_m_s"])
    for row in l["big"]:
        if row["cd_drag"]==drag:
            xs.append(math.sqrt(4*row["area_m2"]/math.pi)*1000);ys.append(-row["v_end_m_s"])
    xy=sorted(zip(xs,ys));ax.loglog(*zip(*xy),marker="o",markersize=3,color=color,label=f"Drag coefficient {drag}")
ax.axhline(.914,color=orange,ls="--",lw=1)
ax.axvspan(63.100934,65.606770,color=orange,alpha=.2)
ax.annotate("0.914 m/s test reference",(2,.914),xytext=(0,5),textcoords="offset points",fontsize=8,color=orange)
ax.set(xlabel="Equivalent fixed-hole diameter (mm)",ylabel="Model touchdown speed (m/s)",ylim=(1e-4,80),
       title="Leak headline arithmetic reproduces")
ax.legend(loc="lower right",frameon=False,fontsize=8)
ax.grid(alpha=.15,which="both")
fig.suptitle("CHECK-045  •  independent numerical audit",fontsize=15,fontweight="bold")
fig.supxlabel("All panels: conditional models, not installed allowables. Leak panel retains the filed gross-mass and centre-height-zero convention.",fontsize=9)
fig.savefig(ROOT/"check45.png",dpi=150)
fig.savefig(ROOT/"check45.svg")
