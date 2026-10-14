#!/usr/bin/env python3
"""Dimension the one selected routing from saved JSON; do not execute a model."""
import json
import math
from pathlib import Path
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

data=json.loads(Path(sys.argv[1]).read_text())
base=json.loads((Path(__file__).resolve().parent/"baseline.json").read_text())
dest=Path(sys.argv[2]) if len(sys.argv)>2 else Path(__file__).resolve().parent
dest.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"svg.fonttype":"none","svg.hashsalt":"paired-racks-one-fixed-proposal"})
colours={1:"#156f9b",2:"#b25513"}
G=base["geometry"]


def save(fig,name):
    p=dest/(name+".svg")
    fig.savefig(p,metadata={"Date":None},facecolor="white")
    p.write_text("\n".join(x.rstrip() for x in p.read_text().splitlines())+"\n")
    fig.savefig(dest/(name+".png"),dpi=115,facecolor="white")
    plt.close(fig)


def line(ax,a,b,axes,**kw):
    ax.plot([a[axes[0]],b[axes[0]]],[a[axes[1]],b[axes[1]]],**kw)


fig,axs=plt.subplots(1,2,figsize=(17,10),layout="constrained")
for ax,axes,title in zip(axs,((0,1),(1,2)),("PLAN: x–y projection","ELEVATION: y–z projection")):
    ax.set_aspect("equal")
    ax.add_patch(Circle((0,0),G["radius_m"],fill=False,ec="#4e5560",lw=1.8))
    for i,c in enumerate(G["bag_centres"]):
        colour="#994f9c" if i in (0,3) else "#63845c"
        ax.add_patch(Circle((c[axes[0]],c[axes[1]]),G["bag_radius_m"],fill=False,ec=colour,ls="--",lw=1.3))
        ax.text(c[axes[0]],c[axes[1]],f"bag {i}",color=colour,ha="center",bbox={"facecolor":"white","alpha":.8,"edgecolor":"none"})
    for obj in data["objects"]:
        if obj["role"]=="frame": line(ax,obj["a"],obj["b"],axes,color="#69737b",lw=.6,alpha=.6)
        elif obj["role"]=="hull_attachment" and "curtain" in obj["id"]:
            line(ax,obj["a"],obj["b"],axes,color="#a59e80",lw=1.,alpha=.65)
    for d in base["ducts"]:
        for p,q in zip(d["points"],d["points"][1:]): line(ax,p,q,axes,color="#28a59d",lw=2.,alpha=.5)
    for row in data["routes"]:
        c=colours[row["bag"]]
        for a,b in row["segments"]: line(ax,a,b,axes,color=c,lw=1.7)
        for be in row["bends"]:
            pts=be["points"]
            ax.plot([p[axes[0]] for p in pts],[p[axes[1]] for p in pts],color=c,lw=1.8)
            ax.add_patch(Circle((be["centre"][axes[0]],be["centre"][axes[1]]),.6,fill=False,ec=c,lw=.7))
        old=G["hangers"][row["host"]]
        line(ax,old["low"],old["top"],axes,color="#b14b60",ls=":",lw=1.2)
        ax.plot(row["eye"][axes[0]],row["eye"][axes[1]],"o",color=c,ms=3)
        if axes==(0,1): ax.annotate(str(row["host"]),(row["eye"][0],row["eye"][1]),xytext=(3,4),textcoords="offset points",fontsize=9,color=c)
    ax.set(xlim=(-41,41),ylim=(-44,41),xlabel="xyz"[axes[0]]+", m",ylabel="xyz"[axes[1]]+", m",title=title)
    ax.grid(alpha=.15)
axs[0].annotate("Racks: x ±2.4 m, y = ±29 m\nFour grooves per rack, 1.2 m pitch",xy=(0,29),xytext=(-37,36),arrowprops={"arrowstyle":"->"},fontsize=10)
axs[1].annotate("23 m frames; guide intersections\nz = 4.0 and 22.5 m",xy=(29,22.5),xytext=(-37,36),arrowprops={"arrowstyle":"->"},fontsize=10)
fig.suptitle("Paired guide racks | Selected routing FAILS | Full installed bag envelopes retained",fontsize=16,weight="bold")
fig.supxlabel("Blue/orange: proposed eight routes. Red dots: original penetrations retained; no retirement credit. Grey: finite frames; ochre: new curtains.\nProjection crossings alone are not tests: finite 3D closest points establish the reported intersections. Loaded displacements remain UNKNOWN.",fontsize=11)
save(fig,"arrangement")


fig=plt.figure(figsize=(17,12),layout="constrained")
gs=fig.add_gridspec(2,2)
ax=fig.add_subplot(gs[0,0]); ax.set_aspect("equal")
# One actual guide in its own plane: basis incoming tangent, then turn normal.
row=data["routes"][0];be=row["bends"][0];c=be["centre"]
u=be["u_in"]; n=[(c[k]-be["entry"][k])/.45 for k in range(3)]
def project(p):
    w=[p[k]-c[k] for k in range(3)]
    return sum(w[k]*u[k] for k in range(3)),sum(w[k]*n[k] for k in range(3))
