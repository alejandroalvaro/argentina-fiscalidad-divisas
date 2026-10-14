from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

import boto3
import pytest
from moto import mock_aws

from argfx.hashing import object_key, sha256_bytes
from argfx.storage import (
    IntegrityError,
    LocalObjectStore,
    ObjectStore,
    S3ObjectStore,
    fetch_verified,
    put_immutable,
)

BUCKET = "argentina-fx-research"


@pytest.fixture(params=["local", "s3"])
def store(
    request: pytest.FixtureRequest, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> Iterator[ObjectStore]:
    if request.param == "local":
        yield LocalObjectStore(tmp_path / "objects")
        return
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")
    with mock_aws():
        client = boto3.client("s3", region_name="us-east-1")
        client.create_bucket(Bucket=BUCKET)
        yield S3ObjectStore(client, BUCKET)


def test_object_key_is_sharded() -> None:
    sha = sha256_bytes(b"x")
    assert object_key(sha) == f"objects/sha256/{sha[:2]}/{sha[2:4]}/{sha}"
    with pytest.raises(ValueError):
        object_key("not-a-hash")


def test_put_is_idempotent_and_roundtrips(store: ObjectStore, tmp_path: Path) -> None:
    src = tmp_path / "doc.pdf"
    src.write_bytes(b"%PDF-1.7 fake prospectus")
    sha, created = put_immutable(store, src, "application/pdf")
    assert created
    assert sha == sha256_bytes(src.read_bytes())

    again, created_again = put_immutable(store, src)
    assert again == sha and not created_again
    assert store.list_keys("objects/") == [object_key(sha)]

    out = fetch_verified(store, sha, tmp_path / "out" / "doc.pdf")
    assert out.read_bytes() == src.read_bytes()


def test_fetch_detects_corruption(store: ObjectStore, tmp_path: Path) -> None:
    good, bad = tmp_path / "good.bin", tmp_path / "bad.bin"
    good.write_bytes(b"original")
    bad.write_bytes(b"tampered")
    sha = sha256_bytes(b"original")
    store.upload(bad, object_key(sha))  # simulate a corrupted object under the right key
    with pytest.raises(IntegrityError):
        fetch_verified(store, sha, tmp_path / "out.bin")
    assert not (tmp_path / "out.bin").exists()


def test_fetch_uses_verified_cache(store: ObjectStore, tmp_path: Path) -> None:
    src = tmp_path / "a.csv"
    src.write_bytes(b"a,b\n1,2\n")
    sha, _ = put_immutable(store, src)
    cache = tmp_path / "cache"
    fetch_verified(store, sha, tmp_path / "first.csv", cache)
    store.delete(object_key(sha))  # remote gone: the second fetch must come from cache
    second = fetch_verified(store, sha, tmp_path / "second.csv", cache)
    assert second.read_bytes() == src.read_bytes()


def test_local_store_rejects_path_escape(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        LocalObjectStore(tmp_path / "objects").exists("../outside")
