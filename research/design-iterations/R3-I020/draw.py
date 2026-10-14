#!/usr/bin/env python3
"""Draw the saved fixed polar construction; no calculator execution."""
import argparse
import html
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
INK = '#183348'
MUTED = '#526779'
TEAL = '#087f8c'
BLUE = '#2463ae'
RED = '#b92334'
ORANGE = '#af620d'
GREY = '#a5b3bd'
PALE = '#f3f7fa'


def drawing(data):
    svg = ['<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="2300" viewBox="0 0 1800 2300">',
           '<title>Failed finite polar transition: one repeated module, signed loads and stock ledger</title>',
           '<desc>Dimensioned D80 capsule and local polar module. Four pin intersections, AD insert overlap, short posts and root adapter gap remain. Nominal force routes leave unsupported moments and negative mass margins.</desc>',
           '<defs><marker id="arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#526779"/></marker></defs>',
           '<rect width="1800" height="2300" fill="#e7eef3"/>',
           '<g font-family="DejaVu Sans,Arial,sans-serif" fill="#183348">']

    def text(x, y, value, size=18, color=INK, weight='normal', anchor='start'):
        svg.append(f'<text x="{x:.3f}" y="{y:.3f}" font-size="{size}" fill="{color}" font-weight="{weight}" text-anchor="{anchor}">{html.escape(str(value))}</text>')

    def lines(x, y, values, size=18, color=INK, step=27):
        for i, v in enumerate(values):
            text(x, y+i*step, v, size, color)

    def line(a, b, color=INK, width=2, dash=None, arrow=False):
        extra = f' stroke-dasharray="{dash}"' if dash else ''
        if arrow: extra += ' marker-end="url(#arrow)"'
        svg.append(f'<line x1="{a[0]:.3f}" y1="{a[1]:.3f}" x2="{b[0]:.3f}" y2="{b[1]:.3f}" stroke="{color}" stroke-width="{width}"{extra}/>')

    def rect(x,y,w,h,fill='none',stroke=INK,width=2):
        svg.append(f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')

    def circle(x,y,r,fill='white',stroke=INK,width=2):
        svg.append(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{r:.3f}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')

    def poly(points,color=INK,width=2,fill='none',dash=None):
        extra=f' stroke-dasharray="{dash}"' if dash else ''
        pts=' '.join(f'{x:.3f},{y:.3f}' for x,y in points)
        svg.append(f'<polyline points="{pts}" fill="{fill}" stroke="{color}" stroke-width="{width}"{extra}/>')

    def panel(x,y,w,h,title,subtitle):
        rect(x,y,w,h,'white','#c7d3dd',1)
        text(x+20,y+33,title,24,INK,'bold')
        text(x+20,y+60,subtitle,16,MUTED)

    def dim(a,b,label,dy=-10,size=16):
        line(a,b,MUTED,1)
        line((a[0],a[1]-5),(a[0],a[1]+5),MUTED,1)
        line((b[0],b[1]-5),(b[0],b[1]+5),MUTED,1)
        text((a[0]+b[0])/2,(a[1]+b[1])/2+dy,label,size,MUTED,anchor='middle')

    text(30,47,'POLAR TRANSITION  ·  ONE FIXED CONSTRUCTION',34,INK,'bold')
    text(30,82,'R3-I020  |  corrected I016 comparison  |  37 sectors × 2 caps  |  geometry unchanged after the failed trial',20,MUTED)
    text(1770,47,'FIT FAIL',30,RED,'bold','end')
    text(1770,81,'Pressure / physical capacity UNKNOWN',18,RED,anchor='end')

    panel(30,110,840,460,'A  Capsule and retained cap structure','Equal X/R scale. Both polar modules shown; all other failed hull structure carries.')
    def global_map(x,r):return (450+4*x,335-4*r)
    boundary=[]
    for i in range(49):
        phi=-math.pi/2+i*math.pi/48
        boundary.append(global_map(40+40*math.cos(phi),40*math.sin(phi)))
    for i in range(49):
        phi=math.pi/2+i*math.pi/48
        boundary.append(global_map(-40+40*math.cos(phi),40*math.sin(phi)))
    boundary.append(boundary[0]);poly(boundary,INK,2,PALE)
    line(global_map(-85,0),global_map(85,0),GREY,1,'8 5')
    for j in range(-40,41,4):line(global_map(j,-40),global_map(j,40),GREY,1)
    for side in (-1,1):
        for deg in range(4,73,4):
            phi=math.radians(deg);x=side*(40+40*math.sin(phi));r=40*math.cos(phi)
            line(global_map(x,-r),global_map(x,r),GREY,1)
        cap=[]
        for i in range(25):
            phi=math.radians(72)+i*(math.pi/2-math.radians(72))/24
            cap.append(global_map(side*(40+40*math.sin(phi)),40*math.cos(phi)))
        poly(cap,RED,5)
        poly([(x,670-y) for x,y in cap],RED,5)
        line(global_map(side*79.387341,-3),global_map(side*79.387341,3),RED,4)
    dim(global_map(-80,-43),global_map(80,-43),'160.000 m overall',dy=10)
    text(385,235,'D = 80 m',19,INK,'bold')
    text(325,286,'80 m barrel',22,MUTED)
    text(325,320,'111-node frames',18,MUTED)
    text(325,386,'37-node cap frames',18,MUTED)
    text(53,558,'Red: 72° → finite button. No whole-cap repair, volume credit or new gas charge.',18,RED)

    panel(900,110,870,860,'B  One meridional module: actual nodes and pins','Equal X/R scale; plate roots and fine hoops indicated. Both endpoints priced separately.')
    g=data['geometry'];nodes=g['nodesXR'];film=data['filmLoadPath']
    def local(p):return (995+56*(p[0]-77),905-56*p[1])
    outer=[]
    for j in range(65):
        phi=math.radians(72)+j*(math.pi/2-math.radians(72))/64
        outer.append(local([40+40*math.sin(phi),40*math.cos(phi)]))
    poly(outer,INK,2)
    poly([local([40+40*math.sin(g['finiteButtonPhiRad']+j*(math.pi/2-g['finiteButtonPhiRad'])/16),
                 40*math.cos(g['finiteButtonPhiRad']+j*(math.pi/2-g['finiteButtonPhiRad'])/16)]) for j in range(17)],RED,5)
    line(local(nodes['C']),local(g['finiteButtonSurfaceXR']),BLUE,4)
    for k in ('A','B'):
        p=nodes[k];at=local([g['lastFrame']['xM'],p[1]])
        circle(*at,8,'#dce5ed',MUTED);line(at,local(p),MUTED,8)
    colors={'AD':ORANGE,'BD':BLUE,'DC':TEAL,'BC':BLUE}
    for m in g['members']:
        a=local(nodes[m['firstNode']]);b=local(nodes[m['lastNode']]);line(a,b,colors[m['name']],3,'6 4')
        pa,pb=m['pinCentresXR'];e=m['directionXR']
        ca=[pa[k]+.250*e[k] for k in (0,1)];cb=[pb[k]-.250*e[k] for k in (0,1)]
        line(local(ca),local(cb),colors[m['name']],56*.350)
        for p in (pa,pb):circle(*local(p),56*.050,'white',RED,2)
    for row in film['rows']:
        pin=local(row['barPinXR']);foot=local(row['clipPostFootXR'])
        line(pin,foot,ORANGE,2);circle(*pin,2,ORANGE,ORANGE)
        if row['stanchion']:
            col=local(row['collectorCentreXR']);beam=local(row['stanchion']['beamAxisPointXR'])
            bad=not row['stanchion']['minimumLengthPass'];line(col,beam,RED if bad else GREY,4)
            circle(*col,56*.050,'white',TEAL,1.5)
    poly([local(r['barPinXR']) for r in film['rows']],ORANGE,2)
    for key,size in [('D',.400),('C',.200)]:
        x,y=local(nodes[key]);rect(x-size*56/2,y-size*56/2,size*56,size*56,'none',TEAL,2)
    for key,off in {'A':(-47,0),'B':(-50,12),'D':(-32,-24),'C':(-40,28)}.items():
        x,y=local(nodes[key]);circle(x,y,3,INK,INK);text(x+off[0],y+off[1],key,23,INK,'bold')
    text(1215,220,'D root: 400 square × 25 box',18,TEAL,'bold')
    lines(1215,251,['A  (77.792261, 10.946997)','B  (77.592261,   9.678969)',
                    'D  (77.566732, 12.206171)','C  (79.387341,   3.000000)'],18,INK,29)
    lines(1215,390,['350 × 20 mm carbon, all four members',
                    'AD / BD / DC / BC pin lengths:',
                    '0.679 / 1.927 / 8.784 / 6.316 m',
                    'Pin centres: 300 mm from each node',
                    'Carbon setback: 250 mm from each pin'],18,INK,29)
    lines(1215,555,['DC carries 17 hoop loads + couples.',
                    'A/B receiving stiffness UNKNOWN.',
                    'Red supports: selected cut does not fit.',
                    '444 short locations across both caps.',
                    'Rows 1/17 cuffs also reach beyond carbon.'],18,RED,29)
    lines(1215,742,['C: 200 square × 20 box, R = 3 m',
                    'Button: 12 mm reused steel',
                    'Surface edge X = 79.887341 m',
                    'Finite ring-to-button offset = 0.500 m',
                    'One-cap polar axial load = 58.362306 MN'],18,TEAL,29)
    text(925,940,'Scope: X=77…80 m near the pole; the existing 72° receiving frame remains fixed.',18,MUTED)

    panel(30,590,840,380,'C  Receiving cuffs and 37-sector phase','Tangential/radial projection at equal scale; axial stems shown separately in panel B.')
    def tr(t,r):return (290+75*t,920-75*(r-9.4))
    alpha=g['sectorAngleRad'];beta=2*math.pi/666
    for key,node_radius in [('A',g['lastFrame']['outerRadiusM']),('B',g['lastFrame']['innerRadiusM'])]:
        end=node_radius*math.sin(alpha/2);rad=node_radius*math.cos(alpha/2)
        line(tr(-end,rad),tr(end,rad),BLUE,8)
        for sign in (-1,1):
            x,y=tr(sign*end,rad);rect(x-22.5,y-11,45,22,'#cedde9',BLUE,1)
        shift=g['cuffDevelopedOffsetsM'][key];x,y=tr(shift,rad)
        rect(x-15,y-12,30,24,'#d0eceb',TEAL,2)
        text(75*end+325,y+6,key,18,BLUE,'bold')
    pts=[]
    rd=nodes['D'][1]
    for k in range(41):
        theta=-alpha/2+k*alpha/40;pts.append(tr(rd*math.sin(theta),rd*math.cos(theta)))
    poly(pts,TEAL,8)
    for k in range(18):
        theta=(k-8.5)*beta;rr=40*math.cos(math.radians(72));circle(*tr(rr*math.sin(theta),rr*math.cos(theta)),2.5,ORANGE,ORANGE)
    text(65,695,'18 film columns / sector',16,ORANGE)
    lines(495,705,['Cuff: 328/296 × 400 mm',
                   '2 mm liner over 292 mm bridge',
                   'Half-film-pitch chord offset:',
                   '−51.638 mm A / −45.657 mm B',
                   'Nearest node-pad gaps:',
                   '+380.078 / +278.136 mm',
                   'PASS only for this named overlap.'],18,INK,31)

    panel(30,990,840,590,'D  Separate centred ends: selected solids collide','Local details, mm. Fork cross-section schematic; pin disks and AD insert cuts dimensioned.')
    centre=250;top=1120;scale=1.65
    for left,right,color in [(-80,-50,BLUE),(-40,40,ORANGE),(50,80,BLUE)]:
        rect(centre+scale*left,top,scale*(right-left),85,'#e0e9ed',color,2)
    rect(centre-scale*110,top+27,scale*220,30,'#a4b5c1',INK,1)
    text(65,1090,'Pin 100 diameter × 220 long',18,INK,'bold')
    dim((centre-scale*80,1233),(centre+scale*80,1233),'30 + 10 + 80 + 10 + 30 = 160',dy=24,size=16)
    text(65,1285,'80 mm eye centred between two 30 mm forks',17,INK)
    text(65,1311,'400 × 20 end plate; separate root and insert per end',16,MUTED)
    da=next(m for m in g['members'] if m['name']=='AD')
    cut=da['carbonCutM']*1000;s=.9;x0=165;y=1380
    rect(x0,y,cut*s,38,'#d0eceb',TEAL)
    rect(x0,y+5,300*s,12,'none',RED,2)
    rect(x0+(cut-300)*s,y+22,300*s,12,'none',ORANGE,2)
    dim((x0,y-12),(x0+cut*s,y-12),'AD carbon 179.211',dy=-10)
    text(65,1455,'Two 300 mm inserts: 420.789 mm overlap',18,RED,'bold')
    text(65,1486,'No shorter insert or moved node is substituted.',17,RED)
    pair=next(v for v in data['clearance']['centredPinPairs'] if v['node']=='D' and v['members']==['AD','DC'])
    p=pair['witnessXR'];origin=(680,1192);ps=1200
    for name,color in [('AD',ORANGE),('BD',BLUE),('DC',TEAL)]:
        m=next(m for m in g['members'] if m['name']==name)
        point=m['pinCentresXR'][1 if m['lastNode']=='D' else 0]
        x=origin[0]+ps*(point[0]-p[0]);y=origin[1]-ps*(point[1]-p[1])
        circle(x,y,.050*ps,'none',color,3);circle(x,y,2,color,color)
    circle(*origin,4,RED,RED)
    text(505,1090,'D: all three 100 mm pin disks',18,RED,'bold')
    lines(505,1315,['AD/DC centres: 5.403 mm',
                    'Required separation: 100 mm',
                    'Witness at both disks’ midpoint',
                    'Tangential coordinate = 0',
                    'Common pin extent: 220 mm',
                    'Also D: AD/BD and BD/DC collide.',
                    'C: DC/BC centres only 20.192 mm.'],17,RED,29)
    text(53,1552,'592 member-end assemblies + 592 distinct roots. A shared fitting is not silently substituted.',17,RED)

    panel(900,990,870,590,'E  Film normal stack and discontinuities','Nominal local normal coordinates, mm. Schematic support arrangement; dimensions govern.')
    x=955;y=1120;sc=1.05
    line((x,y),(x+740,y),INK,3);text(x,y-15,'R40 outer film face; 1 mm polymer (unqualified)',18,INK,'bold')
    rect(x+48,y+1,32,37.5*sc,'#f2dfbc',ORANGE,1)
    circle(x+64,y+60*sc,21.5*sc,'none',ORANGE,2)
    circle(x+64,y+60*sc,27.5*sc,'none',RED,1)
    line((x+64,y+(60+27.5)*sc),(x+64,y+(300-66)*sc),GREY,6)
    circle(x+64,y+300*sc,50*sc,'none',TEAL,2)
    circle(x+64,y+300*sc,66*sc,'none',BLUE,2)
    lines(x+165,y+32,['43 × 1 bar; 55/44 sleeve',
                      'Bar axis: 60 mm normal inset',
                      'Active pad: 37.5 / 31.5 mm',
                      'Full 38.5 mm stock stays charged',
                      '100 × 8 fine hoop: 300 mm inset',
                      '108 sleeve / 132 max foot-cuff OD',
                      'Sleeve-to-foot surface gap: 146.5 mm',
                      'Clip post space: 130.5 ≥ 80 mm'],18,INK,28)
    text(x+165,y+286,'These new nominal gaps pass only their stated checks.',17,TEAL)
    text(x+165,y+322,'Hoop → DC post: min −30.258 mm vs required 80 mm.',17,RED,'bold')
    lines(925,1540,['Root datum: 53.356 mm normal step − 16 mm flat plate = 37.356 mm unbridged.',
                    'Root known step couple −84.205 Nm/clip; transfer remains conditional on the missing geometry.'],17,RED,29)

    panel(30,1600,1740,660,'F  Conditional force routes, complete stock and retained limits','Two scalar radial-load assignments only. Equilibrium arithmetic is not a pressure or assembly qualification.')
    text(55,1700,'Per sector, positive member tension',21,INK,'bold')
    text(530,1700,'f = 0',20,TEAL,'bold');text(710,1700,'f = 1',20,BLUE,'bold')
    c0,c1=data['loadCases'];rows=[]
    for label,key in [('AD MN','AD'),('BD MN','BD'),('BC MN','BC'),('DC reference MN','DC_reference')]:
        rows.append((label,f"{c0['memberSignedTensionN'][key]/1e6:+.6f}",f"{c1['memberSignedTensionN'][key]/1e6:+.6f}"))
    rows += [('DC stress envelope MPa',f"{c0['mainMemberScreens']['DC']['additiveStressPa']/1e6:.3f}",f"{c1['mainMemberScreens']['DC']['additiveStressPa']/1e6:.3f}"),
             ('Unresolved total moment kNm',f"{c0['unresolvedModuleMomentNm']/1000:.3f}",f"{c1['unresolvedModuleMomentNm']/1000:.3f}")]
    for j,(label,a,b) in enumerate(rows):
        yy=1738+j*38
        if j%2==0:rect(50,yy-25,795,35,PALE,'none',0)
        text(60,yy,label,18);text(530,yy,a,18,RED if j>=4 else INK);text(710,yy,b,18,RED if j>=4 else INK)
    lines(55,2000,['f=0: radial hoop compression, axial transfer.',
                   'f=1: all radial + axial transfer to posts/module.',
                   'BC Euler 9.461814 MN: FAIL in both limits.',
                   'DC actual axial force is tensile; no false compression.',
                   'Known A/B, D/C moments need an actual bending path.',
                   'Film trial 68.639 > 50 MPa; button strip also FAIL.'],18,RED,31)
    mass=data['mass'];text(930,1700,'Both-cap stock ledger, tonnes',21,INK,'bold')
    entries=[('Carried corrected-I016 hull',mass['priorHullT']),('Selected retirement',0),
             ('New module: all 114 bill rows',mass['newModuleAddedT']),('Hull + selected new stock',mass['hullT']),
             ('Residual gas, once',mass['residualGasOnceT']),('Known subtotal',mass['knownSubtotalT']),
             ('Sea-level margin',mass['at'][0]['knownMarginT']),('2500 m margin',mass['at'][1]['knownMarginT'])]
    for j,(label,value) in enumerate(entries):
        yy=1738+j*38
        if j%2==0:rect(920,yy-25,825,35,PALE,'none',0)
        text(935,yy,label,18);text(1730,yy,f'{value:,.6f}',18,RED if j>=6 else INK,anchor='end')
    lines(930,2080,['Reused finite button 5.334397 t is already in old hull.',
                    'Old removed-duty stock retained as inactive contingency.',
                    'No simultaneous-installation or saving claim.',
                    'All old remaining FAIL / physical and U+C UNKNOWN.'],18,RED,31)
    text(55,2230,'Next local construction: separate tangential pin planes + dedicated short AD cartridge + priced moment collector.',19,INK,'bold')
    text(30,2288,'Scalar/vector arithmetic only · matrix order 0 · one geometry · no ancestor run or parameter sweep · see README and result.json for all parts and limits',17,MUTED)
    svg.extend(['</g>','</svg>'])
    return '\n'.join(svg)+'\n'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true')
    args=parser.parse_args()
    result=drawing(json.loads((HERE/'result.json').read_text()))
    path=HERE/'geometry.svg'
    if args.check:
        assert path.read_text()==result,'Saved SVG differs from deterministic drawing'
        print('I020 drawing reproduction PASS; drawing has no model imports or calculation calls.')
    else:path.write_text(result)


if __name__=='__main__':main()
