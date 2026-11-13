# Canonical result exports

These files are compact, human-readable summaries of the tables in
`paper/source/`. They are intentionally not participant-level prediction
exports.

| File | Manuscript source |
|---|---|
| `development_curve.csv` | `table_zero_shot_curve.tex` |
| `zero_shot_inference.csv` | `table_zero_shot_inference.tex` |
| `primary_controls.csv` | `table_m1_controls.tex` |
| `classical_fbcsp_summary.csv` | `table_classical_baselines.tex` |
| `fbcsp_inference.csv` | `table_fbcsp_inference.tex` |
| `development_backbones.csv` | `table_development_by_backbone.tex` |
| `external_backbones.csv` | `table_external_by_backbone.tex` |
| `external_protocols.csv` | `table_zero_shot_inference.tex` and `table_lajtos_loro.tex` |

The release manifest records SHA-256 hashes for the complete package. Run
`python scripts/audit_canonical.py` after modifying any summary or paper table.
