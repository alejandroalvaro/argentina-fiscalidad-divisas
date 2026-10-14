# CLAUDE.md: argentina-fiscalidad-divisas

Research pipeline for an academic paper on collecting Argentine export duties in USD. This is **not a web app**: the 8 Group web conventions (FastAPI, port, `/health`, design system) don't apply. The Python conventions do (3.11+, `pyproject.toml`, ruff, type hints, Pydantic). A debt dashboard may come later as a separate project that consumes this repo's outputs.

## Read first

- `docs/protocolo/RESEARCH_PROTOCOL.md`: question, hypotheses, scope.
- `docs/protocolo/AUDIT_PROTOCOL.md`: every change must survive these checks.
- `docs/protocolo/CLAUDE_CODE_TASKS.md`: the phases assigned to Claude Code.

## Rules that are easy to break

- Unknown values stay `None`/`NULL`. Never impute zero.
- Keep currency of account, indexation, currency of payment and residency as separate fields.
- Dollar-linked debt payable in ARS is not a contractual USD need.
- Keep observed data, contract terms, scenarios and assumptions in separate tables.
- Net reserves follow the IMF TMU definition: Treasury FX deposits at the BCRA are NOT subtracted (see docs/DECISIONES.md D-001).
- Treasury, BCRA and consolidated public sector are reported separately. No double counting of intra-public-sector holdings.
- No LLM calls for deterministic calculations. LLM-written text only in the Phase 5 writing layer.
- datos.gob.ar: take series from the static distribution CSV (`infra.datos.gob.ar/.../download/*.csv`). The `apis.datos.gob.ar/series` API drops observations at random; use it only to find the `downloadURL`.
- SIGADE amounts are in USD units; Secretaría de Finanzas cuadros (A.1.x...) are in thousands of USD.
- Originals are immutable and content-addressed by SHA-256 (`argfx.storage.put_immutable`). Register them in `manifests/` via `argfx ingest`.

## Storage

- Git: code, Markdown, tests, small CSV manifests. No PDFs, Parquet, DuckDB, zips or Git LFS.
- R2 bucket `argentina-fx-research`: originals, Parquet, snapshots.
- `data/`: local, regenerable cache.
- `.env` holds R2 credentials and is unreadable to Claude by permission rule. Use `uv run argfx config` / `storage-check` to inspect it without printing secrets.

## Commands

```bash
make install   # uv sync
make check     # ruff + pytest (offline)
make storage-check
```

## Git

Conventional commits. `main` is stable; work on `feature/...` or `fix/...` branches.
