#!/usr/bin/env python3
"""Source-matched U1 shell benchmarks; every solve runs in a bounded user scope."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time


MEMORY_LIMIT = 40 * 1024**3
WALL_LIMIT = 7200
THREAD_KEYS = ("OMP_NUM_THREADS", "CCX_NPROC_STIFFNESS",
               "CCX_NPROC_EQUATION_SOLVER", "CCX_NPROC_RESULTS", "NUMBER_OF_CPUS")


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    Path(path).write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def home_path(path):
    path = Path(path).resolve()
    if not path.is_relative_to("/home"):
        raise ValueError(f"FEA paths must resolve beneath /home: {path}")
    return path


def envelope():
    """Read the kernel's limits, including stricter ancestor limits."""
    entries = Path("/proc/self/cgroup").read_text().splitlines()
    relative = next(line[3:] for line in entries if line.startswith("0::"))
    root = Path("/sys/fs/cgroup")
    current = root / relative.lstrip("/")
    quota, period = (current / "cpu.max").read_text().split()
    memory = (current / "memory.max").read_text().strip()
    swap = (current / "memory.swap.max").read_text().strip()
    if quota == "max" or int(quota) / int(period) > 8:
        raise RuntimeError("The job cgroup lacks its eight-CPU quota")
    if memory == "max" or int(memory) > MEMORY_LIMIT or swap != "0":
        raise RuntimeError("The job cgroup lacks its memory/swap limit")
    limits = []
    for item in (current, *current.parents):
        if item == root:
            break
        limits.append({"path": str(item), **{
            name: (item / name).read_text().strip()
            for name in ("cpu.max", "memory.max") if (item / name).exists()}})
    unit = current.name
    runtime = subprocess.check_output(
        ["systemctl", "--user", "show", unit, "-p", "RuntimeMaxUSec", "--value"],
        text=True).strip()
    if runtime not in ("2h", "7200000000"):
        raise RuntimeError(f"Unexpected scope timeout: {runtime}")
    return {"cgroup": relative, "limits": limits, "swap_max": swap,
            "runtime_max": runtime, "path": str(current)}


def sphere_pressure(young, poisson, thickness, radius):
    return 2 * young * (thickness / radius)**2 / math.sqrt(3 * (1 - poisson**2))


def sphere_mesh(case, divisions):
    """Six spherical Gmsh patches, shared arcs, quadratic quadrilaterals."""
    import gmsh
    import numpy as np

    gmsh.initialize([], readConfigFiles=False)
    try:
        gmsh.option.setNumber("General.NumThreads", 1)
        gmsh.option.setNumber("Mesh.MaxNumThreads2D", 1)
        gmsh.option.setNumber("Mesh.SecondOrderIncomplete", 1)
        gmsh.model.add("sphere")
        geo = gmsh.model.geo
        radius = case["radius_m"]
        centre = geo.addPoint(0, 0, 0)
        vertices = {}
        for x in (-1, 1):
            for y in (-1, 1):
                for z in (-1, 1):
                    vertices[x, y, z] = geo.addPoint(
                        x * radius / math.sqrt(3), y * radius / math.sqrt(3),
                        z * radius / math.sqrt(3))
        faces = [
            [(1,-1,-1),(1,1,-1),(1,1,1),(1,-1,1)],
            [(-1,-1,-1),(-1,-1,1),(-1,1,1),(-1,1,-1)],
            [(-1,1,-1),(-1,1,1),(1,1,1),(1,1,-1)],
            [(-1,-1,-1),(1,-1,-1),(1,-1,1),(-1,-1,1)],
            [(-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)],
            [(-1,-1,-1),(-1,1,-1),(1,1,-1),(1,-1,-1)],
        ]
        edges = {}
        surfaces = []
        for face in faces:
            loop = []
            for a, b in zip(face, face[1:] + face[:1]):
                if (b, a) in edges:
                    loop.append(-edges[b, a])
                else:
                    if (a, b) not in edges:
                        edges[a, b] = geo.addCircleArc(vertices[a], centre, vertices[b])
                    loop.append(edges[a, b])
            surfaces.append(geo.addSurfaceFilling([geo.addCurveLoop(loop)],
                                                   sphereCenterTag=centre))
        geo.synchronize()
        for edge in edges.values():
            gmsh.model.mesh.setTransfiniteCurve(edge, divisions + 1)
        for surface in surfaces:
            gmsh.model.mesh.setTransfiniteSurface(surface)
            gmsh.model.mesh.setRecombine(2, surface)
        gmsh.model.mesh.generate(2)
        gmsh.model.mesh.setOrder(2)
        gmsh.write("mesh.msh")
        tags, coordinates, _ = gmsh.model.mesh.getNodes()
        positions = dict(zip(map(int, tags), coordinates.reshape(-1, 3)))
        types, element_tags, connectivity = gmsh.model.mesh.getElements(2)
        if list(types) != [16]:
            raise RuntimeError(f"Expected only Gmsh eight-node quads, got {types}")
        elements = dict(zip(map(int, element_tags[0]), connectivity[0].reshape(-1, 8)))
        used = sorted({int(n) for row in elements.values() for n in row})
        positions = {n: positions[n] for n in used}
        for position in positions.values():
            if abs(np.linalg.norm(position) - radius) > radius * 1e-9:
                raise RuntimeError("A mesh node is off the frozen spherical surface")
        for tag, row in elements.items():
            p = [positions[int(n)] for n in row[:3]]
            if np.dot(np.cross(p[1]-p[0], p[2]-p[0]), p[0]) < 0:
                elements[tag] = row[[0,3,2,1,7,6,5,4]]
        anchors = []
        for target, dofs in [((0,0,radius),(1,2)), ((0,0,-radius),(1,2)),
                             ((radius,0,0),(2,3))]:
            node = min(positions, key=lambda n: np.linalg.norm(positions[n]-target))
            if np.linalg.norm(positions[node]-target) > radius * 1e-9:
                raise RuntimeError("Rigid-motion gauge node is absent")
            anchors.extend((node, dof) for dof in dofs)
        return positions, elements, anchors
    finally:
        gmsh.finalize()


