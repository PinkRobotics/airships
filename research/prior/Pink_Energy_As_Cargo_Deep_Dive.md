# Energy as Cargo

> Dated concept study, 2026-08-09; retained as written. See the [current float ledger](../../docs/FLOAT-LEDGER.md).
## A technical concept report on standardized battery exchange, autonomous energy tenders, and grid-connected airship base stations

**Project:** Pink Robotics autonomous vacuum-airship network  
**Date:** 2026-08-09  
**Status:** Conceptual systems study; not an engineered design, cost estimate, certification basis, or assertion of available electrical capacity

---

## Executive conclusion

For the British Columbia reference deployment, the strongest primary energy architecture is:

> **Clean grid electricity → standardized charged battery modules at ground depots → P-E1000 regional energy shuttles and P-E10000 mobile energy buffers → mass-balanced battery exchange with working water airships.**

This choice is **not** based on batteries having the highest energy density. They do not. Dense liquid fuel can provide much more useful energy per kilogram. Battery exchange is preferred for the initial B.C. story because it fits the rest of the proposed machine unusually well:

1. The airships are already electric at the actuator and machinery level.
2. B.C. has an unusually low-carbon hydro-dominated grid.
3. A charged battery and the same discharged battery have effectively identical mass.
4. Permanent vacuum buoyancy can therefore be designed around a nearly invariant battery payload.
5. Energy can be exchanged by moving precharged physical modules rather than electrically fast-charging an aircraft.
6. The ground depot can charge slowly, inspect continuously, hold reserve inventory, and swap quickly.
7. The same standardized energy module can circulate across ground stations, P-E1000 shuttles, P-E10000 buffers, and working vehicles.
8. Every return to infrastructure becomes an automatic inspection and health-classification event.
9. Solar can materially extend the endurance of very large, slow, wind-aware energy carriers.
10. Liquid nitrogen remains available for **mass control and ballast**, rather than being burdened with the entire energy-logistics role.

The architecture’s main weakness is equally clear:

> **Mechanical swapping removes aircraft charging delay; it does not remove conservation of energy, battery capital, grid demand, or the physical mass flow of battery inventory.**

A regional fleet consuming 400 MW continuously still requires roughly 471 MW of average grid input at an 85% grid-to-delivered-bus efficiency, before tender propulsion and station overhead. If the module loop takes six hours and the system maintains a 20% reserve, approximately 3.6 GWh of nameplate battery inventory is required at an 80% usable depth of discharge. At specialized-module costs of US$150–500/kWh, that inventory alone represents roughly US$540 million to US$1.8 billion.

The architecture is therefore credible as **large infrastructure**, not as an inexpensive accessory to the airship.

---

# 1. The system in one diagram

```text
B.C. HYDRO / OTHER CLEAN GRID
             │
             ▼
┌───────────────────────────────────────────────┐
│ PINK ENERGY DEPOT                             │
│                                               │
│ depleted → cool → inspect → charge → reserve │
│     ▲                                   │     │
│     └──────── automated magazines ──────┘     │
└───────────────────────────────────────────────┘
             │ charged for depleted
             ▼
      P-E1000 REGIONAL SHUTTLE
             │
             ├───────────────► working P-100 / P-1000 / P-10000
             │                    water airships
             │
             ▼
      P-E10000 REGIONAL BUFFER
      / global-roaming energy node
```

A working airship need not “plug in” at gigawatt power. It operates from modules already connected to its segmented electrical buses. When a tender arrives, charged modules enter while depleted modules leave at approximately the same rate and in symmetric positions.

The energy transfer is therefore:

```text
charged physical module → recipient module bay → recipient bus
depleted physical module ← recipient module bay ← tender
```

not:

```text
tender battery → enormous airborne charger → recipient battery
```

The distinction is fundamental.

---

# 2. Why charged and discharged battery cargo is mass invariant

Stored electrical energy does add mass through \(E=mc^2\), but the difference is operationally negligible.

A 2.7 GWh P-E10000 battery inventory contains:

\[
E = 2.7\times10^9\ \mathrm{Wh}\times3600
  = 9.72\times10^{12}\ \mathrm{J}
\]

and therefore a charged-versus-discharged relativistic mass difference of:

\[
\Delta m = \frac{E}{c^2}
\approx 1.08\times10^{-4}\ \mathrm{kg}
\]

or about **0.108 grams**.

Against 9,000 tonnes of battery cargo, this is zero for flight-control purposes.

That permits a P-E1000 or P-E10000 to be designed around a fixed cargo mass:

- charged batteries aboard: nominal mass;
- depleted batteries aboard: nominal mass;
- modules being exchanged in matched pairs: nominal mass;
- energy state changes: virtually no buoyancy change.

This is uniquely attractive for a vacuum-lift vehicle.

## 2.1 Design consequences

The permanent vacuum displacement can offset:

- dry structure;
- permanent machinery;
- reserve battery bank;
- a fixed number of standard-mass energy modules;
- handling mechanisms;
- defined consumables and margins.

A vehicle should never depend on every module being present. Missing or quarantined modules must be replaced by:

- another same-mass module;
- an inert standard-mass carrier;
- water or LN₂ trim;
- or another controlled ballast state.

The system must standardize **gross handled mass**, not merely battery chemistry.

---

# 3. Standard energy units

A useful hierarchy is:

## 3.1 Pink Energy Module (PEM)

A **PEM** is the smallest independently isolated, identified, cooled, monitored, and replaceable flight unit.

Reference starting point:

- gross handled mass: **1 tonne**;
- installed specific energy baseline: **300 Wh/kg**;
- nameplate energy: **300 kWh**;
- usable depth of discharge: **80%**;
- nominal usable energy: **240 kWh**.

