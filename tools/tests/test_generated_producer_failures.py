"""A failed producer is attempted once per verifier; every dependent check fails."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from claims_rules import Context
from float_regions import Regions


class ProducerFailures(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='producer-errors-', dir=os.environ['TMPDIR'])
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / 'tools').mkdir()
        (self.root / 'docs').mkdir()
        self.start, self.end = '<!-- fixture:start -->', '<!-- fixture:end -->'
        self.body = self.start + '\nGenerated fixture.\n' + self.end + '\n'
        self.files = ['docs/one.md', 'docs/two.md']
        for file in self.files:
            (self.root / file).write_text(self.body)
        (self.root / 'tools/verify.py').write_text('# tools/produce.py emits both files\n')
        (self.root / 'Makefile').write_text('fresh:\n\tpython3 tools/verify.py\n')
        subprocess.run(['git', 'init', '-q'], cwd=self.root, check=True)
        self.producer('success')
        subprocess.run(['git', 'add', '-N', 'tools/produce.py', 'tools/verify.py'], cwd=self.root, check=True)

    def producer(self, behavior):
        output = json.dumps({file: self.body for file in self.files})
        ending = {
            'success': 'print(' + repr(output) + ')\n',
            'exit': 'raise SystemExit(7)\n',
            'json': 'print("not JSON")\n',
        }[behavior]
        (self.root / 'tools/produce.py').write_text(
            'from pathlib import Path\n'
            'p=Path("attempts")\n'
            'p.write_text(str(int(p.read_text())+1 if p.exists() else 1))\n' + ending)

    def attempts(self):
        return int((self.root / 'attempts').read_text())

    def entry(self, file):
        return dict(file=file, generator='tools/produce.py', gate='fresh', verifier='tools/verify.py',
                    region=dict(start=self.start, end=self.end))

    def context_check(self, ctx, file):
        owner = dict(kind='generated', generator='tools/produce.py', region='whole-file')
        with patch.object(ctx, 'generator_owner', return_value=(owner, 'fresh')):
            return ctx.generated_issue(dict(file=file, region='whole-file'), dict(owner=owner, gate='fresh'))

    def test_exit_and_invalid_json_fail_all_regions_after_one_attempt(self):
        for behavior in ('exit', 'json'):
            with self.subTest(behavior=behavior):
                self.producer(behavior)
                (self.root / 'attempts').unlink(missing_ok=True)
                verifier = Regions(self.root, {'fresh'})
                for file in self.files:
                    errors = verifier.check(self.entry(file), dict(line=2))
                    self.assertTrue(errors)
                    self.assertIn('fresh generated region unavailable:', errors[0])
                self.assertEqual(self.attempts(), 1)
                self.assertTrue(Regions(self.root, {'fresh'}).check(self.entry(self.files[0]), dict(line=2)))
                self.assertEqual(self.attempts(), 2)  # A new verifier gets its own attempt.

    def test_exit_and_invalid_json_fail_all_claims_after_one_attempt(self):
        for behavior in ('exit', 'json'):
            with self.subTest(behavior=behavior):
                self.producer(behavior)
                (self.root / 'attempts').unlink(missing_ok=True)
                verifier = Context(self.root, self.files)
                messages = []
                for file in self.files:
                    with self.assertRaises(ValueError) as caught:
                        self.context_check(verifier, file)
                    messages.append(str(caught.exception))
                self.assertTrue(messages[0])
                self.assertEqual(messages[0], messages[1])
                self.assertEqual(self.attempts(), 1)

    def test_timeout_and_spawn_failure_are_not_retried(self):
        original = subprocess.run
        for error in (subprocess.TimeoutExpired(['python3', 'tools/produce.py', '--emit'], 120),
                      OSError('fixture producer unavailable')):
            for kind in ('regions', 'claims'):
                with self.subTest(error=type(error).__name__, verifier=kind):
                    attempts = []
                    def run(argv, **kwargs):
                        if argv[-1] == '--emit':
                            attempts.append(argv)
                            raise error
                        return original(argv, **kwargs)
                    with patch('subprocess.run', side_effect=run):
                        verifier = Regions(self.root, {'fresh'}) if kind == 'regions' else Context(self.root, self.files)
                        for file in self.files:
                            if kind == 'regions':
                                self.assertTrue(verifier.check(self.entry(file), dict(line=2)))
                            else:
                                with self.assertRaises((OSError, subprocess.TimeoutExpired, ValueError)):
                                    self.context_check(verifier, file)
                    self.assertEqual(len(attempts), 1)

    def test_success_remains_cached_and_stale_content_still_fails(self):
        for kind in ('regions', 'claims'):
            with self.subTest(verifier=kind):
                for file in self.files:
                    (self.root / file).write_text(self.body)
                (self.root / 'attempts').unlink(missing_ok=True)
                verifier = Regions(self.root, {'fresh'}) if kind == 'regions' else Context(self.root, self.files)
                if kind == 'regions':
                    self.assertEqual(verifier.check(self.entry(self.files[0]), dict(line=2)), [])
                else:
                    self.assertIsNone(self.context_check(verifier, self.files[0]))
                (self.root / self.files[1]).write_text(self.body.replace('Generated', 'Stale'))
                if kind == 'regions':
                    self.assertTrue(verifier.check(self.entry(self.files[1]), dict(line=2)))
                else:
                    self.assertEqual(self.context_check(verifier, self.files[1])['kind'], 'stale-generated-region')
                self.assertEqual(self.attempts(), 1)


class PlantConcurrency(unittest.TestCase):
    def test_default_respects_small_cpu_count_and_override_is_explicit(self):
        import test_float_hardening as plants
        with patch.dict(os.environ, {}, clear=True):
            for cpus, expected in ((None, 1), (1, 1), (4, 2), (64, 2)):
                with patch.object(plants.os, 'cpu_count', return_value=cpus):
                    self.assertEqual(plants.workers(), expected)
        with patch.dict(os.environ, {'FLOAT_PLANT_WORKERS': '1'}):
            self.assertEqual(plants.workers(), 1)
        with patch.dict(os.environ, {'FLOAT_PLANT_WORKERS': '0'}):
            with self.assertRaises(ValueError):
                plants.workers()


if __name__ == '__main__':
    unittest.main()
