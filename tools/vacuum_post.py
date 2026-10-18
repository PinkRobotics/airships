#!/usr/bin/env python3
"""vacuum_post.py — the vacuum-float delivery adapter (U3 bindings, 2026-10-17).

Reads ONE JSON object on stdin — {"type", "id", "body", "deadline"?} — and
files it through the ship's submit.py door under the operator machinery
identity. It never writes the runtime store directly: every filing goes
through submit.py, and admission is proven only by comparing the stored
submission's authored fields against the frozen envelope.

Bindings (Sciences disposition U3-BOUND-BINDINGS-DISPOSITION-1017):
  - the addressee is resolved ONCE per logical delivery, from the runtime's
    binding/<billet>.json principal.seat, and the full envelope is frozen in
    the owned delivery state BEFORE the first submission; a retry reuses the
    frozen envelope verbatim and never re-resolves addressee or deadline;
  - a printed SUBMITTED proves nothing: admission is the stored submission
    carrying the same authored payload (queue-added timestamps and ingest
    metadata are not authored payload);
  - an earlier identical admission of the same id is success; a conflicting
    payload under the same id is an error (fail closed); sha8 is never proof.
    A retry carrying a CHANGED type/body/deadline under a frozen id is a
    collision: it fails closed and the saved evidence is never replaced.
    Admission comparison covers the complete authored semantic projection
    of the door, where absence is meaning — every expected key must be
    PRESENT (the door writes authority/re/supersedes as explicit nulls),
    values compare by recursive type-sensitive JSON equality (bool/int and
    float/int are distinct; nested drift is a conflict), and an unexpected
    nonempty deadline/authority/standing/links (or re/supersedes/thread/
    scope or any key outside the envelope and the door's documented
    stamps) in the store rejects.

Exit codes (the heartbeat treats any nonzero as keep-pending):
  0  admitted now, or an earlier identical admission verified
  2  CONFLICT: the same id carries a different authored payload — operator
  3  submit.py refused (its documented rc 1), a definite no
  4  no admission evidence (submit crashed, exited oddly, timed out, or
     filed nothing)
  5  addressee binding unresolved — nothing filed, kept pending

Bounds: submit.py is held to SUBMIT_TIMEOUT_S; the caller holds each adapter
call to 150 s. Stdlib only.
"""
import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SUBMIT_TIMEOUT_S = 120
UNIT = 'vacuum-float-heartbeat'
FROM = 'operator'
KIND = 'report'

ROUTES = {
    'line': {
        'billet': 'sciences', 'asks': 'none',
        'completion': ('information only: the vacuum-float scoreboard line '
                       'changed; nobody acts on an unchanged line'),
    },
    'diagnosis-report': {
        'billet': 'co', 'asks': 'reply',
        'completion': ('48 h stall diagnosis: no verified map point within 48 '
                       'hours of the episode anchor; carried to the Desk '
                       'through the CO'),
    },
    'admiral-decision-card': {
        'billet': 'co', 'asks': 'admiral-decision',
        'completion': ('five days without a verified map point: admiral '
                       'decision requested, DEFAULT pause'),
    },
}
# The genuine transport/stamp set, verbatim from the submit door's own
# _STAMPS (ship/tools/submit.py): at, ingested, from_seat, _vouched,
# links_schema, _intake_deferred, admiral_seat. The door stamps these at
# admission; a sender never authors them. NOTHING else is excluded.
DOOR_STAMPS = frozenset({'at', 'ingested', 'from_seat', '_vouched',
                         'links_schema', '_intake_deferred', 'admiral_seat'})
# Keys the door writes ONLY when the sender authored a value (submit.py
# writes each under an authored-if): next, standing, links, thread,
# also_thread, scope, via, door, deadline, next_owner, reservations,
# links_none. When the envelope authors none of them, meaningful absence
# is the stored key being ABSENT — present at all is a conflict.
DOOR_CONDITIONAL = frozenset({'links_none', 'next', 'standing', 'links',
                              'thread', 'also_thread', 'scope', 'via',
                              'door', 'deadline', 'next_owner',
                              'reservations'})
