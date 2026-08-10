#!/usr/bin/env python3
"""Turn the reports in research/reports/ into LaTeX, so the PDFs cannot drift from them.

    python3 tools/md2tex.py            # convert all three
    python3 tools/md2tex.py 01-brief   # just one

WHY A CONVERTER AND NOT A SECOND SET OF SOURCES. The obvious way to get a good PDF is to
write LaTeX by hand. That gives you two copies of every sentence, and this project has
already watched what happens to two copies of anything: `docs/PHYSICS.md` disagreed with
itself by a factor of 24, one solar constant lived in five files and was wrong in all five.
A report and its PDF disagreeing is worse than either being wrong, because the PDF is the
one that gets forwarded. So the Markdown is the source and this builds the LaTeX from it.

It handles the dialect these three documents actually use — headings, paragraphs, bullet and
numbered lists, pipe tables with alignment, bold, italic, inline code, links, block quotes,
rules, footnote-ish parentheticals — and nothing else. An unknown construct is an error, not
a silent pass-through, because a swallowed line in a document nobody proofreads is exactly
the failure this file exists to prevent.

MARKERS AND DIRECTIVES. `13,183<!--f:P10000.cycle.tph-->` becomes `\\F{P10000.cycle.tph}`, so
the number in the PDF comes from the model rather than from the prose — the same rule
`tools/check_figures.py` enforces on the Markdown, carried through to print. Directives that
are invisible in Markdown add what only print needs:

    <!--tex:fig charts/ledger.pdf | Where the energy goes. | 0.92-->
    <!--tex:headline TITLE | body text-->
    <!--tex:keypoint TITLE | body text-->
    <!--tex:limit TITLE | body text-->
    <!--tex:stats 13,183 t/h | delivered by one P-10000 ;; 4.59 kWh | per tonne-->
    <!--tex:pagebreak-->
    <!--tex:skip-->          drop the NEXT block from the PDF only
"""
from __future__ import annotations

import argparse
import decimal
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPORTS = ROOT / 'research' / 'reports'
PDFDIR = ROOT / 'research' / 'pdf'
FIGURES = ROOT / 'research' / 'figures.json'

CITE = re.compile(r'([-−]?[\d][\d,]*(?:\.\d+)?)(\s*(?:[^\d<]{0,24}?))<!--\s*f:([A-Za-z0-9_.]+)\s*-->')
DIRECTIVE = re.compile(r'^<!--\s*tex:(\w+)\s*(.*?)-->\s*$', re.S)


def flatten(obj, prefix=''):
    out = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            out.update(flatten(v, f'{prefix}{k}.'))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out.update(flatten(v, f'{prefix}{i}.'))
    else:
        out[prefix[:-1]] = obj
    return out


def esc(s: str) -> str:
    """Escape for LaTeX text. Order matters: backslash first, and never touch what we emit."""
    out = []
    for ch in s:
        out.append({
            '\\': r'\textbackslash{}', '{': r'\{', '}': r'\}', '$': r'\$', '&': r'\&',
            '#': r'\#', '%': r'\%', '_': r'\_', '~': r'\textasciitilde{}',
            '^': r'\textasciicircum{}',
        }.get(ch, ch))
    return ''.join(out)


UNI = (('—', '---'), ('–', '--'), ('−', '--'), ('…', r'\ldots{}'),
       ('×', r'\,\texttimes\,'), ('≤', r'$\leq$'), ('≥', r'$\geq$'),
       ('→', r'~$\rightarrow$~'), ('∓', r'$\mp$'), ('±', r'$\pm$'),
       ('²', r'\textsuperscript{2}'), ('³', r'\textsuperscript{3}'),
       ('₂', r'\textsubscript{2}'), ('°', r'\textdegree{}'),
       ('·', r'\textperiodcentered{}'), ('¢', r'\textcent{}'), ('§', r'\S{}'),
       ('“', '``'), ('”', "''"), ('‘', '`'), ('’', "'"))


