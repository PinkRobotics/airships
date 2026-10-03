"""Float record contracts and counterexamples on small disposable trees."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import tempfile
import subprocess
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import float_claims as claims


class RecordContracts(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory(prefix='float-contract-')
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        self.record = self.root / 'research/analysis/float-claims'
        self.record.mkdir(parents=True)
        subprocess.run(['git','init','-q'],cwd=self.root,check=True)
        for name, value in [('ROOT', self.root), ('RECORD', self.record)]:
            mock = patch.object(claims, name, value)
            mock.start()
            self.addCleanup(mock.stop)
        self.write('Makefile', 'check: pagecheck\npagecheck:\n\tpython3 tools/render.py\n')
        self.write('tools/render.py', 'def render():\n    return "mass"\n')
        self.ledger = {'atmosphere': {'targetM': 2500},
                       'verdict': 'Nothing floats today as drawn.',
                       'designs': [{'cases': [{'id': 'hull', 'mass': 403.1,
                           'at': {'seaLevel': {'liftToMass': .557725},
                                  'target': {'liftToMass': .435643}}}]}]}
        self.write(claims.LEDGER_PATH, json.dumps(self.ledger))
        self.write(claims.CAP_READINGS, json.dumps({'ranges': {'favourable': {
            'seaLevel': {'min': .75062, 'max': .998418},
            'target': {'min': .58631, 'max': .77987}}}, 'noneReachesOne': True}))
        self.hit, self.entry = self.block('Hull mass is 403.1 t.', 'bound',
            bindings=[{'case': 'hull', 'field': 'mass', 'shown': '403.1'}])

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        if name.endswith(('.py','.mjs')):
            subprocess.run(['git','add','-N','--',name],cwd=self.root,check=True)

    def block(self, text, cls, file='docs/example.md', **extra):
        self.write(file, text + '\n')
        hit = dict(file=file, line=1, sentence=text, status='FAIL', reason='Unbound.', dynamicFigures=[])
        entry = dict(file=file, line=1, key=claims.key_of(text), text=text,
                     **{'class': cls}, reason='The fixture names this particular hull mass.', **extra)
        return hit, entry

    def check(self, entry=None, hit=None):
        return claims.check_entry(entry or self.entry, hit or self.hit,
                                  claims.Sources(self.ledger), self.ledger)

    def rejects(self, message, entry=None, hit=None):
        errors = self.check(entry, hit)
        self.assertTrue(any(message in e for e in errors), errors)

    def shard(self, entries, dated=(), name='example', files=None):
        if files is None:
            files = sorted({e['file'] for e in [*entries, *dated]})
        self.write(f'research/analysis/float-claims/{name}.json', json.dumps(
            dict(schema=claims.SCHEMA, files=files, entries=entries, dated=list(dated))))

    def apply(self, hits, entries, **kwargs):
        self.shard(entries, **kwargs)
        result = copy.deepcopy(hits)
        errors = claims.apply(result, self.ledger)
        return result, errors

    def test_catalog_array_route_matches_page_binder(self):
        import check_float_ledger as gate
        self.assertEqual(gate.dig({'ladder': [{'exponent': 2}]}, 'ladder.0.exponent'), 2)
        with self.assertRaises((KeyError, TypeError, ValueError)):
            gate.dig({'ladder': [{'exponent': 2}]}, 'ladder.no.exponent')

    def test_bound_figure_and_hand_changed_ledger(self):
        self.assertEqual(self.check(), [])
        self.ledger['designs'][0]['cases'][0]['mass'] = 404.1
        self.rejects('differs from its source field')

    def test_shown_precision_scale_and_sign(self):
        self.entry['bindings'][0].update(shown='403100', scale=1000)
        self.hit['sentence'] = 'Hull mass is 403100 kg.'
        self.assertEqual(self.check(), [])
        self.entry['bindings'][0]['scale'] = 1
        self.rejects('differs from its source field')
        self.entry['bindings'][0].update(shown='403.1', abs=True)
        self.hit['sentence'] = 'Hull mass is 403.1 t.'
        self.ledger['designs'][0]['cases'][0]['mass'] = -403.1
        self.assertEqual(self.check(), [])

    def test_figure_must_be_visible(self):
        self.assertEqual(self.check(), [])
        self.hit['sentence'] = 'Hull mass is 404.1 t.'
        self.rejects('is not in the visible text')

    def test_source_resolution(self):
        self.assertEqual(self.check(), [])
        self.entry['bindings'][0]['case'] = 'absent'
        self.rejects('binding does not resolve:')

    def test_json_source_and_wrong_reading(self):
        h, e = self.block('Favourable ratio is 0.998 at sea level.', 'bound', bindings=[{
            'source': claims.CAP_READINGS, 'pointer': '/ranges/favourable/seaLevel/max',
            'shown': '0.998', 'altitude': 'seaLevel'}])
        self.assertEqual(self.check(e, h), [])
        e['bindings'][0]['pointer'] = '/ranges/favourable/seaLevel/min'
        self.rejects('differs from its source field', e, h)

    def test_equality(self):
        h, e = self.block('Nothing floats today as drawn.', 'bound', bindings=[{
            'source': claims.LEDGER_PATH, 'pointer': '/verdict', 'equals': self.ledger['verdict']}])
        self.assertEqual(self.check(e, h), [])
        e['bindings'][0]['equals'] = 'Everything floats.'
        self.rejects('source value', e, h)

    def test_range_altitude_cannot_relabel_or_omit_source_altitude(self):
        h, e = self.block('Favourable ratio is 0.998 at sea level.', 'bound', bindings=[{
            'source': claims.CAP_READINGS, 'pointer': '/ranges/favourable/seaLevel/max',
            'shown': '0.998', 'altitude': 'seaLevel'}])
        self.assertEqual(self.check(e, h), [])
        h['sentence'] = 'Favourable ratio is 0.998 at 2,500 m.'
        e['context'] = ['2500']
        e['bindings'][0]['altitude'] = 'target'
        self.rejects('range altitude must match its source pointer', e, h)
        self.rejects('does not name the altitude', e, h)
        del e['bindings'][0]['altitude']
        h['sentence'] = 'Favourable ratio is 0.998.'
        self.rejects('range altitude must match its source pointer', e, h)
        self.rejects('does not name the altitude', e, h)

    def test_one_check_per_binding(self):
        self.assertEqual(self.check(), [])
        self.entry['bindings'][0]['equals'] = 403.1
        self.rejects('exactly one of: shown, route, equals')

    def test_altitude_removed_or_wrong(self):
        h, e = self.block('Hull ratio is 0.558 at sea level.', 'bound', bindings=[{
            'case': 'hull', 'field': 'at.seaLevel.liftToMass', 'shown': '0.558'}])
        self.assertEqual(self.check(e, h), [])
        h['sentence'] = 'Hull ratio is 0.558.'
        self.rejects('does not name the altitude', e, h)
        h['sentence'] = 'Hull ratio is 0.558 at sea level.'
        e['bindings'][0]['field'] = 'at.target.liftToMass'
        self.rejects('differs from its source field', e, h)
        self.rejects('does not name the altitude', e, h)

    def test_heading_must_be_above_and_near(self):
        h, e = self.block('Hull ratio is 0.436.', 'bound', bindings=[{
            'case': 'hull', 'field': 'at.target.liftToMass', 'shown': '0.436'}], heading='At 2,500 m')
        self.write(h['file'], 'At 2,500 m\n' + h['sentence'])
        h['line'] = 2
        self.assertEqual(self.check(e, h), [])
        self.write(h['file'], 'At 2,500 m\n' + '\n' * 61 + h['sentence'])
        h['line'] = 63
        self.rejects('is not in the 60 lines above', e, h)

    def test_context_and_unbound_numbers(self):
        self.hit['sentence'] += ' Safety factor 1.2.'
        self.entry['context'] = ['1.2']
        self.assertEqual(self.check(), [])
        self.entry['context'] = []
        self.rejects('numbers neither bound nor listed as context: 1.2')

    def test_reason_and_class(self):
        self.assertEqual(self.check(), [])
        self.entry['reason'] = ''
        self.rejects('reason must say why')
        self.entry['class'] = 'UNREVIEWED'
        self.rejects("class 'UNREVIEWED' is not one of")

    def test_required_binding_and_binding_classes(self):
        self.assertEqual(self.check(), [])
        self.entry['bindings'] = []
        self.rejects('a bound block names at least one binding')
        self.entry['class'] = 'other-quantity'
        self.assertEqual(self.check(), [])
        self.entry['bindings'] = [{'case': 'hull', 'field': 'mass', 'shown': '403.1'}]
        self.rejects('bindings are checked only on bound, question and calculator')

    def live(self):
        h, e = self.block('Mass [data-n="ship.mass"] t.', 'live-model', file='ship/example.html')
        h['dynamicFigures'] = [{'route': 'ship.mass', 'display': '403.1'}]
        return h, e

    def test_live_model_verdict_mutation(self):
        h, e = self.live()
        self.assertEqual(self.check(e, h), [])
        h['sentence'] += ' It floats only in the best defensible world.'
        self.rejects('verdict words in a block classed live-model', e, h)

    def test_live_model_requires_resolved_binder(self):
        h, e = self.live()
        self.assertEqual(self.check(e, h), [])
        h['dynamicFigures'][0]['display'] = 'unresolved'
        self.rejects('did not resolve', e, h)
        h['dynamicFigures'] = []
        self.rejects('a live-model block displays at least one figure', e, h)

    def test_route_binding(self):
        h, e = self.live()
        e.update({'class': 'bound', 'bindings': [{'case': 'hull', 'field': 'mass', 'route': 'ship.mass'}]})
        self.assertEqual(self.check(e, h), [])
        h['dynamicFigures'][0]['display'] = '404.1'
        self.rejects('displays 404.1 but its source field', e, h)
        h['dynamicFigures'][0]['display'] = 'unresolved'
        self.rejects('did not resolve', e, h)
        e['bindings'][0]['route'] = 'missing'
        self.rejects('is not displayed in this block', e, h)

    def test_bound_covers_every_binder(self):
        h, e = self.live()
        e.update({'class': 'bound', 'bindings': [{'case': 'hull', 'field': 'mass', 'route': 'ship.mass'}]})
        self.assertEqual(self.check(e, h), [])
        h['dynamicFigures'].append({'route': 'ship.extra', 'display': '999'})
        self.rejects('routes without bindings: ship.extra', e, h)

    def test_calculator_function_and_gate(self):
        h, e = self.block('floats', 'calculator', file='ship/example.html', function='render', gate='pagecheck')
        self.write(h['file'], 'function render() { return ratio >= 1 ? "floats" : "sinks"; }')
        self.assertEqual(self.check(e, h), [])
        e['function'] = 'missing'
        self.rejects('a calculator names a function', e, h)
        e['function'] = 'render'
        e['gate'] = 'missing'
        self.rejects('a calculator names the make target', e, h)

    def test_generated_script_and_page(self):
        h, e = self.block('Mass comparison.', 'generated', generator='tools/render.py', gate='pagecheck')
        self.assertEqual(self.check(e, h), [])
        e['generator'] = 'tools/missing.py'
        self.rejects('a generated block names the tracked script', e, h)
        e['generator'] = 'tools/render.py'
        h['file'] = 'ship/example.html'
        self.rejects('generated is for analysis notes', e, h)

    def test_literature_requires_source(self):
        h, e = self.block('The cited gas vessel floats.', 'literature', source='Fixture monograph')
        self.assertEqual(self.check(e, h), [])
        del e['source']
        self.rejects('a literature block names its source', e, h)

    def test_history_date_and_served_page(self):
        h, e = self.block('The old certified world floats.', 'history', date='2020-01-02')
        self.assertEqual(self.check(e, h), [])
        e['date'] = 'yesterday'
        self.rejects('a history block names its date', e, h)
        e['date'] = '2020-01-02'
        h['file'] = 'ship/example.html'
        self.rejects('history is for dated documents', e, h)

    def test_certified_world_only_in_history(self):
        h, e = self.block('The old certified world floats.', 'history', date='2020-01')
        self.assertEqual(self.check(e, h), [])
        e.update({'class': 'literature', 'source': 'Fixture monograph'})
        self.rejects('"certified world" outside a dated record', e, h)

    def test_other_quantity_cannot_give_verdict(self):
        h, e = self.block('Water mass is 20 t.', 'other-quantity')
        self.assertEqual(self.check(e, h), [])
        h['sentence'] += ' The hull is neutrally buoyant.'
        self.rejects('verdict words in a block classed other-quantity', e, h)

    def test_conditional_says_so(self):
        h, e = self.block('Assumed shell mass is 20 t.', 'conditional')
        self.assertEqual(self.check(e, h), [])
        h['sentence'] = 'Shell mass is 20 t.'
        self.rejects('a conditional block says in its own words', e, h)

    def test_question_only_in_question_documents(self):
        h, e = self.block('Can the hull float?', 'question', file=claims.QUESTION_FILES[0])
        self.assertEqual(self.check(e, h), [])
        h['file'] = 'docs/example.md'
        self.rejects('question is for docs/OPEN-QUESTIONS.md', e, h)

    def assumption(self):
        return self.block('The flight model assumes a hull that floats; no drawn hull does. '
                          'See [the float case](FLOAT.md).', 'bound', bindings=[{
                              'source': claims.LEDGER_PATH, 'pointer': '/verdict',
                              'equals': self.ledger['verdict']}])

    def test_flight_assumption_and_structural_verdict(self):
        a, ae = self.assumption()
        h, e = self.block('The simulated hull floats upward.', 'flight-model', assumption=ae['key'])
        self.assertEqual(self.check(e, h), [])
        result, errors = self.apply([a, h], [ae, e])
        self.assertEqual(errors, [])
        self.assertEqual(result[1]['status'], 'ALLOW')
        h['sentence'] = 'The simulated hull is neutrally buoyant.'
        self.rejects('a flight-model block carries a structural verdict', e, h)
        del e['assumption']
        self.rejects('a flight-model block names the key', e, h)

    def test_flight_reference_must_exist_in_same_file(self):
        a, ae = self.assumption()
        h, e = self.block('The simulated hull floats upward.', 'flight-model', assumption=ae['key'])
        result, errors = self.apply([a, h], [ae, e])
        self.assertEqual(result[1]['status'], 'ALLOW')
        e['assumption'] = 'missing'
        result, errors = self.apply([a, h], [ae, e])
        self.assertIn('no bound block with key missing', result[1]['reason'])

    def test_unrelated_assumption_cannot_license_flight(self):
        a, ae = self.block('Assumed hull mass is 403.1 t.', 'bound', bindings=self.entry['bindings'])
        h, e = self.block('The simulated hull floats upward.', 'flight-model', assumption=ae['key'])
        result, errors = self.apply([a, h], [ae, e])
        self.assertEqual(result[1]['status'], 'FAIL')
        self.assertIn('no bound block', result[1]['reason'])

    def test_flight_assumption_needs_verdict_binding_and_link(self):
        a, ae = self.assumption()
        h, e = self.block('The simulated hull floats upward.', 'flight-model', assumption=ae['key'])
        result, errors = self.apply([a, h], [ae, e])
        self.assertEqual(result[1]['status'], 'ALLOW')
        ae['bindings'] = [{'source': claims.CAP_READINGS, 'pointer': '/noneReachesOne', 'equals': True}]
        result, errors = self.apply([a, h], [ae, e])
        self.assertEqual(result[1]['status'], 'FAIL')
        self.assertIn('no bound block', result[1]['reason'])

    def test_stale_entry_and_unrecorded_edit(self):
        hits, errors = self.apply([self.hit], [self.entry])
        self.assertEqual(errors, [])
        self.assertEqual(hits[0]['status'], 'PASS')
        self.hit['sentence'] = 'Hull mass is 999 t.'
        hits, errors = self.apply([self.hit], [self.entry])
        self.assertIn('No disposition', hits[0]['reason'])
        self.assertIn('stale entry', errors[0])

    def test_two_shards_and_duplicate_entry(self):
        self.shard([self.entry])
        self.assertEqual(claims.load_record()[2], [])
        self.shard([self.entry], name='second')
        self.assertTrue(any('already belongs to another shard' in e for e in claims.load_record()[2]))
        (self.record / 'second.json').unlink()
        self.shard([self.entry, self.entry])
        self.assertTrue(any('two entries with key' in e for e in claims.load_record()[2]))

    def test_schema_and_file_ownership(self):
        self.shard([self.entry])
        self.assertEqual(claims.load_record()[2], [])
        self.shard([self.entry], files=[])
        self.assertIn('which the shard does not list under files', claims.load_record()[2][0])
        self.write('research/analysis/float-claims/example.json', '{"schema":"wrong"}')
        self.assertIn('schema is not', claims.load_record()[2][0])
        self.write('research/analysis/float-claims/example.json', '{')
        self.assertIn('not JSON', claims.load_record()[2][0])

    def test_dated_notice_required_and_removed_in_same_process(self):
        dated = dict(file=self.hit['file'], date='2020-01-02', reason='An explicitly dated account of the former mass estimate.')
        self.write(self.hit['file'], '# Record\n\nDated 2020-01-02; see [current ledger](FLOAT-LEDGER.md).\n\n' + self.hit['sentence'])
        hits, errors = self.apply([self.hit], [], dated=[dated])
        self.assertEqual(errors, [])
        self.assertEqual(hits[0]['status'], 'FAIL')
        # A dated notice establishes provenance, never a disposition for unseen text.
        hits, errors = self.apply([self.hit], [dict(self.entry, **{'class':'history'},date=dated['date'],bindings=[])], dated=[dated])
        self.assertEqual(hits[0]['status'], 'ALLOW')
        self.write(self.hit['file'], '# Record\n\n' + self.hit['sentence'])
        hits, errors = self.apply([self.hit], [], dated=[dated])
        self.assertTrue(any('a dated file carries' in e for e in errors), errors)

    def test_dated_notice_must_link_and_name_date(self):
        dated = dict(file=self.hit['file'], date='2020-01', reason='An explicitly dated account of the former mass estimate.')
        self.write(self.hit['file'], '# Record\n2020-01; [current ledger](FLOAT-LEDGER.md).')
        self.shard([], dated=[dated])
        self.assertEqual(claims.load_record()[2], [])
        self.write(self.hit['file'], '# Record\nFLOAT-LEDGER.md')
        self.assertTrue(any('notice' in e for e in claims.load_record()[2]))

    def pair(self):
        h, e = self.block('Hull ratio 0.558 at sea level and 0.436 at 2,500 m.', 'bound',
            context=['2500'], bindings=[{'case': 'hull', 'field': 'at.seaLevel.liftToMass', 'shown': '0.558'},
                                      {'case': 'hull', 'field': 'at.target.liftToMass', 'shown': '0.436'}])
        cap, ce = self.block('No cap reading reaches one.', 'bound', bindings=[{
            'source': claims.CAP_READINGS, 'pointer': '/noneReachesOne', 'equals': True}])
        cap['line'] = ce['line'] = 3
        return h, e, cap, ce

    def test_p1_same_case_both_altitudes_first(self):
        h, e, cap, ce = self.pair()
        self.assertEqual(self.apply([h, cap], [e, ce])[1], [])
        e['bindings'].pop()
        e['context'].append('0.436')
        self.assertTrue(any('P1:' in s for s in self.apply([h, cap], [e, ce])[1]))

    def test_p1_pointer_cannot_bypass(self):
        h, e, cap, ce = self.pair()
        e['bindings'] = [{'source': claims.LEDGER_PATH,
                          'pointer': '/designs/0/cases/0/at/seaLevel/liftToMass',
                          'shown': '0.558'}]
        e['context'].append('0.436')
        self.assertTrue(any('P1:' in s for s in self.apply([h, cap], [e, ce])[1]))

    def test_p2_requires_cap_readings(self):
        h, e, cap, ce = self.pair()
        self.assertEqual(self.apply([h, cap], [e, ce])[1], [])
        self.assertTrue(any('P2:' in s for s in self.apply([h], [e])[1]))

    def test_ratio_precision_cannot_round_a_deficit_to_one(self):
        h, e = self.block('Hull ratio is 0.558 at sea level.', 'bound', bindings=[{
            'case': 'hull', 'field': 'at.seaLevel.liftToMass', 'shown': '0.558'}])
        self.assertEqual(self.check(e, h), [])
        self.ledger['designs'][0]['cases'][0]['at']['seaLevel']['liftToMass'] = .9999
        h['sentence'] = 'Hull ratio is 1.000 at sea level.'
        e['bindings'][0]['shown'] = '1.000'
        self.rejects('a ratio below one must not be rounded up to one', e, h)
        self.ledger['designs'][0]['cases'][0]['at']['seaLevel']['liftToMass'] = .558
        h['sentence'] = 'Hull ratio is 0.56 at sea level.'
        e['bindings'][0]['shown'] = '0.56'
        self.rejects('lift-to-mass ratios print to three decimals', e, h)

    def test_equality_preserves_boolean_type(self):
        h, e = self.block('No cap reading reaches one.', 'bound', bindings=[{
            'source': claims.CAP_READINGS, 'pointer': '/noneReachesOne', 'equals': True}])
        self.assertEqual(self.check(e, h), [])
        e['bindings'][0]['equals'] = 1
        self.rejects('source value', e, h)

    def test_python_comparisons_remain_in_the_inventory_key(self):
        import check_float_ledger as gate
        with patch.object(gate, 'ROOT', self.root):
            path = self.root / 'tools/example.py'
            self.write('tools/example.py', '\"\"\"The float condition is mass < lift > zero.\"\"\"')
            first = list(gate.source_blocks(path))
            self.assertEqual(len(first), 1)
            self.assertEqual(first[0][1], 'The float condition is mass < lift > zero.')
            self.write('tools/example.py', '\"\"\"The float condition is mass < impossible > zero.\"\"\"')
            second = list(gate.source_blocks(path))
            self.assertEqual(len(second), 1)
            self.assertNotEqual(claims.key_of(first[0][1]), claims.key_of(second[0][1]))

    def test_html_inventory_preserves_assumption_link(self):
        import check_float_ledger as gate
        file = 'ship/example.html'
        self.write(file, '<p>The flight model assumes a hull that floats; no drawn hull does. '
                   '<a href="../float/">The float case</a>.</p>')
        with patch.object(gate, 'ROOT', self.root):
            line, text, raw = list(gate.source_blocks(self.root / file))[0]
        h, e = self.block(text, 'bound', file=file, bindings=[{
            'source': claims.LEDGER_PATH, 'pointer': '/verdict',
            'equals': 'Nothing floats today as drawn.'}])
        h['raw'] = raw
        flight, fe = self.block('The simulated ship floats after releasing its water.',
                               'flight-model', file=file, assumption=e['key'])
        result, errors = self.apply([h, flight], [e, fe])
        self.assertEqual(errors, [])
        self.assertEqual(result[1]['status'], 'ALLOW', result[1]['reason'])
        h['raw'] = raw.replace('../float/', '../docs/elsewhere.md')
        result, errors = self.apply([h, flight], [e, fe])
        self.assertEqual(result[1]['status'], 'FAIL')
        self.assertIn('no bound block', result[1]['reason'])

    def html_assumption(self, href, file='ship/example.html'):
        """An HTML assumption block and the flight block that names it, read as the gate reads."""
        import check_float_ledger as gate
        self.write(file, '<p>The flight model assumes a hull that floats; no drawn hull does. '
                   f'<a href="{href}">The float case</a>.</p>')
        with patch.object(gate, 'ROOT', self.root):
            line, text, raw = list(gate.source_blocks(self.root / file))[0]
        self.assertIn(f'href="{href}"', raw)
        h, e = self.block(text, 'bound', file=file, bindings=[{
            'source': claims.LEDGER_PATH, 'pointer': '/verdict',
            'equals': 'Nothing floats today as drawn.'}])
        h['raw'] = raw
        flight, fe = self.block('The simulated ship floats after releasing its water.',
                                'flight-model', file=file, assumption=e['key'])
        result, errors = self.apply([h, flight], [e, fe])
        self.assertEqual(errors, [])
        return result[1]

    def test_html_assumption_that_links_the_document_is_not_an_assumption(self):
        # The site does not publish docs/, so on a page that link is dead.
        for file, href in (('ship/example.html', '../docs/FLOAT.md'),
                           ('index.html', 'docs/FLOAT.md'),
                           ('ship/example.html', '../docs/FLOAT.md#the-verdict')):
            with self.subTest(file=file, href=href):
                flight = self.html_assumption(href, file)
                self.assertEqual(flight['status'], 'FAIL')
                self.assertIn('no bound block', flight['reason'])

    def test_html_assumption_that_links_the_published_float_case_passes(self):
        for file, href in (('ship/example.html', '../float/'),
                           ('ship/example.html', '../float/index.html'),
                           ('ship/example.html', '../float/#the-verdict'),
                           ('index.html', 'float/'),
                           ('index.html', 'float/index.html')):
            with self.subTest(file=file, href=href):
                flight = self.html_assumption(href, file)
                self.assertEqual(flight['status'], 'ALLOW', flight['reason'])
        # The ledger page and the census page are not the float case; nor is ship/float/.
        for href in ('../float/ledger.html', '../float/census.html', 'float/', '../floats/'):
            with self.subTest(href=href):
                flight = self.html_assumption(href)
                self.assertEqual(flight['status'], 'FAIL')
                self.assertIn('no bound block', flight['reason'])

    def test_markdown_assumption_links_the_document_as_before(self):
        a, ae = self.assumption()
        h, e = self.block('The simulated hull floats upward.', 'flight-model', assumption=ae['key'])
        result, errors = self.apply([a, h], [ae, e])
        self.assertEqual((errors, result[1]['status']), ([], 'ALLOW'))
        # A document links the document; the published page does not stand in for it.
        a, ae = self.block('The flight model assumes a hull that floats; no drawn hull does. '
                           'See [the float case](../float/index.html).', 'bound',
                           bindings=ae['bindings'])
        h, e = self.block('The simulated hull floats upward.', 'flight-model', assumption=ae['key'])
        result, errors = self.apply([a, h], [ae, e])
        self.assertEqual(result[1]['status'], 'FAIL')
        self.assertIn('no bound block', result[1]['reason'])

    def test_json_pointer_escape(self):
        self.assertEqual(claims.pointer({'a': [3]}, '/a/0'), 3)
        self.assertEqual(claims.pointer({'a/b': {'~c': 4}}, '/a~1b/~0c'), 4)

    def test_verdict_is_checked_even_after_inline_pass(self):
        h, e = self.live()
        h['sentence'] += ' The hull floats only in the best defensible world.'
        e['key'] = claims.key_of(h['sentence'])
        h['status'] = 'PASS'
        result, errors = self.apply([h], [e])
        self.assertEqual(result[0]['status'], 'FAIL')
        self.assertIn('verdict words', result[0]['reason'])


    def test_method_comma_before_metre_symbol(self):
        h, e = self.block('The method names pressure, mass, m and force.', 'method')
        self.assertEqual(self.check(e, h), [])

    def test_method_context_and_unlisted_mass(self):
        h, e = self.block('To float, displaced air must exceed mass; use factor 1.2.',
                          'method', context=['1.2'])
        self.assertEqual(self.check(e, h), [])
        h['sentence'] += ' The mass is 403.1 t.'
        self.rejects('numbers neither bound nor listed as context: 403.1', e, h)

    def test_method_does_not_license_other_classes(self):
        h, e = self.block('To float, displaced air must exceed mass.', 'method')
        self.assertEqual(self.check(e, h), [])
        for cls in ('other-quantity', 'conditional', 'live-model'):
            e['class'] = cls
            self.rejects('verdict words', e, h)

    def test_definition_of_done_requires_its_words(self):
        h, e = self.block('The definition of done is unchanged from FLOAT.md: a gated bill under the air density.',
                          'conditional')
        self.assertEqual(self.check(e, h), [])
        h['sentence'] += ' The hull floats today.'
        self.rejects('verdict words', e, h)
        h['sentence'] = 'The bill is under the air density.'
        self.rejects('a conditional block says', e, h)

    def test_retargeting_proposal_requires_denial(self):
        h, e = self.block('Retargeting the span may still be wanted for handling. '
                          'It is **not** a route to floating.', 'conditional')
        self.assertEqual(self.check(e, h), [])
        h['sentence'] = 'Retargeting the span may still be wanted for handling. It is a route to floating.'
        self.rejects('a conditional block says', e, h)
        h['sentence'] = 'Retargeting the span is a route to floating.'
        self.rejects('a conditional block says', e, h)

    def deferred_fixture(self):
        h, e = self.block('The cycle claims a buoyant escape and delivery closure.',
                          'deferred', owner='energy-model')
        e['reason'] = 'Escape and delivery closure require the cycle calculation.'
        self.write('docs/OPEN-QUESTIONS.md', '<a id="float-deferred-energy-model"></a>\n')
        return h, e

    def test_deferred_is_separate_and_preserves_inventory(self):
        h, e = self.deferred_fixture()
        result, errors = self.apply([h], [e])
        self.assertEqual(errors, [])
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['sentence'], h['sentence'])
        self.assertEqual(result[0]['status'], 'DEFERRED')
        self.assertEqual(claims.deferred_counts(result), {'energy-model': 1})
        self.assertEqual(set(claims.DEFERRED_OWNERS),
                         {'energy-model', 'mixed-block', 'hand-arithmetic', 'source-needed'})
        result, errors = self.apply([dict(h, sentence=h['sentence']+' Revised.')], [e])
        self.assertEqual(result[0]['status'], 'FAIL')
        self.assertTrue(any('stale entry' in x for x in errors), errors)

    def test_deferred_unknown_removed_owner_and_missing_anchor(self):
        h, e = self.deferred_fixture()
        result, errors = self.apply([h], [e])
        self.assertEqual(errors, [])
        e['owner'] = 'unknown-owner'
        result, errors = self.apply([h], [e])
        self.assertTrue(any('unknown deferred owner' in x for x in errors), errors)
        e['owner'] = 'energy-model'
        with patch.dict(claims.DEFERRED_OWNERS, {}, clear=True):
            result, errors = self.apply([h], [e])
            self.assertTrue(any('unknown deferred owner' in x for x in errors), errors)
        self.write('docs/OPEN-QUESTIONS.md', 'The open item was removed.\n')
        result, errors = self.apply([h], [e])
        self.assertTrue(any('missing open-item anchor' in x for x in errors), errors)

    def test_deferred_list_freshness_and_content(self):
        h, e = self.deferred_fixture()
        result, errors = self.apply([h], [e])
        self.assertEqual(errors, [])
        rendered = claims.deferred_markdown(result)
        self.assertIn('docs/example.md:1', rendered)
        self.assertIn('energy-model', rendered)
        self.assertIn(e['reason'], rendered)
        self.assertTrue(claims.check_deferred(result))
        self.write(claims.DEFERRED_PATH, rendered)
        self.assertEqual(claims.check_deferred(result), [])
        self.write(claims.DEFERRED_PATH, rendered+'Edited by hand.\n')
        self.assertTrue(claims.check_deferred(result))
        self.write(claims.DEFERRED_PATH, rendered)
        result[0]['line'] = 9
        self.assertTrue(claims.check_deferred(result))


class ScopingLabels(unittest.TestCase):
    def test_record_name_requires_same_configuration_and_mass(self):
        import ship_scoping as scope
        scope.configure()
        self.addCleanup(scope.configure)
        cfg = dict(scope.PLAN_CFG)
        label = scope.hull_label(cfg)
        self.assertEqual(label, 'hull of record')
        cfg['depth'] = 4.0
        scope.configure(depth=4.0)
        self.assertIn("scoping tool's default hull (wall 4.0 m)", scope.hull_label(cfg))
        self.assertIn('depthM', scope.hull_label(cfg))
        scope.configure()
        cfg = dict(scope.PLAN_CFG, sR=0.6)
        self.assertIn('ringPitchM', scope.hull_label(cfg))
        with patch.object(scope, 'SF_DECL', 1.3):
            self.assertIn('sfDeclared', scope.hull_label(scope.PLAN_CFG))
        with patch.object(scope.vc, 'ship0', return_value={'totalT': 1, 'ratioSL': 1, 'ratio2500': 1}):
            with self.assertRaisesRegex(ValueError, 'hull of record does not reproduce'):
                scope.hull_label(scope.PLAN_CFG)



class HardenedLanguage(unittest.TestCase):
    def test_verdict_refusals_and_ordinary_prose(self):
        import check_float_ledger as gate
        refusals = [
            'The hull is lighter than the air it pushes aside, so it rises on its own.',
            'The 52 m hull is heavier than air and sinks on its own.',
            'The vehicle holds itself up in air.',
            'The vehicle lifts itself up.',
            'On the drawn hull, lift exceeds weight at sea level.',
            'The hull net lift is positive at sea level.',
            'The hull rises unaided from the ground.',
            'The hull carries its own structure with lift to spare.',
            'The hull needs ballast to stay down.',
            'The hull weighs less than nothing in air.',
            'On the drawn hull the deficit is closed at sea level.',
            'The vehicle has a surplus of lift.',
            'The hull has a shortfall of lift.',
            'Air supports the hull while it carries its own weight.',
        ]
        ordinary = ['centre of buoyancy', 'floating controls', 'float: right;',
                    'const n = parseFloat(value);',
                    'Climb and letdown each have independent peak-rate and peak-airspeed caps.',
                    'Hold-down descent is priced as climb, on the conservative side; '
                    'climb against hold-down thrust is priced as level flight, with no bound claimed.']
        for sentence in refusals:
            with self.subTest(sentence=sentence):self.assertTrue(gate.interesting(sentence))
        for sentence in ordinary:
            with self.subTest(sentence=sentence):self.assertFalse(gate.interesting(sentence))

    def test_each_false_numeric_hull_class_is_refused(self):
        ledger={'atmosphere':{'targetM':2500},'designs':[]}
        for cls in ('literature','conditional','other-quantity','method','history','question','deferred','live-model','flight-model'):
            text='If settled, the 52 m hull’s sea-level lift exceeds its mass by 41.2 t.'
            hit=dict(file='docs/FLOAT.md',line=1,sentence=text,dynamicFigures=[])
            entry=dict(file=hit['file'],key=claims.key_of(text),line=1,**{'class':cls},
                       reason='A deliberately false numeric hull result.',context=['52','41.2'],
                       date='2026-08',owner='hand-arithmetic',source='Test source',assumption='none')
            errors=claims.check_entry(entry,hit,claims.Sources(ledger),ledger)
            with self.subTest(cls=cls):
                self.assertTrue(any('requires a checked binding' in e for e in errors),errors)

    def test_script_escapes_fragments_templates_and_regex(self):
        from float_text import js_strings
        text = "const re = /['\"]/g; const x = 'The hull ' + 'floats.'; " + \
               "const y = `The hull ${ok ? 'floats' : 'sinks'} at sea level.`; " + \
               "// 'The false comment floats.'\nconst z='The hull fl\\u006fats.';"
        strings=[t for _,t in js_strings(text)]
        self.assertIn('The hull floats.',strings)
        self.assertIn('The hull floats.',strings)
        self.assertTrue(any(s.startswith('The hull ${') for s in strings))
        self.assertNotIn('The false comment floats.',strings)


class GeneratedRegionContracts(unittest.TestCase):
    def setUp(self):
        from float_regions import Regions
        self.tmp=tempfile.TemporaryDirectory(prefix='float-region-')
        self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)
        (self.root/'tools').mkdir()
        (self.root/'docs').mkdir()
        self.start,self.end='<!-- fixture:start -->','<!-- fixture:end -->'
        body=self.start+'\nThe computed float comparison.\n'+self.end+'\n'
        (self.root/'docs/result.md').write_text(body)
        (self.root/'tools/generate.py').write_text('import json\nprint(json.dumps('+repr({'docs/result.md':body})+'))\n')
        (self.root/'tools/verify.py').write_text("# tools/generate.py regenerates this output; ledgercheck compares it too.\n")
        (self.root/'Makefile').write_text('check: fresh\nfresh:\n\tpython3 tools/verify.py\n')
        subprocess.run(['git','init','-q'],cwd=self.root,check=True)
        subprocess.run(['git','add','-N','tools/generate.py','tools/verify.py'],cwd=self.root,check=True)
        self.entry=dict(file='docs/result.md',generator='tools/generate.py',gate='fresh',verifier='tools/verify.py',
                        region=dict(start=self.start,end=self.end))
        self.hit=dict(line=2)

    def check(self, entry=None):
        from float_regions import Regions
        return Regions(self.root,{'fresh'}).check(entry or self.entry,self.hit)

    def test_complete_region_passes(self):self.assertEqual(self.check(),[])

    def test_wrong_unpaired_reversed_and_inexact_markers(self):
        path=self.root/'docs/result.md';body=path.read_text()
        for bad in [body.replace(self.end,'<!-- wrong:end -->'),body.replace(self.start,''),
                    body.replace(self.start,'MARKER_SWAP').replace(self.end,self.start).replace('MARKER_SWAP',self.end),
                    body.replace(self.start,' '+self.start),body+self.end+'\n']:
            with self.subTest(body=bad):
                path.write_text(bad)
                self.assertTrue(self.check())
        path.write_text(body)
        self.assertTrue(self.check(dict(self.entry,region=dict(start='wrong',end=self.end))))

    def test_missing_untracked_generator_and_unrun_check(self):
        self.assertTrue(self.check(dict(self.entry,generator='tools/missing.py')))
        (self.root/'tools/untracked.py').write_text((self.root/'tools/generate.py').read_text())
        self.assertTrue(self.check(dict(self.entry,generator='tools/untracked.py')))
        self.assertTrue(self.check(dict(self.entry,gate='unchecked')))
        (self.root/'Makefile').write_text('check: fresh\nfresh:\n\tpython3 -c "pass"\n')
        self.assertTrue(self.check())

    def test_fresh_content_comparison_and_region_membership(self):
        path=self.root/'docs/result.md'
        path.write_text(path.read_text().replace('computed','invented'))
        self.assertTrue(any('differs from fresh regeneration' in e for e in self.check()))
        self.hit['line']=99
        self.assertTrue(any('outside' in e for e in self.check()))


if __name__ == '__main__':
    unittest.main()
