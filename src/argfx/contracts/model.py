"""Core types of the contract engine.

The dimensions of an obligation are separate fields and never collapse into one another:
currency of account, indexation, currency of settlement, debtor, creditor and holder residency.
Contract cash flows (`CashFlow`) are kept apart from scenario valuations (`Valuation`).
An amount that cannot be computed is None, never zero.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Literal

FlowType = Literal["interes", "amortizacion", "interes_capitalizado"]
Status = Literal["firme", "contingente"]
Indexation = Literal["ninguna", "CER", "UVA", "dolar_linked"]
CreditorType = Literal[
    "privado", "multilateral", "bilateral", "BCRA", "sector_publico", "desconocido"
]
Residency = Literal["residente", "no_residente", "mixta", "desconocida"]
Source = Literal["motor", "sigade"]

# Unit in which a flow is expressed: an ISO 4217 code, or index units (CER, UVA) that a
# scenario converts into the currency of account.
INDEX_UNITS = frozenset({"CER", "UVA"})


@dataclass(frozen=True)
class Obligation:
    """Who owes what to whom, in which currency, under which indexation."""

    instrument_id: str
    name: str
    debtor: str
    creditor_type: CreditorType
    holder_residency: Residency
    currency_of_account: str
    indexation: Indexation
    currency_of_settlement: str
    status: Status = "firme"

    @property
    def unit(self) -> str:
        """Unit of the contract amounts: index units for CER/UVA, otherwise the account currency."""
        if self.indexation in ("CER", "UVA"):
            return self.indexation
        return self.currency_of_account


@dataclass(frozen=True)
class CashFlow:
    """One contractual flow, in the obligation's contract unit.

    `amount` is None when the contract makes it depend on a path (a floating rate, for example)
    that the scenario does not provide; `lower_bound` then carries a floor when one is known.
    `is_payment` is False for interest that capitalizes.
    """

    instrument_id: str
    date: date
    flow_type: FlowType
    amount: float | None
    unit: str
    currency_of_account: str
    indexation: Indexation
    currency_of_settlement: str
    status: Status
    is_payment: bool
    depends_on_scenario: bool
    source: Source
    debtor: str
    creditor_type: CreditorType
    holder_residency: Residency
    scenario_id: str | None = None
    note: str | None = None
    lower_bound: float | None = None
    """When `amount` is unknown but a floor is known (a dual whose other leg has no path)."""
