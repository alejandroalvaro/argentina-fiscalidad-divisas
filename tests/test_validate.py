from __future__ import annotations

import csv
from pathlib import Path

from argfx.schemas import Instrument, isin_is_valid
from argfx.validate import validate_inbox, write_report

SHA_A = "a" * 64
SHA_B = "b" * 64

SOURCE_COLS = [
    "source_id", "issuer", "title", "url", "publication_date", "accessed_at", "period_covered",
    "document_type", "sha256", "license_notes", "local_object_key",
]  # fmt: skip
CLAIM_COLS = [
    "claim_id", "claim", "source_id", "page_or_section", "exact_evidence", "confidence",
    "review_status",
]  # fmt: skip
MANIFEST_COLS = [
    "sha256", "size_bytes", "object_key", "media_type", "original_filename", "source_id",
    "ingested_at", "local_object_key",
]  # fmt: skip


def write(path: Path, cols: list[str], rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(rows)


def source(sid: str, sha: str = SHA_A) -> dict[str, str]:
    return {
        "source_id": sid, "issuer": "BCRA", "title": "t", "url": "https://bcra.gob.ar/x.pdf",
        "publication_date": "", "accessed_at": "2026-10-14", "period_covered": "",
        "document_type": "pdf", "sha256": sha, "license_notes": "", "local_object_key": "",
    }  # fmt: skip


def manifest(sid: str, sha: str = SHA_A, **extra: str) -> dict[str, str]:
    return {
        "sha256": sha, "size_bytes": "10", "object_key": f"objects/{sha}", "media_type": "",
        "original_filename": "x.pdf", "source_id": sid, "ingested_at": "2026-10-14T10:00:00Z",
        "local_object_key": "", **extra,
    }  # fmt: skip


def claim(cid: str, sid: str) -> dict[str, str]:
    return {
        "claim_id": cid, "claim": "c", "source_id": sid, "page_or_section": "p. 1",
        "exact_evidence": "e", "confidence": "alta", "review_status": "sin_revisar",
    }  # fmt: skip


def make_batch(root: Path, lote: str, sources: list[dict[str, str]],
               claims: list[dict[str, str]], manifest_rows: list[dict[str, str]],
               manifest_cols: list[str] = MANIFEST_COLS) -> None:  # fmt: skip
    d = root / lote
    write(d / "sources.csv", SOURCE_COLS, sources)
    write(d / "claims.csv", CLAIM_COLS, claims)
    write(d / "documents_manifest.csv", manifest_cols, manifest_rows)
    (d / "unresolved.md").write_text("nada\n")


def codes(root: Path) -> dict[str, int]:
    out: dict[str, int] = {}
    for i in validate_inbox(root).issues:
        out[i.code] = out.get(i.code, 0) + i.count
    return out


def test_clean_batch_has_no_errors(tmp_path: Path) -> None:
    make_batch(tmp_path, "lote-a", [source("SRC-0001")], [claim("CLM-A-001", "SRC-0001")],
               [manifest("SRC-0001")])  # fmt: skip
    report = validate_inbox(tmp_path)
    assert report.errors == 0 and report.warnings == 0


def test_cross_batch_duplicates_and_unknown_sources(tmp_path: Path) -> None:
    make_batch(tmp_path, "lote-a", [source("SRC-0001")], [claim("CLM-A-001", "SRC-0009")],
               [manifest("SRC-0001")])  # fmt: skip
    make_batch(tmp_path, "lote-b", [source("SRC-0001")], [claim("CLM-A-001", "SRC-0001")],
               [manifest("SRC-0001")])  # fmt: skip
    found = codes(tmp_path)
    assert found["duplicate_id"] == 2  # SRC-0001 and CLM-A-001
    assert found["unknown_source"] == 1


def test_derived_manifest_rows_must_be_marked(tmp_path: Path) -> None:
    cols = [*MANIFEST_COLS, "rol"]
    make_batch(tmp_path, "lote-c", [source("SRC-0001")], [],
               [manifest("SRC-0001", rol="original"), manifest("SRC-0001", SHA_B, rol="")],
               cols)  # fmt: skip
    assert codes(tmp_path) == {"sha_mismatch": 1}

    make_batch(tmp_path, "lote-c", [source("SRC-0001")], [],
               [manifest("SRC-0001", rol="original"),
                manifest("SRC-0001", SHA_B, rol="derivado"),
                manifest("varios (ver tabla)", SHA_B, rol="derivado")], cols)  # fmt: skip
    assert codes(tmp_path) == {"nonstandard_source_ref": 1}


def test_missing_files_and_bad_values(tmp_path: Path) -> None:
    bad = claim("CLM-A-1", "SRC-0001") | {"confidence": "altísima"}
    make_batch(tmp_path, "lote-a", [source("SRC-0001")], [bad], [manifest("SRC-0001")])
    (tmp_path / "lote-a" / "unresolved.md").unlink()
    found = codes(tmp_path)
    assert found["missing_file"] == 1
    assert found["invalid_value"] == 2  # claim_id pattern and confidence


def test_blank_is_unknown_never_zero() -> None:
    row = {
        "instrument_id": "INS-C-0001", "issuer": "Tesoro", "isin": "", "currency_of_account": "USD",
        "currency_of_payment": "ARS", "indexation": "dólar-linked (pagadero en ARS)",
        "outstanding_principal": "", "as_of_date": "2026-06-30", "source_id": "SRC-0102",
        "review_status": "candidato_sin_revisar",
    }  # fmt: skip
    ins = Instrument.model_validate(row)
    assert ins.outstanding_principal is None and ins.isin is None


def test_retired_currency_code_rejected() -> None:
    import pytest
    from pydantic import ValidationError

    row = {
        "instrument_id": "INS-C-0001", "issuer": "Tesoro", "currency_of_account": "ARS",
        "currency_of_payment": "ARP", "indexation": "ninguna", "as_of_date": "2026-06-30",
        "source_id": "SRC-0102", "review_status": "candidato_sin_revisar",
    }  # fmt: skip
    with pytest.raises(ValidationError, match="ARP"):
        Instrument.model_validate(row)


def test_isin_check_digit() -> None:
    assert isin_is_valid("US040114HS26")  # Argentina 2030 global bond
    assert not isin_is_valid("US040114HS27")
    assert not isin_is_valid("AR123")


def test_report_files(tmp_path: Path) -> None:
    make_batch(tmp_path, "lote-a", [source("SRC-0001")], [claim("CLM-A-001", "SRC-0002")],
               [manifest("SRC-0001")])  # fmt: skip
    csv_path, md_path = write_report(validate_inbox(tmp_path), tmp_path / "out")
    assert "unknown_source" in md_path.read_text()
    assert len(list(csv.DictReader(csv_path.open()))) == 1


def test_term_sheets_checked_against_instruments(tmp_path: Path) -> None:
    make_batch(tmp_path, "lote-c", [source("SRC-0001")], [], [manifest("SRC-0001")])
    ins_cols = [
        "instrument_id", "issuer", "currency_of_account", "currency_of_payment", "indexation",
        "outstanding_principal", "as_of_date", "source_id", "review_status",
    ]  # fmt: skip
    write(tmp_path / "lote-c" / "instruments.csv", ins_cols, [{
        "instrument_id": "INS-C-0001", "issuer": "Tesoro", "currency_of_account": "USD",
        "currency_of_payment": "USD", "indexation": "ninguna", "outstanding_principal": "100",
        "as_of_date": "2026-06-30", "source_id": "SRC-0001",
        "review_status": "candidato_sin_revisar",
    }])  # fmt: skip
    term = {
        "instrument_id": "INS-C-0001", "nombre": "x", "deudor": "Tesoro",
        "tipo_acreedor": "desconocido", "residencia_tenedor": "desconocida",
        "moneda_cuenta": "USD", "indexacion": "ninguna", "moneda_liquidacion": "USD",
        "estado": "firme", "fecha_corte": "2026-06-30", "saldo_corte": "100",
        "fecha_emision": "2026-01-01", "primer_periodo": "2026-07-01",
        "vencimiento": "2027-01-01", "frecuencia_meses": "6", "fin_de_mes": "false",
        "base": "30/360", "tipo_tasa": "cero", "indice": "", "margen": "", "multiplicador": "",
        "capitaliza": "false", "source_id": "SRC-0001", "referencia": "p. 1", "notas": "",
    }  # fmt: skip
    d = tmp_path / "lote-g" / "contratos"
    make_batch(tmp_path, "lote-g", [], [], [])
    write(d / "terminos.csv", list(term), [term])
    write(d / "tasas.csv", ["instrument_id", "desde", "tasa", "source_id", "referencia"], [])
    amort_cols = ["instrument_id", "fecha", "fraccion", "source_id", "referencia"]
    write(d / "amortizaciones.csv", amort_cols, [])
    assert "term_sheet_invalid" not in codes(tmp_path)
    assert "balance_mismatch" not in codes(tmp_path)

    write(d / "terminos.csv", list(term), [term | {"saldo_corte": "90"}])
    assert codes(tmp_path)["balance_mismatch"] == 1

    write(d / "terminos.csv", list(term), [term | {"instrument_id": "INS-C-0002"}])
    assert codes(tmp_path)["unknown_instrument"] == 1

    write(d / "terminos.csv", list(term), [term])
    write(d / "amortizaciones.csv", amort_cols, [{
        "instrument_id": "INS-C-0001", "fecha": "2027-01-01", "fraccion": "0.5",
        "source_id": "SRC-0001", "referencia": "p. 2",
    }])  # fmt: skip
    assert codes(tmp_path)["term_sheet_invalid"] == 1
