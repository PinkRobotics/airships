"""Small counterexamples for the public occurrence gate; no network or browser."""
import contextlib
from decimal import Decimal, ROUND_HALF_UP
import io
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import claims
from check_figures import matches_display


class ClaimsFixture:
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(dir=os.environ['TMPDIR'])
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.put('README.md', '')
        self.put('GOALS.md', '')
        self.put('index.html', '<p>Length 110 m.</p>')
        self.put('dist.manifest', 'served index.html\nexcluded docs\n')
        self.put('research/figures.json', '{"length":110}')
        self.put('research/sources.json', '{"sources":[]}')
        self.put('research/claims/carry-report-baseline.json', '{"version":1,"text":"Fixture snapshot."}')
        self.put('research/claims/known-defects.json', json.dumps(dict(
            version=1, headlines={'unowned': 'Some figures lack an owner.'}, defects=[])))

    def put(self, path, text):
        path = self.root / path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def extract(self):
        return claims.extract(self.root, self.root / 'dist.manifest')['occurrences']

    def register(self, owner=None, gate='claimscheck'):
        entries = [claims.entry_for(o, owner or dict(kind='model', key='length', precision=0,
                   unit='m', scenario={'basis': 'fixture'}), gate) for o in self.extract()]
        claims.write_json(self.root / 'research/claims/register.json',
                          dict(version=1, delegations={}, entries=entries))
        self.write_audits()
        return entries

    def write_audits(self):
        path = self.root / 'research/claims/register.json'
        register = claims.read_json(path)
        defects = claims.read_json(path.parent / 'known-defects.json')
        ids = {e['id'] for e in register['entries']}
        defects['defects'] = [d for d in defects['defects'] if set(d['occurrences']) <= ids]
        for name, content in claims.audit_outputs(self.root, path, register, defects).items():
            self.put('research/claims/' + name, content)

    def check(self, accept=False):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = claims.check(self.root, self.root / 'dist.manifest', self.root / 'research/figures.json',
                                  self.root / 'research/claims/register.json', accept)
        return status, output.getvalue()

    def known(self):
        o = self.extract()[0]
        e = claims.entry_for(o)
        claims.write_json(self.root / 'research/claims/register.json', dict(version=1, entries=[e]))
        defect = dict(occurrences=[o['id']], headline='unowned', problem='No owner.',
                      closes='Replace or bind the sentence.',
                      failure=dict(kind='unowned', observed='110', expected='an accountable owner and check'))
        path = self.root / 'research/claims/known-defects.json'
        data = claims.read_json(path)
        data['defects'] = [defect]
        claims.write_json(path, data)
        self.write_audits()
        return o, defect



