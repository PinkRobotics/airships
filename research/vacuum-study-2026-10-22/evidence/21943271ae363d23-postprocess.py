#!/usr/bin/env python3
"""Reproducible tables, plots and numerical checks for completed MAINLINE-047."""
import csv, datetime, gzip, hashlib, json, math, os, pathlib, re
os.environ.setdefault("OPENBLAS_NUM_THREADS","1")
from data_tools import ROOT,P0,summary,path,at_pressure,py_estimate,rms_factor,sweep_rows

[withheld: private task or principal quotation; scientific result/status retained elsewhere]

def plots(rows,bounds,calibration):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    labels=[("old021",332.2164186283597),("current",347.1529189444301),
            ("old021b",401.8559050423529),("fullwave",2181.4248249368884)]
    colors={255:"#b34335",300:"#bc790c",345:"#246392"}
    fig,axes=plt.subplots(2,4,figsize=(16,8),sharey=True,sharex=True)
    for col,(label,width) in enumerate(labels):
        for row,m in enumerate(["W","L"]):
            ax=axes[row,col]
            for y in [255,300,345]:
                pts=sorted([r for r in rows if r["yield_MPa"]==y and r["meridian"]==m
                            and (r["amplitude_mm"]==0 or abs(r["width_mm"]-width)<1e-5)],
                           key=lambda r:r["amplitude_mm"])
                x=[r["amplitude_mm"] for r in pts]
                ax.plot(x,[r["endpoint_kPa"] for r in pts],"--",color=colors[y],alpha=.8)
                ys=[py_estimate(r) for r in pts]
                ax.plot(x,ys,"o-",ms=3,color=colors[y],label=f"{y} MPa yield")
                for r,z in zip(pts,ys):
                    b=r["first_yield_bracket_kPa"]
                    if b:ax.vlines(r["amplitude_mm"],b[0],b[1],color=colors[y],alpha=.6,lw=.7)
            ax.axhline(P0,color="#242424",lw=1)
            ax.axhline(P0*1.05,color="#666666",lw=.8,ls=":")
            ax.set_xscale("symlog",linthresh=1);ax.set_ylim(0,120)
            ax.set_title(f"{m} meridian · w={width:.1f} mm")
            ax.grid(alpha=.15)
            if col==0:ax.set_ylabel("Pressure (kPa)")
            if row==1:ax.set_xlabel("Dimple amplitude (mm)")
    axes[0,0].legend(fontsize=8)
    fig.suptitle("P2 plastic-face sweep · solid: first-yield estimate/bracket · dashed: numerical endpoint",fontsize=12)
    fig.text(.5,.015,"QUESTIONABLE/PROJECTION · horizontal lines: service and 1.05× service · connecting lines are guides between sampled amplitudes",ha="center",fontsize=9)
    fig.tight_layout(rect=[0,.035,1,.95])
    fig.savefig(ROOT/"PRESSURE-SWEEP.pdf");fig.savefig(ROOT/"PRESSURE-SWEEP.png",dpi=150);plt.close(fig)
    if not bounds:
        return
    narrow=[g for g in bounds if g["label"]!="fullwave"]
    fig,ax=plt.subplots(figsize=(10,5.5))
    for i,g in enumerate(narrow):
        for sf,offset,color in [(1.,-.16,"#246392"),(1.05,.16,"#94703b")]:
            b=next(b for b in g["boundaries"] if b["SF"]==sf and b["yield_screen_MPa"]==345)
            mid=b["amplitude_estimate_mm"];lo=b["passing_amplitude_mm"];hi=b["failing_amplitude_mm"]
            ax.errorbar(i+offset,mid,yerr=[[mid-lo],[hi-mid]],fmt="o",color=color,
                        capsize=4,label=f"SF {sf:g}" if i==0 else None)
        c=next(c for c in calibration if c["label"]==g["label"] and c["meridian"]==g["meridian"])["refined_10percent_SF1"]
        if c.get("amplitude_estimate_mm") is not None:
            ax.plot(i,c["amplitude_estimate_mm"],"v",color="#a34439",
                    label="SF 1; endpoint ÷ 1.10" if i==0 else None)
    ax.set_xticks(range(len(narrow)),[f"{g['width_mm']:.0f} mm\n{g['meridian']}" for g in narrow])
    ax.set_ylabel("Dimple amplitude (mm)");ax.set_ylim(bottom=0);ax.grid(axis="y",alpha=.2)
    ax.set_title("345 MPa case: tested tolerance brackets at the three narrow widths")
    ax.legend()
    fig.text(.5,.015,"255 and 300 MPa: no admissible perfect sphere · calibration transfer is conditional · these are model tolerances",ha="center",fontsize=9)
    fig.tight_layout(rect=[0,.035,1,1])
    fig.savefig(ROOT/"TOLERANCE.pdf");fig.savefig(ROOT/"TOLERANCE.png",dpi=150);plt.close(fig)
if __name__=="__main__":main()
