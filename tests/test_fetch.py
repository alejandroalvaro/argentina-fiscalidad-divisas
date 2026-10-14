from __future__ import annotations

import csv
import urllib.error
from pathlib import Path

from argfx.config import Settings
from argfx.fetch import DOWNLOADS_LOG, Fetched, fetch_sources
from argfx.hashing import sha256_bytes
from argfx.manifest import OBJECTS_MANIFEST, read_manifest
from argfx.storage import get_store

PDF = b"%PDF-1.7 texto ordenado"


def write_sources(path: Path, rows: list[dict[str, str]]) -> Path:
    cols = ["source_id", "url", "sha256", "local_object_key"]
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)
    return path


def fake_fetcher(url: str) -> Fetched:
    if url.endswith("404"):
        raise urllib.error.HTTPError(url, 404, "Not Found", {}, None)  # type: ignore[arg-type]
    if url.endswith(".pdf"):
        return Fetched(200, PDF, "application/pdf")
    return Fetched(200, b"<html>cambia en cada visita</html>", "text/html")


def test_fetch_sources_logs_matches_mismatches_and_errors(
    settings: Settings, tmp_path: Path
) -> None:
    sources = write_sources(
        tmp_path / "sources.csv",
        [
            {
                "source_id": "SRC-1",
                "url": "https://x/t.pdf",
                "sha256": sha256_bytes(PDF),
                "local_object_key": "docs/texord.pdf",
            },
            {
                "source_id": "SRC-2",
                "url": "https://x/page",
                "sha256": "0" * 64,
                "local_object_key": "",
            },
            {"source_id": "SRC-3", "url": "https://x/404", "sha256": "", "local_object_key": ""},
        ],
    )
    records = fetch_sources(sources, get_store(settings), settings.manifests_dir, fake_fetcher, 0)
    by_id = {r.source_id: r for r in records}

    assert by_id["SRC-1"].hash_match is True and by_id["SRC-1"].created
    assert by_id["SRC-2"].hash_match is False
    assert by_id["SRC-3"].http_status == 404 and by_id["SRC-3"].sha256 is None

    objects = read_manifest(settings.manifests_dir / OBJECTS_MANIFEST)
    assert {o.source_id for o in objects} == {"SRC-1", "SRC-2"}
    assert next(o for o in objects if o.source_id == "SRC-1").original_filename == "texord.pdf"
    with (settings.manifests_dir / DOWNLOADS_LOG).open() as fh:
        assert len(list(csv.DictReader(fh))) == 3