# Keys the door writes unconditionally with a door default when the
# sender authored none (submit.py doc construction): authority, re and
# supersedes are written null; priority defaults to 5; asks defaults to
# 'none'. These compare against the door default, never skip.
DOOR_DEFAULTS = {'authority': None, 're': None, 'supersedes': None,
                 'priority': 5, 'asks': 'none'}
# Receipt label for the complete compared projection (U3-D2): the receipt
# names the ACTUAL fields compared for this envelope — never the characters
# of a description string. The audit dimensions beside the per-field
# comparison are described once, in PROJECTION.
PROJECTION = ('sender-authored fields compared by recursive type-sensitive '
              'JSON equality + door defaults + conditional absence + '
              'unexpected-key audit')


def sha8(text: str) -> str:
    return hashlib.sha256(text.encode()).hexdigest()[:8]


def json_type_equal(want, got) -> bool:
    """Recursive JSON-type-sensitive equality (U3-D2): Python == is not
    JSON equality — True == 1 and 5 == 5.0 compare equal, and the drift
    hides just as well nested inside containers. bool/int/float are
    distinct scalar types; dicts compare key sets then values; lists
    compare lengths then elements; everything else compares by type,
    then value."""
    if type(want) is not type(got):
        return False
    if isinstance(want, dict):
        return (want.keys() == got.keys()
                and all(json_type_equal(want[k], got[k]) for k in want))
    if isinstance(want, list):
        return (len(want) == len(got)
                and all(json_type_equal(a, b) for a, b in zip(want, got)))
    return want == got


def atomic_write_json(path: Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix='.vacuum_post.')
    try:
        with os.fdopen(fd, 'w') as fh:
            json.dump(obj, fh, indent=1, sort_keys=True)
            fh.write('\n')
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def resolve_principal(runtime: Path, billet: str) -> str | None:
    """Current principal seat for a billet, or None when unresolved. Read
    only; a succession affects new deliveries, never a frozen envelope."""
    binding = runtime / 'binding' / f'{billet}.json'
    try:
        doc = json.loads(binding.read_text())
    except (OSError, ValueError):
        return None
    seat = (doc.get('principal') or {}).get('seat')
    return seat or None


def build_envelope(payload: dict, runtime: Path) -> tuple[dict | None, str]:
    """Resolve the route once and freeze the full authored envelope."""
    ptype = payload.get('type')
    route = ROUTES.get(ptype)
    if route is None:
        return None, f'unknown delivery type {ptype!r}'
    to_seat = resolve_principal(runtime, route['billet'])
    if not to_seat:
        return None, (f'binding unresolved for billet {route["billet"]!r}; '
                      'kept pending without filing')
    envelope = {
        'id': payload.get('id'),
        'kind': KIND,
        'from': FROM,
        'to': to_seat,
        'unit': UNIT,
        'completion': route['completion'],
        'body': payload.get('body'),
        'asks': route['asks'],
        'links_none': True,
        'priority': 5,
    }
    if ptype == 'diagnosis-report':
        envelope['next'] = f'{to_seat}: carry the 48 h stall diagnosis to the Desk'
    else:
        envelope['next'] = 'none'
    if payload.get('deadline'):
        envelope['deadline'] = payload['deadline']
    return envelope, ''


def submit_argv(submit: Path, envelope: dict) -> list[str]:
    argv = [sys.executable, '-I', str(submit),
            '--id', envelope['id'], '--from', FROM, '--to', envelope['to'],
            '--kind', KIND, '--body', envelope['body'],
            '--completion', envelope['completion'],
            '--asks', envelope['asks'], '--unit', UNIT, '--link', 'none',
            '--next', envelope['next']]
    if envelope.get('deadline'):
        argv += ['--deadline', envelope['deadline']]
    return argv


