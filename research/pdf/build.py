#!/usr/bin/env python3
"""Build the three report PDFs.

    python3 research/pdf/build.py            # charts, tex, pdfs
    python3 research/pdf/build.py --fast     # skip the charts
    python3 research/pdf/build.py --check --fast --strict  # compare in TMPDIR

The Markdown in research/reports/ is the source; tools/md2tex.py converts it and this drives
pdfLaTeX over the result. Nothing here contains a sentence of the reports, on purpose.
"""
import argparse, hashlib, pathlib, re, shutil, subprocess, sys, tempfile

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


def pdf_content(path, scratch):
    """Text, links, document/page properties and visible pixels, independent of PDF encoding."""
    def output(cmd):
        return subprocess.run(cmd, check=True, capture_output=True).stdout
    info = output(['pdfinfo', '-box', str(path)]).decode('utf-8', errors='replace')
    pages = int(re.search(r'^Pages:\s+(\d+)', info, re.M)[1])
    info = output(['pdfinfo', '-box', '-f', '1', '-l', str(pages), str(path)]).decode('utf-8', errors='replace')
    # These describe the build/container, not the document. Page geometry, title, author,
    # permissions and tagging remain compared. PDF object IDs/compression are never decoded
    # into a content claim; the rendered pages and extracted text are compared instead.
    ignored = {'CreationDate', 'ModDate', 'Creator', 'Producer', 'File size', 'PDF version',
               'Optimized', 'Custom Metadata', 'Metadata Stream'}
    properties = [line for line in info.splitlines() if line.split(':', 1)[0] not in ignored]
    text = output(['pdftotext', '-layout', str(path), '-'])
    links = output(['pdfinfo', '-url', str(path)])
    scratch.mkdir()
    output(['pdftoppm', '-r', '96', '-png', str(path), str(scratch / 'page')])
    pixels = [hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(scratch.glob('page-*.png'))]
    if pages < 1 or len(pixels) != pages:
        raise ValueError('PDF page raster count does not match its page count')
    return {'properties': properties, 'text': text, 'links': links, 'pages': pixels}


def check(stems, fast, strict):
    """Rebuild in TMPDIR and compare with the recorded PDFs without touching the source tree."""
    with tempfile.TemporaryDirectory(prefix='pdf-check-') as tmp:
        root = pathlib.Path(tmp)
        here = root / 'research' / 'pdf'
        shutil.copytree(HERE, here, ignore=shutil.ignore_patterns('out', '__pycache__'))
        shutil.copytree(ROOT / 'research' / 'reports', root / 'research' / 'reports')
        shutil.copy2(ROOT / 'research' / 'figures.json', root / 'research' / 'figures.json')
        (root / 'tools').mkdir()
        shutil.copy2(ROOT / 'tools' / 'md2tex.py', root / 'tools' / 'md2tex.py')
        cmd = [sys.executable, str(here / 'build.py')]
        if fast: cmd.append('--fast')
        if strict: cmd.append('--strict')
        r = run(cmd + stems, cwd=root)
        print(r.stdout.strip())
        if r.returncode: return 1
        different = False
        for stem in stems:
            recorded = pdf_content(HERE / 'out' / f'{stem}.pdf', root / (stem + '-recorded'))
            rebuilt = pdf_content(here / 'out' / f'{stem}.pdf', root / (stem + '-rebuilt'))
            moved = [key for key in recorded if recorded[key] != rebuilt[key]]
            if moved:
                different = True
                print(f'pdfcheck: {stem}: content differs in {", ".join(moved)}; '
                      'inspect before make pdfgenerate')
            else:
                print(f'pdfcheck: {stem}: text, links, properties and all '
                      f'{len(recorded["pages"])} page rasters match')
        print('pdfcheck ignores build dates, creator/producer metadata, PDF IDs and container '
              'encoding; page rasters are compared at 96 dpi and extracted text exactly')
        return 1 if different else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fast', action='store_true')
    ap.add_argument('--check', action='store_true', help='build in TMPDIR and compare recorded PDF content')
    ap.add_argument('--strict', action='store_true',
                    help='fail on an overfull box wide enough to leave the page')
    ap.add_argument('which', nargs='*')
    a = ap.parse_args()
    if a.check:
        try:
            return check(a.which or list(META), a.fast, a.strict)
        except (OSError, subprocess.SubprocessError, ValueError) as exc:
            print(f'pdfcheck: could not compare PDF content ({type(exc).__name__})', file=sys.stderr)
            return 1

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

        # READ THE LOG. Return code and page count both said fine while four tables in the
        # diligence report were printing one character per line and running off the paper —
        # 73 overfull boxes, the worst 1247 pt, about seventeen inches past the margin.
        log = (HERE / 'out' / f'{stem}.log').read_text(errors='replace')
        over = [float(x) for x in re.findall(r'Overfull \\hbox \(([\d.]+)pt too wide\)', log)]
        bad = [x for x in over if x > 5.0]
        note = f', {len(over)} overfull' if over else ''
        print(f'  {stem}.pdf — {pages} pages, {pdf.stat().st_size // 1024} KB{note}')
        if bad and a.strict:
            worst = max(bad)
            print(f'  {stem}: {len(bad)} box(es) over 5pt, worst {worst:.0f}pt — a table or a '
                  'line is leaving the page.', file=sys.stderr)
            ok = False
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
