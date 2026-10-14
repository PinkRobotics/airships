#!/usr/bin/env python3
"""Draw the one I011 connection schedule from its recorded geometry."""
import argparse
import html
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent


def draw(data):
    g=data['geometry']; parts=[]
    def add(s): parts.append(s)
    def text(x,y,s,size=16,colour='#172b45',weight='normal'):
        add(f'<text x="{x}" y="{y}" font-family="sans-serif" font-size="{size}" fill="{colour}" font-weight="{weight}">{html.escape(s)}</text>')
    def line(x1,y1,x2,y2,c='#30465b',w=2,dash=''):
        add(f'<path d="M{x1:.3f} {y1:.3f}L{x2:.3f} {y2:.3f}" fill="none" stroke="{c}" stroke-width="{w}" stroke-dasharray="{dash}"/>')
    def rect(x,y,w,h,fill='#ffffff',stroke='#d5dce5',radius=8):
        add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{radius}" fill="{fill}" stroke="{stroke}"/>')
    def circle(x,y,r,fill='none',stroke='#30465b',width=2):
        add(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{width}"/>')
    def dimension(x1,x2,y,label):
        line(x1,y,x2,y,'#65758a',1);line(x1,y-6,x1,y+6,'#65758a',1);line(x2,y-6,x2,y+6,'#65758a',1)
        text((x1+x2)/2-7*len(label)/2,y+21,label,14)
    add('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1300 1060" role="img" aria-labelledby="title desc">')
    add('<title id="title">R3-I011 two-column X-web and erection saddle: failed represented design</title>')
    add('<desc id="desc">An equal-scale endpoint plan shows outer j to inner j plus or minus two. The web families occupy axial planes 400 mm apart. Separate dimensioned schematics show both-end hardware and a saddle with a failed 3 mm jaw.</desc>')
    rect(0,0,1300,1060,'#f6f8fb','#f6f8fb',0)
    text(30,36,'R3-I011 · 80 m capsule · SF1.2 · one explicit X-web and attachment design',23,weight='bold')
    text(30,62,'FAIL: mass balance, ring-cuff transfer and erection jaw. Global stability and physical confidence UNKNOWN.',17,'#9a2631')
    rect(30,84,730,408);rect(780,84,490,408)
    text(50,112,'1  Endpoint plan — one scale in both axes',18,weight='bold')
    scale=27.0
    def point(r,j):
        theta=j*2*math.pi/g['columnCount'];return 350+scale*r*math.sin(theta),300-scale*(r*math.cos(theta)-34)
    for r in [g['outerFrameRadiusM'],g['innerFrameRadiusM']]:
        for j in range(-4,4):line(*point(r,j),*point(r,j+1),'#506579',3)
    for j in [-1,0,1]:
        for sign,colour in [(1,'#b34e15'),(-1,'#167b91')]:
            line(*point(g['outerFrameRadiusM'],j),*point(g['innerFrameRadiusM'],j+sign*2),colour,3 if j==0 else 1.4)
    for r in [g['outerFrameRadiusM'],g['innerFrameRadiusM']]:
        for j in range(-4,5):circle(*point(r,j),3,'#ffffff')
    x,y=point(g['outerFrameRadiusM'],0);text(x+9,y-13,'O₀',15)
    for j,label in [(-2,'I₋₂'),(2,'I₊₂')]:
        x,y=point(g['innerFrameRadiusM'],j);text(x-14,y+23,label,15)
    for j in [-2,0,2]:
        x,y=point(g['outerFrameRadiusM'],j);line(x,y-24,x,y-5,'#9a2631',2);line(x-4,y-11,x,y-5,'#9a2631',2);line(x+4,y-11,x,y-5,'#9a2631',2)
    text(50,333,'111 columns · 41 barrel planes x = −40, −38, …, 40 m',16)
    text(50,359,f'R outer = {g["outerFrameRadiusM"]:.3f} m · R inner = {g["innerFrameRadiusM"]:.6f} m',16)
    text(50,385,f'Depth {g["centrelineDepthM"]:.6f} m · angle 4π/111 = {g["angleRad"]:.9f} rad',16)
    text(50,411,f'Pin length {g["webPinLengthM"]:.6f} m · carbon cut {g["webCarbonCutM"]:.6f} m',16)
    text(50,439,'Ring tube 250 × 12 mm · web tube 300 × 2.5 mm (OD × wall)',16)
    text(50,468,'Projected crossings are not connected. Existing wall hoops remain separately billed.',14,'#536679')
    text(800,112,'2  Separate axial web planes',18,weight='bold')
    text(800,138,'Section away from the end; schematic node above.',14)
    line(1025,155,1025,379,'#65758a',1,'5 4')
    rect(875,165,300,30,'#e0e6ed','#506579',0)
    text(871,158,'600 mm node crossarm',14)
    for x,c,label in [(925,'#167b91','−200 mm'),(1125,'#b34e15','+200 mm')]:
        circle(x,290,75,'none',c,2);line(x,195,x,215,c,2);text(x-32,289,label,14,c)
    dimension(925,1125,390,'400 mm centres')
    text(800,445,'300 mm tube OD → 100 mm family clearance',16)
    text(800,472,'Offset-arm moment is charged; no out-of-plane pass.',14,'#536679')
    rect(30,510,730,325);rect(780,510,490,325)
    text(50,540,'3  One web end — schematic; dimensions govern',18,weight='bold')
    text(50,567,'Repeat at BOTH ends: 18,204 complete web-end assemblies.',15)
    rect(102,610,220,12,'#adb9c7','#506579',0);rect(102,678,220,12,'#adb9c7','#506579',0)
    circle(120,650,12,'#ffffff','#30465b',3);line(120,622,120,638);line(120,662,120,678)
    rect(312,598,10,104,'#adb9c7','#506579',0)
    rect(322,610,350,80,'#d9ebe7','#028078',0)
    rect(322,619,160,62,'none','#506579',0)
    line(322,619,482,619,'#506579',3);line(322,681,482,681,'#506579',3)
    text(495,643,'Carbon tube',15);text(495,667,'300 × 2.5 mm',15)
    text(57,730,'Pin 40 × 120 mm',14)
    text(260,730,'Plate Ø320 × 8 mm',14)
    text(482,730,'Insert 294 × 3 × 300 mm',14)
    dimension(120,322,758,'300 mm setback')
    text(50,811,'Two 320 × 120 × 16 mm lugs; washers, retention and bond all included.',14)
    text(800,540,'4  Replacement erection saddle',18,weight='bold')
    text(800,567,'Schematic: film → jaws → flanges → band → hoop',14)
    circle(900,658,52.8,'#edf2f6','#506579',2)
    circle(900,658,49.8,'#d9ebe7','#028078',2)
    line(948,632,1115,632,'#506579',4);line(948,646,1115,646,'#506579',4)
    for x in [973,1000]:circle(x,639,4,'#506579')
    line(1113,638,1198,638,'#b34e15',3)
    text(800,748,'Band 3 × 100 mm; hoop OD166; lining 2 mm',14)
    text(800,774,'Two jaws 80 × 40 × 3 mm; 20 mm cantilever',14)
    text(800,800,'Jaw stress 877 MPa > 355 MPa screen: FAIL',15,'#9a2631',weight='bold')
    text(1050,605,'M12 bolts',14);text(1098,681,'film / patch',14)
    rect(30,855,1240,175,'#fff3f1','#e8c6c1')
    text(50,887,'Recorded result — conditional calculations, not a fabrication release',19,'#9a2631',weight='bold')
    mass=data['mass'];c=data['connectionScreens']
    text(50,918,f'Hull {mass["hullT"]:.3f} t + gas {mass["retainedGasT"]:.3f} t; sea-level margin {mass["at"][0]["knownMarginT"]:.3f} t.',18)
    text(50,948,f'Ring sleeve: {c["ringForceN"]/1e6:.3f} MN demand / {c["ringCuffYieldScreenN"]/1e6:.3f} MN nominal yield screen.',18)
    text(50,977,'Both ends and node offsets are billed. Cap inventory, bond stiffness and loaded-volume corrections remain open.',16)
    text(50,1007,'Next: continuous-ring landing zones and a separately repriced 8 mm jaw; neither next change is solved here.',16)
    add('</svg>')
    return '\n'.join(parts)+'\n'


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    svg=draw(json.loads((HERE/'result.json').read_text()));path=HERE/'geometry.svg'
    if args.check:
        assert path.read_text()==svg
        print('I011 SVG matches the recorded endpoint geometry and dimensions.')
    else:path.write_text(svg)


if __name__=='__main__':main()
