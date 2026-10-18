"""Immutable, content-addressed object storage: R2 (S3 API) or a local directory for offline work.

Objects are written once under their SHA-256 key and never overwritten. Reads verify the hash.
"""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import TYPE_CHECKING, Protocol

from argfx.config import Settings
from argfx.hashing import object_key, sha256_file

if TYPE_CHECKING:
    from mypy_boto3_s3 import S3Client


class IntegrityError(RuntimeError):
    """Stored bytes do not match the expected SHA-256."""


class ObjectStore(Protocol):
    def exists(self, key: str) -> bool: ...
    def upload(self, path: Path, key: str, content_type: str | None = None) -> None: ...
    def download(self, key: str, dest: Path) -> None: ...
    def list_keys(self, prefix: str = "") -> list[str]: ...
    def delete(self, key: str) -> None: ...


class LocalObjectStore:
    def __init__(self, root: Path) -> None:
        self.root = root

    def _path(self, key: str) -> Path:
        path = (self.root / key).resolve()
        if not path.is_relative_to(self.root.resolve()):
            raise ValueError(f"key escapes store root: {key!r}")
        return path

    def exists(self, key: str) -> bool:
        return self._path(key).is_file()

    def upload(self, path: Path, key: str, content_type: str | None = None) -> None:
        dest = self._path(key)
        dest.parent.mkdir(parents=True, exist_ok=True)
        tmp = dest.with_suffix(".partial")
        shutil.copyfile(path, tmp)
        tmp.replace(dest)

    def download(self, key: str, dest: Path) -> None:
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(self._path(key), dest)

    def list_keys(self, prefix: str = "") -> list[str]:
        if not self.root.exists():
            return []
        keys = (p.relative_to(self.root).as_posix() for p in self.root.rglob("*") if p.is_file())
        return sorted(k for k in keys if k.startswith(prefix) and not k.endswith(".partial"))

    def delete(self, key: str) -> None:
        self._path(key).unlink(missing_ok=True)


class S3ObjectStore:
    def __init__(self, client: S3Client, bucket: str) -> None:
        self.client = client
        self.bucket = bucket

    def exists(self, key: str) -> bool:
        from botocore.exceptions import ClientError

        try:
            self.client.head_object(Bucket=self.bucket, Key=key)
        except ClientError as exc:
            if exc.response.get("Error", {}).get("Code") in {"404", "NoSuchKey", "NotFound"}:
                return False
            raise
        return True

    def upload(self, path: Path, key: str, content_type: str | None = None) -> None:
        extra = {"ContentType": content_type} if content_type else None
        self.client.upload_file(str(path), self.bucket, key, ExtraArgs=extra)

    def download(self, key: str, dest: Path) -> None:
        dest.parent.mkdir(parents=True, exist_ok=True)
        self.client.download_file(self.bucket, key, str(dest))

    def list_keys(self, prefix: str = "") -> list[str]:
        paginator = self.client.get_paginator("list_objects_v2")
        keys: list[str] = []
        for page in paginator.paginate(Bucket=self.bucket, Prefix=prefix):
            keys.extend(obj["Key"] for obj in page.get("Contents", []))
        return keys

    def delete(self, key: str) -> None:
        self.client.delete_object(Bucket=self.bucket, Key=key)


def r2_client(settings: Settings) -> S3Client:
    import boto3

    if not settings.has_r2_credentials:
        raise RuntimeError(
            "R2 credentials missing: set R2_ACCOUNT_ID, R2_ACCESS_KEY_ID and R2_SECRET_ACCESS_KEY"
        )
    assert settings.r2_access_key_id and settings.r2_secret_access_key
    return boto3.client(
        "s3",
        endpoint_url=settings.r2_endpoint,
        aws_access_key_id=settings.r2_access_key_id.get_secret_value(),
        aws_secret_access_key=settings.r2_secret_access_key.get_secret_value(),
        region_name="auto",
    )


def public_store(settings: Settings) -> ObjectStore:
    """The public bucket, written with a token scoped to it."""
    import boto3

    key, secret = settings.r2_public_access_key_id, settings.r2_public_secret_access_key
    if not (settings.r2_endpoint and key and secret):
        raise RuntimeError(
            "public bucket credentials missing: set R2_PUBLIC_ACCESS_KEY_ID and "
            "R2_PUBLIC_SECRET_ACCESS_KEY"
        )
    client = boto3.client(
        "s3",
        endpoint_url=settings.r2_endpoint,
        aws_access_key_id=key.get_secret_value(),
        aws_secret_access_key=secret.get_secret_value(),
        region_name="auto",
    )
    return S3ObjectStore(client, settings.r2_public_bucket)


def get_store(settings: Settings) -> ObjectStore:
    if settings.resolved_storage == "r2":
        return S3ObjectStore(r2_client(settings), settings.r2_bucket)
    return LocalObjectStore(settings.local_objects_dir)


def put_immutable(
    store: ObjectStore, path: Path, content_type: str | None = None
) -> tuple[str, bool]:
    """Store a file under its hash. Returns (sha256, created). Existing keys are never rewritten."""
    sha = sha256_file(path)
    key = object_key(sha)
    if store.exists(key):
        return sha, False
    store.upload(path, key, content_type)
    return sha, True


def fetch_verified(
    store: ObjectStore, sha256: str, dest: Path, cache_dir: Path | None = None
) -> Path:
    """Download an object and check its hash. With `cache_dir`, reuse a verified local copy."""
    if cache_dir is not None:
        cached = cache_dir / object_key(sha256)
        if cached.is_file() and sha256_file(cached) == sha256:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(cached, dest)
            return dest
    store.download(object_key(sha256), dest)
    actual = sha256_file(dest)
    if actual != sha256:
        dest.unlink(missing_ok=True)
        raise IntegrityError(f"expected {sha256}, got {actual}")
    if cache_dir is not None:
        cached = cache_dir / object_key(sha256)
        cached.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(dest, cached)
    return dest
