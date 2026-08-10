#!/usr/bin/env python3
"""What a hull makes against what it spends, and how long the battery lasts."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _style import *          # noqa
import matplotlib.pyplot as plt

C = figures()['classes']
IDS = ['P100', 'P1000', 'P10000']
NAMES = {'P100': 'P-100', 'P1000': 'P-1000', 'P10000': 'P-10000'}

fig, (a1, a2) = plt.subplots(1, 2, figsize=(6.6, 2.5), gridspec_kw={'width_ratios': [1.5, 1]})

# SHARE, not log bars. Spend and generation span two orders of magnitude across the classes, so
# the first version put them on a log axis — where a bar's length no longer means its value. The
# ratio is dimensionless, comparable across classes without a log axis, and says the thing that
# matters: every hull makes about a tenth of what it spends.
for i, cid in enumerate(IDS):
    e = C[cid]['energy']
    spend = C[cid]['cycle']['eCycleMWh']
    gen = e['solarPerCycleMWh']
    frac = gen / spend
    y = -i
    a1.barh(y, 1.0, height=0.52, color='#EDEDF1', edgecolor='none')
    a1.barh(y, frac, height=0.52, color=GREEN, edgecolor='none')
    a1.text(frac + 0.022, y, f'{frac*100:.0f}%', va='center', ha='left', fontsize=8.6,
            color=INK, fontweight='bold')
    a1.text(1.02, y, f'{gen:.2f} of {spend:.2f} MWh', va='center', ha='left', fontsize=7.6,
            color=MUTED)
a1.set_yticks([0, -1, -2])
a1.set_yticklabels([NAMES[i] + ('  (ref)' if i == 'P100' else '') for i in IDS],
                   fontsize=8.6, color=INK)
a1.set_xlim(0, 1.62); a1.set_ylim(-2.55, 0.7)
a1.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
a1.set_xticklabels(['0', '25%', '50%', '75%', '100%'])
a1.set_xlabel('share of its own cycle a hull generates')
a1.set_title('Generated against spent', loc='left', pad=9)
bare(a1, left=False)

hours = [C[i]['energy']['hoursOnBattery'] for i in IDS]
a2.barh([-i for i in range(3)], hours, height=0.5, color=ACCENT, edgecolor='none')
for i, v in enumerate(hours):
    a2.text(v + 1.0, -i, f'{v:.1f} h', va='center', fontsize=8.6, color=INK, fontweight='bold')
a2.set_yticks([0, -1, -2]); a2.set_yticklabels([NAMES[i] for i in IDS], fontsize=8.6, color=INK)
a2.set_xlim(0, 48); a2.set_ylim(-2.55, 0.7)
a2.set_xlabel('hours of work on a full battery')
a2.set_title('Endurance', loc='left', pad=9)
bare(a2, left=False)
save(fig, 'deficit')
