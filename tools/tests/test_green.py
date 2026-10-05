"""Failure controls for CI parity and the clean-check runner (no browser/full suite)."""
from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check_ci_parity as parity
import stranger_run as stranger


class ParityTests(unittest.TestCase):
    def test_current_workflow_and_deleting_each_gate(self):
        gates = parity.check()
        gates = [g for g in gates if g not in parity.reference_gates((parity.ROOT / 'Makefile').read_text())]
        workflow = (parity.ROOT / '.github/workflows/ci.yml').read_text()
        doc = parity.yaml.safe_load(workflow)
        step = next(s for s in doc['jobs']['checks']['steps'] if s.get('id') == 'check-gates')
        for gate in gates:
            with self.subTest(gate=gate), tempfile.TemporaryDirectory() as td:
                root = Path(td)
                (root / '.github/workflows').mkdir(parents=True)
                (root / 'Makefile').write_text((parity.ROOT / 'Makefile').read_text())
                step['run'] = 'make --keep-going ' + ' '.join(g for g in gates if g != gate)
                (root / '.github/workflows/ci.yml').write_text(parity.yaml.safe_dump(doc))
                with self.assertRaisesRegex(ValueError, 'missing='):
                    parity.check(root)

    def test_order_extras_duplicates_and_hidden_failure(self):
        template = {'jobs': {'checks': {'steps': [
            {'id': 'check-gates', 'run': 'make --keep-going first second'}]}}}
        step = template['jobs']['checks']['steps'][0]
        for command in ('make --keep-going first first',
                        'make --keep-going first second || true',
                        'make --keep-going $GATES', 'echo make first second'):
            step['run'] = command
            with self.subTest(command=command), self.assertRaises(ValueError):
                parity.ci_gates(parity.yaml.safe_dump(template))
        step['run'] = 'make --keep-going first second'
        step['if'] = 'false'
        with self.assertRaisesRegex(ValueError, 'unconditional'):
            parity.ci_gates(parity.yaml.safe_dump(template))
        self.assertEqual(parity.make_gates('check: first \\\n second # note\n'), ['first', 'second'])
        with self.assertRaises(ValueError):
            parity.make_gates('check: $(GATES)\n')
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / '.github/workflows').mkdir(parents=True)
            (root / 'Makefile').write_text('check: first second\n')
            del step['if']
            for command in ('make --keep-going second first', 'make --keep-going first second extra'):
                step['run'] = command
                (root / '.github/workflows/ci.yml').write_text(parity.yaml.safe_dump(template))
                with self.assertRaisesRegex(ValueError, 'CI parity FAIL'):
                    parity.check(root)


