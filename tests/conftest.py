from __future__ import annotations

from pathlib import Path

import pytest

from argfx.config import Settings

R2_VARS = ("R2_ACCOUNT_ID", "R2_ACCESS_KEY_ID", "R2_SECRET_ACCESS_KEY", "R2_BUCKET")


@pytest.fixture(autouse=True)
def offline_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    """Tests never see the developer's real `.env` or R2 credentials."""
    for var in (*R2_VARS, "ARGFX_STORAGE", "ARGFX_DATA_DIR", "ARGFX_MANIFESTS_DIR"):
        monkeypatch.delenv(var, raising=False)
    monkeypatch.chdir(tmp_path)


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    return Settings(
        _env_file=None,  # type: ignore[call-arg]
        ARGFX_DATA_DIR=tmp_path / "data",
        ARGFX_MANIFESTS_DIR=tmp_path / "manifests",
        ARGFX_STORAGE="local",
    )