def texify(s: str) -> str:
    """Directive text is passed through to LaTeX so a caption can carry \textbf{}, but a bare
    % still comments out the rest of the line and takes the closing brace with it — which is
    how a caption reading "moved ±20%" killed a build. Escape the characters that are never
    markup here, leave the backslash alone."""
    for a, b in UNI:
        s = s.replace(a, b)
    out, i = [], 0
    while i < len(s):
        ch = s[i]
        if ch == '\\':
            out.append(s[i:i + 2]); i += 2; continue
        out.append({'%': r'\%', '&': r'\&', '#': r'\#', '_': r'\_'}.get(ch, ch))
        i += 1
    return ''.join(out)


VALUES: dict = {}


def inline(s: str, keys: set[str], src: str) -> str:
    """Inline markup -> LaTeX. Figure markers become \\F{} and keep their unit."""
    slots: list[str] = []

    def stash(tex: str) -> str:
        slots.append(tex)
        return f'\x00{len(slots) - 1}\x00'

    def cite(m):
        raw, tail, key = m.group(1), m.group(2), m.group(3)
        full = key if key in VALUES else f'classes.{key}'
        if full not in VALUES:
            raise SystemExit(f'{src}: no such figure key — f:{key}')
        # RESOLVE HERE, at the precision the author wrote. A \F{} macro would emit the stored
        # value and print "35.36 min" where the source says "35.4 min" — correct against the
        # model and wrong against the sentence around it. The converter runs from figures.json
        # on every build, so substituting now is exactly as fresh and never mismatched.
        dp = len(raw.split('.')[1]) if '.' in raw else 0
        q = decimal.Decimal(str(float(VALUES[full]))).quantize(
            decimal.Decimal(1).scaleb(-dp), rounding=decimal.ROUND_HALF_UP)
        txt = f'{q:,.{dp}f}' if ',' in raw else f'{q:.{dp}f}'
        # The tail carries the unit ("%", "MWh"). It must be STASHED as well: returning it
        # escaped but unprotected let the final esc() pass over the whole string escape it a
        # second time, and "+5.25%" printed as "+5.25\%".
        return stash(r'\lining{' + txt.replace('-', '--') + '}') + stash(esc(tail))

    s = CITE.sub(cite, s)
    # Any marker left over had no number in front of it — check_figures says the same thing.
    if '<!--' in s:
        leftover = re.search(r'<!--.*?-->', s, re.S)
        raise SystemExit(f'{src}: stray comment in prose — {leftover.group(0)[:60]}')

    s = re.sub(r'`([^`]+)`', lambda m: stash(r'\texttt{' + esc(m.group(1)) + '}'), s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)',
               lambda m: stash(r'\href{' + m.group(2).replace('%', r'\%').replace('#', r'\#')
                               + '}{' + esc(m.group(1)) + '}'), s)
    s = re.sub(r'\*\*([^*]+)\*\*', lambda m: stash(r'\textbf{' + esc(m.group(1)) + '}'), s)
    s = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', lambda m: stash(r'\emph{' + esc(m.group(1)) + '}'), s)
    s = re.sub(r'<sup>([^<]+)</sup>', lambda m: stash(r'\textsuperscript{' + esc(m.group(1)) + '}'), s)
    s = re.sub(r'<br\s*/?>', lambda m: stash(r'\\'), s)

    s = esc(s)
    # Typographic repairs the source writes as plain characters.
    for src_ch, tex in UNI:
        s = s.replace(src_ch, tex)
    # Placeholders NEST: a figure marker inside a bold span is stashed first, so the bold
    # slot contains the marker's placeholder. re.sub does not rescan its replacements, so a
    # single pass leaves a raw NUL in the output and pdflatex says "invalid character".
    for _ in range(12):
        s, n = re.subn(r'\x00(\d+)\x00', lambda m: slots[int(m.group(1))], s)
        if not n:
            break
    else:
        raise SystemExit(f'{src}: inline markup nested more than 12 deep')
    return s


