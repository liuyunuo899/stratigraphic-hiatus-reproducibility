
"""Figure 2: Literature and evidence map.

(a) Timeline of references coloured by theme.
(b) Theme x decade heatmap.
(c) Theme composition.
(d) Accumulation of references.

Corrected the mismatch between theme positions and
y-axis labels in panel (a).

All reference data and classifications remain unchanged.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

from project_guard import verify_project_inputs
verify_project_inputs()

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from figures_common import setup, save


# =====================================================
# 1. Original literature classifications
# =====================================================

THEMES = {
    "Completeness & Sadler effect": [
        "Sadler 1981",
        "Sadler & Strauss 1990",
        "Tipper 1983",
        "Tipper 1998",
        "Sommerfield 2006",
        "Kemp 2012",
        "Kemp et al. 2018",
        "Hagen 2024",
        "Aadland et al. 2018",
        "Bailey & Smith 2010",
        "Miall 2026",
        "Renaudie & Lazarus 2025",
        "Wheeler 1958",
        "Miall 2014",
        "Holbrook & Miall 2020",
        "Ager 1973",
        "Barrell 1917"
    ],

    "Hiatus mechanisms & scaling": [
        "Plotnick 1986",
        "Schumer & Jerolmack 2009",
        "Schumer, Jerolmack & McElroy 2011",
        "Ganti et al. 2011",
        "Straub & Foreman 2018",
        "Trampush & Hajek 2017",
        "Hajek & Straub 2017",
        "Straub et al. 2020",
        "Jerolmack & Paola 2010",
        "Wang et al. 2011",
        "Straub et al. 2009",
        "Pelletier & Turcotte 1997",
        "Barefoot et al. 2023",
        "Sharma et al. 2024",
        "Trampush et al. 2017",
        "Grimaud et al. 2022",
        "Dutkiewicz et al. 2024",
        "Spencer-Cervato 1998",
        "Nordsvan et al. 2025",
        "Sadler & Jerolmack 2014",
        "Tipper 2014",
        "Paola et al. 2018"
    ],

    "Preservation & recycling": [
        "Veizer & Jansen 1979",
        "Veizer & Jansen 1985",
        "Wilkinson & Walker 1989",
        "Hay & Wold 1990",
        "Wilkinson & McElroy 2007",
        "Wilkinson et al. 2009",
        "Peters & Husson 2017",
        "Husson & Peters 2017",
        "Sloss 1963"
    ],

    "Methods: inversion & power-law testing": [
        "Clauset et al. 2009",
        "Stumpf & Porter 2012",
        "Blaauw & Christen 2011",
        "Tarantola 2005",
        "Charvin et al. 2009"
    ],

    "Data platform": [
        "Peters, Husson & Czaplewski 2018"
    ],

    "Hiatus effects on rates": [
        "Sadler 1999"
    ]
}


# =====================================================
# 2. Original colours and theme names
# =====================================================

TCOL = {
    "Completeness & Sadler effect": "#0072B2",
    "Hiatus mechanisms & scaling": "#D55E00",
    "Preservation & recycling": "#009E73",
    "Methods: inversion & power-law testing": "#CC79A7",
    "Data platform": "#E69F00",
    "Hiatus effects on rates": "#666666"
}

SHORT = {
    "Completeness & Sadler effect":
        "Completeness &\nSadler effect",

    "Hiatus mechanisms & scaling":
        "Hiatus mechanisms\n& scaling",

    "Preservation & recycling":
        "Preservation &\nrecycling",

    "Methods: inversion & power-law testing":
        "Methods: inversion\n& PL testing",

    "Data platform":
        "Data platform",

    "Hiatus effects on rates":
        "Hiatus effects\non rates"
}


# =====================================================
# 3. Read actual literature data
# =====================================================

setup()

lit = pd.read_csv(
    ROOT / "literature_review.csv"
)

# Preserve original reference-theme classifications
theme_lookup = {
    key: theme
    for theme, keys in THEMES.items()
    for key in keys
}

lit["theme"] = lit["reference_key"].map(
    theme_lookup
)

# Do not silently omit unclassified references
assert lit["theme"].notna().all(), \
    lit[lit["theme"].isna()]["reference_key"]

lit["decade"] = (
    lit["year"] // 10 * 10
).astype(int)

# Use the same theme order in every panel
order = list(THEMES)


# =====================================================
# 4. Unified figure style
# =====================================================

TITLE_SIZE = 11.5
LABEL_SIZE = 8.8
TICK_SIZE = 7.8
ANNO_SIZE = 7.0

fig = plt.figure(
    figsize=(12.6, 8.8)
)

# Manually adjust panel positions
ax_a = fig.add_axes(
    [0.18, 0.59, 0.29, 0.315]
)

ax_b = fig.add_axes(
    [0.69, 0.59, 0.28, 0.315]
)

ax_c = fig.add_axes(
    [0.18, 0.12, 0.29, 0.315]
)

ax_d = fig.add_axes(
    [0.69, 0.12, 0.28, 0.315]
)


def style(ax, title):

    ax.set_title(
        title,
        fontsize=TITLE_SIZE,
        loc="left",
        fontweight="bold",
        pad=10
    )

    ax.tick_params(
        axis="both",
        which="major",
        labelsize=TICK_SIZE
    )


# =====================================================
# (a) Verified reference timeline
# =====================================================

ax = ax_a

# Corrected:
# Theme positions and y-axis labels use identical order.

for i, theme in enumerate(order):

    g = lit[
        lit["theme"] == theme
    ]

    ax.scatter(
        g["year"],
        np.full(len(g), i)
        + np.linspace(-0.28, 0.28, len(g)),
        s=23,
        color=TCOL[theme],
        alpha=0.85,
        edgecolor="white",
        linewidth=0.35
    )

ax.set_yticks(
    range(len(order))
)

ax.set_yticklabels(
    [SHORT[t] for t in order],
    fontsize=TICK_SIZE
)

ax.set_xlabel(
    "Publication year",
    fontsize=LABEL_SIZE
)

ax.set_xlim(1905, 2032)

ax.set_ylim(
    -0.6,
    len(order) - 0.1
)

style(
    ax,
    "(a) Verified reference timeline"
)


# =====================================================
# (b) Theme by decade
# =====================================================

ax = ax_b

# Counts are calculated directly from the CSV.
pv = lit.pivot_table(
    index="theme",
    columns="decade",
    values="reference_key",
    aggfunc="count",
    fill_value=0
)

# Consistent theme order with panel (a)
pv = pv.reindex(
    index=order,
    columns=sorted(pv.columns),
    fill_value=0
)

im = ax.imshow(
    pv.values,
    aspect="auto",
    cmap="viridis"
)

ax.set_xticks(
    range(len(pv.columns))
)

ax.set_xticklabels(
    pv.columns,
    rotation=55,
    ha="right",
    fontsize=TICK_SIZE
)

ax.set_yticks(
    range(len(pv.index))
)

ax.set_yticklabels(
    [
        SHORT[t].replace("\n", " ")
        for t in pv.index
    ],
    fontsize=7.2
)

# Display actual counts, not fixed values
for i in range(pv.shape[0]):

    for j in range(pv.shape[1]):

        if pv.values[i, j] > 0:

            ax.text(
                j,
                i,
                str(int(pv.values[i, j])),
                ha="center",
                va="center",
                fontsize=ANNO_SIZE,
                color=(
                    "white"
                    if pv.values[i, j]
                    < pv.values.max() / 1.6
                    else "black"
                )
            )

style(
    ax,
    "(b) Theme by decade (n refs)"
)


# =====================================================
# (c) Reference set composition
# =====================================================

ax = ax_c

# Actual reference counts from current CSV
counts = (
    lit["theme"]
    .value_counts()
    .reindex(order)
)

ax.barh(
    range(len(counts)),
    counts.values,
    color=[
        TCOL[t]
        for t in counts.index
    ]
)

ax.set_yticks(
    range(len(counts))
)

ax.set_yticklabels(
    [
        SHORT[t].replace("\n", " ")
        for t in counts.index
    ],
    fontsize=TICK_SIZE
)

ax.set_xlabel(
    "Number of verified references",
    fontsize=LABEL_SIZE
)

for i, v in enumerate(counts.values):

    ax.text(
        v + 0.2,
        i,
        str(int(v)),
        va="center",
        fontsize=TICK_SIZE
    )

style(
    ax,
    "(c) Reference set composition"
)


# =====================================================
# (d) Accumulation of evidence
# =====================================================

ax = ax_d

# Calculate cumulative counts from actual years
ys = np.sort(
    lit["year"].values
)

ax.step(
    ys,
    np.arange(1, len(ys) + 1),
    color="#21618C",
    lw=1.45
)

# Original historical reference markers
for y0 in [
    1981, 2009, 2017
]:

    ax.axvline(
        y0,
        color="grey",
        ls=":",
        lw=0.8
    )

# Adjust annotation positions only
ax.text(
    1979,
    46,
    "Sadler 1981",
    fontsize=ANNO_SIZE,
    color="grey",
    ha="right"
)

ax.text(
    2007,
    39,
    "CTRW/filter\n2009–2011",
    fontsize=ANNO_SIZE,
    color="grey",
    ha="right"
)

ax.text(
    2015,
    7.5,
    "2017–2026\nwave",
    fontsize=ANNO_SIZE,
    color="grey",
    ha="right"
)

ax.set_xlabel(
    "Year",
    fontsize=LABEL_SIZE
)

ax.set_ylabel(
    "Cumulative references",
    fontsize=LABEL_SIZE
)

ax.set_xlim(
    1905, 2032
)

style(
    ax,
    "(d) Accumulation of evidence"
)


# =====================================================
# 5. Save Figure 2
# =====================================================

# Panel positions are manually controlled.
# Do not call tight_layout() here.

save(
    fig,
    "figure_02_literature_map"
)

print(
    "Reference counts by theme:",
    counts.to_dict()
)

print(
    "Total reference rows:",
    len(lit)
)

print(
    "Figure 2 generated successfully."
)
