# Fable Ultracode implementation brief

> Dated implementation brief, 2026-08-09; retained as written. See the [current float ledger](../../docs/FLOAT-LEDGER.md).
## Add “Energy as Cargo” battery exchange, P-E1000/P-E10000 logistics, and grid-connected base stations to the Pink Robotics airship model

You are working in the existing Pink Robotics website repository and its current staging implementation:

- https://guppi.ca/pinkrobotics/
- https://guppi.ca/pinkrobotics/airships/

You are already familiar with the codebase and current wildfire-airship monitor. A separate 3D agent may also be adding semantic P-100/P-1000/P-10000 models and animation hooks. Inspect all current and uncommitted work before changing shared files.

Implement the energy-logistics architecture below as a coherent extension of the existing airship simulation, model, map, calculations, methodology, and progressive-disclosure content.

Do not return only a plan or mockup. Implement as much of the feature as the repository permits, keep assumptions centralized, add tests, and report what remains simplified.

Do not stop for clarification. Make reasonable choices and label them.

---

# 1. Primary decision

The primary British Columbia reference architecture is now:

> **Clean grid electricity → standardized swappable battery modules at ground depots → P-E1000 regional shuttles and P-E10000 regional/global buffers → mass-balanced module exchange with working water airships.**

Do not make Jet A, SAF, e-SAF, hydrogen, or another chemical fuel the primary energy path in the B.C. simulation.

Those options may remain in a collapsed “Alternatives and future fallback” comparison, but they should not drive the main fleet model, map, vehicle status, or default calculations.

Liquid nitrogen remains an onboard:

- controllable ballast state;
- cold reservoir;
- partially recoverable energy store;
- mass-management tool.

Do not replace LN₂ with batteries. Batteries supply electrical energy; LN₂ supplies controllable mass and some recoverable energy.

Solar remains an onboard endurance extender and safe-drift resource.

---

# 2. Why this architecture was selected

Explain this explicitly on the site.

The choice is not that batteries are the densest energy carrier. They are not.

Battery exchange fits this vehicle because:

1. Every important actuator and machine is already electric.
2. British Columbia’s grid is hydro-dominated and BC Hydro reports more than 98% clean/renewable generation.
3. The same battery module has effectively identical mass when charged or discharged.
4. Permanent vacuum lift can be designed around an invariant battery-module payload.
5. Charged modules can enter while depleted modules leave, keeping gross mass and centre of gravity nearly constant.
6. The receiving aircraft does not need to accept gigawatt-scale electrical fast charging.
7. Charging happens earlier and in parallel on the ground.
8. Ground inventory decouples battery charge time from airship turnaround.
9. Every ground touch becomes an automated inspection, cooling, maintenance, and health-classification event.
10. Standard modules can circulate across depots, P-E1000 shuttles, P-E10000 buffers, water airships, and eventually other Pink machines.
11. A P-E10000 can move gigawatt-hours, roam slowly for days or weeks, exploit winds, and use its enormous upper solar surface.
12. The fleet can be green wherever sufficiently low-carbon electricity and charging infrastructure are built.

Also show the counterweight:

> **Swapping removes aircraft charging delay. It does not remove average grid demand, battery capital, cycle wear, fire safety, inspection, or the physical mass flow of modules.**

This sentence is essential.

---

# 3. User-facing headline and copy

Create a major section titled:

> **Energy as Cargo**

Suggested summary:

> Electricity is generated where grids are strong, packaged into standardized physical modules, and moved by autonomous airships to wherever the fleet is doing work. Ground depots charge and inspect modules in parallel. P-E1000 shuttles exchange charged modules for depleted ones. P-E10000 carriers move and buffer gigawatt-hours across regions.

Use or adapt:

> Charged and depleted modules have effectively identical mass, so permanent vacuum lift can be designed around a stable battery payload.

> A gigawatt-equivalent swap does not put a gigawatt through one connector. It moves precharged batteries through multiple mechanical ports.

> The batteries charge on the ground. The aircraft exchange energy inventory in minutes.

> The exchange can be fast because the charging happened earlier.

> Energy is transferred mechanically as battery cargo, then used electrically after the module is connected to the recipient’s segmented bus.

Avoid:

- “free energy”;
- “instant charging”;
- “perpetual flight”;
- “zero fire risk”;
- “unlimited range”;
- “the nearest substation can supply us”;
- “all cells receive full CT every time”;
- “GW/hour.”

Use:

- “GW-equivalent module-transfer rate”;
- “GWh of stored energy exchanged per hour”;
- “conceptual energy depot”;
- “simulated grid demand”;
- “illustrative installed specific energy.”

---

# 4. Preserve clear epistemic boundaries

The site currently distinguishes real wildfire data from simulated aircraft. Extend that discipline.

Use persistent labels such as:

> REAL B.C. FIRE DATA  
> SIMULATED PINK FLEET  
> CONCEPTUAL ENERGY INFRASTRUCTURE

For grid and depot information:

- BC Hydro generation mix, system capacity, published tariff, and published transmission maps may be sourced as real context.
- Depot locations are conceptual unless tied to an actual approved project.
- Proximity to a transmission line or substation does not establish spare capacity.
- No grid connection, land right, permit, or power allocation should be implied.
- Every high-power depot requires a utility interconnection study.

Add this qualification wherever depot nodes appear:

> This node is a conceptual siting candidate. Nearby transmission infrastructure does not establish available capacity or permission to connect.

---

# 5. Vehicle classes

Add two energy-logistics vehicle classes.

