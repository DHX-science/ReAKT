"""Task-specific channel involutions.

The map is part of the experiment definition. It must be a permutation and an
involution (`map[map[i]] == i`); otherwise the paired representation is not the
one used by ReAKT.
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence

import numpy as np


def validate_involution(mapping: Sequence[int], n_channels: int | None = None) -> np.ndarray:
    """Validate and return an integer involution map."""
    mapping = np.asarray(mapping, dtype=np.int64)
    if mapping.ndim != 1:
        raise ValueError("mapping must be one-dimensional")
    n = len(mapping) if n_channels is None else int(n_channels)
    if len(mapping) != n:
        raise ValueError("mapping length does not equal n_channels")
    if not np.array_equal(np.sort(mapping), np.arange(n)):
        raise ValueError("mapping must be a permutation of channel indices")
    if not np.array_equal(mapping[mapping], np.arange(n)):
        raise ValueError("mapping must be an involution")
    return mapping


def apply_involution(x: np.ndarray, mapping: Sequence[int]) -> np.ndarray:
    """Apply a channel map to an array shaped ``[..., channel, time]``."""
    x = np.asarray(x)
    mapping = validate_involution(mapping, x.shape[-2])
    return np.take(x, mapping, axis=-2)


def named_involution(
    channel_names: Iterable[str],
    pairs: Iterable[tuple[str, str]],
    fixed_points: Iterable[str] = (),
) -> np.ndarray:
    """Build an involution from channel names and reciprocal pairs."""
    names = tuple(str(name) for name in channel_names)
    lookup = {name: index for index, name in enumerate(names)}
    mapping = np.arange(len(names), dtype=np.int64)
    seen: set[str] = set()
    for left, right in pairs:
        if left not in lookup or right not in lookup:
            raise ValueError(f"pair contains an unknown channel: {left}, {right}")
        if left == right:
            raise ValueError("a pair must contain two different channels")
        if left in seen or right in seen:
            raise ValueError("a channel appears in more than one pair")
        mapping[lookup[left]] = lookup[right]
        mapping[lookup[right]] = lookup[left]
        seen.update((left, right))
    for name in fixed_points:
        if name not in lookup:
            raise ValueError(f"unknown fixed-point channel: {name}")
        seen.add(name)
    if seen != set(names):
        missing = sorted(set(names) - seen)
        raise ValueError(f"every channel must be paired or fixed; missing={missing}")
    return validate_involution(mapping)
