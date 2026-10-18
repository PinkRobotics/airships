"""Focused checks on the externally visible contracts of tools/float_progress.py.

Every fixture here is unmistakably synthetic: fake seats (SYN-XO, SYN-ADM,
SYN-BUILDER), a fake submissions directory, a fake binding directory, injected
timestamps and an injected posting adapter. No real queue message is sent, no
live ledger is touched and no real clock is waited on. These tests exercise
the contracts the U3 brief names: unauthorized award rejection; replay vs
conflicting event id; immutable correction/history; rubric dual approval,
forward-only and one-per-map-version; scoped current-lane audit zeroing;
unknown vs measured-zero cost and zero denominators; the empty honest initial
state; six-hour unchanged-line no-action behaviour; 48 h / 5-day stall
boundary, idempotency and reset; append recovery; and caps / benchmark
uniqueness against explicit accounting configurations.
"""
from __future__ import annotations

import datetime as dt
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'tools'))

import float_progress as fp  # noqa: E402

XO = 'SYN-XO'
ADM = 'SYN-ADM'
BUILDER = 'SYN-BUILDER'
ANCHOR_AT = '2026-10-17T00:14:57-07:00'


class Habitat:
    """A synthetic world: submissions dir, binding dir, ledger dir, config."""

    def __init__(self):
        self.base = Path(tempfile.mkdtemp(prefix='float-progress-test.'))
        self.submissions = self.base / 'submissions'
        self.binding = self.base / 'binding'
        self.ledger = self.base / 'ledger'
        self.submissions.mkdir(parents=True)
        self.binding.mkdir(parents=True)
        (self.binding / 'xo.json').write_text(json.dumps(
            {'billet': 'xo', 'principal': {'seat': XO}}))
        self.config_path = self.base / 'config.json'
        self.config = {
            'schema_version': 1,
            'programme': 'vacuum-float',
            'map_version': 'map-v0',
            'rubric_version': 'v0',
            'verifier_billet': 'xo',
            'verifier_seats': [XO],
            'admiral_seats': [ADM],
            'binding_dir': str(self.binding),
            'submissions_dir': str(self.submissions),
            'programme_start': {'anchor': 'accepted-execution-order',
                                'id': 'SYN-ORDER-1', 'at': ANCHOR_AT},
            'scoring': {'caps_window': 'rolling-168h-utc'},
            'cost': {'ratio_basis': 'UNSET', 'interval': 'UNSET'},
        }
        self.flush_config()
        self._counter = 0

    def flush_config(self, **overrides):
        cfg = dict(self.config)
        cfg.update(overrides)
        self.config_path.write_text(json.dumps(cfg, indent=1))

    def close(self):
        shutil.rmtree(self.base, ignore_errors=True)

    # -- fixtures ----------------------------------------------------------

    def file_submission(self, submission_id, *, from_seat, at, scope=None,
                        artifacts=None, lane='builder-b', kind='report', model=''):
        record = {
            'id': submission_id,
            'kind': kind,
            'from_seat': from_seat,
            'to': 'someone',
            'at': at,
            'body': 'synthetic fixture body',
        }
        if model:
            record['model'] = model
        if lane:
            record['lane'] = lane
        if scope is not None:
            record['scope'] = scope
        if artifacts is not None:
            record['artifacts'] = artifacts
        path = self.submissions / f'{submission_id}.json'
        path.write_text(json.dumps(record, indent=1))
        return submission_id

    def award(self, submission_id, *, from_seat=XO, at, lane='builder-b',
              model='', **block):
        block.setdefault('kind', 'map-point')
        scope = {'programme': 'vacuum-float', 'award': block}
        return self.file_submission(submission_id, from_seat=from_seat, at=at,
                                    lane=lane, scope=scope, model=model)

    # -- driving the tool --------------------------------------------------

    def run(self, *argv):
        full = ['--ledger', str(self.ledger), '--config', str(self.config_path),
                *argv]
        rc = fp.main(full)
        return rc

    def ingest(self, *submission_ids, now='2026-10-18T12:00:00+00:00'):
        return self.run('ingest', *sum((['--id', s] for s in submission_ids), []),
                        '--now', now)

    def scoreboard_json(self, now='2026-10-18T12:00:00+00:00'):
        events, _torn = fp.Ledger(self.ledger, json.loads(self.config_path.read_text())).read_events()
        state = json.loads((self.ledger / 'ledger-state.json').read_text())
        cfg = json.loads(self.config_path.read_text())
        return fp.scoreboard(fp.derive(events, cfg, state), cfg, generated_at=now,
                             state=state)

    def scoreboard_run(self, now):
        """Run the scoreboard verb (a regeneration) and return its JSON."""
        out = self.base / 'board.json'
        self.run('scoreboard', '--json-out', str(out), '--now', now)
        return json.loads(out.read_text())

    def events(self):
        events, _torn = fp.Ledger(self.ledger, json.loads(self.config_path.read_text())).read_events()
        return events


class EmptyState(unittest.TestCase):
    def setUp(self):
        self.h = Habitat()

    def tearDown(self):
        self.h.close()

    def test_empty_ledger_is_honestly_empty(self):
        board = self.h.scoreboard_json()
        self.assertEqual(board['margin'], {'value': None, 'status': 'UNVERIFIED'})
        self.assertEqual(board['material_gap_pct'], {'value': None, 'status': 'UNKNOWN'})
        self.assertEqual(board['validated_map_points'], 0)
        self.assertIsNone(board['cost_per_verified_point'])
        self.assertIn('no verified map point', board['missing_data'][0])
        line = fp.scoreboard_line(board)
        self.assertIn('UNVERIFIED', line)
        self.assertIn('UNKNOWN', line)
        self.assertNotIn('+10', line)
        state = json.loads((self.h.ledger / 'ledger-state.json').read_text())
        self.assertEqual(state['activation']['state'], 'ACTIVATION BLOCKED')

    def test_selfcheck_ok_on_empty_ledger(self):
        rc = self.h.run('selfcheck')
        self.assertEqual(rc, 0)


class Authority(unittest.TestCase):
    def setUp(self):
        self.h = Habitat()

    def tearDown(self):
        self.h.close()

    def test_builder_award_block_is_a_nomination_not_an_award(self):
        self.h.award('SYN-B1', from_seat=BUILDER, at=ANCHOR_AT,
                     kind='map-point', points=10,
                     result={'margin': 12.5, 'units': '%'})
        self.h.ingest('SYN-B1')
        events = self.h.events()
        self.assertEqual(events[0]['event_type'], 'nomination')
        self.assertFalse(events[0]['verified'])
        self.assertEqual(events[0]['points'], 0)
        board = self.h.scoreboard_json()
        self.assertEqual(board['margin']['value'], None)
        self.assertEqual(len(board['unverified_nominations']), 1)
        self.assertIn('not a verifier seat', board['unverified_nominations'][0]['reason'])

    def test_points_mismatch_stays_a_nomination(self):
        self.h.award('SYN-X1', at=ANCHOR_AT, kind='map-point', points=25,
                     result={'margin': 1.0, 'units': '%'})
        self.h.ingest('SYN-X1')
        events = self.h.events()
        self.assertEqual(events[0]['event_type'], 'nomination')
        self.assertIn('rubric', events[0]['note'])

    def test_verifier_award_via_scope_block_credits_and_moves_margin(self):
        self.h.award('SYN-X2', at='2026-10-18T01:00:00+00:00',
                     kind='map-point', points=10,
                     result={'margin': 4.2, 'material_gap_pct': 61.0, 'units': '%'})
        self.h.ingest('SYN-X2')
        board = self.h.scoreboard_json()
        self.assertEqual(board['margin']['value'], 4.2)
        self.assertEqual(board['material_gap_pct']['value'], 61.0)
        self.assertEqual(board['lanes']['builder-b']['points'], 10)

    def test_award_via_sha_verified_artifact(self):
        art = {'type': 'vacuum-float-award', 'kind': 'benchmark', 'points': 15,
               'benchmark_key': 'SYN-BENCH-1', 'lane': 'builder-a'}
        art_path = self.h.submissions / 'SYN-ART-1.json'
        blob = json.dumps(art).encode()
        import hashlib
        self.h.file_submission('SYN-X3', from_seat=XO, at='2026-10-18T02:00:00+00:00',
                               lane=None,
                               artifacts=[{'path': str(art_path),
                                           'sha256': hashlib.sha256(blob).hexdigest()}])
        art_path.write_bytes(blob)
        self.h.ingest('SYN-X3')
        board = self.h.scoreboard_json()
        self.assertEqual(board['lanes']['builder-a']['points'], 15)

    def test_artifact_with_wrong_sha_is_not_trusted(self):
        art = {'type': 'vacuum-float-award', 'kind': 'map-point', 'points': 10}
        art_path = self.h.submissions / 'SYN-ART-2.json'
        art_path.write_text(json.dumps(art))
        self.h.file_submission('SYN-X4', from_seat=XO, at='2026-10-18T03:00:00+00:00',
                               lane=None,
                               artifacts=[{'path': str(art_path),
                                           'sha256': '0' * 64}])
        self.h.ingest('SYN-X4')
        board = self.h.scoreboard_json()
        self.assertEqual(board['validated_map_points'], 0)
        self.assertEqual(board['unverified_nominations'][0]['reason'],
                         'nomination: no explicit typed block (neither scope.award nor a '
                         'sha-matching vacuum-float-award artifact)')

    def test_verifier_resolved_from_binding_and_history_preserved(self):
        # A successor binding still accepts the historical verifier seat, and
        # the binding principal is accepted without being configured.
        (self.h.binding / 'xo.json').write_text(json.dumps(
            {'billet': 'xo', 'principal': {'seat': 'SYN-XO-SUCCESSOR'}}))
        self.h.award('SYN-X5', from_seat='SYN-XO-SUCCESSOR', at='2026-10-18T04:00:00+00:00',
                     kind='map-point', points=10, result={'margin': 1.0, 'units': '%'})
        self.h.ingest('SYN-X5')
        self.assertEqual(self.h.scoreboard_json()['lanes']['builder-b']['points'], 10)
        # historical seat still authoritative after succession
        self.h.award('SYN-X6', from_seat=XO, at='2026-10-18T05:00:00+00:00',
                     kind='material-card', points=5)
        self.h.ingest('SYN-X6')
        self.assertEqual(self.h.scoreboard_json()['lanes']['builder-b']['points'], 15)


