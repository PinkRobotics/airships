"""Conditional compression targets. Execute only through run_job.py/simjob."""
from pathlib import Path
import csv
import json
import math
import numpy as np
from scipy.special import logsumexp
from scipy.optimize import brentq
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parent
TAG="QUESTIONABLE / PROJECTION"
rows=[]
checks=[]
summaries=[]

def check(name,a,b,rtol=1e-10,atol=1e-13):
    good=bool(abs(a-b)<=atol+rtol*abs(b))
    checks.append(dict(name=name,actual=float(a),expected=float(b),passed=good))
    assert good,(name,a,b)

for reserve in ["5","019"]:
    for load in ["operating","own_screen"]:
        with (ROOT/f"intake/043-fold/MEMBERS-f5-{reserve}-{load}.csv").open() as f:
            data=list(csv.DictReader(f))
        stress=np.array([float(x["peak_compression_Pa"]) for x in data])
        volume=np.array([float(x["volume_m3"]) for x in data])
        length=np.array([float(x["arc_length_m"]) for x in data])
        area=volume/length
        assert len(data)==750 and np.all(stress>0) and np.all(area>0)
        logstress=np.log(stress/1e9)
        out=dict(reserve=reserve,load=load,q=float(data[0]["q"]),
                 peak_compression_GPa=float(stress.max()/1e9),
                 area_m2=float(area.mean()),actual_length_m=[float(length.min()),float(length.mean()),float(length.max())])
        for m in range(5,41):
            for pf in [1e-3,1e-6]:
                target=-math.log1p(-pf)
                logh=math.log(target)
                whole=math.exp((logsumexp(m*logstress)-logh)/m)
                # Same statistical population, stress and uniform peak envelope.
                # Unlike the equal complete-member convention, length is explicit.
                s3=math.exp((logsumexp(m*logstress+np.log(length/3))-logh)/m)
                coupon=math.exp((logsumexp(m*logstress+np.log(volume/1e-6))-logh)/m)
                all3=whole*(float(area.mean())*3/1e-6)**(1/m)
                for ref in [whole]:
                    back=-math.expm1(-float(np.exp(m*(logstress-math.log(ref))).sum()))
                    check(f"inverse-{reserve}-{load}-{m}-{pf}",back,pf)
                check(f"size-{reserve}-{load}-{m}-{pf}",s3*(float(area.mean())*3/1e-6)**(1/m),coupon)
                rows.append(dict(tag=TAG,reserve=reserve,load=load,q=out["q"],m=m,frame_Pf_target=pf,
                    equal_complete_member_scale_GPa=whole,
                    common_3m_reference_scale_GPa=s3,
                    coupon_1cm3_scale_GPa=coupon,
                    hypothetical_all_750_lengths_3m_coupon_scale_GPa=all3,
                    three_m_member_volume_cm3=float(area.mean())*3e6,
                    coupon_to_3m_strength_retention=(float(area.mean())*3e6)**(-1/m)))
        h10=float(np.exp(10*(logstress-math.log(3.9))).sum())
        out["hypothetical_whole_3p9_m10_Pf"]=-math.expm1(-h10)
        out["hypothetical_coupon1cm3_3p9_m10_Pf"]=-math.expm1(-float((volume/1e-6*np.exp(10*(logstress-math.log(3.9)))).sum()))
        out["m_required_at_hypothetical_3p9_GPa"]={}
        for basis,weight in [("equal_complete_member",np.zeros(750)),("coupon_1cm3",np.log(volume/1e-6))]:
            out["m_required_at_hypothetical_3p9_GPa"][basis]={}
            for pf in [1e-3,1e-6]:
                target=math.log(-math.log1p(-pf))
                m=brentq(lambda m: logsumexp(m*(logstress-math.log(3.9))+weight)-target,1.,100.)
                out["m_required_at_hypothetical_3p9_GPa"][basis][str(pf)]=m
                check(f"m-root-{reserve}-{load}-{basis}-{pf}",
                      math.exp(logsumexp(m*(logstress-math.log(3.9))+weight)), -math.log1p(-pf))
        summaries.append(out)

with (ROOT/"TARGET-SURFACE.csv").open("w") as f:
    w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)
(ROOT/"TARGETS.json").write_text(json.dumps(dict(tag=TAG,actual_frame_Pf=None,
    hypothesis="independent compression Weibull; each member at its own peak stress",
    summary=summaries,rows=rows,checks=checks),indent=2)+"\n")

plt.rcParams.update({"font.size":10})
fig,ax=plt.subplots(1,2,figsize=(11.4,4.8),layout="constrained")
for reserve,color in [("5","#1565a7"),("019","#b7501b")]:
    for pf,style in [(1e-3,"-"),(1e-6,"--")]:
        sub=[x for x in rows if x["reserve"]==reserve and x["load"]=="own_screen" and x["frame_Pf_target"]==pf]
        for axis,key in [(ax[0],"equal_complete_member_scale_GPa"),(ax[1],"coupon_1cm3_scale_GPa")]:
            axis.plot([x["m"] for x in sub],[x[key] for x in sub],style,color=color,
                      label=f"{reserve}% reserve" if False else f"reserve {reserve}; Pf={pf:g}")
for axis in ax:
    axis.set(xlabel="Assumed compression Weibull modulus m",ylabel="Required characteristic compression (GPa)",yscale="log")
    axis.grid(alpha=.2);axis.legend(fontsize=8)
ax[0].axhline(3.9,color="#555555",lw=.8,label="Hypothesis only")
ax[0].set_title("Equal complete-member calibration")
ax[1].set_title("1 cm³ coupon; actual member volumes")
fig.suptitle("041 f5 at each point's own screen — QUESTIONABLE / PROJECTION\nNo measured tube compression distribution is asserted",fontsize=12)
fig.savefig(ROOT/"TARGET-SURFACE.png",dpi=180)
fig.savefig(ROOT/"TARGET-SURFACE.pdf")
print(json.dumps(dict(rows=len(rows),checks=len(checks),summary=summaries),indent=2))
