# Public EEG repository audit

The following public repositories were used as organizational references for
the ReAKT release. They are not dependencies of ReAKT and no source code,
data, or weights are copied from them.

| Project | URL | Observed organization | ReAKT packaging decision |
|---|---|---|---|
| FBMSNet | https://github.com/deep-bci/FBMSNet | README with architecture and result figure; `codes/`, `environment.txt`, instructions, and bundled dataset files | Keep a concise README, separate source/config/results, and exclude bundled data |
| SincMSNet | https://github.com/Want2Vanish/SincMSNet | README with architecture, environment instructions, training code, and result figure; uses an older Python/PyTorch environment | Record runtime requirements explicitly, but use a modern portable core interface |
| MSVTNet | https://github.com/SheepTAO/MSVTNet | Top-level training code, `environment.yml`, dependency on the `dpeeg` package, and an `out/` result tree with a supporting document | Separate runnable scripts from result exports and describe external dependencies rather than vendoring them |
| DMSANet | https://github.com/xingxin-99/DMSANet | PyTorch source, FBCSP implementation, environment/requirements files, visualization scripts, and model initialization files | Include tests and result manifests, but exclude third-party checkpoints and raw data |

The repositories differ in license metadata, runtime age, data packaging, and
whether detailed results are stored as images, spreadsheets, or output trees.
The ReAKT package therefore uses a deliberately smaller public boundary:
method core, portable configs, explicit input schema, tests, and compact
canonical summaries.