class AppendOnly(unittest.TestCase):
    def setUp(self):
        self.h = Habitat()
        self.h.award('SYN-X10', at='2026-10-18T01:00:00+00:00',
                     kind='map-point', points=10, result={'margin': 2.0, 'units': '%'})
        self.h.ingest('SYN-X10')

    def tearDown(self):
        self.h.close()

    def test_identical_replay_is_a_noop(self):
        raw_before = (self.h.ledger / 'events.jsonl').read_text()
        self.h.ingest('SYN-X10')
        self.assertEqual((self.h.ledger / 'events.jsonl').read_text(), raw_before)
        self.assertEqual(self.h.scoreboard_json()['lanes']['builder-b']['points'], 10)

    def test_conflicting_payload_under_same_id_is_refused(self):
        # Same accepted id is immutable in the real queue; the ledger still
        # enforces the invariant against any regeneration path.
        self.assertEqual(self.h.run('selfcheck'), 0)  # sanity: current ledger is clean
        original = json.loads((self.h.ledger / 'events.jsonl').read_text().splitlines()[0])
        mutated = dict(original)
        mutated['points'] = 25
        # Direct conflicting append is flagged by selfcheck ...
        (self.h.ledger / 'events.jsonl').open('a').write(
            fp.canonical_json(mutated) + '\n')
        self.assertEqual(self.h.run('selfcheck'), 1)
        # ... and derive() never double-credits the mutated duplicate
        self.assertEqual(self.h.run('repair-tail'), 0)
        (self.h.ledger / 'events.jsonl').open('a').write(
            fp.canonical_json(mutated) + '\n')
        self.assertEqual(self.h.scoreboard_json()['lanes']['builder-b']['points'], 10)

    def test_correction_appends_and_original_is_preserved(self):
        target = self.h.events()[0]['event_id']
        self.h.award('SYN-X11', at='2026-10-18T06:00:00+00:00', lane='builder-b',
                     kind='correction', target_event_id=target, action='amend',
                     new_points=7, reason='synthetic amendment')
        self.h.ingest('SYN-X11')
        raw = (self.h.ledger / 'events.jsonl').read_text().splitlines()
        self.assertEqual(len(raw), 2)
        original = json.loads(raw[0])
        self.assertEqual(original['points'], 10)  # bytes untouched
        board = self.h.scoreboard_json()
        self.assertEqual(board['lanes']['builder-b']['points'], 7)

    def test_revoke_removes_credit_without_erasing_history(self):
        target = self.h.events()[0]['event_id']
        self.h.award('SYN-X12', at='2026-10-18T07:00:00+00:00', lane='builder-b',
                     kind='correction', target_event_id=target, action='revoke')
        self.h.ingest('SYN-X12')
        board = self.h.scoreboard_json()
        self.assertEqual(board['lanes']['builder-b']['points'], 0)
        self.assertEqual(len(self.h.events()), 2)  # original still present

    def test_correction_of_unknown_target_is_refused(self):
        self.h.award('SYN-X13', at='2026-10-18T08:00:00+00:00', lane='builder-b',
                     kind='correction', target_event_id='q-SYN-NOWHERE',
                     action='revoke')
        self.h.ingest('SYN-X13')
        self.assertEqual(len(self.h.events()), 1)

    def test_torn_tail_is_uncommitted_and_repairable(self):
        raw = (self.h.ledger / 'events.jsonl').read_text()
        with (self.h.ledger / 'events.jsonl').open('a') as fh:
            fh.write('{"event_id": "q-SYN-TORN", "points": 999')  # no newline, invalid json
        board = self.h.scoreboard_json()
        self.assertEqual(board['lanes']['builder-b']['points'], 10)  # torn line not counted
        rc = self.h.run('selfcheck')
        self.assertEqual(rc, 1)
        self.h.run('repair-tail')
        self.assertEqual((self.h.ledger / 'events.jsonl').read_text(), raw)
        self.assertEqual(self.h.run('selfcheck'), 0)


class CapsAndUniqueness(unittest.TestCase):
    def setUp(self):
        self.h = Habitat()

    def tearDown(self):
        self.h.close()

    def _falsifications(self, count, start='2026-10-19T01:00:00+00:00', hours=1):
        # count awards, `hours` apart, starting at `start` (all synthetic UTC instants)
        base = fp.parse_iso(start, what='fixture')
        for i in range(count):
            at = (base + dt.timedelta(hours=hours * i)).isoformat()
            self.h.award(f'SYN-F{i}', at=at, kind='falsification', points=10)
            self.h.ingest(f'SYN-F{i}')

    def test_falsification_rolling_cap_three(self):
        self._falsifications(4)
        board = self.h.scoreboard_json()
        self.assertEqual(board['lanes']['builder-b']['points'], 30)
        uncredited = board['lanes']['builder-b']['uncredited']
        self.assertEqual(len(uncredited), 1)
        self.assertIn('over-cap', uncredited[0]['reason'])
        self.assertIn('rolling 168 h', uncredited[0]['reason'])

    def test_cap_boundary_is_rolling_and_exact(self):
        # three admitted at T0, T0+1h, T0+2h; a fourth exactly 168 h after the
        # FIRST is still inside the closed window ending at its instant
        t0 = fp.parse_iso('2026-10-18T00:00:00+00:00', what='fixture')
        self._falsifications(3, start=t0.isoformat(), hours=1)
        edge = t0 + dt.timedelta(hours=168)
        self.h.award('SYN-FE', at=edge.isoformat(), kind='falsification', points=10)
        self.h.ingest('SYN-FE')
        board = self.h.scoreboard_json()
        self.assertEqual(len(board['lanes']['builder-b']['uncredited']), 1)
        # one second past the boundary the FIRST has aged out, but the
        # over-cap boundary event still occupies the window: stacking never
        # outruns the cap
        near = edge + dt.timedelta(seconds=1)
        self.h.award('SYN-FN', at=near.isoformat(), kind='falsification', points=10)
        self.h.ingest('SYN-FN')
        board = self.h.scoreboard_json()
        self.assertEqual(len(board['lanes']['builder-b']['uncredited']), 2)
        self.assertEqual(board['lanes']['builder-b']['points'], 30)
        # only when the whole shadow ages out does the window reopen
        clear = edge + dt.timedelta(hours=168, seconds=1)
        self.h.award('SYN-FC', at=clear.isoformat(), kind='falsification', points=10)
        self.h.ingest('SYN-FC')
        board = self.h.scoreboard_json()
        self.assertEqual(len(board['lanes']['builder-b']['uncredited']), 2)
        self.assertEqual(board['lanes']['builder-b']['points'], 40)

    def test_over_cap_event_still_occupies_its_window(self):
        # five in a row: the 4th and 5th score 0, and the 5th is over-cap
        # because the over-cap 4th still counts as verified in the window
        self._falsifications(5)
        board = self.h.scoreboard_json()
        self.assertEqual(board['lanes']['builder-b']['points'], 30)
        self.assertEqual(len(board['lanes']['builder-b']['uncredited']), 2)

    def test_caps_are_per_lane_not_programme_wide(self):
        for i in range(4):
            self.h.award(f'SYN-FA{i}', at=f'2026-10-19T0{i + 1}:00:00+00:00',
                         lane='builder-a', kind='falsification', points=10)
            self.h.ingest(f'SYN-FA{i}')
        # builder-b's window is untouched by builder-a's capped events
        self._falsifications(3)
        board = self.h.scoreboard_json()
        self.assertEqual(board['lanes']['builder-a']['points'], 30)
        self.assertEqual(board['lanes']['builder-b']['points'], 30)
        self.assertEqual(len(board['lanes']['builder-a']['uncredited']), 1)
        self.assertEqual(len(board['lanes']['builder-b']['uncredited']), 0)

    def test_benchmark_once_ever_regardless_of_ids(self):
        for i, at in enumerate(['2026-10-18T01:00:00+00:00', '2026-10-25T01:00:00+00:00',
                                '2026-11-01T01:00:00+00:00']):
            self.h.award(f'SYN-K{i}', at=at, kind='benchmark', points=15,
                         benchmark_key='SYN-BENCH-SAME')
            self.h.ingest(f'SYN-K{i}')
        board = self.h.scoreboard_json()
        self.assertEqual(board['lanes']['builder-b']['points'], 15)
        self.assertEqual(len(board['lanes']['builder-b']['uncredited']), 2)

    def test_map_version_rollover_does_not_regrant_benchmark_credit(self):
        self.h.award('SYN-K0', at='2026-10-18T01:00:00+00:00', kind='benchmark',
                     points=15, benchmark_key='SYN-BENCH-ROLL')
        self.h.ingest('SYN-K0')
        self.h.award('SYN-M0', at='2026-10-18T02:00:00+00:00', lane='builder-b',
                     kind='map-version', map_version='map-v1')
        self.h.ingest('SYN-M0')
        self.h.award('SYN-K1', at='2026-10-18T03:00:00+00:00', kind='benchmark',
                     points=15, benchmark_key='SYN-BENCH-ROLL')
        self.h.ingest('SYN-K1')
        board = self.h.scoreboard_json()
        self.assertEqual(board['map_version'], 'map-v1')
        self.assertEqual(board['lanes']['builder-b']['points'], 15)
        self.assertEqual(board['lanes']['builder-b']['prior_map_points'], 15)
        self.assertEqual(board['lanes']['builder-b']['current_map_points'], 0)

    def test_material_card_rolling_cap_five(self):
        for i in range(6):
            self.h.award(f'SYN-C{i}', at=f'2026-10-20T0{i + 1}:00:00+00:00',
                         kind='material-card', points=5)
            self.h.ingest(f'SYN-C{i}')
        board = self.h.scoreboard_json()
        self.assertEqual(board['lanes']['builder-b']['points'], 25)


