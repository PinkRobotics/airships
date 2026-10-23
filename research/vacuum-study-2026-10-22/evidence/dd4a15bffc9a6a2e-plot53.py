"""Standalone scientific figures from the completed settlement artifacts."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
probe = json.loads((ROOT/"THERMAL-PROBE.json").read_text())
rows = json.loads((ROOT/"RESIZED-CONSEQUENCES.json").read_text())
reference = json.loads((ROOT/"REFERENCE-THERMAL-ROWS.json").read_text())
palette = {"forced_conduction": "#be4d25", "mixed_conduction": "#167d8d",
           "forced_gap": "#d99362", "mixed_gap": "#79b8bb"}
labels = {"forced_conduction": "Forced, conduction",
          "mixed_conduction": "Mixed, conduction",
          "forced_gap": "Forced + gap term",
          "mixed_gap": "Mixed + gap term"}
plt.rcParams.update({"font.size": 10, "axes.spines.top": False,
                     "axes.spines.right": False, "figure.facecolor": "#fafafa",
                     "axes.facecolor": "#fafafa"})
fig, axes = plt.subplots(1, 3, figsize=(15, 4.8), constrained_layout=True)
order = ["forced_conduction", "mixed_conduction", "forced_gap", "mixed_gap"]
y = np.arange(4)
axes[0].barh(y, [probe[k]["gradient_K"][0] for k in order],
             color=[palette[k] for k in order], height=.62)
axes[0].set_yticks(y, [labels[k] for k in order])
axes[0].invert_yaxis()
axes[0].set_xlabel("Face gradient, K")
axes[0].set_title("The discrepancy is reproducible\nR10 historical white-finish geometry")
for j, k in enumerate(order):
    val = probe[k]["gradient_K"][0]
    axes[0].text(val+.004, j, f"{val:.6f}", va="center", fontsize=9)
axes[0].set_xlim(0, .56)
for model in order:
    points = sorted([r for r in reference if r["model"] == model and r["profile"] == "MLCCAg"],
                    key=lambda r:r["radius_m"])
    axes[1].plot([r["radius_m"] for r in points],
                 [r["values"]["min_outer_K"][0]-273.15 for r in points],
                 color=palette[model], ls="--" if model.endswith("gap") else "-",
                 marker="o", ms=3, label=labels[model])
axes[1].set_title("Cold-night reference temperature\nMultilayer CCAg/ITO, tc proportional to R")
axes[1].set_xlabel("Radius, m")
axes[1].set_ylabel("Minimum outer temperature, °C")
axes[1].legend(frameon=False, fontsize=8, loc="lower left")
cases = [(r,w,True,True,"bake") for r in [10,12,15] for w in ["ISA","optimistic"]]
x = np.arange(len(cases))
for j, model in enumerate(order):
    selected = {tuple(r["case"]): r for r in rows if r["model"] == model}
    delta = [selected[k]["payload_difference_kg"] for k in cases]
    axes[2].bar(x+(j-1.5)*.18, delta, width=.17, color=palette[model])
axes[2].axhline(0, color="#555555", lw=.8)
axes[2].set_xticks(x, [f"R{r}\n{'ISA' if w=='ISA' else 'Opt.'}" for r,w,_,_,_ in cases])
axes[2].set_ylabel("Payload change from filed thermal table, kg")
axes[2].set_title("Cost after resizing\n200°F cure included; bake, retained floor")
for ax in axes:
    ax.grid(axis="y", alpha=.12)
    ax.set_axisbelow(True)
fig.suptitle("MAINLINE-053 · Thermal boundary choices and their consequences", fontsize=15)
fig.supxlabel("QUESTIONABLE / PROJECTION · Numerical reconciliation does not establish installed-hull qualification", fontsize=9)
fig.savefig(ROOT/"THERMAL-SETTLEMENT.png", dpi=180)
fig.savefig(ROOT/"THERMAL-SETTLEMENT.svg")
fig.savefig(ROOT/"THERMAL-SETTLEMENT.pdf")
plt.close(fig)
print("Scientific figures written.")
