#!/usr/bin/env python3
"""Draw the frozen construction from saved output; no scientific rerun."""
import hashlib
import json
import math
from pathlib import Path
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'svg.hashsalt':'radial-yoke-fixed-1'})
src=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
j=json.loads(src.read_text())
b=json.loads((Path(__file__).parent/'baseline.json').read_text())
geo=b['inherited']['geometry'];rb=geo['bag_radius_m'];hull=geo['radius_m']
colours={9:'#be2945',10:'#dc7b27',11:'#95722d',12:'#5668c4',16:'#269d99',21:'#286ccc',22:'#a8479a',23:'#4c8851'}
blue='#29688f';teal='#148582';red='#b82539';grey='#8a959d'

def line3(ax,points,**kw):
    a=np.asarray(points);ax.plot(a[:,0],a[:,1],a[:,2],**kw)
def bag3(ax,centre,radius,alpha=.22):
    theta=np.linspace(0,2*np.pi,60)
    for phi in [-np.pi/3,-np.pi/6,0,np.pi/6,np.pi/3]:
        p=np.array([centre[0]+radius*np.cos(phi)*np.cos(theta),centre[1]+radius*np.cos(phi)*np.sin(theta),np.full_like(theta,centre[2]+radius*np.sin(phi))]).T
        line3(ax,p,color=grey,alpha=alpha,lw=.65)
    for phi in [0,np.pi/2]:
        p=np.array([centre[0]+radius*np.cos(theta)*np.cos(phi),centre[1]+radius*np.cos(theta)*np.sin(phi),centre[2]+radius*np.sin(theta)]).T
        line3(ax,p,color=grey,alpha=alpha,lw=.65)
def route3(ax,row,lw=1.6):
    for a,bp in row['segments']:line3(ax,[a,bp],color=colours[row['host']],lw=lw)
    for bend in row['bends']:
        line3(ax,bend['points'],color=colours[row['host']],lw=lw)
        c=np.array(bend['centre']);u=np.array(bend['u_in']);v=np.cross(np.array(bend['axis']),u)
        theta=np.linspace(0,2*np.pi,64)
        points=c+.60*(np.outer(np.cos(theta),u)+np.outer(np.sin(theta),v))
        line3(ax,points,color=grey,lw=.65)
def save(fig,name):
    fig.savefig(out/(name+'.svg'),metadata={'Date':None},facecolor='white')
    svg=out/(name+'.svg')
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
    fig.savefig(out/(name+'.png'),dpi=150,facecolor='white')
    plt.close(fig)

fig=plt.figure(figsize=(17,10),layout='constrained')
ax=fig.add_subplot(1,2,1,projection='3d');side=fig.add_subplot(1,2,2)
for c in geo['bag_centres']:bag3(ax,c,rb)
for row in j['routes']:
    route3(ax,row);tip=row['eye'];ax.text(*tip,str(row['host']),color=colours[row['host']],fontsize=9)
for obj in j['objects']:
    if obj['role']=='module':line3(ax,[obj['a'],obj['b']],color=teal,lw=.75)
    if obj['role']=='frame':line3(ax,[obj['a'],obj['b']],color=blue,lw=.45,alpha=.6)
ax.set(xlabel='x (m)',ylabel='y (m)',zlabel='z (m)',xlim=(-40,40),ylim=(-40,40),zlim=(-30,40))
ax.set_box_aspect((1,1,.875));ax.view_init(elev=22,azim=-38)
ax.set_title('Full three-dimensional route through retained racks',pad=18)
for c in geo['bag_centres']:
    side.add_patch(plt.Circle((c[1],c[2]),rb,fill=False,color=grey,lw=1))
side.add_patch(plt.Circle((0,0),hull,fill=False,color=blue,ls='--',lw=1))
for row in j['routes']:
    for a,bp in row['segments']:
        side.plot([a[1],bp[1]],[a[2],bp[2]],color=colours[row['host']],lw=1.3)
    for bend in row['bends']:
        a=np.asarray(bend['points']);side.plot(a[:,1],a[:,2],color=colours[row['host']],lw=1.3)
    side.scatter(row['eye'][1],row['eye'][2],s=14,color=colours[row['host']])
side.set(xlabel='y (m)',ylabel='z (m)',xlim=(-41,41),ylim=(-40,41),aspect='equal')
side.grid(alpha=.18);side.set_title('Side projection; clearance is evaluated in 3D')
fig.suptitle('Radial escape yokes: frozen geometry FAIL',fontsize=20,fontweight='bold')
fig.supxlabel('4.000 m outreach • full bag envelopes retained • lower rack approaches at y = ±29.000 m, z = 4.000 m\nHosts 9/10 still cross; host 23 enters upper bag 0. No penetration retirement or displaced-volume credit.',fontsize=12)
save(fig,'arrangement')

