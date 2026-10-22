.PHONY: install test lint notebook
install:
	pip install -e ".[dev]"
test:
	pytest
lint:
	ruff check src tests
notebook:
	jupyter lab
