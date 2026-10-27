"""Fetch Macrostrat North American columns and their units via the public API v2.

Data source: Macrostrat (https://macrostrat.org), CC BY 4.0.
Reference: Peters, Husson & Czaplewski (2018), Geochemistry, Geophysics, Geosystems 19, 1393-1409.
Access date: 2026-10-20.
Outputs:
  data/raw/macrostrat_columns_na.csv
  data/raw/macrostrat_units_na.csv
"""
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
import sys
if "--confirm-refresh-raw-data" not in sys.argv:
    raise SystemExit("已禁止自动更新原始数据。如确定要重新下载Macrostrat数据，请先备份，并显式追加 --confirm-refresh-raw-data 参数。")

import requests, time, json
import pandas as pd

BASE = "https://macrostrat.org/api/v2"
OUT_COLS = str(ROOT / "data/raw/macrostrat_columns_na.csv")
OUT_UNITS = str(ROOT / "data/raw/macrostrat_units_na.csv")

def fetch_columns():
    r = requests.get(f"{BASE}/columns?project_id=1&format=json", timeout=180)
    r.raise_for_status()
    return r.json()["success"]["data"]

def fetch_units(col_ids, chunk=80):
    rows = []
    for i in range(0, len(col_ids), chunk):
        ids = ",".join(str(c) for c in col_ids[i:i+chunk])
        r = requests.get(f"{BASE}/units?col_id={ids}&format=json", timeout=300)
        r.raise_for_status()
        rows.extend(r.json()["success"]["data"])
        time.sleep(0.3)
    return rows

if __name__ == "__main__":
    cols = fetch_columns()
    cdf = pd.DataFrame(cols)
    cdf.to_csv(OUT_COLS, index=False)
    print("columns:", len(cdf))
    units = fetch_units(list(cdf["col_id"].astype(int)))
    udf = pd.DataFrame(units)
    udf.to_csv(OUT_UNITS, index=False)
    print("units:", len(udf), "from", udf["col_id"].nunique(), "columns")