def expected_stored(envelope: dict) -> dict:
    """The COMPLETE sender-authored semantic projection the stored
    submission must carry for this envelope (U3-D2): every key the
    envelope authors compares; door-written defaults (authority/re/
    supersedes null, priority 5, asks 'none') compare against their
    default when unauthored; conditional keys the envelope does not
    author are expected ABSENT — absence is meaning. Derived from the
    actual submit.py door contract, so an unexpected value in any
    authored semantic field is a conflict rather than a skip."""
    expected = dict(envelope)  # every authored key compares, no list
    for key, default in DOOR_DEFAULTS.items():
        expected.setdefault(key, default)
    if expected.get('asks') is None:
        expected['asks'] = 'none'
    return expected


def admission_differs(stored: dict, envelope: dict) -> list[str]:
    """Complete semantic comparison against expected_stored plus an
    exhaustive stored-key audit (U3-D2): only the door's documented
    _STAMPS (at/ingested/from_seat/_vouched/links_schema/
    _intake_deferred/admiral_seat) are excluded; conditional keys the
    envelope never authored (deadline/standing/links/re-supplied
    thread/scope/via/...) must be ABSENT, and any stored key outside the
    envelope + door contract is an unexpected authored field — both
    reject instead of comparing identical."""
    problems = []
    expected = expected_stored(envelope)
    for field, want in expected.items():
        if field not in stored:
            # the genuine door writes EVERY expected key — authority, re
            # and supersedes as explicit nulls — so a missing key is a
            # conflict, never the unauthored default in disguise (U3-D2)
            problems.append(f'{field}: absent from the stored submission')
        elif not json_type_equal(want, stored[field]):
            problems.append(f'{field}: filed {stored[field]!r} != envelope '
                            f'{want!r} (type-sensitive)')
    for field in sorted(DOOR_CONDITIONAL - set(envelope)):
        if field in stored:
            problems.append(f'{field}: filed {stored[field]!r} '
                            '!= envelope absence')
    explained = set(expected) | (DOOR_CONDITIONAL - set(envelope))
    for field in sorted(set(stored) - explained - DOOR_STAMPS):
        problems.append(f'{field}: unexpected authored field '
                        f'{stored[field]!r}')
    return problems