def table(block: list[str], keys: set[str], src: str) -> str:
    rows = [[c.strip() for c in ln.strip().strip('|').split('|')] for ln in block]
    spec_row = rows[1]
    # `---:` right, `:---:` centre, anything else left.
    align = ''.join('c' if (c.strip().startswith(':') and c.strip().endswith(':'))
                    else ('r' if c.strip().endswith(':') else 'l') for c in spec_row)
    body = [rows[0]] + rows[2:]
    ncol = len(spec_row)
    # The first column is the label column and wraps; numeric columns should not.
    colspec = ('@{}' + ('>{\\raggedright\\arraybackslash}X' if align[0] == 'l' else align[0])
               + ''.join(align[1:]) + '@{}')
    out = [r'\begin{tabularx}{\linewidth}{' + colspec + '}', r'\toprule']
    head = ' & '.join(r'{\sffamily\bfseries\small ' + inline(c, keys, src) + '}'
                      for c in body[0][:ncol])
    out += [head + r' \\', r'\midrule']
    for r in body[1:]:
        cells = (r + [''] * ncol)[:ncol]
        out.append(' & '.join(inline(c, keys, src) for c in cells) + r' \\')
    out += [r'\bottomrule', r'\end{tabularx}']
    return '\n'.join(out)


def directive(kind: str, arg: str) -> str:
    parts = [texify(p.strip()) for p in arg.split('|')]
    if kind == 'fig':
        path, cap = parts[0], parts[1] if len(parts) > 1 else ''
        width = parts[2] if len(parts) > 2 else '1.0'
        return '\\placedfig{' + path + '}{' + cap + '}{' + width + '}'
    if kind in ('headline', 'keypoint', 'limit'):
        cmd = {'headline': 'headline', 'keypoint': 'keypoint', 'limit': 'limitbox'}[kind]
        return '\\' + cmd + '{' + parts[0] + '}{' + (parts[1] if len(parts) > 1 else '') + '}'
    if kind == 'stats':
        items = [texify(p.strip()) for p in arg.split(';;')]
        cells = []
        for it in items:
            big, _, lab = it.partition('|')
            cells.append('\\bignum{' + big.strip() + '}{}\\\\[1pt]{\\sffamily\\scriptsize\\color{muted}'
                         + lab.strip() + '}')
        w = round(1.0 / max(1, len(cells)) - 0.01, 3)
        return ('\\par\\medskip\\noindent' + ''.join(
            f'\\begin{{minipage}}[t]{{{w}\\linewidth}}\\raggedright ' + c + '\\end{minipage}%\n'
            for c in cells) + '\\par\\medskip')
    if kind == 'pagebreak':
        return r'\clearpage'
    if kind == 'skip':
        return '\x01SKIP\x01'
    raise SystemExit(f'unknown tex directive: {kind}')


