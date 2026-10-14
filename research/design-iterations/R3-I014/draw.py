#!/usr/bin/env python3
"""Dimensioned record of the fixed I014 construction; not a production drawing."""
import argparse
from html import escape
import json
import math
from pathlib import Path

HERE=Path(__file__).resolve().parent


def render():
    data=json.loads((HERE/'result.json').read_text()); g=data['geometry']; m=data['mass']
    a=data['erectionAttachment']; c=data['trials'][0]['connections']
    out=['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1550" viewBox="0 0 1600 1550">',
         '<title>I014 continuous circumferential force path and 8 mm jaw trial</title>',
         '<desc>One 80 m failed mass design: explicit midpoint bridges, integral web landings, both-end hardware and unresolved grip. The plan has equal scales; component details are schematic and dimensioned.</desc>',
         '<style>text{font-family:DejaVu Sans,Arial,sans-serif;fill:#e8edf3;font-size:18px}.title{font-size:30px;font-weight:bold}.sub{font-size:23px;font-weight:bold}.small{font-size:16px}.muted{fill:#b4c1ce}.bad{fill:#ff9b8d}.cyan{fill:#79d5ec}.green{fill:#93deb3}.orange{fill:#f0ba73}</style>',
         '<rect width="1600" height="1550" fill="#111b27"/>']
    def text(x,y,s,cls='',anchor='start'):
        out.append(f'<text x="{x:.2f}" y="{y:.2f}" class="{cls}" text-anchor="{anchor}">{escape(s)}</text>')
    def line(x1,y1,x2,y2,color='#c9d3dd',width=2,dash=None):
        d=f' stroke-dasharray="{dash}"' if dash else ''
        out.append(f'<line x1="{x1:.3f}" y1="{y1:.3f}" x2="{x2:.3f}" y2="{y2:.3f}" stroke="{color}" stroke-width="{width}"{d}/>')
    def rect(x,y,w,h,fill,stroke='none'):
        out.append(f'<rect x="{x:.3f}" y="{y:.3f}" width="{w:.3f}" height="{h:.3f}" fill="{fill}" stroke="{stroke}"/>')
    def circle(x,y,r,fill='none',stroke='#c9d3dd',width=2):
        out.append(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{r:.3f}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')
    def panel(x,y,w,h,title):
        rect(x,y,w,h,'#182635','#34485a');text(x+18,y+32,title,'sub')
    def dim(x1,x2,y,s):
        line(x1,y,x2,y);line(x1,y-5,x1,y+5);line(x2,y-5,x2,y+5);text((x1+x2)/2,y-8,s,'small','middle')
    text(24,44,'I014 · continuous force path, explicit joints, retained failure','title')
    text(24,78,f'Known subtotal {m["knownSubtotalT"]:.3f} t · margin {m["at"][0]["knownMarginT"]:.3f} t at sea level · global pressure capacity UNKNOWN','bad')
    panel(24,104,760,400,'A  Same-scale endpoint plan · one of 41 planes')
    ro,ri=g['outerRingRadiusM'],g['innerRingRadiusM'];alpha=2*math.pi/111
    def pt(r,j):return (400+r*math.sin(j*alpha)*39,193+(ro-r*math.cos(j*alpha))*39)
    for r in (ro,ri):
        for j in range(-3,3):line(*pt(r,j),*pt(r,j+1),'#79d5ec',4)
        for j in range(-3,4):circle(*pt(r,j),4,'#93deb3','#93deb3')
    for j in (-1,0,1):
        line(*pt(ro,j),*pt(ri,j+2),'#f0ba73',3)
        line(*pt(ro,j),*pt(ri,j-2),'#a794e8',3)
    text(46,156,f'Rₒ={ro:.6f} m; Rᵢ={ri:.6f} m; 111 columns','small')
    text(46,430,f'j→j±2; pin length {g["webPinLengthM"]:.6f} m; carbon {g["webCarbonCutM"]:.6f} m','small')
    text(46,458,'±200 mm axial planes; 100 mm tube gap; crossings have no joint','small')
    text(46,484,'41 stations at 2 m pitch; cap geometry is not represented here','small muted')
    panel(804,104,772,400,'B  Mid-chord circumferential bridge')
    text(824,156,'Longitudinal section; gap enlarged; dimensions control','small muted')
    # Axial carbon path and the separate 1 mm adhesive layers.
    for yy in (226,302):
        rect(835,yy,341,12,'#79d5ec');rect(1184,yy,341,12,'#79d5ec')
    for yy in (209,314):rect(925,yy,510,15,'#f0ba73')
    for yy in (224,314):
        rect(925,yy,251,2,'#e28ad8');rect(1184,yy,251,2,'#e28ad8')
    line(1180,192,1180,342,'#aebdca',1,'4 4')
    dim(925,1435,185,'1004 mm bridge: 292 OD / 252 ID, 20 wall')
    dim(925,1176,365,'500 mm overlap');dim(1184,1435,365,'500 mm overlap')
    text(1180,393,'4 mm butt gap; no butt-bearing credit','small','middle')
    text(824,424,'Base ring 250×12; 1 mm bond; 9102 complete bridges','small')
    soft=data['trials'][1]['connections']['circumferenceJoint']['meanLapShearPa']/1e6
    text(824,451,f'One bridge+bonds {data["hardware"]["spliceKg"]:.3f} kg; mean shear {c["circumferenceJoint"]["meanLapShearPa"]/1e6:.2f}–{soft:.2f} MPa','small')
    text(824,478,'Bond peel, peak shear, cure and moment transfer UNKNOWN','small bad')
    panel(24,524,760,490,'C  Integral node · axial/radial section')
    text(44,575,'Locally 310 OD / 226 ID over 600 mm developed ring length','small')
    cx,cy,scale=405,766,.78
    circle(cx,cy,155*scale,'#3c765e','#93deb3')
    circle(cx,cy,125*scale,'#286079','#79d5ec')
    circle(cx,cy,113*scale,'#182635','#79d5ec')
    for sign in (-1,1):
        # Curved pad, 160 mm along the ring; section shows its radial profile.
        pts=[]
        for r in range(-70,71,5):pts.append((cx+sign*math.sqrt(155**2-r*r)*scale,cy-r*scale))
        pts.extend([(cx+sign*168*scale,cy-70*scale),(cx+sign*168*scale,cy+70*scale)])
        out.append('<polygon points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in pts)+'" fill="#93deb3"/>')
        lo,hi=sorted((cx+sign*168*scale,cx+sign*188*scale));rect(lo,cy-70*scale,hi-lo,140*scale,'#3c765e','#93deb3')
        rect(lo,cy-58*scale,hi-lo,116*scale,'#182635')
        lo,hi=sorted((cx+sign*188*scale,cx+sign*212*scale));rect(lo,cy-90*scale,hi-lo,180*scale,'#93deb3')
        rect(lo,cy-24*scale,hi-lo,48*scale,'#9aabb9');rect(lo,cy-20*scale,hi-lo,40*scale,'#182635')
        xx=sign*222;rect(cx+xx*scale-8*scale,cy-60*scale,16*scale,120*scale,'#9aabb9')
        line(cx+sign*170*scale,cy,cx+sign*290*scale,cy,'#e8edf3',5)
    dim(cx-200*scale,cx+200*scale,917,'pin centres x=−200 / +200 mm')
    text(44,946,'160×140×12 box neck, 20 long; 180×160×24 tongue','small')
    text(44,974,'One lug at |x|=214…230; neck ends at |x|=188: 26 mm gap','small')
    text(44,1000,'222 mm force lever; eccentric pin and end plate FAIL','small bad')
    panel(804,524,772,490,'D  Both web ends · q measured from pin')
    text(824,575,'Same detail at both ends; 18 204 complete assemblies','small')
    ox,oy,sc=875,750,.75
    # Tube wall and steel insert in a longitudinal section.
    for sign in (-1,1):
        rect(ox+.400*1000*sc,oy+sign*150*sc-1,270,2,'#79d5ec')
        rect(ox+.400*1000*sc,oy+sign*147*sc-1,225,3,'#9aabb9')
    rect(ox-.050*1000*sc,oy+22*sc-8*sc,.442*1000*sc,16*sc,'#9aabb9')
    rect(ox+.392*1000*sc,oy-160*sc,8*sc,320*sc,'#9aabb9')
    rect(ox-12*sc,oy-35*sc,24*sc,70*sc,'#93deb3')
    line(ox,oy-30*sc,ox,oy+90*sc,'#e8edf3',5)
    dim(ox,ox+400*sc,604,'400 mm pin-to-carbon setback at each end')
    dim(ox+400*sc,ox+700*sc,900,'296 mm bond + 4 mm weld relief')
    text(824,928,'Web 300×2.5; insert 294×3×300; plate Ø320×8','small')
    text(824,954,'ONE 442×120×16 outboard lug; Ø40×120 pin; 24 tongue','small')
    text(824,980,'3 mm insert weld + two 6 mm lug seams; mirror for −x family','small')
    text(824,1005,f'Pin VM {c["pinVonMisesTrialPa"]/1e6:.0f}; plate strip {c["endPlateStripBendingPa"]/1e6:.0f} MPa: FAIL','small bad')
    panel(24,1034,1552,458,'E  Separate 8 mm jaw trial · dimensioned mass and unresolved interfaces')
    text(44,1085,'Nominal section detail; unqualified grip/assembly','small muted')
    hx,hy,hs=205,1265,1.12
    circle(hx,hy,88*hs,'#8795a3','#c8d1d9');circle(hx,hy,85*hs,'#775d75','#e28ad8');circle(hx,hy,83*hs,'#182635','#79d5ec')
    for side in (-1,1):
        yy=hy+side*88*hs
        rect(hx-28,yy-4,56,8,'#9aabb9');line(hx,yy-20,hx,yy+20,'#e8edf3',5)
    for yy in (hy-16,hy+8):rect(hx+88*hs,yy,40*hs,8*hs,'#9aabb9')
    bx=hx+88*hs+30*hs;line(bx,hy-32,bx,hy+32,'#e8edf3',4)
    line(hx+88*hs,hy+1,495,hy+1,'#e28ad8',3)
    text(54,1115,'Hoop Ø166; lining 2; band 3×100','small')
    text(54,1140,'Two splits; four 60×50×6 flanges','small')
    text(355,1213,'two M8','small');text(355,1240,'grip bolts','small')
    text(355,1311,'50×40 contact','small');text(355,1338,'80×40×8 jaws','small')
    text(54,1413,'Two M12 band bolts; 2×200×200 patch plies','small')
    text(54,1442,'Bondlines, head/nut/washer and weld masses charged','small')
    text(552,1115,f'Attachment {a["eachKg"]:.6f} kg × 40 393 = {a["totalT"]:.3f} t','sub')
    rows=[('Unchanged nominal demand',f'{a["requiredNominalN"]/1000:.6f} kN'),
          ('8 mm jaw root / nominal plate screen',f'{a["jawBendingPa"]/1e6:.1f} / 355 MPa · limited PASS'),
          ('6 mm band flange at assumed μ=0.3',f'{a["flangeBendingPa"]/1e6:.1f} / 355 MPa · FAIL'),
          ('Grip pressure / M8 prying trial',f'{a["gripPressureRequiredPa"]/1e6:.3f} MPa / {a["M8DoublePryingTrialPa"]/1e6:.1f} MPa'),
          ('Known hull + gas',f'{m["hullT"]:.3f} + {m["retainedGasT"]:.3f} t'),
          ('Sea-level / 2500 m margin',f'{m["at"][0]["knownMarginT"]:.3f} / {m["at"][1]["knownMarginT"]:.3f} t'),
          ('Remaining new-frame allowance',f'{m["maximumNewFrameT"]:.3f} t BEFORE adding any frame')]
    for i,(left,right) in enumerate(rows):
        y=1154+i*39;text(552,y,left,'small');text(1528,y,right,'small bad' if i in (2,5,6) else 'small','end')
    text(552,1450,'Film grip, hoop bearing, global stability and full-vehicle confidence UNKNOWN','small bad')
    text(24,1524,'Dimensions in mm unless marked m. One construction hypothesis; no manufacturing, flight or pressure qualification. README and result.json define the calculation scope.','small muted')
    out.append('</svg>');return '\n'.join(out)+'\n'


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');args=p.parse_args();svg=render();path=HERE/'geometry.svg'
    if args.check:
        assert path.read_text()==svg;print('I014 SVG matches the frozen geometry, bill and failure labels.')
    else:path.write_text(svg)


if __name__=='__main__':main()
