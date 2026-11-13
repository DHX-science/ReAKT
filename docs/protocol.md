# ReAKT reproduction protocol

## EEGMMIDB development

The development protocol contains 104 participants, 64 EEG channels, a 160 Hz
sampling rate, and 0--4 s post-cue epochs. ME source runs are R03, R07, and R11;
MI target runs are R04, R08, and R12. The MI target data are partitioned into
five matched outer folds within subject. The support fractions are 0.20, 0.40,
0.60, 0.80, and 1.00. At each fraction, the selected labelled MI support is
combined with all permitted ME source trials; the outer query is scored only
after the fit is complete.

The primary feature export uses a frozen ME-supervised EEGNet backbone. The
channel involution is applied before the same source-fitted standardizer and
backbone are used to produce `h` and `h_R`. The public core package begins at
the resulting paired feature boundary.

## Lajtos 2023 external evaluation

The external evaluation uses 31 participants and 30 exposed channels. The
ordinary protocol is a stratified five-fold analysis. The strict protocol is a
three-fold leave-one-run-out analysis with run-disjoint queries. Support
fractions are 0.25, 0.50, 0.75, and 1.00. The two protocols are summarized
separately because they have different query boundaries.

## Query boundary

For every fold, the following quantities are fit using only ME source trials and
labelled MI support trials: feature normalization, source bandwidths, kernel
parameters, ridge solution, and support LOO intercept. Query labels are used
only to compute evaluation metrics. The unit tests include a query-label
non-interference check.

## ReAKT settings

The canonical settings are private even-kernel weight `0.25` and ridge
regularization `1.0`. Bandwidths are source-derived median pairwise squared
distances, and the odd and even Gram matrices are normalized by their source
diagonal means. These settings are recorded in the JSON configurations and in
each runner output.
