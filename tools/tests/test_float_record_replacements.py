"""The sole record writer requires an explicit live-text hash replacement."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from update_float_records import retire_reviewed, dated_disposition


class Replacements(unittest.TestCase):
    def fixture(self):
        shards = {'record': {'entries': [{'file': 'page.html', 'key': 'old', 'class': 'bound'}]}}
        catalogue = {'entries': [{'file': 'page.html', 'key': 'new'}], 'replacements': [
            {'file': 'page.html', 'oldKey': 'old', 'newKey': 'new',
             'reason': 'Reviewed live-text correction.'}]}
        return shards, {('page.html', 'new'): {}}, catalogue

    def test_replacement_is_explicit_and_second_run_changes_nothing(self):
        shards, hits, catalogue = self.fixture()
        self.assertEqual(retire_reviewed(shards, hits, catalogue), 1)
        snapshot = copy.deepcopy(shards)
        self.assertEqual(retire_reviewed(shards, hits, catalogue), 0)
        self.assertEqual(shards, snapshot)

    def test_unknown_new_hash_or_absent_new_text_is_refused(self):
        for absent in ('review', 'text'):
            shards, hits, catalogue = self.fixture()
            if absent == 'review':
                catalogue['entries'] = []
            else:
                hits = {}
            with self.assertRaises(SystemExit):
                retire_reviewed(shards, hits, catalogue)
            self.assertEqual(len(shards['record']['entries']), 1)

    def test_frozen_history_is_refused(self):
        shards, hits, catalogue = self.fixture()
        shards['record']['entries'][0]['class'] = 'history'
        with self.assertRaises(SystemExit):
            retire_reviewed(shards, hits, catalogue)

    def test_missing_review_never_retires_a_block(self):
        shards, hits, catalogue = self.fixture()
        catalogue['replacements'] = []
        self.assertEqual(retire_reviewed(shards, hits, catalogue), 0)
        self.assertEqual(len(shards['record']['entries']), 1)



class DatedDecisions(unittest.TestCase):
    def hit(self, text):
        from float_claims import key_of
        return dict(file='docs/audit/26-10-03-example.md', key=key_of(text), line=7, sentence=text)

    def test_new_verdicts_require_the_shared_explicit_catalogue(self):
        for text in ('The drawn hull floats.', 'The drawn hull stays aloft.',
                     'The track climbs the ridge.', 'The hull is positively buoyant.',
                     'The hull is floating.'):
            hit = self.hit(text)
            key = (hit['file'], hit['key'])
            with self.subTest(text=text), self.assertRaisesRegex(SystemExit, 'New dated verdict needs review'):
                dated_disposition(hit, {}, {})
            review = dict(file=hit['file'], key=hit['key'], **{'class': 'history'},
                date='2026-10-03', reason='Reviewed historical assertion retained as evidence, not a current result.')
            result = dated_disposition(hit, {}, {key: review})
            self.assertEqual(result, dict(review, line=7))
            self.assertEqual(dated_disposition(hit, {key: result}, {}), result)

    def test_nonverdict_freeze_and_existing_decision_are_retained(self):
        hit = self.hit('This is an audit of the working notes.')
        entry = dated_disposition(hit, {}, {})
        self.assertEqual(entry['class'], 'history')
        entry['reason'] = 'An existing explicit review must survive a plain refresh.'
        self.assertEqual(dated_disposition(hit, {(hit['file'],hit['key']):entry}, {})['reason'], entry['reason'])

    def test_provenance_destinations_are_not_verdicts_but_labels_are(self):
        hit = self.hit('Dated record: 2026-10-03; historical, not a current result. '
                       'See [the float ledger](../FLOAT-LEDGER.md).')
        self.assertEqual(dated_disposition(hit, {}, {})['class'], 'history')
        hit = self.hit('See [the hull floats](../FLOAT-LEDGER.md).')
        with self.assertRaisesRegex(SystemExit, 'New dated verdict needs review'):
            dated_disposition(hit, {}, {})

    def test_bad_decision_never_freezes_new_verdict(self):
        hit = self.hit('The hull ascends.')
        base = dict(file=hit['file'], key=hit['key'], **{'class':'history'},
                    date='2026-10-03', reason='Explicit review of this historical block.')
        for field, value in (('class','conditional'), ('date','2026-10-02'), ('reason','')):
            with self.subTest(field=field), self.assertRaisesRegex(SystemExit, 'Dated decision requires'):
                dated_disposition(hit, {}, {(hit['file'],hit['key']):dict(base, **{field:value})})

if __name__ == '__main__':
    unittest.main()
