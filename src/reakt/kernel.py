"""Closed-form ReAKT kernel read-out.

This module is the small, dependency-light implementation of the method used
after frozen feature extraction. It follows the canonical settings in the
manuscript: source-derived median bandwidths, source diagonal normalization,
an antisymmetric shared odd kernel, a domain-private even kernel, private
weight 0.25, and ridge 1.0.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


def distance_squared(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    xnorm = np.sum(x * x, axis=1)
    ynorm = np.sum(y * y, axis=1)
    return np.maximum(xnorm[:, None] + ynorm[None, :] - 2.0 * (x @ y.T), 0.0)


def source_bandwidths(source: np.ndarray) -> np.ndarray:
    """Compute one median pairwise bandwidth per feature channel."""
    source = np.asarray(source, dtype=np.float64)
    if source.ndim != 3 or len(source) < 3:
        raise ValueError("source must have shape [trial, channel, token] and >=3 trials")
    result = np.empty(source.shape[1], dtype=np.float64)
    for channel in range(source.shape[1]):
        distances = distance_squared(source[:, channel, :], source[:, channel, :])
        upper = distances[np.triu_indices(len(source), 1)]
        result[channel] = max(float(np.median(upper)), 1e-8)
    return result


def orbit_kernels(
    source_odd: np.ndarray,
    source_even: np.ndarray,
    target_odd: np.ndarray,
    target_even: np.ndarray,
    odd_bandwidth: np.ndarray | None = None,
    even_bandwidth: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Construct normalized shared odd and domain-private even Gram matrices."""
    source_odd = np.asarray(source_odd, dtype=np.float64)
    source_even = np.asarray(source_even, dtype=np.float64)
    target_odd = np.asarray(target_odd, dtype=np.float64)
    target_even = np.asarray(target_even, dtype=np.float64)
    if source_odd.ndim != 3 or source_odd.shape != source_even.shape:
        raise ValueError("source odd/even features must have matching 3-D shapes")
    if target_odd.ndim != 3 or target_odd.shape != target_even.shape:
        raise ValueError("target odd/even features must have matching 3-D shapes")
    if source_odd.shape[1:] != target_odd.shape[1:]:
        raise ValueError("source and target feature geometry must match")
    if odd_bandwidth is None:
        odd_bandwidth = source_bandwidths(source_odd)
    if even_bandwidth is None:
        even_bandwidth = source_bandwidths(source_even)
    odd_bandwidth = np.asarray(odd_bandwidth, dtype=np.float64)
    even_bandwidth = np.asarray(even_bandwidth, dtype=np.float64)

    odd = np.concatenate([source_odd, target_odd], axis=0)
    even = np.concatenate([source_even, target_even], axis=0)
    ko = np.zeros((len(odd), len(odd)), dtype=np.float64)
    ke = np.zeros_like(ko)
    for channel in range(odd.shape[1]):
        values = odd[:, channel, :]
        same = distance_squared(values, values)
        opposite = distance_squared(values, -values)
        ko += 0.5 * (
            np.exp(-same / (2.0 * odd_bandwidth[channel]))
            - np.exp(-opposite / (2.0 * odd_bandwidth[channel]))
        ) / odd.shape[1]
        values_even = even[:, channel, :]
        ke += np.exp(
            -distance_squared(values_even, values_even)
            / (2.0 * even_bandwidth[channel])
        ) / even.shape[1]

    n_source = len(source_odd)
    odd_scale = max(float(np.mean(np.diag(ko)[:n_source])), 1e-8)
    even_scale = max(float(np.mean(np.diag(ke)[:n_source])), 1e-8)
    ko, ke = ko / odd_scale, ke / even_scale
    if not np.isfinite(ko).all() or not np.isfinite(ke).all():
        raise RuntimeError("non-finite ReAKT kernel")
    return ko, ke


