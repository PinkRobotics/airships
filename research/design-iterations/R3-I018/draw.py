#!/usr/bin/env python3
"""Draw the declared arrangement from saved calculator JSON; no model execution."""
import json
import math
from pathlib import Path
import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle, Polygon

data=json.loads(Path(sys.argv[1]).read_text())
dest=Path(sys.argv[2]) if len(sys.argv)>2 else Path(__file__).resolve().parent
dest.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'svg.fonttype':'none','svg.hashsalt':'I018-isolated-air-v1'})
colours={'U0':'#9b4d96','U3':'#bb641f','L12':'#087c88'}
state=data['states'][0]
rb=data['bag_radius_m']; r=(3*data['inventory']['external_m3']/(4*math.pi))**(1/3)


def save(fig,name):
    path=dest/(name+'.svg')
    fig.savefig(path,metadata={'Date':None},facecolor='white')
    path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines())+'\n')
    fig.savefig(dest/(name+'.png'),dpi=115,facecolor='white')
    plt.close(fig)


fig=plt.figure(figsize=(16,10),layout='constrained')
gs=fig.add_gridspec(2,2,width_ratios=(1.15,1))
ax=fig.add_subplot(gs[:,0]); ax.set_aspect('equal')
ax.add_patch(Circle((0,0),r,facecolor='#fff5d9',edgecolor='#535b69',linewidth=2))
for bag in state['bags']:
    b=bag['bag']; c=data['bag_centres'][b]; colour=colours[bag['region']]
    ax.add_patch(Circle((c[0],c[2]),rb,fill=False,edgecolor=colour,linestyle='--',linewidth=1.6))
    top=bag['surrogate_fill_top_z_m']
    zs=[c[2]-rb+2*rb*j/120 for j in range(121)]
    zs=[z for z in zs if z<top]+[top]
    side=[math.sqrt(max(0.,rb*rb-(z-c[2])**2)) for z in zs]
    poly=[(c[0]-s,z) for s,z in zip(side,zs)]+[(c[0]+s,z) for s,z in zip(reversed(side),reversed(zs))]
    ax.add_patch(Polygon(poly,facecolor=colour,alpha=.18,edgecolor='none'))
    ax.text(c[0],c[2],f"{bag['region'] if b in (0,3) else 'L'+str(b)}\n{'.60' if b in (0,3) else '.25'} mm",ha='center',va='center',color=colour,weight='bold')
    ax.plot(c[0],c[2]-rb,'ks',ms=5)
for duct in data['ducts']:
    xs=[p[0] for p in duct['points']]; zs=[p[2] for p in duct['points']]
    ax.plot(xs,zs,lw=3,color=colours[duct['region']])
for reg,h in data['headers'].items():
    x,_,z=h['centre']; ax.plot(x,z,'o',ms=9,color=colours[reg])
ax.annotate('',xy=(-r,34),xytext=(r,34),arrowprops={'arrowstyle':'<->','color':'#3c4452'})
ax.text(0,35.4,f'Loaded reference diameter {2*r:.3f} m',ha='center',fontsize=10)
ax.set(xlim=(-41,41),ylim=(-48,41),xlabel='x, m  (y suppressed in this elevation)',ylabel='z, m',title='Fixed full envelopes and one declared air-volume surrogate')
ax.grid(alpha=.15)
ax.text(.02,.02,'Dashed circles: installed R = %.3f m envelopes\nShading: cold sea-level cap quadrature, not solved shape\nSquares: fixed port pressure / temperature taps'%rb,transform=ax.transAxes,fontsize=9,va='bottom',bbox={'facecolor':'white','alpha':.9,'edgecolor':'none'})

ap=fig.add_subplot(gs[0,1]); ap.set_aspect('equal')
for reg,h in data['headers'].items():
    x,y,z=h['centre']; colour=colours[reg]
    if reg=='L12':
        u=1/math.sqrt(2); length=h['length_m']
        ap.plot([x-u*length/2,x+u*length/2],[y+u*length/2,y-u*length/2],lw=13,color=colour,alpha=.5)
        ap.text(0,1.9,'L12: 12 m × 1.50 m bore',ha='center',color=colour,fontsize=10)
    else:
        ap.add_patch(Rectangle((x-2,y-.55),4,1.1,facecolor=colour,alpha=.5))
        ap.text(x,y+1.2,f'{reg}: 4 m × 1.10 m bore',ha='center',color=colour,fontsize=10)
    ap.plot(x,y,'ko',ms=3)
for d in data['ducts']:
    p=d['points'][0]; c=data['bag_centres'][d['bag']]
    ap.annotate('to bag '+str(d['bag']),xy=(p[0],p[1]),xytext=(c[0]*.85,c[1]*.85),fontsize=9,
                arrowprops={'arrowstyle':'->','color':colours[d['region']]})
ap.set(xlim=(-14,14),ylim=(-12,12),xlabel='x, m',ylabel='y, m',title='Separated headers: plan at z = %.3f m'%data['headers']['U0']['centre'][2])
ap.grid(alpha=.2)

