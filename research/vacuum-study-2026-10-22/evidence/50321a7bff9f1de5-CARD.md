# MAINLINE-045: damage tolerance. A dent, a hail strike and a puncture on the two evacuated leads. ESTIMATE

Unit vacuum-mainline045-damage-tolerance-1020. Order ord-admiral-rr2-mainline045-dispatch-1019. Status ESTIMATE. Tags QUESTIONABLE, and PROJECTION where named. Nothing here is a certification. Started 2026-10-20T03:29:16-07:00 (order read); the end time is in RESULTS.json. Times are measurements, not limits.

Inputs: 028b (P2's lead), 022d (P3's lead), 015 and 015b (knockdown against dimple), 037 (loads, mooring, VB), 019 (reserve), 016 and 034 (vacuum holding), 031 and 038 (altitude, ground pressure). 043 (SiC reliability) has not filed; this card uses sourced tube strengths instead. Four sourcing sub-workers of this seat opened the threat, sandwich-impact, SiC-and-film and leak sources; their files are pinned.

## The answer

**Neither lead is damage tolerant, and neither can be made so on its own budget.** For both, damage tolerance is an operating requirement: shelter or vent before hail, and touch nothing while evacuated.

**P2 (028b, beryllium on CR-III):** the dent itself does not lower gamma. But the face pushes the dent further into the core.
- **Gamma.** Every impact dent is narrow beside the buckle: lambda 0.08-0.26 against the 0.63 below which 015's plateau cannot take gamma under 0.564 at any depth.
- **The growth.** Each face carries a fixed 238.7 kN/m (pR/4), and the core crushes at 0.241 MPa. Over a crushed zone wider than 54.8 mm (clamped edge; 27.1 mm simply supported), that force drives the dent deeper once it passes about 0.6-1.5 mm at 60-160 mm across (0.15-1.3 mm simply supported). This is this seat's derivation. Compression-after-impact sources describe the same failure: face wrinkling over crushed core, abrupt dent growth at peak load, and failure on impact above a preload strain.
- **The threats.** The design hail (50.8 mm at 32.0 m/s, 32.1 J) crushes about 81 mm and dents 0.39-5.4 mm. On the Shi-calibrated and all-energy readings that dent grows, a local collapse at the 500 m pressure; on the simply supported edge it grows on all three. So do hail from about 45 mm (35 mm on the simply supported edge), birds struck in flight, the 135.6 J tool drop, and any mooring contact.
- **Contact.** A 0.5 m contact at 0.914 m/s crushes through the core.

**P3 (022d, SiC frame and Zylon film):**
- **Tubes.** The design hail breaks a tube with probability 0.011-0.053 a strike, on the sourced tube strengths.
- **One lost member.** Its neighbours carry up to 1.54 times the axial force and 2.4-3.3 times the peak stress, with up to 947 MPa of wall tension. That breaks SiC, so the frame cascades. The film over the two bays it leaves goes to SF 0.84.
- **The film.** At 1.38 GPa a puncture runs once its half-length passes 0.007-1.91 mm.
- **A torn bay.** It fills the hull in seconds, and P3 hits the ground at 23-35 m/s.

**A puncture does not push either hull past its pressure, beyond the weather.** As air comes in, the hull sinks to a lower float level. Floating neutrally, the pressure difference is M R T / V at any altitude, so the descent adds only ISA's warmer air: 1.1 percent at sea level. P2, at SF 1.000, has no margin for that, as it has none for a 3 K warmer day (031).
- **Holes up to about 63 mm** land P2 under TAR 473's 0.914 m/s.
- **Holes of 130-147 mm** match the 4.2 m/s of 14 CFR 31's 36 in drop.
- **A 0.3 m hole** lands at 8.6-11.4 m/s.

