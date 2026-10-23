"""Declared-mode scoring with discrete member forces and actual end moments.

All scalar material/joint capacities remain unqualified projections.
"""
import math
import numpy as np
from scipy.optimize import brentq
from frame_tools import LIFT,SURFACE
import beam as b

RHOJ,SIGMAJ,TAU=1550.,1470e6,28.9e6
FILM_RHO,FILM_EFFECTIVE,FILM_FLOOR=1560.,1.74e9,12e-6
FT=15.586e6
RESERVES={"5":.05*LIFT,"019":411.2989440716474}


def roots(alpha,beta,euler,strength,kind):
    aa=alpha/euler
    if kind=="compression":
        bb=alpha+beta+strength/euler
        return 2*strength/(bb+np.sqrt(np.maximum(bb*bb-4*aa*strength,0)))
    bb=beta-alpha+strength/euler
    return (np.sqrt(bb*bb+4*aa*strength)-bb)/(2*aa)


def section(area,gyration):
    ro=np.sqrt(2*gyration*gyration+area/(2*math.pi))
    ri=np.sqrt(2*gyration*gyration-area/(2*math.pi))
    return float(ro),float(ro-ri),area*gyration*gyration


def end_design(N,M,T,ro,target):
    """Exact annular axial/bending sleeve plus bonded-ring shear projection."""
    N=np.maximum(N,0)
    # Solve SIGMA*a = q*(N + 4 M rj/(rj²+ro²)) by monotone fixed point.
    area=target*(N+2*M/ro)/SIGMAJ
    for _ in range(12):
        outer=np.sqrt(ro*ro+area/math.pi)
        area=target*(N+4*M*outer/(outer*outer+ro*ro))/SIGMAJ
    outer=np.sqrt(ro*ro+area/math.pi)
    I=area*(outer*outer+ro*ro)/4
    equivalent=np.sqrt((N+2*M/ro)**2+(T/ro)**2)
    overlap=target*equivalent/(2*math.pi*ro*TAU)
    mass=RHOJ*area*overlap
    axial_util=target*(N/area+M*outer/I)/SIGMAJ
    bond_util=target*equivalent/(2*math.pi*ro*overlap*TAU)
    return {"area":area,"outer":outer,"overlap":overlap,"mass":mass,
            "axial_util":axial_util,"bond_util":bond_util}


