# Data dictionary and units

This guide describes the **existing archived files**. It does not define or modify new observations.

## Inputs

| File | Important columns | Meaning |
|---|---|---|
| `data/raw/macrostrat_columns_na.csv` | `col_id`, `col_group`, `lat`, `lng` | North American column records and mapping/tectonic category keys |
| `data/raw/macrostrat_units_na.csv` | `col_id`, `t_age`, `b_age`, `max_thick` | Unit age boundaries (`Ma`), thickness (`m`) and column membership |
| `literature_review.csv` | `reference_key`, `year`, `title`, bibliographic/context fields | The selected 55-reference corpus required by `src/figure_02.py` |

Macrostrat geological ages are in Ma before present (larger ages are older). For positive hiatuses, `h = t_age(older lower unit) - b_age(younger upper unit)`.

## Processed real-data outputs

| File | Typical fields | Meaning |
|---|---|---|
| `columns_summary.csv` | `col_id`, `setting`, `duration`, `n_units`, `total_thick`, `n_hiatus` | Per-column stratigraphic summary |
| `hiatuses.csv` | `col_id`, `setting`, `hiatus_myr` | Strictly positive adjacent-unit time gaps (Myr) |
| `completeness.csv` | `col_id`, `setting`, `tau`, `completeness` | Fraction of occupied time bins at resolution `tau` (Myr) |
| `sadler_pairs.csv.gz` | `col_id`, `setting`, `timespan_myr`, `rate_m_per_myr` | Archived pairwise accumulation-rate observations; gzip must be restored to `sadler_pairs.csv` |
| `sadler_summary.csv` | `setting`, `timespan_mid`, `rate_median`, `rate_q25`, `rate_q75`, `n` | Aggregated accumulation rates and interquartile ranges |
| `hiatus_powerlaw_fits.csv` | `setting`, `xmin`, `alpha`, `alpha_lo`, `alpha_hi`, `n_tail`, `llr_powerlaw_vs_exp` | Candidate power-law tail fits; not full goodness-of-fit acceptance |

Here `completeness` means **time-bin occupancy**: a bin is counted when any preserved unit intersects that bin. It is not the exact within-bin fraction of represented time.

## Synthetic outputs

| File | Important fields | Meaning |
|---|---|---|
| `ensemble_runs.csv` | `kind`, `run`, `M_gross`, `M_final`, `P`, `n_layers`, `C_...` | 600 baseline synthetic runs; `P = M_final/M_gross` |
| `ensemble_hiatuses.csv` | `kind`, `run`, `hiatus_myr` | Positive synthetic gaps reported by the original layer-age algorithm |
| `sensitivity_sweep.csv` | `kind`, `theta`, `ve_over_vd`, `P_med`, `P_q25`, `P_q75`, `n_hiat_med` | 36 combination summaries (50 runs per combination) |
| `inversion_observations.csv` | `t_obs`, `z_obs`, `sigma_t`, `sigma_z` | 25 noisy-age synthetic observations and error scales |
| `inversion_curves.csv` | `lam`, `t`, `rate` | Four nonnegative Tikhonov-smoothed rates sampled on a time grid |
| `inversion_ensemble.csv` | `M_gross`, `P` | 5,000 stochastic *gap-fill* scenarios, separate from the Tikhonov solutions |

In the synthetic model the time step is 0.5 kyr over 5 Myr. Deposition and erosion rates are in metres per kyr. Unless noted, stored synthetic hiatus durations and `tau` are in Myr, while figures can convert those values into kyr for axis labels.
