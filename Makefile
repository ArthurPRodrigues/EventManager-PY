# Simple Makefile for local dev (Linux/macOS)

PYTHON ?= python3
VENV_DIR := .venv
VENV_PY := $(VENV_DIR)/bin/python
VENV_PIP := $(VENV_DIR)/bin/pip

.PHONY: default help run clean

default: help

help:
	@echo "Targets:"
	@echo "  install  - Create venv and install dependencies"
	@echo "  run      - Start the application"
	@echo "  clean    - Remove caches and build artifacts"

$(VENV_DIR):
	$(PYTHON) -m venv $(VENV_DIR)

install: $(VENV_DIR)
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install -r requirements.txt

run:
	PYTHONPATH=src $(PYTHON) -m main

clean:
	rm -rf __pycache__ src/**/__pycache__