#!/usr/bin/env python3
"""Serial, admitted CalculiX execution. Never invoke the solver outside simjob."""
import argparse, datetime, hashlib, json, os, pathlib, subprocess, sys, time
ROOT = pathlib.Path(__file__).resolve().parent
SIMJOB = "unpublished-local-ref:6b66f99ebd630954"
def stamp():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
def run(name, mem="2G", cores=1):
    d=ROOT/"runs"/name
    assert (d/"model.inp").exists()
    assert not (d/"LAUNCH.json").exists(), name
    scratch=pathlib.Path("unpublished-local-ref:67a4cf125292e701")/name
    scratch.mkdir(parents=True,exist_ok=True)
    model=json.loads((d/"MODEL.json").read_text())
    if model["analysis"]=="buckle":
        assert cores==1, "029 eigen reliability requires one solver core"
    env=dict(os.environ,TMPDIR=str(scratch),OMP_NUM_THREADS=str(cores),
             OPENBLAS_NUM_THREADS="1",MKL_NUM_THREADS="1",
             CCX_NPROC_STIFFNESS=str(cores),CCX_NPROC_EQUATION_SOLVER=str(cores))
    argv=[sys.executable,SIMJOB,"run","--cores",str(cores),"--mem",mem,"--timeout","7200",
          "--",sys.executable,str(pathlib.Path(__file__).resolve()),name,"--inside"]
    record=dict(name=name,started_at=stamp(),cores=cores,mem=mem,argv=argv,
                deck_sha256=hashlib.sha256((d/"model.inp").read_bytes()).hexdigest(),
                runner_sha256=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
                available_before=pathlib.Path("/proc/meminfo").read_text(),
                psi_before=pathlib.Path("/proc/pressure/memory").read_text())
    (d/"LAUNCH.json").write_text(json.dumps(record,indent=2)+"\n")
    start=time.monotonic()
    with (d/"simjob.stdout").open("w") as out,(d/"simjob.stderr").open("w") as err:
        p=subprocess.run(argv,env=env,stdout=out,stderr=err)
    record.update(ended_at=stamp(),elapsed_s=time.monotonic()-start,returncode=p.returncode)
    (d/"LAUNCH.json").write_text(json.dumps(record,indent=2)+"\n")
    return record
def inside(name):
    d=ROOT/"runs"/name
    t=time.monotonic()
    with (d/"ccx.stdout").open("w") as out,(d/"ccx.stderr").open("w") as err:
        p=subprocess.run(["ref-c5feaeda041c435960d7","-v","-o",str(d/"resource.txt"),
                          "ref-ab3b45338c202f661802","-i","model"],cwd=d,stdout=out,stderr=err)
    (d/"SOLVER.json").write_text(json.dumps(dict(returncode=p.returncode,
        elapsed_s=time.monotonic()-t,ended_at=stamp()),indent=2)+"\n")
    return p.returncode
if __name__=="__main__":
    a=argparse.ArgumentParser();a.add_argument("name");a.add_argument("--inside",action="store_true")
    x=a.parse_args()
    if x.inside:sys.exit(inside(x.name))
    print(json.dumps(run(x.name)))
