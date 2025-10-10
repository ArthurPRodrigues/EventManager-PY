# Simple Makefile for local dev (Linux/macOS)

PYTHON ?= python3
VENV_DIR := .venv
VENV_PY := $(VENV_DIR)/bin/python
VENV_PIP := $(VENV_DIR)/bin/pip
VENV_PRECOMMIT := $(VENV_DIR)/bin/pre-commit # <-- 1. ADICIONE ESTA LINHA

.PHONY: default help run clean play

default: help

help:
	@echo "Targets:"
	@echo "  install     - Create venv, install fonts, and install production dependencies"
	@echo "  install-dev - Create venv, install fonts, and install all dependencies (prod + dev)"
	@echo "  run         - Start the application"
	@echo "  clean       - Remove caches and build artifacts"
	@echo "  play <name> - Run playground script (e.g., make play friendship)"

$(VENV_DIR):
	$(PYTHON) -m venv $(VENV_DIR)

install-fonts:
	mkdir -p ~/.fonts
	cp -r assets/fonts/* ~/.fonts/ 2>/dev/null || true
	fc-cache -f ~/.fonts

install: $(VENV_DIR) install-fonts
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install -e .

install-dev: install
	$(VENV_PIP) install -e ".[dev]"
	$(VENV_PRECOMMIT) install
	$(VENV_PRECOMMIT) install --hook-type commit-msg

run:
	PYTHONPATH=src $(VENV_PY) -m main

clean:
	rm -rf __pycache__ src/**/__pycache__

play:
	@script_name=$(filter-out $@,$(MAKECMDGOALS)); \
	if [ -z "$$script_name" ]; then \
		echo "Usage: make play <script_name>"; \
		echo "Example: make play friendship"; \
		exit 1; \
	fi; \
	script_file="src/scripts/play_$$script_name.py"; \
	if [ -f "$$script_file" ]; then \
		PYTHONPATH=src $(PYTHON) "$$script_file"; \
	else \
		echo "Error: Script not found: $$script_file"; \
		exit 1; \
	fi

%:
	@: