# Contributing

Please keep changes reproducible and scoped to the canonical protocol.

Before opening a pull request:

```bash
python scripts/validate_package.py
python scripts/audit_canonical.py
python -m pytest -q
python scripts/smoke_test.py
```

Do not commit raw EEG, participant identifiers, participant-level prediction
files, checkpoints, or machine-specific absolute paths. If a result changes,
update the release version, `PROVENANCE.md`, the relevant summary table, and
`results/release_manifest.json` together.
