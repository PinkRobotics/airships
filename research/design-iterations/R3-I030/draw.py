#!/usr/bin/env python3
"""Draw the saved finite geometry; no calculator import or numerical replay."""
import html
import json
from math import cos, sin, pi, sqrt
from pathlib import Path

HERE=Path(__file__).resolve().parent
D=json.loads((HERE/'hoop.json').read_text())
B=json.loads((HERE/'baseline.json').read_text())
S=json.loads((HERE/'sources.json').read_text())['design']
G=B['inherited']['geometry']
svg=['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1430" viewBox="0 0 1600 1430">',
     '<rect width="1600" height="1430" fill="white"/>',
     '<style>text{font-family:DejaVu Sans,sans-serif;fill:#182a3a} .small{font-size:13px} .body{font-size:16px}</style>']
def text(x,y,value,size=16,color='#182a3a'):
    svg.append(f'<text x="{x:.3f}" y="{y:.3f}" font-size="{size}" fill="{color}">{html.escape(str(value))}</text>')
def line(a,b,color='#355b72',width=1,dash=''):
    svg.append(f'<line x1="{a[0]:.3f}" y1="{a[1]:.3f}" x2="{b[0]:.3f}" y2="{b[1]:.3f}" stroke="{color}" stroke-width="{width:.3f}"'+(f' stroke-dasharray="{dash}"' if dash else '')+'/>')
def poly(points,color,width=1,fill='none'):
    svg.append('<polyline points="'+' '.join(f'{x:.3f},{y:.3f}' for x,y in points)+f'" stroke="{color}" stroke-width="{width:.3f}" fill="{fill}"/>')
def circle(x,y,r,color='#355b72',width=1,fill='none'):
    svg.append(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{r:.3f}" fill="{fill}" stroke="{color}" stroke-width="{width:.3f}"/>')
def rect(x,y,w,h,fill='#eef2f5',stroke='#355b72'):
    svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}"/>')
def add(a,b):return tuple(x+y for x,y in zip(a,b))
def mul(a,t):return tuple(x*t for x in a)
def sub(a,b):return tuple(x-y for x,y in zip(a,b))
def dot(a,b):return sum(x*y for x,y in zip(a,b))
def norm(a):return sqrt(dot(a,a))
def unit(a):return mul(a,1/norm(a))

text(35,40,'R3-I030 | one frozen exterior transfer hoop',27)
text(35,70,'29 m centreline radius, z = 0; 76 m hull; four full bag envelopes. Unloaded geometry, not a fit or equilibrium certificate.',16)
text(35,97,'Teal: finite hoop   red: paid receiver members   gold: ropes   blue: guide guards   grey: retained frames',15)

def view(x0,title,projection):
    scale=5.6; origin=(x0+250,370)
    def project(p):
        x,y=projection(p)
        return (origin[0]+scale*x,origin[1]-scale*y)
    text(x0+15,137,title,19)
    for bag,c in enumerate(G['bag_centres']):
        x,y=project(c);circle(x,y,scale*G['bag_radius_m'],'#b7c7d4',.8)
        text(x-9,y+5,f'B{bag}',13,'#788e9d')
    circle(*origin,scale*G['radius_m'],'#8197a8',1)
    for o in D['objects']:
        role=o['role']
        if role=='frame':line(project(o['a']),project(o['b']),'#c5cdd2',.65)
        elif role=='hoop_sector':line(project(o['a']),project(o['b']),'#168b8a',max(1.4,scale*.5))
        elif role=='receiver_members':line(project(o['a']),project(o['b']),'#bb4f49',max(1.4,scale*.3))
        elif role in ('rope','tail'):line(project(o['a']),project(o['b']),'#b78016',.9)
        elif role=='actuator':line(project(o['a']),project(o['b']),'#493a8f',2)
    for root in D['roots']:
        p=project(root['ring_point']);circle(*p,3,'#ad3f3b',1,'white');text(p[0]+4,p[1]-4,'R'+str(root['id']),11)
        p=project(root['receiver']);rect(p[0]-2,p[1]-2,4,4,'#bb4f49','#bb4f49')
    for route in D['routes']:
        for j,be in enumerate(route['bends']):
            u=be['u_in'];n=unit(sub(be['centre'],be['entry']))
            points=[project(add(be['centre'],mul(add(mul(u,cos(k*pi/24)),mul(n,sin(k*pi/24))),S['guard_radius_m']))) for k in range(49)]
            poly(points,'#246ba1',1.1)
            for name in ('entry','exit'):circle(*project(be[name]),1.6,'#c6453d',.5,'#c6453d')
        p=project(route['bends'][0]['intersection']);text(p[0]+6,p[1]+13,str(route['host']),12)
    line(project((-35,0,0)),project((-25,0,0)),'#182a3a',2)
    text(x0+45,622,'10 m scale; widths shown where resolved',13)
    return project

view(15,'Plan: x / y',lambda p:(p[0],p[1]))
view(545,'Elevation: x / z',lambda p:(p[0],p[2]))
view(1075,'Axonometric: actual 3D routes',lambda p:((p[0]-p[1])/sqrt(2),(-p[0]-p[1]+2*p[2])/sqrt(6)))
line((30,652),(1570,652),'#bdc9d1',1)
text(35,683,'Finite construction details — exact dimensions below; detail panels have independent scales',21)

