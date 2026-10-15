# R3-I036 — six-segment titanium wedge cord grip (result: CONDITIONAL FAIL on mass)

Status: **computed result, one frozen construction, no qualification.** Six paid titanium
wedge segments grip the cord in a matching aluminium cone, replacing the resin pot. The
honest outcome is a large mass increase and a failed conditional cap screen; the grip
itself stays unproven (contact UNKNOWN). Nothing here demonstrates physical float, and
every prior engineering failure/unknown remains.

Construction: local frame per end, z=0 at the free-cord exit, +z into the fitting.

```
            z=0                             z=L        z=L+H   z=L+H+F        z_r    z_p=z_r+60/100
 free cord   |  six Ti wedges in Al cone     |chamber H |flange F|iso|cap C  |       receiver plate
  <---------+===============================+==========+=======+==+========+=======[]========[]====>
 -z         0                               L          L+H   L+H+F  z_c+0.5  z_r     z_p    z_p+P   stud rear
            | cord D  | tail 8mm ends at z=L+8 (paid cord, not a spring)
            wedge outer cone r = D/2 + t0 + z.tan5; 2 deg gaps between the six 58 deg segments
            cap bolts insert chamber-side; stud carries T to the clamped plate; plate->anchor UNSIZED
```

Frozen dimensions (mm, d60 | d180/11): grip L 60|97; wedge nose thickness 4|6; cone
half-angle 5 deg both; body OD 50|80 (z=0..L+H); chamber H 50|80; flange and cap OD/thk
90/12|140/18 both; bolt circle 70|110; cap bolts M6|M10 with 6.6|10.6 clearance; stud
M14|M23 with 14.6|23.6 cap bore; interior nut height N 21|34.5; stud bearing washer
28/14.6/2|46/23.6/3; isolation 0.5 everywhere; receiver plate 56/12|92/18 at central
clearance 14.6|23.6, front at actual cap rear +60|100; stud tip projection 3|5.

Complete axial stacks are declared in `baseline.json` and verified by the calculator at
run time (every interval, both families). Derived key positions: d60 stud spans
[96.0, 232.5] (blank 136.5), cap bolt 35.9 under head; d180/11 stud spans [152.5, 374.0]
(blank 221.5), cap bolt 54.5 under head. The cap-bolt head-side washer annulus
[29,41]|[45,65] lies inside actual flange material [13.2,45]|[20.8,70] in both families.

## Cord identity

Per cord L_total = L_free + (L+8) + (L+8). The recorded datum already carries exactly
this: (meanCord − lFreeMean)/2 = 0.068000|0.105000 m = L+8 for both families (verified
at 1e-9 m). No extra run, no unrecorded length increase; replacing the resin pot does
not remove embedded cord mass and the cord bill is unchanged.

## Paid stock per end (kg)

| Row (material) | d60 | d180/11 | centre rule |
|---|---:|---:|---|
| six Ti wedge segments | 0.0794 | 0.3148 | own solid centroid |
| Al body with integral flange | 0.6355 | 2.5402 | own solid centroid |
| Al cap | 0.1963 | 0.7097 | own solid centroid |
| four Ti cap bolts (+heads) | 0.0241 | 0.1047 | stack midpoints |
| four Ti cap nuts | 0.0062 | 0.0304 | stack midpoints |
| eight Ti cap washers | 0.0034 | 0.0160 | stack midpoints |
| one Ti stud blank | 0.0931 | 0.4077 | span midpoint |
| three Ti stud nuts | 0.0783 | 0.3472 | stack midpoints |
| three Ti stud bearing washers | 0.0119 | 0.0488 | stack midpoints |
| one Ti receiver plate | 0.1220 | 0.4952 | own solid centroid |
| **new hardware per end** | **1.2502** | **5.0147** | assembly centre z=106.0|169.8 |
| machining 3% on new Al (body+cap) | 0.0250 | 0.0975 | provision, not occupied metal |
| interface/seal/handling lump | 0.0250 | 0.0500 | assembly centre; sufficiency UNKNOWN |

Stud-nut hex across-flats 22.4|36.8 is a declared ASSUMED priced-stock rule (1.6x
nominal; the freeze fixes heights only). Blanks are priced as full nominal cylinders;
thread capacity UNKNOWN. Isolation occupancy (washers and the 0.5 annuli) is listed in
`grip.json` and covered by the lump, not priced twice. Retained protection 0.025 kg/end
continues unchanged.

## Removal candidates — conditional only, zero qualified

| Removed row (exact accepted values) | d60 kg/end | d180/11 kg/end |
|---|---:|---:|
| accepted Al socket body | 0.07594839509961494 | 0.29494000995555875 |
| its machining row (3%) | 0.0022784518529884482 | 0.0088482002986667625 |
| resin pot | 0.0017 | 0.0061 |
| replaced stud | 0.0549 | 0.2321 |
| **conditional total per end** | **0.1348** | **0.5420** |

