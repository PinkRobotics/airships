"""Shared chart style. Every figure in the PDFs is drawn from research/figures.json.

A chart that is drawn from a hand-typed array is a chart that goes stale silently, which is
the one failure this project has spent its whole life fighting. So there is one loader here
and the generators may not type a model number either.

Typeface matches the documents: TeX Gyre Pagella for numerals and any running text, TeX Gyre
Heros for labels. Matplotlib finds them by family name through fontconfig, which lists them
even though luaotfload did not.
"""
from __future__ import annotations

import json
import pathlib

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt          # noqa: E402
from matplotlib import font_manager      # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE
ROOT = HERE.parent.parent.parent
FIGURES = ROOT / 'research' / 'figures.json'

INK = '#16161A'
MUTED = '#55555F'
FAINT = '#8A8A94'
RULE = '#D8D8DE'
# CATEGORICAL PAIRS MUST DIFFER IN LIGHTNESS, not only in hue. ACCENT and COOL sat at almost
# the same luminance, so descent.pdf collapsed to one solid dark block in greyscale and the
# whole point of the figure went with it. People print these.
#
# The pairing rule: when two series sit side by side, take one from the dark end and one from
# the light end. Saturated accent is for single-series emphasis, where nothing has to be told
# apart from it.
ACCENT = '#C4185C'        # L* ~40
ACCENT_L = '#F2B8CE'      # L* ~80
COOL = '#2C5B87'          # L* ~38
COOL_L = '#BFD4E6'        # L* ~83
WARN = '#D9A441'
GREEN = '#3F7D52'
PALE = '#F4F4F6'

_families = {f.name for f in font_manager.fontManager.ttflist}
SERIF = 'TeX Gyre Pagella' if 'TeX Gyre Pagella' in _families else 'DejaVu Serif'
SANS = 'TeX Gyre Heros' if 'TeX Gyre Heros' in _families else 'DejaVu Sans'

plt.rcParams.update({
    'font.family': SANS,
    'font.size': 8.4,
    'axes.edgecolor': RULE,
    'axes.labelcolor': MUTED,
    'axes.titlecolor': INK,
    'axes.titlesize': 9.2,
    'axes.titleweight': 'bold',
    'axes.labelsize': 8.2,
    'axes.linewidth': 0.7,
    'axes.grid': False,
    'xtick.color': MUTED,
    'ytick.color': MUTED,
    'xtick.labelsize': 8.0,
    'ytick.labelsize': 8.0,
    'xtick.major.width': 0.7,
    'ytick.major.width': 0.7,
    'xtick.major.size': 3,
    'ytick.major.size': 3,
    'legend.frameon': False,
    'legend.fontsize': 8.0,
    'figure.facecolor': 'white',
    'savefig.facecolor': 'white',
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.02,
    'pdf.fonttype': 42,
    'pdf.compression': 9,
})


def figures() -> dict:
    return json.loads(FIGURES.read_text())


def flat() -> dict:
    def walk(o, p=''):
        out = {}
        if isinstance(o, dict):
            for k, v in o.items():
                out.update(walk(v, f'{p}{k}.'))
        elif isinstance(o, list):
            for i, v in enumerate(o):
                out.update(walk(v, f'{p}{i}.'))
        else:
            out[p[:-1]] = o
        return out
    return walk(figures())


def bare(ax, left=True, bottom=True):
    """Strip the box down to the two rules that carry information."""
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    ax.spines['left'].set_visible(left)
    ax.spines['bottom'].set_visible(bottom)
    ax.tick_params(length=3, width=0.7)
    return ax


def save(fig, name: str):
    path = OUT / f'{name}.pdf'
    if name in {'ledger', 'ledger-limit', 'deficit', 'sensitivity'}:
        import textwrap
        fig.canvas.draw()
        bottom = fig.get_tightbbox(fig.canvas.get_renderer()).y0 / fig.get_figheight()
        note = 'Prescribed-profile diagnostic analysis. These supplied-effort figures do not establish delivery, endurance, savings or operating cost. See the generated energy closure record for feasible plans.'
        fig.text(.5, bottom-.04, "Diagnostic analysis\n" +
                 "\n".join(textwrap.wrap(note, max(45, int(fig.get_figwidth()*17)))),
                 ha='center', va='top', fontsize=6.5, color=MUTED)
    fig.savefig(path)
    plt.close(fig)
    print(f'    {name}.pdf')
    return path
