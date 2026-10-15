"""Generate contractual cash flows from a term sheet, starting from the balance at a cut-off date.

Specialized pieces:
- fixed coupons with step-ups (`FixedRate`), annual or per period (monthly effective, TEM);
- floating coupons (`FloatingRate`): index x multiplier + spread, averaged over the period,
  optionally capped at another index plus a spread;
- capitalization: interest added to principal at each period end, paid with the principal;
- a full period of a regular grid under 30/360 accrues its nominal months, whatever February
  does;
- short periods under a per-period rate: the rate scales with the 30/360 fraction of a full
  period, compounding when interest capitalizes ((1+r)^f - 1, the LECAP and BONCAP formula);
- amortization by fractions of the original face, applied pro rata to the balance outstanding
  at each date, so that buybacks and partial exchanges are respected;
- operations after the cut-off (issues, reopenings, buybacks, swaps), as changes in face value
  that take effect from the start of the period in which they settle;
- options: see `argfx.contracts.options`.

The engine reads only the term sheet and, for floating rates, the scenario. A rate it cannot
obtain leaves the interest as None and every later amount that depends on it as None.
"""

from __future__ import annotations

import calendar
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
    cap_index: str | None = None
    """The rate never exceeds cap_index + cap_spread (BCRA notes: LIBOR or SOFR minus a point)."""
    cap_spread: float = 0.0


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
    frequency_months: int | None = None
    """Nominal period length; a per-period rate needs it to scale short periods."""
    listed_dates: bool = False
    """Period ends listed one by one in the norm (business-day adjusted), not a regular grid."""
    face_changes: tuple[tuple[date, float], ...] = ()
    """(settlement date, change in original face) after `as_of`: issues and reopenings add,
    buybacks and swaps out subtract. Proceeds and prices are financing, not contract flows."""
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
        maturity = self.period_dates[-1]
        late = [d for d, _ in self.face_changes if not (self.as_of < d < maturity)]
        if late:
            raise ValueError(
                f"{self.obligation.instrument_id}: face changes outside (cut-off, maturity) {late}"
            )


def _full_period(start: date, end: date, months: int) -> bool:
    """True when [start, end) spans exactly `months` calendar months on the grid's day."""
    span = (end.year - start.year) * 12 + end.month - start.month
    month_end = end.day == calendar.monthrange(end.year, end.month)[1]
    return span == months and (end.day >= start.day or month_end)


def _accrual(ts: TermSheet, start: date, end: date, scenario: Scenario | None) -> float | None:
    """Interest per unit of principal over [start, end)."""
    rate = ts.rate
    if isinstance(rate, ZeroRate):
        return 0.0
    if isinstance(rate, FixedRate):
        if rate.per_period:
            r = rate.rate_on(start)
            if ts.frequency_months is None:
                return r
            if _full_period(start, end, ts.frequency_months):
                return r
            basis = ts.day_count if ts.day_count in ("30/360", "30E/360") else "30/360"
            f = year_fraction(start, end, basis) * 12 / ts.frequency_months
            return (1 + r) ** f - 1 if ts.capitalizes else r * f
        cuts = sorted({start, end, *(d for d, _ in rate.steps if start < d < end)})
        if (
            ts.day_count == "30/360"
            and ts.frequency_months is not None
            and not ts.listed_dates
            and len(cuts) == 2
            and _full_period(start, end, ts.frequency_months)
        ):
            # A full regular period counts its nominal months, also when it starts or ends on
            # the last day of February (SIGADE: 31-01 to 28-02 and 29-02 to 31-03 are 30 days).
            return rate.rate_on(start) * ts.frequency_months / 12
        return sum(rate.rate_on(a) * year_fraction(a, b, ts.day_count) for a, b in pairwise(cuts))
    if scenario is None:
        return None
    index = scenario.average(rate.index, start, end)
    if index is None:
        return None
    annual = index * rate.multiplier + rate.spread
    if rate.cap_index is not None:
        cap = scenario.average(rate.cap_index, start, end)
        if cap is None:
            return None
        annual = min(annual, cap + rate.cap_spread)
    return annual * year_fraction(start, end, ts.day_count)


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
    # Balance per unit of original face at the start of the current period: the interest
    # capitalized since issue, or the share of face not yet amortized.
    factor: float | None = 1.0
    if ts.capitalizes:
        for a, b in pairwise((ts.accrual_start, *past)):
            acc = _accrual(ts, a, b, scenario)
            factor = None if factor is None or acc is None else factor * (1 + acc)

    for d in (x for x in ts.period_dates if x > ts.as_of):
        change = sum(v for c, v in ts.face_changes if prev <= c < d)
        if change:
            unit = factor if ts.capitalizes else remaining
            principal = None if principal is None or unit is None else principal + change * unit
        accrual = _accrual(ts, prev, d, scenario)
        if ts.capitalizes:
            factor = None if factor is None or accrual is None else factor * (1 + accrual)
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