class AuditZero(unittest.TestCase):
    def setUp(self):
        self.h = Habitat()
        for lane, at in (('builder-a', '2026-10-18T01:00:00+00:00'),
                         ('builder-b', '2026-10-18T02:00:00+00:00')):
            self.h.award(f'SYN-A-{lane}', at=at, lane=lane, kind='map-point',
                         points=10, result={'margin': 1.0, 'units': '%'})
            self.h.ingest(f'SYN-A-{lane}')

    def tearDown(self):
        self.h.close()

    def test_zeroes_only_named_lane_current_map(self):
        # audit-zero is a control event: an explicit block with lane + map_version
        self.h.file_submission('SYN-Z1', from_seat=XO, at='2026-10-18T03:00:00+00:00',
                               lane='builder-a',
                               scope={'programme': 'vacuum-float', 'award': {
                                   'kind': 'audit-zero', 'lane': 'builder-a',
                                   'map_version': 'map-v0'}})
        self.h.ingest('SYN-Z1')
        board = self.h.scoreboard_json()
        self.assertEqual(board['lanes']['builder-a']['current_map_points'], 0)
        self.assertEqual(board['lanes']['builder-a']['points'], 0)
        self.assertEqual(board['lanes']['builder-b']['points'], 10)
        # history preserved: both award events still in the ledger
        self.assertEqual(len(self.h.events()), 3)

    def test_zero_filed_before_a_later_rollover_still_applies(self):
        # replay must reconstruct the map CURRENT AT EACH EVENT (the log's
        # starting map version), not evaluate old filings against the final
        # map: audit-zero(v0) followed by map-version(v1) zeroes v0's balance
        self.h.file_submission('SYN-Z3', from_seat=XO, at='2026-10-18T03:00:00+00:00',
                               lane='builder-a',
                               scope={'programme': 'vacuum-float', 'award': {
                                   'kind': 'audit-zero', 'lane': 'builder-a',
                                   'map_version': 'map-v0'}})
        self.h.ingest('SYN-Z3')
        self.h.file_submission('SYN-M9', from_seat=XO, at='2026-10-18T04:00:00+00:00',
                               lane='builder-a',
                               scope={'programme': 'vacuum-float', 'award': {
                                   'kind': 'map-version', 'map_version': 'map-v1'}})
        self.h.ingest('SYN-M9')
        board = self.h.scoreboard_json()
        self.assertEqual(board['lanes']['builder-a']['points'], 0)
        self.assertEqual(board['lanes']['builder-a']['map_points'], 0)
        self.assertEqual(board['lanes']['builder-a']['zeroed_by'], 'q-SYN-Z3')

    def test_stale_map_reference_does_not_target_newer_map(self):
        self.h.file_submission('SYN-M1', from_seat=XO, at='2026-10-18T02:30:00+00:00',
                               lane='builder-a',
                               scope={'programme': 'vacuum-float', 'award': {
                                   'kind': 'map-version', 'map_version': 'map-v1'}})
        self.h.ingest('SYN-M1')
        self.h.file_submission('SYN-Z2', from_seat=XO, at='2026-10-18T04:00:00+00:00',
                               lane='builder-a',
                               scope={'programme': 'vacuum-float', 'award': {
                                   'kind': 'audit-zero', 'lane': 'builder-a',
                                   'map_version': 'map-v0'}})
        self.h.ingest('SYN-Z2')
        board = self.h.scoreboard_json()
        self.assertEqual(board['map_version'], 'map-v1')
        # prior map's points preserved; the stale audit never touched map-v1
        self.assertEqual(board['lanes']['builder-a']['prior_map_points'], 10)
        self.assertEqual(board['lanes']['builder-a']['current_map_points'], 0)
        reasons = ' '.join(u['reason'] for u in board['unverified_nominations'])
        self.assertIn('NOT applied to a newer map', reasons)


class RubricChanges(unittest.TestCase):
    def setUp(self):
        self.h = Habitat()

    def tearDown(self):
        self.h.close()

    def _rubric_change(self, sid, at, version='v1', approvals=None):
        self.h.file_submission(sid, from_seat=XO, at=at, lane='builder-b',
                               scope={'programme': 'vacuum-float', 'award': {
                                   'kind': 'rubric-change', 'rubric_version': version,
                                   'approvals': approvals or []}})

    def test_requires_admiral_approval_record(self):
        self._rubric_change('SYN-R0', '2026-10-18T01:00:00+00:00')
        self.h.ingest('SYN-R0')
        events = self.h.events()
        self.assertEqual(events[0]['event_type'], 'nomination')
        self.assertIn('Admiral-seat', events[0]['note'])

    def test_dual_approval_applies_once(self):
        self.h.file_submission('SYN-R-ADM', from_seat=ADM, at='2026-10-18T01:00:00+00:00',
                               kind='acknowledgment')
        self._rubric_change('SYN-R1', '2026-10-18T02:00:00+00:00',
                            approvals=[{'id': 'SYN-R-ADM'}])
        self.h.ingest('SYN-R1')
        state = json.loads((self.h.ledger / 'ledger-state.json').read_text())
        self.assertEqual(state['rubric_version'], 'v1')
        board = self.h.scoreboard_json()
        self.assertEqual(board['rubric_version'], 'v1')

    def test_one_change_per_map_version_and_forward_only(self):
        self.h.file_submission('SYN-R-ADM', from_seat=ADM, at='2026-10-18T01:00:00+00:00',
                               kind='acknowledgment')
        self._rubric_change('SYN-R1', '2026-10-18T02:00:00+00:00',
                            approvals=[{'id': 'SYN-R-ADM'}])
        self.h.ingest('SYN-R1')
        # a second change in the same map version is refused
        self.h.file_submission('SYN-R-ADM2', from_seat=ADM, at='2026-10-18T03:00:00+00:00',
                               kind='acknowledgment')
        self._rubric_change('SYN-R2', '2026-10-18T04:00:00+00:00', version='v2',
                            approvals=[{'id': 'SYN-R-ADM2'}])
        self.h.ingest('SYN-R2')
        state = json.loads((self.h.ledger / 'ledger-state.json').read_text())
        self.assertEqual(state['rubric_version'], 'v1')
        # a non-advancing version is refused even in a fresh map version
        self.h.file_submission('SYN-M1', from_seat=XO, at='2026-10-18T05:00:00+00:00',
                               lane='builder-b',
                               scope={'programme': 'vacuum-float', 'award': {
                                   'kind': 'map-version', 'map_version': 'map-v1'}})
        self.h.ingest('SYN-M1')
        self.h.file_submission('SYN-R-ADM3', from_seat=ADM, at='2026-10-18T06:00:00+00:00',
                               kind='acknowledgment')
        self._rubric_change('SYN-R3', '2026-10-18T07:00:00+00:00', version='v1',
                            approvals=[{'id': 'SYN-R-ADM3'}])
        self.h.ingest('SYN-R3')
        state = json.loads((self.h.ledger / 'ledger-state.json').read_text())
        self.assertEqual(state['rubric_version'], 'v1')
        self.assertEqual(state['map_version'], 'map-v1')