## 5.1 P-E1000 — regional energy shuttle

Purpose:

- collect charged battery magazines from a depot;
- return depleted magazines;
- serve one or more working aircraft;
- exchange while following the recipient’s safe transit leg;
- maintain almost invariant cargo mass;
- operate as a fast regional distributor.

Reference cargo assumption:

- nominal payload class: 1,000 tonnes;
- 90% assigned to battery modules: 900 tonnes;
- 10% retained for magazines, rails, handling, thermal systems, containment, and margin;
- installed battery specific energy baseline: 300 Wh/kg;
- nameplate cargo energy: 270 MWh;
- usable at 80% depth of discharge: 216 MWh.

Expose 200–500 Wh/kg as a sensitivity range.

## 5.2 P-E10000 — strategic energy buffer

Purpose:

- transport gigawatt-hours over long distance;
- establish a mobile regional energy node;
- resupply P-E1000 shuttles;
- directly serve large working aircraft;
- hold strategic reserve;
- reposition using altitude, weather, and solar;
- roam globally when energy delivery is not urgent.

Reference cargo assumption:

- nominal payload class: 10,000 tonnes;
- 9,000 tonnes of battery modules;
- 300 Wh/kg installed baseline;
- 2.7 GWh nameplate;
- 2.16 GWh usable at 80% depth of discharge.

Do not describe it as an infinite or perpetual power source.

Its identity changes with load:

- at 10 MW net average draw: roughly nine days from 2.16 GWh before solar;
- at 400 MW delivered to a fleet: roughly 5.4 hours before solar and reserve;
- solar can extend self-endurance but cannot support a large regional load by itself.

## 5.3 Stable mass design

Charged and discharged energy states change battery mass only by \(E/c^2\), which is negligible.

For 2.7 GWh, the difference is about 0.108 grams.

The visual and simulation should therefore treat charged and depleted copies of the same module as equal mass.

Vehicle mass changes only when:

- a module is physically absent;
- a different-mass module is installed;
- water/LN₂/fuel/consumable mass changes;
- trim ballast changes.

Require same-mass replacements or standard inert carriers when a slot cannot be filled.

---

# 6. Standardized energy units

Implement a two-level hierarchy.

## 6.1 Pink Energy Module — PEM

Reference baseline:

- gross mass: 1,000 kg;
- installed specific energy: 300 Wh/kg;
- nameplate energy: 300 kWh;
- usable depth: 80%;
- usable energy: 240 kWh.

A PEM is independently:

- identified;
- isolated;
- monitored;
- cooled;
- latched;
- vented;
- inspectable;
- replaceable.

## 6.2 Pink Energy Magazine — PEM-G

Reference baseline:

- five PEMs;
- gross mass: 5 tonnes;
- nameplate energy: 1.5 MWh;
- usable energy: 1.2 MWh;
- exchanged as one rapid mechanical cargo unit.

Keep module mass, magazine size, and modules per magazine configurable.

The simulation must support alternative 1-, 5-, 10-, and 20-tonne handled units.

## 6.3 Common interface

Every compatible module/magazine should expose:

- stable ID;
- tightly controlled gross mass;
- physical dimensions;
- structural rails;
- robotic grapple points;
- locking points;
- blind-mate electrical contacts;
- precharge/contactors;
- data interface;
- optical/local communication;
- coolant interfaces;
- controlled vent path;
- BMS;
- thermal and pressure sensing;
- gas sensing;
- strain/impact log;
- inspection fiducials;
- service history;
- remaining-life estimate.

“Purely mechanical exchange” means the energy crosses between vehicles inside physical modules rather than through a high-rate charger. It does not eliminate electrical isolation, precharge, cooling, data, or bus synchronization.

## 6.4 Multiple chemistry profiles

Standardize the interface, not one chemistry forever.

Support configuration profiles such as:

- `PEM_HIGH_ENERGY`
- `PEM_HIGH_POWER`
- `PEM_LONG_LIFE`
- `PEM_HIGH_SAFETY`
- `PEM_SECOND_LIFE_STATIONARY`

Each profile can vary:

- Wh/kg;
- power capability;
- cycle life;
- cost;
- thermal limits;
- charge rate;
- allowed mission classes.

Do not claim a chemistry is flight-ready merely because it appears in the simulator.

---

# 7. Exchange architecture

## 7.1 Paired mass-balanced transfer

Animate and calculate:

- charged magazine enters;
- depleted magazine exits simultaneously;
- opposing ports operate symmetrically;
- gross mass remains nearly constant;
- centre-of-gravity movement is bounded.

Never model:

1. unloading all depleted modules;
2. leaving the recipient hundreds of tonnes light;
3. later loading charged modules.

Use paired flow.

## 7.2 Segmented banks

Every working airship must retain at least two independent battery banks.

Sequence:

1. Bank A powers the ship.
2. Bank B isolates.
3. B’s depleted magazines leave while charged magazines enter.
4. Mechanical latches, cooling, data, insulation, and precharge verify.
5. Bank B connects.
6. Load may transition to B.
7. Bank A can then be exchanged.

The aircraft must retain deterministic flight-control power throughout.

## 7.3 Air-to-air rendezvous

The Regional Mind should plan exchange:

- outside the fire convection area;
- on a recipient transit/return leg;
- in a forecast calm layer;
- within relative-speed, roll, pitch, yaw, turbulence, and structural envelopes;
- with a deterministic abort route.

The two Vehicle Minds temporarily solve a joint control problem.

