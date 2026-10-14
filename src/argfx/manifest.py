"""Git-versioned manifest of stored objects (`manifests/objects.csv`).

One row per unique SHA-256. The manifest is the link between Git (small, reviewable) and R2
(originals, Parquet, snapshots). Rows are append-only; a hash already present is not added again.
"""

from __future__ import annotations

import csv
import mimetypes
from datetime import UTC, datetime
from pathlib import Path

from pydantic import BaseModel, Field

from argfx.hashing import object_key
from argfx.storage import ObjectStore, put_immutable

OBJECTS_MANIFEST = "objects.csv"


class ObjectRecord(BaseModel):
    sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    size_bytes: int = Field(ge=0)
    object_key: str
    media_type: str | None = None
    original_filename: str
    source_id: str | None = None
    ingested_at: datetime

    @classmethod
    def columns(cls) -> list[str]:
        return list(cls.model_fields)


def read_manifest(path: Path) -> list[ObjectRecord]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as fh:
        return [
            ObjectRecord.model_validate({k: (v if v != "" else None) for k, v in row.items()})
            for row in csv.DictReader(fh)
        ]


def append_record(path: Path, record: ObjectRecord) -> bool:
    """Append unless the hash is already listed. Returns True when a row was written."""
    if any(r.sha256 == record.sha256 for r in read_manifest(path)):
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    new_file = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=ObjectRecord.columns(), lineterminator="\n")
        if new_file:
            writer.writeheader()
        row = record.model_dump(mode="json")
        writer.writerow({k: ("" if v is None else v) for k, v in row.items()})
    return True


def ingest_file(
    path: Path, store: ObjectStore, manifests_dir: Path, source_id: str | None = None
) -> tuple[ObjectRecord, bool]:
    """Store a file immutably and register it. Returns (record, newly_uploaded)."""
    media_type = mimetypes.guess_type(path.name)[0]
    sha, created = put_immutable(store, path, media_type)
    record = ObjectRecord(
        sha256=sha,
        size_bytes=path.stat().st_size,
        object_key=object_key(sha),
        media_type=media_type,
        original_filename=path.name,
        source_id=source_id,
        ingested_at=datetime.now(UTC).replace(microsecond=0),
    )
    append_record(manifests_dir / OBJECTS_MANIFEST, record)
    return record, created
