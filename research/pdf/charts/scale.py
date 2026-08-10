#!/usr/bin/env python3
"""The hulls at true relative scale, against things people already have a size for.

Drawn from lenM and diaM in figures.json, so the silhouettes cannot disagree with the
specification table on the facing page.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _style import *          # noqa
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle

C = figures()['classes']
ROWS = [
    ('P-10000', C['P10000']['spec']['lenM'], C['P10000']['spec']['diaM'], ACCENT, True),
    ('P-1000',  C['P1000']['spec']['lenM'],  C['P1000']['spec']['diaM'],  COOL, True),
    ('P-100',   C['P100']['spec']['lenM'],   C['P100']['spec']['diaM'],   COOL_L, True),
    ('LZ 129 Hindenburg', 245, 41, FAINT, True),
    ('Boeing 747-400', 71, 19, MUTED, False),
]

# The axis is in METRES and the aspect is locked, so every vertical step has to be in metres
# too. Stepping in scaled units piled all five hulls on top of each other.
GAP = 26.0
fig, ax = plt.subplots(figsize=(6.5, 2.45))
y = 0.0
for name, L, D, colour, is_hull in ROWS:
    y -= D / 2 + GAP
    if is_hull:
        ax.add_patch(Ellipse((L / 2, y), L, D, facecolor=colour, edgecolor='none'))
    else:
        ax.add_patch(Rectangle((0, y - D / 2), L, D, facecolor=colour, edgecolor='none'))
    ax.text(-18, y, name, ha='right', va='center', fontsize=8.4,
            color=INK, fontweight='bold' if name.startswith('P-') else 'normal')
    ax.text(L + 16, y, f'{L:,.0f} m', ha='left', va='center', fontsize=8.0, color=MUTED)
    y -= D / 2

# a 100 m rule, because a drawing without one is a picture
ax.plot([0, 100], [y - 46, y - 46], color=INK, lw=1.4)
for x in (0, 100):
    ax.plot([x, x], [y - 54, y - 38], color=INK, lw=1.4)
ax.text(50, y - 62, '100 m', ha='center', va='top', fontsize=7.6, color=INK)

ax.set_xlim(-230, 1000)
ax.set_ylim(y - 96, 44)
ax.set_aspect('equal')
ax.axis('off')
save(fig, 'scale')
