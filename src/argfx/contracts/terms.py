"""Read term sheets from `contratos/`: three CSV tables, each row citing its source.

- `terminos.csv`: one row per instrument (dimensions, balance at the cut-off, schedule, rate type).
- `tasas.csv`: fixed-rate steps (instrument_id, desde, tasa).
- `amortizaciones.csv`: amortization dates and fractions of the original face.
- `fechas.csv` (optional): the full list of period ends, for instruments whose norm enumerates
  them instead of following a grid. It replaces primer_periodo/frecuencia for that instrument.
- `duales.csv` (optional): the second leg of each dual, one row per instrument. The first leg is
  the row in `terminos.csv`; the dual pays the larger of the two in the settlement currency.
- `operaciones.csv` (optional): issues, reopenings, buybacks and swaps after the cut-off, in
  original face value (D-008). An instrument issued after the cut-off has saldo_corte 0 and an
  `emision` row on its issue date.

A blank cell is unknown. The engine refuses a term sheet with missing required terms instead of
guessing them.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import replace
from datetime import date
from pathlib import Path
from typing import Annotated, Literal

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field

from argfx.contracts.daycount import DayCount
from argfx.contracts.engine import FixedRate, FloatingRate, Rate, TermSheet, ZeroRate
from argfx.contracts.habiles import BusinessCalendar
from argfx.contracts.model import CreditorType, Indexation, Obligation, Residency, Status
from argfx.contracts.schedule import regular_dates
from argfx.schemas import INSTRUMENT_ID, SOURCE_ID, Opt, OptFloat, OptStr

OptInt = Annotated[int | None, Opt]
# A blank cell in an optional flag column (one an older table lacks) means false.
Flag = Annotated[bool, BeforeValidator(lambda v: False if v in ("", None) else v)]

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
    tem_dias: OptInt = Field(default=None, gt=0)
    """Floating rates: days of the compounding that turns the annual rate into a TEM (TAMAR: 32)."""
    promedio_plazo: Flag = False
    """Floating rates: the index is averaged over the whole term, not period by period."""
    saldo_es_valor_nominal: Flag = False
    """saldo_corte is original face value (VNO) that the engine capitalizes from issue, as the
    legal formula does, instead of SIGADE's balance already capitalized to the last anniversary."""
    indice_inicial: OptFloat = Field(default=None, gt=0)
    """CER or UVA of the issue date, the base of SIGADE's index units. Operations are published
    in pesos of face value; dividing by it gives the units in which saldo_corte is kept."""
    rezago_habiles: OptInt = Field(default=None, ge=0)
    """Business-day lag of the norm: CER or UVA read that many business days before issue and
    before each payment; a floating index averaged over a window moved back as much."""
    indice_base: OptFloat = Field(default=None, gt=0)
    """CER or UVA of `rezago_habiles` business days before issue, the base of the norm."""
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


OPERATION_SIGN = {
    "emision": 1,
    "reapertura": 1,
    "canje_entrada": 1,
    "rescate": -1,
    "canje_salida": -1,
}


class OperationRow(BaseModel):
    model_config = ConfigDict(extra="forbid")

    instrument_id: str = Field(pattern=INSTRUMENT_ID)
    fecha: date
    tipo: Literal["emision", "reapertura", "rescate", "canje_entrada", "canje_salida"]
    valor_nominal: float = Field(gt=0)
    source_id: str = Field(pattern=SOURCE_ID)
    referencia: str


def _read(path: Path, model: type[BaseModel]) -> list:  # type: ignore[type-arg]
    with path.open(newline="", encoding="utf-8") as fh:
        return [model.model_validate(r) for r in csv.DictReader(fh)]


class DualRow(BaseModel):
    """Second leg of a dual. Its balance is the first leg's times `factor_saldo` (CER units times
    the issue CER gives pesos of face, for instance); `saldo_es_valor_nominal` marks a balance
    that the engine must still capitalize from issue."""

    model_config = ConfigDict(extra="forbid")

    instrument_id: str = Field(pattern=INSTRUMENT_ID)
    moneda_cuenta: str = Field(pattern=r"^[A-Z]{3}$")
    indexacion: Indexation
    tipo_tasa: Literal["fija", "fija_por_periodo", "flotante", "cero"]
    tasa: OptFloat = None
    indice: OptStr = None
    margen: OptFloat = None
    multiplicador: OptFloat = None
    tope_indice: OptStr = None
    tope_margen: OptFloat = None
    tem_dias: OptInt = Field(default=None, gt=0)
    promedio_plazo: Flag = False
    rezago_habiles: OptInt = Field(default=None, ge=0)
    """Business-day lag: of the averaging window for a floating leg, of the index read at each
    payment for a CER or UVA leg."""
    capitaliza: bool
    base: DayCount
    primer_periodo: date
    frecuencia_meses: int = Field(gt=0)
    fin_de_mes: bool
    periodo_final_corto: bool = False
    factor_saldo: float = Field(gt=0)
    saldo_es_valor_nominal: bool
    source_id: str = Field(pattern=SOURCE_REFS)
    referencia: str
    notas: OptStr = None


