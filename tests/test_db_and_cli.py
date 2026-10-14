from __future__ import annotations

from pathlib import Path

import pytest

from argfx import cli
from argfx.config import Settings
from argfx.db import connect


def test_duckdb_parquet_roundtrip(settings: Settings, tmp_path: Path) -> None:
    con = connect(settings)
    assert settings.duckdb_path.exists()
    pq = tmp_path / "flows.parquet"
    con.execute(
        "COPY (SELECT * FROM (VALUES ('AL30', 'USD', 1.5), ('TX26', 'ARS', NULL)) "
        "t(instrument_id, currency_of_payment, amount)) TO ? (FORMAT parquet)",
        [str(pq)],
    )
    rows = con.execute(
        "SELECT instrument_id, amount FROM read_parquet(?) ORDER BY 1", [str(pq)]
    ).fetchall()
    assert rows == [("AL30", 1.5), ("TX26", None)]  # unknown stays NULL, never zero


def test_cli_storage_check_and_ingest(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setenv("ARGFX_STORAGE", "local")
    assert cli.main(["storage-check"]) == 0
    doc = tmp_path / "boletin.txt"
    doc.write_text("Boletín Oficial")
    assert cli.main(["ingest", str(doc), "--source-id", "BO-1"]) == 0
    assert (tmp_path / "manifests" / "objects.csv").exists()
    out = capsys.readouterr().out
    assert "OK" in out and "stored" in out
