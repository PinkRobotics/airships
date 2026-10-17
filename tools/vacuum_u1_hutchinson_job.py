#!/usr/bin/env python3
"""One-use bounded response launcher; file measured pre-solve queue record first.

Configuration is an owned, pinned execution manifest, not a method parameter file.
There is deliberately no retry/resume, mesh selection or tolerance override.
"""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import traceback


CASE_SHA = "7cb94fc2614a45d864a533e525fda7b567eb820293ba03f0377b94df92c4b252"
PROTOCOL_SHA = "86b6abca429983c9e907b0bf99cc8923361c5e08cc316d4e59a1f3ce6548590c"
ORDER = "ord-sciences-g1-fourth-hutchinson-frozen-implement-run-1017"
SEAT = "lead-sciences-1228320beb59564c"
REPORT = "rpt-1228-u1-fourth-hutchinson-pre-solve-1017"
TOTAL_SECONDS = 7200
CLEANUP_SECONDS = 12
THREADS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "BLIS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS",
           "GOTO_NUM_THREADS", "OMP_THREAD_LIMIT")


def utc():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def home(path):
    result = Path(path).resolve()
    if not result.is_relative_to("/home"):
        raise ValueError(f"Outside /home: {result}")
    return result


def write(path, value):
    with home(path).open("x") as stream:
        json.dump(value, stream, indent=2, allow_nan=False)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())


def scope_status(unit):
    result = subprocess.run(["systemctl", "--user", "show", unit+".scope",
                             "-p", "ActiveState", "-p", "SubState", "-p", "ControlGroup"],
                            capture_output=True, text=True, timeout=3)
    if result.returncode:
        raise RuntimeError(f"Cannot measure scope {unit}: {result.stderr}")
    fields = dict(line.split("=", 1) for line in result.stdout.splitlines() if "=" in line)
    return fields


def inactive(fields):
    return fields.get("ActiveState") == "inactive" and fields.get("ControlGroup") == ""


def launch_window(started, current):
    total_deadline = started + TOTAL_SECONDS
    response_deadline = total_deadline - CLEANUP_SECONDS
    remaining = math.floor(response_deadline-current)
    if remaining < 3:
        raise RuntimeError("Setup exhausted the response allocation; no response launched")
    return dict(total_deadline=total_deadline, response_deadline=response_deadline,
                scope_seconds=remaining, timeout_seconds=remaining-2,
                cleanup_reserved_seconds=CLEANUP_SECONDS)


def check_pins(config):
    for record in config["pins"]:
        if sha(home(record["path"])) != record["sha256"]:
            raise RuntimeError(f"Changed prerequisite: {record['path']}")
    repo = home(config["source"])
    base = repo / "research/validation/vacuum-float/u1/hutchinson-dimple"
    if sha(base/"case.json") != CASE_SHA or sha(base/"protocol.json") != PROTOCOL_SHA:
        raise RuntimeError("Frozen method/case does not match")
    for unit in config["inactive_scopes"]:
        state = scope_status(unit)
        if not inactive(state):
            raise RuntimeError(f"Heavy scope not confirmed inactive: {unit}: {state}")
    if config["authority"] != ORDER:
        raise RuntimeError("Unexpected authority")