pp=fig.add_subplot(gs[1,1])
for b in (0,1):
    bag=state['bags'][b]; c=data['bag_centres'][b]
    reg=next(s for s in state['regions'] if s['region']==bag['region'])
    zz=[c[2]-rb+2*rb*j/80 for j in range(81)]
    dp=[reg['p_at_zero_pa']*math.exp(-state['air_inverse_scale_m']*z)-state['gas_p_at_zero_pa']*math.exp(-state['gas_inverse_scale_m']*z) for z in zz]
    pp.plot(dp,zz,lw=2,color=colours[bag['region']],label='U0 / U3' if b==0 else 'L1 / L2 common air')
pp.axvline(0,color='red',ls=':',lw=1)
pp.set(xlabel='Air minus common helium pressure, Pa',ylabel='z, m',title='Cold sea-level nominal fields; positive pressure only')
pp.legend(fontsize=10); pp.grid(alpha=.2)
fig.suptitle('I018 | Isolated upper air regions, common helium | Physical compatibility UNKNOWN / cuff FAIL',fontsize=15,weight='bold')
save(fig,'arrangement')


fig,axes=plt.subplots(3,1,figsize=(16,11),layout='constrained')
def box(ax,x,y,w,h,label,colour):
    ax.add_patch(Rectangle((x,y),w,h,facecolor='white',edgecolor=colour,lw=1.7))
    ax.text(x+w/2,y+h/2,label,ha='center',va='center',fontsize=10)
def arrow(ax,a,b,label='',both=False,colour='#3c4452'):
    ax.annotate('',xy=b,xytext=a,arrowprops={'arrowstyle':'<->' if both else '->','color':colour,'lw':1.8})
    if label: ax.text((a[0]+b[0])/2,(a[1]+b[1])/2+.13,label,ha='center',fontsize=9)
for ax,reg in zip(axes,('U0','L12','U3')):
    colour=colours[reg]; lower=reg=='L12'; rating=16 if lower else 8
    ax.set(xlim=(0,16),ylim=(-.2,3.7)); ax.axis('off')
    ax.text(0,3.38,f"{reg} | two {rating} m³/s blowers at assumed 3 kPa | {'lower bags 1 and 2 connected' if lower else 'one isolated upper bag'}",color=colour,fontsize=13,weight='bold')
    for y,n in ((2.15,1),(.8,2)):
        box(ax,.1,y,.8,.6,'air',colour)
        box(ax,1.45,y,1.35,.6,'B'+str(n),colour)
        box(ax,3.3,y,1.25,.6,'SV + CV',colour)
        arrow(ax,(.9,y+.3),(1.45,y+.3)); arrow(ax,(2.8,y+.3),(3.3,y+.3))
        arrow(ax,(4.55,y+.3),(5.15,1.8))
    box(ax,5.15,1.35,1.7,.9,'OWN HEADER\nno cross-tie',colour)
    box(ax,7.55,1.45,1.5,.7,'PV / flow\ncontrol',colour)
    arrow(ax,(6.85,1.8),(7.55,1.8),both=True)
    if lower:
        for y,bag in ((2.05,1),(.95,2)):
            box(ax,9.7,y,1.3,.65,'SV '+str(bag),colour)
            arrow(ax,(9.05,1.8),(9.7,y+.325),both=True)
            box(ax,12.15,y,3.55,.65,'L'+str(bag)+' air',colour)
            arrow(ax,(11.,y+.325),(12.15,y+.325),'1.030 m bore',True,colour)
        ax.text(13.9,.66,'One fixed air / He tap pair at each bag port',ha='center',fontsize=9)
    else:
        box(ax,9.7,1.45,1.3,.7,'bag SV',colour)
        arrow(ax,(9.05,1.8),(9.7,1.8),both=True)
        box(ax,12.15,1.35,3.55,.9,reg+' air only',colour)
        arrow(ax,(11.,1.8),(12.15,1.8),'1.030 m bore',True,colour)
        ax.text(13.9,1.03,'Fixed bottom-port air / He taps → electrical control',ha='center',fontsize=9)
    box(ax,7.6,.05,3.4,.65,'MV + RV1 + RV2 → ambient',colour)
    arrow(ax,(6.,1.35),(7.6,.38),'exhaust')
    ax.text(7.7,2.98,'Air supply and exhaust stay within this region.',fontsize=10)
    ax.text(9.8,-.12,'CLOSED bag SV: trapped-air fault; header relief unavailable.',fontsize=10,color='#a52626')
fig.suptitle('I018 | Independent pressure boundaries and explicit incomplete failure protection',fontsize=16,weight='bold')
fig.supxlabel('SV: shutoff   CV: check   PV: regulating throttle   MV: modulating vent   RV: mechanical relief\nCommon outside atmosphere and electrical supply do not connect the three pressurized air regions. No helium vent in the nominal inventory law.',fontsize=11)
save(fig,'control-paths')
