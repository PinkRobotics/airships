"""Focused checks on tools/float_post.py, the vacuum-float delivery adapter.

Everything here is unmistakably synthetic: a fake runtime tree (binding/ and
queue/submissions/), a switchable fake submit.py stand-in, and the real
adapter executed as a subprocess exactly as the heartbeat executes it. No
real queue filing ever happens — the fake submit writes only inside the
temporary directory this test owns. These exercise the delivery contract the
U3 bindings disposition names: resolve once and freeze; file through the
door; admission proven by stored authored fields, not by printed output;
identical prior admission is success; conflicting payload under the same id
fails closed; refusal, missing evidence, crash and timeout stay pending; an
unresolved binding files nothing; and the composed heartbeat invocation
delivers end to end through the fake door.
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import float_post as fpost  # noqa: E402
from test_float_progress import Habitat  # noqa: E402

FAKE_SUBMIT = '''#!/usr/bin/env python3
"""Test stand-in for the ship submit door. FAKE_MODE switches behavior:
file (default), refuse, silent, crash or sleep."""
import json
import os
import sys
import time
from pathlib import Path

mode = os.environ.get('FAKE_MODE', 'file')
argv = sys.argv[1:]


def flag(name):
    if name in argv:
        i = argv.index(name)
        return argv[i + 1] if i + 1 < len(argv) else ''
    return None


sid = flag('--id')
runtime = Path(os.environ['FAKE_RUNTIME'])
if mode == 'crash':
    sys.exit(9)
if mode == 'sleep':
    time.sleep(30)
if mode == 'refuse':
    print('REFUSED: unknown seat')
    sys.exit(1)
if mode == 'silent':
    print('SUBMITTED')
    sys.exit(0)
doc = {
    'id': sid,
    'kind': flag('--kind'),
    'from': flag('--from'),
    'to': flag('--to'),
    'unit': flag('--unit'),
    'completion': flag('--completion'),
    'body': flag('--body'),
    'asks': flag('--asks'),
    'next': flag('--next'),
    'authority': None,
    're': None,
    'supersedes': None,
    'priority': 5,
    'links_none': flag('--link') == 'none',
    'at': '2026-10-17T12:00:00-07:00',
    'ingested': '2026-10-17T12:00:30-07:00',
}
if flag('--deadline'):
    doc['deadline'] = flag('--deadline')
store = runtime / 'queue' / 'submissions'
store.mkdir(parents=True, exist_ok=True)
(store / f'{sid}.json').write_text(json.dumps(doc, indent=1) + '\\n')
print('SUBMITTED')
sys.exit(0)
'''

# Runs the real adapter with SUBMIT_TIMEOUT_S shrunk to 1 s, argv forwarded
# unchanged — the only way to exercise the TimeoutExpired path quickly.
WRAPPED_ADAPTER = '''#!/usr/bin/env python3
import sys
sys.path.insert(0, sys.argv[1])
del sys.argv[1]
import float_post
float_post.SUBMIT_TIMEOUT_S = 1
sys.exit(float_post.main())
'''


class AdapterRun:
    """A synthetic runtime, fake door and the real adapter around them."""

    def __init__(self, base):
        self.tmp = Path(base)
        self.runtime = self.tmp / 'fake-runtime'
        self.submit = self.tmp / 'fake-submit.py'
        self.submit.write_text(FAKE_SUBMIT)
        self.adapter = ROOT / 'tools' / 'float_post.py'
        self.delivery = self.tmp / 'fake-delivery'
        self.bind('sciences', 'sciences-p-1')
        self.bind('co', 'co-p-1')

    def bind(self, billet, seat):
        d = self.runtime / 'binding'
        d.mkdir(parents=True, exist_ok=True)
        (d / f'{billet}.json').write_text(
            json.dumps({'principal': {'seat': seat}}))

    def unbind(self, billet):
        (self.runtime / 'binding' / f'{billet}.json').unlink()

    def post_command(self):
        return [sys.executable, '-I', str(self.adapter),
                '--runtime', str(self.runtime), '--submit', str(self.submit),
                '--delivery-state', str(self.delivery)]

    def run(self, payload, mode='file', wrap_timeout=False, raw_stdin=None):
        env = dict(os.environ, FAKE_MODE=mode, FAKE_RUNTIME=str(self.runtime))
        argv = self.post_command()
        if wrap_timeout:
            wrapper = self.tmp / 'wrapped-adapter.py'
            wrapper.write_text(WRAPPED_ADAPTER)
            argv = [sys.executable, str(wrapper), str(ROOT / 'tools'),
                    *argv[3:]]
        data = raw_stdin if raw_stdin is not None else json.dumps(payload) + '\n'
        return subprocess.run(argv, input=data, capture_output=True,
                              text=True, env=env, timeout=120)

    def stored(self, item_id):
        try:
            return json.loads((self.runtime / 'queue' / 'submissions'
                               / f'{item_id}.json').read_text())
        except (OSError, ValueError):
            return None

    def stored_path(self, item_id):
        return self.runtime / 'queue' / 'submissions' / f'{item_id}.json'

    def state(self, item_id):
        try:
            return json.loads((self.delivery / f'{item_id}.json').read_text())
        except (OSError, ValueError):
            return None


LINE = {'type': 'line', 'id': 'vf-line-1-abcd1234',
        'body': 'vacuum-float · builder-b · 1 map point · 0 tokens',
        'now': '2026-10-17T13:00:00+00:00'}
DIAGNOSIS = {'type': 'diagnosis-report', 'id': 'vf-stall-97531abc-48h',
             'body': '48 h stall diagnosis, synthetic',
             'deadline': '2026-10-19T08:00:00+00:00',
             'now': '2026-10-19T09:00:00+00:00'}


class FloatPostAdapter(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix='float-post-test.'))
        self.r = AdapterRun(self.tmp)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_resolves_freezes_files_and_admits(self):
        proc = self.r.run(LINE)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        stored = self.r.stored(LINE['id'])
        self.assertEqual(stored['to'], 'sciences-p-1')  # billet resolved once
        self.assertEqual(stored['kind'], 'report')
        self.assertEqual(stored['from'], 'operator')
        self.assertEqual(stored['unit'], 'vacuum-float-heartbeat')
        self.assertEqual(stored['asks'], 'none')
        self.assertEqual(stored['next'], 'none')
        self.assertEqual(stored['body'], LINE['body'])
        self.assertTrue(stored['links_none'])
        state = self.r.state(LINE['id'])
        self.assertTrue(state['admitted'])
        self.assertEqual(state['attempts'], 1)
        self.assertEqual(state['envelope']['to'], 'sciences-p-1')

    def test_diagnosis_routes_to_co_asking_a_reply(self):
        proc = self.r.run(DIAGNOSIS)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        stored = self.r.stored(DIAGNOSIS['id'])
        self.assertEqual(stored['to'], 'co-p-1')
        self.assertEqual(stored['asks'], 'reply')
        self.assertEqual(stored['next'],
                         'co-p-1: carry the 48 h stall diagnosis to the Desk')
        self.assertEqual(stored['deadline'], DIAGNOSIS['deadline'])

    def test_prior_identical_admission_is_success_without_refiling(self):
        # Rewritten against the genuine door contract (U3-D2): the door's
        # OWN stamps (at/ingested/...) are the only excluded keys — a
        # re-stamped store is still the identical admission — while any
        # OTHER unexpected key is an authored-field conflict, never noise
        # to be ignored.
        self.r.run(LINE)
        path = self.r.stored_path(LINE['id'])
        doc = json.loads(path.read_text())
        self.assertIn('re', doc)            # the faithful fake door wrote it
        self.assertIsNone(doc['supersedes'])
        doc['at'] = '2026-10-18T09:00:00-07:00'        # queue re-stamp ...
        doc['ingested'] = '2026-10-18T09:00:30-07:00'  # ... is not payload
        path.write_text(json.dumps(doc, indent=1) + '\n')
        proc = self.r.run(LINE)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn('already admitted', proc.stdout)
        after = json.loads(path.read_text())
        self.assertEqual(after['at'], '2026-10-18T09:00:00-07:00')

    def test_conflicting_payload_under_same_id_fails_closed(self):
        self.r.run(LINE)
        path = self.r.stored_path(LINE['id'])
        doc = json.loads(path.read_text())
        doc['body'] = 'a different line entirely'
        path.write_text(json.dumps(doc, indent=1) + '\n')
        proc = self.r.run(LINE)
        self.assertEqual(proc.returncode, 2, proc.stdout)
        self.assertIn('CONFLICT', proc.stderr)
        self.assertFalse(self.r.state(LINE['id'])['admitted'])

    # -- U3 bounded repair regressions -------------------------------------

    def test_changed_identity_under_frozen_id_rejects_untouched(self):
        # U3-D1: a request arriving under a frozen id with a CHANGED body,
        # type or deadline is a collision — rc 2, nothing filed, and the
        # saved state + stored submission stay byte-identical.
        self.r.run(LINE)
        state_file = self.r.delivery / f"{LINE['id']}.json"
        stored_file = self.r.stored_path(LINE['id'])
        before = (state_file.read_bytes(), stored_file.read_bytes())
        for changed in ({'body': 'a different line entirely'},
                        {'type': 'diagnosis-report'},
                        {'deadline': '2026-10-20T00:00:00+00:00'}):
            payload = dict(LINE)
            payload.update(changed)
            proc = self.r.run(payload)
            self.assertEqual(proc.returncode, 2, (changed, proc.stdout))
            self.assertIn('CONFLICT', proc.stderr)
            self.assertIn('frozen identity', proc.stderr)
        self.assertEqual(state_file.read_bytes(), before[0])
        self.assertEqual(stored_file.read_bytes(), before[1])

    def test_identical_retry_after_binding_and_clock_change_reuses_envelope(self):
        # U3-D1 companion: an IDENTICAL logical retry after the binding
        # moved (succession) and the clock advanced reuses the frozen
        # envelope — addressee and deadline never re-resolved.
        self.r.run(DIAGNOSIS)
        frozen_to = self.r.stored(DIAGNOSIS['id'])['to']
        self.r.bind('co', 'co-p-9')                    # succession after freeze
        later = dict(DIAGNOSIS, now='2026-10-20T09:00:00+00:00')
        proc = self.r.run(later)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn('already admitted', proc.stdout)
        state = self.r.state(DIAGNOSIS['id'])
        self.assertEqual(state['envelope']['to'], frozen_to)
        self.assertEqual(state['envelope']['deadline'], DIAGNOSIS['deadline'])

    def test_unexpected_semantic_fields_in_store_reject(self):
        # U3-D2: meaningful fields the envelope never authored — deadline,
        # authority, standing, links — appearing in the stored submission
        # are conflicts; absence is meaning, not a skip.
        self.r.run(LINE)
        path = self.r.stored_path(LINE['id'])
        base = json.loads(path.read_text())
        for field, value in (('deadline', '2026-10-20T00:00:00+00:00'),
                             ('authority', [{'id': 'some-order'}]),
                             ('standing', 'held'),
                             ('links', [{'rel': 'amends', 'id': 'x'}])):
            doc = dict(base)
            doc[field] = value
            path.write_text(json.dumps(doc, indent=1) + '\n')
            proc = self.r.run(LINE)
            self.assertEqual(proc.returncode, 2, (field, proc.stdout))
            self.assertIn('CONFLICT', proc.stderr)
            self.assertIn(field, proc.stderr)

    def test_door_null_and_default_shape_normalizes(self):
        # U3-D2 companion: the actual door's absence shape — authority
        # written null, deadline/standing/links omitted, stamps present —
        # compares equal and admits as prior-identical.
        self.r.run(LINE)
        path = self.r.stored_path(LINE['id'])
        filed = json.loads(path.read_text())
        door_shape = {k: filed[k] for k in ('id', 'kind', 'from', 'to',
                                            'unit', 'completion', 'body',
                                            'asks', 'next', 'priority',
                                            'links_none')}
        door_shape.update({'authority': None, 're': None, 'supersedes': None,
                           'at': '2026-10-17T12:00:00-07:00',
                           'ingested': '2026-10-17T12:00:30-07:00'})
        path.write_text(json.dumps(door_shape, indent=1) + '\n')
        proc = self.r.run(LINE)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertIn('already admitted', proc.stdout)

    def test_unexpected_authored_semantics_reject(self):
        # U3-D2 completion: fields the submit door writes from sender
        # semantics — re, supersedes — or only when a sender authored a
        # value — scope, thread — plus keys no door contract explains
        # (landing) appearing in the stored submission are conflicts under
        # this envelope, whatever they carry. The old projection skipped
        # them as "door machinery"; the door's own contract makes them
        # sender-authored.
        self.r.run(LINE)
        path = self.r.stored_path(LINE['id'])
        base = json.loads(path.read_text())
        for field, value in (('re', 'ord-sciences-g1-x'),
                             ('supersedes', 'rpt-old'),
                             ('scope', 'ops'),
                             ('thread', 'thread-1'),
                             ('landing', 'L-97')):
            doc = dict(base)
            doc[field] = value
            path.write_text(json.dumps(doc, indent=1) + '\n')
            proc = self.r.run(LINE)
            self.assertEqual(proc.returncode, 2, (field, proc.stdout))
            self.assertIn(field, proc.stderr)

    def test_absent_conditional_key_means_absent(self):
        # U3-D2: for keys the door writes only when authored, absence is
        # meaning — the stored key being PRESENT, even with a null value,
        # is a conflict, because the door omits the key entirely.
        self.r.run(LINE)
        path = self.r.stored_path(LINE['id'])
        base = json.loads(path.read_text())
        for field in ('scope', 'deadline', 'standing', 'links'):
            doc = dict(base)
            doc[field] = None
            path.write_text(json.dumps(doc, indent=1) + '\n')
            proc = self.r.run(LINE)
            self.assertEqual(proc.returncode, 2, field)
            self.assertIn(field, proc.stderr)

    def test_every_envelope_field_is_compared(self):
        # U3-D2: the projection is the complete sender-authored set, not
        # a fixed field list — an envelope authoring an extra semantic
        # field has that field compared, and a differing stored value is
        # a conflict under the same id.
        sys.path.insert(0, str(ROOT / 'tools'))
        import float_post
        envelope = {'id': 'vf-line-9-zz', 'kind': 'report',
                    'from': 'operator', 'to': 'sciences-p-1',
                    'unit': 'vacuum-float-heartbeat', 'completion': 'c',
                    'body': 'b', 'asks': 'none', 'next': 'none',
                    'links_none': True, 'priority': 5,
                    'scope': 'operations'}
        stored_ok = dict(envelope, at='t', ingested='t', authority=None,
                         re=None, supersedes=None)
        self.assertEqual(float_post.admission_differs(stored_ok, envelope),
                         [])
        stored_bad = dict(stored_ok, scope='sciences')
        problems = float_post.admission_differs(stored_bad, envelope)
        self.assertTrue(any('scope' in p for p in problems), problems)

    def test_door_stamps_stay_excluded(self):
        # U3-D2 control: the door's own admission stamps — submit.py's
        # _STAMPS: at, ingested, from_seat, _vouched, links_schema — are
        # genuine transport and never conflicts, whatever they carry.
        self.r.run(LINE)
        path = self.r.stored_path(LINE['id'])
        base = json.loads(path.read_text())
        for field, value in (('at', '2030-01-01T00:00:00+00:00'),
                             ('ingested', '2030-01-01T00:00:00+00:00'),
                             ('from_seat', 'some-seat'),
                             ('_vouched', True),
                             ('links_schema', 7)):
            doc = dict(base)
            doc[field] = value
            path.write_text(json.dumps(doc, indent=1) + '\n')
            proc = self.r.run(LINE)
            self.assertEqual(proc.returncode, 0, (field, proc.stderr))

    def test_definite_refusal_is_rc3_and_files_nothing(self):
        proc = self.r.run(LINE, mode='refuse')
        self.assertEqual(proc.returncode, 3, proc.stdout)
        self.assertIsNone(self.r.stored(LINE['id']))
        state = self.r.state(LINE['id'])
        self.assertFalse(state['admitted'])
        self.assertIn('REFUSED', state['last_error'])

    def test_printed_submitted_without_store_is_rc4(self):
        proc = self.r.run(LINE, mode='silent')
        self.assertEqual(proc.returncode, 4, proc.stdout)
        self.assertIsNone(self.r.stored(LINE['id']))
        state = self.r.state(LINE['id'])
        self.assertFalse(state['admitted'])
        self.assertIn('no admission evidence', state['last_error'])

    def test_crash_and_timeout_stay_pending(self):
        proc = self.r.run(LINE, mode='crash')
        self.assertEqual(proc.returncode, 4, proc.stdout)
        state = self.r.state(LINE['id'])
        self.assertEqual(state['attempts'], 1)
        self.assertFalse(state['admitted'])
        proc = self.r.run(LINE, mode='sleep', wrap_timeout=True)
        self.assertEqual(proc.returncode, 4, proc.stdout)
        state = self.r.state(LINE['id'])
        self.assertEqual(state['attempts'], 2)      # retried, still pending
        self.assertFalse(state['admitted'])
        self.assertIn('timed out', state['last_error'])

    def test_unresolved_binding_is_rc5_and_files_nothing(self):
        self.r.unbind('co')
        proc = self.r.run(DIAGNOSIS)
        self.assertEqual(proc.returncode, 5, proc.stdout)
        self.assertIn('binding unresolved', proc.stderr)
        self.assertIsNone(self.r.state(DIAGNOSIS['id']))  # nothing frozen
        self.assertIsNone(self.r.stored(DIAGNOSIS['id']))  # nothing filed

    def test_frozen_envelope_survives_binding_change_and_keeps_deadline(self):
        proc = self.r.run(DIAGNOSIS, mode='refuse')   # freeze, file nothing
        self.assertEqual(proc.returncode, 3, proc.stdout)
        frozen_to = self.r.state(DIAGNOSIS['id'])['envelope']['to']
        self.assertEqual(frozen_to, 'co-p-1')
        self.r.bind('co', 'co-p-2')                    # a succession happens
        proc = self.r.run(DIAGNOSIS)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        stored = self.r.stored(DIAGNOSIS['id'])
        self.assertEqual(stored['to'], frozen_to)      # never re-resolved
        self.assertEqual(stored['deadline'], DIAGNOSIS['deadline'])
        self.assertEqual(self.r.state(DIAGNOSIS['id'])['envelope']['to'],
                         frozen_to)

    def test_malformed_payload_is_rc4(self):
        proc = self.r.run(None, raw_stdin='not json at all\n')
        self.assertEqual(proc.returncode, 4, proc.stdout)
        proc = self.r.run({'type': 'line', 'id': 'x'})   # body missing
        self.assertEqual(proc.returncode, 4, proc.stdout)


class ComposedInvocation(unittest.TestCase):
    """The heartbeat drives the real adapter against the fake door."""

    def setUp(self):
        self.h = Habitat()
        self.r = AdapterRun(self.h.base)

    def tearDown(self):
        self.h.close()

    def _heartbeat(self, now):
        return self.h.run('heartbeat', '--now', now,
                          '--post-command', *self.r.post_command())

    def test_heartbeat_delivers_line_through_adapter(self):
        saved = {k: os.environ.get(k) for k in ('FAKE_MODE', 'FAKE_RUNTIME')}
        os.environ['FAKE_MODE'] = 'file'
        os.environ['FAKE_RUNTIME'] = str(self.r.runtime)
        try:
            rc = self._heartbeat('2026-10-17T06:00:00+00:00')
        finally:
            for k, v in saved.items():
                if v is None:
                    os.environ.pop(k, None)
                else:
                    os.environ[k] = v
        self.assertEqual(rc, 0)
        delivery = json.loads((self.h.ledger / 'delivery-pending.json').read_text())
        hb = json.loads((self.h.ledger / 'heartbeat-state.json').read_text())
        admitted = [it for it in delivery['items'].values() if it['admitted']]
        self.assertEqual(len(admitted), 1)
        line_item = admitted[0]
        self.assertEqual(line_item['type'], 'line')
        stored = self.r.stored(line_item['id'])
        self.assertIsNotNone(stored)
        self.assertEqual(stored['body'], line_item['body'])
        self.assertEqual(stored['to'], 'sciences-p-1')
        self.assertEqual(hb['pending_delivery'], [])
        self.assertEqual(hb['last_admitted_line'], line_item['body'])
        # an unchanged line on a later run: no second filing anywhere
        rc = self._heartbeat('2026-10-17T12:00:00+00:00')
        self.assertEqual(rc, 0)
        files = list((self.r.runtime / 'queue' / 'submissions').glob('*.json'))
        self.assertEqual(len(files), 1)

    def test_heartbeat_keeps_item_pending_when_door_refuses(self):
        os.environ['FAKE_MODE'] = 'refuse'
        os.environ['FAKE_RUNTIME'] = str(self.r.runtime)
        try:
            rc = self._heartbeat('2026-10-17T06:00:00+00:00')
        finally:
            os.environ.pop('FAKE_MODE', None)
            os.environ.pop('FAKE_RUNTIME', None)
        self.assertEqual(rc, 1)                    # undelivered is failure
        delivery = json.loads((self.h.ledger / 'delivery-pending.json').read_text())
        hb = json.loads((self.h.ledger / 'heartbeat-state.json').read_text())
        item = next(it for it in delivery['items'].values())
        self.assertFalse(item['admitted'])
        self.assertEqual(item['attempts'], 1)      # once per scheduled run
        self.assertIn(item['id'], hb['pending_delivery'])
        self.assertIsNone(self.r.stored(item['id']))


class RebuiltAdmissionSemantics(unittest.TestCase):
    """U3 rebuilt-source regressions (NEW3600): type-sensitive recursive
    equality, expected-key PRESENCE, and a receipt that names the actual
    compared fields. These fail on the inherited f164 comparator, which
    used Python == (True==1, 5==5.0, nested drift) and stored.get (a
    missing authority/re/supersedes read as its default)."""

    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix='float-post-test.'))
        self.r = AdapterRun(self.tmp)
        self.envelope = fpost.build_envelope(
            dict(LINE), self.r.runtime)[0]

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_type_sensitive_equality_rejects_bool_int_float_nested(self):
        # U3-D2: Python == is not JSON equality. bool/int, float/int and
        # drift nested inside containers must all be conflicts.
        expected = fpost.expected_stored(self.envelope)
        # the ISOLATING bool/int case: the envelope authors links_none
        # True while the store carries 1 — equal under Python ==, a
        # conflict under JSON types (priority True vs 5 differs under ==
        # too, so it does not isolate the defect)
        stored = dict(expected)
        stored['links_none'] = 1
        self.assertNotEqual(
            fpost.admission_differs(stored, self.envelope), [],
            'links_none True vs 1 must be a type conflict')
        stored = dict(expected)
        stored['priority'] = 5.0                     # 5 == 5.0 under ==
        self.assertNotEqual(
            fpost.admission_differs(stored, self.envelope), [],
            'priority 5 vs 5.0 must be a type conflict')
        # nested drift inside an AUTHORED container: a links list whose
        # member dict carries 1 where the envelope authored 1 and the
        # store mutated it to True, deep-copied before mutation so the
        # envelope itself is never aliased
        import copy
        env_links = dict(self.envelope, links_none=False,
                         links=[{'rel': 'closes', 'id': 1,
                                 'part': 'completion'}])
        stored_links = copy.deepcopy(fpost.expected_stored(env_links))
        stored_links['links'][0]['id'] = True            # == but not ===
        self.assertNotEqual(
            fpost.admission_differs(stored_links, env_links), [],
            'nested 1 vs True must be a type conflict')
        # and the equal case stays equal (control)
        self.assertEqual(fpost.admission_differs(
            fpost.expected_stored(self.envelope), self.envelope), [])

    def test_missing_expected_key_rejects(self):
        # U3-D2: the real door always writes authority/re/supersedes —
        # their ABSENCE in the store is a conflict, never the default.
        for missing in ('authority', 're', 'supersedes', 'body'):
            stored = fpost.expected_stored(self.envelope)
            del stored[missing]
            problems = fpost.admission_differs(stored, self.envelope)
            self.assertTrue(problems, missing)
            self.assertIn(missing, problems[0])

    def test_receipt_names_actual_compared_fields(self):
        # U3-D2: the receipt's compared_fields lists the real projection
        # fields — never the characters of a description string.
        proc = self.r.run(LINE)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        receipt = self.r.state(LINE['id'])['receipt']
        fields = receipt['compared_fields']
        self.assertIsInstance(fields, list)
        self.assertIn('id', fields)
        self.assertIn('body', fields)
        for name in fields:
            self.assertGreater(len(name), 1, repr(fields))




if __name__ == '__main__':
    unittest.main()
