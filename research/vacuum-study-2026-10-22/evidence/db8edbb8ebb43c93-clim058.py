#!/usr/bin/env python3
"""MAINLINE-058 site climatology: London Heathrow (NOAA ISD 03772099999; 51.4775 N, 0.4614 W, 25.29 m), 2014-2023.
Parses NOAA Global Hourly (ISD) CSV files (untrusted downloads, read as text only) into one record per UTC hour:
the FM-12 SYNOP at HH:00 supplies air temperature, dew point and sea-level pressure; total cloud (oktas) is the largest
layer coverage in that SYNOP, else the nearest METAR's total or layer cover; wind from the SYNOP. Quality codes 2/3/6/7
are rejected. Solar elevation from the NOAA/Spencer approximation. Writes runs/heathrow_hourly058.npz and a summary.
usage: clim058.py <download directory>"""
import csv
import datetime as dt
import json
import math
import sys
from pathlib import Path

import numpy as np

OUT = Path("unpublished-local-ref:3c8f53a40b5020e4"
           "vacuum-mainline058-flyable-band-1020/runs")
BAD = set("2367")
LAT, LON, ELEV = 51.4775, -0.461389, 25.29


def val(field, scale, missing, idx=0, qidx=1):
    if not field:
        return None
    parts = field.split(",")
    try:
        v, q = parts[idx], parts[qidx]
    except IndexError:
        return None
    if q in BAD or v.lstrip("+-").strip("9") == "" and len(v.lstrip("+-")) >= 4:
        return None
    try:
        x = int(v)
    except ValueError:
        return None
    if abs(x) == missing:
        return None
    return x / scale


def coverage(row):
    """Largest valid layer coverage code 0-8 among GA1-GA3 (9/10 obscured -> 8); None if absent."""
    best = None
    for k in ("GA1", "GA2", "GA3"):
        f = row.get(k) or ""
        p = f.split(",")
        if len(p) >= 2 and p[0].isdigit() and p[1] not in BAD:
            c = int(p[0])
            if c == 99:
                continue
            c = 8 if c in (9, 10) else c
            best = c if best is None else max(best, c)
    return best


def total_gf(row):
    f = row.get("GF1") or ""
    p = f.split(",")
    if len(p) >= 3 and p[0].isdigit() and p[2] not in BAD:
        c = int(p[0])
        if c == 99:
            return None
        return 8 if c in (9, 10) else min(c, 8)
    return None


def solar_elevation(t):
    """Degrees; t a UTC datetime. Spencer (1971) declination and equation of time."""
    n = t.timetuple().tm_yday
    g = 2 * math.pi / 365 * (n - 1 + (t.hour - 12) / 24)
    decl = (0.006918 - 0.399912 * math.cos(g) + 0.070257 * math.sin(g) - 0.006758 * math.cos(2 * g)
            + 0.000907 * math.sin(2 * g) - 0.002697 * math.cos(3 * g) + 0.00148 * math.sin(3 * g))
    eot = 229.18 * (0.000075 + 0.001868 * math.cos(g) - 0.032077 * math.sin(g) - 0.014615 * math.cos(2 * g)
                    - 0.040849 * math.sin(2 * g))
    tst = t.hour * 60 + t.minute + eot + 4 * LON
    ha = math.radians(tst / 4 - 180)
    lat = math.radians(LAT)
    s = math.sin(lat) * math.sin(decl) + math.cos(lat) * math.cos(decl) * math.cos(ha)
    return math.degrees(math.asin(max(-1, min(1, s))))


