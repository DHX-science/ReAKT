# Manuscript linkage

The `source/` folder contains a clean copy of the manuscript source, table
inputs, figure PDFs, and the Elsevier class file corresponding to the canonical
manuscript. It excludes auxiliary files, logs, temporary renders, and compiled
submission PDFs.

Build from `paper/source/` with a LaTeX installation, for example:

```bash
cd paper/source
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode supplementary_figures.tex
pdflatex -interaction=nonstopmode supplementary_figures.tex
```

The manuscript and supplement are also maintained in the author's separate
submission directory; this copy is provided for provenance and convenience.