The machining rows reconcile to the accepted 0.23525614743131826 t exactly. **Qualified
retirement is zero**: the conditional bill credits these four rows only if the
substitution is accepted; the zero-qualified-retirement bill credits none. Everything
else stays paid, explicitly including the old exterior jam nut, the retained anchors and
receiver interface, cord, clips, blocks, doubler pads, attachment bolts and pressure
structure.

## Both bills (tonnes, accepted accounting, lift and gas counted once)

| Line | accepted before | conditional substitution | zero-qualified-retirement |
|---|---:|---:|---:|
| new hardware (both families) | — | 132.45 | 132.45 |
| new machining + lump | — | 4.18 | 4.18 |
| removals credited | — | −14.31 | 0 |
| delta hardware | — | +122.32 | +136.63 |
| assembly share 5% once | — | +6.12 | +6.83 |
| total delta | — | +128.44 | +143.46 |
| sockets line | 16.41 | 138.73 | 153.04 |
| whole-spokes line | 241.51 | 369.94 | 384.97 |
| total | 2229.49 | 2357.92 | 2372.95 |
| **sea-level margin** | **+20.31** | **−108.12** | **−123.15** |
| 2500 m margin | −472.19 | −600.62 | −615.65 |

Rollup convention is the accepted one, rowwise: the sockets line moves by the hardware
delta, the assembly line absorbs the share once, the whole-spokes line moves with the
total, margins move oppositely. x1.5 station-hardware scenario: candidate increment
78.32|85.83 t against the new sea-level margin −108.12|−123.15 t (stored inherited
increment 16.05 t disclosed; blocks/doublers/attachment at stored two-decimal
precision). SF1.2 is a separate construction and stays substitution-UNKNOWN; the
nominal mass delta is not its result.

## Conditional screens (dimensional elastic metal only — none is a proof)

| Screen | d60 | d180/11 | verdict |
|---|---:|---:|---|
| fitting demand T (kN, carried) | 17.7 | 46.27 | accepted saved values |
| cone normal total (kN) | 203.1 | 530.9 | frictionless nominal |
| required cord-face friction | tan5°=0.0875 | 0.0875 | available UNKNOWN |
| cord-face mean pressure (MPa) | 141.1 | 141.1 | crushing UNKNOWN — weakest |
| cone-face mean pressure (MPa) | 52.6 | 54.1 | — |
| body hoop (MPa vs 150) | 58.7 (0.39) | 58.8 (0.39) | conditional pass |
| cap bending, upper-bound strip (MPa vs 150) | 176.1 (1.17) | 189.7 (1.26) | **CONDITIONAL FAIL** |
| stud tension (MPa vs 880) | 115.0 (0.13) | 111.4 (0.13) | thread root UNKNOWN |
| plate bearing (MPa vs 880) | 39.5 (0.04) | 37.8 (0.04) | transfer UNSIZED/UNKNOWN |
| isolation layer compression (MPa) | 3.12 | 3.38 | occupancy only |

The cap screen is the known-conservative radial-strip shape, not a plate solution; its
exceedance is an upper-bound result, not a proven physical failure — but within this
construction the cap as drawn does not clear the assumed working limit. Cord contact
(crushing, fibre damage, friction, slip, seating, creep, retention under unload) is
UNKNOWN; segment load equality is a symmetry assumption, not demonstrated sharing.

## Compliance boundary

The entire cord/grip/receiver compliance and take-up remain UNKNOWN; the resin stage is
not replaced by zero compliance and the I028 n=5 declared-model packets are carried
unchanged as labelled historical comparators (chord-basis historical; n=2..12 class
bounds, global stability and centroid sensitivity UNKNOWN). T0 and fitting demand are
carried independently from the accepted saved values with no second fitting factor.

## Unknowns

Direct cord contact/slip/creep and transfer into the retained receiver are the weakest
remaining engineering assumptions. Also UNKNOWN: rear insertion, nut access, wrench
clearance and station-pitch fit of the longer envelope; receiver-plate adapter or
reinforcement (a named positive unknown, not zero); thread, fatigue, wet/creep and
galvanic sufficiency beyond the declared provisions; installation and global
equilibrium (predecessor closure stays withdrawn).

## Inherited status

R3-I031 remains an unreviewed archive with all nine findings open; its outputs enter no
balance here (the before-state is reconstructed solely from the accepted R3-I028 saved
records). One later unissued direction, conditional on this result, is a paid wider
receiver saddle with a frozen anchor attachment; it is not part of this unit and cannot
rescue its result.

## Reproduction

Single guarded execution: `python3 -I -B research/design-iterations/R3-I036/grip.py
--write` reads `baseline.json` and writes `grip.json` (stdlib only; frozen inputs; no
ancestor import). Three starts were consumed: the initial start and two demonstrated
implementation-defect repairs of the same frozen construction (a washer interval and a
key path, both caught before any physics output); the third start completed. Inputs and
outputs are hash-bound in `grip.json` and `sources.json`.
