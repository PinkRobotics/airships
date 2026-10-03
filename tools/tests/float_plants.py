"""Second reading counterexamples, preserved as runtime-assembled plants."""

def register(change):
    """Called by plant.py with its `change` helper."""
    # ---------------- A1: bound figures changed where printed ----------------
    change('A1-float-headline',
           'docs/FLOAT.md headline: 0.558 -> 0.658 (record-basis sea-level ratio)',
           edits=[('docs/FLOAT.md', 'lift is **0.558 of mass at sea level',
                   'lift is **0.658 of mass at sea level')])
    change('A1-float-43t',
           'docs/FLOAT.md headline: "short by 4.3 t" -> "short by 9.3 t"',
           edits=[('docs/FLOAT.md', 'short by **4.3 t and 53.6 t**',
                   'short by **9.3 t and 53.6 t**')])
    change('A1-float-range',
           'docs/FLOAT.md range sentence: 0.751 -> 0.851',
           edits=[('docs/FLOAT.md', 'ranges from **0.751 to 0.998 at sea level**',
                   'ranges from **0.851 to 0.998 at sea level**')])
    change('A1-readme',
           'README.md: 0.558 -> 0.658',
           edits=[('README.md', "Its 52 m hull’s lift is 0.558 of its mass",
                   "Its 52 m hull’s lift is 0.658 of its mass")],
           gates=('ledgercheck', 'floatpagecheck', 'readmecheck'))
    change('A1-index',
           'index.html: "no drawn hull does" -> "the 52 m hull does" (false verdict)',
           edits=[('index.html', 'The flight model assumes a hull that floats;\n          <a href="float/">no drawn hull does</a>.',
                   'The flight model assumes a hull that floats;\n          <a href="float/">the 52 m hull does</a>.')])
    change('A1-engineering',
           'engineering/index.html: cap-range 0.751 -> 0.851',
           edits=[('engineering/index.html', 'runs from 0.751 to 0.998 at sea level',
                   'runs from 0.851 to 0.998 at sea level')])
    change('A1-levels',
           'cell/levels.html: generated 0.766 (favourable target ratio) -> 0.866',
           edits=[('cell/levels.html', 'data-cat="ship.bestWorldRatioTarget" data-f="3">0.766</span>',
                   'data-cat="ship.bestWorldRatioTarget" data-f="3">0.866</span>')])
    change('A1-shipcell',
           'cell/ship.html: generated 0.766 -> 0.866',
           edits=[('cell/ship.html', 'data-n="ship.bestWorldRatioTarget" data-f="3">0.766</span>',
                   'data-n="ship.bestWorldRatioTarget" data-f="3">0.866</span>')])
    change('A1-shipindex',
           'ship/index.html: cap-range 0.751 -> 0.851',
           edits=[('ship/index.html', 'runs from 0.751 to 0.998 at sea level',
                   'runs from 0.851 to 0.998 at sea level')])
    change('A1-concept',
           'concept/index.html: "No drawn hull floats." -> "Every drawn hull floats."',
           edits=[('concept/index.html', 'Breach containment is compartment membranes across the void. No drawn hull floats.',
                   'Breach containment is compartment membranes across the void. Every drawn hull floats.')])
    _mk(change)
    _mk2(change)
    _mk3(change)
    _mk4(change)
    _mk5(change)
    _mk6(change)
    _mk7(change)
    _mk8(change)
    _mk9(change)

