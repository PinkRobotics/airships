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


class ClaimsTest(unittest.TestCase):
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
        return entries

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
        return o, defect

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


if __name__ == '__main__':
    unittest.main()
