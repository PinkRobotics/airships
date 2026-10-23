#!/usr/bin/env python3
"""MAINLINE-047: authorized adaptation of pinned MAINLINE-029 axisymmetric.py.

N, mm, MPa. Full integration CAX8, native finite-strain J2 plastic faces.
Upstream source and hash are preserved in inputs/ and INPUT-CUSTODY.json.
"""
import argparse
import hashlib
import json
import math
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent


def case_parameters(case):
    if case == "lead028b":
        tf, tc = 0.794624066985892, 23.23721790601544
        return dict(case=case, radius_outer_mm=10000., face_outer_mm=tf,
                    face_inner_mm=tf, core_mm=tc, E_face_MPa=290000.,
                    nu_face=0.0768, E_core_MPa=103.4213593975254,
                    G_meridian_MPa=103.4213593975254,
                    G_hoop_MPa=46.88434959354485,
                    E_inplane_MPa=0.01, G_inplane_MPa=0.005,
                    core_kind="orthotropic", topology="full_sphere",
                    required_pressure_MPa=0.09546083791390515,
                    gamma_handbook_required=0.5641635666030133,
                    equivalent_thickness_mm=math.sqrt(3)*(tc+tf),
                    scarf_ratio_037b=30.34139731914874,
                    residual_face_compression_037b_MPa=3.4102225696822703)
    if case == "homogeneous":
        return dict(case=case, radius_outer_mm=100., face_outer_mm=0.25,
                    face_inner_mm=0.25, core_mm=0.5, E_face_MPa=210000.,
                    nu_face=0.33, E_core_MPa=210000., nu_core=0.33,
                    G_meridian_MPa=210000./2.66, G_hoop_MPa=210000./2.66,
                    core_kind="isotropic", topology="full_sphere")
    if case in ("flat", "dimple", "transfer40"):
        ti = 0.40 if case == "dimple" else 0.42
        ro = 125.97 if case == "transfer40" else 42.8
        return dict(case=case, radius_outer_mm=ro, face_outer_mm=0.42,
                    face_inner_mm=ti, core_mm=3.1, E_face_MPa=210000.,
                    nu_face=0.33, E_core_MPa=40., nu_core=0.,
                    G_meridian_MPa=20., G_hoop_MPa=20., core_kind="isotropic",
                    topology="clamped_hemisphere", paper_linear_MPa=27.56
                    if case == "dimple" else 27.53,
                    paper_imperfect_MPa=5.63 if case == "dimple" else 6.03)
    if case in ("lead021", "lead021b"):
        # Use the sealed, unrounded points, not the rounded brief dimensions.
        if case == "lead021":
            p = ROOT / "inputs/rpt-ref-769a7442efd5a04681e9/RESULTS.json"
            d = json.loads(p.read_text())["main"]["floating_point"]
        else:
            p = ROOT / "inputs/rpt-ref-1080d4f6a1af4cfa8c67/RESULTS.json"
            d = json.loads(p.read_text())["floating_point"]
        return dict(case=case, radius_outer_mm=10000., face_outer_mm=d["tf_m"]*1000,
                    face_inner_mm=d["tf_m"]*1000, core_mm=d["core_m"]*1000,
                    E_face_MPa=290000., nu_face=0.33,
                    E_core_MPa=d["core_Ec_Pa"]/1e6,
                    G_meridian_MPa=103.4213593975254,
                    G_hoop_MPa=46.88434959354485,
                    E_inplane_MPa=0.01, G_inplane_MPa=0.005,
                    core_kind="orthotropic", topology="full_sphere",
                    required_pressure_MPa=0.09546083791390515,
                    gamma_handbook_required=d["needed_values"]["gamma"],
                    specified_dimple_mm=11.8 if case == "lead021" else 46.,
                    equivalent_thickness_mm=math.sqrt(3)*d["h_m"]*1000)
    raise ValueError(case)