def _mk(change):
    import hashlib

    REC = 'hull-52m/as-drawn/gamma-0.30/chord-1050/sf-1.2'
    FAV = 'hull-52m/as-drawn/gamma-0.65/chord-1450/sf-1.2'

    def find(doc, file, key):
        for e in doc['entries']:
            if e.get('file') == file and e.get('key') == key:
                return e
        raise KeyError(f'{file} {key}')

    def rekey(e, repl, base=None):
        t = e.get('text') or base
        assert t, 'no text field and no base sentence given'
        for a, b in repl:
            assert a in t, a
            t = t.replace(a, b)
        if 'text' in e:
            e['text'] = t
        e['key'] = hashlib.sha256(t.encode()).hexdigest()[:16]
        return t

    def set_shown(e, field, shown=None, newfield=None, **kw):
        for b in e['bindings']:
            if b.get('field') == field and 'case' in b:
                if newfield:
                    b['field'] = newfield
                if shown is not None:
                    b['shown'] = shown
                b.update(kw)
                return b
        raise KeyError(field)

    # ---------------- A2: wrong figure + matching record ----------------
    def a2a(doc):
        e = find(doc, 'docs/FLOAT.md', 'c48b2da0068e22eb')
        rekey(e, [('**0.558 of mass', '**0.658 of mass')])
        set_shown(e, 'at.seaLevel.liftToMass', shown='0.658')

    change('A2a-float-shown',
           'docs/FLOAT.md 0.558->0.658 AND record entry re-keyed with shown=0.658 (no row holds 0.658)',
           edits=[('docs/FLOAT.md', 'lift is **0.558 of mass at sea level',
                   'lift is **0.658 of mass at sea level')],
           json_edits=[('research/analysis/float-claims/docs.json', a2a)])

    def a2b(doc):
        import json as _json
        from pathlib import Path
        import re
        from check_float_ledger import clean
        pristine = {'README.md:34': next(clean(m[0]) for m in re.finditer(r'\S[^\n]*(?:\n(?!\s*\n)[^\n]*)*', Path('README.md').read_text()) if 'Its lift-to-mass ratio is' in m[0]).replace('Its lift-to-mass ratio is 0.991','Its lift-to-mass ratio is 0.981')}
        e = find(doc, 'README.md', 'd6b5c798cf1ab59c')
        rekey(e, [('ratio is 0.981 at sea level', 'ratio is 0.991 at sea level')],
              base=pristine['README.md:34'])
        set_shown(e, 'at.seaLevel.liftToMass', shown='0.991')

    change('A2b-readme-shown',
           'README.md 0.981->0.991 AND record re-keyed with shown=0.991 (no row holds 0.991)',
           edits=[('README.md', 'Its lift-to-mass ratio is 0.981 at sea level',
                   'Its lift-to-mass ratio is 0.991 at sea level')],
           json_edits=[('research/analysis/float-claims/front.json', a2b)])

    def a2c(doc):
        e = find(doc, 'docs/FLOAT.md', 'c48b2da0068e22eb')
        rekey(e, [('lift is **0.558 of mass at sea level and 0.436 at 2,500 m**',
                   'lift is **0.981 of mass at sea level and 0.766 at 2,500 m**')])
        set_shown(e, 'at.seaLevel.liftToMass', case=FAV, shown='0.981')
        set_shown(e, 'at.target.liftToMass', case=FAV, shown='0.766')

    change('A2c-basis-swap',
           'docs/FLOAT.md: record-basis sentence given the FAVOURABLE figures (0.981/0.766) while still '
           'saying "That basis assumes knockdown 0.30 and 1,050 MPa chords"; record re-keyed and re-bound '
           'to the favourable row (a real row, real values)',
           edits=[('docs/FLOAT.md', 'lift is **0.558 of mass at sea level and 0.436 at 2,500 m**',
                   'lift is **0.981 of mass at sea level and 0.766 at 2,500 m**')],
           json_edits=[('research/analysis/float-claims/docs.json', a2c)])

    # ---------------- A3: ledger edited by hand ----------------
    def a3(doc):
        a2a(doc)  # same sentence + record agreement as A2a

    def first_only(text):
        return text.replace('"liftToMass": 0.558,', '"liftToMass": 0.658,', 1)

    change('A3-hand-ledger',
           'float-ledger.json hand-edited (record-row seaLevel liftToMass 0.558->0.658, first occurrence) '
           '+ FLOAT.md sentence + record entry all agreeing',
           edits=[('docs/FLOAT.md', 'lift is **0.558 of mass at sea level',
                   'lift is **0.658 of mass at sea level')],
           json_edits=[('research/analysis/float-claims/docs.json', a3)],
           py_edits=[('research/analysis/float-ledger.json', first_only)])

    # ---------------- A4: swaps and rounding ----------------
    def a4swap(doc):
        e = find(doc, 'docs/FLOAT.md', 'c48b2da0068e22eb')
        rekey(e, [('lift is **0.558 of mass at sea level and 0.436 at 2,500 m**',
                   'lift is **0.436 of mass at sea level and 0.558 at 2,500 m**')])
        # swap the FIELDS the two figures are bound to (mechanically consistent misattribution)
        for b in e['bindings']:
            if b.get('field') == 'at.seaLevel.liftToMass' and b.get('shown') == '0.558':
                b['field'], b['shown'] = 'at.target.liftToMass', '0.436'
            elif b.get('field') == 'at.target.liftToMass' and b.get('shown') == '0.436':
                b['field'], b['shown'] = 'at.seaLevel.liftToMass', '0.558'

    change('A4-altitude-swap',
           'docs/FLOAT.md: sea-level and 2,500 m figures swapped in the sentence; record re-keyed and the '
           'two bindings\' fields swapped to match (each figure now bound to the OTHER altitude)',
           edits=[('docs/FLOAT.md', 'lift is **0.558 of mass at sea level and 0.436 at 2,500 m**',
                   'lift is **0.436 of mass at sea level and 0.558 at 2,500 m**')],
           json_edits=[('research/analysis/float-claims/docs.json', a4swap)])

    def a4over(doc):
        e = find(doc, 'docs/FLOAT.md', 'c48b2da0068e22eb')
        rekey(e, [('short by **4.3 t and 53.6 t**', 'over by **4.3 t and 53.6 t**')])

    change('A4-short-to-over',
           'docs/FLOAT.md: "short by 4.3 t and 53.6 t" -> "over by ..."; record re-keyed, bindings unchanged '
           '(margins are bound with abs=true)',
           edits=[('docs/FLOAT.md', 'short by **4.3 t and 53.6 t**', 'over by **4.3 t and 53.6 t**')],
           json_edits=[('research/analysis/float-claims/docs.json', a4over)])

    def a4round(doc, shown):
        e = find(doc, 'docs/FLOAT.md', '50e86beac8d4a01b')
        rekey(e, [(f'**0.751 to 0.998 at sea level**', f'**0.751 to {shown} at sea level**')])
        for b in e['bindings']:
            if b.get('pointer') == '/ranges/favourable/seaLevel/max':
                b['shown'] = shown

    change('A4-round-1.00',
           'docs/FLOAT.md range: "0.998" -> "1.00"; record shown updated to 1.00',
           edits=[('docs/FLOAT.md', 'ranges from **0.751 to 0.998 at sea level**',
                   'ranges from **0.751 to 1.00 at sea level**')],
           json_edits=[('research/analysis/float-claims/docs.json', lambda d: a4round(d, '1.00'))])

    change('A4-round-1.0',
           'docs/FLOAT.md range: "0.998" -> "1.0"; record shown updated to 1.0',
           edits=[('docs/FLOAT.md', 'ranges from **0.751 to 0.998 at sea level**',
                   'ranges from **0.751 to 1.0 at sea level**')],
           json_edits=[('research/analysis/float-claims/docs.json', lambda d: a4round(d, '1.0'))])

    def a4transpose(doc):
        e = find(doc, 'docs/FLOAT.md', 'c48b2da0068e22eb')
        rekey(e, [('short by **4.3 t and 53.6 t**', 'short by **3.4 t and 53.6 t**')])
        set_shown(e, 'at.seaLevel.margin', shown='3.4')

    change('A4-transpose',
           'docs/FLOAT.md: "4.3 t" -> "3.4 t"; record shown updated to 3.4',
           edits=[('docs/FLOAT.md', 'short by **4.3 t and 53.6 t**', 'short by **3.4 t and 53.6 t**')],
           json_edits=[('research/analysis/float-claims/docs.json', a4transpose)])

    def a4places(doc):
        e = find(doc, 'docs/FLOAT.md', '26c4f1021df1ef16')
        rekey(e, [('disagree in **20 places**', 'disagree in **24 places**')])
        for b in e['bindings']:
            if b.get('pointer') == '/disagreementCount':
                b['shown'] = '24'

    change('A4-20-places',
           'docs/FLOAT.md: "disagree in 20 places" -> "24 places"; record shown updated to 24',
           edits=[('docs/FLOAT.md', 'disagree in **20 places**', 'disagree in **24 places**')],
           json_edits=[('research/analysis/float-claims/docs.json', a4places)])

