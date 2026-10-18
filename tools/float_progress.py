#!/usr/bin/env python3
"""Vacuum Float programme progress machinery (U3, Builder B).

Plumbing for the redirected programme, not a scientific result. It maintains
an append-only event ledger in an OWNED location given explicitly on every
run -- never a hard-coded repository or runtime path -- and derives every view
(scoreboard, balances, stall state) from those events. Nothing here verifies
science: Una (the XO seat, resolved canonically from the ship binding at
ingest, with her accepted historical seats preserved) is the exclusive
verifier and scorer. A builder filing is a nomination and carries no points.

Authority contract (see research/program/vacuum-float/SCHEMA.md): an accepted
queue record -- read read-only from the submissions directory by exact id --
yields a verification event only when it was filed by a verifier seat AND
carries an explicit typed block (record scope, or a named artifact whose
sha256 matches and whose JSON type is vacuum-float-award). Missing or
mismatched authority leaves the filing an unverified nomination with the
precise reason recorded. Runtime records are never written by this tool.

Honesty rules carried in code: the initial state is empty (UNVERIFIED margin,
UNKNOWN material gap, zero points, no fabricated carry-in); identical replay
of an accepted event is a no-op while the same event id with a different
payload is refused; corrections append and never rewrite; a torn final line
is an uncommitted append, excluded from every view until repaired; benchmark,
falsification and material-card credit is bounded by once-ever and rolling
168-hour caps that no new id, replay, boundary stacking or map-version
rollover can widen; unknown cost
is not zero and a zero denominator yields an unavailable ratio, never
infinity. Activation of the six-hour heartbeat is a separate act from
implementation: the delivered default posts nothing and every view carries
the activation blocker.
"""
from __future__ import annotations

import argparse
import datetime as dt
import fcntl
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_FILE = ROOT / 'research' / 'program' / 'vacuum-float' / 'schema.json'
INITIAL_STATE_FILE = ROOT / 'research' / 'program' / 'vacuum-float' / 'state-initial.json'
DEFAULT_SUBMISSIONS_DIR = Path('/home/tyler/data/helm/ship/queue/submissions')
DEFAULT_BINDING_DIR = Path('/home/tyler/data/helm/ship/binding')

EVENTS_NAME = 'events.jsonl'
STATE_NAME = 'ledger-state.json'
HEARTBEAT_STATE_NAME = 'heartbeat-state.json'
SCOREBOARD_JSON_NAME = 'scoreboard.json'
SCOREBOARD_LINE_NAME = 'scoreboard.line'
NOTICES_DIR_NAME = 'notices'

SCHEMA_VERSION = 1

# POINTS.md v0 (redirect section 7), verbatim in weight. Kinds name the table
# rows; the rubric file remains the normative text and version carrier.
RUBRIC_V0 = {
    'map-point': 10,
    'scoreboard-improve': 25,
    'benchmark': 15,
    'falsification': 10,
    'material-card': 5,
    'claim-withdrawn': -10,
    'landing-no-number': -5,
    'envelope-breach': -20,
    'tokens-100m': -1,
}
WEEKLY_CAPS = {'falsification': 3, 'material-card': 5}
ONCE_EVER_KINDS = {'benchmark'}
# Kinds that may carry scientific scoreboard values. Only verifier-verified
# events of these kinds move margin or material gap.
SCIENTIFIC_KINDS = {'map-point', 'scoreboard-improve'}
# Control kinds travel in the same typed block but carry no points.
CONTROL_KINDS = {'audit-zero', 'map-version', 'rubric-change', 'cost-update',
                 'correction'}
VERIFIER_ONLY_KINDS = {'audit-zero', 'map-version', 'rubric-change', 'correction'}
EVENT_TYPES = {'nomination', 'verification-award'} | CONTROL_KINDS

STALL_DIAGNOSIS_AFTER = dt.timedelta(hours=48)
STALL_DECISION_CARD_AFTER = dt.timedelta(days=5)

# Scorer conventions (v0), Una 2026-10-17: the two weekly caps run on a
# ROLLING 168 hours of exact instants keyed on the verification report's own
# UTC instant -- no timezone, no calendar week, no boundary to stack across.
CAP_WINDOW = dt.timedelta(hours=168)
TOKENS_PER_UNIT = 100_000_000
# Usage excluded from every lane (programme overhead): Sciences' head seat,
# the scorer and any scorer re-run sub-worker, the CO, the external review.
OVERHEAD_ROLES = ('sciences-head', 'scorer', 'scorer-rerun', 'co', 'review')
# Heartbeat delivery bounds (Sciences disposition U3-BOUND-BINDINGS-1017):
# each adapter call is capped at 150 s, at most THREE adapter attempts happen
# per heartbeat (due 5-day card first, then the 48 h diagnosis, then the
# oldest pending line), and an undelivered due item is retried only on the
# next SCHEDULED run — never by an in-run polling loop.
HEARTBEAT_POST_TIMEOUT_S = 150
HEARTBEAT_MAX_POST_ATTEMPTS = 3
DELIVERY_STATE_NAME = 'delivery-pending.json'
LINE_COMPLETION = ('information only: the vacuum-float scoreboard line '
                   'changed; nobody acts on an unchanged line')

_VERSION_RE = re.compile(r'^(.*?)(\d+)$')


class Refused(Exception):
    """A refusal that must be reported precisely, never silently bypassed."""


def canonical_json(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(',', ':'), ensure_ascii=False)


def payload_digest(event: dict) -> str:
    """Digest of the event minus bookkeeping fields the ledger itself sets."""
    material = {k: v for k, v in event.items() if k != 'ingested_at'}
    return hashlib.sha256(canonical_json(material).encode('utf-8')).hexdigest()


def parse_iso(value: str, *, what: str) -> dt.datetime:
    parsed = dt.datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise Refused(f'{what} must carry a timezone offset: {value!r}')
    return parsed


def iso_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds')


def version_number(name: str) -> int | None:
    match = _VERSION_RE.match(str(name).strip())
    return int(match.group(2)) if match else None


# --------------------------------------------------------------------------
# configuration


def load_initial_defaults() -> dict:
    with INITIAL_STATE_FILE.open() as fh:
        return json.load(fh)


def load_config(path: str | None) -> dict:
    if path is None:
        return load_initial_defaults()
    with open(path) as fh:
        return json.load(fh)


def resolve_verifier_seats(cfg: dict, *, binding_dir: Path | None = None,
                           extra: list[str] | None = None) -> set[str]:
    """Canonical verifier seats: configured seats, plus the CURRENT binding
    principal for the verifier billet, plus seats already accepted as verifier
    authority (a later succession never invalidates a historical record)."""
    seats = {s for s in cfg.get('verifier_seats', []) if s}
    seats.update(s for s in (extra or []) if s)
    billet = cfg.get('verifier_billet')
    base = Path(binding_dir) if binding_dir else Path(cfg.get('binding_dir', str(DEFAULT_BINDING_DIR)))
    if billet:
        record = base / f'{billet}.json'
        try:
            with record.open() as fh:
                binding = json.load(fh)
            seat = (binding.get('principal') or {}).get('seat')
            if seat:
                seats.add(seat)
        except FileNotFoundError:
            pass  # unknown stays unknown; the configured seats still bind
        except (OSError, ValueError) as exc:
            raise Refused(f'unreadable binding record {record}: {exc}') from exc
    return seats


def resolve_admiral_seats(cfg: dict, *, extra: list[str] | None = None) -> set[str]:
    """Admiral-seat approvers for rubric changes. The canonical register of
    minted Admiral role seats is not machine-readable from here; the list is
    explicit configuration, empty by default and populated by Sciences/Desk."""
    seats = {s for s in cfg.get('admiral_seats', []) if s}
    seats.update(s for s in (extra or []) if s)
    return seats


# --------------------------------------------------------------------------
# ledger storage


