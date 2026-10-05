"""Checked block adapters for claims.py; all inputs are repository-local and read-only."""
from contextlib import contextmanager
import importlib
import json
from pathlib import Path
import re
import subprocess


@contextmanager
def float_root(root):
    import check_float_ledger as gate
    import float_claims as records
    old = gate.ROOT, records.ROOT, records.RECORD
    gate.ROOT = records.ROOT = root
    records.RECORD = root / 'research/analysis/float-claims'
    try:
        yield gate, records
    finally:
        gate.ROOT, records.ROOT, records.RECORD = old


def label_for(occ):
    """A leading label owns its numeric clause, not another independently stated quantity.

    Accepted words: assumption, assumed, target, illustration, illustrative, vision.
    A colon/dash introduces the labelled clause. Commas/semicolons and a new explicit
    label delimit its scope. A declarative second clause cannot borrow the first label.
    """
    text = occ['text']
    start = len(occ['before'])
    # before is a bounded window; locate this occurrence within its original sentence.
    windows = list(re.finditer(re.escape(occ['raw']), text, re.I))
    positions = [m.start() for m in windows if text[max(0, m.start()-40):m.start()] == occ['before']]
    if len(positions) != 1:
        return None
    pos = positions[0]
    clause_start = max(text.rfind(';', 0, pos), text.rfind(',', 0, pos)) + 1
    clause = text[clause_start:pos]
    match = re.match(r'\s*(assumption|assumed|target|illustration|illustrative|vision)\s*[:—–-]\s*', clause, re.I)
    if not match:
        return None
    # One explicit quantity per leading label; a number-word identifier also requires
    # its own later label. This deliberately leaves multi-quantity prose for review.
    import claims
    if any(claims.NUMBER.finditer(clause[match.end():])):
        return None
    return match[1].lower()


