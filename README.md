# The Seifert–van Kampen theorem, after TauCeti

An informal account of how the Seifert–van Kampen theorem is proved in the Lean library
[TauCeti](https://github.com/TauCetiProject/TauCeti) at commit
`37f5e9dce5ac83d2825198ac72d7f5d64eb26c85`. Statements and selected proof steps
are linked to the corresponding Lean declarations and lines. Variables and
notation are introduced in the sections that use them.

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

The eight arguments have 44 selected sentence or equation links. Each opens
one pinned Lean range for that specific step, including explicit invocations of
earlier results. Unmarked prose and proof headings carry no proof-wide link.
The project-owned `informal/proofsteps.sty` records word positions or the exact
dimensions of a displayed equation; `informal/proofsteps.json` records the
corresponding Lean ranges and their hashes. The exporter rejects changed ranges,
whole-proof markers, and steps with multiple code targets. These new links are
agent-authored and await human review.

To regenerate this revision, build the PDF twice with
`bash informal/tools/canonical_pdf.sh --source-commit COMMIT build/proof-ideas`,
copy `build/proof-ideas/a/markers.json` to `informal/markers.json`, and commit it.
Then export both the statements and proofs with the producer checkout:

```sh
python3 tools/proof_steps.py \
  --formal-companion /path/to/formal-companion \
  --library-src /path/to/pinned/TauCeti/source \
  --packages-src /path/to/pinned/TauCeti/.lake/packages \
  --build-dir build/proof-ideas/a \
  --pdf-url https://github.com/mathlib-initiative/seifert-van-kampen-tauceti/releases/download/v2/svk-tauceti.pdf
python3 pdf-overlay/tools/check_generated.py
python3 tools/proof_steps.py --check
python3 pdf-overlay/tools/serve.py --build
```

In the viewer, click a marked sentence or equation to open its corresponding Lean lines.
Proof steps may also point into the pinned Mathlib dependency: their target names
`package: mathlib` and the matching pin is recorded in `proofsteps.json`.
The Lebesgue-radius step in Proposition 1.1 links directly to the lemma call
inside Mathlib's interval-subdivision helper, which TauCeti invokes through
`exists_monotone_Icc_subset_open_cover_unitInterval`. Dependency ranges are checked
against the source inventory and the exact committed source before export.


Mathlib notion cards also show their definitions and structure fields inline.
Supply `--packages-src` from the same pinned TauCeti checkout when regenerating
them: this revision uses Mathlib commit
`1b1ccf4b088b32fa3f23f2de1127433254a81e1e`. The snippets are from Mathlib's
Apache-2.0 source, with each card linking to the declaration at that revision.

To rebuild Mathlib's token hovers, use the Verso workspace prepared for this
TauCeti revision, with its original dependency pins and matching Verso package:

```sh
python3 tools/mathlib_hovers.py \
  --formal-companion /path/to/formal-companion \
  --verso-project /path/to/verso/libs/svk-tauceti-lib
python3 pdf-overlay/tools/check_generated.py
python3 pdf-overlay/tools/serve.py --build-only
```

This builds only the Mathlib modules used by the cards and combines their
hovers with the TauCeti pages. It checks source revisions before building and
requires every Mathlib card to have a matching hover statement. Separate page
builds have separate hover identifiers; the exporter remaps them when combining
the results. The generated `pdf-overlay/verso.json` is committed with the overlay.

The v2 PDF URL is the proposed destination for this revision; publishing it
requires review of the new PDF and proof-step links. The published v1 remains
available at its original URL.