class Ledger:
    """Append-only event store plus its small state file, both under one owned
    directory. Every mutation holds an exclusive flock for the whole
    read-modify-write, so heartbeat and manual runs cannot interleave."""

    def __init__(self, root: Path, cfg: dict):
        self.root = Path(root)
        self.cfg = cfg
        self.root.mkdir(parents=True, exist_ok=True)
        (self.root / NOTICES_DIR_NAME).mkdir(exist_ok=True)
        self.lock_path = self.root / 'ledger.lock'
        self.events_path = self.root / EVENTS_NAME
        self.state_path = self.root / STATE_NAME
        self._init_state()

    def _default_state(self) -> dict:
        return {
            'schema_version': SCHEMA_VERSION,
            'programme': self.cfg.get('programme', 'vacuum-float'),
            'map_version': self.cfg.get('map_version', 'map-v0'),
            # the map version the LOG starts from; map_version above advances
            # on each verified map-version event, so replay reconstruction
            # needs the starting value preserved separately
            'map_version_start': self.cfg.get('map_version', 'map-v0'),
            'rubric_version': self.cfg.get('rubric_version', 'v0'),
            'authority_seats_seen': sorted(resolve_verifier_seats(self.cfg)),
            'admiral_seats_seen': sorted(resolve_admiral_seats(self.cfg)),
            'created_at': iso_now(),
            'activation': {
                'state': 'ACTIVATION BLOCKED',
                # bindings resolved owner (Sciences), routes and the timer
                # allocation; what still blocks activation is sign-off,
                # landing and the measured install
                'missing': [
                    'Una verification/sign-off of the U3 candidate',
                    'landing of the source on the CO order',
                    'measured install of service and timer by Operations',
                ],
            },
        }

    def _init_state(self) -> None:
        if not self.state_path.exists():
            atomic_write_json(self.state_path, self._default_state())

    def state(self) -> dict:
        with self.state_path.open() as fh:
            return json.load(fh)

    def write_state(self, state: dict) -> None:
        atomic_write_json(self.state_path, state)

    def read_events(self) -> tuple[list[dict], dict]:
        """Every committed event, plus a torn-tail report. A final line that is
        not valid JSON is an interrupted append: excluded from every view and
        reported, never counted as a committed award."""
        events: list[dict] = []
        torn = {'present': False, 'bytes': 0, 'offset': 0}
        if not self.events_path.exists():
            return events, torn
        raw = self.events_path.read_bytes()
        offset = 0
        for line in raw.splitlines(keepends=True):
            text = line.decode('utf-8', 'replace').strip()
            if text:
                try:
                    events.append(json.loads(text))
                except ValueError:
                    torn = {'present': True, 'bytes': len(raw) - offset, 'offset': offset}
                    break
            offset += len(line)
        return events, torn

    def append(self, event: dict) -> None:
        line = canonical_json(event) + '\n'
        with self.events_path.open('a') as fh:
            fh.write(line)
            fh.flush()
            os.fsync(fh.fileno())

    def repair_tail(self) -> dict:
        """Truncate a torn final line. The removed bytes were never a
        committed event."""
        _, torn = self.read_events()
        if not torn['present']:
            return {'repaired': False, 'reason': 'no torn tail'}
        with self.events_path.open('r+b') as fh:
            fh.truncate(torn['offset'])
            fh.flush()
            os.fsync(fh.fileno())
        return {'repaired': True, 'removed_bytes': torn['bytes']}

    def __enter__(self) -> 'Ledger':
        self._lock_fh = self.lock_path.open('a+')
        fcntl.flock(self._lock_fh, fcntl.LOCK_EX)
        return self

    def __exit__(self, *exc) -> None:
        fcntl.flock(self._lock_fh, fcntl.LOCK_UN)
        self._lock_fh.close()


def atomic_write_json(path: Path, obj) -> None:
    atomic_write(path, json.dumps(obj, indent=1, sort_keys=True) + '\n')


def atomic_write(path: Path, text: str) -> None:
    tmp = path.with_name(path.name + '.tmp')
    with tmp.open('w') as fh:
        fh.write(text)
        fh.flush()
        os.fsync(fh.fileno())
    tmp.replace(path)


# --------------------------------------------------------------------------
# authority adapter (read-only over accepted queue submissions)


def read_submission(submissions_dir: Path, submission_id: str) -> dict:
    path = Path(submissions_dir) / f'{submission_id}.json'
    try:
        with path.open() as fh:
            record = json.load(fh)
    except FileNotFoundError as exc:
        raise Refused(f'no accepted submission {submission_id} in {submissions_dir}') from exc
    except ValueError as exc:
        raise Refused(f'corrupt submission {submission_id}: {exc}') from exc
    return record


def artifact_block(record: dict, base_dir: Path) -> dict | None:
    """The typed block from a named artifact, only when its sha256 matches.
    A mismatched digest is never trusted."""
    for art in record.get('artifacts', []) or []:
        path = Path(art.get('path', ''))
        digest = art.get('sha256', '')
        if not str(path) or not digest:
            continue
        if not path.is_absolute():
            path = base_dir / path
        try:
            blob = path.read_bytes()
        except OSError:
            continue
        if hashlib.sha256(blob).hexdigest() != digest:
            continue
        try:
            doc = json.loads(blob)
        except ValueError:
            continue
        if isinstance(doc, dict) and doc.get('type') == 'vacuum-float-award':
            return doc
    return None


def typed_block_from_record(record: dict, base_dir: Path) -> tuple[dict | None, str]:
    """The explicit typed block: the record's scope, else a sha-verified
    artifact of type vacuum-float-award. (None, reason) when absent."""
    scope = record.get('scope')
    if isinstance(scope, dict) and scope.get('programme') == 'vacuum-float':
        block = scope.get('award')
        if isinstance(block, dict):
            return block, 'scope.award'
    art = artifact_block(record, base_dir)
    if art is not None:
        return art, 'artifact'
    return None, ('no explicit typed block (neither scope.award nor a sha-matching '
                  'vacuum-float-award artifact)')


def expected_points(kind: str, block: dict) -> int:
    if kind == 'tokens-100m':
        return RUBRIC_V0[kind] * int(block.get('units', 1))
    return RUBRIC_V0[kind]


def classify_submission(record: dict, cfg: dict, *, base_dir: Path,
                        binding_dir: Path | None = None,
                        verifier_seen: list[str] | None = None,
                        admiral_seen: list[str] | None = None,
                        submissions_dir: Path | None = None,
                        ) -> tuple[dict, str]:
    """Build the ledger event an accepted submission maps to. Verifier seats
    with an explicit typed block yield verification events; everything else is
    a nomination, which never carries points."""
    submission_id = record.get('id', '')
    from_seat = record.get('from_seat', '')
    verifier_seats = resolve_verifier_seats(cfg, binding_dir=binding_dir, extra=verifier_seen)
    block, source = typed_block_from_record(record, base_dir)
    event = {
        'event_id': f'q-{submission_id}',
        'event_type': 'nomination',
        'from_seat': from_seat,
        'lane': record.get('lane', ''),
        'model': record.get('model', ''),
        'authority': {'record_id': submission_id, 'source': source},
        'verified': False,
        'points': 0,
        'event_at': record.get('at', ''),
        'note': '',
    }
    if block is None:
        event['note'] = f'nomination: {source}'
        return event, event['note']
    if block.get('kind') == 'cost-update':
        # measured accounting may be filed by any seat: never an award, never
        # points, and its honesty does not depend on verifier authority
        return build_control_event(event, block, 'cost-update', cfg,
                                   admiral_seen=admiral_seen,
                                   submissions_dir=submissions_dir,
                                   base_dir=base_dir)
    if from_seat not in verifier_seats:
        event['note'] = (f'nomination: typed block present but from_seat {from_seat!r} '
                         'is not a verifier seat')
        return event, event['note']
    return build_verified_event(event, block, cfg,
                                admiral_seen=admiral_seen,
                                submissions_dir=submissions_dir,
                                base_dir=base_dir)


def build_verified_event(event: dict, block: dict, cfg: dict, *,
                         admiral_seen: list[str] | None = None,
                         submissions_dir: Path | None = None,
                         base_dir: Path | None = None) -> tuple[dict, str]:
    """Validate a verifier-filed typed block. Refusals are precise and leave
    the filing a nomination."""
    kind = block.get('kind', '')
    for field in ('lane', 'model'):
        if block.get(field):
            event[field] = block[field]
    if kind in CONTROL_KINDS:
        return build_control_event(event, block, kind, cfg,
                                   admiral_seen=admiral_seen,
                                   submissions_dir=submissions_dir,
                                   base_dir=base_dir)
    if kind not in RUBRIC_V0:
        event['note'] = f'nomination: award kind {kind!r} is not in rubric v0'
        return event, event['note']
    points = block.get('points')
    if not isinstance(points, int) or points != expected_points(kind, block):
        event['note'] = (f'nomination: award points {points!r} do not match rubric v0 '
                         f'for {kind!r} ({expected_points(kind, block)})')
        return event, event['note']
    if kind in ONCE_EVER_KINDS and not block.get('benchmark_key'):
        event['note'] = f'nomination: award kind {kind!r} requires a benchmark_key'
        return event, event['note']
    event = dict(event)
    event['event_type'] = 'verification-award'
    event['verified'] = True
    event['points'] = points
    event['award'] = {k: v for k, v in block.items() if k != 'points'}
    return event, 'verification-award'