class SplitParityTests(unittest.TestCase):
    def setUp(self):
        import copy
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / '.github/workflows').mkdir(parents=True)
        self.make = 'CI_OUTSIDE_CHECK := plants\ncheck: first second\nplants:\n\ttrue\n'
        self.doc = {'on': {'push': None, 'pull_request': None}, 'jobs': {
            'checks': {'steps': [{'id': 'check-gates', 'run': 'make --keep-going first second'}]},
            'plants': {'steps': [{'run': 'make plants'}]}}}
        self.copy = copy.deepcopy

    def check(self, make=None, doc=None):
        (self.root / 'Makefile').write_text(self.make if make is None else make)
        (self.root / '.github/workflows/ci.yml').write_text(parity.yaml.safe_dump(self.doc if doc is None else doc))
        return parity.check(self.root)

    def test_split_passes_and_missing_job_is_red(self):
        self.assertEqual(self.check(), ['first', 'second'])
        doc = self.copy(self.doc)
        del doc['jobs']['plants']
        with self.assertRaisesRegex(ValueError, 'exactly once'):
            self.check(doc=doc)

    def test_renamed_target_and_extra_gate_are_red(self):
        with self.assertRaisesRegex(ValueError, 'real, explicit'):
            self.check(make=self.make.replace('plants:', 'renamed:'))
        doc = self.copy(self.doc)
        doc['jobs']['plants']['steps'][0]['run'] = 'make renamed'
        with self.assertRaisesRegex(ValueError, 'extra CI make gate'):
            self.check(doc=doc)
        doc['jobs']['plants']['steps'][0]['run'] = 'make plants extra'
        with self.assertRaisesRegex(ValueError, 'extra CI make gate'):
            self.check(doc=doc)

    def test_duplicate_disjoint_and_literal_contract(self):
        doc = self.copy(self.doc)
        doc['jobs']['duplicate'] = self.copy(doc['jobs']['plants'])
        with self.assertRaisesRegex(ValueError, 'exactly once'):
            self.check(doc=doc)
        with self.assertRaisesRegex(ValueError, 'disjoint'):
            self.check(make=self.make.replace('check: first second', 'check: first second plants'))
        for body in ('$(TARGETS)', 'plants plants'):
            with self.subTest(body=body), self.assertRaises(ValueError):
                self.check(make=self.make.replace(':= plants', ':= '+body))
        doc = self.copy(self.doc)
        doc['jobs']['plants']['steps'][0]['run'] = 'make plants || true'
        with self.assertRaises(ValueError):
            self.check(doc=doc)

    def test_erased_contract_and_hidden_extra_step_are_red(self):
        with self.assertRaisesRegex(ValueError, 'extra CI make gate'):
            self.check(make=self.make.replace('CI_OUTSIDE_CHECK := plants\n', ''))
        doc = self.copy(self.doc)
        doc['jobs']['plants']['steps'].append({'run': 'echo preparing\nmake extra'})
        with self.assertRaisesRegex(ValueError, 'literal make step'):
            self.check(doc=doc)

    def test_no_job_or_step_can_skip_or_hide_failure(self):
        for level in ('job', 'step'):
            for key, value in (('if', 'false'), ('continue-on-error', True)):
                doc = self.copy(self.doc)
                mapping = doc['jobs']['plants'] if level == 'job' else doc['jobs']['plants']['steps'][0]
                mapping[key] = value
                with self.subTest(level=level, key=key), self.assertRaisesRegex(ValueError, 'unconditional'):
                    self.check(doc=doc)
        doc = self.copy(self.doc)
        doc['jobs']['plants']['needs'] = 'checks'
        with self.assertRaisesRegex(ValueError, 'independent'):
            self.check(doc=doc)

    def test_every_push_and_pull_request_without_filters(self):
        for events in ({'push': None}, {'pull_request': None},
                       {'push': {'paths': ['tools/**']}, 'pull_request': None},
                       {'push': {'branches': ['main']}, 'pull_request': None}):
            doc = self.copy(self.doc)
            doc['on'] = events
            with self.subTest(events=events), self.assertRaises(ValueError):
                self.check(doc=doc)


class ReferenceParityTests(unittest.TestCase):
    check = SplitParityTests.check

    def setUp(self):
        SplitParityTests.setUp(self)
        self.make = ('# reference: exact output from the reference toolchain.\n'
                     'CI_REFERENCE_CHECK := reference\n' + self.make.replace(
                         'check: first second', 'check: first reference second'))

    def test_reference_is_local_and_real_tree_is_green(self):
        self.assertEqual(self.check(), ['first', 'reference', 'second'])
        text = (parity.ROOT / 'Makefile').read_text()
        self.assertEqual(parity.check(), parity.make_gates(text))
        self.assertEqual(parity.reference_gates(text), ['goldenui', 'pdfcheck'])

    def test_reference_cannot_appear_in_ci_or_leave_check(self):
        doc = self.copy(self.doc)
        doc['jobs']['checks']['steps'][0]['run'] += ' reference'
        with self.assertRaisesRegex(ValueError, 'extra='):
            self.check(doc=doc)
        for command in ('echo reference', "bash -c 'make reference'"):
            doc = self.copy(self.doc)
            doc['jobs']['plants']['steps'].append({'run': command})
            with self.subTest(command=command), self.assertRaisesRegex(ValueError, 'reference gate appears'):
                self.check(doc=doc)
        with self.assertRaisesRegex(ValueError, 'check prerequisite'):
            self.check(make=self.make.replace('first reference second', 'first second'))

    def test_reason_literal_and_disjoint_contract(self):
        with self.assertRaisesRegex(ValueError, 'reason line'):
            self.check(make=self.make.replace('# reference: exact output from the reference toolchain.\n', ''))
        for value in ('$(REFERENCES)', 'reference reference'):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.check(make=self.make.replace(':= reference', ':= '+value))
        with self.assertRaisesRegex(ValueError, 'disjoint'):
            self.check(make=self.make.replace(':= plants', ':= reference') + '\nreference:\n')


