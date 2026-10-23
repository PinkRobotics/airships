"""Collect raw paths, comparisons and standalone figures without pressure fitting."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import re
import sys
import time

import numpy as np
import scipy
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent


def read(p):
    return json.loads(p.read_text())


def collect(final=False):
    cases=[]
    for p in sorted((ROOT/"runs").glob("*/RESULT.json")):
        r=read(p)
        history=[json.loads(s) for s in (p.parent/"PATH.jsonl").read_text().splitlines()]
        row={"name":p.parent.name,"result_path":str(p),
             "kind":"indentation imported geometry" if "indentation_parent" in r["parameters"] else "Gaussian imperfection",
             **r}
        if r["peak"]:
            pressure=r["peak"]["pressure_MPa"]
            row["paper_simulation_MPa"]=6.03
            row["gap_to_paper_percent"]=100*(pressure/6.03-1)
            row["first_screen_brackets_MPa"]={
                k:[v["last_below"]["pressure_MPa"],v["first_above"]["pressure_MPa"]]
                for k,v in r["first_events"].items()}
            row["maximum_equilibrium_relative_residual"]=max(h["relative_residual"] for h in history)
            row["postpeak_drop_percent"]=100*(1-history[-1]["pressure_MPa"]/pressure)
            row["maximum_accepted_foam_plastic_increment"]=max(
                (h.get("maximum_core_plastic_increment",0.) for h in history))
            row["raw_path_rows"]=len(history)
        cases.append(row)
    byname={r["name"]:r for r in cases}
    comparisons=[]
    pairs=[
        ("angular 96 to 192; core4", "base96c4","base192c4"),
        ("radial core4 to core8","base192c4","base192c8"),
        ("radial core8 to core12; faces2 to3","base192c8","base192c12"),
        ("angular 192 to384; core8","base192c8","base384c8"),
        ("plastic/displacement step refinement; core4","base96c4","guarded96c4"),
        ("plastic/displacement step refinement; core8","base192c8","guarded192c8-tight"),
        ("contact radius reading","indent-outer96p30k-pressure","indent-mid96p30k-pressure"),
        ("contact mesh refinement","indent-mid96p30k-pressure","indent-mid192p30k-pressure"),
        ("contact penalty refinement","indent-mid96p30k-pressure","indent-mid96p60k-pressure"),
    ]
    for label,first,second in pairs:
        if first in byname and second in byname:
            a=byname[first]["peak"]["pressure_MPa"];b=byname[second]["peak"]["pressure_MPa"]
            comparisons.append({"comparison":label,"first":first,"second":second,
                                "first_peak_MPa":a,"second_peak_MPa":b,
                                "relative_change_percent":100*(b/a-1)})
    indents=[]
    for p in sorted((ROOT/"runs").glob("*/INDENT-RESULT.json")):
        indents.append({"name":p.parent.name,**read(p)})
    resources=[]
    for p in sorted((ROOT/"logs").glob("*/RECEIPTS.json")):
        r=read(p);resource=p.parent/"resource.txt"
        peak=None
        if resource.exists():
            m=re.search(r"Maximum resident set size \(kbytes\):\s*(\d+)",resource.read_text())
            if m:peak=int(m.group(1))
        resources.append({"job":p.parent.name,"receipts":r,"job_peak_RSS_KiB":peak,
                          "scope":"Peak RSS is per admitted job, not attributed to each case in a sequential batch."})
    pending=[p.parent.name for p in (ROOT/"logs").glob("SOURCE-PINS.json")
             if not (p.parent/"RECEIPTS.json").exists()]
    result={"unit":"vacuum-mainline056-fe-benchmark-crushable-1020",
            "tag":"QUESTIONABLE / PROJECTION","certification":"none",
            "started_at":read(ROOT/"START.json")["started_at"],
            "collected_at":datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "work_complete":final and not pending,"pending_job_receipts":pending,
            "target_provenance":"6.03 MPa is EUCASS2023-367's pressure simulation, not a measured pressure test.",
            "pressure_cases":cases,"indentation_cases":indents,
            "mesh_step_contact_comparisons":comparisons,
            "linear_results":read(ROOT/"LINEAR.json"),
            "verification":read(ROOT/"VERIFICATION.json"),
            "contact_verification":read(ROOT/"CONTACT-VERIFICATION.json"),
            "source_pin_verification":read(ROOT/"CUSTODY-AUDIT.json"),
            "resource_jobs":resources,
            "environment":{"python":sys.version,"numpy":np.__version__,"scipy":scipy.__version__,
                           "matplotlib":matplotlib.__version__},
            "no_P2_gamma_release":True}
    (ROOT/"RESULTS.json").write_text(json.dumps(result,indent=2)+"\n")
    plots(cases)
    print(json.dumps({"cases":len(cases),"indentations":len(indents),"jobs":len(resources),
                      "pending":pending,"comparisons":comparisons},indent=2),flush=True)
    return result


def plots(cases):
    names={r["name"] for r in cases}
    selected=["base192c8","guarded192c8-tight","mid96c4-guarded",
              "indent-outer96p30k-pressure","indent-mid96p30k-pressure",
              "indent-mid192p30k-pressure"]
    fig,ax=plt.subplots(figsize=(9,5.2))
    for name in selected:
        if name not in names:continue
        rows=[json.loads(x) for x in (ROOT/"runs"/name/"PATH.jsonl").read_text().splitlines()]
        ax.plot([-r["outer_pole_mm"] for r in rows],[r["pressure_MPa"] for r in rows],label=name,lw=1.5)
    ax.axhline(6.03,color="black",linestyle="--",label="Paper simulation, 6.03 MPa")
    ax.set(xlabel="Additional inward outer-pole displacement (mm)",
           ylabel="External pressure (MPa)",title="Conditional plastic benchmark paths")
    ax.grid(alpha=.25);ax.legend(fontsize=7,loc="best")
    fig.text(.01,.005,"QUESTIONABLE / PROJECTION. Different radius and imperfection assumptions are separate cases.",fontsize=8)
    fig.tight_layout(rect=(0,.02,1,1))
    for ext in ["png","pdf"]:fig.savefig(ROOT/f"PRESSURE-PATHS.{ext}",dpi=170)
    plt.close(fig)
    visible=[r for r in cases if r["peak"] is not None and r["name"]!="pilot48"]
    fig,ax=plt.subplots(figsize=(9,max(5.2,.28*len(visible)+1.6)))
    ax.barh([r["name"] for r in visible],[r["peak"]["pressure_MPa"] for r in visible],color="#356b91")
    ax.axvline(6.03,color="black",linestyle="--",label="Paper simulation")
    ax.set(xlabel="Traced peak pressure (MPa)",title="Numerical scenarios; these are not a confidence interval")
    ax.grid(axis="x",alpha=.25);ax.legend(fontsize=8)
    ax.tick_params(axis="y",labelsize=7)
    fig.tight_layout()
    for ext in ["png","pdf"]:fig.savefig(ROOT/f"PEAK-COMPARISONS.{ext}",dpi=170)
    plt.close(fig)
    # Geometry comparison at the same outer radius: no displacement magnification.
    fig,ax=plt.subplots(figsize=(8,4.8))
    for name,label in [("indent-outer96p30k-indent","reconstructed indentation"),
                       ("indent48-indent","coarse indentation")]:
        p=ROOT/"runs"/name/"END.npz"
        if not p.exists():continue
        z=np.load(p);X=z["X"];x=X+z["u"].reshape(-1,2)
        # The outer/inner nodes are identified through element-row connectivity.
        conn=z["conn"]
        pars=read(p.parent/"INDENT-RESULT.json")["parameters"]
        nr=2*pars["nface"]+pars["ncore"]
        for j,ls in [(0,"--"),(nr-1,"-")]:
            # Select extremal thickness row nodes via true element edge.
            local=[0,4,1] if j==0 else [3,6,2]
            idx=np.unique(conn[j::nr][:,local])
            ids=idx[np.argsort(X[idx,0])]
            keep=X[ids,0]<12.
            ax.plot(x[ids[keep],0],x[ids[keep],1],ls,label=label+(" inner" if j==0 else " outer"))
    if ax.lines:
        angle=np.linspace(0,.29,200)
        offset=2.955*np.exp(-(42.8*angle/4.28)**2)
        for rad,label in [(42.8,"Gaussian outer"),(38.86,"Gaussian inner")]:
            ax.plot((rad-offset)*np.sin(angle),(rad-offset)*np.cos(angle),
                    ":",color="gray",label=label)
        ax.set(xlabel="Radial coordinate (mm)",ylabel="Axial coordinate (mm)",
               title="Stress-free imported pole geometry (actual scale)")
        ax.axis("equal");ax.grid(alpha=.25);ax.legend(fontsize=8);fig.tight_layout()
        for ext in ["png","pdf"]:fig.savefig(ROOT/f"IMPORTED-GEOMETRY.{ext}",dpi=170)
    plt.close(fig)


if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--final",action="store_true")
    args=p.parse_args();collect(args.final)
