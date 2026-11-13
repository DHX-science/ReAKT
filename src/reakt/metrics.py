"""Small evaluation helpers."""

from __future__ import annotations

import numpy as np


def accuracy_from_scores(scores: np.ndarray, labels: np.ndarray) -> float:
    scores = np.asarray(scores, dtype=np.float64)
    labels = np.asarray(labels, dtype=np.int64)
    if scores.ndim != 1 or labels.shape != scores.shape:
        raise ValueError("scores and labels must be matching 1-D arrays")
    return float(np.mean((scores >= 0).astype(np.int64) == labels))
