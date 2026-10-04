"""Receipt refusal and writer failure cases; no browser or model subprocesses."""
import json
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check_float_plants as gate


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


if __name__ == '__main__':
    unittest.main()
