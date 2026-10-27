
"""Figure 10: Integrated synthesis and research roadmap.

(a) Mechanism and diagnostic evidence matrix.
(b) Hiatus exponent versus log10 median hiatus.
(c) Prioritised research roadmap.

Only layout and text positions are modified.
The original qualitative matrix is retained unchanged.
"""

from pathlib import Path
import textwrap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROOT = Path(__file__).resolve().parents[1]

from project_guard import verify_project_inputs
verify_project_inputs()

from figures_common import (
    setup, save, SYN, PROC, SETTING_SHORT
)

setup()

# Read your actual calculated data
fits = pd.read_csv(
    f"{PROC}/hiatus_powerlaw_fits.csv"
).set_index("setting")

runs = pd.read_csv(
    f"{SYN}/ensemble_runs.csv"
)

# Unified typography
TITLE_SIZE = 11.5
LABEL_SIZE = 8.8
TICK_SIZE = 7.8
NOTE_SIZE = 8.0

fig = plt.figure(figsize=(12.8, 8.8))

# Panel positions
ax_a = fig.add_axes([0.065, 0.525, 0.91, 0.385])
ax_b = fig.add_axes([0.085, 0.11, 0.385, 0.31])
ax_c = fig.add_axes([0.560, 0.11, 0.405, 0.31])

def set_title(ax, title):
    ax.set_title(
        title,
        loc="left",
        fontsize=TITLE_SIZE,
        fontweight="bold",
        pad=12
    )
    ax.tick_params(
        axis="both",
        which="major",
        labelsize=TICK_SIZE
    )

# =====================================================
# (a) Mechanism and diagnostic evidence matrix
# =====================================================

ax = ax_a
ax.set_xlim(0, 10.2)
ax.set_ylim(-0.55, 6.2)
ax.axis("off")

rows_m = [
    "F1 white-noise forcing",
    "F2 multi-periodic forcing",
    "F3 long-memory forcing",
    "Real: orogenic/foreland/passive",
    "Real: cratonic platform",
    "Real: shield & arctic"
]

cols_m = [
    "Heavy-tailed\nhiatus CCDF",
    "Low completeness\nat fine $\\tau$",
    "Low preservation\nefficiency",
    "Power law beats\nexponential (LLR)"
]

# Original author's qualitative judgements.
# These values are NOT automatically calculated.
# Keep unchanged for numerical/figure reproduction.
M = [
    ["Y", "Y", "Y", "Y"],
    ["Y", "~", "~", "Y"],
    ["Y", "N", "N", "Y"],
    ["Y", "~", "~", "Y"],
    ["~", "Y", "~", "N"],
    ["Y", "~", "~", "~"]
]

cmap = {
    "Y": "#1E8449",
    "~": "#B7950B",
    "N": "#922B21"
}

words = {
    "Y": "yes",
    "~": "partly",
    "N": "no"
}

centers = [4.25, 5.78, 7.31, 8.84]

y_positions = [
    5.06 - i * 0.82
    for i in range(len(rows_m))
]

for i, (label, yy) in enumerate(
    zip(rows_m, y_positions)
):
    ax.text(
        0.05, yy, label,
        fontsize=8.7,
        va="center",
        ha="left"
    )

    for j, xx in enumerate(centers):
        val = M[i][j]

        ax.add_patch(
            Rectangle(
                (xx - 0.49, yy - 0.25),
                0.98, 0.50,
                facecolor=cmap[val],
                edgecolor="none",
                alpha=0.85
            )
        )

        ax.text(
            xx, yy, words[val],
            fontsize=8.1,
            color="white",
            ha="center",
            va="center"
        )

for xx, heading in zip(centers, cols_m):
    ax.text(
        xx, 5.70, heading,
        fontsize=8.3,
        ha="center",
        va="bottom",
        linespacing=1.2
    )

ax.text(
    0.05, -0.37,
    "Compiled from Figs. 4, 5, 7, 8; "
    "'partly' = intermediate or range-limited behaviour.",
    fontsize=NOTE_SIZE,
    color="grey",
    ha="left",
    va="center"
)

set_title(
    ax,
    "(a) Mechanism × diagnostic evidence matrix"
)

# =====================================================
# (b) Setting-level hiatus statistics
# =====================================================

ax = ax_b

# The coordinates come directly from your CSV
for st, r in fits.iterrows():
    x = r["alpha"]
    y = np.log10(r["median"])

    ax.scatter(
        x, y,
        s=55,
        color="#21618C",
        zorder=3
    )

# Only text offsets are adjusted.
# These offsets DO NOT affect point coordinates.
label_offsets = {
    "Appalachian orogen": (12, -12),
    "Cordilleran & Alaska orogen": (12, -1),
    "Cratonic platform": (11, -3),
    "Foreland (Rocky Mtn.)": (12, 12),
    "Passive margin & coastal plain": (12, -1),
    "Shield & Arctic": (11, 3)
}

for st, r in fits.iterrows():
    x = r["alpha"]
    y = np.log10(r["median"])

    ax.annotate(
        SETTING_SHORT[st],
        xy=(x, y),
        xytext=label_offsets.get(st, (10, 5)),
        textcoords="offset points",
        fontsize=8.1,
        ha="left",
        va="center",
        annotation_clip=False
    )

# Adapt axis limits to actual results.
# Reserve additional space for labels.
alpha_min = fits["alpha"].min()
alpha_max = fits["alpha"].max()
yvals = np.log10(fits["median"].values)
alpha_range = alpha_max - alpha_min

ax.set_xlim(
    alpha_min - max(0.35, 0.10 * alpha_range),
    alpha_max + max(1.5, 0.5 * alpha_range)
)

ax.set_ylim(
    yvals.min() - 0.16,
    yvals.max() + 0.24
)

ax.set_xlabel(
    "Hiatus power-law exponent $\\alpha$ (real settings)",
    fontsize=LABEL_SIZE
)

ax.set_ylabel(
    "log$_{10}$ median hiatus (Myr)",
    fontsize=LABEL_SIZE
)

set_title(
    ax,
    "(b) Setting-level hiatus statistics"
)

# =====================================================
# (c) Prioritised research roadmap
# =====================================================

ax = ax_c
ax.set_xlim(0, 10)
ax.set_ylim(0.35, 6.45)
ax.axis("off")

# Preserve all original wording and order.
items = [
    "1. Global hiatus databases with uncertainty-aware ages (extend beyond N. America)",
    "2. Age-depth models that explicitly allow hiatuses (beyond smooth priors)",
    "3. Coupled landscape-stratigraphy models with mass tracking and recycling",
    "4. Independent constraints on eroded mass (thermochronology, provenance)",
    "5. Community protocols for power-law testing of geologic durations",
    "6. Assimilation of real forcing records into inverse stratigraphic models"
]

for i, item in enumerate(items):

    y_center = 5.83 - i * 0.91

    ax.add_patch(
        Rectangle(
            (0.10, y_center - 0.38),
            9.8, 0.76,
            facecolor="#F2F3F4",
            edgecolor="#99A3A4",
            lw=0.75
        )
    )

    # Automatically wrap long text inside each box
    wrapped = textwrap.fill(
        item,
        width=55,
        break_long_words=False,
        break_on_hyphens=False
    )

    ax.text(
        0.36,
        y_center,
        wrapped,
        fontsize=8.5,
        ha="left",
        va="center",
        linespacing=1.25
    )

set_title(
    ax,
    "(c) Prioritised research roadmap"
)

# =====================================================
# Save figure
# =====================================================

save(fig, "figure_10_synthesis")

print("Figure 10 generated successfully.")
