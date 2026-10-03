"""The sole record writer requires an explicit live-text hash replacement."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from update_float_records import retire_reviewed


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


if __name__ == '__main__':
    unittest.main()