def _mk2(change):
    """A4 follow-up: take the altitude-swap GREEN all the way through page regeneration."""
    import hashlib

    def swap(doc):
        for e in doc['entries']:
            if e.get('file') == 'docs/FLOAT.md' and e.get('key') == 'c48b2da0068e22eb':
                t = e['text'].replace(
                    'lift is **0.558 of mass at sea level and 0.436 at 2,500 m**',
                    'lift is **0.436 of mass at sea level and 0.558 at 2,500 m**')
                e['text'] = t
                e['key'] = hashlib.sha256(t.encode()).hexdigest()[:16]
                for b in e['bindings']:
                    if b.get('field') == 'at.seaLevel.liftToMass' and b.get('shown') == '0.558':
                        b['field'], b['shown'] = 'at.target.liftToMass', '0.436'
                    elif b.get('field') == 'at.target.liftToMass' and b.get('shown') == '0.436':
                        b['field'], b['shown'] = 'at.seaLevel.liftToMass', '0.558'

    change('A4b-altitude-swap-regenerated',
           'A4-altitude-swap PLUS make floatpages run, so the served page follows the swapped sentence',
           edits=[('docs/FLOAT.md', 'lift is **0.558 of mass at sea level and 0.436 at 2,500 m**',
                   'lift is **0.436 of mass at sea level and 0.558 at 2,500 m**')],
           json_edits=[('research/analysis/float-claims/docs.json', swap)],
           gates=('ledgercheck', 'floatpages', 'floatpagecheck'))

