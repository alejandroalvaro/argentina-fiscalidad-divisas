"""Load the SIGADE maturity profile as cash flows (source "sigade").

SIGADE projects every operation with rates and exchange rates frozen at the cut-off. It is an
official projection, not a contract term sheet, and stays labeled as such. Amounts are taken in
the loan's own currency ("en Moneda del Prestamo"): CER units for UCP, USD for DLK.
"""

from __future__ import annotations

import csv
import re
from datetime import date
from pathlib import Path

from argfx.contracts.model import CashFlow, CreditorType, Indexation, Status
from argfx.contracts.scenario import SIGADE_CODE_TO_ISO

MATURITIES = "sigade_{cutoff}_vencimientos_de_la_deuda_en_situacion_de_pago_normal.csv"
BALANCES = "sigade_{cutoff}_saldo_de_deuda_en_situacion_de_pago_normal.csv"

CREDITOR_BY_CLASS: dict[str, CreditorType] = {
    **dict.fromkeys(
        ["BID", "BIRF", "CAF", "FONPLATA", "BCIE", "BEI", "FIDA", "OFID", "FMI"], "multilateral"
    ),
    "CLUB DE PARIS": "bilateral",
    "BILATERALES": "bilateral",
    "ANTICIPOS BCRA": "BCRA",
    "BANCA": "privado",
}
# Rate types whose projected interest depends on a path SIGADE froze at the cut-off.
SCENARIO_RATES = {"TASA SOFR", "TASA LIBO", "TASA BADLAR", "DIVERSAS", "TASA FMI", "CAJA DE AHORRO"}


CONTINGENT_CLASSES = frozenset({"AVALES", "LETRAS EN GARANTÍA"})


def unit_dimensions(loan_code: str, payment_code: str) -> tuple[str, str, Indexation, str]:
    """(unit, currency of account, indexation, currency of settlement) for SIGADE codes."""
    settlement = SIGADE_CODE_TO_ISO.get(payment_code, payment_code)
    if loan_code == "UCP":
        return "CER", "ARS", "CER", settlement
    if loan_code == "DLK":
        return "USD", "USD", "dolar_linked", settlement
    iso = SIGADE_CODE_TO_ISO.get(loan_code, loan_code)
    return iso, iso, "ninguna", settlement


def _service_date(r: dict[str, str]) -> date:
    """From the Año/Mes/Día columns. "Fecha de Servicio" has a two-digit year, which Python reads
    as 1969-1999 for 69-99, while SIGADE schedules run to the 2080s."""
    d = date(int(r["Año"]), int(r["Mes"]), int(r["Día"]))
    if d.strftime("%m/%d/%y") != r["Fecha de Servicio"][:8]:
        raise ValueError(f"inconsistent service date: {r['Fecha de Servicio']} vs {d}")
    return d


# A SIGADE operation is identified by name, loan currency and rate type together: one loan can
# have tranches in several currencies, or a fixed and a SOFR tranche in the same currency.
OperationKey = tuple[str, str, str]
_RATE_IN_NOTES = re.compile(r"tipo de tasa SIGADE: ([^;]+)")


def read_instrument_index(instruments_csv: Path) -> dict[OperationKey, tuple[str, str]]:
    """(name, loan currency, rate type) -> (instrument_id, issuer), from lote C's instruments.csv.

    The rate type is not a column there; it is read from the `notes` field.
    """
    with instruments_csv.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    index: dict[OperationKey, tuple[str, str]] = {}
    for r in rows:
        m = _RATE_IN_NOTES.search(r["notes"])
        if not m:
            raise ValueError(f"{r['instrument_id']}: no SIGADE rate type in notes")
        key = (r["operation_name_sigade"], r["currency_code_sigade"], m.group(1).strip())
        if key in index:
            raise ValueError(f"operation not unique in {instruments_csv}: {key}")
        index[key] = (r["instrument_id"], r["issuer"])
    return index


def load_sigade_flows(
    folder: Path, cutoff: str, instruments: dict[OperationKey, tuple[str, str]] | None = None
) -> list[CashFlow]:
    """`instruments` comes from `read_instrument_index`; unmapped operations keep their name."""
    index = instruments or {}
    with (folder / BALANCES.format(cutoff=cutoff)).open(newline="", encoding="utf-8") as fh:
        payment = {
            (r["Nombre de la Operación"], r["Moneda del Prestamo"], r["Tipo de Tasa"]): r[
                "Moneda de Pago"
            ]
            for r in csv.DictReader(fh)
        }
    flows: list[CashFlow] = []
    with (folder / MATURITIES.format(cutoff=cutoff)).open(newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            name, cls = r["Nombre de la Operación"], r["BOLETIN"]
            key = (name, r["Moneda de Origen"], r["Tipo de Tasa"])
            if key not in payment:
                raise ValueError(f"maturity row without a balance row: {key}")
            unit, account, indexation, settlement = unit_dimensions(
                r["Moneda de Origen"], payment[key]
            )
            instrument_id, debtor = index.get(key, (name, "desconocido"))
            # Guarantees: avales, and the letters given in guarantee to the FODER, which expire
            # every 31 December without payment unless a put option is exercised (D-011).
            status: Status = "contingente" if cls in CONTINGENT_CLASSES else "firme"
            floating = r["Tipo de Tasa"] in SCENARIO_RATES
            for kind, column in (
                ("amortizacion", "Principal en Moneda del Prestamo"),
                ("interes", "Interes en Moneda del Prestamo"),
            ):
                amount = float(r[column]) if r[column].strip() else None
                if amount == 0.0:
                    continue
                flows.append(
                    CashFlow(
                        instrument_id=instrument_id,
                        date=_service_date(r),
                        flow_type=kind,  # type: ignore[arg-type]
                        amount=amount,
                        unit=unit,
                        currency_of_account=account,
                        indexation=indexation,
                        currency_of_settlement=settlement,
                        status=status,
                        is_payment=True,
                        depends_on_scenario=floating and kind == "interes",
                        source="sigade",
                        debtor=debtor,
                        creditor_type=creditor_type(cls),
                        holder_residency="desconocida",
                        scenario_id=f"sigade_congelado_{cutoff}" if floating else None,
                        note=f"SIGADE {cls}; {r['Tipo de Tasa']}",
                    )
                )
    return flows


def creditor_type(sigade_class: str) -> CreditorType:
    """Bonds, bills and guaranteed loans have mixed or unknown holders: left as unknown."""
    return CREDITOR_BY_CLASS.get(sigade_class, "desconocido")
