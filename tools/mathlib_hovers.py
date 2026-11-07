#!/usr/bin/env python3
"""Build the PDF cards' Mathlib token hovers with TauCeti's pinned Verso workspace.

Uses the producer's code-only page adapter and dependency-aware hover exporter.
Only compiled rendering inputs under .lake/build are rewritten; Lean sources,
dependency pins, and the PDF are unchanged.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
NS = "org.mathlib-initiative.formal-companion.overlay"


def run(argv, work, *, heavy=False):
    """Run an argument list, with restrained resource priority for Lean builds."""
    command = ["nice", "-n", "10", "ionice", "-c3", *argv] if heavy else argv
    env = {**os.environ, "LEAN_NUM_THREADS": os.environ.get("LEAN_NUM_THREADS", "8")}
    subprocess.run(command, cwd=work, env=env, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--formal-companion", required=True, type=Path)
    parser.add_argument("--verso-project", required=True, type=Path)
    args = parser.parse_args()
    producer = args.formal_companion.resolve()
    work = args.verso_project.resolve()
    sys.path.insert(0, str(producer / "scripts"))
    from informalize.verso_host import code_only_map
    sys.path.insert(0, str(producer / "templates/overlay/runtime/tools"))
    import verso_extract as verso

    declaration_data = json.loads((ROOT / "informal/declarations.json").read_text())
    library = declaration_data["library"]
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=work, text=True).strip()
    if head != library["commit"]:
        raise ValueError("Verso workspace is not at the pinned TauCeti revision")
    references = [r for r in declaration_data["references"] if r.get("package") == "mathlib"]
    pins = {(r["repo"], r["commit"]) for r in references}
    if len(pins) != 1:
        raise ValueError("expected one pinned Mathlib repository")
    repo, commit = pins.pop()
    repo = "https://" + repo
    manifest = json.loads((work / "lake-manifest.json").read_text())
    package = next(p for p in manifest["packages"] if p["name"] == "mathlib")
    if package["rev"] != commit or verso.dependency_uri(package["url"]) != repo:
        raise ValueError("Verso workspace moved the pinned Mathlib dependency")
    mathlib = work / manifest.get("packagesDir", ".lake/packages") / "mathlib"
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=mathlib, text=True).strip()
    if head != commit:
        raise ValueError("Mathlib checkout is not at its pinned revision")

    entries = verso.bundle_entries(ROOT / "pdf-overlay/annotations.bundle.json")
    ends = [end for _, annotation in entries for end in annotation.get("object", [])
            if end.get("uri") == repo and verso.snippet_text(end)]
    modules = sorted({end["location"]["module"] for end in ends})
    for module in modules:
        relative = module.replace(".", "/") + ".lean"
        pinned = subprocess.check_output(["git", "show", commit + ":" + relative], cwd=mathlib)
        if (mathlib / relative).read_bytes() != pinned:
            raise ValueError("Mathlib source changed: " + module)

    run(["lake", "build", ":literateHtml"], work, heavy=True)
    run(["lake", "build", *["+" + module + ":literate" for module in modules]], work, heavy=True)
    build = work / ".lake/build/overlay-mathlib-hovers"
    build.mkdir(parents=True, exist_ok=True)
    mapping = build / "original-modules.tsv"
    mapping.write_text("".join(
        f"{module}\t{work / '.lake/build/literate' / (module.replace('.', '/') + '.json')}\t{mathlib}\n"
        for module in modules))
    inputs = code_only_map(mapping, build / "inputs")
    config = build / "literate.toml"
    config.write_text("show_docstrings = false\n")
    pages = build / "pages"
    run(["lake", "env", str(work / ".lake/packages/verso/.lake/build/bin/verso-literate-html"),
         str(pages), str(inputs), str(config)], work, heavy=True)

    value, counts = verso.extract_pages(work / ".lake/build/literate-html", entries,
                                        commit=library["commit"], dependency_pages={repo: pages})
    problems = verso.committed_problems(value)
    stale = verso.unpinned(value, entries)
    if problems or stale:
        raise ValueError("; ".join([*problems, *([stale] if stale else [])]))
    value, joined = verso.joined(value, entries)
    missing = [end["location"]["declaration"] for end in ends
               if not any(len(run) > 2 and run[2] is not None
                          for runs in value["statements"].get(verso.card_target(end), []) for run in runs)]
    if missing or joined["dropped"]:
        raise ValueError("missing or stale hover statements: " + ", ".join(missing))
    verso.write_out(ROOT / "pdf-overlay/verso.json", verso.dumps_lines(value))
    print(json.dumps({"mathlib_cards": len(ends), "mathlib_modules": len(modules),
                      "hovers": len(value["hovers"]), **counts, "dropped": joined["dropped"]},
                     indent=2))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, StopIteration, subprocess.CalledProcessError) as error:
        raise SystemExit(str(error)) from error
