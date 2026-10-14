from __future__ import annotations

from pathlib import Path

import pytest

from argfx.config import Settings


def test_defaults_are_offline() -> None:
    s = Settings(_env_file=None)  # type: ignore[call-arg]
    assert not s.has_r2_credentials
    assert s.resolved_storage == "local"
    assert s.r2_bucket == "argentina-fx-research"


def test_reads_env_file_and_ignores_unknown_keys(tmp_path: Path) -> None:
    env = tmp_path / ".env"
    env.write_text(
        "R2_ACCOUNT_ID=abc123\nR2_ACCESS_KEY_ID=key\nR2_SECRET_ACCESS_KEY=topsecret\n"
        "R2_BUCKET=argentina-fx-research\nSOMETHING_ELSE=1\n# comment\n"
    )
    s = Settings(_env_file=env)  # type: ignore[call-arg]
    assert s.has_r2_credentials
    assert s.resolved_storage == "r2"
    assert s.r2_endpoint == "https://abc123.r2.cloudflarestorage.com"


def test_secrets_never_leak_into_repr_or_summary(tmp_path: Path) -> None:
    s = Settings(
        _env_file=None,  # type: ignore[call-arg]
        r2_account_id="acct",
        r2_access_key_id="AKIDVALUE",
        r2_secret_access_key="SECRETVALUE",
    )
    text = repr(s) + str(s.public_summary())
    assert "AKIDVALUE" not in text
    assert "SECRETVALUE" not in text


@pytest.mark.parametrize("value", ["local", "r2"])
def test_explicit_storage_wins(monkeypatch: pytest.MonkeyPatch, value: str) -> None:
    monkeypatch.setenv("ARGFX_STORAGE", value)
    assert Settings(_env_file=None).resolved_storage == value  # type: ignore[call-arg]