class Context:
    def __init__(self, root, files):
        self.root, self.files = root, files
        self.float_blocks = None
        self.emissions = {}
        self.region_issues = {}
        self.contexts = None
        self.sections = {}
        self.bodies = {}

    def body(self, file):
        path = self.root / file
        st = path.stat()
        signature = (st.st_mtime_ns, st.st_size)
        old = self.bodies.get(file)
        if old is None or old[0] != signature:
            self.bodies[file] = (signature, path.read_text())
        return self.bodies[file][1]

    def floats(self):
        if self.float_blocks is not None:
            return self.float_blocks
        import claims
        self.float_blocks = {}
        ledger_path = self.root / 'research/analysis/float-ledger.json'
        if not ledger_path.exists():
            return self.float_blocks
        with float_root(self.root) as (gate, records):
            ledger = json.loads(ledger_path.read_text())
            cat = gate.catalog_values() if (self.root / 'engineering/engineering.js').exists() else None
            rows = {c['id']: c for d in ledger['designs'] for c in d['cases']}
            hits = []
            for rel in self.files:
                if rel.startswith('float/') or rel == 'notices.html':
                    continue
                bounds = {}
                if rel.endswith('.html'):
                    parser = gate.Blocks(); parser.feed((self.root / rel).read_text())
                    bounds = {(line,text):(line,end) for line,end,text,raw,tag in parser.out}
                for line, text, raw in gate.source_blocks(self.root / rel):
                    hit = gate.inspect_block(rel, line, text, raw, rows, ledger, cat)
                    hit['bounds'] = bounds.get((line,text), (line,line))
                    hits.append(hit)
            errors = records.apply(hits, ledger)
            # apply also audits shards outside this gate. Their stale entries belong to
            # ledgercheck. Errors about a covered file must not become an allowance.
            covered_errors = [e for e in errors if any(('for '+f+' (line') in e or e.startswith(f+':') for f in self.files)]
            owned, _, load_errors = records.load_record()
            if load_errors:
                covered_errors += load_errors
            for hit in hits:
                key = records.key_of(hit['sentence'])
                record = owned.get(hit['file'], {}).get(key, {})
                hit['record'] = record.get('_shard', 'research/analysis/float-claims')
                hit['key'] = key
                hit['match_text'] = claims.clean_markdown(records.TOKEN.sub(' ', hit['raw']))
                if covered_errors:
                    hit['status'] = 'FAIL'
                    hit['reason'] = '; '.join(covered_errors)
                self.float_blocks.setdefault(hit['file'], []).append(hit)
        return self.float_blocks

    def float_hit(self, occ):
        candidates = []
        for h in self.floats().get(occ['file'], []):
            if occ['surface']=='model-span':
                line = occ.get('binding_line')
                if (line is not None and h['bounds'][0] <= line <= h['bounds'][1] and
                        any(f['route']==occ['raw'] for f in h.get('dynamicFigures',[]))):
                    candidates.append(h)
                continue
            if occ['surface'] in {'metadata', 'aria-label', 'alt', 'default', 'script-default'}:
                continue
            if occ['text'] and occ['text'] in h['match_text']:
                candidates.append(h)
        return min(candidates, key=lambda h: len(h['match_text'])) if candidates else None

    def generator_owner(self, occ):
        region = occ['region']
        if occ['file']=='README.md' and region and region.startswith('readme:'):
            return dict(kind='generated',generator='tools/gen_readme.py',region=region), 'readmecheck'
        if region and region.startswith('served-energy:'):
            return dict(kind='generated', generator='tools/gen_energy_pages.mjs', region=region), 'servedenergycheck'
        if region and region.startswith('energy:'):
            return dict(kind='generated', generator='research/analysis/energy-documents.mjs', region=region), 'energydoccheck'
        if occ['file'] in {'float/index.html', 'float/ledger.html', 'float/census.html'}:
            return dict(kind='generated', generator='tools/gen_float_pages.py', region='whole-file'), 'floatpagecheck'
        analysis_producers = {
            'energy-profiles.md':'energy-tables.mjs', 'energy-feasible.md':'energy-tables.mjs',
            'energy-requirements.md':'energy-tables.mjs', 'energy-omissions.md':'energy-omissions.mjs',
            'energy-unheld.md':'energy-unheld.mjs', 'descent.md':'energy-descent.mjs'}
        if occ['file'].startswith('research/analysis/') and Path(occ['file']).name in analysis_producers:
            generator = 'research/analysis/' + analysis_producers[Path(occ['file']).name]
            return dict(kind='generated',generator=generator,region='whole-file'), 'energydoccheck'
        if occ['file'] in {'notices.html', 'DATA-SOURCES.md'}:
            return dict(kind='generated', generator='tools/noticegen.py', region='whole-file'), 'noticecheck'
        return None

    def generated_issue(self, occ, entry):
        owner = entry['owner']
        expected = self.generator_owner(occ)
        if expected != (owner, entry['gate']):
            return dict(kind='generator-region-miss', observed=occ['region'], expected=owner['region'])
        generator = owner['generator']
        if not (self.root / generator).is_file():
            return dict(kind='generator-missing', observed=None, expected=generator)
        if generator in {'research/analysis/energy-tables.mjs', 'research/analysis/energy-omissions.mjs', 'research/analysis/energy-unheld.mjs', 'research/analysis/energy-descent.mjs'}:
            if generator not in self.checked_analysis:
                p = subprocess.run(['node',generator,'--check'],cwd=self.root,capture_output=True,text=True,timeout=120)
                self.checked_analysis[generator] = p.returncode
            if self.checked_analysis[generator]:
                return dict(kind='stale-generated-region', observed=occ['file'], expected=generator + ' --check')
            return None
        # Recompute only the producer, never its browser-based gate. These producers
        # emit files or have pure rendering APIs; the full gates retain deeper checks.
        if generator not in self.emissions:
            if generator == 'tools/gen_float_pages.py':
                import gen_float_pages as gen
                old = gen.ROOT
                try:
                    gen.ROOT = self.root
                    self.emissions[generator] = {page: result.html for page, result in gen.render(self.root).items()}
                finally:
                    gen.ROOT = old
            elif generator == 'tools/noticegen.py':
                import noticecheck, noticegen
                recs, errors = noticecheck.records(self.root)
                if errors:
                    raise ValueError('notice provenance records failed: ' + '; '.join(errors))
                self.emissions[generator] = noticegen.outputs(recs)
            else:
                p = subprocess.run(['python3' if generator.endswith('.py') else 'node', generator, '--emit'], cwd=self.root, capture_output=True, text=True, timeout=120)
                if p.returncode:
                    raise ValueError('region producer failed: ' + generator)
                self.emissions[generator] = json.loads(p.stdout)
        expected_text = self.emissions[generator][occ['file']]
        actual = self.body(occ['file'])
        if owner['region'] != 'whole-file':
            from float_regions import region as region_text
            marker = owner['region']
            start, end = '<!-- ' + marker + ':start -->', '<!-- ' + marker + ':end -->'
            if marker.startswith('readme:'):
                def inline_region(body):
                    if body.count(start)!=1 or body.count(end)!=1 or body.index(start)>=body.index(end):
                        raise ValueError('expected one exact ordered README region')
                    return body[body.index(start):body.index(end)+len(end)]
                expected_text,actual=inline_region(expected_text),inline_region(actual)
            else:
                expected_text = region_text(expected_text, start, end)[0]
                actual = region_text(actual, start, end)[0]
        if actual != expected_text:
            return dict(kind='stale-generated-region', observed=owner['region'], expected=generator + ' fresh output')
        return None

    def choose(self, occ, fallback):
        import claims
        if occ['surface'] == 'model-span':
            return self.span_owner(occ), 'claimscheck'
        rule = claims.nonclaim_rule(occ)
        if rule:
            return dict(kind='nonclaim', rule=rule), 'claimscheck'
        deferred = self.float_hit(occ)
        if deferred and deferred['status']=='DEFERRED':
            return dict(kind='ledger',record=deferred['record'],key=deferred['key'],reason=deferred['reason']), 'ledgercheck'
        generated = self.generator_owner(occ)
        if generated:
            return generated
        # Recorded deferrals remain defects before arithmetic ownership is considered.
        # Float record ownership takes precedence only where a real inventoried block
        # covers this occurrence; unrecorded numeric float prose remains a defect.
        hit = self.float_hit(occ)
        if hit:
            return dict(kind='ledger', record=hit['record'], key=hit['key'], reason=hit['reason']), 'ledgercheck'
        label = label_for(occ)
        if label:
            return dict(kind='labelled', label=label), 'claimscheck'
        return fallback(occ)

    def span_owner(self, occ):
        attribute = occ['context']
        producers = {'ship/index.html':'ship/explorer.js', 'engineering/index.html':'engineering/engineering.js',
                     'cell/levels.html':'cell/levels.js', 'cell/ship.html':'cell/ship.html'}
        owner = dict(kind='model-span', key=occ['raw'], attribute=attribute,
                    producer=producers.get(occ['file'], 'unbound'),
                    format={k:v for k,v in occ['attrs'].items() if k in {'data-f', 'data-mm', 'data-mul'}})
        hit = self.float_hit(occ)
        if hit:
            owner['physical_basis'] = dict(record=hit['record'], key=hit['key'], reason=hit['reason'])
        return owner


    def span_issue(self, occ, entry):
        import claims
        expected = self.span_owner(occ)
        if entry['gate'] != 'claimscheck' or entry['owner'] != expected or expected['producer'] == 'unbound':
            return dict(kind='model-span-binding-miss', observed=occ['raw'], expected='the page own model key and format')
        if self.contexts is None:
            script = self.root / 'tools/claims_bindings.mjs'
            if not script.is_file():
                raise ValueError('missing model binding adapter')
            p = subprocess.run(['node', 'tools/claims_bindings.mjs'], cwd=self.root, capture_output=True, text=True, timeout=60)
            if p.returncode:
                raise ValueError('model binding contexts failed')
            self.contexts = json.loads(p.stdout)
        try:
            value = self.contexts[occ['file']]
            for part in expected['key'].split('.'):
                value = value[int(part)] if isinstance(value, list) else value[part]
            import math
            if type(value) not in (int, float) or not math.isfinite(value):
                raise ValueError('not a finite computed number')
            fmt = expected['format']
            precision = int(fmt.get('data-f', '0'))
            if not 0 <= precision <= 12:
                raise ValueError('invalid span precision')
            scaled = value * (1000 if 'data-mm' in fmt else 1) * float(fmt.get('data-mul', '1'))
            if not math.isfinite(scaled):
                raise ValueError('invalid span scale')
        except (KeyError, TypeError, IndexError, ValueError, OverflowError):
            return dict(kind='missing-model-span-key', observed=occ['raw'], expected='a finite number from the page computed context')
        hit = self.float_hit(occ)
        if hit and hit['status']=='DEFERRED':
            return dict(kind='float-deferred', observed=occ['raw'], expected=hit['deferredReason'])
        if hit and hit['status'] not in {'PASS','ALLOW'}:
            return dict(kind='float-record-miss', observed=occ['raw'], expected=hit['reason'])
        return None

    def reference_issue(self, occ):
        # A section symbol names numbered headings in its own document. Ranges such
        # as §§1–3 resolve every integer in the range, not only its first endpoint.
        file = occ['file']
        if file not in self.sections:
            body = (self.root / file).read_text()
            if file.endswith('.md'):
                headings = re.findall(r'^#{1,6}\s+([^\n]+)', body, re.M)
            else:
                headings = re.findall(r'<h[1-6]\b[^>]*>(.*?)</h[1-6]>', body, re.S|re.I)
            import claims
            self.sections[file] = {m[1] for h in headings if (m := re.match(r'(\d+(?:\.\d+)*)[.)]?\s', claims.clean_markdown(h)))}
        targets = [occ['raw']]
        suffix = re.match(r'[–—-](\d+)\b', occ['after'])
        if suffix and occ['raw'].isdigit() and int(suffix[1]) >= int(occ['raw']):
            if int(suffix[1])-int(occ['raw']) > 100:
                return dict(kind='broken-reference', observed=occ['raw'], expected='a bounded existing section range')
            targets = [str(n) for n in range(int(occ['raw']), int(suffix[1])+1)]
        missing = [t for t in targets if t not in self.sections[file]]
        if missing:
            return dict(kind='broken-reference', observed=occ['raw'], expected='existing section(s): ' + ', '.join(missing))
        return None

    def ledger_issue(self, occ, entry):
        hit = self.float_hit(occ)
        owner = entry['owner']
        if not hit or entry['gate'] != 'ledgercheck' or owner['record'] != hit['record'] or owner['key'] != hit['key']:
            return dict(kind='float-record-miss', observed=occ['raw'], expected='an inventoried block with its exact record key')
        if owner['reason'] != hit['reason']:
            return dict(kind='float-record-miss', observed=owner['reason'], expected=hit['reason'])
        if hit['status'] == 'DEFERRED':
            return dict(kind='float-deferred', observed=occ['raw'], expected=hit['deferredReason'])
        if hit['status'] not in {'PASS', 'ALLOW'}:
            return dict(kind='float-record-miss', observed=occ['raw'], expected=hit['reason'])
        return None
