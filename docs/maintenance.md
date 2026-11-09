# Maintenance

For everyday validation and site builds, use the commands in
[CONTRIBUTING.md](../CONTRIBUTING.md). This guide covers the steps needed when
the text, proof links, or generated runtime changes.

## Sources and ownership

The rendering pipeline is:

```text
informal/*.tex + sections/ + items.json + proofsteps.json
    → canonical PDF and markers
    → annotations/ (Literature Links)
    → pdf-overlay/annotations.bundle.json + verso.json
    → site/ → GitHub Pages
```

`informal/declarations.json` is the Lean source inventory.
`informal/items.json` records the statement-level links and mathematical
specializations; `informal/proofsteps.json` records the selected Lean ranges.
The latter's hashes protect excerpts and enclosing declarations.

`pdf-overlay/overlay.config.json` controls presentation and output paths.
`annotations/_defaults.json` and the resolved bundle identify the published PDF.
Generated manifests record tool versions and input hashes. Treat those records
as the source of truth for revisions rather than copying pins into new scripts.

The formal-companion producer is currently a private repository. Access to it
is needed to regenerate exports or update the shared viewer. It is not needed
to check this public repository, build its website, or read the committed
Literature Links data.

## Build the text

Install TeX Live with `pdflatex`, `latexmk`, Latin Modern, TikZ, and the packages
listed in `informal/informalize.json`. A development PDF can be built with:

```sh
make pdf
```

The output is `build/pdf/svk-tauceti.pdf`. This does not update the public
annotations: their coordinates belong to the exact released PDF.

For a release, commit the intended text and curation changes first. Use a fresh
build directory and record that source commit:

```sh
SOURCE_COMMIT=$(git rev-parse HEAD)
bash informal/tools/canonical_pdf.sh \
  --source-commit "$SOURCE_COMMIT" build/release
```

This requires Poppler's `pdftotext`, `pdftoppm`, and `pdfinfo` in addition to
TeX. It builds twice, checks that the PDFs have identical bytes, validates the
statement markers, and writes a receipt and proof sheets. Reproducibility is
checked on that TeX installation; another installation may produce different
bytes.

Inspect the PDF and proof sheets, then copy and commit the markers:

```sh
cp build/release/a/markers.json informal/markers.json
git add informal/markers.json
git commit -m "Record markers for the revised text"
```

If the text or other files under `informal/` change after the build, rebuild
before exporting.

## Export statements and proof steps

Prepare the TauCeti source and its Mathlib dependency at the exact commits in
`informal/informalize.json` and `informal/proofsteps.json`. Choose a new,
versioned release URL for the PDF. Set the following paths to your checkouts:

```sh
PRODUCER=/path/to/formal-companion
TAUCETI=/path/to/pinned/TauCeti
PDF_URL=https://github.com/mathlib-initiative/seifert-van-kampen-tauceti/releases/download/NEW_TAG/svk-tauceti.pdf

python3 tools/proof_steps.py \
  --formal-companion "$PRODUCER" \
  --library-src "$TAUCETI" \
  --packages-src "$TAUCETI/.lake/packages" \
  --build-dir build/release/a \
  --pdf-url "$PDF_URL"
make check
```

Replace `NEW_TAG` with the intended release tag. Use the canonical PDF from
this build as the release asset. The exporter checks the selected ranges
against pinned source and emits standard Literature Links endpoints.
Viewer-specific rendering data stays in the existing extension namespace;
reuse standard fields wherever they already express the correspondence.

A proof marker selects a sentence or equation. Most steps have one Lean range;
an explicit helper chain can have several. Multi-line highlights use one
region per page with a quadrilateral for each marked line, so no line is lost
when the viewer selects the region.

## Regenerate hovers

The committed `pdf-overlay/verso.json` supplies token hovers without requiring
readers or CI to build Lean. When snippets change, regenerate hovers from a
prepared Verso workspace at the same TauCeti and Mathlib revisions:

```sh
python3 tools/mathlib_hovers.py \
  --formal-companion "$PRODUCER" \
  --verso-project /path/to/prepared/verso/TauCeti
make check
```

The workspace must already contain TauCeti's rendered pages and the matching
Verso package. This command builds the needed Mathlib modules, combines their
hovers with TauCeti's, and refuses missing or stale snippets. Its resource
priority wrapper uses the Linux `nice` and `ionice` commands.

## Publish

1. Commit the regenerated annotations, bundle, hover data, and manifests.
   Review the diff and run `make check`.
2. Publish the canonical `build/release/a/svk-tauceti.pdf` under the new tag.
   Do not replace an older release's PDF.
3. Update the README's download link and run `make site` from a fresh checkout
   to verify that the public asset can be fetched and matches the recorded hash.
4. Push the completed work to `main`. The Pages workflow runs the checks and
   site build before uploading an artifact; a failed check or PDF hash mismatch prevents
   deployment.
5. Wait for the workflow to finish, then inspect the
   [public homepage](https://mathlib-initiative.github.io/seifert-van-kampen-tauceti/).
   Check the affected pages, selected highlights, and Lean cards.

The homepage redirects directly to the PDF viewer and preserves query strings
and page or selection fragments. The published website, rather than a
localhost server, is the review destination.

For a shared viewer update, regenerate from formal-companion, run the same
checks, and deploy. If the PDF bytes and annotation geometry did not change,
keep the current PDF release.