Do not depict two fragile hulls casually touching.

Represent a conceptual:

- soft-capture stage;
- alignment bridge;
- load-sharing truss;
- robotic magazine transfer paths;
- emergency disconnect.

## 7.4 Ground transfer

Ground depots may use:

- robotic elevators;
- gantries;
- suspended transfer bridges;
- vertical conveyors;
- smaller handling aircraft.

The large airship may remain above the ground.

Treat the exact interface as conceptual.

---

# 8. Equivalent transfer rate

Implement:

```ts
equivalentSwapPowerMW =
  activePorts *
  usableEnergyPerMagazineMWh *
  3600 /
  secondsPerMagazine;
```

Also calculate the nameplate rate.

Reference baseline:

- magazine: 5 t;
- nameplate: 1.5 MWh;
- usable: 1.2 MWh;
- eight paired ports;
- 30 seconds per magazine.

Result:

- 960 magazines/hour;
- 1.44 GWh/hour nameplate;
- 1.152 GWh/hour usable;
- 1.152 GW-equivalent usable transfer rate.

Display:

> No 1.15 GW charging connector is active. The number is the rate at which previously charged energy inventory is moved mechanically.

Reference exchange timing:

- P-E1000: 180 magazines;
- at 8 ports and 30 s/magazine: 11.25 minutes pure transfer;
- at 16 ports: 5.63 minutes.

- P-E10000: 1,800 magazines;
- at 16 ports and 30 s: 56.25 minutes;
- at 32 ports: 28.13 minutes.

Show pure mechanical transfer separately from:

- approach;
- capture;
- verification;
- retries;
- separation.

## 8.1 Show mass flow

At 1.2 MWh usable per 5-tonne magazine:

- 40 MW delivered = 33.3 magazines/h = 167 t/h;
- 100 MW = 83.3 magazines/h = 417 t/h;
- 300 MW = 250 magazines/h = 1,250 t/h;
- 500 MW = 416.7 magazines/h = 2,083 t/h;
- 1 GW = 833.3 magazines/h = 4,167 t/h.

Make this visible.

The system is both an energy network and an industrial mass-logistics network.

---

# 9. Ground Energy Depot

Add simulated Pink Energy Depots.

A depot is not an EV charging point. It is:

- transmission-connected industrial load;
- AC/DC conversion plant;
- module warehouse;
- cooling facility;
- automated inspection line;
- parallel charging plant;
- reserve inventory;
- quarantine/fire-separation installation;
- robotic airship cargo terminal;
- maintenance/recycling node.

## 9.1 Depot zones

Model at least:

1. `GRID_INTERCONNECTION`
2. `AC_DC_CONVERSION`
3. `DEPLETED_RECEIVING`
4. `COOLING`
5. `FAST_INSPECTION`
6. `DEEP_INSPECTION`
7. `CHARGING`
8. `CHARGED_RESERVE`
9. `MAGAZINE_ASSEMBLY`
10. `AIRSHIP_TRANSFER`
11. `QUARANTINE`
12. `MAINTENANCE`
13. `SECOND_LIFE`
14. `RECYCLE`

## 9.2 Depot power

Use:

```ts
gridPowerMW =
  (deliveredFleetPowerMW +
   tenderPropulsionPowerMW +
   stationAuxiliaryPowerMW) /
  gridToDeliveredEfficiency;
```

Default efficiency:

- 85%;
- expose 75–92%.

Examples before tender and auxiliary loads:

- 40 MW useful → 47.1 MW grid;
- 100 MW → 117.6 MW;
- 300 MW → 352.9 MW;
- 400 MW → 470.6 MW;
- 500 MW → 588.2 MW;
- 1 GW → 1.176 GW.

## 9.3 Inventory

Use:

```ts
requiredNameplateInventoryMWh =
  deliveredPowerMW *
  completeModuleLoopHours *
  reserveMultiplier /
  usableDepthOfDischarge;
```

Example:

- 400 MW useful;
- six-hour loop;
- reserve multiplier 1.2;
- 80% usable DoD;

requires:

- 2.88 GWh usable circulating inventory;
- 3.6 GWh nameplate inventory.

Do not incorrectly divide inventory by round-trip efficiency. Efficiency determines grid input; DoD and loop time determine circulating nameplate inventory.

## 9.4 Parallel charging

Do not create one fictional 500 MW charger.

For a 1-tonne/300-kWh PEM:

- 0.25C = 75 kW;
- 0.5C = 150 kW;
- 1C = 300 kW.

The depot supplies power through thousands of parallel channels.

Ground inventory decouples tender turnaround from charge time.

## 9.5 Station tiers

Provide presets:

- research: 1–10 MW;
- local: 10–50 MW;
- regional: 50–200 MW;
- major wildfire hub: 200–500 MW;
- strategic: 500 MW–1 GW+.

Label 100–500 MW stations as transmission-scale industrial facilities.

---

# 10. B.C. grid context and data

Use official public information where appropriate.

Relevant context:

- BC Hydro says over 98% of its generation is clean and renewable.
- BC Hydro reported about 13.4 GW maximum generating capacity after Site C.
- Transmission customers take high-voltage service and may need to own their substation and line.
- Connections can take years.
- RS 1830 rates effective April 1, 2026 list:
  - C$12.178/kVA-month demand;
  - 4.914 cents/kWh energy.

Do not assert local available capacity.

Optional real-data integrations:

- BC Hydro published transmission maps;
- BC Hydro balancing-authority hourly/daily system load;
- official tariff values and effective date.

