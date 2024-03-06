.PHONY: help init clean clean-venv unlock uninstall distclean jupyter-notebook jupyter-lab

.DEFAULT_GOAL := help

PYTHON = .venv/bin/python

help:   ## Show this help
	@grep -E '^([a-zA-Z_-]+):.*## ' $(MAKEFILE_LIST) | awk -F ':.*## ' '{printf "%-20s %s\n", $$1, $$2}'

.pkg-initialized: JuliaProject.toml
	julia --project=. -e 'import Pkg; Pkg.instantiate()'
	@touch $@

$(PYTHON): requirements.in
	python3 -m venv .venv
	$@ -m pip install --upgrade pip
	$@ -m pip install pip-tools
	@touch $@  # mark updated

requirements.txt: $(PYTHON) requirements.in
	$(PYTHON) -m piptools compile -o $@ requirements.in
	$(PYTHON) -m piptools sync
	@touch $@  # mark updated

%.ipynb : | %.jl
	JULIA_NUM_THREADS=1 jupytext --to notebook --execute $(*).jl

%.ipynb : | %.py
	jupytext --to notebook --execute $(*).py

init: requirements.txt .pkg-initialized  ## Create the virtual project environment

jupyter-notebook: requirements.txt .pkg-initialized ## Run a Jupyter notebook server
	JULIA_NUM_THREADS=auto jupyter notebook --no-browser

jupyter-lab: requirements.txt .pkg-initialized  ## Run a Jupyter lab server
	JULIA_NUM_THREADS=auto jupyter lab --no-browser

clean: ## Remove generated files

clean-venv: ## Remove environment files
	rm -f .pkg-initialized
	rm -rf .venv

unlock: clean-venv ## Remove environment and lock files
	rm -f requirements.txt
	rm -f Manifest.toml
	rm -f JuliaManifest.toml

distclean: clean unlock ## Restore clean repository state
	rm -rf .ipynb_checkpoints
