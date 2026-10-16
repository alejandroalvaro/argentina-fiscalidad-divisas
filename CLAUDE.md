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

- Contract engine (phase 2): contract flows, scenario valuations and buckets stay separate. Engine flows come from `contratos/` term sheets; instruments without terms use the SIGADE projection, labeled `source=sigade`. See `docs/FASE2_MOTOR.md`.
- SIGADE operations are keyed by (name, loan currency, rate type); names alone repeat. SIGADE dates have two-digit years: take Año/Mes/Día.
- CER and TAMAR lags: 10 business days, from `series/` (BCRA A3500 days as observed calendar, Ley 27.399 rules after). A CER lag needs `indice_inicial` (issue-date CER, SIGADE's unit base) and `indice_base`; load it only where SIGADE's units are verified. See `docs/FASE2_MOTOR.md`.
- LECAP/BONCAP: the SIGADE balance already includes capitalization up to the last monthly anniversary of issue, and SIGADE does not project later capitalization. Anchor periods on the issue date, with `periodo_final_corto=true` and `base=30E/360` (legal formula VPV = VNO x (1+Tm)^(DIAS/30)).

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
uv run argfx calendario   # phase 2: obligations calendar into data/calendario/
uv run argfx conciliacion # phase 3: reconcile with the Finanzas workbook into data/conciliacion/
uv run argfx devengados   # phase 3 / D-009: capitalized interest accrued by quarter
```

## Git

Conventional commits. `main` is stable; work on `feature/...` or `fix/...` branches.