class ClaimsTest(ClaimsFixture, unittest.TestCase):
    def test_html_surfaces_inline_svg_controls_and_metadata(self):
        self.put('index.html', '''<title>9 classes</title><meta name="description" content="8 tonnes">
        <p>Hull <strong>110</strong> m long; three classes.</p><img alt="7 m" aria-label="6 m">
        <svg><title>5 metres</title><desc>4 metres</desc><text>3 m</text></svg>
        <input value="2" aria-valuenow="2"><output>1.25</output><textarea>12</textarea>
        <style>p{width:999px}</style><script>const a=998;</script>''')
        occ = self.extract()
        self.assertEqual([o['raw'] for o in occ], ['9', '8', '110', 'three', '7', '6', '5', '4', '3', '2', '2', '1.25', '12'])
        self.assertIn('Hull 110 m long; three classes.', [o['text'] for o in occ])

    def test_script_defaults_not_computation(self):
        self.put('index.html', '''<script>
        const x=999; el.textContent="12 t"; el.innerHTML=`<p>9 m and ${x}</p>`;
        document.write('7 m'); el.setAttribute('aria-label', '6 m');
        </script>''')
        self.assertEqual([o['raw'] for o in self.extract()], ['12', '9', '7', '6'])

    def test_json_ld(self):
        self.put('index.html', '<script type="application/ld+json">{"name":"Hull 8", "rating":4}</script>')
        self.assertEqual([o['raw'] for o in self.extract()], ['8', '4'])

    def test_markdown_cells_numbers_in_links_code_and_spelled(self):
        self.put('index.html', '')
        self.put('README.md', '''# nine counter-arguments

Three classes and twenty-one tonnes.

| Head | Value |
|---|---|
| Water | [110 t](reference-987.md) |

```
port 1234
```
''')
        occ = self.extract()
        self.assertEqual([o['raw'] for o in occ], ['nine', 'Three', 'twenty-one', '110', '1234'])

    def test_comma_is_not_part_of_number_and_markers_bind(self):
        self.put('index.html', '')
        self.put('research/reports/sample.md', '110<!--f:length-->, then 1,100.5<!--f:other--> m.')
        self.assertEqual([(o['raw'], o['marker']) for o in self.extract()], [('110', 'length'), ('1,100.5', 'other')])

    def test_stable_ids_whitespace_and_lines_not_writing(self):
        before = self.extract()[0]['id']
        self.put('index.html', '\n\n<p>Length\n    110 m.</p>\n')
        self.assertEqual(before, self.extract()[0]['id'])
        self.put('index.html', '<p>Width 110 m.</p>')
        self.assertNotEqual(before, self.extract()[0]['id'])

    def test_duplicate_sentences_keep_each_occurrence(self):
        self.put('index.html', '<p>110 m.</p><p>110 m.</p>')
        occ = self.extract()
        self.assertNotEqual(occ[0]['id'], occ[1]['id'])
        self.assertEqual([o['ordinal'] for o in occ], [1, 2])

    def test_manifest_partial_and_other_docs_out_of_scope(self):
        self.put('dist.manifest', 'served index.html\nserved extra\nPARTIAL extra/tests\n')
        self.put('extra/test.html', '<p>12 m</p>')
        self.put('extra/tests/no.html', '<p>13 m</p>')
        self.put('docs/not.md', '14 m')
        self.assertEqual([o['raw'] for o in self.extract()], ['12', '110'])

    def test_table_context_changes(self):
        self.put('index.html', '<table><tr><th>Length</th><td>110 m</td></tr></table>')
        old = self.extract()[0]
        self.put('index.html', '<table><tr><th>Width</th><td>110 m</td></tr></table>')
        new = self.extract()[0]
        self.assertEqual(old['id'], new['id'])
        self.assertNotEqual(claims.placement(old), claims.placement(new))

    def test_new_number_goes_red(self):
        self.register()
        self.put('index.html', '<p>Length 110 m.</p><p>Capacity 42 t.</p>')
        status, output = self.check()
        self.assertEqual(status, 1)
        self.assertIn('UNREGISTERED', output)
        self.assertIn('42', output)

    def test_changed_bound_number_names_old_new_key(self):
        self.register()
        self.put('index.html', '<p>Length 111 m.</p>')
        status, output = self.check()
        self.assertEqual(status, 1)
        self.assertIn('old=110 new=111 key=length', output)

    def test_deleted_register_entry_goes_red(self):
        self.register()
        path = self.root / 'research/claims/register.json'
        data = claims.read_json(path)
        data['entries'].clear()
        claims.write_json(path, data)
        self.assertIn('UNREGISTERED', self.check()[1])

    def test_moved_model_figure_names_values_and_key(self):
        self.register()
        self.put('research/figures.json', '{"length":111}')
        status, output = self.check()
        self.assertEqual(status, 1)
        self.assertIn('"expected":111', output)
        self.assertIn('"observed":"110"', output)
        self.assertIn('"key":"length"', output)

    def test_accessibility_move_does_not_inherit_binding(self):
        self.register()
        self.put('index.html', '<img alt="Length 110 m.">')
        self.assertIn('placement-changed', self.check()[1])

    def test_ratchet_requires_accept_new_and_prints_each_addition(self):
        self.known()
        self.assertIn('new defect needs', self.check()[1])
        status, output = self.check(True)
        self.assertEqual(status, 0)
        self.assertIn('ACCEPT NEW index.html::', output)
        self.assertEqual(self.check()[0], 0)

    def test_fixed_defect_entry_must_be_removed(self):
        self.known()
        self.check(True)
        self.put('index.html', '<p>Length 111 m.</p>')
        self.assertIn('known defect no longer reproduces', self.check()[1])

    def test_deleting_defect_without_page_change_fails(self):
        self.known()
        self.check(True)
        self.put('research/claims/known-defects.json', '{"version":1,"headlines":{"unowned":"Unowned."},"defects":[]}')
        self.register()
        self.assertIn('defect removed but its occurrence is still published', self.check()[1])

    def test_editing_accepted_defect_cannot_be_reaccepted(self):
        self.known()
        self.check(True)
        path = self.root / 'research/claims/known-defects.json'
        data = claims.read_json(path)
        data['defects'][0]['problem'] = 'Changed evidence'
        claims.write_json(path, data)
        self.assertIn('accepted defect changed', self.check(True)[1])

    def test_page_fix_register_update_and_defect_retirement_green(self):
        self.known()
        self.check(True)
        self.put('index.html', '<p>Current length 110 m.</p>')
        self.register()
        self.put('research/claims/known-defects.json', '{"version":1,"headlines":{"unowned":"Unowned."},"defects":[]}')
        self.write_audits()
        self.assertEqual(self.check()[0], 0)

    def test_generated_regions_are_checked(self):
        self.register(dict(kind='generated', generator='tools/gen_fallback.py', region='FALLBACK'), 'fallbackcheck')
        self.assertIn('generator-region-miss', self.check()[1])
        self.put('index.html', '<div><!--FALLBACK-->110 m<!--/FALLBACK--></div>')
        self.put('tools/gen_fallback.py', '')
        self.register(dict(kind='generated', generator='tools/gen_fallback.py', region='FALLBACK'), 'fallbackcheck')
        self.assertEqual(self.check()[0], 0)

    def test_figure_marker_is_generated_region_and_checked(self):
        self.put('index.html', '')
        self.put('research/reports/sample.md', 'Length 110 m<!--f:length-->.')
        self.register(dict(kind='generated', generator='figure-marker', region='length'), 'figcheck')
        self.assertEqual(self.check()[0], 0)
        self.put('research/figures.json', '{"length":111}')
        self.assertIn('stale-model', self.check()[1])

    def test_label_must_be_in_same_block(self):
        self.register(dict(kind='labelled', label='target'))
        self.assertIn('label-missing', self.check()[1])
        self.put('index.html', '<p>Target: length 110 m.</p>')
        self.register(dict(kind='labelled', label='target'))
        self.assertEqual(self.check()[0], 0)
        self.put('index.html', '<p>Target</p><p>Length 110 m.</p>')
        self.register(dict(kind='labelled', label='target'))
        self.assertIn('label-missing', self.check()[1])

    def test_cited_capture_and_digest_review(self):
        owner = dict(kind='cited', source='source', locator='Table 2',
                     review=dict(by='claims lane', date='2026-10-01', digest=self.extract()[0]['digest']))
        self.register(owner)
        self.assertIn('source-missing', self.check()[1])
        self.put('research/sources.json', '{"sources":[{"id":"source","file":"papers/source.txt"}]}')
        self.assertIn('capture-missing', self.check()[1])
        self.put('research/papers/source.txt', '110 m')
        self.assertEqual(self.check()[0], 0)
        owner['review']['digest'] = 'old'
        self.register(owner)
        self.assertIn('review-void', self.check()[1])

    def test_no_capture_reason_is_recorded(self):
        owner = dict(kind='cited', source='source', locator='Table 2', no_capture_reason='Redistribution withheld.',
                     review=dict(by='claims lane', date='2026-10-01', digest=self.extract()[0]['digest']))
        self.put('research/sources.json', '{"sources":[{"id":"source"}]}')
        self.register(owner)
        self.assertEqual(self.check()[0], 0)

    def test_delegation_requires_real_inventory(self):
        self.register(dict(kind='delegated', inventory='floatcheck'), 'floatcheck')
        self.assertIn('delegation-miss', self.check()[1])
        oid = self.extract()[0]['id']
        self.put('inventory.py', 'import json\nprint(' + repr(json.dumps(dict(version=1, gate='floatcheck', occurrences=[oid]))) + ')\n')
        path = self.root / 'research/claims/register.json'
        data = claims.read_json(path)
        data['delegations'] = {'floatcheck': {'command': [sys.executable, 'inventory.py', '--inventory']}}
        claims.write_json(path, data)
        self.assertEqual(self.check()[0], 0)
        self.put('inventory.py', 'print("not json")')
        with self.assertRaises(ValueError):
            self.check()

    def test_nonclaim_rules_are_token_specific_and_tested(self):
        examples = [('P-100', '100', 'named-identifier'), ('3D view', '3', 'named-identifier'),
                    ('Date 2026-10-01', '2026', 'iso-date'), ('1. Begin', '1', 'section-or-step'),
                    ('See section 4', '4', 'cross-reference'), ('v1.2', '1.2', 'version'),
                    ('Area m²', '²', 'unit-exponent-or-formula-index')]
        for text, raw, rule in examples:
            with self.subTest(rule=rule):
                self.put('index.html', '<p>' + text + '</p>')
                o = next(o for o in self.extract() if o['raw'] == raw)
                self.assertEqual(claims.nonclaim_rule(o), rule)
        self.put('index.html', '<p>Date 2026-10-01, length 12 m, model 1 m.</p>')
        for o in self.extract():
            if o['raw'] in {'12', '1'}:
                self.assertIsNone(claims.nonclaim_rule(o))

    def test_exact_nonclaim_requires_reason_and_changed_words_orphan(self):
        with self.assertRaises(ValueError):
            self.register(dict(kind='nonclaim', rule='exact'))
            self.check()
        self.register(dict(kind='nonclaim', rule='exact', reason='Fixture axis tick.'))
        self.assertEqual(self.check()[0], 0)
        self.put('index.html', '<p>Width 110 m.</p>')
        self.assertIn('orphaned', self.check()[1])

    def test_rounding_matches_original_comparison(self):
        for value in [13722.5, -1.25, 0, 1.391, 8.454, 54.325, 999.999]:
            for dp in range(4):
                for raw in [str(value), f'{value:.{dp}f}', f'{value + 1:.{dp}f}']:
                    q = Decimal(str(float(value))).quantize(Decimal(1).scaleb(-dp), rounding=ROUND_HALF_UP)
                    expected = abs(float(q) - float(raw)) <= 10 ** (-dp) / 2 + 1e-9
                    self.assertEqual(matches_display(value, raw, dp), expected)
        self.assertTrue(matches_display(13722.5, '13,723'))
        self.assertTrue(matches_display(-1.25, '−1.3'))

    def test_numeric_and_conditional_script_defaults_and_unicode(self):
        self.put('index.html', """<script>el.textContent=42;
        el.innerText=condition ? '9 tonnes' : '10 tonnes';
        el.textContent='\\u2759';</script>""")
        self.assertEqual([o['raw'] for o in self.extract()], ['42', '9', '10'])

    def test_accessibility_in_markdown(self):
        self.put('index.html', '')
        self.put('README.md', '<img alt="110 m" aria-label="Three classes">')
        self.assertEqual([o['raw'] for o in self.extract()], ['110', 'Three'])

    def test_precision_cannot_be_tuned_to_mask_stale_display(self):
        self.put('index.html', '<p>Length 110.49 m.</p>')
        self.register(dict(kind='model', key='length', unit='m', precision=0, scenario={'basis':'test'}))
        self.assertIn('precision-mismatch', self.check()[1])

    def test_missing_model_key_is_red(self):
        self.register()
        self.put('research/figures.json', '{}')
        self.assertIn('missing-model-key', self.check()[1])

    def test_rendering_metadata_rule_is_narrow(self):
        self.put('index.html', '<meta name="theme-color" content="#0a0a0c"><meta name="description" content="110 m">')
        occ = self.extract()
        self.assertEqual(claims.nonclaim_rule(occ[0]), 'rendering-metadata')
        self.assertIsNone(claims.nonclaim_rule(occ[-1]))
        self.put('index.html', '<p>SF 1.2 needs review.</p>')
        self.assertIsNone(claims.nonclaim_rule(self.extract()[0]))

    def test_malformed_fallback_region_is_red(self):
        self.put('index.html', '<p><!--FALLBACK-->110 m</p>')
        self.put('tools/gen_fallback.py', '')
        self.register(dict(kind='generated', generator='tools/gen_fallback.py', region='FALLBACK'), 'fallbackcheck')
        self.assertIn('unbalanced markers', self.check()[1])

    def test_delegated_gate_arriving_must_own_the_occurrence(self):
        self.register(dict(kind='delegated', inventory='floatcheck'), 'floatcheck')
        path = self.root / 'research/claims/register.json'
        data = claims.read_json(path)
        data['delegations'] = {'floatcheck': {'command': [sys.executable, 'inventory.py', '--inventory'],
                                             'optional_until_present': 'inventory.py'}}
        claims.write_json(path, data)
        self.assertIn('delegation-miss', self.check()[1])
        self.put('inventory.py', 'print(\'{"version":1,"gate":"floatcheck","occurrences":[]}\')')
        self.assertIn('delegation-miss', self.check()[1])

    def test_inventory_narrowing_cannot_retire_unchanged_page_defects(self):
        self.known()
        self.check(True)
        self.put('dist.manifest', 'excluded index.html')
        self.put('research/claims/register.json', '{"version":1,"entries":[]}')
        self.put('research/claims/known-defects.json', '{"version":1,"headlines":{"unowned":"Unowned."},"defects":[]}')
        self.assertIn('retirement requires changed page bytes', self.check()[1])

    def test_root_and_all_path_overrides(self):
        self.register()
        (self.root / 'dist.manifest').rename(self.root / 'site.manifest')
        (self.root / 'research/figures.json').rename(self.root / 'other-figures.json')
        (self.root / 'research/claims/register.json').rename(self.root / 'research/claims/custom.json')
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = claims.main(['check', '--root', str(self.root), '--manifest', 'site.manifest',
                                  '--figures', 'other-figures.json', '--register', 'research/claims/custom.json'])
        self.assertEqual(result, 0)

    def test_water_release_is_not_arrival(self):
        self.put('index.html', '<p>Delivered 110 t/h.</p>')
        self.put('research/figures.json', '{"classes":{"P100":{"cycle":{"tph":110}}}}')
        self.register(dict(kind='model', key='classes.P100.cycle.tph', unit='t/h', precision=0,
                           scenario={'water':'released'}))
        self.assertIn('water-basis', self.check()[1])

    def test_seed_rules_use_meaning_not_equal_values(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location('claims_seed', Path(claims.__file__).parents[1] / 'research/claims/seed.py')
        seed = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(seed)
        self.put('index.html', '')
        self.put('README.md', '| | P-100 | P-1000 | P-10000 |\n|---|---|---|---|\n| Energy | 1.25 MWh | 7.4 MWh | 45.9 MWh |')
        bound = [seed.choose(o)[0] for o in self.extract() if o['raw'] in {'1.25','7.4','45.9'}]
        self.assertEqual([o['key'] for o in bound], ['classes.' + c + '.cycle.eCycleMWh' for c in ('P100','P1000','P10000')])
        self.put('README.md', 'Unrelated 1.25 MWh.')
        self.assertIsNone(seed.choose(self.extract()[0])[0])
        self.put('index.html', '<p>Assumption: 110 m.</p>')
        self.assertEqual(seed.choose(self.extract()[1])[0]['kind'], 'labelled')

    def test_visible_marker_identifier_in_code_example(self):
        self.put('index.html', '')
        self.put('README.md', '    Length 110 m<!--f:P100.spec.lenM-->')
        occ = self.extract()
        self.assertEqual([o['raw'] for o in occ], ['100', '110'])
        self.assertEqual(claims.nonclaim_rule(occ[0]), 'named-identifier')
        self.assertEqual(occ[1]['marker'], 'P100.spec.lenM')

    def test_deterministic(self):
        self.assertEqual(claims.canonical(self.extract()), claims.canonical(self.extract()))


class OwnershipRulesTest(ClaimsFixture, unittest.TestCase):
    def test_carry_twice_preserves_files_and_ratchet_receipts(self):
        self.known()
        self.check(True)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(claims.carry(self.root, self.root/'dist.manifest', self.root/'research/figures.json', self.root/'research/claims/register.json'), 0)
        before = {p.name: p.read_bytes() for p in (self.root/'research/claims').glob('*.json')}
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(claims.carry(self.root, self.root/'dist.manifest', self.root/'research/figures.json', self.root/'research/claims/register.json'), 0)
        self.assertEqual(before, {p.name: p.read_bytes() for p in (self.root/'research/claims').glob('*.json')})

    def test_same_rule_rebinding_requires_receipt_and_verified_owner(self):
        o, _ = self.known()
        self.check(True)
        self.put('index.html', '<p>Length 110 m.</p>')
        self.register()
        self.assertEqual(self.check()[0], 1)
        accepted = claims.read_json(self.root/'research/claims/accepted-defects.json')
        entry = claims.read_json(self.root/'research/claims/register.json')['entries'][0]
        changes = {o['id']: dict(before=accepted['accepted'][o['id']], after=None,
                   source_before=accepted['source_digests'][o['id']], entry_digest=claims.digest(claims.canonical(entry)))}
        accepted['transitions'] = [dict(changes=changes, digest=claims.digest(claims.canonical(changes)))]
        claims.write_json(self.root/'research/claims/accepted-defects.json', accepted)
        self.put('research/claims/known-defects.json', '{"version":1,"headlines":{"unowned":"Unowned."},"defects":[]}')
        self.write_audits()
        self.assertEqual(self.check()[0], 0)
        self.put('research/figures.json', '{"length":111}')
        self.assertIn('no longer has a verified owner', self.check()[1])

    def test_float_record_adapter_bound_allowed_deferred_and_outside(self):
        from claims_rules import Context
        self.put('Makefile', 'check: ledgercheck\n')
        self.put('research/analysis/float-ledger.json', '{"designs":[],"atmosphere":{"targetM":2500}}')
        self.put('index.html', '<p>Mass 110 kg.</p><p>Length 120 m.</p>')
        self.put('docs/OPEN-QUESTIONS.md', '<a id="float-deferred-source-needed"></a>')
        import float_claims
        import check_float_ledger
        from unittest.mock import patch
        cosmetic = patch.object(check_float_ledger, 'proposal', return_value='Fixture block.')
        cosmetic.start(); self.addCleanup(cosmetic.stop)
        text = 'Mass 110 kg.'
        record = dict(file='index.html',key=float_claims.key_of(text),line=1,**{'class':'method'},
                      context=['110'],reason='A stated method context, not a float result.')
        self.put('research/analysis/float-claims/fixture.json', json.dumps(dict(schema='float-claims/1',files=['index.html'],entries=[record])))
        def context():
            return Context(self.root, ['index.html'])
        occ, outside = self.extract()
        ctx = context()
        owner, gate = ctx.choose(occ, claims.seed_owner)
        self.assertEqual(owner['key'], float_claims.key_of(text))
        self.assertEqual(gate, 'ledgercheck')
        entry = claims.entry_for(occ,owner,gate)
        self.assertIsNone(ctx.ledger_issue(occ,entry))
        self.assertIsNone(ctx.float_hit(outside))
        owner['key'] = 'unrelated'
        self.assertEqual(ctx.ledger_issue(occ,entry)['kind'], 'float-record-miss')
        record.update(**{'class':'deferred'},owner='source-needed',reason='The physical basis requires a reviewed source.')
        self.put('research/analysis/float-claims/fixture.json', json.dumps(dict(schema='float-claims/1',files=['index.html'],entries=[record])))
        ctx = context();owner,gate = ctx.choose(occ,claims.seed_owner)
        self.assertEqual(ctx.ledger_issue(occ,claims.entry_for(occ,owner,gate))['kind'], 'float-deferred')
        record.update(**{'class':'bound'}, bindings=[dict(source='research/analysis/float-ledger.json',pointer='/value',shown='110')])
        self.put('research/analysis/float-ledger.json','{"designs":[],"atmosphere":{"targetM":2500},"value":110}')
        self.put('research/analysis/float-claims/fixture.json', json.dumps(dict(schema='float-claims/1',files=['index.html'],entries=[record])))
        ctx = context();owner,gate=ctx.choose(occ,claims.seed_owner)
        self.assertIsNone(ctx.ledger_issue(occ,claims.entry_for(occ,owner,gate)))
        self.put('research/analysis/float-ledger.json','{"designs":[],"atmosphere":{"targetM":2500},"value":111}')
        ctx=context();owner,gate=ctx.choose(occ,claims.seed_owner)
        self.assertEqual(ctx.ledger_issue(occ,claims.entry_for(occ,owner,gate))['kind'],'float-record-miss')

    def test_energy_regions_own_inside_only_and_regenerate(self):
        from claims_rules import Context
        self.put('tools/gen_energy_pages.mjs', "console.log(JSON.stringify({'index.html':'<p><!-- served-energy:home:start -->Target: 110 m.<!-- served-energy:home:end --></p>'}));")
        # Markers are exact lines for the producer's region contract.
        source='<p>\n<!-- served-energy:home:start -->\nTarget: 110 m.\n<!-- served-energy:home:end -->\n</p><p>Length 120 m.</p>'
        self.put('index.html',source)
        self.put('tools/gen_energy_pages.mjs', 'console.log('+json.dumps(json.dumps({'index.html':source}))+');')
        inside,outside=self.extract();ctx=Context(self.root,['index.html'])
        owner,gate=ctx.generator_owner(inside)
        self.assertEqual(gate,'servedenergycheck');self.assertIsNone(ctx.generator_owner(outside))
        self.assertIsNone(ctx.generated_issue(inside,claims.entry_for(inside,owner,gate)))
        self.put('index.html',source.replace('110','111'))
        self.assertEqual(ctx.generated_issue(inside,claims.entry_for(inside,owner,gate))['kind'],'stale-generated-region')
        self.put('index.html', '<p>Assumption: 110 m.</p>')
        self.assertIsNone(Context(self.root,['index.html']).generator_owner(self.extract()[0]))

    def test_labels_are_sentence_and_quantity_specific(self):
        from claims_rules import label_for
        for word in ['Assumption','Assumed','Target','Illustration','Illustrative','Vision']:
            self.put('index.html',f'<p>{word}: length 110 m.</p>')
            self.assertEqual(label_for(self.extract()[0]),word.lower())
        for text in ['Target: one thing. This is background. Length 110 m.',
                     'Target: 100 m; actual length 110 m.',
                     'Target: 100 m, length 110 m.', 'We have a target. Length 110 m.']:
            self.put('index.html','<p>'+text+'</p>')
            occ=next(o for o in self.extract() if o['raw']=='110')
            self.assertIsNone(label_for(occ),text)


class HoleRulesTest(ClaimsFixture, unittest.TestCase):
    def test_delivering_and_every_delivery_form_are_red(self):
        for verb in ['deliver','delivers','delivered','delivering','delivery','deliveries']:
            self.put('index.html',f'<p>The model is {verb} 110 t/h.</p>')
            o=self.extract()[0]
            self.assertEqual(claims.water_basis_issue(o,'classes.P100.cycle.tph')['kind'],'water-basis')
        self.put('index.html','<p>The model requests 110 tonnes; water released is not suppression.</p>')
        self.assertIsNone(claims.water_basis_issue(self.extract()[0],'classes.P100.cycle.tph'))
        self.put('index.html','<p>Water was released in this example. Delivering 110 t/h at a fire is asserted.</p>')
        o=next(o for o in self.extract() if o['raw']=='110')
        self.assertEqual(claims.water_basis_issue(o,'classes.P100.cycle.tph')['kind'],'water-basis')
        self.assertIsNone(claims.water_basis_issue(o,'classes.P100.spec.payloadT'))

    def test_model_spans_are_extracted_even_without_numeric_text(self):
        from claims_rules import Context
        self.put('index.html','<p>Lift <span data-n="ship.liftT" data-f="2"></span> t.</p>')
        o=self.extract()[0]
        self.assertEqual(o['surface'],'model-span');self.assertEqual(o['raw'],'ship.liftT')
        ctx=Context(self.root,['index.html']);owner=ctx.span_owner(o)
        self.assertEqual(ctx.span_issue(o,claims.entry_for(o,owner))['kind'],'model-span-binding-miss')
        # Use a recognised page to exercise finite model keys, formatting and absence.
        self.put('dist.manifest','served ship/index.html')
        self.put('ship/index.html','<span data-n="ship.liftT" data-f="2"></span>')
        o=self.extract()[0];ctx=Context(self.root,['ship/index.html']);ctx.contexts={'ship/index.html':{'ship':{'liftT':110}}}
        owner=ctx.span_owner(o);entry=claims.entry_for(o,owner)
        self.assertIsNone(ctx.span_issue(o,entry))
        ctx.contexts['ship/index.html']['ship'].clear()
        self.assertEqual(ctx.span_issue(o,entry)['kind'],'missing-model-span-key')
        ctx.contexts['ship/index.html']['ship']['liftT']='110'
        self.assertEqual(ctx.span_issue(o,entry)['kind'],'missing-model-span-key')
        ctx.contexts['ship/index.html']['ship']['liftT']=float('nan')
        self.assertEqual(ctx.span_issue(o,entry)['kind'],'missing-model-span-key')

    def test_symbol_reference_resolves_and_broken_target_is_red(self):
        from claims_rules import Context
        self.put('index.html','')
        self.put('README.md','# 4. Geometry\n\nSee §4, not an assertion of 110 m.\n')
        occ=next(o for o in self.extract() if o['raw']=='4' and 'See' in o['text'])
        self.assertEqual(claims.nonclaim_rule(occ),'section-symbol-reference')
        ctx=Context(self.root,['README.md'])
        self.assertIsNone(ctx.reference_issue(occ))
        self.put('README.md','# 5. Geometry\n\nSee §4, not an assertion of 110 m.\n')
        self.assertEqual(Context(self.root,['README.md']).reference_issue(occ)['kind'],'broken-reference')
        figure=next(o for o in self.extract() if o['raw']=='110')
        self.assertIsNone(claims.nonclaim_rule(figure))

    def test_reference_ranges_check_every_section(self):
        from claims_rules import Context
        self.put('index.html','')
        self.put('README.md','# 1. One\n\n# 3. Three\n\nSee §§1–3.\n')
        occ=next(o for o in self.extract() if o['raw']=='1' and 'See' in o['text'])
        self.assertEqual(Context(self.root,['README.md']).reference_issue(occ)['kind'],'broken-reference')
        self.put('README.md','# 1. One\n\n# 2. Two\n\n# 3. Three\n\nSee §§1–3.\n')
        self.assertIsNone(Context(self.root,['README.md']).reference_issue(occ))


class ResidueRulesTest(ClaimsFixture, unittest.TestCase):
    def test_function_word_roles_both_sides(self):
        examples=[('First, inspect the model.','First','discourse-ordinal'),
                  ('The first is a choice.','first','discourse-ordinal'),
                  ('The first draft is superseded.','first','document-or-process-order'),
                  ('The browser uses first-party requests.','first','named-word'),
                  ('A one-way route.','one','named-word'),
                  ('No one has to average the values.','one','pronominal-one'),
                  ('Each one browsable below.','one','pronominal-one'),
                  ('It is a small one.','one','pronominal-one'),
                  ('The single biggest lever.','single','idiomatic-single')]
        for text,raw,rule in examples:
            self.put('index.html','<p>'+text+'</p>')
            occ=next(o for o in self.extract() if o['raw'].lower()==raw.lower())
            self.assertEqual(claims.function_word_rule(occ),rule,text)
        for text,raw in [('First 110 tonnes delivered.','First'),('One tonne per hour.','One'),
                         ('Each one-tonne load.','one'),('A single aircraft.','single'),
                         ('A second cycle lasts 110 minutes.','second'),('Two thirds of the energy.','Two')]:
            self.put('index.html','<p>'+text+'</p>')
            occ=next(o for o in self.extract() if o['raw'].lower().startswith(raw.lower()))
            self.assertIsNone(claims.function_word_rule(occ),text)

    def test_residue_changes_make_check_red_and_carry_repairs_it(self):
        self.known();self.check(True)
        with contextlib.redirect_stdout(io.StringIO()):
            claims.carry(self.root,self.root/'dist.manifest',self.root/'research/figures.json',self.root/'research/claims/register.json')
        self.assertIn('Length 110 m.',(self.root/'research/claims/page-defects.tsv').read_text())
        self.put('research/claims/page-defects.tsv','stale')
        self.assertIn('missing or stale audit table',self.check()[1])

    def test_every_audit_table_is_required_and_exact(self):
        self.register()
        self.assertEqual(self.check()[0], 0)
        for name in ('page-defects.tsv', 'nonclaim-reclassifications.tsv', 'carry-report.tsv'):
            path = self.root / 'research/claims' / name
            original = path.read_text()
            for mutation in ('append', 'missing'):
                with self.subTest(name=name, mutation=mutation):
                    if mutation == 'append':
                        path.write_text(original + 'The 52 m hull floats.\n')
                    else:
                        path.unlink()
                    status, output = self.check()
                    self.assertEqual(status, 1)
                    self.assertIn(name + ': missing or stale audit table', output)
                    path.write_text(original)
                    self.assertEqual(self.check()[0], 0)

    def test_tsv_preserves_quoted_cells(self):
        import csv
        rows = [['Sentence', 'Reason'], ['A pipe | and tab\tinside.', 'A newline\ninside.']]
        self.assertEqual(list(csv.reader(io.StringIO(claims.tsv(rows)), delimiter='\t')), rows)


class DocumentScopeTest(ClaimsFixture, unittest.TestCase):
    def test_first_reader_documents_are_covered_history_and_source_notes_are_not(self):
        for name in ['docs/PHYSICS.md','docs/ARCHITECTURE.md','research/analysis/note.md','sim/README.md','tests/README.md','tools/README.md','DATA-SOURCES.md']:
            self.put(name,'A quantity 42 t.')
        for name in ['docs/working/history.md','docs/audit/history.md','research/notes/paper.md']:
            self.put(name,'A quantity 43 t.')
        files=[p.relative_to(self.root).as_posix() for p in claims.tier_files(self.root,self.root/'dist.manifest')]
        self.assertEqual(files[-7:],['docs/PHYSICS.md','docs/ARCHITECTURE.md','research/analysis/note.md','sim/README.md','tests/README.md','tools/README.md','DATA-SOURCES.md'])
        self.assertNotIn('43',[o['raw'] for o in self.extract()])

    def test_analysis_gate_context_does_not_bind_equal_digits_elsewhere(self):
        from claims_rules import Context
        import check_analysis as gate
        from unittest.mock import patch
        self.put('index.html','')
        self.put('research/analysis/fixture.json','{"length":110}')
        self.put('research/analysis/fixture.md','The model length is **110 m**; a different 110 m figure.\n\nUnrelated 110 m.\n')
        with patch.object(gate,'MANIFEST',[('fixture.md','fixture','length','d')]), patch.object(gate,'CONTEXTS',{('fixture.md','length'):r'model length is \*\*{number} m'}):
            occ=self.extract();ctx=Context(self.root,['research/analysis/fixture.md'])
            first=next(o for o in occ if o['raw']=='110')
            self.assertIsNotNone(ctx.analysis_owner(first))
            others=[o for o in occ if o['raw']=='110'][1:]
            self.assertTrue(all(ctx.analysis_owner(o) is None for o in others))

    def test_computed_percentage_owns_only_its_complete_display(self):
        from claims_rules import Context
        import check_analysis as gate
        from unittest.mock import patch
        self.put('index.html', '')
        self.put('research/analysis/fixture.json', '{"utilisation":1.0}')
        with patch.object(gate, 'MANIFEST', [('fixture.md', 'fixture', 'utilisation', '.0%')]), \
             patch.object(gate, 'CONTEXTS', {('fixture.md', 'utilisation'): r'Utilisation is {number} of the cap'}):
            self.put('research/analysis/fixture.md', 'Utilisation is 100% of the cap; unrelated 100.\n')
            numbers = [o for o in self.extract() if o['raw'] == '100']
            ctx = Context(self.root, ['research/analysis/fixture.md'])
            self.assertEqual(ctx.analysis_owner(numbers[0])['region'], 'research/analysis/fixture.json#utilisation')
            self.assertIsNone(ctx.analysis_owner(numbers[1]))
            for text in ('Utilisation is 99% of the cap.\n', 'Utilisation is 100 of the cap.\n'):
                self.put('research/analysis/fixture.md', text)
                ctx = Context(self.root, ['research/analysis/fixture.md'])
                self.assertTrue(all(ctx.analysis_owner(o) is None for o in self.extract()))

    def test_generated_markdown_is_held_by_check_producer(self):
        from claims_rules import Context
        self.put('index.html','')
        self.put('research/analysis/energy-unheld.md','110 tonnes.\n')
        self.put('research/analysis/energy-unheld.mjs', "import fs from 'node:fs'; if(fs.readFileSync('research/analysis/energy-unheld.md','utf8')!=='110 tonnes.\\n')process.exitCode=1;")
        o=self.extract()[0];ctx=Context(self.root,['research/analysis/energy-unheld.md'])
        owner,gate=ctx.generator_owner(o)
        self.assertIsNone(ctx.generated_issue(o,claims.entry_for(o,owner,gate)))
        self.put('research/analysis/energy-unheld.md','111 tonnes.\n')
        ctx=Context(self.root,['research/analysis/energy-unheld.md'])
        self.assertEqual(ctx.generated_issue(o,claims.entry_for(o,owner,gate))['kind'],'stale-generated-region')

    def test_motion_numbers_have_json_owner_and_reject_a_hand_edit(self):
        from claims_rules import Context
        self.put('index.html','')
        prefix='<!-- energy:motion:start -->\n'
        suffix=' tonnes.\n<!-- energy:motion:end -->\n'
        self.put('research/analysis/energy-motion.json','{"gap":110}')
        self.put('research/analysis/energy-motion.md',prefix+'110'+suffix)
        self.put('research/analysis/energy-motion.mjs',
                 "import fs from 'node:fs'; const d=JSON.parse(fs.readFileSync('research/analysis/energy-motion.json')); "
                 "const expected="+json.dumps(prefix)+"+d.gap+"+json.dumps(suffix)+"; "
                 "if(!process.argv.includes('--check')||fs.readFileSync('research/analysis/energy-motion.md','utf8')!==expected)process.exitCode=1;")
        occ=self.extract()[0]
        ctx=Context(self.root,['research/analysis/energy-motion.md'])
        owner,gate=ctx.generator_owner(occ)
        self.assertEqual(owner['source'],'research/analysis/energy-motion.json')
        self.assertEqual(gate,'energydoccheck')
        self.assertIsNone(ctx.generated_issue(occ,claims.entry_for(occ,owner,gate)))
        self.put('research/analysis/energy-motion.md',prefix+'111'+suffix)
        ctx=Context(self.root,['research/analysis/energy-motion.md'])
        self.assertEqual(ctx.generated_issue(occ,claims.entry_for(occ,owner,gate))['kind'],'stale-generated-region')


class SpanBasisTest(ClaimsFixture, unittest.TestCase):
    def test_model_key_does_not_clear_a_deferred_float_block(self):
        from claims_rules import Context
        self.put('index.html','')
        self.put('dist.manifest','served ship/index.html')
        self.put('ship/index.html','<p>Mass <span data-n="ship.massT"></span> t.</p>')
        occ=self.extract()[0];ctx=Context(self.root,['ship/index.html'])
        hit=dict(bounds=(1,1),dynamicFigures=[dict(route='ship.massT')],match_text='Mass t.',
                 record='research/analysis/float-claims/fixture.json',key='exact',status='DEFERRED',
                 reason='deferred: An independent physical basis is needed.',deferredReason='An independent physical basis is needed.')
        ctx.float_blocks={'ship/index.html':[hit]};ctx.contexts={'ship/index.html':{'ship':{'massT':110}}}
        owner=ctx.span_owner(occ)
        self.assertEqual(owner['physical_basis']['key'],'exact')
        self.assertEqual(ctx.span_issue(occ,claims.entry_for(occ,owner))['kind'],'float-deferred')
        hit.update(status='ALLOW',reason='method: The context is checked.')
        owner=ctx.span_owner(occ)
        self.assertIsNone(ctx.span_issue(occ,claims.entry_for(occ,owner)))
        hit['bounds']=(2,2)
        self.assertIsNone(ctx.float_hit(occ))


class ReadmeProducerTest(ClaimsFixture, unittest.TestCase):
    def test_readme_inline_and_indented_regions_own_only_checked_contents(self):
        from claims_rules import Context
        self.put('index.html','')
        source='Outside 120 m. <!-- readme:example:start -->Inside 110 m.<!-- readme:example:end --> Tail 130 m.\n'
        self.put('README.md',source)
        self.put('tools/gen_readme.py','import json\nprint('+repr(json.dumps({'README.md':source}))+')\n')
        occ=self.extract();inside=next(o for o in occ if o['raw']=='110');outside=[o for o in occ if o['raw'] in {'120','130'}]
        ctx=Context(self.root,['README.md']);owner,gate=ctx.generator_owner(inside)
        self.assertEqual(gate,'readmecheck');self.assertTrue(all(ctx.generator_owner(o) is None for o in outside))
        self.assertIsNone(ctx.generated_issue(inside,claims.entry_for(inside,owner,gate)))
        self.put('README.md',source.replace('110','111'))
        ctx=Context(self.root,['README.md'])
        self.assertEqual(ctx.generated_issue(inside,claims.entry_for(inside,owner,gate))['kind'],'stale-generated-region')


class ObjectionProducerTest(ClaimsFixture, unittest.TestCase):
    def test_solar_owner_is_exact_and_refuses_stale_text(self):
        from claims_rules import Context
        source='Outside 120 m.\n\n<!-- solar:area:start -->\nCoverage 85%.\n<!-- solar:area:end -->\n'
        file='research/reports/02-paper.md'
        self.put(file,source)
        self.put('tools/gen_solar_prose.py','import json\nprint('+repr(json.dumps({file:source}))+')\n')
        occ=self.extract();inside=next(o for o in occ if o['raw']=='85')
        ctx=Context(self.root,[file]);owner,gate=ctx.generator_owner(inside)
        self.assertEqual(gate,'analysischeck')
        self.assertIsNone(ctx.generated_issue(inside,claims.entry_for(inside,owner,gate)))
        self.assertIsNone(ctx.generator_owner(next(o for o in occ if o['raw']=='120')))
        self.put(file,source.replace('85%','86%'))
        self.assertEqual(Context(self.root,[file]).generated_issue(inside,claims.entry_for(inside,owner,gate))['kind'],'stale-generated-region')


class GeneratedDeferralTest(ClaimsFixture, unittest.TestCase):
    def test_generated_region_cannot_clear_its_recorded_deferral(self):
        from claims_rules import Context
        self.put('index.html','<p>\n<!-- served-energy:home:start -->\nMass 110 kg.\n<!-- served-energy:home:end -->\n</p>')
        occ=self.extract()[0];ctx=Context(self.root,['index.html'])
        hit=dict(match_text=occ['text'],record='research/analysis/float-claims/fixture.json',key='exact',
                 status='DEFERRED',reason='deferred: A physical source is needed.',deferredReason='A physical source is needed.')
        ctx.float_blocks={'index.html':[hit]}
        owner,gate=ctx.choose(occ,claims.seed_owner)
        self.assertEqual(owner['kind'],'ledger')
        self.assertEqual(ctx.ledger_issue(occ,claims.entry_for(occ,owner,gate))['kind'],'float-deferred')
        hit.update(status='ALLOW',reason='method: Model quantity is checked.')
        owner,gate=ctx.choose(occ,claims.seed_owner)
        self.assertEqual(owner['generator'],'tools/gen_energy_pages.mjs')


if __name__ == '__main__':
    unittest.main()
