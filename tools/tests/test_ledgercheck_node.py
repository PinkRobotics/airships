"""Missing Node must be one dependency refusal, before any prose comparisons."""
import os
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
MESSAGE = 'ledgercheck: node is missing from PATH; install Node to run this gate.'
sys.path.insert(0, str(ROOT / 'tools'))
import check_float_ledger as gate


class ExactArchivalResearch(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.archive = self.root / 'research/archive'
        self.archive.mkdir(parents=True)
        self.claim = self.archive / 'record.md'
        self.claim.write_text('This archived design floats with a mass of 30 kg.\n')
        raw = self.claim.read_bytes()
        self.manifest = {'schema': 'public-research-manifest-v2', 'files': [{
            'path': 'record.md', 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}]}
        self.policy_path = self.root / gate.ARCHIVAL_POLICY
        self.policy_path.parent.mkdir(parents=True)
        self.policy = {'schema': 'exact-archival-research-v1', 'root': 'research/archive',
                       'source_r21_manifest_sha256': '1' * 64,
                       'reason': 'Frozen archival evidence; not a current vehicle endorsement.'}
        self.write_fixture_pins()
        self.ledger = json.loads((ROOT / 'research/analysis/float-ledger.json').read_text())

    def write_fixture_pins(self):
        raw = json.dumps(self.manifest).encode()
        (self.archive / 'MANIFEST.json').write_bytes(raw)
        self.policy['manifest'] = {'path': 'research/archive/MANIFEST.json', 'bytes': len(raw),
                                   'sha256': hashlib.sha256(raw).hexdigest(),
                                   'entries': len(self.manifest['files'])}
        self.policy_path.write_text(json.dumps(self.policy))

    def inventory(self, paths):
        with patch.object(gate, 'ROOT', self.root), patch.object(gate, 'paths', return_value=paths), \
                patch.object(gate, 'catalog_values', return_value={}), \
                patch.object(gate, 'generated_inventory', return_value=[]):
            return gate.inventory(self.ledger)

    def test_exact_hit_is_inventoried_as_archival(self):
        hits = self.inventory([self.claim])
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]['status'], 'ALLOW')
        self.assertEqual(hits[0]['disposition'], 'archival-research')
        self.assertIn('30 kg', hits[0]['sentence'])
        self.assertEqual(hits[0]['archivalSha256'], self.manifest['files'][0]['sha256'])

    def test_changed_byte_fails_even_without_a_new_claim(self):
        self.claim.write_bytes(self.claim.read_bytes() + b'\n')
        with self.assertRaisesRegex(ValueError, 'file identity mismatch'):
            self.inventory([self.claim])

    def test_new_claim_inside_or_outside_archive_has_no_allowance(self):
        added = self.archive / 'new.md'
        outside = self.root / 'outside.md'
        for path in (added, outside):
            path.write_bytes(self.claim.read_bytes())
        hits = self.inventory([self.claim, added, outside])
        self.assertEqual([h['status'] for h in hits], ['ALLOW', 'FAIL', 'FAIL'])

    def test_changed_manifest_cannot_accept_changed_working_bytes(self):
        self.claim.write_text('This design floats with a mass of 99 kg.\n')
        self.manifest['files'][0]['sha256'] = hashlib.sha256(self.claim.read_bytes()).hexdigest()
        (self.archive / 'MANIFEST.json').write_text(json.dumps(self.manifest))
        with self.assertRaisesRegex(ValueError, 'manifest identity mismatch'):
            self.inventory([self.claim])

    def test_missing_file_and_invalid_policy_fail_closed(self):
        self.claim.unlink()
        with self.assertRaises(OSError):
            self.inventory([])
        self.policy_path.write_text('{}')
        with self.assertRaisesRegex(ValueError, 'invalid archival policy'):
            self.inventory([])

    def test_duplicate_escape_and_missing_hash_entries_fail_closed(self):
        original = json.loads(json.dumps(self.manifest))
        for mutation in ('duplicate', 'escape', 'missing_hash'):
            self.manifest = json.loads(json.dumps(original))
            if mutation == 'duplicate':
                self.manifest['files'].append(dict(self.manifest['files'][0]))
            elif mutation == 'escape':
                self.manifest['files'][0]['path'] = '../record.md'
            else:
                del self.manifest['files'][0]['sha256']
            self.write_fixture_pins()
            with self.assertRaises(ValueError):
                self.inventory([self.claim])


class MissingNode(unittest.TestCase):
    maxDiff = None

    def test_script_refuses_before_inventory(self):
        with tempfile.TemporaryDirectory() as empty:
            # Keep repository inventory available while removing only the Node dependency.
            (Path(empty) / 'git').symlink_to(shutil.which('git'))
            result = subprocess.run(
                [sys.executable, 'tools/check_float_ledger.py'], cwd=ROOT,
                env=dict(os.environ, PATH=empty), capture_output=True, text=True, timeout=60)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(result.stdout, '')
        self.assertEqual(result.stderr.strip(), MESSAGE)

    def test_make_reports_the_same_single_dependency_failure(self):
        make = shutil.which('make')
        self.assertIsNotNone(make)
        with tempfile.TemporaryDirectory() as empty:
            # Keep repository inventory available while removing only the Node dependency.
            (Path(empty) / 'git').symlink_to(shutil.which('git'))
            result = subprocess.run(
                [make, '--no-print-directory', 'ledgercheck', 'PY=' + sys.executable], cwd=ROOT,
                env=dict(os.environ, PATH=empty), capture_output=True, text=True, timeout=60)
        self.assertNotEqual(result.returncode, 0)
        text = result.stdout + result.stderr
        self.assertEqual(text.count(MESSAGE), 1)
        self.assertNotIn('inventoried blocks', text)
        self.assertNotIn('Traceback', text)


if __name__ == '__main__':
    unittest.main()
