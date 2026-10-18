"""Receipt refusal and writer failure cases; no browser or model subprocesses."""
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check_float_plants as gate

# Run in a fresh interpreter whose cwd is a tree: load that tree's plant registry and report
# every repository module it read, the case ids, and each appended payload.
REGISTRY = '''
import json, sys
from pathlib import Path
root = Path.cwd().resolve()
sys.path.insert(0, str(root / 'tools/tests'))
import test_float_hardening
cases = test_float_hardening.specs()
files = [Path(m.__file__).resolve() for m in list(sys.modules.values()) if getattr(m, '__file__', None)]
print(json.dumps(dict(modules=sorted({f.relative_to(root).as_posix() for f in files if f.is_relative_to(root)}),
                      cases=sorted(cases),
                      appended={name: spec['append'][1] for name, spec in cases.items() if 'append' in spec})))
'''


def registry(root):
    run = subprocess.run([sys.executable, '-B', '-c', REGISTRY], cwd=root, capture_output=True, text=True, check=True)
    return json.loads(run.stdout)


class PlantState(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='plant-state-')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for rel in set(gate.REQUIRED) | set(gate.EXTRA):
            path = self.root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('# gate fixture\n')
        (self.root / 'Makefile').write_text(''.join(f'{t}:\n\tpython3 fixture.py\n' for t in gate.RULES))
        (self.root / gate.RECORD).parent.mkdir(parents=True)
        self.cases = ['wrong-claim', 'positive-control']
        mock = patch.object(gate, 'expected_cases', return_value=self.cases)
        mock.start()
        self.addCleanup(mock.stop)
        # These writer calls use synthetic two-case reports, not the real plants.
        output = patch('builtins.print')
        output.start()
        self.addCleanup(output.stop)

    def record(self):
        (self.root / gate.RECORD).write_text(json.dumps(gate.snapshot(self.root)))

    def report(self, env):
        rows = [dict(id=name, code=0, green=True) for name in gate.BASELINES]
        rows += [dict(id='wrong-claim', code=2, green=False, expected='No disposition', output='No disposition'),
                 dict(id='positive-control', code=0, green=True)]
        Path(env['FLOAT_PLANT_REPORT']).write_text(json.dumps(rows))

    def test_missing_invalid_and_matching_receipt_without_git(self):
        self.assertIn('make floatplants', gate.check(self.root))
        (self.root / gate.RECORD).write_text('not json')
        self.assertIn('invalid receipt', gate.check(self.root))
        self.record()
        self.assertIsNone(gate.check(self.root))
        self.assertEqual(gate.snapshot(self.root), gate.snapshot(self.root))

    def test_comment_change_and_revert_require_exact_contents(self):
        self.record()
        path = self.root / 'tools/float_text.py'
        original = path.read_text()
        path.write_text(original + '# changed\n')
        self.assertIn('tools/float_text.py; run make floatplants', gate.check(self.root))
        self.record()
        self.assertIsNone(gate.check(self.root))
        path.write_text(original)
        self.assertIn('make floatplants', gate.check(self.root))

    def test_added_deleted_inputs_and_recipe_changes(self):
        self.record()
        extra = self.root / 'tools/float_new_rule.py'
        extra.write_text('# new rule\n')
        self.assertIn('tools/float_new_rule.py', gate.check(self.root))
        extra.unlink()
        self.assertIsNone(gate.check(self.root))
        (self.root / 'tools/float_text.py').unlink()
        with self.assertRaisesRegex(ValueError, 'missing or unreadable'):
            gate.check(self.root)
        (self.root / 'tools/float_text.py').write_text('# gate fixture\n')
        makefile = self.root / 'Makefile'
        makefile.write_text(makefile.read_text().replace('floatplants:\n', 'floatplants: other\n'))
        self.assertIn('Makefile#floatplants', gate.check(self.root))

    def test_failed_or_incomplete_run_preserves_receipt(self):
        self.record()
        previous = (self.root / gate.RECORD).read_bytes()
        with patch.object(gate.subprocess, 'run', return_value=SimpleNamespace(returncode=1)):
            self.assertEqual(gate.run_full(self.root), 1)
        self.assertEqual((self.root / gate.RECORD).read_bytes(), previous)
        def incomplete(argv, *, cwd, env):
            Path(env['FLOAT_PLANT_REPORT']).write_text('[]')
            return SimpleNamespace(returncode=0)
        with patch.object(gate.subprocess, 'run', side_effect=incomplete):
            with self.assertRaisesRegex(ValueError, 'complete passing report'):
                gate.run_full(self.root)
        self.assertEqual((self.root / gate.RECORD).read_bytes(), previous)

    def test_writer_forces_full_selection_and_detects_midrun_changes(self):
        def execute(argv, *, cwd, env):
            self.assertEqual(env['FLOAT_PLANT_MODE'], 'all')
            self.assertEqual(env['FLOAT_PLANT_CASES'], '')
            self.assertNotIn('--observe', argv)
            self.report(env)
            return SimpleNamespace(returncode=0)
        with patch.dict(os.environ, FLOAT_PLANT_MODE='fast', FLOAT_PLANT_CASES='wrong-claim'):
            with patch.object(gate.subprocess, 'run', side_effect=execute):
                self.assertEqual(gate.run_full(self.root), 0)
        self.assertIsNone(gate.check(self.root))
        previous = (self.root / gate.RECORD).read_bytes()
        def changed(argv, *, cwd, env):
            result = execute(argv, cwd=cwd, env=env)
            (self.root / 'tools/float_text.py').write_text('# changed during tests\n')
            return result
        with patch.object(gate.subprocess, 'run', side_effect=changed):
            with self.assertRaisesRegex(ValueError, 'changed during full plants'):
                gate.run_full(self.root)
        self.assertEqual((self.root / gate.RECORD).read_bytes(), previous)

    def test_false_green_and_wrong_red_reason_are_rejected(self):
        with patch.dict(os.environ):
            env = dict(FLOAT_PLANT_REPORT=str(self.root / 'report.json'))
            self.report(env)
            rows = json.loads(Path(env['FLOAT_PLANT_REPORT']).read_text())
        rows[-2]['code'] = 0
        with self.assertRaisesRegex(ValueError, 'required result'):
            gate.validate_report(rows, self.cases)
        rows[-2]['code'] = 2
        rows[-2]['output'] = 'unrelated failure'
        with self.assertRaisesRegex(ValueError, 'expected reason'):
            gate.validate_report(rows, self.cases)

    def test_shards_partition_sorted_cases_and_validate_numbers(self):
        cases = ['z', 'a', 'm', 'b', 'x']
        parts = [gate.shard_cases(cases, i, 3) for i in range(1, 4)]
        self.assertEqual(parts, [['a', 'x'], ['b', 'z'], ['m']])
        self.assertEqual(sorted(sum(parts, [])), sorted(cases))
        self.assertEqual(gate.parse_shard('1/4'), (1, 4))
        for value in ('0/4', '5/4', '1/0', '1', '1/4.0', '01/4', ''):
            with self.subTest(value=value), self.assertRaises(ValueError):
                gate.parse_shard(value)
        for index, count in ((0, 2), (3, 2), (1, 6), (True, 2)):
            with self.assertRaises(ValueError):
                gate.shard_cases(cases, index, count)

    def test_shard_forces_selection_validates_report_and_never_writes_receipt(self):
        self.record()
        path = self.root / gate.RECORD
        before = path.read_bytes()
        def execute(argv, *, cwd, env):
            self.assertEqual(env['FLOAT_PLANT_MODE'], 'all')
            self.assertEqual(env['FLOAT_PLANT_CASES'], 'positive-control')
            self.assertNotIn('--observe', argv)
            rows = [dict(id=name, code=0, green=True) for name in gate.BASELINES]
            rows.append(dict(id='positive-control', code=0, green=True))
            Path(env['FLOAT_PLANT_REPORT']).write_text(json.dumps(rows))
            return SimpleNamespace(returncode=0)
        with patch.dict(os.environ, FLOAT_PLANT_MODE='fast', FLOAT_PLANT_CASES='wrong-claim'), \
                patch.object(gate.subprocess, 'run', side_effect=execute):
            self.assertEqual(gate.run_shard('1/2', self.root), 0)
        self.assertEqual(path.read_bytes(), before)
        path.unlink()
        with patch.object(gate.subprocess, 'run', side_effect=execute):
            self.assertEqual(gate.run_shard('1/2', self.root), 0)
        self.assertFalse(path.exists())
        def incomplete(argv, *, cwd, env):
            Path(env['FLOAT_PLANT_REPORT']).write_text('[]')
            return SimpleNamespace(returncode=0)
        with patch.object(gate.subprocess, 'run', side_effect=incomplete), \
                self.assertRaisesRegex(ValueError, 'complete passing report'):
            gate.run_shard('1/2', self.root)
        self.assertFalse(path.exists())

    def test_shard_failure_and_midrun_change_preserve_receipt(self):
        self.record()
        path = self.root / gate.RECORD
        before = path.read_bytes()
        with patch.object(gate.subprocess, 'run', return_value=SimpleNamespace(returncode=7)):
            self.assertEqual(gate.run_shard('1/2', self.root), 7)
        def changed(argv, *, cwd, env):
            rows = [dict(id=name, code=0, green=True) for name in gate.BASELINES]
            rows.append(dict(id='positive-control', code=0, green=True))
            Path(env['FLOAT_PLANT_REPORT']).write_text(json.dumps(rows))
            (self.root / 'tools/float_text.py').write_text('# changed during tests\n')
            return SimpleNamespace(returncode=0)
        with patch.object(gate.subprocess, 'run', side_effect=changed), \
                self.assertRaisesRegex(ValueError, 'changed during shard plants'):
            gate.run_shard('1/2', self.root)
        self.assertEqual(path.read_bytes(), before)


