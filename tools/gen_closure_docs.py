#!/usr/bin/env python3
"""Render conditional closure prose from the mass budget; never re-price the hull.

python3 tools/gen_closure_docs.py --write
python3 tools/gen_closure_docs.py --check

Only the named closure sections are owned here. Other studies keep their own generators.
"""
import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def section(text, start, end, body):
    lo = text.index(start) + len(start)
    hi = text.index(end, lo)
    return text[:lo] + '\n\n' + body.strip() + '\n\n' + text[hi:]


def render():
    data = json.loads((ROOT / 'research/analysis/mass-budget.json').read_text())
    r = data['classes']['P100']
    rho = r['shellDensityWallKgPerM3']
    floor = r['rightSized']['floor']
    wall = floor['closureWallKgPerM3']
    rows = floor['hullThatCloses']
    best = rows['0.508']
    def hull(row):
        return f"{row['lenM']} × {row['diaM']} m"
    def packed(row):
        return f"{row['volumeM3']:,} m³, {hull(row)}" if row['closes'] else '**never**'
    cases = '; '.join(f"{c}: f = {data['evidence']['sundries_frac'][c]['value']:.2f}, "
                      f"wall {v['closureWallKgPerM3']:.3f} kg/m³"
                      for c, v in r['rightSized'].items())
    walls = f"The cases differ with their own sundries fractions: {cases}."
    literature = '\n'.join([
        '| source | shell | verdict against the floor closure wall |',
        '|---|---|---|',
        f'| Jenett et al. 2019, discrete lattice | 0.508 kg/m³ | below by {100*(1-.508/wall):.1f}% |',
        f'| Jenett + 50% for joints and skin | 0.75 kg/m³ | below by {100*(1-.75/wall):.1f}% |',
        f'| Metlen 2013, frame with a real membrane | ≈0.94 kg/m³ equivalent | passes the lift wall; fails the closure wall by {100*(.94/wall-1):.1f}% |',
        f'| Akhmeteli & Gavrilin 2021, sandwich sphere | 1.16 kg/m³ | fails both; {100*(1.16/wall-1):.1f}% above the closure wall |'])
    closure = ['| shell | volume that closes | × baseline | hull |', '|---|---|---|---|']
    for shell, row in rows.items():
        name = shell + ' kg/m³' + (' (Jenett, published)' if shell == '0.508' else '')
        if row['closes']:
            closure.append(f"| {name} | {row['volumeM3']:,} m³ | {row['timesBaseline']:.2f}× | {hull(row)} |")
        else:
            closure.append(f'| {name} | **never** | — | — |')
    packing = ['| | φ = 0.74 (close-packed spheres) | φ = 0.85 | φ = 1.0 (space-filling cells) |',
               '|---|---|---|---|',
               '| effective closure wall | ' + ' | '.join(f'{rho*p/(1 + data['evidence']['sundries_frac']['floor']['value']):.3f} kg/m³' for p in (.74,.85,1.)) + ' |']
    for shell in ('0.264','0.508','0.750'):
        packing.append('| hull at shell ' + shell + ' | ' + ' | '.join(
            packed(floor['cellular'][f'phi={p}'][shell]) for p in (.74,.85,1.)) + ' |')
    packing.append('')
    packing.append('The packing wall is ρφ/(1 + f); the table uses the floor f = 0.10. '
                   'Credible (f = 0.15) and demonstrated (f = 0.20) lower each wall further.')
    mass = (ROOT/'research/analysis/mass-budget.md').read_text()
    body = f'''**Displacement is a design variable and the payload is the requirement.** Shell mass
per enclosed volume is held constant in this conditional study. Area-scaled equipment grows
more slowly than volume. The complete bill can therefore close by growing the hull only when:

> Net lift after shell sundries = ρ_air − shell_kg/m³ × (1 + f) > 0.
> Sundries are a fraction of everything, including the shell; payload is separate.

Air density at 2,500 m is **{rho:.3f} kg/m³**. At or above this lift wall the shell has no
net lift at any size. Closing the equipment budget needs a lower shell density:
**ρ/(1 + f), or {wall:.3f} kg/m³ in the floor case (f = 0.10)**.

{walls}

Against the floor closure wall, the literature separates:

{literature}

And the hull that closes, in the floor case:

{chr(10).join(closure)}

**At the best published shell density the reference ship conditionally closes at {hull(best)} —
still shorter than the Hindenburg.** Its volume is **{best['timesBaseline']:.2f}× the reference**.
This is a complete equipment-bill balance under constant shell density, not a checked structure.

The conditional volume grows from {best['volumeM3']:,} m³ at 0.508 kg/m³ to
{rows['0.750']['volumeM3']:,} m³ at 0.75 kg/m³ ({hull(rows['0.750'])}). At 0.90 kg/m³
it **never closes**: shell plus its 10% sundries costs 0.990 kg/m³, above the air density.'''
    mass = section(mass, '## But the allowance is not a law, and this is the correction that matters',
                   '## The sealed-cell architecture', body)
    mass = section(mass, 'scaled by the packing fraction φ:', '**Packing fraction is now', '\n'.join(packing))
    summary = f'''The budget as specified fails by {r['cases']['floor']['overBy']:.2f}× at its most favourable,
and {floor['overBy']:.2f}× with the battery sized to the prescribed cycle. At the best published
shell density the conditional complete bill closes at **{best['timesBaseline']:.2f}× the reference volume,
a {best['lenM']} m hull**. The lift wall is **{rho:.3f} kg/m³**; the floor equipment-budget closure
wall is **{wall:.3f} kg/m³**, reduced further by packing losses and larger sundries fractions.

What decides this sealed-cell budget is the density of one complete cell and its packing
fraction. Neither is measured here, and these conditional sizes do not validate a hull.'''
    mass = mass[:mass.index('## The honest summary')] + '## The honest summary\n\n' + summary + '\n'
    # This sentence transcribed an obsolete fraction; the model's floor is ten percent.
    mass = mass.replace('`sundries_frac` is 5% at the floor', '`sundries_frac` is 10% at the floor')
    plan = (ROOT/'docs/VERIFICATION-PLAN.md').read_text()
    plan_body = f'''> **Air density is {rho:.3f} kg/m³ at 2,500 m:** a shell at or above it has no net lift
> at any size. The complete budget can be grown until it closes only below
> **ρ/(1 + f) = {wall:.3f} kg/m³ in the floor case**, because sundries include the shell.

{walls}

Displacement is a design variable; payload is the requirement. These constant-density
closure sizes balance the conditional equipment bill and do not validate a drawn hull.

{literature}

The 0.508 kg/m³ floor closes at {best['volumeM3']:,} m³, a {best['lenM']} m ship, shorter than
the Hindenburg; 0.75 needs {rows['0.750']['timesBaseline']:.2f}× the baseline volume. At 0.90 it never closes.

Two things also matter:

- **Shape.** A monocoque fineness-4 hull's estimated ~2.45× buckling penalty would take
  Jenett's 0.508 to 1.25 kg/m³, over both walls.
- **Packing.** This budget prices **many permanently sealed vacuum cells**. Their buckling
  radius is the cell's; ambient space between cells lifts nothing. At φ = 0.74 the floor
  closure wall is **{rho*.74/1.1:.3f} kg/m³**, from ρφ/(1 + f).

The sealed-cell density and packing fraction have neither been chosen nor measured.'''
    plan = section(plan, '## The critical path: one number decides whether this can exist', '\n---', plan_body)
    plan = re.sub(r'Here is our wall: [\d.]+ kg/m³ of enclosed volume, less the packing\s+fraction\.',
                  f'Here is the floor closure wall: ρφ/(1 + f), or {wall:.3f}φ kg/m³ of enclosed volume.', plan)
    plan = re.sub(r"The mass budget's true wall is a single number that Jenett's\s+published shell clears with 47% margin, and the hull is free to grow to meet it\.",
                  f"The floor budget's closure wall includes shell sundries; Jenett's published shell clears it with {100*(1-.508/wall):.1f}% margin before packing losses.", plan)
    vacuum = (ROOT/'research/analysis/vacuum-cell.md').read_text()
    vacuum = section(vacuum, '## The one number', '## What the sealed-cell architecture', f'''> **Air density is {rho:.4f} kg/m³ at 2,500 m.** At or above this lift wall a shell
> has no net lift at any size. With sundries on everything, including the shell, a hull
> can be grown until its equipment budget closes only below ρ/(1 + f):
> **{wall:.3f} kg/m³ in the floor case (f = 0.10)**.

{walls} These are conditional mass balances, not structural validation.''')
    cell = (ROOT/'cell/index.html').read_text()
    panel = f'''<div class="muted mono" style="font-size:var(--t-12);letter-spacing:.08em;text-transform:uppercase">
    the closure wall — floor budget, 10% sundries</div>
  <div class="big" style="margin:var(--s3) 0"><span id="wallNum">{wall:.3f}</span>
    <span class="unit">kg per m³ of enclosed volume</span></div>
  <p style="margin:0">Air density at 2,500 m is {rho:.3f} kg/m³: a shell at or above it has
  <strong>no net lift at any size</strong>. This budget puts sundries on everything,
  including the shell. A constant-density hull can be grown until its bill closes only
  below ρ/(1 + f). The floor uses f = 0.10; credible uses 0.15 ({r['rightSized']['credible']['closureWallKgPerM3']:.3f});
  demonstrated uses 0.20 ({r['rightSized']['demonstrated']['closureWallKgPerM3']:.3f} kg/m³).
  The comparisons below use the lift wall; neither wall validates a structure.</p>'''
    cell = section(cell, '<h2>One number decides everything</h2>\n<div class="panel">', '</div>\n\n<div class="supersede">', panel)
    cell = cell.replace("$('#wallNum').textContent = fmt(wall, 3);", "$('#wallNum').textContent = fmt(wall / 1.10, 3);")
    questions = (ROOT/'docs/OPEN-QUESTIONS.md').read_text()
    # Dated previous corrections stay visible. Own a separate current correction.
    correction = f"""> **2026-10-05 correction to #11:** shell sundries were omitted from the resized
> bill. The 0.508 kg/m³ floor now closes conditionally at {best['volumeM3']:,} m³,
> a {best['lenM']} m hull. Its closure wall is {wall:.3f} kg/m³; {rho:.3f} kg/m³ is the lift wall.
> This complete equipment bill does not validate a drawn hull."""
    begin, end = '<!-- closure-correction:start -->', '<!-- closure-correction:end -->'
    if begin not in questions:
        anchor = '> See [the regeneration audit](audit/26-10-02-analysis-regeneration.md).'
        questions = questions.replace(anchor, anchor + '\n\n' + begin + '\n' + end)
    questions = section(questions, begin, end, correction)
    return {'research/analysis/mass-budget.md': mass, 'docs/VERIFICATION-PLAN.md': plan,
            'research/analysis/vacuum-cell.md': vacuum, 'cell/index.html': cell,
            'docs/OPEN-QUESTIONS.md': questions}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument('--write', action='store_true')
    mode.add_argument('--check', action='store_true')
    args = ap.parse_args()
    bad = []
    for rel, body in render().items():
        path = ROOT / rel
        if args.write:
            path.write_text(body)
        elif path.read_text() != body:
            bad.append(rel)
    if bad:
        print('closure prose differs from fresh generation: ' + ', '.join(bad))
        return 1
    print('closure prose: five documents match the current complete-bill records')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