Do not make the page depend on fragile PDF scraping at runtime. Curate verified values in a dated source file and link the official source.

Represent conceptual depot candidates in a manually reviewed config or simulation layer.

Do not place a depot at every hydro dam. The preferred architecture is:

> hydro-dominated grid → strategically located transmission-connected depot

not:

> every tender must fly to a dam.

---

# 11. Electricity-cost model

Implement an assumptions-based operating-cost calculator.

Use separate currencies explicitly.

For B.C. tariff calculations, use CAD.

Simplified RS 1830 calculation:

```ts
monthlyEnergyKWh =
  peakGridPowerMW * 1000 * hoursInMonth * loadFactor;

energyChargeCAD =
  monthlyEnergyKWh * 0.04914;

demandChargeCAD =
  peakGridPowerMW * 1000 * 12.178; // approximate PF = 1

totalElectricityCAD =
  energyChargeCAD + demandChargeCAD;
```

Show exclusions:

- taxes;
- riders;
- power factor;
- interconnection losses not already modeled;
- special contracts;
- connection capital;
- utility study;
- other tariff terms.

Reference result:

At 90% load factor, approximate input electricity cost is C$67.7/MWh.

At 85% system efficiency, this is approximately C$79.6/MWh delivered before:

- tender flight;
- module depreciation;
- maintenance;
- inspection;
- station O&M;
- financing.

## 11.1 400 MW example

For a continuous 400 MW useful fleet load:

- grid input at 85%: 470.6 MW;
- 343.5 GWh/month at 730 hours;
- energy charge: about C$16.88M/month;
- demand charge: about C$5.73M/month;
- total: about C$22.61M/month;
- about C$77.4/MWh delivered.

Mark it as arithmetic, not a BC Hydro quote.

---

# 12. Battery capital and cycle wear

Support cost scenarios in US dollars:

- US$150/kWh optimistic scale;
- US$300/kWh reference specialized;
- US$500/kWh conservative specialized.

Explain that current EV/stationary market pack prices are lower bounds because Pink modules require:

- flight structure;
- thermal containment;
- robotic interfaces;
- standardized mass;
- cooling;
- high-voltage contacts;
- inspection design;
- traceability;
- certification.

Reference capital:

### P-E1000, 270 MWh

- $40.5M at $150/kWh;
- $81M at $300/kWh;
- $135M at $500/kWh.

### P-E10000, 2.7 GWh

- $405M;
- $810M;
- $1.35B.

### 3.6 GWh depot inventory

- $540M;
- $1.08B;
- $1.80B.

## 12.1 Wear cost

Implement:

```ts
batteryWearCostPerDeliveredMWh =
  moduleCostPerKWh * 1000 /
  (fullEquivalentCycles * usableDepthOfDischarge);
```

At $300/kWh and 80% DoD:

- 1,000 cycles → $375/MWh;
- 2,000 cycles → $187.5/MWh;
- 5,000 cycles → $75/MWh;
- 10,000 cycles → $37.5/MWh.

Make battery wear a first-class metric.

Do not let the UI imply electricity price is the dominant cost.

Add:

- residual value;
- second-life value;
- calendar-aging factor;
- financing;
- maintenance;

as optional later fields.

---

# 13. Interconnection cost

Do not publish a precise station construction cost without a site study.

Provide configurable cost categories:

- utility studies;
- system reinforcement;
- customer transmission line;
- customer substation;
- transformers/switchgear;
- AC/DC conversion;
- charging racks;
- cooling;
- robotics;
- inspection;
- land/civil works;
- fire separation;
- battery inventory;
- maintenance;
- contingency.

BC Hydro’s 2026 workshop material used 50 MW reinforcement examples of C$25M, C$50M, and C$100M.

Treat these as context, not a cost formula.

UI wording:

> Actual interconnection cost and schedule are site-specific. Published scenario ranges are shown only to establish scale.

---

# 14. Module inspection

The user’s target is that every returning battery should be inspected extensively.

Implement a tiered, honest model.

## 14.1 Continuous in-flight digital twin

Track:

- cell voltages;
- temperature;
- current;
- SOC;
- SOH;
- resistance;
- strain;
- pressure;
- gas/vent events;
- coolant state;
- insulation;
- vibration/shock;
- assignment history;
- fault history.

## 14.2 Every air-to-air exchange

Fast checks:

- identity;
- compatibility;
- voltage;
- temperature;
- insulation;
- contactor state;
- recent faults;
- external damage;
- cooling integrity.

Do not model CT in the air.

## 14.3 Every ground touch

Model:

- all-face machine vision;
- dimensional/deformation scan;
- thermal imaging;
- latch/connector inspection;
- BMS download;
- isolation/leakage;
- impedance;
- coolant test;
- gas/off-gas;
- automated ultrasound;
- selected X-ray/radiographic views;
- comparison with that exact module’s historical baseline.

## 14.4 Deep inspection

Full CT, extended ultrasound, capacity tests, and disassembly are:

- anomaly-triggered;
- scheduled;
- mission-class-triggered;
- statistically sampled;
- or performed at 100% only when future throughput supports it.

Do not promise full multi-angle CT of every cell at every touch as a current capability.

Show scanner throughput as a research variable.

NASA workshop reference points:

- approximately two minutes for a contemporary full 18650 CT scan in one presented system;
- vendor roadmap toward 10 and five seconds;
- ultrasound vendor claim around one cell/second.

At five seconds/cell:

