#!/usr/bin/env python3
"""Where a cycle's energy goes. Drawn from figures.json, never from a typed array.

The class is a parameter because the P-100 is the reference ship and the P-10000 is the limit
case, and both figures appear in the reports. Everything about the layout is derived from the
data, so the same code sets a 1.25 MWh cycle and a 45.9 MWh one without a magic number moving.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _style import *          # noqa
import matplotlib.pyplot as plt

CLS = 'P100'
NAME = 'P-100'
OUT = 'ledger'

F = figures()['classes'][CLS]
L = F['energy']['ledgerMWh']
total = F['cycle']['eCycleMWh']

ORDER = [('SOURCE_APPROACH', 'Approach', '', ACCENT),
         ('WATER_FILL', 'Fill', '', COOL),
         ('OUTBOUND_TRANSIT', 'Outbound', '', COOL),
         ('WATER_RELEASE', 'Release', '', COOL),
         ('BUOYANCY_ESCAPE', 'Escape', '', COOL),
         ('RETURN_TRANSIT', 'Return', '', COOL),
         ('recovery', 'Nitrogen recovery', '', GREEN)]

vals = [L[k] for k, _, _, _ in ORDER]
lo, hi = min(vals), max(vals)
span = hi - lo
# Every offset is a fraction of the span, so the same code lays out a 1.25 MWh cycle and a
# 45.9 MWh one. Absolute offsets looked right on one and collided on the other.
pad_l = span * 0.30 if lo < 0 else span * 0.04
XMIN, XMAX = lo - pad_l, hi + span * 0.52
gap = span * 0.018
SHARE_X = XMAX

fig, ax = plt.subplots(figsize=(6.5, 3.1))
for i, (k, lab, sub, c) in enumerate(ORDER):
    y, v = -i, L[k]
    ax.barh(y, v, height=0.58, color=c, edgecolor='none')
    ax.text(v + (gap if v >= 0 else -gap), y, f'{v:.3f}'.replace('-', '\u2212'), va='center',
            ha='left' if v >= 0 else 'right', fontsize=8.2, color=INK,
            fontweight='bold' if abs(v) > span * 0.25 else 'normal')
    ax.text(SHARE_X, y, f'{v / total * 100:+.1f}%'.replace('+', ' ').replace('-', '\u2212'),
            va='center', ha='right', fontsize=8.0, color=FAINT)

ax.axvline(0, color=MUTED, lw=0.9, zorder=3)
ax.set_yticks([-i for i in range(len(ORDER))])
ax.set_yticklabels([lab for _, lab, _, _ in ORDER], fontsize=8.6, color=INK)
for i, (_, _, sub, _) in enumerate(ORDER):
    if sub:
        ax.annotate(sub, xy=(0, -i), xycoords=('axes fraction', 'data'),
                    xytext=(-6, -9), textcoords='offset points',
                    ha='right', va='center', fontsize=7.0, color=FAINT)
ax.set_xlim(XMIN, XMAX)
ax.set_ylim(-len(ORDER) + 0.45, 0.75)
ax.set_xlabel(f'{NAME}, 15 km: MWh supplied — record basis, INFEASIBLE', labelpad=2)
bare(ax, left=False)
ax.text(SHARE_X, 0.75, 'share', ha='right', va='bottom', fontsize=7.2, color=FAINT,
        fontstyle='italic')
save(fig, OUT)