def sphere_deck(case, divisions):
    nodes, elements, anchors = sphere_mesh(case, divisions)
    lines = ["*HEADING", "U1 perfect sphere, SI; ideal elastic eigenvalue only", "*NODE"]
    # CalculiX's numeric input fields are limited to 20 characters.
    lines += [f"{tag}, " + ", ".join(f"{v:.12e}" for v in xyz)
              for tag, xyz in nodes.items()]
    lines += ["*ELEMENT, TYPE=S8R, ELSET=SHELL"]
    lines += [f"{tag}, " + ", ".join(map(str, row)) for tag, row in elements.items()]
    lines += ["*MATERIAL, NAME=ELASTIC", "*ELASTIC",
              f"{case['young_pa']}, {case['poisson']}",
              "*SHELL SECTION, ELSET=SHELL, MATERIAL=ELASTIC", str(case["thickness_m"]),
              "*NORMAL"]
    for tag, row in elements.items():
        for node in row:
            normal = nodes[int(node)] / case["radius_m"]
            lines.append(f"{tag}, {node}, " + ", ".join(f"{v:.12e}" for v in normal))
    lines += ["*BOUNDARY"] + [f"{node}, {dof}, {dof}" for node, dof in anchors]
    lines += ["*STEP", "*BUCKLE, SOLVER=SPOOLES", "8, 0.000001, 64, 1000",
              "*DLOAD", f"SHELL, P, {-case['reference_pressure_pa']}",
              "*NODE FILE, OUTPUT=2D", "U", "*END STEP"]
    Path("job.inp").write_text("\n".join(lines) + "\n")
    return {"nodes": len(nodes), "elements": len(elements), "element": "S8R",
            "nominal_shell_dofs": 6 * len(nodes), "anchors": anchors,
            "mesh_sha256": digest("mesh.msh"), "deck_sha256": digest("job.inp")}


def parse_factors(text):
    match = re.search(r"B\s*U\s*C\s*K\s*L\s*I\s*N\s*G.*?F\s*A\s*C\s*T\s*O\s*R", text,
                      flags=re.IGNORECASE | re.DOTALL)
    if not match:
        return []
    return [float(value.replace("D", "E")) for value in re.findall(
        r"^\s*\d+\s+([-+]?\d+\.\d+(?:[EeDd][-+]?\d+)?)\s*$",
        text[match.end():], flags=re.MULTILINE)]


