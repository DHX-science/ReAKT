"""Deterministic smoke test for the public ReAKT implementation."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from reakt.kernel import fit_reakt  # noqa: E402
from reakt.metrics import accuracy_from_scores  # noqa: E402


def main() -> None:
    rng = np.random.default_rng(20261113)
    source_y = np.tile([0, 1], 8)
    target_y = np.tile([0, 1], 6)
    source_odd = rng.normal(size=(len(source_y), 3, 4))
    source_even = rng.normal(size=(len(source_y), 3, 4))
    target_odd = rng.normal(size=(len(target_y), 3, 4))
    target_even = rng.normal(size=(len(target_y), 3, 4))
    support = np.array([0, 1, 2, 3, 4, 5], dtype=np.int64)
    query = np.arange(6, len(target_y), dtype=np.int64)
    scores = fit_reakt(
        source_odd, source_even, source_y,
        target_odd, target_even, target_y,
        support, query,
    )
    acc = accuracy_from_scores(scores, target_y[query])
    altered = target_y.copy()
    altered[query] = 1 - altered[query]
    scores_again = fit_reakt(
        source_odd, source_even, source_y,
        target_odd, target_even, altered,
        support, query,
    )
    if not np.allclose(scores, scores_again):
        raise AssertionError("query labels influenced the ReAKT fit")
    print(f"ReAKT smoke test passed; query accuracy={acc:.3f}; n_query={len(query)}")


if __name__ == "__main__":
    main()
