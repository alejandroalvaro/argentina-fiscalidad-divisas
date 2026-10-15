"""Download the documents listed in a Grok `sources.csv` and store them immutably.

Each download is logged in `manifests/downloads.csv`, including the hash Grok reported, so that
differences between Grok's copy and ours stay visible. Dynamic HTML pages often hash differently
on every request; binary files (PDF, XLSX, ZIP) should match.
"""

from __future__ import annotations

import csv
import tempfile
import time
import urllib.error
import urllib.request
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlparse

from pydantic import BaseModel

from argfx.manifest import ingest_file
from argfx.storage import ObjectStore

DOWNLOADS_LOG = "downloads.csv"
DEFAULT_USER_AGENT = "argfx/0.1 (academic research; Argentina fiscal FX)"
TIMEOUT_S = 60


class DownloadRecord(BaseModel):
    source_id: str
    url: str
    fetched_at: datetime
    http_status: int | None
    sha256: str | None
    size_bytes: int | None
    grok_sha256: str | None
    hash_match: bool | None
    created: bool | None
    error: str | None

    @classmethod
    def columns(cls) -> list[str]:
        return list(cls.model_fields)


@dataclass
class Fetched:
    status: int
    body: bytes
    content_type: str | None


Fetcher = Callable[[str], Fetched]


def http_fetch(url: str, user_agent: str = DEFAULT_USER_AGENT) -> Fetched:
    req = urllib.request.Request(url, headers={"User-Agent": user_agent, "Accept": "*/*"})
    with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
        return Fetched(resp.status, resp.read(), resp.headers.get_content_type())


# Pages that answer 200 with an error body. The Boletín Oficial does it for a detalleAviso link
# without the publication date at the end.
ERROR_BODIES = (b"Hubo un error en el sistema. Por favor contactarse con el administrador",)


class ErrorPage(OSError):
    """A 200 response whose body is a known error page."""


def read_sources(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def filename_for(row: dict[str, str]) -> str:
    """Prefer Grok's local name (keeps the extension), else the last URL segment."""
    local = (row.get("local_object_key") or "").strip()
    if local:
        return Path(local).name
    name = Path(urlparse(row["url"]).path).name
    return name or f"{row['source_id']}.html"


def append_log(path: Path, record: DownloadRecord) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    new_file = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=DownloadRecord.columns(), lineterminator="\n")
        if new_file:
            writer.writeheader()
        row = record.model_dump(mode="json")
        writer.writerow({k: ("" if v is None else v) for k, v in row.items()})


def fetch_sources(
    sources_csv: Path,
    store: ObjectStore,
    manifests_dir: Path,
    fetcher: Fetcher = http_fetch,
    delay_s: float = 1.0,
) -> list[DownloadRecord]:
    records: list[DownloadRecord] = []
    for i, row in enumerate(read_sources(sources_csv)):
        if i and delay_s:
            time.sleep(delay_s)  # be polite with government servers
        source_id, url = row["source_id"], row["url"].strip()
        grok_sha = (row.get("sha256") or "").strip() or None
        now = datetime.now(UTC).replace(microsecond=0)
        status: int | None = None
        try:
            fetched = fetcher(url)
            status = fetched.status
            if any(marker in fetched.body for marker in ERROR_BODIES):
                raise ErrorPage("error page instead of the document; check the URL")
            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / filename_for(row)
                path.write_bytes(fetched.body)
                obj, created = ingest_file(path, store, manifests_dir, source_id)
            record = DownloadRecord(
                source_id=source_id,
                url=url,
                fetched_at=now,
                http_status=status,
                sha256=obj.sha256,
                size_bytes=obj.size_bytes,
                grok_sha256=grok_sha,
                hash_match=(obj.sha256 == grok_sha) if grok_sha else None,
                created=created,
                error=None,
            )
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            if isinstance(exc, urllib.error.HTTPError):
                status = exc.code
            record = DownloadRecord(
                source_id=source_id,
                url=url,
                fetched_at=now,
                http_status=status,
                sha256=None,
                size_bytes=None,
                grok_sha256=grok_sha,
                hash_match=None,
                created=None,
                error=f"{type(exc).__name__}: {exc}",
            )
        append_log(manifests_dir / DOWNLOADS_LOG, record)
        records.append(record)
    return records
