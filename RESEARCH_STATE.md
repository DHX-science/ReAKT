# ReAKT release state

## Current package

This release is the data-free public package corresponding to the manuscript
source copied under `paper/source/`. The canonical method settings are private
even-kernel weight `0.25`, ridge `1.0`, source-derived median bandwidths, and
the task-specific involution maps recorded in `configs/channel_maps.json`.

## Canonical protocols

- EEGMMIDB development: 104 included participants, 64 channels, five matched
  outer folds, MI support fractions 0.20--1.00.
- EEGMMIDB held-out-run: the same 104 participants and three complete MI-run
  queries.
- Lajtos 2023 ordinary external analysis: 31 participants, 30 channels,
  five trial-stratified folds, support fractions 0.25--1.00.
- Lajtos 2023 strict external sensitivity: all 31 participants, three
  run-disjoint folds.

## Evidence boundary

The package provides the exact closed-form ReAKT read-out, the montage maps,
portable protocol definitions, canonical summary exports, and tests. Raw EEG,
participant-level predictions, and ME checkpoints remain outside the release.
The public runner therefore starts from the frozen feature boundary described
in `docs/reproduction.md`.

## Release rule

Any future result update must change the release version and update
`PROVENANCE.md` and `results/release_manifest.json`; historical summary values
must not be silently overwritten.