**What must move.** P2's float margin is 14.6 kg (11.6 g/m2). The structural fixes it needs do not fit:
- A face that bridges the design hail's 81 mm zone is past the budget's cliff: 59 mm already reads usage 1.35.
- The design hail needs 0.58-1.76 MPa of crush, a core about 1.7-3.3 times denser. A core 1.5 times denser already reads usage 1.62, and 3 times reads 3.98.
- A 25 kg shield reads 1.021.

P3's structural fixes fail as well:
- A tear-stopping film reads SF 0.88-0.98.
- 1.5 mm tube walls read 0.80.
- Each 100 kg of protection costs 0.039 of P3's 1.258.

The operating fix for P2: before hail, vent to 46 percent of the design pressure difference. That admits about 2646 kg of air, roughly 10 minutes through a 200 mm valve, and the hull must be held down. P3 needs a hangar.

## 1. The threats

Hail, from the IEC 61215-2 ice-ball table, with the masses that table does not print taken at its own 25 mm ball's density (920 kg/m3):

| Ice ball | Velocity | Mass | Energy | rho v^2 |
|---|---|---|---|---|
| 25 mm | 23.0 m/s | 7.5 g (IEC table) | 2.0 J | 0.49 MPa |
| 35 mm | 27.2 m/s | 20.7 g (IEC 25 mm density) | 7.6 J | 0.68 MPa |
| 45 mm | 30.7 m/s | 43.9 g (IEC table) | 20.7 J | 0.87 MPa |
| 55 mm | 33.9 m/s | 80.2 g (IEC 25 mm density) | 46.1 J | 1.06 MPa |
| 65 mm | 36.7 m/s | 132.3 g (IEC 25 mm density) | 89.1 J | 1.24 MPa |
| 75 mm | 39.5 m/s | 203.0 g (IEC table) | 158.4 J | 1.44 MPa |

- **The design hail** is NBSIR 82-2487's 2 in ice ball at terminal velocity: 32.0 m/s, 32.1 J. SPC's severe-hail line is 1 in (25.4 mm). A 66 ft/s wind takes a 2.5 in stone to 40.8 m/s.
- **Birds:** 14 CFR 25.571(e)(1)'s 4 lb (1.81 kg) and 25.631's 8 lb (3.63 kg). Geese and ducks fly at 15-20 m/s (Alerstam). A moored hull meets a bird at that speed; flying at 037's VB it adds 18.0 m/s:
  - 4 lb: 363 J moored, 1310 J flying;
  - 8 lb: 726 J moored, 2621 J flying.

  71 percent of transport-aircraft bird strikes are at or below 500 ft, and they fall 35 percent per 1000 ft above it.
- **Handling and tool drops:** Boeing's small drop 5.4 J and BVID cut-off 135.6 J, both with a 1 in hemisphere. Airbus gives 35 J for a typical area. The CMH-17 civil survey's upper energy is 30 J.
- **Mooring contact:** no source gives a mast contact speed. TAR 473's 0.914 m/s landing floor and 14 CFR 25.473's 3.05 m/s descent stand in (PROJECTION). On the hull plus its 0.5 rho V added mass (7334 kg), that is 3.1 and 34.1 kJ.
- **Debris (ASTM E1996):** level A is a 2 g steel ball at 39.6 m/s (1.57 J). Levels D and E are a 9 lb 2x4 at 15.2 and 24.4 m/s (474 and 1214 J).

## 2. P2's response

