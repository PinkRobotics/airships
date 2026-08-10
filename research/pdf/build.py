#!/usr/bin/env python3
"""Build the three report PDFs.

    python3 research/pdf/build.py            # charts, tex, pdfs
    python3 research/pdf/build.py --fast     # skip the charts

The Markdown in research/reports/ is the source; tools/md2tex.py converts it and this drives
lualatex over the result. Nothing here contains a sentence of the reports, on purpose.
"""
import argparse, pathlib, re, shutil, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent.parent

META = {
    '01-brief': dict(
        kicker='Pink Robotics \\textperiodcentered\\ Briefing',
        sub="A briefing \\textperiodcentered\\ 9 August 2026 \\textperiodcentered\\ "
            "Vancouver, BC \\\\ Figures are generated from the simulation at "
            "\\texttt{pinkrobotics.ca/airships} and verified against it automatically.",
        foot='Pink Robotics \\textperiodcentered\\ wildfire airships \\textperiodcentered\\ briefing'),
    '02-paper': dict(
        kicker='Pink Robotics \\textperiodcentered\\ Technical Paper',
        sub="Version 1 \\textperiodcentered\\ 9 August 2026 \\\\ Every model figure is cited by "
            "key and checked against the simulation that produces it; source figures are cited "
            "in place. Nothing described here has been built.",
        foot='Continuous aerial water delivery by vacuum-lift airship'),
    '03-diligence': dict(
        kicker='Pink Robotics \\textperiodcentered\\ Diligence Report',
        sub="Prepared for technical and commercial diligence \\textperiodcentered\\ 9 August 2026 "
            "\\\\ A report on a concept, not on a company. No hardware exists. The apparatus that "
            "produced these numbers is the asset under examination.",
        foot='Vacuum-lift wildfire airships \\textperiodcentered\\ diligence'),
}


def run(cmd, **kw):
    # errors='replace': latexmk relays whatever the log contains, and a Type1 font name with a
    # high byte in it crashed the build script rather than the build.
    r = subprocess.run(cmd, capture_output=True, text=True, errors='replace', **kw)
    if r.returncode != 0:
        sys.stderr.write(r.stdout[-4000:] + r.stderr[-2000:])
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fast', action='store_true')
    ap.add_argument('which', nargs='*')
    a = ap.parse_args()

    if not a.fast:
        for chart in sorted((HERE / 'charts').glob('*.py')):
            r = run([sys.executable, str(chart)], cwd=HERE)
            print(f'  chart {chart.stem}: {"ok" if r.returncode == 0 else "FAILED"}')
            if r.returncode:
                return 1

    r = run([sys.executable, str(ROOT / 'tools' / 'md2tex.py')], cwd=ROOT)
    if r.returncode:
        return 1
    print(r.stdout.strip())

    stems = a.which or list(META)
    ok = True
    for stem in stems:
        m = META[stem]
        main_tex = HERE / f'{stem}.tex'
        main_tex.write_text(
            f'\\newcommand{{\\reportkicker}}{{{m["kicker"]}}}\n'
            f'\\newcommand{{\\reportsub}}{{{m["sub"]}}}\n'
            f'\\newcommand{{\\runningfoot}}{{{m["foot"]}}}\n'
            '\\input{doc}\n'
            '\\begin{document}\n'
            f'\\input{{{stem}.body}}\n'
            '\\end{document}\n')
        r = run(['latexmk', '-pdf', '-interaction=nonstopmode', '-halt-on-error',
                 '-outdir=out', f'{stem}.tex'], cwd=HERE)
        pdf = HERE / 'out' / f'{stem}.pdf'
        if r.returncode or not pdf.exists():
            print(f'  {stem}: BUILD FAILED'); ok = False; continue
        # pdfinfo, because pdflatex writes compressed object streams and /Count is not in
        # the plain bytes — grepping for it silently reported 0 pages for every build.
        info = subprocess.run(['pdfinfo', str(pdf)], capture_output=True, text=True,
                              errors='replace')
        mm = re.search(r'^Pages:\s+(\d+)', info.stdout, re.M)
        pages = int(mm.group(1)) if mm else 0
        print(f'  {stem}.pdf — {pages} pages, {pdf.stat().st_size // 1024} KB')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
