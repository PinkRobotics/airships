#!/usr/bin/env python3
"""Draw the selected computed case as native SVG; requires Matplotlib.

Input is saved calculate.py JSON. No load cases are solved by this script.
"""
import argparse
import hashlib
import importlib.util
import json
from math import cos, pi, sin
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle

ROOT = Path(__file__).resolve().parent
matplotlib.rcParams.update({"svg.hashsalt":"R3-I013", "svg.fonttype":"none",
                           "font.size":10, "font.family":"DejaVu Sans"})


def arrow(ax, a, b, label, offset=(0,0), color="#334155"):
    ax.annotate("",xy=b,xytext=a,arrowprops={"arrowstyle":"<->","color":color,"lw":1})
    ax.text((a[0]+b[0])/2+offset[0],(a[1]+b[1])/2+offset[1],label,
            ha="center",va="bottom",color=color,fontsize=9,
            bbox={"facecolor":"white","edgecolor":"none","alpha":.85,"pad":1})


def save(fig, name, out, preview):
    target=out/f"{name}.svg"
    fig.savefig(target,metadata={"Date":None,"Creator":"R3-I013 draw.py"})
    target.write_text("\n".join(line.rstrip() for line in target.read_text().splitlines())+"\n")
    if preview:
        preview.mkdir(parents=True,exist_ok=True)
        fig.savefig(preview/f"{name}.png",dpi=125)
    plt.close(fig)


