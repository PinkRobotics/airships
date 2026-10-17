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


def cylinder_line_load(young, poisson, thickness, radius, length, m, n):
    """SP-8007 Rev 2 equations 1--5, theoretical gamma=1, in N/m."""
    rigidity = young * thickness**3 / (12 * (1 - poisson**2))
    curvature = length**2 * math.sqrt(1 - poisson**2) / (radius * thickness)
    beta = n * length / (m * math.pi * radius)
    shape = m**2 * (1 + beta**2)**2
    return (shape + 12 * curvature**2 / (math.pi**4 * shape)) * math.pi**2 * rigidity / length**2


def cylinder_deck(case, mesh_index):
    """Four shared cylindrical patches and consistent quadratic edge loads."""
    import gmsh
    import numpy as np

    radius, length = case["radius_m"], case["length_m"]
    circum = case["mesh_divisions_circumference"][mesh_index]
    axial = case["mesh_divisions_axial"][mesh_index]
    if circum % 4:
        raise ValueError("Circumferential division count must be divisible by four")
    gmsh.initialize([], readConfigFiles=False)
    try:
        gmsh.option.setNumber("General.NumThreads", 1)
        gmsh.option.setNumber("Mesh.MaxNumThreads2D", 1)
        gmsh.option.setNumber("Mesh.SecondOrderIncomplete", 1)
        gmsh.model.add("cylinder")
        geo = gmsh.model.geo
        rings, arcs = [], []
        for z in (0, length):
            centre = geo.addPoint(0, 0, z)
            points = [geo.addPoint(radius*math.cos(i*math.pi/2),
                                  radius*math.sin(i*math.pi/2), z) for i in range(4)]
            rings.append(points)
            arcs.append([geo.addCircleArc(points[i], centre, points[(i+1)%4])
                         for i in range(4)])
        vertical = [geo.addLine(rings[0][i], rings[1][i]) for i in range(4)]
        surfaces = [geo.addSurfaceFilling([geo.addCurveLoop(
            [arcs[0][i], vertical[(i+1)%4], -arcs[1][i], -vertical[i]])])
                    for i in range(4)]
        geo.synchronize()
        for edge in arcs[0] + arcs[1]:
            gmsh.model.mesh.setTransfiniteCurve(edge, circum//4 + 1)
        for edge in vertical:
            gmsh.model.mesh.setTransfiniteCurve(edge, axial + 1)
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
            raise RuntimeError(f"Expected eight-node quads; got {types}")
        elements = dict(zip(map(int, element_tags[0]), connectivity[0].reshape(-1, 8)))
        nodes = {n: positions[n] for n in sorted({int(n) for row in elements.values() for n in row})}
        for point in nodes.values():
            if abs(np.linalg.norm(point[:2]) - radius) > radius*1e-8:
                raise RuntimeError("Mesh node lies off the frozen cylindrical surface")
        for tag, row in elements.items():
            p = [nodes[int(n)] for n in row[:3]]
            if np.dot(np.cross(p[1]-p[0], p[2]-p[0]), [p[0][0], p[0][1], 0]) < 0:
                elements[tag] = row[[0,3,2,1,7,6,5,4]]
        bottom = [n for n, p in nodes.items() if abs(p[2]) < length*1e-9]
        top = [n for n, p in nodes.items() if abs(p[2]-length) < length*1e-9]
        loads = {}
        loaded_edges = 0
        edge_force = -case["reference_line_load_n_per_m"] * 2*math.pi*radius/circum
        top_set = set(top)
        for row in elements.values():
            for a, b, mid in ((0,1,4),(1,2,5),(2,3,6),(3,0,7)):
                if int(row[a]) in top_set and int(row[b]) in top_set:
                    loaded_edges += 1
                    for index, weight in ((a,1/6),(b,1/6),(mid,2/3)):
                        node = int(row[index])
                        loads[node] = loads.get(node, 0) + weight*edge_force
        expected = -2*math.pi*radius*case["reference_line_load_n_per_m"]
        if loaded_edges != circum or not math.isclose(sum(loads.values()), expected, rel_tol=1e-12):
            raise RuntimeError("Consistent axial rim load failed its force balance")
        lines = ["*HEADING", "U1 SP8007 gamma=1 cylinder, SI", "*NODE"]
        lines += [f"{tag}, " + ", ".join(f"{v:.12e}" for v in xyz) for tag, xyz in nodes.items()]
        lines += ["*ELEMENT, TYPE=S8R, ELSET=SHELL"]
        lines += [f"{tag}, " + ", ".join(map(str, row)) for tag, row in elements.items()]
        lines += ["*MATERIAL, NAME=ELASTIC", "*ELASTIC", f"{case['young_pa']}, {case['poisson']}",
                  "*SHELL SECTION, ELSET=SHELL, MATERIAL=ELASTIC", str(case["thickness_m"]), "*NORMAL"]
        for tag, row in elements.items():
            for node in row:
                x, y, _ = nodes[int(node)]
                lines.append(f"{tag}, {node}, {x/radius:.12e}, {y/radius:.12e}, 0.")
        lines += ["*BOUNDARY"] + [f"{node}, 1, 2" for node in bottom + top]
        lines += [f"{node}, 3, 3" for node in bottom]
        lines += ["*STEP", "*BUCKLE, SOLVER=SPOOLES", "8, 0.000001, 64, 1000", "*CLOAD"]
        lines += [f"{node}, 3, {force:.12e}" for node, force in sorted(loads.items())]
        lines += ["*NODE FILE, OUTPUT=2D", "U", "*END STEP"]
        Path("job.inp").write_text("\n".join(lines) + "\n")
        return {"nodes": len(nodes), "elements": len(elements), "element": "S8R",
                "nominal_shell_dofs": 6*len(nodes), "loaded_edges": loaded_edges,
                "net_axial_load_n": sum(loads.values()), "bottom_nodes": len(bottom),
                "top_nodes": len(top), "mesh_sha256": digest("mesh.msh"), "deck_sha256": digest("job.inp")}
    finally:
        gmsh.finalize()


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


def sandwich_pressure(young, face_ratio, core_ratio):
    """Akhmeteli--Gavrilin Eq9: full expression and thin-face approximation."""
    return (2*young*face_ratio*(core_ratio+face_ratio),
            2*young*face_ratio*core_ratio)


def sandwich_deck(case, mesh_index):
    """Fig4 meridional quadrant with shared, perfectly bonded solid layers."""
    import gmsh
    import numpy as np

    radius = case["radius_m"]
    face = radius*case["face_thickness_over_radius"]
    core = radius*case["core_thickness_over_radius"]
    radii = [radius-2*face-core, radius-face-core, radius-face, radius]
    meridian = case["mesh_divisions_meridian"][mesh_index]
    radial = [case["mesh_divisions_faces"][mesh_index],
              case["mesh_divisions_core"][mesh_index],
              case["mesh_divisions_faces"][mesh_index]]
    gmsh.initialize([], readConfigFiles=False)
    try:
        gmsh.option.setNumber("General.NumThreads", 1)
        gmsh.option.setNumber("Mesh.MaxNumThreads2D", 1)
        gmsh.option.setNumber("Mesh.SecondOrderIncomplete", 1)
        gmsh.model.add("sandwich")
        geo = gmsh.model.geo
        centre = geo.addPoint(0, 0, 0)
        bottom = [geo.addPoint(r, 0, 0) for r in radii]
        top = [geo.addPoint(0, r, 0) for r in radii]
        arcs = [geo.addCircleArc(a, centre, b) for a, b in zip(bottom, top)]
        bottom_edges = [geo.addLine(bottom[i], bottom[i+1]) for i in range(3)]
        top_edges = [geo.addLine(top[i], top[i+1]) for i in range(3)]
        surfaces = [geo.addPlaneSurface([geo.addCurveLoop(
            [bottom_edges[i], arcs[i+1], -top_edges[i], -arcs[i]])]) for i in range(3)]
        geo.synchronize()
        for edge in arcs:
            gmsh.model.mesh.setTransfiniteCurve(edge, meridian+1)
        for i, divisions in enumerate(radial):
            for edge in (bottom_edges[i], top_edges[i]):
                gmsh.model.mesh.setTransfiniteCurve(edge, divisions+1)
            gmsh.model.mesh.setTransfiniteSurface(surfaces[i])
            gmsh.model.mesh.setRecombine(2, surfaces[i])
        gmsh.model.mesh.generate(2)
        gmsh.model.mesh.setOrder(2)
        gmsh.write("mesh.msh")
        tags, coordinates, _ = gmsh.model.mesh.getNodes()
        positions = dict(zip(map(int, tags), coordinates.reshape(-1, 3)))
        layers = []
        for surface in surfaces:
            types, element_tags, connectivity = gmsh.model.mesh.getElements(2, surface)
            if list(types) != [16]:
                raise RuntimeError(f"Expected quadratic eight-node quads; got {types}")
            elements = dict(zip(map(int, element_tags[0]), connectivity[0].reshape(-1, 8)))
            for tag, row in elements.items():
                p = [positions[int(n)] for n in row[:3]]
                if np.cross(p[1]-p[0], p[2]-p[0])[2] < 0:
                    elements[tag] = row[[0,3,2,1,7,6,5,4]]
            layers.append(elements)
        used = sorted({int(n) for layer in layers for row in layer.values() for n in row})
        nodes = {n: positions[n] for n in used}
        node_sets = [{int(n) for row in layer.values() for n in row} for layer in layers]
        if any(len(node_sets[i] & node_sets[i+1]) != 2*meridian+1 for i in (0,1)):
            raise RuntimeError("Layer interfaces do not share the full quadratic meridian")
        pole = [n for n, p in nodes.items() if abs(p[0]) < radius*1e-10]
        equator = [n for n, p in nodes.items() if abs(p[1]) < radius*1e-10]
        loads = []
        for tag, row in layers[2].items():
            for label, (a, b, mid) in enumerate(((0,1,4),(1,2,5),(2,3,6),(3,0,7)), 1):
                if all(abs(np.linalg.norm(nodes[int(row[j])])-radius)<radius*1e-9
                       for j in (a,b,mid)):
                    loads.append((tag, label))
        if len(loads) != meridian:
            raise RuntimeError("The entire outer meridian must carry pressure")
        lines = ["*HEADING", "U1 Akhmeteli Fig4/5 reconstruction, SI, ideal eigenvalue", "*NODE"]
        lines += [f"{tag}, " + ", ".join(f"{v:.12e}" for v in xyz) for tag, xyz in nodes.items()]
        for name, layer in zip(("INNER", "CORE", "OUTER"), layers):
            lines += [f"*ELEMENT, TYPE=CAX8R, ELSET={name}"]
            lines += [f"{tag}, " + ", ".join(map(str, row)) for tag, row in layer.items()]
        constants = case["core_engineering_constants"]
        keys = ("E1_pa","E2_pa","E3_pa","nu12","nu13","nu23","G12_pa","G13_pa")
        lines += ["*MATERIAL, NAME=FACE", "*ELASTIC",
                  f"{case['face_young_pa']}, {case['face_poisson']}",
                  "*MATERIAL, NAME=HONEYCOMB", "*ELASTIC, TYPE=ENGINEERING CONSTANTS",
                  ", ".join(str(constants[key]) for key in keys), str(constants["G23_pa"]),
                  "*ORIENTATION, NAME=RADIAL, SYSTEM=CYLINDRICAL", "0., 0., 0., 0., 0., 1.",
                  "*SOLID SECTION, ELSET=INNER, MATERIAL=FACE", "",
                  "*SOLID SECTION, ELSET=CORE, MATERIAL=HONEYCOMB, ORIENTATION=RADIAL", "",
                  "*SOLID SECTION, ELSET=OUTER, MATERIAL=FACE", "", "*BOUNDARY"]
        lines += [f"{node}, 1, 1" for node in pole] + [f"{node}, 2, 2" for node in equator]
        lines += ["*STEP", "*BUCKLE, SOLVER=SPOOLES", "8, 0.000001, 64, 1000", "*DLOAD"]
        lines += [f"{tag}, P{label}, {case['reference_pressure_pa']}" for tag, label in loads]
        lines += ["*NODE FILE, OUTPUT=2D", "U", "*END STEP"]
        Path("job.inp").write_text("\n".join(lines) + "\n")
        return {"nodes": len(nodes), "elements": sum(map(len,layers)), "element": "CAX8R",
                "layer_elements": list(map(len,layers)), "nominal_axisymmetric_dofs": 2*len(nodes),
                "pressure_edges": len(loads), "pole_nodes": len(pole), "equator_nodes": len(equator),
                "mesh_sha256": digest("mesh.msh"), "deck_sha256": digest("job.inp")}
    finally:
        gmsh.finalize()


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
        if case["benchmark"] == "classical-sphere":
            record["mesh"] = sphere_deck(case, case["mesh_divisions"][args.mesh_index])
        elif case["benchmark"] == "sp8007-cylinder":
            record["mesh"] = cylinder_deck(case, args.mesh_index)
        elif case["benchmark"] == "akhmeteli-gavrilin":
            record["mesh"] = sandwich_deck(case, args.mesh_index)
        else:
            raise ValueError(f"Unknown benchmark: {case['benchmark']}")
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
                   "cgroup_memory_peak_bytes": int((Path(measured["path"])/"memory.peak").read_text()),
                   "memory_events": (Path(measured["path"])/"memory.events").read_text(),
                   "equations": re.findall(r"number of equations\s*:?\s*(\d+)", stdout, re.I)})
    for quantity in ("pressure_pa", "line_load_n_per_m"):
        if "reference_" + quantity in case:
            record[quantity] = min(factors)*case["reference_" + quantity] if complete else None
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
    shutil.copyfile(Path(__file__).resolve(), run / "runner.py")
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
               "7200s", sys.executable, str(run / "runner.py"), "_job",
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