class CostAccounting(unittest.TestCase):
    def setUp(self):
        self.h = Habitat()

    def tearDown(self):
        self.h.close()

    def _cost(self, sid, at, tokens, coverage, lane='builder-b', session='SYN-SESSION-1',
              bucket='lane', role='', model='syn-model'):
        self.h.file_submission(sid, from_seat=BUILDER, at=at, lane=lane, model=model,
                               scope={'programme': 'vacuum-float', 'award': {
                                   'kind': 'cost-update',
                                   'result': {'tokens': tokens, 'coverage': coverage,
                                              'session': session, 'bucket': bucket,
                                              'role': role,
                                              'interval': {'from': at, 'to': at}}}})

    def test_unmeasured_session_is_named_not_zero_filled(self):
        self._cost('SYN-C1', '2026-10-18T01:00:00+00:00', None, 'unmeasured',
                   session='SYN-SESS-UNREADABLE')
        self.h.ingest('SYN-C1')
        board = self.h.scoreboard_json()
        self.assertEqual(board['measured_tokens_per_lane'], {})
        self.assertEqual(len(board['unmeasured_sessions']), 1)
        self.assertEqual(board['unmeasured_sessions'][0]['session'], 'SYN-SESS-UNREADABLE')
        self.assertIn('SYN-SESS-UNREADABLE', board['coverage_line'])
        self.assertIn('measured 0 of 1', board['coverage_line'])
        self.assertIsNone(board['cost_per_verified_point'])
        self.assertIn('separately', board['cost_per_verified_point_note'])

    def test_zero_points_means_unavailable_ratio_even_with_agreed_basis(self):
        self.h.flush_config(**{'cost': {'ratio_basis': 'agreed', 'interval': 'SYN'}})
        self._cost('SYN-C2', '2026-10-18T01:00:00+00:00', 12_000_000, 'measured')
        self.h.ingest('SYN-C2')
        board = self.h.scoreboard_json()
        self.assertEqual(board['measured_tokens_per_lane'], {'builder-b': 12_000_000})
        self.assertIsNone(board['cost_per_verified_point'])
        self.assertIn('zero admitted map points', board['cost_per_verified_point_note'])

    def test_measured_zero_cost_is_distinct_from_unknown(self):
        self._cost('SYN-C3', '2026-10-18T01:00:00+00:00', 0, 'measured')
        self.h.ingest('SYN-C3')
        board = self.h.scoreboard_json()
        self.assertEqual(board['measured_tokens_per_lane'], {'builder-b': 0})
        self.assertEqual(board['unmeasured_sessions'], [])
        self.assertEqual(board['coverage_line'], 'measured 1 of 1 known sessions')

    def test_same_session_snapshots_dedup_latest_wins(self):
        # cumulative snapshots of ONE session: the latest reading stands,
        # redelivery of an older snapshot never re-adds
        self._cost('SYN-C4', '2026-10-18T01:00:00+00:00', 10_000_000, 'measured')
        self._cost('SYN-C5', '2026-10-19T01:00:00+00:00', 14_000_000, 'measured')
        self._cost('SYN-C5B', '2026-10-19T02:00:00+00:00', 14_000_000, 'measured')  # redelivery
        self._cost('SYN-C5C', '2026-10-18T06:00:00+00:00', 11_000_000, 'measured')  # stale
        self.h.ingest('SYN-C4', 'SYN-C5', 'SYN-C5B', 'SYN-C5C')
        board = self.h.scoreboard_json()
        self.assertEqual(board['measured_tokens_per_lane'], {'builder-b': 14_000_000})
        self.assertEqual(board['token_accounting']['builder-b']['measured_sessions'], 1)

    def test_sessions_sum_per_lane_and_split_per_model(self):
        self._cost('SYN-S1', '2026-10-18T01:00:00+00:00', 20_000_000, 'measured',
                   session='SYN-SESS-A', model='syn-model-a')
        self._cost('SYN-S2', '2026-10-18T02:00:00+00:00', 30_000_000, 'measured',
                   session='SYN-SESS-B', model='syn-model-b')
        self.h.ingest('SYN-S1', 'SYN-S2')
        board = self.h.scoreboard_json()
        self.assertEqual(board['measured_tokens_per_lane'], {'builder-b': 50_000_000})
        self.assertEqual(board['measured_tokens_per_lane_model'],
                         {'builder-b · syn-model-a': 20_000_000,
                          'builder-b · syn-model-b': 30_000_000})

    def test_overhead_usage_is_excluded_from_lanes_and_shown_beside(self):
        self._cost('SYN-O1', '2026-10-18T01:00:00+00:00', 99_000_000, 'measured',
                   session='SYN-SESS-SCORER', bucket='overhead', role='scorer')
        self._cost('SYN-O2', '2026-10-18T02:00:00+00:00', 7_000_000, 'measured',
                   session='SYN-SESS-CO', bucket='overhead', role='co')
        self._cost('SYN-O3', '2026-10-18T03:00:00+00:00', 4_000_000, 'measured',
                   session='SYN-SESS-LANE')
        self.h.ingest('SYN-O1', 'SYN-O2', 'SYN-O3')
        board = self.h.scoreboard_json()
        self.assertEqual(board['measured_tokens_per_lane'], {'builder-b': 4_000_000})
        overhead = board['programme_overhead_tokens']
        self.assertEqual(overhead['total'], 106_000_000)
        self.assertEqual(overhead['by_role'], {'scorer': 99_000_000, 'co': 7_000_000})
        # the lane keeps only its own session; no crossing from overhead
        self.assertEqual(board['token_accounting']['builder-b']['measured_tokens'],
                         4_000_000)

    def test_crossings_observed_at_regeneration_and_never_auto_awarded(self):
        self._cost('SYN-X1', '2026-10-18T01:00:00+00:00', 250_000_000, 'measured')
        self.h.ingest('SYN-X1')
        board = self.h.scoreboard_run('2026-10-18T06:00:00+00:00')
        acct = board['token_accounting']['builder-b']
        self.assertEqual(acct['crossings_observable'], 2)
        self.assertEqual(acct['crossings_observed'], 2)
        self.assertEqual(acct['penalty_events_awarded'], 0)
        self.assertEqual(len(acct['pending_crossings']), 2)
        # never auto-awarded: no scored lane exists and nothing was minted
        self.assertNotIn('builder-b', board['lanes'])
        self.assertEqual(board['validated_map_points'], 0)
        state = json.loads((self.h.ledger / 'ledger-state.json').read_text())
        self.assertEqual(state['token_crossings']['builder-b']['1']['observed_at'],
                         '2026-10-18T06:00:00+00:00')
        self.assertEqual(state['token_crossings']['builder-b']['1']['map_version'],
                         'map-v0')
        self.assertEqual(acct['remainder_tokens'], 50_000_000)

    def test_observation_date_is_recorded_once_never_rewritten(self):
        self._cost('SYN-X2', '2026-10-18T01:00:00+00:00', 120_000_000, 'measured')
        self.h.ingest('SYN-X2')
        self.h.scoreboard_run('2026-10-18T06:00:00+00:00')
        # a later regeneration must not move the recorded observation date
        self.h.scoreboard_run('2026-10-20T06:00:00+00:00')
        state = json.loads((self.h.ledger / 'ledger-state.json').read_text())
        self.assertEqual(state['token_crossings']['builder-b']['1']['observed_at'],
                         '2026-10-18T06:00:00+00:00')

    def test_late_found_record_adds_its_crossing_when_found(self):
        self._cost('SYN-X3', '2026-10-18T01:00:00+00:00', 80_000_000, 'measured',
                   session='SYN-SESS-EARLY')
        self.h.ingest('SYN-X3')
        self.h.scoreboard_run('2026-10-18T06:00:00+00:00')
        board = json.loads((self.h.base / 'board.json').read_text())
        self.assertEqual(board['token_accounting']['builder-b']['crossings_observable'], 0)
        # the late-found record is ingested much later; its crossing counts
        # from the regeneration that first sees it, never backdated
        self._cost('SYN-X4', '2026-10-18T02:00:00+00:00', 90_000_000, 'measured',
                   session='SYN-SESS-LATE')
        self.h.ingest('SYN-X4', now='2026-10-25T12:00:00+00:00')
        board = self.h.scoreboard_run('2026-10-25T13:00:00+00:00')
        acct = board['token_accounting']['builder-b']
        self.assertEqual(acct['crossings_observable'], 1)
        pending = acct['pending_crossings']
        self.assertEqual(pending[0]['crossing'], 1)
        self.assertEqual(pending[0]['observed_at'], '2026-10-25T13:00:00+00:00')

    def test_una_award_clears_the_pending_crossing(self):
        self._cost('SYN-X5', '2026-10-18T01:00:00+00:00', 100_000_000, 'measured')
        self.h.ingest('SYN-X5')
        board = self.h.scoreboard_run('2026-10-18T06:00:00+00:00')
        self.assertEqual(len(board['token_accounting']['builder-b']['pending_crossings']), 1)
        self.h.award('SYN-T1', at='2026-10-18T07:00:00+00:00', kind='tokens-100m',
                     points=-1, units=1)
        self.h.ingest('SYN-T1')
        board = self.h.scoreboard_json()
        acct = board['token_accounting']['builder-b']
        self.assertEqual(acct['penalty_events_awarded'], 1)
        self.assertEqual(acct['pending_crossings'], [])
        self.assertEqual(board['lanes']['builder-b']['points'], -1)

    def test_cost_update_never_awards_the_token_penalty(self):
        self._cost('SYN-C6', '2026-10-18T01:00:00+00:00', 300_000_000, 'measured')
        self.h.ingest('SYN-C6')
        board = self.h.scoreboard_json()
        self.assertEqual(board['validated_map_points'], 0)
        # a lane with only cost entries has no scored lane at all
        self.assertNotIn('builder-b', board['lanes'])
        self.assertIn('Una-verified', board['token_penalty_note'])

    def test_token_penalty_is_a_verifier_award(self):
        self.h.award('SYN-T2', at='2026-10-18T01:00:00+00:00', kind='tokens-100m',
                     points=-3, units=3)
        self.h.ingest('SYN-T2')
        self.assertEqual(self.h.scoreboard_json()['lanes']['builder-b']['points'], -3)