def convert(md: str, keys: set[str], src: str) -> str:
    lines = md.split('\n')
    out: list[str] = []
    i, skip_next = 0, False
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
            continue

        m = DIRECTIVE.match(ln.strip())
        if m:
            tex = directive(m.group(1), m.group(2))
            if tex == '\x01SKIP\x01':
                skip_next = True
            else:
                out.append(tex)
            i += 1
            continue

        if ln.startswith('---') and set(ln.strip()) == {'-'}:
            out.append(r'\thinrule')
            i += 1
            continue

        if ln.startswith('#'):
            level = len(ln) - len(ln.lstrip('#'))
            text = inline(ln[level:].strip(), keys, src)
            if skip_next:
                skip_next = False
            elif level == 1:
                out.append(r'\reporttitle{' + text + '}')
            else:
                cmd = {2: 'section', 3: 'subsection', 4: 'subsubsection'}.get(level, 'subsubsection')
                out.append('\\' + cmd + '*{' + text + '}')
                out.append('\\addcontentsline{toc}{' + ('section' if level == 2 else 'subsection')
                           + '}{' + text + '}')
            i += 1
            continue

        if ln.lstrip().startswith('> '):
            block = []
            while i < len(lines) and lines[i].lstrip().startswith('>'):
                block.append(lines[i].lstrip()[1:].strip())
                i += 1
            body = inline(' '.join(x for x in block if x), keys, src)
            out.append(r'\begin{quote}\itshape ' + body + r'\end{quote}')
            continue

        if ln.lstrip().startswith('|'):
            block = []
            while i < len(lines) and lines[i].lstrip().startswith('|'):
                block.append(lines[i])
                i += 1
            if skip_next:
                skip_next = False
            else:
                out.append(table(block, keys, src))
            continue

        if re.match(r'^\s*[-*]\s+', ln):
            items, i = read_list(lines, i, r'^\s*[-*]\s+')
            out.append(render_list('itemize', items, keys, src))
            continue

        if re.match(r'^\s*\d+\.\s+', ln):
            items, i = read_list(lines, i, r'^\s*\d+\.\s+')
            out.append(render_list('enumerate', items, keys, src))
            continue

        # paragraph
        block = []
        while i < len(lines) and lines[i].strip() and not lines[i].startswith('#') \
                and not lines[i].lstrip().startswith(('|', '> ')) \
                and not re.match(r'^\s*([-*]|\d+\.)\s+', lines[i]) \
                and not DIRECTIVE.match(lines[i].strip()) \
                and not (lines[i].startswith('---') and set(lines[i].strip()) == {'-'}):
            block.append(lines[i].strip())
            i += 1
        if skip_next:
            skip_next = False
        else:
            out.append(inline(' '.join(block), keys, src))
    return '\n\n'.join(out)


def read_list(lines: list[str], i: int, pat: str) -> tuple[list[str], int]:
    items: list[str] = []
    while i < len(lines):
        ln = lines[i]
        if re.match(pat, ln):
            items.append(re.sub(pat, '', ln).strip())
            i += 1
        elif ln.startswith('  ') and ln.strip() and items:
            items[-1] += ' ' + ln.strip()
            i += 1
        else:
            break
    return items, i


def render_list(env: str, items: list[str], keys: set[str], src: str) -> str:
    body = '\n'.join(r'\item ' + inline(x, keys, src) for x in items)
    return f'\\begin{{{env}}}\n{body}\n\\end{{{env}}}'


def write_figures_tex(flat: dict) -> int:
    """Emit \\F{} definitions. Numbers get thousands separators and keep their precision."""
    lines = ['% GENERATED by tools/md2tex.py from research/figures.json — do not edit.',
             '% Every \\F{key} in the documents resolves here, so a PDF cannot quote a number',
             '% the model has moved past.', '']
    for k in sorted(flat):
        v = flat[k]
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            continue
        if float(v) == int(v) and abs(v) >= 1000:
            txt = f'{int(v):,}'
        elif float(v) == int(v):
            txt = str(int(v))
        else:
            txt = f'{v:,}'
        txt = txt.replace('-', '--')
        lines.append(r'\expandafter\def\csname fig@' + k + r'\endcsname{' + txt + '}')
    (PDFDIR / 'figures.tex').write_text('\n'.join(lines) + '\n')
    return sum(1 for k in flat if isinstance(flat[k], (int, float)) and not isinstance(flat[k], bool))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('which', nargs='*', help='report stems, e.g. 01-brief')
    args = ap.parse_args()

    flat = flatten(json.loads(FIGURES.read_text()))
    VALUES.update(flat)
    n = write_figures_tex(flat)
    keys = set(flat)
    print(f'md2tex: figures.tex — {n} keys')

    stems = args.which or ['01-brief', '02-paper', '03-diligence']
    for stem in stems:
        src = REPORTS / f'{stem}.md'
        if not src.exists():
            print(f'md2tex: no such report — {src}', file=sys.stderr)
            return 1
        body = convert(src.read_text(), keys, src.name)
        (PDFDIR / f'{stem}.body.tex').write_text(body + '\n')
        print(f'md2tex: {stem}.body.tex — {len(body.splitlines())} lines')
    return 0


if __name__ == '__main__':
    sys.exit(main())
