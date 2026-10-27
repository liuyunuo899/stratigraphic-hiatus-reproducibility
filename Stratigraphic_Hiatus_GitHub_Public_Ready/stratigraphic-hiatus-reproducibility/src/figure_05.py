"""Figure 5: Case I Sadler diagrams and completeness.
(a) Median accumulation rate vs timespan by setting (IQR shaded).
(b) Completeness vs resolution tau by setting (median over columns).
(c) Column-level completeness at 5 Myr vs total recorded duration.
(d) Median hiatus duration vs completeness (columns, log-log).

Only figure layout / typography are adjusted.
No data values, formulas, or filters are changed.
"""

from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

from project_guard import verify_project_inputs
verify_project_inputs()

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from figures_common import (
    setup, save, SETTING_ORDER,
    SETTING_SHORT, PALETTE, PROC
)

setup()

# =====================================================
# 1. Read original data
# =====================================================

sd = pd.read_csv(f"{PROC}/sadler_summary.csv")
cp = pd.read_csv(f"{PROC}/completeness.csv")
s = pd.read_csv(f"{PROC}/columns_summary.csv")
h = pd.read_csv(f"{PROC}/hiatuses.csv")

# =====================================================
# 2. Unified figure style
# =====================================================

TITLE_SIZE = 11.5
LABEL_SIZE = 8.8
TICK_SIZE = 7.8
LEGEND_SIZE = 6.7

fig, axes = plt.subplots(2, 2, figsize=(10.8, 8.4))

fig.subplots_adjust(
    left=0.085,
    right=0.985,
    bottom=0.18,
    top=0.93,
    wspace=0.25,
    hspace=0.34
)

def panel_title(ax, text):
    ax.set_title(
        text,
        loc="left",
        pad=10,
        fontsize=TITLE_SIZE,
        fontweight="bold"
    )
    ax.tick_params(axis="both", which="major", labelsize=TICK_SIZE)
    ax.tick_params(axis="both", which="minor", labelsize=TICK_SIZE)

handles = []
labels = []

# =====================================================
# (a) Sadler diagram by setting
# =====================================================

ax = axes[0, 0]

for st in SETTING_ORDER:
    g = sd[sd["setting"] == st].sort_values("timespan_mid")
    g = g[g["n"] >= 30]

    ln = ax.loglog(
        g["timespan_mid"],
        g["rate_median"],
        "-o",
        ms=3.2,
        lw=1.5,
        color=PALETTE[st],
        label=SETTING_SHORT[st]
    )[0]

    ax.fill_between(
        g["timespan_mid"],
        g["rate_q25"],
        g["rate_q75"],
        color=PALETTE[st],
        alpha=0.12
    )

    handles.append(ln)
    labels.append(SETTING_SHORT[st])

ax.set_xlabel("Measurement timespan (Myr)", fontsize=LABEL_SIZE)
ax.set_ylabel("Median accumulation rate (m/Myr)", fontsize=LABEL_SIZE)
panel_title(ax, "(a) Sadler diagram by setting")

ax.legend(
    loc="lower left",
    bbox_to_anchor=(0.018, 0.025),
    fontsize=7.0,
    ncol=1,
    frameon=True,
    facecolor="white",
    edgecolor="#B0B0B0",
    framealpha=0.96,
    fancybox=False,
    borderaxespad=0.0,
    borderpad=0.35,
    labelspacing=0.28,
    handlelength=1.8,
    handletextpad=0.5
)

# =====================================================
# (b) Completeness vs resolution
# =====================================================

ax = axes[0, 1]

for st in SETTING_ORDER:
    g = cp[cp["setting"] == st].groupby("tau")["completeness"].median()

    ax.semilogx(
        g.index,
        g.values,
        "-o",
        ms=3.4,
        lw=1.5,
        color=PALETTE[st]
    )

ax.set_xlabel("Resolution $\\tau$ (Myr)", fontsize=LABEL_SIZE)
ax.set_ylabel("Median completeness C($\\tau$)", fontsize=LABEL_SIZE)
ax.set_ylim(0, 1)
panel_title(ax, "(b) Completeness vs resolution")

# =====================================================
# (c) Completeness vs column duration
# =====================================================

ax = axes[1, 0]

c5 = cp[cp["tau"] == 5].set_index("col_id")["completeness"]

ss = (
    s.set_index("col_id")
    .join(c5.rename("C5"))
    .dropna(subset=["C5"])
)

for st in SETTING_ORDER:
    g = ss[ss["setting"] == st]

    ax.scatter(
        g["duration"],
        g["C5"],
        s=9,
        color=PALETTE[st],
        alpha=0.45
    )

ax.set_xscale("log")
ax.set_ylim(0, 1.02)
ax.set_xlabel("Recorded duration (Myr)", fontsize=LABEL_SIZE)
ax.set_ylabel("C(5 Myr)", fontsize=LABEL_SIZE)
panel_title(ax, "(c) Completeness vs column duration")

# =====================================================
# (d) Hiatus length vs completeness
# =====================================================

ax = axes[1, 1]

hm = h.groupby("col_id")["hiatus_myr"].median().rename("med_h")

ss2 = ss.join(hm, how="inner")

for st in SETTING_ORDER:
    g = ss2[ss2["setting"] == st]

    ax.scatter(
        g["med_h"],
        g["C5"],
        s=9,
        color=PALETTE[st],
        alpha=0.45
    )

ax.set_xscale("log")
ax.set_ylim(0, 1.02)
ax.set_xlabel("Median hiatus duration per column (Myr)", fontsize=LABEL_SIZE)
ax.set_ylabel("C(5 Myr)", fontsize=LABEL_SIZE)
panel_title(ax, "(d) Hiatus length vs completeness")

# =====================================================
# 3. Shared legend at bottom
# =====================================================

# 4. Save figure
# =====================================================

save(fig, "figure_05_caseI_sadler_completeness")

print("Figure 5 generated successfully.")