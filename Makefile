PYTHON ?= python3
PDF_BUILD_DIR ?= build/pdf

.PHONY: help check test site pdf

help:
	@printf '%s\n' \
	  'make check  Validate generated files, proof links, and tests (offline)' \
	  'make test   Run project regression tests' \
	  'make site   Check and build the website using the released PDF' \
	  'make pdf    Build a development PDF (requires TeX Live)' \
	  'Override Python with PYTHON=python3.11.'

check:
	$(PYTHON) pdf-overlay/tools/check_generated.py
	$(PYTHON) tools/proof_steps.py --check
	$(MAKE) test PYTHON="$(PYTHON)"

test:
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py'

site: check
	$(PYTHON) pdf-overlay/tools/serve.py --build-only

pdf:
	bash informal/tools/build_pdf.sh "$(PDF_BUILD_DIR)"