def main():
    src = Path(sys.argv[1])
    syn, met = {}, {}
    files = sorted(src.glob("20[0-9][0-9]-03772099999.csv"))
    for f in files:
        with open(f, newline="", encoding="utf-8", errors="replace") as fh:
            for row in csv.DictReader(fh):
                if row.get("STATION") != "03772099999":
                    continue
                try:
                    t = dt.datetime.strptime(row["DATE"], "%Y-%m-%dT%H:%M:%S")
                except (KeyError, ValueError):
                    continue
                typ = (row.get("REPORT_TYPE") or "").strip()
                if typ == "FM-12" and t.minute == 0:
                    syn[t] = row
                elif typ in ("FM-15", "FM-16"):
                    met.setdefault(t.replace(minute=0) + dt.timedelta(hours=1 if t.minute >= 30 else 0), []).append((t, row))
    start = dt.datetime(2014, 1, 1)
    end = dt.datetime(2024, 1, 1)
    hours = int((end - start).total_seconds() // 3600)
    T = np.full(hours, np.nan)
    TD = np.full(hours, np.nan)
    SLP = np.full(hours, np.nan)
    CL = np.full(hours, -1.0)
    WS = np.full(hours, np.nan)
    SUN = np.zeros(hours)
    src_cloud = np.zeros(hours, dtype=int)
    for i in range(hours):
        t = start + dt.timedelta(hours=i)
        SUN[i] = solar_elevation(t)
        r = syn.get(t)
        mlist = sorted(met.get(t, []), key=lambda x: abs((x[0] - t).total_seconds()))
        if r is not None:
            a = val(r.get("TMP"), 10, 9999)
            b = val(r.get("DEW"), 10, 9999)
            c = val(r.get("SLP"), 10, 99999)
            w = val(r.get("WND"), 10, 9999, 3, 4)
            T[i] = np.nan if a is None else a + 273.15
            TD[i] = np.nan if b is None else b + 273.15
            SLP[i] = np.nan if c is None else c
            WS[i] = np.nan if w is None else w
            cv = coverage(r)
            if cv is not None:
                CL[i], src_cloud[i] = cv, 1
        if np.isnan(T[i]) or np.isnan(TD[i]):
            for _, mr in mlist:
                a = val(mr.get("TMP"), 10, 9999)
                b = val(mr.get("DEW"), 10, 9999)
                if a is not None and b is not None:
                    T[i], TD[i] = a + 273.15, b + 273.15
                    break
        if np.isnan(SLP[i]):
            for _, mr in mlist:
                q = val(mr.get("MA1"), 10, 99999)          # altimeter (QNH); ~SLP at 25 m elevation
                if q is not None:
                    SLP[i] = q
                    break
        if CL[i] < 0:
            for _, mr in mlist:
                cv = total_gf(mr)
                cv = coverage(mr) if cv is None else cv
                if cv is not None:
                    CL[i], src_cloud[i] = cv, 2
                    break
    ok = ~np.isnan(T) & ~np.isnan(TD) & ~np.isnan(SLP)
    np.savez_compressed(OUT / "heathrow_hourly058.npz", start=str(start), T_K=T, Td_K=TD, SLP_hPa=SLP, cloud_oktas=CL,
                        wind_m_s=WS, sun_elevation_deg=SUN, cloud_source=src_cloud)
    summ = {"station": "03772099999 HEATHROW, UK", "lat": LAT, "lon": LON, "elevation_m": ELEV,
            "period_utc": [str(start), str(end)], "hours": hours, "complete_T_Td_SLP_hours": int(ok.sum()),
            "cloud_known_hours": int((CL >= 0).sum()), "synop_hours": len([k for k in syn if start <= k < end]),
            "files": [f.name for f in files],
            "T_K_percentiles": {str(q): float(np.nanpercentile(T, q)) for q in (0.1, 1, 5, 10, 50, 90, 95, 99, 99.9)},
            "SLP_hPa_percentiles": {str(q): float(np.nanpercentile(SLP, q)) for q in (0.1, 1, 5, 10, 50, 90, 95, 99, 99.9)},
            "Td_K_percentiles": {str(q): float(np.nanpercentile(TD, q)) for q in (1, 50, 99)},
            "night_fraction": float(np.mean(SUN < 0)),
            "overcast_7plus_fraction_of_known": float(np.mean(CL[CL >= 0] >= 7))}
    (OUT / "heathrow_summary058.json").write_text(json.dumps(summ, indent=1))
    print(json.dumps(summ, indent=1))


if __name__ == "__main__":
    main()
