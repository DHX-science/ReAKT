"""Audit that public summaries still match the canonical paper tables."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from reakt.montage import validate_involution


ROOT = Path(__file__).resolve().parents[1]


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def close(actual: str, expected: float, tol: float = 1e-9) -> bool:
    return abs(float(actual) - expected) <= tol


def main() -> None:
    paper = ROOT / "paper" / "source"
    required = [
        paper / "main.tex",
        paper / "table_zero_shot_curve.tex",
        paper / "table_classical_baselines.tex",
        paper / "table_lajtos_loro.tex",
    ]
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise SystemExit("missing canonical paper source: " + ", ".join(missing))

    curve = rows(ROOT / "results" / "development_curve.csv")
    expected_curve = [
        ("0.20", 76.85, 77.26, -0.40),
        ("0.40", 79.04, 77.26, 1.78),
        ("0.60", 79.76, 77.26, 2.50),
        ("0.80", 80.26, 77.26, 3.00),
        ("1.00", 79.75, 77.26, 2.49),
    ]
    if len(curve) != len(expected_curve):
        raise SystemExit("development curve row count changed")
    for row, (support, reakt, zero, delta) in zip(curve, expected_curve):
        if row["support"] != support or not (
            close(row["reakt_c"], reakt)
            and close(row["me_only_zero_shot"], zero)
            and close(row["delta_vs_zero_shot"], delta)
        ):
            raise SystemExit(f"canonical curve mismatch at support {support}")

    curve_tex = (paper / "table_zero_shot_curve.tex").read_text(encoding="utf-8")
    for support, reakt, zero, delta in expected_curve:
        token = f"{support} & {reakt:.2f}"
        if token not in curve_tex:
            raise SystemExit(f"paper/table mismatch at support {support}")

    loro = rows(ROOT / "results" / "zero_shot_inference.csv")
    expected_loro = [("0.25", 75.16), ("0.50", 75.70), ("0.75", 75.86), ("1.00", 76.29)]
    loro_rows = [row for row in loro if row["protocol"] == "Lajtos-LORO"]
    if len(loro_rows) != len(expected_loro):
        raise SystemExit("LORO row count changed")
    loro_tex = (paper / "table_lajtos_loro.tex").read_text(encoding="utf-8")
    for row, (support, reakt) in zip(loro_rows, expected_loro):
        if row["support"] != support or not close(row["reakt_c"], reakt):
            raise SystemExit(f"LORO summary mismatch at support {support}")
        if f"{support} & {reakt:.2f}" not in loro_tex:
            raise SystemExit(f"paper/LORO mismatch at support {support}")

    fbcsp_tex = (paper / "table_fbcsp_inference.tex").read_text(encoding="utf-8")
    for token in ("50.97", "53.32", "59.68", "72.15"):
        if token not in fbcsp_tex:
            raise SystemExit(f"FBCSP canonical token missing: {token}")

    maps = json.loads((ROOT / "configs" / "channel_maps.json").read_text())
    eeg = maps["EEGMMIDB_64"]
    pairs = [tuple(pair) for pair in eeg["pairs"]]
    from reakt.montage import named_involution

    validate_involution(named_involution(eeg["channels"], pairs, eeg["fixed_points"]))
    validate_involution(maps["Lajtos2023_30"]["mapping"])
    print("canonical audit passed")


if __name__ == "__main__":
    main()
