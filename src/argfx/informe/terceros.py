"""Debt with holders outside the public sector, each currency in its own unit (D-017).

Finanzas publishes the private holding in all currencies together, converted to dollars, and
its split by currency only as percentages of a pie chart. This module opens it: the part paid
in foreign currency stays in millions of USD, and the part paid in pesos (pesos, CER and dollar
linked) goes back to pesos at the A 3500 rate of the cut-off, the rate Finanzas used.

On the peso side, the Treasury is not alone: at the end of 2023 the BCRA owed its own
remunerated liabilities (pases, LELIQ) to the banks. The consolidated row adds them, so the
transfer of the absorption from the BCRA to the Treasury (chapter 3) does not read as new debt.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

FX_SHARES = ("pct_dolares", "pct_euros_y_otros")
PESO_SHARES = ("pct_dolar_linked", "pct_cer", "pct_pesos")


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def read_structure(path: Path) -> dict[str, dict[str, float]]:
    out: dict[str, dict[str, float]] = defaultdict(dict)
    for r in _read(path):
        out[r["corte"]][r["concepto"]] = float(r["valor"])
    return dict(out)


def third_party_debt(
    structure: dict[str, dict[str, float]],
    holders_csv: Path,
    remunerated_csv: Path,
    rate_eom: dict[str, float],
    cpi: dict[str, float],
    base_mes: str,
) -> list[dict[str, object]]:
    """One row per cut-off. Millions of USD for foreign currency; trillions of pesos, current
    and of `base_mes`, for pesos."""
    holders = {r["corte"]: r for r in _read(holders_csv)}
    remunerated = {r["mes"]: r for r in _read(remunerated_csv)}
    rows = []
    for corte, s in sorted(structure.items()):
        mes = corte[:7]
        h = holders[corte]
        private = float(h["deuda_en_poder_del_sector_privado_usd_millones"])
        agencies = float(h["multilaterales_y_bilaterales_usd_millones"])
        base, holdouts = s["base_privados_sin_holdouts"], s["holdouts"]
        if abs(base + holdouts - private) > 1:
            raise ValueError(f"{corte}: pie base plus holdouts {base + holdouts} != {private}")
        fx_private = base * sum(s[k] for k in FX_SHARES) / 100
        peso_private_musd = base * sum(s[k] for k in PESO_SHARES) / 100
        rate = rate_eom[mes]
        peso_private = peso_private_musd * rate / 1e6
        bcra = (
            float(remunerated[mes]["total_pasivos_remunerados_pases_leliq_lefi_otros_mm_ars"]) / 1e6
        )
        k = cpi[base_mes] / cpi[mes]
        fx_public = s["divisas_pago_normal_total"] - fx_private - agencies
        rows.append(
            {
                "corte": corte,
                "divisas_privados_usd": round(fx_private),
                "divisas_holdouts_usd": round(holdouts),
                "divisas_organismos_usd": round(agencies),
                "divisas_terceros_usd": round(fx_private + agencies),
                "divisas_sector_publico_usd": round(fx_public),
                "divisas_total_pago_normal_usd": round(s["divisas_pago_normal_total"]),
                "pesos_privados_tesoro_usd": round(peso_private_musd),
                "tipo_de_cambio": rate,
                "pesos_privados_tesoro_corrientes": round(peso_private, 2),
                "pasivos_remunerados_bcra_corrientes": round(bcra, 2),
                "pesos_terceros_consolidado_corrientes": round(peso_private + bcra, 2),
                "pesos_privados_tesoro_constantes": round(peso_private * k, 1),
                "pasivos_remunerados_bcra_constantes": round(bcra * k, 1),
                "pesos_terceros_consolidado_constantes": round((peso_private + bcra) * k, 1),
                "pesos_de": base_mes,
            }
        )
    return rows


def write_rows(rows: list[dict[str, object]], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    return path
