#!/usr/bin/env python3
"""Offline tier 1 occurrence inventory and claims gate. See research/claims/README.md."""
from __future__ import annotations

import argparse
import csv
import io
from collections import Counter, defaultdict
import hashlib
from html import unescape
from html.parser import HTMLParser
import json
import math
from pathlib import Path
import re
import subprocess
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_figures import CITE, flatten, matches_display

ROOT = Path(__file__).resolve().parents[1]
SCOPE = ('Static public text and model-bound spans: manifest HTML, README.md, GOALS.md, reports; '
         'then PHYSICS, ARCHITECTURE, analysis Markdown, simulator/test/tool READMEs and DATA-SOURCES. '
         'History, source notes without dated reviews, PDFs, other runtime values and image pixels remain outside scope.')

WORDS = ('zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen '
         'fifteen sixteen seventeen eighteen nineteen twenty thirty forty fifty sixty seventy '
         'eighty ninety hundred thousand million billion first second third fourth fifth sixth '
         'seventh eighth ninth tenth half halves quarter quarters single double twice dozen').split()
NUMBER = re.compile(r'(?<![\w])(?:[-+−]?(?:\d+(?:,\d{3})*(?:\.\d+)?|\.\d+)(?:[eE][+-]?\d+)?)'
                    r'|\d+(?:\.\d+)?|[⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉½¼¾]'
                    r'|\b(?:' + '|'.join(WORDS) + r')(?:[- ](?:' + '|'.join(WORDS) + r'))*\b', re.I)
BLOCK = set('p li td th h1 h2 h3 h4 h5 h6 figcaption dt dd blockquote text title desc '
            'button label option summary pre output textarea div section article nav header footer '
            'form fieldset legend table tr ul ol dl main figure body'.split())
VOID = set('area base br col embed hr img input link meta param source track wbr'.split())
FALLBACK = {'FALLBACK', 'FALLBACK-HUD', 'FALLBACK-ROSTER', 'FALLBACK-FIRES'}
LABEL = re.compile(r'\b(vision|assumption|assumed|target|historical)\b', re.I)
KINDS = {'model-span', 'model', 'generated', 'delegated', 'cited', 'nonclaim', 'labelled', 'ledger'}


def digest(value):
    return hashlib.sha256(value.encode()).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'))


def marker_action(text):
    text = text.strip()
    if text in FALLBACK:
        return text, True
    if text.startswith('/') and text[1:] in FALLBACK:
        return text[1:], False
    if text in {'mass-budget:plant-comparators:start', 'mass-budget:plant-comparators:end'}:
        return 'mass-budget:plant-comparators', text.endswith(':start')
    m = re.fullmatch(r'(energy|served-energy|readme|logistics|atmosphere|solar|battery|editorial):([a-z-]+):(start|end)', text)
    return (m[1] + ':' + m[2], m[3] == 'start') if m else (None, None)


def read_json(path):
    return json.loads(path.read_text())


def register_text(value):
    encode = lambda obj: json.dumps(obj, ensure_ascii=False, separators=(',', ':'), allow_nan=False)
    fields = []
    for key, obj in value.items():
        text = '[\n' + ',\n'.join(encode(row) for row in obj) + '\n]' if key == 'entries' else encode(obj)
        fields.append(encode(key) + ':' + text)
    return '{\n' + ',\n'.join(fields) + '\n}\n'


def write_json(path, value):
    text = register_text(value) if path.name == 'register.json' else json.dumps(value, ensure_ascii=False, indent=2) + '\n'
    if not path.exists() or path.read_text() != text:
        path.write_text(text)


def normal(text):
    return re.sub(r'\s+', ' ', unescape(text)).strip()


def clean_markdown(text):
    # Keep marker identity on the numeric token, not on its unit or a neighbouring numeral.
    text = CITE.sub(lambda m: m[1] + '〖' + m[2] + '〗' +
                    m[0][len(m[1]):m[0].index('<!--')], text)
    text = re.sub(r'<!--.*?-->', '', text, flags=re.S)
    text = re.sub(r'!?\[([^\]]*)\]\([^)]*\)', r'\1', text)
    text = re.sub(r'<(https?://[^>]+)>', r'\1', text)
    text = re.sub(r'<[^>]+>', '', text)
    return normal(re.sub(r'[*`]', '', text))


