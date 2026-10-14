"""SHA-256 helpers. The hash is the identity of every original document."""

from __future__ import annotations

import hashlib
from pathlib import Path

CHUNK_SIZE = 1024 * 1024


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as fh:
        while chunk := fh.read(CHUNK_SIZE):
            digest.update(chunk)
    return digest.hexdigest()


def object_key(sha256: str) -> str:
    """Content-addressed key, sharded by the first two byte pairs to keep prefixes small."""
    if len(sha256) != 64 or any(c not in "0123456789abcdef" for c in sha256):
        raise ValueError(f"not a lowercase hex SHA-256: {sha256!r}")
    return f"objects/sha256/{sha256[:2]}/{sha256[2:4]}/{sha256}"
