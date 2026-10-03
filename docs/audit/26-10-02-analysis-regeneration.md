# Analysis regeneration, 2026-10-02

The 2026-08-13 capsule change a32809fb5536e3dace98541cc6594820568c806c changed nominal fleet dimensions and cycle inputs in research/figures.json, while leaving the mass-budget generator and its spheroid area call unchanged. The three generated analyses were not refreshed then. This regeneration uses the existing capsule area function, as ruled on 2026-10-02. The old-formula regeneration is superseded: it reproduced stale-cache effects but still priced the wrong surface. The first-study film reference remains the dated 190 by 47 m spheroid. No energy model is changed; regenerated energy context is recorded here for its owner.

Each pointer identifies its printed JSON location. The companion JSON preserves full values and historical inputs.

| Printed at | Old | New | Cause | Float effect |
|---|---:|---:|---|---|
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/credible/16 cycles/batteryMWh | 20.05 | 22.26 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/credible/16 cycles/batteryT | 66.8 | 74.2 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/credible/16 cycles/leftForShellT | -155.3 | -161.1 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/credible/16 cycles/totalT | 278.6 | 285.3 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/credible/2 cycles/batteryMWh | 2.51 | 2.78 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/credible/2 cycles/batteryT | 8.4 | 9.3 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/credible/2 cycles/leftForShellT | -96.8 | -96.2 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/credible/2 cycles/totalT | 211.3 | 210.6 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/credible/4 cycles/batteryMWh | 5.01 | 5.56 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/credible/4 cycles/batteryT | 16.7 | 18.5 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/credible/4 cycles/leftForShellT | -105.2 | -105.5 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/credible/4 cycles/totalT | 220.9 | 221.3 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/credible/8 cycles/batteryMWh | 10.02 | 11.13 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/credible/8 cycles/batteryT | 33.4 | 37.1 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/credible/8 cycles/leftForShellT | -121.9 | -124.0 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/credible/8 cycles/totalT | 240.2 | 242.6 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/demonstrated/16 cycles/batteryMWh | 20.05 | 22.26 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/demonstrated/16 cycles/batteryT | 134.6 | 149.4 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/demonstrated/16 cycles/leftForShellT | -597.7 | -600.2 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/demonstrated/16 cycles/totalT | 817.3 | 820.2 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/demonstrated/2 cycles/batteryMWh | 2.51 | 2.78 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/demonstrated/2 cycles/batteryT | 16.8 | 18.7 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/demonstrated/2 cycles/leftForShellT | -480.0 | -469.5 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/demonstrated/2 cycles/totalT | 676.0 | 663.4 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/demonstrated/4 cycles/batteryMWh | 5.01 | 5.56 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/demonstrated/4 cycles/batteryT | 33.6 | 37.3 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/demonstrated/4 cycles/leftForShellT | -496.8 | -488.1 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/demonstrated/4 cycles/totalT | 696.2 | 685.8 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/demonstrated/8 cycles/batteryMWh | 10.02 | 11.13 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/demonstrated/8 cycles/batteryT | 67.3 | 74.7 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/demonstrated/8 cycles/leftForShellT | -530.5 | -525.5 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/demonstrated/8 cycles/totalT | 736.5 | 730.6 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/floor/16 cycles/batteryMWh | 20.05 | 22.26 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/floor/16 cycles/batteryT | 40.1 | 44.5 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/floor/16 cycles/leftForShellT | 6.0 | 1.7 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/floor/16 cycles/requiredShellKgPerM3 | 0.0272 | 0.0078 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/floor/16 cycles/totalT | 93.4 | 98.1 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/floor/2 cycles/batteryMWh | 2.51 | 2.78 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/floor/2 cycles/batteryT | 5.0 | 5.6 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/floor/2 cycles/leftForShellT | 41.1 | 40.7 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/floor/2 cycles/requiredShellKgPerM3 | 0.1866 | 0.1848 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/floor/2 cycles/totalT | 54.8 | 55.3 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/floor/4 cycles/batteryMWh | 5.01 | 5.56 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/floor/4 cycles/batteryT | 10.0 | 11.1 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/floor/4 cycles/leftForShellT | 36.0 | 35.1 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/floor/4 cycles/requiredShellKgPerM3 | 0.1638 | 0.1596 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/floor/4 cycles/totalT | 60.4 | 61.4 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/floor/8 cycles/batteryMWh | 10.02 | 11.13 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/floor/8 cycles/batteryT | 20.0 | 22.3 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/floor/8 cycles/leftForShellT | 26.0 | 24.0 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/floor/8 cycles/requiredShellKgPerM3 | 0.1183 | 0.109 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/batterySensitivity/floor/8 cycles/totalT | 71.4 | 73.6 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/cases/credible/baseExShellExSundriesT | 242.09 | 240.53 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/cases/credible/everythingButShellT | 303.1 | 301.4 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/cases/credible/lines/1/tonnes | 9.8 | 8.24 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/cases/credible/lines/15/tonnes | 61.06 | 60.83 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/cases/credible/overBy | 4.68 | 4.66 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/cases/credible/totalT | 468.1 | 466.4 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/cases/demonstrated/baseExShellExSundriesT | 680.74 | 668.37 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/cases/demonstrated/everythingButShellT | 867.9 | 853.1 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/cases/demonstrated/lines/1/tonnes | 77.94 | 65.57 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/cases/demonstrated/lines/15/tonnes | 187.19 | 184.71 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/cases/demonstrated/overBy | 11.23 | 11.08 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/cases/demonstrated/totalT | 1123.1 | 1108.3 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/cases/floor/baseExShellExSundriesT | 84.84 | 84.68 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/cases/floor/everythingButShellT | 104.5 | 104.3 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/cases/floor/lines/1/tonnes | 0.98 | 0.82 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/cases/floor/lines/15/tonnes | 19.66 | 19.64 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/cases/floor/totalT | 216.3 | 216.1 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/descentWithoutNitrogen/cycleMWhAsBuilt | 1.253 | 1.391 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/descentWithoutNitrogen/cycleMWhWithoutCryo | 0.595 | 0.733 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/descentWithoutNitrogen/cycleSavingPct | 52.5 | 47.3 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/hullAreaM2 | 22592 | 19007 | capsule surface and refreshed capsule-era inputs | geometry/allowance denominator; not a structural result |
| research/analysis/mass-budget.json#/classes/P100/requiredKgPerM2 | 4.426 | 5.261 | capsule surface and refreshed capsule-era inputs | geometry/allowance denominator; not a structural result |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/baseExShellExSundriesT | 187.95 | 187.77 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.74/0.264/diaM | 71 | 83 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.74/0.264/lenM | 287 | 166 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.74/0.264/timesBaseline | 3.44 | 3.42 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.74/0.264/volumeM3 | 757318 | 751301 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.74/0.508/diaM | 95 | 111 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.74/0.508/lenM | 385 | 221 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.74/0.508/timesBaseline | 8.29 | 8.14 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.74/0.508/volumeM3 | 1823933 | 1791764 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.85/0.264/diaM | 66 | 77 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.85/0.264/lenM | 266 | 154 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.85/0.264/timesBaseline | 2.74 | 2.72 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.85/0.264/volumeM3 | 602996 | 599285 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.85/0.508/diaM | 81 | 95 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.85/0.508/lenM | 329 | 189 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.85/0.508/timesBaseline | 5.17 | 5.11 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.85/0.508/volumeM3 | 1138161 | 1124703 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.85/0.750/diaM | 151 | 174 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.85/0.750/lenM | 611 | 348 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.85/0.750/timesBaseline | 33.25 | 31.71 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.85/0.750/volumeM3 | 7315760 | 6976947 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=1.0/0.264/diaM | 61 | 71 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=1.0/0.264/lenM | 245 | 142 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=1.0/0.264/timesBaseline | 2.14 | 2.13 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=1.0/0.264/volumeM3 | 471338 | 469225 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=1.0/0.508/diaM | 71 | 83 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=1.0/0.508/lenM | 286 | 165 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=1.0/0.508/timesBaseline | 3.4 | 3.38 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=1.0/0.508/volumeM3 | 748634 | 742759 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=1.0/0.750/diaM | 94 | 109 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=1.0/0.750/lenM | 380 | 219 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=1.0/0.750/timesBaseline | 7.98 | 7.85 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=1.0/0.750/volumeM3 | 1756369 | 1726314 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/everythingButShellT | 240.9 | 240.7 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.264/diaM | 61 | 71 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.264/lenM | 245 | 142 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.264/timesBaseline | 2.14 | 2.13 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.264/volumeM3 | 471338 | 469225 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.350/diaM | 63 | 74 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.350/lenM | 257 | 148 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.350/timesBaseline | 2.47 | 2.45 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.350/volumeM3 | 542365 | 539434 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.508/diaM | 71 | 83 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.508/lenM | 286 | 165 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.508/timesBaseline | 3.4 | 3.38 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.508/volumeM3 | 748634 | 742759 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.600/diaM | 77 | 90 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.600/lenM | 310 | 179 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.600/timesBaseline | 4.36 | 4.32 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.600/volumeM3 | 959615 | 949938 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.750/diaM | 94 | 109 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.750/lenM | 380 | 219 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.750/timesBaseline | 7.98 | 7.85 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.750/volumeM3 | 1756369 | 1726314 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.900/diaM | 158 | 182 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.900/lenM | 641 | 365 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.900/timesBaseline | 38.33 | 36.4 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.900/volumeM3 | 8433177 | 8007682 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/lines/1/tonnes | 9.8 | 8.24 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/lines/15/tonnes | 52.94 | 52.92 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/lines/3/tonnes | 12.53 | 13.91 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/shellBudgetLeftT | -101.0 | -100.8 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/totalT | 405.9 | 405.7 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/baseExShellExSundriesT | 571.74 | 562.15 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.74/0.264/diaM | 110 | 125 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.74/0.264/lenM | 443 | 249 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.74/0.264/timesBaseline | 12.69 | 11.62 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.74/0.264/volumeM3 | 2791792 | 2556442 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.74/0.508/diaM | 167 | 185 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.74/0.508/lenM | 675 | 370 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.74/0.508/timesBaseline | 44.83 | 38.06 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.74/0.508/volumeM3 | 9862367 | 8373478 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.85/0.264/diaM | 99 | 113 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.85/0.264/lenM | 401 | 227 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.85/0.264/timesBaseline | 9.43 | 8.76 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.85/0.264/volumeM3 | 2075358 | 1926413 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.85/0.508/diaM | 132 | 149 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.85/0.508/lenM | 534 | 297 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.85/0.508/timesBaseline | 22.19 | 19.72 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.85/0.508/volumeM3 | 4882494 | 4338405 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.85/0.750/diaM | 380 | 397 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.85/0.750/lenM | 1536 | 794 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.85/0.750/timesBaseline | 528.32 | 375.61 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.85/0.750/volumeM3 | 116230555 | 82633219 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=1.0/0.264/diaM | 90 | 103 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=1.0/0.264/lenM | 362 | 205 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=1.0/0.264/timesBaseline | 6.92 | 6.51 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=1.0/0.264/volumeM3 | 1522629 | 1431105 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=1.0/0.508/diaM | 109 | 124 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=1.0/0.508/lenM | 441 | 248 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=1.0/0.508/timesBaseline | 12.5 | 11.45 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=1.0/0.508/volumeM3 | 2749504 | 2519581 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=1.0/0.750/diaM | 164 | 182 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=1.0/0.750/lenM | 662 | 363 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=1.0/0.750/timesBaseline | 42.27 | 36.04 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=1.0/0.750/volumeM3 | 9299500 | 7927907 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/everythingButShellT | 737.1 | 725.6 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.264/diaM | 90 | 103 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.264/lenM | 362 | 205 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.264/timesBaseline | 6.92 | 6.51 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.264/volumeM3 | 1522629 | 1431105 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.350/diaM | 95 | 109 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.350/lenM | 384 | 217 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.350/timesBaseline | 8.25 | 7.7 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.350/volumeM3 | 1814147 | 1693460 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.508/diaM | 109 | 124 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.508/lenM | 441 | 248 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.508/timesBaseline | 12.5 | 11.45 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.508/volumeM3 | 2749504 | 2519581 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.600/diaM | 122 | 138 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.600/lenM | 493 | 276 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.600/timesBaseline | 17.47 | 15.74 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.600/volumeM3 | 3844427 | 3462698 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.750/diaM | 164 | 182 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.750/lenM | 662 | 363 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.750/timesBaseline | 42.27 | 36.04 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.750/volumeM3 | 9299500 | 7927907 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.900/diaM | 417 | 433 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.900/lenM | 1684 | 866 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.900/timesBaseline | 696.33 | 487.13 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.900/volumeM3 | 153193461 | 107169282 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/lines/1/tonnes | 77.94 | 65.57 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/lines/15/tonnes | 165.39 | 163.47 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/lines/3/tonnes | 25.23 | 28.01 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/overBy | 9.92 | 9.81 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/shellBudgetLeftT | -488.4 | -478.8 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/totalT | 992.3 | 980.8 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/baseExShellExSundriesT | 52.36 | 53.03 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.74/0.264/diaM | 55 | 65 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.74/0.264/lenM | 223 | 130 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.74/0.264/volumeM3 | 357865 | 359402 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.74/0.508/diaM | 73 | 85 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.74/0.508/lenM | 294 | 170 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.74/0.508/timesBaseline | 3.69 | 3.7 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.74/0.508/volumeM3 | 811637 | 814181 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.85/0.264/diaM | 51 | 60 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.85/0.264/lenM | 208 | 121 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.85/0.264/timesBaseline | 1.31 | 1.32 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.85/0.264/volumeM3 | 288126 | 289426 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.85/0.508/diaM | 63 | 74 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.85/0.508/lenM | 254 | 147 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.85/0.508/timesBaseline | 2.39 | 2.4 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.85/0.508/volumeM3 | 525039 | 527049 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.85/0.750/diaM | 109 | 127 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.85/0.750/lenM | 440 | 255 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.85/0.750/volumeM3 | 2725986 | 2725487 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=1.0/0.264/diaM | 48 | 56 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=1.0/0.264/lenM | 192 | 111 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=1.0/0.264/timesBaseline | 1.03 | 1.04 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=1.0/0.264/volumeM3 | 227571 | 228644 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=1.0/0.508/diaM | 55 | 65 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=1.0/0.508/lenM | 223 | 129 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=1.0/0.508/timesBaseline | 1.61 | 1.62 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=1.0/0.508/volumeM3 | 353975 | 355499 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=1.0/0.750/diaM | 72 | 84 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=1.0/0.750/lenM | 290 | 168 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=1.0/0.750/timesBaseline | 3.56 | 3.58 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=1.0/0.750/volumeM3 | 784115 | 786622 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/everythingButShellT | 68.8 | 69.5 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.264/diaM | 48 | 56 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.264/lenM | 192 | 111 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.264/timesBaseline | 1.03 | 1.04 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.264/volumeM3 | 227571 | 228644 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.350/diaM | 50 | 58 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.350/lenM | 201 | 117 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.350/timesBaseline | 1.18 | 1.19 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.350/volumeM3 | 260368 | 261566 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.508/diaM | 55 | 65 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.508/lenM | 223 | 129 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.508/timesBaseline | 1.61 | 1.62 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.508/volumeM3 | 353975 | 355499 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.600/diaM | 60 | 70 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.600/lenM | 241 | 140 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.600/timesBaseline | 2.03 | 2.04 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.600/volumeM3 | 447479 | 449285 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.750/diaM | 72 | 84 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.750/lenM | 290 | 168 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.750/timesBaseline | 3.56 | 3.58 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.750/volumeM3 | 784115 | 786622 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.900/diaM | 113 | 132 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.900/lenM | 457 | 265 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.900/timesBaseline | 13.92 | 13.91 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.900/volumeM3 | 3062477 | 3060477 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/lines/1/tonnes | 0.98 | 0.82 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/lines/15/tonnes | 16.41 | 16.48 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/lines/3/tonnes | 7.52 | 8.35 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/requiredShellKgPerM3 | 0.1752 | 0.1722 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/shellBudgetLeftT | 38.5 | 37.9 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/totalT | 180.5 | 181.3 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/credible/16 cycles/batteryMWh | 118.38 | 135.26 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/credible/16 cycles/batteryT | 394.6 | 450.9 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/credible/16 cycles/leftForShellT | -535.4 | -577.3 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/credible/16 cycles/totalT | 1615.7 | 1663.9 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/credible/2 cycles/batteryMWh | 14.8 | 16.91 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/credible/2 cycles/batteryT | 49.3 | 56.4 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/credible/2 cycles/leftForShellT | -190.1 | -182.8 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/credible/2 cycles/totalT | 1218.6 | 1210.2 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/credible/4 cycles/batteryMWh | 29.6 | 33.82 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/credible/4 cycles/batteryT | 98.7 | 112.7 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/credible/4 cycles/leftForShellT | -239.4 | -239.1 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/credible/4 cycles/totalT | 1275.3 | 1275.0 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/credible/8 cycles/batteryMWh | 59.19 | 67.63 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/credible/8 cycles/batteryT | 197.3 | 225.4 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/credible/8 cycles/leftForShellT | -338.1 | -351.8 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/credible/8 cycles/totalT | 1388.8 | 1404.6 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/demonstrated/16 cycles/batteryMWh | 118.38 | 135.26 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/demonstrated/16 cycles/batteryT | 794.5 | 907.8 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/demonstrated/16 cycles/leftForShellT | -2815.5 | -2875.7 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/demonstrated/16 cycles/totalT | 4378.6 | 4450.9 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/demonstrated/2 cycles/batteryMWh | 14.8 | 16.91 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/demonstrated/2 cycles/batteryT | 99.3 | 113.5 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/demonstrated/2 cycles/leftForShellT | -2120.3 | -2081.4 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/demonstrated/2 cycles/totalT | 3544.3 | 3497.7 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/demonstrated/4 cycles/batteryMWh | 29.6 | 33.82 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/demonstrated/4 cycles/batteryT | 198.6 | 227.0 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/demonstrated/4 cycles/leftForShellT | -2219.6 | -2194.9 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/demonstrated/4 cycles/totalT | 3663.5 | 3633.9 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/demonstrated/8 cycles/batteryMWh | 59.19 | 67.63 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/demonstrated/8 cycles/batteryT | 397.3 | 453.9 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/demonstrated/8 cycles/leftForShellT | -2418.2 | -2421.8 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/demonstrated/8 cycles/totalT | 3901.9 | 3906.2 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/floor/16 cycles/batteryMWh | 118.38 | 135.26 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/floor/16 cycles/batteryT | 236.8 | 270.5 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/floor/16 cycles/leftForShellT | 388.8 | 356.5 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/floor/16 cycles/requiredShellKgPerM3 | 0.1767 | 0.162 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/floor/16 cycles/totalT | 572.3 | 607.9 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/floor/2 cycles/batteryMWh | 14.8 | 16.91 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/floor/2 cycles/batteryT | 29.6 | 33.8 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/floor/2 cycles/leftForShellT | 596.0 | 593.2 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/floor/2 cycles/requiredShellKgPerM3 | 0.2709 | 0.2696 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/floor/2 cycles/totalT | 344.4 | 347.5 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/floor/4 cycles/batteryMWh | 29.6 | 33.82 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/floor/4 cycles/batteryT | 59.2 | 67.6 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/floor/4 cycles/leftForShellT | 566.4 | 559.4 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/floor/4 cycles/requiredShellKgPerM3 | 0.2574 | 0.2543 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/floor/4 cycles/totalT | 377.0 | 384.7 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/floor/8 cycles/batteryMWh | 59.19 | 67.63 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/floor/8 cycles/batteryT | 118.4 | 135.3 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/floor/8 cycles/leftForShellT | 507.2 | 491.7 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/floor/8 cycles/requiredShellKgPerM3 | 0.2305 | 0.2235 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/batterySensitivity/floor/8 cycles/totalT | 442.1 | 459.1 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/cases/credible/baseExShellExSundriesT | 1410.33 | 1395.97 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/cases/credible/everythingButShellT | 1869.4 | 1852.9 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/cases/credible/lines/1/tonnes | 97.51 | 83.15 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/cases/credible/lines/15/tonnes | 459.05 | 456.9 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/cases/credible/overBy | 3.52 | 3.5 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/cases/credible/totalT | 3519.4 | 3502.9 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/cases/demonstrated/baseExShellExSundriesT | 3659.66 | 3606.63 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/cases/demonstrated/everythingButShellT | 4902.0 | 4838.4 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/cases/demonstrated/lines/1/tonnes | 360.0 | 306.97 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/cases/demonstrated/lines/15/tonnes | 1242.33 | 1231.73 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/cases/demonstrated/overBy | 7.45 | 7.39 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/cases/demonstrated/totalT | 7454.0 | 7390.4 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/cases/floor/baseExShellExSundriesT | 523.52 | 522.08 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/cases/floor/everythingButShellT | 687.6 | 686.0 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/cases/floor/lines/1/tonnes | 9.75 | 8.31 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/cases/floor/lines/15/tonnes | 164.11 | 163.97 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/cases/floor/overBy | 1.81 | 1.8 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/cases/floor/totalT | 1805.2 | 1803.6 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/descentWithoutNitrogen/cycleMWhAsBuilt | 7.399 | 8.454 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/descentWithoutNitrogen/cycleMWhWithoutCryo | 4.703 | 5.758 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/descentWithoutNitrogen/cycleSavingPct | 36.4 | 31.9 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/hullAreaM2 | 104349 | 88976 | capsule surface and refreshed capsule-era inputs | geometry/allowance denominator; not a structural result |
| research/analysis/mass-budget.json#/classes/P1000/requiredKgPerM2 | 9.583 | 11.239 | capsule surface and refreshed capsule-era inputs | geometry/allowance denominator; not a structural result |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/baseExShellExSundriesT | 1084.32 | 1080.51 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.74/0.264/diaM | 137 | 159 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.74/0.264/lenM | 542 | 318 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.74/0.264/timesBaseline | 2.41 | 2.39 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.74/0.264/volumeM3 | 5298629 | 5256638 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.74/0.508/diaM | 183 | 212 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.74/0.508/lenM | 725 | 424 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.74/0.508/timesBaseline | 5.78 | 5.67 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.74/0.508/volumeM3 | 12706475 | 12478961 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.85/0.264/diaM | 127 | 148 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.85/0.264/lenM | 502 | 295 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.85/0.264/timesBaseline | 1.92 | 1.91 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.85/0.264/volumeM3 | 4222239 | 4196569 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.85/0.508/diaM | 157 | 182 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.85/0.508/lenM | 620 | 364 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.85/0.508/timesBaseline | 3.61 | 3.57 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.85/0.508/volumeM3 | 7949564 | 7854781 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.85/0.750/diaM | 290 | 332 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.85/0.750/lenM | 1147 | 665 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.85/0.750/timesBaseline | 22.87 | 21.78 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.85/0.750/volumeM3 | 50306574 | 47925841 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=1.0/0.264/diaM | 117 | 136 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=1.0/0.264/lenM | 463 | 272 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=1.0/0.264/timesBaseline | 1.5 | 1.49 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=1.0/0.264/volumeM3 | 3302788 | 3288408 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=1.0/0.508/diaM | 136 | 158 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=1.0/0.508/lenM | 539 | 317 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=1.0/0.508/timesBaseline | 2.38 | 2.36 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=1.0/0.508/volumeM3 | 5238099 | 5197109 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=1.0/0.750/diaM | 181 | 210 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=1.0/0.750/lenM | 716 | 419 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=1.0/0.750/timesBaseline | 5.56 | 5.47 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=1.0/0.750/volumeM3 | 12238660 | 12026131 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/everythingButShellT | 1494.5 | 1490.1 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.264/diaM | 117 | 136 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.264/lenM | 463 | 272 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.264/timesBaseline | 1.5 | 1.49 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.264/volumeM3 | 3302788 | 3288408 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.350/diaM | 122 | 143 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.350/lenM | 485 | 285 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.350/timesBaseline | 1.73 | 1.72 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.350/volumeM3 | 3798952 | 3778798 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.508/diaM | 136 | 158 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.508/lenM | 539 | 317 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.508/timesBaseline | 2.38 | 2.36 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.508/volumeM3 | 5238099 | 5197109 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.600/diaM | 148 | 172 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.600/lenM | 586 | 344 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.600/timesBaseline | 3.05 | 3.02 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.600/volumeM3 | 6707672 | 6639723 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.750/diaM | 181 | 210 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.750/lenM | 716 | 419 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.750/timesBaseline | 5.56 | 5.47 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.750/volumeM3 | 12238660 | 12026131 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.900/diaM | 303 | 348 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.900/lenM | 1202 | 695 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.900/timesBaseline | 26.31 | 24.95 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.900/volumeM3 | 57879596 | 54895008 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/lines/1/tonnes | 97.51 | 83.15 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/lines/15/tonnes | 410.15 | 409.58 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/lines/3/tonnes | 73.99 | 84.54 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/shellBudgetLeftT | -214.8 | -210.9 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/totalT | 3144.5 | 3140.1 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/baseExShellExSundriesT | 3003.26 | 2971.47 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.74/0.264/diaM | 183 | 211 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.74/0.264/lenM | 725 | 422 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.74/0.264/timesBaseline | 5.79 | 5.57 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.74/0.264/volumeM3 | 12732283 | 12252804 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.74/0.508/diaM | 259 | 294 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.74/0.508/lenM | 1024 | 589 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.74/0.508/timesBaseline | 16.28 | 15.12 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.74/0.508/volumeM3 | 35813317 | 33268676 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.85/0.264/diaM | 168 | 194 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.85/0.264/lenM | 666 | 388 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.85/0.264/timesBaseline | 4.48 | 4.34 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.85/0.264/volumeM3 | 9858098 | 9546847 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.85/0.508/diaM | 214 | 245 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.85/0.508/lenM | 848 | 491 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.85/0.508/timesBaseline | 9.25 | 8.78 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.85/0.508/volumeM3 | 20347491 | 19310540 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.85/0.750/diaM | 482 | 529 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.85/0.750/lenM | 1907 | 1058 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.85/0.750/timesBaseline | 105.2 | 87.77 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.85/0.750/volumeM3 | 231441856 | 193090069 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=1.0/0.264/diaM | 154 | 178 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=1.0/0.264/lenM | 608 | 355 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=1.0/0.264/timesBaseline | 3.41 | 3.32 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=1.0/0.264/volumeM3 | 7508387 | 7313772 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=1.0/0.508/diaM | 182 | 210 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=1.0/0.508/lenM | 722 | 420 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=1.0/0.508/timesBaseline | 5.71 | 5.5 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=1.0/0.508/volumeM3 | 12567220 | 12098099 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=1.0/0.750/diaM | 255 | 290 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=1.0/0.750/lenM | 1008 | 580 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=1.0/0.750/timesBaseline | 15.54 | 14.47 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=1.0/0.750/volumeM3 | 34193223 | 31825841 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/everythingButShellT | 4114.3 | 4076.2 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.264/diaM | 154 | 178 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.264/lenM | 608 | 355 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.264/timesBaseline | 3.41 | 3.32 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.264/volumeM3 | 7508387 | 7313772 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.350/diaM | 162 | 187 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.350/lenM | 640 | 374 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.350/timesBaseline | 3.98 | 3.87 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.350/volumeM3 | 8764007 | 8509580 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.508/diaM | 182 | 210 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.508/lenM | 722 | 420 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.508/timesBaseline | 5.71 | 5.5 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.508/volumeM3 | 12567220 | 12098099 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.600/diaM | 200 | 230 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.600/lenM | 794 | 461 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.600/timesBaseline | 7.59 | 7.24 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.600/volumeM3 | 16687176 | 15936605 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.750/diaM | 255 | 290 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.750/lenM | 1008 | 580 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.750/timesBaseline | 15.54 | 14.47 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.750/volumeM3 | 34193223 | 31825841 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.900/diaM | 517 | 565 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.900/lenM | 2046 | 1129 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.900/timesBaseline | 129.85 | 106.76 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.900/volumeM3 | 285676058 | 234865032 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/lines/1/tonnes | 360.0 | 306.97 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/lines/15/tonnes | 1111.05 | 1104.69 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/lines/3/tonnes | 148.97 | 170.21 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/overBy | 6.67 | 6.63 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/shellBudgetLeftT | -2169.9 | -2138.1 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/totalT | 6666.3 | 6628.2 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/baseExShellExSundriesT | 327.91 | 332.8 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=0.74/0.264/diaM | 114 | 133 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=0.74/0.264/lenM | 452 | 266 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=0.74/0.264/volumeM3 | 3076424 | 3087784 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=0.74/0.508/diaM | 149 | 175 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=0.74/0.508/lenM | 592 | 349 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=0.74/0.508/timesBaseline | 3.15 | 3.16 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=0.74/0.508/volumeM3 | 6926097 | 6944272 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=0.85/0.264/diaM | 106 | 124 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=0.85/0.264/lenM | 420 | 248 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=0.85/0.264/volumeM3 | 2480324 | 2489979 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=0.85/0.508/diaM | 129 | 151 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=0.85/0.508/lenM | 513 | 302 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=0.85/0.508/volumeM3 | 4500170 | 4514847 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=0.85/0.750/diaM | 222 | 259 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=0.85/0.750/lenM | 881 | 519 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=0.85/0.750/volumeM3 | 22777568 | 22768289 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=1.0/0.264/diaM | 98 | 115 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=1.0/0.264/lenM | 389 | 229 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=1.0/0.264/timesBaseline | 0.89 | 0.9 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=1.0/0.264/volumeM3 | 1961575 | 1969581 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=1.0/0.508/diaM | 114 | 133 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=1.0/0.508/lenM | 450 | 266 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=1.0/0.508/timesBaseline | 1.38 | 1.39 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=1.0/0.508/volumeM3 | 3043201 | 3054471 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=1.0/0.750/diaM | 148 | 173 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=1.0/0.750/lenM | 585 | 345 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=1.0/0.750/timesBaseline | 3.04 | 3.05 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=1.0/0.750/volumeM3 | 6693884 | 6711833 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/everythingButShellT | 472.5 | 477.8 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.264/diaM | 98 | 115 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.264/lenM | 389 | 229 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.264/timesBaseline | 0.89 | 0.9 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.264/volumeM3 | 1961575 | 1969581 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.350/diaM | 103 | 120 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.350/lenM | 407 | 240 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.350/volumeM3 | 2242666 | 2251586 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.508/diaM | 114 | 133 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.508/lenM | 450 | 266 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.508/timesBaseline | 1.38 | 1.39 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.508/volumeM3 | 3043201 | 3054471 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.600/diaM | 123 | 143 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.600/lenM | 486 | 287 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.600/volumeM3 | 3840488 | 3853753 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.750/diaM | 148 | 173 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.750/lenM | 585 | 345 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.750/timesBaseline | 3.04 | 3.05 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.750/volumeM3 | 6693884 | 6711833 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.900/diaM | 231 | 269 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.900/lenM | 914 | 539 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.900/timesBaseline | 11.6 | 11.59 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.900/volumeM3 | 25513024 | 25491741 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/lines/1/tonnes | 9.75 | 8.31 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/lines/15/tonnes | 144.55 | 145.04 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/lines/3/tonnes | 44.39 | 50.72 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/overBy | 1.59 | 1.6 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/requiredShellKgPerM3 | 0.2642 | 0.262 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/shellBudgetLeftT | 581.2 | 576.3 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/totalT | 1590.1 | 1595.4 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/credible/16 cycles/batteryMWh | 733.9 | 869.2 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/credible/16 cycles/batteryT | 2446.3 | 2897.3 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/credible/16 cycles/leftForShellT | -62.6 | -365.0 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/credible/16 cycles/totalT | 10072.0 | 10419.8 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/credible/2 cycles/batteryMWh | 91.74 | 108.65 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/credible/2 cycles/batteryT | 305.8 | 362.2 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/credible/2 cycles/leftForShellT | 2077.9 | 2170.2 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/credible/2 cycles/requiredShellKgPerM3 | 0.0945 | 0.0986 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/credible/2 cycles/totalT | 7610.4 | 7504.3 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/credible/4 cycles/batteryMWh | 183.48 | 217.3 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/credible/4 cycles/batteryT | 611.6 | 724.3 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/credible/4 cycles/leftForShellT | 1772.2 | 1808.0 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/credible/4 cycles/requiredShellKgPerM3 | 0.0806 | 0.0822 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/credible/4 cycles/totalT | 7962.0 | 7920.8 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/credible/8 cycles/batteryMWh | 366.95 | 434.6 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/credible/8 cycles/batteryT | 1223.2 | 1448.7 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/credible/8 cycles/leftForShellT | 1160.6 | 1083.7 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/credible/8 cycles/requiredShellKgPerM3 | 0.0528 | 0.0493 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/credible/8 cycles/totalT | 8665.3 | 8753.8 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/demonstrated/16 cycles/batteryMWh | 733.9 | 869.2 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/demonstrated/16 cycles/batteryT | 4925.5 | 5833.6 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/demonstrated/16 cycles/leftForShellT | -10387.0 | -11040.4 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/demonstrated/16 cycles/totalT | 22464.4 | 23248.5 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/demonstrated/2 cycles/batteryMWh | 91.74 | 108.65 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/demonstrated/2 cycles/batteryT | 615.7 | 729.2 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/demonstrated/2 cycles/leftForShellT | -6077.2 | -5936.1 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/demonstrated/2 cycles/totalT | 17292.6 | 17123.3 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/demonstrated/4 cycles/batteryMWh | 183.48 | 217.3 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/demonstrated/4 cycles/batteryT | 1231.4 | 1458.4 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/demonstrated/4 cycles/leftForShellT | -6692.9 | -6665.3 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/demonstrated/4 cycles/totalT | 18031.4 | 17998.3 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/demonstrated/8 cycles/batteryMWh | 366.95 | 434.6 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/demonstrated/8 cycles/batteryT | 2462.8 | 2916.8 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/demonstrated/8 cycles/leftForShellT | -7924.2 | -8123.6 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/demonstrated/8 cycles/totalT | 19509.1 | 19748.4 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/floor/16 cycles/batteryMWh | 733.9 | 869.2 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/floor/16 cycles/batteryT | 1467.8 | 1738.4 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/floor/16 cycles/leftForShellT | 5035.0 | 4779.2 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/floor/16 cycles/requiredShellKgPerM3 | 0.2289 | 0.2172 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/floor/16 cycles/totalT | 4461.6 | 4742.9 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/floor/2 cycles/batteryMWh | 91.74 | 108.65 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/floor/2 cycles/batteryT | 183.5 | 217.3 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/floor/2 cycles/leftForShellT | 6319.3 | 6300.3 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/floor/2 cycles/requiredShellKgPerM3 | 0.2872 | 0.2864 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/floor/2 cycles/totalT | 3048.8 | 3069.6 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/floor/4 cycles/batteryMWh | 183.48 | 217.3 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/floor/4 cycles/batteryT | 367.0 | 434.6 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/floor/4 cycles/leftForShellT | 6135.8 | 6083.0 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/floor/4 cycles/requiredShellKgPerM3 | 0.2789 | 0.2765 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/floor/4 cycles/totalT | 3250.6 | 3308.7 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/floor/8 cycles/batteryMWh | 366.95 | 434.6 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/floor/8 cycles/batteryT | 733.9 | 869.2 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/floor/8 cycles/leftForShellT | 5768.9 | 5648.4 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/floor/8 cycles/requiredShellKgPerM3 | 0.2622 | 0.2567 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/batterySensitivity/floor/8 cycles/totalT | 3654.3 | 3786.7 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/cases/credible/baseExShellExSundriesT | 12978.58 | 12830.0 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/cases/credible/everythingButShellT | 17400.4 | 17229.5 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/cases/credible/lines/1/tonnes | 977.62 | 829.04 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/cases/credible/lines/15/tonnes | 4421.79 | 4399.5 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/cases/credible/overBy | 3.39 | 3.37 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/cases/credible/totalT | 33900.4 | 33729.5 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/cases/demonstrated/baseExShellExSundriesT | 27217.63 | 26963.02 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/cases/demonstrated/everythingButShellT | 37765.2 | 37459.6 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/cases/demonstrated/lines/1/tonnes | 1675.23 | 1420.62 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/cases/demonstrated/lines/15/tonnes | 10547.53 | 10496.6 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/cases/demonstrated/overBy | 6.33 | 6.3 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/cases/demonstrated/totalT | 63285.2 | 62979.6 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/cases/floor/baseExShellExSundriesT | 6588.15 | 6573.29 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/cases/floor/everythingButShellT | 8364.6 | 8348.2 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/cases/floor/lines/1/tonnes | 97.76 | 82.9 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/cases/floor/lines/15/tonnes | 1776.42 | 1774.93 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/cases/floor/totalT | 19540.6 | 19524.2 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/descentWithoutNitrogen/cycleMWhAsBuilt | 45.869 | 54.325 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/descentWithoutNitrogen/cycleMWhWithoutCryo | 38.265 | 46.721 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/descentWithoutNitrogen/cycleSavingPct | 16.6 | 14.0 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/hullAreaM2 | 485575 | 411775 | capsule surface and refreshed capsule-era inputs | geometry/allowance denominator; not a structural result |
| research/analysis/mass-budget.json#/classes/P10000/requiredKgPerM2 | 20.594 | 24.285 | capsule surface and refreshed capsule-era inputs | geometry/allowance denominator; not a structural result |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/baseExShellExSundriesT | 6770.6 | 6706.58 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.74/0.264/diaM | 271 | 315 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.74/0.264/lenM | 1082 | 631 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.74/0.264/timesBaseline | 1.89 | 1.87 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.74/0.264/volumeM3 | 41491383 | 41100464 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.74/0.508/diaM | 362 | 420 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.74/0.508/lenM | 1448 | 841 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.74/0.508/timesBaseline | 4.52 | 4.43 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.74/0.508/volumeM3 | 99413997 | 97369762 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.85/0.264/diaM | 251 | 293 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.85/0.264/lenM | 1003 | 585 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.85/0.264/timesBaseline | 1.5 | 1.49 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.85/0.264/volumeM3 | 33067814 | 32824453 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.85/0.508/diaM | 310 | 360 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.85/0.508/lenM | 1239 | 721 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.85/0.508/timesBaseline | 2.83 | 2.79 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.85/0.508/volumeM3 | 62228487 | 61364304 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.85/0.750/diaM | 572 | 657 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.85/0.750/lenM | 2289 | 1314 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.85/0.750/timesBaseline | 17.84 | 16.89 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.85/0.750/volumeM3 | 392576873 | 371656262 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=1.0/0.264/diaM | 231 | 270 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=1.0/0.264/lenM | 925 | 539 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=1.0/0.264/timesBaseline | 1.18 | 1.17 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=1.0/0.264/volumeM3 | 25870630 | 25730156 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=1.0/0.508/diaM | 270 | 314 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=1.0/0.508/lenM | 1078 | 628 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=1.0/0.508/timesBaseline | 1.86 | 1.85 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=1.0/0.508/volumeM3 | 41017744 | 40635855 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=1.0/0.750/diaM | 358 | 415 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=1.0/0.750/lenM | 1430 | 830 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=1.0/0.750/timesBaseline | 4.35 | 4.27 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=1.0/0.750/volumeM3 | 95758327 | 93846930 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/everythingButShellT | 10261.2 | 10187.6 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.264/diaM | 231 | 270 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.264/lenM | 925 | 539 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.264/timesBaseline | 1.18 | 1.17 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.264/volumeM3 | 25870630 | 25730156 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.350/diaM | 242 | 282 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.350/lenM | 969 | 565 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.350/timesBaseline | 1.35 | 1.34 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.350/volumeM3 | 29754666 | 29561454 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.508/diaM | 270 | 314 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.508/lenM | 1078 | 628 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.508/timesBaseline | 1.86 | 1.85 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.508/volumeM3 | 41017744 | 40635855 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.600/diaM | 293 | 341 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.600/lenM | 1171 | 682 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.600/timesBaseline | 2.39 | 2.36 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.600/volumeM3 | 52515130 | 51890977 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.750/diaM | 358 | 415 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.750/lenM | 1430 | 830 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.750/timesBaseline | 4.35 | 4.27 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.750/volumeM3 | 95758327 | 93846930 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.900/diaM | 600 | 687 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.900/lenM | 2398 | 1374 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.900/timesBaseline | 20.52 | 19.33 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.900/volumeM3 | 451502886 | 425317491 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/lines/1/tonnes | 977.62 | 829.04 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/lines/15/tonnes | 3490.59 | 3480.99 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/lines/3/tonnes | 458.69 | 543.25 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/overBy | 2.68 | 2.67 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/requiredShellKgPerM3 | 0.0875 | 0.0904 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/shellBudgetLeftT | 1925.1 | 1989.1 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/totalT | 26761.2 | 26687.6 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/baseExShellExSundriesT | 14718.35 | 14633.99 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.74/0.264/diaM | 319 | 371 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.74/0.264/lenM | 1275 | 741 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.74/0.264/timesBaseline | 3.08 | 3.03 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.74/0.264/volumeM3 | 67784415 | 66691136 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.74/0.508/diaM | 433 | 500 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.74/0.508/lenM | 1732 | 1001 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.74/0.508/timesBaseline | 7.73 | 7.46 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.74/0.508/volumeM3 | 169992673 | 164208465 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.85/0.264/diaM | 295 | 343 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.85/0.264/lenM | 1179 | 686 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.85/0.264/timesBaseline | 2.44 | 2.4 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.85/0.264/volumeM3 | 53575160 | 52887257 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.85/0.508/diaM | 367 | 426 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.85/0.508/lenM | 1468 | 851 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.85/0.508/timesBaseline | 4.71 | 4.6 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.85/0.508/volumeM3 | 103524890 | 101115005 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.85/0.750/diaM | 717 | 813 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.85/0.750/lenM | 2868 | 1626 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.85/0.750/timesBaseline | 35.08 | 32.02 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.85/0.750/volumeM3 | 771701743 | 704512559 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=1.0/0.264/diaM | 271 | 316 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=1.0/0.264/lenM | 1083 | 631 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=1.0/0.264/timesBaseline | 1.89 | 1.87 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=1.0/0.264/volumeM3 | 41590987 | 41184608 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=1.0/0.508/diaM | 317 | 369 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=1.0/0.508/lenM | 1270 | 738 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=1.0/0.508/timesBaseline | 3.04 | 3.0 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=1.0/0.508/volumeM3 | 66980471 | 65912064 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=1.0/0.750/diaM | 427 | 494 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=1.0/0.750/lenM | 1709 | 988 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=1.0/0.750/timesBaseline | 7.42 | 7.18 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=1.0/0.750/volumeM3 | 163333972 | 157935107 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/everythingButShellT | 22766.0 | 22664.8 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.264/diaM | 271 | 316 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.264/lenM | 1083 | 631 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.264/timesBaseline | 1.89 | 1.87 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.264/volumeM3 | 41590987 | 41184608 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.350/diaM | 284 | 331 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.350/lenM | 1136 | 662 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.350/timesBaseline | 2.18 | 2.16 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.350/volumeM3 | 48039748 | 47489135 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.508/diaM | 317 | 369 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.508/lenM | 1270 | 738 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.508/timesBaseline | 3.04 | 3.0 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.508/volumeM3 | 66980471 | 65912064 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.600/diaM | 346 | 402 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.600/lenM | 1383 | 803 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.600/timesBaseline | 3.94 | 3.86 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.600/volumeM3 | 86655440 | 84916398 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.750/diaM | 427 | 494 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.750/lenM | 1709 | 988 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.750/timesBaseline | 7.42 | 7.18 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.750/volumeM3 | 163333972 | 157935107 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.900/diaM | 756 | 855 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.900/lenM | 3025 | 1710 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.900/timesBaseline | 41.18 | 37.28 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.900/volumeM3 | 905962550 | 820222816 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/lines/1/tonnes | 1675.23 | 1420.62 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/lines/15/tonnes | 8047.67 | 8030.8 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/lines/3/tonnes | 923.54 | 1093.79 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/overBy | 4.83 | 4.82 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/shellBudgetLeftT | -6385.0 | -6300.7 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/totalT | 48286.0 | 48184.8 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/baseExShellExSundriesT | 2863.36 | 2899.24 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.74/0.264/diaM | 242 | 283 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.74/0.264/lenM | 968 | 566 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.74/0.264/volumeM3 | 29688613 | 29770046 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.74/0.508/diaM | 317 | 370 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.74/0.508/lenM | 1267 | 741 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.74/0.508/volumeM3 | 66569935 | 66679573 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.85/0.264/diaM | 225 | 264 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.85/0.264/lenM | 901 | 527 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.85/0.264/volumeM3 | 23954169 | 24024804 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.85/0.508/diaM | 275 | 321 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.85/0.508/lenM | 1098 | 642 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.85/0.508/timesBaseline | 1.97 | 1.98 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.85/0.508/volumeM3 | 43357573 | 43457314 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.85/0.750/diaM | 469 | 548 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.85/0.750/lenM | 1877 | 1097 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.85/0.750/timesBaseline | 9.84 | 9.82 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.85/0.750/volumeM3 | 216429913 | 216116487 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=1.0/0.264/diaM | 208 | 244 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=1.0/0.264/lenM | 834 | 488 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=1.0/0.264/volumeM3 | 18957753 | 19017325 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=1.0/0.508/diaM | 241 | 282 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=1.0/0.508/lenM | 965 | 564 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=1.0/0.508/timesBaseline | 1.33 | 1.34 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=1.0/0.508/volumeM3 | 29369201 | 29450083 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=1.0/0.750/diaM | 313 | 366 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=1.0/0.750/lenM | 1253 | 733 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=1.0/0.750/volumeM3 | 64351939 | 64461694 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/everythingButShellT | 4267.3 | 4306.8 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.264/diaM | 208 | 244 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.264/lenM | 834 | 488 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.264/volumeM3 | 18957753 | 19017325 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.350/diaM | 218 | 255 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.350/lenM | 872 | 510 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.350/timesBaseline | 0.98 | 0.99 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.350/volumeM3 | 21665860 | 21731627 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.508/diaM | 241 | 282 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.508/lenM | 965 | 564 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.508/timesBaseline | 1.33 | 1.34 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.508/volumeM3 | 29369201 | 29450083 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.600/diaM | 261 | 305 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.600/lenM | 1042 | 610 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.600/timesBaseline | 1.68 | 1.69 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.600/volumeM3 | 37028737 | 37121244 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.750/diaM | 313 | 366 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.750/lenM | 1253 | 733 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.750/volumeM3 | 64351939 | 64461694 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.900/diaM | 487 | 569 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.900/lenM | 1948 | 1138 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.900/timesBaseline | 11.0 | 10.98 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.900/volumeM3 | 242030733 | 241575171 | capsule surface and refreshed capsule-era inputs | better in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/lines/1/tonnes | 97.76 | 82.9 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/lines/15/tonnes | 1403.94 | 1407.52 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/lines/3/tonnes | 275.21 | 325.95 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/overBy | 1.54 | 1.55 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/requiredShellKgPerM3 | 0.2831 | 0.2814 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/shellBudgetLeftT | 6227.5 | 6191.7 | capsule surface and refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/totalT | 15443.3 | 15482.8 | capsule surface and refreshed capsule-era inputs | worse in this conditional equipment budget |
| research/analysis/water-availability.json#/geometry/P100/conservatismVsHullDisc | 3.53 | 10.52 | refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/water-availability.json#/geometry/P100/hullLenM | 190 | 110 | refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/water-availability.json#/geometry/P100/hullStationDiscHa | 2.84 | 0.95 | refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/water-availability.json#/geometry/P1000/conservatismVsHullDisc | 7.8 | 22.48 | refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/water-availability.json#/geometry/P1000/hullLenM | 404 | 238 | refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/water-availability.json#/geometry/P1000/hullStationDiscHa | 12.82 | 4.45 | refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/water-availability.json#/geometry/P10000/conservatismVsHullDisc | 16.59 | 48.57 | refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/water-availability.json#/geometry/P10000/hullLenM | 876 | 512 | refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/water-availability.json#/geometry/P10000/hullStationDiscHa | 60.27 | 20.59 | refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/descent.json#/classes/P100/cycleContext/eCycleMWh | 1.253 | 1.391 | refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/descent.json#/classes/P100/cycleContext/honestLetdownPctOfCycle | 33.8 | 31.5 | refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/descent.json#/classes/P1000/cycleContext/eCycleMWh | 7.399 | 8.454 | refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/descent.json#/classes/P1000/cycleContext/honestLetdownPctOfCycle | 49 | 45.6 | refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/descent.json#/classes/P10000/cycleContext/eCycleMWh | 45.869 | 54.325 | refreshed capsule-era inputs | context or intermediate; no direct float verdict |
| research/analysis/descent.json#/classes/P10000/cycleContext/honestLetdownPctOfCycle | 48.7 | 44.4 | refreshed capsule-era inputs | context or intermediate; no direct float verdict |

