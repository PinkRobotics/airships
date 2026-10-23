"""Render the checked results with clear footer spacing."""
import os
os.environ.setdefault("MPLCONFIGDIR","unpublished-local-ref:b4499a42f3b2733e")
from pathlib import Path
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
MODELS=("forced_conduction","mixed_conduction","forced_gap","mixed_gap")
r=json.loads((ROOT/"RESULTS.json").read_text())
four=r["four_R10_historical_reference"]
summary=r["model_consequences"]
labels=["Forced / conduction","Mixed / conduction","Forced / gap .20","Mixed / gap .20"]
colors=["#245a81","#41816b","#629dc2","#86bca4"]
fig,axes=plt.subplots(2,2,figsize=(11,7.8),layout="constrained")
series=[
 ([four[m]["gradient_K"] for m in MODELS],"R10 reference: face gradient","K"),
 ([four[m]["swing_K"] for m in MODELS],"R10 reference: day–night swing","K"),
 ([-summary[m]["minimum_payload_delta_kg"] for m in MODELS],"Largest resized payload loss","kg"),
 ([(1-summary[m]["minimum_scarf_SF"])*100 for m in MODELS],"Largest frozen scarf deficit","percent below SF=1")]
for ax,(vals,title,unit) in zip(axes.flat,series):
    ax.barh(labels,vals,color=colors)
    ax.invert_yaxis();ax.set_title(title,loc="left",fontsize=11,fontweight="bold")
    ax.set_xlabel(unit);ax.spines[["top","right"]].set_visible(False)
    ax.set_xlim(0,max(vals)*1.32)
    for j,v in enumerate(vals):
        ax.text(v+max(vals)*.025,j,f"{v:.6f}",va="center",fontsize=9)
fig.suptitle("CHECK-053 · independent reproduction",fontsize=17,fontweight="bold")
fig.text(.5,-.075,"Thermal probe: historical white finish, foil density 2640 kg/m³. Payload/bond: selected multilayer finish.\nConditional scalar models; physical qualification remains open.",ha="center",fontsize=9)
for suffix in ("pdf","svg","png"):
    fig.savefig(ROOT/f"CHECK-053.{suffix}",dpi=170,bbox_inches="tight")
plt.close(fig)
