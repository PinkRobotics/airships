"""Notice gate contracts and red/restored proofs on a disposable repository copy."""
from __future__ import annotations

import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import noticecheck
import noticegen
import publish


class NoticeContracts(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='notice-contract-')
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        self.rel = 'research/papers/example.pdf'
        self.file = self.root / self.rel
        self.file.parent.mkdir(parents=True)
        self.file.write_bytes(b'%PDF-1.4\nsynthetic test work\n')
        self.record = pathlib.Path(str(self.file) + '.prov.json')
        self.rec = dict(file='example.pdf', source='https://example.org/work', publisher='Fixture publisher',
                        licence='Fixture permission', licenceUrl='https://example.org/terms',
                        licenceStatement='Fixture reproduction permitted with credit.',
                        licenceEvidence='Synthetic fixture, not a real licence.', licenceReason='Test fixture',
                        attribution='Credit: Fixture publisher', notes='Synthetic bytes, unmodified',
                        decision='redistributed', sha256=hashlib.sha256(self.file.read_bytes()).hexdigest())
        self.save()
        (self.root / 'data').mkdir()
        (self.root / 'LICENSE').write_text('Fixture code licence\n')
        (self.root / 'dist.manifest').write_text('\n'.join('served ' + n for n in
                                                          (*noticecheck.REQUIRED, 'index.html', 'data', 'media')))
        (self.root / 'index.html').write_text(noticecheck.map_credit([]) +
                                            '<footer><a href="notices.html">Notices</a></footer>')
        self.generate()
        self.assertEqual(noticecheck.check(self.root), [])

    def save(self):
        self.record.write_text(json.dumps(self.rec))

    def generate(self):
        recs, errors = noticecheck.records(self.root)
        self.assertEqual(errors, [])
        for name, content in noticegen.outputs(recs).items():
            (self.root / name).write_text(content)

    def assert_error(self, part, **kwargs):
        errors = noticecheck.check(self.root, **kwargs)
        self.assertTrue(any(part in e for e in errors), errors)

    def test_every_named_output_is_verified(self):
        child = self.file.with_name('second.pdf')
        child.write_bytes(b'%PDF-1.4\nsecond synthetic work\n')
        self.rec['outputs'] = [dict(file=p.name, bytes=p.stat().st_size,
                                   sha256=hashlib.sha256(p.read_bytes()).hexdigest())
                               for p in (self.file, child)]
        self.save()
        self.generate()
        self.assertEqual(noticecheck.check(self.root), [])
        original = child.read_bytes()
        child.write_bytes(original.replace(b'second', b'edited'))
        self.assert_error('second.pdf: hash mismatch')
        child.write_bytes(original)
        child.unlink()
        self.assert_error('redistributed file missing: research/papers/second.pdf')
        child.write_bytes(original)
        for bad in ('../second.pdf', '/second.pdf', 'second.pdf/../other.pdf'):
            with self.subTest(path=bad):
                self.rec['outputs'][1]['file'] = bad
                self.save()
                self.assert_error('invalid output')
        self.rec['outputs'][1]['file'] = 'second.pdf'
        self.rec['outputs'].append(dict(self.rec['outputs'][1]))
        self.save()
        self.assert_error('duplicate output')

    def test_missing_decision_and_invalid_decision(self):
        for value in (None, [], 'yes'):
            with self.subTest(value=value):
                self.rec['decision'] = value
                self.save()
                self.assert_error('missing or invalid decision')

    def test_missing_sidecar(self):
        self.record.unlink()
        self.assert_error('unrecorded third-party file: ' + self.rel)

    def test_missing_redistributed_file(self):
        self.file.unlink()
        self.assert_error('redistributed file missing: ' + self.rel)

    def test_every_notice_is_read(self):
        for name in ('NOTICE', 'DATA-SOURCES.md', 'notices.html'):
            with self.subTest(name=name):
                p = self.root / name
                original = p.read_bytes()
                p.write_bytes(original.replace(b'Fixture permission', b'Fixture permissioN', 1))
                self.assert_error(name + ' differs from fresh generation')
                p.write_bytes(original)
                self.assertEqual(noticecheck.check(self.root), [])

    def test_fake_notice_row(self):
        with (self.root / 'NOTICE').open('a') as stream:
            stream.write('\n| research/papers/nonexistent.pdf | Fake credit |\n')
        self.assert_error('NOTICE differs from fresh generation')

    def test_both_corrupt_record_hash_and_asset_bytes(self):
        self.rec['sha256'] = '0' * 64
        self.save()
        self.assert_error('hash mismatch')
        self.rec['sha256'] = hashlib.sha256(self.file.read_bytes()).hexdigest()
        self.save()
        self.file.write_bytes(b'changed asset')
        self.assert_error('hash mismatch')

    def test_public_rejects_every_excluded_kind_and_allows_absent_originals(self):
        for decision in ('link-only', 'withheld', 'to-confirm'):
            with self.subTest(decision=decision):
                self.rec['decision'] = decision
                self.save()
                self.generate()
                self.assertEqual(noticecheck.check(self.root), [])
                self.assert_error('public tree contains ' + decision, public=True)
                original = self.file.read_bytes()
                self.file.unlink()
                self.assertEqual(noticecheck.check(self.root, public=True), [])
                self.file.write_bytes(original)

    def test_excluded_record_still_requires_hash(self):
        self.rec['decision'] = 'link-only'
        self.rec.pop('sha256')
        self.save()
        self.file.unlink()
        self.assert_error('missing or invalid sha256')

    def test_only_exact_project_paths_are_exempt(self):
        self.assertTrue(all(noticecheck.FIRST_PARTY.values()))
        for rel in noticecheck.FIRST_PARTY:
            with self.subTest(rel=rel):
                self.assertFalse(noticecheck.third_party(rel))
        for rel in ('research/papers/new/README.md', 'media/new.jpg', 'data/new.json',
                    'research/prior/new.md', 'research/papers/nested/NEW.PDF', 'assets/font.WOFF2',
                    'app/vendor/lib.js'):
            with self.subTest(rel=rel):
                p = self.root / rel
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(b'new third party file')
                self.assert_error('unrecorded third-party file: ' + rel)
                p.unlink()

    def test_tracked_deleted_file_is_not_silently_lost(self):
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        subprocess.run(['git', '-C', str(self.root), 'add', self.rel], check=True)
        self.file.unlink()
        self.record.unlink()
        self.assert_error('unrecorded third-party file: ' + self.rel)

    def test_malformed_json_and_nonobject(self):
        for content in ('{', '[]', 'null'):
            with self.subTest(content=content):
                self.record.write_text(content)
                self.assertTrue(noticecheck.check(self.root))

    def test_duplicate_decision_keys_are_not_one_decision(self):
        self.record.write_text(json.dumps(self.rec)[:-1] + ', "decision": "redistributed"}')
        self.assert_error('invalid record')

    def test_path_escape_duplicate_record_and_symlink(self):
        self.rec['file'] = '../../outside.pdf'
        self.save()
        self.assert_error('invalid file path')
        self.rec['file'] = 'example.pdf'
        self.save()
        other = self.record.with_name('duplicate.prov.json')
        shutil.copyfile(self.record, other)
        self.assert_error('duplicate records')
        other.unlink()
        self.file.unlink()
        self.file.symlink_to('example.pdf.prov.json')
        self.assert_error('symlink asset refused')

    def test_boolean_compatibility_must_agree(self):
        self.rec['redistributed'] = False
        self.save()
        self.assert_error('compatibility field disagrees')

    def test_measurements_are_computed_not_trusted(self):
        p = self.root / 'data/roads-bc.json'
        p.write_text('[[[1,2],[3,4]],[[5,6],[7,8],[9,10]]]')
        rec = dict(self.rec, file='roads-bc.json', sha256=hashlib.sha256(p.read_bytes()).hexdigest(),
                   measurements={'bytes': p.stat().st_size, 'polylines': 2, 'vertices': 5})
        sidecar = p.with_suffix('.prov.json')
        sidecar.write_text(json.dumps(rec))
        self.generate()
        (self.root / 'index.html').write_text(noticecheck.map_credit(noticecheck.records(self.root)[0]))
        self.assertEqual(noticecheck.check(self.root), [])
        rec['measurements']['vertices'] = 4
        sidecar.write_text(json.dumps(rec))
        self.assert_error('measurements differ from file')

    def test_service_exception_is_narrow(self):
        rec = dict(self.rec, file='live/wind.json', kind='service', decision='link-only', sha256=None)
        p = self.root / 'data/wind.prov.json'
        p.write_text(json.dumps(rec))
        self.assertEqual(noticecheck.records(self.root)[1], [])
        target = self.root / 'data/live/wind.json'
        target.parent.mkdir()
        target.write_text('{}')
        self.assert_error('service record must have null hash and no bundled file')
        target.unlink()
        rec['file'] = 'anything.pdf'
        p.write_text(json.dumps(rec))
        self.assert_error('unsupported kind or service identity')

    def test_write_never_updates_index_or_repairs_a_bad_hash(self):
        index = (self.root / 'index.html').read_bytes()
        cmd = [sys.executable, str(ROOT / 'tools/noticecheck.py'), '--root', str(self.root), '--write']
        self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
        self.assertEqual(index, (self.root / 'index.html').read_bytes())
        before = (self.root / 'NOTICE').read_bytes()
        self.rec['sha256'] = '0' * 64
        self.save()
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('hash mismatch', result.stdout)
        self.assertEqual(before, (self.root / 'NOTICE').read_bytes())


