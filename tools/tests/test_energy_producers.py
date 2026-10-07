"""Verify producer modes on disposable trees, including every output's mtime."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


def snapshot(root):
    return {p.relative_to(root).as_posix():
            (hashlib.sha256(p.read_bytes()).hexdigest(), p.stat().st_mtime_ns)
            for p in root.rglob('*') if p.is_file()}


class EnergyDocumentsModes(unittest.TestCase):
    script = 'research/analysis/energy-documents.mjs'

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(dir=os.environ.get('TMPDIR'))
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.root = Path(cls.tmp.name)/'tree'
        # Copy code and committed input/output directories; no private checkout
        # metadata or hand-up artifacts are needed by this public test.
        cls.root.mkdir()
        for name in ('research/analysis', 'research/reports', 'docs', 'sim', '3d/model'):
            (cls.root/name).parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(ROOT/name, cls.root/name,
                            ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
        cls.emit = cls.run_mode('--emit')
        if cls.emit.returncode:
            raise AssertionError(cls.emit.stderr.decode())
        cls.outputs = json.loads(cls.emit.stdout)
        if len(cls.outputs) != 8:
            raise AssertionError('Expected exactly eight generated outputs')

    @classmethod
    def run_mode(cls, *args):
        return subprocess.run(['node', cls.script, *args], cwd=cls.root,
                              capture_output=True, timeout=180)

    def restore(self):
        for path, body in self.outputs.items():
            (self.root/path).write_bytes(body.encode())

    def unchanged_run(self, args, expected):
        before = snapshot(self.root)
        result = self.run_mode(*args)
        self.assertEqual(result.returncode, expected,
                         (result.stdout+result.stderr).decode())
        self.assertEqual(snapshot(self.root), before, 'Producer changed bytes or mtimes')
        return (result.stdout+result.stderr).decode()

    def test_current_check_does_not_write(self):
        self.restore()
        self.unchanged_run(('--check',), 0)

    def test_stale_output_is_named_and_preserved(self):
        self.restore()
        file = 'docs/ENERGY-MODEL-2026-10.md'
        p = self.root/file
        p.write_bytes(p.read_bytes()+b'\nSTALE OUTPUT\n')
        self.assertIn(file+': stale', self.unchanged_run(('--check',), 1))

    def test_all_missing_and_stale_outputs_are_named_and_preserved(self):
        self.restore()
        missing = ('docs/PHYSICS.md', 'docs/OPEN-QUESTIONS.md',
                   'research/reports/02-paper.md', 'research/reports/03-diligence.md',
                   'research/analysis/energy-documents.json')
        stale = ('sim/README.md', 'docs/ENERGY-CLOSURE-2026-10.md',
                 'docs/ENERGY-MODEL-2026-10.md')
        for file in missing:
            (self.root/file).unlink()
        for file in stale:
            p = self.root/file
            p.write_bytes(p.read_bytes()+b'\nSTALE OUTPUT\n')
        output = self.unchanged_run(('--check',), 1)
        for file in missing:
            self.assertIn(file+': missing', output)
        for file in stale:
            self.assertIn(file+': stale', output)

    def test_corrupted_report_does_not_hide_other_stale_outputs(self):
        self.restore()
        report = 'research/reports/02-paper.md'
        other = 'docs/ENERGY-MODEL-2026-10.md'
        (self.root/report).write_bytes(b'broken generated report\n')
        p = self.root/other
        p.write_bytes(p.read_bytes()+b'\nSTALE OUTPUT\n')
        output = self.unchanged_run(('--check',), 1)
        for file in (report, other):
            self.assertIn(file+': stale', output)

    def test_unknown_or_conflicting_arguments_refuse_before_writing(self):
        self.restore()
        for args in (('--chek',), ('--check', '--typo'), ('--emit', '--typo'),
                     ('--check', '--emit'), ('--check', '--check'), ('extra',)):
            with self.subTest(args=args):
                output = self.unchanged_run(args, 2)
                self.assertEqual(output, 'Usage: node '+self.script+' [--check | --emit]\n')

    def test_unknown_argument_refuses_without_model_inputs(self):
        self.restore()
        file = self.root/'research/analysis/energy-necessary.json'
        saved = file.read_bytes()
        file.unlink()
        try:
            output = self.unchanged_run(('--typo',), 2)
            self.assertEqual(output, 'Usage: node '+self.script+' [--check | --emit]\n')
        finally:
            file.write_bytes(saved)

    def test_emit_is_read_only_and_default_generation_matches_it(self):
        self.restore()
        before = snapshot(self.root)
        result = self.run_mode('--emit')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, self.emit.stdout)
        self.assertEqual(snapshot(self.root), before)
        result = self.run_mode()
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        for file, body in self.outputs.items():
            self.assertEqual((self.root/file).read_bytes(), body.encode(), file)


class EnergyRecordModes(unittest.TestCase):
    def test_bag_and_rotor_checks_preserve_bytes_and_mtimes(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('TMPDIR')) as tmp:
            root = Path(tmp)/'tree'
            root.mkdir()
            for name in ('research/analysis', 'sim'):
                (root/name).parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(ROOT/name, root/name)
            # Small model fixture: exercise the real producer entry points and
            # filesystem boundary without repeating their expensive searches.
            # Full-model RED/GREEN runs remain separate integration evidence.
            (root/'sim/index.js').write_text('''export const CLASSES={fixture:{id:'fixture'}}, MODES={balanced:{}},
              PHASES=[], ROTOR_EFFICIENCY_VALUES=[0.7];
              export const ballastRequirement=()=>({feasible:true,ballastT:1});
              export const planCycle=()=>({feasible:true,worst:{unheldT:0},eCycleMWh:1});
              export const drawAt=()=>({thrustLimitT:1});''')
            for name in ('energy-bag-comparison', 'energy-rotor-range'):
                script = 'research/analysis/'+name+'.mjs'
                file = 'research/analysis/'+name+'.json'
                def run(*args):
                    return subprocess.run(['node', script, *args], cwd=root,
                                          capture_output=True, timeout=180)
                generated = run()
                self.assertEqual(generated.returncode, 0, generated.stderr.decode())
                for flag in ('--typo', '--emit'):
                    before = snapshot(root)
                    p = run(flag)
                    self.assertEqual(p.returncode, 2, p.stderr.decode())
                    self.assertEqual(p.stderr.decode(), 'Usage: node '+script+' [--check]\n')
                    self.assertEqual(snapshot(root), before)
                before = snapshot(root)
                p = run('--check')
                self.assertEqual(p.returncode, 0, p.stderr.decode())
                self.assertEqual(snapshot(root), before)
                canonical = (root/file).read_bytes()
                (root/file).write_bytes(canonical+b'\nSTALE OUTPUT\n')
                before = snapshot(root)
                p = run('--check')
                self.assertEqual(p.returncode, 1, p.stderr.decode())
                self.assertIn(file+': stale', p.stderr.decode())
                self.assertEqual(snapshot(root), before)
                (root/file).unlink()
                before = snapshot(root)
                p = run('--check')
                self.assertEqual(p.returncode, 1, p.stderr.decode())
                self.assertIn(file+': missing', p.stderr.decode())
                self.assertEqual(snapshot(root), before)
                p = run()
                self.assertEqual(p.returncode, 0, p.stderr.decode())
                self.assertEqual((root/file).read_bytes(), canonical)


class PythonProducerModes(unittest.TestCase):
    def test_payload_and_motion_catalogue_modes(self):
        with tempfile.TemporaryDirectory(dir=os.environ.get('TMPDIR')) as tmp:
            root = Path(tmp)/'tree'
            root.mkdir()
            for name in ('research/analysis', 'sim', 'tools'):
                (root/name).parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(ROOT/name, root/name,
                                ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
            for script, outputs in (
                    ('research/analysis/payload-exchange.py',
                     ('research/analysis/payload-exchange.json', 'research/analysis/payload-exchange.md')),
                    ('tools/review_gate_motion.py', ('tools/float_dispositions.json',))):
                command = 'python3 '+script
                def run(*args):
                    return subprocess.run(['python3', '-B', script, *args], cwd=root,
                                          capture_output=True, timeout=60)
                original = {f:(root/f).read_bytes() for f in outputs}
                before = snapshot(root)
                p = run('--check')
                self.assertEqual(p.returncode, 0, (p.stdout+p.stderr).decode())
                self.assertEqual(snapshot(root), before)
                file = outputs[0]
                (root/file).write_bytes(original[file]+b'\nSTALE OUTPUT\n')
                # The motion catalogue is also an input; use valid stale JSON.
                if script.startswith('tools/'):
                    (root/file).write_bytes(original[file]+b'\n')
                before = snapshot(root)
                p = run('--check')
                self.assertEqual(p.returncode, 1, (p.stdout+p.stderr).decode())
                self.assertIn(file+': stale', p.stderr.decode())
                self.assertEqual(snapshot(root), before)
                for f in outputs:
                    (root/f).unlink()
                before = snapshot(root)
                p = run('--check')
                self.assertEqual(p.returncode, 1, (p.stdout+p.stderr).decode())
                for f in outputs:
                    self.assertIn(f+': missing', p.stderr.decode())
                self.assertEqual(snapshot(root), before)
                for flag in ('--typo', '--emit'):
                    before = snapshot(root)
                    p = run(flag)
                    self.assertEqual(p.returncode, 2)
                    self.assertEqual(p.stderr.decode(), 'Usage: '+command+' [--check]\n')
                    self.assertEqual(snapshot(root), before)
                # Restore the prose/input shell before checking default writes.
                for f, data in original.items():
                    (root/f).write_bytes(data)
                p = run()
                self.assertEqual(p.returncode, 0, p.stderr.decode())
                for f, data in original.items():
                    self.assertEqual((root/f).read_bytes(), data, f)