One tonne is not a final engineering answer. It is a useful systems-model unit because it is:

- small enough to isolate damage;
- large enough to avoid tracking individual cells during fleet operations;
- compatible with robotic handling;
- divisible into larger magazines;
- manageable in inspection and maintenance lines.

## 3.2 Pink Energy Magazine (PEM-G)

A **magazine** mechanically groups several PEMs for rapid exchange.

Reference starting point:

- 5 PEMs;
- gross mass: **5 tonnes**;
- nameplate energy: **1.5 MWh** at 300 Wh/kg;
- usable energy: **1.2 MWh** at 80% depth of discharge.

The site should allow 1-, 5-, 10-, and 20-tonne exchange units as sensitivities.

## 3.3 Standardize the interface, not one chemistry forever

The common standard should define:

- external geometry;
- gross mass tolerance;
- structural rails and latches;
- robotic grapple points;
- blind-mate electrical contacts;
- precharge and contactor behavior;
- cooling couplings;
- vent routing;
- data/identity interface;
- insulation and isolation tests;
- fire-containment boundary;
- inspection fiducials;
- service and recycling information.

Different modules can then be optimized for different duties:

| Module family | Priority | Possible role |
|---|---|---|
| PEM-H | high specific energy | long-range energy transport |
| PEM-P | high power | actuator bursts and emergency control |
| PEM-L | long life / lower cost | high-cycle tender and depot circulation |
| PEM-S | maximum safety | populated-area or fire-proximity service |
| PEM-2L | second life | stationary depot buffering |

A 175 Wh/kg, 10,000-cycle sodium-ion product claim and a 300 Wh/kg aviation-oriented pack assumption illustrate the trade: **maximum energy density may not minimize lifetime cost**. The simulation should make chemistry a configurable fleet resource, not a cosmetic label.

---

# 4. Reference energy-carrier classes

The existing nomenclature can be extended:

- **P-E1000:** regional energy shuttle;
- **P-E10000:** strategic energy buffer, long-range carrier, and regional distribution node.

Assume 90% of the nominal payload allocation is battery modules. The remaining 10% covers magazines, rails, thermal systems, handling equipment, isolation, and operational margin. This is a modeling convention, not a completed mass ledger.

## 4.1 Energy inventory by installed specific energy

### P-E1000 — 900 tonnes of battery modules

| Installed specific energy | Nameplate inventory | Usable at 80% DoD |
|---:|---:|---:|
| 200 Wh/kg | 180 MWh | 144 MWh |
| 250 Wh/kg | 225 MWh | 180 MWh |
| **300 Wh/kg baseline** | **270 MWh** | **216 MWh** |
| 400 Wh/kg | 360 MWh | 288 MWh |
| 500 Wh/kg | 450 MWh | 360 MWh |

### P-E10000 — 9,000 tonnes of battery modules

| Installed specific energy | Nameplate inventory | Usable at 80% DoD |
|---:|---:|---:|
| 200 Wh/kg | 1.8 GWh | 1.44 GWh |
| 250 Wh/kg | 2.25 GWh | 1.80 GWh |
| **300 Wh/kg baseline** | **2.70 GWh** | **2.16 GWh** |
| 400 Wh/kg | 3.60 GWh | 2.88 GWh |
| 500 Wh/kg | 4.50 GWh | 3.60 GWh |

The 500 Wh/kg line is an advanced sensitivity, not a mature complete-module assumption. NASA’s aviation work repeatedly emphasizes that pack-level specific energy is lower than cell-level performance once structure, cooling, containment, wiring, and controls are included.

## 4.2 What that energy means

A baseline P-E10000 with 2.16 GWh of usable energy can theoretically support:

| Net average draw | Endurance before solar |
|---:|---:|
| 5 MW | 18.0 days |
| 10 MW | 9.0 days |
| 20 MW | 4.5 days |
| 40 MW | 2.25 days |
| 100 MW | 21.6 hours |
| 400 MW | 5.4 hours |

This table reveals two different identities:

1. **Self-propelled roaming vehicle:** multi-day or multi-week endurance is plausible if average draw is kept low.
2. **Regional power distributor:** a large fleet can drain the same inventory in hours.

The website must distinguish those modes.

---

# 5. P-E10000 as a global-roaming vehicle

Neutral buoyancy eliminates the need to spend propulsion energy continuously supporting weight. It does **not** eliminate drag, crosswind control, hotel loads, thermal management, or actuator use.

The P-E10000 can nevertheless exploit several favorable properties:

- travel slowly when urgency is low;
- use altitude-dependent wind fields;
- drift instead of station-keeping;
- schedule motion around weather;
- preserve battery energy for high-value maneuvers;
- harvest solar energy over a very large upper surface;
- remain aloft without airport visits;
- exchange modules without changing gross mass.

## 5.1 First-order solar envelope

For the illustrative 821 m × 205 m same-proportion geometry, the projected top ellipse is about:

\[
A_{\text{top}}\approx132,000\ \mathrm{m^2}
\]

A conservative conceptual calculation using:

- 70% active coverage;
- 22% module efficiency;
- 90% electrical/orientation derate;
- 1,000 W/m² reference irradiance;

gives:

\[
P_{\text{PV,peak}}\approx18.3\ \mathrm{MW}
\]

Gross full-area calculations at 20–25% efficiency yield approximately 26–33 MW peak, but 18 MW is a more responsible website baseline.

Real average output will be much lower and depends on:

- latitude;
- season;
- time of day;
- cloud;
- smoke;
- orientation;
- cell temperature;
- curvature and shading;
- maintenance and damage.