def _rate(t: TermRow | DualRow, steps: list[RateRow]) -> Rate:
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
            tem_days=t.tem_dias,
            whole_term=t.promedio_plazo,
            lag_days=t.rezago_habiles or 0,
        )
    if not steps:
        raise ValueError(f"{t.instrument_id}: fixed rate without rows in tasas.csv or a tasa")
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


TERM_FILES = (
    "terminos.csv", "tasas.csv", "amortizaciones.csv", "fechas.csv", "operaciones.csv",
    "duales.csv",
)  # fmt: skip


def merge_term_folders(base: Path, overlay: Path, out: Path) -> None:
    """Write into `out` the term tables of `base` with those of `overlay` on top.

    An instrument in the overlay's terminos.csv replaces every row of that instrument in the
    base; rows of other instruments in the overlay (operations on instruments of the base, for
    instance) are added.
    """

    def rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
        if not path.exists():
            return [], []
        with path.open(newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            return list(reader.fieldnames or []), list(reader)

    _, new_terms = rows(overlay / "terminos.csv")
    replaced = {r["instrument_id"] for r in new_terms}
    out.mkdir(parents=True, exist_ok=True)
    for name in TERM_FILES:
        head_b, base_rows = rows(base / name)
        head_o, over_rows = rows(overlay / name)
        if not head_b and not head_o:
            continue
        header = head_b + [c for c in head_o if c not in head_b]
        # Each replaced instrument takes the place of its first row in the base; the rest of
        # the overlay goes at the end, so a merge changes only the rows it has to.
        incoming: dict[str, list[dict[str, str]]] = defaultdict(list)
        for r in over_rows:
            incoming[r["instrument_id"]].append(r)
        merged: list[dict[str, str]] = []
        for r in base_rows:
            iid = r["instrument_id"]
            if iid not in replaced:
                merged.append(r)
            elif iid in incoming:
                merged.extend(incoming.pop(iid))
        merged.extend(r for rows_ in incoming.values() for r in rows_)
        with (out / name).open("w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=header, restval="", lineterminator="\n")
            w.writeheader()
            w.writerows(merged)


def load_term_sheets(folder: Path, calendar: BusinessCalendar | None = None) -> list[TermSheet]:
    """Term sheets of `folder`. Business-day lags use `calendar`, by default the rules of Ley
    27.399 alone (`build_calendar` passes the one observed in BCRA data)."""
    calendar = calendar or BusinessCalendar()
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
    ops: dict[str, list[OperationRow]] = defaultdict(list)
    if (folder / "operaciones.csv").exists():
        for o in _read(folder / "operaciones.csv", OperationRow):
            ops[o.instrument_id].append(o)

    sheets = []
    seen: set[str] = set()
    for t in terms:
        if t.instrument_id in seen:
            raise ValueError(f"duplicate instrument in terminos.csv: {t.instrument_id}")
        seen.add(t.instrument_id)
        own_ops = ops.get(t.instrument_id, [])
        indexed = t.indexacion in ("CER", "UVA")
        face_unit = 1.0
        if own_ops and indexed:
            if t.indice_inicial is None:
                raise ValueError(
                    f"{t.instrument_id}: operations on a {t.indexacion}-indexed instrument need "
                    "indice_inicial to turn pesos of face value into index units"
                )
            face_unit = t.indice_inicial
        index_lag, rebase = 0, 1.0
        if indexed and t.rezago_habiles:
            if t.indice_inicial is None or t.indice_base is None:
                raise ValueError(
                    f"{t.instrument_id}: a {t.indexacion} lag needs indice_inicial and "
                    "indice_base to move SIGADE's units onto the base of the norm"
                )
            index_lag, rebase, face_unit = (
                t.rezago_habiles,
                t.indice_inicial / t.indice_base,
                (t.indice_base),
            )
        elif t.indice_base is not None:
            raise ValueError(f"{t.instrument_id}: indice_base without an index lag")
        if t.indexacion == "dolar_linked" and t.rezago_habiles:
            index_lag = t.rezago_habiles  # A 3500 of that many business days before payment
        if t.fecha_emision > t.fecha_corte:
            issued = [o for o in own_ops if o.tipo == "emision" and o.fecha == t.fecha_emision]
            if t.saldo_corte != 0 or not issued:
                raise ValueError(
                    f"{t.instrument_id}: issued after the cut-off, needs saldo_corte 0 and an "
                    "emision row on fecha_emision in operaciones.csv"
                )
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
                outstanding=t.saldo_corte * rebase,
                outstanding_is_face=t.saldo_es_valor_nominal,
                index_lag_days=index_lag,
                index_rebase=rebase,
                calendar=calendar,
                period_dates=_period_dates(t, explicit.get(t.instrument_id)),
                listed_dates=bool(explicit.get(t.instrument_id)),
                accrual_start=t.fecha_emision,
                day_count=t.base,
                rate=_rate(t, rates.get(t.instrument_id, [])),
                amortization=tuple(sorted((a.fecha, a.fraccion) for a in amortization)),
                capitalizes=t.capitaliza,
                frequency_months=t.frecuencia_meses,
                face_changes=tuple(
                    sorted(
                        (o.fecha, OPERATION_SIGN[o.tipo] * o.valor_nominal / face_unit)
                        for o in own_ops
                    )
                ),
                source_id=t.source_id,
                reference=t.referencia,
                notes=(t.notas,) if t.notas else (),
            )
        )
    unknown = (set(rates) | set(amort) | set(explicit) | set(ops)) - seen
    if unknown:
        raise ValueError(f"rows for instruments not in terminos.csv: {unknown}")
    return sheets


