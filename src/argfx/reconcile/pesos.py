"""Debt payable in pesos held inside the public sector, at the cut-off.

Two layers, kept apart as in `consolidacion.py`:
- official: the share of the debt held by public-sector agencies, by currency and indexation
  (Secretaría de Finanzas, `tenencias/composicion_acreedor_<date>.csv`), applied to its total;
- identified: what each holder reports (`tenencias/tenencias_pesos_<date>.csv`): the BCRA monthly
  balance, the FGS monthly report by category and the Banco Nación statements. Valuations differ
  (book value, market value), so the identified layer checks the order of magnitude of the
  official one and does not replace it.

The gross side is SIGADE by family: CER, nominal pesos (fixed, variable and duals, plus the
transitory advances of the BCRA) and dollar-linked. Amounts in millions of USD at the cut-off
exchange rate of the Finanzas workbook (A.1.1).
"""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

from argfx.contracts.calendar import _write

# SIGADE families payable in pesos, grouped as the official composition groups them.
GROUPS = {
    "ARS CER": "cer",
    "ARS nominal": "pesos",
    "ARS variable": "pesos",
    "dual": "pesos",
    "adelantos transitorios BCRA (intra sector público)": "pesos",
    "dólar-linked": "dolar_linked",
}
OFFICIAL = {"cer": "sector_publico_pesos_cer", "pesos": "sector_publico_pesos",
            "dolar_linked": "sector_publico_dolar_linked"}  # fmt: skip


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def build_peso_consolidation(
    composition_csv: Path,
    holdings_csv: Path,
    instruments_csv: Path,
    ars_per_usd: float,
    out: Path,
) -> dict[str, float]:
    gross: dict[str, float] = defaultdict(float)
    for r in _read(instruments_csv):
        group = GROUPS.get(r["instrument_family"])
        if group:
            gross[group] += float(r["outstanding_usd_equiv_sigade"] or 0) / 1e6
    comp = {r["partida"]: r for r in _read(composition_csv)}
    public_total = float(comp["sector_publico_moneda_total"]["millones_usd"])
    rows = []
    for group, item in OFFICIAL.items():
        public = public_total * float(comp[item]["porcentaje"]) / 100
        rows.append(
            {
                "grupo": group,
                "bruta_musd": round(gross[group], 1),
                "sector_publico_oficial_musd": round(public, 1),
                "sector_publico_pct": round(100 * public / gross[group], 1),
                "en_otras_manos_musd": round(gross[group] - public, 1),
            }
        )
    by_holder: dict[str, float] = defaultdict(float)
    for r in _read(holdings_csv):
        by_holder[r["tenedor"]] += float(r["millones_ars"]) / ars_per_usd
    identified = [
        {"tenedor": h, "millones_usd": round(v, 1)}
        for h, v in sorted(by_holder.items(), key=lambda x: -x[1])
    ]
    _write(out / "pesos_sector_publico.csv", rows)
    _write(out / "pesos_tenencias_identificadas.csv", identified)
    total_gross = sum(r["bruta_musd"] for r in rows)
    total_public = sum(r["sector_publico_oficial_musd"] for r in rows)
    return {
        "pesos_bruta_musd": round(total_gross, 1),
        "pesos_sector_publico_oficial_musd": round(total_public, 1),
        "pesos_sector_publico_pct": round(100 * total_public / total_gross, 1),
        "pesos_identificado_musd": round(sum(by_holder.values()), 1),
    }
