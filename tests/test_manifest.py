from __future__ import annotations

from pathlib import Path

from argfx.config import Settings
from argfx.manifest import OBJECTS_MANIFEST, ingest_file, read_manifest
from argfx.storage import get_store


def test_ingest_registers_once(settings: Settings, tmp_path: Path) -> None:
    store = get_store(settings)
    doc = tmp_path / "prospecto.pdf"
    doc.write_bytes(b"%PDF fake")
    copy = tmp_path / "prospecto_copia.pdf"
    copy.write_bytes(doc.read_bytes())

    first, created = ingest_file(doc, store, settings.manifests_dir, source_id="SRC-001")
    second, created_again = ingest_file(copy, store, settings.manifests_dir)

    assert created and not created_again
    assert first.sha256 == second.sha256
    rows = read_manifest(settings.manifests_dir / OBJECTS_MANIFEST)
    assert len(rows) == 1
    assert rows[0].source_id == "SRC-001"
    assert rows[0].media_type == "application/pdf"
    assert rows[0].original_filename == "prospecto.pdf"


def test_missing_values_stay_missing(settings: Settings, tmp_path: Path) -> None:
    doc = tmp_path / "sin_extension"
    doc.write_bytes(b"data")
    ingest_file(doc, get_store(settings), settings.manifests_dir)
    (row,) = read_manifest(settings.manifests_dir / OBJECTS_MANIFEST)
    assert row.source_id is None
    assert row.media_type is None
