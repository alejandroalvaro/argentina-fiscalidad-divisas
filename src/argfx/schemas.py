"""Row schemas for Grok batches (`inbox/<lote>/`).

Columns follow `docs/protocolo/GROK_TASKS.md`. A blank cell means unknown and is kept as None;
it is never read as zero. Extra columns are allowed and reported, never dropped.
"""

from __future__ import annotations

import re
from datetime import date, datetime
from typing import Annotated, Literal

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, field_validator

SOURCE_ID = r"^SRC-\d{4}$"
CLAIM_ID = r"^CLM-[A-Z]-\d{3}$"
INSTRUMENT_ID = r"^INS-[A-Z]-\d{4}$"
SHA256 = r"^[0-9a-f]{64}$"

# ISO 4217 codes in use, plus XDR (SDR). Retired codes such as ARP are rejected on purpose.
ISO_4217 = frozenset(
    {
        "AED",
        "ARS",
        "AUD",
        "BOB",
        "BRL",
        "CAD",
        "CHF",
        "CLP",
        "CNY",
        "COP",
        "DKK",
        "DZD",
        "EUR",
        "GBP",
        "HKD",
        "INR",
        "JPY",
        "KRW",
        "KWD",
        "MXN",
        "NOK",
        "NZD",
        "PEN",
        "PYG",
        "SAR",
        "SEK",
        "SGD",
        "USD",
        "UYU",
        "XDR",
        "ZAR",
    }
)


def _blank_to_none(value: object) -> object:
    if isinstance(value, str) and value.strip() == "":
        return None
    return value


Opt = BeforeValidator(_blank_to_none)
OptStr = Annotated[str | None, Opt]
OptDate = Annotated[date | None, Opt]
OptFloat = Annotated[float | None, Opt]


def isin_is_valid(isin: str) -> bool:
    """ISO 6166 check digit (Luhn over letters expanded to numbers)."""
    if not re.fullmatch(r"[A-Z]{2}[A-Z0-9]{9}\d", isin):
        return False
    digits = "".join(str(int(c, 36)) for c in isin[:-1])
    total = 0
    for i, d in enumerate(reversed(digits)):
        n = int(d) * (2 if i % 2 == 0 else 1)
        total += n // 10 + n % 10
    return (10 - total % 10) % 10 == int(isin[-1])


class Row(BaseModel):
    model_config = ConfigDict(extra="allow", str_strip_whitespace=True)


class Source(Row):
    source_id: str = Field(pattern=SOURCE_ID)
    issuer: str
    title: str
    url: str = Field(pattern=r"^https?://")
    publication_date: OptDate = None
    accessed_at: date
    period_covered: OptStr = None
    document_type: str
    sha256: Annotated[str | None, Opt, Field(pattern=SHA256)] = None
    license_notes: OptStr = None
    local_object_key: OptStr = None


class Claim(Row):
    claim_id: str = Field(pattern=CLAIM_ID)
    claim: str
    source_id: str = Field(pattern=SOURCE_ID)
    page_or_section: OptStr = None
    exact_evidence: str
    confidence: Literal["alta", "media", "baja"]
    review_status: Literal["sin_revisar", "revisado", "rechazado"]


class ManifestRow(Row):
    sha256: str = Field(pattern=SHA256)
    size_bytes: int = Field(ge=0)
    object_key: str
    media_type: OptStr = None
    original_filename: str
    source_id: str
    ingested_at: datetime
    local_object_key: OptStr = None
    # original: the downloaded document. derivado: a file Grok produced (export, table).
    # A derived file may cite several sources as "SRC-0001;SRC-0002".
    rol: Annotated[Literal["original", "derivado"] | None, Opt] = None


Indexation = Literal[
    "ninguna",  # contract has no indexation
    "ninguna informada",  # the source reports none; not the same as "ninguna"
    "CER",
    "UVA",
    "dólar-linked (pagadero en ARS)",
    "TAMAR",
    "BADLAR",
]


class Instrument(Row):
    instrument_id: str = Field(pattern=INSTRUMENT_ID)
    issuer: str
    isin: OptStr = None
    currency_of_account: str
    currency_of_payment: str
    indexation: Indexation
    outstanding_principal: OptFloat = None
    as_of_date: date
    source_id: str = Field(pattern=SOURCE_ID)
    review_status: Literal["candidato_sin_revisar", "revisado", "rechazado"]

    @field_validator("currency_of_account", "currency_of_payment")
    @classmethod
    def iso_currency(cls, v: str) -> str:
        if v not in ISO_4217:
            raise ValueError(f"{v!r} is not an ISO 4217 code in use (pesos are ARS, not ARP)")
        return v

    @field_validator("isin")
    @classmethod
    def isin_check(cls, v: str | None) -> str | None:
        if v is not None and not isin_is_valid(v):
            raise ValueError(f"invalid ISIN {v!r}")
        return v


class SeriesObservation(Row):
    series_id: str
    fecha: date
    valor: OptFloat = None
    unidad: OptStr = None
    source_id: str = Field(pattern=SOURCE_ID)


# file name inside inbox/<lote>/ -> schema
FILE_SCHEMAS: dict[str, type[Row]] = {
    "sources.csv": Source,
    "claims.csv": Claim,
    "documents_manifest.csv": ManifestRow,
    "instruments.csv": Instrument,
}
SERIES_GLOB = "tablas/series_*.csv"
