# Working in this repository

- Use the public site for previews and review:
  https://mathlib-initiative.github.io/seifert-van-kampen-tauceti/
  The maintainer has asked that future work be published there. Validate and
  push ready changes, wait for Pages, and check the live result. Do not leave
  requested changes available only on localhost.
- Read CONTRIBUTING.md for file ownership and docs/maintenance.md for builds
  and releases. Run `make check` and `make site` before publishing.
- Keep the README focused on reading the text and getting started. Put detailed
  maintenance instructions in docs/.
- Before editing mathematics, read informal/STYLE.md and
  informal/STYLE-project.md. Give actual arguments, introduce notation when it
  is needed, and tag specific sentences or equations rather than whole proofs.
- Prefer existing Literature Links fields and capabilities. Add extensions only
  for a concrete unmet need. Do not add Lean syntax to the printed exposition.
- Files listed as generated in either GENERATED.json come from formal-companion.
  Update the producer and regenerate them; do not hand-edit vendored runtimes,
  exported annotations, or hashes to bypass validation.
- Keep tests under tests/ and project-specific tools under tools/. Avoid adding
  dependencies for tasks the standard library already handles.
- Keep PDF assets immutable and versioned. A text change requires rebuilding
  the PDF and annotations together. Documentation-only changes need no new PDF.
