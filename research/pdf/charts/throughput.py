#!/usr/bin/env python3
"""The headline: sustained delivery, and where the cycle minutes go."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _style import *          # noqa
import matplotlib.pyplot as plt

C = figures()['classes']
IDS = ['P100', 'P1000', 'P10000']
NAMES = {'P100': 'P-100', 'P1000': 'P-1000', 'P10000': 'P-10000'}

fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 2.65), gridspec_kw={'width_ratios': [1, 1.35]})

# --- left: sustained delivery, log scale because the classes span two decades -------------
# A DOT PLOT, not bars, because the axis is logarithmic. A bar encodes quantity as LENGTH, so a
# log axis makes it lie: 13,183 against 175 is 75x and the bars read about 3x. A dot encodes
# position only, which a log axis does not distort — and the axis label says "log" either way.
tph = [C[i]['cycle']['tph'] for i in IDS]
for x, v, col in zip(range(3), tph, [ACCENT, COOL, COOL]):
    a1.plot([x, x], [80, v], color=RULE, lw=1.0, zorder=1)
    a1.plot([x], [v], 'o', ms=9 if x == 0 else 7, color=col, zorder=3,
            markeredgecolor='white', markeredgewidth=0.8)
    a1.text(x, v * 1.35, f'{v:,}', ha='center', va='bottom', fontsize=9.0,
            fontweight='bold' if x == 0 else 'normal', color=INK)
a1.set_yscale('log')
a1.set_ylim(80, 60000)
a1.set_xlim(-0.6, 2.6)
a1.set_xticks(range(3))
a1.set_xticklabels([NAMES[i] + ('\nreference' if i == 'P100' else '') for i in IDS],
                   fontsize=8.6, color=INK)
a1.set_yticks([100, 1000, 10000]); a1.set_yticklabels(['100', '1,000', '10,000'])
a1.set_ylabel('tonnes per hour, sustained  (log scale)')
a1.set_title('Delivered per hour', loc='left', pad=9)
bare(a1)

# --- right: the cycle, and how little of it is transit --------------------------------------
PH = [('SOURCE_APPROACH', 'approach + stop', COOL_L),
      ('WATER_FILL', 'fill', COOL),
      ('OUTBOUND_TRANSIT', 'outbound', MUTED),
      ('WATER_RELEASE', 'release', ACCENT),
      ('BUOYANCY_ESCAPE', 'escape', ACCENT_L),
      ('RETURN_TRANSIT', 'return', FAINT)]
for row, cid in enumerate(IDS):
    d = C[cid]['cycle']['durations']
    left = 0.0
    for k, lab, colour in PH:
        w = d[k]
        a2.barh(-row, w, left=left, height=0.55, color=colour, edgecolor='white', linewidth=0.8)
        if w > 3.4:
            a2.text(left + w / 2, -row, f'{w:.1f}', ha='center', va='center', fontsize=7.2,
                    color='white', fontweight='bold')
        left += w
    a2.text(left + 0.7, -row, f'{left:.1f} min', va='center', fontsize=8.4,
            color=INK, fontweight='bold')
a2.set_yticks([0, -1, -2]); a2.set_yticklabels([NAMES[i] for i in IDS], fontsize=8.6, color=INK)
a2.set_xlim(0, 56); a2.set_ylim(-2.6, 0.85)
a2.set_xlabel('minutes')
a2.set_title('One cycle, 15 km each way', loc='left', pad=9)
bare(a2, left=False)
handles = [plt.Rectangle((0, 0), 1, 1, color=c) for _, _, c in PH]
a2.legend(handles, [l for _, l, _ in PH], ncol=6, loc='upper right',
          bbox_to_anchor=(1.02, 1.20), fontsize=6.6, handlelength=0.8,
          handleheight=0.9, columnspacing=1.0, borderpad=0)
save(fig, 'throughput')