class PlantPayloadFingerprint(unittest.TestCase):
    """A plant built from another file's bytes must move the receipt's fingerprint when they change."""

    def test_every_module_the_plant_registry_loads_is_fingerprinted(self):
        loaded = registry(gate.ROOT)['modules']
        hashed = {rel for rel in gate.snapshot()['files'] if not rel.startswith('Makefile#')}
        self.assertIn('tools/tests/test_float_hardening.py', loaded)
        self.assertEqual(sorted(set(loaded) - hashed), [])

    def test_fixture_only_payload_change_refuses_the_old_receipt(self):
        temporary = tempfile.TemporaryDirectory(prefix='plant-payload-')
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        inputs = {rel for rel in gate.snapshot()['files'] if not rel.startswith('Makefile#')}
        for rel in sorted(inputs | set(registry(gate.ROOT)['modules']) | {'Makefile'}):
            (root / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(gate.ROOT / rel, root / rel)
        (root / gate.RECORD).parent.mkdir(parents=True)
        (root / gate.RECORD).write_text(json.dumps(gate.snapshot(root)))
        self.assertIsNone(gate.check(root))
        before = registry(root)
        # The positive control's own payload names the anchor: its first range-diff pair, = to !.
        payload = before['appended']['M5-landing-table-rebase']
        pair = next(line for line in payload.splitlines() if re.match(r'1:  [0-9a-f]+ = 1:  ', line))
        fixture = root / 'tools/tests/test_attestation_shape.py'
        original = fixture.read_text()
        self.assertEqual(original.count(pair), 1)
        fixture.write_text(original.replace(pair, pair.replace(' = ', ' ! ', 1)))
        after = registry(root)
        self.assertEqual(after['cases'], before['cases'])
        self.assertNotEqual(after['appended']['M5-landing-table-rebase'], payload)
        recorded = json.loads((root / gate.RECORD).read_text())
        self.assertNotEqual(gate.snapshot(root)['sha256'], recorded['sha256'],
                            'a fixture-only plant change left the full-plants fingerprint unchanged')
        self.assertIn('tools/tests/test_attestation_shape.py; run make floatplants', gate.check(root))
        fixture.write_text(original)
        self.assertIsNone(gate.check(root))


if __name__ == '__main__':
    unittest.main()
