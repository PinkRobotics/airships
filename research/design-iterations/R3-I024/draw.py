#!/usr/bin/env python3
"""Deterministic drawing of saved finite geometry; executes no engineering model."""
import argparse
import html
import json
import math
from pathlib import Path
HERE=Path(__file__).resolve().parent


def drawing(d):
    out=['<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="2650" viewBox="0 0 1800 2650">',
         '<rect width="1800" height="2650" fill="#eef2f5"/>',
         '<style>text{font-family:Arial,sans-serif} .small{font-size:16px} .body{font-size:20px} .title{font-size:26px;font-weight:bold}</style>']
    def text(x,y,s,size=20,color='#172a3a',weight='normal'):
        out.append(f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" fill="{color}" font-weight="{weight}">{html.escape(str(s))}</text>')
    def line(x1,y1,x2,y2,color='#617687',width=2,dash=''):
        out.append(f'<line x1="{x1:.2f}" y1="{y1:.2f}" x2="{x2:.2f}" y2="{y2:.2f}" stroke="{color}" stroke-width="{width}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
    def rect(x,y,w,h,fill='white',stroke='#b8c4cf',width=1):
        out.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')
    def circle(x,y,r,fill='none',stroke='#172a3a',width=2):out.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{r:.2f}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')
    def panel(x,y,w,h,title):rect(x,y,w,h);text(x+20,y+35,title,24,weight='bold')
    def polygon(points,fill,stroke='#334b60',opacity=.35):
        out.append('<polygon points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in points)+f'" fill="{fill}" fill-opacity="{opacity}" stroke="{stroke}" stroke-width="1.1"/>')
    def hull(points):
        pts=sorted(set(points))
        def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
        low=[];high=[]
        for p in pts:
            while len(low)>1 and cross(low[-2],low[-1],p)<=0:low.pop()
            low.append(p)
        for p in reversed(pts):
            while len(high)>1 and cross(high[-2],high[-1],p)<=0:high.pop()
            high.append(p)
        return low[:-1]+high[:-1]
    def corners(s):
        c=s['centreXRT'];axes=s['axes'];dims=s['dimensionsM'];points=[]
        for a in [-1,1]:
            if s['kind'] in ['cylinder','tube']:
                coords=[[a*dims[0]/2,math.cos(j*math.pi/8)*dims[1]/2,math.sin(j*math.pi/8)*dims[2]/2] for j in range(16)]
            else:coords=[[a*dims[0]/2,b*dims[1]/2,z*dims[2]/2] for b in [-1,1] for z in [-1,1]]
            points.extend([[c[k]+sum(v*axis[k] for v,axis in zip(q,axes)) for k in range(3)] for q in coords])
        return points
    def body(s,project,color=None,opacity=.24):
        if s['kind']=='ringbox':return
        name=s['name'];color=color or ('#df9337' if 'collector' in name else '#af4d7d' if 'AD' in name else '#c95854' if 'button' in name else '#267d9b' if 'carbon' in name else '#8292a1')
        polygon(hull([project(p) for p in corners(s)]),color,color,opacity)
    g=d['geometry'];fit=d['clearance'];mass=d['mass'];cases=d['loadCases'];members={m['name']:m for m in g['members']}
    text(40,48,'R3-I024  |  Spaced polar node: finite construction and retained failures',34,weight='bold')
    text(40,82,'D80 × 160 m capsule · 37 sectors per cap · one selected arrangement · actual displaced pin centres',22)
    rect(40,101,1720,48,'#8f2635','#8f2635');text(60,133,'ASSEMBLY FAIL  |  Known contact / access / attachment failures; physical float, global pressure and complete U+C UNKNOWN',22,'white','bold')
    panel(40,165,1720,150,'Full envelope and unchanged pressure tributary')
    s=1.2;cx=265;cy=250
    out.append(f'<path d="M {cx-40*s} {cy-40*s} H {cx+40*s} A {40*s} {40*s} 0 0 1 {cx+40*s} {cy+40*s} H {cx-40*s} A {40*s} {40*s} 0 0 1 {cx-40*s} {cy-40*s} Z" fill="#dae5ed" stroke="#536b7c" stroke-width="2"/>')
    line(cx-80*s,cy,cx+80*s,cy,'#536b7c',1,'5 5')
    for sign in [-1,1]:rect(cx+sign*73*s-9,cy-20,18,40,'#c95854','#8f2635')
    text(100,299,'Both caps repeat the same local selection',16)
    text(495,230,f"121590 Pa · polar axial force {d['unchangedPressureAndFilm']['polarAxialOneCapN']/1e6:.6f} MN per cap, once",22)
    text(495,263,'18 film bays × 666 columns; old incoming boundary separate; finite button pressure separate',20)
    text(495,294,'No 611 MN whole-end reapplication, ancestor model, matrix solve, sweep or volume credit',19)
    panel(40,335,800,1005,'Actual X–R projection (78 px/m; no display offsets)')
    project=lambda p:(150+(p[0]-76.0)*78,1250-(p[1]-2.0)*78)
    for r in range(3,14):
        x,y=project([76,r,0]);line(100,y,730,y,'#e1e7ec',1);text(63,y+5,str(r)+' m',15)
    for sld in g['solids']:
        if 'adapter' in sld['group'] and not sld['group'].endswith('-8'):continue
        body(sld,project)
    for name,p in g['nodesXRT'].items():
        x,y=project(p);circle(x,y,4,'#172a3a');text(x+18,y-10,name,23,weight='bold')
    for name,m in members.items():
        p,q=m['pinCentresXRT'];x,y=project(p);xx,yy=project(q);line(x,y,xx,yy,'#172a3a',1,'5 4')
        for point in [p,q]:a,b=project(point);circle(a,b,4,'white','#172a3a')
        text((x+xx)/2+20,(y+yy)/2,name,20,weight='bold')
    for st in g['stanchions']:
        p=st['beamAxisPointXRT'];x,y=project(p);text(x-36,y+5,str(st['row']),14)
    witness=next(w for w in fit['materialIntersectionWitnesses'] if w['first']=='AD pin A' and w['second']=='BD carbon')
    x,y=project(witness['pointXRT']);circle(x,y,12,'none','#b22f3f',3);line(x,y,675,520,'#b22f3f',2);text(565,482,'A pin / BD wall',18,'#b22f3f','bold');text(565,508,'material witness',18,'#b22f3f')
    text(70,1285,'Blue: carbon  |  ochre: collector  |  magenta: AD  |  red: button',17)
    text(70,1314,'Tube/plate outer silhouettes are shown; hollow interiors use the saved solid tests.',16)
    def pin_plan(node,x,y,w,h,scale,reference_x):
        panel(x,y,w,h,node+' pin planes: tangential T versus axial X')
        pr=lambda p:(x+w/2+p[2]*scale,y+h/2+(p[0]-reference_x)*scale)
        line(x+30,y+h/2,x+w-25,y+h/2,'#d6e0e8',1);line(x+w/2,y+55,x+w/2,y+h-35,'#d6e0e8',1)
        for sld in g['solids']:
            if sld.get('pin') and sld['name'].endswith(' '+node):
                body(sld,pr,opacity=.65);a,b=pr(sld['centreXRT']);text(a+25,b-15,sld['name'],17)
                if node=='C':
                    angle=g['sectorAngleRad'];co,si=math.cos(angle),math.sin(angle)
                    rot=lambda p:[p[0],co*p[1]-si*p[2],si*p[1]+co*p[2]]
                    other=dict(sld,centreXRT=rot(sld['centreXRT']),axes=[rot(v) for v in sld['axes']]);body(other,pr,'#a7b7c4',.25)
        text(x+25,y+h-18,'100 × 220 mm pins; local pin axes are normal to each actual member axis.',16)
    pin_plan('D',860,335,900,300,430,77.61)
    text(885,405,'T = −500, 0, +500 mm',18)
    pin_plan('C',860,655,900,350,285,79.30)
    text(885,725,'DC: X −350 / T +250 mm; BC: X +350 / T −250 mm',17)
    text(885,751,'Faint pins: next of 37 sectors. Projection alone is not a clearance proof.',16)
    panel(860,1025,900,315,'AD cartridge detail: e–n plane, 700 px/m')
    ad=members['AD'];px=1010;py=1195;scale=700;L=ad['pinLengthM']
    for p in [0.,L]:circle(px+p*scale,py,.110*scale,'#f0d4e2','#934166');circle(px+p*scale,py,.051*scale,'white','#934166')
    rect(px+.160*scale,py-.090*scale,(L-.320)*scale,.180*scale,'#db9dbb','#934166')
    for u in [.110,L-.160]:rect(px+u*scale,py-.090*scale,.050*scale,.180*scale,'#db9dbb','#934166')
    for p in [.110,L-.110]:circle(px+p*scale,py,8,'none','#b22f3f',3)
    text(890,1089,f"Pin spacing {L*1000:.3f} mm; free 180 mm neck {ad['freeNeckLengthM']*1000:.3f} mm",19)
    text(890,1295,'FAIL: round eye meets cylindrical shoulder only at its 110 mm tangent.',19,'#b22f3f','bold')
    text(890,1321,'FAIL: 220 mm blank cannot contain the eyes; paid stock is not a fabricated cartridge.',17,'#b22f3f')
    panel(40,1360,800,335,'Root normal-datum adapter: actual inclined webs')
    adp=g['rootAdapter'];normal=adp['normalXRT'];tangent=[-normal[1],normal[0],0.];old=adp['oldInterfaceXRT'];new=adp['newInterfaceXRT'];k=2.2
    def local(p):
        q=[p[i]-old[i] for i in range(3)];return (420+sum(q[i]*tangent[i] for i in range(3))*1000*k,1455+sum(q[i]*normal[i] for i in range(3))*1000*k)
    for p,sense in [(old,1),(new,-1)]:
        a,b=local(p);rect(a-176,b if sense==1 else b-17.6,352,17.6,'#889fac','#536b7c')
    a,b=local([old[i]+.008*normal[i] for i in range(3)]);c,e=local([new[i]-.008*normal[i] for i in range(3)])
    polygon([(a-95,b),(a+95,b),(c+95,e),(c-95,e)],'#d2a269','#8e673c',.6)
    text(65,1416,'Two 160 × 120 × 8 plates; two 100 × 12 webs; four M8 × 50 per end',17)
    text(65,1618,f"Normal step {adp['normalStepM']*1000:.3f} mm; tangent {adp['tangentStepM']*1000:.3f} mm; web {adp['webLengthM']*1000:.3f} mm",18)
    text(65,1646,'Required −84.205 Nm incoming-bar couple retained; 24 mm grip; both feet separate.',17)
    text(65,1674,'Two webs are at T ±35 mm. Drawing shows their common normal/tangent projection.',16)
    panel(40,1715,800,525,'All 17 posts: finite hoop cuff and separate beam-foot checks')
    for x,label in [(65,'Row'),(125,'Cut mm'),(235,'Socket gap'),(365,'Beam cuff'),(500,'Source T mm'),(665,'Foot gap mm')]:text(x,1785,label,16,weight='bold')
    for i,s in enumerate(g['stanchions']):
        cuff=s['finiteHoopCuffAttachment'];color='#b22f3f' if not s['insertFit'] or not s['cuffWithinCarbon'] or cuff['connectionFitStatus']=='FAIL' else '#172a3a'
        for x,value in [(75,str(s['row'])),(125,f"{s['selectedTubeLengthM']*1000:.3f}"),(235,f"{s['insertGapM']*1000:.3f}"),(365,'inside' if s['cuffWithinCarbon'] else 'OUT'),(500,f"{cuff['sourceAxialCoordinateM']*1000:.3f}"),(665,f"{cuff['provedAxialMaterialGapM']*1000:.3f}")]:text(x,1815+i*20,value,17,color)
    text(65,2175,'Hoop cuff T = ±40 mm. Positive foot gap proves no contact; zero is not a joint PASS.',16)
    text(65,2204,'Source datum uses an infinite cylinder. Socket gap in mm; beam cuff check is separate.',16)
    panel(860,1360,900,525,'Vector demands at the unqualified receiving frame')
    text(885,1425,'Full DC wrench → actual pin forces plus D torsion; no old 2D force reuse.',18)
    text(885,1456,'Collector C → D → A yoke; B retains its separate main-member reactions.',18)
    for x,label in [(885,'Member axial force MN'),(1230,'f = 0'),(1460,'f = 1')]:text(x,1493,label,20,weight='bold')
    for i,name in enumerate(['AD','BD','BC','DC_reference']):
        text(900,1528+i*29,name,19)
        for j,x in enumerate([1230,1460]):text(x,1528+i*29,f"{cases[j]['memberSignedTensionN'][name]/1e6:+.6f}",19)
    for j,c in enumerate(cases):
        y=1668+j*90;peak=max(s['additiveNormalStressPa'] for leg in c['collectorLegs'] for s in leg['sectionEndpoints'])
        text(885,y,f"f={j}: collector additive envelope {peak/1e6:.3f} MPa vs 355 → FAIL",20,'#b22f3f','bold')
        r=c['receiverDemands'][0];moment=r['coupleToInheritedFrameXRTnm']
        text(885,y+29,'A required moment (Mx, Mr, Mt) MNm = '+', '.join(f'{v/1e6:+.3f}' for v in moment),18)
        text(885,y+55,f"Algebraic moment residual {c['momentIdentityResidualNm']:.2e} Nm; capacity not inferred.",17)
    panel(860,1905,900,335,'Button and collector connection details')
    b=g['buttonSupport'];text(885,1970,'Button: 300 × 300 × 16 box; 400 × 400 × 20 plate at each end.',19)
    text(885,2000,'Eight M24 × 140 per end, 320 mm perimeter pattern; 1200 mm of 10 mm weld.',18)
    text(885,2030,'FAIL: 40 mm plate/pad-to-box gap at each end; no free joining stub.',20,'#b22f3f','bold')
    text(885,2060,f"New receiver couple {cases[0]['buttonFeet']['deliveredReceiverCoupleXRTnm'][2]/1000:.3f} kNm; original −95.672 kNm retained as comparison.",17)
    text(885,2083,f"Internal tensile-positive button force {cases[0]['buttonSectionEndpoints'][0]['signedAxialN']/1000:+.3f} kN: compression; Euler branch tested.",16)
    text(885,2100,'Collector: 500 × 500 × 20 box, 20 mm splice gap, four 750 × 500 × 20 covers.',18)
    text(885,2130,'16 M24 per series splice side, 32 total; 365 mm overlap each side.',18)
    text(885,2160,'Actual wall/cover load demands recorded. Prying, slip, weld moment sharing,',18)
    text(885,2188,'access-hatch weakening and receiving-frame stiffness remain unqualified.',18)
    panel(40,2260,1720,350,'Assembly attempt, stock reconciliation and limits')
    text(65,2328,'1  Preassemble split cuffs, yokes and backers.  2  Assemble box halves and face-cover splice; keep nut hatches open.',20)
    text(65,2360,'3  Offer fork roots and keyed DC end.  4  Insert each 220 mm pin along its actual axis through a 300 mm travel.',20)
    text(65,2392,'5  Attach sockets, adapters and button feet; close access covers only after inspection. This sequence is blocked.',20,'#b22f3f')
    blocked=sum(bool(a['provedObstructions']) for a in fit['pinInsertionAccess'])
    text(65,2432,f"{len(fit['materialIntersectionWitnesses'])} representative material witnesses; {len(fit['unresolvedOverlapBounds'])} unresolved bound overlaps; {blocked} proved insertion obstructions.",20,'#b22f3f','bold')
    text(65,2467,f"Carried hull {mass['acceptedI020HullT']:.6f} − retirement {mass['selectedRetirementT']:.6f} + new stock {mass['newAddedT']:.6f} = hull {mass['hullT']:.6f} t.",21,weight='bold')
    text(65,2501,f"Hull + gas once {mass['residualGasOnceT']:.6f} = subtotal {mass['knownSubtotalT']:.6f} t; margins {mass['at'][0]['knownMarginT']:.6f} / {mass['at'][1]['knownMarginT']:.6f} t.",21,weight='bold')
    text(65,2538,'Old replaced duties remain inactive contingency, not co-installed geometry. Film, button-strip and inherited hull failures remain.',19)
    text(65,2571,'One selected geometry only. All conditional nominal screens coexist with assembly FAIL and global / physical / U+C UNKNOWN.',19)
    text(40,2635,'Saved geometry and demands only · dimensions in metres unless labelled · source/stock/connection tables in README and result.json',16)
    out.append('</svg>');return '\n'.join(out)+'\n'


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');parser.add_argument('--check',action='store_true');args=parser.parse_args()
    text=drawing(json.loads((HERE/'result.json').read_text()));path=HERE/'geometry.svg'
    if args.write:path.write_text(text)
    elif args.check:assert path.read_text()==text,'Saved drawing differs';print('I024 saved drawing matches saved geometry and demand record.')
    else:print(text)


if __name__=='__main__':main()