def build(args):
    p = case_parameters(args.case)
    if args.face_mm is not None:
        p["face_inner_mm"]=p["face_outer_mm"]=args.face_mm
    if args.core_mm is not None:
        p["core_mm"]=args.core_mm
    if args.face_mm is not None or args.core_mm is not None:
        p["equivalent_thickness_mm"]=math.sqrt(3)*(p["core_mm"]+
            (p["face_inner_mm"]+p["face_outer_mm"])/2)
    if args.meridian == "W":
        p["G_meridian_MPa"], p["G_hoop_MPa"] = p["G_hoop_MPa"], p["G_meridian_MPa"]
    if args.nu is not None:
        p["nu_face"] = args.nu
    if args.inplane is not None:
        p["E_inplane_MPa"] = args.inplane
        p["G_inplane_MPa"] = args.inplane/2
    ro, ti, to, tc = (p[k] for k in ["radius_outer_mm", "face_inner_mm", "face_outer_mm", "core_mm"])
    ri = ro - ti - to - tc
    # Quadratic serendipity quadrilaterals on a tensor grid; omit cell-center nodes.
    layers = [(ri, ri+ti, args.nface, "INNER"),
              (ri+ti, ro-to, args.ncore, "CORE"),
              (ro-to, ro, args.nface, "OUTER")]
    radial = [ri]
    materials = []
    for a, b, count, name in layers:
        radial.extend(a+(b-a)*k/(2*count) for k in range(1, 2*count+1))
        materials.extend([name]*count)
    nr = len(materials)
    na = args.ntheta
    end = math.pi/2 if p["topology"] == "clamped_hemisphere" else math.pi
    if args.width is None:
        if p["core_kind"] == "isotropic":
            width = 0.1*ro
        else:
            # Gaussian defect, lambda_I = [12(1-nu²)]^.25 sqrt(R/t_eq)*theta0=1.
            teq = p["equivalent_thickness_mm"]
            width = math.sqrt(ro*teq)/(12*(1-0.3**2))**0.25
            p["width_basis_nu"] = 0.3  # MAINLINE-015's map, independent of material nu.
    else:
        width = args.width
    p.update(amplitude_mm=args.amplitude, gaussian_width_mm=width,
             meridian_direction=args.meridian, element_type=args.element,
             ntheta=na, ncore=args.ncore, nface=args.nface,
             load_control="monotonically ramped follower pressure" if args.analysis == "static" else "linear stress-stiffness eigenproblem",
             material_law="native finite-strain J2, perfect plastic" if args.yield_stress else "StVK elastic",
             yield_stress_MPa=args.yield_stress,
             hardening_MPa=args.hardening,
             imperfection="stress-free Gaussian inward radial offset of every layer; same radial thickness")
    nodes, lookup = [], {}
    for j in range(2*na+1):
        theta = end*j/(2*na)
        # Optional pole refinement without changing the prescribed defect.
        if args.grading != 1:
            theta = end*(j/(2*na))**args.grading
        delta = args.amplitude*math.exp(-(ro*theta/width)**2)
        for k, r in enumerate(radial):
            if j % 2 and k % 2:
                continue
            nid = len(nodes)+1
            rad = r-delta
            x, y = rad*math.sin(theta), rad*math.cos(theta)
            if j == 0 or (j == 2*na and end == math.pi):
                x = 0.
            if j == 2*na and end == math.pi/2:
                y = 0.
            nodes.append((nid, x, y, 0.))
            lookup[j, k] = nid
    elems, groups = [], {}
    for j in range(na):
        for k in range(nr):
            a, b = 2*j, 2*k
            grid = [(a,b),(a+2,b),(a+2,b+2),(a,b+2),
                    (a+1,b),(a+2,b+1),(a+1,b+2),(a,b+1)]
            eid = len(elems)+1
            elems.append((eid, *[lookup[x] for x in grid]))
            group = materials[k] if materials[k] != "CORE" or p["core_kind"] == "isotropic" else f"CORE{j}"
            groups.setdefault(group, []).append(eid)
    lines = ["*HEADING", f"MAINLINE-047 {args.name}; QUESTIONABLE PROJECTION; N-mm-MPa",
             "*NODE"]
    lines.extend(",".join([str(n[0])]+[f"{x:.14g}" for x in n[1:]]) for n in nodes)
    lines.append(f"*ELEMENT,TYPE={args.element},ELSET=ALL")
    lines.extend(",".join(map(str,e)) for e in elems)
    def set_lines(kind, name, ids):
        lines.append(f"*{kind},{kind}={name}")
        for i in range(0,len(ids),16):
            lines.append(",".join(map(str,ids[i:i+16])))
    for name, ids in groups.items():
        set_lines("ELSET", name, ids)
    set_lines("ELSET", "FACES", groups["INNER"]+groups["OUTER"])
    axis = [lookup[0,k] for k in range(len(radial))]
    if end == math.pi:
        axis += [lookup[2*na,k] for k in range(len(radial))]
    set_lines("NSET", "AXIS", axis)
    rim = [lookup[2*na,k] for k in range(len(radial))]
    set_lines("NSET", "RIM", rim)
    pole = [lookup[0,0], lookup[0,len(radial)-1]]
    set_lines("NSET", "POLES", pole)
    set_lines("NSET", "ALLN", [n[0] for n in nodes])
    lines.extend(["*MATERIAL,NAME=FACE", "*ELASTIC",
                  f"{p['E_face_MPa']},{p['nu_face']}"])
    if args.yield_stress:
        lines.extend(["*PLASTIC", f"{args.yield_stress},0",
                      f"{args.yield_stress+0.1*args.hardening},0.1"])
    lines.append("*MATERIAL,NAME=COREMAT")
    if p["core_kind"] == "isotropic":
        lines.extend(["*ELASTIC",f"{p['E_core_MPa']},{p['nu_core']}"])
    else:
        # Local axes: 1=meridian, 2=radial-through-thickness, 3=circumference.
        # Unavailable in-plane properties are explicit regularizations; Poisson=0.
        lines.extend(["*ELASTIC,TYPE=ENGINEERING CONSTANTS",
                      f"{p['E_inplane_MPa']},{p['E_core_MPa']},{p['E_inplane_MPa']},0,0,0,{p['G_meridian_MPa']},{p['G_inplane_MPa']}",
                      f"{p['G_hoop_MPa']}"])
    for name in ("INNER", "OUTER"):
        lines.append(f"*SOLID SECTION,ELSET={name},MATERIAL=FACE")
    if p["core_kind"] == "isotropic":
        lines.append("*SOLID SECTION,ELSET=CORE,MATERIAL=COREMAT")
    else:
        for j in range(na):
            theta = end*((j+0.5)/na)**args.grading
            ct, st = math.cos(theta), math.sin(theta)
            delta = args.amplitude*math.exp(-(ro*theta/width)**2)
            rmid = (ro+ri)/2-delta
            dr = 2*args.amplitude*ro*ro*theta/width**2*math.exp(-(ro*theta/width)**2)
            tx, ty = dr*st+rmid*ct, dr*ct-rmid*st
            norm = math.hypot(tx,ty)
            tx, ty = tx/norm, ty/norm
            lines.extend([f"*ORIENTATION,NAME=O{j}",
                          f"{tx:.14g},{ty:.14g},0,{-ty:.14g},{tx:.14g},0",
                          f"*SOLID SECTION,ELSET=CORE{j},MATERIAL=COREMAT,ORIENTATION=O{j}"])
    lines.extend(["*BOUNDARY", "AXIS,1,1"])
    if end == math.pi/2:
        lines.append("RIM,1,2")
    else:
        # Eliminate axial rigid translation at one south-pole point only.
        lines.append(f"{lookup[2*na,0]},2,2")
    if args.analysis == "buckle":
        lines.extend(["*STEP", "*BUCKLE", "8,0.00001,40,2000"])
    else:
        lines.extend(["*STEP,NLGEOM,INC=2000", "*STATIC",
                      f"{args.increment},1,{args.minimum_increment},{args.maximum_increment}"])
    lines.append("*DLOAD")
    for j in range(na):
        eid = j*nr+nr
        lines.append(f"{eid},P3,{args.pressure:.14g}")
    if args.analysis == "buckle":
        # Retain 029's eigenvector output request; omission in the initial
        # 047 eigen control accompanied a native SIGSEGV, recorded separately.
        lines.extend(["*NODE FILE,FREQUENCY=1","U"])
    lines.extend(["*NODE PRINT,NSET=POLES,FREQUENCY=1","U,RF"])
    if args.analysis == "static":
        lines.extend(["*EL PRINT,ELSET=FACES,FREQUENCY=1", "S,PEEQ" if args.yield_stress else "S"])
    lines.append("*END STEP")
    directory = ROOT/"runs"/args.name
    directory.mkdir(parents=True, exist_ok=False)
    deck = directory/"model.inp"
    deck.write_text("\n".join(lines)+"\n")
    p.update(name=args.name, analysis=args.analysis, pressure_reference_MPa=args.pressure,
             defined_nodes=len(nodes), defined_elements=len(elems),
             nominal_axisymmetric_dofs=2*len(nodes), deck_sha256=hashlib.sha256(deck.read_bytes()).hexdigest(),
             args=vars(args))
    (directory/"MODEL.json").write_text(json.dumps(p,indent=2)+"\n")
    print(json.dumps({k:p[k] for k in ("name","defined_nodes","defined_elements","pressure_reference_MPa","gaussian_width_mm")}))


if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("name")
    a.add_argument("--case",choices=["lead028b","flat","dimple","lead021","lead021b","transfer40","homogeneous"],required=True)
    a.add_argument("--analysis",choices=["buckle","static"],default="buckle")
    a.add_argument("--ntheta",type=int,default=96)
    a.add_argument("--ncore",type=int,default=4)
    a.add_argument("--nface",type=int,default=1)
    a.add_argument("--element",choices=["CAX8","CAX8R"],default="CAX8")
    a.add_argument("--pressure",type=float,default=1.)
    a.add_argument("--amplitude",type=float,default=0.)
    a.add_argument("--width",type=float)
    a.add_argument("--grading",type=float,default=1.)
    a.add_argument("--meridian",choices=["L","W"],default="L")
    a.add_argument("--nu",type=float)
    a.add_argument("--inplane",type=float)
    a.add_argument("--face-mm",type=float)
    a.add_argument("--core-mm",type=float)
    a.add_argument("--yield-stress",type=float)
    a.add_argument("--hardening",type=float,default=0.)
    a.add_argument("--increment",type=float,default=0.01)
    a.add_argument("--maximum-increment",type=float,default=0.02)
    a.add_argument("--minimum-increment",type=float,default=1e-7)
    build(a.parse_args())