Solar should be modeled as an endurance extender and safe-drift resource, not as guaranteed propulsion power.

## 5.2 First-order axial drag sensitivity

For an illustrative frontal area of about 33,000 m², air density 1.225 kg/m³, propulsive efficiency 75%, and effective axial drag coefficient 0.05:

| Airspeed | Idealized propulsive power |
|---:|---:|
| 18 km/h | 0.17 MW |
| 36 km/h | 1.35 MW |
| 54 km/h | 4.55 MW |
| 72 km/h | 10.78 MW |
| 90 km/h | 21.06 MW |
| 108 km/h | 36.39 MW |

A plausible \(C_d\) sensitivity of 0.03–0.08 changes the 72 km/h result to approximately 6.5–17.3 MW.

These values are **not predictions**. They omit:

- crosswinds;
- station-keeping;
- gust response;
- rotor/hull interference;
- control power;
- weather deviation;
- structural deformation;
- thermal and hotel loads.

They are useful because they demonstrate the cubic speed penalty. A strategic energy carrier can gain tremendous endurance by accepting a slow arrival and sailing through favorable winds.

---

# 6. Exchange mechanics

## 6.1 “Purely mechanical” means no high-rate battery-to-battery recharge

The central benefit is that stored energy crosses the interface inside physical modules. It does not mean the process has no electrical or data operations.

Every swap still needs:

- bus isolation;
- contactor opening;
- residual-voltage verification;
- mechanical unlatching;
- paired mass movement;
- structural locking;
- coolant connection;
- identity and health handshake;
- insulation test;
- precharge;
- bus synchronization;
- contactor closure;
- post-connection verification.

The energy **inventory transfer** is mechanical. The newly installed module still connects electrically to the receiving vehicle.

## 6.2 Paired, symmetric, mass-balanced exchange

The default transfer should be:

```text
PORT SIDE                         STARBOARD SIDE

charged magazine  ─────► recipient ◄───── charged magazine
depleted magazine ◄───── recipient ─────► depleted magazine
```

Charged and depleted magazines move simultaneously through opposing ports near the combined center of mass.

Benefits:

- gross mass remains nearly constant;
- center of gravity remains bounded;
- bending moments are predictable;
- no large transient buoyancy step occurs;
- the donor and recipient can plan the exchange as one coupled system.

## 6.3 Segmented recipient banks

Every working vehicle should have at least two electrically independent energy banks.

Example:

1. Bank A powers the aircraft.
2. Bank B is isolated and exchanged.
3. New Bank B is verified and synchronized.
4. Load transfers to B.
5. Bank A becomes available for exchange.

No exchange operation should remove the only active source of flight-control power.

## 6.4 Air-to-air rendezvous

The exchange should occur:

- outside the fire convection area;
- in a relatively calm forecast layer;
- on a known segment of the recipient’s route;
- under a strict relative-motion envelope;
- with deterministic collision and structural limits;
- with automatic abort capability.

The vehicles temporarily become one coordinated control problem.

The connection may ultimately use:

- soft capture;
- load-sharing trusses;
- robotic transfer bridges;
- flexible alignment stages;
- multiple parallel magazine paths.

It should not be portrayed as two fragile hulls simply touching.

## 6.5 Ground exchange

A ground station can move modules through:

- robotic elevators;
- gantries;
- suspended transfer bridges;
- vertical conveyors;
- smaller module-handling aircraft.

The large airship may remain above the ground, as it remains above the lake. The exact ground interface is open research.

---

# 7. Gigawatt-equivalent exchange

Use the term:

> **GW-equivalent module-transfer rate**

or:

> **GWh of stored energy exchanged per hour**

Do not use “GW per hour.”

For a 5-tonne magazine containing 1.5 MWh nameplate and 1.2 MWh usable energy:

\[
P_{\text{equiv}}=
\frac{N_{\text{ports}}\times E_{\text{mag}}\times3600}
{t_{\text{swap}}}
\]

## 7.1 Example rates

| Paired ports | Seconds per magazine | Nameplate GWh/h | Usable GWh/h |
|---:|---:|---:|---:|
| 4 | 60 | 0.36 | 0.288 |
| 4 | 30 | 0.72 | 0.576 |
| **8** | **30** | **1.44** | **1.152** |
| 16 | 30 | 2.88 | 2.304 |
| 32 | 30 | 5.76 | 4.608 |
| 16 | 10 | 8.64 | 6.912 |

An 8-port, 30-second target therefore represents **1.44 GW equivalent nameplate transfer** without a 1.44 GW electrical charging connector.

## 7.2 Complete cargo exchange time

With 5-tonne magazines:

- P-E1000 battery cargo: 180 magazines;
- P-E10000 battery cargo: 1,800 magazines.

| Vehicle | Ports | Seconds/magazine | Pure transfer time |
|---|---:|---:|---:|
| P-E1000 | 8 | 30 | 11.25 min |
| P-E1000 | 16 | 30 | 5.63 min |
| P-E10000 | 16 | 30 | 56.25 min |
| P-E10000 | 32 | 30 | 28.13 min |

These times exclude:

- approach and capture;
- alignment;
- safety checks;
- latching and unlatching;
- coolant handling;
- fault retries;
- post-transfer verification;
- separation.

The site should show **mechanical target** and **complete operation time** separately.

## 7.3 The hidden mass-flow problem

At 1.2 MWh usable per 5-tonne magazine:

| Delivered fleet power | Magazines/hour | Battery mass flow |
|---:|---:|---:|
| 40 MW | 33.3 | 167 t/h |
| 100 MW | 83.3 | 417 t/h |
| 300 MW | 250 | 1,250 t/h |
| 500 MW | 416.7 | 2,083 t/h |
| 1 GW | 833.3 | 4,167 t/h |