mod=j['modules'][0];row=j['routes'][0];loads=j['states'][0]['modules'][0]
origin=np.asarray(mod['low']);n=np.asarray(mod['normal']);t1=np.asarray(mod['tangent1']);t2=np.asarray(mod['tangent2'])
def local(p):
    q=np.asarray(p)-origin;return np.array([q@t1,q@t2,q@n])
fig=plt.figure(figsize=(17,10),layout='constrained')
ax=fig.add_subplot(1,2,1,projection='3d');right=fig.add_subplot(1,2,2)
for obj in j['objects']:
    if obj['host']==9 and obj['role'] in ('module','footprint','socket'):
        a,bp=local(obj['a']),local(obj['b']);line3(ax,[a,bp],color=teal if obj['role']!='footprint' else '#92734d',lw=1.3)
tip=local(mod['tip']);ax.scatter(*tip,color=red,s=55);ax.text(*tip,' D: rope socket',fontsize=11)
for k,root in enumerate(mod['roots']):
    p,a=local(root['surface']),local(root['root']);ax.scatter(*p,s=30,color=blue)
    ax.text(*a,f' A{k}',fontsize=10)
    direction=np.asarray(loads['roots'][k]['reaction_on_module_n']);direction=direction/np.linalg.norm(direction)
    dv=np.array([direction@t1,direction@t2,direction@n])*.55
    ax.quiver(*a,*dv,color=red,arrow_length_ratio=.22,linewidth=1.3)
    lug=local(root['existing_cradle_lug']);ax.scatter(*lug,color='#92734d',s=24)
ax.set(xlabel='latitude tangent (m)',ylabel='meridian tangent (m)',zlabel='outward radial (m)',xlim=(-1.4,1.4),ylim=(-1.4,1.4),zlim=(-.2,4.6))
ax.set_box_aspect((2.8,2.8,4.8));ax.view_init(elev=20,azim=-42)
ax.set_title('Host 9: finite module and demanded root reactions',pad=20)

right.axis('off')
text=(
    'ATTACHMENT AND LOAD PATH\n\n'
    'Bag centre → original attachment defines radial n.\n'
    'Four feet: ±0.750 m along each tangent,\n'
    'projected onto the unchanged spherical bag.\n'
    'Root joints: 0.300 m outward from each foot.\n'
    'Dead-ended rope socket D: 4.000 m along n.\n\n'
    'Rope → tip plate / four pins → four 100×100×6\n'
    'RHS legs → finite root joints / 120×120×6 posts\n'
    '→ 0.250 m radius reinforced pads → four curved\n'
    '0.250 m wide straps → original cradle-band\n'
    'points at ±0.250 m latitude tangent.\n\n'
    'Each strap is 0.900 m long; laminate 6 mm.\n'
    'Pads: 10 mm laminate; 20% bond stock is paid.\n'
    'Root pins: 50 mm × 180 mm; two 18 mm clevis plates.\n'
    'Tip plate: 300 × 300 × 20 mm; finite sockets.\n\n'
    'RETAINED BENDS AND REQUIRED MOTION\n\n'
    'Two rack bends: 450 mm pitch radius; guard 600 mm.\n'
    '60 mm axle; two bearings; 26 mm groove width.\n'
    'Actuator nominal 1.000 m, command 0.800–1.200 m.\n'
    'Required clearance: 0.250 m + 0.200 m hardware\n'
    '+ 0.200 m bag motion + calculated rope sag.\n\n'
    'Red arrows: sea-level cold root force requirements.\n'
    f'Rope tension: {j["states"][0]["rows"][0]["tension_n"]/1000:.1f} kN.\n'
    'Exact-CG residual couple: about 5.99 kN m.\n'
    'Root couples, membrane and connections remain\n'
    'UNKNOWN; static balance is conditional.\n'
    'No tip or root is treated as a free fixed support.'
)
right.text(.02,.99,text,va='top',fontsize=12,linespacing=1.25)
fig.suptitle('One repeated radial-yoke topology — dimensions and reaction path',fontsize=19,fontweight='bold')
fig.supxlabel('Dimensions in metres unless stated. Nominal fixed geometry only; computed large root motion is rejected, not drawn as a compatible shape.',fontsize=11)
save(fig,'module-detail')
print(json.dumps(dict(input_sha256=hashlib.sha256(src.read_bytes()).hexdigest(),drawing_source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),files={p.name:dict(bytes=p.stat().st_size,sha256=hashlib.sha256(p.read_bytes()).hexdigest()) for p in sorted(out.iterdir()) if p.suffix in ('.svg','.png')}),indent=2))
