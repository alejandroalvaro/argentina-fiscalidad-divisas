"""The whole yearly dollar account: what the country needs besides public debt service.

Chapter 2.5 compares third-party maturities with the goods surplus the IMF projects. That leaves
out the other uses of dollars: services (tourism above all), private interest and dividends, and
the purchases of dollars by persons and firms. This module measures them and puts them in one
table, in millions of USD.

- Observed: the BCRA foreign-exchange market by sector and concept (SRC-1604). The workbook's
  pivot sheets only show totals, so the records are read from its pivot cache, which keeps every
  (month, sector, concept) amount in dollars. Persons ("Personas Humanas") are kept apart from
  firms, so that what persons bought since April 2025 can be compared with what firms bought when
  they were free to buy, in 2017-2019.
- Projected: the IMF balance of payments of the second review (SRC-1263, table 2) for goods,
  services, primary and secondary income and the public interest inside primary income.
- Scenarios: yearly purchases of dollars by persons and firms at an observed pace. They are
  assumptions, written apart from the observed and the projected rows.
"""

from __future__ import annotations

import csv
import re
import zipfile
from collections import defaultdict
from pathlib import Path
from xml.etree.ElementTree import iterparse

NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
PERSONS = "Personas Humanas"
# Not firms: the public sector (spelt two ways in the cache) and banks and exchange houses.
NOT_FIRMS = ("Sector P", "Entidades financieras")
# Concept keys, from the B (group) and D (detail) fields of the pivot cache.
HOARDING = "Compra-venta de billetes y divisas"
TRAVEL = ("tarjetas y viajes", "Transporte de pasajeros")


def _cache_fields(definition: str) -> tuple[list[str], dict[str, list[str]]]:
    names: list[str] = []
    items: dict[str, list[str]] = {}
    for m in re.finditer(r'<cacheField name="([^"]*)"[^>]*>(.*?)</cacheField>', definition, re.S):
        names.append(m.group(1))
        items[m.group(1)] = re.findall(r'<(?:s|n|d) v="([^"]*)"', m.group(2))
    return names, items


def concepts(sector: str, group: str, detail: str) -> list[str]:
    """The keys of this table that a market record adds to (a record can add to none)."""
    out = []
    if HOARDING in group:
        if sector == PERSONS:
            out.append("atesoramiento_personas")
        elif not sector.startswith(NOT_FIRMS):
            out.append("atesoramiento_empresas")
    if group == "02- Servicios":
        out.append("viajes" if any(t in detail for t in TRAVEL) else "otros_servicios")
    if detail.startswith("Utilidades y Dividendos"):
        out.append("utilidades")
    if detail.startswith("Intereses") and not sector.startswith("Sector P"):
        out.append("intereses_privados")
    if group.startswith("01- Bienes"):
        out.append("bienes")
    if group.startswith("02- Préstamos") and not sector.startswith("Sector P"):
        out.append("prestamos_privados")
    if detail.startswith(("Inversión directa - Ingresos", "Inversión de portafolio - Ingresos")):
        out.append("inversion_no_residentes")
    return out


def read_market(xlsx: Path) -> dict[str, dict[str, float]]:
    """Month (YYYY-MM) -> concept -> millions of USD, from the workbook's pivot cache."""
    with zipfile.ZipFile(xlsx) as z:
        names, items = _cache_fields(
            z.read("xl/pivotCache/pivotCacheDefinition1.xml").decode("utf-8")
        )
        out: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
        with z.open("xl/pivotCache/pivotCacheRecords1.xml") as fh:
            for _, el in iterparse(fh):
                if el.tag != NS + "r":
                    continue
                rec: dict[str, str] = {}
                for name, child in zip(names, el, strict=False):
                    v = child.get("v", "")
                    rec[name] = items[name][int(v)] if child.tag == NS + "x" else v
                el.clear()
                keys = concepts(rec["Sector"], rec["B"], rec["D"])
                if keys:
                    month = out[rec["Mes"][:7]]
                    for k in keys:
                        month[k] += float(rec["Monto"]) / 1e6
    return {m: dict(v) for m, v in out.items()}


def yearly_pace(monthly: dict[str, dict[str, float]], desde: str, hasta: str) -> dict[str, float]:
    """Average of the months in [desde, hasta], times twelve."""
    months = [m for m in monthly if desde <= m <= hasta]
    if not months:
        raise ValueError(f"sin datos del mercado de cambios entre {desde} y {hasta}")
    total: dict[str, float] = defaultdict(float)
    for m in months:
        for k, v in monthly[m].items():
            total[k] += v
    return {k: v * 12 / len(months) for k, v in total.items()}


def dollar_account(
    imf: list[dict[str, str]],
    maturities: dict[int, float],
    persons: dict[str, float],
    firms: float,
) -> list[dict[str, object]]:
    """Yearly account for each year with an IMF projection and a maturity figure.

    `persons` maps a scenario label to yearly purchases by persons; `firms` is the yearly purchase
    by firms if their restriction is lifted. Amounts are positive for uses of dollars.
    """
    rows: list[dict[str, object]] = []
    for r in imf:
        year = int(r["anio"])
        if year not in maturities:
            continue
        goods = float(r["balanza_bienes_musd"])
        secondary = float(r["ingreso_secundario_musd"])
        services = -float(r["servicios_musd"])
        private_income = -(float(r["ingreso_primario_musd"]) - float(r["interes_publico_musd"]))
        before_debt = goods + secondary - services - private_income
        before_hoarding = before_debt - maturities[year]
        row: dict[str, object] = {
            "anio": year,
            "saldo_bienes": goods,
            "ingreso_secundario": secondary,
            "servicios": services,
            "rentas_privadas": private_income,
            "disponible_para_deuda": round(before_debt),
            "vencimientos_terceros": round(maturities[year]),
            "resultado_antes_de_atesoramiento": round(before_hoarding),
            "empresas_sin_cepo": round(firms),
        }
        for label, amount in persons.items():
            row[f"personas_{label}"] = round(amount)
            row[f"brecha_{label}"] = round(before_hoarding - amount)
            row[f"brecha_{label}_y_empresas"] = round(before_hoarding - amount - firms)
        rows.append(row)
    return rows


def read_maturities(chart_csv: Path) -> dict[int, float]:
    """Third-party maturities by year from the chart table of chapter 2.5."""
    with chart_csv.open(newline="", encoding="utf-8") as fh:
        return {
            int(r["x"]): float(r["valor"])
            for r in csv.DictReader(fh)
            if r["serie"].startswith("Vencimientos")
        }


def write_rows(rows: list[dict[str, object]], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    return path