- 720 cells/hour/scanner;
- one million cells = 1,389 scanner-hours;
- nine million cells = 12,500 scanner-hours.

The model should expose:

- cells/module;
- scanners;
- seconds/cell;
- inspection queue;
- modules cleared/hour;
- deep-inspection backlog.

## 14.5 Design for inspectability

Show that PEMs are deliberately:

- indexed;
- fiducialized;
- radiography-friendly;
- accessible from several directions;
- divided into removable cell slabs where useful;
- compared against their own historical scans.

---

# 15. Module lifecycle

Add module states:

```ts
type EnergyModuleState =
  | "MANUFACTURED"
  | "QUALIFICATION"
  | "CHARGED_RESERVE"
  | "LOADED"
  | "IN_FLIGHT"
  | "INSTALLED"
  | "DISCHARGING"
  | "DEPLETED"
  | "RETURNING"
  | "COOLING"
  | "FAST_INSPECTION"
  | "DEEP_INSPECTION"
  | "CHARGING"
  | "QUARANTINE"
  | "MAINTENANCE"
  | "SECOND_LIFE"
  | "RECYCLE";
```

Add a health-classification ladder:

- flight critical;
- normal flight;
- tender only;
- benign/global buffer;
- stationary depot;
- quarantine;
- recycle.

The Mind should assign the best modules to the hardest missions.

Do not simulate every cell or every PEM globally as a separate animated object. Aggregate inventory by cohort for performance, while exposing representative module digital twins in detail panels.

---

# 16. Tender state machines

## 16.1 P-E1000

```ts
type EnergyShuttleState =
  | "AVAILABLE"
  | "TO_DEPOT"
  | "DEPOT_APPROACH"
  | "DEPLETED_UNLOAD"
  | "CHARGED_LOAD"
  | "TO_RECIPIENT"
  | "RENDEZVOUS_APPROACH"
  | "SOFT_CAPTURE"
  | "MASS_BALANCED_EXCHANGE"
  | "VERIFY_AND_SYNC"
  | "SEPARATION"
  | "TO_NEXT_RECIPIENT"
  | "RETURN_TO_DEPOT"
  | "WEATHER_HOLD"
  | "SAFE_DRIFT"
  | "MAINTENANCE";
```

## 16.2 P-E10000

```ts
type EnergyBufferState =
  | "STRATEGIC_RESERVE"
  | "DEPOT_REPLENISHMENT"
  | "REGIONAL_TRANSIT"
  | "REGIONAL_HOLD"
  | "SERVE_SHUTTLE"
  | "SERVE_LARGE_RECIPIENT"
  | "WIND_LAYER_REPOSITION"
  | "SOLAR_RECOVERY"
  | "SAFE_DRIFT"
  | "RETURN_TO_DEPOT"
  | "REDEPLOY";
```

## 16.3 Depot

```ts
type DepotState =
  | "NOMINAL"
  | "GRID_LIMITED"
  | "CHARGER_LIMITED"
  | "INSPECTION_LIMITED"
  | "INVENTORY_LIMITED"
  | "TRANSFER_LIMITED"
  | "WEATHER_CLOSED"
  | "ISLANDED"
  | "EMERGENCY_RESERVE";
```

---

# 17. Dispatch logic

The Regional Mind should forecast energy demand rather than wait for a low-SOC alarm.

For every recipient:

1. Forecast phase-by-phase power for several cycles.
2. Calculate reserve breach time.
3. Determine required module quantity and power class.
4. Find available P-E1000s.
5. Find nearest charged inventory or P-E10000 buffer.
6. Evaluate weather and rendezvous windows.
7. Minimize:
   - mission interruption;
   - tender energy;
   - structural risk;
   - inventory imbalance;
   - battery wear;
   - inspection risk;
   - reserve depletion.
8. Schedule a mass-balanced exchange.
9. Replan on weather, fire, depot, or module-health changes.

P-E10000 logic should decide whether to:

- remain as regional reserve;
- move closer;
- feed P-E1000s;
- directly serve a large ship;
- exploit solar;
- drift to a better wind layer;
- return for replenishment.

Use explainable deterministic heuristics in the initial site, not decorative black-box AI.

---

# 18. Suggested data model

Adapt to the repository and existing shared types.