class HeartbeatAndStalls(unittest.TestCase):
    def setUp(self):
        self.h = Habitat()
        self.post_log = self.h.base / 'posted.log'
        self.post_cmd = ['/bin/sh', '-c', f'cat >> {self.post_log}']

    def tearDown(self):
        self.h.close()

    def _heartbeat(self, now):
        return self.h.run('heartbeat', '--now', now, '--post-command', *self.post_cmd)

    def _posted_lines(self):
        if not self.post_log.exists():
            return []
        return [ln for ln in self.post_log.read_text().splitlines() if ln.strip()]

    def _posted_payloads(self):
        return [json.loads(ln) for ln in self._posted_lines()]

    def _delivery(self):
        return json.loads((self.h.ledger / 'delivery-pending.json').read_text())

    def test_unchanged_line_causes_no_seat_work(self):
        self._heartbeat('2026-10-17T06:00:00+00:00')
        first = self._posted_lines()
        self.assertEqual(len(first), 1)
        self._heartbeat('2026-10-17T12:00:00+00:00')
        self._heartbeat('2026-10-17T18:00:00+00:00')
        self.assertEqual(len(self._posted_lines()), 1)  # unchanged: no new post

    def test_changed_line_posts_once(self):
        self._heartbeat('2026-10-17T06:00:00+00:00')
        self.h.award('SYN-H1', at='2026-10-17T07:00:00+00:00', kind='map-point',
                     points=10, result={'margin': 3.3, 'units': '%'})
        self.h.ingest('SYN-H1')
        self._heartbeat('2026-10-17T12:00:00+00:00')
        lines = self._posted_lines()
        self.assertEqual(len(lines), 2)
        self.assertIn('3.3', lines[1])

    # -- U3 bounded repair: four deterministic delivery regressions --------

    def test_sha8_collision_between_episodes_fails_closed(self):
        # U3-D1: sha8 is a digest prefix, never proof. A saved stall item
        # found under the id the current episode maps to, but carrying a
        # DIFFERENT episode key or notice type, is a collision: the run
        # fails closed before any write, the saved item is preserved
        # byte-identical, and nothing is posted for the colliding episode.
        import io
        import contextlib
        self._heartbeat('2026-10-19T08:00:00+00:00')  # anchor diagnosis due
        dpath = self.h.ledger / 'delivery-pending.json'
        doc = json.loads(dpath.read_text())
        nid = next(i for i, it in doc['items'].items()
                   if it['type'] == 'diagnosis-report')
        doc['items'][nid]['episode_key'] = 'episode-Z'  # forced collision
        dpath.write_text(json.dumps(doc, indent=1))
        before = dpath.read_bytes()
        posts_before = len(self._posted_lines())
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc = self._heartbeat('2026-10-19T10:00:00+00:00')
        self.assertEqual(rc, 2)
        self.assertIn('collision', err.getvalue())
        self.assertEqual(dpath.read_bytes(), before)   # nothing rewritten
        self.assertEqual(len(self._posted_lines()), posts_before)

    def test_corrupt_delivery_state_fails_closed(self):
        # U3-D4: unreadable delivery JSON is never an empty queue. The run
        # exits nonzero BEFORE any delivery write, the corrupt bytes stay
        # byte-identical, and no adapter call happens.
        import io
        import contextlib
        self._heartbeat('2026-10-17T06:00:00+00:00')  # real state first
        dpath = self.h.ledger / 'delivery-pending.json'
        corrupt = b'{"next_line_seq": 1, "items": {'   # truncated JSON
        dpath.write_bytes(corrupt)
        posts_before = len(self._posted_lines())
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc = self._heartbeat('2026-10-17T12:00:00+00:00')
        self.assertEqual(rc, 2)
        self.assertIn('not readable JSON', err.getvalue())
        self.assertEqual(dpath.read_bytes(), corrupt)  # byte-identical
        self.assertEqual(len(self._posted_lines()), posts_before)

    def test_wrong_delivery_schema_fails_closed(self):
        # U3-D4: parseable JSON that is not the delivery schema (wrong
        # container, non-integer sequence, item without id/type) fails the
        # same way: nonzero, bytes preserved, nothing posted.
        import io
        import contextlib
        self._heartbeat('2026-10-17T06:00:00+00:00')
        dpath = self.h.ledger / 'delivery-pending.json'
        posts_before = len(self._posted_lines())
        for bad in ('[1, 2, 3]',
                    '{"next_line_seq": "one", "items": {}}',
                    '{"next_line_seq": 1, "items": {"x": {"seq": 1}}}'):
            dpath.write_text(bad)
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                rc = self._heartbeat('2026-10-17T12:00:00+00:00')
            self.assertEqual(rc, 2, bad)
            self.assertIn('failing closed', err.getvalue(), bad)
            self.assertEqual(dpath.read_text(), bad)   # byte-identical
        self.assertEqual(len(self._posted_lines()), posts_before)

    def test_absent_delivery_state_initializes(self):
        # U3-D4 companion: only an ABSENT file initializes a fresh queue;
        # the baseline line posts normally and a retained state retries.
        self.assertFalse((self.h.ledger / 'delivery-pending.json').exists())
        rc = self._heartbeat('2026-10-17T06:00:00+00:00')
        self.assertEqual(rc, 0)
        self.assertEqual(len(self._posted_payloads()), 1)
        rc = self._heartbeat('2026-10-17T12:00:00+00:00')
        self.assertEqual(rc, 0)                     # retained: no re-post
        self.assertEqual(len(self._posted_payloads()), 1)

    def _seeded_delivery(self):
        """One real run first, so the state carries a genuine line item."""
        self._heartbeat('2026-10-17T06:00:00+00:00')
        return self.h.ledger / 'delivery-pending.json'

    def _rewrite(self, doc):
        import json as _json
        (self.h.ledger / 'delivery-pending.json').write_text(
            _json.dumps(doc, indent=1, sort_keys=True) + '\n')

    def test_non_boolean_admitted_fails_closed(self):
        # U3-D4: an admission flag that is not an exact boolean — the
        # string "false", "true", or a bare 1 — used to read as ADMITTED
        # (any truthy value), silently pulling the item out of due work
        # and into cursor recovery. The loader rejects it before any
        # read, use, write or recovery, bytes preserved, nothing posted.
        import io
        import contextlib
        dpath = self._seeded_delivery()
        posts_before = len(self._posted_lines())
        for bad in ('false', 'true', 1):
            doc = self._delivery()
            for item in doc['items'].values():
                item['admitted'] = bad
            self._rewrite(doc)
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                rc = self._heartbeat('2026-10-17T12:00:00+00:00')
            self.assertEqual(rc, 2, bad)
            self.assertIn('exact boolean', err.getvalue(), bad)
        self.assertEqual(len(self._posted_lines()), posts_before)

    def test_map_key_id_equality_fails_closed(self):
        # U3-D4: the items map is keyed by the item's own id; an entry
        # whose key and id disagree is corrupt identity, not pending work.
        import io
        import contextlib
        self._seeded_delivery()
        doc = self._delivery()
        some_key = sorted(doc['items'])[0]
        doc['items']['renamed-' + some_key] = doc['items'].pop(some_key)
        self._rewrite(doc)
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc = self._heartbeat('2026-10-17T12:00:00+00:00')
        self.assertEqual(rc, 2)
        self.assertIn('map key', err.getvalue())

    def test_line_sequence_shape_fails_closed(self):
        # U3-D4: a line's sequence must be a unique positive integer —
        # never a boolean (True == 1 collides with seq 1), a string, zero
        # or negative.
        import io
        import contextlib
        self._seeded_delivery()
        for bad in (True, '2', 0, -1):
            doc = self._delivery()
            for item in doc['items'].values():
                if item.get('type') == 'line':
                    item['seq'] = bad
            self._rewrite(doc)
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                rc = self._heartbeat('2026-10-17T12:00:00+00:00')
            self.assertEqual(rc, 2, bad)
            self.assertIn('positive integer', err.getvalue(), bad)

    def test_duplicate_line_sequence_fails_closed(self):
        # U3-D4: two line items sharing one sequence number is corrupt
        # allocation, never admitted evidence.
        import io
        import contextlib
        dpath = self._seeded_delivery()
        doc = self._delivery()
        clone_key = 'vf-line-1-dup'
        doc['items'][clone_key] = dict(doc['items'][sorted(doc['items'])[0]])
        doc['items'][clone_key]['id'] = clone_key
        self._rewrite(doc)
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc = self._heartbeat('2026-10-17T12:00:00+00:00')
        self.assertEqual(rc, 2)
        self.assertIn('duplicated', err.getvalue())

    def test_counter_below_existing_sequence_fails_closed(self):
        # U3-D4: next_line_seq below an existing line sequence would
        # allocate a used number again on the next line — reject before
        # any allocation.
        import io
        import contextlib
        self._seeded_delivery()
        doc = self._delivery()
        doc['next_line_seq'] = 0
        self._rewrite(doc)
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc = self._heartbeat('2026-10-17T12:00:00+00:00')
        self.assertEqual(rc, 2)
        self.assertIn('below', err.getvalue())

    def test_missing_per_type_fields_fail_closed(self):
        # U3-D4: each item type carries required fields — a line needs
        # seq and body, a diagnosis its episode key, a card its deadline.
        # Their absence is schema-invalid, not silently deferred work.
        import io
        import contextlib
        import copy
        self._seeded_delivery()
        # every case starts from a FRESH valid snapshot: a rejected file is
        # preserved byte-identical, so reusing the live document would let
        # one case's corruption mask the next case's intended field
        clean = copy.deepcopy(self._delivery())
        cases = (
            ({'id': 'vf-stall-a-48h', 'type': 'diagnosis-report',
              'created_at': 't', 'attempts': 0, 'admitted': False,
              'body': 'b'},                                  # no episode_key
             'episode_key'),
            ({'id': 'vf-stall-b-5d', 'type': 'admiral-decision-card',
              'created_at': 't', 'attempts': 0, 'admitted': False,
              'body': 'b', 'episode_key': 'e'},              # no deadline
             'deadline'),
            ({'id': 'vf-line-9-q', 'type': 'line', 'seq': 9,
              'created_at': 't', 'attempts': 0, 'admitted': False},  # no body
             'body'),
        )
        for extra, field in cases:
            doc = copy.deepcopy(clean)
            doc['items'][extra['id']] = dict(extra)
            self._rewrite(doc)
            err = io.StringIO()
            with contextlib.redirect_stderr(err):
                rc = self._heartbeat('2026-10-17T12:00:00+00:00')
            self.assertEqual(rc, 2, extra['id'])
            self.assertIn(f'lacks required field {field!r}', err.getvalue(),
                          extra['id'])

    def test_absent_admitted_flag_means_pending(self):
        # U3-D4 positive control: an item with NO admitted key at all is
        # valid pending work (meaningful absence) and is delivered —
        # exact-boolean validation must not reject the absent case.
        self._seeded_delivery()
        doc = self._delivery()
        for item in doc['items'].values():
            item.pop('admitted', None)
        self._rewrite(doc)
        rc = self._heartbeat('2026-10-17T12:00:00+00:00')
        self.assertEqual(rc, 0)

    def test_crash_between_admitted_write_and_cursor_posts_nothing_new(self):
        # U3-D3: the delivery state says seq 1 admitted but the heartbeat
        # cursor never advanced (crash between the two writes). Restart
        # recovers forward from the durable admitted sequence: no second
        # id for the unchanged line, no adapter call, run rc 0.
        self._heartbeat('2026-10-17T06:00:00+00:00')  # baseline admitted
        hb = self.h.ledger / 'heartbeat-state.json'
        doc = json.loads(hb.read_text())
        doc.pop('last_admitted_line', None)           # simulate the crash
        doc.pop('last_admitted_seq', None)
        hb.write_text(json.dumps(doc, indent=1))
        posts_before = len(self._posted_lines())
        rc = self._heartbeat('2026-10-17T12:00:00+00:00')
        self.assertEqual(rc, 0)
        self.assertEqual(len(self._posted_lines()), posts_before)
        self.assertEqual(len(self._delivery()['items']), 1)  # no fresh id
        recovered = json.loads(hb.read_text())
        self.assertEqual(recovered.get('last_admitted_seq'), 1)
        self.assertTrue(recovered.get('delivery_cursor_recovered_at'))

    def test_pending_crash_preserves_id_and_aba_posts_legitimate_changes(self):
        # U3-D3: a crash BEFORE admission leaves the pending id in place —
        # the retry posts under the SAME id — and a line that legitimately
        # evolves A -> B -> A posts each real change under a fresh id.
        self._heartbeat('2026-10-17T06:00:00+00:00')  # A: baseline admitted
        self.h.award('SYN-H5', at='2026-10-17T07:00:00+00:00', kind='map-point',
                     points=10, result={'margin': 4.4, 'units': '%'})
        self.h.ingest('SYN-H5')
        self._heartbeat('2026-10-17T12:00:00+00:00')  # B created, admitted
        dpath = self.h.ledger / 'delivery-pending.json'
        doc = json.loads(dpath.read_text())
        bid = next(i for i, it in doc['items'].items() if it.get('seq') == 2)
        # simulate the crash BEFORE B's admission write: item back to
        # pending, heartbeat cursor still on A
        doc['items'][bid]['admitted'] = False
        dpath.write_text(json.dumps(doc, indent=1))
        hb = self.h.ledger / 'heartbeat-state.json'
        hdoc = json.loads(hb.read_text())
        hdoc['last_admitted_line'] = next(
            it['body'] for it in doc['items'].values()
            if it.get('seq') == 1)
        hdoc['last_admitted_seq'] = 1
        hb.write_text(json.dumps(hdoc, indent=1))
        rc = self._heartbeat('2026-10-17T18:00:00+00:00')  # retry, same id
        self.assertEqual(rc, 0)
        payloads = self._posted_payloads()
        self.assertEqual(payloads[-1]['id'], bid)      # same id retried
        self.assertEqual(len(self._delivery()['items']), 2)
        # A again: remove the award event; the regressed line is a real
        # change and must post under a NEW id, not be suppressed by the
        # old A admission
        events = self.h.ledger / 'events.jsonl'
        kept = [ln for ln in events.read_text().splitlines()
                if 'SYN-H5' not in ln]
        events.write_text('\n'.join(kept) + '\n')
        rc = self._heartbeat('2026-10-17T20:00:00+00:00')
        self.assertEqual(rc, 0)
        payloads = self._posted_payloads()
        self.assertTrue(payloads[-1]['id'].startswith('vf-line-3'),
                        payloads[-1]['id'])
        self.assertEqual(len(self._delivery()['items']), 3)

    def test_stall_boundaries_and_idempotency(self):
        # anchor 2026-10-17T00:14:57-07:00 (= 07:14:57Z)
        self._heartbeat('2026-10-18T06:00:00+00:00')  # < 48h: nothing due
        notices = list((self.h.ledger / 'notices').glob('*.md'))
        self.assertEqual(notices, [])
        self._heartbeat('2026-10-19T08:00:00+00:00')  # > 48h: diagnosis due once
        notices = list((self.h.ledger / 'notices').glob('*diagnosis*.md'))
        self.assertEqual(len(notices), 1)
        self._heartbeat('2026-10-19T14:00:00+00:00')  # duplicate run: idempotent
        notices = list((self.h.ledger / 'notices').glob('*diagnosis*.md'))
        self.assertEqual(len(notices), 1)
        self._heartbeat('2026-10-22T08:00:00+00:00')  # > 5d: decision card once
        cards = list((self.h.ledger / 'notices').glob('*admiral-decision*.md'))
        self.assertEqual(len(cards), 1)
        self._heartbeat('2026-10-22T14:00:00+00:00')
        cards = list((self.h.ledger / 'notices').glob('*admiral-decision*.md'))
        self.assertEqual(len(cards), 1)
        card = cards[0].read_text()
        self.assertIn('DEFAULT: pause', card)

    def test_verified_point_resets_stall_and_retains_history(self):
        self._heartbeat('2026-10-19T08:00:00+00:00')  # diagnosis emitted
        self.h.award('SYN-H2', at='2026-10-19T09:00:00+00:00', kind='map-point',
                     points=10, result={'margin': 1.1, 'units': '%'})
        self.h.ingest('SYN-H2')
        self._heartbeat('2026-10-19T10:00:00+00:00')
        state = json.loads((self.h.ledger / 'heartbeat-state.json').read_text())
        # the anchor episode's emitted diagnosis is retained as history ...
        self.assertEqual(len(state['stall_episodes']), 1)
        anchor_key = next(iter(state['stall_episodes']))
        self.assertTrue(anchor_key.startswith('anchor:'))
        self.assertIn('diagnosis-report', state['stall_episodes'][anchor_key]['emitted'])
        # ... while the live clock now runs on the verified point, nothing due
        self.assertTrue(state['last_stall']['episode_key'].startswith('map-point:'))
        self.assertEqual(state['last_stall']['due'], [])

    def test_nomination_does_not_reset_stall(self):
        self._heartbeat('2026-10-19T08:00:00+00:00')
        self.h.award('SYN-H3', from_seat=BUILDER, at='2026-10-19T09:00:00+00:00',
                     kind='map-point', points=10, result={'margin': 1.1, 'units': '%'})
        self.h.ingest('SYN-H3')
        self._heartbeat('2026-10-19T10:00:00+00:00')
        state = json.loads((self.h.ledger / 'heartbeat-state.json').read_text())
        self.assertTrue(state['last_stall']['episode_key'].startswith('anchor:'))
        self.assertIn('diagnosis-report', state['last_stall']['due'])

    def test_failed_delivery_pending_then_success_then_noop(self):
        marker = self.h.base / 'go.marker'
        fail_until_marker = ['/bin/sh', '-c',
                             f'test -f {marker} && cat >> {self.post_log}']
        self.post_cmd = fail_until_marker
        rc1 = self._heartbeat('2026-10-17T06:00:00+00:00')
        delivery = self._delivery()
        state = json.loads((self.h.ledger / 'heartbeat-state.json').read_text())
        self.assertEqual(rc1, 1)                       # failure reported exactly
        item_id = state['pending_delivery'][0]
        item = delivery['items'][item_id]
        self.assertEqual(item['attempts'], 1)
        self.assertFalse(item['admitted'])             # stays pending, not lost
        self.assertEqual(item['last_rc'], 1)
        self.assertEqual(self._posted_lines(), [])
        rc2 = self._heartbeat('2026-10-17T12:00:00+00:00')  # scheduled retry
        delivery = self._delivery()
        self.assertEqual(rc2, 1)
        self.assertEqual(delivery['items'][item_id]['attempts'], 2)
        self.assertEqual(delivery['items'][item_id]['id'], item_id)  # stable id
        marker.write_text('go')
        rc3 = self._heartbeat('2026-10-17T18:00:00+00:00')
        delivery = self._delivery()
        state = json.loads((self.h.ledger / 'heartbeat-state.json').read_text())
        self.assertEqual(rc3, 0)
        self.assertEqual(len(self._posted_lines()), 1)  # delivered exactly once
        self.assertTrue(delivery['items'][item_id]['admitted'])
        self.assertEqual(state['pending_delivery'], [])
        self.assertEqual(state['last_admitted_line'],
                         self._posted_payloads()[0]['body'])
        rc4 = self._heartbeat('2026-10-18T00:00:00+00:00')  # unchanged: no-op
        self.assertEqual(rc4, 0)
        self.assertEqual(len(self._posted_lines()), 1)      # never duplicated
        self.assertEqual(delivery['items'][item_id]['attempts'], 3)  # no re-post

    def test_attempt_budget_prioritizes_and_defers(self):
        # first run fails: the baseline line is created, attempted, retained
        self.post_cmd = ['/bin/sh', '-c', 'exit 4']
        rc = self._heartbeat('2026-10-17T06:00:00+00:00')
        self.assertEqual(rc, 1)
        # a changed line (awarded BEFORE the episode anchor, so the stall
        # episode is unaffected) gives the second run FOUR due items
        self.h.award('SYN-H7', at='2026-10-17T07:00:00+00:00', kind='map-point',
                     points=10, result={'margin': 3.3, 'units': '%'})
        self.h.ingest('SYN-H7')
        # anchor 2026-10-17T07:14:57Z: at this --now the 5-day card and the
        # 48 h diagnosis are due beside TWO pending lines. The budget admits
        # three attempts per run, in priority order card, diagnosis, oldest
        # line; the newest line is DEFERRED — retained, unattempted, rc 1
        rc = self._heartbeat('2026-10-22T08:00:00+00:00')
        delivery = self._delivery()
        state = json.loads((self.h.ledger / 'heartbeat-state.json').read_text())
        self.assertEqual(rc, 1)
        items = delivery['items']
        self.assertEqual(sorted(it['type'] for it in items.values()),
                         ['admiral-decision-card', 'diagnosis-report',
                          'line', 'line'])
        attempted = [it for it in items.values() if it.get('attempts', 0) > 0]
        self.assertEqual(len(attempted), fp.HEARTBEAT_MAX_POST_ATTEMPTS)
        self.assertEqual(sorted(it['type'] for it in attempted),
                         ['admiral-decision-card', 'diagnosis-report', 'line'])
        deferred = [it for it in items.values()
                    if it.get('attempts', 0) == 0]
        self.assertEqual([it['type'] for it in deferred], ['line'])  # newest
        self.assertEqual([it['seq'] for it in deferred], [2])
        self.assertIn(deferred[0]['id'], state['pending_delivery'])
        card = next(it for it in items.values()
                    if it['type'] == 'admiral-decision-card')
        # DATE frozen at the card's first creation, +48 h, and persisted
        self.assertEqual(card['deadline'],
                         '2026-10-24T08:00:00+00:00')

    def test_post_subprocess_is_time_bounded(self):
        sleeper = ['/bin/sh', '-c', 'sleep 60']
        self.post_cmd = sleeper
        saved = fp.HEARTBEAT_POST_TIMEOUT_S
        fp.HEARTBEAT_POST_TIMEOUT_S = 0  # expire immediately
        try:
            rc = self._heartbeat('2026-10-17T06:00:00+00:00')
        finally:
            fp.HEARTBEAT_POST_TIMEOUT_S = saved
        delivery = self._delivery()
        item = next(it for it in delivery['items'].values())
        self.assertEqual(rc, 1)
        self.assertIn('timeout', str(item['last_rc']))
        self.assertFalse(item['admitted'])

    def test_no_post_command_records_pending_and_exits_zero(self):
        rc = self.h.run('heartbeat', '--now', '2026-10-17T06:00:00+00:00')
        delivery = self._delivery()
        state = json.loads((self.h.ledger / 'heartbeat-state.json').read_text())
        self.assertEqual(rc, 0)  # a probe without the adapter is not a failure
        self.assertEqual(self._posted_lines(), [])
        self.assertEqual(state['pending_delivery'],
                         list(delivery['items']))  # pending is still visible
        item = next(it for it in delivery['items'].values())
        self.assertEqual(item['type'], 'line')     # the one-time baseline
        self.assertEqual(item['attempts'], 0)      # never attempted, retained

    def test_scoreboard_json_carries_line_atomically(self):
        self._heartbeat('2026-10-17T06:00:00+00:00')
        board = json.loads((self.h.ledger / 'scoreboard.json').read_text())
        self.assertIn('vacuum-float ·', board['line'])
        self.assertEqual(board['generated_at'], '2026-10-17T06:00:00+00:00')
        self.assertIn('line', board)  # one atomic file for the morning report

    def test_sequence_allocated_at_creation_and_id_stable(self):
        self._heartbeat('2026-10-17T06:00:00+00:00')
        first = self._posted_payloads()[0]
        delivery = self._delivery()
        self.assertEqual(delivery['next_line_seq'], 1)
        self.assertTrue(first['id'].startswith('vf-line-1-'))
        # a second, changed line allocates the NEXT sequence even while the
        # first is still pending (allocation is at creation, not publication)
        fail = ['/bin/sh', '-c', 'exit 4']
        self.post_cmd = fail
        self.h.award('SYN-H5', at='2026-10-17T07:00:00+00:00', kind='map-point',
                     points=10, result={'margin': 3.3, 'units': '%'})
        self.h.ingest('SYN-H5')
        self._heartbeat('2026-10-17T12:00:00+00:00')
        delivery = self._delivery()
        line_items = sorted((it for it in delivery['items'].values()
                             if it['type'] == 'line'), key=lambda it: it['seq'])
        self.assertEqual([it['seq'] for it in line_items], [1, 2])
        self.assertEqual(delivery['next_line_seq'], 2)

    def test_card_date_frozen_and_retained_on_late_retry(self):
        self.post_cmd = ['/bin/sh', '-c', 'exit 4']  # never admits
        self._heartbeat('2026-10-22T08:00:00+00:00')  # both notices due
        card1 = next(it for it in self._delivery()['items'].values()
                     if it['type'] == 'admiral-decision-card')
        # a LATER run must not recompute the DATE (late delivery keeps it)
        self._heartbeat('2026-10-23T18:00:00+00:00')
        card2 = next(it for it in self._delivery()['items'].values()
                     if it['type'] == 'admiral-decision-card')
        self.assertEqual(card1['deadline'], card2['deadline'])
        self.assertIn(card1['deadline'], card2['body'])
        notice = next((self.h.ledger / 'notices').glob('*admiral-decision*.md'))
        self.assertIn(card1['deadline'], notice.read_text())