The mechanical interface can move energy quickly, but a gigawatt-scale network becomes a heavy industrial material-handling system.

That is one of the most important truths to expose on the website.

---

# 8. Ground base station architecture

A Pink Energy Depot is not a large EV charger. It is a transmission-connected battery factory, warehouse, inspection center, robotic cargo terminal, and emergency-energy reserve.

## 8.1 Major zones

1. **Transmission interconnection**
   - customer-owned substation;
   - transformers;
   - protection;
   - metering;
   - power quality;
   - redundant feeds where justified.

2. **AC/DC conversion**
   - multiple isolated converter blocks;
   - sectionalized DC buses;
   - black-start and emergency power;
   - fault-current control.

3. **Arrival and unload**
   - depleted magazine reception;
   - identity verification;
   - temperature and gas screening;
   - damaged-unit diversion.

4. **Cooling and conditioning**
   - modules do not go directly from hard discharge to charging;
   - thermal equalization;
   - coolant service;
   - quarantine triggers.

5. **Inspection**
   - external vision and metrology;
   - thermal imaging;
   - isolation and leakage tests;
   - BMS history;
   - impedance;
   - ultrasound;
   - radiography/CT as appropriate.

6. **Charging**
   - thousands of parallel moderate-rate channels;
   - chemistry-aware profiles;
   - thermal management;
   - grid-aware scheduling.

7. **Charged reserve**
   - mission-ready inventory;
   - strategic reserve;
   - chemistry and health cohorts.

8. **Magazine assembly**
   - load-balanced grouping;
   - known gross mass;
   - known power capability;
   - known mission suitability.

9. **Airship interface**
   - multiple parallel exchange ports;
   - buffers for incoming/outgoing magazines;
   - weather and abort logic.

10. **Quarantine and fire separation**
    - isolated vaults;
    - controlled venting;
    - fire-tested spacing and containment;
    - remote handling.

11. **Repair, second life, and recycling**
    - flight-critical retirement;
    - less-demanding reassignment;
    - stationary use;
    - material recovery.

## 8.2 No single extreme charger is required

A 1-tonne, 300 kWh PEM charged at:

- 0.25C: 75 kW;
- 0.5C: 150 kW;
- 1C: 300 kW.

A depot supplying 400 MW can therefore distribute charging across thousands of independent channels. The aircraft can leave quickly because it takes already charged inventory; the cells can charge at the rate that best balances life, thermal load, and grid conditions.

The station still needs the **average power**. It simply avoids asking one arriving tender to absorb hundreds of megawatts instantly.

---

# 9. Grid quantities

## 9.1 Fundamental power equation

\[
P_{\text{grid}}=
\frac{
P_{\text{recipient fleet}}
+P_{\text{tender flight}}
+P_{\text{station auxiliaries}}
}{
\eta_{\text{grid-to-delivered bus}}
}
\]

At an 85% reference efficiency:

| Useful fleet power | Minimum grid input before tender/auxiliary loads |
|---:|---:|
| 40 MW | 47.1 MW |
| 100 MW | 117.6 MW |
| 300 MW | 352.9 MW |
| 400 MW | 470.6 MW |
| 500 MW | 588.2 MW |
| 1 GW | 1.176 GW |

Battery swapping changes the shape of the load and the turnaround time. It does not change this average-energy requirement.

## 9.2 Inventory equation

A useful Little’s-Law approximation is:

\[
E_{\text{inventory,nameplate}}=
\frac{
P_{\text{delivered}}
\times
T_{\text{module loop}}
\times
R_{\text{reserve}}
}{
D_{\text{usable}}
}
\]

where:

- \(T_{\text{module loop}}\) includes charging, cooling, inspection, outbound travel, exchange, and return;
- \(R_{\text{reserve}}\) is greater than 1;
- \(D_{\text{usable}}\) is usable depth of discharge.

Example:

- useful fleet power: 400 MW;
- complete module loop: 6 h;
- reserve multiplier: 1.20;
- usable DoD: 0.80.

\[
E_{\text{inventory,nameplate}}
=
\frac{400\times6\times1.2}{0.8}
=
3.6\ \mathrm{GWh}
\]

A seven-hour loop raises this to 4.2 GWh.

## 9.3 Station tiers

| Station tier | Grid connection | Representative role |
|---|---:|---|
| Research/pilot | 1–10 MW | module and robotics development |
| Local | 10–50 MW | small operational cluster |
| Regional | 50–200 MW | several P-100-class missions |
| Major wildfire hub | 200–500 MW | sustained regional response |
| Strategic | 500 MW–1+ GW | P-E10000 replenishment / national network |

Current road-vehicle charging standards top out in the low-megawatt range, while NASA’s large electrified-aircraft test infrastructure is around the 12 MW class. A 100–500 MW Pink depot is therefore **transmission-scale industrial infrastructure**, not an extrapolated airport charger.

---

# 10. British Columbia grid context

B.C. is an unusually favorable first geography because BC Hydro reports:

- over 98% of its generation is clean and renewable, overwhelmingly hydro;
- maximum generating capacity of about 13.4 GW after Site C;
- transmission service generally begins at 60 kV and large transmission connections can take years;
- a transmission customer may need to build, own, operate, and maintain its own substation and line.

None of those facts establishes available capacity at a proposed depot.

The website must say:

> **Proximity to a transmission line or substation does not establish spare capacity or permission to connect. Every depot requires a utility interconnection study.**

## 10.1 Current transmission tariff reference

BC Hydro’s default RS 1830 rates effective April 1, 2026 list:

