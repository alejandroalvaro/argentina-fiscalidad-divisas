"""Local DuckDB cache. The database file is regenerable and never committed."""

from __future__ import annotations

from pathlib import Path

import duckdb

from argfx.config import Settings


def connect(settings: Settings, path: Path | None = None) -> duckdb.DuckDBPyConnection:
    """Open the local cache database (or `:memory:` when path is given as such)."""
    db_path = path or settings.duckdb_path
    if str(db_path) != ":memory:":
        db_path.parent.mkdir(parents=True, exist_ok=True)
    return duckdb.connect(str(db_path))


def enable_r2(con: duckdb.DuckDBPyConnection, settings: Settings) -> None:
    """Let DuckDB read `r2://<bucket>/...` Parquet directly. Needs network (httpfs extension)."""
    if not settings.has_r2_credentials:
        raise RuntimeError("R2 credentials missing")
    assert settings.r2_access_key_id and settings.r2_secret_access_key
    con.execute("INSTALL httpfs; LOAD httpfs;")

    # CREATE SECRET does not take bound parameters, so values are quoted as SQL literals.
    def lit(value: str | None) -> str:
        return "'" + (value or "").replace("'", "''") + "'"

    con.execute(
        "CREATE OR REPLACE TEMPORARY SECRET argfx_r2 ("
        f"TYPE r2, KEY_ID {lit(settings.r2_access_key_id.get_secret_value())}, "
        f"SECRET {lit(settings.r2_secret_access_key.get_secret_value())}, "
        f"ACCOUNT_ID {lit(settings.r2_account_id)})"
    )