def launch(config_path, config):
    started = time.monotonic()
    root = home(config["output"])
    root.mkdir(exist_ok=True)
    # Exclusive creation is the irreversible attempt reservation, before setup.
    write(root/"attempt-reserved.json", dict(at=utc(), config=str(config_path),
          config_sha256=sha(config_path), authority=ORDER,
          deadline_monotonic=started+TOTAL_SECONDS, no_restart=True,
          cleanup_reserved_seconds=CLEANUP_SECONDS))
    unit = config["unit"]
    exit_code, cleanup, terminal_error = 2, None, None
    started_scope = False
    try:
        check_pins(config)
        if not inactive(scope_status(unit)):
            raise RuntimeError("Response scope is not inactive before reservation")
        env = os.environ.copy()
        env.update({key: "1" for key in THREADS})
        env.update(PYTHON_CPU_COUNT="1", OMP_DYNAMIC="FALSE", MKL_DYNAMIC="FALSE",
                   CUDA_VISIBLE_DEVICES="", PYTHONUNBUFFERED="1", PYTHONDONTWRITEBYTECODE="1")
        for key, name in (("TMPDIR", "tmp"), ("TMP", "tmp"), ("TEMP", "tmp"),
                          ("XDG_CACHE_HOME", "cache")):
            directory = root/name
            directory.mkdir(exist_ok=True)
            env[key] = str(directory)
        cpu = min(os.sched_getaffinity(0))
        window = launch_window(started, time.monotonic())
        command = ["systemd-run", "--user", "--scope", "--unit="+unit,
                   "-p", "CPUQuota=100%", "-p", "MemoryMax=8589934592",
                   "-p", "MemorySwapMax=0", "-p", "RuntimeMaxSec="+str(window["scope_seconds"]),
                   "timeout", "--signal=TERM", "--kill-after=1s",
                   str(window["timeout_seconds"])+"s", "taskset", "-c", str(cpu),
                   sys.executable, str(Path(__file__).resolve()), "inside", str(config_path),
                   "--deadline", str(window["response_deadline"])]
        write(root/"launch.json", dict(at=utc(), command=command, window=window, environment={
            key: env[key] for key in (*THREADS, "TMPDIR", "TMP", "TEMP", "XDG_CACHE_HOME",
                                      "PYTHON_CPU_COUNT", "OMP_DYNAMIC", "MKL_DYNAMIC")},
            source=config["source"], config_sha256=sha(config_path)))
        with (root/"stdout.log").open("x") as out, (root/"stderr.log").open("x") as err:
            started_scope = True
            result = subprocess.run(command, cwd=home(config["source"]), env=env,
                                    stdout=out, stderr=err, timeout=window["scope_seconds"]+1)
            exit_code = result.returncode
    except Exception as error:
        terminal_error = dict(exception=repr(error), traceback=traceback.format_exc())
    finally:
        try:
            state = scope_status(unit)
            if started_scope and not inactive(state):
                stopped = subprocess.run(["systemctl", "--user", "stop", unit+".scope"],
                                         capture_output=True, text=True, timeout=3)
                cleanup = dict(exit_code=stopped.returncode, stdout=stopped.stdout,
                               stderr=stopped.stderr)
            after = scope_status(unit)
            if not inactive(after):
                exit_code = 2
        except Exception as error:
            after = dict(error=repr(error))
            exit_code = 2
        elapsed = time.monotonic()-started
        if elapsed > TOTAL_SECONDS:
            exit_code = 2
        record = dict(at=utc(), exit_code=exit_code, wall_seconds=elapsed,
                      total_limit_seconds=TOTAL_SECONDS, within_total_budget=elapsed <= TOTAL_SECONDS,
                      cleanup_reserved_seconds=CLEANUP_SECONDS, cleanup=cleanup,
                      terminal_error=terminal_error, final_scope=after)
        write(root/"exit-cleanup.json", record)
    print(json.dumps(dict(output=str(root), **record)), flush=True)
    return exit_code


