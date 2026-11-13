# Configuration files

The JSON files in this directory are portable descriptions of the canonical
paper protocols. They are intentionally free of local paths. The exact
channel orders and reciprocal maps are kept separately in
`channel_maps.json` so that montage validation can happen before feature
extraction.

The values here describe the paper's data and preprocessing version; they do
not download data or train a backbone. A local raw-EEG adapter should read the
same fields and write the frozen-feature NPZ schema in
`docs/feature_schema.md`.