def build_control_event(event: dict, block: dict, kind: str, cfg: dict, *,
                        admiral_seen: list[str] | None = None,
                        submissions_dir: Path | None = None,
                        base_dir: Path | None = None) -> tuple[dict, str]:
    if kind in VERIFIER_ONLY_KINDS and not event.get('from_seat'):
        event['note'] = f'nomination: control kind {kind!r} lost its filer'
        return event, event['note']
    if kind == 'cost-update':
        # Any seat may file measured cost; it is never an award and never
        # changes points. Coverage language is preserved verbatim.
        event = dict(event)
        event['event_type'] = 'cost-update'
        event['verified'] = False
        event['points'] = 0
        event['result'] = block.get('result', {})
        return event, 'cost-update'
    if kind == 'audit-zero':
        if not block.get('lane') or not block.get('map_version'):
            event['note'] = 'nomination: audit-zero requires lane and map_version'
            return event, event['note']
        event = dict(event)
        event['event_type'] = 'audit-zero'
        event['verified'] = True
        event['points'] = 0
        event['award'] = dict(block)
        return event, 'audit-zero'
    if kind == 'map-version':
        new = block.get('map_version', '')
        if not new:
            event['note'] = 'nomination: map-version requires map_version'
            return event, event['note']
        event = dict(event)
        event['event_type'] = 'map-version'
        event['verified'] = True
        event['points'] = 0
        event['award'] = {'map_version': new}
        return event, 'map-version'
    if kind == 'correction':
        target = block.get('target_event_id', '')
        action = block.get('action', '')
        if not target or action not in ('revoke', 'amend'):
            event['note'] = ('nomination: correction requires target_event_id and '
                             "action revoke|amend")
            return event, event['note']
        if action == 'amend' and not isinstance(block.get('new_points'), int):
            event['note'] = 'nomination: amending correction requires integer new_points'
            return event, event['note']
        event = dict(event)
        event['event_type'] = 'correction'
        event['verified'] = True
        event['points'] = 0
        event['award'] = {'target_event_id': target, 'action': action,
                          'new_points': block.get('new_points'),
                          'reason': block.get('reason', '')}
        return event, 'correction'
    # rubric-change: dual approval, forward-only, one per map version.
    new = block.get('rubric_version', '')
    approvals = block.get('approvals', [])
    if not new:
        event['note'] = 'nomination: rubric-change requires rubric_version'
        return event, event['note']
    admiral_seats = resolve_admiral_seats(cfg, extra=admiral_seen)
    approver_seats = []
    for ref in approvals:
        ref_id = ref.get('id') if isinstance(ref, dict) else ref
        if not ref_id:
            continue
        if submissions_dir is None:
            event['note'] = 'nomination: rubric-change approval records unreadable (no submissions dir)'
            return event, event['note']
        try:
            approval_record = read_submission(submissions_dir, ref_id)
        except Refused as exc:
            event['note'] = f'nomination: rubric-change approval {ref_id}: {exc}'
            return event, event['note']
        approver_seats.append(approval_record.get('from_seat', ''))
    # The filer is already a verifier seat (classify_submission checked); the
    # second approval must come from an Admiral seat's accepted record.
    has_admiral = any(seat in admiral_seats for seat in approver_seats)
    if not has_admiral:
        event['note'] = ('nomination: rubric-change requires BOTH Una and an Admiral-seat '
                         f'approval record (verifier filer: present; admiral approval: absent; '
                         f'configured admiral seats: {sorted(admiral_seats) or "none"})')
        return event, event['note']
    event = dict(event)
    event['event_type'] = 'rubric-change'
    event['verified'] = True
    event['points'] = 0
    event['award'] = {'rubric_version': new, 'approvals': approvals}
    return event, 'rubric-change'


# --------------------------------------------------------------------------
# derivation


def cap_window_priors(instants: list[dt.datetime], when: dt.datetime) -> int:
    """Scorer conventions (v0) section 1: how many same-kind verified awards
    the lane already carries in the closed 168 hours ending at `when`. Every
    verified award of the capped kind counts -- an over-cap event is still
    verified evidence and still occupies its window -- so stacking can never
    outrun the cap and a cleared window reopens it."""
    window_start = when - CAP_WINDOW
    return sum(1 for instant in instants if window_start <= instant <= when)


def derive(events: list[dict], cfg: dict, state: dict) -> dict:
    """Every view is derived from events; nothing stored can drift. Events
    replay in chronological order: an audit-zero or a map-version advance
    resets a lane's current-map balance from its event onward, later awards in
    the same map version still count, and a correction adjusts the balance
    while the original event's bytes stay untouched."""
    # replay starts from the map version the LOG began at (recorded at state
    # creation and never advanced), so an award or audit-zero filed before a
    # later rollover is evaluated against the map that was current THEN —
    # never against the final map version. Legacy states without the field
    # fall back to the live value (no map-version events existed yet).
    current_map = state.get('map_version_start') or state['map_version']
    lanes: dict[str, dict] = {}
    unverified: list[dict] = []
    benchmark_keys: set[str] = set()
    capped_instants: dict[tuple[str, str], list[dt.datetime]] = {}
    best_margin = None
    best_gap = None
    cost_entries: list[dict] = []
    penalty_awarded: dict[str, int] = {}
    rubric_version = state['rubric_version']
    awards_by_id: dict[str, dict] = {}
    duplicates: list[dict] = []
    model_tallies: dict[tuple[str, str], dict] = {}

    ordered = sorted(
        (e for e in events if e.get('event_at')),
        key=lambda e: (e['event_at'], e.get('event_id', '')),
    )

    def lane_slot(lane: str) -> dict:
        return lanes.setdefault(lane, {'points': 0, 'current_map_points': 0,
                                       'prior_map_points': 0, 'awards': 0,
                                       'uncredited': [],
                                       'map_points_count': 0,
                                       'current_map_map_points': 0,
                                       'prior_map_map_points': 0,
                                       'map_points_zeroed_by_audit': 0})

    seen_ids: set[str] = set()
    for event in ordered:
        event_id = event.get('event_id', '')
        if event_id:
            if event_id in seen_ids:
                # a duplicated line never double-credits: the first occurrence
                # in file order wins and selfcheck flags the anomaly
                duplicates.append({'event_id': event_id,
                                   'reason': 'duplicate event id in the log; '
                                             'first occurrence credited'})
                continue
            seen_ids.add(event_id)
        etype = event.get('event_type')
        lane = event.get('lane') or '?'
        if etype == 'nomination':
            unverified.append({'event_id': event.get('event_id'),
                               'reason': event.get('note') or 'nomination'})
            continue
        if etype == 'cost-update':
            result = event.get('result') or {}
            cost_entries.append({
                'lane': lane, 'model': event.get('model'),
                'at': event.get('event_at'),
                'session': result.get('session') or event.get('authority', {}).get('record_id', ''),
                'bucket': result.get('bucket', 'lane'),
                'role': result.get('role', ''),
                'tokens': result.get('tokens'),
                'coverage': result.get('coverage', 'unavailable'),
                'interval': result.get('interval'),
            })
            continue
        if etype == 'map-version':
            if event.get('verified'):
                current_map = event.get('award', {}).get('map_version', current_map)
                for slot in lanes.values():
                    slot['prior_map_points'] += slot['current_map_points']
                    slot['current_map_points'] = 0
                    slot['prior_map_map_points'] += slot['current_map_map_points']
                    slot['current_map_map_points'] = 0
                for record in awards_by_id.values():
                    if record.get('credited') and record.get('bucket') == 'current':
                        record['bucket'] = 'prior'
            continue
        if etype == 'rubric-change':
            if event.get('verified'):
                rubric_version = event.get('award', {}).get('rubric_version', rubric_version)
            continue
        if etype == 'correction':
            award = event.get('award', {})
            original = awards_by_id.get(award.get('target_event_id'))
            if original is None:
                unverified.append({'event_id': event.get('event_id'),
                                   'reason': 'correction names an unknown or future event'})
                continue
            slot = lanes.get(original['lane'])
            if slot is None:
                continue
            if award.get('action') == 'revoke':
                if original['credited']:
                    in_current = original.get('bucket', 'current') == 'current'
                    slot['points'] -= original['points']
                    if in_current:
                        slot['current_map_points'] -= original['points']
                    else:
                        slot['prior_map_points'] -= original['points']
                    if original.get('kind') == 'map-point':
                        # the point identity itself is withdrawn, from the
                        # map bucket it was credited into — a revoke after a
                        # rollover adjusts the prior balance, never a
                        # negative current one
                        slot['map_points_count'] -= 1
                        if in_current:
                            slot['current_map_map_points'] -= 1
                        else:
                            slot['prior_map_map_points'] -= 1
                    original['credited'] = False
                slot['uncredited'].append(
                    {'event_id': original['event_id'], 'reason': 'revoked by correction'})
            elif award.get('action') == 'amend':
                new_points = award.get('new_points')
                if original['credited'] and isinstance(new_points, int):
                    in_current = original.get('bucket', 'current') == 'current'
                    slot['points'] += new_points - original['points']
                    if in_current:
                        slot['current_map_points'] += new_points - original['points']
                    else:
                        slot['prior_map_points'] += new_points - original['points']
                    original['points'] = new_points
                    # an amend rescores one admitted map point; it neither
                    # creates nor destroys a point identity
                slot['uncredited'].append(
                    {'event_id': original['event_id'],
                     'reason': f"amended by correction to {new_points}"})
            continue
        if etype == 'audit-zero':
            target = event.get('award', {})
            target_map = target.get('map_version')
            target_lane = target.get('lane')
            applied = bool(event.get('verified')) and target_map == current_map
            if applied and target_lane in lanes:
                slot = lanes[target_lane]
                # the audit withdraws the lane's current-map credit entirely:
                # both the lifetime total and the current-map balance, while
                # prior map versions stay preserved. The current-map point
                # count is zeroed explicitly and the number withdrawn is
                # recorded — never folded silently into zero.
                slot['points'] -= slot['current_map_points']
                slot['current_map_points'] = 0
                slot['map_points_count'] -= slot['current_map_map_points']
                slot['map_points_zeroed_by_audit'] += slot['current_map_map_points']
                slot['current_map_map_points'] = 0
                slot['zeroed_by'] = event.get('event_id')
            elif not applied and event.get('verified'):
                unverified.append({
                    'event_id': event.get('event_id'),
                    'reason': (f'audit-zero names map version {target_map}, not the current '
                               f'{current_map}: recorded, NOT applied to a newer map')})
            continue
        if etype != 'verification-award':
            unverified.append({'event_id': event.get('event_id'),
                               'reason': f'unrecognised event_type {etype!r}'})
            continue
        if not event.get('verified'):
            unverified.append({'event_id': event.get('event_id'),
                               'reason': 'award-shaped event without verifier authority'})
            continue

        award = event.get('award', {})
        kind = award.get('kind', '')
        key = award.get('benchmark_key') or event.get('event_id', '')
        when = parse_iso(event['event_at'], what=f'event {event.get("event_id")}')

        slot = lane_slot(lane)
        credit, reason = True, ''
        if kind in ONCE_EVER_KINDS:
            if key in benchmark_keys:
                credit, reason = False, f'benchmark-once: {key} already credited'
            else:
                benchmark_keys.add(key)
        if kind in WEEKLY_CAPS:
            instants = capped_instants.setdefault((lane, kind), [])
            priors = cap_window_priors(instants, when)
            instants.append(when)
            if priors >= WEEKLY_CAPS[kind]:
                credit, reason = False, (
                    f'over-cap: {priors + 1}th verified {kind} in the rolling 168 h window '
                    f'ending at its verification instant (cap {WEEKLY_CAPS[kind]}); still '
                    'verified evidence, never banked, rolled into a later window or rescored')
        if kind in SCIENTIFIC_KINDS:
            result = award.get('result') or {}
            margin = result.get('margin')
            gap = result.get('material_gap_pct')
            if isinstance(margin, (int, float)) and (best_margin is None or margin > best_margin):
                best_margin = margin
            if isinstance(gap, (int, float)) and (best_gap is None or gap < best_gap):
                best_gap = gap

        slot['awards'] += 1
        if credit:
            slot['points'] += event.get('points', 0)
            slot['current_map_points'] += event.get('points', 0)
            if kind == 'map-point':
                # a distinct admitted point identity: counted separately from
                # its rubric score, so a +10 map point is one point, not ten
                slot['map_points_count'] += 1
                slot['current_map_map_points'] += 1
            model = event.get('model') or 'unknown'
            tallies_key = (lane, model)
            tally = model_tallies.setdefault(tallies_key, {
                'lane': lane, 'model': model, 'points': 0,
                'map_points': 0, 'awards': 0})
            tally['points'] += event.get('points', 0)
            tally['awards'] += 1
            if kind == 'map-point':
                tally['map_points'] += 1
        else:
            slot['uncredited'].append({'event_id': event.get('event_id'), 'reason': reason})
        if kind == 'tokens-100m' and credit:
            penalty_awarded[lane] = (penalty_awarded.get(lane, 0)
                                     + max(1, int(award.get('units', 1))))
        awards_by_id[event.get('event_id', '')] = {
            'event_id': event.get('event_id'), 'lane': lane, 'kind': kind,
            'bucket': 'current' if credit else None,
            'points': event.get('points', 0), 'credited': credit}

    leaderboard = sorted(model_tallies.values(),
                         key=lambda t: (-t['points'], t['lane'], t['model']))
    return {
        'map_version': current_map,
        'rubric_version': rubric_version,
        'lanes': lanes,
        'leaderboard': leaderboard,
        'unverified': unverified,
        'duplicate_events': duplicates,
        'margin': best_margin,
        'material_gap_pct': best_gap,
        'cost_entries': cost_entries,
        'penalty_awarded': penalty_awarded,
    }