def inside(config_path, config, deadline):
    # Imports occur only within the one-CPU scope with its library controls set.
    import vacuum_u1_hutchinson_runtime as runtime
    import vacuum_u1_hutchinson_controller as control
    from vacuum_u1_hutchinson_mechanics import Shell

    root, repo = home(config["output"]), home(config["source"])
    budget = control.Deadline(deadline)
    budget()
    reservation = json.loads((root/"attempt-reserved.json").read_text())
    if (reservation["config_sha256"] != sha(config_path)
            or deadline != reservation["deadline_monotonic"]-CLEANUP_SECONDS):
        raise RuntimeError("Internal phase does not match the sole reserved attempt")
    check_pins(config)
    ident = runtime.identity(repo)
    if ident["tip"] != config["tip"] or ident["tree"] != config["tree"] or ident["status"]:
        raise RuntimeError(f"Executable source is not the governed clean object: {ident}")
    measured = runtime.controls(config["unit"], 7200)
    software = runtime.software()
    prerequisites = json.loads(home(config["prerequisites"]).read_text())
    if prerequisites["status"] != "PASS" or prerequisites["numerical_check_seconds"] > 1800:
        raise RuntimeError("Nonresponse prerequisites did not pass within allocation")
    if software != prerequisites["software"]:
        raise RuntimeError("Installed Python/build/BLAS changed since the passing checks")
    manifest = dict(at=utc(), authority=ORDER, status="PRE_SOLVE_READY_NO_RESPONSE_YET",
                    source=ident, config=dict(path=str(config_path), sha256=sha(config_path)),
                    frozen_case_sha256=CASE_SHA, frozen_protocol_sha256=PROTOCOL_SHA,
                    prerequisites=config["prerequisites"], software=software, controls=measured,
                    pins=config["pins"], response_started=False,
                    cylinder_handoff=config["cylinder_handoff"],
                    response_deadline_monotonic=deadline,
                    total_deadline_monotonic=reservation["deadline_monotonic"],
                    cleanup_reserved_seconds=CLEANUP_SECONDS,
                    remaining_response_seconds=deadline-time.monotonic(),
                    qualification="One sequential response, terminal first failure; no retry or tuning.")
    runtime.save(root/"pre-solve-manifest.json", manifest)
    artifact = dict(path=str(root/"pre-solve-manifest.json"), sha256=runtime.digest(root/"pre-solve-manifest.json"))
    report = dict(id=REPORT, kind="report", **{"from": SEAT}, to="sciences-p-10151529",
                  cc=["xo-r-10111326", "co-r-10111331"], unit="vacuum-float-u1-1017", re=ORDER,
                  authority=[dict(id=ORDER)], asks="none",
                  next=SEAT+": execute the already-authorized sole bounded sequential response and return exact evidence",
                  standing="Frozen protocol unchanged; corrected cylinder handoff filed and gate scope inactive; no U1 closure, U2/U4 release, self-verification or award.",
                  artifacts=[artifact], at=utc(),
                  body="Pre-solve manifest filed before any physical response under conditional execution authority. "
                       "It pins clean governed source, frozen case/protocol, complete nonresponse test history and "
                       "installed Python/numpy/scipy/BLAS, plus measured one-CPU/8GiB/swap0/thread controls. "
                       "The sole sequential64/128/256 job uses one total7200s deadline including setup and a12s cleanup reserve. "
                       "First UNRESOLVED stops all remaining meshes with no restart, tuning or ceiling reset. "
                       "Cylinder handoff has been returned and its gate scope is inactive. "
                       "No further Head wait is required by the execution order. Manifest: "+artifact["path"]+
                       " SHA256 "+artifact["sha256"])
    outbox = home(config["seat_root"])/".ship/outbox"
    expected = Path(__file__).resolve().parents[3]
    if home(config["seat_root"])/".ship" != expected:
        raise RuntimeError("Outbox does not belong to this owned worktree")
    temp, final = outbox/(REPORT+".json.tmp"), outbox/(REPORT+".json")
    if final.exists():
        raise RuntimeError("Pre-solve record already exists: no second response")
    write(temp, report)
    os.rename(temp, final)
    descriptor = os.open(outbox, os.O_RDONLY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    runtime.save(root/"pre-solve-filed.json", dict(at=utc(), report=str(final), sha256=sha(final),
                                                manifest=artifact))
    audit = runtime.Audit(root)
    def stopped(signum, frame):
        raise control.Unresolved("UNRESOLVED_RESOURCE_SIGNAL", signal=signum)
    signal.signal(signal.SIGTERM, stopped)
    try:
        budget()
        audit.event("response_start", pre_solve_report_sha256=sha(final), controls=measured)
        outcome = control.sequence(Shell, audit, budget)
    except Exception as error:
        outcome = dict(status="UNRESOLVED", reason=getattr(error, "reason", "UNRESOLVED_IMPLEMENTATION_OR_RESOURCE"),
                       details=getattr(error, "details", {}), exception=repr(error), traceback=traceback.format_exc())
        audit.event("terminal_exception", **outcome)
    finally:
        audit.close()
    source_after = runtime.identity(repo)
    if source_after != ident:
        outcome = dict(status="UNRESOLVED", reason="UNRESOLVED_SOURCE_CHANGED",
                       unvalidated_outcome=outcome, source_before=ident)
    outcome.update(at=utc(), source_after=source_after, resource=runtime.accounting(measured),
                   response_remaining_seconds=deadline-time.monotonic(),
                   total_remaining_seconds=reservation["deadline_monotonic"]-time.monotonic(),
                   config_sha256=sha(config_path))
    runtime.save(root/"outcome.json", outcome)
    print(json.dumps(runtime.json_value(outcome), allow_nan=False), flush=True)
    return {"PASS": 0, "FAIL": 1, "UNRESOLVED": 2}[outcome["status"]]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("phase", choices=("launch", "inside"))
    parser.add_argument("config", type=Path)
    parser.add_argument("--deadline", type=float)
    args = parser.parse_args()
    path = home(args.config)
    config = json.loads(path.read_text())
    if args.phase == "launch":
        if args.deadline is not None:
            parser.error("Deadline override is unavailable")
        return launch(path, config)
    if args.deadline is None:
        parser.error("Internal phase requires the launch deadline")
    return inside(path, config, args.deadline)


if __name__ == "__main__":
    raise SystemExit(main())
