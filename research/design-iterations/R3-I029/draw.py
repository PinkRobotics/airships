#!/usr/bin/env python3
"""Draw the saved cassette result, without importing or rerunning its calculator."""
import hashlib
import html
import json
import math
import sys
from pathlib import Path
U=Path(__file__).resolve().parent

def main():
    assert sys.argv[1:]==['--write']
    raw=(U/'cassette.json').read_bytes();d=json.loads(raw);g=d['geometry'];m=d['mass'];s=d['summary']
    out=['<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="1780" viewBox="0 0 1400 1780">',
         '<rect width="1400" height="1780" fill="#f7f9fb"/>',
         '<style>text{font-family:DejaVu Sans,sans-serif;fill:#172b3b;font-size:17px}.h{font-size:27px;font-weight:bold}.sub{font-size:20px;font-weight:bold}.small{font-size:14px}.fail{fill:#a51f32;font-weight:bold}.note{fill:#526778}</style>']
    def text(x,y,t,cls=''):out.append(f'<text x="{x:.2f}" y="{y:.2f}" class="{cls}">{html.escape(str(t))}</text>')
    def rect(x,y,w,h,fill,stroke='#536775',sw=1):out.append(f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def line(a,b,color='#314d63',sw=1,dash=''):
        out.append(f'<line x1="{a[0]:.3f}" y1="{a[1]:.3f}" x2="{b[0]:.3f}" y2="{b[1]:.3f}" stroke="{color}" stroke-width="{sw}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
    def circle(x,y,r,fill,stroke='#314d63',sw=1):out.append(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{r:.3f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def poly(points,fill,stroke='#314d63',sw=1):out.append('<polygon points="'+' '.join(f'{x:.3f},{y:.3f}' for x,y in points)+f'" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
    def panel(x,y,w,h,title):rect(x,y,w,h,'white','#c9d5de');text(x+20,y+33,title,'sub')
    text(38,48,'R3-I029 | receiver-integrated split cassette','h')
    text(38,82,'FAIL: +144.131 t hull mass; strength and assembly fail. Installed structure / float UNKNOWN.','fail')
    text(38,108,'One frozen design. Coordinates are metres. Finite stock is shown; projections do not certify clearance.','note')
    panel(32,130,570,1070,'1  Full module in X-R projection; equal scale')
    # Equal physical scale for both axes, with the complete radial span on paper.
    def project(p):return (92+(p[0]-76.6)*86,190+(13.0-p[1])*86)
    for r in range(3,14):
        a=project([76.7,r,0]);b=project([80.6,r,0]);line(a,b,'#e4eaf0');text(56,a[1]+5,r,'small')
    for x in (77,78,79,80):
        a=project([x,2.4,0]);b=project([x,13,0]);line(a,b,'#e4eaf0');text(a[0]-7,a[1]+25,x,'small')
    text(80,1146,'X (axial) →     R vertical ↑     T into / out of page','small')
    for ch in g['cheeks']:
        p=ch['centreXRTm'];e,t,n=ch['axes'];L,W,H=ch['dimensionsM']
        corners=[[p[i]+a*L/2*e[i]+b*H/2*n[i] for i in range(3)] for a,b in [(-1,-1),(1,-1),(1,1),(-1,1)]]
        poly([project(x) for x in corners],'#d98b32','#93540e',1.4)
    for member in g['members']:
        a,b=member['firstXRTm'],member['lastXRTm'];dx=b[0]-a[0];dy=b[1]-a[1];length=math.hypot(dx,dy)
        nx,ny=(-dy/length,dx/length) if length else (1,0);w=member['sizeM']/2
        points=[[p[0]+sgn*w*nx,p[1]+sgn*w*ny,0] for p,sgn in [(a,1),(b,1),(b,-1),(a,-1)]]
        color='#8dbbc7' if 'root' in member['name'] else '#bfced5'
        poly([project(p) for p in points],color,'#506f80',.8)
    for c in g['receiverClamps']:
        x,y=project(c['centreXRTm']);rect(x-.22*86,y-.25*86,.44*86,.5*86,'#8cbdb5','#226c66',1.6);circle(x,y,.164*86,'#edf2f6');text(x+29,y+6,c['name']+' cuff / clamp','small')
    for name in ('D','C'):
        x,y=project(g['ringNodes'][name]);size=.4 if name=='D' else .2
        rect(x-size/2*86,y-size/2*86,size*86,size*86,'#4f6577');text(x+28,y-13,name+' ring','small')
    ends={}
    for c in d['clearance']['pinAccess']:
        member,node=c['pin'].split('-');p=[(a+b)/2 for a,b in zip(*c['occupiedEndsXRTm'])];ends.setdefault(member,[]).append(p)
        a,b=[project(q) for q in c['insertionSweptEndpointsXRTm']];line(a,b,'#ab273b' if c['status']=='FAIL' else '#805ba6',2,'4 3');x,y=project(p);circle(x,y,4,'#ab273b' if c['status']=='FAIL' else '#805ba6')
    for member,ps in ends.items():
        if len(ps)==2:line(project(ps[0]),project(ps[1]),'#263a49',4 if member=='AD' else 6)
    text(369,365,'8 retained pins','small');text(369,389,'Dashed: insertion','small');text(369,413,'envelopes only','small')
    text(369,510,'Inner / outer','small');text(369,534,'20 mm cheeks','small');text(369,558,'1.20 m T width','small');text(369,582,'0.80 m centres','small')
    text(369,645,'2 spacers at each','small');text(369,669,'of 4 stations','small');text(369,693,'T = ±0.42 m','small')
    text(66,1178,'Unchanged AD-A pin / BD carbon obstruction: FAIL.','fail')
    panel(626,130,742,530,'2  A/B split clamp; section normal to T')
    cx,cy,scale=960,390,570
    rect(cx-.22*scale,cy-.25*scale,.44*scale,.5*scale,'#a6cbc3','#266d65',1.5)
    circle(cx,cy,.166*scale,'#d4a32c','#8c6c1b');circle(cx,cy,.164*scale,'#64798a','#314d63');circle(cx,cy,.148*scale,'white','#314d63')
    line((cx,cy-.25*scale),(cx,cy+.25*scale),'#172b3b',1.5,'6 4')
    for r in (-.22,.22):
        line((cx-.26*scale,cy-r*scale),(cx+.26*scale,cy-r*scale),'#a51f32',7)
    line((cx-.22*scale-15,cy),(cx-.22*scale-85,cy),'#266d65',3);text(674,cy-16,'← −X','small')
    line((cx+.22*scale+15,cy),(cx+.22*scale+85,cy),'#266d65',3);text(1160,cy-16,'+X →','small')
    text(650,195,'Two 220 × 500 × 360 mm half blanks; open ±X approach.','small')
    text(650,222,'Bore 332; cuff OD / ID 328 / 296; paid liner 2 mm.','small')
    text(650,566,'T lengths: clamp 360 mm, cuff 400 mm; 20 mm each end.','small')
    text(650,593,'M30 × 520 ties: 504 grip + 46 nut / washer / projection = 550 mm.','small')
    text(650,622,'FAIL: ties 30 mm short. Clamp bridge M24 also too short.','fail')
    panel(626,684,742,516,'3  Continuous AD plate; unrolled pin plane')
    ad=g['ad'];L=ad['blankLengthM'];scale=530;ax,ay=718,833
    rect(ax,ay,L*scale,.28*scale,'#e3ad65','#93540e',2)
    for distance in (.14,L-.14):circle(ax+distance*scale,ay+.14*scale,.051*scale,'white','#93540e',2)
    text(650,756,'Full rectangular blank: 1003.760 × 280 × 80 mm.','small')
    text(650,785,'Bores 102 mm; retained pins 100 mm; no zero-area shoulder.','small')
    text(650,1032,'Net width 178 mm; end ligament 89 mm.','small')
    text(650,1062,'Inherited AD tension: 173.033 / 145.525 MPa nominal net stress.','small')
    text(650,1092,'Positive plate section does not clear the retained AD-A pin.','small')
    text(650,1130,'FAIL at AD-A insertion; other complete sweeps UNKNOWN.','fail')
    text(650,1165,'Pin/tool finite envelopes are in cassette.json; no access certificate.','small')
    panel(32,1224,1336,252,'4  Paid known mass and unchanged displacement')
    columns=[('Previous hull',m['previousHullT']),('Selected hull',m['knownHullT']),('Gas, once',m['residualGasOnceT']),('Hull + gas',m['knownSubtotalT'])]
    for i,(label,value) in enumerate(columns):text(58+i*325,1294,label,'small');text(58+i*325,1327,f'{value:,.3f} t','h')
    text(58,1370,'New stock 574.797 t; selected removal 430.666 t; qualified retirement 0.000 t.','small')
    text(58,1401,'Fixed-volume margins: −5,299.339 t at 0 m; −5,478.689 t at 2500 m; each still minus U+C.','fail')
    text(58,1432,'No-retirement bound: hull + gas 6,549.358 t. Displacement unchanged; all-up equipment / payload UNKNOWN.','small')
    panel(32,1500,1336,236,'5  What this candidate establishes')
    text(58,1567,'Full vector wrenches and paid local-stock gravity are carried; force / moment closure is bookkeeping.','small')
    text(58,1600,'49.424 GPa maximum conditional section demand; 11.262 GPa receiver-tie tension: nominal FAIL.','fail')
    text(58,1633,'Ring contact, rotational stiffness, loaded shape, neighbor solids and whole-hull stability remain UNKNOWN.','small')
    text(58,1666,'Next untested change: triangulated route to two separated frame stations, retaining full pressure and gravity duties.','small')
    text(58,1704,'Figure is a saved-result projection, not a manufactured layout or independent numerical verification.','small')
    text(38,1760,'Saved result SHA256 '+hashlib.sha256(raw).hexdigest(),'small')
    out.append('</svg>');(U/'geometry.svg').write_text('\n'.join(out)+'\n');print('DRAW_COMPLETED saved-result only; '+hashlib.sha256((U/'geometry.svg').read_bytes()).hexdigest(),flush=True)

if __name__=='__main__':main()