```ts
type EnergyCarrierClassId = "PE1000" | "PE10000";

type ModuleChemistryProfile =
  | "HIGH_ENERGY"
  | "HIGH_POWER"
  | "LONG_LIFE"
  | "HIGH_SAFETY"
  | "SECOND_LIFE";

interface PinkEnergyModule {
  id: string;
  profile: ModuleChemistryProfile;

  grossMassKg: number;
  nameplateKWh: number;
  usableKWh: number;
  stateOfCharge: number;
  stateOfHealth: number;

  maxChargeKW: number;
  maxDischargeKW: number;
  temperatureC: number;
  internalResistanceIndex: number;

  cycleCount: number;
  equivalentFullCycles: number;
  manufactureDate?: string;

  state: EnergyModuleState;
  currentHolderId?: string;
  magazineId?: string;

  inspectionStatus:
    | "CLEARED"
    | "LIMITED"
    | "DEEP_INSPECTION"
    | "QUARANTINE";

  lastInspectionAt?: string;
  nextInspectionAt?: string;
  warnings: string[];
}

interface EnergyMagazine {
  id: string;
  moduleIds: string[];

  grossMassKg: number;
  nameplateMWh: number;
  usableMWh: number;
  stateOfCharge: number;
  maximumPowerMW: number;

  healthClass:
    | "FLIGHT_CRITICAL"
    | "NORMAL_FLIGHT"
    | "TENDER"
    | "BENIGN_BUFFER"
    | "STATIONARY"
    | "QUARANTINE";

  sourceId?: string;
  destinationId?: string;
}

interface EnergyDepot {
  id: string;
  name: string;
  position: [number, number];

  conceptual: boolean;
  sourceNotes: string[];
  lastVerifiedAt?: string;

  gridConnectionMW: number;
  chargingCapacityMW: number;
  auxiliaryLoadMW: number;
  gridToModuleEfficiency: number;

  transferPorts: number;
  secondsPerMagazine: number;

  fastInspectionLanes: number;
  deepInspectionScanners: number;
  secondsPerFastInspection: number;
  secondsPerCellCT: number;

  chargedInventoryMWh: number;
  chargingInventoryMWh: number;
  coolingInventoryMWh: number;
  depletedInventoryMWh: number;
  quarantineInventoryMWh: number;
  reserveInventoryMWh: number;

  currentState: DepotState;
  bottleneck:
    | "GRID"
    | "CHARGING"
    | "INSPECTION"
    | "INVENTORY"
    | "TRANSFER"
    | "WEATHER"
    | "NONE";
}

interface EnergyCarrier {
  id: string;
  classId: EnergyCarrierClassId;

  ownReserveMWh: number;
  cargoNameplateMWh: number;
  cargoUsableMWh: number;
  chargedCargoMWh: number;
  depletedCargoMWh: number;

  state: EnergyShuttleState | EnergyBufferState;
  sourceId?: string;
  recipientId?: string;
  nextRecipientId?: string;

  solarPowerMW: number;
  propulsionPowerMW: number;
  hotelPowerMW: number;
  predictedEnduranceHours: number;

  route?: GeoJSON.LineString;
  warnings: string[];
}

interface EnergyExchangePlan {
  id: string;

  donorId: string;
  recipientId: string;

  chargedMagazinesIn: number;
  depletedMagazinesOut: number;
  energyTransferredUsableMWh: number;

  pairedPorts: number;
  secondsPerMagazine: number;
  pureTransferSeconds: number;
  completeExchangeSeconds: number;

  equivalentTransferPowerMW: number;

  recipientEnergyBeforeMWh: number;
  recipientEnergyAfterMWh: number;
  recipientEnduranceBeforeHours: number;
  recipientEnduranceAfterHours: number;

  plannedStartAt: string;
  rendezvousPosition: [number, number];
  rendezvousAltitudeM: number;

  massDeltaKg: number;
  cgShiftM: number;

  rationale: string;
  warnings: string[];
}
```

Use aggregate cohorts in production rather than materializing millions of module objects.

---

# 19. Shared assumptions

Create one discoverable configuration file.

Recommended defaults:

```ts
const energyCargoDefaults = {
  installedSpecificEnergyWhKg: 300,
  specificEnergyRangeWhKg: [200, 500],

  pemGrossMassKg: 1000,
  pemUsableDepth: 0.80,

  pemsPerMagazine: 5,
  magazineGrossMassKg: 5000,

  gridToDeliveredEfficiency: 0.85,
  efficiencyRange: [0.75, 0.92],

  reserveMultiplier: 1.20,

  pe1000BatteryCargoTonnes: 900,
  pe10000BatteryCargoTonnes: 9000,

  pe1000ExchangePorts: 8,
  pe10000ExchangePorts: 16,
  secondsPerMagazine: 30,

  moduleCostUsdPerKWh: 300,
  moduleCostScenariosUsdPerKWh: [150, 300, 500],

  usableDepthOfDischarge: 0.80,
  referenceEquivalentFullCycles: 5000,

  pe10000SolarCoverage: 0.70,
  pe10000PvEfficiency: 0.22,
  pe10000SolarDerate: 0.90,
  referenceIrradianceWM2: 1000,

  bcHydroRs1830EnergyCadPerKWh: 0.04914,
  bcHydroRs1830DemandCadPerKvaMonth: 12.178,
  bcHydroTariffEffectiveDate: "2026-04-01"
};
```

Every displayed output affected by these assumptions must link to the assumptions panel.

---

# 20. P-E10000 solar and global-roaming model

Use the existing illustrative 821 m × 205 m geometry unless shared configuration changes.

Approximate projected top ellipse:

- about 132,000 m².

Reference conceptual PV calculation:

```ts
peakSolarMW =
  topProjectedAreaM2 *
  coverage *
  pvEfficiency *
  orientationDerate *
  irradianceWM2 /
  1e6;
```

At the defaults above:

- about 18.3 MW peak.

Label this:

> Conceptual clear-sky peak; not expected average output.

Implement adjustable:

- latitude;
- season;
- time of day;
- cloud/smoke derate;
- orientation;
- active area;
- cell efficiency.

## 20.1 Speed sensitivity

Add a first-order drag model:

```ts
dragPowerW =
  0.5 *
  airDensityKgM3 *
  dragCoefficient *
  frontalAreaM2 *
  airspeedMps ** 3 /
  propulsiveEfficiency;
```

Default sensitivity only; not CFD.

For the illustrative P-E10000 with \(C_d=0.05\):

- 36 km/h ≈ 1.35 MW;
- 72 km/h ≈ 10.8 MW;
- 90 km/h ≈ 21.1 MW.

Clearly state omissions.

Use this to demonstrate:

> Slowing down and exploiting the wind can increase endurance dramatically.

Do not promise indefinite flight.

---

