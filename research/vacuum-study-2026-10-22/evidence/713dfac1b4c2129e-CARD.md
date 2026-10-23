# MAINLINE-005b NFI-CRUSH: P2 core through-thickness crush — ESTIMATE_PENDING_CHECKER

Unit vacuum-mainline005b-nfi-crush-1019. The next job named by CARD-005, filed the same way. Nothing here is a certification. Every sourced value is QUESTIONABLE.

## The model, QUESTIONABLE

The external pressure bears on the outer face. Both faces carry equal membrane force, and the core must pass the through-thickness load from the outer face to the inner face without crushing. On the brief's example model the core compressive stress sits near p/2, half the external pressure, where the two faces share the membrane resultant. I use sigma_core = p/2 exactly and tag the model QUESTIONABLE: no sandwich reference was pinned for it, the factor of two is the brief's own example, and a real core also sees local face bending the model ignores.

Required core compressive strength is therefore 47730.4 Pa, about 0.048 MPa, for every P2 row: P2, P2-A, P2-C, P2-K and P2-E alike. It does not vary with face or core thickness in this model, only with external pressure. MAINLINE-007's rows take the same line the moment that card is filed: required strength p/2 at their external pressure, with their core densities read against the table below. That card is not filed yet, so no 007 number is stated here.

## Real cores near the requirement, sourced, QUESTIONABLE

| core | density (kg/m3) | compressive strength | margin on 47730 Pa | source |
|---|---|---|---|---|
| EPS foam, geofoam EPS15 class | 14.4 | 25 kPa at 1% strain; about 70 kPa at 10% strain for 15 kg/m3 EPS | fails at 1%, passes at 10% | geofoam table via Oceanic Supply; 15 kg/m3 70 kPa via Insulation Shop EWI listing |
| EPS foam, lightest class | 11 | 50 kPa at 10% strain | 1.05 | National Polystyrene technical data (AS 1366.3) |
| Aluminium honeycomb, Hexcel ACG-1 lightest | 20.8 | 0.552 MPa bare | 11.6 | Hexcel HexWeb ACG-1 datasheet via lookpolymers |
| Aluminium honeycomb, Hexcel CR-PAA 3/8-5056 | 36.8 | 1.07 MPa bare minimum | 22 | Hexcel CR-PAA datasheet via lookpolymers |
| Aramid (Nomex) honeycomb, Hexcel HRH-10 1.5 pcf | 24 | 0.621 MPa stabilized typical | 13 | Hexcel HRH-10 datasheet via lookpolymers |
| PMI foam, Rohacell 71 HERO | 71 | 1.10 MPa (ISO 844) | 23 | MatWeb, Evonik Rohacell 71 HERO |
| PMI foam, Rohacell range | 52-110 | 0.8-3.6 MPa (ISO 844) | 17-75 | Evonik Rohacell RIST-HT via Knowde |
| Silica aerogel blanket, Pyrogel XTF | 200 | 102 kPa at 10% strain (ASTM C165) | 2.1 | Aspen Pyrogel XTF datasheet |
| Metallic microlattice, Ni-P | 0.9 | recovers past 50% strain; no crush strength near 47.7 kPa published | does not meet it | Schaedler et al., Science 334, 962-965 (2011), doi 10.1126/science.1211649 — PROJECTION only |

## The lowest core density at which crush is met

About 11 kg/m3, in EPS-class foam, on the 10%-strain strength definition: 50 kPa against 47.7 kPa required, a margin of 1.05 that no one should build on. On the stricter 1%-strain geofoam definition the same foams need about 18-22 kg/m3. Every honeycomb and PMI foam listed clears the requirement by more than ten times from 20 kg/m3 up. The rows' incumbent 16 kg/m3 sits between the two EPS definitions, so whether the assumed core passes depends on which strain definition the checker adopts; that choice is the open row in NFI.json.

Crush, on this QUESTIONABLE model, is not what binds P2. Buckling and face yield from MAINLINE-005 bind orders of magnitude harder. What crush does is set a floor under core density: go below about 11 kg/m3 for lightness and this mode, ignored until now, becomes the governing one.
