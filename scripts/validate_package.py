"""Check the data-free release before publishing it."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    forbidden_suffixes = {
        ".pt", ".pth", ".ckpt", ".fif", ".gdf", ".mat", ".edf",
        ".npz", ".npy", ".pkl", ".pickle",
    }
    bad = []
    for path in ROOT.rglob("*"):
        if path.is_file() and (path.suffix.lower() in forbidden_suffixes
                               or path.name.endswith(".tar.gz")):
            bad.append(str(path.relative_to(ROOT)))
    if bad:
        raise SystemExit("forbidden data/checkpoint files: " + ", ".join(bad))

    manifest = json.loads((ROOT / "results" / "result_manifest.json").read_text())
    for name in manifest["tables"]:
        path = ROOT / "results" / name
        if not path.exists():
            raise SystemExit(f"manifest table is missing: {name}")
        pd.read_csv(path)
    print("release validation passed")
    print(f"files checked: {sum(p.is_file() for p in ROOT.rglob('*'))}")


if __name__ == "__main__":
    main()
