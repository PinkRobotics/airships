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

w = 0.34
for i, cid in enumerate(IDS):
    e = C[cid]['energy']
    spend = C[cid]['cycle']['eCycleMWh']
    gen = e['solarPerCycleMWh']
    a1.bar(i - w / 2, spend, width=w, color=INK, edgecolor='none')
    a1.bar(i + w / 2, gen, width=w, color=GREEN, edgecolor='none')
    a1.text(i - w / 2, spend * 1.10, f'{spend:.2f}', ha='center', va='bottom', fontsize=7.8, color=INK)
    a1.text(i + w / 2, gen * 1.10, f'{gen:.2f}', ha='center', va='bottom', fontsize=7.8, color=GREEN)
    a1.annotate(f'−{e["deficitPerCycleMWh"]:.2f}', xy=(i, spend * 0.26), ha='center',
                fontsize=8.4, color=ACCENT, fontweight='bold')
a1.set_yscale('log'); a1.set_ylim(0.08, 260)
a1.set_yticks([0.1, 1, 10, 100]); a1.set_yticklabels(['0.1', '1', '10', '100'])
a1.set_xticks(range(3)); a1.set_xticklabels([NAMES[i] for i in IDS], fontsize=8.6, color=INK)
a1.set_ylabel('MWh per cycle')
a1.set_title('Spent against generated', loc='left', pad=9)
bare(a1)
h = [plt.Rectangle((0, 0), 1, 1, color=c) for c in (INK, GREEN)]
a1.legend(h, ['spent', 'solar, generated'], loc='upper left', fontsize=7.4,
          handlelength=0.9, handleheight=0.9, ncol=2, bbox_to_anchor=(-0.01, 1.04))

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
