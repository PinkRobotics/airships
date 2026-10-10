"""Offline restoration preserves history and never replaces local gate inputs."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import restore_claims


class RestoreClaimsTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.directory = self.root / 'research/claims'
        self.directory.mkdir(parents=True)
        self.originals = {name: json.dumps({'historical': name}).encode()
                          for name in restore_claims.OUTPUTS}
        self.git('init', '-q')
        for name, data in self.originals.items():
            (self.directory / name).write_bytes(data)
        self.git('add', 'research')
        tree = self.git('write-tree')
        commit = self.git('-c', 'user.name=Fixture', '-c', 'user.email=fixture@example.invalid',
                          'commit-tree', tree, '-m', 'Disposable restoration fixture')
        self.source = {'version': 1, 'commit': commit,
                       'files': {name: {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}
                                 for name, data in self.originals.items()}}
        self.save_source()
        for name in self.originals:
            (self.directory / name).unlink()

    def git(self, *args):
        return subprocess.check_output(['git', '-C', str(self.root), *args]).decode().strip()

    def save_source(self):
        (self.directory / 'restore-source.json').write_text(json.dumps(self.source))

    def test_missing_records_restore_exact_history_and_second_run_preserves_edits(self):
        restore_claims.restore(self.root)
        for name, data in self.originals.items():
            self.assertEqual((self.directory / name).read_bytes(), data)
        path = self.directory / 'accepted-defects.json'
        path.write_bytes(b'locally changed acceptance history')
        restore_claims.restore(self.root)
        self.assertEqual(path.read_bytes(), b'locally changed acceptance history')

    def test_bad_hash_writes_no_record(self):
        self.source['files']['accepted-defects.json']['sha256'] = '0' * 64
        self.save_source()
        with self.assertRaisesRegex(ValueError, 'hash mismatch'):
            restore_claims.restore(self.root)
        self.assertTrue(all(not (self.directory / n).exists() for n in self.originals))

    def test_unavailable_commit_fails_without_reset(self):
        self.source['commit'] = '0' * 40
        self.save_source()
        with self.assertRaisesRegex(ValueError, 'pinned source unavailable'):
            restore_claims.restore(self.root)
        self.assertTrue(all(not (self.directory / n).exists() for n in self.originals))

    def test_symlink_rejected_without_touching_external_file(self):
        outside = self.root / 'external'
        outside.write_bytes(b'unchanged')
        (self.directory / 'register.json').symlink_to(outside)
        with self.assertRaisesRegex(ValueError, 'symlink'):
            restore_claims.restore(self.root)
        self.assertEqual(outside.read_bytes(), b'unchanged')

    def test_partial_local_records_remain_untouched(self):
        path = self.directory / 'carry-history.json'
        path.write_bytes(b'local history')
        restore_claims.restore(self.root)
        self.assertEqual(path.read_bytes(), b'local history')
        self.assertEqual((self.directory / 'register.json').read_bytes(), self.originals['register.json'])


if __name__ == '__main__':
    unittest.main()
