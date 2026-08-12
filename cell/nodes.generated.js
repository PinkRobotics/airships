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
      "massGMin": 14.78,
      "massGMax": 14.78,
      "massGSum": 14.78,
      "massPct": 3.2,
      "volumeMm3Min": 13944,
      "volumeMm3Max": 13944,
      "overhangFracMin": 0.138,
      "overhangFracMax": 0.138,
      "trianglesMin": 33280,
      "trianglesMax": 33280,
      "nonManifoldEdgesMin": 74,
      "nonManifoldEdgesMax": 74,
      "repFile": "node_09_lattice.stl",
      "repU": [
        0,
        0,
        0
      ],
      "repUText": "(0, 0, 0)",
      "repMassG": 14.78
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
      "minArmAngleDeg": 45.0,
      "slotBaseMm": 16.38,
      "massGMin": 15.01,
      "massGMax": 19.51,
      "massGSum": 194.3,
      "massPct": 41.8,
      "volumeMm3Min": 14158,
      "volumeMm3Max": 18402,
      "overhangFracMin": 0.113,
      "overhangFracMax": 0.161,
      "trianglesMin": 38288,
      "trianglesMax": 53348,
      "nonManifoldEdgesMin": 55,
      "nonManifoldEdgesMax": 71,
      "repFile": "node_02_lattice.stl",
      "repU": [
        -1,
        0,
        -1
      ],
      "repUText": "(-1, 0, -1)",
      "repMassG": 15.76
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
      "minArmAngleDeg": 45.0,
      "slotBaseMm": 16.38,
      "massGMin": 7.98,
      "massGMax": 11.69,
      "massGSum": 55.26,
      "massPct": 11.9,
      "volumeMm3Min": 7531,
      "volumeMm3Max": 11031,
      "overhangFracMin": 0.122,
      "overhangFracMax": 0.143,
      "trianglesMin": 21972,
      "trianglesMax": 35044,
      "nonManifoldEdgesMin": 29,
      "nonManifoldEdgesMax": 39,
      "repFile": "node_10_lattice.stl",
      "repU": [
        0,
        0,
        2
      ],
      "repUText": "(0, 0, 2)",
      "repMassG": 8.71
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
      "minArmAngleDeg": 45.0,
      "slotBaseMm": 18.98,
      "massGMin": 5.45,
      "massGMax": 5.83,
      "massGSum": 135.35,
      "massPct": 29.1,
      "volumeMm3Min": 5140,
      "volumeMm3Max": 5500,
      "overhangFracMin": 0.125,
      "overhangFracMax": 0.159,
      "trianglesMin": 16712,
      "trianglesMax": 17524,
      "nonManifoldEdgesMin": 47,
      "nonManifoldEdgesMax": 48,
      "repFile": "node_22_rimVertex.stl",
      "repU": [
        2,
        1,
        0
      ],
      "repUText": "(2, 1, 0)",
      "repMassG": 5.82
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
      "minArmAngleDeg": 45.0,
      "slotBaseMm": 16.38,
      "massGMin": 8.14,
      "massGMax": 8.14,
      "massGSum": 65.12,
      "massPct": 14.0,
      "volumeMm3Min": 7675,
      "volumeMm3Max": 7679,
      "overhangFracMin": 0.201,
      "overhangFracMax": 0.203,
      "trianglesMin": 22192,
      "trianglesMax": 22232,
      "nonManifoldEdgesMin": 63,
      "nonManifoldEdgesMax": 66,
      "repFile": "node_47_hexHub.stl",
      "repU": [
        1,
        -1,
        -1
      ],
      "repUText": "(1, -1, -1)",
      "repMassG": 8.14
    }
  },
  "order": [
    "lattice-12",
    "lattice-11",
    "lattice-8",
    "rimVertex-7",
    "hexHub-9"
  ],
  "cuts": {
    "order": [
      "mainLongDeep",
      "mainLong",
      "mainLongDeep2",
      "mainShort",
      "mainShortDeep",
      "rimLong"
    ],
    "groups": {
      "mainLongDeep": {
        "sku": "main",
        "lengthKey": "long",
        "deductMm": 32.76,
        "count": 48,
        "kinds": {
          "octet": 48
        },
        "key": "mainLongDeep",
        "name": "octet, into the centre",
        "kindsText": "48 octet"
      },
      "mainLong": {
        "sku": "main",
        "lengthKey": "long",
        "deductMm": 35.36,
        "count": 48,
        "kinds": {
          "spoke": 48
        },
        "key": "mainLong",
        "name": "spoke",
        "kindsText": "48 spoke"
      },
      "mainLongDeep2": {
        "sku": "main",
        "lengthKey": "long",
        "deductMm": 28.64,
        "count": 12,
        "kinds": {
          "octet": 12
        },
        "key": "mainLongDeep2",
        "name": "octet, into the centre",
        "kindsText": "12 octet"
      },
      "mainShort": {
        "sku": "main",
        "lengthKey": "short",
        "deductMm": 35.36,
        "count": 48,
        "kinds": {
          "tie": 48
        },
        "key": "mainShort",
        "name": "tie",
        "kindsText": "48 tie"
      },
      "mainShortDeep": {
        "sku": "main",
        "lengthKey": "short",
        "deductMm": 32.76,
        "count": 24,
        "kinds": {
          "tie": 24
        },
        "key": "mainShortDeep",
        "name": "tie, into the centre",
        "kindsText": "24 tie"
      },
      "rimLong": {
        "sku": "rim",
        "lengthKey": "long",
        "deductMm": 37.96,
        "count": 36,
        "kinds": {
          "rim": 36
        },
        "key": "rimLong",
        "name": "rim",
        "kindsText": "36 rim"
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
    "massG": 464.81,
    "manifestMassKg": 0.465,
    "graph": {
      "octet": 60,
      "rim": 36,
      "spoke": 48,
      "tie": 72
    },
    "res": 112
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
    "slotBaseMaxMm": 18.98,
    "slotBaseSpreadMm": 6.72,
    "collarReachMm": 10.5,
    "rimMemberEnds": 72,
    "halfPitchMm": 177.25,
    "voxelMm": 0.883,
    "ribHVoxels": 0.28,
    "clearanceVoxels": 0.17
  }
};

export const FAMILIES = NODES.families;
export const FAMILY_ORDER = NODES.order;
export const NODE_TOTALS = NODES.totals;
export const JOINT = NODES.joint;
export const CUT_GROUPS = NODES.cuts;