**The point (028b's nominal AF/scarf least set):**
- faces 0.7946 mm at 300.33 MPa;
- core 23.237 mm;
- gamma needed 0.564164, usage 0.971978.

Its equivalent thickness is t_eq = 41.62 mm (R/t 240). 015b's lambda-1 width (the 1/e radius of a Gaussian dimple) is 357 mm.

**Gamma, by 015's map.** A dimple narrower than lambda 1 is no worse than the lambda-1 curve, and no lower than the plateau at its width.
- **Below lambda 0.631** (a 1/e radius under 225 mm), no depth takes gamma under 0.564.
- **Wider dimples** may reach 16.1 mm (Eq 3 at lambda 1) or 9.3 mm (Lee's envelope over lambda 1-5).
- **Every impact dent below is narrow**, lambda 0.077-0.258, taking the crushed radius as the 1/e radius. Only a mooring contact (lambda 0.70) is wide.

**The dent's growth (this seat's derivation, QUESTIONABLE).** Under a paraboloid dent of depth d and radius b, the face pushes on the core with q0 + 4 (N - N_cr(b)) d / b^2:
- q0 = p - 2N/R = 47.7 kPa is the core's share on the undamaged shell;
- N = 238.7 kN/m;
- N_cr(b) = lam^2 D / b^2 is the patch's own buckling force, with D = 12.19 N m.

The core resumes crushing when that exceeds 0.241 MPa. No dent narrower than 54.8 mm (clamped) or 27.1 mm (simply supported) grows at any depth. Wider dents grow past:

| Dent diameter | Grows past (clamped) | Grows past (simply supported) | Gamma limit |
|---|---|---|---|
| 40 mm | no growth | 0.15 mm | none |
| 55 mm | deeper than the core | 0.20 mm | none |
| 60 mm | 1.09 mm | 0.23 mm | none |
| 80 mm | 0.61 mm | 0.37 mm | none |
| 100 mm | 0.72 mm | 0.55 mm | none |
| 160 mm | 1.47 mm | 1.33 mm | none |
| 300 mm | 4.71 mm | 4.59 mm | none |
| 700 mm | deeper than the core | deeper than the core | 16.1 mm |
| 1000 mm | deeper than the core | deeper than the core | 9.3 mm |

On the minimum crush (the 20 percent scatter Hexcel states), thresholds are 25 percent lower; at 80 mm, 0.46 mm clamped.

**The dents (this seat's model, QUESTIONABLE).** The face membrane works at 2 pi sigma0 t_f d, with sigma0 = 345 MPa. The core crushes over b = a + (t_f/2) sqrt(sigma0/sigma_c), where a is the contact radius.

The model is checked against two sources:
- **Pach's test:** 1.57 J with a 1 in hemisphere on 0.508 mm 2024-T3 dents 1.1-1.2 mm, about 30 mm across. Pach's core crush is not printed, so it is taken at 0.4-0.9 MPa (PROJECTION). The model gives 1.49-1.54 mm peak and 22-27 mm.
- **Clarke's finite elements:** on the same 16 kg/m3 3/8 in core, the FE gives 1.9 times the model's depth. Core damage width equals dent width (slope 1.05).

Hail is read three ways:
- **Fluid:** the ice presses at rho v^2.
- **Shi-calibrated:** at 2.16 rho v^2, from Shi et al.'s own plastic work (6.55 percent) and dent (0.48 mm) for 50.8 mm ice on a 3 mm plate.
- **All energy:** the whole kinetic energy goes into the panel.

A polymer-core aluminium panel dented under 40-50 mm ice and not under 30 mm, which the Shi-calibrated reading matches.

| Threat | Reading | Dent depth | Crushed diameter | Clamped | Simply supported |
|---|---|---|---|---|---|
| hail 25.0 mm at 23.0 m/s | fluid rho v2 | 0.00 mm | 0 mm | no crush | no crush |
| hail 25.0 mm at 23.0 m/s | Shi-calibrated k rho v2 | 0.00 mm | 0 mm | no crush | no crush |
| hail 25.0 mm at 23.0 m/s | all energy to the panel | 1.22 mm | 55 mm | stable | grows |
| hail 35.0 mm at 27.2 m/s | fluid rho v2 | 0.00 mm | 0 mm | no crush | no crush |
| hail 35.0 mm at 27.2 m/s | Shi-calibrated k rho v2 | 0.36 mm | 65 mm | stable | grows |
| hail 35.0 mm at 27.2 m/s | all energy to the panel | 2.55 mm | 65 mm | grows | grows |
| hail 45.0 mm at 30.7 m/s | fluid rho v2 | 0.18 mm | 75 mm | stable | stable |
| hail 45.0 mm at 30.7 m/s | Shi-calibrated k rho v2 | 1.11 mm | 75 mm | grows | grows |
| hail 45.0 mm at 30.7 m/s | all energy to the panel | 4.32 mm | 75 mm | grows | grows |
| hail 50.8 mm at 32.0 m/s | fluid rho v2 | 0.39 mm | 81 mm | stable | grows |
| hail 50.8 mm at 32.0 m/s | Shi-calibrated k rho v2 | 1.68 mm | 81 mm | grows | grows |
| hail 50.8 mm at 32.0 m/s | all energy to the panel | 5.43 mm | 81 mm | grows | grows |
| hail 75.0 mm at 39.5 m/s | fluid rho v2 | 2.47 mm | 105 mm | grows | grows |
| hail 75.0 mm at 39.5 m/s | Shi-calibrated k rho v2 | 6.74 mm | 105 mm | grows | grows |
| hail 75.0 mm at 39.5 m/s | all energy to the panel | 12.40 mm | 105 mm | grows | grows |
| Boeing small tool drop, 5.4 J, 25.4 mm hemisphere | 80 percent absorbed (depth x2 band) | 2.1-4.2 mm | 44 mm | stable | grows |
| Airbus typical area, 35.0 J, 25.4 mm hemisphere | 80 percent absorbed (depth x2 band) | 5.5-11.0 mm | 51 mm | stable | grows |
| Boeing large tool drop (BVID cut-off), 135.6 J, 25.4 mm hemisphere | 80 percent absorbed (depth x2 band) | 11.0-21.9 mm | 55 mm | grows | grows |
| bird 1.81 kg at 20.0 m/s (moored, bird's own speed) | fluid rho v2 | 0.4 mm | 184 mm | stable | stable |
| bird 1.81 kg at 20.0 m/s (moored, bird's own speed) | all energy to the panel | 17.1 mm | 184 mm | grows | grows |
| bird 1.81 kg at 38.0 m/s (flying at 037's VB into the bird) | fluid rho v2 | 11.1 mm | 184 mm | grows | grows |
| bird 1.81 kg at 38.0 m/s (flying at 037's VB into the bird) | all energy to the panel | 23.2 mm (through the core) | 184 mm | grows | grows |
| mooring contact at 0.914 m/s (TAR 473 landing floor), 0.5 m contact | core crush only | through the 23.2 mm core | 500 mm | grows | grows |

**Notes on the dents:**
- **The design hail grows on two of three readings (clamped).** It grows on all three on the simply supported edge. The fluid reading's 0.39 mm sits under its 0.61 mm threshold.
- **Small threats:** 25 mm hail does not crush the core on the pressure readings. Tool drops to 35 J leave crushed zones under 54.8 mm, so they are stable on the clamped edge.
- **Mooring contact:** at 0.914 m/s it crushes through the core over 0.5 m (lambda 0.70, gamma limit 16.1 mm). That is a global collapse. A 9.3 mm crush over a lambda-1 patch needs only 0.50 m/s.
- **Face cracking:** the dents' membrane strain reaches 0.9 percent for the design hail and 2.8 percent for 75 mm, against SR-200's 10 percent uniaxial minimum. Beryllium's impact resistance is "extremely low" (NASA 1971, block), and no thin-sheet impact test was found. A cracked outer face leaks into the core cells (NFI).

**The largest undetected dent that keeps SF 1.** Any dent narrower than 54.8 mm (clamped) or 27.1 mm (simply supported) keeps SF 1, until its face cracks. A wider dent must be shallower than the growth threshold above:
- 0.61 mm at 80 mm across;
- 1.47 mm at 160 mm;
- 4.7 mm at 300 mm.

Only dents at least 0.45 m across are held by gamma (16.1 / 9.3 mm). The thresholds from 60 to 160 mm across (0.23-1.47 mm) sit at or under the BVID depths: Boeing 0.25, NPL 0.5 and NASA 1.27 mm. P2 cannot accept a barely visible dent of that width.

## 3. P3's response

**The point (022d's best equilateral screened, Zylon/CFRP, cap, 5 percent reserve)** is reproduced exactly: SF 1.258252477 at s 3.1708 m.
- **Tubes:** OD 275.1 mm, wall 1.1374 mm, member force 873.8 kN (0.893 GPa).
- **Film:** 1.383 GPa on total gauge. Each ply's fibres sit at 48 percent of Zylon's 5.8 GPa.
- **Exposure:** tubes cover 30 percent of the projected surface.

**A tube struck by hail.** The wall is taken as a shallow shell on its own membrane foundation (characteristic length 6.8 mm). It bends 55.5 MPa per MPa of ice contact pressure over a 12 mm contact. Weibull failure on the sourced Hexoloy tube data: C-ring 299 MPa, m 4.6; sectored flexure 192 MPa, m 5.5.

| Ice ball | Wall stress, fluid / Shi-calibrated | Fracture per strike (Shi-calibrated) | Strikes to a 50 percent chance |
|---|---|---|---|
| 25.0 mm at 23.0 m/s | 27 / 58 MPa | 0.0005-0.0014 | 484-1272 |
| 35.0 mm at 27.2 m/s | 38 / 82 MPa | 0.0025-0.0090 | 77-272 |
| 45.0 mm at 30.7 m/s | 48 / 104 MPa | 0.0077-0.0337 | 21-90 |
| 55.0 mm at 33.9 m/s | 59 / 127 MPa | 0.0191-0.0971 | 7-36 |
| 65.0 mm at 36.7 m/s | 69 / 149 MPa | 0.0393-0.2169 | 3-18 |
| 75.0 mm at 39.5 m/s | 80 / 172 MPa | 0.0759-0.4224 | 2-9 |
| 50.8 mm at 32.0 m/s | 52 / 113 MPa | 0.0113-0.0528 | 13-61 |

A storm puts many stones on the tubes' 30 percent of the upper projected area (no hail flux was sourced). So hail of 45 mm and over breaks members.

A tool drop is worse. GE/NASA (CR-134990) broke a 9 mm SiC plate catastrophically with a 0.67 J steel ball. The tube wall is 1.14 mm, and ASTM E1996's level A ball carries 1.57 J. Birds and timber on the tubes are not scored (NFI).

**One lost member: a linear frame screen** on frequency-4 and -5 geodesics with rigid joints and 022d's section.
- **f4:** mean edge 2.98 m, intact compression 734-861 kN against pRs/(2 sqrt 3) = 822 kN.
- **f5:** mean edge 2.39 m.

Removing one member does three things:
- **Axial:** the neighbours' axial force rises up to 1.30 times, and up to 1.54 anywhere.
- **Bending:** the bending moments jump from about 3 to 64-129 kN m.
- **Stress:** the peak wall stress rises 2.43-3.27 times, with far-face tension of 138-947 MPa against SiC's 160-320 MPa tensile range.

With pinned joints the frame becomes a mechanism (condition number 1e17). P3 is not single-member tolerant; one lost tube cascades.

The film over the 60-degree rhombus the two bays become spans 1.5 times the inradius. At the same rise-to-span its tension rises in proportion, and the film goes from SF 1.258 to 0.839 (PROJECTION).

**Film puncture and tear.** A slit runs once its half-length passes E G_c / (pi sigma^2). No Zylon film modulus or toughness was sourced. With a projected 81-180 GPa, and the toughness of other polymer films, the critical half-length is:
- 0.007 mm on StratoFilm's 500 J/m2;
- 0.08-0.17 mm on Kapton's Elmendorf tear;
- 0.54-1.91 mm on Mylar's essential work of fracture.

Any puncture runs the bay open. ILC Dover set 8 m as the Kapton sail's ripstop limit and called Kapton's tear resistance "extremely low".

Holding the film under a stress that stops a 50 mm hole (Mylar's toughness) means:
- 204-304 MPa;
- 881 kg of film;
- P3 at SF 0.885-0.975.

Zylon also keeps only 35 percent of its strength after six months of daylight.

## 4. Puncture and leak

**Inflow** is choked through a sharp-edged hole (Cd 0.6). For a hole that does not grow:

| Hole | Inflow | 48.9 kg (019's internal-gas item) | 244 kg (P3's 5% reserve) | 411 kg (019's whole reserve) | P2 lands after | at |
|---|---|---|---|---|---|---|
| 1 mm | 0.108 g/s | 126.09 h | 630.47 h | 1060.71 h | 606.99 h | 0.00 m/s |
| 3 mm | 0.969 g/s | 14.01 h | 70.05 h | 117.86 h | 67.44 h | 0.00 m/s |
| 10 mm | 10.771 g/s | 1.26 h | 6.30 h | 10.61 h | 6.07 h | 0.02 m/s |
| 30 mm | 96.940 g/s | 0.14 h | 0.70 h | 1.18 h | 0.68 h | 0.21 m/s |
| 100 mm | 1077.109 g/s | 0.01 h | 0.06 h | 0.11 h | 0.07 h | 2.29 m/s |

**No implosion from the leak itself.** The hull is a fixed volume: as air comes in, its float level falls, and air keeps entering. At neutral buoyancy the pressure difference is (non-air mass) R T / V at any altitude, so the descent itself adds nothing but ISA's warmer air: a peak of 1.0110 of the 500 m difference near the ground.

At 028b's point that is SF 0.989, the same as a 3.1 K warmer day (031). Faster holes make the hull heavy before it falls, so the difference only drops.

**Tear modes:**
- **P3:** yes. The film runs.
- **P2:** the face at a hole's edge reads 601 MPa elastic (factor 0.57 on 345 MPa). It yields out to 3.9 hole radii, and whether that edge crumples further is not modelled (NFI).

**Touchdown speed against hole size** (P2, drag 0.2-0.47):
- under TAR 473's 0.914 m/s floor up to a 63-66 mm hole;
- the 4.2 m/s of 14 CFR 31.27(c)'s 36 in drop at 130-147 mm;
- 8.6-11.4 m/s for a 0.3 m hole;
- 21-28 m/s for 1 m.

A torn P3 bay (4.35 m2) lands in 23-29 s at 23-35 m/s, about 5131 kg heavy.

**What the hull carries to land.** A vacuum hull lands by taking air in:
- **Ballast air:** 242 kg to reach sea level neutral.
- **An air-admission valve** that keeps the internal pressure up with the descent:
  - 70 mm for a 0.914 m/s descent;
  - 103 mm for 2 m/s;
  - 200 mm for TAR 887(c)'s 7.5 m/s air-induction rate.

Pulling the hull down without that air overloads P2 by 6.1 percent at sea level (038). 14 CFR 101.19 requires a moored balloon to carry a device that rapidly deflates it if it escapes. For a vacuum hull, that is a rapid air valve, and it lands the hull heavy.

TAR 895 asks for disposable ballast to restore equilibrium; a vacuum hull's ballast is its air. 14 CFR 101.13 limits moored balloons to 152.4 m above the surface, below the 500 m design point (NFI).

## 5. Detection

- **P2's critical damage:** a crushed zone over 27-55 mm across under a dent of 0.15-1.1 mm. That is at or under BVID.
  - Tap testing finds disbonds of 29 mm (automated) or 41.8 mm (manual) at 90/95 on 0.5 mm aluminium. Its sensitivity falls with face thickness; this face is 0.795 mm beryllium.
  - A shallow print can hide a large crush. A disbond can let the face relax.
  - Laser topography resolves 0.2 mm contours.
  - No limit was found for ultrasound, thermography or shearography on metal faces.
- **Leaks:** an internal pressure gauge finds a 0.36 mm hole in an hour at 1 Pa, and a 0.11 mm hole at 0.1 Pa, against the 016/034 monitoring.
- **P3:** no tube or film inspection limit was sourced.

**Detection cannot catch growth in time.** A dent that will grow does so at once, under load. A film tear runs in seconds. So inspection only finds stable damage, before the next load excursion (a +10 K day adds 4.4 percent, 031). It must be event-driven:
- an impact-sensor network (sources show location and energy) to flag the event;
- then a laser profile and an automated tap or thermography survey of the struck area, from a drone or robot at 500 m;
- with internal pressure logged continuously.

A 1257 m2 hull at 500 m has no inspection access today (NFI).

## 6. The requirement and its cost

**P2** must keep every dent from growing under the 500 m load: a crushed zone below 54.8 mm or a dent below the growth threshold. On its own budget:
- **Face** to bridge a crushed patch:
  - 54.8 mm (clamped) costs usage 0.9734;
  - 59 mm reads 1.35;
  - simply supported, 29.3 mm reads 1.37.
  - The design hail's 81 mm cannot be bridged.
- **Core:** the design hail needs 0.58 MPa crush (Shi-calibrated) or 1.76 MPa (all energy). A core 1.5-3 times denser (crush scaled by k^5/3, PROJECTION) reads usage 1.62-3.98.
- **Shield:** P2's margin is 14.6 kg. 25 kg reads 1.021, 100 kg 1.184.
- **Operating:** vent to 46 percent of the design difference before hail. About 2646 kg of air goes in, and the hull is held down heavy. Touch nothing while evacuated; contact at 0.5 m/s over a lambda-1 patch already passes gamma's limit.

**P3** must lose no member and no film. On its own budget:
- **Tube walls:** 1.5 mm reads SF 0.800 and 2 mm 0.469.
- **Tear-stopping film:** SF 0.885-0.975.
- **Single-member tolerance:** 2.4-3.3 times the wall stress; not available.
- **Protection:** 100 kg costs 0.039 of SF, and its protective value is unquantified.

Venting does not protect the tubes from hail; P3 needs a hangar before hail and no handling contact.

For both leads, the damage-tolerance requirement is a shelter-or-vent protocol, an air valve, and event-driven inspection, not mass. The cost is a ground facility, and the leads' gamma and SF stay as filed only while nothing hits them.

## Method and checks

This seat's own code:
- **dt45.py:** 015's map, the face patch, holes and descent, the geodesic frame, the shell under a disc load, and the dent models.
- **det45.py:** the deterministic half.
- **p3_022d.py:** 022d's P3 point and a local re-optimiser, from 022d's METHOD.
- **price45.py:** 028b's least set, through 037b's replica, with an added mode.
- **run45.py and card45.py.**

**Reproduction checks.** 10 pass:
- 028b's usage 0.971978, gamma 0.564164, wrinkle 0.434628, face 0.794624 mm, core 23.2372 mm;
- 022d's SF 1.258252477, tubes 4183.590023 kg, film 214.541558 kg, joints 44.191468 kg, sag 99.720419 kg.

**Map and flow checks:**
- 015b's map reproduces its beryllium and 021/021b amplitudes (2.360, 1.499, 11.801, 7.079, 45.82 mm).
- The choked inflow reproduces 016's 2.48 mm2 hole for 48.894 kg a day.
- The disc-load moment matches Timoshenko's small-load formula to 0.02 percent.

Every sourced value is drawn from the sourcing files by property and product, and asserted.

## Then

Stop and file. The robotics seat sends the next job. NFI.json carries the open rows. A checker runs behind this card.