- demand charge: **C$12.178/kVA-month**;
- energy charge: **4.914 cents/kWh**.

At a 90% load factor and approximately unity power factor, the simplified effective input-energy cost is about **C$67.7/MWh**, before tax, riders, connection capital, losses beyond the assumed model, and other tariff conditions.

At 85% grid-to-delivered-bus efficiency, that becomes roughly:

\[
\frac{67.7}{0.85}\approx
\mathrm{C\$79.6/MWh}
\]

delivered to the working fleet before tender flight, battery wear, maintenance, inspection, and capital recovery.

## 10.2 Illustrative 400 MW continuous case

- useful fleet demand: 400 MW;
- grid input at 85%: 470.6 MW;
- monthly input at 730 h: 343.5 GWh;
- simplified RS 1830 energy charge: C$16.88 million/month;
- simplified demand charge: C$5.73 million/month;
- total: **C$22.61 million/month**;
- delivered electricity cost: approximately **C$77.4/MWh**.

This is an arithmetic illustration, not a utility quote.

## 10.3 Connection capital and timing

BC Hydro’s 2026 interconnection workshop materials show 50 MW system-reinforcement scenarios at C$25 million, C$50 million, and C$100 million. These are policy examples, not a formula or project estimate.

The correct website implementation is therefore a range:

```text
connection reinforcement:
user-adjustable conceptual allowance
default: not estimated until site study
```

Do not publish a fictional “available depot” merely because a transmission line is nearby.

---

# 11. Battery capital

## 11.1 Market benchmarks are lower bounds

DOE estimated a mass-produced light-duty EV pack at US$139/kWh usable in 2023. BloombergNEF reported a 2025 global average lithium-ion pack price of US$108/kWh and US$70/kWh for stationary-storage packs.

Pink flight modules would add:

- aerospace-grade structure;
- standardized robotic interfaces;
- mass tolerance;
- containment;
- cooling;
- blind-mate high-voltage connection;
- sensing;
- inspection markers;
- low-volume manufacturing;
- certification;
- maintenance and traceability.

Use market prices as lower bounds, not as Pink module quotes.

## 11.2 Planning scenarios

Use three installed module cost cases:

- optimistic scale: **US$150/kWh**;
- reference: **US$300/kWh**;
- conservative specialized: **US$500/kWh**.

### Vehicle battery inventory

| Asset | Energy | US$150/kWh | US$300/kWh | US$500/kWh |
|---|---:|---:|---:|---:|
| P-E1000 | 270 MWh | $40.5M | $81M | $135M |
| P-E10000 | 2.7 GWh | $405M | $810M | $1.35B |
| 3.6 GWh depot loop inventory | 3.6 GWh | $540M | $1.08B | $1.80B |

Battery inventory is likely to dominate station economics.

---

# 12. Cycle life can dominate electricity cost

Battery depreciation per delivered MWh can be approximated as:

\[
C_{\text{wear}}=
\frac{
C_{\text{pack,\$/kWh}}\times1000
}{
N_{\text{full-equivalent cycles}}\times D_{\text{usable}}
}
\]

At 80% usable depth:

| Module cost | 1,000 cycles | 2,000 cycles | 5,000 cycles | 10,000 cycles |
|---:|---:|---:|---:|---:|
| US$139/kWh | $174/MWh | $87/MWh | $35/MWh | $17/MWh |
| US$200/kWh | $250/MWh | $125/MWh | $50/MWh | $25/MWh |
| **US$300/kWh** | **$375/MWh** | **$188/MWh** | **$75/MWh** | **$38/MWh** |
| US$500/kWh | $625/MWh | $313/MWh | $125/MWh | $63/MWh |

This excludes calendar aging, residual value, maintenance, financing, and recycling.

The implication is important:

> A lower-density, safer, longer-cycle chemistry may move energy more cheaply than the highest-density chemistry.

The fleet optimizer should minimize **lifetime cost, risk, and mission failure probability**, not simply kilograms per kWh.

---

# 13. Inspection and digital twins

The circulating-module architecture provides a major safety advantage: every module repeatedly returns to controlled infrastructure.

## 13.1 Continuous onboard monitoring

Each PEM should record:

- individual cell voltage;
- temperature;
- current;
- estimated state of charge;
- estimated state of health;
- internal resistance;
- pressure/strain;
- gas or vent events;
- coolant conditions;
- vibration and shock;
- insulation resistance;
- connector events;
- thermal excursions;
- complete assignment and handling history.

## 13.2 Every air-to-air exchange

A rapid bridge inspection should verify:

- identity;
- approved configuration;
- temperature;
- voltage window;
- isolation;
- contactor state;
- coolant integrity;
- recent faults;
- external damage;
- destination compatibility.

No deep imaging should be required in the coupled vehicles.

## 13.3 Every ground touch

A ground inspection tunnel should perform:

- machine vision on all external surfaces;
- dimensional/deformation metrology;
- connector and latch inspection;
- thermal imaging;
- insulation/leakage test;
- BMS history download;
- cell voltage and self-discharge analysis;
- impedance or conductance analysis;
- coolant leak and pressure test;
- gas/off-gas screening;
- automated ultrasound;
- radiographic views where useful;
- comparison against the module’s own historical baseline.

## 13.4 Full CT of every cell every touch

This should remain an explicit research aspiration, not a current operational assumption.

NASA’s 2025 battery-workshop material describes:

- contemporary full 18650 CT around two minutes per cell in one commercial system;
- a claimed roadmap toward 10- and 5-second scans;
- large data and automated-analysis requirements.

At five seconds per cell:

- one scanner: 720 cells/hour;
- one million cells: 1,389 scanner-hours;
- nine million cells: 12,500 scanner-hours.

