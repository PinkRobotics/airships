# 037b interlayer sourcing summary

All values are QUESTIONABLE (vendor "typical" data or secondary reports); one row is a PROJECTION. Details in interlayer.json (51 rows).

**Best compliant candidates (read on pages)**
- RTV 566 (Momentive): measured shear modulus 0.5 to 0.64 MPa for 95-190 um layers (Dokania and Kruit 2008). Primed lap shear 465 psi (3.2 MPa), specific gravity 1.49 (base), service -115 to +260 C, room-temperature cure (7 d), TML 0.14%, CVCM 0.02%.
- NuSil CV-2566: primed lap shear 500 psi (3.4 MPa) on the 2014 sheet, 575 psi in the 2023 guide; SG 1.49; Shore A 55; Tg -125 C; DMA storage modulus 4 MPa above Tg (no shear modulus printed); stated use -140 to 300 C.
- Sylgard 184: G 0.44 MPa (25 C cure, derived from E 1.32 MPa), SG 1.03, service -45 to 200 C; no lap shear on the sheet. DOWSIL 93-500: primed lap shear 3.2 MPa, SG 1.03.
- Stiffer urethane/epoxy: Appli-Thane 7300 G 24.9 MPa but 2.8 g/cc; 3M DP6310NS 593 MPa, lap shear 3600 psi at 23 C falling to 900 psi at 82 C; 2216 B/A "shear modulus" 342 MPa at RT rising to 2745 MPa at -100 C (label suspect), Milbond 159 MPa at 20 C rising to 592 MPa at -50 C.

**Practice**
- Shear stress scales as G x a/(2t) x delta-alpha x delta-T (Daly and Hawk, via Huie 2024); softer and thicker lowers it. In their worked example (23 ppm/K mismatch) RTV 566 gives 3.4 psi, 2216 gives 9539 psi.
- Closed-form athermal bond rules (Bayar, van Bezooijen, Monti) are for a lens in a cell; they differ by about 3x on the same bond. Applying them to a flat face-core joint is a PROJECTION.
- Closest sandwich precedent: NASA Glenn 2013, Ti heat pipes bonded to Al face sheets failed from mismatch. A low-modulus layer and a thicker bond were identified as ways to lower shear, but they chose a high-strength film adhesive cured hot.
- Beryllium: NASA Ames/Arizona 1990 says a classic silicone bonded mount is not feasible for beryllium and uses flexures.

**Gaps**
No beryllium-to-honeycomb elastomer-interlayer precedent and no Materion bonding guide found. No measured CV-2566 shear modulus; current Avantor sheet unreachable (HTTP 522). RTV 567, EA 9361 and soft urethanes (Solithane, Uralane, Lord) not sourced. 2216 lap shear is secondary only.
