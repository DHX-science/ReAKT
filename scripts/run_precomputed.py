"""Run one ReAKT fold from a precomputed feature NPZ."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from reakt.kernel import fit_reakt  # noqa: E402
from reakt.metrics import accuracy_from_scores  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--private-weight", type=float, default=0.25)
    parser.add_argument("--ridge", type=float, default=1.0)
    args = parser.parse_args()
    with np.load(args.input, allow_pickle=False) as z:
        required = {
            "source_odd", "source_even", "source_y",
            "target_odd", "target_even", "target_y",
            "support_idx", "query_idx",
        }
        missing = sorted(required.difference(z.files))
        if missing:
            raise SystemExit(f"missing NPZ fields: {', '.join(missing)}")
        arrays = {name: z[name] for name in required}
    scores = fit_reakt(
        arrays["source_odd"], arrays["source_even"], arrays["source_y"],
        arrays["target_odd"], arrays["target_even"], arrays["target_y"],
        arrays["support_idx"], arrays["query_idx"],
        private_weight=args.private_weight, ridge=args.ridge,
    )
    labels = arrays["target_y"][arrays["query_idx"]]
    payload = {
        "method": "ReAKT-C",
        "input": str(args.input),
        "private_weight": args.private_weight,
        "ridge": args.ridge,
        "n_source": int(len(arrays["source_y"])),
        "n_target": int(len(arrays["target_y"])),
        "n_support": int(len(arrays["support_idx"])),
        "n_query": int(len(arrays["query_idx"])),
        "accuracy": accuracy_from_scores(scores, labels),
        "scores": scores.tolist(),
        "query_labels": labels.tolist(),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps({k: payload[k] for k in ("method", "accuracy", "n_support", "n_query")}, indent=2))


if __name__ == "__main__":
    main()
