#!/usr/bin/env python3
"""MAINLINE-017 improvement directions. Own arithmetic from pinned 014/009/011/007/008 values.
P2 model (014): S=(L-100)/1.05, A=4piR^2, faces 2A tf rho_f, core A tc rho_c, joints 5%, sys 100.
 Modes: CR-1457 global/crimp (Vc,Kc,gamma; gamma=kd on stiff branch, 1 on crimp branch), yield 4 sig tf/R,
 crush strength/(p/2), honeycomb wrinkling 0.33 (design cw) with equibiaxial factor from x^3+x=1.
 Geometry re-optimised over core depth tc (log scan + refine) at every property multiplier.
 Improvement factor: multiplier for E_f,sigma_f,E_c,G_c,crush,kd,cw; divisor for rho_f,rho_c.
 Single: bisection to least=1, cap at 1e4. Combo: differential evolution minimising product of factors.
P3 model (011): V=8piR^2/(sqrt3 s^2)+2, M=3V-6, tube mass=L-97.515-0.02V-50, Asec=tube/(M s rho),
 exact annulus, yield/Euler/local/film as in 011 INPUTS, s<=3 design band, r_o<=s/3, re-optimised over s and r_o."""
import hashlib, json, math, time
import numpy as np
from datetime import datetime
from pathlib import Path
from scipy.optimize import differential_evolution, minimize_scalar
from zoneinfo import ZoneInfo
START=datetime.now(ZoneInfo("America/Los_Angeles")).isoformat(timespec="microseconds"); MONO=time.monotonic()
OUT=Path(__file__).resolve().parent
R,NU,P,LIFT=10.,0.33,95460.83791390515,4889.442150186961
A=4*math.pi*R*R; S=(LIFT-100.)/1.05; ROOT=math.sqrt(1-NU*NU)
_x=0.68
for _ in range(60): _x=_x-(_x**3+_x-1)/(3*_x*_x+1)
BIAX=_x
def sha(p):
    d=Path(p).read_bytes(); return hashlib.sha256(d).hexdigest(),len(d)
pins=[]
def pin(p,exp=None,n=None,role=""):
    s,b=sha(p); r={"path":str(p),"sha256":s,"bytes":b,"role":role}
    if exp: r.update(expected_sha256=exp,expected_bytes=n,match=(s==exp and b==n))
    pins.append(r); return r
pin("unpublished-local-ref:d0b8c122b0211990","0492ca25921dbc5115c6a6d5b6ed6f710fa42f63c6b3bdace2731a8b919dd230",1840,"CARD-017 brief")
pin("withheld-source:b528d6a62c81ce0b","8f359d6c04f84d158ccc232173cb61e86eeede3797fe362d8212066a096f94b5",5874,"COMMON")
B14="unpublished-local-ref:0e3453b543e23937"
pin(f"{B14}/CARD.md","df9e014f7450625b98c18d5a3b2d182b105fff7755e6758baea5424dd85aed14",5045,"014 CARD"); pin(f"{B14}/RESULTS.json","0e2d7bf61d20e6ee2316d545ba53d8a850378379ff126a95ce8cae8181df0eb8",85107,"014 RESULTS"); pin(f"{B14}/INPUTS.json","4d22ff53856afea6f5f8094b7e439e6eecca8ea50e5271a64e74c11c6d38b061",7030,"014 INPUTS")
B9="unpublished-local-ref:ba5f5575d309b9ca"
pin(f"{B9}/CARD.md","a724c23d825f5134f1cdb5dd1010180fb6844509748bb79770df94d7505fb868",7132,"009 CARD"); pin(f"{B9}/RESULTS.json","f109f7eee35012a705e68805b63c1eb107a26f51d609b4e18a48277a9fddfeef",13427,"009 RESULTS")
B11="unpublished-local-ref:023f471e5af2c782"
pin(f"{B11}/CARD.md","ab3fd04af99fcf371ea221a96366cc88ffe3730b6dd8caff216751b19b9462a1",4051,"011 CARD"); pin(f"{B11}/RESULTS.json","d529b7e4efa6fadc53491eb6094de55986b9bf092fae6f295fd8490d86c5b538",98848,"011 RESULTS"); pin(f"{B11}/INPUTS.json","a3e6574dbff669515d8659281f1dfbce3177582cdc64542d6e2218d96afec945",4801,"011 INPUTS")
pin("evidence/b84f229e5f0e7f47-RESULTS.json","b84f229e5f0e7f47af4788c15f0a75794ddfe3bb0d9a64723031815a49dca88d",42460,"008 RESULTS (face sources)")
pin("evidence/cd02e4ec651bc748-RESULTS.json","cd02e4ec651bc748c7f09385b764e0c1880041651461547fed49ebc4c813e2b5",31544,"007 RESULTS (core sources)")

[withheld: private task or principal quotation; scientific result/status retained elsewhere]