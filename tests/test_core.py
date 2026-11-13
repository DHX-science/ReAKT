from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from reakt.kernel import fit_reakt, orbit_kernels  # noqa: E402
from reakt.montage import apply_involution, named_involution  # noqa: E402
from reakt.representation import paired_representation  # noqa: E402


def test_paired_representation_is_invertible():
    rng = np.random.default_rng(1)
    h = rng.normal(size=(5, 2, 3))
    hr = rng.normal(size=(5, 2, 3))
    odd, even = paired_representation(h, hr)
    assert np.allclose(odd + even, h)
    assert np.allclose(even - odd, hr)


def test_odd_kernel_changes_sign_under_reflection():
    rng = np.random.default_rng(2)
    so = rng.normal(size=(6, 2, 3))
    se = rng.normal(size=(6, 2, 3))
    to = rng.normal(size=(4, 2, 3))
    te = rng.normal(size=(4, 2, 3))
    ko, _ = orbit_kernels(so, se, to, te)
    ko_flip, _ = orbit_kernels(so, se, -to, te)
    assert np.allclose(ko_flip[-len(to):, :len(so)], -ko[-len(to):, :len(so)])


def test_query_labels_do_not_change_scores():
    rng = np.random.default_rng(3)
    sy = np.tile([0, 1], 5)
    ty = np.tile([0, 1], 5)
    so = rng.normal(size=(10, 2, 3))
    se = rng.normal(size=(10, 2, 3))
    to = rng.normal(size=(10, 2, 3))
    te = rng.normal(size=(10, 2, 3))
    support = np.array([0, 1, 2, 3])
    query = np.arange(4, 10)
    first = fit_reakt(so, se, sy, to, te, ty, support, query)
    changed = ty.copy()
    changed[query] = 1 - changed[query]
    second = fit_reakt(so, se, sy, to, te, changed, support, query)
    assert np.allclose(first, second)


def test_named_montage_map_is_reciprocal():
    names = ("L1", "R1", "M")
    mapping = named_involution(names, (("L1", "R1"),), ("M",))
    x = np.arange(6).reshape(1, 3, 2)
    assert mapping.tolist() == [1, 0, 2]
    assert np.array_equal(apply_involution(x, mapping), x[:, [1, 0, 2], :])
