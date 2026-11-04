# The Seifert--van Kampen theorem, after TauCeti

An informal account, without proofs, of the definitions and results on which the theorem
`TauCeti.isPushout_fundamentalGroup` depends in the Lean library [TauCeti](https://github.com/TauCetiProject/TauCeti) at
commit `37f5e9dce5ac83d2825198ac72d7f5d64eb26c85`. Each numbered statement, and each lettered part of one, is
a box in the PDF linked to the Lean declaration that states it.

- `informal/`: the LaTeX source. `main.tex` is the document, `sections/` its sections,
  `items.json` the table of items and their declarations, `STYLE.md` and
  `STYLE-project.md` the rules it is written to.
- `annotations/`: the links from each box of the PDF to the Lean declarations, in the
  Literature Links format.
- `pdf-overlay/`: the viewer that shows the PDF with those links.

Build the PDF from this directory with TeX Live (pdflatex, latexmk):

```sh
bash informal/tools/build_pdf.sh build/pdf
```

Two builds on one TeX installation give the same bytes; the published PDF is the one whose
sha256 the annotations pin.

The text and the PDF are released under the Apache License, Version 2.0 (`LICENSE`). The runtime that
formal-companion copies into `informal/` (`fcmarkers.sty`, `STYLE.md`, `tools/`) is under
the Apache License 2.0 (`informal/LICENSE-runtime`).
