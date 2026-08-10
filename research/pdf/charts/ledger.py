#!/usr/bin/env python3
"""Where a cycle's energy goes, and what the anchor is worth. Drawn from figures.json."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _style import *          # noqa
import matplotlib.pyplot as plt

F = figures()['classes']['P10000']
L = F['energy']['ledgerMWh']
total = F['cycle']['eCycleMWh']

ORDER = [('RETURN_TRANSIT',  'Return transit',      'drag + cryogenic plant',   COOL),
         ('WATER_FILL',      'Pumping',             '10,000 t up a 300 m head', COOL),
         ('other',           'Hotel + manoeuvring', '',                         COOL),
         ('OUTBOUND_TRANSIT','Outbound transit',    'loaded, 130 km/h',         COOL),
         ('letdown',         'Letdown',             'rotors, anchor deployed',  ACCENT),
         ('anchor',          'Anchor',              'lifting the bag 15 m',     ACCENT),
         ('recovery',        'Nitrogen recovery',   'credited back',            GREEN)]

XMAX = 20.5
fig, ax = plt.subplots(figsize=(6.5, 3.1))
for i, (k, lab, sub, c) in enumerate(ORDER):
    y, v = -i, L[k]
    ax.barh(y, v, height=0.58, color=c, edgecolor='none')
    # value hugs the bar end; the share lives in its own column so nothing can collide
    ax.text(v + (0.28 if v >= 0 else -0.28), y, f'{abs(v):.3f}', va='center',
            ha='left' if v >= 0 else 'right', fontsize=8.2, color=INK,
            fontweight='bold' if abs(v) > 5 else 'normal')
    ax.text(XMAX, y, f'{v / total * 100:+.1f}%'.replace('+', ' '), va='center', ha='right',
            fontsize=8.0, color=FAINT)

ax.axvline(0, color=MUTED, lw=0.9, zorder=3)
ax.set_yticks([-i for i in range(len(ORDER))])
ax.set_yticklabels([f'{lab}' for _, lab, _, _ in ORDER], fontsize=8.6, color=INK)
for i, (_, _, sub, _) in enumerate(ORDER):
    if sub:
        ax.annotate(sub, xy=(0, -i), xycoords=('axes fraction', 'data'),
                    xytext=(-6, -9), textcoords='offset points',
                    ha='right', va='center', fontsize=7.0, color=FAINT)
ax.set_xlim(-6.2, XMAX)
ax.set_ylim(-len(ORDER) + 0.45, 0.75)
ax.set_xticks([-5, 0, 5, 10, 15])
ax.set_xlabel('MWh per cycle', labelpad=2)
bare(ax, left=False)
ax.text(XMAX, 0.75, 'share', ha='right', va='bottom', fontsize=7.2, color=FAINT,
        fontstyle='italic')
save(fig, 'ledger')