At two minutes per cell:

- one scanner: 30 cells/hour;
- nine million cells: 300,000 scanner-hours.

A P-E10000 could contain millions of cells, depending on format. Even future high-throughput CT requires substantial parallelism.

The recommended policy is:

1. **100% fast multimodal inspection** at every ground touch.
2. **Targeted or statistically designed CT** by default.
3. **Full CT** when triggered by history, anomaly, mission class, or sufficiently capable future infrastructure.
4. Design the module and cell layout for radiographic accessibility from the beginning.

Ultrasound is particularly attractive because NASA workshop material describes it as complementary to CT and able to detect low-atomic-number materials, gases, separators, and electrolyte-related features that X-ray methods may not directly resolve.

## 13.5 Module assignment by health

The Mind should assign:

- newest/highest-power modules to severe missions;
- healthy high-cycle modules to benign tenders;
- degraded but safe modules to stationary storage;
- questionable modules to quarantine;
- end-of-life modules to recycling.

The common interface creates a natural second-life ladder.

---

# 14. Fire safety

A P-E1000 or P-E10000 contains an extraordinary electrochemical-energy inventory. It cannot be one open battery room.

Required design principles include:

- small isolated fire zones;
- independent contactors;
- thermal barriers;
- controlled outward venting;
- propagation-resistant spacing;
- gas detection;
- liquid-cooling isolation;
- damaged-module remote extraction;
- module-level fire tests;
- installation-scale propagation tests;
- no single shared air path;
- deterministic fault response.

UL 9540A is the recognized U.S./Canadian test method for thermal-runaway fire propagation in stationary energy-storage systems and is referenced by NFPA 855. It is useful precedent, not an aviation certification path.

The website should never imply that modularity automatically prevents propagation. It should say:

> **Bounded failure is a design requirement that must be demonstrated at cell, module, magazine, vehicle, and depot scale.**

---

# 15. Why battery exchange was selected over alternatives

## 15.1 Direct airborne battery-to-battery charging

To transfer a P-E1000’s 270 MWh in ten minutes electrically would require an average:

\[
270\ \mathrm{MWh}/(1/6\ \mathrm{h})
=1.62\ \mathrm{GW}
\]

That demands:

- a gigawatt-class electrical connector;
- extremely high recipient charge acceptance;
- enormous conversion and cooling hardware;
- fault interruption at extreme power;
- additional battery charge/discharge losses;
- coupled flight for the full charge interval.

Mechanical module exchange achieves a similar **equivalent inventory rate** without sending 1.62 GW through the interface.

## 15.2 Jet fuel, SAF, or e-SAF

Hydrocarbon fuel remains much denser. Around 43 MJ/kg corresponds to roughly 12 kWh/kg chemical, and perhaps about 5.4 kWh/kg electric at an illustrative 45% conversion efficiency—approximately 18 times a 300 Wh/kg battery.

Fuel may remain a future remote/emergency fallback.

It is not the primary B.C. reference because it adds:

- liquid transfer logistics;
- combustion generators;
- lower electricity-to-work efficiency if synthesized from clean power;
- fuel fire and spill systems;
- carbon accounting;
- less elegant mass behavior as fuel is consumed.

The site should say **“not used in the primary B.C. model”**, not “fuel can never be useful.”

## 15.3 Green hydrogen

Hydrogen has exceptional gravimetric energy, but DOE notes that liquid hydrogen’s volumetric energy is much lower than hydrocarbon fuel and it requires approximately 20 K storage.

It adds:

- a second, much colder cryogenic system;
- boil-off and dormancy management;
- flammable-gas handling;
- bulky tanks;
- difficult airborne transfer.

It may be revisited for special long-range vehicles, but it is not necessary to explain the first network.

## 15.4 Liquid nitrogen

LN₂ remains excellent for:

- controllable dense ballast;
- mass-state adjustment;
- cold storage;
- partial energy recovery;
- coupling with waste heat.

Liquid-air/nitrogen storage literature generally places practical or proposed electrical round-trip efficiency around 50–60% with cold/heat recovery, materially below lithium-ion assumptions around 85–90%.

LN₂ should therefore remain the **mass battery**, not the primary imported electrical-energy carrier.

## 15.5 Solar alone

Solar materially extends endurance and supports safe drift, but:

- it is intermittent;
- surface area scales more slowly than payload volume;
- smoke/cloud/latitude reduce output;
- a regional response fleet may demand hundreds of megawatts.

Solar complements the exchange network; it does not eliminate it.

## 15.6 Ground tether charging

An equipped lake or fixed base might eventually provide direct power through a tether. That could be efficient, but it constrains route geometry and introduces a high-voltage moving tether over water and terrain. It is a useful optional future mode, not the universal network.

---

# 16. Standards and precedent

Current precedent supports pieces of the concept, not the whole system:

- IEC 62840-1:2025 and IEC 62840-2:2025 cover interoperable and safe road-vehicle battery-swap systems, generally up to 1,500 V DC.
- Commercial heavy-truck swap systems use modular blocks and automated swaps measured in minutes.
- The Megawatt Charging System targets up to about 3.75 MW for road vehicles.
- NASA’s NEAT facility supports electrified-aircraft testing up to the roughly 12 MW class.
- NASA research anticipates multi-kV, multi-MW aircraft distribution and future systems in the 10–20 MW class.
- UL 9540A/NFPA 855 address stationary storage propagation hazards.

A Pink vehicle may require:

- multiple 10–20 kV-class sectionalized buses;
- tens to hundreds of megawatts;
- rapid DC fault isolation;
- airborne robotic exchange;
- gigawatt-equivalent module logistics.

No existing standard should be presented as covering this complete architecture.