# 21. Map additions

Add toggles:

- Energy Depots
- P-E1000 Shuttles
- P-E10000 Buffers
- Energy Logistics Routes
- Module Exchange Events
- Conceptual Transmission Context
- Energy Demand Heat
- Charged Inventory
- Inspection Bottlenecks

Use distinct restrained symbology.

Clicking a depot should show:

- conceptual/real status;
- grid connection;
- current draw;
- charging output;
- inventory by state;
- reserve;
- modules/hour;
- inspection throughput;
- exchange ports;
- bottleneck;
- current electricity-cost estimate;
- current recipient commitments;
- warnings;
- source notes.

Clicking P-E1000 should show:

- charged cargo;
- depleted cargo;
- own reserve;
- source depot/buffer;
- recipient;
- ETA;
- exchange quantity;
- equivalent transfer rate;
- next assignment.

Clicking P-E10000 should show:

- nameplate and usable inventory;
- charged/depleted mix;
- solar now;
- net load;
- self-endurance;
- supported fleet power;
- incoming/outgoing P-E1000s;
- strategic reserve;
- selected wind layer;
- next action.

---

# 22. Recipient Energy Logistics panel

Add to every water airship:

## Energy now

- connected usable energy;
- reserve;
- phase power;
- average forecast power;
- solar;
- LN₂ recovery;
- predicted endurance;
- current battery health class.

## Logistics

- requested energy;
- assigned tender;
- tender cargo;
- ETA;
- rendezvous;
- magazines exchanged;
- equivalent transfer rate;
- expected duration;
- endurance before/after;
- next planned exchange.

## Mind explanation

Generate deterministic text from actual state:

> LAST  
> Completed cycle 18 with 46 MWh remaining above reserve.

> NOW  
> Returning toward the lake while Bank B is prepared for exchange.

> NEXT  
> P-E1000-03 will soft-capture at 2,400 m and exchange 36 paired magazines.

> PLAN  
> Add 43.2 MWh usable without changing gross mass. Bank A remains online. Exchange is scheduled outside the fire-convection zone in the lowest-turbulence forecast layer.

---

# 23. Depot detail visualization

Build a schematic inventory flow:

```text
depleted arrival
  → cooling
  → inspection
  → charging
  → charged reserve
  → magazine assembly
  → outbound tender
```

Show animated aggregate quantities, not thousands of DOM elements.

Display bottleneck highlighting:

- grid-limited;
- charger-limited;
- inspection-limited;
- inventory-limited;
- transfer-limited;
- weather-closed.

Add a timeline/queue view.

---

# 24. Mechanical exchange visualization

Coordinate with the 3D model work if available.

Animate:

1. matching trajectory;
2. soft capture;
3. transfer bridge deployment;
4. Bank B isolation;
5. paired charged-in/depleted-out magazine movement;
6. latching;
7. coolant/data connection;
8. insulation/precharge;
9. bus connection;
10. Bank A/B transition;
11. bridge retract;
12. separation.

Show mass arrows entering and leaving equally.

Show:

- recipient gross mass;
- donor gross mass;
- CG shift;
- connected banks;
- energy inventory;
- no enormous charging cable.

Add reduced-motion step controls.

---

# 25. Inspection UI

Create a representative module digital twin.

Show:

- ID;
- chemistry profile;
- SOC/SOH;
- capacity;
- resistance;
- temperature;
- cycles;
- mission history;
- shock/vibration;
- last fast inspection;
- last CT;
- last ultrasound;
- anomaly delta from baseline;
- health class;
- next assignment;
- quarantine reason when applicable.

Add inspection-lane controls:

- scanners;
- cells/module;
- seconds/cell;
- percentage receiving CT;
- ultrasound lanes;
- queue.

Do not use fake “AI detected 99.99% safe” language.

---

# 26. Comparison with alternatives

Add a concise collapsible comparison.

## Battery module exchange — selected B.C. default

- high electricity-to-bus efficiency;
- clean local grid;
- invariant cargo mass;
- no rapid electrical charge interface;
- continuous inspection;
- high battery capital and mass.

## Direct airborne charging

- avoids physical module handling;
- requires enormous transfer power and recipient charge acceptance;
- adds heat and conversion;
- not selected.

## Dense liquid fuel / SAF

- far better energy density;
- useful future remote fallback;
- lower clean-electricity-to-work efficiency;
- changing mass, liquid transfer, combustion systems;
- not primary B.C. model.

## Hydrogen

- high gravimetric but low volumetric energy;
- very cold or high-pressure storage;
- flammability and transfer complexity;
- not selected.

## LN₂

- valuable mass-control medium;
- lower round-trip electrical efficiency;
- retained as ballast battery rather than primary energy logistics.

## Solar

- excellent endurance extender;
- intermittent and insufficient alone for major regional demand.

Do not argue that battery exchange is universally optimal.

---

# 27. Current research and source section

Add source notes for:

- BC Hydro clean generation mix;
- BC Hydro maximum capacity;
- BC Hydro transmission connections;
- RS 1830 rates effective April 1, 2026;
- BC Hydro 2026 interconnection workshop scenarios;
- DOE battery-pack cost;
- BloombergNEF 2025 pack prices;
- NASA cell-to-pack scaling and 300 Wh/kg research assumptions;
- NREL 85% RTE modeling;
- IEC 62840-1/-2 battery swapping;
- CATL QIJI heavy-truck swap as commercial precedent;
- MCS up to 3.75 MW;
- NASA NEAT MW-scale aircraft testing;
- UL 9540A;
- NASA CT and ultrasound workshop material;
- DOE battery recycling/second-life work.