class MapPointCount(unittest.TestCase):
    """The distinct admitted map-point count is a separate fact from the
    rubric score (U3-I2): a +10 map point is ONE point identity."""

    def setUp(self):
        self.h = Habitat()

    def tearDown(self):
        self.h.close()

    def _one_map_point(self, points=10):
        self.h.award('SYN-C1', at='2026-10-18T01:00:00+00:00', kind='map-point',
                     points=points, result={'margin': 2.2, 'units': '%'})
        self.h.ingest('SYN-C1')
        return self.h.scoreboard_json()

    def test_single_map_point_counts_one_not_its_score(self):
        board = self._one_map_point(points=10)
        lane = board['lanes']['builder-b']
        self.assertEqual(lane['points'], 10)
        self.assertEqual(lane['map_points'], 1)
        self.assertEqual(board['validated_map_points'], 1)
        self.assertEqual(board['verified_score'], 10)

    def test_benchmark_only_history_count_zero_ratio_unavailable(self):
        self.h.award('SYN-C2', at='2026-10-18T01:00:00+00:00', kind='benchmark',
                     points=3, benchmark_key='synth-bench-1')
        self.h.ingest('SYN-C2')
        self.h.flush_config(cost={'ratio_basis': 'native-record tokens',
                                  'interval': 'programme lifetime'})
        board = self.h.scoreboard_json()
        self.assertEqual(board['validated_map_points'], 0)
        self.assertIn('zero admitted map points', board['cost_per_verified_point_note'])
        self.assertIsNone(board['cost_per_verified_point'])

    def test_token_penalty_does_not_alter_point_count(self):
        self.h.award('SYN-C3', at='2026-10-18T01:00:00+00:00', kind='map-point',
                     points=10, result={'margin': 2.2, 'units': '%'})
        self.h.award('SYN-C4', at='2026-10-18T02:00:00+00:00', kind='tokens-100m',
                     points=-1, units=1)
        self.h.ingest('SYN-C3', 'SYN-C4')
        board = self.h.scoreboard_json()
        lane = board['lanes']['builder-b']
        self.assertEqual(lane['points'], 9)          # score moves ...
        self.assertEqual(lane['map_points'], 1)      # ... the count does not
        self.assertEqual(board['validated_map_points'], 1)

    def test_map_rollover_moves_count_current_to_prior(self):
        self._one_map_point()
        self.h.award('SYN-C5', at='2026-10-18T03:00:00+00:00', kind='map-version',
                     map_version='map-v1')
        self.h.ingest('SYN-C5')
        board = self.h.scoreboard_json()
        lane = board['lanes']['builder-b']
        self.assertEqual(lane['current_map_map_points'], 0)
        self.assertEqual(lane['prior_map_map_points'], 1)
        self.assertEqual(lane['map_points'], 1)  # lifetime count survives rollover

    def test_revoke_after_rollover_adjusts_the_prior_bucket(self):
        self.test_map_rollover_moves_count_current_to_prior()
        self.h.award('SYN-C6', at='2026-10-18T04:00:00+00:00', kind='correction',
                     target_event_id='q-SYN-C1', action='revoke')
        self.h.ingest('SYN-C6')
        board = self.h.scoreboard_json()
        lane = board['lanes']['builder-b']
        self.assertEqual(lane['map_points'], 0)
        self.assertEqual(lane['prior_map_map_points'], 0)
        self.assertEqual(lane['current_map_map_points'], 0)

    def test_audit_zero_zeroes_current_map_count_explicitly(self):
        self._one_map_point()
        self.h.award('SYN-C7', at='2026-10-18T01:30:00+00:00', kind='map-point',
                     points=10, result={'margin': 2.4, 'units': '%'})
        self.h.ingest('SYN-C7')
        # audit-zero is a control event: an explicit block with lane + map_version
        self.h.file_submission('SYN-C8', from_seat=XO,
                               at='2026-10-18T02:00:00+00:00', lane='builder-b',
                               scope={'programme': 'vacuum-float', 'award': {
                                   'kind': 'audit-zero', 'lane': 'builder-b',
                                   'map_version': 'map-v0'}})
        self.h.ingest('SYN-C8')
        board = self.h.scoreboard_json()
        lane = board['lanes']['builder-b']
        self.assertEqual(lane['current_map_map_points'], 0)
        self.assertEqual(lane['map_points'], 0)
        self.assertEqual(lane['map_points_zeroed_by_audit'], 2)  # explicit, not silent

    def test_leaderboard_attributes_points_to_producing_model(self):
        self.h.award('SYN-L1', at='2026-10-18T01:00:00+00:00', kind='map-point',
                     points=10, model='glm-5.3', result={'margin': 2.2, 'units': '%'})
        self.h.award('SYN-L2', at='2026-10-18T02:00:00+00:00', lane='builder-a',
                     kind='map-point', points=10, model='gpt-5.2',
                     result={'margin': 1.1, 'units': '%'})
        self.h.award('SYN-L3', at='2026-10-18T03:00:00+00:00', kind='benchmark',
                     points=15, model='glm-5.3', benchmark_key='synth-bench-2')
        self.h.ingest('SYN-L1', 'SYN-L2', 'SYN-L3')
        board = self.h.scoreboard_json()
        board_leader = {(e['lane'], e['model']): e for e in board['leaderboard']}
        self.assertEqual(board_leader[('builder-b', 'glm-5.3')]['points'], 25)
        self.assertEqual(board_leader[('builder-b', 'glm-5.3')]['map_points'], 1)
        self.assertEqual(board_leader[('builder-a', 'gpt-5.2')]['points'], 10)
        self.assertEqual(board_leader[('builder-a', 'gpt-5.2')]['map_points'], 1)
        self.assertEqual(board_leader[('builder-b', 'glm-5.3')]['awards'], 2)


