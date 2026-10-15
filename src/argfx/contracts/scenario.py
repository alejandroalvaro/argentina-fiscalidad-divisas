"""Scenarios: named paths for rates, indices and exchange rates, kept apart from contract terms.

A path is a step function: the value at date d is the last point on or before d. Before the
first point there is no value, and anything that needs it comes out as None (never zero).

Names in use:
- rates, annual nominal in decimals: "TAMAR", "BADLAR", "SOFR", ...
- indices, level per index unit: "CER", "UVA"
- exchange rates, units of currency per USD: "FX:ARS", "FX:EUR", ... ("FX:USD" is always 1)
"""

from __future__ import annotations

import bisect
import csv
from dataclasses import dataclass, field
from datetime import date, datetime
from itertools import pairwise
from pathlib import Path

from argfx.contracts.model import INDEX_UNITS, CashFlow

# SIGADE uses its own codes for a few units.
SIGADE_CODE_TO_ISO = {"ARP": "ARS", "SDR": "XDR"}


@dataclass
class Scenario:
    scenario_id: str
    description: str
    paths: dict[str, list[tuple[date, float]]] = field(default_factory=dict)

    def set_path(self, name: str, points: list[tuple[date, float]]) -> None:
        self.paths[name] = sorted(points)

    def value(self, name: str, on: date) -> float | None:
        if name == "FX:USD":
            return 1.0
        points = self.paths.get(name)
        if not points:
            return None
        i = bisect.bisect_right([d for d, _ in points], on) - 1
        return points[i][1] if i >= 0 else None

    def average(self, name: str, start: date, end: date) -> float | None:
        """Time-weighted average of the path over [start, end)."""
        points = self.paths.get(name)
        if not points or end <= start:
            return None
        if self.value(name, start) is None:
            return None
        cuts = sorted({start, end, *(d for d, _ in points if start < d < end)})
        total = 0.0
        for a, b in pairwise(cuts):
            v = self.value(name, a)
            if v is None:
                return None
            total += v * (b - a).days
        return total / (end - start).days

    @classmethod
    def frozen_from_sigade(cls, fx_csv: Path) -> Scenario:
        """All rates and indices constant at the SIGADE cut-off, the basis of its projection.

        SIGADE quotes each code in units per USD. CER comes as an index level; UCP (pesos + CER)
        and DLK (dollar link) are units of account, not separate paths.
        """
        with fx_csv.open(newline="", encoding="utf-8") as fh:
            rows = list(csv.DictReader(fh))
        cutoff = datetime.strptime(rows[0]["Fecha"][:8], "%m/%d/%y").date()
        s = cls(
            scenario_id=f"sigade_congelado_{cutoff.isoformat()}",
            description=f"Tipos de cambio e índices de SIGADE congelados al {cutoff.isoformat()}",
        )
        for r in rows:
            code, rate = r["Moneda"], float(r["Tipo de Cambio"])
            if code in ("UCP", "DLK"):
                continue
            if code == "CER":
                s.set_path("CER", [(cutoff, rate)])
            else:
                s.set_path(f"FX:{SIGADE_CODE_TO_ISO.get(code, code)}", [(cutoff, rate)])
        return s


@dataclass(frozen=True)
class Valuation:
    """A contract flow converted under a scenario. Amounts are None when a path is missing."""

    flow: CashFlow
    scenario_id: str
    amount_account: float | None
    amount_settlement: float | None
    amount_usd: float | None


def _convert(amount: float | None, src: str, dst: str, on: date, s: Scenario) -> float | None:
    if amount is None:
        return None
    if src == dst:
        return amount
    if src in INDEX_UNITS:
        level = s.value(src, on)
        return None if level is None else _convert(amount * level, "ARS", dst, on, s)
    per_usd_src, per_usd_dst = s.value(f"FX:{src}", on), s.value(f"FX:{dst}", on)
    if per_usd_src is None or per_usd_dst is None:
        return None
    return amount / per_usd_src * per_usd_dst


def value_flow(flow: CashFlow, s: Scenario) -> Valuation:
    on = flow.date
    account = _convert(flow.amount, flow.unit, flow.currency_of_account, on, s)
    return Valuation(
        flow=flow,
        scenario_id=s.scenario_id,
        amount_account=account,
        amount_settlement=_convert(
            account, flow.currency_of_account, flow.currency_of_settlement, on, s
        ),
        amount_usd=_convert(account, flow.currency_of_account, "USD", on, s),
    )
