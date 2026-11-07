# The Seifert–van Kampen theorem, after TauCeti

An informal account, without proofs, of the definitions and results on which the theorem
`TauCeti.isPushout_fundamentalGroup` depends in the Lean library [TauCeti](https://github.com/TauCetiProject/TauCeti) at
commit `37f5e9dce5ac83d2825198ac72d7f5d64eb26c85`. Each numbered statement, and each lettered part of one, is
a box in the PDF linked to the Lean declaration that states it.

[Read the annotated text](https://mathlib-initiative.github.io/seifert-van-kampen-tauceti/pdf-overlay/viewer/index.html) ·
[Download the PDF](https://github.com/mathlib-initiative/seifert-van-kampen-tauceti/releases/download/v1/svk-tauceti.pdf) ·
[Browse the annotations](annotations/)

- `informal/`: the LaTeX source. `main.tex` is the document, `sections/` its sections,
  `items.json` the table of items and their declarations, `STYLE.md` and
  `STYLE-project.md` the rules it is written to.
- `annotations/`: the links from each box of the PDF to the Lean declarations, in the
  Literature Links format.
- `pdf-overlay/`: the viewer that shows the PDF with those links.

The annotations use [Literature Links](https://github.com/mathlib-initiative/literature-links).
The viewer and validation tools need Python 3.11 or later. From a fresh clone:

```sh
python3 pdf-overlay/tools/check_generated.py
python3 pdf-overlay/tools/serve.py --build
```

The viewer fetches the published PDF and verifies its SHA-256 before serving it locally.

Build the PDF from this directory with TeX Live (pdflatex, latexmk):

```sh
bash informal/tools/build_pdf.sh build/pdf
```

Two builds on one TeX installation give the same bytes; the published PDF is the one whose
sha256 the annotations pin.

The text and the PDF are released under the Apache License, Version 2.0 (`LICENSE`). The runtime that
formal-companion copies into `informal/` (`fcmarkers.sty`, `STYLE.md`, `tools/`) is under
the Apache License 2.0 (`informal/LICENSE-runtime`).

## Proofs linked to the Lean

Selected results now have proofs, and the gluing definitions have explicit
constructions with their well-definedness checks. The arguments include the
three-loop factorization in the generation theorem, the homotopy-grid proof
for gluing, the local functor equations, and the pushout universal property.
They use the earlier numbered results and omit routine endpoint renaming and
path reparametrizations.

Eight linked passages carry 17 pinned Lean ranges, including selected
invocations later in the proof. Click a proof or construction to inspect its
code. The project-owned `informal/proofsteps.sty` records its PDF regions;
`informal/proofsteps.json` records the Lean ranges and their hashes. The
exporter rejects changed ranges and records these passages as agent-authored
and awaiting human review.

To regenerate this revision, build the PDF twice with
`bash informal/tools/canonical_pdf.sh --source-commit COMMIT build/proof-ideas`,
copy `build/proof-ideas/a/markers.json` to `informal/markers.json`, and commit it.
Then export both the statements and proofs with the producer checkout:

```sh
python3 tools/proof_steps.py \
  --formal-companion /path/to/formal-companion \
  --library-src /path/to/pinned/TauCeti/source \
  --build-dir build/proof-ideas/a \
  --pdf-url https://github.com/mathlib-initiative/seifert-van-kampen-tauceti/releases/download/v2/svk-tauceti.pdf
python3 pdf-overlay/tools/check_generated.py
python3 tools/proof_steps.py --check
python3 pdf-overlay/tools/serve.py --build
```

In the viewer, click a proof or construction or its entry beneath the statement
to open the Lean ranges.

The v2 PDF URL is the proposed destination for this revision; publishing it
requires review of the new PDF and proof-step links. The published v1 remains
available at its original URL.
