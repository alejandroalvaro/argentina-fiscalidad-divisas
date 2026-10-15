"""Read term sheets from `contratos/`: three CSV tables, each row citing its source.

- `terminos.csv`: one row per instrument (dimensions, balance at the cut-off, schedule, rate type).
- `tasas.csv`: fixed-rate steps (instrument_id, desde, tasa).
- `amortizaciones.csv`: amortization dates and fractions of the original face.
- `fechas.csv` (optional): the full list of period ends, for instruments whose norm enumerates
  them instead of following a grid. It replaces primer_periodo/frecuencia for that instrument.

A blank cell is unknown. The engine refuses a term sheet with missing required terms instead of
guessing them.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from argfx.contracts.daycount import DayCount
from argfx.contracts.engine import FixedRate, FloatingRate, Rate, TermSheet, ZeroRate
from argfx.contracts.model import CreditorType, Indexation, Obligation, Residency, Status
from argfx.contracts.schedule import regular_dates
from argfx.schemas import INSTRUMENT_ID, SOURCE_ID, OptFloat, OptStr

SOURCE_REFS = r"^SRC-\d{4}(;SRC-\d{4})*$"


class TermRow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    instrument_id: str = Field(pattern=INSTRUMENT_ID)
    nombre: str
    deudor: str
    tipo_acreedor: CreditorType
    residencia_tenedor: Residency
    moneda_cuenta: str = Field(pattern=r"^[A-Z]{3}$")
    indexacion: Indexation
    moneda_liquidacion: str = Field(pattern=r"^[A-Z]{3}$")
    estado: Status
    fecha_corte: date
    saldo_corte: float = Field(ge=0)
    fecha_emision: date
    primer_periodo: date
    vencimiento: date
    frecuencia_meses: int = Field(gt=0)
    fin_de_mes: bool
    periodo_final_corto: bool = False
    base: DayCount
    tipo_tasa: Literal["fija", "fija_por_periodo", "flotante", "cero"]
    indice: OptStr = None
    margen: OptFloat = None
    multiplicador: OptFloat = None
    tope_indice: OptStr = None
    tope_margen: OptFloat = None
    capitaliza: bool
    source_id: str = Field(pattern=SOURCE_REFS)
    referencia: str
    notas: OptStr = None


class RateRow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    instrument_id: str = Field(pattern=INSTRUMENT_ID)
    desde: date
    tasa: float
    source_id: str = Field(pattern=SOURCE_ID)
    referencia: str


class AmortizationRow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    instrument_id: str = Field(pattern=INSTRUMENT_ID)
    fecha: date
    fraccion: float = Field(gt=0, le=1)
    source_id: str = Field(pattern=SOURCE_ID)
    referencia: str


class DateRow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    instrument_id: str = Field(pattern=INSTRUMENT_ID)
    fecha: date
    source_id: str = Field(pattern=SOURCE_ID)
    referencia: str


def _read(path: Path, model: type[BaseModel]) -> list:  # type: ignore[type-arg]
    with path.open(newline="", encoding="utf-8") as fh:
        return [model.model_validate(r) for r in csv.DictReader(fh)]


def _rate(t: TermRow, steps: list[RateRow]) -> Rate:
    if t.tipo_tasa == "cero":
        return ZeroRate()
    if t.tipo_tasa == "flotante":
        if not t.indice:
            raise ValueError(f"{t.instrument_id}: floating rate without index")
        if t.tope_indice is None and t.tope_margen is not None:
            raise ValueError(f"{t.instrument_id}: tope_margen without tope_indice")
        return FloatingRate(
            t.indice,
            t.margen or 0.0,
            1.0 if t.multiplicador is None else t.multiplicador,
            cap_index=t.tope_indice,
            cap_spread=t.tope_margen or 0.0,
        )
    if not steps:
        raise ValueError(f"{t.instrument_id}: fixed rate without rows in tasas.csv")
    return FixedRate(
        tuple(sorted((s.desde, s.tasa) for s in steps)),
        per_period=t.tipo_tasa == "fija_por_periodo",
    )


def _period_dates(t: TermRow, explicit: list[date] | None) -> tuple[date, ...]:
    if explicit:
        dates = sorted(set(explicit))
        if len(dates) != len(explicit):
            raise ValueError(f"{t.instrument_id}: repeated date in fechas.csv")
        if dates[-1] != t.vencimiento:
            raise ValueError(f"{t.instrument_id}: fechas.csv does not end at maturity")
        return tuple(dates)
    return tuple(
        regular_dates(
            t.primer_periodo, t.vencimiento, t.frecuencia_meses, t.fin_de_mes,
            final_stub=t.periodo_final_corto,
        )
    )  # fmt: skip


def load_term_sheets(folder: Path) -> list[TermSheet]:
    terms: list[TermRow] = _read(folder / "terminos.csv", TermRow)
    rates: dict[str, list[RateRow]] = defaultdict(list)
    for r in _read(folder / "tasas.csv", RateRow):
        rates[r.instrument_id].append(r)
    amort: dict[str, list[AmortizationRow]] = defaultdict(list)
    for a in _read(folder / "amortizaciones.csv", AmortizationRow):
        amort[a.instrument_id].append(a)
    explicit: dict[str, list[date]] = defaultdict(list)
    if (folder / "fechas.csv").exists():
        for r in _read(folder / "fechas.csv", DateRow):
            explicit[r.instrument_id].append(r.fecha)

    sheets = []
    seen: set[str] = set()
    for t in terms:
        if t.instrument_id in seen:
            raise ValueError(f"duplicate instrument in terminos.csv: {t.instrument_id}")
        seen.add(t.instrument_id)
        obligation = Obligation(
            instrument_id=t.instrument_id,
            name=t.nombre,
            debtor=t.deudor,
            creditor_type=t.tipo_acreedor,
            holder_residency=t.residencia_tenedor,
            currency_of_account=t.moneda_cuenta,
            indexation=t.indexacion,
            currency_of_settlement=t.moneda_liquidacion,
            status=t.estado,
        )
        amortization = amort.get(t.instrument_id) or [
            AmortizationRow(
                instrument_id=t.instrument_id, fecha=t.vencimiento, fraccion=1.0,
                source_id=t.source_id.split(";")[0], referencia="al vencimiento (bullet)",
            )
        ]  # fmt: skip
        sheets.append(
            TermSheet(
                obligation=obligation,
                as_of=t.fecha_corte,
                outstanding=t.saldo_corte,
                period_dates=_period_dates(t, explicit.get(t.instrument_id)),
                accrual_start=t.fecha_emision,
                day_count=t.base,
                rate=_rate(t, rates.get(t.instrument_id, [])),
                amortization=tuple(sorted((a.fecha, a.fraccion) for a in amortization)),
                capitalizes=t.capitaliza,
                frequency_months=t.frecuencia_meses,
                source_id=t.source_id,
                reference=t.referencia,
                notes=(t.notas,) if t.notas else (),
            )
        )
    unknown = (set(rates) | set(amort)) - seen
    if unknown:
        raise ValueError(f"rates or amortizations for instruments not in terminos.csv: {unknown}")
    return sheets
