# Provenance, attribution and code ownership

## Code ownership and publication

The repository owner has **confirmed that the Python source code in this project is their own work** and has authorised its publication in a public GitHub repository. There is **no outstanding third-party authorisation check for the author's own Python scripts**. The scientific scripts are shared in their archived form, without changing calculation methods, parameters or results.

This publication package does not automatically grant a software licence. **No `LICENSE` file has yet been selected.** Public availability on GitHub permits the files to be viewed and downloaded according to GitHub's applicable terms, but it is not the same as an explicit open-source permission to modify and redistribute the software. If the owner wants to grant those reuse rights, they may select an open-source licence (for example, MIT) separately. Such a licence should cover only material for which the owner controls the rights, and it does not automatically relicense third-party datasets or publications.

## Third-party data attribution

The two original stratigraphic input CSV files are a fixed snapshot derived from the public **Macrostrat** database. Please credit Macrostrat and its associated publication: Peters, S. E., Husson, J. M., and Czaplewski, J. (2018), *Macrostrat: A Platform for Geological Data Integration and Deep-Time Earth Crust Research*, *Geochemistry, Geophysics, Geosystems*, 19, 1393–1409, https://doi.org/10.1029/2018GC007467.

Ownership of the Python code does **not** replace applicable Macrostrat data attribution or licensing conditions. The repository owner should follow the data provider's terms when publishing copies of those fixed source datasets. The bibliographic entries in `literature_review.csv` identify published third-party works; this repository does not grant new rights to their original publications.

## Archive provenance and restored inputs

The repository was assembled from the author's `1(3).zip` project, including Python scripts, the fixed Macrostrat snapshot, the previously computed empirical and synthetic tables, figures, and the corresponding `ESR_Manuscript.docx` / `ESR_Supplement.docx` materials used for figure mapping.

The archive initially lacked `PROJECT_ID.txt` and `literature_review.csv`, which are required by `src/project_guard.py`. `PROJECT_ID.txt` was restored using the identity string declared in the original script. The 55-entry `literature_review.csv` was restored from the same earlier project materials, with its exact bytes matching the original script's locked SHA-256 digest. No bibliography entry was invented or edited to satisfy the lock.

## Manuscript and figure boundaries

The Word manuscript files are **not distributed** in this code/data repository. `figures/submission/` contains figure PNG files extracted without alteration from the supplied manuscript documents to retain the submission figure crosswalk. The originally computed figures remain under `figures/`.

## Reproducibility integrity

The author's original scientific Python scripts and preserved numerical outputs are retained **byte-for-byte**. Only packaging material was added: project identity and locked literature input recovery, explanatory documents, lossless gzip data compression, restored-data/checksum helper scripts and submitted-figure extracts. `FILE_SHA256.csv` records the packaged file digests. Exploratory algorithm-diagnostic results were not substituted for the study's original reported results.
