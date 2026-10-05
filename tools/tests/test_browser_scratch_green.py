"""An interrupted browser run must not change checks or publication selection."""
from contextlib import redirect_stderr
import io
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
import browser_scratch
import publish


class BrowserScratchTests(unittest.TestCase):
    def test_distinct_runs_restore_environment_and_clean_up(self):
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, {"TMPDIR": td}):
            root = Path(td)
            before = {key: os.environ.get(key) for key in ('TMPDIR', 'AIRSHIPS_TMPDIR')}
            with patch.object(browser_scratch, 'ROOT', root), \
                    patch.object(browser_scratch, '_readable', return_value=True):
                with browser_scratch.browser_scratch() as outer:
                    self.assertEqual(Path(outer).parent, root)
                    with browser_scratch.browser_scratch() as inner:
                        self.assertNotEqual(outer, inner)
                        self.assertEqual(Path(inner).parent, Path(outer))
                        self.assertEqual(os.environ['AIRSHIPS_TMPDIR'], inner)
                    self.assertFalse(Path(inner).exists())
                    self.assertEqual(os.environ['TMPDIR'], outer)
                self.assertFalse(Path(outer).exists())
            self.assertEqual(before, {key: os.environ.get(key) for key in before})

    def test_without_explicit_scratch_uses_checkout(self):
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ):
            os.environ.pop('TMPDIR', None)
            with patch.object(browser_scratch, 'ROOT', Path(td)), \
                    patch.object(browser_scratch, '_readable', return_value=True):
                with browser_scratch.browser_scratch() as name:
                    self.assertEqual(Path(name).parent, Path(td) / '.browser-scratch')
                self.assertFalse(Path(name).exists())

    def test_explicit_unreadable_scratch_does_not_fall_back(self):
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, {'TMPDIR': td}):
            with patch.object(browser_scratch, '_readable', return_value=False) as probe:
                with self.assertRaisesRegex(RuntimeError, 'explicit TMPDIR'):
                    with browser_scratch.browser_scratch():
                        self.fail('unreadable scratch was accepted')
                self.assertEqual(probe.call_count, 1)
                self.assertEqual(list(Path(td).iterdir()), [])

    def test_failed_probe_prints_the_browsers_own_stderr(self):
        with tempfile.TemporaryDirectory() as td:
            browser = Path(td) / 'chromium'
            browser.write_text('#!/bin/sh\necho "the browser says why" >&2\nexit 7\n')
            browser.chmod(0o755)
            scratch = Path(td) / 'scratch'
            scratch.mkdir()
            printed = io.StringIO()
            with redirect_stderr(printed):
                self.assertFalse(browser_scratch._readable(scratch, str(browser)))
            self.assertIn('exited with code 7', printed.getvalue())
            self.assertIn('the browser says why', printed.getvalue())

    def test_leftover_does_not_change_gates_stamps_status_or_published_copy(self):
        commands = [
            [sys.executable, 'tools/stamp_site.py', '--check'],
            [sys.executable, '3d/scripts/stamp-version.py', '--check'],
            [sys.executable, 'tools/check_boundaries.py'],
            [sys.executable, 'tests/firstparty/static.py'],
        ]
        if shutil.which('node'):
            commands.append(['node', '3d/scripts/stamp-version.mjs', '--check'])

        def execute(command):
            result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            return result.stdout, result.stderr

        def status():
            return subprocess.check_output(['git', 'status', '--porcelain'], cwd=ROOT)

        stamps = {p: (ROOT / p).read_bytes() for p in ('sim/version.json', '3d/version.json')}
        scratch = ROOT / '.browser-scratch'
        scratch.mkdir(exist_ok=True)
        served, excluded, partial = publish.read_manifest()
        self.assertIn(scratch.name, excluded)
        self.assertNotIn(scratch.name, served)
        before_files = [(src, rel) for src, rel in publish.wanted_files(served, partial)]
        before_status = status()
        with tempfile.TemporaryDirectory() as td:
            dest = Path(td) / 'published'
            dest.mkdir()
            # Copy only to disposable scratch. Never invoke the publishing write path.
            for src, rel in before_files:
                (dest / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(src, dest / rel)
            commands += [[sys.executable, 'tools/publish.py', '--check', '--dest', str(dest)],
                         [sys.executable, 'tools/noticecheck.py', '--dest', str(dest)]]
            before = [execute(command) for command in commands]
            with tempfile.TemporaryDirectory(prefix='leftover-', dir=scratch) as name:
                probe = Path(name) / 'probe.html'
                probe.write_text('<script type="module">\n'
                                 'import "../../sim/config.js?v=leftover";\n'
                                 'import "../../3d/index.js?v=leftover";\n'
                                 'fetch("https://scratch.invalid/probe");\n</script>')
                execute(['git', 'check-ignore', str(probe.relative_to(ROOT))])
                after = [execute(command) for command in commands]
                self.assertEqual(after, before)
                self.assertEqual(status(), before_status)
                self.assertEqual(list(publish.wanted_files(served, partial)), before_files)
                self.assertFalse(any(scratch.name in rel.parts for _, rel in before_files))
                self.assertEqual(stamps, {p: (ROOT / p).read_bytes() for p in stamps})
                for command, (out, err) in zip(commands, after):
                    print('scratch unchanged:', ' '.join(command[:2]))
                    print((out + err).strip())
            # Classification remains strict for every name except the explicit exclusions.
            with tempfile.TemporaryDirectory(prefix='unclassified-', dir=ROOT) as name:
                self.assertIn(Path(name).name, publish.check_complete(served, excluded))
        self.assertEqual(status(), before_status)


if __name__ == '__main__':
    unittest.main()
