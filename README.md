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

## Selected proof ideas

The text includes eight short proof ideas, from path subdivision and homotopy
grids to the construction and uniqueness of the van Kampen homomorphism.
Each is a Literature Links `proof_step` passage. Its cards show exact ranges
of the pinned Lean source, including selected invocations later in the proof.
The original statements and their numbering are unchanged.

The project-owned `informal/proofsteps.sty` records the PDF regions;
`informal/proofsteps.json` records the Lean ranges and a hash of each range.
The exporter refuses a range whose bytes have changed. It marks these sketches
as agent-authored and awaiting human review.

To regenerate this revision, build the PDF twice with
`bash informal/tools/canonical_pdf.sh --source-commit COMMIT build/proof-ideas`,
copy `build/proof-ideas/a/markers.json` to `informal/markers.json`, and commit it.
Then export both the statements and proof ideas with the producer checkout:

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

In the viewer, enable **Proof steps** to highlight the proof ideas.

The v2 PDF URL is the proposed destination for this revision; publishing it
requires review of the new PDF and proof-step links. The published v1 remains
available at its original URL.
