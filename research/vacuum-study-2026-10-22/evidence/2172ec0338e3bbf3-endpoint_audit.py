"""Postprocess completed baseline states; no FE solve or numerical library.

Owner NPZ files supply only endpoint labels and geometry for correspondence.
Forces use this check's independently solved displacements. Standard-library
NPY decoding avoids importing either the owner code or a numerical library.
"""
from pathlib import Path
import array
import ast
import json
import math
import struct
import sys
import zipfile

ROOT=Path(__file__).resolve().parent


def load_arrays(path,names):
    output={}
    with zipfile.ZipFile(path) as z:
        for name in names:
            with z.open(name+".npy") as f:
                magic=f.read(8)
                assert magic[:6]==b"\x93NUMPY"
                fmt="<H" if magic[6]==1 else "<I"
                length=struct.unpack(fmt,f.read(struct.calcsize(fmt)))[0]
                header=ast.literal_eval(f.read(length).decode())
                assert not header["fortran_order"]
                code={"<f8":"d","<i8":"q","<i4":"i"}[header["descr"]]
                values=array.array(code)
                values.frombytes(f.read())
                if sys.byteorder!="little":values.byteswap()
                shape=header["shape"]
                if len(shape)==2:
                    output[name]=[values[i:i+shape[1]] for i in range(0,len(values),shape[1])]
                else:output[name]=values
    return output


def dot(x,y):return sum(a*b for a,b in zip(x,y))
def sub(x,y):return [a-b for a,b in zip(x,y)]
def add(x,y):return [a+b for a,b in zip(x,y)]
def norm(x):return math.sqrt(dot(x,x))
def cross(x,y):return [x[1]*y[2]-x[2]*y[1],x[2]*y[0]-x[0]*y[2],x[0]*y[1]-x[1]*y[0]]
def key(x):return tuple(round(v,9) for v in x)
def stats(x):return dict(min=min(x),mean=sum(x)/len(x),max=max(x))


def force_left(i,j,x,u,area,inertia):
    delta=sub(x[j],x[i]);length=norm(delta)
    t=[v/length for v in delta]
    du=sub(u[6*i:6*i+3],u[6*j:6*j+3])
    rotation=add(u[6*i+3:6*i+6],u[6*j+3:6*j+6])
    axial=dot(du,t)
    transverse=sub(du,[axial*v for v in t])
    rotational=cross(rotation,t)
    return [410e9*area/length*axial*t[k]+12*410e9*inertia/length**3*transverse[k]+
            6*410e9*inertia/length**2*rotational[k] for k in range(3)]


owner=json.loads((ROOT/"intake/owner/RESULTS.json").read_text())
rows=[]
for f,label,source in [
    (6,"f6-m12","static/f6-m12-rise1/static.npz"),
    (4,"f4-m24","classical/rigid-f4-m24/modes.npz"),
    (2,"f2-m48","classical/rigid-f2-m48/modes.npz")]:
    own=load_arrays(ROOT/"runs"/label/"STATIC.npz",["points","chains","u"])
    metadata=json.loads((ROOT/"runs"/label/"RESULTS.json").read_text())
    model=metadata["model"]
    a=load_arrays(ROOT/"intake/owner-data"/source,["coordinates","chains"])
    lookup={}
    for chain in own["chains"]:
        x=own["points"];u=own["u"]
        chord=sub(x[chain[-1]],x[chain[0]])
        chord=[v/norm(chord) for v in chord]
        left=dot(force_left(chain[0],chain[1],x,u,model["A_m2"],model["I_m4"]),chord)
        right=dot(force_left(chain[-2],chain[-1],x,u,model["A_m2"],model["I_m4"]),chord)
        lookup[key(x[chain[0]]),key(x[chain[-1]])]=(left,right)
    ordered_first,ordered_second=[],[]
    for chain in a["chains"]:
        k=(key(a["coordinates"][chain[0]]),key(a["coordinates"][chain[-1]]))
        if k in lookup:left,right=lookup[k]
        else:
            right,left=lookup[k[1],k[0]]
        ordered_first.append(left);ordered_second.append(right)
    two_end=[(l+r)/2 for l,r in zip(ordered_first,ordered_second)]
    claimed=next(r for r in owner["comparison"] if r["frequency"]==f)["static"]
    reported=claimed["member_endpoint_chord_thrust_all_N"]
    differences=[a-b for a,b in zip(ordered_first,reported)]
    rows.append(dict(frequency=f,
        owner_selected_endpoint_stats=claimed["member_endpoint_chord_thrust_N"],
        independent_first_endpoint_in_owner_orientation_stats=stats(ordered_first),
        independent_second_endpoint_in_owner_orientation_stats=stats(ordered_second),
        independent_both_endpoint_mean_stats=stats(two_end),
        max_difference_owner_vs_first_endpoint_N=max(map(abs,differences)),
        max_relative_difference_owner_vs_first_endpoint=max(abs(d)/max(abs(v),1) for d,v in zip(differences,reported)),
        own_first_endpoint_in_owner_order_N=ordered_first,
        own_second_endpoint_in_owner_order_N=ordered_second,
        own_both_end_mean_in_owner_order_N=two_end,
        independent_displacements=True,
        owner_displacements_used=False))
    assert rows[-1]["max_relative_difference_owner_vs_first_endpoint"]<2e-8
    print(json.dumps({k:v for k,v in rows[-1].items() if not isinstance(v,list)}))
result=dict(method="Global-coordinate end-force recovery from independently solved baseline states, matched by endpoint coordinates.",
    new_solver_or_simulation_run=False,owner_coordinates_used_only_for_labels=True,
    conclusion="Owner values sample the first endpoint in its stored member orientation. Both-end means differ slightly; specify the sampling convention.",
    rows=rows)
(ROOT/"ENDPOINT-AUDIT.json").write_text(json.dumps(result,indent=2)+"\n")
