"""Process Macrostrat columns/units into hiatus, completeness and rate datasets.

Definitions
-----------
- Units are sorted within a column by decreasing basal age (oldest first).
- A hiatus between two superposed units is t_age(lower) - b_age(upper), kept only
  if strictly positive (an explicit temporal gap between the top of the lower unit
  and the base of the overlying unit).
- Temporal completeness C(tau): fraction of time bins of width tau, spanning the
  column's total recorded duration, that contain at least one unit interval.
- Sadler-type pairwise rates: for every pair of dated horizons (unit tops and
  bases) in a column, rate = preserved thickness between horizons / age difference.
- Settings are aggregated from Macrostrat col_group labels into six
  physiographic-tectonic classes (see SETTINGS map).
Outputs: data/processed/columns_summary.csv, hiatuses.csv, completeness.csv,
         sadler_pairs.csv
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
from project_guard import verify_project_inputs
verify_project_inputs()

import numpy as np
import pandas as pd

RAW = str(ROOT / "data/raw")
PROC = str(ROOT / "data/processed")

SETTINGS = {
    "Cratonic platform": ["Midcontinent", "Northern Mid-Continent", "Southwest Mid-Continent",
                          "Midwestern Basins and Arches", "Southern Prairie Prov., Hudson Platform",
                          "Prairie Provinces and British Columbia", "Texas-Oklahoma Tectonic Region"],
    "Passive margin & coastal plain": ["Atlantic Coastal Plain", "Gulf Coast"],
    "Foreland (Rocky Mtn.)": ["Central-Southern Rockies", "Northern Rockies"],
    "Appalachian orogen": ["Northern Appalachians", "Southern Appalachians", "Piedmont-Blue Ridge",
                           "Northeast United States"],
    "Cordilleran & Alaska orogen": ["Canadian Cordillera I", "Canadian Cordillera II", "Canadian Cordillera III",
                                    "Northern California", "Central California", "Southern California",
                                    "Great Basin", "Northwest", "Northwest, Yukon Territories",
                                    "Northern Alaska", "Southern Alaska", "Mexico"],
    "Shield & Arctic": ["Canadian Shield", "Canadian Arctic I", "Canadian Arctic II", "Canadian Arctic III",
                        "Southeastern Canada"],
}
GROUP2SETTING = {g: s for s, gs in SETTINGS.items() for g in gs}
TAUS = [0.5, 1, 2, 5, 10, 20, 50]  # Myr


def load():
    cols = pd.read_csv(f"{RAW}/macrostrat_columns_na.csv")
    units = pd.read_csv(f"{RAW}/macrostrat_units_na.csv", low_memory=False)
    return cols, units


def column_metrics(units_col):
    u = units_col.dropna(subset=["t_age", "b_age"]).copy()
    u = u[(u["b_age"] >= u["t_age"])]
    u = u.sort_values("b_age", ascending=False)
    if len(u) < 3:
        return None
    t_age = u["t_age"].values.astype(float)
    b_age = u["b_age"].values.astype(float)
    thick = u["max_thick"].fillna(0).clip(lower=0).values.astype(float)
    gaps = t_age[:-1] - b_age[1:]  # top age of the older (lower) unit minus basal age of the overlying unit
    hiatuses = gaps[gaps > 0]
    t_min, t_max = t_age.min(), b_age.max()
    duration = t_max - t_min
    total_thick = thick.sum()
    comp = {}
    for tau in TAUS:
        nb = int(np.ceil(duration / tau))
        if nb < 1:
            comp[tau] = np.nan; continue
        edges = t_min + np.arange(nb + 1) * tau
        covered = np.zeros(nb, dtype=bool)
        for lo, hi in zip(t_age, b_age):  # unit covers [t_age, b_age]
            covered |= (hi > edges[:-1]) & (lo < edges[1:])
        comp[tau] = covered.mean()
    # Sadler pairwise rates
    # Sadler pairwise rates: build piecewise cumulative thickness vs age
    ages = np.unique(np.concatenate([t_age, b_age]))
    ages.sort()
    layer_thick = np.zeros(len(ages) - 1)
    for lo, hi, th in zip(t_age, b_age, thick):
        if hi > lo and th > 0:
            seg = np.clip(np.minimum(ages[1:], hi) - np.maximum(ages[:-1], lo), 0, None)
            layer_thick += seg / (hi - lo) * th
    cum = np.concatenate([[0], np.cumsum(layer_thick)])  # thickness below each age level
    pairs = []
    for i in range(len(ages)):
        for j in range(i + 1, len(ages)):
            dt = ages[j] - ages[i]
            dh = cum[j] - cum[i]  # thickness preserved between age_i and age_j
            if dt > 0 and dh > 0:
                pairs.append((dt, dh / dt))  # timespan (Myr), rate (m/Myr)
    return dict(duration=duration, n_units=len(u), total_thick=total_thick,
                n_hiatus=len(hiatuses), hiatuses=hiatuses, completeness=comp,
                pairs=pairs, t_min=t_min, t_max=t_max)


def main():
    cols, units = load()
    cols["setting"] = cols["col_group"].map(GROUP2SETTING)
    cols = cols.dropna(subset=["setting"])
    units = units[units["col_id"].isin(cols["col_id"])]
    summary_rows, hiatus_rows, comp_rows, sadler_rows = [], [], [], []
    for col_id, ucol in units.groupby("col_id"):
        meta = cols[cols["col_id"] == col_id].iloc[0]
        m = column_metrics(ucol)
        if m is None:
            continue
        summary_rows.append(dict(col_id=col_id, col_name=meta["col_name"],
                                 col_group=meta["col_group"], setting=meta["setting"],
                                 lat=meta["lat"], lng=meta["lng"], duration=m["duration"],
                                 n_units=m["n_units"], total_thick=m["total_thick"],
                                 n_hiatus=m["n_hiatus"], t_min=m["t_min"], t_max=m["t_max"]))
        for h in m["hiatuses"]:
            hiatus_rows.append(dict(col_id=col_id, setting=meta["setting"], hiatus_myr=h))
        for tau, c in m["completeness"].items():
            comp_rows.append(dict(col_id=col_id, setting=meta["setting"], tau=tau, completeness=c))
        for dt, rate in m["pairs"]:
            sadler_rows.append(dict(col_id=col_id, setting=meta["setting"], timespan_myr=dt, rate_m_per_myr=rate))
    pd.DataFrame(summary_rows).to_csv(f"{PROC}/columns_summary.csv", index=False)
    pd.DataFrame(hiatus_rows).to_csv(f"{PROC}/hiatuses.csv", index=False)
    pd.DataFrame(comp_rows).to_csv(f"{PROC}/completeness.csv", index=False)
    pd.DataFrame(sadler_rows).to_csv(f"{PROC}/sadler_pairs.csv", index=False)
    print("columns used:", len(summary_rows), "| hiatuses:", len(hiatus_rows),
          "| sadler pairs:", len(sadler_rows))


if __name__ == "__main__":
    main()
