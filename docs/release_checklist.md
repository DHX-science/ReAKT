# GitHub release checklist

- [ ] Replace the placeholder GitHub URL in `CITATION.cff`.
- [ ] Add the final manuscript DOI when it exists.
- [ ] Run `python scripts/validate_package.py`.
- [ ] Run `python -m pytest -q`.
- [ ] Run `python scripts/smoke_test.py`.
- [ ] Check that no raw EEG, participant-level prediction, or checkpoint file
      has been added.
- [ ] Update the version in `pyproject.toml` and `CITATION.cff` for every new
      canonical result export.
- [ ] Regenerate `results/release_manifest.json` after any source or result
      change.
