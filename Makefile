.PHONY: install lint format test check config storage-check clean-cache

install:
	uv sync

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff check --fix .
	uv run ruff format .

test:
	uv run pytest

check: lint test

config:
	uv run argfx config

storage-check:
	uv run argfx storage-check

clean-cache:
	rm -rf data/cache