def _mk3(change):
    """A5: ten false-verdict phrasings planted at once; per-paragraph inventory analysed offline."""
    S = [
        ('V1-vocab-floats',      'The 52 m hull floats.'),
        ('V2-vocab-neutral',     'The 52 m hull is neutrally buoyant at sea level.'),
        ('P1-lighter-than-air',  'The 52 m hull is lighter than the air it displaces.'),
        ('P2-lift-exceeds',      'On the drawn hull, lift exceeds weight at sea level.'),
        ('P3-net-lift-positive', 'The drawn hull’s net lift is positive at sea level.'),
        ('P4-rises-unaided',     'The 52 m hull rises unaided from the ground.'),
        ('P5-carries-own',       'The 52 m hull carries its own structure with lift to spare.'),
        ('P6-ballast-to-stay',   'The 52 m hull needs ballast to stay down.'),
        ('P7-weighs-less',       'The 52 m hull weighs less than nothing in air.'),
        ('P8-deficit-closed',    'On the drawn hull the deficit is closed at sea level.'),
    ]
    md = '# Making the cell float\n'
    md_new = '# Making the cell float\n\n' + '\n\n'.join(t for _, t in S) + '\n'
    change('A5-floatmd-phrasings',
           'docs/FLOAT.md: ten false-verdict paragraphs planted after the title (2 gate-vocabulary + 8 engineer phrasings)',
           edits=[('docs/FLOAT.md', md, md_new)],
           gates=('ledgercheck',),
           commands=['python3 tools/check_float_ledger.py --inventory > second-opinion/logs/A5-floatmd-inventory.json'])
    body = '<body>\n'
    body_new = '<body>\n<section id="a5plant">\n' + '\n'.join(f'<p>{t}</p>' for _, t in S) + '\n</section>\n'
    change('A5-index-phrasings',
           'index.html: the same ten false-verdict sentences as <p> elements after <body>',
           edits=[('index.html', body, body_new)],
           gates=('ledgercheck',),
           commands=['python3 tools/check_float_ledger.py --inventory > second-opinion/logs/A5-index-inventory.json'])

