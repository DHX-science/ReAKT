# ReAKT provenance

## Scientific source

The public summaries and paper source were taken from the canonical audited
submission directory:

`neurocomputing_submission_ReAKT_revision_D11_20261112_final_audited`

The package does not combine values from earlier ROSR/CPER, RSKT, EA, or audit
exports. The manuscript tables copied into `paper/source/` are the source of
truth for the CSV summaries in `results/`.

## Frozen definitions

The release preserves the following definitions:

1. ReAKT uses the odd/even projections of a frozen ME feature and its reflected
   view.
2. The odd kernel is antisymmetric and the even kernel is domain-private.
3. Bandwidths and the ridge fit are estimated without outer-query labels.
4. EEGMMIDB uses the 104-participant canonical inclusion set and the 64-channel
   map in `configs/channel_maps.json`.
5. Lajtos uses all 31 released participants and the 30-channel map in the same
   file.
6. Reported result CSVs retain the manuscript's displayed values and protocol
   labels, including the distinction between ordinary five-fold and strict
   LORO analyses.

## Verification performed for this release

- Core unit tests pass.
- Synthetic query-label non-interference smoke test passes.
- Result manifest tables parse successfully.
- Forbidden raw-data and checkpoint extensions are absent.
- Absolute local paths are absent from package text files.
- Clean manuscript and supplement sources compile successfully before build
  artifacts are removed from the release tree.

## Reference repositories

FBMSNet, SincMSNet, MSVTNet, and DMSANet informed repository organization only.
Their code, datasets, and weights are not dependencies or contents of this
release; the audit is recorded in `docs/reference_repositories.md`.