@dataclass
class ReAKTModel:
    """Fitted ReAKT-C predictor for one outer fold."""

    private_weight: float = 0.25
    ridge: float = 1.0
    _alpha: np.ndarray | None = None
    _intercept: float = 0.0
    _n_source: int = 0
    _train_ids: np.ndarray | None = None
    _query_kernel: np.ndarray | None = None

    def fit(
        self,
        ko: np.ndarray,
        ke: np.ndarray,
        n_source: int,
        source_y: np.ndarray,
        target_y: np.ndarray,
        support_idx: np.ndarray,
    ) -> "ReAKTModel":
        """Fit on all ME source trials and labelled MI support trials."""
        ko = np.asarray(ko, dtype=np.float64)
        ke = np.asarray(ke, dtype=np.float64)
        source_y = np.asarray(source_y, dtype=np.int64)
        target_y = np.asarray(target_y, dtype=np.int64)
        support_idx = np.asarray(support_idx, dtype=np.int64)
        if ko.shape != ke.shape or ko.ndim != 2 or ko.shape[0] != ko.shape[1]:
            raise ValueError("ko and ke must be square matrices with equal shape")
        if n_source != len(source_y):
            raise ValueError("n_source must equal the number of source labels")
        if len(target_y) + n_source != ko.shape[0]:
            raise ValueError("kernel size does not match source and target trials")
        if set(np.unique(target_y[support_idx]).tolist()) != {0, 1}:
            raise ValueError("support must contain both target classes")

        source_ids = np.arange(n_source, dtype=np.int64)
        target_ids = n_source + support_idx
        train_ids = np.concatenate([source_ids, target_ids])
        domain_train = np.concatenate([
            np.zeros(n_source, dtype=np.int8),
            np.ones(len(support_idx), dtype=np.int8),
        ])
        shared_train = ko[np.ix_(train_ids, train_ids)]
        private_train = ke[np.ix_(train_ids, train_ids)] * (
            domain_train[:, None] == domain_train[None, :]
        )
        kernel_train = shared_train + self.private_weight * private_train
        labels = np.concatenate([
            2 * source_y - 1,
            2 * target_y[support_idx] - 1,
        ]).astype(np.float64)
        matrix = kernel_train + self.ridge * np.eye(len(train_ids))
        inverse = np.linalg.inv(matrix)
        self._alpha = inverse @ labels
        diagonal = np.diag(inverse)[n_source:]
        if len(diagonal) == 0 or np.min(diagonal) <= 0.0:
            raise RuntimeError("nonpositive support LOO precision diagonal")
        self._intercept = float(np.mean(self._alpha[n_source:] / diagonal))
        self._n_source = n_source
        self._train_ids = train_ids
        return self

    def predict(
        self,
        ko: np.ndarray,
        ke: np.ndarray,
        target_query_idx: np.ndarray,
    ) -> np.ndarray:
        """Return signed scores for target indices excluded from fitting."""
        if self._alpha is None or self._train_ids is None:
            raise RuntimeError("fit must be called before predict")
        query_idx = np.asarray(target_query_idx, dtype=np.int64)
        query_ids = self._n_source + query_idx
        shared_query = ko[np.ix_(query_ids, self._train_ids)]
        private_query = np.zeros_like(shared_query)
        support_cols = self._train_ids[self._n_source:]
        if len(support_cols):
            private_query[:, self._n_source:] = ke[np.ix_(query_ids, support_cols)]
        kernel_query = shared_query + self.private_weight * private_query
        scores = kernel_query @ self._alpha + self._intercept
        if scores.shape != query_idx.shape or not np.isfinite(scores).all():
            raise RuntimeError("invalid ReAKT prediction")
        return scores


def fit_reakt(
    source_odd: np.ndarray,
    source_even: np.ndarray,
    source_y: np.ndarray,
    target_odd: np.ndarray,
    target_even: np.ndarray,
    target_y: np.ndarray,
    support_idx: np.ndarray,
    query_idx: np.ndarray,
    *,
    private_weight: float = 0.25,
    ridge: float = 1.0,
) -> np.ndarray:
    """Fit ReAKT-C and return signed scores for the held-out target query."""
    ko, ke = orbit_kernels(source_odd, source_even, target_odd, target_even)
    model = ReAKTModel(private_weight=private_weight, ridge=ridge)
    model.fit(ko, ke, len(source_y), source_y, target_y, support_idx)
    if np.intersect1d(support_idx, query_idx).size:
        raise ValueError("support and query overlap")
    return model.predict(ko, ke, query_idx)