def _mk4(change):
    """A6: nine distinct false sentences (same falsehood), one record entry per class."""
    import hashlib

    SENTS = [
        ('lit',    'literature',   'The 52 m hull’s sea-level lift exceeds its mass by 41.2 t on the published curve.'),
        ('cond',   'conditional',  'If the cap accounting is settled, the 52 m hull’s sea-level lift exceeds its mass by 41.2 t.'),
        ('otherq', 'other-quantity', 'The 52 m hull’s sea-level lift exceeds its mass by 41.2 t of carried water.'),
        ('method', 'method',       'The float check subtracts mass from lift; the 52 m hull clears it by 41.2 t at sea level.'),
        ('hist',   'history',      'The 52 m hull’s sea-level lift exceeded its mass by 41.2 t in the August census.'),
        ('quest',  'question',     'Does the 52 m hull’s sea-level lift exceed its mass by 41.2 t today?'),
        ('defer',  'deferred',     'The 52 m hull’s sea-level lift exceeds its mass by 41.2 t in the redacted reading.'),
        ('live',   'live-model',   'The 52 m hull’s sea-level lift exceeds its mass by 41.2 t on the rendered page.'),
        ('flight', 'flight-model', 'The 52 m hull’s sea-level lift exceeds its mass by 41.2 t in the flight reference.'),
    ]

    def add_entries(doc):
        for tag, cls, sent in SENTS:
            entry = {'file': 'docs/FLOAT.md', 'key': hashlib.sha256(sent.encode()).hexdigest()[:16],
                     'line': 3, 'class': cls,
                     'reason': 'Planted A6 false sentence; a careless contributor chose this class.',
                     'context': ['52', '41.2']}
            if cls == 'literature':
                entry['source'] = 'Metlen 2013, vacuum LTA vehicle study'
            if cls == 'history':
                entry['date'] = '2026-08'
            if cls == 'deferred':
                entry['owner'] = 'hand-arithmetic'
            if cls == 'flight-model':
                entry['assumption'] = 'c48b2da0068e22eb'
            doc['entries'].append(entry)

    md = '# Making the cell float\n'
    md_new = '# Making the cell float\n\n' + '\n\n'.join(s for _, _, s in SENTS) + '\n'
    change('A6-classes',
           'docs/FLOAT.md: nine false "lift exceeds mass by 41.2 t" sentences, each with a record '
           'entry in a different class (literature, conditional, other-quantity, method, history, '
           'question, deferred, live-model, flight-model)',
           edits=[('docs/FLOAT.md', md, md_new)],
           json_edits=[('research/analysis/float-claims/docs.json', add_entries)],
           gates=('ledgercheck',))

