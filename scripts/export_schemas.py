"""Export the row schemas to JSON Schema in schemas/, so a batch can be checked without argfx.

Usage: uv run python scripts/export_schemas.py
"""

from __future__ import annotations

import json
from pathlib import Path

from argfx.contracts.terms import AmortizationRow, DateRow, RateRow, TermRow
from argfx.schemas import Claim, Instrument, ManifestRow, SeriesObservation, Source

OUT = Path(__file__).resolve().parent.parent / "schemas"
MODELS = {
    "sources": Source,
    "claims": Claim,
    "documents_manifest": ManifestRow,
    "instruments": Instrument,
    "series": SeriesObservation,
    "contratos_terminos": TermRow,
    "contratos_tasas": RateRow,
    "contratos_amortizaciones": AmortizationRow,
    "contratos_fechas": DateRow,
}

if __name__ == "__main__":
    for name, model in MODELS.items():
        schema = model.model_json_schema()
        schema["$comment"] = "Generated from src/argfx/schemas.py; do not edit by hand."
        path = OUT / f"{name}.schema.json"
        path.write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(path.relative_to(OUT.parent))
