"""Lossless records, producer round trips and unchanged-file writes."""
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))
import record_energy_fix as solar


class SolarRecord(unittest.TestCase):
    def test_producer_compact_round_trip(self):
        with tempfile.TemporaryDirectory() as td:
            before, after = [Path(td) / name for name in ('before', 'after')]
            for root, value in ((before, 1.25), (after, 2.5)):
                (root / 'research/analysis').mkdir(parents=True)
                (root / 'tests/energy').mkdir(parents=True)
                (root / 'tests/energy/unheld.mjs').write_text('// unheldT-1.0\n')
                (root / 'research/analysis/energy-example.json').write_text(
                    json.dumps({'a@b%': value, 'text': 'case ' + str(value),
                                'flag': value > 2, 'added': 3 if value > 2 else None}))
            argv = ['record_energy_fix.py', '--part', 'SOLAR', '--before', str(before)]
            with patch.object(solar, 'ROOT', after), patch.object(sys, 'argv', argv):
                solar.main()
                path = after / 'research/analysis/solar-input-changes.json'
                first = path.read_bytes(), path.stat().st_mtime_ns
                solar.main()
            compact = json.loads(first[0])
            self.assertEqual(compact.get('format'), 'compact-solar-v1')
            expanded = solar.expand_solar_record(compact)
            rel = 'research/analysis/energy-example.json'
            self.assertEqual(expanded['changes'], [dict(file=rel, field='a%40b%25', old=1.25, new=2.5, decimals=3)])
            self.assertEqual(expanded['textAndFlagChanges'], [dict(file=rel, field='flag', old=False, new=True),
                dict(file=rel, field='text', old='case 1.25', new='case 2.5')])
            self.assertEqual(expanded['addedOrRemovedNumericFields'], [dict(file=rel, field='added', old=None, new=3)])
            self.assertEqual(first, (path.read_bytes(), path.stat().st_mtime_ns))

    def test_front_codes_preserve_order_and_metadata(self):
        old = dict(reason='kept', comparison='kept', fieldEncoding='kept',
                   changes=[dict(file=f, field=p, old=0.0, new=-0.0, decimals=6)
                            for f, p in [('a', 'xyz'), ('b', 'xyz'), ('a', 'xyq')]],
                   textAndFlagChanges=[], addedOrRemovedNumericFields=[])
        self.assertEqual(solar.expand_solar_record(solar.compact_solar_record(old)), old)

    def test_unknown_and_corrupt_forms_refused(self):
        with self.assertRaises(ValueError):
            solar.compact_solar_record({'unknown': []})



class CarryRecord(unittest.TestCase):
    def test_changed_fields_only_and_idempotence(self):
        import claims
        before = dict(id='a', text='kept', gate='old', owner={'kind': 'old'}, placement=[1])
        after = dict(before, gate='new', owner={'kind': 'new'})
        run = dict(files={'a': {'then': 1, 'now': 1}}, headlines={}, retired=[], added=['b'],
                   revalidated=[dict(id='a', before=before, after=after)], defect_changes={'a': {'before': 'x', 'after': None}})
        compact = claims.compact_carry_run(run)
        self.assertEqual(compact['revalidated'], [dict(id='a', changed={'gate': ['old', 'new'],
                                                                     'owner': [{'kind': 'old'}, {'kind': 'new'}]})])
        for key in ('files', 'headlines', 'retired', 'added', 'defect_changes'):
            self.assertEqual(run[key], compact[key])
        self.assertEqual(claims.compact_carry_run(compact), compact)
        typed = dict(run, revalidated=[dict(id='a', before=dict(id='a', flag=False, precision=1, sign=0.0),
            after=dict(id='a', flag=0, precision=1.0, sign=-0.0))])
        self.assertEqual(set(claims.compact_carry_run(typed)['revalidated'][0]['changed']),
                         {'flag', 'precision', 'sign'})

    def test_invalid_form_refused(self):
        import claims
        with self.assertRaises(ValueError):
            claims.compact_carry_run({'revalidated': []})



from test_claims import ClaimsFixture


class CarryProducer(ClaimsFixture, unittest.TestCase):
    def test_carry_writes_compact_entries_and_skips_unchanged(self):
        import claims
        import contextlib
        import io
        self.known()
        self.check(True)
        register_path = self.root/'research/claims/register.json'
        register = claims.read_json(register_path)
        register['entries'][0]['gate'] = 'former-gate'
        claims.write_json(register_path, register)
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(claims.carry(self.root, self.root/'dist.manifest',
                self.root/'research/figures.json', self.root/'research/claims/register.json'), 0)
        path = self.root/'research/claims/carry-history.json'
        row = claims.read_json(path)['runs'][-1]['revalidated'][0]
        self.assertEqual(set(row), {'id', 'changed'})
        first = {p.name: (p.read_bytes(), p.stat().st_mtime_ns)
                 for p in (self.root/'research/claims').iterdir() if p.is_file()}
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(claims.carry(self.root, self.root/'dist.manifest',
                self.root/'research/figures.json', self.root/'research/claims/register.json'), 0)
        self.assertEqual(first, {p.name: (p.read_bytes(), p.stat().st_mtime_ns)
                 for p in (self.root/'research/claims').iterdir() if p.is_file()})


if __name__ == '__main__':
    unittest.main()
