.PHONY: help init clean clean-venv unlock uninstall distclean jupyter-notebook jupyter-lab

.DEFAULT_GOAL := help

PYTHON = .venv/bin/python

help:   ## Show this help
	@grep -E '^([a-zA-Z_-]+):.*## ' $(MAKEFILE_LIST) | awk -F ':.*## ' '{printf "%-20s %s\n", $$1, $$2}'

.pkg-initialized: JuliaProject.toml
	JULIA_CONDAPKG_BACKEND=Null julia --project=. -e 'import Pkg; Pkg.instantiate()'
	@touch $@

$(PYTHON): environment.yml
	conda env create -p ./.venv -f environment.yml
	conda env export -p ./.venv > environment.lock.yml
	@touch $@  # mark updated

%.ipynb : | %.jl
	JULIA_NUM_THREADS=1 jupytext --to notebook --execute $(*).jl

%.ipynb : | %.py
	jupytext --to notebook --execute $(*).py

init: $(PYTHON) .pkg-initialized  ## Create the virtual project environment

jupyter-notebook: $(PYTHON) .pkg-initialized ## Run a Jupyter notebook server
	JULIA_NUM_THREADS=auto JULIA_CONDAPKG_BACKEND=Null jupyter notebook --no-browser

jupyter-lab: $(PYTHON) .pkg-initialized  ## Run a Jupyter lab server
	JULIA_NUM_THREADS=auto JULIA_CONDAPKG_BACKEND=Null jupyter lab --no-browser

clean: ## Remove generated files

clean-venv: ## Remove environment files
	rm -f .pkg-initialized
	rm -rf .venv

unlock: clean-venv ## Remove environment and lock files
	rm -f requirements.txt
	rm -f Manifest.toml
	rm -f JuliaManifest.toml
	rm -f environment.lock.yml

distclean: clean unlock ## Restore clean repository state
	rm -rf .ipynb_checkpoints
	rm -rf Python/.ipynb_checkpoints
	rm -rf Julia/.ipynb_checkpoints
	rm -rf .CondaPkg/
