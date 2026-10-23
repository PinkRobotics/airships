"""Rank and explicitly defined condition diagnostics; no artificial supports."""
import json
import numpy as np
from frame45 import mesh
from check45 import ROOT,save

p=json.loads((ROOT/"ARITHMETIC.json").read_text())["p3"]
owner=json.loads((ROOT/"inputs/owner/DET.json").read_text())["frame"]
out=[]
for f in [4,5]:
    points,tris,edges=mesh(f)
    b=np.zeros((len(edges),3*len(points)))
    for k,(i,j) in enumerate(edges):
        vector=points[j]-points[i];length=np.linalg.norm(vector)
        vector=vector/length*np.sqrt(410e9*p["A"]/length)
        b[k,3*i:3*i+3]=-vector;b[k,3*j:3*j+3]=vector
    sig=np.linalg.svd(b,compute_uv=False)
    damaged=np.delete(b,0,axis=0)
    sigd=np.linalg.svd(damaged,compute_uv=False)
    rank=int(np.sum(sig>sig[0]*1e-10));rankd=int(np.sum(sigd>sigd[0]*1e-10))
    out.append(dict(frequency=f,nodes=len(points),members=len(edges),
      intact_rank=rank,damaged_rank=rankd,
      intact_nonrigid_nullity=3*len(points)-rank-6,damaged_nonrigid_nullity=3*len(points)-rankd-6,
      intact_condition_after_orthogonal_rigid_mode_projection=float((sig[0]/sig[-1])**2),
      damaged_condition_after_same_projection=None,damaged_condition_interpretation="infinite: one extra exact mechanism",
      removed_edge=edges[0].tolist(),owner_intact_condition=owner[f"f{f}"]["pinned_intact_cond"],
      owner_damaged_condition=owner[f"f{f}"]["pinned_one_gone_cond"],
      comparison_scope="The anchored/scaled matrix constraints are not stated in the permitted non-code inputs; numerical condition depends on that representation. Rank is the invariant comparison."))
save("TRUSS-RANK-CHECKS.json",out)
print(json.dumps(out,indent=2))
