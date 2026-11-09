# The Seifert–van Kampen theorem, after TauCeti

An informal account of how [TauCeti](https://github.com/TauCetiProject/TauCeti)
proves the Seifert–van Kampen theorem. Statements and selected proof steps link
directly to their Lean counterparts through
[Literature Links](https://mathlib-initiative.github.io/literature-links/).

**[Read the annotated PDF](https://mathlib-initiative.github.io/seifert-van-kampen-tauceti/)** ·
[Download the PDF](https://github.com/mathlib-initiative/seifert-van-kampen-tauceti/releases/download/v11/svk-tauceti.pdf) ·
[Browse the annotations](annotations/)

The viewer connects individual sentences and equations to pinned Lean source
ranges, with definitions and token hovers available alongside the text.
The public site is the primary place to read and review changes.

## Repository guide

| Directory | Contents |
| --- | --- |
| [informal/](informal/) | LaTeX text, mathematical notation, and curated statement and proof-step links |
| [annotations/](annotations/) | Exported Literature Links records |
| [pdf-overlay/](pdf-overlay/) | Generated viewer, bundled annotations, and hover data |
| [tools/](tools/) | Project-specific annotation and hover exporters |
| [tests/](tests/) | Tests for source ranges, annotation integrity, and highlight geometry |
| [docs/](docs/) | Build, regeneration, and publication instructions |

## Development

On Linux or macOS, Python 3.11 or later, Git, and Make are enough to validate
the repository and build the website. No Python packages or Lean installation are needed for these
commands:

```sh
make check
make site
```

The site build downloads the released PDF, verifies its SHA-256, and writes
the website to `site/`. Changes pushed to `main` are checked and deployed to
GitHub Pages.

See [CONTRIBUTING.md](CONTRIBUTING.md) for editing guidance and
[the maintenance guide](docs/maintenance.md) for PDF builds and new releases.

## License

The text and project code are released under [Apache-2.0](LICENSE).
Generated runtime and bundled dependencies retain their
[license notices](pdf-overlay/THIRD_PARTY.md).
