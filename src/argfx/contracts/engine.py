"""Generate contractual cash flows from a term sheet, starting from the balance at a cut-off date.

Specialized pieces:
- fixed coupons with step-ups (`FixedRate`), annual or per period (monthly effective, TEM);
- floating coupons (`FloatingRate`): index x multiplier + spread, averaged over the period;
- capitalization: interest added to principal at each period end, paid with the principal;
- amortization by fractions of the original face, applied pro rata to the balance outstanding
  at each date, so that buybacks and partial exchanges are respected;
- options: see `argfx.contracts.options`.

The engine reads only the term sheet and, for floating rates, the scenario. A rate it cannot
obtain leaves the interest as None and every later amount that depends on it as None.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from itertools import pairwise

from argfx.contracts.daycount import DayCount, year_fraction
from argfx.contracts.model import CashFlow, Obligation
from argfx.contracts.scenario import Scenario


@dataclass(frozen=True)
class FixedRate:
    """Rate steps as (effective from, rate). `per_period` means the rate applies once per period
    (a monthly effective rate, for instance) instead of being annual and day-counted."""

    steps: tuple[tuple[date, float], ...]
    per_period: bool = False

    def rate_on(self, d: date) -> float:
        current = None
        for start, rate in self.steps:
            if start <= d:
                current = rate
        if current is None:
            raise ValueError(f"no rate in force on {d}")
        return current


@dataclass(frozen=True)
class FloatingRate:
    index: str
    spread: float = 0.0
    multiplier: float = 1.0


@dataclass(frozen=True)
class ZeroRate:
    pass


Rate = FixedRate | FloatingRate | ZeroRate


@dataclass(frozen=True)
class TermSheet:
    obligation: Obligation
    as_of: date
    outstanding: float
    period_dates: tuple[date, ...]
    """Every contractual period end (coupon or capitalization date), ascending, to maturity."""
    accrual_start: date
    """Start of the first accrual period (issue date)."""
    day_count: DayCount
    rate: Rate
    amortization: tuple[tuple[date, float], ...]
    """(date, fraction of the original face). Fractions must add up to 1."""
    capitalizes: bool = False
    source_id: str | None = None
    reference: str | None = None
    notes: tuple[str, ...] = field(default_factory=tuple)

    def __post_init__(self) -> None:
        total = sum(f for _, f in self.amortization)
        if abs(total - 1) > 1e-9:
            raise ValueError(f"{self.obligation.instrument_id}: amortization adds to {total}")
        dates = set(self.period_dates)
        missing = [d for d, _ in self.amortization if d not in dates]
        if missing:
            raise ValueError(
                f"{self.obligation.instrument_id}: amortization off schedule {missing}"
            )


def _accrual(ts: TermSheet, start: date, end: date, scenario: Scenario | None) -> float | None:
    """Interest per unit of principal over [start, end)."""
    rate = ts.rate
    if isinstance(rate, ZeroRate):
        return 0.0
    if isinstance(rate, FixedRate):
        if rate.per_period:
            return rate.rate_on(start)
        cuts = sorted({start, end, *(d for d, _ in rate.steps if start < d < end)})
        return sum(rate.rate_on(a) * year_fraction(a, b, ts.day_count) for a, b in pairwise(cuts))
    if scenario is None:
        return None
    index = scenario.average(rate.index, start, end)
    if index is None:
        return None
    return (index * rate.multiplier + rate.spread) * year_fraction(start, end, ts.day_count)


def generate(ts: TermSheet, scenario: Scenario | None = None) -> list[CashFlow]:
    """Contractual flows after `as_of`, from the outstanding balance at `as_of`."""
    ob = ts.obligation
    floating = isinstance(ts.rate, FloatingRate)
    sid = scenario.scenario_id if (floating and scenario) else None

    def flow(d: date, kind: str, amount: float | None, payment: bool, note: str | None) -> CashFlow:
        return CashFlow(
            instrument_id=ob.instrument_id,
            date=d,
            flow_type=kind,  # type: ignore[arg-type]
            amount=amount,
            unit=ob.unit,
            currency_of_account=ob.currency_of_account,
            indexation=ob.indexation,
            currency_of_settlement=ob.currency_of_settlement,
            status=ob.status,
            is_payment=payment,
            # Amortization of a floating-rate bond is contractual unless interest capitalizes.
            depends_on_scenario=floating and (kind != "amortizacion" or ts.capitalizes),
            source="motor",
            debtor=ob.debtor,
            creditor_type=ob.creditor_type,
            holder_residency=ob.holder_residency,
            scenario_id=sid,
            note=note,
        )

    past = [d for d in ts.period_dates if d <= ts.as_of]
    prev = past[-1] if past else ts.accrual_start
    amort = dict(ts.amortization)
    remaining = sum(f for d, f in ts.amortization if d > ts.as_of)
    principal: float | None = ts.outstanding
    out: list[CashFlow] = []

    for d in (x for x in ts.period_dates if x > ts.as_of):
        accrual = _accrual(ts, prev, d, scenario)
        interest = None if (principal is None or accrual is None) else principal * accrual
        note = None if interest is not None else "tasa sin trayectoria en el escenario"
        if ts.capitalizes:
            out.append(flow(d, "interes_capitalizado", interest, False, note))
            principal = None if interest is None or principal is None else principal + interest
        elif interest != 0.0:
            out.append(flow(d, "interes", interest, True, note))
        if d in amort:
            share = amort[d] / remaining
            paid = None if principal is None else principal * share
            out.append(flow(d, "amortizacion", paid, True, None))
            if principal is not None and paid is not None:
                principal -= paid
            remaining -= amort[d]
        prev = d
    return out