Use exact dates and distinguish:

- official data;
- vendor claim;
- research assumption;
- Pink simulation assumption.

---

# 28. Performance

Do not instantiate:

- millions of cells;
- thousands of individual modules for every vehicle;
- one interval per module;
- one animated DOM object per magazine.

Use:

- aggregate inventory cohorts;
- one global simulation clock;
- deterministic derived state;
- instanced representative modules in 3D;
- detailed digital twins only for selected examples;
- memoized calculations;
- workers for expensive routing/inventory optimization if needed.

The page must remain smooth with the existing wildfire fleet plus energy logistics.

---

# 29. Accessibility

Provide:

- non-map energy-network table;
- keyboard-selectable depots/tenders;
- DOM-based state summaries;
- pause/resume;
- previous/next phase;
- reduced-motion exchange;
- text equivalent for energy-flow and inspection charts;
- no status communicated only by color.

---

# 30. Tests

Add unit tests for:

- charged and depleted modules retaining the same gross mass;
- \(E/c^2\) mass difference calculation;
- PEM and magazine energy;
- PE1000/PE10000 inventory;
- usable DoD;
- equivalent transfer rate;
- exchange time;
- paired mass balance;
- CG bound;
- bank isolation;
- recipient endurance;
- grid input;
- inventory sizing;
- module mass flow;
- tariff arithmetic;
- battery wear cost;
- solar peak;
- drag-power sensitivity;
- module state transitions;
- quarantine;
- inspection queues;
- tender dispatch;
- no available depot;
- weather hold;
- deterministic simulation.

Required numerical checks:

- 5 t magazine at 300 Wh/kg = 1.5 MWh nameplate;
- 80% usable = 1.2 MWh;
- eight ports, 30 seconds = 1.152 GW usable equivalent;
- PE1000 at 900 t and 300 Wh/kg = 270 MWh;
- PE10000 at 9,000 t = 2.7 GWh;
- 400 MW / 0.85 = 470.588 MW grid before overhead;
- 400 MW × 6 h × 1.2 / 0.8 = 3.6 GWh nameplate inventory;
- $300/kWh, 2,000 cycles, 80% DoD = $187.50/MWh wear;
- 2.7 GWh charge mass difference ≈ 0.108 g.

Add integration tests for:

- page load;
- toggle energy layer;
- select depot;
- select P-E1000;
- select P-E10000;
- inspect recipient logistics;
- run exchange;
- modify assumptions;
- see grid/inventory/cost update;
- reduced motion;
- mobile layout;
- fallback data.

---

# 31. Acceptance criteria

The feature is complete when:

1. “Energy as Cargo” is a first-class section.
2. The primary B.C. architecture no longer depends on Jet A/SAF.
3. Batteries, solar, and LN₂ have clearly distinct roles.
4. P-E1000 and P-E10000 exist in shared configuration.
5. The baseline 900 t / 9,000 t inventories calculate correctly.
6. Standard PEMs and magazines are modeled.
7. Charged/depleted mass invariance is explained.
8. Exchanges are paired and mass-balanced.
9. Segmented banks retain flight power.
10. Gigawatt-equivalent transfer is calculated and qualified.
11. Mass flow is displayed.
12. Ground depots have charging, inspection, reserve, quarantine, and transfer states.
13. Grid power and circulating inventory are calculated separately.
14. Battery capital and wear are visible.
15. BC Hydro tariff arithmetic is dated and sourced.
16. Conceptual depots cannot be mistaken for approved grid capacity.
17. P-E1000 logistics animate on the map.
18. P-E10000 buffers animate or appear as strategic nodes.
19. Recipient panels show endurance and planned exchanges.
20. Depot panels show inventory and bottlenecks.
21. Inspection uses a tiered model.
22. Full CT every cell every touch is not falsely presented as current capability.
23. The system uses aggregate inventory for performance.
24. Accessibility and reduced motion work.
25. Tests, type checking, linting, and production build pass.
26. The final implementation reports all deliberate simplifications.

---

# 32. Suggested implementation order

## Foundation

- shared assumptions;
- calculation library;
- PEM/magazine types;
- energy carrier classes;
- depot types;
- unit tests.

## Static explanation

- Energy as Cargo content;
- architecture diagram;
- class comparison;
- alternative comparison;
- source/methodology.

## Simulation

- recipient energy forecast;
- depot inventory;
- P-E1000 dispatch;
- P-E10000 reserve;
- exchange plans;
- global clock integration.

## UI

- map layers;
- detail panels;
- energy-flow diagram;
- depot queue;
- cost/assumption controls;
- inspection digital twin.

## 3D integration

- paired magazine exchange;
- segmented bank visualization;
- depot handling;
- reduced-motion phases.

## Refinement

- performance;
- mobile;
- accessibility;
- tests;
- static fallback;
- documentation.

---

# 33. Final report from the coding agent

At completion, report:

- exact routes/components changed;
- architecture decisions;
- assumptions;
- equations;
- data sources;
- default depot and fleet configuration;
- how P-E1000/P-E10000 dispatch works;
- how module inventory is aggregated;
- how exchange is animated;
- cost outputs;
- test/build results;
- deliberate simplifications;
- remaining high-value work;
- screenshots of:
  - Energy as Cargo overview;
  - depot;
  - P-E1000;
  - P-E10000;
  - paired exchange;
  - inspection view;
  - mobile layout.
