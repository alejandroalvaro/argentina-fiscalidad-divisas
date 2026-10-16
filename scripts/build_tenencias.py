"""Build tenencias/tenencias_identificadas_2026-06-30.csv: Treasury debt held inside the public
sector, instrument by instrument, with the method of each row.

- directo: SIGADE assigns the creditor (letras intransferibles with the BCRA) or the name says it
  (LETRA/U$S/INTRA SP).
- estimado: BCRA holdings of USD bonds at 2025-12-31 (Anexo III of its financial statements,
  mapped in lote S), and the AL35 and AE38 delivered to the BCRA in the RC 31/2026 conversion
  (ONCP, Otras Operaciones). Whether the BCRA still held them at the cut-off is not published.

Face values are original face in USD; the reconciliation turns them into the residual face.
"""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "tenencias" / "tenencias_identificadas_2026-06-30.csv"
FIELDS = ["instrument_id", "tenedor", "valor_nominal_original_usd", "metodo", "fecha_dato",
          "source_id", "referencia"]  # fmt: skip


def main() -> None:
    rows = []
    with (ROOT / "contratos" / "terminos.csv").open(newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["tipo_acreedor"] == "BCRA" and float(r["saldo_corte"] or 0) > 0:
                rows.append({
                    "instrument_id": r["instrument_id"], "tenedor": "BCRA",
                    "valor_nominal_original_usd": r["saldo_corte"], "metodo": "directo",
                    "fecha_dato": "2026-06-30", "source_id": "SRC-0102",
                    "referencia": f"{r['nombre']}: SIGADE la registra con acreedor BCRA; "
                    "la tenencia es todo el saldo",
                })  # fmt: skip
    with (ROOT / "inbox" / "lote-c" / "instruments.csv").open(newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if "INTRA SP" in r["operation_name_sigade"].upper():
                rows.append({
                    "instrument_id": r["instrument_id"], "tenedor": "sector público (sin detalle)",
                    "valor_nominal_original_usd": r["outstanding_principal"], "metodo": "directo",
                    "fecha_dato": "2026-06-30", "source_id": "SRC-0102",
                    "referencia": f"{r['operation_name_sigade']}: el nombre en SIGADE dice "
                    "intra sector público; la tenencia es todo el saldo",
                })  # fmt: skip
    mapping = ROOT / "inbox" / "lote-s" / "tablas" / "mapeo_anexo_iii_bcra_a_instrument_id.csv"
    with mapping.open(newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            vn = r["vn_original_miles_EECC2025_col2025"]
            if r["moneda_publicada"] != "USD" or not vn or not r["instrument_id"]:
                continue
            if (
                "Intransferible" in r["especie_texto_publicado"]
                or "Letra" in r["especie_texto_publicado"]
            ):
                continue  # the letters come from SIGADE above, at the cut-off
            rows.append({
                "instrument_id": r["instrument_id"], "tenedor": "BCRA",
                "valor_nominal_original_usd": str(float(vn) * 1000), "metodo": "estimado",
                "fecha_dato": "2025-12-31", "source_id": "SRC-1156",
                "referencia": f"{r['especie_texto_publicado']}: Anexo III de los estados contables "
                f"del BCRA al 31-12-2025 (mapeo del lote S, confianza {r['confianza']}); se supone "
                "sin cambios hasta el corte",
            })  # fmt: skip
    for iid, vn, row in (("INS-C-0405", "4390330748", 22), ("INS-C-0403", "2261685537", 23)):
        rows.append({
            "instrument_id": iid, "tenedor": "BCRA", "valor_nominal_original_usd": vn,
            "metodo": "estimado", "fecha_dato": "2026-06-08", "source_id": "SRC-0947",
            "referencia": "entregado al BCRA en la conversión de la RC 31/2026 (ONCP, "
            f"colocaciones 2026, Otras Operaciones fila {row}); que lo tuviera al corte es un "
            "supuesto",
        })  # fmt: skip
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=FIELDS, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"{len(rows)} filas en {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