def score(response,arrays,area=None,gyration=None,film=None,reserve="5",
          joint_target=None,original_joints=False):
    geo=response["geometry"];ref=response["section"]
    area=ref["area_m2"] if area is None else area
    gyration=ref["gyration_m"] if gyration is None else gyration
    ro,wall,I=section(area,gyration)
    film=b.SELECTED["film_total_m"] if film is None else film
    N=np.maximum(arrays["subelement_N"],1e-12)
    M=arrays["subelement_M"]
    member=np.asarray(arrays["subelement_member"],int)
    L=np.asarray(geo["member_arc_lengths_m"])[member]
    euler=math.pi**2*b.E*I/(L*L*N)
    alpha=N/area
    # Include computed pressure bending plus the declared L/1000 imperfection.
    beta=(M+N*L/1000)*ro/I
    gamma=.099+.901*math.exp(-math.sqrt(ro/wall)/16)
    compression=3.9e9/alpha
    perry=roots(alpha,beta,euler,3.9e9,"compression")
    tension=roots(alpha,beta,euler,FT,"tension")
    modes={"compression_axial":float(compression.min()),
           "euler":float(euler.min()),
           "local_axial":float((gamma*.6*b.E*wall/ro/alpha).min()),
           "perry_with_FE_bending":float(perry.min()),
           "tension_with_FE_bending":float(tension.min()),
           "film":2*FILM_EFFECTIVE*film/(b.P*geo["film_curvature_radius_max_m"]),
           "global_perfect_linear":response["linear_lambda"][0]*area/ref["area_m2"]}
    modes["global_k0p2"]=.2*modes["global_perfect_linear"]
    JN,JM,JT=arrays["joint_N"],arrays["joint_M"],arrays["joint_T"]
    if original_joints:
        Aj=b.SELECTED["joint"]["section_area_m2"]
        overlap=b.SELECTED["joint"]["overlap_m"]
        outer=math.sqrt(ro*ro+Aj/math.pi)
        Ij=Aj*(outer*outer+ro*ro)/4
        demand=JN/Aj+JM*outer/Ij
        bond=np.sqrt((JN+2*JM/ro)**2+(JT/ro)**2)/(2*math.pi*ro*overlap)
        modes["joint_axial_bending"]=float((SIGMAJ/demand).min())
        modes["joint_bond_axial_bending_torsion"]=float((TAU/bond).min())
        joint_mass=2*geo["members"]*RHOJ*Aj*overlap
        joint={"original_area_m2":Aj,"original_overlap_m":overlap,
               "max_axial_bending_stress_at_1_Pa":float(demand.max()),
               "max_bond_shear_at_1_Pa":float(bond.max()),
               "area_minmax_m2":[Aj,Aj],"overlap_minmax_m":[overlap,overlap]}
    else:
        target=joint_target if joint_target is not None else min(v for k,v in modes.items() if k!="global_perfect_linear")
        design=end_design(JN,JM,JT,ro,target)
        joint_mass=float(design["mass"].sum())
        modes["joint_axial_bending"]=float(target/np.max(design["axial_util"]))
        modes["joint_bond_axial_bending_torsion"]=float(target/np.max(design["bond_util"]))
        joint={"target":target,"area_minmax_m2":[float(design["area"].min()),float(design["area"].max())],
               "overlap_minmax_m":[float(design["overlap"].min()),float(design["overlap"].max())],
               "max_axial_utilization":float(design["axial_util"].max()),
               "max_bond_utilization":float(design["bond_util"].max())}
    least=min(v for k,v in modes.items() if k!="global_perfect_linear")
    unknocked=min(v for k,v in modes.items() if k!="global_k0p2")
    q=least
    bend=q*(M+N*L/1000)*ro/I/(1-q/euler)
    extreme=q*alpha+bend
    signed_t=bend-q*alpha
    mass={"tube":b.RHO*area*geo["total_arc_m"],"film":SURFACE*FILM_RHO*film,
          "joint":joint_mass,"nodes":geo["node_mass_kg"],"systems":100.,
          "sag_lift_loss":geo["sag_lift_debit_kg"],"reserve":RESERVES[reserve]}
    mass["total_with_reserve_and_sag"]=sum(mass.values())
    mass["headroom"]=LIFT-mass["total_with_reserve_and_sag"]
    return {"frequency":geo["frequency"],"section":{"area_m2":area,"gyration_m":gyration,
             "r_o_m":ro,"wall_m":wall,"inertia_m4":I},"film_total_m":film,
            "modes":modes,"least_screened_SF":least,"least_without_global_knockdown":unknocked,
            "binding_modes":[k for k,v in modes.items() if abs(v-least)<2e-6],
            "required_SiC_extreme_compression_at_screened_limit_Pa":float(extreme.max()),
            "max_tension_at_screened_limit_Pa":float(np.maximum(signed_t,0).max()),
            "operating_FE_extreme_compression_Pa":float(np.max(alpha+M*ro/I)),
            "operating_FE_peak_bending_moment_Nm":float(M.max()),
            "joint_end_peak_moment_Nm":float(JM.max()),
            "joint_end_peak_torsion_Nm":float(JT.max()),
            "joint_end_peak_compression_N":float(JN.max()),
            "mass_kg":mass,"joint":joint,"reserve":reserve,
            "qualified_structural_SF":None,"qualified_joint_capacity":None,
            "tag":"QUESTIONABLE / PROJECTION"}