def cost_view(view: dict, cfg: dict, state: dict | None = None) -> dict:
    """Session-keyed accounting under the scorer conventions (v0) section 2.
    Each session's native record reports a CUMULATIVE total: keep the latest
    snapshot per session (a redelivered or stale record never double-counts,
    a late-found record adds in when found) and sum sessions per lane.
    Overhead usage (Sciences head, scorer and her re-runs, CO, external
    review) is excluded from every lane and reported beside cost per point.
    The ratio appears only with an agreed basis and a non-zero verified-point
    denominator; a zero denominator is an unavailable ratio, never infinity
    or zero cost-per-point."""
    basis = cfg.get('cost', {}).get('ratio_basis', 'UNSET')
    # distinct admitted map-point identities over the programme lifetime —
    # never the summed rubric score, and never silently zero for want of a
    # ratio: the count and the score are separate facts
    validated_map_points = sum(l.get('map_points_count', 0)
                               for l in view['lanes'].values())
    verified_score = sum(l.get('points', 0) for l in view['lanes'].values())
    lane_sessions: dict[tuple[str, str], tuple[str, float, str]] = {}
    overhead_sessions: dict[tuple[str, str], tuple[str, float, str]] = {}
    unmeasured_by_key: dict[tuple[str, str], dict] = {}
    for entry in view['cost_entries']:
        lane = entry.get('lane') or '?'
        session = entry.get('session') or ''
        at = str(entry.get('at', ''))
        bucket = entry.get('bucket', 'lane')
        overhead = bucket == 'overhead'
        role = str(entry.get('role', ''))
        key_owner = f'overhead:{role}' if overhead else lane
        measured = (entry.get('coverage') == 'measured'
                    and isinstance(entry.get('tokens'), (int, float)))
        if not measured:
            prev = unmeasured_by_key.get((key_owner, session))
            if prev is None or at >= prev.get('at', ''):
                unmeasured_by_key[(key_owner, session)] = {
                    'owner': key_owner, 'session': session, 'role': role, 'at': at,
                    'coverage': entry.get('coverage', 'unavailable')}
            continue
        table = overhead_sessions if overhead else lane_sessions
        prev = table.get((key_owner, session))
        if prev is None or at > prev[0]:
            table[(key_owner, session)] = (at, entry['tokens'], entry.get('model', ''))
    lane_tokens: dict[str, float] = {}
    lane_model_tokens: dict[tuple[str, str], float] = {}
    for (owner, _session), (_at, tokens, model) in lane_sessions.items():
        lane_tokens[owner] = lane_tokens.get(owner, 0) + tokens
        if model:
            lane_model_tokens[(owner, model)] = lane_model_tokens.get((owner, model), 0) + tokens
    overhead_by_role: dict[str, float] = {}
    for (owner, _session), (_at, tokens, _model) in overhead_sessions.items():
        role = owner.split(':', 1)[1]
        overhead_by_role[role] = overhead_by_role.get(role, 0) + tokens

    observed = (state or {}).get('token_crossings', {})
    awarded_all = view.get('penalty_awarded', {})
    token_accounting = {}
    for lane, total in sorted(lane_tokens.items()):
        observable = int(total // TOKENS_PER_UNIT)
        awarded = int(awarded_all.get(lane, 0))
        lane_obs = observed.get(lane, {})
        seen = [k for k in range(1, observable + 1) if str(k) in lane_obs]
        pending = [{'crossing': k, 'observed_at': lane_obs[str(k)]['observed_at'],
                    'map_version_at_observation': lane_obs[str(k)].get('map_version')}
                   for k in seen if k > awarded]
        token_accounting[lane] = {
            'measured_tokens': total,
            'measured_sessions': sum(1 for (owner, _s) in lane_sessions if owner == lane),
            'crossings_observable': observable,
            'crossings_observed': len(seen),
            'penalty_events_awarded': awarded,
            'pending_crossings': pending,
            'crossings_not_yet_observed': [k for k in range(1, observable + 1)
                                           if str(k) not in lane_obs],
            'remainder_tokens': total - observable * TOKENS_PER_UNIT,
            'note': ('penalty points come only from Una-verified tokens-100m awards; the '
                     'ledger observes crossings and never mints them'),
        }
        over = awarded - len(seen)
        if over > 0:
            # Una's award is never refused and never rescored here; the
            # excess above observed crossings is surfaced for her disposition
            token_accounting[lane]['over_award_discrepancy'] = over
            token_accounting[lane]['note'] += (
                f'; WARNING: {over} penalty event(s) awarded above the '
                f'{len(seen)} observed crossing(s) — displayed for the Scorer, never rescinded')
    unmeasured = sorted(unmeasured_by_key.values(),
                        key=lambda u: (u['owner'], u['session']))
    measured_sessions = len(lane_sessions) + len(overhead_sessions)
    known_sessions = measured_sessions + len(unmeasured)
    named = sorted({u['session'] or u['owner'] for u in unmeasured})
    coverage_line = (f'measured {measured_sessions} of {known_sessions} known sessions'
                     + (f"; unmeasured: {', '.join(named)}" if named else ''))

    ratio = None
    if basis == 'UNSET':
        note = 'accounting basis not agreed; counts and measured cost shown separately'
    elif validated_map_points == 0:
        note = ('zero admitted map points: ratio unavailable, never zero or infinite '
                '(benchmarks, penalties and other kinds never create the denominator)')
    elif unmeasured:
        note = 'cost coverage incomplete: ratio unavailable'
    else:
        total = sum(lane_tokens.values())
        ratio = {'tokens': total, 'validated_map_points': validated_map_points,
                 'tokens_per_validated_map_point': total / validated_map_points,
                 'interval': cfg.get('cost', {}).get('interval', 'UNSET'),
                 'count_basis': ('distinct Una-admitted map-point identities, '
                                 'cumulative programme lifetime')}
        note = 'computed'
    return {
        'validated_map_points': validated_map_points,
        'verified_score': verified_score,
        'measured_tokens_per_lane': lane_tokens,
        'measured_tokens_per_lane_model': {f'{lane} · {model}': tokens
                                           for (lane, model), tokens
                                           in sorted(lane_model_tokens.items())},
        'programme_overhead_tokens': {'total': sum(overhead_by_role.values()),
                                      'by_role': overhead_by_role,
                                      'note': ('Sciences-head, scorer (and her re-runs), CO and '
                                               'review usage; excluded from every lane')},
        'unmeasured_sessions': unmeasured,
        'coverage_line': coverage_line,
        'token_accounting': token_accounting,
        'cost_per_verified_point': ratio,
        'cost_per_verified_point_note': note,
        'token_penalty_note': ('the per-100M-token penalty is a Una-verified award on measured '
                               'accounting evidence; observed crossings pend until she '
                               'admits them'),
    }


def update_token_observations(state: dict, board: dict, *, now_iso: str) -> bool:
    """Scorer conventions (v0) section 2: record, once and never rewritten,
    the regeneration instant that first observes each new 100M-token crossing
    per lane, with the map version current then. The observation dates the
    crossing for Una's award; it never mints the award, never backdates a
    late-found record and never rewrites a recorded date."""
    crossings = state.setdefault('token_crossings', {})
    changed = False
    for lane, data in board.get('token_accounting', {}).items():
        lane_x = crossings.setdefault(lane, {})
        for k in range(1, data['crossings_observable'] + 1):
            if str(k) not in lane_x:
                lane_x[str(k)] = {'observed_at': now_iso,
                                  'map_version': state.get('map_version')}
                changed = True
    return changed


def scoreboard(view: dict, cfg: dict, *, generated_at: str,
               state: dict | None = None) -> dict:
    missing = []
    if view['margin'] is None:
        missing.append('no verified map point: margin UNVERIFIED')
    if view['material_gap_pct'] is None:
        missing.append('material gap UNKNOWN')
    board = {
        'programme': cfg.get('programme', 'vacuum-float'),
        'generated_at': generated_at,
        'map_version': view['map_version'],
        'rubric_version': view['rubric_version'],
        'margin': {'value': view['margin'],
                   'status': 'UNVERIFIED' if view['margin'] is None else 'verified'},
        'material_gap_pct': {'value': view['material_gap_pct'],
                             'status': 'UNKNOWN' if view['material_gap_pct'] is None else 'verified'},
        'basis': 'Una-verified events only; empty initial state; no inherited, helium or predicted values',
        'lanes': {lane: {'points': data['points'],
                         'map_points': data.get('map_points_count', 0),
                         'current_map_points': data.get('current_map_points', 0),
                         'current_map_map_points': data.get('current_map_map_points', 0),
                         'prior_map_map_points': data.get('prior_map_map_points', 0),
                         'map_points_zeroed_by_audit': data.get('map_points_zeroed_by_audit', 0),
                         'prior_map_points': data.get('prior_map_points', 0),
                         'zeroed_by': data.get('zeroed_by'),
                         'uncredited': data.get('uncredited', [])}
                  for lane, data in view['lanes'].items()},
        'leaderboard': view.get('leaderboard', []),
        'unverified_nominations': view['unverified'],
        'duplicate_events': view.get('duplicate_events', []),
        'missing_data': missing,
    }
    board.update(cost_view(view, cfg, state))
    return board


def scoreboard_line(board: dict) -> str:
    margin = board['margin']['value']
    gap = board['material_gap_pct']['value']
    points = ' '.join(f"{lane} {data['points']:+d}"
                      for lane, data in sorted(board['lanes'].items())) or 'no lanes'
    map_points = sum(l.get('map_points', 0) for l in board['lanes'].values())
    missing = board['missing_data'][0] if board['missing_data'] else 'none'
    return (f"vacuum-float · map {board['map_version']} · rubric {board['rubric_version']} · "
            f"margin {'UNVERIFIED' if margin is None else margin} · "
            f"material gap {'UNKNOWN' if gap is None else f'{gap}%'} · "
            f"points {points} · map points {map_points} · verified by Una · "
            f"missing: {missing}")


# --------------------------------------------------------------------------
# stall episodes


def episode_anchor(events: list[dict], cfg: dict) -> tuple[str, str]:
    """The current stall episode key and its start: the programme-start
    anchor, or the LAST verified map-point award once one exists. Heartbeats,
    nominations, landings and cost updates never reset a scientific stall."""
    start = cfg.get('programme_start', {})
    key = f"anchor:{start.get('id', 'UNSET')}"
    at = start.get('at', '')
    best = None
    for event in events:
        if (event.get('event_type') == 'verification-award' and event.get('verified')
                and event.get('award', {}).get('kind') == 'map-point'):
            when = event.get('event_at', '')
            if when and (best is None or when > best[1]):
                best = (event['event_id'], when)
    if best is not None:
        key, at = f'map-point:{best[0]}', best[1]
    return key, at


def evaluate_stall(events: list[dict], cfg: dict, now: dt.datetime) -> dict:
    key, at = episode_anchor(events, cfg)
    if not at:
        return {'episode_key': key, 'anchor_at': None, 'elapsed_seconds': None,
                'due': [], 'note': 'no programme-start anchor configured'}
    started = parse_iso(at, what='episode anchor')
    elapsed = now - started
    due = []
    if elapsed >= STALL_DIAGNOSIS_AFTER:
        due.append('diagnosis-report')
    if elapsed >= STALL_DECISION_CARD_AFTER:
        due.append('admiral-decision-card')
    return {'episode_key': key, 'anchor_at': at,
            'elapsed_seconds': int(elapsed.total_seconds()), 'due': due}


def emit_stall_notices(ledger: Ledger, stall: dict, *, now_iso: str,
                       hb_state: dict,
                       card_dates: dict[str, str] | None = None) -> list[str]:
    """Idempotent per stall episode: a duplicate run cannot re-emit a notice
    already emitted for this episode. Historical episodes are retained after
    a later verified point resets the clock."""
    if not stall.get('due'):
        return []
    key = stall['episode_key']
    episodes = hb_state.setdefault('stall_episodes', {})
    episode = episodes.setdefault(key, {'anchor_at': stall.get('anchor_at'),
                                        'emitted': [], 'history': []})
    notices_dir = ledger.root / NOTICES_DIR_NAME
    fresh = []
    for kind in stall['due']:
        if kind in episode['emitted']:
            continue
        path = notices_dir / f"{key.replace(':', '_').replace('/', '_')}__{kind}.md"
        if kind == 'diagnosis-report':
            body = (
                "# 48h stall diagnosis — vacuum-float\n\n"
                f"Generated: {now_iso}\nEpisode anchor: {key} at {stall.get('anchor_at')}\n"
                f"Elapsed: {stall.get('elapsed_seconds')} s with no verified map point.\n\n"
                "No verified map point has landed within 48 hours of the episode anchor.\n"
                "Route: to the Desk through the CO's existing reporting route. This file is a\n"
                "mechanism artifact, not a queue message; the owner route delivers it.\n"
                "DEFAULT none. Not permission to act; no seat is stopped, woken or retired.\n")
        else:
            frozen_date = (card_dates or {}).get(key)
            date_text = (f"DEFAULT: pause. DATE: {frozen_date} (frozen at the card's "
                         "first creation, +48 h; retained on retry and late "
                         "delivery). Routed through the CO as a typed "
                         "admiral-decision."
                         if frozen_date else
                         "DEFAULT: pause. DATE: none set — routed through the CO as a "
                         "typed admiral-decision.")
            body = (
                "# 5-day stall admiral-decision card — vacuum-float\n\n"
                f"Generated: {now_iso}\nEpisode anchor: {key} at {stall.get('anchor_at')}\n"
                f"Elapsed: {stall.get('elapsed_seconds')} s with no verified map point.\n\n"
                "DECISION REQUIRED: continue or pause the vacuum-float programme.\n"
                f"{date_text} The default is not permission; nothing acts on this file.\n")
        atomic_write(path, body)
        episode['emitted'].append(kind)
        episode['history'].append({'kind': kind, 'at': now_iso, 'path': str(path)})
        fresh.append(str(path))
    return fresh


# --------------------------------------------------------------------------
# verbs


def cmd_ingest(args, cfg: dict) -> int:
    submissions = Path(args.submissions or cfg.get('submissions_dir', DEFAULT_SUBMISSIONS_DIR))
    with Ledger(args.ledger, cfg) as ledger:
        state = ledger.state()
        existing, torn = ledger.read_events()
        by_id: dict[str, dict] = {}
        for event in existing:
            by_id.setdefault(event.get('event_id'), event)
        state_dirty = False
        results = []
        for submission_id in args.id:
            try:
                record = read_submission(submissions, submission_id)
                event, classification = classify_submission(
                    record, cfg, base_dir=submissions, binding_dir=args.binding_dir,
                    verifier_seen=state.get('authority_seats_seen'),
                    admiral_seen=state.get('admiral_seats_seen'),
                    submissions_dir=submissions)
            except Refused as exc:
                results.append({'id': submission_id, 'result': 'refused', 'reason': str(exc)})
                continue
            event['ingested_at'] = args.now or iso_now()
            prior = by_id.get(event['event_id'])
            if prior is not None:
                if payload_digest(prior) == payload_digest(event):
                    results.append({'id': submission_id, 'result': 'no-op',
                                    'reason': 'identical replay of an accepted event'})
                else:
                    results.append({'id': submission_id, 'result': 'refused', 'reason': (
                        f'event id {event["event_id"]} already exists with a different payload; '
                        'no second award and no silent overwrite')})
                continue
            if event['event_type'] in ('map-version', 'rubric-change'):
                reason = check_forward_only(event, existing, state)
                if reason:
                    results.append({'id': submission_id, 'result': 'refused', 'reason': reason})
                    continue
            if event['event_type'] == 'correction':
                target = event['award']['target_event_id']
                if target not in by_id:
                    results.append({'id': submission_id, 'result': 'refused', 'reason': (
                        f'correction target {target} is not an existing event; '
                        'a correction must reference an earlier event')})
                    continue
            ledger.append(event)
            by_id[event['event_id']] = event
            results.append({'id': submission_id, 'result': classification,
                            'event_id': event['event_id']})
            if event['event_type'] == 'verification-award':
                seat = event.get('from_seat')
                if seat and seat not in state.get('authority_seats_seen', []):
                    state['authority_seats_seen'] = sorted(
                        set(state.get('authority_seats_seen', [])) | {seat})
                    state_dirty = True
            elif event['event_type'] == 'map-version':
                state['map_version'] = event['award']['map_version']
                state_dirty = True
            elif event['event_type'] == 'rubric-change':
                state['rubric_version'] = event['award']['rubric_version']
                state_dirty = True
        if state_dirty:
            ledger.write_state(state)
        report = {'ingested': results, 'torn_tail': torn['present']}
        print(json.dumps(report, indent=1))
        return 0


def check_forward_only(event: dict, existing: list[dict], state: dict) -> str | None:
    """map-version and rubric-change move forward only, and a rubric changes
    at most once per map version. Returns a refusal reason or None."""
    award = event.get('award', {})
    if event['event_type'] == 'map-version':
        new, old = award.get('map_version', ''), state['map_version']
        new_n, old_n = version_number(new), version_number(old)
        if new == old or (new_n is not None and old_n is not None and new_n <= old_n):
            return (f'map-version must move forward: {new!r} does not advance {old!r}')
        return None
    new, old = award.get('rubric_version', ''), state['rubric_version']
    new_n, old_n = version_number(new), version_number(old)
    if new == old or (new_n is not None and old_n is not None and new_n <= old_n):
        return f'rubric-version must move forward: {new!r} does not advance {old!r}'
    prior_changes = [e for e in existing if e.get('event_type') == 'rubric-change']
    if prior_changes:
        return (f'rubric already changed in map version {state["map_version"]}: '
                'at most one change per map version')
    return None


def cmd_scoreboard(args, cfg: dict) -> int:
    with Ledger(args.ledger, cfg) as ledger:
        state = ledger.state()
        events, torn = ledger.read_events()
        now_iso = args.now or iso_now()
        view = derive(events, cfg, state)
        board = scoreboard(view, cfg, generated_at=now_iso, state=state)
        if update_token_observations(state, board, now_iso=now_iso):
            ledger.write_state(state)
            # the regeneration that first observes a crossing reports it as
            # observed, so the published board matches the recorded state
            board = scoreboard(derive(events, cfg, state), cfg,
                               generated_at=now_iso, state=state)
        line = scoreboard_line(board)
        if args.json_out:
            atomic_write(Path(args.json_out), json.dumps(board, indent=1, sort_keys=True) + '\n')
        if args.out:
            atomic_write(Path(args.out), line + '\n')
        print(line)
        if torn['present']:
            print(f'TORN TAIL: {torn["bytes"]} uncommitted bytes; run repair-tail',
                  file=sys.stderr)
        return 0


def sha8(text: str) -> str:
    return hashlib.sha256(text.encode('utf-8')).hexdigest()[:8]


def notice_body(ptype: str, stall: dict, *, date_iso: str | None) -> str:
    """Queue body for a stall notice. The 5-day card's DATE is frozen at the
    delivery item's first creation and retained verbatim on every retry."""
    key = stall.get('episode_key')
    anchor = stall.get('anchor_at')
    elapsed = stall.get('elapsed_seconds')
    if ptype == 'diagnosis-report':
        return ("# 48 h stall diagnosis — vacuum-float\n\n"
                f"Episode {key} at {anchor}; {elapsed} s without a verified "
                "map point.\nRoute: the CO carries this diagnosis to the Desk "
                "(asks reply).\nDEFAULT none. Not permission to act; no seat "
                "is stopped, woken or retired.\n")
    date_line = (f"DATE: {date_iso} (first creation of this card +48 h; "
                 "retained on retry and late delivery)"
                 if date_iso else "DATE: none set")
    return ("# 5-day stall admiral-decision card — vacuum-float\n\n"
            f"Episode {key} at {anchor}; {elapsed} s without a verified "
            "map point.\nDECISION REQUIRED: continue or pause the "
            "vacuum-float programme.\nDEFAULT: pause. " + date_line + ".\n"
            "The default is not permission; nothing acts on this message, "
            "and the five-day trigger is not an automatic lifecycle "
            "action.\n")


class DeliveryStateError(Exception):
    """Existing delivery state is unreadable or not the delivery schema."""


def load_delivery(path: Path) -> dict:
    """Load the delivery-pending state (U3-D4): only an ABSENT file
    initializes a fresh queue. Unreadable bytes or a schema-invalid
    document raise DeliveryStateError so the caller fails closed with the
    original bytes preserved — pending work is never silently dropped and
    ids/sequences are never reset on top of existing evidence. The
    schema is exact: every item's map key equals its id, its id/type are
    nonempty strings, its type is one of the three delivery types with
    its required fields present and every consumed value well-formed —
    body a nonempty string, a notice's episode key a nonempty string,
    attempts (when present) a nonnegative integer never a boolean,
    created_at (when present) a string, the decision card's deadline a
    MANDATORY timezone-aware ISO string and any optional deadline on a
    line or diagnosis equally aware ISO when present — the admitted flag
    is an exact boolean when present, line sequences are
    unique positive integers (never booleans) and next_line_seq never
    sits below an existing sequence — all validated BEFORE any read, use,
    write or cursor recovery, so no consumer can treat a corrupt value as
    admitted evidence."""
    if not path.exists():
        return {'next_line_seq': 0, 'items': {}}
    try:
        doc = json.loads(path.read_text())
    except ValueError as exc:
        raise DeliveryStateError(
            f'{path}: delivery state is not readable JSON ({exc}); failing '
            'closed — the file is preserved untouched') from exc
    next_seq = doc.get('next_line_seq') if isinstance(doc, dict) else None
    items = doc.get('items') if isinstance(doc, dict) else None
    if (not isinstance(items, dict) or isinstance(next_seq, bool)
            or not isinstance(next_seq, int) or next_seq < 0):
        raise DeliveryStateError(
            f'{path}: delivery state does not match the delivery schema '
            '(expected object with an items map and a nonnegative integer '
            'next_line_seq); failing closed — the file is preserved untouched')
    type_required = {'line': ('seq', 'body'),
                     'diagnosis-report': ('body', 'episode_key'),
                     'admiral-decision-card': ('body', 'episode_key',
                                               'deadline')}
    seen_seq: set[int] = set()
    max_seq = 0
    for iid, item in items.items():
        if not isinstance(item, dict) or not item.get('id') or not item.get('type'):
            raise DeliveryStateError(
                f'{path}: delivery item {iid!r} lacks an id/type; failing '
                'closed — the file is preserved untouched')
        if not isinstance(item['id'], str) or not isinstance(item['type'], str):
            # ids name files and argv flags, types feed membership tests —
            # a non-string id or type is corrupt identity, never work
            raise DeliveryStateError(
                f'{path}: delivery item {iid!r} id/type must be nonempty '
                f'strings (id {item["id"]!r}, type {item["type"]!r}); '
                'failing closed — the file is preserved untouched')
        if item['id'] != iid:
            raise DeliveryStateError(
                f'{path}: delivery item {iid!r} carries id {item["id"]!r}; '
                'map key and id must be equal — failing closed, the file '
                'is preserved untouched')
        ptype = item['type']
        if ptype not in type_required:
            raise DeliveryStateError(
                f'{path}: delivery item {iid!r} has unknown type '
                f'{ptype!r}; failing closed — the file is preserved '
                'untouched')
        if 'admitted' in item and not isinstance(item['admitted'], bool):
            raise DeliveryStateError(
                f'{path}: delivery item {iid!r} admitted is '
                f'{item["admitted"]!r}, not an exact boolean — a truthy '
                'string or number is never admitted evidence; failing '
                'closed — the file is preserved untouched')
        if 'attempts' in item:
            att = item['attempts']
            if (isinstance(att, bool) or not isinstance(att, int)
                    or att < 0):
                raise DeliveryStateError(
                    f'{path}: delivery item {iid!r} attempts is {att!r}, '
                    'not a nonnegative integer (a boolean never counts) — '
                    'the counter feeds post-adapter arithmetic; failing '
                    'closed — the file is preserved untouched')
        # an ABSENT attempts key keeps the documented zero default: fresh
        # items start at zero and the heartbeat increments before a retry
        if 'created_at' in item and not isinstance(item['created_at'], str):
            raise DeliveryStateError(
                f'{path}: delivery item {iid!r} created_at is '
                f'{item["created_at"]!r}, not a string — ordering metadata '
                'is consumed by the due sort before any attempt; failing '
                'closed — the file is preserved untouched')
        for required in type_required[ptype]:
            if required not in item:
                raise DeliveryStateError(
                    f'{path}: delivery item {iid!r} ({ptype}) lacks '
                    f'required field {required!r}; failing closed — the '
                    'file is preserved untouched')
        # every CONSUMED value is validated here, before any adapter call,
        # cursor recovery or delivery write (U3-D4)
        body = item['body']
        if not isinstance(body, str) or not body:
            raise DeliveryStateError(
                f'{path}: delivery item {iid!r} body is {body!r}, not a '
                'nonempty string; failing closed — the file is preserved '
                'untouched')
        if ptype in ('diagnosis-report', 'admiral-decision-card'):
            ek = item['episode_key']
            if not isinstance(ek, str) or not ek:
                raise DeliveryStateError(
                    f'{path}: delivery item {iid!r} episode key is {ek!r}, '
                    'not a nonempty string; failing closed — the file is '
                    'preserved untouched')
        if ptype == 'admiral-decision-card':
            dl = item['deadline']
            if not isinstance(dl, str) or not dl:
                raise DeliveryStateError(
                    f'{path}: delivery item {iid!r} card deadline is '
                    f'{dl!r}; the decision-card DATE is mandatory — a '
                    'nonempty timezone-aware ISO string, frozen at first '
                    'creation and preserved on retry; failing closed — '
                    'the file is preserved untouched')
        elif 'deadline' in item:
            # OPTIONAL for lines and diagnoses, but a PRESENT key is
            # consumed verbatim into the adapter payload — null or naive
            # noise is never silently dropped at posting time
            dl = item['deadline']
            if not isinstance(dl, str) or not dl:
                raise DeliveryStateError(
                    f'{path}: delivery item {iid!r} optional deadline is '
                    f'{dl!r}, not a nonempty string; failing closed — the '
                    'file is preserved untouched')
        if 'deadline' in item and isinstance(item['deadline'], str):
            try:
                parsed = dt.datetime.fromisoformat(item['deadline'])
            except ValueError:
                parsed = None
            if (parsed is None or parsed.tzinfo is None
                    or parsed.utcoffset() is None):
                raise DeliveryStateError(
                    f'{path}: delivery item {iid!r} deadline '
                    f'{item["deadline"]!r} is not a timezone-aware ISO '
                    'timestamp (naive or unparsable); failing closed — '
                    'the file is preserved untouched')
        if ptype == 'line':
            seq = item['seq']
            if isinstance(seq, bool) or not isinstance(seq, int) or seq < 1:
                raise DeliveryStateError(
                    f'{path}: line {iid!r} seq {seq!r} is not a positive '
                    'integer (a boolean is never a sequence); failing '
                    'closed — the file is preserved untouched')
            if seq in seen_seq:
                raise DeliveryStateError(
                    f'{path}: line seq {seq} is duplicated under {iid!r}; '
                    'failing closed — the file is preserved untouched')
            seen_seq.add(seq)
            max_seq = max(max_seq, seq)
    if next_seq < max_seq:
        raise DeliveryStateError(
            f'{path}: next_line_seq {next_seq} is below the highest line '
            f'sequence {max_seq}, which would reuse an allocated sequence; '
            'failing closed — the file is preserved untouched')
    return doc


def delivery_items_due(delivery: dict) -> list[dict]:
    """Undelivered items in attempt priority: due 5-day cards first, then
    48 h diagnoses, then the oldest pending line. All pending items are
    retained even when the per-run attempt budget defers them."""
    pending = [it for it in delivery['items'].values() if not it.get('admitted')]
    rank = {'admiral-decision-card': 0, 'diagnosis-report': 1, 'line': 2}
    return sorted(pending, key=lambda it: (rank.get(it.get('type'), 3),
                                           it.get('created_at', ''),
                                           it.get('id', '')))


def cmd_heartbeat(args, cfg: dict) -> int:
    """The six-hour mechanism (delivery contract: Sciences disposition
    U3-BOUND-BINDINGS-1017). Regenerates the scoreboard — scoreboard.json
    atomically carries the exact line beside generated_at for the read-only
    morning-report projection — then works a PENDING DELIVERY QUEUE through
    the post adapter: logical items are persisted with stable ids, allocated
    sequence numbers and full payloads BEFORE any adapter call; the adapter
    freezes the envelope and proves admission against the stored submission.
    At most three adapter attempts per run (due 5-day card, then the 48 h
    diagnosis, then the oldest pending line); an undelivered due item is
    retried only on the next SCHEDULED run and makes the heartbeat exit
    nonzero. No in-run loop. Never awards anything."""
    with Ledger(args.ledger, cfg) as ledger:
        state = ledger.state()
        events, _torn = ledger.read_events()
        now_iso = args.now or iso_now()
        view = derive(events, cfg, state)
        board = scoreboard(view, cfg, generated_at=now_iso, state=state)
        if update_token_observations(state, board, now_iso=now_iso):
            ledger.write_state(state)
            board = scoreboard(derive(events, cfg, state), cfg,
                               generated_at=now_iso, state=state)
        line = scoreboard_line(board)
        board['line'] = line
        atomic_write(ledger.root / SCOREBOARD_JSON_NAME,
                     json.dumps(board, indent=1, sort_keys=True) + '\n')
        hb_path = ledger.root / HEARTBEAT_STATE_NAME
        hb_state = (json.loads(hb_path.read_text()) if hb_path.exists()
                    else {'last_line': None, 'runs': 0})
        delivery_path = ledger.root / DELIVERY_STATE_NAME
        try:
            delivery = load_delivery(delivery_path)
        except DeliveryStateError as exc:
            # fail closed BEFORE any delivery write: the corrupt bytes stay
            # byte-identical on disk, no adapter call happens, no id or
            # sequence is reused, and the timer's OnFailure sees rc 2
            print(f'float_progress: {exc}', file=sys.stderr)
            return 2
        changed = line != hb_state.get('last_line')
        if changed:
            atomic_write(ledger.root / SCOREBOARD_LINE_NAME, line + '\n')

        # -- stall evaluation and notice delivery items --------------------
        stall = evaluate_stall(events, cfg, parse_iso(now_iso, what='--now'))
        card_dates: dict[str, str] = {}
        for kind in (stall.get('due') or []):
            ptype = ('admiral-decision-card' if kind == 'admiral-decision-card'
                     else 'diagnosis-report')
            suffix = '5d' if ptype == 'admiral-decision-card' else '48h'
            nid = f"vf-stall-{sha8(str(stall.get('episode_key')))}-{suffix}"
            item = delivery['items'].get(nid)
            if item is not None and (item.get('episode_key')
                                     != stall.get('episode_key')
                                     or item.get('type') != ptype):
                # U3-D1: sha8 is 8 hex chars of digest, never proof — the
                # same prefix can arise for distinct episodes. Fail closed
                # with nothing written: the saved item is preserved, the
                # colliding episode is not silently suppressed under it,
                # and no adapter call happens this run.
                print(f'float_progress: delivery id collision under {nid}: '
                      f'saved episode {item.get("episode_key")!r} type '
                      f'{item.get("type")!r} != incoming episode '
                      f'{stall.get("episode_key")!r} type {ptype!r}',
                      file=sys.stderr)
                return 2
            if item is None:
                item = {'id': nid, 'type': ptype, 'created_at': now_iso,
                        'attempts': 0, 'admitted': False,
                        'episode_key': stall.get('episode_key')}
                if ptype == 'admiral-decision-card':
                    # DATE is set at the card's FIRST CREATION (+48 h) and
                    # never recomputed, retained on retry and late delivery
                    date_iso = (parse_iso(now_iso, what='--now')
                                + dt.timedelta(hours=48)).isoformat()
                    item['deadline'] = date_iso
                    item['body'] = notice_body(ptype, stall, date_iso=date_iso)
                else:
                    item['body'] = notice_body(ptype, stall, date_iso=None)
                delivery['items'][nid] = item
            if item.get('deadline'):
                card_dates[item.get('episode_key') or ''] = item['deadline']
        notices = emit_stall_notices(ledger, stall, now_iso=now_iso,
                                     hb_state=hb_state,
                                     card_dates=card_dates)

        # -- the line item --------------------------------------------------
        # U3-D3: the delivery state is DURABLE and authoritative for
        # admissions; the heartbeat cursor is a cache. A crash after an
        # item's admitted write but before the cursor write leaves the
        # cursor behind — recover forward from the durable admitted
        # sequence BEFORE deciding whether a new line item is needed, so
        # an unchanged already-admitted line never gets a fresh id and a
        # second submission. Reversing the two writes would only move the
        # crash window; recovery from the durable side closes it.
        durable_seq = max(
            (it.get('seq', 0) for it in delivery['items'].values()
             if it.get('type') == 'line' and it.get('admitted')), default=0)
        if durable_seq > hb_state.get('last_admitted_seq', 0):
            hb_state['last_admitted_seq'] = durable_seq
            for it in delivery['items'].values():
                if (it.get('type') == 'line' and it.get('admitted')
                        and it.get('seq') == durable_seq):
                    hb_state['last_admitted_line'] = it.get('body')
            hb_state['delivery_cursor_recovered_at'] = now_iso
        last_admitted = hb_state.get('last_admitted_line')
        line_pending = any(it.get('type') == 'line' and not it.get('admitted')
                           and it.get('body') == line
                           for it in delivery['items'].values())
        if line != last_admitted and not line_pending:
            # the sequence is allocated at pending-item creation, not at
            # successful publication, so the id is stable through crash and
            # retry; the first admitted line is the one-time baseline
            seq = delivery.get('next_line_seq', 0) + 1
            delivery['next_line_seq'] = seq
            lid = f'vf-line-{seq}-{sha8(line)}'
            delivery['items'][lid] = {'id': lid, 'type': 'line', 'seq': seq,
                                      'body': line, 'created_at': now_iso,
                                      'attempts': 0, 'admitted': False}
        # persist logical items and payloads BEFORE calling the adapter
        atomic_write_json(delivery_path, delivery)

        # -- bounded adapter attempts ---------------------------------------
        results = []
        attempted = 0
        if args.post_command:
            for item in delivery_items_due(delivery):
                if attempted >= HEARTBEAT_MAX_POST_ATTEMPTS:
                    break  # deferred items stay pending and fail the run
                payload = {'type': item['type'], 'id': item['id'],
                           'body': item['body'], 'now': now_iso}
                if item.get('deadline'):
                    payload['deadline'] = item['deadline']
                try:
                    proc = subprocess.run(args.post_command,
                                          input=json.dumps(payload) + '\n',
                                          capture_output=True, text=True,
                                          timeout=HEARTBEAT_POST_TIMEOUT_S)
                    rc, err = proc.returncode, (proc.stderr or '').strip()[:200]
                except subprocess.TimeoutExpired:
                    rc, err = (f'timeout after {HEARTBEAT_POST_TIMEOUT_S} s',
                               'adapter timed out')
                except OSError as exc:
                    rc, err = ('start-failure', f'adapter failed to start: {exc}')
                item['attempts'] = item.get('attempts', 0) + 1
                item['last_attempt_at'] = now_iso
                item['last_rc'] = rc
                if rc == 0:
                    item['admitted'] = True
                    item['admitted_at'] = now_iso
                    item.pop('last_error', None)
                    if (item['type'] == 'line'
                            and item.get('seq', 0) > hb_state.get(
                                'last_admitted_seq', 0)):
                        hb_state['last_admitted_line'] = item['body']
                        hb_state['last_admitted_seq'] = item['seq']
                else:
                    item['last_error'] = f'rc={rc}: {err}'
                atomic_write_json(delivery_path, delivery)
                attempted += 1
                results.append({'id': item['id'], 'type': item['type'],
                                'rc': rc, 'admitted': bool(item['admitted'])})

        undelivered = delivery_items_due(delivery)
        hb_state['runs'] = hb_state.get('runs', 0) + 1
        hb_state['last_run_at'] = now_iso
        hb_state['last_line'] = line                      # regenerated
        hb_state['last_admitted_line'] = hb_state.get('last_admitted_line')
        hb_state['last_published_line'] = hb_state.get('last_admitted_line')
        hb_state['pending_delivery'] = [it['id'] for it in undelivered]
        hb_state['last_stall'] = stall
        atomic_write_json(hb_path, hb_state)
        print(json.dumps({'line': line, 'changed': changed, 'stall': stall,
                          'new_notices': notices,
                          'delivery_attempts': results,
                          'pending_delivery': hb_state['pending_delivery'],
                          'activation': state.get('activation')}, indent=1))
        # any due undelivered item — including items the attempt budget
        # deferred — fails the run for the timer's OnFailure, with no loop
        if args.post_command and undelivered:
            return 1
        return 0


def cmd_status(args, cfg: dict) -> int:
    with Ledger(args.ledger, cfg) as ledger:
        state = ledger.state()
        events, torn = ledger.read_events()
        board = scoreboard(derive(events, cfg, state), cfg,
                           generated_at=args.now or iso_now(), state=state)
        report = {
            'ledger': str(ledger.root),
            'events': len(events),
            'torn_tail': torn,
            'activation': state.get('activation'),
            'verifier_seats': sorted(resolve_verifier_seats(
                cfg, binding_dir=args.binding_dir, extra=state.get('authority_seats_seen'))),
            'scoreboard': board,
            'scoreboard_line': scoreboard_line(board),
        }
        print(json.dumps(report, indent=1, sort_keys=True))
        return 0


def cmd_selfcheck(args, cfg: dict) -> int:
    problems = []
    with Ledger(args.ledger, cfg) as ledger:
        events, torn = ledger.read_events()
        if torn['present']:
            problems.append(f'torn tail of {torn["bytes"]} bytes (interrupted append)')
        seen: dict[str, str] = {}
        for event in events:
            eid = event.get('event_id', '')
            digest = payload_digest(event)
            if eid in seen and seen[eid] != digest:
                problems.append(f'conflicting payload under event id {eid}')
            seen[eid] = digest
            etype = event.get('event_type')
            if etype not in EVENT_TYPES:
                problems.append(f'{eid}: unrecognised event_type {etype!r}')
                continue
            if etype == 'verification-award':
                award = event.get('award', {})
                kind = award.get('kind', '')
                if not event.get('verified'):
                    problems.append(f'{eid}: award event without verified authority')
                elif kind not in RUBRIC_V0:
                    problems.append(f'{eid}: unknown award kind {kind!r}')
                elif event.get('points') != expected_points(kind, award):
                    problems.append(f'{eid}: points do not match rubric v0 for {kind!r}')
            elif etype == 'audit-zero':
                if not (event.get('award', {}).get('lane')
                        and event.get('award', {}).get('map_version')):
                    problems.append(f'{eid}: audit-zero without lane and map_version')
            elif etype == 'correction':
                award = event.get('award', {})
                if not (award.get('target_event_id')
                        and award.get('action') in ('revoke', 'amend')):
                    problems.append(f'{eid}: correction without target_event_id and valid action')
            elif etype in ('map-version', 'rubric-change'):
                field = ('map_version' if etype == 'map-version' else 'rubric_version')
                if not event.get('award', {}).get(field):
                    problems.append(f'{eid}: {etype} without {field}')
    if problems:
        print(json.dumps({'status': 'FAIL', 'problems': problems}, indent=1))
        return 1
    print(json.dumps({'status': 'OK', 'events_checked': len(seen)}))
    return 0


def cmd_repair_tail(args, cfg: dict) -> int:
    with Ledger(args.ledger, cfg) as ledger:
        print(json.dumps(ledger.repair_tail(), indent=1))
    return 0


def cmd_schema(args) -> int:
    with SCHEMA_FILE.open() as fh:
        print(fh.read(), end='')
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description='Vacuum Float progress ledger, scoreboard and heartbeat (U3 plumbing).')
    parser.add_argument('--ledger', help='owned ledger directory (explicit, never the repository)')
    parser.add_argument('--config', help='JSON configuration (default: research/program/vacuum-float/state-initial.json)')
    parser.add_argument('--binding-dir', help='ship binding directory for canonical verifier resolution')
    sub = parser.add_subparsers(dest='verb', required=True)

    p = sub.add_parser('ingest', help='ingest accepted queue submissions by exact id (read-only)')
    p.add_argument('--id', action='append', required=True, dest='id',
                   help='submission id; repeatable')
    p.add_argument('--submissions', help='submissions directory (default from config)')
    p.add_argument('--now', help=argparse.SUPPRESS)
    p.set_defaults(fn=cmd_ingest)

    p = sub.add_parser('scoreboard', help='derive and optionally write the scoreboard')
    p.add_argument('--out', help='write the single scoreboard line here')
    p.add_argument('--json-out', help='write the full scoreboard JSON here')
    p.add_argument('--now', help=argparse.SUPPRESS)
    p.set_defaults(fn=cmd_scoreboard)

    p = sub.add_parser('heartbeat', help='six-hour mechanism run: regenerate, publish on change, evaluate stalls')
    p.add_argument('--post-command', nargs=argparse.REMAINDER, metavar='ARGV',
                   help='sanctioned posting adapter argv; the line arrives on stdin (default: none — activation blocked)')
    p.add_argument('--now', help=argparse.SUPPRESS)
    p.set_defaults(fn=cmd_heartbeat)

    p = sub.add_parser('status', help='ledger summary, unverified nominations with reasons, activation state')
    p.add_argument('--now', help=argparse.SUPPRESS)
    p.set_defaults(fn=cmd_status)

    p = sub.add_parser('selfcheck', help='verify ledger invariants; nonzero exit on violation')
    p.set_defaults(fn=cmd_selfcheck)

    p = sub.add_parser('repair-tail', help='truncate one torn final append (uncommitted bytes only)')
    p.set_defaults(fn=cmd_repair_tail)

    p = sub.add_parser('schema', help='print the machine-readable event schema')
    p.set_defaults(fn=cmd_schema)

    args = parser.parse_args(argv)
    if args.verb == 'schema':
        return cmd_schema(args)
    if not args.ledger:
        parser.error('--ledger is required for every verb except schema')
    cfg = load_config(args.config)
    try:
        return args.fn(args, cfg)
    except Refused as exc:
        print(f'REFUSED: {exc}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
