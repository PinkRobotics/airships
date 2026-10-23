#!/usr/bin/env python3
"""MAINLINE-013: build cores.json from the four sourcing files, applying the curation stated below and nothing else.

Inputs (one level, named): <workspace>/.ship/work/sources/{metal-lattice,ceramic-carbon-lattice,aerogel,catalog}.json,
each written by a sourcing sub-worker of this seat under the rule "every value from a page actually opened, every DOI
checked against Crossref". This script copies their values; it never edits a number. Curation:
  - a record enters the evaluated table when it carries a density and at least one of Ec, Gc, compressive strength;
    the rest are listed under not_evaluated with the reason;
  - wrinkle form: CR-1457 honeycomb (eq 2.2-14) for honeycomb architectures, continuum (eq 2.2-5) for every other;
  - Gc: the sourced value when one exists (honeycomb: the smaller of L and W, the one MAINLINE-007/007b compared);
    otherwise G_rule "isotropic_nu0", Gc = Ec/2, the optimistic isotropic bound (COMMON.md: optimistic estimates);
  - honeycomb cell size (for the dimpling column only) parsed from a fraction-of-an-inch cell in the product name;
  - every sourced value is tagged QUESTIONABLE; the record's own MEASURED/PROJECTION status is kept;
  - curator overrides, each with its reason, are listed in OVERRIDES and applied by core_id.
Run: python3 -I build_cores.py
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCES = os.path.abspath(os.path.join(HERE, "..", "..", "sources"))
FAMILIES = ["metal-lattice", "ceramic-carbon-lattice", "aerogel", "catalog"]

DERIVATION_RULES = {
    "isotropic_nu0": {"G_over_E": 0.5,
                      "name": "isotropic elasticity G = E/(2(1+nu)) at nu = 0: the largest G an isotropic core with "
                              "nu >= 0 can have, the optimistic bound (QUESTIONABLE)"},
}
SENSITIVITY_NOTE = ("At nu = 1/3 instead, G = 3E/8: Gc falls by 0.75 and the EcGc product by 0.75. No margin in this "
                    "card is near enough to 1 for that to change a verdict unless the RESULTS say so.")

# curator overrides: core_id -> (fields to set, reason). Filled after reading each record; empty means none applied.
OVERRIDES = {
    "hexcel-a1-23-19": ({"cell_size_m": 0.019}, "cell 19 mm from the designation type-density-cell"),
    "hexcel-a1-24-6": ({"cell_size_m": 0.006}, "cell 6 mm from the designation type-density-cell"),
    "ec-eca-i-6.4-24": ({"cell_size_m": 0.0064}, "cell 6.4 mm from the designation"),
    "ec-eca-19.2-24": ({"cell_size_m": 0.0192}, "cell 19.2 mm from the designation"),
    "ec-ecm-3003-19.2-29": ({"cell_size_m": 0.0192}, "cell 19.2 mm from the designation"),
}
# Kashani 2019 tension rows: the paper states tension and compression moduli agree per sample, so the tensile modulus
# stands in for Ec (named here); the tensile strength is NOT a compressive strength and goes to the notes only.
TENSION_AS_EC = ("kashani2019-npg-3-tension", "kashani2019-npg-5.1-tension", "kashani2019-npg-8-tension",
                 "kashani2019-npg-11-tension", "kashani2019-npg-16.15-tension", "kashani2019-npg-17.85-tension",
                 "kashani2019-npg-20-tension")
# strength bases that cannot show a core carries p/2 without collapsing (a large-strain, undefined-strain, indentation
# or tension figure): such a value can FAIL the crush check (if even it is below p/2) but never pass it.
LARGE_STRAIN_PREFIXES = ("qiu2012-", "si2014-fibernfa-", "xu2019-hbnag-", "basotect-gplus-", "kashani2019-", "zhu2015-")
for _rid in TENSION_AS_EC:
    OVERRIDES[_rid] = ({"_tension_as_ec": True},
                       "Ec := the tensile modulus (Kashani 2019 main text: tension and compression moduli are consistent "
                       "for each sample); a ~200 micron foil, not a bulk core")
# curator exclusions: core_id -> reason. The record stays in the sources file and is listed under not_evaluated.
EXCLUDE = {
    "chen2017-cellular-carbon-sla-range": "abstract values (23.9 MPa, 0.36 MPa) without the density of the sample that gave them; the 30 kg/m3 is the low end of a family range quoted second-hand, so pairing them would be optimistic by an unknown factor",
    "meza2014-hollow-alumina-octet-heaviest-context": "context point at 258 kg/m3 whose modulus and strength come from different samples (the gatherer says not to pair them)",
    "mecklenburg2012-aerographite-0.2": "values only from a Wikipedia article (the paper is paywalled); not a verified source",
    "mecklenburg2012-aerographite-15": "values only from a Wikipedia article (the paper is paywalled); not a verified source",
    "eps-typeXI-typical-datasheet": "maker not named, OCR text layer, and its shear modulus exceeds its Young's modulus, "
                                    "which no isotropic foam with a positive Poisson ratio can do; the gatherer flagged it unreliable",
    "eps-1pcf-virginia-tech": "abstract read only through a summarising tool, so the numbers are not a verbatim quote; its "
                              "modulus is from three-point bending, not compression",
    "polyimide-polyumac-9.6-crushed": "a foam crushed on purpose to lower its modulus (acoustic processing), not an as-made core",
    "hrh10-6.4-24": "the same product and values as the US-sheet row hrh10-1_4-1.5 (6 ksi = 41 MPa); kept once",
    "hrh10-9.5-24": "the same product and values as the US-sheet row hrh10-3_8-1.5; kept once",
}


def cell_size_m(text):
    m = re.search(r"(?<![\d.])(\d)/(\d{1,2})(?![\d])", text or "")
    if not m:
        return None
    num, den = int(m.group(1)), int(m.group(2))
    if den not in (4, 8, 16, 32) or num >= den:
        return None
    return num / den * 0.0254


def main():
    cores, scaling, not_evaluated, gaps, searched = [], [], [], {}, {}
    files = {}
    for fam in FAMILIES:
        path = os.path.join(SOURCES, f"{fam}.json")
        if not os.path.exists(path):
            gaps[fam] = ["sources file missing at build time"]
            continue
        d = json.load(open(path))
        files[fam] = path
        gaps[fam] = d.get("gaps", [])
        searched[fam] = d.get("searched", [])
        for s in d.get("scaling", []):
            scaling.append(dict(s, family=fam, tag="QUESTIONABLE"))
        for r in d.get("records", []):
            rid = r.get("core_id")
            if rid in EXCLUDE:
                not_evaluated.append({"core_id": rid, "family": fam, "density_kg_m3": r.get("density_kg_m3"),
                                      "reason": "EXCLUDED: " + EXCLUDE[rid], "source": r.get("source")})
                continue
            if rid in TENSION_AS_EC and r.get("E_tension_Pa"):
                r = dict(r, E_c_Pa=r["E_tension_Pa"], E_c_as_printed=f"{r['E_tension_Pa']} Pa (tensile modulus)",
                         E_c_basis="tensile modulus standing in for Ec (paper: tension and compression moduli consistent)",
                         notes=(r.get("notes") or "") + f" Tensile strength {r.get('sigma_tension_Pa')} Pa, not used for crush.")
            has = [k for k in ("E_c_Pa", "G_c_Pa", "G_L_Pa", "G_W_Pa", "sigma_c_Pa") if r.get(k)]
            if not r.get("density_kg_m3") or not has:
                not_evaluated.append({"core_id": rid, "family": fam, "density_kg_m3": r.get("density_kg_m3"),
                                      "reason": "no density" if not r.get("density_kg_m3") else "no Ec, Gc or strength",
                                      "source": r.get("source")})
                continue
            text = " ".join(str(r.get(k) or "") for k in ("name", "architecture", "material"))
            honeycomb = "honeycomb" in text.lower()
            gl, gw = r.get("G_L_Pa"), r.get("G_W_Pa")
            gc = r.get("G_c_Pa") or (min(x for x in (gl, gw) if x) if (gl or gw) else None)
            core = {
                "core_id": rid, "family": fam, "name": r.get("name"), "material": r.get("material"),
                "architecture": r.get("architecture"), "status": r.get("status") or "MEASURED", "tag": "QUESTIONABLE",
                "density_kg_m3": r["density_kg_m3"], "density_as_printed": r.get("density_as_printed"),
                "E_c_Pa": r.get("E_c_Pa"), "E_c_as_printed": r.get("E_c_as_printed"), "E_c_basis": r.get("E_c_basis"),
                "G_c_Pa": gc, "G_L_Pa": gl, "G_W_Pa": gw, "G_c_as_printed": r.get("G_c_as_printed"),
                "G_c_basis": r.get("G_c_basis"),
                "sigma_c_Pa": r.get("sigma_c_Pa"), "sigma_c_as_printed": r.get("sigma_c_as_printed"),
                "sigma_c_basis": r.get("sigma_c_basis"),
                "sigma_c_stabilized_Pa": r.get("sigma_c_stabilized_Pa"), "crush_Pa": r.get("crush_Pa"),
                "sigma_c_class": ("large_strain_or_not_uniaxial" if rid.startswith(LARGE_STRAIN_PREFIXES) else "structural")
                if r.get("sigma_c_Pa") else None,
                "wrinkle_form": "honeycomb" if honeycomb else "continuum",
                "G_rule": None if gc else "isotropic_nu0",
                "cell_size_m": cell_size_m(r.get("name")) if honeycomb else None,
                "reading": r.get("reading"), "notes": r.get("notes"), "source": r.get("source"),
            }
            if rid in OVERRIDES:
                fields, reason = OVERRIDES[rid]
                core.update(fields)
                core["curator_override"] = reason
            cores.append(core)
    out = {"schema": 1, "card": "MAINLINE-013", "built_from": files, "derivation_rules": DERIVATION_RULES,
           "sensitivity_note": SENSITIVITY_NOTE, "cores": cores, "scaling": scaling,
           "not_evaluated": not_evaluated, "gaps": gaps, "searched": searched}
    with open(os.path.join(HERE, "cores.json"), "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")
    print(f"cores {len(cores)}, scaling {len(scaling)}, not evaluated {len(not_evaluated)}, files {sorted(files)}")


if __name__ == "__main__":
    main()
