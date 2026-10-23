"""Optional standalone plot of the frozen MAINLINE-028 results."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
data = json.loads((ROOT / "RESULTS.json").read_text())
panels = ["small_planning", "stock_envelope", "1m_projection",
          "2m_projection", "4m_projection"]
labels = ["0.305 × 0.610", "0.610 × 1.829", "1 × 1", "2 × 2", "4 × 4"]
routes = [
    ("lab8_scarf", "8 g/m² edge deposit + scarf", "#11796b", "-"),
    ("af015_scarf", "73.24 g/m² AF film + scarf", "#3267ad", "-"),
    ("hex100_scarf", "100 g/m² HexBond film + scarf", "#b07419", "-"),
    ("lab8_eb_eta08", "8 g/m² deposit + EB, 80% retention", "#a63d4b", "--"),
]
fig, axes = plt.subplots(1, 2, figsize=(13.2, 5.9))
fig.patch.set_facecolor("#fbfbfa")
for ax in axes:
    ax.set_facecolor("#fbfbfa")
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", color="#ddddda", linewidth=.6)
    ax.set_xticks(range(len(panels)), labels, fontsize=9)
    ax.set_xlabel("Raw panel blank dimensions, m (all projected)", labelpad=10)
for route, label, color, style in routes:
    rows = [next(x for x in data["cases"] if x["panel"] == p and x["route"] == route)
            for p in panels]
    axes[0].plot([x["fixed_geometry"]["total_kg"] for x in rows],
                 marker="o", color=color, linestyle=style, label=label)
    axes[1].plot([x["reoptimized_5pct_margin"]["evaluation"]["least_known_mode_SF"]
                  for x in rows], marker="o", color=color, linestyle=style)
axes[0].axhline(data["case"]["joint_allowance_kg"], color="#333333",
               linestyle=":", linewidth=1.3)
axes[0].text(3.98, 220.5, "216.43 kg allowance", ha="right", fontsize=9)
axes[0].set_ylim(0, 355)
axes[0].set_ylabel("Installed joining inventory in model, kg")
axes[0].set_title("Mass at the original 021 geometry", loc="left", fontsize=12)
axes[1].axhline(1, color="#333333", linestyle=":", linewidth=1.3)
axes[1].set_ylim(.82, 1.065)
axes[1].set_ylabel("Least modeled SF (unknown bond modes excluded)")
axes[1].set_title("Faces/core resized to preserve 5% float margin", loc="left", fontsize=12)
fig.suptitle("MAINLINE-028: joining mass can fit; interface performance remains unproved",
             fontsize=14, x=.06, ha="left", y=.98)
handles, legend_labels = axes[0].get_legend_handles_labels()
fig.legend(handles, legend_labels, loc="lower center", ncol=2,
           bbox_to_anchor=(.5, .075), frameon=False, fontsize=10)
fig.text(.06, .025,
         "All hull routes are PROJECTION. Same corrected 021 material/core; gamma 0.595318 and wrinkle coefficient 0.370681 held fixed.",
         fontsize=9, color="#444444")
fig.subplots_adjust(left=.065, right=.98, top=.86, bottom=.29, wspace=.27)
fig.savefig(ROOT / "joining-trade.png", dpi=170)
fig.savefig(ROOT / "joining-trade.svg")
plt.close(fig)