def read_admission(runtime: Path, item_id: str) -> dict | None:
    path = runtime / 'queue' / 'submissions' / f'{item_id}.json'
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument('--runtime', required=True,
                    help='ship runtime root (binding/ and queue/ live here)')
    ap.add_argument('--submit', required=True,
                    help='path to the ship submit.py door')
    ap.add_argument('--delivery-state', required=True,
                    help='owned directory for frozen envelopes and receipts')
    args = ap.parse_args()

    try:
        payload = json.loads(sys.stdin.read())
    except ValueError as exc:
        print(f'vacuum_post: stdin is not JSON: {exc}', file=sys.stderr)
        return 4
    item_id = payload.get('id')
    if not item_id or not payload.get('type') or payload.get('body') is None:
        print('vacuum_post: payload needs type, id and body', file=sys.stderr)
        return 4

    runtime = Path(args.runtime)
    state_path = Path(args.delivery_state) / f'{item_id}.json'
    state_path.parent.mkdir(parents=True, exist_ok=True)

    if state_path.exists():
        try:
            state = json.loads(state_path.read_text())
        except ValueError:
            state = {}
        envelope = state.get('envelope')
        if not envelope:
            print(f'vacuum_post: delivery state for {item_id} is corrupt',
                  file=sys.stderr)
            return 2
        # U3-D1: the saved envelope is reused only for the SAME logical
        # request. A changed type/body/deadline arriving under this id is a
        # collision: fail closed, file nothing, and leave the saved state
        # untouched (no write — the evidence stays exactly as frozen).
        frozen_identity = {'type': state.get('type'),
                           'body': envelope.get('body'),
                           'deadline': envelope.get('deadline')}
        incoming = {'type': payload.get('type'),
                    'body': payload.get('body'),
                    'deadline': payload.get('deadline')}
        if incoming != frozen_identity:
            print(f'vacuum_post: CONFLICT under {item_id}: incoming request '
                  f'{incoming!r} != frozen identity {frozen_identity!r}',
                  file=sys.stderr)
            return 2
        # frozen envelope reused verbatim; addressee/deadline never re-resolved
    else:
        envelope, why = build_envelope(payload, runtime)
        if envelope is None:
            print(f'vacuum_post: {why}', file=sys.stderr)
            return 5
        state = {'id': item_id, 'type': payload['type'],
                 'frozen_at': None, 'attempts': 0, 'admitted': False}
        state['envelope'] = envelope
        # freeze BEFORE the first submission, so a crash never re-resolves
        atomic_write_json(state_path, state)

    state['attempts'] = state.get('attempts', 0) + 1
    state['last_attempt_at'] = payload.get('now', '')

    # an earlier identical admission is success without filing again
    stored = read_admission(runtime, item_id)
    if stored is not None:
        problems = admission_differs(stored, envelope)
        if not problems:
            state['admitted'] = True
            state['admitted_by'] = 'prior identical admission'
            state['receipt'] = {'submission': item_id,
                                'compared_fields': sorted(expected_stored(
                                    envelope)),
                                'projection': PROJECTION}
            atomic_write_json(state_path, state)
            print(f'vacuum_post: {item_id} already admitted (identical payload)')
            return 0
        print(f'vacuum_post: CONFLICT under {item_id}: ' + '; '.join(problems),
              file=sys.stderr)
        state['last_error'] = 'conflicting payload under the same id'
        state['admitted'] = False  # fail closed: the store no longer matches
        state.pop('admitted_by', None)
        atomic_write_json(state_path, state)
        return 2

    try:
        proc = subprocess.run(submit_argv(Path(args.submit), envelope),
                              capture_output=True, text=True,
                              timeout=SUBMIT_TIMEOUT_S)
        out = (proc.stdout or '') + (proc.stderr or '')
    except subprocess.TimeoutExpired:
        out = f'submit.py timed out after {SUBMIT_TIMEOUT_S} s'
        proc = None
    except OSError as exc:
        out = f'submit.py failed to start: {exc}'
        proc = None

    stored = read_admission(runtime, item_id)
    if stored is not None:
        problems = admission_differs(stored, envelope)
        if not problems:
            state['admitted'] = True
            state['admitted_by'] = 'filed this attempt'
            state['receipt'] = {'submission': item_id,
                                'compared_fields': sorted(expected_stored(
                                    envelope)),
                                'projection': PROJECTION}
            atomic_write_json(state_path, state)
            print(f'vacuum_post: {item_id} admitted')
            return 0
        print(f'vacuum_post: CONFLICT under {item_id}: ' + '; '.join(problems),
              file=sys.stderr)
        state['last_error'] = 'conflicting payload under the same id'
        state['admitted'] = False  # fail closed: the store no longer matches
        state.pop('admitted_by', None)
        atomic_write_json(state_path, state)
        return 2

    # submit.py's documented refusal is rc 1 with a REFUSED line; anything
    # else nonzero (a crash, rc 9) is no admission evidence, still retryable
    refused = proc is not None and proc.returncode == 1
    immutable = 'exists (submissions are immutable)' in out
    if refused and not immutable:
        # a definite no (bad flag, unknown seat): kept pending, reported
        state['last_error'] = f'submit rc={proc.returncode}: {out.strip()[:300]}'
        atomic_write_json(state_path, state)
        print(f'vacuum_post: {item_id} refused: {out.strip()[:300]}',
              file=sys.stderr)
        return 3
    # filed nothing provable: rc 0 without a store entry, an immutable-exists
    # without a readable store entry, a crash or a timeout — all retryable
    # under the SAME id on the next scheduled run
    state['last_error'] = f'no admission evidence: {out.strip()[:300]}'
    atomic_write_json(state_path, state)
    print(f'vacuum_post: {item_id} pending (no admission evidence)',
          file=sys.stderr)
    return 4


if __name__ == '__main__':
    sys.exit(main())