class StrangerTests(unittest.TestCase):
    def test_first_node_suite_failure_is_not_masked_by_second_suite(self):
        with tempfile.TemporaryDirectory() as td:
            run = Path(td)
            node = run / 'node'
            node.write_text('#!/bin/sh\ncase "$*" in *tests/node/*) exit 7;; esac\nexit 0\n')
            node.chmod(0o755)
            env = dict(os.environ, PATH=f'{run}:/usr/bin:/bin')
            result = subprocess.run(['make', '--no-print-directory', 'test-node'],
                                    cwd=parity.ROOT, env=env, capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn('Error 7', result.stderr)

    def test_env_is_empty_home_is_fresh_and_red_does_not_stop_next_gate(self):
        with tempfile.TemporaryDirectory() as td:
            run = Path(td)
            env = stranger.clean_environment(run)
            self.assertEqual(list((run / 'home').iterdir()), [])
            (run / 'Makefile').write_text(
                'red:\n\t@echo intentional-red; exit 7\n'
                'green:\n\t@test -z "$$STRANGER_TEST_SECRET"\n'
                '\t@test ! -e "$$HOME/tmp"\n\t@test -d "$$TMPDIR"\n\t@echo green-after-red\n')
            with patch.dict(os.environ, {'STRANGER_TEST_SECRET': 'must-not-leak'}), redirect_stdout(io.StringIO()):
                gates = stranger.run_gates(run, ['red', 'green'], env, [], 10, lambda s: s)
            self.assertEqual([g['status'] for g in gates], ['fail', 'pass'])
            self.assertTrue(any('green-after-red' in line for line in gates[1]['output_tail']))
            self.assertEqual(list((run / 'home').iterdir()), [])
            self.assertNotEqual(stranger.report_exit({'errors': [], 'gates': gates}), 0)
            self.assertEqual(stranger.report_exit({'errors': [], 'gates': gates[1:]}), 0)
            for gate in gates:
                self.assertEqual(set(gate), {'gate', 'status', 'exit_code', 'seconds', 'output_tail'})
                self.assertGreaterEqual(gate['seconds'], 0)

    def test_timeout_is_red(self):
        with tempfile.TemporaryDirectory() as td:
            code, _ = stranger.process(['/bin/sh', '-c', 'sleep 5'], Path(td), timeout=0.05)
            self.assertEqual(code, 124)

    def test_public_report_scrubs_paths_and_identity(self):
        with tempfile.TemporaryDirectory() as td:
            run = Path(td)
            scrub = stranger.scrubber(parity.ROOT, run)
            account = stranger.pwd.getpwuid(os.getuid())
            record = json.dumps({'message': f'{parity.ROOT}/test {run}/out {account.pw_dir}/secret '
                                f'{account.pw_name} {stranger.socket.gethostname()}'})
            cleaned = scrub(record)
            self.assertNotIn(str(parity.ROOT), cleaned)
            self.assertNotIn(str(run), cleaned)
            self.assertNotIn(account.pw_dir, cleaned)
            self.assertNotIn(account.pw_name, cleaned)
            self.assertEqual(set(json.loads(cleaned)), {'message'})

    def test_runner_does_not_probe_retired_ports(self):
        def clone(source, destination, *args):
            destination.mkdir()
            (destination / 'Makefile').write_text('check: sample\n')
            return '0' * 40, {'kind': 'fixture'}

        with tempfile.TemporaryDirectory() as td:
            output = Path(td) / 'report.json'
            row = {'gate': 'sample', 'status': 'pass', 'exit_code': 0,
                   'seconds': 0, 'output_tail': []}
            with patch.object(sys, 'argv', ['stranger_run.py', '--output', str(output)]), \
                    patch.dict(os.environ, {'TMPDIR': td}), \
                    patch.object(stranger, 'clone_input', side_effect=clone), \
                    patch.object(stranger, 'isolation_probe', return_value=([], [])), \
                    patch.object(stranger, 'tool_versions', return_value={}), \
                    patch.object(stranger.shutil, 'which', return_value='/bin/sh'), \
                    patch.object(stranger, 'run_gates', return_value=[row]) as run, \
                    patch.object(stranger.socket, 'socket', side_effect=AssertionError('fixed-port probe')), \
                    redirect_stdout(io.StringIO()):
                code = stranger.main()
            report = json.loads(output.read_text())
            self.assertEqual(code, 0)
            self.assertEqual(run.call_count, 1)
            self.assertEqual(report['gates'], [row])
            self.assertEqual(report['errors'], [])
            self.assertNotIn('fixed test ports', json.dumps(report))
            self.assertIn('system-chosen loopback ports', json.dumps(report['isolation']))

    def test_missing_tmpdir_writes_report_and_exits_nonzero(self):
        with tempfile.TemporaryDirectory() as td:
            out = Path(td) / 'report.json'
            env = dict(os.environ)
            env.pop('TMPDIR', None)
            result = subprocess.run([sys.executable, str(parity.ROOT / 'tools/stranger_run.py'),
                                     '--output', str(out)], env=env, capture_output=True)
            self.assertEqual(result.returncode, 1)
            report = json.loads(out.read_text())
            self.assertEqual(report['status'], 'fail')
            self.assertEqual(report['gates'], [])
            self.assertIn('TMPDIR', report['errors'][0])


if __name__ == '__main__':
    unittest.main()
