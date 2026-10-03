#!/usr/bin/env python3
"""The float-claims record: one reviewed disposition for every float-looking block.

`tools/check_float_ledger.py` inventories every block of prose or display text that looks
like a statement about mass, density, lift or floating. This module decides whether each
inventoried block is accounted for. The record lives in `research/analysis/float-claims/`,
one JSON shard per group of files; a file belongs to at most one shard.

A block is keyed by the first 16 hex digits of the SHA-256 of its inventoried text. Editing
a float sentence therefore drops its disposition, and the gate fails until the new sentence
has been read and classed again. A disposition whose block has gone also fails.

A shard is one JSON object:
  {"schema": "float-claims/1",
   "files":   ["docs/FLOAT.md", ...],                 every file this shard answers for
   "dated":   [{"file", "date", "reason"}, ...],      whole files that are dated records
   "entries": [{"file", "key", "line", "class", "reason", ...}, ...]}
`key` decides; `line` must identify an occurrence of that block. The record script refreshes locations. An entry may also carry:
  bindings  a list; each binding names a source and one way of checking it:
              source: {"case": LEDGER_CASE, "field": "at.seaLevel.liftToMass"}
                   or {"source": "research/analysis/x.json", "pointer": "/a/0/b"}
              check:  "shown": "0.558"   the typed figure, compared at its printed precision
                   or "route": "ship.ratio"   a figure the page binder displays in this block
                   or "equals": VALUE    the source value itself, for a sentence with no figure
              options: "scale" (multiply the source first), "abs" (compare magnitudes),
                       "altitude": "seaLevel" | "target" (for a source that is not a ledger row)
  context   typed numbers that are inputs or labels, not results (a safety factor, a date)
  heading   text found within 60 lines above the block (a table header, a caption) that
            names the altitude for a row that cannot name it itself

Classes (a block has exactly one):
  bound           its figures are checked against a ledger row or another generated JSON file
  live-model      every figure is rendered from the model by the page's binder; no verdict
  calculator      a display template whose figures or verdict the page's own script computes
                  from the model; it names that function and the make target that runs the page
  generated       a tracked generator writes the file, whose existing freshness target runs in
                  make check; or an exact marker-delimited region carries generator, gate,
                  verifier and region {start, end}. The generator's --emit returns a JSON
                  path-to-text map, which this gate freshly compares. The named target must
                  invoke the tracked verifier, and that verifier must name the generator.
  literature      someone else's design, or a physical constant; the source is named
  history         a dated record of what was once said; never on a served page. Dated
                  provenance under "dated" never grants an unseen block a disposition; it carries,
                  in its first 12 lines, a notice that links docs/FLOAT-LEDGER.md
  other-quantity  a mass or density that is not a float result (payload, water, a material)
  conditional     a requirement, an assumption or a scenario, and the block says so
  flight-model    a statement of the simulated flight cycle; it names the block of the same
                  file that says the flight model assumes a hull that floats
  question        an open question; only in the two question documents
  method          a computation, definition, principle or requirement naming no design result;
                  every printed number is listed as context and verdict words remain visible
  deferred        unreviewed by this record; owner names an anchored open item and reason
                  explains this block; counted separately, never as a bound pass

Verdict words (floats, neutrally buoyant, a design exists, within N percent, lighter than
air) may appear only in a block classed bound, calculator, literature, history, question, method or deferred.
A flight-model block may say that the simulated ship floats or is buoyant, because its file
states the assumption once; it may not carry the structural verdicts (neutrally buoyant,
a design exists, within N percent, lighter than air).
"Certified world" may appear only in history: nothing in the evidence is certified.

Page rules, for every file that binds a lift-to-mass ratio of a hull:
  P1  the first such block states the sea-level and the working-altitude ratio together;
  P2  one block is bound to `research/analysis/cap-readings.json` (the range of readings).
Ratios print to three decimals; a value below one never rounds up to one.
Each cap-range binding names the altitude encoded in its source pointer.
The same checks apply to ledger-case and JSON-pointer bindings. Every bound binder route
must be covered, and a live-model binder must resolve. A flight assumption explicitly
names the flight model, withholds buoyancy from drawn hulls, binds the ledger verdict,
and links the float case where its reader can open it: an HTML page links the published
page (float/index.html; a link to the directory counts), and a Markdown document links
docs/FLOAT.md. An HTML block that links docs/FLOAT.md is not an assumption block: the site
does not publish docs/. Dated notices name their date as well as linking the ledger.

Usage:
  python3 tools/float_claims.py --propose FILE [FILE ...]   # a shard skeleton, class UNREVIEWED
  python3 tools/float_claims.py --stats                     # counts by class, file and owner
  python3 tools/float_claims.py --write-deferred            # regenerate docs/FLOAT-DEFERRED.md
Deferred owners are declared in DEFERRED_OWNERS with their open-question anchors.
A missing owner or anchor is a record error; an edited block loses its disposition.
The gate also refuses a stale generated deferred list.
The gate itself is `make ledgercheck`, which calls `apply()` below. A block that fits no
class is a question for whoever rules the wording: it is left failing, never forced.

The three pages under float/ are not inventoried, exactly as the generated
docs/FLOAT-LEDGER.md is not: `make floatpagecheck` holds each to a fresh render of its
document, whose review it inherits.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import pathlib
import re
import sys

from float_text import relation, verdict_relation
from float_regions import Regions
from float_qualifiers import check as check_qualifiers

sys.dont_write_bytecode = True
ROOT = pathlib.Path(__file__).resolve().parent.parent
RECORD = ROOT / 'research/analysis/float-claims'
SCHEMA = 'float-claims/1'
LEDGER_PATH = 'research/analysis/float-ledger.json'
CAP_READINGS = 'research/analysis/cap-readings.json'
CLASSES = ('bound', 'live-model', 'calculator', 'generated', 'literature', 'history',
           'other-quantity', 'conditional', 'flight-model', 'question', 'method', 'deferred')
VERDICT_OK = ('bound', 'generated', 'calculator', 'literature', 'history', 'question', 'method', 'deferred')
QUESTION_FILES = ('docs/OPEN-QUESTIONS.md', 'docs/VERIFICATION-PLAN.md')
DEFERRED_PATH = 'docs/FLOAT-DEFERRED.md'
DEFERRED_OWNERS = {
    'energy-model': 'float-deferred-energy-model',
    'mixed-block': 'float-deferred-mixed-block',
    'hand-arithmetic': 'float-deferred-hand-arithmetic',
    'source-needed': 'float-deferred-source-needed',
}
NOTICE_LINES = 12
HEADING_LINES = 60
VERDICT = re.compile(r'\bfloat(?:s|ed)?\b(?!\s+(?:ratio|ledger|window|case|claim|gate|result|verdict))'
                     r'|\bneutrally buoyant\b|\bneutral buoyancy\b|\ba design exists\b'
                     r'|\blighter than (?:the )?air\b'
                     r'|\bwithin (?:two|three|five|\d+(?:\.\d+)?)\s*(?:percent|per cent|%)', re.I)
STRUCTURAL = re.compile(r'\bneutrally buoyant\b|\bneutral buoyancy\b|\ba design exists\b'
                        r'|\blighter than (?:the )?air\b'
                        r'|\bwithin (?:two|three|five|\d+(?:\.\d+)?)\s*(?:percent|per cent|%)', re.I)
ASSUMES = re.compile(r'\bassum', re.I)
BANNED = re.compile(r'certified world', re.I)
CONDITION = re.compile(r'\bassum|\bif\b|\bwould\b|\bscenario|\brequire|\btarget|\bmust\b|\bunverified'
                       r'|\bconditional|\bhypothetical|\bnot yet\b|\bintended|\bplanned|\bneeds?\b'
                       r'|\bmeant to\b|\bdesigned to\b|\bwhen\b|\bshould\b', re.I)
NUM = re.compile(r'(?<![\w.])[-−+]?\d[\d,]*(?:\.\d+)?')
TOKEN = re.compile(r'\[[^\]]*data-(?:n|cat)="[^"]+"[^\]]*\]')
DATE = re.compile(r'^\d{4}-\d{2}(?:-\d{2})?$')


def key_of(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:16]


def visible(text: str) -> str:
    """The inventoried text without the binder tokens the inventory writes in brackets."""
    return TOKEN.sub(' ', text)


def norm(number: str) -> str:
    return number.replace(',', '').replace('−', '-').lstrip('+').strip()


def numbers(text: str) -> list[str]:
    return [norm(m) for m in NUM.findall(visible(text))]


def pointer(doc, path: str):
    for part in [p for p in path.split('/') if p != '']:
        part = part.replace('~1', '/').replace('~0', '~')
        doc = doc[int(part)] if isinstance(doc, list) else doc[part]
    return doc


def dig(doc, path: str):
    for part in path.split('.'):
        doc = doc[int(part)] if isinstance(doc, list) else doc[part]
    return doc


def altitudes(text: str, ledger) -> set:
    found = set()
    if re.search(r'sea[ -]level', text, re.I):
        found.add('seaLevel')
    target = ledger['atmosphere']['targetM']
    if re.search(r'working altitude|target altitude', text, re.I):
        found.add('target')
    for m in re.finditer(r'(\d[\d,]*)\s*m\b', text):
        if float(m[1].replace(',', '')) == float(target):
            found.add('target')
    return found


def check_targets() -> set:
    """The make targets that `make check` runs: a calculator names one of them."""
    for line in (ROOT / 'Makefile').read_text(encoding='utf-8').splitlines():
        if line.startswith('check:'):
            return set(line.split('##')[0].split(':', 1)[1].split())
    return set()


def file_lines(rel: str) -> list:
    path = ROOT / rel
    return path.read_text(encoding='utf-8').splitlines() if path.is_file() else []


def links_to(text, file, target):
    """Require a local Markdown or HTML link resolving to the named document."""
    links = re.findall(r'\]\(([^\s)]+)(?:\s+[^)]*)?\)|href=[\"\']([^\"\']+)', text)
    return any((ROOT / file).parent.joinpath((md or html).split('#')[0]).resolve()
               == (ROOT / target).resolve() for md, html in links)


def links_float_case(text, file):
    """Whether a block links the float case where its reader can open it.

    A page links the published page; a link to its directory counts. A document links the
    document. The site does not publish docs/, so on a page that link would be dead."""
    targets = ('float', 'float/index.html') if file.endswith('.html') else ('docs/FLOAT.md',)
    return any(links_to(text, file, target) for target in targets)


def squash(text: str) -> str:
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]*>', ' ', text)).strip()


class Sources:
    """Read each named JSON file once; resolve a binding to its source value."""
    def __init__(self, ledger):
        self.ledger = ledger
        self.rows = {c['id']: c for d in ledger['designs'] for c in d['cases']}
        self.docs = {LEDGER_PATH: ledger}
        self.regions = Regions(ROOT,check_targets())

    def value(self, b):
        if 'case' in b:
            if b['case'] not in self.rows:
                raise KeyError(f"unknown ledger case {b['case']!r}")
            return dig(self.rows[b['case']], b['field'])
        rel = b.get('source', LEDGER_PATH)
        if rel not in self.docs:
            path = ROOT / rel
            if path.suffix != '.json' or not path.is_file() or ROOT not in path.resolve().parents:
                raise KeyError(f'source {rel!r} is not a JSON file in this repository')
            self.docs[rel] = json.loads(path.read_text(encoding='utf-8'))
        return pointer(self.docs[rel], b['pointer'])

    def ratio_field(self, b):
        """Canonical identity for case and JSON-pointer spellings of hull ratios."""
        if b.get('field', '') in ('at.seaLevel.liftToMass', 'at.target.liftToMass'):
            return b.get('case'), b['field']
        rel, ptr = b.get('source', LEDGER_PATH), b.get('pointer', '')
        match = re.search(r'/(?:at/(seaLevel|target)/liftToMass|(ratioSL|ratio2500))$', ptr)
        if not match:
            return None
        parent = ptr[:match.start()]
        identity = (rel, parent)
        if rel == LEDGER_PATH:
            identity = pointer(self.ledger, parent)['id']
        altitude = match[1] or ('seaLevel' if match[2] == 'ratioSL' else 'target')
        return identity, f'at.{altitude}.liftToMass'


def shown_matches(value, shown: str, scale=1.0, absolute=False) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    value = value * scale
    if absolute:
        value = abs(value)
    places = len(norm(shown).partition('.')[2])
    return f'{value:.{places}f}' == f'{float(norm(shown)):.{places}f}'


def check_entry(entry, hit, sources, ledger):
    """Return a list of reasons this disposition does not hold for this block."""
    errors = []
    text = hit['sentence']
    plain = visible(text)
    cls = entry.get('class')
    definition = re.search(r'\bdefinition of done\b', plain, re.I)
    proposal = (re.search(r'\bretargeting\b.*\bmay still be wanted\b', plain, re.I) and
                re.search(r'\bnot\b\W+a route to floating\b', plain, re.I))
    verdict_text = re.sub(r'\bFLOAT\.md\b', '', plain) if cls == 'conditional' and definition else plain
    if cls not in CLASSES:
        return [f'class {cls!r} is not one of: ' + ', '.join(CLASSES)]
    reason = entry.get('reason', '')
    if not isinstance(reason, str) or not 8 <= len(reason) <= 240:
        errors.append('reason must say why, in 8 to 240 characters')
    if cls == 'deferred' and entry.get('owner') not in DEFERRED_OWNERS:
        errors.append('unknown deferred owner')
    if cls == 'flight-model':
        if STRUCTURAL.search(plain) or verdict_relation(plain):
            errors.append('a flight-model block carries a structural verdict; bind it or reword it')
        if not entry.get('assumption'):
            errors.append('a flight-model block names the key of the block that states the float assumption')
    elif (VERDICT.search(verdict_text) or verdict_relation(verdict_text)) and cls not in VERDICT_OK:
        errors.append(f'verdict words in a block classed {cls}; permitted classes: ' + ', '.join(VERDICT_OK))
    if BANNED.search(plain) and cls != 'history':
        errors.append('"certified world" outside a dated record: nothing in the evidence is certified')
    # A named drawn hull's numeric lift/mass comparison is a result, even when a
    # contributor labels it literature, history, method, conditional or deferred.
    if (re.search(r'\b(?:52 m hull|drawn hull|hull of record)\b',plain,re.I) and
            re.search(r'lift.*(?:exceeds?|exceeded|exceed|clears).*\d',plain,re.I) and
            cls not in ('bound','generated')):
        errors.append('named hull lift comparison requires a checked binding, not a class allowance')
    is_page = hit['file'].endswith('.html')
    bindings = entry.get('bindings', [])
    if cls == 'bound' and not bindings:
        errors.append('a bound block names at least one binding')
    if cls not in ('bound', 'question', 'calculator') and bindings:
        errors.append(f'bindings are checked only on bound, question and calculator blocks, not {cls}')
    routes = {f['route']: f for f in hit.get('dynamicFigures', [])}
    shown = set()
    bound_routes = set()
    need = set()
    for b in bindings:
        if sum(k in b for k in ('shown', 'route', 'equals')) != 1:
            errors.append('a binding carries exactly one of: shown, route, equals')
            continue
        try:
            value = sources.value(b)
            ratio = sources.ratio_field(b)
            errors.extend(check_qualifiers(b, text, sources, ledger))
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            errors.append(f'binding does not resolve: {exc}')
            continue
        if b.get('field', '').startswith('at.'):
            need.add(b['field'].split('.')[1])
        if ratio:
            need.add(ratio[1].split('.')[1])
        if b.get('altitude'):
            need.add(b['altitude'])
        scale = float(b.get('scale', 1))
        if 'equals' in b:
            if value != b['equals'] or isinstance(value, bool) != isinstance(b['equals'], bool):
                errors.append(f"source value {value!r} is not {b['equals']!r}")
        elif 'route' in b:
            bound_routes.add(b['route'])
            fig = routes.get(b['route'])
            if fig is None:
                errors.append(f"route {b['route']!r} is not displayed in this block")
            elif fig.get('display') in (None, 'unresolved'):
                errors.append(f"route {b['route']!r} did not resolve when the page's catalog was executed")
            elif not shown_matches(value, fig['display'], scale, b.get('abs', False)):
                errors.append(f"route {b['route']!r} displays {fig['display']} but its source field is {value!r}")
        elif 'shown' in b:
            s = norm(str(b['shown']))
            shown.add(s)
            if s not in numbers(text):
                errors.append(f"bound figure {b['shown']!r} is not in the visible text")
            elif not shown_matches(value, s, scale, b.get('abs', False)):
                errors.append(f"bound figure {b['shown']!r} differs from its source field ({value!r})")
        else:
            errors.append('a binding carries one of: shown, route, equals')
        is_range = (b.get('source') == CAP_READINGS and
                    re.fullmatch(r'/ranges/[^/]+/(seaLevel|target)/(?:min|max)', b.get('pointer', '')))
        if is_range:
            need.add(is_range[1])
            if b.get('altitude') != is_range[1]:
                errors.append('range altitude must match its source pointer')
        display = b.get('shown') if 'shown' in b else routes.get(b.get('route'), {}).get('display')
        if (ratio or is_range) and display not in (None, 'unresolved'):
            if len(norm(str(display)).partition('.')[2]) != 3:
                errors.append('lift-to-mass ratios print to three decimals')
            if isinstance(value, (int, float)) and value < 1 <= float(norm(str(display))):
                errors.append('a ratio below one must not be rounded up to one')
    heading = entry.get('heading', '')
    if heading:
        above = file_lines(hit['file'])[max(0, int(hit['line']) - 1 - HEADING_LINES):int(hit['line']) - 1]
        if squash(heading) not in squash(' '.join(above)):
            errors.append(f'heading {heading!r} is not in the {HEADING_LINES} lines above the block')
            heading = ''
    missing = need - altitudes(plain + ' ' + heading, ledger)
    if missing:
        words = {'seaLevel': 'sea level', 'target': f"{ledger['atmosphere']['targetM']:,} m"}
        errors.append('the block does not name the altitude of its bound figure: '
                      + ', '.join(words.get(a, a) for a in sorted(missing)))
    if cls in ('bound', 'live-model', 'method'):
        context = {norm(str(c)) for c in entry.get('context', [])}
        loose = sorted({n for n in numbers(text) if n not in shown and n not in context})
        if loose:
            errors.append('numbers neither bound nor listed as context: ' + ', '.join(loose))
    if cls == 'live-model' and not routes:
        errors.append('a live-model block displays at least one figure through the page binder')
    if cls == 'live-model':
        for route, fig in routes.items():
            if fig.get('display') in (None, 'unresolved'):
                errors.append(f"route {route!r} did not resolve when the page's catalog was executed")
    if cls == 'bound' and routes.keys() - bound_routes:
        errors.append('routes without bindings: ' + ', '.join(sorted(routes.keys() - bound_routes)))
    if cls == 'calculator':
        function = entry.get('function', '')
        if not function or function not in '\n'.join(file_lines(hit['file'])):
            errors.append('a calculator names a function, present in its file, that computes what it displays')
        if entry.get('gate') not in check_targets():
            errors.append('a calculator names the make target, run by `make check`, that executes its page')
    if cls == 'generated':
        gen = entry.get('generator', '')
        if not gen or not (ROOT / gen).is_file() or gen not in sources.regions.tracked:
            errors.append('a generated block names the tracked script that writes its file')
        if entry.get('gate') not in check_targets():
            errors.append('a generated block names a freshness target run by make check')
        if entry.get('region'):
            errors.extend(sources.regions.check(entry,hit))
        elif is_page:
            errors.append('generated is for analysis notes, not for a served page')
    if cls == 'literature' and not entry.get('source'):
        errors.append('a literature block names its source')
    if cls == 'history':
        if not DATE.match(str(entry.get('date', ''))):
            errors.append('a history block names its date as YYYY-MM or YYYY-MM-DD')
        if is_page:
            errors.append('history is for dated documents; a served page states the present')
    if cls == 'conditional' and not (CONDITION.search(plain) or definition or proposal):
        errors.append('a conditional block says in its own words that it is an assumption, a requirement or a scenario')
    if cls == 'question' and hit['file'] not in QUESTION_FILES:
        errors.append('question is for ' + ' and '.join(QUESTION_FILES))
    return errors


def load_record():
    """Return ({file: {key: entry}}, {file: dated entry}, [errors]) from every shard."""
    owned, dated, errors = {}, {}, []
    if not RECORD.is_dir():
        return owned, dated, errors
    for shard in sorted(RECORD.glob('*.json')):
        rel = shard.relative_to(ROOT).as_posix()
        try:
            doc = json.loads(shard.read_text(encoding='utf-8'))
        except json.JSONDecodeError as exc:
            errors.append(f'{rel}: not JSON ({exc})')
            continue
        if doc.get('schema') != SCHEMA:
            errors.append(f'{rel}: schema is not {SCHEMA}')
            continue
        files = doc.get('files', [])
        for name in files:
            if name in owned:
                errors.append(f'{rel}: {name} already belongs to another shard')
            owned.setdefault(name, {})
        for entry in doc.get('dated', []):
            name = entry.get('file')
            reason = entry.get('reason', '')
            if name not in files:
                errors.append(f'{rel}: dated file {name!r}, which the shard does not list under files')
            elif name.endswith('.html'):
                errors.append(f'{rel}: {name}: a served page states the present; it is never a dated record')
            elif not DATE.match(str(entry.get('date', ''))):
                errors.append(f'{rel}: {name}: a dated file names its date as YYYY-MM or YYYY-MM-DD')
            elif not isinstance(reason, str) or not 8 <= len(reason) <= 240:
                errors.append(f'{rel}: {name}: reason must say why, in 8 to 240 characters')
            elif not file_lines(name):
                errors.append(f'{rel}: dated file {name} does not exist')
            elif not (entry['date'] in '\n'.join(file_lines(name)[:NOTICE_LINES]) and
                      links_to('\n'.join(file_lines(name)[:NOTICE_LINES]), name, 'docs/FLOAT-LEDGER.md')):
                errors.append(f'{rel}: {name}: a dated file carries, in its first {NOTICE_LINES} lines, a notice that '
                              'names its date and links docs/FLOAT-LEDGER.md')
            else:
                dated[name] = dict(entry, _shard=rel)
        for entry in doc.get('entries', []):
            name, key = entry.get('file'), entry.get('key')
            if name not in files:
                errors.append(f'{rel}: entry for {name!r}, which the shard does not list under files')
                continue
            if key in owned[name]:
                errors.append(f'{rel}: {name} has two entries with key {key}')
            if entry.get('class') == 'deferred':
                owner = entry.get('owner')
                if owner not in DEFERRED_OWNERS:
                    errors.append(f'{rel}: {name}: unknown deferred owner {owner!r}')
                else:
                    questions = '\n'.join(file_lines('docs/OPEN-QUESTIONS.md'))
                    anchor = re.escape(DEFERRED_OWNERS[owner])
                    if not re.search(r'<a\s+id=[\"\']' + anchor + r'[\"\']\s*>', questions):
                        errors.append(f'{rel}: {name}: missing open-item anchor for {owner}')
            owned[name][key] = dict(entry, _shard=rel)
    return owned, dated, errors


def apply(hits, ledger):
    """Give every failing inventoried block its recorded disposition, or say why it has none.

    Mutates `hits` (status and reason) and returns the record-level errors. A block the
    path rules already allow is left alone.
    """
    owned, dated, errors = load_record()
    sources = Sources(ledger)
    seen = {name: set() for name in owned}
    ratio_blocks = {}
    assumptions = {}
    flights = []
    for hit in hits:
        if hit.get('pointer') is not None or 'sentence' not in hit:
            continue
        name, key = hit['file'], key_of(hit['sentence'])
        hit['key'] = key
        entry = owned.get(name, {}).get(key)
        if entry is not None:
            seen[name].add(key)
        if hit['status'] == 'ALLOW' or (hit['status'] == 'PASS' and entry is None):
            continue
        if entry is None:
            hit['reason'] = ('No disposition in research/analysis/float-claims/ for this text'
                             + ('' if name in owned else ' (the file belongs to no shard)') + '. ' + hit['reason'])
            continue
        problems = check_entry(entry, hit, sources, ledger)
        locations = {int(h['line']) for h in hits if h.get('file')==name and key_of(h.get('sentence',''))==key}
        if int(entry.get('line',0)) not in locations:
            problems.append('record line does not identify an occurrence of its block')
        if problems:
            hit['status'] = 'FAIL'
            hit['reason'] = '; '.join(problems)
            continue
        hit['status'] = ('PASS' if entry['class'] == 'bound' else
                         'DEFERRED' if entry['class'] == 'deferred' else 'ALLOW')
        if entry['class'] == 'deferred':
            hit['owner'] = entry['owner']
            hit['deferredReason'] = entry['reason']
        hit['disposition'] = entry['class']
        hit['reason'] = f"{entry['class']}: {entry['reason']}"
        if entry['class'] == 'flight-model':
            flights.append((hit, entry))
        assumption_text = visible(hit['sentence'])
        verdict_bound = any(b.get('source') == LEDGER_PATH and b.get('pointer') == '/verdict'
                            and b.get('equals') == 'Nothing floats today as drawn.'
                            for b in entry.get('bindings', []))
        if (entry['class'] == 'bound' and verdict_bound and ASSUMES.search(assumption_text)
                and re.search(r'flight (?:model|simulation)', assumption_text, re.I)
                and re.search(r'hull.*float', assumption_text, re.I)
                and re.search(r'no drawn hull|nothing floats today as drawn|no.*hull.*(?:drawn|float)',
                              assumption_text, re.I)
                and links_float_case(hit.get('raw', hit['sentence']), name)):
            assumptions.setdefault(name, set()).add(key)
        if entry['class'] == 'bound':
            fields = {field for b in entry.get('bindings', []) if (field := sources.ratio_field(b))}
            capped = any(b.get('source') == CAP_READINGS for b in entry.get('bindings', []))
            ratio_blocks.setdefault(name, []).append((int(hit['line']), fields, capped))
    for hit, entry in flights:
        if entry['assumption'] not in assumptions.get(hit['file'], set()):
            hit['status'] = 'FAIL'
            hit.pop('disposition', None)
            hit['reason'] = (f"flight-model: no bound block with key {entry['assumption']} in this file says that "
                             'the flight model assumes a hull that floats')
    for name, keys in owned.items():
        for key in sorted(set(keys) - seen[name]):
            errors.append(f"{keys[key]['_shard']}: stale entry {key} for {name} (line {keys[key].get('line', '?')}): "
                          'its text changed or was removed; class the new text and delete this entry')
    for name, blocks in sorted(ratio_blocks.items()):
        with_ratio = sorted(b for b in blocks if b[1])
        if not with_ratio:
            continue
        line, fields, _ = with_ratio[0]
        cases = {c for c, _ in fields}
        both = any({(c, 'at.seaLevel.liftToMass'), (c, 'at.target.liftToMass')} <= fields for c in cases)
        if not both:
            errors.append(f'{name}:{line}: P1: the first block that states a lift-to-mass ratio gives one altitude; '
                          'state the sea-level and the working-altitude ratio of the same case together')
        if not any(b[2] for b in blocks):
            errors.append(f'{name}: P2: the page states a lift-to-mass ratio but no block is bound to {CAP_READINGS}; '
                          'say once that the bill and the drawing disagree in the end caps and that no reading reaches 1')
    return errors


def deferred_counts(hits):
    """Count inventoried occurrences, including repeated text, separately from passes."""
    counts = {}
    for hit in hits:
        if hit.get('status') == 'DEFERRED':
            owner = hit['owner']
            counts[owner] = counts.get(owner, 0) + 1
    return dict(sorted(counts.items()))


def deferred_markdown(hits):
    """Render the public list from current locations and recorded reasons."""
    rows = sorted((h for h in hits if h.get('status') == 'DEFERRED'),
                  key=lambda h: (h['file'], h['line'], h['key']))
    def escape(value):
        return str(value).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('|', '&#124;').replace('\n', ' ')
    out = ['# Deferred statements', '',
           'This record has not reviewed the blocks listed here. '
           'Deferral assigns an open item; it does not approve a claim or count as a bound pass.', '',
           'Generated by `python3 tools/float_claims.py --write-deferred`.', '',
           '| File and line | Open item | Reason |', '| --- | --- | --- |']
    for h in rows:
        owner = h['owner']
        out.append(f"| {escape(h['file'])}:{h['line']} | "
                   f"[{owner}](OPEN-QUESTIONS.md#{DEFERRED_OWNERS[owner]}) | "
                   f"{escape(h['deferredReason'])} |")
    if not rows:
        out += ['', 'No blocks are currently deferred.']
    return '\n'.join(out) + '\n'


def check_deferred(hits):
    path = ROOT / DEFERRED_PATH
    try:
        current = path.read_text(encoding='utf-8')
    except OSError:
        return [f'{DEFERRED_PATH}: generated list unavailable; run --write-deferred']
    if current != deferred_markdown(hits):
        return [f'{DEFERRED_PATH}: stale generated list; run --write-deferred']
    return []


def write_deferred(hits):
    """Write the list and its metadata dispositions without excluding it from inventory."""
    import check_float_ledger as gate
    path = ROOT / DEFERRED_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(deferred_markdown(hits), encoding='utf-8')
    entries = []
    for line, text, raw in gate.source_blocks(path):
        entries.append(dict(file=DEFERRED_PATH, line=line, key=key_of(text),
                            **{'class': 'method'}, context=sorted(set(numbers(text))),
                            reason='Generated review metadata lists unresolved source requirements; it approves no quoted design result.'))
    RECORD.mkdir(parents=True, exist_ok=True)
    doc = dict(schema=SCHEMA, files=[DEFERRED_PATH], entries=entries)
    (RECORD / 'deferred-list.json').write_text(json.dumps(doc, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--propose', nargs='+', metavar='FILE')
    ap.add_argument('--stats', action='store_true')
    ap.add_argument('--write-deferred', action='store_true', help='regenerate the public list and its metadata record')
    args = ap.parse_args()
    sys.path.insert(0, str(ROOT / 'tools'))
    import check_float_ledger as gate
    ledger = json.loads((ROOT / LEDGER_PATH).read_text(encoding='utf-8'))
    hits = gate.inventory(ledger)
    errors = apply(hits, ledger)
    if args.write_deferred:
        if errors:
            for error in errors:
                print('record: ' + error)
            return 1
        write_deferred(hits)
        print('deferred list: generated ' + DEFERRED_PATH)
        return 0
    if args.propose:
        wanted = [pathlib.Path(f).as_posix() for f in args.propose]
        entries, done = [], set()
        for hit in hits:
            if hit['file'] in wanted and hit['status'] == 'FAIL' and 'key' in hit and (hit['file'], hit['key']) not in done:
                done.add((hit['file'], hit['key']))
                entries.append({'file': hit['file'], 'key': hit['key'], 'line': hit['line'], 'class': 'UNREVIEWED',
                                'reason': '', 'text': hit['sentence'][:200],
                                'routes': [f['route'] for f in hit.get('dynamicFigures', [])],
                                'numbers': sorted(set(numbers(hit['sentence'])))})
        print(json.dumps({'schema': SCHEMA, 'files': wanted, 'entries': entries}, ensure_ascii=False, indent=1))
        return 0
    if args.stats:
        by_class, by_file = {}, {}
        for hit in hits:
            if hit.get('pointer') is not None or 'sentence' not in hit:
                continue
            label = hit.get('disposition') or ('UNDISPOSED' if hit['status'] == 'FAIL' else 'path-class allowance')
            by_class[label] = by_class.get(label, 0) + 1
            if hit['status'] == 'FAIL':
                by_file[hit['file']] = by_file.get(hit['file'], 0) + 1
        for label, n in sorted(by_class.items(), key=lambda kv: (-kv[1], kv[0])):
            print(f'{n:5d}  {label}')
        for owner in DEFERRED_OWNERS:
            print(f'{deferred_counts(hits).get(owner, 0):5d}  deferred to {owner}')
        for name, n in sorted(by_file.items(), key=lambda kv: (-kv[1], kv[0])):
            print(f'{n:5d}  undisposed in {name}')
        for e in errors:
            print('record:', e)
        return 0
    ap.print_help()
    return 0


if __name__ == '__main__':
    sys.exit(main())
