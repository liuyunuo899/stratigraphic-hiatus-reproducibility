# Stratigraphic hiatus reproducibility archive

**Manuscript:** *When does the stratigraphic record appear scale-invariant? Linking hiatus statistics, temporal occupancy, and sediment preservation through deposition–erosion dynamics*

**Target journal:** *Earth-Science Reviews*

**Repository:** https://github.com/liuyunuo899/stratigraphic-hiatus-reproducibility

This repository provides the fixed input data, archived numerical outputs, Python source code, plotting scripts, and documentation associated with the manuscript. It is intended to support **reproduction of the reported calculations using the archived inputs**, not to claim independent physical validation of the model or formal proof of geological scale invariance.

## 1. Data and analyses

The project combines three components:

- **Case Study I — North American Macrostrat data.** The archived API-derived snapshot contains 949 column records and 24,141 unit records. After the analysis selection rules, 948 columns and 24,139 units remain; 6,281 positive inter-unit hiatuses are reported. The archived Sadler-style analysis contains 683,120 age-span/accumulation-rate pairs.
- **Case Study II — deposition–stasis–erosion simulations.** The baseline consists of 200 runs for each of three forcing classes (F1: white noise; F2: multi-periodic forcing with noise; F3: integrated noise with noise), or 600 runs in total. A separate sensitivity analysis uses 36 configurations (3 forcing classes × 4 threshold values × 3 erosion/deposition rate ratios), with 50 runs per configuration (1,800 runs total).
- **Inverse illustration.** A synthetic example provides 25 age–thickness observations, four nonnegative Tikhonov fits, and a **separate** set of 5,000 stochastic missing-deposition scenarios. These scenarios are not posterior draws from the Tikhonov fits and were not selected by a chi-square acceptance threshold.

The numerical definitions, assumptions, and interpretation limits are described in the manuscript and in [`METHOD_NOTES.md`](METHOD_NOTES.md). In particular, `C(τ)` is **time-bin occupancy**, not an exact fraction of geological time preserved, and the synthetic results reflect the archived layer-storage and age-bookkeeping implementation.

## 2. Repository structure

```text
README.md                         This guide
LICENSE                           MIT License for the original Python code
SOURCE_AND_LICENSE.md             Provenance and third-party data attribution
PROJECT_ID.txt                    Project identity marker
literature_review.csv             Fixed 55-reference input table
requirements.txt                  Reference Python package versions
FILE_SHA256.csv                   Checksums for archived repository files
FIGURE_MAP.md                     Mapping between code and manuscript figure numbers
DATA_DICTIONARY.md                Dataset and variable descriptions
METHOD_NOTES.md                   Implementation and interpretation notes
src/                              Data processing, analysis, simulation, inversion and plotting
scripts/                          Archive verification and dataset restoration utilities
data/raw/                         Archived Macrostrat input CSVs
data/processed/                   Archived empirical outputs; compressed Sadler-pair table
data/synthetic/                   Archived simulation, sensitivity and inversion outputs
figures/                          Figure assets, including submitted figures when supplied
```

The GitHub `LICENSE` file is maintained in the public repository. The fixed Macrostrat datasets and published third-party literature are **not automatically relicensed under MIT**.

## 3. Download and set up

Download the full repository using **Code → Download ZIP** on GitHub, extract it, and open a terminal **in the repository root** (the folder containing `requirements.txt`, `src/`, `scripts/`, and `data/`). Alternatively:

```bash
git clone https://github.com/liuyunuo899/stratigraphic-hiatus-reproducibility.git
cd stratigraphic-hiatus-reproducibility
```

Python **3.12** is recommended. Install the versions listed in the supplied environment file:

```bash
python -m pip install -r requirements.txt
```

On some Windows systems, use `py -3.12` instead of `python` if appropriate. Run the commands below **from the repository root**. Retain the original folder structure; copying a single `.py` file elsewhere is not sufficient.

## 4. Verify the archived results (recommended first)

For a first check, use the files already archived in the repository. **Do not run `src/data_fetch.py`.**

Run these commands in order:

```bash
python scripts/verify_repository.py
python scripts/restore_sadler_pairs.py
python src/project_guard.py
python src/verify_results.py
```

What each step does:

