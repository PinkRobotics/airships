#!/usr/bin/env python3
"""What holds a ship down at the water, as a fraction of what has to be held.

Absolute tonnes on a log axis hid the finding: 13,722 against 12,666 looks identical there,
and the whole point is that one is larger than the other. Normalised, the story is one glance
— the bar is the job, the blue tick is how far the rotors reach, and on two classes it stops
short of the end.
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from _style import *          # noqa
import matplotlib.pyplot as plt

C = figures()['classes']
IDS = ['P100', 'P1000', 'P10000']
NAMES = {'P100': 'P-100', 'P1000': 'P-1000', 'P10000': 'P-10000'}

fig, ax = plt.subplots(figsize=(6.5, 2.5))
for row, cid in enumerate(IDS):
    d = C[cid]['descent']
    hold, rotor, bag = d['holdAtSourceT'], d['rotorCapT'], d['anchorT']
    y = -row
    bagf, rotf = bag / hold, (hold - bag) / hold
    ax.barh(y, bagf, height=0.5, color=ACCENT, edgecolor='none')
    # Light against dark, with a white separator: the two segments have to be tellable
    # apart on a photocopy, not only on a screen.
    ax.barh(y, rotf, left=bagf, height=0.5, color=COOL_L, edgecolor='white',
            linewidth=0.9)
    ax.text(bagf / 2, y, f'anchor  {bagf*100:.0f}%', ha='center', va='center',
            fontsize=8.0, color='white', fontweight='bold')
    if rotf > 0.055:
        ax.text(bagf + rotf / 2, y, f'{rotf*100:.0f}%', ha='center', va='center',
                fontsize=7.6, color=INK)
    # How far the rotors reach on their own. The P-100's marker would be at 197% and off the
    # axis, so it is clamped with an arrowhead — the number is in the right-hand column either
    # way, and a marker that leaves the plot is worse than one that says it did.
    reach = rotor / hold
    if reach <= 1.06:
        ax.plot([reach, reach], [y - 0.34, y + 0.34], color=INK, lw=1.7, solid_capstyle='butt')
    else:
        ax.plot([1.03, 1.03], [y - 0.34, y + 0.34], color=INK, lw=1.7, solid_capstyle='butt')
        ax.annotate('', xy=(1.075, y), xytext=(1.03, y),
                    arrowprops=dict(arrowstyle='-|>', color=INK, lw=1.1, shrinkA=0, shrinkB=0))
    ax.text(1.21, y, f'{hold:,.0f} t', va='center', ha='right', fontsize=8.2, color=MUTED)
    # A WORD, not a colour: "does it close" was pink-versus-black, invisible to a
    # colour-confusable reader and on a mono printer alike. (TeX Gyre Heros has no check or
    # ballot glyph, and a word beats a symbol the reader has to decode anyway.)
    ax.text(1.37, y, f'{reach*100:.0f}%', va='center', ha='right', fontsize=8.2,
            color=INK, fontweight='bold')
    ax.text(1.60, y, 'closes' if reach >= 1 else 'short', va='center', ha='right', fontsize=7.6,
            color=MUTED if reach >= 1 else ACCENT,
            fontstyle='normal' if reach >= 1 else 'italic')

ax.axvline(1.0, color=MUTED, lw=0.9, ls=(0, (3, 2)))
ax.plot([], [], color=INK, lw=1.7, label='how far the rotors reach unaided')
ax.legend(loc='lower left', bbox_to_anchor=(-0.005, -0.40), fontsize=7.4, handlelength=0.7)
ax.set_yticks([0, -1, -2]); ax.set_yticklabels([NAMES[i] for i in IDS], fontsize=8.8, color=INK)
ax.set_xlim(0, 1.62); ax.set_ylim(-2.62, 0.95)
ax.text(1.21, 0.50, 'to hold', ha='right', va='bottom', fontsize=7.2, color=FAINT,
        fontstyle='italic')
ax.text(1.37, 0.50, 'rotors', ha='right', va='bottom', fontsize=7.2, color=FAINT,
        fontstyle='italic')
ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
ax.set_xticklabels(['0', '25%', '50%', '75%', '100%'])
ax.set_xlabel('share of the surplus lift that has to be held down at the water')
bare(ax, left=False)
save(fig, 'descent')
