"""Raw evidence, installed-library identity and measured resource guards."""

import contextlib
import ctypes
from datetime import datetime, timezone
import hashlib
import io
import json
import math
import os
from pathlib import Path
import subprocess
import sys

import numpy as np
import scipy


THREAD_KEYS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
               "BLIS_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS",
               "GOTO_NUM_THREADS", "OMP_THREAD_LIMIT")
MEMORY = 8589934592


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024*1024), b""):
            h.update(block)
    return h.hexdigest()


def home_path(path):
    result = Path(path).resolve()
    if not result.is_relative_to("/home"):
        raise ValueError(f"Work/evidence path outside /home: {result}")
    return result


def json_value(value):
    if isinstance(value, np.ndarray):
        return json_value(value.tolist())
    if isinstance(value, np.generic):
        return json_value(value.item())
    if isinstance(value, dict):
        return {str(k): json_value(v) for k, v in value.items()}
    if isinstance(value, (tuple, list)):
        return [json_value(v) for v in value]
    if isinstance(value, float) and not math.isfinite(value):
        # Preserve a nonfinite observation explicitly, never clip it to a number.
        return {"nonfinite_binary64": repr(value)}
    return value


def save(path, value):
    path = home_path(path)
    with path.open("x") as stream:
        json.dump(json_value(value), stream, indent=2, allow_nan=False)
        stream.write("\n")
        stream.flush()
        os.fsync(stream.fileno())


class Audit:
    def __init__(self, root):
        self.root = home_path(root)
        self.raw = self.root / "raw"
        self.raw.mkdir()
        self.stream = (self.root / "events.jsonl").open("x")
        self.serial = 0

    def event(self, event, **data):
        self.stream.write(json.dumps(json_value(dict(at=now(), event=event, **data)),
                                     allow_nan=False, separators=(",", ":")) + "\n")
        self.stream.flush()
        os.fsync(self.stream.fileno())

    def arrays(self, label, **values):
        self.serial += 1
        path = self.raw / f"{self.serial:06d}-{label}.npz"
        with path.open("xb") as stream:
            np.savez(stream, **values)
            stream.flush()
            os.fsync(stream.fileno())
        return {"path": str(path), "sha256": digest(path),
                "shapes": {key: list(np.asarray(value).shape) for key, value in values.items()}}

    def close(self):
        self.stream.close()


def git(repo, *args):
    return subprocess.check_output(["git", "--no-optional-locks", *args],
                                   cwd=repo, text=True).strip()


def identity(repo):
    return dict(source=str(home_path(repo)), tip=git(repo, "rev-parse", "HEAD"),
                tree=git(repo, "rev-parse", "HEAD^{tree}"),
                status=git(repo, "status", "--porcelain=v1"))


def controls(unit, maximum_seconds):
    relative = next(line[3:] for line in Path("/proc/self/cgroup").read_text().splitlines()
                    if line.startswith("0::"))
    root = Path("/sys/fs/cgroup")
    current = root / relative.lstrip("/")
    ancestors = []
    for path in (current, *current.parents):
        if path == root:
            break
        ancestors.append(dict(path=str(path), **{
            key: (path/key).read_text().strip()
            for key in ("cpu.max", "memory.max", "memory.swap.max") if (path/key).exists()}))
    quota, period = ancestors[0]["cpu.max"].split()
    if quota == "max" or int(quota)/int(period) > 1:
        raise RuntimeError("Missing at-most-one-CPU cgroup quota")
    memory = ancestors[0]["memory.max"]
    if memory == "max" or int(memory) > MEMORY or ancestors[0]["memory.swap.max"] != "0":
        raise RuntimeError("Missing memory/swap ceiling")
    affinity = sorted(os.sched_getaffinity(0))
    if len(affinity) != 1:
        raise RuntimeError("Expected one CPU affinity")
    runtime = subprocess.check_output(["systemctl", "--user", "show", unit + ".scope",
                                       "--property=RuntimeMaxUSec", "--value"], text=True).strip()
    # The job's own deadline/outer timeout is authoritative in addition to this
    # exact bounded systemd duration, supplied by our launcher in whole seconds.
    pieces = runtime.split()
    factors = {"h": 3600, "min": 60, "s": 1, "ms": .001, "us": .000001}
    duration = 0.0
    for piece in pieces:
        for suffix in ("min", "ms", "us", "h", "s"):
            if piece.endswith(suffix):
                duration += float(piece[:-len(suffix)]) * factors[suffix]
                break
        else:
            raise RuntimeError(f"Unrecognized measured scope duration: {runtime}")
    if not 0 < duration <= maximum_seconds:
        raise RuntimeError(f"Unbounded/incorrect scope duration: {runtime}")
    env = {key: os.environ.get(key) for key in THREAD_KEYS}
    if set(env.values()) != {"1"}:
        raise RuntimeError(f"Thread controls not all one: {env}")
    paths = {key: str(home_path(os.environ[key]))
             for key in ("TMPDIR", "TMP", "TEMP", "XDG_CACHE_HOME")}
    return dict(at=now(), cgroup=relative, cgroup_path=str(current), ancestors=ancestors,
                affinity=affinity, runtime_max=runtime,
                runtime_seconds=duration, thread_environment=env, paths=paths,
                process_threads=len(list(Path("/proc/self/task").iterdir())),
                command_line=Path("/proc/self/cmdline").read_bytes().split(b"\0")[:-1].__repr__())


def accounting(control):
    path = Path(control["cgroup_path"])
    return {key: (path/key).read_text().strip() for key in
            ("cpu.stat", "memory.peak", "memory.events", "memory.swap.current", "pids.current")
            if (path/key).exists()}


def software():
    builds = {}
    for name, module in (("numpy", np), ("scipy", scipy)):
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            module.show_config()
        builds[name] = dict(version=module.__version__, module=module.__file__,
                            build=stream.getvalue())
    libraries = sorted({line.split()[-1] for line in Path("/proc/self/maps").read_text().splitlines()
                        if "openblas" in line and line.split()[-1].startswith("/")})
    if not libraries:
        raise RuntimeError("No loaded BLAS library could be measured")
    measured = []
    for name in libraries:
        library = ctypes.CDLL(name)
        symbols = subprocess.check_output(["nm", "-D", name], text=True)
        candidates = [line.split()[-1] for line in symbols.splitlines()
                      if "openblas_get_num_threads" in line]
        if not candidates:
            # Debian's libblas/liblapack compatibility DSOs share the directory
            # with their loaded OpenBLAS provider but do not export its getter.
            # Keep their exact binary identity; measure the actual provider below.
            measured.append(dict(path=name, sha256=digest(name), getter=None,
                                 available_getters=[], threads=None,
                                 role="compatibility DSO; provider measured separately"))
            continue
        symbol = min(candidates, key=len)
        getter = getattr(library, symbol)
        getter.restype, getter.argtypes = ctypes.c_int, []
        count = getter()
        if count != 1:
            raise RuntimeError(f"Actual BLAS threads not one: {name} {count}")
        measured.append(dict(path=name, sha256=digest(name), getter=symbol,
                             available_getters=candidates, threads=count))
    if not any(record["getter"] for record in measured):
        raise RuntimeError("No loaded OpenBLAS provider exposes a measurable thread count")
    return dict(python=sys.version, executable=str(Path(sys.executable).resolve()),
                executable_sha256=digest(Path(sys.executable).resolve()), builds=builds,
                blas=measured, process_threads=len(list(Path("/proc/self/task").iterdir())))