def public_excerpt(text):
    """Excerpts are for review; identity always hashes the unmodified source sentence."""
    text = re.sub(r"(?:\x2fhome\x2f|\x7e\x2f)[^\s<>`]+", "[local path]", text)
    text = re.sub(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", "[address]", text)
    text = re.sub(r"(?:https?://)?(?:[A-Za-z0-9-]+\.)+[A-Za-z]{2,}(?:/[^\s<>]*)?", "[link]", text)
    return text


def safe_relative(root, name):
    path = root / name
    if Path(name).is_absolute() or '..' in Path(name).parts or not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('path must stay inside the selected root')
    return path


def tier_files(root, manifest):
    served, partial = [], []
    for raw in manifest.read_text().splitlines():
        row = raw.strip().split(None, 2)
        if not row or row[0].startswith('#'):
            continue
        if row[0] in {'served', 'PARTIAL'}:
            if len(row) < 2:
                raise ValueError('malformed publish manifest')
            safe_relative(root, row[1])
            (served if row[0] == 'served' else partial).append(row[1])
    paths = {root / 'README.md', root / 'GOALS.md'}
    paths.update((root / 'research/reports').glob('*.md'))
    for name in served:
        src = safe_relative(root, name)
        if not src.exists():
            raise ValueError(f'manifest served entry missing: {name}')
        for path in ([src] if src.is_file() else sorted(src.rglob('*.html'))):
            rel = path.relative_to(root).as_posix()
            if path.suffix.lower() == '.html' and not any(rel == p or rel.startswith(p + '/') for p in partial):
                safe_relative(root, rel)
                paths.add(path)
    extra = [root/'docs/PHYSICS.md', root/'docs/ARCHITECTURE.md',
             *sorted((root/'research/analysis').glob('*.md')), root/'sim/README.md',
             root/'tests/README.md', root/'tools/README.md', root/'DATA-SOURCES.md']
    return sorted(paths) + [p for p in extra if p.is_file() and p not in paths]


class Reader(HTMLParser):
    """Each text node has one nearest block owner; inline markup never splits a sentence."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.units = []
        self.region = None
        self.order = 0
        self.scripts = []

    def emit(self, text, surface, region=None, context='', attrs=None, order=None):
        if normal(text):
            self.units.append(dict(text=normal(text), surface=surface, region=region,
                                   context=normal(context), attrs=attrs or {},
                                   order=self.order if order is None else order))
            self.order += 1

    def handle_comment(self, text):
        name, start = marker_action(text)
        if name is None:
            return
        for e in self.stack:
            if e['parts']:
                self.emit(''.join(e['parts']), e['tag'], e['region'], attrs=e['attrs'], order=e['order'])
                e['parts'].clear()
        self.region = name if start else None
        for e in self.stack:
            e['region'] = self.region

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for binding in ('data-n', 'data-cat'):
            if binding in a:
                self.emit(a[binding], 'model-span', self.region, context=binding, attrs=a)
                self.units[-1]['binding_line'] = self.getpos()[0]
        if any(e['tag'] in {'script', 'style'} for e in self.stack):
            return
        for key in ('alt', 'aria-label', 'aria-description', 'aria-valuetext', 'title', 'placeholder', 'aria-valuenow'):
            if a.get(key):
                self.emit(a[key], key, self.region, attrs=a)
        if tag == 'meta' and a.get('content'):
            self.emit(a['content'], 'metadata', self.region, context=a.get('name', a.get('property', '')), attrs=a)
        if tag == 'input' and a.get('value') and a.get('type', 'text') not in {'hidden', 'checkbox', 'radio'}:
            self.emit(a['value'], 'default', self.region, context=a.get('id', '') + ' ' + a.get('aria-label', ''), attrs=a)
        if tag == 'br':
            self.handle_data(' ')
        if tag not in VOID:
            self.stack.append(dict(tag=tag, attrs=a, parts=[], region=self.region, order=self.order, unit_start=len(self.units)))
            self.order += 1

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_data(self, data):
        if any(e['tag'] == 'style' for e in self.stack):
            return
        owner = next((e for e in reversed(self.stack) if e['tag'] in BLOCK or e['tag'] == 'script'), None)
        if owner is None:
            self.emit(data, 'text', self.region)
        else:
            owner['parts'].append(data)

    def handle_endtag(self, tag):
        index = next((i for i in range(len(self.stack) - 1, -1, -1) if self.stack[i]['tag'] == tag), None)
        if index is None:
            return
        for e in self.stack[index:][::-1]:
            if e['tag'] == 'tr':
                cells = [u for u in self.units[e['unit_start']:] if u['surface'] in {'td', 'th'}]
                row = ' | '.join(u['text'] for u in cells)
                for i, cell in enumerate(cells):
                    cell['context'] = str(i) + ' | ' + row
            value = ''.join(e['parts'])
            if e['tag'] == 'script':
                self.scripts.append((value, e['attrs']))
            else:
                self.emit(value, e['tag'], e['region'], attrs=e['attrs'], order=e['order'])
        del self.stack[index:]

    def finish(self):
        if self.stack:
            self.handle_endtag(self.stack[0]['tag'])
        self.units.sort(key=lambda u: u['order'])
        # Static markup in script templates and literal assignments to rendered DOM fields.
        # Expressions are blanked; their runtime values belong to browser/model gates.
        for code, attrs in self.scripts:
            if attrs.get('type') == 'application/ld+json':
                def visit(obj):
                    if isinstance(obj, dict):
                        for v in obj.values():
                            visit(v)
                    elif isinstance(obj, list):
                        for v in obj:
                            visit(v)
                    elif isinstance(obj, (str, int, float)) and not isinstance(obj, bool):
                        self.emit(str(obj), 'structured-metadata')
                visit(json.loads(code))
                continue
            for static in re.finditer(r'\.(?:textContent|innerText|value)\s*=\s*([-+]?\d+(?:\.\d+)?)\s*[;,]', code):
                self.emit(static[1], 'script-default')
            literal = re.compile(r'`(?:\\.|[^`])*`|"(?:\\.|[^"\\])*"|\'(?:\\.|[^\'\\])*\'', re.S)
            for m in literal.finditer(code):
                value = m[0][1:-1]
                prefix = code[max(0, m.start() - 120):m.start()]
                markup = bool(re.search(r'<(?:p|span|div|input|output|td|th|text|option|li|label|h[1-6])\b', value))
                sink = bool(re.search(r'(?:\.(?:textContent|innerText|innerHTML|value|title)\s*=\s*|'
                                      r'document\.write\(\s*|insertAdjacentHTML\([^,]+,\s*|'
                                      r'setAttribute\(["\'](?:alt|aria-label|title)["\'],\s*)$', prefix))
                # Literal arms of a conditional assigned to a displayed field are also
                # public defaults. This is conservative and inventories both arms.
                conditional_sink = bool(re.search(r'\.(?:textContent|innerText|innerHTML|value)\s*=[^;]*[?:]\s*$', prefix))
                if not (markup or sink or conditional_sink):
                    continue
                value = re.sub(r'\\u([0-9a-fA-F]{4})|\\x([0-9a-fA-F]{2})',
                               lambda e: chr(int(e[1] or e[2], 16)), value)
                value = re.sub(r'\$\{[^}]*\}', ' ', value)
                value = value.replace('\\n', '\n').replace('\\"', '"').replace("\\'", "'")
                if markup:
                    child = Reader()
                    child.feed(value)
                    child.finish()
                    for unit in child.units:
                        unit['surface'] = 'script-default:' + unit['surface']
                        self.units.append(unit)
                else:
                    self.emit(value, 'script-default')
        return self.units


def markdown_units(source):
    # README's checked producer has both indented and inline region markers.
    source = re.sub(r'(<!--\s*readme:[a-z-]+:(?:start|end)\s*-->)', r'\n\1\n', source)
    # Markdown permits embedded HTML. Capture attributes too, without double-counting
    # its visible text (which the Markdown pass below already retains).
    reader = Reader()
    reader.feed(source)
    html_units = reader.finish()
    units = [u for u in html_units if u['surface'] in {
        'alt', 'aria-label', 'aria-description', 'aria-valuetext', 'aria-valuenow',
        'title', 'metadata', 'default', 'placeholder', 'structured-metadata'} or u['surface'].startswith('script-default')]
    buf = []
    fenced = False
    headers = []
    active_region = None
    def emit(text, surface, context=''):
        units.append(dict(text=clean_markdown(text), surface=surface, context=clean_markdown(context),
                          region=active_region, attrs={}))
    def flush():
        if buf:
            emit(' '.join(buf), 'paragraph')
            buf.clear()
    for line in source.splitlines():
        marker = re.fullmatch(r'\s*<!--\s*(.*?)\s*-->\s*', line)
        name, start = marker_action(marker[1]) if marker else (None, None)
        if name:
            flush()
            active_region = name if start else None
            continue
        if fenced or line.startswith('    '):
            # A marker comment in displayed example code is itself visible. Its numeric
            # identifier is a separate occurrence as well as the adjacent bound value.
            for comment in re.finditer(r'<!--.*?-->', line):
                units.append(dict(text=normal(comment[0]), surface='code-comment', context='', region=None, attrs={}))
        if re.match(r'^\s*(```|~~~)', line):
            flush()
            fenced = not fenced
            continue
        if fenced:
            emit(line, 'code')
        elif not line.strip():
            flush()
            headers = []
        elif line.lstrip().startswith('|'):
            flush()
            cells = re.split(r'(?<!\\)\|', line.strip())[1:-1]
            if all(re.fullmatch(r'[\s:-]+', c) for c in cells):
                continue
            if not headers:
                headers = cells
            for i, cell in enumerate(cells):
                emit(cell, 'cell', ' | '.join([cells[0], str(i), headers[i] if i < len(headers) else '', line]))
        elif re.match(r'^\s*(?:#{1,6}\s|[-*+]\s|\d+[.)]\s|>)', line):
            flush()
            if line.lstrip().startswith('#'):
                emit(re.sub(r'^\s*#+\s*', '', line), 'heading')
            else:
                buf.append(line)
        else:
            buf.append(line)
    flush()
    return units


def extract(root, manifest):
    occurrences, files = [], []
    for path in tier_files(root, manifest):
        rel = path.relative_to(root).as_posix()
        files.append(rel)
        source = path.read_text()
        if path.suffix == '.html':
            reader = Reader()
            reader.feed(source)
            units = reader.finish()
        else:
            units = markdown_units(source)
        ordinals = Counter()
        for unit in units:
            if unit['surface'] == 'model-span':
                key = unit['text']
                text_part = 'Model span ' + canonical(dict(attribute=unit['context'], key=key, attrs=unit['attrs']))
                sentence_hash = digest(text_part)
                ordinals[sentence_hash] += 1
                occurrences.append(dict(id=f"{rel}::{sentence_hash}::{ordinals[sentence_hash]}", file=rel,
                    digest=sentence_hash, ordinal=ordinals[sentence_hash], text=text_part, raw=key,
                    surface='model-span', block=text_part, context=unit['context'], region=unit['region'],
                    marker=None, before='', after='', attrs=unit['attrs'], binding_line=unit.get('binding_line')))
                continue
            text, keys = unit['text'], {}
            # Remove invisible key sentinels after recording the preceding token's end.
            for m in list(re.finditer(r'〖([^〗]+)〗', text))[::-1]:
                text = text[:m.start()] + text[m.end():]
            shift = 0
            for m in re.finditer(r'〖([^〗]+)〗', unit['text']):
                keys[m.start() - shift] = m[1]
                shift += m.end() - m.start()
            block = normal(text)
            # Cells, attributes and SVG labels are atomic. Prose paragraphs use sentences.
            spans = list(re.finditer(r'.+?(?:[.!?](?=\s+[A-Z])|$)', text)) if unit['surface'] in {
                'paragraph', 'p', 'li', 'div', 'section', 'article', 'blockquote'} else [re.match(r'[\s\S]*', text)]
            for sentence in spans:
                if not sentence:
                    continue
                text_part = normal(sentence[0])
                sentence_hash = digest(text_part)
                for match in NUMBER.finditer(sentence[0]):
                    ordinals[sentence_hash] += 1
                    ordinal = ordinals[sentence_hash]
                    pos = sentence.start() + match.start()
                    raw = match[0]
                    occurrences.append(dict(
                        id=f'{rel}::{sentence_hash}::{ordinal}', file=rel, digest=sentence_hash,
                        ordinal=ordinal, text=text_part, raw=raw, surface=unit['surface'],
                        block=block, context=unit['context'], region=unit['region'],
                        marker=keys.get(sentence.start() + match.end()),
                        before=text[max(0, pos - 40):pos], after=text[pos + len(raw):pos + len(raw) + 45],
                        attrs=unit['attrs']))
    return dict(version=1, scope=SCOPE, files=files, occurrences=occurrences)


def function_word_rule(occ):
    """Only explicitly tested grammatical roles; physical counts remain claims."""
    raw, before, after = occ['raw'].lower(), occ['before'], occ['after']
    if raw in {'first', 'second', 'third', 'fourth', 'fifth'}:
        if not before.strip() and re.match(r',\s', after):
            return 'discourse-ordinal'
        if re.search(r'\bthe\s+$', before, re.I) and re.match(r'\s+is\b', after):
            return 'discourse-ordinal'
        if re.match(r'\s+on the list\b', after, re.I):
            return 'discourse-ordinal'
        if re.match(r'\s+(?:draft|commit|review round|question|job)\b', after, re.I):
            return 'document-or-process-order'
    if raw == 'first' and re.match(r'-party\b', after, re.I):
        return 'named-word'
    if raw == 'one':
        if re.match(r'-(?:way|off)\b', after, re.I):
            return 'named-word'
        if re.search(r'\b(?:no|each)\s+$', before, re.I) and re.match(r'\s+(?:has|can|needs|browsable|carrying)\b', after, re.I):
            return 'pronominal-one'
        if re.match(r'\s+(?:where|that|which)\b', after, re.I):
            return 'pronominal-one'
        if re.search(r'\b(?:small|buildable|central|tempting)\s+$', before, re.I) and re.match(r'[.,;:!?)]|$', after):
            return 'pronominal-one'
    if raw == 'single' and re.match(r'\s+(?:biggest|right answer|point of failure)\b', after, re.I):
        return 'idiomatic-single'
    return None


def nonclaim_rule(occ):
    raw, before, after, text = (occ[k] for k in ('raw', 'before', 'after', 'text'))
    function = function_word_rule(occ)
    if function:
        return function
    if raw in '⁰¹²³⁴⁵⁶⁷⁸⁹₀₁₂₃₄₅₆₇₈₉' and re.search(r'[A-Za-zµΩ)]$', before):
        return 'unit-exponent-or-formula-index'
    if re.search(r'(?:\bP[-‑–]?|\bO|\bLN|\bCO|\bSHIP-|\bship )$', before, re.I) and raw.isdigit():
        return 'named-identifier'
    if occ['surface'] == 'metadata':
        name = occ['attrs'].get('name', '')
        if name == 'theme-color' and re.fullmatch(r'#[0-9a-fA-F]{3,8}', text):
            return 'rendering-metadata'
        if name == 'viewport' and re.fullmatch(r'width=device-width,\s*initial-scale=1(?:\.0)?', text):
            return 'rendering-metadata'
    if raw == '3' and re.match(r'D\b', after):
        return 'named-identifier'
    if re.search(r'\b\d{4}-\d{2}-\d{2}\b', text) and re.fullmatch(r'\d{4}|-?\d{2}', raw):
        # Check this token, not the presence of some date elsewhere in the sentence.
        window = before + raw + after
        at = len(before)
        if any(m.start() <= at < m.end() for m in re.finditer(r'\b\d{4}-\d{2}-\d{2}\b', window)):
            return 'iso-date'
    if occ['surface'] in {'heading', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'paragraph', 'li', 'p'}:
        if not before.strip(' *#') and re.match(r'[.)]\s', after) and re.fullmatch(r'\d+(?:\.\d+)?', raw):
            return 'section-or-step'
    if re.search(r'§§?\s*\d+[–—-]$', before) and raw.isdigit():
        return 'section-range-endpoint'
    if re.search(r'§§?\s*$', before) and re.fullmatch(r'\d+(?:\.\d+)*', raw):
        return 'section-symbol-reference'
    if re.search(r'\b(?:section|step|figure|fig\.|table|defect|item|chapter|level)\s+#?$', before, re.I) and raw.isdigit():
        return 'cross-reference'
    if re.search(r'\bv$', before) and re.fullmatch(r'\d+(?:\.\d+)?', raw):
        return 'version'
    return None


def placement(occ):
    return dict(surface=occ['surface'], block_digest=digest(occ['block']),
                context_digest=digest(occ['context']), region=occ['region'], marker=occ['marker'])


def entry_for(occ, owner=None, gate='claimscheck'):
    return dict(id=occ['id'], file=occ['file'], digest=occ['digest'], ordinal=occ['ordinal'],
                text=public_excerpt(occ['text']), raw=occ['raw'], placement=placement(occ), owner=owner, gate=gate)


def model_issue(occ, owner, flat):
    key = owner['key']
    value = flat.get(key)
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value):
        return dict(kind='missing-model-key', key=key, observed=occ['raw'], expected='finite figure')
    dp = owner['precision']
    printed_dp = len(occ['raw'].split('.')[1]) if '.' in occ['raw'] else 0
    if dp != printed_dp:
        return dict(kind='precision-mismatch', key=key, observed=printed_dp, expected=dp)
    try:
        if not matches_display(value, occ['raw'], dp):
            return dict(kind='stale-model', key=key, observed=occ['raw'], expected=value)
    except (ValueError, ArithmeticError):
        return dict(kind='invalid-model-display', key=key, observed=occ['raw'], expected=value)
    return water_basis_issue(occ, key)


DELIVERY = re.compile(r'\bdeliver(?:s|ed|ing|y|ies|ing-water)?\b', re.I)


def water_basis_issue(occ, key):
    if key.endswith(('.cycle.tph', '.cycle.kwhPerTonne', '.cycle.deliveredT')):
        words = occ['text'] + ' ' + occ['context']
        if DELIVERY.search(words):
            return dict(kind='water-basis', key=key, observed=occ['raw'],
                        expected='water requested, kept aboard and delivered per cycle over the planned lines; released water is not suppression; bind a reviewed exact-input plan')
    return None


def inventory(root, gate, contract):
    argv = contract['command']
    if not isinstance(argv, list) or not all(isinstance(a, str) for a in argv) or '--inventory' not in argv:
        raise ValueError(f'{gate}: inventory command must be an argv list with --inventory')
    result = subprocess.run(argv, cwd=root, capture_output=True, text=True, timeout=15)
    if result.returncode:
        raise ValueError(f'{gate}: inventory command failed (exit {result.returncode})')
    data = json.loads(result.stdout)
    if data.get('version') != 1 or data.get('gate') != gate or not isinstance(data.get('occurrences'), list):
        raise ValueError(f'{gate}: invalid inventory contract')
    ids = data['occurrences']
    if not all(isinstance(i, str) for i in ids) or len(ids) != len(set(ids)):
        raise ValueError(f'{gate}: duplicate or invalid inventory occurrence')
    return set(ids)


def validate_entry(entry):
    for field in ('id', 'file', 'digest', 'ordinal', 'text', 'raw', 'placement', 'owner', 'gate'):
        if field not in entry:
            raise ValueError(f'register entry missing {field}')
    owner = entry['owner']
    if owner is None:
        if entry['gate'] != 'claimscheck':
            raise ValueError('unowned entry must use claimscheck')
        return
    kind = owner.get('kind')
    if kind not in KINDS:
        raise ValueError('invalid owner kind')
    required = {
        'model-span': ['key', 'attribute', 'producer', 'format'],
        'ledger': ['record', 'key', 'reason'],
        'model': ['key', 'precision', 'unit', 'scenario'],
        'generated': ['generator', 'region'], 'delegated': ['inventory'],
        'cited': ['source', 'locator', 'review'], 'nonclaim': ['rule'], 'labelled': ['label'],
    }[kind]
    if any(k not in owner for k in required):
        raise ValueError(f'{kind} owner missing required field')
    if kind == 'model' and (type(owner['precision']) is not int or not 0 <= owner['precision'] <= 12
                            or not owner['scenario'] or not owner['unit']):
        raise ValueError('model needs display precision, unit and scenario')
    if kind == 'nonclaim' and owner['rule'] == 'exact' and not owner.get('reason'):
        raise ValueError('exact nonclaim exception needs a reason')
    if kind == 'cited':
        review = owner['review']
        if not owner['locator'] or not all(review.get(k) for k in ('by', 'date', 'digest')):
            raise ValueError('cited owner needs locator and dated, digest-bound reviewer')
        if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', review['date']):
            raise ValueError('invalid citation review date')


def failure(occ, entry, flat, root, inventories, sources, rules=None):
    if placement(occ) != entry['placement']:
        return dict(kind='placement-changed', observed=placement(occ), expected=entry['placement'])
    owner = entry['owner']
    if owner is None:
        return dict(kind='unowned', observed=occ['raw'], expected='an accountable owner and check')
    kind = owner['kind']
    if rules is None and (kind in {'ledger', 'model-span'} or owner.get('rule') in {'section-symbol-reference','section-range-endpoint'}):
        from claims_rules import Context
        rules = Context(root, [occ['file']])
    if kind == 'model-span':
        return rules.span_issue(occ, entry)
    if kind == 'ledger':
        if occ['marker']:
            issue = water_basis_issue(occ, 'classes.' + occ['marker'])
            if issue:
                return issue
        if rules is None:
            from claims_rules import Context
            rules = Context(root, [occ['file']])
        return rules.ledger_issue(occ, entry)
    if kind in {'nonclaim', 'labelled', 'cited'} and entry['gate'] != 'claimscheck':
        return dict(kind='wrong-gate', observed=entry['gate'], expected='claimscheck')
    if kind == 'model':
        if entry['gate'] != 'claimscheck':
            return dict(kind='wrong-gate', observed=entry['gate'], expected='claimscheck')
        return model_issue(occ, owner, flat)
    if kind == 'nonclaim':
        if owner['rule'] in {'section-symbol-reference','section-range-endpoint'}:
            issue = rules.reference_issue(occ)
            if issue:
                return issue
        if owner['rule'] != 'exact' and nonclaim_rule(occ) != owner['rule']:
            return dict(kind='nonclaim-rule-miss', observed=nonclaim_rule(occ), expected=owner['rule'])
    elif kind == 'labelled':
        from claims_rules import label_for
        if label_for(occ) != owner['label']:
            return dict(kind='label-missing', observed=occ['raw'], expected=owner['label'])
    elif kind == 'generated':
        if owner['generator'] == 'analysis-figure':
            if rules is None:
                from claims_rules import Context
                rules = Context(root, [occ['file']])
            return rules.analysis_issue(occ, entry)
        if owner['generator'] in {'tools/gen_energy_pages.mjs', 'research/analysis/energy-documents.mjs', 'tools/gen_float_pages.py', 'tools/noticegen.py', 'tools/gen_readme.py', 'research/analysis/energy-tables.mjs', 'research/analysis/energy-omissions.mjs', 'research/analysis/energy-unheld.mjs', 'research/analysis/energy-descent.mjs', 'research/analysis/energy-motion.mjs', 'tools/gen_logistics_prose.py', 'research/analysis/loaded-atmosphere.mjs', 'tools/gen_solar_prose.py', 'tools/gen_solar_budget_comparison.py', 'research/analysis/battery-ratios.mjs', 'tools/gen_editorial_prose.py', 'tools/gen_assembly_prose.py', 'research/analysis/delivery.py', 'tools/gen_mass_budget_prose.py'}:
            if rules is None:
                from claims_rules import Context
                rules = Context(root, [occ['file']])
            return rules.generated_issue(occ, entry)
        if owner['generator'] == 'figure-marker':
            if entry['gate'] != 'figcheck' or owner['region'] != occ['marker'] or not occ['file'].startswith('research/reports/'):
                return dict(kind='generator-region-miss', observed=occ['marker'], expected=owner['region'])
            key = occ['marker']
            model = dict(key=key if key in flat else 'classes.' + key,
                         precision=len(occ['raw'].split('.')[1]) if '.' in occ['raw'] else 0)
            return model_issue(occ, model, flat)
        if owner['generator'] == 'tools/gen_fallback.py':
            if (entry['gate'] != 'fallbackcheck' or occ['file'] != 'index.html' or
                    owner['region'] not in FALLBACK or occ['region'] != owner['region']):
                return dict(kind='generator-region-miss', observed=occ['region'], expected=owner['region'])
            source = (root / occ['file']).read_text()
            start, end = '<!--' + owner['region'] + '-->', '<!--/' + owner['region'] + '-->'
            if source.count(start) != 1 or source.count(end) != 1 or source.index(start) >= source.index(end):
                return dict(kind='generator-region-miss', observed='unbalanced markers', expected=owner['region'])
            if not (root / owner['generator']).is_file():
                return dict(kind='generator-missing', observed=None, expected=owner['generator'])
        else:
            return dict(kind='generator-unsupported', observed=owner['generator'], expected='reviewed region adapter')
    elif kind == 'delegated':
        if owner.get('arithmetic'):
            issue = model_issue(occ, owner['arithmetic'], flat)
            if issue:
                return issue
        if owner['inventory'] != entry['gate'] or occ['id'] not in inventories.get(entry['gate'], set()):
            return dict(kind='delegation-miss', observed=occ['raw'], expected=entry['gate'])
    elif kind == 'cited':
        source = sources.get(owner['source'])
        if source is None:
            return dict(kind='source-missing', observed=owner['source'], expected='research/sources.json record')
        local = source.get('file')
        reason = source.get('noCaptureReason') or owner.get('no_capture_reason')
        if not (local and safe_relative(root / 'research', local).is_file()) and not reason:
            return dict(kind='capture-missing', observed=local, expected='local capture or recorded no-capture reason')
        if owner['review']['digest'] != occ['digest']:
            return dict(kind='review-void', observed=occ['digest'], expected=owner['review']['digest'])
    return None


def index_unique(rows, field, what):
    result = {}
    for row in rows:
        key = row[field]
        if key in result:
            raise ValueError(f'duplicate {what}: {key}')
        result[key] = row
    return result


def check(root, manifest, figures, register_path, accept_new=False):
    extracted = extract(root, manifest)
    occurrences = index_unique(extracted['occurrences'], 'id', 'extracted occurrence')
    register = read_json(register_path)
    if register.get('version') != 1:
        raise ValueError('unsupported register version')
    entries = index_unique(register['entries'], 'id', 'register entry')
    flat = flatten(read_json(figures))
    from claims_rules import Context
    rules = Context(root, extracted['files'])
    sources_path = root / 'research/sources.json'
    sources = index_unique(read_json(sources_path)['sources'], 'id', 'source') if sources_path.exists() else {}
    contracts = register.get('delegations', {})
    if len(contracts) > 2:
        raise ValueError('at most two delegated inventory commands are supported in the offline time budget')
    inventories = {}
    for gate, contract in contracts.items():
        pending = contract.get('optional_until_present')
        if pending and not safe_relative(root, pending).exists():
            continue
        inventories[gate] = inventory(root, gate, contract)
    for gate, ids in inventories.items():
        if ids - occurrences.keys():
            raise ValueError(f'{gate}: orphaned delegated inventory occurrence: {sorted(ids - occurrences.keys())[0]}')
    for entry in entries.values():
        validate_entry(entry)
    defects_path = register_path.parent / 'known-defects.json'
    ratchet_path = register_path.parent / 'accepted-defects.json'
    defects = read_json(defects_path)
    if defects.get('version') != 1 or not 1 <= len(defects['headlines']) <= 7:
        raise ValueError('known defects need one to seven public headline groups')
    known = {}
    for defect in defects['defects']:
        if not defect.get('closes') or not defect.get('problem') or defect['headline'] not in defects['headlines']:
            raise ValueError('defect needs headline, problem and closure')
        if not defect.get('occurrences'):
            raise ValueError('empty known defect')
        for oid in defect['occurrences']:
            if oid in known:
                raise ValueError(f'duplicate known defect: {oid}')
            known[oid] = defect
    accepted = read_json(ratchet_path) if ratchet_path.exists() else {'version': 1, 'accepted': {}, 'runs': []}
    if accepted.get('version') != 1:
        raise ValueError('unsupported ratchet version')
    previous = accepted['accepted']
    accepted_sources = accepted.get('source_digests', {})
    if set(previous) != set(accepted_sources):
        raise ValueError('ratchet needs a source digest for every accepted occurrence')
    previous = dict(previous)
    recorded = {}
    for run in accepted.get('runs', []):
        if run.get('digest') != digest(canonical({oid: previous[oid] for oid in run['added']})):
            raise ValueError('ratchet acceptance receipt changed')
        for oid in run['added']:
            if oid in recorded:
                raise ValueError('duplicate ratchet acceptance')
            recorded[oid] = True
    if set(recorded) != set(previous):
        raise ValueError('ratchet entries lack an --accept-new receipt')
    retired = {}
    for transition in accepted.get('transitions', []):
        changes = transition['changes']
        if transition['digest'] != digest(canonical(changes)):
            raise ValueError('carry transition receipt changed')
        for oid, change in changes.items():
            if previous.get(oid) != change['before']:
                raise ValueError('carry transition does not follow accepted history')
            if change['after'] is None:
                previous.pop(oid, None)
                retired[oid] = change
            else:
                previous[oid] = change['after']
                retired.pop(oid, None)
    errors, pending = [], {}
    for oid, change in retired.items():
        if oid in occurrences:
            entry = entries.get(oid)
            if (entry is None or digest(canonical(entry)) != change.get('entry_digest') or
                    failure(occurrences[oid], entry, flat, root, inventories, sources, rules) is not None):
                errors.append(f'{oid}: carry retirement no longer has a verified owner')
        else:
            path = safe_relative(root, oid.split('::')[0])
            if path.exists() and digest(path.read_text()) == change['source_before']:
                errors.append(f'{oid}: ratchet: retirement requires changed page bytes, not a narrower inventory')

    counts = {file: Counter() for file in extracted['files']}
    for oid, old in previous.items():
        if oid not in known:
            if oid in occurrences:
                errors.append(f'{oid}: ratchet: defect removed but its occurrence is still published')
            path = safe_relative(root, oid.split('::')[0])
            if path.exists() and digest(path.read_text()) == accepted_sources.get(oid):
                errors.append(f'{oid}: ratchet: retirement requires changed page bytes, not a narrower inventory')
        if oid in known and old != digest(canonical(known[oid])):
            errors.append(f'{oid}: ratchet: accepted defect changed; preserve its evidence')
    for oid, entry in entries.items():
        if oid not in occurrences:
            owner = entry['owner'] or {}
            key = owner.get('key', owner.get('region', 'unowned'))
            candidates = [o for o in extracted['occurrences'] if o['file'] == entry['file'] and o['ordinal'] == entry['ordinal'] and o['id'] not in entries]
            # A numeric-only edit preserves the sentence's word skeleton. This is diagnostic
            # matching only: it NEVER transfers ownership or a review onto changed text.
            skeleton = lambda s: NUMBER.sub('#', s)
            changed = [o['raw'] for o in candidates if skeleton(public_excerpt(o['text'])) == skeleton(entry['text'])]
            errors.append(f"{oid}: orphaned register entry; old={entry['raw']} new={','.join(changed) or 'missing/changed text'} key={key}")
    for oid, occ in occurrences.items():
        row = counts[occ['file']]
        row['occurrences'] += 1
        entry = entries.get(oid)
        if entry is None:
            row['unregistered'] += 1
            errors.append(f"{oid}: UNREGISTERED {occ['surface']} value={occ['raw']} text={public_excerpt(occ['text'])[:150]}")
            continue
        if any(entry[k] != occ[k] for k in ('file', 'digest', 'ordinal', 'raw')) or entry['text'] != public_excerpt(occ['text']):
            errors.append(f'{oid}: register identity/payload mismatch')
        problem = failure(occ, entry, flat, root, inventories, sources, rules)
        defect = known.get(oid)
        if defect:
            row['known-defect'] += 1
            if problem != defect['failure']:
                errors.append(f'{oid}: known defect no longer reproduces: recorded={canonical(defect["failure"])} now={canonical(problem)}')
            elif oid not in previous:
                pending[oid] = digest(canonical(defect))
                if not accept_new:
                    errors.append(f'{oid}: ratchet: new defect needs check --accept-new')
        elif problem:
            errors.append(f'{oid}: {canonical(problem)}')
        else:
            owner = entry['owner']
            kind = owner['kind']
            row[kind] += 1
            if kind == 'nonclaim':
                row['rule:' + owner['rule']] += 1
    for oid in known.keys() - occurrences.keys():
        errors.append(f'{oid}: known defect no longer reproduces: occurrence removed or changed; retire it and re-register the corrected text')
    if accept_new and not errors and pending:
        for oid in sorted(pending):
            print(f'ACCEPT NEW {oid}: {canonical(known[oid]["failure"])}')
        accepted['accepted'].update(pending)
        accepted.setdefault('source_digests', {}).update({
            oid: digest(safe_relative(root, occurrences[oid]['file']).read_text()) for oid in pending})
        accepted['runs'].append(dict(added=sorted(pending), digest=digest(canonical(pending))))
        write_json(ratchet_path, accepted)
    try:
        outputs = audit_outputs(root, register_path, register, defects, rules)
    except (KeyError, ValueError, OSError) as exc:
        errors.append('audit tables: regeneration unavailable (' + type(exc).__name__ + ')')
        outputs = {}
    for name, fresh in outputs.items():
        path = register_path.parent / name
        if not path.is_file() or path.read_text() != fresh:
            errors.append(name + ': missing or stale audit table; run carry and review the drift')
    print(SCOPE)
    print('file | occurrences | model | model-span | generated | delegated | cited | nonclaim | labelled | ledger | known defect | unregistered')
    columns = ['occurrences', 'model', 'model-span', 'generated', 'delegated', 'cited', 'nonclaim', 'labelled', 'ledger', 'known-defect', 'unregistered']
    for file, row in counts.items():
        print(file + ' | ' + ' | '.join(str(row[c]) for c in columns))
        rules = ', '.join(f'{k[5:]}={v}' for k, v in sorted(row.items()) if k.startswith('rule:'))
        if rules:
            print('  nonclaim rules: ' + rules)
    totals = sum(counts.values(), Counter())
    print('TOTAL | ' + ' | '.join(str(totals[c]) for c in columns))
    groups = Counter(d['headline'] for d in known.values())
    for name, headline in defects['headlines'].items():
        print(f'Known defects: {groups[name]} | {headline}')
    for error in errors:
        print('claimscheck: ' + error)
    print(f'claimscheck: {"FAIL" if errors else "PASS"}; {len(errors)} errors; {len(known)} known defect occurrences')
    return 1 if errors else 0


def defect_for(occ, problem):
    kind = problem['kind']
    if kind == 'stale-model':
        headline, need = 'stale', 'a generator or a rewording'
    elif kind == 'water-basis':
        headline, need = 'water', 'a rewording of the model water basis'
    elif kind in {'delegation-miss', 'float-deferred', 'float-record-miss'}:
        headline, need = 'float', 'a ledger entry or a rewording'
    elif kind == 'broken-reference':
        headline, need = 'reference', 'a rewording that names an existing section'
    elif occ['surface'].startswith(('script-default', 'model-span')) or occ['surface'] in {'default', 'text', 'aria-label', 'desc'}:
        headline, need = 'generated', 'a generator'
    elif occ['file'].startswith(('research/', 'docs/', 'DATA-SOURCES')):
        headline, need = 'review', 'a citation with a dated review, a generator, or a label'
    else:
        headline, need = 'unowned', 'a generator, a label, or a citation with a dated review'
    return dict(occurrences=[occ['id']], headline=headline,
                problem='The occurrence needs ' + need + '. ' + str(problem.get('expected', '')),
                failure=problem, closes='Supply ' + need + '; carry and recheck the exact occurrence.')


def tsv(rows):
    """Quote tabs/newlines as data; keep excerpts safe for the public repository."""
    output = io.StringIO(newline='')
    writer = csv.writer(output, delimiter='\t', lineterminator='\n')
    writer.writerows([[str(value) for value in row] for row in rows])
    return output.getvalue()


def residue_text(entries, defects, rules=None):
    by_id = {e['id']: e for e in entries}
    rows = [['File', 'Headline', 'Sentence', 'Number or model key', 'Reason', 'Owner needed', 'Occurrence ID']]
    for defect in sorted(defects, key=lambda d: (by_id[d['occurrences'][0]]['file'], d['occurrences'][0])):
        for oid in defect['occurrences']:
            entry = by_id[oid]
            sentence = entry['text']
            basis = (entry['owner'] or {}).get('physical_basis')
            if basis and rules is not None:
                hit = next((h for h in rules.floats().get(entry['file'], []) if h['key'] == basis['key']), None)
                if hit:
                    from float_claims import TOKEN
                    sentence = clean_markdown(TOKEN.sub(' ', hit['sentence']))
            reason = defect['problem'] + ' ' + str(defect['failure']['expected'])
            kind = defect['failure']['kind']
            need = ('rewording' if kind in {'water-basis', 'broken-reference'} else
                    'ledger entry or rewording' if kind.startswith('float-') or kind == 'delegation-miss' else
                    'generator' if defect['headline'] in {'generated', 'stale'} else
                    'citation with a dated review, generator, or label')
            rows.append([entry['file'], defect['headline'], public_excerpt(sentence), entry['raw'], public_excerpt(reason), need, oid])
    return tsv(rows)


def nonclaim_text(entries):
    rules = {'discourse-ordinal', 'document-or-process-order', 'named-word', 'pronominal-one', 'idiomatic-single', 'section-range-endpoint'}
    rows = [['File', 'Word', 'Rule', 'Sentence', 'Occurrence ID']]
    for e in entries:
        owner = e['owner'] or {}
        if owner.get('kind') == 'nonclaim' and owner.get('rule') in rules:
            rows.append([e['file'], e['raw'], owner['rule'], public_excerpt(e['text']), e['id']])
    return tsv(rows)


def carry_report_text(root, register_path, register, defects):
    out = register_path.parent
    baseline = read_json(out / 'carry-report-baseline.json')
    history_path = out / 'carry-history.json'
    history = read_json(history_path)['runs'] if history_path.exists() else []
    before = history[0]['files'] if history else {}
    rows = [['Kind', 'Item', 'Occurrences before', 'Occurrences current', 'Defects before', 'Defects current', 'Detail']]
    for line, text in enumerate(baseline['text'].splitlines(), 1):
        if not text:
            continue
        rows.append(['historical snapshot', str(line), '', '', '', '', text])
    files = Counter(e['file'] for e in register['entries'])
    known = Counter(oid.split('::')[0] for d in defects['defects'] for oid in d['occurrences'])
    for name in sorted(set(before) | set(files)):
        old = before.get(name, {})
        rows.append(['current file', name, old.get('then', 0), files[name], old.get('defects_then', 0), known[name],
                     'Original supplied inventory versus current same-rule carry; exact changes are in carry-history.json.'])
    counts = Counter(d['headline'] for d in defects['defects'] for _ in d['occurrences'])
    for name, title in sorted(defects['headlines'].items()):
        old = history[0]['headlines'].get(name, {}).get('then', 0) if history else 0
        rows.append(['current headline', name, '', '', old, counts[name], title])
    return tsv(rows)


def audit_outputs(root, register_path, register, defects, rules=None):
    """One emitter for carry and the mandatory, read-only freshness gate."""
    return {'page-defects.tsv': residue_text(register['entries'], defects['defects'], rules),
            'nonclaim-reclassifications.tsv': nonclaim_text(register['entries']),
            'carry-report.tsv': carry_report_text(root, register_path, register, defects)}


_SEED = None


def seed_owner(occ):
    global _SEED
    if _SEED is None:
        import importlib.util
        spec = importlib.util.spec_from_file_location('claims_seed', ROOT / 'research/claims/seed.py')
        _SEED = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_SEED)
    return _SEED.choose(occ)


CARRY_KEYS = {'files', 'headlines', 'retired', 'added', 'revalidated', 'defect_changes'}


def compact_carry_run(run):
    """Keep exact changed fields; other run fields retain their full contents."""
    if set(run) != CARRY_KEYS:
        raise ValueError('unrecognised carry run keys')
    rows = []
    for item in run['revalidated']:
        if set(item) == {'id', 'changed'}:
            if not isinstance(item['changed'], dict) or any(
                    not isinstance(pair, list) or len(pair) != 2 for pair in item['changed'].values()):
                raise ValueError('invalid compact carry changes')
            rows.append(item)
        elif set(item) == {'id', 'before', 'after'}:
            before, after = item['before'], item['after']
            if set(before) != set(after) or before.get('id') != item['id'] or after.get('id') != item['id']:
                raise ValueError('unrecognised carry entry schema or identity')
            rows.append(dict(id=item['id'], changed={k: [before[k], after[k]]
                for k in sorted(before) if canonical(before[k]) != canonical(after[k])}))
        else:
            raise ValueError('unrecognised revalidated item')
    return dict(run, revalidated=rows)


def carry_history_text(history):
    """Plain JSON; each changed entry is a row, with deterministic key order."""
    if set(history) != {'version', 'runs'} or history['version'] != 1:
        raise ValueError('unrecognised carry history')
    encode = lambda value: json.dumps(value, ensure_ascii=False, separators=(',', ':'), allow_nan=False)
    runs = []
    for run in history['runs']:
        fields = []
        for key, value in compact_carry_run(run).items():
            body = '[\n' + ',\n'.join(encode(row) for row in value) + '\n]' if key == 'revalidated' else encode(value)
            fields.append(encode(key) + ':' + body)
        runs.append('{\n' + ',\n'.join(fields) + '\n}')
    return '{"version":1,"runs":[\n' + ',\n'.join(runs) + '\n]}\n'


def write_carry_history(path, history):
    text = carry_history_text(history)
    if not path.exists() or path.read_text() != text:
        path.write_text(text)


def carry(root, manifest, figures, register_path):
    """Apply the same rules to every occurrence, preserving append-only acceptance history."""
    extracted = extract(root, manifest)
    flat = flatten(read_json(figures))
    out = register_path.parent
    old_reg = read_json(register_path)
    old_entries = index_unique(old_reg['entries'], 'id', 'register entry')
    old_def = read_json(out / 'known-defects.json')
    old_known = {oid: d for d in old_def['defects'] for oid in d['occurrences']}
    sources_path = root / 'research/sources.json'
    sources = index_unique(read_json(sources_path)['sources'], 'id', 'source') if sources_path.exists() else {}
    from claims_rules import Context
    rules = Context(root, extracted['files'])
    entries, defects = [], []
    for occ in extracted['occurrences']:
        owner, gate = rules.choose(occ, seed_owner)
        entry = entry_for(occ, owner, gate)
        entries.append(entry)
        problem = failure(occ, entry, flat, root, {}, sources, rules)
        if problem:
            old = old_known.get(occ['id'])
            defects.append(old if old and old['failure'] == problem else defect_for(occ, problem))
    new_reg = dict(version=1, delegations={}, entries=entries)
    headlines = dict(old_def['headlines'])
    headlines['reference'] = 'Section references need an existing target.'
    new_def = dict(version=1, headlines=headlines, defects=defects)
    new_known = {oid: d for d in defects for oid in d['occurrences']}
    accepted_path = out / 'accepted-defects.json'
    accepted = read_json(accepted_path)
    effective = dict(accepted['accepted'])
    resolved = {}
    for t in accepted.get('transitions', []):
        for oid, c in t['changes'].items():
            if c['after'] is None:
                effective.pop(oid, None)
                resolved[oid] = c
            else:
                resolved.pop(oid, None)
                effective[oid] = c['after']
    changes = {}
    current = {o['id']: o for o in extracted['occurrences']}
    new_entries = {e['id']: e for e in entries}
    for oid, before in effective.items():
        after = digest(canonical(new_known[oid])) if oid in new_known else None
        if before != after:
            if oid not in current:
                path = safe_relative(root, oid.split('::')[0])
                if path.exists() and digest(path.read_text()) == accepted['source_digests'].get(oid):
                    raise ValueError('carry cannot retire a defect by narrowing unchanged source scope')
            changes[oid] = dict(before=before, after=after,
                                source_before=accepted['source_digests'].get(oid),
                                entry_digest=digest(canonical(new_entries[oid])) if oid in new_entries else None,
                                reason='same-rule revalidation' if oid in current else 'source occurrence retired')
    for oid, prior in resolved.items():
        if oid not in current:
            continue
        after = digest(canonical(new_known[oid])) if oid in new_known else None
        entry_digest = digest(canonical(new_entries[oid]))
        if after is not None or entry_digest != prior['entry_digest']:
            changes[oid] = dict(before=None, after=after, source_before=prior['source_before'],
                                entry_digest=entry_digest, reason='verified owner revalidated by current rules')
    if changes:
        accepted.setdefault('transitions', []).append(dict(changes=changes, digest=digest(canonical(changes))))
        write_json(accepted_path, accepted)
    changed = new_reg != old_reg or new_def != old_def
    if changed:
        write_json(register_path, new_reg)
        write_json(out / 'known-defects.json', new_def)
    print('Carry drift: file | occurrences then | now | defects then | now')
    per_file = {}
    for file in sorted({e['file'] for e in old_entries.values()} | set(extracted['files'])):
        row = dict(then=sum(e['file'] == file for e in old_entries.values()),
                   now=sum(e['file'] == file for e in entries),
                   defects_then=sum(oid.split('::')[0] == file for oid in old_known),
                   defects_now=sum(oid.split('::')[0] == file for oid in new_known))
        per_file[file] = row
        print(file + ' | ' + ' | '.join(str(n) for n in row.values()))
    old_groups = Counter(d['headline'] for d in old_known.values())
    new_groups = Counter(d['headline'] for d in new_known.values())
    for name in sorted(new_def['headlines']):
        print(f"Headline {name}: {old_groups[name]} -> {new_groups[name]}")
    if changed:
        path = out / 'carry-history.json'
        history = read_json(path) if path.exists() else dict(version=1, runs=[])
        history['runs'].append(dict(files=per_file, headlines={k:dict(then=old_groups[k],now=new_groups[k]) for k in new_def['headlines']},
            retired=sorted(old_entries.keys()-current.keys()), added=sorted(current.keys()-old_entries.keys()),
            revalidated=[dict(id=e['id'], before=old_entries[e['id']], after=e) for e in entries if e['id'] in old_entries and old_entries[e['id']] != e],
            defect_changes=changes))
        write_carry_history(path, history)
    for name, content in audit_outputs(root, register_path, new_reg, new_def, rules).items():
        path = out / name
        if not path.exists() or path.read_text() != content:
            path.write_text(content)
    print('Carry changed' if changed else 'Carry unchanged (idempotent)')
    return check(root, manifest, figures, register_path, accept_new=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['extract', 'check', 'carry'])
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--manifest', type=Path, default=Path('dist.manifest'))
    parser.add_argument('--figures', type=Path, default=Path('research/figures.json'))
    parser.add_argument('--register', type=Path, default=Path('research/claims/register.json'))
    parser.add_argument('--accept-new', action='store_true', help='accept and print reproduced additions to the defect ratchet')
    args = parser.parse_args(argv)
    root = args.root.resolve()
    def resolve(path):
        return path if path.is_absolute() else root / path
    try:
        if args.command == 'extract':
            if args.accept_new:
                parser.error('--accept-new requires check')
            print(json.dumps(extract(root, resolve(args.manifest)), ensure_ascii=False, indent=2))
            return 0
        if args.command == 'carry':
            return carry(root, resolve(args.manifest), resolve(args.figures), resolve(args.register))
        return check(root, resolve(args.manifest), resolve(args.figures), resolve(args.register), args.accept_new)
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as exc:
        # Do not echo absolute local paths from exceptions into public evidence.
        print(f'claimscheck: ERROR {type(exc).__name__}: ' + str(exc).replace(str(root), '<root>'), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