def job(args):
    run = home_path(args.run_dir)
    os.chdir(run)
    for name in ("TMPDIR", "TMP", "TEMP", "XDG_CACHE_HOME"):
        if not home_path(os.environ[name]).is_relative_to(run):
            raise RuntimeError(f"{name} escapes the run directory")
    measured = envelope()
    available = sorted(os.sched_getaffinity(0))
    os.sched_setaffinity(0, available[:8])
    case = json.loads(Path("case.json").read_text())
    record = {"started": now(), "envelope": measured, "threads_requested": args.threads,
              "thread_environment": {key: os.environ[key] for key in THREAD_KEYS},
              "cpu_affinity": sorted(os.sched_getaffinity(0)),
              "case_sha256": digest("case.json"), "runner_sha256": digest(__file__),
              "solver": shutil.which("ccx"), "solver_sha256": digest(shutil.which("ccx"))}
    save("run.json", record)
    if args.deck:
        record["mesh"] = json.loads(Path("mesh-definition.json").read_text())
        if digest("job.inp") != record["mesh"]["deck_sha256"]:
            raise RuntimeError("Fixed deck differs from its frozen mesh definition")
    else:
        record["mesh"] = sphere_deck(case, case["mesh_divisions"][args.mesh_index])
        save("mesh-definition.json", record["mesh"])
    save("run.json", record)
    started = time.monotonic()
    maximum_threads = 0
    with open("solver.stdout", "w") as stdout, open("solver.stderr", "w") as stderr:
        child = subprocess.Popen([record["solver"], "-i", "job"], stdout=stdout, stderr=stderr)
        record["solver_pid"] = child.pid
        save("run.json", record)
        while True:
            pid, status, usage = os.wait4(child.pid, os.WNOHANG)
            if pid:
                child.returncode = os.waitstatus_to_exitcode(status)
                break
            try:
                contents = Path(f"/proc/{child.pid}/status").read_text()
                maximum_threads = max(maximum_threads, int(re.search(r"Threads:\s+(\d+)", contents)[1]))
            except FileNotFoundError:
                pass
            time.sleep(0.2)
    elapsed = time.monotonic() - started
    dat = Path("job.dat").read_text() if Path("job.dat").exists() else ""
    stdout = Path("solver.stdout").read_text()
    factors = parse_factors(dat)
    complete = child.returncode == 0 and "Job finished" in stdout and len(factors) == 8
    complete = complete and all(math.isfinite(x) and x > 0 for x in factors)
    record.update({"ended": now(), "exit_code": child.returncode,
                   "wall_seconds": elapsed, "cpu_seconds": usage.ru_utime + usage.ru_stime,
                   "peak_rss_kib": usage.ru_maxrss, "max_observed_threads": maximum_threads,
                   "average_cpu_cores": (usage.ru_utime + usage.ru_stime) / elapsed,
                   "factors": factors, "eigenproblem_completed": complete,
                   "status": "COMPLETED" if complete else "FAILED_SOLVE",
                   "pressure_pa": min(factors)*case["reference_pressure_pa"] if complete else None,
                   "cgroup_memory_peak_bytes": int((Path(measured["path"])/"memory.peak").read_text()),
                   "memory_events": (Path(measured["path"])/"memory.events").read_text(),
                   "equations": re.findall(r"number of equations\s*:?\s*(\d+)", stdout, re.I)})
    save("run.json", record)
    print(json.dumps(record), flush=True)
    return 0 if complete else 2


def launch(args):
    if args.threads not in (1, 2, 4, 8):
        raise ValueError("Threads must be 1, 2, 4 or 8")
    run = home_path(args.run_dir)
    run.mkdir(parents=True, exist_ok=False)
    free = shutil.disk_usage(run).free
    if free < 5 * 1024**3:
        raise RuntimeError("Fewer than 5 GiB free on the run filesystem")
    shutil.copyfile(args.case, run / "case.json")
    if args.deck:
        source = home_path(args.deck)
        shutil.copyfile(source / "job.inp", run / "job.inp")
        shutil.copyfile(source / "mesh-definition.json", run / "mesh-definition.json")
    env = os.environ.copy()
    for key in THREAD_KEYS:
        env[key] = str(args.threads)
    env.update(OPENBLAS_NUM_THREADS="1", MKL_NUM_THREADS=str(args.threads),
               OMP_DYNAMIC="FALSE", CUDA_VISIBLE_DEVICES="", PYTHONUNBUFFERED="1")
    for key, name in (("TMPDIR", "tmp"), ("TMP", "tmp"), ("TEMP", "tmp"),
                      ("XDG_CACHE_HOME", "cache")):
        (run / name).mkdir(exist_ok=True)
        env[key] = str(run / name)
    unit = "vacuum-u1-" + hashlib.sha256(str(run).encode()).hexdigest()[:16]
    command = ["systemd-run", "--user", "--scope", "--unit="+unit,
               "-p", "CPUQuota=800%", "-p", "MemoryMax=40G", "-p", "MemorySwapMax=0",
               "-p", "RuntimeMaxSec=7200", "timeout", "--signal=TERM", "--kill-after=10s",
               "7200s", sys.executable, str(Path(__file__).resolve()), "_job",
               "--run-dir", str(run), "--threads", str(args.threads),
               "--mesh-index", str(args.mesh_index)]
    if args.deck:
        command += ["--deck", str(args.deck)]
    record = {"command": command, "started": now(), "free_bytes": free, "unit": unit}
    save(run / "launch.json", record)
    with (run / "scope.stdout").open("w") as stdout, (run / "scope.stderr").open("w") as stderr:
        result = subprocess.run(command, cwd=run, env=env, stdout=stdout, stderr=stderr)
    record.update(ended=now(), exit_code=result.returncode)
    save(run / "launch.json", record)
    print(json.dumps(record), flush=True)
    if (run / "run.json").exists():
        print((run / "run.json").read_text(), flush=True)
    if result.returncode:
        print((run / "scope.stderr").read_text(), file=sys.stderr)
    return result.returncode


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("solve", "_job"))
    parser.add_argument("--case", type=Path)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--mesh-index", type=int, default=0)
    parser.add_argument("--threads", type=int, default=8)
    parser.add_argument("--deck", type=Path)
    args = parser.parse_args()
    return launch(args) if args.action == "solve" else job(args)


if __name__ == "__main__":
    raise SystemExit(main())