## Correction, 2026-10-03 — separate causes and omitted strings

This dated correction adds to the earlier table; it does not replace that account. The float results and energy model are unchanged. Current float results are in [the ledger](../FLOAT-LEDGER.md).

| Surface computation for P100 | Area m² | Cause |
|---|---:|---|
| Old spheroid formula, pre-August 190 × 47 m | 22,592 | cached pre-August geometry |
| Same formula, capsule-era 110 × 55 m | 16,243 | changed dimensions, formula held fixed |
| Capsule formula, same capsule-era dimensions | 19,007 | changed surface formula, inputs held fixed |

Verified with `python3 tools/correct_analysis_audit.py --check`; the script evaluates the old formula and the current capsule function, then runs the mass-budget generator on both historical input snapshots. A cache refresh exposes changed dimensions and cycle inputs together; changing the area formula is a separate effect. Battery and cycle rows move with refreshed cycle inputs. Barrier mass and area-normalised allowance move with the surface area. Totals, sundries and closing-hull rows can inherit both. The table below identifies the actual stages affecting each originally reported mass-budget row.

| Printed at | Refreshed inputs (old formula) | Surface formula (same inputs) |
|---|---|---|
| mass-budget.json#/classes/P100/batterySensitivity/credible/16 cycles/batteryMWh | 20.05 → 22.26 | 22.26 → 22.26 |
| mass-budget.json#/classes/P100/batterySensitivity/credible/16 cycles/batteryT | 66.8 → 74.2 | 74.2 → 74.2 |
| mass-budget.json#/classes/P100/batterySensitivity/credible/16 cycles/leftForShellT | -155.3 → -159.9 | -159.9 → -161.1 |
| mass-budget.json#/classes/P100/batterySensitivity/credible/16 cycles/totalT | 278.6 → 283.9 | 283.9 → 285.3 |
| mass-budget.json#/classes/P100/batterySensitivity/credible/2 cycles/batteryMWh | 2.51 → 2.78 | 2.78 → 2.78 |
| mass-budget.json#/classes/P100/batterySensitivity/credible/2 cycles/batteryT | 8.4 → 9.3 | 9.3 → 9.3 |
| mass-budget.json#/classes/P100/batterySensitivity/credible/2 cycles/leftForShellT | -96.8 → -95.0 | -95.0 → -96.2 |
| mass-budget.json#/classes/P100/batterySensitivity/credible/2 cycles/totalT | 211.3 → 209.2 | 209.2 → 210.6 |
| mass-budget.json#/classes/P100/batterySensitivity/credible/4 cycles/batteryMWh | 5.01 → 5.56 | 5.56 → 5.56 |
| mass-budget.json#/classes/P100/batterySensitivity/credible/4 cycles/batteryT | 16.7 → 18.5 | 18.5 → 18.5 |
| mass-budget.json#/classes/P100/batterySensitivity/credible/4 cycles/leftForShellT | -105.2 → -104.3 | -104.3 → -105.5 |
| mass-budget.json#/classes/P100/batterySensitivity/credible/4 cycles/totalT | 220.9 → 219.9 | 219.9 → 221.3 |
| mass-budget.json#/classes/P100/batterySensitivity/credible/8 cycles/batteryMWh | 10.02 → 11.13 | 11.13 → 11.13 |
| mass-budget.json#/classes/P100/batterySensitivity/credible/8 cycles/batteryT | 33.4 → 37.1 | 37.1 → 37.1 |
| mass-budget.json#/classes/P100/batterySensitivity/credible/8 cycles/leftForShellT | -121.9 → -122.8 | -122.8 → -124.0 |
| mass-budget.json#/classes/P100/batterySensitivity/credible/8 cycles/totalT | 240.2 → 241.2 | 241.2 → 242.6 |
| mass-budget.json#/classes/P100/batterySensitivity/demonstrated/16 cycles/batteryMWh | 20.05 → 22.26 | 22.26 → 22.26 |
| mass-budget.json#/classes/P100/batterySensitivity/demonstrated/16 cycles/batteryT | 134.6 → 149.4 | 149.4 → 149.4 |
| mass-budget.json#/classes/P100/batterySensitivity/demonstrated/16 cycles/leftForShellT | -597.7 → -590.6 | -590.6 → -600.2 |
| mass-budget.json#/classes/P100/batterySensitivity/demonstrated/16 cycles/totalT | 817.3 → 808.8 | 808.8 → 820.2 |
| mass-budget.json#/classes/P100/batterySensitivity/demonstrated/2 cycles/batteryMWh | 2.51 → 2.78 | 2.78 → 2.78 |
| mass-budget.json#/classes/P100/batterySensitivity/demonstrated/2 cycles/batteryT | 16.8 → 18.7 | 18.7 → 18.7 |
| mass-budget.json#/classes/P100/batterySensitivity/demonstrated/2 cycles/leftForShellT | -480.0 → -459.9 | -459.9 → -469.5 |
| mass-budget.json#/classes/P100/batterySensitivity/demonstrated/2 cycles/totalT | 676.0 → 651.9 | 651.9 → 663.4 |
| mass-budget.json#/classes/P100/batterySensitivity/demonstrated/4 cycles/batteryMWh | 5.01 → 5.56 | 5.56 → 5.56 |
| mass-budget.json#/classes/P100/batterySensitivity/demonstrated/4 cycles/batteryT | 33.6 → 37.3 | 37.3 → 37.3 |
| mass-budget.json#/classes/P100/batterySensitivity/demonstrated/4 cycles/leftForShellT | -496.8 → -478.6 | -478.6 → -488.1 |
| mass-budget.json#/classes/P100/batterySensitivity/demonstrated/4 cycles/totalT | 696.2 → 674.3 | 674.3 → 685.8 |
| mass-budget.json#/classes/P100/batterySensitivity/demonstrated/8 cycles/batteryMWh | 10.02 → 11.13 | 11.13 → 11.13 |
| mass-budget.json#/classes/P100/batterySensitivity/demonstrated/8 cycles/batteryT | 67.3 → 74.7 | 74.7 → 74.7 |
| mass-budget.json#/classes/P100/batterySensitivity/demonstrated/8 cycles/leftForShellT | -530.5 → -516.0 | -516.0 → -525.5 |
| mass-budget.json#/classes/P100/batterySensitivity/demonstrated/8 cycles/totalT | 736.5 → 719.2 | 719.2 → 730.6 |
| mass-budget.json#/classes/P100/batterySensitivity/floor/16 cycles/batteryMWh | 20.05 → 22.26 | 22.26 → 22.26 |
| mass-budget.json#/classes/P100/batterySensitivity/floor/16 cycles/batteryT | 40.1 → 44.5 | 44.5 → 44.5 |
| mass-budget.json#/classes/P100/batterySensitivity/floor/16 cycles/leftForShellT | 6.0 → 1.8 | 1.8 → 1.7 |
| mass-budget.json#/classes/P100/batterySensitivity/floor/16 cycles/requiredShellKgPerM3 | 0.0272 → 0.0084 | 0.0084 → 0.0078 |
| mass-budget.json#/classes/P100/batterySensitivity/floor/16 cycles/totalT | 93.4 → 98.0 | 98.0 → 98.1 |
| mass-budget.json#/classes/P100/batterySensitivity/floor/2 cycles/batteryMWh | 2.51 → 2.78 | 2.78 → 2.78 |
| mass-budget.json#/classes/P100/batterySensitivity/floor/2 cycles/batteryT | 5.0 → 5.6 | 5.6 → 5.6 |
| mass-budget.json#/classes/P100/batterySensitivity/floor/2 cycles/leftForShellT | 41.1 → 40.8 | 40.8 → 40.7 |
| mass-budget.json#/classes/P100/batterySensitivity/floor/2 cycles/requiredShellKgPerM3 | 0.1866 → 0.1854 | 0.1854 → 0.1848 |
| mass-budget.json#/classes/P100/batterySensitivity/floor/2 cycles/totalT | 54.8 → 55.1 | 55.1 → 55.3 |
| mass-budget.json#/classes/P100/batterySensitivity/floor/4 cycles/batteryMWh | 5.01 → 5.56 | 5.56 → 5.56 |
| mass-budget.json#/classes/P100/batterySensitivity/floor/4 cycles/batteryT | 10.0 → 11.1 | 11.1 → 11.1 |
| mass-budget.json#/classes/P100/batterySensitivity/floor/4 cycles/leftForShellT | 36.0 → 35.2 | 35.2 → 35.1 |
| mass-budget.json#/classes/P100/batterySensitivity/floor/4 cycles/requiredShellKgPerM3 | 0.1638 → 0.1601 | 0.1601 → 0.1596 |
| mass-budget.json#/classes/P100/batterySensitivity/floor/4 cycles/totalT | 60.4 → 61.3 | 61.3 → 61.4 |
| mass-budget.json#/classes/P100/batterySensitivity/floor/8 cycles/batteryMWh | 10.02 → 11.13 | 11.13 → 11.13 |
| mass-budget.json#/classes/P100/batterySensitivity/floor/8 cycles/batteryT | 20.0 → 22.3 | 22.3 → 22.3 |
| mass-budget.json#/classes/P100/batterySensitivity/floor/8 cycles/leftForShellT | 26.0 → 24.1 | 24.1 → 24.0 |
| mass-budget.json#/classes/P100/batterySensitivity/floor/8 cycles/requiredShellKgPerM3 | 0.1183 → 0.1095 | 0.1095 → 0.109 |
| mass-budget.json#/classes/P100/batterySensitivity/floor/8 cycles/totalT | 71.4 → 73.5 | 73.5 → 73.6 |
| mass-budget.json#/classes/P100/cases/credible/baseExShellExSundriesT | 242.09 → 239.34 | 239.34 → 240.53 |
| mass-budget.json#/classes/P100/cases/credible/everythingButShellT | 303.1 → 300.0 | 300.0 → 301.4 |
| mass-budget.json#/classes/P100/cases/credible/lines/1/driver | 22,592 m2 hull surface → 16,243 m2 hull surface | 16,243 m2 hull surface → 19,007 m2 hull surface |
| mass-budget.json#/classes/P100/cases/credible/lines/1/tonnes | 9.8 → 7.05 | 7.05 → 8.24 |
| mass-budget.json#/classes/P100/cases/credible/lines/15/tonnes | 61.06 → 60.65 | 60.65 → 60.83 |
| mass-budget.json#/classes/P100/cases/credible/overBy | 4.68 → 4.65 | 4.65 → 4.66 |
| mass-budget.json#/classes/P100/cases/credible/totalT | 468.1 → 465.0 | 465.0 → 466.4 |
| mass-budget.json#/classes/P100/cases/demonstrated/baseExShellExSundriesT | 680.74 → 658.84 | 658.84 → 668.37 |
| mass-budget.json#/classes/P100/cases/demonstrated/everythingButShellT | 867.9 → 841.6 | 841.6 → 853.1 |
| mass-budget.json#/classes/P100/cases/demonstrated/lines/1/driver | 22,592 m2 hull surface → 16,243 m2 hull surface | 16,243 m2 hull surface → 19,007 m2 hull surface |
| mass-budget.json#/classes/P100/cases/demonstrated/lines/1/tonnes | 77.94 → 56.04 | 56.04 → 65.57 |
| mass-budget.json#/classes/P100/cases/demonstrated/lines/15/tonnes | 187.19 → 182.81 | 182.81 → 184.71 |
| mass-budget.json#/classes/P100/cases/demonstrated/overBy | 11.23 → 10.97 | 10.97 → 11.08 |
| mass-budget.json#/classes/P100/cases/demonstrated/totalT | 1123.1 → 1096.8 | 1096.8 → 1108.3 |
| mass-budget.json#/classes/P100/cases/floor/baseExShellExSundriesT | 84.84 → 84.56 | 84.56 → 84.68 |
| mass-budget.json#/classes/P100/cases/floor/everythingButShellT | 104.5 → 104.2 | 104.2 → 104.3 |
| mass-budget.json#/classes/P100/cases/floor/lines/1/driver | 22,592 m2 hull surface → 16,243 m2 hull surface | 16,243 m2 hull surface → 19,007 m2 hull surface |
| mass-budget.json#/classes/P100/cases/floor/lines/1/tonnes | 0.98 → 0.7 | 0.7 → 0.82 |
| mass-budget.json#/classes/P100/cases/floor/lines/15/tonnes | 19.66 → 19.63 | 19.63 → 19.64 |
| mass-budget.json#/classes/P100/cases/floor/totalT | 216.3 → 216.0 | 216.0 → 216.1 |
| mass-budget.json#/classes/P100/descentWithoutNitrogen/cycleMWhAsBuilt | 1.253 → 1.391 | 1.391 → 1.391 |
| mass-budget.json#/classes/P100/descentWithoutNitrogen/cycleMWhWithoutCryo | 0.595 → 0.733 | 0.733 → 0.733 |
| mass-budget.json#/classes/P100/descentWithoutNitrogen/cycleSavingPct | 52.5 → 47.3 | 47.3 → 47.3 |
| mass-budget.json#/classes/P100/hullAreaM2 | 22592 → 16243 | 16243 → 19007 |
| mass-budget.json#/classes/P100/requiredKgPerM2 | 4.426 → 6.156 | 6.156 → 5.261 |
| mass-budget.json#/classes/P100/rightSized/credible/baseExShellExSundriesT | 187.95 → 186.58 | 186.58 → 187.77 |
| mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.74/0.264/diaM | 71 → 83 | 83 → 83 |
| mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.74/0.264/lenM | 287 → 165 | 165 → 166 |
| mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.74/0.264/timesBaseline | 3.44 → 3.38 | 3.38 → 3.42 |
| mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.74/0.264/volumeM3 | 757318 → 743889 | 743889 → 751301 |
| mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.74/0.508/diaM | 95 → 110 | 110 → 111 |
| mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.74/0.508/lenM | 385 → 220 | 220 → 221 |
| mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.74/0.508/timesBaseline | 8.29 → 8.01 | 8.01 → 8.14 |
| mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.74/0.508/volumeM3 | 1823933 → 1761168 | 1761168 → 1791764 |
| mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.85/0.264/diaM | 66 → 77 | 77 → 77 |
| mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.85/0.264/lenM | 266 → 153 | 153 → 154 |
| mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.85/0.264/timesBaseline | 2.74 → 2.7 | 2.7 → 2.72 |
| mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.85/0.264/volumeM3 | 602996 → 594171 | 594171 → 599285 |
| mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.85/0.508/diaM | 81 → 94 | 94 → 95 |
| mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.85/0.508/lenM | 329 → 189 | 189 → 189 |
| mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.85/0.508/timesBaseline | 5.17 → 5.05 | 5.05 → 5.11 |
| mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.85/0.508/volumeM3 | 1138161 → 1110359 | 1110359 → 1124703 |
| mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.85/0.750/diaM | 151 → 172 | 172 → 174 |
| mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.85/0.750/lenM | 611 → 344 | 344 → 348 |
| mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.85/0.750/timesBaseline | 33.25 → 30.5 | 30.5 → 31.71 |
| mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=0.85/0.750/volumeM3 | 7315760 → 6709131 | 6709131 → 6976947 |
| mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=1.0/0.264/diaM | 61 → 71 | 71 → 71 |
| mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=1.0/0.264/lenM | 245 → 141 | 141 → 142 |
| mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=1.0/0.264/timesBaseline | 2.14 → 2.12 | 2.12 → 2.13 |
| mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=1.0/0.264/volumeM3 | 471338 → 465806 | 465806 → 469225 |
| mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=1.0/0.508/diaM | 71 → 82 | 82 → 83 |
| mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=1.0/0.508/lenM | 286 → 164 | 164 → 165 |
| mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=1.0/0.508/timesBaseline | 3.4 → 3.34 | 3.34 → 3.38 |
| mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=1.0/0.508/volumeM3 | 748634 → 735485 | 735485 → 742759 |
| mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=1.0/0.750/diaM | 94 → 109 | 109 → 109 |
| mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=1.0/0.750/lenM | 380 → 217 | 217 → 219 |
| mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=1.0/0.750/timesBaseline | 7.98 → 7.72 | 7.72 → 7.85 |
| mass-budget.json#/classes/P100/rightSized/credible/cellular/phi=1.0/0.750/volumeM3 | 1756369 → 1697509 | 1697509 → 1726314 |
| mass-budget.json#/classes/P100/rightSized/credible/everythingButShellT | 240.9 → 239.3 | 239.3 → 240.7 |
| mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.264/diaM | 61 → 71 | 71 → 71 |
| mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.264/lenM | 245 → 141 | 141 → 142 |
| mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.264/timesBaseline | 2.14 → 2.12 | 2.12 → 2.13 |
| mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.264/volumeM3 | 471338 → 465806 | 465806 → 469225 |
| mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.350/diaM | 63 → 74 | 74 → 74 |
| mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.350/lenM | 257 → 148 | 148 → 148 |
| mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.350/timesBaseline | 2.47 → 2.43 | 2.43 → 2.45 |
| mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.350/volumeM3 | 542365 → 535133 | 535133 → 539434 |
| mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.508/diaM | 71 → 82 | 82 → 83 |
| mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.508/lenM | 286 → 164 | 164 → 165 |
| mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.508/timesBaseline | 3.4 → 3.34 | 3.34 → 3.38 |
| mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.508/volumeM3 | 748634 → 735485 | 735485 → 742759 |
| mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.600/diaM | 77 → 89 | 89 → 90 |
| mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.600/lenM | 310 → 178 | 178 → 179 |
| mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.600/timesBaseline | 4.36 → 4.27 | 4.27 → 4.32 |
| mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.600/volumeM3 | 959615 → 939054 | 939054 → 949938 |
| mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.750/diaM | 94 → 109 | 109 → 109 |
| mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.750/lenM | 380 → 217 | 217 → 219 |
| mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.750/timesBaseline | 7.98 → 7.72 | 7.72 → 7.85 |
| mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.750/volumeM3 | 1756369 → 1697509 | 1697509 → 1726314 |
| mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.900/diaM | 158 → 180 | 180 → 182 |
| mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.900/lenM | 641 → 359 | 359 → 365 |
| mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.900/timesBaseline | 38.33 → 34.89 | 34.89 → 36.4 |
| mass-budget.json#/classes/P100/rightSized/credible/hullThatCloses/0.900/volumeM3 | 8433177 → 7675621 | 7675621 → 8007682 |
| mass-budget.json#/classes/P100/rightSized/credible/lines/1/driver | 22,592 m2 hull surface → 16,243 m2 hull surface | 16,243 m2 hull surface → 19,007 m2 hull surface |
| mass-budget.json#/classes/P100/rightSized/credible/lines/1/tonnes | 9.8 → 7.05 | 7.05 → 8.24 |
| mass-budget.json#/classes/P100/rightSized/credible/lines/15/tonnes | 52.94 → 52.74 | 52.74 → 52.92 |
| mass-budget.json#/classes/P100/rightSized/credible/lines/3/driver | 3.76 MWh → 4.17 MWh | 4.17 MWh → 4.17 MWh |
| mass-budget.json#/classes/P100/rightSized/credible/lines/3/tonnes | 12.53 → 13.91 | 13.91 → 13.91 |
| mass-budget.json#/classes/P100/rightSized/credible/shellBudgetLeftT | -101.0 → -99.6 | -99.6 → -100.8 |
| mass-budget.json#/classes/P100/rightSized/credible/totalT | 405.9 → 404.3 | 404.3 → 405.7 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/baseExShellExSundriesT | 571.74 → 552.62 | 552.62 → 562.15 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.74/0.264/diaM | 110 → 122 | 122 → 125 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.74/0.264/lenM | 443 → 243 | 243 → 249 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.74/0.264/timesBaseline | 12.69 → 10.84 | 10.84 → 11.62 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.74/0.264/volumeM3 | 2791792 → 2384578 | 2384578 → 2556442 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.74/0.508/diaM | 167 → 177 | 177 → 185 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.74/0.508/lenM | 675 → 355 | 355 → 370 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.74/0.508/timesBaseline | 44.83 → 33.55 | 33.55 → 38.06 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.74/0.508/volumeM3 | 9862367 → 7380265 | 7380265 → 8373478 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.85/0.264/diaM | 99 → 111 | 111 → 113 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.85/0.264/lenM | 401 → 222 | 222 → 227 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.85/0.264/timesBaseline | 9.43 → 8.25 | 8.25 → 8.76 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.85/0.264/volumeM3 | 2075358 → 1815150 | 1815150 → 1926413 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.85/0.508/diaM | 132 → 144 | 144 → 149 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.85/0.508/lenM | 534 → 288 | 288 → 297 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.85/0.508/timesBaseline | 22.19 → 17.99 | 17.99 → 19.72 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.85/0.508/volumeM3 | 4882494 → 3957100 | 3957100 → 4338405 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.85/0.750/diaM | 380 → 362 | 362 → 397 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.85/0.750/lenM | 1536 → 724 | 724 → 794 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.85/0.750/timesBaseline | 528.32 → 285.48 | 285.48 → 375.61 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=0.85/0.750/volumeM3 | 116230555 → 62804808 | 62804808 → 82633219 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=1.0/0.264/diaM | 90 → 101 | 101 → 103 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=1.0/0.264/lenM | 362 → 202 | 202 → 205 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=1.0/0.264/timesBaseline | 6.92 → 6.19 | 6.19 → 6.51 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=1.0/0.264/volumeM3 | 1522629 → 1361024 | 1361024 → 1431105 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=1.0/0.508/diaM | 109 → 121 | 121 → 124 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=1.0/0.508/lenM | 441 → 242 | 242 → 248 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=1.0/0.508/timesBaseline | 12.5 → 10.69 | 10.69 → 11.45 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=1.0/0.508/volumeM3 | 2749504 → 2351488 | 2351488 → 2519581 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=1.0/0.750/diaM | 164 → 174 | 174 → 182 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=1.0/0.750/lenM | 662 → 349 | 349 → 363 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=1.0/0.750/timesBaseline | 42.27 → 31.86 | 31.86 → 36.04 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/cellular/phi=1.0/0.750/volumeM3 | 9299500 → 7009277 | 7009277 → 7927907 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/everythingButShellT | 737.1 → 714.2 | 714.2 → 725.6 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.264/diaM | 90 → 101 | 101 → 103 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.264/lenM | 362 → 202 | 202 → 205 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.264/timesBaseline | 6.92 → 6.19 | 6.19 → 6.51 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.264/volumeM3 | 1522629 → 1361024 | 1361024 → 1431105 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.350/diaM | 95 → 107 | 107 → 109 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.350/lenM | 384 → 213 | 213 → 217 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.350/timesBaseline | 8.25 → 7.28 | 7.28 → 7.7 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.350/volumeM3 | 1814147 → 1602347 | 1602347 → 1693460 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.508/diaM | 109 → 121 | 121 → 124 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.508/lenM | 441 → 242 | 242 → 248 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.508/timesBaseline | 12.5 → 10.69 | 10.69 → 11.45 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.508/volumeM3 | 2749504 → 2351488 | 2351488 → 2519581 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.600/diaM | 122 → 134 | 134 → 138 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.600/lenM | 493 → 268 | 268 → 276 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.600/timesBaseline | 17.47 → 14.5 | 14.5 → 15.74 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.600/volumeM3 | 3844427 → 3190484 | 3190484 → 3462698 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.750/diaM | 164 → 174 | 174 → 182 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.750/lenM | 662 → 349 | 349 → 363 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.750/timesBaseline | 42.27 → 31.86 | 31.86 → 36.04 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.750/volumeM3 | 9299500 → 7009277 | 7009277 → 7927907 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.900/diaM | 417 → 393 | 393 → 433 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.900/lenM | 1684 → 786 | 786 → 866 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.900/timesBaseline | 696.33 → 364.51 | 364.51 → 487.13 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/hullThatCloses/0.900/volumeM3 | 153193461 → 80192220 | 80192220 → 107169282 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/lines/1/driver | 22,592 m2 hull surface → 16,243 m2 hull surface | 16,243 m2 hull surface → 19,007 m2 hull surface |
| mass-budget.json#/classes/P100/rightSized/demonstrated/lines/1/tonnes | 77.94 → 56.04 | 56.04 → 65.57 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/lines/15/tonnes | 165.39 → 161.56 | 161.56 → 163.47 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/lines/3/driver | 3.76 MWh → 4.17 MWh | 4.17 MWh → 4.17 MWh |
| mass-budget.json#/classes/P100/rightSized/demonstrated/lines/3/tonnes | 25.23 → 28.01 | 28.01 → 28.01 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/overBy | 9.92 → 9.69 | 9.69 → 9.81 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/shellBudgetLeftT | -488.4 → -469.3 | -469.3 → -478.8 |
| mass-budget.json#/classes/P100/rightSized/demonstrated/totalT | 992.3 → 969.4 | 969.4 → 980.8 |
| mass-budget.json#/classes/P100/rightSized/floor/baseExShellExSundriesT | 52.36 → 52.91 | 52.91 → 53.03 |
| mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.74/0.264/diaM | 55 → 65 | 65 → 65 |
| mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.74/0.264/lenM | 223 → 130 | 130 → 130 |
| mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.74/0.264/volumeM3 | 357865 → 358982 | 358982 → 359402 |
| mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.74/0.508/diaM | 73 → 85 | 85 → 85 |
| mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.74/0.508/lenM | 294 → 170 | 170 → 170 |
| mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.74/0.508/timesBaseline | 3.69 → 3.69 | 3.69 → 3.7 |
| mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.74/0.508/volumeM3 | 811637 → 812553 | 812553 → 814181 |
| mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.85/0.264/diaM | 51 → 60 | 60 → 60 |
| mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.85/0.264/lenM | 208 → 120 | 120 → 121 |
| mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.85/0.264/timesBaseline | 1.31 → 1.31 | 1.31 → 1.32 |
| mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.85/0.264/volumeM3 | 288126 → 289133 | 289133 → 289426 |
| mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.85/0.508/diaM | 63 → 74 | 74 → 74 |
| mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.85/0.508/lenM | 254 → 147 | 147 → 147 |
| mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.85/0.508/timesBaseline | 2.39 → 2.39 | 2.39 → 2.4 |
| mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.85/0.508/volumeM3 | 525039 → 526257 | 526257 → 527049 |
| mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.85/0.750/diaM | 109 → 127 | 127 → 127 |
| mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.85/0.750/lenM | 440 → 254 | 254 → 255 |
| mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=0.85/0.750/volumeM3 | 2725986 → 2713551 | 2713551 → 2725487 |
| mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=1.0/0.264/diaM | 48 → 56 | 56 → 56 |
| mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=1.0/0.264/lenM | 192 → 111 | 111 → 111 |
| mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=1.0/0.264/timesBaseline | 1.03 → 1.04 | 1.04 → 1.04 |
| mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=1.0/0.264/volumeM3 | 227571 → 228446 | 228446 → 228644 |
| mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=1.0/0.508/diaM | 55 → 65 | 65 → 65 |
| mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=1.0/0.508/lenM | 223 → 129 | 129 → 129 |
| mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=1.0/0.508/timesBaseline | 1.61 → 1.61 | 1.61 → 1.62 |
| mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=1.0/0.508/volumeM3 | 353975 → 355087 | 355087 → 355499 |
| mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=1.0/0.750/diaM | 72 → 84 | 84 → 84 |
| mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=1.0/0.750/lenM | 290 → 168 | 168 → 168 |
| mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=1.0/0.750/timesBaseline | 3.56 → 3.57 | 3.57 → 3.58 |
| mass-budget.json#/classes/P100/rightSized/floor/cellular/phi=1.0/0.750/volumeM3 | 784115 → 785084 | 785084 → 786622 |
| mass-budget.json#/classes/P100/rightSized/floor/everythingButShellT | 68.8 → 69.4 | 69.4 → 69.5 |
| mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.264/diaM | 48 → 56 | 56 → 56 |
| mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.264/lenM | 192 → 111 | 111 → 111 |
| mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.264/timesBaseline | 1.03 → 1.04 | 1.04 → 1.04 |
| mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.264/volumeM3 | 227571 → 228446 | 228446 → 228644 |
| mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.350/diaM | 50 → 58 | 58 → 58 |
| mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.350/lenM | 201 → 116 | 116 → 117 |
| mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.350/timesBaseline | 1.18 → 1.19 | 1.19 → 1.19 |
| mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.350/volumeM3 | 260368 → 261319 | 261319 → 261566 |
| mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.508/diaM | 55 → 65 | 65 → 65 |
| mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.508/lenM | 223 → 129 | 129 → 129 |
| mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.508/timesBaseline | 1.61 → 1.61 | 1.61 → 1.62 |
| mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.508/volumeM3 | 353975 → 355087 | 355087 → 355499 |
| mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.600/diaM | 60 → 70 | 70 → 70 |
| mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.600/lenM | 241 → 139 | 139 → 140 |
| mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.600/timesBaseline | 2.03 → 2.04 | 2.04 → 2.04 |
| mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.600/volumeM3 | 447479 → 448677 | 448677 → 449285 |
| mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.750/diaM | 72 → 84 | 84 → 84 |
| mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.750/lenM | 290 → 168 | 168 → 168 |
| mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.750/timesBaseline | 3.56 → 3.57 | 3.57 → 3.58 |
| mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.750/volumeM3 | 784115 → 785084 | 785084 → 786622 |
| mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.900/diaM | 113 → 132 | 132 → 132 |
| mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.900/lenM | 457 → 264 | 264 → 265 |
| mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.900/timesBaseline | 13.92 → 13.85 | 13.85 → 13.91 |
| mass-budget.json#/classes/P100/rightSized/floor/hullThatCloses/0.900/volumeM3 | 3062477 → 3046041 | 3046041 → 3060477 |
| mass-budget.json#/classes/P100/rightSized/floor/lines/1/driver | 22,592 m2 hull surface → 16,243 m2 hull surface | 16,243 m2 hull surface → 19,007 m2 hull surface |
| mass-budget.json#/classes/P100/rightSized/floor/lines/1/tonnes | 0.98 → 0.7 | 0.7 → 0.82 |
| mass-budget.json#/classes/P100/rightSized/floor/lines/15/tonnes | 16.41 → 16.47 | 16.47 → 16.48 |
| mass-budget.json#/classes/P100/rightSized/floor/lines/3/driver | 3.76 MWh → 4.17 MWh | 4.17 MWh → 4.17 MWh |
| mass-budget.json#/classes/P100/rightSized/floor/lines/3/tonnes | 7.52 → 8.35 | 8.35 → 8.35 |
| mass-budget.json#/classes/P100/rightSized/floor/requiredShellKgPerM3 | 0.1752 → 0.1727 | 0.1727 → 0.1722 |
| mass-budget.json#/classes/P100/rightSized/floor/shellBudgetLeftT | 38.5 → 38.0 | 38.0 → 37.9 |
| mass-budget.json#/classes/P100/rightSized/floor/totalT | 180.5 → 181.1 | 181.1 → 181.3 |
| mass-budget.json#/classes/P1000/batterySensitivity/credible/16 cycles/batteryMWh | 118.38 → 135.26 | 135.26 → 135.26 |
| mass-budget.json#/classes/P1000/batterySensitivity/credible/16 cycles/batteryT | 394.6 → 450.9 | 450.9 → 450.9 |
| mass-budget.json#/classes/P1000/batterySensitivity/credible/16 cycles/leftForShellT | -535.4 → -565.2 | -565.2 → -577.3 |
| mass-budget.json#/classes/P1000/batterySensitivity/credible/16 cycles/totalT | 1615.7 → 1650.0 | 1650.0 → 1663.9 |
| mass-budget.json#/classes/P1000/batterySensitivity/credible/2 cycles/batteryMWh | 14.8 → 16.91 | 16.91 → 16.91 |
| mass-budget.json#/classes/P1000/batterySensitivity/credible/2 cycles/batteryT | 49.3 → 56.4 | 56.4 → 56.4 |
| mass-budget.json#/classes/P1000/batterySensitivity/credible/2 cycles/leftForShellT | -190.1 → -170.7 | -170.7 → -182.8 |
| mass-budget.json#/classes/P1000/batterySensitivity/credible/2 cycles/totalT | 1218.6 → 1196.3 | 1196.3 → 1210.2 |
| mass-budget.json#/classes/P1000/batterySensitivity/credible/4 cycles/batteryMWh | 29.6 → 33.82 | 33.82 → 33.82 |
| mass-budget.json#/classes/P1000/batterySensitivity/credible/4 cycles/batteryT | 98.7 → 112.7 | 112.7 → 112.7 |
| mass-budget.json#/classes/P1000/batterySensitivity/credible/4 cycles/leftForShellT | -239.4 → -227.0 | -227.0 → -239.1 |
| mass-budget.json#/classes/P1000/batterySensitivity/credible/4 cycles/totalT | 1275.3 → 1261.1 | 1261.1 → 1275.0 |
| mass-budget.json#/classes/P1000/batterySensitivity/credible/8 cycles/batteryMWh | 59.19 → 67.63 | 67.63 → 67.63 |
| mass-budget.json#/classes/P1000/batterySensitivity/credible/8 cycles/batteryT | 197.3 → 225.4 | 225.4 → 225.4 |
| mass-budget.json#/classes/P1000/batterySensitivity/credible/8 cycles/leftForShellT | -338.1 → -339.8 | -339.8 → -351.8 |
| mass-budget.json#/classes/P1000/batterySensitivity/credible/8 cycles/totalT | 1388.8 → 1390.7 | 1390.7 → 1404.6 |
| mass-budget.json#/classes/P1000/batterySensitivity/demonstrated/16 cycles/batteryMWh | 118.38 → 135.26 | 135.26 → 135.26 |
| mass-budget.json#/classes/P1000/batterySensitivity/demonstrated/16 cycles/batteryT | 794.5 → 907.8 | 907.8 → 907.8 |
| mass-budget.json#/classes/P1000/batterySensitivity/demonstrated/16 cycles/leftForShellT | -2815.5 → -2831.1 | -2831.1 → -2875.7 |
| mass-budget.json#/classes/P1000/batterySensitivity/demonstrated/16 cycles/totalT | 4378.6 → 4397.3 | 4397.3 → 4450.9 |
| mass-budget.json#/classes/P1000/batterySensitivity/demonstrated/2 cycles/batteryMWh | 14.8 → 16.91 | 16.91 → 16.91 |
| mass-budget.json#/classes/P1000/batterySensitivity/demonstrated/2 cycles/batteryT | 99.3 → 113.5 | 113.5 → 113.5 |
| mass-budget.json#/classes/P1000/batterySensitivity/demonstrated/2 cycles/leftForShellT | -2120.3 → -2036.8 | -2036.8 → -2081.4 |
| mass-budget.json#/classes/P1000/batterySensitivity/demonstrated/2 cycles/totalT | 3544.3 → 3444.1 | 3444.1 → 3497.7 |
| mass-budget.json#/classes/P1000/batterySensitivity/demonstrated/4 cycles/batteryMWh | 29.6 → 33.82 | 33.82 → 33.82 |
| mass-budget.json#/classes/P1000/batterySensitivity/demonstrated/4 cycles/batteryT | 198.6 → 227.0 | 227.0 → 227.0 |
| mass-budget.json#/classes/P1000/batterySensitivity/demonstrated/4 cycles/leftForShellT | -2219.6 → -2150.2 | -2150.2 → -2194.9 |
| mass-budget.json#/classes/P1000/batterySensitivity/demonstrated/4 cycles/totalT | 3663.5 → 3580.3 | 3580.3 → 3633.9 |
| mass-budget.json#/classes/P1000/batterySensitivity/demonstrated/8 cycles/batteryMWh | 59.19 → 67.63 | 67.63 → 67.63 |
| mass-budget.json#/classes/P1000/batterySensitivity/demonstrated/8 cycles/batteryT | 397.3 → 453.9 | 453.9 → 453.9 |
| mass-budget.json#/classes/P1000/batterySensitivity/demonstrated/8 cycles/leftForShellT | -2418.2 → -2377.2 | -2377.2 → -2421.8 |
| mass-budget.json#/classes/P1000/batterySensitivity/demonstrated/8 cycles/totalT | 3901.9 → 3852.6 | 3852.6 → 3906.2 |
| mass-budget.json#/classes/P1000/batterySensitivity/floor/16 cycles/batteryMWh | 118.38 → 135.26 | 135.26 → 135.26 |
| mass-budget.json#/classes/P1000/batterySensitivity/floor/16 cycles/batteryT | 236.8 → 270.5 | 270.5 → 270.5 |
| mass-budget.json#/classes/P1000/batterySensitivity/floor/16 cycles/leftForShellT | 388.8 → 357.7 | 357.7 → 356.5 |
| mass-budget.json#/classes/P1000/batterySensitivity/floor/16 cycles/requiredShellKgPerM3 | 0.1767 → 0.1626 | 0.1626 → 0.162 |
| mass-budget.json#/classes/P1000/batterySensitivity/floor/16 cycles/totalT | 572.3 → 606.5 | 606.5 → 607.9 |
| mass-budget.json#/classes/P1000/batterySensitivity/floor/2 cycles/batteryMWh | 14.8 → 16.91 | 16.91 → 16.91 |
| mass-budget.json#/classes/P1000/batterySensitivity/floor/2 cycles/batteryT | 29.6 → 33.8 | 33.8 → 33.8 |
| mass-budget.json#/classes/P1000/batterySensitivity/floor/2 cycles/leftForShellT | 596.0 → 594.4 | 594.4 → 593.2 |
| mass-budget.json#/classes/P1000/batterySensitivity/floor/2 cycles/requiredShellKgPerM3 | 0.2709 → 0.2702 | 0.2702 → 0.2696 |
| mass-budget.json#/classes/P1000/batterySensitivity/floor/2 cycles/totalT | 344.4 → 346.2 | 346.2 → 347.5 |
| mass-budget.json#/classes/P1000/batterySensitivity/floor/4 cycles/batteryMWh | 29.6 → 33.82 | 33.82 → 33.82 |
| mass-budget.json#/classes/P1000/batterySensitivity/floor/4 cycles/batteryT | 59.2 → 67.6 | 67.6 → 67.6 |
| mass-budget.json#/classes/P1000/batterySensitivity/floor/4 cycles/leftForShellT | 566.4 → 560.6 | 560.6 → 559.4 |
| mass-budget.json#/classes/P1000/batterySensitivity/floor/4 cycles/requiredShellKgPerM3 | 0.2574 → 0.2548 | 0.2548 → 0.2543 |
| mass-budget.json#/classes/P1000/batterySensitivity/floor/4 cycles/totalT | 377.0 → 383.4 | 383.4 → 384.7 |
| mass-budget.json#/classes/P1000/batterySensitivity/floor/8 cycles/batteryMWh | 59.19 → 67.63 | 67.63 → 67.63 |
| mass-budget.json#/classes/P1000/batterySensitivity/floor/8 cycles/batteryT | 118.4 → 135.3 | 135.3 → 135.3 |
| mass-budget.json#/classes/P1000/batterySensitivity/floor/8 cycles/leftForShellT | 507.2 → 492.9 | 492.9 → 491.7 |
| mass-budget.json#/classes/P1000/batterySensitivity/floor/8 cycles/requiredShellKgPerM3 | 0.2305 → 0.2241 | 0.2241 → 0.2235 |
| mass-budget.json#/classes/P1000/batterySensitivity/floor/8 cycles/totalT | 442.1 → 457.8 | 457.8 → 459.1 |
| mass-budget.json#/classes/P1000/cases/credible/baseExShellExSundriesT | 1410.33 → 1383.88 | 1383.88 → 1395.97 |
| mass-budget.json#/classes/P1000/cases/credible/everythingButShellT | 1869.4 → 1839.0 | 1839.0 → 1852.9 |
| mass-budget.json#/classes/P1000/cases/credible/lines/1/driver | 104,349 m2 hull surface → 76,039 m2 hull surface | 76,039 m2 hull surface → 88,976 m2 hull surface |
| mass-budget.json#/classes/P1000/cases/credible/lines/1/tonnes | 97.51 → 71.06 | 71.06 → 83.15 |
| mass-budget.json#/classes/P1000/cases/credible/lines/15/tonnes | 459.05 → 455.08 | 455.08 → 456.9 |
| mass-budget.json#/classes/P1000/cases/credible/overBy | 3.52 → 3.49 | 3.49 → 3.5 |
| mass-budget.json#/classes/P1000/cases/credible/totalT | 3519.4 → 3489.0 | 3489.0 → 3502.9 |
| mass-budget.json#/classes/P1000/cases/demonstrated/baseExShellExSundriesT | 3659.66 → 3561.99 | 3561.99 → 3606.63 |
| mass-budget.json#/classes/P1000/cases/demonstrated/everythingButShellT | 4902.0 → 4784.8 | 4784.8 → 4838.4 |
| mass-budget.json#/classes/P1000/cases/demonstrated/lines/1/driver | 104,349 m2 hull surface → 76,039 m2 hull surface | 76,039 m2 hull surface → 88,976 m2 hull surface |
| mass-budget.json#/classes/P1000/cases/demonstrated/lines/1/tonnes | 360.0 → 262.33 | 262.33 → 306.97 |
| mass-budget.json#/classes/P1000/cases/demonstrated/lines/15/tonnes | 1242.33 → 1222.8 | 1222.8 → 1231.73 |
| mass-budget.json#/classes/P1000/cases/demonstrated/overBy | 7.45 → 7.34 | 7.34 → 7.39 |
| mass-budget.json#/classes/P1000/cases/demonstrated/totalT | 7454.0 → 7336.8 | 7336.8 → 7390.4 |
| mass-budget.json#/classes/P1000/cases/floor/baseExShellExSundriesT | 523.52 → 520.88 | 520.88 → 522.08 |
| mass-budget.json#/classes/P1000/cases/floor/everythingButShellT | 687.6 → 684.7 | 684.7 → 686.0 |
| mass-budget.json#/classes/P1000/cases/floor/lines/1/driver | 104,349 m2 hull surface → 76,039 m2 hull surface | 76,039 m2 hull surface → 88,976 m2 hull surface |
| mass-budget.json#/classes/P1000/cases/floor/lines/1/tonnes | 9.75 → 7.11 | 7.11 → 8.31 |
| mass-budget.json#/classes/P1000/cases/floor/lines/15/tonnes | 164.11 → 163.85 | 163.85 → 163.97 |
| mass-budget.json#/classes/P1000/cases/floor/overBy | 1.81 → 1.8 | 1.8 → 1.8 |
| mass-budget.json#/classes/P1000/cases/floor/totalT | 1805.2 → 1802.3 | 1802.3 → 1803.6 |
| mass-budget.json#/classes/P1000/descentWithoutNitrogen/cycleMWhAsBuilt | 7.399 → 8.454 | 8.454 → 8.454 |
| mass-budget.json#/classes/P1000/descentWithoutNitrogen/cycleMWhWithoutCryo | 4.703 → 5.758 | 5.758 → 5.758 |
| mass-budget.json#/classes/P1000/descentWithoutNitrogen/cycleSavingPct | 36.4 → 31.9 | 31.9 → 31.9 |
| mass-budget.json#/classes/P1000/hullAreaM2 | 104349 → 76039 | 76039 → 88976 |
| mass-budget.json#/classes/P1000/requiredKgPerM2 | 9.583 → 13.151 | 13.151 → 11.239 |
| mass-budget.json#/classes/P1000/rightSized/credible/baseExShellExSundriesT | 1084.32 → 1068.42 | 1068.42 → 1080.51 |
| mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.74/0.264/diaM | 137 → 158 | 158 → 159 |
| mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.74/0.264/lenM | 542 → 317 | 317 → 318 |
| mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.74/0.264/timesBaseline | 2.41 → 2.36 | 2.36 → 2.39 |
| mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.74/0.264/volumeM3 | 5298629 → 5197580 | 5197580 → 5256638 |
| mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.74/0.508/diaM | 183 → 211 | 211 → 212 |
| mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.74/0.508/lenM | 725 → 422 | 422 → 424 |
| mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.74/0.508/timesBaseline | 5.78 → 5.56 | 5.56 → 5.67 |
| mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.74/0.508/volumeM3 | 12706475 → 12236757 | 12236757 → 12478961 |
| mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.85/0.264/diaM | 127 → 147 | 147 → 148 |
| mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.85/0.264/lenM | 502 → 294 | 294 → 295 |
| mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.85/0.264/timesBaseline | 1.92 → 1.89 | 1.89 → 1.91 |
| mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.85/0.264/volumeM3 | 4222239 → 4155775 | 4155775 → 4196569 |
| mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.85/0.508/diaM | 157 → 181 | 181 → 182 |
| mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.85/0.508/lenM | 620 → 362 | 362 → 364 |
| mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.85/0.508/timesBaseline | 3.61 → 3.52 | 3.52 → 3.57 |
| mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.85/0.508/volumeM3 | 7949564 → 7740792 | 7740792 → 7854781 |
| mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.85/0.750/diaM | 290 → 327 | 327 → 332 |
| mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.85/0.750/lenM | 1147 → 655 | 655 → 665 |
| mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.85/0.750/timesBaseline | 22.87 → 20.84 | 20.84 → 21.78 |
| mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=0.85/0.750/volumeM3 | 50306574 → 45844716 | 45844716 → 47925841 |
| mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=1.0/0.264/diaM | 117 → 136 | 136 → 136 |
| mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=1.0/0.264/lenM | 463 → 271 | 271 → 272 |
| mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=1.0/0.264/timesBaseline | 1.5 → 1.48 | 1.48 → 1.49 |
| mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=1.0/0.264/volumeM3 | 3302788 → 3261101 | 3261101 → 3288408 |
| mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=1.0/0.508/diaM | 136 → 158 | 158 → 158 |
| mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=1.0/0.508/lenM | 539 → 316 | 316 → 317 |
| mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=1.0/0.508/timesBaseline | 2.38 → 2.34 | 2.34 → 2.36 |
| mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=1.0/0.508/volumeM3 | 5238099 → 5139145 | 5139145 → 5197109 |
| mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=1.0/0.750/diaM | 181 → 208 | 208 → 210 |
| mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=1.0/0.750/lenM | 716 → 417 | 417 → 419 |
| mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=1.0/0.750/timesBaseline | 5.56 → 5.36 | 5.36 → 5.47 |
| mass-budget.json#/classes/P1000/rightSized/credible/cellular/phi=1.0/0.750/volumeM3 | 12238660 → 11798027 | 11798027 → 12026131 |
| mass-budget.json#/classes/P1000/rightSized/credible/everythingButShellT | 1494.5 → 1476.2 | 1476.2 → 1490.1 |
| mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.264/diaM | 117 → 136 | 136 → 136 |
| mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.264/lenM | 463 → 271 | 271 → 272 |
| mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.264/timesBaseline | 1.5 → 1.48 | 1.48 → 1.49 |
| mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.264/volumeM3 | 3302788 → 3261101 | 3261101 → 3288408 |
| mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.350/diaM | 122 → 142 | 142 → 143 |
| mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.350/lenM | 485 → 284 | 284 → 285 |
| mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.350/timesBaseline | 1.73 → 1.7 | 1.7 → 1.72 |
| mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.350/volumeM3 | 3798952 → 3744468 | 3744468 → 3778798 |
| mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.508/diaM | 136 → 158 | 158 → 158 |
| mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.508/lenM | 539 → 316 | 316 → 317 |
| mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.508/timesBaseline | 2.38 → 2.34 | 2.34 → 2.36 |
| mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.508/volumeM3 | 5238099 → 5139145 | 5139145 → 5197109 |
| mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.600/diaM | 148 → 171 | 171 → 172 |
| mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.600/lenM | 586 → 342 | 342 → 344 |
| mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.600/timesBaseline | 3.05 → 2.98 | 2.98 → 3.02 |
| mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.600/volumeM3 | 6707672 → 6553121 | 6553121 → 6639723 |
| mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.750/diaM | 181 → 208 | 208 → 210 |
| mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.750/lenM | 716 → 417 | 417 → 419 |
| mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.750/timesBaseline | 5.56 → 5.36 | 5.36 → 5.47 |
| mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.750/volumeM3 | 12238660 → 11798027 | 11798027 → 12026131 |
| mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.900/diaM | 303 → 342 | 342 → 348 |
| mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.900/lenM | 1202 → 684 | 684 → 695 |
| mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.900/timesBaseline | 26.31 → 23.78 | 23.78 → 24.95 |
| mass-budget.json#/classes/P1000/rightSized/credible/hullThatCloses/0.900/volumeM3 | 57879596 → 52321328 | 52321328 → 54895008 |
| mass-budget.json#/classes/P1000/rightSized/credible/lines/1/driver | 104,349 m2 hull surface → 76,039 m2 hull surface | 76,039 m2 hull surface → 88,976 m2 hull surface |
| mass-budget.json#/classes/P1000/rightSized/credible/lines/1/tonnes | 97.51 → 71.06 | 71.06 → 83.15 |
| mass-budget.json#/classes/P1000/rightSized/credible/lines/15/tonnes | 410.15 → 407.76 | 407.76 → 409.58 |
| mass-budget.json#/classes/P1000/rightSized/credible/lines/3/driver | 22.20 MWh → 25.36 MWh | 25.36 MWh → 25.36 MWh |
| mass-budget.json#/classes/P1000/rightSized/credible/lines/3/tonnes | 73.99 → 84.54 | 84.54 → 84.54 |
| mass-budget.json#/classes/P1000/rightSized/credible/shellBudgetLeftT | -214.8 → -198.9 | -198.9 → -210.9 |
| mass-budget.json#/classes/P1000/rightSized/credible/totalT | 3144.5 → 3126.2 | 3126.2 → 3140.1 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/baseExShellExSundriesT | 3003.26 → 2926.83 | 2926.83 → 2971.47 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.74/0.264/diaM | 183 → 208 | 208 → 211 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.74/0.264/lenM | 725 → 417 | 417 → 422 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.74/0.264/timesBaseline | 5.79 → 5.37 | 5.37 → 5.57 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.74/0.264/volumeM3 | 12732283 → 11813346 | 11813346 → 12252804 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.74/0.508/diaM | 259 → 288 | 288 → 294 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.74/0.508/lenM | 1024 → 576 | 576 → 589 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.74/0.508/timesBaseline | 16.28 → 14.17 | 14.17 → 15.12 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.74/0.508/volumeM3 | 35813317 → 31170011 | 31170011 → 33268676 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.85/0.264/diaM | 168 → 192 | 192 → 194 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.85/0.264/lenM | 666 → 384 | 384 → 388 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.85/0.264/timesBaseline | 4.48 → 4.21 | 4.21 → 4.34 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.85/0.264/volumeM3 | 9858098 → 9251790 | 9251790 → 9546847 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.85/0.508/diaM | 214 → 242 | 242 → 245 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.85/0.508/lenM | 848 → 483 | 483 → 491 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.85/0.508/timesBaseline | 9.25 → 8.37 | 8.37 → 8.78 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.85/0.508/volumeM3 | 20347491 → 18408695 | 18408695 → 19310540 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.85/0.750/diaM | 482 → 502 | 502 → 529 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.85/0.750/lenM | 1907 → 1005 | 1005 → 1058 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.85/0.750/timesBaseline | 105.2 → 75.28 | 75.28 → 87.77 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=0.85/0.750/volumeM3 | 231441856 → 165612073 | 165612073 → 193090069 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=1.0/0.264/diaM | 154 → 176 | 176 → 178 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=1.0/0.264/lenM | 608 → 352 | 352 → 355 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=1.0/0.264/timesBaseline | 3.41 → 3.24 | 3.24 → 3.32 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=1.0/0.264/volumeM3 | 7508387 → 7121454 | 7121454 → 7313772 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=1.0/0.508/diaM | 182 → 208 | 208 → 210 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=1.0/0.508/lenM | 722 → 415 | 415 → 420 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=1.0/0.508/timesBaseline | 5.71 → 5.3 | 5.3 → 5.5 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=1.0/0.508/volumeM3 | 12567220 → 11667438 | 11667438 → 12098099 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=1.0/0.750/diaM | 255 → 284 | 284 → 290 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=1.0/0.750/lenM | 1008 → 568 | 568 → 580 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=1.0/0.750/timesBaseline | 15.54 → 13.58 | 13.58 → 14.47 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/cellular/phi=1.0/0.750/volumeM3 | 34193223 → 29865418 | 29865418 → 31825841 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/everythingButShellT | 4114.3 → 4022.6 | 4022.6 → 4076.2 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.264/diaM | 154 → 176 | 176 → 178 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.264/lenM | 608 → 352 | 352 → 355 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.264/timesBaseline | 3.41 → 3.24 | 3.24 → 3.32 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.264/volumeM3 | 7508387 → 7121454 | 7121454 → 7313772 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.350/diaM | 162 → 185 | 185 → 187 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.350/lenM | 640 → 370 | 370 → 374 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.350/timesBaseline | 3.98 → 3.76 | 3.76 → 3.87 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.350/volumeM3 | 8764007 → 8264220 | 8264220 → 8509580 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.508/diaM | 182 → 208 | 208 → 210 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.508/lenM | 722 → 415 | 415 → 420 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.508/timesBaseline | 5.71 → 5.3 | 5.3 → 5.5 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.508/volumeM3 | 12567220 → 11667438 | 11667438 → 12098099 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.600/diaM | 200 → 227 | 227 → 230 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.600/lenM | 794 → 454 | 454 → 461 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.600/timesBaseline | 7.59 → 6.94 | 6.94 → 7.24 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.600/volumeM3 | 16687176 → 15269992 | 15269992 → 15936605 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.750/diaM | 255 → 284 | 284 → 290 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.750/lenM | 1008 → 568 | 568 → 580 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.750/timesBaseline | 15.54 → 13.58 | 13.58 → 14.47 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.750/volumeM3 | 34193223 → 29865418 | 29865418 → 31825841 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.900/diaM | 517 → 534 | 534 → 565 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.900/lenM | 2046 → 1068 | 1068 → 1129 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.900/timesBaseline | 129.85 → 90.43 | 90.43 → 106.76 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/hullThatCloses/0.900/volumeM3 | 285676058 → 198936815 | 198936815 → 234865032 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/lines/1/driver | 104,349 m2 hull surface → 76,039 m2 hull surface | 76,039 m2 hull surface → 88,976 m2 hull surface |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/lines/1/tonnes | 360.0 → 262.33 | 262.33 → 306.97 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/lines/15/tonnes | 1111.05 → 1095.77 | 1095.77 → 1104.69 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/lines/3/driver | 22.20 MWh → 25.36 MWh | 25.36 MWh → 25.36 MWh |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/lines/3/tonnes | 148.97 → 170.21 | 170.21 → 170.21 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/overBy | 6.67 → 6.57 | 6.57 → 6.63 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/shellBudgetLeftT | -2169.9 → -2093.5 | -2093.5 → -2138.1 |
| mass-budget.json#/classes/P1000/rightSized/demonstrated/totalT | 6666.3 → 6574.6 | 6574.6 → 6628.2 |
| mass-budget.json#/classes/P1000/rightSized/floor/baseExShellExSundriesT | 327.91 → 331.6 | 331.6 → 332.8 |
| mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=0.74/0.264/diaM | 114 → 133 | 133 → 133 |
| mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=0.74/0.264/lenM | 452 → 266 | 266 → 266 |
| mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=0.74/0.264/volumeM3 | 3076424 → 3084014 | 3084014 → 3087784 |
| mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=0.74/0.508/diaM | 149 → 174 | 174 → 175 |
| mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=0.74/0.508/lenM | 592 → 349 | 349 → 349 |
| mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=0.74/0.508/timesBaseline | 3.15 → 3.15 | 3.15 → 3.16 |
| mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=0.74/0.508/volumeM3 | 6926097 → 6929793 | 6929793 → 6944272 |
| mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=0.85/0.264/diaM | 106 → 124 | 124 → 124 |
| mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=0.85/0.264/lenM | 420 → 248 | 248 → 248 |
| mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=0.85/0.264/volumeM3 | 2480324 → 2487343 | 2487343 → 2489979 |
| mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=0.85/0.508/diaM | 129 → 151 | 151 → 151 |
| mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=0.85/0.508/lenM | 513 → 302 | 302 → 302 |
| mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=0.85/0.508/volumeM3 | 4500170 → 4507761 | 4507761 → 4514847 |
| mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=0.85/0.750/diaM | 222 → 259 | 259 → 259 |
| mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=0.85/0.750/lenM | 881 → 518 | 518 → 519 |
| mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=0.85/0.750/volumeM3 | 22777568 → 22665013 | 22665013 → 22768289 |
| mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=1.0/0.264/diaM | 98 → 115 | 115 → 115 |
| mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=1.0/0.264/lenM | 389 → 229 | 229 → 229 |
| mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=1.0/0.264/timesBaseline | 0.89 → 0.89 | 0.89 → 0.9 |
| mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=1.0/0.264/volumeM3 | 1961575 → 1967796 | 1967796 → 1969581 |
| mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=1.0/0.508/diaM | 114 → 133 | 133 → 133 |
| mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=1.0/0.508/lenM | 450 → 265 | 265 → 266 |
| mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=1.0/0.508/timesBaseline | 1.38 → 1.39 | 1.39 → 1.39 |
| mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=1.0/0.508/volumeM3 | 3043201 → 3050769 | 3050769 → 3054471 |
| mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=1.0/0.750/diaM | 148 → 172 | 172 → 173 |
| mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=1.0/0.750/lenM | 585 → 345 | 345 → 345 |
| mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=1.0/0.750/timesBaseline | 3.04 → 3.04 | 3.04 → 3.05 |
| mass-budget.json#/classes/P1000/rightSized/floor/cellular/phi=1.0/0.750/volumeM3 | 6693884 → 6698148 | 6698148 → 6711833 |
| mass-budget.json#/classes/P1000/rightSized/floor/everythingButShellT | 472.5 → 476.5 | 476.5 → 477.8 |
| mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.264/diaM | 98 → 115 | 115 → 115 |
| mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.264/lenM | 389 → 229 | 229 → 229 |
| mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.264/timesBaseline | 0.89 → 0.89 | 0.89 → 0.9 |
| mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.264/volumeM3 | 1961575 → 1967796 | 1967796 → 1969581 |
| mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.350/diaM | 103 → 120 | 120 → 120 |
| mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.350/lenM | 407 → 240 | 240 → 240 |
| mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.350/volumeM3 | 2242666 → 2249356 | 2249356 → 2251586 |
| mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.508/diaM | 114 → 133 | 133 → 133 |
| mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.508/lenM | 450 → 265 | 265 → 266 |
| mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.508/timesBaseline | 1.38 → 1.39 | 1.39 → 1.39 |
| mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.508/volumeM3 | 3043201 → 3050769 | 3050769 → 3054471 |
| mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.600/diaM | 123 → 143 | 143 → 143 |
| mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.600/lenM | 486 → 287 | 287 → 287 |
| mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.600/volumeM3 | 3840488 → 3848306 | 3848306 → 3853753 |
| mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.750/diaM | 148 → 172 | 172 → 173 |
| mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.750/lenM | 585 → 345 | 345 → 345 |
| mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.750/timesBaseline | 3.04 → 3.04 | 3.04 → 3.05 |
| mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.750/volumeM3 | 6693884 → 6698148 | 6698148 → 6711833 |
| mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.900/diaM | 231 → 269 | 269 → 269 |
| mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.900/lenM | 914 → 538 | 538 → 539 |
| mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.900/timesBaseline | 11.6 → 11.53 | 11.53 → 11.59 |
| mass-budget.json#/classes/P1000/rightSized/floor/hullThatCloses/0.900/volumeM3 | 25513024 → 25367320 | 25367320 → 25491741 |
| mass-budget.json#/classes/P1000/rightSized/floor/lines/1/driver | 104,349 m2 hull surface → 76,039 m2 hull surface | 76,039 m2 hull surface → 88,976 m2 hull surface |
| mass-budget.json#/classes/P1000/rightSized/floor/lines/1/tonnes | 9.75 → 7.11 | 7.11 → 8.31 |
| mass-budget.json#/classes/P1000/rightSized/floor/lines/15/tonnes | 144.55 → 144.92 | 144.92 → 145.04 |
| mass-budget.json#/classes/P1000/rightSized/floor/lines/3/driver | 22.20 MWh → 25.36 MWh | 25.36 MWh → 25.36 MWh |
| mass-budget.json#/classes/P1000/rightSized/floor/lines/3/tonnes | 44.39 → 50.72 | 50.72 → 50.72 |
| mass-budget.json#/classes/P1000/rightSized/floor/overBy | 1.59 → 1.59 | 1.59 → 1.6 |
| mass-budget.json#/classes/P1000/rightSized/floor/requiredShellKgPerM3 | 0.2642 → 0.2625 | 0.2625 → 0.262 |
| mass-budget.json#/classes/P1000/rightSized/floor/shellBudgetLeftT | 581.2 → 577.5 | 577.5 → 576.3 |
| mass-budget.json#/classes/P1000/rightSized/floor/totalT | 1590.1 → 1594.1 | 1594.1 → 1595.4 |
| mass-budget.json#/classes/P10000/batterySensitivity/credible/16 cycles/batteryMWh | 733.9 → 869.2 | 869.2 → 869.2 |
| mass-budget.json#/classes/P10000/batterySensitivity/credible/16 cycles/batteryT | 2446.3 → 2897.3 | 2897.3 → 2897.3 |
| mass-budget.json#/classes/P10000/batterySensitivity/credible/16 cycles/leftForShellT | -62.6 → -244.5 | -244.5 → -365.0 |
| mass-budget.json#/classes/P10000/batterySensitivity/credible/16 cycles/totalT | 10072.0 → 10281.1 | 10281.1 → 10419.8 |
| mass-budget.json#/classes/P10000/batterySensitivity/credible/2 cycles/batteryMWh | 91.74 → 108.65 | 108.65 → 108.65 |
| mass-budget.json#/classes/P10000/batterySensitivity/credible/2 cycles/batteryT | 305.8 → 362.2 | 362.2 → 362.2 |
| mass-budget.json#/classes/P10000/batterySensitivity/credible/2 cycles/leftForShellT | 2077.9 → 2290.7 | 2290.7 → 2170.2 |
| mass-budget.json#/classes/P10000/batterySensitivity/credible/2 cycles/requiredShellKgPerM3 | 0.0945 → 0.1041 | 0.1041 → 0.0986 |
| mass-budget.json#/classes/P10000/batterySensitivity/credible/2 cycles/totalT | 7610.4 → 7365.7 | 7365.7 → 7504.3 |
| mass-budget.json#/classes/P10000/batterySensitivity/credible/4 cycles/batteryMWh | 183.48 → 217.3 | 217.3 → 217.3 |
| mass-budget.json#/classes/P10000/batterySensitivity/credible/4 cycles/batteryT | 611.6 → 724.3 | 724.3 → 724.3 |
| mass-budget.json#/classes/P10000/batterySensitivity/credible/4 cycles/leftForShellT | 1772.2 → 1928.5 | 1928.5 → 1808.0 |
| mass-budget.json#/classes/P10000/batterySensitivity/credible/4 cycles/requiredShellKgPerM3 | 0.0806 → 0.0877 | 0.0877 → 0.0822 |
| mass-budget.json#/classes/P10000/batterySensitivity/credible/4 cycles/totalT | 7962.0 → 7782.2 | 7782.2 → 7920.8 |
| mass-budget.json#/classes/P10000/batterySensitivity/credible/8 cycles/batteryMWh | 366.95 → 434.6 | 434.6 → 434.6 |
| mass-budget.json#/classes/P10000/batterySensitivity/credible/8 cycles/batteryT | 1223.2 → 1448.7 | 1448.7 → 1448.7 |
| mass-budget.json#/classes/P10000/batterySensitivity/credible/8 cycles/leftForShellT | 1160.6 → 1204.2 | 1204.2 → 1083.7 |
| mass-budget.json#/classes/P10000/batterySensitivity/credible/8 cycles/requiredShellKgPerM3 | 0.0528 → 0.0547 | 0.0547 → 0.0493 |
| mass-budget.json#/classes/P10000/batterySensitivity/credible/8 cycles/totalT | 8665.3 → 8615.2 | 8615.2 → 8753.8 |
| mass-budget.json#/classes/P10000/batterySensitivity/demonstrated/16 cycles/batteryMWh | 733.9 → 869.2 | 869.2 → 869.2 |
| mass-budget.json#/classes/P10000/batterySensitivity/demonstrated/16 cycles/batteryT | 4925.5 → 5833.6 | 5833.6 → 5833.6 |
| mass-budget.json#/classes/P10000/batterySensitivity/demonstrated/16 cycles/leftForShellT | -10387.0 → -10833.9 | -10833.9 → -11040.4 |
| mass-budget.json#/classes/P10000/batterySensitivity/demonstrated/16 cycles/totalT | 22464.4 → 23000.6 | 23000.6 → 23248.5 |
| mass-budget.json#/classes/P10000/batterySensitivity/demonstrated/2 cycles/batteryMWh | 91.74 → 108.65 | 108.65 → 108.65 |
| mass-budget.json#/classes/P10000/batterySensitivity/demonstrated/2 cycles/batteryT | 615.7 → 729.2 | 729.2 → 729.2 |
| mass-budget.json#/classes/P10000/batterySensitivity/demonstrated/2 cycles/leftForShellT | -6077.2 → -5729.5 | -5729.5 → -5936.1 |
| mass-budget.json#/classes/P10000/batterySensitivity/demonstrated/2 cycles/totalT | 17292.6 → 16875.4 | 16875.4 → 17123.3 |
| mass-budget.json#/classes/P10000/batterySensitivity/demonstrated/4 cycles/batteryMWh | 183.48 → 217.3 | 217.3 → 217.3 |
| mass-budget.json#/classes/P10000/batterySensitivity/demonstrated/4 cycles/batteryT | 1231.4 → 1458.4 | 1458.4 → 1458.4 |
| mass-budget.json#/classes/P10000/batterySensitivity/demonstrated/4 cycles/leftForShellT | -6692.9 → -6458.7 | -6458.7 → -6665.3 |
| mass-budget.json#/classes/P10000/batterySensitivity/demonstrated/4 cycles/totalT | 18031.4 → 17750.4 | 17750.4 → 17998.3 |
| mass-budget.json#/classes/P10000/batterySensitivity/demonstrated/8 cycles/batteryMWh | 366.95 → 434.6 | 434.6 → 434.6 |
| mass-budget.json#/classes/P10000/batterySensitivity/demonstrated/8 cycles/batteryT | 2462.8 → 2916.8 | 2916.8 → 2916.8 |
| mass-budget.json#/classes/P10000/batterySensitivity/demonstrated/8 cycles/leftForShellT | -7924.2 → -7917.1 | -7917.1 → -8123.6 |
| mass-budget.json#/classes/P10000/batterySensitivity/demonstrated/8 cycles/totalT | 19509.1 → 19500.5 | 19500.5 → 19748.4 |
| mass-budget.json#/classes/P10000/batterySensitivity/floor/16 cycles/batteryMWh | 733.9 → 869.2 | 869.2 → 869.2 |
| mass-budget.json#/classes/P10000/batterySensitivity/floor/16 cycles/batteryT | 1467.8 → 1738.4 | 1738.4 → 1738.4 |
| mass-budget.json#/classes/P10000/batterySensitivity/floor/16 cycles/leftForShellT | 5035.0 → 4791.3 | 4791.3 → 4779.2 |
| mass-budget.json#/classes/P10000/batterySensitivity/floor/16 cycles/requiredShellKgPerM3 | 0.2289 → 0.2178 | 0.2178 → 0.2172 |
| mass-budget.json#/classes/P10000/batterySensitivity/floor/16 cycles/totalT | 4461.6 → 4729.6 | 4729.6 → 4742.9 |
| mass-budget.json#/classes/P10000/batterySensitivity/floor/2 cycles/batteryMWh | 91.74 → 108.65 | 108.65 → 108.65 |
| mass-budget.json#/classes/P10000/batterySensitivity/floor/2 cycles/batteryT | 183.5 → 217.3 | 217.3 → 217.3 |
| mass-budget.json#/classes/P10000/batterySensitivity/floor/2 cycles/leftForShellT | 6319.3 → 6312.4 | 6312.4 → 6300.3 |
| mass-budget.json#/classes/P10000/batterySensitivity/floor/2 cycles/requiredShellKgPerM3 | 0.2872 → 0.2869 | 0.2869 → 0.2864 |
| mass-budget.json#/classes/P10000/batterySensitivity/floor/2 cycles/totalT | 3048.8 → 3056.4 | 3056.4 → 3069.6 |
| mass-budget.json#/classes/P10000/batterySensitivity/floor/4 cycles/batteryMWh | 183.48 → 217.3 | 217.3 → 217.3 |
| mass-budget.json#/classes/P10000/batterySensitivity/floor/4 cycles/batteryT | 367.0 → 434.6 | 434.6 → 434.6 |
| mass-budget.json#/classes/P10000/batterySensitivity/floor/4 cycles/leftForShellT | 6135.8 → 6095.1 | 6095.1 → 6083.0 |
| mass-budget.json#/classes/P10000/batterySensitivity/floor/4 cycles/requiredShellKgPerM3 | 0.2789 → 0.277 | 0.277 → 0.2765 |
| mass-budget.json#/classes/P10000/batterySensitivity/floor/4 cycles/totalT | 3250.6 → 3295.4 | 3295.4 → 3308.7 |
| mass-budget.json#/classes/P10000/batterySensitivity/floor/8 cycles/batteryMWh | 366.95 → 434.6 | 434.6 → 434.6 |
| mass-budget.json#/classes/P10000/batterySensitivity/floor/8 cycles/batteryT | 733.9 → 869.2 | 869.2 → 869.2 |
| mass-budget.json#/classes/P10000/batterySensitivity/floor/8 cycles/leftForShellT | 5768.9 → 5660.5 | 5660.5 → 5648.4 |
| mass-budget.json#/classes/P10000/batterySensitivity/floor/8 cycles/requiredShellKgPerM3 | 0.2622 → 0.2573 | 0.2573 → 0.2567 |
| mass-budget.json#/classes/P10000/batterySensitivity/floor/8 cycles/totalT | 3654.3 → 3773.5 | 3773.5 → 3786.7 |
| mass-budget.json#/classes/P10000/cases/credible/baseExShellExSundriesT | 12978.58 → 12709.45 | 12709.45 → 12830.0 |
| mass-budget.json#/classes/P10000/cases/credible/everythingButShellT | 17400.4 → 17090.9 | 17090.9 → 17229.5 |
| mass-budget.json#/classes/P10000/cases/credible/lines/1/driver | 485,575 m2 hull surface → 351,903 m2 hull surface | 351,903 m2 hull surface → 411,775 m2 hull surface |
| mass-budget.json#/classes/P10000/cases/credible/lines/1/tonnes | 977.62 → 708.49 | 708.49 → 829.04 |
| mass-budget.json#/classes/P10000/cases/credible/lines/15/tonnes | 4421.79 → 4381.42 | 4381.42 → 4399.5 |
| mass-budget.json#/classes/P10000/cases/credible/overBy | 3.39 → 3.36 | 3.36 → 3.37 |
| mass-budget.json#/classes/P10000/cases/credible/totalT | 33900.4 → 33590.9 | 33590.9 → 33729.5 |
| mass-budget.json#/classes/P10000/cases/demonstrated/baseExShellExSundriesT | 27217.63 → 26756.46 | 26756.46 → 26963.02 |
| mass-budget.json#/classes/P10000/cases/demonstrated/everythingButShellT | 37765.2 → 37211.8 | 37211.8 → 37459.6 |
| mass-budget.json#/classes/P10000/cases/demonstrated/lines/1/driver | 485,575 m2 hull surface → 351,903 m2 hull surface | 351,903 m2 hull surface → 411,775 m2 hull surface |
| mass-budget.json#/classes/P10000/cases/demonstrated/lines/1/tonnes | 1675.23 → 1214.06 | 1214.06 → 1420.62 |
| mass-budget.json#/classes/P10000/cases/demonstrated/lines/15/tonnes | 10547.53 → 10455.29 | 10455.29 → 10496.6 |
| mass-budget.json#/classes/P10000/cases/demonstrated/overBy | 6.33 → 6.27 | 6.27 → 6.3 |
| mass-budget.json#/classes/P10000/cases/demonstrated/totalT | 63285.2 → 62731.8 | 62731.8 → 62979.6 |
| mass-budget.json#/classes/P10000/cases/floor/baseExShellExSundriesT | 6588.15 → 6561.24 | 6561.24 → 6573.29 |
| mass-budget.json#/classes/P10000/cases/floor/everythingButShellT | 8364.6 → 8335.0 | 8335.0 → 8348.2 |
| mass-budget.json#/classes/P10000/cases/floor/lines/1/driver | 485,575 m2 hull surface → 351,903 m2 hull surface | 351,903 m2 hull surface → 411,775 m2 hull surface |
| mass-budget.json#/classes/P10000/cases/floor/lines/1/tonnes | 97.76 → 70.85 | 70.85 → 82.9 |
| mass-budget.json#/classes/P10000/cases/floor/lines/15/tonnes | 1776.42 → 1773.72 | 1773.72 → 1774.93 |
| mass-budget.json#/classes/P10000/cases/floor/totalT | 19540.6 → 19511.0 | 19511.0 → 19524.2 |
| mass-budget.json#/classes/P10000/descentWithoutNitrogen/cycleMWhAsBuilt | 45.869 → 54.325 | 54.325 → 54.325 |
| mass-budget.json#/classes/P10000/descentWithoutNitrogen/cycleMWhWithoutCryo | 38.265 → 46.721 | 46.721 → 46.721 |
| mass-budget.json#/classes/P10000/descentWithoutNitrogen/cycleSavingPct | 16.6 → 14.0 | 14.0 → 14.0 |
| mass-budget.json#/classes/P10000/hullAreaM2 | 485575 → 351903 | 351903 → 411775 |
| mass-budget.json#/classes/P10000/requiredKgPerM2 | 20.594 → 28.417 | 28.417 → 24.285 |
| mass-budget.json#/classes/P10000/rightSized/credible/baseExShellExSundriesT | 6770.6 → 6586.03 | 6586.03 → 6706.58 |
| mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.74/0.264/diaM | 271 → 314 | 314 → 315 |
| mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.74/0.264/lenM | 1082 → 628 | 628 → 631 |
| mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.74/0.264/timesBaseline | 1.89 → 1.85 | 1.85 → 1.87 |
| mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.74/0.264/volumeM3 | 41491383 → 40601887 | 40601887 → 41100464 |
| mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.74/0.508/diaM | 362 → 417 | 417 → 420 |
| mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.74/0.508/lenM | 1448 → 835 | 835 → 841 |
| mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.74/0.508/timesBaseline | 4.52 → 4.33 | 4.33 → 4.43 |
| mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.74/0.508/volumeM3 | 99413997 → 95331244 | 95331244 → 97369762 |
| mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.85/0.264/diaM | 251 → 291 | 291 → 293 |
| mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.85/0.264/lenM | 1003 → 583 | 583 → 585 |
| mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.85/0.264/timesBaseline | 1.5 → 1.48 | 1.48 → 1.49 |
| mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.85/0.264/volumeM3 | 33067814 → 32479861 | 32479861 → 32824453 |
| mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.85/0.508/diaM | 310 → 358 | 358 → 360 |
| mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.85/0.508/lenM | 1239 → 717 | 717 → 721 |
| mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.85/0.508/timesBaseline | 2.83 → 2.75 | 2.75 → 2.79 |
| mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.85/0.508/volumeM3 | 62228487 → 60403166 | 60403166 → 61364304 |
| mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.85/0.750/diaM | 572 → 646 | 646 → 657 |
| mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.85/0.750/lenM | 2289 → 1293 | 1293 → 1314 |
| mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.85/0.750/timesBaseline | 17.84 → 16.1 | 16.1 → 16.89 |
| mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=0.85/0.750/volumeM3 | 392576873 → 354291877 | 354291877 → 371656262 |
| mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=1.0/0.264/diaM | 231 → 269 | 269 → 270 |
| mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=1.0/0.264/lenM | 925 → 538 | 538 → 539 |
| mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=1.0/0.264/timesBaseline | 1.18 → 1.16 | 1.16 → 1.17 |
| mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=1.0/0.264/volumeM3 | 25870630 → 25499369 | 25499369 → 25730156 |
| mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=1.0/0.508/diaM | 270 → 313 | 313 → 314 |
| mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=1.0/0.508/lenM | 1078 → 626 | 626 → 628 |
| mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=1.0/0.508/timesBaseline | 1.86 → 1.82 | 1.82 → 1.85 |
| mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=1.0/0.508/volumeM3 | 41017744 → 40146494 | 40146494 → 40635855 |
| mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=1.0/0.750/diaM | 358 → 412 | 412 → 415 |
| mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=1.0/0.750/lenM | 1430 → 825 | 825 → 830 |
| mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=1.0/0.750/timesBaseline | 4.35 → 4.18 | 4.18 → 4.27 |
| mass-budget.json#/classes/P10000/rightSized/credible/cellular/phi=1.0/0.750/volumeM3 | 95758327 → 91926777 | 91926777 → 93846930 |
| mass-budget.json#/classes/P10000/rightSized/credible/everythingButShellT | 10261.2 → 10048.9 | 10048.9 → 10187.6 |
| mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.264/diaM | 231 → 269 | 269 → 270 |
| mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.264/lenM | 925 → 538 | 538 → 539 |
| mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.264/timesBaseline | 1.18 → 1.16 | 1.16 → 1.17 |
| mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.264/volumeM3 | 25870630 → 25499369 | 25499369 → 25730156 |
| mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.350/diaM | 242 → 282 | 282 → 282 |
| mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.350/lenM | 969 → 563 | 563 → 565 |
| mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.350/timesBaseline | 1.35 → 1.33 | 1.33 → 1.34 |
| mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.350/volumeM3 | 29754666 → 29271392 | 29271392 → 29561454 |
| mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.508/diaM | 270 → 313 | 313 → 314 |
| mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.508/lenM | 1078 → 626 | 626 → 628 |
| mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.508/timesBaseline | 1.86 → 1.82 | 1.82 → 1.85 |
| mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.508/volumeM3 | 41017744 → 40146494 | 40146494 → 40635855 |
| mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.600/diaM | 293 → 339 | 339 → 341 |
| mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.600/lenM | 1171 → 678 | 678 → 682 |
| mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.600/timesBaseline | 2.39 → 2.33 | 2.33 → 2.36 |
| mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.600/volumeM3 | 52515130 → 51160365 | 51160365 → 51890977 |
| mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.750/diaM | 358 → 412 | 412 → 415 |
| mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.750/lenM | 1430 → 825 | 825 → 830 |
| mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.750/timesBaseline | 4.35 → 4.18 | 4.18 → 4.27 |
| mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.750/volumeM3 | 95758327 → 91926777 | 91926777 → 93846930 |
| mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.900/diaM | 600 → 675 | 675 → 687 |
| mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.900/lenM | 2398 → 1351 | 1351 → 1374 |
| mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.900/timesBaseline | 20.52 → 18.36 | 18.36 → 19.33 |
| mass-budget.json#/classes/P10000/rightSized/credible/hullThatCloses/0.900/volumeM3 | 451502886 → 403869466 | 403869466 → 425317491 |
| mass-budget.json#/classes/P10000/rightSized/credible/lines/1/driver | 485,575 m2 hull surface → 351,903 m2 hull surface | 351,903 m2 hull surface → 411,775 m2 hull surface |
| mass-budget.json#/classes/P10000/rightSized/credible/lines/1/tonnes | 977.62 → 708.49 | 708.49 → 829.04 |
| mass-budget.json#/classes/P10000/rightSized/credible/lines/15/tonnes | 3490.59 → 3462.9 | 3462.9 → 3480.99 |
| mass-budget.json#/classes/P10000/rightSized/credible/lines/3/driver | 137.61 MWh → 162.98 MWh | 162.98 MWh → 162.98 MWh |
| mass-budget.json#/classes/P10000/rightSized/credible/lines/3/tonnes | 458.69 → 543.25 | 543.25 → 543.25 |
| mass-budget.json#/classes/P10000/rightSized/credible/overBy | 2.68 → 2.65 | 2.65 → 2.67 |
| mass-budget.json#/classes/P10000/rightSized/credible/requiredShellKgPerM3 | 0.0875 → 0.0959 | 0.0959 → 0.0904 |
| mass-budget.json#/classes/P10000/rightSized/credible/shellBudgetLeftT | 1925.1 → 2109.6 | 2109.6 → 1989.1 |
| mass-budget.json#/classes/P10000/rightSized/credible/totalT | 26761.2 → 26548.9 | 26548.9 → 26687.6 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/baseExShellExSundriesT | 14718.35 → 14427.43 | 14427.43 → 14633.99 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.74/0.264/diaM | 319 → 368 | 368 → 371 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.74/0.264/lenM | 1275 → 736 | 736 → 741 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.74/0.264/timesBaseline | 3.08 → 2.97 | 2.97 → 3.03 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.74/0.264/volumeM3 | 67784415 → 65424344 | 65424344 → 66691136 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.74/0.508/diaM | 433 → 495 | 495 → 500 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.74/0.508/lenM | 1732 → 989 | 989 → 1001 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.74/0.508/timesBaseline | 7.73 → 7.22 | 7.22 → 7.46 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.74/0.508/volumeM3 | 169992673 → 158788417 | 158788417 → 164208465 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.85/0.264/diaM | 295 → 341 | 341 → 343 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.85/0.264/lenM | 1179 → 682 | 682 → 686 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.85/0.264/timesBaseline | 2.44 → 2.36 | 2.36 → 2.4 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.85/0.264/volumeM3 | 53575160 → 52019094 | 52019094 → 52887257 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.85/0.508/diaM | 367 → 422 | 422 → 426 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.85/0.508/lenM | 1468 → 844 | 844 → 851 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.85/0.508/timesBaseline | 4.71 → 4.48 | 4.48 → 4.6 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.85/0.508/volumeM3 | 103524890 → 98627904 | 98627904 → 101115005 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.85/0.750/diaM | 717 → 792 | 792 → 813 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.85/0.750/lenM | 2868 → 1584 | 1584 → 1626 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.85/0.750/timesBaseline | 35.08 → 29.64 | 29.64 → 32.02 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=0.85/0.750/volumeM3 | 771701743 → 651976614 | 651976614 → 704512559 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=1.0/0.264/diaM | 271 → 314 | 314 → 316 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=1.0/0.264/lenM | 1083 → 628 | 628 → 631 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=1.0/0.264/timesBaseline | 1.89 → 1.85 | 1.85 → 1.87 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=1.0/0.264/volumeM3 | 41590987 → 40607764 | 40607764 → 41184608 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=1.0/0.508/diaM | 317 → 367 | 367 → 369 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=1.0/0.508/lenM | 1270 → 733 | 733 → 738 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=1.0/0.508/timesBaseline | 3.04 → 2.94 | 2.94 → 3.0 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=1.0/0.508/volumeM3 | 66980471 → 64669257 | 64669257 → 65912064 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=1.0/0.750/diaM | 427 → 488 | 488 → 494 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=1.0/0.750/lenM | 1709 → 977 | 977 → 988 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=1.0/0.750/timesBaseline | 7.42 → 6.95 | 6.95 → 7.18 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/cellular/phi=1.0/0.750/volumeM3 | 163333972 → 152842201 | 152842201 → 157935107 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/everythingButShellT | 22766.0 → 22416.9 | 22416.9 → 22664.8 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.264/diaM | 271 → 314 | 314 → 316 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.264/lenM | 1083 → 628 | 628 → 631 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.264/timesBaseline | 1.89 → 1.85 | 1.85 → 1.87 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.264/volumeM3 | 41590987 → 40607764 | 40607764 → 41184608 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.350/diaM | 284 → 329 | 329 → 331 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.350/lenM | 1136 → 658 | 658 → 662 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.350/timesBaseline | 2.18 → 2.13 | 2.13 → 2.16 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.350/volumeM3 | 48039748 → 46760952 | 46760952 → 47489135 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.508/diaM | 317 → 367 | 367 → 369 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.508/lenM | 1270 → 733 | 733 → 738 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.508/timesBaseline | 3.04 → 2.94 | 2.94 → 3.0 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.508/volumeM3 | 66980471 → 64669257 | 64669257 → 65912064 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.600/diaM | 346 → 399 | 399 → 402 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.600/lenM | 1383 → 797 | 797 → 803 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.600/timesBaseline | 3.94 → 3.77 | 3.77 → 3.86 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.600/volumeM3 | 86655440 → 83041219 | 83041219 → 84916398 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.750/diaM | 427 → 488 | 488 → 494 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.750/lenM | 1709 → 977 | 977 → 988 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.750/timesBaseline | 7.42 → 6.95 | 6.95 → 7.18 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.750/volumeM3 | 163333972 → 152842201 | 152842201 → 157935107 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.900/diaM | 756 → 832 | 832 → 855 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.900/lenM | 3025 → 1663 | 1663 → 1710 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.900/timesBaseline | 41.18 → 34.28 | 34.28 → 37.28 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/hullThatCloses/0.900/volumeM3 | 905962550 → 754154707 | 754154707 → 820222816 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/lines/1/driver | 485,575 m2 hull surface → 351,903 m2 hull surface | 351,903 m2 hull surface → 411,775 m2 hull surface |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/lines/1/tonnes | 1675.23 → 1214.06 | 1214.06 → 1420.62 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/lines/15/tonnes | 8047.67 → 7989.49 | 7989.49 → 8030.8 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/lines/3/driver | 137.61 MWh → 162.98 MWh | 162.98 MWh → 162.98 MWh |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/lines/3/tonnes | 923.54 → 1093.79 | 1093.79 → 1093.79 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/overBy | 4.83 → 4.79 | 4.79 → 4.82 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/shellBudgetLeftT | -6385.0 → -6094.1 | -6094.1 → -6300.7 |
| mass-budget.json#/classes/P10000/rightSized/demonstrated/totalT | 48286.0 → 47936.9 | 47936.9 → 48184.8 |
| mass-budget.json#/classes/P10000/rightSized/floor/baseExShellExSundriesT | 2863.36 → 2887.19 | 2887.19 → 2899.24 |
| mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.74/0.264/diaM | 242 → 283 | 283 → 283 |
| mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.74/0.264/lenM | 968 → 566 | 566 → 566 |
| mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.74/0.264/volumeM3 | 29688613 → 29733244 | 29733244 → 29770046 |
| mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.74/0.508/diaM | 317 → 370 | 370 → 370 |
| mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.74/0.508/lenM | 1267 → 740 | 740 → 741 |
| mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.74/0.508/volumeM3 | 66569935 → 66538977 | 66538977 → 66679573 |
| mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.85/0.264/diaM | 225 → 264 | 264 → 264 |
| mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.85/0.264/lenM | 901 → 527 | 527 → 527 |
| mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.85/0.264/volumeM3 | 23954169 → 23999043 | 23999043 → 24024804 |
| mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.85/0.508/diaM | 275 → 321 | 321 → 321 |
| mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.85/0.508/lenM | 1098 → 642 | 642 → 642 |
| mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.85/0.508/timesBaseline | 1.97 → 1.97 | 1.97 → 1.98 |
| mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.85/0.508/volumeM3 | 43357573 → 43388284 | 43388284 → 43457314 |
| mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.85/0.750/diaM | 469 → 547 | 547 → 548 |
| mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.85/0.750/lenM | 1877 → 1095 | 1095 → 1097 |
| mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.85/0.750/timesBaseline | 9.84 → 9.78 | 9.78 → 9.82 |
| mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=0.85/0.750/volumeM3 | 216429913 → 215128763 | 215128763 → 216116487 |
| mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=1.0/0.264/diaM | 208 → 244 | 244 → 244 |
| mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=1.0/0.264/lenM | 834 → 488 | 488 → 488 |
| mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=1.0/0.264/volumeM3 | 18957753 → 18999865 | 18999865 → 19017325 |
| mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=1.0/0.508/diaM | 241 → 282 | 282 → 282 |
| mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=1.0/0.508/lenM | 965 → 564 | 564 → 564 |
| mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=1.0/0.508/timesBaseline | 1.33 → 1.34 | 1.34 → 1.34 |
| mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=1.0/0.508/volumeM3 | 29369201 → 29413937 | 29413937 → 29450083 |
| mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=1.0/0.750/diaM | 313 → 366 | 366 → 366 |
| mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=1.0/0.750/lenM | 1253 → 732 | 732 → 733 |
| mass-budget.json#/classes/P10000/rightSized/floor/cellular/phi=1.0/0.750/volumeM3 | 64351939 → 64328779 | 64328779 → 64461694 |
| mass-budget.json#/classes/P10000/rightSized/floor/everythingButShellT | 4267.3 → 4293.5 | 4293.5 → 4306.8 |
| mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.264/diaM | 208 → 244 | 244 → 244 |
| mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.264/lenM | 834 → 488 | 488 → 488 |
| mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.264/volumeM3 | 18957753 → 18999865 | 18999865 → 19017325 |
| mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.350/diaM | 218 → 255 | 255 → 255 |
| mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.350/lenM | 872 → 510 | 510 → 510 |
| mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.350/timesBaseline | 0.98 → 0.99 | 0.99 → 0.99 |
| mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.350/volumeM3 | 21665860 → 21709826 | 21709826 → 21731627 |
| mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.508/diaM | 241 → 282 | 282 → 282 |
| mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.508/lenM | 965 → 564 | 564 → 564 |
| mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.508/timesBaseline | 1.33 → 1.34 | 1.34 → 1.34 |
| mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.508/volumeM3 | 29369201 → 29413937 | 29413937 → 29450083 |
| mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.600/diaM | 261 → 305 | 305 → 305 |
| mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.600/lenM | 1042 → 609 | 609 → 610 |
| mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.600/timesBaseline | 1.68 → 1.68 | 1.68 → 1.69 |
| mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.600/volumeM3 | 37028737 → 37068124 | 37068124 → 37121244 |
| mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.750/diaM | 313 → 366 | 366 → 366 |
| mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.750/lenM | 1253 → 732 | 732 → 733 |
| mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.750/volumeM3 | 64351939 → 64328779 | 64328779 → 64461694 |
| mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.900/diaM | 487 → 568 | 568 → 569 |
| mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.900/lenM | 1948 → 1136 | 1136 → 1138 |
| mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.900/timesBaseline | 11.0 → 10.93 | 10.93 → 10.98 |
| mass-budget.json#/classes/P10000/rightSized/floor/hullThatCloses/0.900/volumeM3 | 242030733 → 240387737 | 240387737 → 241575171 |
| mass-budget.json#/classes/P10000/rightSized/floor/lines/1/driver | 485,575 m2 hull surface → 351,903 m2 hull surface | 351,903 m2 hull surface → 411,775 m2 hull surface |
| mass-budget.json#/classes/P10000/rightSized/floor/lines/1/tonnes | 97.76 → 70.85 | 70.85 → 82.9 |
| mass-budget.json#/classes/P10000/rightSized/floor/lines/15/tonnes | 1403.94 → 1406.32 | 1406.32 → 1407.52 |
| mass-budget.json#/classes/P10000/rightSized/floor/lines/3/driver | 137.61 MWh → 162.98 MWh | 162.98 MWh → 162.98 MWh |
| mass-budget.json#/classes/P10000/rightSized/floor/lines/3/tonnes | 275.21 → 325.95 | 325.95 → 325.95 |
| mass-budget.json#/classes/P10000/rightSized/floor/overBy | 1.54 → 1.55 | 1.55 → 1.55 |
| mass-budget.json#/classes/P10000/rightSized/floor/requiredShellKgPerM3 | 0.2831 → 0.282 | 0.282 → 0.2814 |
| mass-budget.json#/classes/P10000/rightSized/floor/shellBudgetLeftT | 6227.5 → 6203.7 | 6203.7 → 6191.7 |
| mass-budget.json#/classes/P10000/rightSized/floor/totalT | 15443.3 → 15469.5 | 15469.5 → 15482.8 |

