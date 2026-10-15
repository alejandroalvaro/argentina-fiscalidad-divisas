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

# Snapshot main's inbox/, overlay every grok/* branch's inbox/, and validate (no checkout needed).
# Merged batches are included so new batches can cite their sources and instruments.
validate-grok:
	git fetch -q --prune origin
	rm -rf data/inbox && mkdir -p data/inbox
	git archive origin/main inbox | tar -x -C data/inbox
	for b in $$(git for-each-ref --format='%(refname:short)' refs/remotes/origin/grok/); do \
		if git cat-file -e $$b:inbox 2>/dev/null; then git archive $$b inbox | tar -x -C data/inbox; fi; done
	uv run argfx validate data/inbox/inbox --out data/validacion