---

# 17. Simulation model

The website should calculate rather than merely narrate the network.

## 17.1 Core equations

### Module energy

\[
E_{\text{module,nameplate}}=
m_{\text{module}}\times e_{\text{specific}}
\]

\[
E_{\text{module,usable}}=
E_{\text{nameplate}}\times D_{\text{usable}}
\]

### Recipient endurance

\[
t_{\text{endurance}}=
\frac{E_{\text{usable aboard}}-E_{\text{reserve}}}
{P_{\text{forecast average}}}
\]

### Equivalent exchange power

\[
P_{\text{swap,equiv}}=
\frac{N_{\text{ports}}\times E_{\text{magazine}}}
{t_{\text{magazine}}}
\]

### Grid input

\[
P_{\text{grid}}=
\frac{P_{\text{delivered}}+P_{\text{tender}}+P_{\text{aux}}}
{\eta_{\text{system}}}
\]

### Inventory

\[
E_{\text{stock,nameplate}}=
\frac{
P_{\text{delivered}}
\times T_{\text{loop}}
\times R_{\text{reserve}}
}{
D_{\text{usable}}
}
\]

### Battery wear

\[
C_{\text{wear/MWh}}=
\frac{C_{\$/kWh}\times1000}
{N_{\text{cycles}}\times D_{\text{usable}}}
\]

## 17.2 Module state machine

```text
MANUFACTURED
→ QUALIFICATION
→ CHARGED_RESERVE
→ LOADED
→ IN_FLIGHT
→ INSTALLED
→ DISCHARGING
→ DEPLETED
→ RETURNING
→ COOLING
→ FAST_INSPECTION
→ [DEEP_INSPECTION | CHARGING | QUARANTINE]
→ CHARGED_RESERVE
→ SECOND_LIFE
→ RECYCLE
```

## 17.3 P-E1000 state machine

```text
AVAILABLE
→ DEPOT_APPROACH
→ DEPLETED_UNLOAD
→ CHARGED_LOAD
→ TO_RECIPIENT
→ RENDEZVOUS
→ MASS_BALANCED_EXCHANGE
→ SEPARATION
→ TO_NEXT_RECIPIENT | RETURN_TO_DEPOT
```

## 17.4 P-E10000 state machine

```text
STRATEGIC_RESERVE
→ DEPOT_REPLENISHMENT
→ REGIONAL_TRANSIT
→ REGIONAL_HOLD
→ SERVE_P-E1000
→ DIRECT_SERVE_LARGE_SHIP
→ WIND_LAYER_REPOSITION
→ SOLAR_RECOVERY
→ SAFE_DRIFT
→ RETURN_OR_REDEPLOY
```

---

# 18. Recommended public-facing framing

Use:

> **Energy is cargo.**

> Ground stations charge and inspect standardized battery modules. P-E1000 shuttles exchange charged modules for depleted ones. P-E10000 carriers move and buffer gigawatt-hours across regions. The batteries charge on the ground; the airships exchange physical energy inventory in minutes.

> Charged and depleted modules have effectively identical mass, so permanent vacuum lift can be designed around a stable battery payload.

> A gigawatt-equivalent swap does not put a gigawatt through one connector. It moves precharged batteries through multiple mechanical ports.

> Swapping removes turnaround delay. It does not remove grid demand, battery wear, capital cost, or the need to move thousands of tonnes of modules.

Avoid:

- “free energy”;
- “perpetual solar flight”;
- “instant gigawatt charging”;
- “no fire risk”;
- “every battery is fully CT scanned every time”;
- “the nearest transmission line has available power”;
- “all energy infrastructure already exists.”

---

# 19. Recommended research program

## Gate 1 — digital model

- common energy and mass accounting;
- module logistics simulator;
- depot sizing;
- tender routing;
- lifecycle cost;
- failure and reserve modeling.

## Gate 2 — small standardized module

- robotic latch;
- blind-mate power/data/cooling;
- mass tolerance;
- isolation;
- thermal containment;
- inspection fiducials.

## Gate 3 — parallel ground exchange

- bidirectional matched transfer;
- multiple ports;
- continuous bus operation;
- fault recovery;
- automated inventory handling.

## Gate 4 — inspection line

- multimodal automatic inspection;
- baseline comparison;
- ultrasound;
- radiography;
- quarantine;
- digital twin.

## Gate 5 — megawatt electrical district

- sectionalized DC bus;
- fault interruption;
- converter blocks;
- battery-bank hot swap;
- thermal management.

## Gate 6 — moving-platform exchange

- two ground vehicles;
- suspended platforms;
- tethered aircraft;
- increasingly difficult relative motion.

## Gate 7 — airborne exchange

- benign conditions;
- small modules;
- deterministic abort;
- structural load measurement.

## Gate 8 — regional depot

- utility study;
- 10–50 MW pilot;
- inventory operations;
- emergency exercises.

Scale only after each gate demonstrates that the prior assumption is real.

---

# 20. Principal open questions

1. What installed specific energy is achievable after containment, cooling, robotic interfaces, and mass standardization?
2. Which chemistry minimizes total cost per delivered MWh under high circulation?
3. What magazine mass minimizes handling time without creating unacceptable structural loads?
4. Can an airborne connector and bus interrupt multi-megawatt faults safely?
5. What relative-motion envelope permits reliable exchange?
6. How much battery inventory must be held for weather closures and grid outages?
7. Can a P-E10000’s solar surface offset its average self-propulsion load on representative global routes?
8. What is the true tender propulsion energy per tonne-kilometre?
9. What is the minimum practical module inspection time?
10. Can module-level thermal runaway be contained without unacceptable mass?
11. What utility interconnection sites can actually support 50, 200, or 500 MW?
12. How should Indigenous rights, land use, emergency governance, and environmental review shape depot siting?
13. How does battery mineral demand compare with the climate-adaptation benefit delivered?
14. At what distance does dense liquid fuel become superior despite lower conversion efficiency?
15. Does the mechanical transfer system remain reliable after tens of thousands of cycles?

