"""Which stored originals can be republished, and the copy into the public bucket.

Official documents (governments, central banks, official international bodies, official
statistics and gazettes) are republished as stored. Press, private associations, academic
papers and third-party copies of official texts stay private: the public table gives their
URL and SHA-256 so a reader can check a copy they fetch themselves.
"""

from __future__ import annotations

import csv
import tempfile
from collections.abc import Iterable
from pathlib import Path

from argfx.storage import ObjectStore

# Lowercase fragments of the `issuer` field that mark a source as not republishable.
# Checked before anything else, so a third-party copy of an official text stays private.
THIRD_PARTY = (
    "infobae", "bloomberg", "ámbito", "el cronista", "perfil", "el destape",
    "clarín", "bae negocios", "rio times", "extra catamarca", "letra p", "eldiarioar",
    "chequeado", "tiempo de san juan", "parte de pesca", "bichos de campo", "el litoral",
    "punto federal", "urgente24", "newsdigitales", "poder360", "el argentino diario",
    "adeba", "cafci", "cámara argentina", "cámara de industria", "mercados argentina",
    "consultora", "bolsa de comercio", "nber", "levy economics", "white rose",
    "aaep", "mehrling", "unu-wider", "warren mosler", "leyes.co", "justia", "legisweb",
    "aiddata", "ifswf", "facultad de ciencias económicas", "compendio", "sin fuente",
)  # fmt: skip
# Issuers that start with these words are third parties; matched only at the start because
# "la nación" also ends many official names (Presidencia de la Nación).
THIRD_PARTY_PREFIX = ("la nación", "ciara-cec")

FIELDS = [
    "source_id", "sha256", "object_key", "media_type", "issuer", "url", "publicar", "motivo",
    "url_publica",
]  # fmt: skip


def classify(issuer: str) -> tuple[bool, str]:
    low = issuer.strip().lower()
    if not low:
        return False, "sin emisor registrado"
    if low.split(" ")[0] == "tn" or low.startswith(THIRD_PARTY_PREFIX):
        return False, "fuente de terceros"
    for frag in THIRD_PARTY:
        if frag in low:
            return False, "fuente de terceros"
    return True, "documento oficial"


def read_sources(inbox: Path) -> dict[str, dict[str, str]]:
    """First registration of each source_id across every sources.csv under the inbox."""
    out: dict[str, dict[str, str]] = {}
    for path in sorted(inbox.glob("**/sources.csv")):
        with path.open(encoding="utf-8") as f:
            for row in csv.DictReader(f):
                out.setdefault(row["source_id"].strip(), row)
    return out


def build_table(
    objects_csv: Path, inbox: Path, base_url: str | None = None
) -> list[dict[str, str]]:
    sources = read_sources(inbox)
    rows: list[dict[str, str]] = []
    with objects_csv.open(encoding="utf-8") as f:
        for obj in csv.DictReader(f):
            src = sources.get(obj["source_id"], {})
            issuer = (src.get("issuer") or "").strip()
            ok, why = classify(issuer)
            public_url = f"{base_url.rstrip('/')}/{obj['object_key']}" if ok and base_url else ""
            rows.append({
                "source_id": obj["source_id"], "sha256": obj["sha256"],
                "object_key": obj["object_key"], "media_type": obj["media_type"],
                "issuer": issuer, "url": (src.get("url") or "").strip(),
                "publicar": "si" if ok else "no", "motivo": why,
                "url_publica": public_url,
            })  # fmt: skip
    return rows


def write_table(rows: Iterable[dict[str, str]], path: Path) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)


def copy_public(rows: Iterable[dict[str, str]], src: ObjectStore, dst: ObjectStore) -> int:
    """Copy each republishable object missing from `dst`; returns how many were copied."""
    copied = 0
    with tempfile.TemporaryDirectory() as tmp:
        for row in rows:
            if row["publicar"] != "si" or dst.exists(row["object_key"]):
                continue
            local = Path(tmp) / row["sha256"]
            src.download(row["object_key"], local)
            dst.upload(local, row["object_key"], row["media_type"] or None)
            local.unlink()
            copied += 1
    return copied
