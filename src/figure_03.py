
"""Figure 3: Case I data overview (Macrostrat, North America).
(a) Column locations by setting.
(b) Columns per setting.
(c) Two example columns as age-thickness staircases.
(d) Column duration versus unit count.

Only figure layout and legend positions have been modified.
"""

from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

from project_guard import verify_project_inputs
verify_project_inputs()

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from figures_common import (
    setup, save, SETTING_ORDER, SETTING_SHORT, PALETTE, PROC
)

setup()

# =====================================================
# 1. Read original data
# =====================================================

s = pd.read_csv(f"{PROC}/columns_summary.csv")

units = pd.read_csv(
    str(ROOT / "data/raw/macrostrat_units_na.csv"),
    low_memory=False
)

# =====================================================
# 2. Figure layout
# =====================================================

fig = plt.figure(figsize=(10.8, 8.25))

positions = {
    "a": [0.095, 0.575, 0.365, 0.327],
    "b": [0.660, 0.575, 0.300, 0.327],
    "c": [0.095, 0.124, 0.365, 0.327],
    "d": [0.660, 0.124, 0.300, 0.327],
}

# Unified panel titles
def panel_title(ax, text):
    ax.set_title(
        text,
        loc="left",
        pad=9,
        fontsize=11.5,
        fontweight="bold"
    )

# =====================================================
# (a) Column locations
# =====================================================

ax = fig.add_axes(positions["a"])

for st in SETTING_ORDER:
    g = s[s["setting"] == st]

    ax.scatter(
        g["lng"],
        g["lat"],
        s=3,
        color=PALETTE[st],
        alpha=0.6,
        label=SETTING_SHORT[st]
    )

ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

panel_title(
    ax,
    "(a) Column locations (n = %d)" % len(s)
)

# Legend inside the lower-right blank area
ax.legend(
    loc="lower right",
    bbox_to_anchor=(0.983, 0.023),
    ncol=1,
    fontsize=6.45,
    markerscale=2.2,
    frameon=True,
    fancybox=False,
    framealpha=0.96,
    borderpad=0.34,
    labelspacing=0.30,
    handletextpad=0.45
)

# =====================================================

# =====================================================
# (b) Columns by setting
# =====================================================

ax = fig.add_axes(positions["b"])

counts = (
    s["setting"]
    .value_counts()
    .reindex(SETTING_ORDER)
)

ax.barh(
    range(len(counts)),
    counts.values,
    color=[PALETTE[k] for k in counts.index]
)

ax.set_yticks(range(len(counts)))

ax.set_yticklabels(
    [SETTING_SHORT[k] for k in counts.index],
    fontsize=7.7
)

# Reserve space for numeric labels
ax.set_xlim(0, 360)
ax.set_xticks([0, 100, 200, 300])

# Place numeric labels outside the bars
for i, v in enumerate(counts.values):
    ax.text(
        v + 4,
        i,
        str(v),
        va="center",
        ha="left",
        fontsize=8,
        clip_on=True
    )

ax.set_xlabel("Columns used")

panel_title(
    ax,
    "(b) Columns by setting"
)

# =====================================================
# (c) Example stratigraphic columns
# =====================================================

ax = fig.add_axes(positions["c"])

ex = {
    "Cratonic platform": None,
    "Foreland (Rocky Mtn.)": None
}

# Select the same example columns as the original code
for st in ex:
    cand = (
        s[s["setting"] == st]
        .sort_values("n_units", ascending=False)
    )

    ex[st] = cand.iloc[0]["col_id"]

for st, cid in ex.items():

    u = (
        units[units["col_id"] == cid]
        .dropna(subset=["t_age", "b_age"])
        .sort_values("b_age", ascending=False)
    )

    u = u[(u["t_age"] <= 600)]

    cum = np.cumsum(
        u["max_thick"]
        .fillna(0)
        .clip(lower=0)
        .values
    )

    tt = []
    zz = []

    for (t0, t1, c0) in zip(
        u["t_age"],
        u["b_age"],
        np.concatenate([[0], cum[:-1]])
    ):
        tt += [t0, t1]
        zz += [c0, c0]

    tt.append(u["b_age"].iloc[-1])

    zz.append(
        cum[-1] if len(cum) else 0
    )

    ax.step(
        tt,
        zz,
        where="post",
        label=f"{SETTING_SHORT[st]} (col {cid})",
        color=PALETTE[st]
    )

ax.set_xlabel("Age (Ma)")
ax.set_ylabel("Cumulative preserved thickness (m)")

panel_title(
    ax,
    "(c) Example columns"
)

# Legend in the upper-right blank area
ax.legend(
    loc="upper right",
    bbox_to_anchor=(0.987, 0.968),
    fontsize=7.35,
    ncol=1,
    frameon=True,
    fancybox=False,
    framealpha=0.96,
    borderpad=0.35,
    handlelength=2.2,
    labelspacing=0.36
)

# =====================================================
# (d) Column duration vs unit count
# =====================================================

ax = fig.add_axes(positions["d"])

for st in SETTING_ORDER:
    g = s[s["setting"] == st]

    ax.scatter(
        g["duration"],
        g["n_units"],
        s=5,
        color=PALETTE[st],
        alpha=0.45
    )

ax.set_xscale("log")
ax.set_yscale("log")

ax.set_xlabel("Column recorded duration (Myr)")
ax.set_ylabel("Units per column")

panel_title(
    ax,
    "(d) Duration vs unit count"
)

# =====================================================
# 3. Save figure
# =====================================================

# Layout positions are manually defined.
# Do not use fig.tight_layout() here.

save(fig, "figure_03_caseI_overview")

print("Figure 3 generated successfully.")
