"""Algebraic paired representation used by ReAKT."""

from __future__ import annotations

import numpy as np


def paired_representation(
    h: np.ndarray, h_reflected: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Return the odd and even projections of a feature/reflection pair.

    Parameters
    ----------
    h, h_reflected:
        Arrays with identical shape ``[trial, feature_channel, token]``.
        ``h_reflected`` is produced by applying the task-specific channel map
        before the frozen backbone, then extracting features with the same
        backbone and normalization statistics.
    """
    h = np.asarray(h, dtype=np.float64)
    h_reflected = np.asarray(h_reflected, dtype=np.float64)
    if h.shape != h_reflected.shape or h.ndim != 3:
        raise ValueError("h and h_reflected must have the same 3-D shape")
    return (h - h_reflected) / 2.0, (h + h_reflected) / 2.0
