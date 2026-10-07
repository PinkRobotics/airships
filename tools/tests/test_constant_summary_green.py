"""Counterfactual summary controls; included in the existing ciparity target."""
import copy
import importlib.util
import math
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location('constant_study', ROOT / 'research/validation/constant_study.py')
study = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(study)


def row(field, old, new):
    numeric = type(old) in (int, float) and type(new) in (int, float)
    return dict(file='a.json', field=field, published_old=old, old=old, new=new,
                difference=new-old if numeric else None)


def result(rows):
    return dict(old_R_air={'JS': 287.0528, 'Python': 287.05}, standard_R_air=287.053,
                standard_definition='8314.32 J/(kmol K) / 28.9644 kg/kmol',
                source_basis='Current working files; base_commit names HEAD, not the uncommitted candidate tree.', commands=[], outputs=['a.json', 'unchanged.json'],
                changed_fields=rows, baseline_regeneration_drift=[{}])


class SummaryWriter(unittest.TestCase):
    def render(self, rows):
        value = result(rows)
        before = copy.deepcopy(value)
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'study.json'
            study.write_study(value, out)
            first = out.read_bytes()
            study.write_study(value, out)
            self.assertEqual(out.read_bytes(), first)
            self.assertEqual(value, before)
            return out.with_suffix('.md').read_text()

    def test_counts_bands_order_and_special_rows(self):
        rows = [row('/tiny', 1.0, math.nextafter(1.0, 2.0)), row('/small', 1.0, 1.00002),
                row('/largest', 2.0, 3.0), row('/middle', 10.0, 11.0),
                row('/text|field', 'old', 'new'), row('/flag', False, True),
                row('/zero', 0.0, 1.0), row('/added', None, 2.0), row('/removed', 2.0, None)]
        md = self.render(rows)
        self.assertIn('9 changed leaves: 5 numeric; 2 text or flag; 1 added; 1 removed.', md)
        self.assertIn('Baseline regeneration drift: 1 leaves.', md)
        self.assertIn('Rounding-scale', md)
        self.assertIn('| [1e-16, 1e-15) | 1 |', md)
        self.assertIn('| [1e-5, 1e-4) | 1 |', md)
        self.assertLess(md.index('| a.json | /largest |'), md.index('| a.json | /middle |'))
        self.assertIn('/text\\|field', md)
        self.assertIn('| a.json | /zero | 0.0 | 0.0 | 1.0 | 1.0 | undefined (fresh old zero) |', md)
        self.assertIn('| unchanged.json | 0 |', md)
        self.assertIn('All special rows listed: 5; omitted: 0.', md)

    def test_top_forty_and_threshold_cap(self):
        small = self.render([row(f'/small/{i:03}', 1.0, 1.0 + (i+1)*1e-6) for i in range(60)])
        self.assertIn('Selected numeric rows: 40; listed: 40; omitted by row cap: 20;', small)
        self.assertNotIn('| a.json | /small/000 |', small)
        self.assertIn('| a.json | /small/059 |', small)
        large = self.render([row(f'/large/{i:03}', 1.0, 1.0 + (i+1)*0.01) for i in range(220)])
        self.assertIn('Selected numeric rows: 200; listed: 200; omitted by row cap: 20;', large)
        self.assertIn('220 numeric leaves have magnitude at least 1e-3.', large)
        self.assertLess(len(large.encode()), 40000)

    def test_size_limit_discloses_special_omissions(self):
        md = self.render([row(f'/text/name{i:03}', 'a'*200, 'b'*200) for i in range(100)])
        self.assertLess(len(md.encode()), 40000)
        self.assertRegex(md, r'All special rows listed: \d+; omitted: [1-9]\d*\.')
        self.assertIn('Complete rows remain in constant-study.json', md)

    def test_repeated_records_counts_ids_and_shared_changes(self):
        ids = list(range(21, 32))
        rows = [row(f'/classes/P10000/byFire/{i}/feasible', True, False) for i in ids]
        rows += [row(f'/classes/P10000/byFire/{i}/value', 7, None) for i in ids]
        rows += [row(f'/classes/P10000/byFire/{i}/reason', None, 'bounded') for i in ids]
        rows += [row(f'/ten/{i}/flag', False, True) for i in range(10)]
        rows += [row('/zero', 0.0, 1.0)]
        md = self.render(rows)
        self.assertIn('| Published/generated file | Text or flag | Added | Removed | Fresh old zero | Total |', md)
        self.assertIn('| a.json | 21 | 11 | 11 | 1 | 44 |', md)
        self.assertIn('| a.json | /classes/P10000/byFire/{n}/feasible | text or flag | true → false | 11 | S1 |', md)
        self.assertIn('| a.json | /classes/P10000/byFire/{n}/value | removed | value removed (fresh old: 7) | 11 | S1 |', md)
        self.assertIn('| a.json | /classes/P10000/byFire/{n}/reason | added | value added: "bounded" | 11 | S1 |', md)
        self.assertEqual(md.count('| S1 | 21..31 |'), 1)
        self.assertNotIn('| a.json | /ten/{n}/flag |', md)
        for i in range(10):
            self.assertIn(f'| a.json | /ten/{i}/flag | False | False | True | None | n/a |', md)
        self.assertIn('Collapsed groups: 3; represented leaves: 33; full special rows: 11.', md)
        self.assertIn('All special rows listed: 44; omitted: 0.', md)
        self.assertLess(len(md.encode()), 40000)

    def test_varied_changes_multiple_ids_and_non_digit_segments(self):
        rows = [row(f'/P10000/{i}/rows/{i+20}/flag', False, bool(i % 2)) for i in range(11)]
        rows += [row(f'/same/00{i}/flag', False, True) for i in range(11)]
        md = self.render(rows)
        self.assertIn('| a.json | /P10000/{n}/rows/{n}/flag | text or flag | varies; see changed_fields in JSON | 11 | S1 |', md)
        self.assertIn('| S1 | ' + ', '.join(f'{i}/{i+20}' for i in range(11)) + ' |', md)
        self.assertIn('| S2 | ' + ', '.join(f'00{i}' for i in range(11)) + ' |', md)
        self.assertNotIn('/P{n}', md)

    def test_live_record_is_complete_within_limit(self):
        value = __import__('json').loads((ROOT / 'research/validation/constant-study.json').read_text())
        before = copy.deepcopy(value)
        md = study.summary(value)
        self.assertEqual(value, before)
        from collections import Counter
        rows = value['changed_fields']
        special = [r for r in rows if not (type(r['old']) in (int, float) and
                   type(r['new']) in (int, float)) or r['old'] == 0]
        def kind(r):
            if r['old'] is None: return 'added'
            if r['new'] is None: return 'removed'
            return 'fresh old zero' if type(r['old']) in (int, float) and type(r['new']) in (int, float) else 'text or flag'
        counts = Counter((r['file'], kind(r)) for r in special)
        for filename in sorted({r['file'] for r in special}):
            values = [counts[filename, k] for k in ('text or flag', 'added', 'removed', 'fresh old zero')]
            self.assertIn('| ' + ' | '.join(map(str, [filename, *values, sum(values)])) + ' |', md)
        import re
        match = re.search(r'All special rows listed: (\d+); omitted: (\d+)\.', md)
        self.assertIsNotNone(match)
        self.assertEqual(sum(map(int, match.groups())), len(special))
        self.assertIn('Complete rows remain in constant-study.json', md)
        self.assertEqual(md, (ROOT / 'research/validation/constant-study.md').read_text())
        self.assertLess(len(md.encode()), 40000)