def _mk5(change):
    """A7: one model input at its source (research/analysis/vacuum-cell.py), nothing else."""
    GATES = ('ledgercheck', 'ledgercheck-selftest', 'analysisfresh', 'test-node',
             'golden', 'censuscheck')
    PROBE = 'python3 second-opinion/rec.py'
    VC = 'research/analysis/vacuum-cell.py'
    change('A7-knockdown',
           'vacuum-cell.py SHIP0 giKnockdown 0.3 -> 1.0 (house-harsh knockdown removed; sweep says '
           'the record row is NOT sized by gamma at chord 1050: mass 403.1 -> 403.9 t, still x0.557)',
           edits=[(VC, 'giKnockdown=0.3, giKnockdownFrame=0.65',
                   'giKnockdown=1.0, giKnockdownFrame=0.65')],
           gates=GATES, commands=[PROBE])
    change('A7-chord',
           'vacuum-cell.py SHIP0 sigmaWorldsMPa s1050 1050 -> 1450 (the strongest named coupon '
           'world; sweep says even sigma -> infinity leaves the record row at x0.638)',
           edits=[(VC, 's1050=1050.0', 's1050=1450.0')],
           gates=GATES, commands=[PROBE])
    change('A7-sf',
           'vacuum-cell.py SHIP0 sfDeclared 1.2 -> 0.6 (crossing found at ~0.62; at 0.6 the record '
           'row reads x1.030 at sea level — the hull floats only because less strength is promised)',
           edits=[(VC, 'sfDeclared=1.2,', 'sfDeclared=0.6,')],
           gates=GATES, commands=[PROBE])
    change('A7-density',
           'vacuum-cell.py rho_air()/isa_pressure() sea-level pressure 101325 -> 184500 Pa '
           '(x1.82: the only atmosphere edit that crosses — record row reads x1.015 at sea level; '
           'P_ATM, which sizes the wall, is a separate constant and is not touched)',
           edits=[(VC, 'return 101325.0 * (isa_temperature(alt_m) / 288.15)',
                   'return 184500.0 * (isa_temperature(alt_m) / 288.15)'),
                  (VC, 'return (101325.0 / (287.05 * 288.15)) * \\',
                   'return (184500.0 / (287.05 * 288.15)) * \\')],
           gates=GATES, commands=[PROBE])
    change('A7b-sf-regenerated',
           'A7-sf PLUS the full regeneration a contributor would run: make ledger (rewrites '
           'float-ledger.json + FLOAT-LEDGER.md from the weakened source), make floatpages, '
           'then ledgercheck + floatpagecheck + analysisfresh + golden — do any of them catch '
           'the typed site prose (ship/index.html "does not float", FLOAT.md 0.558, record '
           'binding to case id sf-1.2 which no longer exists)?',
           edits=[(VC, 'sfDeclared=1.2,', 'sfDeclared=0.6,')],
           gates=(),
           commands=[PROBE, 'make ledger', 'make floatpages', 'make ledgercheck',
                     'make floatpagecheck', 'make analysisfresh', 'make golden'])

def _mk6(change):
    """A7 extension: the same input changed on the JS MIRROR side only (ship/model.js),
    where test-node (not cellparity) is the suite the task names."""
    GATES = ('ledgercheck', 'ledgercheck-selftest', 'analysisfresh', 'test-node',
             'golden', 'censuscheck')
    change('A7-jsmirror-knockdown',
           'ship/model.js SHIP0.giKnockdown 0.3 -> 1.0 (browser mirror only; the Python '
           'source untouched). Plus make cellparity to see where the parity gate lives.',
           edits=[('ship/model.js', 'giKnockdown: 0.3, giKnockdownFrame: 0.65',
                   'giKnockdown: 1.0, giKnockdownFrame: 0.65')],
           gates=GATES, commands=['make cellparity'])

def _mk7(change):
    """A8: stale and orphaned record entries."""
    TITLE = '# Making the cell float'

    def dup(doc):   # into front.json
        import json as _json
        docs = _json.load(open('research/analysis/float-claims/docs.json'))
        e = next(x for x in docs['entries'] if x['key'] == 'd98f3a0474099c95')
        doc['entries'].append(_json.loads(_json.dumps(e)))

    def wrong_line(doc):
        e = next(x for x in doc['entries'] if x['key'] == 'd98f3a0474099c95')
        e['line'] = 400

    def empty_reason(doc):
        e = next(x for x in doc['entries'] if x['key'] == 'd98f3a0474099c95')
        e['reason'] = ''

    change('A8-orphan',
           'docs/FLOAT.md: the classed TITLE line deleted outright; its record entry left behind '
           '(every later line shifts up by one)',
           edits=[('docs/FLOAT.md', '# Making the cell float\n\n', '')],
           gates=('ledgercheck',))
    change('A8-onechar',
           'docs/FLOAT.md: one character of the classed title changed (float -> floaf); entry untouched',
           edits=[('docs/FLOAT.md', TITLE, '# Making the cell floaf')],
           gates=('ledgercheck',))
    change('A8-dup-shard',
           'the docs/FLOAT.md title entry copied VERBATIM into a second shard (front.json): the same '
           '(file, key) now in two shards',
           json_edits=[('research/analysis/float-claims/front.json', dup)],
           gates=('ledgercheck',))
    change('A8-wrong-line',
           "the title entry's line changed 1 -> 400 (points at nothing); text and key untouched",
           json_edits=[('research/analysis/float-claims/docs.json', wrong_line)],
           gates=('ledgercheck',))
    change('A8-empty-reason',
           "the title entry's reason changed to the empty string",
           json_edits=[('research/analysis/float-claims/docs.json', empty_reason)],
           gates=('ledgercheck',))

