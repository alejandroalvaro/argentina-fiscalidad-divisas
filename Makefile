.PHONY: install lint format test check config storage-check clean-cache validate-grok

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

# Snapshot every grok/* branch's inbox/ into data/inbox and validate it (no checkout needed)
validate-grok:
	git fetch -q origin
	rm -rf data/inbox && mkdir -p data/inbox
	for b in $$(git for-each-ref --format='%(refname:short)' refs/remotes/origin/grok/); do \
		git archive $$b inbox | tar -x -C data/inbox; done
	uv run argfx validate data/inbox/inbox --out data/validacion