1. `verify_repository.py` compares the files listed in `FILE_SHA256.csv` with their recorded SHA-256 checksums. A missing or changed tracked file produces a failure; this script does **not** run the numerical analyses.
2. `restore_sadler_pairs.py` losslessly restores `data/processed/sadler_pairs.csv` from `sadler_pairs.csv.gz` and checks its SHA-256 checksum. If the CSV is already present with the correct checksum, it is left unchanged.
3. `project_guard.py` checks the fixed project identity and the hashes of the two original Macrostrat CSV files and `literature_review.csv`.
4. `verify_results.py` checks selected archived numerical outputs, including the column and hiatus counts, fitted exponents, ensemble size, preservation-efficiency medians, and inversion-scenario results. Passing this test establishes agreement with the archived numerical checkpoints **only**; it does not establish physical validity of the models.

**Important checksum note:** `FILE_SHA256.csv` also tracks `README.md`. If a repository maintainer legitimately updates this README or another tracked documentation file, its corresponding checksum and `size_bytes` entry must be updated. Do not change checksums for raw data or scientific outputs unless those files have genuinely been changed and the implications are documented. A failed integrity check must not be bypassed by altering scientific results.

## 5. Re-run the numerical workflow (optional)

The project provides the original computational scripts. Re-running them can overwrite archived output tables; perform this step in a **separate working copy** if you want to preserve the originally deposited outputs and their checksums.

First complete the environment setup and restore `sadler_pairs.csv` as described above. Then run, in order:

```bash
python src/data_processing.py
python src/analysis.py
python src/simulation.py
python src/inversion.py
python src/verify_results.py
```

The archived input files and random seeds are part of the reproducibility record. Exact output-file hashes and rendering may depend on the software environment. Do not replace manuscript results with outputs obtained after changing the model, parameters, data snapshot, or analysis rules.

### Regenerate the ten original computational figures

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

These scripts use the **original ten-figure code numbering**. The manuscript contains **nine main figures plus Supplementary Fig. S1**:

| Original plotting script | Manuscript designation |
|---|---|
| `figure_01.py` | Figure 1 |
| `figure_02.py` | Supplementary Fig. S1 |
| `figure_03.py`–`figure_10.py` | Figures 2–9, respectively |

See [`FIGURE_MAP.md`](FIGURE_MAP.md) for the individual output filenames and manuscript-image mapping. Archived manuscript figure images and newly rendered code figures need not be byte-for-byte identical; this does not by itself indicate changed numerical data.

## 6. Macrostrat source data: do not refresh for manuscript reproduction

The original stratigraphic observations were retrieved programmatically from the public [Macrostrat](https://macrostrat.org) database through its API and archived in:

```text
data/raw/macrostrat_columns_na.csv
data/raw/macrostrat_units_na.csv
```

**These archived CSVs are the inputs used for the reported manuscript results.** They are already present in the repository; there is no reason to download them again when reproducing the paper. The current live Macrostrat API may return different records.

The optional script `src/data_fetch.py` is intentionally protected against accidental execution. Running it without the confirmation flag exits with `SystemExit`; this is an **expected safeguard**, not evidence that the analysis workflow has failed.

Only if you deliberately want to retrieve a **new** Macrostrat snapshot, first back up the archived files and use a **separate working copy**:

```bash
python src/data_fetch.py --confirm-refresh-raw-data
```

**Warning:** This command contacts the live API and may overwrite `data/raw/macrostrat_columns_na.csv` and `data/raw/macrostrat_units_na.csv`. The resulting files may not match the archived checksums or manuscript results. The confirmation flag does not preserve the original files or guarantee a complete download. Do **not** use refreshed data in place of the manuscript snapshot when checking the reported results.

## 7. Data provenance, reuse, and citation

- **Macrostrat source:** Peters, S. E., Husson, J. M., and Czaplewski, J. (2018), “Macrostrat: A Platform for Geological Data Integration and Deep-Time Earth Crust Research,” *Geochemistry, Geophysics, Geosystems*, **19**, 1393–1409. https://doi.org/10.1029/2018GC007467
- **Software license:** The author's original Python code is distributed under the [MIT License](LICENSE). Third-party source datasets remain subject to their own applicable terms and attribution requirements; see [`SOURCE_AND_LICENSE.md`](SOURCE_AND_LICENSE.md).
- **Manuscript:** Please cite the associated *Earth-Science Reviews* manuscript when it becomes available as a published article. No publication DOI is claimed in this repository.
- **Code repository:** https://github.com/liuyunuo899/stratigraphic-hiatus-reproducibility

The repository is a numerical reproduction and transparency package. It does not provide new physical validation, formal power-law goodness-of-fit p-values, or posterior inference for the separate stochastic missing-deposition scenarios.
