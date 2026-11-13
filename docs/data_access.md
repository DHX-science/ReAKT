# Data and local paths

This repository does not redistribute EEG data or participant-level files.
Obtain EEGMMIDB and the Lajtos 2023 recordings from their original sources and
follow the terms that accompany each dataset. Prepare local feature exports
outside this repository and pass them to `scripts/run_precomputed.py`.

The public runner expects the feature-level NPZ schema documented in the main
README. A local adapter may read raw EEG, apply the dataset-specific
preprocessing and frozen backbone, construct the task-specific channel map,
and then write that schema. Do not commit raw recordings, participant
metadata, checkpoints, or absolute local paths.