def load_duals(folder: Path, sheets: list[TermSheet]) -> dict[str, TermSheet]:
    """Second legs from `duales.csv`, keyed by instrument, built on the first leg's term sheet."""
    path = folder / "duales.csv"
    if not path.exists():
        return {}
    by_id = {ts.obligation.instrument_id: ts for ts in sheets}
    legs: dict[str, TermSheet] = {}
    for d in _read(path, DualRow):
        first = by_id.get(d.instrument_id)
        if first is None:
            raise ValueError(f"{d.instrument_id}: dual leg without a row in terminos.csv")
        if d.instrument_id in legs:
            raise ValueError(f"{d.instrument_id}: more than one row in duales.csv")
        if d.tipo_tasa in ("fija", "fija_por_periodo") and d.tasa is None:
            raise ValueError(f"{d.instrument_id}: fixed second leg without tasa")
        steps = (
            [RateRow(instrument_id=d.instrument_id, desde=first.accrual_start, tasa=d.tasa,
                     source_id=d.source_id.split(";")[0], referencia=d.referencia)]
            if d.tasa is not None else []
        )  # fmt: skip
        maturity = first.period_dates[-1]
        dates = tuple(
            regular_dates(d.primer_periodo, maturity, d.frecuencia_meses, d.fin_de_mes,
                          final_stub=d.periodo_final_corto)
        )  # fmt: skip
        legs[d.instrument_id] = replace(
            first,
            obligation=replace(
                first.obligation, currency_of_account=d.moneda_cuenta, indexation=d.indexacion
            ),
            outstanding=first.outstanding / first.index_rebase * d.factor_saldo,
            outstanding_is_face=d.saldo_es_valor_nominal,
            period_dates=dates,
            day_count=d.base,
            rate=_rate(d, steps),
            amortization=((maturity, 1.0),) if len(first.amortization) == 1 else first.amortization,
            capitalizes=d.capitaliza,
            frequency_months=d.frecuencia_meses,
            listed_dates=False,
            face_changes=tuple(
                (c, v / first.index_rebase * d.factor_saldo) for c, v in first.face_changes
            ),
            # A CER or UVA second leg reads its index with the lag of its own row; its balance
            # is already in the units of the norm (factor_saldo uses the lagged base).
            index_lag_days=(d.rezago_habiles or 0) if d.indexacion in ("CER", "UVA") else 0,
            index_rebase=1.0,
            source_id=d.source_id,
            reference=d.referencia,
            notes=(d.notas,) if d.notas else (),
        )
    return legs