# The actual first guide plane and tangent directions, read from the saved result.
be=D['routes'][0]['bends'][0]
u=be['u_in'];n=unit(sub(be['centre'],be['entry']));origin=(225,925);sc=130
def local(p):
    q=sub(p,be['centre']);return(origin[0]+sc*dot(q,u),origin[1]-sc*dot(q,n))
text(35,722,'Host 9: lower guide plane',18)
circle(*origin,.6*sc,'#246ba1',2)
circle(*origin,.45*sc,'#168b8a',2)
circle(*origin,.03*sc,'#182a3a',2,'#b7c7d4')
poly([local(p) for p in be['points']],'#b78016',3)
line(local(add(be['entry'],mul(be['u_in'],-1.0))),local(be['entry']),'#b78016',3)
line(local(be['exit']),local(add(be['exit'],mul(be['u_out'],1.0))),'#b78016',3)
line(local(be['intersection']),origin,'#bb4f49',8)
for label in ('entry','exit','intersection'):
    p=local(be[label]);circle(*p,4,'#c6453d',1,'white');text(p[0]+5,p[1]-7,label,13)
text(35,1084,'450 mm pitch radius; 600 mm guard',15)
text(35,1106,'60 mm axle, 120 mm bearing span',15)
text(35,1128,'26 mm groove; 18 mm rope + paid tails',15)
text(35,1150,'150 × 150 × 6 mm arm to hoop',15)

text(435,722,'Each of eight sector splices',18)
rect(455,790,310,190,'#e5f4f3','#168b8a')
rect(475,810,270,150,'white','#168b8a')
line((610,790),(610,980),'#bc4e47',2,'5 4')
rect(445,775,330,15,'#b8c1c8','#405768');rect(445,980,330,15,'#b8c1c8','#405768')
for y in (787,983):
    for x in (480,560,660,740):circle(x,y,5,'#182a3a',1,'white')
text(440,1034,'Four steel covers: 800 × 350 × 20 mm',14)
text(440,1056,'16 M24 shanks, 560 mm + paid nuts',14)
text(440,1078,'500 × 500 × 12 mm aluminium RHS',14)
text(440,1100,'45° curved sector; bolt group r = 210 mm',14)
text(440,1122,'Half-sector force/couple enters each splice',14)
text(440,1144,'Prying, slip, fatigue and plate flexure UNKNOWN',14)

text(835,722,'Receiver member and end connections',18)
rect(865,850,275,68,'#faeae8','#bb4f49')
rect(850,818,15,132,'#b8c1c8','#405768');rect(1140,818,15,132,'#b8c1c8','#405768')
for x in (858,1148):
    for y in (831,938):circle(x,y,5,'#182a3a',1,'white')
poly([(865,845),(915,850),(865,820)],'#405768',1,'#d7dfe5')
poly([(1090,918),(1140,945),(1140,920)],'#405768',1,'#d7dfe5')
circle(1002,884,11,'#182a3a',2,'#b7c7d4')
text(840,1008,'300 × 300 × 10 mm aluminium RHS',14)
text(840,1030,'Two 400 × 400 × 25 mm end flanges',14)
text(840,1052,'4 gussets + 8 M24 bolts at each end',14)
text(840,1074,'60 × 250 mm steel axial pin; double shear',14)
text(840,1096,'Bolted flanges must also transmit full moment',14)
text(840,1118,'Existing rack receiver → paid root → curtain',14)
text(840,1140,'Eight mappings and exact xyz are in hoop.json',14)

text(1230,722,'Direct cradle connection',17)
poly([(1245,940),(1300,902),(1355,888),(1410,902),(1465,940)],'#8197a8',3)
rect(1315,858,80,30,'#d0dde5','#405768')
circle(1355,848,8,'#182a3a',2,'white')
line((1355,840),(1440,785),'#b78016',3)
poly([(1355,900),(1300,913),(1255,940)],'#168b8a',5)
poly([(1355,900),(1410,913),(1455,940)],'#168b8a',5)
text(1225,1008,'400 × 400 × 20 mm saddle',14)
text(1225,1030,'500 × 500 × 10 mm contact pad',14)
text(1225,1052,'Two 1 m × 250 × 6 mm ribbons',14)
text(1225,1074,'Bond mass +20%; paid clevis/pin',14)
text(1225,1096,'Old socket reused; yoke removed',14)
text(1225,1118,'Local contact/peel remains UNKNOWN',14)
text(1225,1140,'No retirement of old liners/cuffs',14)

line((30,1190),(1570,1190),'#bdc9d1',1)
text(35,1225,'Interpretation',19)
text(35,1254,'Curves use saved finite tangencies; small red points mark entry/exit. Guide guards are drawn in their actual 3D planes.',16)
text(35,1280,'Full bag circles are projected envelopes. Apparent separation in one panel is not a 3D clearance result; use saved witnesses.',16)
text(35,1306,'RHS, splices, roots, hardware, access and retained duties are paid once. Conservative capsule bounds do not certify joints.',16)
text(35,1332,'No loaded global shape, coupled ring/curtain compatibility, contact solution or physical float is established by this drawing.',16)
text(35,1370,'Source: hoop.json and sources.json. Reproduce with: python3 research/design-iterations/R3-I030/draw.py',14)
svg.append('</svg>')
(HERE/'geometry.svg').write_text('\n'.join(svg)+'\n')
print(json.dumps({'output':'research/design-iterations/R3-I030/geometry.svg','input':'research/design-iterations/R3-I030/hoop.json','geometry_recalculated':False}))
