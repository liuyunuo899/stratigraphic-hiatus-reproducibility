# Stratigraphic hiatus statistics, temporal completeness and sediment preservation

Code and fixed-data reproducibility archive for the manuscript **"When is the stratigraphic record scale-invariant? Linking hiatus statistics, temporal completeness, and sediment preservation through deposition–erosion dynamics"**, prepared for *Earth-Science Reviews*.

This repository is built from the author's supplied **`1(3).zip`** and the corresponding **`ESR_Manuscript.docx` / `ESR_Supplement.docx`**. All `src/*.py` files, archived empirical and synthetic numerical CSVs, and original `figures/figure_*` images are preserved byte-for-byte. The project identity marker and the exact SHA-256-matched 55-reference literature table were restored because they were absent from the supplied archive but required by its unchanged code.

## Scope and principal results

- Case Study I uses an archived North American Macrostrat snapshot: 949 raw column entries, 24,141 unit records, 948 retained columns, 6,281 positive observed hiatuses, and 683,120 pairs used in the Sadler-style accumulation-rate analysis.
- Case Study II comprises 200 seeded runs for each of F1 white noise, F2 multi-periodic forcing and F3 integrated-noise forcing (600 runs in total), plus 36 threshold/rate-ratio combinations with 50 runs each.
- The inversion illustration uses 25 synthetic age observations, four nonnegative Tikhonov fits at smoothing weights 0.1, 1, 10 and 100, and 5,000 independent stochastic missing-deposition scenarios.
- The original ten figure scripts (`figure_01.py`–`figure_10.py`) map to **nine main figures and Supplementary Fig. S1** in the Earth-Science Reviews manuscript; see [FIGURE_MAP.md](FIGURE_MAP.md).

This is a **numerical reproduction of the archived implementation**, not a correction or external validation of its physical assumptions. In particular, `simulation.py` retains its original layer-age bookkeeping; the stochastic missing-deposition scenarios in `inversion.py` are **not** a χ²-filtered posterior from the Tikhonov fits. See [METHOD_NOTES.md](METHOD_NOTES.md).

## Repository contents

```text
PROJECT_ID.txt                    Project guard identity marker
literature_review.csv             Fixed 55-reference literature table
src/                              Original scientific and plot scripts
data/raw/                         Locked Macrostrat source snapshot
data/processed/                   Archived Case I outputs
  sadler_pairs.csv.gz             Lossless archive of the large pairs file
data/synthetic/                   Original ensembles, parameter sweep, inverse results
figures/                          Original code-output PNG and PDF figures
  submission/                     PNGs embedded in the submitted manuscript
scripts/restore_sadler_pairs.py   Exact recovery of the large CSV
scripts/verify_repository.py      SHA-256 integrity verification
requirements.txt                  Reference Python dependencies
FIGURE_MAP.md                     Script filename -> manuscript figure mapping
DATA_DICTIONARY.md                Data columns, units, and interpretation
METHOD_NOTES.md                   Scientific implementation and interpretation limitations
FILE_SHA256.csv                   File-level integrity manifest
SOURCE_AND_LICENSE.md             Provenance, attribution, publication rights
README_CN.md                      Chinese-language upload and use guide
```

## Reproduction (Python)

Use Python 3.12 in a clean virtual environment if possible. The dependencies in `requirements.txt` document one reference environment; they were missing from the supplied archive. Outputs are most reliable when using the same environment, random seeds and archived input files.

```bash
python -m pip install -r requirements.txt
python scripts/verify_repository.py
python scripts/restore_sadler_pairs.py
python src/project_guard.py
python src/verify_results.py
```

The guard verifies the three unchanged locked inputs, including `literature_review.csv`. **Do not run `src/data_fetch.py` for reproduction**: it queries a live API and could return a different snapshot.

To regenerate the existing output tables (this may take substantially longer than simply verifying them):

```bash
python src/data_processing.py
python src/analysis.py
python src/simulation.py
python src/inversion.py
python src/verify_results.py
```

To regenerate original-script figures (filenames refer to the **original ten-figure** sequence):

```bash
python src/figure_01.py
python src/figure_02.py
python src/figure_03.py
python src/figure_04.py
python src/figure_05.py
python src/figure_06.py
python src/figure_07.py
python src/figure_08.py
python src/figure_09.py
python src/figure_10.py
```

Scripts save into `figures/`. The separate `figures/submission/` images are **taken directly from the supplied manuscript Word files**. They may differ from original code-output PNGs in pixel dimensions or rendering, and are not evidence of a new dataset or altered numerical computation.

## Data provenance and interpretation

The raw Macrostrat CSVs represent the **fixed North American snapshot contained in this archive**, not a live up-to-date API extract. The observed positive gaps are computed using the top of the older unit minus the base of the younger unit. `C(τ)` is a **time-bin occupancy statistic**, not a measurement of the exact fraction of depositional time preserved within each bin. The analysis uses simplified tail fitting and does not produce definitive power-law acceptance p-values.

The archived numerical results should not be replaced by exploratory model diagnostics. Full limitations and figure provenance are summarised in [METHOD_NOTES.md](METHOD_NOTES.md) and [FIGURE_MAP.md](FIGURE_MAP.md).

## Citation and reuse

Please cite the corresponding article after publication and the Macrostrat database (Peters et al., 2018). Citation metadata for the unpublished manuscript are intentionally **not invented**; add the publication DOI and a release tag once available. **The repository owner confirms ownership of the Python source code and may publish it publicly.** No open-source licence has been selected yet; the owner may add one (e.g. MIT) if they wish to permit reuse. The Macrostrat input data remain subject to applicable third-party attribution and licensing conditions. See [SOURCE_AND_LICENSE.md](SOURCE_AND_LICENSE.md).
