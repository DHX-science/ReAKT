# ReAKT: task-structured antisymmetric ME-to-MI transfer

This repository contains the reproducible implementation of **ReAKT** and the
small, inspectable evaluation interface used for the accompanying manuscript.
The public package is data-free: it contains source code, protocol files,
summary results, and tests, but no EEG recordings, participant identifiers, or
trained checkpoints.

ReAKT accepts frozen ME and MI feature pairs produced by a task-structured
channel involution. For each trial, the paired features are decomposed into

\[
z^-=(h-h_R)/2,\qquad z^+=(h+h_R)/2.
\]

The odd component is read out with an antisymmetric RBF kernel. A domain-private
even RBF kernel is fitted on the labelled MI support and can provide the small
target correction used by ReAKT-C. The outer query labels are never used for a
fit, normalization statistic, bandwidth, or gate.

## Repository layout

```text
ReAKT_open_source/
├── configs/                 # portable experiment specifications
├── docs/                    # protocol, data layout, and reference audit
├── figures/                 # figure-generation entry point and notes
├── paper/                   # manuscript packaging notes only
├── results/                 # small, auditable summary exports
├── scripts/                 # runnable smoke, prediction, and summary scripts
├── src/reakt/               # core implementation
├── tests/                   # deterministic unit and smoke tests
├── CITATION.cff
├── LICENSE
├── pyproject.toml
└── requirements.txt
```

## Installation

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install -e .
```

Run the tests:

```bash
python -m pytest -q
```

Before publishing a release, run the data and manifest check:

```bash
python scripts/validate_package.py
```

To verify that the public summaries still match the canonical manuscript
version, run:

```bash
python scripts/audit_canonical.py
```

## Minimal smoke run

The smoke script creates deterministic synthetic ME/MI features, fits the
same ReAKT kernel used by the paper, and verifies prediction and query-label
non-interference.

```bash
python scripts/smoke_test.py
```

## Running on precomputed features

The public runner is intentionally based on precomputed frozen features. This
keeps the method implementation independent of a particular EEG backbone and
makes the query boundary explicit. An input NPZ must contain:

```text
source_odd, source_even, source_y,
target_odd, target_even, target_y,
support_idx, query_idx
```

with feature arrays shaped `[trial, feature_channel, token]` and integer binary
labels. Run:

```bash
python scripts/run_precomputed.py \
  --input path/to/fold_features.npz \
  --output outputs/fold_00.json
```

The script writes predictions, accuracy, support/query counts, and the exact
kernel settings used for the run. See `docs/reproduction.md` for the full
EEGMMIDB and Lajtos protocol and the adapter boundary for reproducing the
frozen-backbone feature export.

## Canonical result identity

The summary exports in `results/` are copied from the manuscript's canonical
tables and are not recomputed from hidden or private files. The primary
development protocol uses 104 EEGMMIDB participants, five matched outer folds,
and MI support fractions 0.20, 0.40, 0.60, 0.80, and 1.00. The external Lajtos
protocol uses the ordinary five-fold and strict three-fold leave-one-run-out
analyses described in `docs/protocol.md`.

The canonical EEGMMIDB EEGNet values at 0.20 support are ReAKT-C 76.85% and
ME-only zero-shot 77.26%. These are summary values; the repository does not
claim that a summary CSV replaces the original participant-level data.

The exact EEGMMIDB and Lajtos channel orders and involution maps are recorded
in `configs/channel_maps.json`. The frozen-feature input contract is documented
in `docs/feature_schema.md`, so a local raw-EEG adapter can be checked against
the same channel map before feature extraction.

## Data and checkpoints

The raw datasets and ME-pretrained checkpoints are not redistributed here.
Follow the dataset licenses and the acquisition-specific preprocessing rules
in `docs/data_access.md`. Place local data and checkpoints outside the Git
repository and pass paths through a local configuration file or command-line
argument.

## Reference implementations

The package organization was informed by the public FBMSNet, SincMSNet,
MSVTNet, and DMSANet repositories. They are listed and audited in
`docs/reference_repositories.md`. No third-party source code, data, or weights
are copied into this repository.