class OverAwardSurfaced(unittest.TestCase):
    """Una's award is never refused or rescored; an award above the observed
    crossings is a displayed discrepancy for her disposition (U3-I1)."""

    def setUp(self):
        self.h = Habitat()

    def tearDown(self):
        self.h.close()

    def test_over_award_displayed_never_rescinded(self):
        self.h.file_submission(
            'SYN-O1', from_seat=BUILDER, at='2026-10-18T01:00:00+00:00',
            lane='builder-b', model='syn-model',
            scope={'programme': 'vacuum-float', 'award': {
                'kind': 'cost-update',
                'result': {'tokens': 150_000_000, 'coverage': 'measured',
                           'interval': {'from': '2026-10-18T01:00:00+00:00',
                                        'to': '2026-10-18T01:00:00+00:00'},
                           'session': 'syn-sess-1', 'bucket': 'lane'}}})
        self.h.ingest('SYN-O1')
        self.h.scoreboard_run('2026-10-18T02:00:00+00:00')  # observe the crossing
        self.h.award('SYN-O2', at='2026-10-18T03:00:00+00:00', kind='tokens-100m',
                     points=-2, units=2)  # two units awarded, one observed
        self.h.ingest('SYN-O2')
        board = self.h.scoreboard_json()
        accounting = board['token_accounting']['builder-b']
        self.assertEqual(accounting['crossings_observed'], 1)
        self.assertEqual(accounting['penalty_events_awarded'], 2)
        self.assertEqual(accounting['over_award_discrepancy'], 1)
        self.assertIn('WARNING', accounting['note'])
        self.assertEqual(board['lanes']['builder-b']['points'], -2)  # never rescinded