class RepositoryMutationProofs(unittest.TestCase):
    def test_requested_mutations_red_then_restored(self):
        with tempfile.TemporaryDirectory(prefix='notice-repository-') as temp:
            source, dest = pathlib.Path(temp) / 'source', pathlib.Path(temp) / 'dest'
            source.mkdir()
            dest.mkdir()
            for name in (*noticecheck.REQUIRED, 'index.html', 'dist.manifest'):
                shutil.copy2(ROOT / name, source / name)
            for folder in noticecheck.FOLDERS:
                shutil.copytree(ROOT / folder, source / folder)
            served, _, partial = publish.read_manifest()
            for src, rel in publish.wanted_files(served, partial):
                target = dest / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, target)
            self.assertEqual(noticecheck.check(source, dest), [])

            def mutate(path, content, expected, label, public=False):
                before = path.read_bytes() if path.exists() else None
                try:
                    if content is None:
                        path.unlink()
                    else:
                        path.write_bytes(content)
                    cmd = [sys.executable, str(ROOT / 'tools/noticecheck.py'), '--root', str(source), '--dest', str(dest)]
                    if public:
                        cmd.append('--public')
                    result = subprocess.run(cmd, capture_output=True, text=True)
                    self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
                    self.assertIn(expected, result.stdout)
                    relevant = next(line for line in result.stdout.splitlines() if expected in line)
                    print(f'{label}: RED exit=1; {relevant}')
                finally:
                    if before is None:
                        path.unlink(missing_ok=True)
                    else:
                        path.write_bytes(before)
                self.assertEqual(noticecheck.check(source, dest), [])
                print(f'{label}: restored PASS')

            paper = 'research/papers/akhmeteli-gavrilin-2021-vacuum-balloon.pdf'
            record = source / (paper + '.prov.json')
            mutate(record, None, 'unrecorded third-party file: ' + paper, 'delete paper sidecar')
            notice = source / 'NOTICE'
            row = next(line for line in notice.read_bytes().splitlines(keepends=True)
                       if line.startswith(b'| ' + paper.encode() + b' |'))
            mutate(notice, notice.read_bytes().replace(row, b'', 1), 'NOTICE differs', 'delete paper NOTICE row')
            data = source / 'DATA-SOURCES.md'
            mutate(data, data.read_bytes().replace(b'Open Government Licence - British Columbia',
                                                   b'Open Government LicencE - British Columbia', 1),
                   'DATA-SOURCES.md differs', 'change one licence character')
            mutate(source / 'research/papers/unlisted.pdf', b'%PDF fixture',
                   'unrecorded third-party file: research/papers/unlisted.pdf', 'add unlisted PDF')
            rec = json.loads(record.read_text())
            rec['sha256'] = '0' * 64
            mutate(record, json.dumps(rec).encode(), 'hash mismatch', 'corrupt one hash')
            mutate(record, record.read_bytes(), 'public tree contains link-only file: research/papers/',
                   'public gate with link-only originals present', public=True)
            index = dest / 'index.html'
            mutate(index, index.read_bytes() + b'<a href="missing-target.html">broken</a>',
                   'broken relative link', 'broken published link')
            page = dest / 'notices.html'
            mutate(page, page.read_bytes() + b'\nmanual edit\n', 'published notices.html differs', 'edit served notice')
            mutate(dest / 'NOTICE', None, 'published output missing: NOTICE', 'missing served NOTICE')
            for r in noticecheck.records(source)[0]:
                if r['decision'] != 'redistributed':
                    (source / r['path']).unlink(missing_ok=True)
            self.assertEqual(noticecheck.check(source, public=True), [])
            print('public gate after excluded originals removed from disposable copy: PASS')


if __name__ == '__main__':
    unittest.main()
