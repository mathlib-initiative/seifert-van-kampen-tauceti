# Contributing

Use the [public PDF viewer](https://mathlib-initiative.github.io/seifert-van-kampen-tauceti/)
to review the current text and its Lean links. Include the item number or a
link to the selected passage when reporting a problem.

## Find the source

| Change | Edit |
| --- | --- |
| Mathematical prose and diagrams | `informal/sections/*.tex` |
| Shared notation | `informal/notation.sty` |
| Statement links, hypotheses, and specializations | `informal/items.json` |
| Proof-step ranges and reading notes | `informal/proofsteps.json` |
| Viewer title and display options | `pdf-overlay/overlay.config.json` |
| Homepage routing | `site/index.html` |
| Project export behavior | `tools/`, with regression tests in `tests/` |

Read the [project editorial guide](informal/STYLE-project.md) before changing
the text. It records the notation, assumed background, and proof-tagging choices.

## Validate a change

Run from the repository root on Linux or macOS with Python 3.11 or later,
Git, and Make:

```sh
make check
make site
```

`make check` validates generated files, Literature Links records, pinned proof
excerpts, and the project tests. It works offline and does not require Lean,
TeX, or access to formal-companion. `make site` runs those checks before building
the static website; its first run needs network access to the released PDF.
Use `make help` to list commands, or `make check PYTHON=python3.11` to choose Python.

A text or annotation change also needs regeneration before these checks can
pass. Follow [the maintenance guide](docs/maintenance.md); changing a hash to
silence a failed check is not regeneration.

## Source and generated files

The files listed in `informal/GENERATED.json` and `pdf-overlay/GENERATED.json`
come from formal-companion. Make shared runtime or viewer changes in that
project and regenerate the consumer copy. Keep third-party assets and their
notices together.

The annotation files, bundle, markers, and hover data are generated from the
curated inputs. Update the inputs rather than patching the exported JSON.
The build output under `site/` is ignored except for its authored
`index.html`; PDFs, caches, and intermediate TeX files stay outside Git.

Keep project tools small and use the Python standard library. Add a regression
test when changing range validation, annotation geometry, or export behavior.
Existing commands and pinned source locations should continue to work.

## Publishing and review

Push ready changes to the public repository. The Pages workflow checks and
builds `main` before deploying it. Verify the resulting public page, including
the PDF's “Verified PDF” status and any affected annotations, before reporting
the update complete. Use the public URL for previews and review.

For a changed PDF, publish a new versioned asset before deploying annotations
that reference it. Keep existing release assets available so older links remain
valid. Documentation-only changes do not require a PDF release.

Machine checks establish that the exported material matches its recorded
sources. They do not certify that the informal proof or its mathematical
correspondence is correct. Proof-step provenance remains agent-authored until
a human has reviewed the relevant correspondence.