def _mk8(change):
    """A9(b): one false float sentence planted in each place the gate does not read."""
    FALSE = 'The 52 m hull floats at sea level.'
    GATES = ('ledgercheck', 'floatpagecheck', 'lint', 'test-node', 'golden',
             'readmecheck', 'noticecheck', 'labelledcheck')
    change('A9-js-metadata',
           '3d/model/metadata.js: the typed scene string (rendered in the 3d viewer page) changed to '
           'say the 52 m hull floats at sea level',
           edits=[('3d/model/metadata.js',
                   "'the entire project is one complete evacuated cell that is positively buoyant — not a ship, '",
                   "'the entire project is the 52 m hull, and the 52 m hull floats at sea level — not a ship, '")],
           gates=GATES)
    change('A9-float-index',
           'float/index.html: "' + FALSE + '" inserted after the h1 (page is a render of docs/FLOAT.md)',
           edits=[('float/index.html', '<h1 id="making-the-cell-float">Making the cell float</h1>',
                   '<h1 id="making-the-cell-float">Making the cell float</h1>\n<p><strong>' + FALSE + '</strong></p>')],
           gates=GATES)
    change('A9-float-ledger',
           'float/ledger.html: "' + FALSE + '" inserted after the h1 (render of docs/FLOAT-LEDGER.md)',
           edits=[('float/ledger.html', '<h1 id="float-ledger">Float ledger</h1>',
                   '<h1 id="float-ledger">Float ledger</h1>\n<p><strong>' + FALSE + '</strong></p>')],
           gates=GATES)
    change('A9-cockpit-tables',
           'app/cockpit/tables.js: the typed no-fires string extended with the false sentence '
           '(types into the cockpit page)',
           edits=[('app/cockpit/tables.js',
                   '? `No fire is listed, because ${nothingWhy()}.`',
                   '? `No fire is listed, because ${nothingWhy()}. ' + FALSE + '`')],
           gates=GATES)
    change('A9-goals',
           'GOALS.md: "including that nothing floats today" -> "including that the 52 m hull floats '
           'at sea level"',
           edits=[('GOALS.md', 'including that nothing floats today.',
                   'including that the 52 m hull floats at sea level.')],
           gates=GATES)

def _mk9(change):
    """A10: the census and the cap readings."""
    G = ('censuscheck', 'ledgercheck', 'floatpagecheck')
    change('A10-census-json',
           'research/analysis/member-census.json: disagreementCount 20 -> 19 (a recorded disagreement '
           'hidden from the published count)',
           edits=[('research/analysis/member-census.json', '"disagreementCount": 20',
                   '"disagreementCount": 19')],
           gates=G)
    change('A10-census-md',
           'docs/MEMBER-CENSUS.md: "20 recorded comparisons with disagreements" -> 21',
           edits=[('docs/MEMBER-CENSUS.md', '**20 recorded comparisons with disagreements**',
                   '**21 recorded comparisons with disagreements**')],
           gates=G)
    change('A10-caps-json',
           'research/analysis/cap-readings.json: record-basis chord allowable 1050.0 -> 1051.0 MPa',
           edits=[('research/analysis/cap-readings.json', '"chordAllowableMPa": 1050.0',
                   '"chordAllowableMPa": 1051.0')],
           gates=G)
    change('A10-caps-md',
           'research/analysis/cap-readings.md: "As billed | record" mass 403.101266 -> 403.201266',
           edits=[('research/analysis/cap-readings.md', '| As billed | record | 403.101266',
                   '| As billed | record | 403.201266')],
           gates=G)
