/* GENERATED — do not edit. `python3 tools/gen_node_families.py` rewrites this file.
 *
 * The 51 printed joints of the article, grouped into the five families the manifest's own
 * (role, arms) histogram produces, with every field taken from
 * research/geometry/nodes/manifest.json — the meshes that were actually written — and the
 * arm composition taken from tools/gen_nodes.py::article_graph().
 *
 * The browser cannot read the manifest off disk, and five families times a dozen fields is
 * not a number you hand-copy. tools/check_explorer.py regroups the manifest and fails if
 * this file has drifted from it, which is the same freshness gate check_figures_fresh runs
 * for figures, applied to geometry.
 */

export const NODES = {
  "families": {
    "lattice-12": {
      "key": "lattice-12",
      "name": "the cell centre",
      "role": "lattice",
      "arms": 12,
      "count": 1,
      "memberEnds": 12,
      "memberEndPct": 2.8,
      "composition": {
        "octet": 12
      },
      "lands": 0,
      "armToLandDeg": null,
      "minArmAngleDeg": 60.0,
      "slotBaseMm": 12.26,
      "massGMin": 14.9,
      "massGMax": 14.9,
      "massGSum": 14.9,
      "massPct": 2.1,
      "volumeMm3Min": 14061,
      "volumeMm3Max": 14061,
      "overhangFracMin": 0.148,
      "overhangFracMax": 0.148,
      "trianglesMin": 25264,
      "trianglesMax": 25264,
      "nonManifoldEdgesMin": 292,
      "nonManifoldEdgesMax": 292,
      "repFile": "node_09_lattice.stl",
      "repU": [
        0,
        0,
        0
      ],
      "repUText": "(0, 0, 0)",
      "repMassG": 14.9
    },
    "lattice-11": {
      "key": "lattice-11",
      "name": "the workhorse",
      "role": "lattice",
      "arms": 11,
      "count": 12,
      "memberEnds": 132,
      "memberEndPct": 30.6,
      "composition": {
        "octet": 7,
        "tie": 4
      },
      "lands": 0,
      "armToLandDeg": null,
      "minArmAngleDeg": 43.6,
      "slotBaseMm": 16.91,
      "massGMin": 15.16,
      "massGMax": 19.71,
      "massGSum": 196.28,
      "massPct": 27.4,
      "volumeMm3Min": 14306,
      "volumeMm3Max": 18591,
      "overhangFracMin": 0.122,
      "overhangFracMax": 0.164,
      "trianglesMin": 29276,
      "trianglesMax": 40820,
      "nonManifoldEdgesMin": 184,
      "nonManifoldEdgesMax": 230,
      "repFile": "node_07_lattice.stl",
      "repU": [
        0,
        -1,
        1
      ],
      "repUText": "(0, -1, 1)",
      "repMassG": 15.92
    },
    "lattice-8": {
      "key": "lattice-8",
      "name": "the square-face centre",
      "role": "lattice",
      "arms": 8,
      "count": 6,
      "memberEnds": 48,
      "memberEndPct": 11.1,
      "composition": {
        "octet": 4,
        "tie": 4
      },
      "lands": 1,
      "armToLandDeg": 45.0,
      "minArmAngleDeg": 42.7,
      "slotBaseMm": 17.26,
      "massGMin": 11.5,
      "massGMax": 16.81,
      "massGSum": 81.21,
      "massPct": 11.4,
      "volumeMm3Min": 10846,
      "volumeMm3Max": 15858,
      "overhangFracMin": 0.128,
      "overhangFracMax": 0.153,
      "trianglesMin": 21060,
      "trianglesMax": 33728,
      "nonManifoldEdgesMin": 58,
      "nonManifoldEdgesMax": 72,
      "repFile": "node_10_lattice.stl",
      "repU": [
        0,
        0,
        2
      ],
      "repUText": "(0, 0, 2)",
      "repMassG": 13.04
    },
    "rimVertex-7": {
      "key": "rimVertex-7",
      "name": "the corner",
      "role": "rimVertex",
      "arms": 7,
      "count": 24,
      "memberEnds": 168,
      "memberEndPct": 38.9,
      "composition": {
        "rim": 3,
        "spoke": 2,
        "tie": 2
      },
      "lands": 3,
      "armToLandDeg": null,
      "minArmAngleDeg": 43.0,
      "slotBaseMm": 19.84,
      "massGMin": 13.42,
      "massGMax": 13.42,
      "massGSum": 322.08,
      "massPct": 45.0,
      "volumeMm3Min": 12657,
      "volumeMm3Max": 12663,
      "overhangFracMin": 0.151,
      "overhangFracMax": 0.169,
      "trianglesMin": 26848,
      "trianglesMax": 26996,
      "nonManifoldEdgesMin": 119,
      "nonManifoldEdgesMax": 127,
      "repFile": "node_37_rimVertex.stl",
      "repU": [
        0,
        1,
        -2
      ],
      "repUText": "(0, 1, -2)",
      "repMassG": 13.42
    },
    "hexHub-9": {
      "key": "hexHub-9",
      "name": "the hexagon hub",
      "role": "hexHub",
      "arms": 9,
      "count": 8,
      "memberEnds": 72,
      "memberEndPct": 16.7,
      "composition": {
        "spoke": 6,
        "tie": 3
      },
      "lands": 1,
      "armToLandDeg": 54.74,
      "minArmAngleDeg": 43.2,
      "slotBaseMm": 17.04,
      "massGMin": 12.59,
      "massGMax": 12.59,
      "massGSum": 100.72,
      "massPct": 14.1,
      "volumeMm3Min": 11876,
      "volumeMm3Max": 11881,
      "overhangFracMin": 0.123,
      "overhangFracMax": 0.144,
      "trianglesMin": 22752,
      "trianglesMax": 22804,
      "nonManifoldEdgesMin": 124,
      "nonManifoldEdgesMax": 128,
      "repFile": "node_47_hexHub.stl",
      "repU": [
        1,
        -1,
        -1
      ],
      "repUText": "(1, -1, -1)",
      "repMassG": 12.59
    }
  },
  "order": [
    "lattice-12",
    "lattice-11",
    "lattice-8",
    "rimVertex-7",
    "hexHub-9"
  ],
  "assembly": [
    {
      "a": [
        -1,
        -1,
        0
      ],
      "b": [
        0,
        0,
        0
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        -1,
        0,
        -1
      ],
      "b": [
        0,
        0,
        0
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        -1,
        0,
        1
      ],
      "b": [
        0,
        0,
        0
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        -1,
        1,
        0
      ],
      "b": [
        0,
        0,
        0
      ],
      "fam": "octet",
      "closing": false
    },
    {
      "a": [
        0,
        -1,
        -1
      ],
      "b": [
        0,
        0,
        0
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        0,
        -1,
        1
      ],
      "b": [
        0,
        0,
        0
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        0,
        0,
        0
      ],
      "b": [
        0,
        1,
        -1
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        0,
        0,
        0
      ],
      "b": [
        0,
        1,
        1
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        0,
        0,
        0
      ],
      "b": [
        1,
        -1,
        0
      ],
      "fam": "octet",
      "closing": false
    },
    {
      "a": [
        0,
        0,
        0
      ],
      "b": [
        1,
        0,
        -1
      ],
      "fam": "octet",
      "closing": false
    },
    {
      "a": [
        0,
        0,
        0
      ],
      "b": [
        1,
        0,
        1
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        0,
        0,
        0
      ],
      "b": [
        1,
        1,
        0
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        -1,
        -1,
        0
      ],
      "b": [
        -1,
        0,
        -1
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        -1,
        -1,
        0
      ],
      "b": [
        -1,
        0,
        1
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        -1,
        -1,
        0
      ],
      "b": [
        0,
        -1,
        -1
      ],
      "fam": "octet",
      "closing": false
    },
    {
      "a": [
        -1,
        -1,
        0
      ],
      "b": [
        0,
        -1,
        1
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        -1,
        0,
        -1
      ],
      "b": [
        -1,
        1,
        0
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        -1,
        0,
        -1
      ],
      "b": [
        0,
        -1,
        -1
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        -1,
        0,
        -1
      ],
      "b": [
        0,
        1,
        -1
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        -1,
        0,
        1
      ],
      "b": [
        -1,
        1,
        0
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        -1,
        0,
        1
      ],
      "b": [
        0,
        -1,
        1
      ],
      "fam": "octet",
      "closing": false
    },
    {
      "a": [
        -1,
        0,
        1
      ],
      "b": [
        0,
        1,
        1
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        -1,
        1,
        0
      ],
      "b": [
        0,
        1,
        -1
      ],
      "fam": "octet",
      "closing": false
    },
    {
      "a": [
        -1,
        1,
        0
      ],
      "b": [
        0,
        1,
        1
      ],
      "fam": "octet",
      "closing": false
    },
    {
      "a": [
        0,
        -1,
        -1
      ],
      "b": [
        1,
        -1,
        0
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        0,
        -1,
        -1
      ],
      "b": [
        1,
        0,
        -1
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        0,
        -1,
        1
      ],
      "b": [
        1,
        -1,
        0
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        0,
        -1,
        1
      ],
      "b": [
        1,
        0,
        1
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        0,
        1,
        -1
      ],
      "b": [
        1,
        0,
        -1
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        0,
        1,
        -1
      ],
      "b": [
        1,
        1,
        0
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        0,
        1,
        1
      ],
      "b": [
        1,
        0,
        1
      ],
      "fam": "octet",
      "closing": false
    },
    {
      "a": [
        0,
        1,
        1
      ],
      "b": [
        1,
        1,
        0
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        1,
        -1,
        0
      ],
      "b": [
        1,
        0,
        -1
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        1,
        -1,
        0
      ],
      "b": [
        1,
        0,
        1
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        1,
        0,
        -1
      ],
      "b": [
        1,
        1,
        0
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        1,
        0,
        1
      ],
      "b": [
        1,
        1,
        0
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        -1,
        -1,
        -1
      ],
      "b": [
        -1,
        -1,
        0
      ],
      "fam": "tie",
      "closing": false
    },
    {
      "a": [
        -1,
        -1,
        -1
      ],
      "b": [
        -1,
        0,
        -1
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        -1,
        -1,
        -1
      ],
      "b": [
        0,
        -1,
        -1
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        -1,
        -1,
        1
      ],
      "b": [
        -1,
        -1,
        0
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        -1,
        -1,
        1
      ],
      "b": [
        -1,
        0,
        1
      ],
      "fam": "tie",
      "closing": false
    },
    {
      "a": [
        -1,
        -1,
        1
      ],
      "b": [
        0,
        -1,
        1
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        -1,
        1,
        -1
      ],
      "b": [
        -1,
        0,
        -1
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        -1,
        1,
        -1
      ],
      "b": [
        -1,
        1,
        0
      ],
      "fam": "tie",
      "closing": false
    },
    {
      "a": [
        -1,
        1,
        -1
      ],
      "b": [
        0,
        1,
        -1
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        -1,
        1,
        1
      ],
      "b": [
        -1,
        0,
        1
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        -1,
        1,
        1
      ],
      "b": [
        -1,
        1,
        0
      ],
      "fam": "tie",
      "closing": false
    },
    {
      "a": [
        -1,
        1,
        1
      ],
      "b": [
        0,
        1,
        1
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        1,
        -1,
        -1
      ],
      "b": [
        0,
        -1,
        -1
      ],
      "fam": "tie",
      "closing": false
    },
    {
      "a": [
        1,
        -1,
        -1
      ],
      "b": [
        1,
        -1,
        0
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        1,
        -1,
        -1
      ],
      "b": [
        1,
        0,
        -1
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        1,
        -1,
        1
      ],
      "b": [
        0,
        -1,
        1
      ],
      "fam": "tie",
      "closing": false
    },
    {
      "a": [
        1,
        -1,
        1
      ],
      "b": [
        1,
        -1,
        0
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        1,
        -1,
        1
      ],
      "b": [
        1,
        0,
        1
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        1,
        1,
        -1
      ],
      "b": [
        0,
        1,
        -1
      ],
      "fam": "tie",
      "closing": false
    },
    {
      "a": [
        1,
        1,
        -1
      ],
      "b": [
        1,
        0,
        -1
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        1,
        1,
        -1
      ],
      "b": [
        1,
        1,
        0
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        1,
        1,
        1
      ],
      "b": [
        0,
        1,
        1
      ],
      "fam": "tie",
      "closing": false
    },
    {
      "a": [
        1,
        1,
        1
      ],
      "b": [
        1,
        0,
        1
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        1,
        1,
        1
      ],
      "b": [
        1,
        1,
        0
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        -2,
        0,
        0
      ],
      "b": [
        -1,
        -1,
        0
      ],
      "fam": "octet",
      "closing": false
    },
    {
      "a": [
        -2,
        0,
        0
      ],
      "b": [
        -1,
        0,
        -1
      ],
      "fam": "octet",
      "closing": false
    },
    {
      "a": [
        -2,
        0,
        0
      ],
      "b": [
        -1,
        0,
        1
      ],
      "fam": "octet",
      "closing": false
    },
    {
      "a": [
        -2,
        0,
        0
      ],
      "b": [
        -1,
        1,
        0
      ],
      "fam": "octet",
      "closing": false
    },
    {
      "a": [
        -1,
        -1,
        0
      ],
      "b": [
        0,
        -2,
        0
      ],
      "fam": "octet",
      "closing": false
    },
    {
      "a": [
        -1,
        0,
        -1
      ],
      "b": [
        0,
        0,
        -2
      ],
      "fam": "octet",
      "closing": false
    },
    {
      "a": [
        -1,
        0,
        1
      ],
      "b": [
        0,
        0,
        2
      ],
      "fam": "octet",
      "closing": false
    },
    {
      "a": [
        -1,
        1,
        0
      ],
      "b": [
        0,
        2,
        0
      ],
      "fam": "octet",
      "closing": false
    },
    {
      "a": [
        0,
        -2,
        0
      ],
      "b": [
        0,
        -1,
        -1
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        0,
        -2,
        0
      ],
      "b": [
        0,
        -1,
        1
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        0,
        -2,
        0
      ],
      "b": [
        1,
        -1,
        0
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        0,
        -1,
        -1
      ],
      "b": [
        0,
        0,
        -2
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        0,
        -1,
        1
      ],
      "b": [
        0,
        0,
        2
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        0,
        0,
        -2
      ],
      "b": [
        0,
        1,
        -1
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        0,
        0,
        -2
      ],
      "b": [
        1,
        0,
        -1
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        0,
        0,
        2
      ],
      "b": [
        0,
        1,
        1
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        0,
        0,
        2
      ],
      "b": [
        1,
        0,
        1
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        0,
        1,
        -1
      ],
      "b": [
        0,
        2,
        0
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        0,
        1,
        1
      ],
      "b": [
        0,
        2,
        0
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        0,
        2,
        0
      ],
      "b": [
        1,
        1,
        0
      ],
      "fam": "octet",
      "closing": false
    },
    {
      "a": [
        1,
        -1,
        0
      ],
      "b": [
        2,
        0,
        0
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        1,
        0,
        -1
      ],
      "b": [
        2,
        0,
        0
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        1,
        0,
        1
      ],
      "b": [
        2,
        0,
        0
      ],
      "fam": "octet",
      "closing": true
    },
    {
      "a": [
        1,
        1,
        0
      ],
      "b": [
        2,
        0,
        0
      ],
      "fam": "octet",
      "closing": false
    },
    {
      "a": [
        -2,
        -1,
        0
      ],
      "b": [
        -1,
        -1,
        0
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        -2,
        0,
        -1
      ],
      "b": [
        -1,
        0,
        -1
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        -2,
        0,
        1
      ],
      "b": [
        -1,
        0,
        1
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        -2,
        1,
        0
      ],
      "b": [
        -1,
        1,
        0
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        -1,
        -2,
        0
      ],
      "b": [
        -1,
        -1,
        0
      ],
      "fam": "tie",
      "closing": false
    },
    {
      "a": [
        -1,
        0,
        -2
      ],
      "b": [
        -1,
        0,
        -1
      ],
      "fam": "tie",
      "closing": false
    },
    {
      "a": [
        -1,
        0,
        2
      ],
      "b": [
        -1,
        0,
        1
      ],
      "fam": "tie",
      "closing": false
    },
    {
      "a": [
        -1,
        2,
        0
      ],
      "b": [
        -1,
        1,
        0
      ],
      "fam": "tie",
      "closing": false
    },
    {
      "a": [
        0,
        -2,
        -1
      ],
      "b": [
        0,
        -1,
        -1
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        0,
        -2,
        1
      ],
      "b": [
        0,
        -1,
        1
      ],
      "fam": "tie",
      "closing": false
    },
    {
      "a": [
        0,
        -1,
        -2
      ],
      "b": [
        0,
        -1,
        -1
      ],
      "fam": "tie",
      "closing": false
    },
    {
      "a": [
        0,
        -1,
        2
      ],
      "b": [
        0,
        -1,
        1
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        0,
        1,
        -2
      ],
      "b": [
        0,
        1,
        -1
      ],
      "fam": "tie",
      "closing": false
    },
    {
      "a": [
        0,
        1,
        2
      ],
      "b": [
        0,
        1,
        1
      ],
      "fam": "tie",
      "closing": false
    },
    {
      "a": [
        0,
        2,
        -1
      ],
      "b": [
        0,
        1,
        -1
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        0,
        2,
        1
      ],
      "b": [
        0,
        1,
        1
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        1,
        -2,
        0
      ],
      "b": [
        1,
        -1,
        0
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        1,
        0,
        -2
      ],
      "b": [
        1,
        0,
        -1
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        1,
        0,
        2
      ],
      "b": [
        1,
        0,
        1
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        1,
        2,
        0
      ],
      "b": [
        1,
        1,
        0
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        2,
        -1,
        0
      ],
      "b": [
        1,
        -1,
        0
      ],
      "fam": "tie",
      "closing": false
    },
    {
      "a": [
        2,
        0,
        -1
      ],
      "b": [
        1,
        0,
        -1
      ],
      "fam": "tie",
      "closing": false
    },
    {
      "a": [
        2,
        0,
        1
      ],
      "b": [
        1,
        0,
        1
      ],
      "fam": "tie",
      "closing": false
    },
    {
      "a": [
        2,
        1,
        0
      ],
      "b": [
        1,
        1,
        0
      ],
      "fam": "tie",
      "closing": false
    },
    {
      "a": [
        -1,
        -1,
        -1
      ],
      "b": [
        -2,
        -1,
        0
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        -1,
        -1,
        -1
      ],
      "b": [
        -2,
        0,
        -1
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        -1,
        -1,
        -1
      ],
      "b": [
        -1,
        -2,
        0
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        -1,
        -1,
        -1
      ],
      "b": [
        -1,
        0,
        -2
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        -1,
        -1,
        -1
      ],
      "b": [
        0,
        -2,
        -1
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        -1,
        -1,
        -1
      ],
      "b": [
        0,
        -1,
        -2
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        -1,
        -1,
        1
      ],
      "b": [
        -2,
        -1,
        0
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        -1,
        -1,
        1
      ],
      "b": [
        -2,
        0,
        1
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        -1,
        -1,
        1
      ],
      "b": [
        -1,
        -2,
        0
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        -1,
        -1,
        1
      ],
      "b": [
        -1,
        0,
        2
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        -1,
        -1,
        1
      ],
      "b": [
        0,
        -2,
        1
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        -1,
        -1,
        1
      ],
      "b": [
        0,
        -1,
        2
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        -1,
        1,
        -1
      ],
      "b": [
        -2,
        0,
        -1
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        -1,
        1,
        -1
      ],
      "b": [
        -2,
        1,
        0
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        -1,
        1,
        -1
      ],
      "b": [
        -1,
        0,
        -2
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        -1,
        1,
        -1
      ],
      "b": [
        -1,
        2,
        0
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        -1,
        1,
        -1
      ],
      "b": [
        0,
        1,
        -2
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        -1,
        1,
        -1
      ],
      "b": [
        0,
        2,
        -1
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        -1,
        1,
        1
      ],
      "b": [
        -2,
        0,
        1
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        -1,
        1,
        1
      ],
      "b": [
        -2,
        1,
        0
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        -1,
        1,
        1
      ],
      "b": [
        -1,
        0,
        2
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        -1,
        1,
        1
      ],
      "b": [
        -1,
        2,
        0
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        -1,
        1,
        1
      ],
      "b": [
        0,
        1,
        2
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        -1,
        1,
        1
      ],
      "b": [
        0,
        2,
        1
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        1,
        -1,
        -1
      ],
      "b": [
        0,
        -2,
        -1
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        1,
        -1,
        -1
      ],
      "b": [
        0,
        -1,
        -2
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        1,
        -1,
        -1
      ],
      "b": [
        1,
        -2,
        0
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        1,
        -1,
        -1
      ],
      "b": [
        1,
        0,
        -2
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        1,
        -1,
        -1
      ],
      "b": [
        2,
        -1,
        0
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        1,
        -1,
        -1
      ],
      "b": [
        2,
        0,
        -1
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        1,
        -1,
        1
      ],
      "b": [
        0,
        -2,
        1
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        1,
        -1,
        1
      ],
      "b": [
        0,
        -1,
        2
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        1,
        -1,
        1
      ],
      "b": [
        1,
        -2,
        0
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        1,
        -1,
        1
      ],
      "b": [
        1,
        0,
        2
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        1,
        -1,
        1
      ],
      "b": [
        2,
        -1,
        0
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        1,
        -1,
        1
      ],
      "b": [
        2,
        0,
        1
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        1,
        1,
        -1
      ],
      "b": [
        0,
        1,
        -2
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        1,
        1,
        -1
      ],
      "b": [
        0,
        2,
        -1
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        1,
        1,
        -1
      ],
      "b": [
        1,
        0,
        -2
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        1,
        1,
        -1
      ],
      "b": [
        1,
        2,
        0
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        1,
        1,
        -1
      ],
      "b": [
        2,
        0,
        -1
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        1,
        1,
        -1
      ],
      "b": [
        2,
        1,
        0
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        1,
        1,
        1
      ],
      "b": [
        0,
        1,
        2
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        1,
        1,
        1
      ],
      "b": [
        0,
        2,
        1
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        1,
        1,
        1
      ],
      "b": [
        1,
        0,
        2
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        1,
        1,
        1
      ],
      "b": [
        1,
        2,
        0
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        1,
        1,
        1
      ],
      "b": [
        2,
        0,
        1
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        1,
        1,
        1
      ],
      "b": [
        2,
        1,
        0
      ],
      "fam": "spoke",
      "closing": true
    },
    {
      "a": [
        -2,
        -1,
        0
      ],
      "b": [
        -2,
        0,
        0
      ],
      "fam": "tie",
      "closing": false
    },
    {
      "a": [
        -2,
        0,
        -1
      ],
      "b": [
        -2,
        0,
        0
      ],
      "fam": "tie",
      "closing": false
    },
    {
      "a": [
        -2,
        0,
        1
      ],
      "b": [
        -2,
        0,
        0
      ],
      "fam": "tie",
      "closing": false
    },
    {
      "a": [
        -2,
        1,
        0
      ],
      "b": [
        -2,
        0,
        0
      ],
      "fam": "tie",
      "closing": false
    },
    {
      "a": [
        -1,
        -2,
        0
      ],
      "b": [
        0,
        -2,
        0
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        -1,
        0,
        -2
      ],
      "b": [
        0,
        0,
        -2
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        -1,
        0,
        2
      ],
      "b": [
        0,
        0,
        2
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        -1,
        2,
        0
      ],
      "b": [
        0,
        2,
        0
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        0,
        -2,
        -1
      ],
      "b": [
        0,
        -2,
        0
      ],
      "fam": "tie",
      "closing": false
    },
    {
      "a": [
        0,
        -2,
        1
      ],
      "b": [
        0,
        -2,
        0
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        0,
        -1,
        -2
      ],
      "b": [
        0,
        0,
        -2
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        0,
        -1,
        2
      ],
      "b": [
        0,
        0,
        2
      ],
      "fam": "tie",
      "closing": false
    },
    {
      "a": [
        0,
        1,
        -2
      ],
      "b": [
        0,
        0,
        -2
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        0,
        1,
        2
      ],
      "b": [
        0,
        0,
        2
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        0,
        2,
        -1
      ],
      "b": [
        0,
        2,
        0
      ],
      "fam": "tie",
      "closing": false
    },
    {
      "a": [
        0,
        2,
        1
      ],
      "b": [
        0,
        2,
        0
      ],
      "fam": "tie",
      "closing": false
    },
    {
      "a": [
        1,
        -2,
        0
      ],
      "b": [
        0,
        -2,
        0
      ],
      "fam": "tie",
      "closing": false
    },
    {
      "a": [
        1,
        0,
        -2
      ],
      "b": [
        0,
        0,
        -2
      ],
      "fam": "tie",
      "closing": false
    },
    {
      "a": [
        1,
        0,
        2
      ],
      "b": [
        0,
        0,
        2
      ],
      "fam": "tie",
      "closing": false
    },
    {
      "a": [
        1,
        2,
        0
      ],
      "b": [
        0,
        2,
        0
      ],
      "fam": "tie",
      "closing": false
    },
    {
      "a": [
        2,
        -1,
        0
      ],
      "b": [
        2,
        0,
        0
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        2,
        0,
        -1
      ],
      "b": [
        2,
        0,
        0
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        2,
        0,
        1
      ],
      "b": [
        2,
        0,
        0
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        2,
        1,
        0
      ],
      "b": [
        2,
        0,
        0
      ],
      "fam": "tie",
      "closing": true
    },
    {
      "a": [
        -2,
        0,
        -1
      ],
      "b": [
        -2,
        -1,
        0
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        -2,
        0,
        1
      ],
      "b": [
        -2,
        -1,
        0
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        -2,
        1,
        0
      ],
      "b": [
        -2,
        0,
        -1
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        -2,
        1,
        0
      ],
      "b": [
        -2,
        0,
        1
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        -2,
        1,
        0
      ],
      "b": [
        -1,
        2,
        0
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        -1,
        -2,
        0
      ],
      "b": [
        -2,
        -1,
        0
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        -1,
        0,
        -2
      ],
      "b": [
        -2,
        0,
        -1
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        -1,
        0,
        -2
      ],
      "b": [
        0,
        1,
        -2
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        -1,
        0,
        2
      ],
      "b": [
        -2,
        0,
        1
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        -1,
        0,
        2
      ],
      "b": [
        0,
        -1,
        2
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        -1,
        0,
        2
      ],
      "b": [
        0,
        1,
        2
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        0,
        -2,
        -1
      ],
      "b": [
        -1,
        -2,
        0
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        0,
        -2,
        -1
      ],
      "b": [
        1,
        -2,
        0
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        0,
        -2,
        1
      ],
      "b": [
        -1,
        -2,
        0
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        0,
        -2,
        1
      ],
      "b": [
        0,
        -1,
        2
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        0,
        -2,
        1
      ],
      "b": [
        1,
        -2,
        0
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        0,
        -1,
        -2
      ],
      "b": [
        -1,
        0,
        -2
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        0,
        -1,
        -2
      ],
      "b": [
        0,
        -2,
        -1
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        0,
        -1,
        -2
      ],
      "b": [
        1,
        0,
        -2
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        0,
        -1,
        2
      ],
      "b": [
        1,
        0,
        2
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        0,
        1,
        2
      ],
      "b": [
        1,
        0,
        2
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        0,
        2,
        -1
      ],
      "b": [
        -1,
        2,
        0
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        0,
        2,
        -1
      ],
      "b": [
        0,
        1,
        -2
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        0,
        2,
        -1
      ],
      "b": [
        1,
        2,
        0
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        0,
        2,
        1
      ],
      "b": [
        -1,
        2,
        0
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        0,
        2,
        1
      ],
      "b": [
        0,
        1,
        2
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        0,
        2,
        1
      ],
      "b": [
        1,
        2,
        0
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        1,
        -2,
        0
      ],
      "b": [
        2,
        -1,
        0
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        1,
        0,
        -2
      ],
      "b": [
        0,
        1,
        -2
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        1,
        0,
        -2
      ],
      "b": [
        2,
        0,
        -1
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        2,
        0,
        -1
      ],
      "b": [
        2,
        -1,
        0
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        2,
        0,
        1
      ],
      "b": [
        1,
        0,
        2
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        2,
        0,
        1
      ],
      "b": [
        2,
        -1,
        0
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        2,
        1,
        0
      ],
      "b": [
        1,
        2,
        0
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        2,
        1,
        0
      ],
      "b": [
        2,
        0,
        -1
      ],
      "fam": "rim",
      "closing": true
    },
    {
      "a": [
        2,
        1,
        0
      ],
      "b": [
        2,
        0,
        1
      ],
      "fam": "rim",
      "closing": true
    }
  ],
  "cuts": {
    "order": [
      "mainLong",
      "mainLongDeep",
      "mainLongDeep2",
      "mainLongDeep3",
      "mainShort",
      "mainShortDeep",
      "mainShortDeep2",
      "rimLongDeep",
      "rimLong"
    ],
    "groups": {
      "mainLong": {
        "sku": "main",
        "lengthKey": "long",
        "deductMm": 36.88,
        "cutMm": 206.142,
        "trueMemberMm": 243.023,
        "count": 48,
        "kinds": {
          "spoke": 48
        },
        "closingCutMm": 205.742,
        "swingReliefMm": 0.2,
        "key": "mainLong",
        "name": "spoke",
        "kindsText": "48 spoke"
      },
      "mainLongDeep": {
        "sku": "main",
        "lengthKey": "long",
        "deductMm": 34.17,
        "cutMm": 211.183,
        "trueMemberMm": 245.354,
        "count": 24,
        "kinds": {
          "octet": 24
        },
        "closingCutMm": 210.883,
        "swingReliefMm": 0.15,
        "key": "mainLongDeep",
        "name": "octet",
        "kindsText": "24 octet"
      },
      "mainLongDeep2": {
        "sku": "main",
        "lengthKey": "long",
        "deductMm": 33.82,
        "cutMm": 216.846,
        "trueMemberMm": 250.669,
        "count": 24,
        "kinds": {
          "octet": 24
        },
        "closingCutMm": 216.546,
        "swingReliefMm": 0.15,
        "key": "mainLongDeep2",
        "name": "octet",
        "kindsText": "24 octet"
      },
      "mainLongDeep3": {
        "sku": "main",
        "lengthKey": "long",
        "deductMm": 29.17,
        "cutMm": 221.5,
        "trueMemberMm": 250.669,
        "count": 12,
        "kinds": {
          "octet": 12
        },
        "closingCutMm": 221.2,
        "swingReliefMm": 0.15,
        "key": "mainLongDeep3",
        "name": "octet",
        "kindsText": "12 octet"
      },
      "mainShort": {
        "sku": "main",
        "lengthKey": "short",
        "deductMm": 37.1,
        "cutMm": 134.376,
        "trueMemberMm": 171.479,
        "count": 24,
        "kinds": {
          "tie": 24
        },
        "closingCutMm": 133.876,
        "swingReliefMm": 0.25,
        "key": "mainShort",
        "name": "tie",
        "kindsText": "24 tie"
      },
      "mainShortDeep": {
        "sku": "main",
        "lengthKey": "short",
        "deductMm": 36.75,
        "cutMm": 129.77,
        "trueMemberMm": 166.525,
        "count": 24,
        "kinds": {
          "tie": 24
        },
        "closingCutMm": 129.27,
        "swingReliefMm": 0.25,
        "key": "mainShortDeep",
        "name": "tie",
        "kindsText": "24 tie"
      },
      "mainShortDeep2": {
        "sku": "main",
        "lengthKey": "short",
        "deductMm": 33.95,
        "cutMm": 139.025,
        "trueMemberMm": 172.973,
        "count": 24,
        "kinds": {
          "tie": 24
        },
        "closingCutMm": 138.525,
        "swingReliefMm": 0.25,
        "key": "mainShortDeep2",
        "name": "tie",
        "kindsText": "24 tie"
      },
      "rimLongDeep": {
        "sku": "rim",
        "lengthKey": "long",
        "deductMm": 39.68,
        "cutMm": 202.778,
        "trueMemberMm": 242.465,
        "count": 24,
        "kinds": {
          "rim": 24
        },
        "closingCutMm": 202.078,
        "swingReliefMm": 0.35,
        "key": "rimLongDeep",
        "name": "rim",
        "kindsText": "24 rim"
      },
      "rimLong": {
        "sku": "rim",
        "lengthKey": "long",
        "deductMm": 39.68,
        "cutMm": 203.877,
        "trueMemberMm": 243.564,
        "count": 12,
        "kinds": {
          "rim": 12
        },
        "closingCutMm": 203.177,
        "swingReliefMm": 0.35,
        "key": "rimLong",
        "name": "rim",
        "kindsText": "12 rim"
      }
    },
    "members": 216
  },
  "totals": {
    "nodes": 51,
    "families": 5,
    "members": 216,
    "memberEnds": 432,
    "landedNodes": 38,
    "lands": 86,
    "massG": 715.19,
    "manifestMassKg": 0.715,
    "graph": {
      "octet": 60,
      "rim": 36,
      "spoke": 48,
      "tie": 72
    },
    "res": 96
  },
  "joint": {
    "pipeOdMm": 10.0,
    "pipeIdMm": 8.0,
    "clearanceMm": 0.15,
    "stubMm": 20.0,
    "treeEndsMm": 20.0,
    "closingEndsMm": 2.0,
    "coreRMm": 8.0,
    "lipMm": 2.5,
    "shoulderMm": 2.0,
    "padRMm": 0.0,
    "ribHMm": 0.25,
    "ribs": 3,
    "perStrutDemandN": 3372.0,
    "glueAreaMm2": 113,
    "glueShearMPa": 29.82,
    "glueMarginAt10MPa": 0.3,
    "spigotSectionMm2": 35.8,
    "spigotStressMPa": 94.2,
    "slotOuterRMm": 5.15,
    "slotBaseMinMm": 12.26,
    "slotBaseMaxMm": 19.84,
    "slotBaseSpreadMm": 7.58,
    "collarReachMm": 10.5,
    "rimMemberEnds": 72,
    "halfPitchMm": 177.25,
    "voxelMm": 1.049,
    "ribHVoxels": 0.24,
    "clearanceVoxels": 0.14
  }
};

export const FAMILIES = NODES.families;
export const FAMILY_ORDER = NODES.order;
export const NODE_TOTALS = NODES.totals;
export const JOINT = NODES.joint;
export const CUT_GROUPS = NODES.cuts;
export const ASSEMBLY = NODES.assembly;
