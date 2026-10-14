"""Runtime settings, read from environment variables and the local `.env` file.

Secrets are held as `SecretStr` so they never show up in reprs, logs or tracebacks.
"""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import AliasChoices, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

StorageBackend = Literal["auto", "r2", "local"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # Cloudflare R2 (S3-compatible). Names match the variables in `.env`.
    r2_account_id: str | None = None
    r2_access_key_id: SecretStr | None = None
    r2_secret_access_key: SecretStr | None = None
    r2_bucket: str = "argentina-fx-research"

    # Local paths. Everything under data_dir is regenerable or mirrored in R2 and stays out of Git.
    data_dir: Path = Field(default=Path("data"), validation_alias=AliasChoices("ARGFX_DATA_DIR"))
    manifests_dir: Path = Field(
        default=Path("manifests"), validation_alias=AliasChoices("ARGFX_MANIFESTS_DIR")
    )
    storage: StorageBackend = Field(default="auto", validation_alias=AliasChoices("ARGFX_STORAGE"))

    @property
    def r2_endpoint(self) -> str | None:
        if not self.r2_account_id:
            return None
        return f"https://{self.r2_account_id}.r2.cloudflarestorage.com"

    @property
    def has_r2_credentials(self) -> bool:
        return bool(self.r2_account_id and self.r2_access_key_id and self.r2_secret_access_key)

    @property
    def resolved_storage(self) -> Literal["r2", "local"]:
        """`auto` uses R2 when credentials are present and the local object store otherwise."""
        if self.storage == "auto":
            return "r2" if self.has_r2_credentials else "local"
        return self.storage

    @property
    def local_objects_dir(self) -> Path:
        return self.data_dir / "objects"

    @property
    def cache_dir(self) -> Path:
        return self.data_dir / "cache"

    @property
    def duckdb_path(self) -> Path:
        return self.cache_dir / "argfx.duckdb"

    def public_summary(self) -> dict[str, str]:
        """Configuration safe to print: secrets reduced to present/missing."""
        return {
            "storage": f"{self.storage} -> {self.resolved_storage}",
            "r2_bucket": self.r2_bucket,
            "r2_endpoint": self.r2_endpoint or "(missing R2_ACCOUNT_ID)",
            "r2_access_key_id": "present" if self.r2_access_key_id else "missing",
            "r2_secret_access_key": "present" if self.r2_secret_access_key else "missing",
            "data_dir": str(self.data_dir),
            "manifests_dir": str(self.manifests_dir),
            "duckdb_path": str(self.duckdb_path),
        }


def get_settings(**overrides: object) -> Settings:
    return Settings(**overrides)  # type: ignore[arg-type]
