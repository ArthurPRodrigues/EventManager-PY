# Simple Makefile for local dev (Linux/macOS)

PYTHON ?= python3

.PHONY: default help run clean

default: help

help:
	@echo "Targets:"
	@echo "  run      - Start the application"
	@echo "  clean    - Remove caches and build artifacts"

run:
	PYTHONPATH=src $(PYTHON) -m main

clean:
	rm -rf __pycache__ src/**/__pycache__