def draw(data, out, preview):
    spec=importlib.util.spec_from_file_location("i013_geometry",ROOT/"calculate.py")
    model=importlib.util.module_from_spec(spec);spec.loader.exec_module(model)
    assert data["calculator_sha256"]==hashlib.sha256((ROOT/"calculate.py").read_bytes()).hexdigest()
    case=min(data["cases"],key=lambda c:c["clearance"]["all_represented_paths"]["gap_bound_m"])
    gap=case["clearance"]["main_to_main"]
    caption=(f'{case["foundation"]} foundation · {case["altitude_m"]:g} m · {case["wind_ms"]:g} m/s '
             f'· gas +{case["gas_superheat_k"]:g} K · azimuth {case["wind_azimuth_deg"]:g}°')
    blue,orange,red,green="#1d4ed8","#c2410c","#be123c","#15803d"
    fig,axes=plt.subplots(1,2,figsize=(13,7),layout="constrained")
    for ax,vertical,name in ((axes[0],2,"Side elevation (x, z)"),(axes[1],1,"Plan projection (x, y)")):
        ax.add_patch(Circle((0,0),model.R,fill=False,color="#334155",lw=1.5))
        if vertical==2: ax.axhline(0,color="#94a3b8",ls=":",lw=.8)
        for centre in model.GEO["bag_centres"]:
            ax.add_patch(Circle((centre[0],centre[vertical]),model.GEO["bag_radius_m"],
                                edgecolor="#64748b",facecolor="#cbd5e1",alpha=.22,ls="--"))
        for hanger in case["hangers"]["rows"]:
            ax.plot([p[0] for p in hanger["points"]],[p[vertical] for p in hanger["points"]],color=green,lw=.55,alpha=.6)
        for duct in model.GEO["ducts"]:
            ax.plot([p[0] for p in duct["points"]],[p[vertical] for p in duct["points"]],color=red,lw=1.1,alpha=.75)
        for row in case["lines"]:
            color=blue if row["id"]%3==0 else orange
            ax.plot([p[0] for p in row["points"]],[p[vertical] for p in row["points"]],color=color,lw=1.6)
            station=row["station"]
            ax.plot([station["lower_pin"][0],station["upper_pin"][0]],
                    [station["lower_pin"][vertical],station["upper_pin"][vertical]],color="#0f172a",lw=2.2)
        for p in model.GEO["modules"]: ax.plot(p[0],p[vertical],"o",color="#0f172a",ms=3)
        ax.set_aspect("equal");ax.set_xlim(-44,44);ax.set_ylim((-48,48) if vertical==2 else (-44,44))
        ax.set_xlabel("x (m)");ax.set_ylabel("z (m)" if vertical==2 else "y (m)")
        ax.set_title(name,loc="left",fontweight="bold");ax.grid(alpha=.16)
    arrow(axes[0],(-38,43),(38,43),"76 m nominal diameter",offset=(0,.5))
    axes[0].text(0,-46,"8 apices: radius 18.908 m; z = −40.816 m",ha="center",fontsize=9)
    axes[1].text(0,41,"Projection overlaps do not imply 3D contact",ha="center",fontsize=9,color="#475569")
    fig.suptitle("R3-I013 · external main suspension and retained internal interfaces\n"+caption,fontsize=14,fontweight="bold")
    fig.supxlabel("Blue: inner lines   Orange: outer lines   Green: bag hangers   Red: pressure ducts\n"
                  "Dashed bag envelopes are design bounds, not solved surfaces. Pressure/contact compatibility remains UNKNOWN/FAIL.",fontsize=10)
    save(fig,"overview",out,preview)

    fig,(ax,detail)=plt.subplots(1,2,figsize=(13,7),layout="constrained",gridspec_kw={"width_ratios":[1,1.1]})
    ids=[int(gap[k].split("-")[1]) for k in ("a","b")]
    module=ids[0]//3;phi=module*pi/4;azimuth=(-sin(phi),cos(phi),0.)
    low=model.LAYOUT[ids[0]]["low"]
    def projection(p):return model.dot(model.sub(p,low),azimuth),p[2]-low[2]
    for i in ids:
        row=case["lines"][i];line=model.LAYOUT[i]
        ss=[j/150 for j in range(211)]
        xyz=[model.add(low,model.curve(row["n0_n"],row["q_n_per_reference_m"],s)) for s in ss]
        xy=[projection(p) for p in xyz]
        ax.plot([p[0] for p in xy],[p[1] for p in xy],color=orange,lw=1.3)
        # A physical-radius envelope in the displayed tangent/vertical projection.
        tangent=[model.unit(model.sub(xyz[min(j+1,len(xyz)-1)],xyz[max(0,j-1)])) for j in range(len(xyz))]
        normals=[]
        for t in tangent:
            tx,tz=model.dot(t,azimuth),t[2];n=(tx*tx+tz*tz)**.5
            normals.append((-tz/n*.04,tx/n*.04))
        edge=[(p[0]+n[0],p[1]+n[1]) for p,n in zip(xy,normals)]
        edge+=list(reversed([(p[0]-n[0],p[1]-n[1]) for p,n in zip(xy,normals)]))
        ax.add_patch(Polygon(edge,color=orange,alpha=.18,lw=0))
        chord=model.sub(row["station"]["lower_pin"],low)
        end=projection(model.add(low,model.mul(chord,1.4/row["free_length_m"])))
        ax.plot([0,end[0]],[0,end[1]],ls="--",color="#64748b",lw=.8)
    pa,pb=projection(gap["point_a_m"]),projection(gap["point_b_m"])
    for point in (pa,pb): ax.add_patch(Circle(point,.04,fill=False,color="#0f172a",lw=1.2))
    left,right=sorted((pa,pb))
    arrow(ax,(left[0],left[1]+.13),(right[0],right[1]+.13),f'Centres: {gap["centreline_separation_m"]*1000:.3f} mm',offset=(0,.025))
    arrow(ax,(left[0]+.04,left[1]-.11),(right[0]-.04,right[1]-.11),f'Surface: {(gap["centreline_separation_m"]-.08)*1000:.3f} mm',offset=(0,-.065))
    ax.annotate("Ø80 mm covered ropes",xy=left,xytext=(-.70,.86),arrowprops={"arrowstyle":"->","color":"#475569"},fontsize=9)
    ax.plot(0,0,"o",color="#0f172a")
    ax.text(0,-.10,"Common apex; first 0.500 m of rope coordinate excluded",ha="center",fontsize=8)
    ax.text(0,1.14,f'Bounded clearance: {gap["gap_bound_m"]*1000:.3f} mm\n'
            f'after {gap["curve_and_support_allowance_m"]*1000:.3f} mm curve/support allowance',ha="center",fontsize=10,fontweight="bold")
    ax.text(0,1.02,"Solid: loaded curve · dashed: loaded-end chord · sag not enlarged",ha="center",fontsize=8)
    sag=gap["sag_vector_a_m"]
    ax.text(0,-.23,f'Local sag vector (x,y,z): ({sag[0]*1000:+.3f}, {sag[1]*1000:+.3f}, {sag[2]*1000:+.3f}) mm',ha="center",fontsize=8)
    ax.set_aspect("equal");ax.set_xlim(-.78,.78);ax.set_ylim(-.28,1.30)
    ax.set_xlabel("Local azimuthal coordinate (m)");ax.set_ylabel("Height above module apex (m)");ax.grid(alpha=.15)
    ax.set_title(f'Loaded closest region · module {module}, lines {ids[0]} / {ids[1]}',loc="left",fontweight="bold")

    detail.add_patch(Rectangle((-.5,0),1,.07,facecolor="#94a3b8",edgecolor="#334155"))
    detail.plot([-1,1],[0,0],color=green,lw=2)
    pin=(0,.42)
    for foot in ((-.3,.07),(.3,.07)):
        detail.plot([foot[0],pin[0]],[foot[1],pin[1]],color=blue,lw=9,alpha=.3)
        detail.plot([foot[0],pin[0]],[foot[1],pin[1]],color=blue,lw=1)
    u=model.LAYOUT[ids[0]]["unit"];n=model.LAYOUT[ids[0]]["normal"]
    un=model.dot(u,n);ut=(1-un*un)**.5
    end=(-ut*1.4,.42-un*1.4)
    v=(end[0]/1.4,(end[1]-.42)/1.4);side=(-v[1],v[0])
    barrel_end=(pin[0]+v[0]*.85,pin[1]+v[1]*.85)
    polygon=[(p[0]+sign*.155/2*side[0],p[1]+sign*.155/2*side[1]) for p,sign in ((pin,1),(barrel_end,1),(barrel_end,-1),(pin,-1))]
    detail.add_patch(Polygon(polygon,facecolor="#cbd5e1",edgecolor="#334155"))
    detail.plot([barrel_end[0],end[0]],[barrel_end[1],end[1]],color="#64748b",lw=5)
    detail.plot([end[0],end[0]+v[0]*.4],[end[1],end[1]+v[1]*.4],color=orange,lw=3)
    detail.plot(*pin,"o",color="#0f172a");detail.plot(*end,"o",color="#0f172a")
    arrow(detail,(.65,0),(.65,.42),"420 mm pin offset",offset=(.05,.04))
    arrow(detail,(-.5,-.12),(.5,-.12),"1,000 mm spread plate",offset=(0,-.10))
    detail.text(-.45,.15,"4 × Ø100 / 8 mm legs\n600 mm square foot pattern",fontsize=9,ha="left")
    detail.text(-1.75,1.02,"24 supports, each with:\n70 mm Al spread plate\n155/125 mm cylinder barrel\n75 mm rod; 600 mm stroke\n1.1–1.7 m commanded pin length",fontsize=10,va="top")
    detail.text(-.4,-.41,"Finite translation and rotation of curtain/patch foundation\n0.5 / 2 / 10 MN/m; 0.2 / 1 / 5 MN m/rad\nMaterial values and secants remain assumptions",fontsize=9,ha="center")
    detail.set_aspect("equal");detail.set_xlim(-1.9,1.12);detail.set_ylim(-.55,1.45)
    detail.set_xlabel("Tangent coordinate (m)");detail.set_ylabel("Outward from nominal pressure skin (m)")
    detail.set_title("Reference support dimensions (two legs projected)",loc="left",fontweight="bold");detail.grid(alpha=.12)
    fig.suptitle("R3-I013 · closest cable region and priced support\n"+caption,fontsize=14,fontweight="bold")
    fig.supxlabel("Conditional geometric screen. The internal bag contact case fails; neither drawing establishes a compatible physical vehicle.",fontsize=10)
    save(fig,"closest-region",out,preview)


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input",type=Path)
    parser.add_argument("--out",type=Path,default=ROOT)
    parser.add_argument("--preview",type=Path)
    args=parser.parse_args()
    args.out.mkdir(parents=True,exist_ok=True)
    draw(json.loads(args.input.read_text()),args.out,args.preview)