class SchemaFile(unittest.TestCase):
    def test_schema_prints_and_initial_state_is_honest(self):
        import contextlib
        import io
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            self.assertEqual(fp.main(['schema']), 0)
        schema = json.loads(buf.getvalue())
        self.assertEqual(schema['schema'], 'vacuum-float-progress')
        defaults = fp.load_initial_defaults()
        self.assertEqual(defaults['programme_start']['id'],
                         'ord-sciences-g1-vacuum-u3-builder-b-start-1017')
        self.assertEqual(defaults['admiral_seats'], [])
        self.assertEqual(defaults['cost']['ratio_basis'], 'UNSET')


class RebuiltConsumedValueValidation(unittest.TestCase):
    """U3 rebuilt-source regressions (NEW3600): every value the heartbeat
    CONSUMES is validated at load time — attempts shape, card deadline as
    a mandatory timezone-aware ISO string, optional deadlines, body and
    episode_key as nonempty strings, string created_at before ordering —
    all BEFORE any adapter call, cursor recovery or delivery write. The
    negatives prove zero posts and byte-identical retained records."""

    def setUp(self):
        self.h = Habitat()
        self.post_log = self.h.base / 'posted.log'
        self.post_cmd = ['/bin/sh', '-c', f'cat >> {self.post_log}']

    def tearDown(self):
        self.h.close()

    def _heartbeat(self, now):
        return self.h.run('heartbeat', '--now', now,
                          '--post-command', *self.post_cmd)

    def _posted_lines(self):
        if not self.post_log.exists():
            return []
        return [ln for ln in self.post_log.read_text().splitlines() if ln.strip()]

    def _delivery(self):
        return json.loads((self.h.ledger / 'delivery-pending.json').read_text())

    def _rewrite(self, doc):
        (self.h.ledger / 'delivery-pending.json').write_text(
            json.dumps(doc, indent=1, sort_keys=True) + '\n')

    def _seeded(self):
        self._heartbeat('2026-10-17T06:00:00+00:00')
        return self.h.ledger / 'delivery-pending.json'

    def _clean_doc(self):
        """One real baseline run, snapshotted; every case starts from a
        clean deepcopy so mutations never accumulate across cases (a
        rejected file is preserved byte-identical, so without the reset
        one case's corruption would shadow the next)."""
        import copy
        if not hasattr(self, '_clean'):
            self._heartbeat('2026-10-17T06:00:00+00:00')
            self._clean = copy.deepcopy(self._delivery())
        return copy.deepcopy(self._clean)

    def _fail_closed_case(self, mutate, needle, now='2026-10-17T12:00:00+00:00'):
        import io
        import contextlib
        dpath = self.h.ledger / 'delivery-pending.json'
        hb_path = self.h.ledger / 'heartbeat-state.json'
        doc = self._clean_doc()
        mutate(doc)
        self._rewrite(doc)
        before = dpath.read_bytes()
        hb_before = hb_path.read_bytes()
        posts_before = len(self._posted_lines())
        err = io.StringIO()
        with contextlib.redirect_stderr(err):
            rc = self._heartbeat(now)
        self.assertEqual(rc, 2, err.getvalue())
        self.assertIn(needle, err.getvalue())
        self.assertEqual(dpath.read_bytes(), before)      # delivery untouched
        self.assertEqual(hb_path.read_bytes(), hb_before)  # cursor untouched
        self.assertEqual(len(self._posted_lines()), posts_before)  # no post

    def test_attempts_shape_fails_closed(self):
        # U3-D4: attempts, when present, is an exact nonnegative integer —
        # never a boolean or a string count. A string "0" used to reach the
        # post-adapter arithmetic and crash the run after filing.
        for bad in ('0', True, -1, 1.5):
            def mutate(doc, bad=bad):
                for item in doc['items'].values():
                    item['attempts'] = bad
            self._fail_closed_case(mutate, 'attempts')
        # absent attempts on a PENDING item keeps the documented zero
        # default AND delivers: exactly one extra fake post, under the
        # SAME item id, admitted, with the counter starting at one
        doc = self._clean_doc()
        item_id = next(iter(doc['items']))
        posts_before = len(self._posted_lines())
        for item in doc['items'].values():
            item.pop('admitted', None)
            item.pop('attempts', None)
        self._rewrite(doc)
        rc = self._heartbeat('2026-10-17T12:00:00+00:00')
        self.assertEqual(rc, 0)
        self.assertEqual(len(self._posted_lines()), posts_before + 1)
        self.assertEqual(json.loads(self._posted_lines()[-1])['id'], item_id)
        after = self._delivery()['items'][item_id]
        self.assertTrue(after['admitted'])
        self.assertEqual(after['attempts'], 1)

    def test_card_deadline_is_mandatory_aware_iso(self):
        # U3-D4: the admiral decision card's deadline is mandatory and must
        # be a nonempty timezone-aware ISO string; missing/null/empty/
        # wrong-type/naive all fail closed before anything is posted.
        def card(doc, deadline=..., **extra):
            item = {'id': 'vf-stall-x-5d', 'type': 'admiral-decision-card',
                    'created_at': 't', 'attempts': 0, 'admitted': False,
                    'body': 'five days without a verified map point',
                    'episode_key': 'anchor:2026-10-17T00:14:57-07:00'}
            if deadline is not ...:
                item['deadline'] = deadline
            item.update(extra)
            doc['items'][item['id']] = item
        for bad in (None, '', 5, 'not-a-date', '2026-10-22T00:14:57'):
            def mutate(doc, bad=bad):
                card(doc, deadline=bad)
            self._fail_closed_case(mutate, 'deadline')
        # naive-only is rejected even though it parses as ISO
        # the OMITTED case too: a card with no deadline key at all is
        # rejected the same way — zero synthetic calls, byte-identical
        # delivery and cursor evidence (asserted by _fail_closed_case)
        def mutate_omitted(doc):
            card(doc)                       # no deadline key whatsoever
        self._fail_closed_case(mutate_omitted, 'deadline')

    def test_optional_deadline_on_other_types_validates(self):
        # U3-D4: deadline is OPTIONAL for lines and diagnoses, but when the
        # key is present its value must be a valid timezone-aware ISO
        # string — never silently dropped from the payload as null/naive.
        for bad in (None, '2026-10-19T08:00:00', 'soon'):
            def mutate(doc, bad=bad):
                for item in doc['items'].values():
                    item['deadline'] = bad
            self._fail_closed_case(mutate, 'deadline')
        # a VALID optional deadline rides the payload untouched — the
        # control item is made DUE (pending), so the payload is observable
        doc = self._clean_doc()
        for item in doc['items'].values():
            item['admitted'] = False
            item['deadline'] = '2026-10-19T08:00:00+00:00'
        self._rewrite(doc)
        rc = self._heartbeat('2026-10-17T12:00:00+00:00')
        self.assertEqual(rc, 0)
        payload = json.loads(self._posted_lines()[-1])
        self.assertEqual(payload.get('deadline'), '2026-10-19T08:00:00+00:00')

    def test_body_episode_key_and_created_at_shapes_fail_closed(self):
        # U3-D4: consumed strings are validated before use — body is a
        # nonempty string for every type, a notice's episode_key is a
        # nonempty string, created_at is a string before ordering.
        for bad_body in (5, None, '', ['vf']):
            def m1(doc, bad=bad_body):
                for item in doc['items'].values():
                    item['body'] = bad
            self._fail_closed_case(m1, 'body')
        for bad_key in (7, '', None, {'k': 1}):
            def m2(doc, bad=bad_key):
                doc['items']['vf-stall-y-48h'] = {
                    'id': 'vf-stall-y-48h', 'type': 'diagnosis-report',
                    'created_at': 't', 'attempts': 0, 'admitted': False,
                    'body': '48 h stall diagnosis', 'episode_key': bad}
            self._fail_closed_case(m2, 'episode key')
        def m3(doc):
            for item in doc['items'].values():
                item['created_at'] = 17
        self._fail_closed_case(m3, 'created_at')

    def test_item_id_and_type_must_be_strings(self):
        # U3-D4: id and type are consumed as strings (filenames, argv,
        # membership tests); a non-string id or type is corrupt identity.
        def m1(doc):
            for item in doc['items'].values():
                item['id'] = 5
            doc['items'][5] = doc['items'].pop(next(iter(doc['items'])))
        self._fail_closed_case(m1, 'id')
        def m2(doc):
            for item in doc['items'].values():
                item['type'] = 1
        self._fail_closed_case(m2, 'type')



if __name__ == '__main__':
    unittest.main()