The omitted strings below were compared at `467867ca8685f2bd168f553710f32adab3d0f78b` and `ff8a2e44544773b883132ace7524960888c1bd97`. The companion JSON names `84717cdb2b1c3256787cbdb2ab2fa4f0e2195808` as its latest input snapshot, before the refreshed artifacts were committed; the latter comparison uses the commit that first added this audit. The earlier numeric-leaf table omitted text containing numbers and two reworded vacuum-cell notes.

| Printed at | Earlier text | Later text |
|---|---|---|
| research/analysis/mass-budget.json#/classes/P100/cases/credible/lines/1/driver | 22,592 m2 hull surface | 19,007 m2 hull surface |
| research/analysis/mass-budget.json#/classes/P100/cases/demonstrated/lines/1/driver | 22,592 m2 hull surface | 19,007 m2 hull surface |
| research/analysis/mass-budget.json#/classes/P100/cases/floor/lines/1/driver | 22,592 m2 hull surface | 19,007 m2 hull surface |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/lines/1/driver | 22,592 m2 hull surface | 19,007 m2 hull surface |
| research/analysis/mass-budget.json#/classes/P100/rightSized/credible/lines/3/driver | 3.76 MWh | 4.17 MWh |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/lines/1/driver | 22,592 m2 hull surface | 19,007 m2 hull surface |
| research/analysis/mass-budget.json#/classes/P100/rightSized/demonstrated/lines/3/driver | 3.76 MWh | 4.17 MWh |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/lines/1/driver | 22,592 m2 hull surface | 19,007 m2 hull surface |
| research/analysis/mass-budget.json#/classes/P100/rightSized/floor/lines/3/driver | 3.76 MWh | 4.17 MWh |
| research/analysis/mass-budget.json#/classes/P1000/cases/credible/lines/1/driver | 104,349 m2 hull surface | 88,976 m2 hull surface |
| research/analysis/mass-budget.json#/classes/P1000/cases/demonstrated/lines/1/driver | 104,349 m2 hull surface | 88,976 m2 hull surface |
| research/analysis/mass-budget.json#/classes/P1000/cases/floor/lines/1/driver | 104,349 m2 hull surface | 88,976 m2 hull surface |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/lines/1/driver | 104,349 m2 hull surface | 88,976 m2 hull surface |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/credible/lines/3/driver | 22.20 MWh | 25.36 MWh |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/lines/1/driver | 104,349 m2 hull surface | 88,976 m2 hull surface |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/demonstrated/lines/3/driver | 22.20 MWh | 25.36 MWh |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/lines/1/driver | 104,349 m2 hull surface | 88,976 m2 hull surface |
| research/analysis/mass-budget.json#/classes/P1000/rightSized/floor/lines/3/driver | 22.20 MWh | 25.36 MWh |
| research/analysis/mass-budget.json#/classes/P10000/cases/credible/lines/1/driver | 485,575 m2 hull surface | 411,775 m2 hull surface |
| research/analysis/mass-budget.json#/classes/P10000/cases/demonstrated/lines/1/driver | 485,575 m2 hull surface | 411,775 m2 hull surface |
| research/analysis/mass-budget.json#/classes/P10000/cases/floor/lines/1/driver | 485,575 m2 hull surface | 411,775 m2 hull surface |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/lines/1/driver | 485,575 m2 hull surface | 411,775 m2 hull surface |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/credible/lines/3/driver | 137.61 MWh | 162.98 MWh |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/lines/1/driver | 485,575 m2 hull surface | 411,775 m2 hull surface |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/demonstrated/lines/3/driver | 137.61 MWh | 162.98 MWh |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/lines/1/driver | 485,575 m2 hull surface | 411,775 m2 hull surface |
| research/analysis/mass-budget.json#/classes/P10000/rightSized/floor/lines/3/driver | 137.61 MWh | 162.98 MWh |
| research/analysis/vacuum-cell.json#/designPoint/filmIsAChoiceAndTheModelPickedOneIncoherently/permeationNote | An interior partition has vacuum on BOTH sides, so there is no partial-pressure gradient and no permeation driving force at all. A permeation barrier is only needed where vacuum meets atmosphere — the outer envelope, which is 22,592 m2 against 660,000 m2 of interior wall at 1 m cells, a factor of 29. | An interior partition has vacuum on BOTH sides, so there is no partial-pressure gradient and no permeation driving force at all. A permeation barrier is only needed where vacuum meets atmosphere — the dated 190 x 47 m spheroid reference envelope, 22,592 m2 against 660,000 m2 of interior wall at 1 m cells, a factor of 29. |
| research/analysis/vacuum-cell.json#/gradedPressure/band/geometryNote | 5% of this hull behind 22,592 m2 of envelope is a band about half a metre deep, so its ten steps are sub-cell-scale layers — which is the seal-at-every-scale doctrine anyway, and film mass is span-proportional so thinner layers cost no more. | 5% of the dated 190 x 47 m spheroid reference behind 22,592 m2 of envelope is a band about half a metre deep, so its ten steps are sub-cell-scale layers — which is the seal-at-every-scale doctrine anyway, and film mass is span-proportional so thinner layers cost no more. |
