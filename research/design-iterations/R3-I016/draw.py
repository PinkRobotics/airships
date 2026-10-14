#!/usr/bin/env python3
"""One dimensioned I016 attempt, including its explicit geometry failures."""
import argparse
from html import escape
import json
import math
from pathlib import Path

HERE=Path(__file__).resolve().parent


def render():
    r=json.loads((HERE/'result.json').read_text())
    g=r['geometry'];m=r['mass'];p=r['pressure'];f=r['filmSupport'];d=r['polarClosure']
    stations=g['oneCapMainStations'];hub=g['polarHub']
    out=['<svg xmlns="http://www.w3.org/2000/svg" width="1800" height="2020" viewBox="0 0 1800 2020">',
         '<title>I016 finite cap-to-cap construction: geometry and strength FAIL</title>',
         '<desc>Equal-scale capsule and cap plots, finite polar dome and hub, explicit single-lug and meridian connections, failed film-support fit and complete conservative mass bill.</desc>',
         '<style>text{font-family:DejaVu Sans,Arial,sans-serif;fill:#e8edf3;font-size:19px}.title{font-size:32px;font-weight:bold}.sub{font-size:25px;font-weight:bold}.small{font-size:17px}.bad{fill:#ff9d8e}.muted{fill:#b6c4d1}.blue{fill:#7bd6ee}.green{fill:#9ad6a8}</style>',
         '<rect width="1800" height="2020" fill="#111b27"/>']
    def text(x,y,s,cls='',anchor='start'):
        out.append(f'<text x="{x:.3f}" y="{y:.3f}" class="{cls}" text-anchor="{anchor}">{escape(str(s))}</text>')
    def line(x1,y1,x2,y2,c='#c5d3df',w=2,dash=''):
        out.append(f'<line x1="{x1:.3f}" y1="{y1:.3f}" x2="{x2:.3f}" y2="{y2:.3f}" stroke="{c}" stroke-width="{w}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
    def rect(x,y,w,h,fill,stroke='none'):
        out.append(f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" fill="{fill}" stroke="{stroke}"/>')
    def circle(x,y,rad,fill='none',stroke='#c5d3df',w=2):
        out.append(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{rad:.3f}" fill="{fill}" stroke="{stroke}" stroke-width="{w}"/>')
    def poly(points,c,w=2):
        out.append('<polyline points="'+' '.join(f'{x:.3f},{y:.3f}' for x,y in points)+f'" fill="none" stroke="{c}" stroke-width="{w}"/>')
    def panel(x,y,w,h,title):
        rect(x,y,w,h,'#192736','#344a5c');text(x+20,y+35,title,'sub')
    def dim(x1,x2,y,s):
        line(x1,y,x2,y);line(x1,y-5,x1,y+5);line(x2,y-5,x2,y+5);text((x1+x2)/2,y-9,s,'small','middle')
    text(24,44,'I016 · finite cap-to-cap rings, polar closure and a failed complete bill','title')
    text(24,80,'Geometry and nominal strength FAIL · no inherited cap/wall saving selected · pressure capacity and physical confidence UNKNOWN','bad')

    panel(24,106,1752,480,'A  Entire 80 × 160 m capsule · equal x/r scale')
    ox,oy,s=455,340,4.5
    xy=lambda x,y:(ox+x*s,oy-y*s)
    outline=[]
    for sign in (1,-1):
        right=[(40+40*math.sin(a),sign*40*math.cos(a)) for a in [i*math.pi/180 for i in range(91)]]
        left=[(-x,y) for x,y in right]
        poly([xy(*v) for v in left[::-1]+[(-40,sign*40),(40,sign*40)]+right],'#dbe6ef',3)
    for x in range(-40,41,2):
        line(*xy(x,-39.845),*xy(x,39.845),'#426d82',1)
    for radius in (39.845-.445,35.229615384615386-.445):
        for sign in (-1,1):line(*xy(-40,sign*radius),*xy(40,sign*radius),'#efb66f',2)
    for sign in (-1,1):
        for row in stations[1:]:
            x=sign*row['xM'];ro=row['outerRadiusM'];ri=row['innerRadiusM']
            line(*xy(x,-ro),*xy(x,ro),'#7bd6ee',2)
            for v in (-ri,ri):circle(*xy(x,v),2,'#9ad6a8','#9ad6a8')
        for side in (-1,1):
            pts=[xy(sign*a['xM'],side*(a['outerRadiusM']-.445)) for a in stations]
            pts.append(xy(sign*hub['xM'],side*hub['outerRadiusM']))
            poly(pts,'#efb66f',2)
        line(*xy(sign*hub['xM'],-3.3),*xy(sign*hub['xM'],3.3),'#efb66f',5)
    line(*xy(-82,0),*xy(82,0),'#718697',1,'5 5')
    dim(*[xy(v,0)[0] for v in (-80,80)],555,'160 m overall; 80 m barrel, two R40 caps')
    text(935,184,'Inherited barrel: 41 planes, x=−40+2k, k=0…40')
    text(935,218,'111 ring nodes; cap node j aligns with barrel node 3j')
    text(935,252,'Each cap: 18 frames at φ=4°,8°,…,72°; 37 nodes')
    text(935,286,'37 outer + 37 inner meridians; both endpoints priced')
    text(935,320,'Finite 12 mm steel polar dome; hub radius 3 m')
    text(935,354,'New outer cap rings also carry the pressure-hoop duty')
    text(935,388,'Fine-hoop count excludes every main ring: counted once')
    text(935,430,f'Hull {m["hullT"]:.3f} t + gas {m["residualGasOnceT"]:.3f} t','bad')
    text(935,464,f'Sea-level / 2500 m: {m["at"][0]["knownMarginT"]:.3f} / {m["at"][1]["knownMarginT"]:.3f} t','bad')
    text(935,514,'This selected layout cannot be assembled as dimensioned.','bad')
    text(935,546,'Its explicit fit failures prevent a replacement credit.','bad')

    panel(24,606,860,480,'B  Right cap and taper · equal x/r scale')
    cx,cy,sc=90,1007,7.6
    cp=lambda x,y:(cx+(x-40)*sc,cy-y*sc)
    angles=[i*math.pi/180 for i in range(91)]
    poly([cp(40+40*math.sin(a),40*math.cos(a)) for a in angles],'#e0e8f0',3)
    for row in stations:
        line(*cp(row['xM'],0),*cp(row['xM'],row['outerRadiusM']),'#426d82',1)
    for family,color in [('outer','#7bd6ee'),('inner','#9ad6a8')]:
        poly([cp(row['xM'],row[family+'RadiusM']) for row in stations],color,3)
        for row in stations:circle(*cp(row['xM'],row[family+'RadiusM']),2,color,color)
    poly([cp(40+40*math.sin(a),40*math.cos(a)) for a in angles[72:]],'#efb66f',7)
    for layer in ('outer','inner'):
        pts=r['meridians']['paths'][layer]['oneEndSegments']
        poly([cp(*pts[0]['fromM'])]+[cp(*v['toM']) for v in pts],'#efb66f',2)
    circle(*cp(hub['xM'],3.),4,'#efb66f','#efb66f')
    text(455,688,'Surface: x=40+40 sin φ, r=40 cos φ','small')
    text(455,723,'Frame inset prices ±360 mm axial envelope','small')
    text(455,757,'+170 mm radial box; 10 mm nominal reserve','small')
    text(455,791,'Inner/outer radius ratio is fixed at 0.88416','small')
    text(455,825,'φ=72°: surface r=12.360680 m','small')
    text(455,859,f'Outer/inner frame r={stations[-1]["outerRadiusM"]:.6f} /','small')
    text(455,889,f'{stations[-1]["innerRadiusM"]:.6f} m; chords 1.863 / 1.648 m','small')
    text(455,926,'Last ring to outer hub: 7.414 m node distance','small')
    text(455,960,'Final chord axial direction cosine: 0.1814','small bad')
    text(50,1058,'19 cap-to-hub meridian segments/end; full station table and actual end cuts in result.json','small')

    panel(904,606,872,480,'C  A finite polar construction · details schematic')
    # Dimensioned half-meridian detail of the dome/hub, not an inflated zero-radius ring.
    polar_point=lambda x,rad:(958+(x-stations[-1]['xM'])*132,960-rad*19.5)
    poly([polar_point(40+40*math.sin(math.radians(a)),40*math.cos(math.radians(a))) for a in range(72,91)],'#efb66f',7)
    for layer in ('outer','inner'):
        last=r['meridians']['paths'][layer]['oneEndSegments'][-1]
        line(*polar_point(*last['fromM']),*polar_point(*last['toM']),'#7bd6ee',3)
    hx,hy=polar_point(hub['xM'],3.)
    rect(hx-33,hy-7,66,14,'#8a9da9','#dbe6ef')
    rect(hx-27,hy-3,54,6,'#192736')
    line(hx,hy,*polar_point(hub['surfaceXAt3mM'],3.),'#efb66f',3)
    root_x,root_y=polar_point(stations[-1]['xM'],stations[-1]['surfaceRadiusM'])
    line(root_x,root_y,root_x,polar_point(stations[-1]['xM'],stations[-1]['outerRadiusM']+.165)[1],'#ff9d8e',3,'3 3')
    text(950,686,'12 mm spherical plate','small')
    text(1245,714,'37 gores + finite central button','small')
    text(1245,748,'R3 button boundary at x=79.887341 m','small')
    text(1245,782,'Hub x=79.387341 m; 0.5 m inset','small')
    text(1245,816,'Steel box: 600 radial × 500 axial × 12','small')
    text(1245,850,'Outer/inner pins: r=3.25 / 2.75 m','small')
    text(1245,884,'37 Ø40×4, 500-long dome-to-hub posts','small')
    text(1245,918,'200×12 root flange; 8 M16 per sector','small')
    text(948,999,f'Dome membrane {d["membraneCompressionPa"]/1e6:.1f} MPa; local plate strip {d["oneWayPlateBendingPa"]/1e6:.0f} MPa: FAIL','small bad')
    text(948,1031,f'Hub post {d["domeHubPostScreen"]["directStressPa"]/1e6:.0f} MPa; steel proxy 355 MPa: FAIL','small bad')
    text(948,1063,f'200 mm root flange leaves {d["rootFlangeToFrameCuffRadialGapM"]:.3f} m radial gap: no connecting path','small bad')

    panel(24,1106,860,438,'D  Real endpoints and transitions · dimensions in mm')
    text(48,1180,'Cap X-web: 300×2.5 carbon, j→j±1; planes x=±200','small')
    text(48,1214,'One corrected outboard lug |x|=214…230; neck ends188','small')
    text(48,1248,'26 mm neck gap; 222 mm force lever; eccentric end demands','small')
    text(48,1282,'550 setback; one 592×120×16 lug; Ø320×8 end plate','small')
    text(48,1316,'294×3×300 insert; 296 bond + 4 relief; Ø40×120 pin','small')
    line(48,1336,856,1336,'#506477')
    text(48,1373,'Meridian: 250×12; root 445 inboard; pin offsets ±150','small')
    text(48,1407,'250 setback; 225×6×200 insert; 194 bond + 6 relief','small')
    text(48,1441,'Two 302×180×20 lugs; Ø80×150 pin; Ø270×8 plate','small')
    text(48,1475,'330/314×400 cuff, eight M16; 500×650×40 two-pin root','small')
    text(48,1513,'Unnotched cuff intersects the integral pad at |x|=160 mm: FAIL','small bad')

    panel(904,1106,872,438,'E  Film-support fit FAIL · radial section')
    # The actual overlapping normal datums are drawn rather than visually repaired.
    x0,y0,scale=1070,1220,1.25
    line(950,y0,1185,y0,'#e0e8f0',2)
    circle(x0,y0+89*scale,83*scale,'#285b72','#7bd6ee',3)
    circle(x0,y0+21.5*scale,21.5*scale,'#a85750','#ff9d8e',3)
    text(1220,1190,'Skin datum r=R; bar 43×1 at R−21.5 mm','small')
    text(1220,1224,'Fine hoop 166×6 at R−89 mm','small')
    text(1220,1258,'Ordinary hoop overlap: 37 mm','small bad')
    text(1220,1292,'178 OD splice cuff overlap: 43 mm','small bad')
    text(1220,1337,'666 bars; cap pitch 0.8° = 558.505 mm','small')
    text(1220,1371,'Main supports: 60×3 posts, minimum80 mm','small')
    text(1220,1405,'888 positions have insufficient available length','small bad')
    text(948,1463,'Profiled 80 mm foot packers and full hardware are priced; no hidden spacer or deletion.','small')
    text(948,1504,'Next layout must separate these normal datums and close the meridian/end-block force path.','small bad')

    panel(24,1564,1752,404,'F  Full known bill and limiting demands · a negative result, not a pressure rating')
    entries=[('Retained I014 other hull',m['retainedOtherHullT']),
             ('Carried corrected I014 frame + attachments',sum(m['carriedI014NewBillT'].values())),
             ('Added cap frames + actual ends',sum(r['capFrames']['massT'].values())),
             ('Added outer/inner meridians + roots',sum(r['meridians']['massT'].values())),
             ('Added film support + packing',sum(f['massT'].values())),
             ('Finite polar closures',sum(d['massT'].values())),
             ('Additional erection attachments',r['erectionAttachment']['additionalMassT'])]
    for k,(label,value) in enumerate(entries):
        y=1638+k*36;text(48,y,label,'small');text(824,y,f'{value:.6f} t','small','end')
    text(934,1638,f'One cap thrust {p["oneCapAxialResultantN"]/1e6:.3f} MN; outer path {p["barrelMeridianForceN"]/1e6:.3f} MN/member','small')
    text(934,1676,'Meridian 1841 MPa > carbon proxy1450; pin/insert/weld demands FAIL','small bad')
    text(934,1714,'Fine hoop 2.710 MN vs pin-Euler0.280 MN; local film clips FAIL','small bad')
    text(934,1752,'I014 erection flange372.4 MPa >355 retained; no wind-load dilution','small bad')
    text(934,1790,f'Allowance BEFORE frame/polar/meridians: {m["maximumNewFrameT"]:.3f} t','small bad')
    text(934,1828,f'Actual frame/polar/meridians: {m["frameAndPolarAndMeridianT"]:.3f} t','small bad')
    text(934,1870,'Only scalar equilibrium and partial positive elastic energy; matrix order0','small')
    text(934,1908,'Prestress/follower tangent, cap coupling, U+C and physical float UNKNOWN','small bad')
    text(48,1940,'All original references and failures carry. Shared new rings counted once. Retained legacy rows provide no credited foundation or pressure capacity.','small muted')
    text(24,2000,'Dimensioned failed construction attempt. Panels C–E schematic; A/B equal scale. README/result.json give exact coordinates, sections, joint quantities and limits.','small muted')
    out.append('</svg>')
    return '\n'.join(out)+'\n'


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');a=p.parse_args()
    svg=render();path=HERE/'geometry.svg'
    if a.check:
        assert path.read_text()==svg
        print('I016 SVG matches the frozen construction, explicit clashes and full bill.')
    else:
        path.write_text(svg)


if __name__=='__main__':
    main()
