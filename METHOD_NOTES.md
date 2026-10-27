# Reproduction-specific methodological notes

These notes distinguish **what the uploaded programs actually compute** from stronger scientific claims. They are based on the unchanged code and the user's current ESR manuscript.

1. **Data source.** `src/data_processing.py` uses the fixed Macrostrat CSV snapshot in `data/raw/`. The live fetch script `src/data_fetch.py` is not run for numerical reproduction. The archived data contain 949 column rows and 24,141 unit rows; 948 columns enter the summary.
2. **Empirical gaps and completeness.** Positive gaps are calculated from successive unit ages; `C(tau)` counts bins intersected by any retained unit. It does not propagate dated-boundary uncertainty or directly compute exact geologic time coverage.
3. **Power-law statistics.** `src/analysis.py` searches an `xmin` via a KS criterion, estimates a continuous-tail exponent, bootstraps the exponent with the chosen cutoff held fixed (1,000 replicates), and compares log-likelihoods with an exponential. No simulated absolute goodness-of-fit p-values or comprehensive lognormal/truncated alternatives are computed.
4. **Switching model.** `src/simulation.py` uses F1 Gaussian white noise, F2 sinusoidal periods 40/100/400/1200 kyr with noise, and F3 integrated Gaussian increments with noise. Default rates are `v_d = v_e = 0.2 m/kyr`, thresholds `theta_d = theta_e = 0.5`, duration 5 Myr and step 0.5 kyr. Master seed `20261020`.
5. **Unchanged layer bookkeeping.** Despite the LIFO description in its header, the actual erosion branch processes archived layers before a simultaneously open layer. Stored interval ends use the start time of the final deposition step, and partial erosion does not update the stored end age. Its temporal-bin algorithm counts the endpoint bin. Results reproduce **this implementation**, and no subsequent diagnostic version is substituted.
6. **Inverse illustration.** `src/inversion.py` computes four nonnegative smooth inversions (0.1, 1, 10, 100) and separately samples 5,000 hypothetical deposit-then-erode gap scenarios with probability 0.7 and exponential thickness. These scenario samples are **not a χ²-filtered posterior**, and the data in the submitted manuscript are not presented here as such.
7. **Interpretive matrix.** Original `src/figure_10.py` contains a pre-specified qualitative yes/partly/no matrix; it is not automatically estimated from the CSV files.

## What this repository does not contain

- No independent physical validation of the model's layer-age conventions.
- No additional LIFO, time-bin, or partial-erosion diagnostic scripts: those were exploratory checks kept outside the manuscript's numerical results.
- No fabricated correction of power-law p-values, bootstrap confidence limits, erosion histories or parameter estimates.

Please read these methodological constraints together with the limitations and data availability sections of the manuscript. Numerical reproducibility and substantive scientific validity are different questions.
