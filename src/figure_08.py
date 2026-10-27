
"""Figure 8: Case II completeness-preservation coupling.

(a) Completeness C(tau) curves by forcing class.
(b) Preservation efficiency P distributions.
(c) Parameter sensitivity sweep.
(d) Hiatus duration versus preservation efficiency.

Only figure layout, fonts, and legend positions are modified.
All data and calculations remain unchanged.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

from project_guard import verify_project_inputs
verify_project_inputs()

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from figures_common import (
    setup, save, FCOLORS, FLABELS, SYN
)

setup()

# =====================================================
# 1. Read your calculated data
# =====================================================

runs = pd.read_csv(
    f"{SYN}/ensemble_runs.csv"
)

sweep = pd.read_csv(
    f"{SYN}/sensitivity_sweep.csv"
)

hiats = pd.read_csv(
    f"{SYN}/ensemble_hiatuses.csv"
)

TAUS = [
    0.005, 0.01, 0.02, 0.05,
    0.1, 0.2, 0.5, 1.0
]

# =====================================================
# 2. Unified figure formatting
# =====================================================

TITLE_SIZE = 11.5
LABEL_SIZE = 8.8
TICK_SIZE = 7.8
LEGEND_SIZE = 7.0

fig, axes = plt.subplots(
    2, 2,
    figsize=(10.8, 8.2)
)

fig.subplots_adjust(
    left=0.087,
    right=0.983,
    bottom=0.105,
    top=0.925,
    wspace=0.27,
    hspace=0.36
)


def format_panel(ax, caption):

    ax.set_title(
        caption,
        loc="left",
        pad=10,
        fontsize=TITLE_SIZE,
        fontweight="bold"
    )

    ax.tick_params(
        axis="both",
        which="major",
        labelsize=TICK_SIZE
    )

    ax.tick_params(
        axis="both",
        which="minor",
        labelsize=TICK_SIZE
    )

    ax.xaxis.label.set_size(LABEL_SIZE)
    ax.yaxis.label.set_size(LABEL_SIZE)


legend_kwargs = dict(
    frameon=True,
    framealpha=0.96,
    facecolor="white",
    edgecolor="#B0B0B0",
    fancybox=False,
    borderpad=0.35,
    handlelength=1.8,
    labelspacing=0.30
)

# =====================================================
# (a) Completeness by forcing class
# =====================================================

ax = axes[0, 0]

for k in ["F1", "F2", "F3"]:

    g = runs[runs["kind"] == k]

    med = [
        g[f"C_{t}"].median()
        for t in TAUS
    ]

    lo = [
        g[f"C_{t}"].quantile(0.25)
        for t in TAUS
    ]

    hi = [
        g[f"C_{t}"].quantile(0.75)
        for t in TAUS
    ]

    ax.semilogx(
        np.array(TAUS) * 1000,
        med,
        "-o",
        ms=3.5,
        color=FCOLORS[k],
        label=FLABELS[k]
    )

    ax.fill_between(
        np.array(TAUS) * 1000,
        lo,
        hi,
        color=FCOLORS[k],
        alpha=0.15
    )

ax.set_xlabel(
    "Resolution $\\tau$ (kyr)"
)

ax.set_ylabel(
    "Completeness C($\\tau$)"
)

ax.set_ylim(0, 1.02)

ax.legend(
    fontsize=LEGEND_SIZE,
    loc="upper left",
    bbox_to_anchor=(0.02, 0.975),
    **legend_kwargs
)

format_panel(
    ax,
    "(a) Completeness by forcing class"
)

# =====================================================
# (b) Preservation efficiency
# =====================================================

ax = axes[0, 1]

data = [
    runs[runs["kind"] == k]["P"].values
    for k in ["F1", "F2", "F3"]
]

bp = ax.boxplot(
    data,
    tick_labels=["F1", "F2", "F3"],
    showfliers=False,
    patch_artist=True,
    widths=0.5
)

for patch, k in zip(
    bp["boxes"],
    ["F1", "F2", "F3"]
):

    patch.set_facecolor(
        FCOLORS[k]
    )

    patch.set_alpha(0.7)

ax.set_ylabel(
    "Preservation efficiency P"
)

ax.set_ylim(0, 1.02)

format_panel(
    ax,
    "(b) Preservation efficiency"
)

# =====================================================
# (c) Sensitivity sweep
# =====================================================

ax = axes[1, 0]

markers = {
    "F1": "o",
    "F2": "s",
    "F3": "^"
}

for k in ["F1", "F2", "F3"]:

    g = sweep[
        sweep["kind"] == k
    ]

    for vev, ls in [
        (0.5, ":"),
        (1.0, "-"),
        (2.0, "--")
    ]:

        gg = g[
            g["ve_over_vd"] == vev
        ]

        ax.plot(
            gg["theta"],
            gg["P_med"],
            ls + markers[k],
            color=FCOLORS[k],
            ms=4,
            lw=1.0,
            label=f"{k}, $v_e/v_d$={vev}"
        )

ax.set_xlabel(
    "Stasis threshold $\\theta$"
)

ax.set_ylabel(
    "Median P"
)

# Only expands the display area for the legend.
# No data values are changed.
ax.set_ylim(-0.02, 0.93)

# Modified: legend inside upper-right corner
ax.legend(
    fontsize=6.1,
    ncol=2,
    loc="upper right",
    bbox_to_anchor=(0.985, 0.985),
    columnspacing=0.6,
    handlelength=1.3,
    handletextpad=0.4,
    borderpad=0.35,
    labelspacing=0.28,
    frameon=True,
    framealpha=0.96,
    facecolor="white",
    edgecolor="#B0B0B0",
    fancybox=False
)

format_panel(
    ax,
    "(c) Sensitivity sweep"
)

# =====================================================
# (d) Hiatus length vs preservation
# =====================================================

ax = axes[1, 1]

med_h = (
    hiats.groupby(
        ["kind", "run"]
    )["hiatus_myr"]
    .median()
    .reset_index()
    .rename(
        columns={
            "hiatus_myr": "med_h"
        }
    )
)

m = runs.merge(
    med_h,
    on=["kind", "run"]
)

for k in ["F1", "F2", "F3"]:

    g = m[
        m["kind"] == k
    ]

    ax.scatter(
        g["med_h"] * 1000,
        g["P"],
        s=6,
        color=FCOLORS[k],
        alpha=0.4,
        label=k
    )

ax.set_xscale("log")

ax.set_xlabel(
    "Median hiatus duration per run (kyr)"
)

ax.set_ylabel("P")

ax.legend(
    fontsize=LEGEND_SIZE,
    loc="upper right",
    bbox_to_anchor=(0.985, 0.98),
    **legend_kwargs
)

format_panel(
    ax,
    "(d) Hiatus length vs preservation"
)

# =====================================================
# 3. Save figure
# =====================================================

save(
    fig,
    "figure_08_caseII_coupling"
)

print("Figure 8 generated successfully.")