---

# 21. Final assessment

The battery-exchange idea improves the Pink Robotics architecture because it aligns energy logistics with the defining physics of the vehicle:

- permanent vacuum lift;
- nearly invariant cargo mass;
- huge internal volume;
- distributed electric actuation;
- autonomous coordination;
- persistent operation;
- modular repair and inspection.

The best concise formulation is:

> **Electricity is generated where grids are strong, packaged into standardized physical modules, and moved by autonomous airships to wherever the fleet is doing work.**

The P-E1000 is the regional shuttle.

The P-E10000 is the mobile warehouse, strategic reserve, and potentially global-roaming energy node.

The ground depot is the hidden heart of the system.

And the central caveat is:

> **The exchange can be fast because the charging happened earlier. The system still pays for every megawatt-hour in grid capacity, battery wear, inspection, and physical module circulation.**

---

# Sources and research anchors

1. BC Hydro, “Our system” — clean generation mix:  
   https://www.bchydro.com/toolbar/about/sustainability/our-clean-system.html

2. BC Hydro, “Market signals strong interest in providing new capacity” — 13.4 GW maximum generating capacity and Site C:  
   https://www.bchydro.com/news/press_centre/news_releases/2025/capacity-rfeoi.html

3. BC Hydro, transmission connections — customer substation/line and multi-year connection process:  
   https://www.bchydro.com/accounts-billing/electrical-connections/large-load/transmission.html

4. BC Hydro, transmission rates — RS 1830 rates effective April 1, 2026:  
   https://app.bchydro.com/accounts-billing/rates-energy-use/electricity-rates/transmission_rate.html

5. BC Hydro, 2026 Transmission Customer Interconnection Policy workshop materials:  
   https://www.bchydro.com/content/dam/BCHydro/customer-portal/documents/corporate/regulatory-planning-documents/regulatory-matters/transmission-customer-interconnection-policy-workshop2-presentation-2026-03-04.pdf

6. U.S. DOE, mass-produced light-duty EV battery-pack cost estimate:  
   https://www.energy.gov/cmei/vehicles/articles/fotw-1354-august-5-2024-electric-vehicle-battery-pack-costs-light-duty

7. BloombergNEF, “New Record Lows for Battery Prices,” December 19, 2025:  
   https://about.bnef.com/insights/clean-transport/new-record-lows-for-battery-prices/

8. NASA, “Battery Cell-to-Pack Scaling Trends for Electric Aircraft”:  
   https://ntrs.nasa.gov/api/citations/20210017488/downloads/Battery_Cell_to_Pack_Scaling_Trends_for_Electric_Aircraft_6_14.pdf

9. NASA, “Energy Storage for NASA Missions” — 300 Wh/kg pack research assumption:  
   https://ntrs.nasa.gov/api/citations/20205009101/downloads/ARPAE_energy%20storage_Lvovich_.pdf

10. CATL, Naxtra sodium-ion announcement — vendor claims for energy density and cycle life:  
    https://www.catl.com/en/news/6401.html

11. NREL, “Moving Beyond 4-Hour Li-Ion Batteries” — 85% RTE modeling assumption:  
    https://docs.nrel.gov/docs/fy23osti/85878.pdf

12. IEC 62840-1:2025 and IEC 62840-2:2025 — road-vehicle battery swap guidance and safety:  
    https://webstore.iec.ch/en/publication/66398  
    https://webstore.iec.ch/en/publication/66390

13. CATL QIJI heavy-truck modular battery swapping:  
    https://www.catl.com/en/news/6041.html

14. U.S. DOE Alternative Fuels Data Center, Megawatt Charging System:  
    https://afdc.energy.gov/fuels/electricity-stations

15. NASA Electric Aircraft Testbed (NEAT):  
    https://www.nasa.gov/eap-labs-and-testbeds/neat/

16. NASA NEAT summary of capabilities:  
    https://www.nasa.gov/wp-content/uploads/2025/06/tm-20250001338-neat-summary-of-capabilities-v3.pdf

17. UL Solutions, UL 9540A thermal-runaway propagation test method:  
    https://www.ul.com/services/ul-9540a-test-method

18. NASA Aerospace Battery Workshop, high-throughput CT:  
    https://www.nasa.gov/wp-content/uploads/2024/01/battery-quality-control-via-glimpses-high-throughput-ct-scanning-capabilities-abw-2025.pdf

19. NASA Aerospace Battery Workshop, ultrasound-enhanced cell screening:  
    https://www.nasa.gov/wp-content/uploads/2024/01/ultrasound-enhanced-cell-quality-control-selection-and-validation-of-li-ion-cells-abw-2025-v2.pdf

20. U.S. DOE, National Blueprint for Lithium Batteries — design for reuse and recycling:  
    https://www.energy.gov/sites/default/files/2021-06/FCAB%20National%20Blueprint%20Lithium%20Batteries%200621_0.pdf

21. U.S. DOE, hydrogen storage energy-density comparison:  
    https://www.energy.gov/cmei/fuels/hydrogen-storage

22. Morgan et al., liquid-air energy-storage pilot analysis:  
    https://cris.brighton.ac.uk/ws/files/5530179/Liquid_air_energy_storage_Analysis_and_first_results_from_a_pilot_scale_demonstration_plant.pdf.pdf