points=[project(p) for p in be["points"]]
ax.add_patch(Circle((0,0),.6,fill=False,ec="#777",ls="--",label="1.20 m swept guard envelope"))
ax.add_patch(Circle((0,0),.51,fill=False,ec="#69737b",lw=2))
ax.add_patch(Circle((0,0),.03,color="#555"))
ax.plot([p[0] for p in points],[p[1] for p in points],lw=4,color=colours[1])
entry=project(be["entry"]);leave=project(be["exit"])
ax.plot([entry[0]-.55,entry[0]],[entry[1],entry[1]],lw=4,color=colours[1])
out=[sum(be["u_out"][k]*basis[k] for k in range(3)) for basis in (u,n)]
ax.plot([leave[0],leave[0]+out[0]*.55],[leave[1],leave[1]+out[1]*.55],lw=4,color=colours[1])
ax.annotate("R = 450 mm\nD/d = 50",xy=points[8],xytext=(-1.15,.65),arrowprops={"arrowstyle":"->"})
ax.annotate("60 mm axle\n120 mm bearing span\n2 × 4 kg bearings",xy=(0,0),xytext=(.48,-.88),arrowprops={"arrowstyle":"->"})
ax.annotate("18 mm rope\n70 mm clamp envelope",xy=entry,xytext=(-1.2,-.95),arrowprops={"arrowstyle":"->"})
ax.set(xlim=(-1.3,1.25),ylim=(-1.15,1.15),xlabel="guide-plane incoming direction, m",ylabel="guide-plane normal, m",title=f"Host 9 lower guide: actual circular bend, {math.degrees(be['angle_rad']):.1f}°")
ax.grid(alpha=.15)

ax=fig.add_subplot(gs[0,1]);ax.set_aspect("equal")
for obj in data["objects"]:
    if obj["rack"]==-1 and obj["role"]=="frame": line(ax,obj["a"],obj["b"],(0,2),color="#69737b",lw=.8)
for r in (r for r in data["routes"] if r["rack"]==-1):
    for be in r["bends"]: ax.add_patch(Circle((be["centre"][0],be["centre"][2]),.6,fill=False,ec=colours[1]))
for root in data["states"][0]["racks"][0]["root_requirements"]:
    line(ax,root["root"],root["pad"],(0,2),color="#8b6b36",lw=3)
    ax.plot(root["pad"][0],root["pad"][2],"s",color="#8b6b36",ms=5)
ax.annotate("200 × 200 × 6 RHS\n100 × 100 × 4 paired braces\nGuide beams joined to all posts",xy=(-2.4,14),xytext=(-15,18),arrowprops={"arrowstyle":"->"},fontsize=9)
ax.annotate("4 root struts/rack: 150 × 150 × 6\n500 × 500 × 20 root plates\n1 m × 8 mm curtains to original anchors",xy=(4.9,0),xytext=(6,7),arrowprops={"arrowstyle":"->"},fontsize=9)
ax.annotate("4.8 m",xy=(-2.4,-1.3),xytext=(1.4,-1.3),arrowprops={"arrowstyle":"<->"})
ax.set(xlim=(-17,19),ylim=(-3,26),xlabel="x, m; rack depth 0.9 m along y",ylabel="z, m",title="One rack: finite member and root construction")
ax.grid(alpha=.15)

ax=fig.add_subplot(gs[1,0]);ax.axis("off")
st=data["states"][0];rr=st["rows"][0];ld=rr["guide_loads"][0]
lines=["COLD SEA-LEVEL NECESSARY DEMANDS",
       f"Host 9 rope: T = {rr['tension_n']/1000:.2f} kN; 1.5T = {rr['force_limit_n']/1000:.2f} kN",
       "18 mm straight-rope working screen: 38.17 kN → FAIL",
       f"Lower guide force = ({', '.join(f'{x/1000:.2f}' for x in ld['force_on_guide_n'])}) kN",
       f"Two bearings: each requires {ld['two_bearings_limit_each_n']/1000:.2f} kN at limit",
       f"60 mm axle limit bending: {ld['60mm_axle_bending_mpa']:.1f} MPa (unqualified)",
       "",
       "Each rack: four explicitly allocated root forces + pad moments.",
       "Finite beam, curtain and joint compliances are all charged.",
       "Demand/K exceeds the small-displacement envelope; it is not",
       "a predicted displacement. No elastic frame or global trim solution.",
       "",
       "Lower bridle: two 100 × 15 mm links, 250 mm tangential spacing",
       "either side of original lug; eye 150 mm radially outboard.",
       "20 kg links/pins/doublers + 12 kg socket per lower end.",
       "Residual bridle force and lower-bag moment remain unclosed."]
ax.text(.01,.98,"\n".join(lines),va="top",fontsize=11,linespacing=1.5)

ax=fig.add_subplot(gs[1,1]);ax.axis("off")
geo=data["geometry"];foreign=geo["foreign_upper_min"]
lines=["THE ROUTING CANNOT RETIRE THE OLD PENETRATIONS",
       "Exact lower-leg / own-bag gap: worst −3.205 m.",
       f"Host 23 / upper bag 0: {foreign['gap_m']:.3f} m finite-rope gap.",
       "Ropes 9 and 10 cross at (0.332, −25.603, 3.507) m.",
       "Adjacent lower-guard envelopes overlap by 0.240 m.",
       "±0.20 m hardware and bag envelopes make these worse.",
       "",
       f"Retained-hardware construction: {data['mass']['construction_kg']/1000:.3f} t",
       f"= 74.889 t − 0 retired + {data['mass']['new_items_kg']/1000:.3f} t selected new stock.",
       "Old 1.346 t liners, old ropes and actuators remain counted once.",
       "New stock is separate; no shared-actuator or liner-saving credit.",
       "Nominal pressure/flow carry only. Relief and trapped-bag FAIL.",
       "Actual contact hardware, bridle equilibrium and curtain peel: UNKNOWN.",
       "This cost bound is not an installable two-system equilibrium."]
ax.text(.01,.98,"\n".join(lines),va="top",fontsize=11,linespacing=1.5)
fig.suptitle("Guide and support details | Finite parts and failed load requirements | One unchanged routing",fontsize=16,weight="bold")
save(fig,"support-detail")
