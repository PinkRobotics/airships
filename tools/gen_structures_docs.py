#!/usr/bin/env python3
"""Regenerate the corrected structural tables from their current model inputs."""
import argparse
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
import subdivision_study as sub


def table(headers, rows):
    return '\n'.join('| ' + ' | '.join(map(str, row)) + ' |'
                     for row in [headers, ['---'] * len(headers), *rows])


def put(body, name, text, header):
    start, end = f'<!-- structures:{name}:start -->', f'<!-- structures:{name}:end -->'
    fresh = start + '\n' + text + '\n' + end
    if start in body:
        pattern = re.escape(start) + r'.*?' + re.escape(end)
    else:
        pattern = re.escape(header) + r'\n(?:\|[^\n]*\n)+'
    body, n = re.subn(pattern, lambda _: fresh + ('\n' if start not in body else ''), body, flags=re.S)
    if n != 1:
        raise ValueError(f'{name}: expected one table, found {n}')
    return body


def outputs():
    vc = json.loads((ROOT / 'research/analysis/vacuum-cell.json').read_text())
    name = 'research/analysis/vacuum-cell.md'
    body = (ROOT / name).read_text()
    rows = [[n, f"{r['exponent']:.3f}", f"{r['totalKgPerM3']:.3f}",
             f"{r['liftToMassSeaLevel']:.3f}", f"{r['liftToMassAt2500m']:.3f}",
             'formula only' + ('; compression-capped' if r['yieldCapped'] else '')]
            for n, r in vc['hierarchy']['ladder'].items()]
    headers = ['levels', 'exponent', 'density kg/m³', 'lift/mass at sea level',
               'lift/mass at 2,500 m', 'status']
    body = put(body, 'hierarchy', table(headers, rows), '| ' + ' | '.join(headers) + ' |')
    rows = [[('1 — hard vacuum' if n == '1' else n),
             f"{r['structureKgPerM3']:.3f}", f"{r['gasKgPerM3']:.3f}",
             f"{r['filmsKgPerM3']:.3f}", f"{r['netLiftKgPerM3']:+.3f}"]
            for n, r in vc['gradedPressure']['bulk'].items() if n in ('1', '2', '10')]
    headers = ['N levels', 'structure', 'gas held', 'films', 'net lift']
    body = put(body, 'bulk', table(headers, rows), '| ' + ' | '.join(headers) + ' |')
    result = {name: body}

    name = 'docs/FLOAT.md'
    body = (ROOT / name).read_text()
    rows, transitions = [], []
    for span, n in ((1., 2), (2., 2), (4., 2), (3., 4), (6., 4)):
        r = sub.best_article(span, n)
        if r is None:
            raise ValueError('No film-safe article in the declared catalogue')
        vol = span ** 3 / 2
        rows.append([f'{span:.1f}', n, r['nodes'], f"{r['strutMm']:.0f} mm",
                     f"{r['odMm']:.1f} × {r['wallMm']:.2f} mm",
                     *[f'{v:.2f}' for v in (r['tubeKg']/vol, r['jointKg']/vol,
                        r['filmKg']/vol, r['kgPerM3'], r['overWall'], r['eulerMargin'],
                        r['localMargin'], r['yieldMargin'], r['filmBending']['marginAtSF'])]])
        old = r['axialOnly']
        transitions.append([f'{span:.1f} m', n, f"{old['odMm']:.1f} × {old['wallMm']:.2f} mm",
                            f"{old['filmBending']['marginAtSF']:.2f}",
                            f"{old['filmBending']['failsAtAtm']:.2f} atm",
                            f"{r['odMm']:.1f} × {r['wallMm']:.2f} mm", f"{r['kgPerM3']:.2f}"])
    headers = ['span', 'n', 'joints', 'strut', 'tube OD × wall', 'tube', 'joints', 'film',
               'kg/m³', '× wall', 'Euler', 'local', 'compression', 'film @ SF 1.5']
    body = put(body, 'subdivision', table(headers, rows),
               '| span | n | joints | strut | tube OD × wall | tube | joints | film | kg/m³ | × wall | Euler | local | yield | film @ SF 1.5 |')
    headers = ['article A span', 'n', 'axial-only tube', 'film margin @ SF 1.5',
               'ultimate pressure', 'film-sized tube', 'repriced kg/m³']
    body = put(body, 'transitions', table(headers, transitions), '| ' + ' | '.join(headers) + ' |')
    result[name] = body

    name = 'cell/band.html'
    body = (ROOT / name).read_text()
    band = vc['gradedPressure']['band']
    text = ("<h2>Pressure staging: a separate cell calculation</h2>\n"
            "<p>The graded-pressure band is an unbuilt cell concept, separate from the hull "
            "calculator below. Its outer film sees "
            f"{band['outerSurfaceDifferentialAtm']:.1f} atm, while "
            f"{band['interfaceCount']} complete homothetic internal interfaces total "
            f"{band['internalInterfaceAreaM2']:,.0f} m². At the declared "
            f"{band['filmSpanM']:.1f} m film span, those internal films cost "
            f"{band['filmsDeltaKgPerM3']:.4f} kg/m³ of enclosed volume; the whole band's "
            f"net mass cost is {band['netCostKgPerM3']:+.4f} kg/m³. "
            "The current compression-capped reference cannot lift itself at working altitude, "
            "so a percentage of available net lift is unavailable. "
            "The former internal-film charge was 0.0017 kg/m³ and the former same-input "
            "net cost −0.0191 kg/m³; pricing the complete interfaces corrects that calculation. "
            "See the cell analysis "
            "for the dated correction and load-path assumptions.</p>")
    body = put(body, 'band-pressure', text, '')
    result[name] = body
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--write', action='store_true')
    p.add_argument('--emit', action='store_true')
    args = p.parse_args()
    generated = outputs()
    if args.emit:
        print(json.dumps(generated, ensure_ascii=False))
        return 0
    stale = []
    for name, body in generated.items():
        path = ROOT / name
        if path.read_text() != body:
            if args.write:
                path.write_text(body)
            else:
                stale.append(name)
    if stale:
        print('structures documents differ from fresh generation: ' + ', '.join(stale))
        return 1
    print('structures documents: hierarchy, bulk, subdivision and pressure-band regions match')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
