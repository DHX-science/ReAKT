# Reproducing the manuscript exports

1. Install the package and run `python scripts/smoke_test.py`.
2. Obtain the two datasets from their original sources.
3. Recreate the frozen ME backbone feature export using the acquisition-specific
   preprocessing and the split seeds in `configs/`.
4. Write one NPZ per outer fold with the schema in `README.md`.
5. Run `scripts/run_precomputed.py` for each fold.
6. Aggregate only outer-query predictions. Do not average fold accuracies when
   the manuscript protocol requires pooled subject-level predictions.

The current repository includes compact canonical summary CSVs so that the
reported values can be inspected without distributing participant-level data.
The `result_manifest.json` records exactly what is and is not included.
