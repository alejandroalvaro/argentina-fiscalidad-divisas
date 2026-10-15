"""Protocol time buckets: monthly for months 1 to 36 after the cut-off, annual for years 4 to 20.

Month 1 is the calendar month after the cut-off month. Year k (4 to 20) covers months
12(k-1)+1 to 12k. Flows after year 20 go to "mas_de_20".

Sums never turn an unknown amount into zero: each group reports the sum of the known amounts
and how many flows had no amount.
"""

from __future__ import annotations

import math
from collections.abc import Iterable
from dataclasses import asdict
from datetime import date

from argfx.contracts.scenario import Valuation


def month_index(d: date, cutoff: date) -> int:
    return (d.year - cutoff.year) * 12 + (d.month - cutoff.month)


def bucket(d: date, cutoff: date) -> tuple[str, str] | None:
    """(horizon, label) or None for flows on or before the cut-off month."""
    m = month_index(d, cutoff)
    if m <= 0:
        return None
    if m <= 36:
        return "mensual", f"M{m:02d}"
    k = math.ceil(m / 12)
    if k <= 20:
        return "anual", f"A{k:02d}"
    return "anual", "mas_de_20"


DIMENSIONS = (
    "source",
    "status",
    "flow_type",
    "is_payment",
    "depends_on_scenario",
    "currency_of_account",
    "indexation",
    "currency_of_settlement",
    "creditor_type",
    "holder_residency",
)


def aggregate(
    valuations: Iterable[Valuation], cutoff: date, by: tuple[str, ...] = DIMENSIONS
) -> list[dict[str, object]]:
    if "currency_of_settlement" not in by:
        raise ValueError("settlement amounts in different currencies cannot be added up")
    groups: dict[tuple[object, ...], dict[str, object]] = {}
    for v in valuations:
        b = bucket(v.flow.date, cutoff)
        if b is None:
            continue
        flow = asdict(v.flow)
        key = (*b, *(flow[k] for k in by))
        g = groups.setdefault(
            key,
            {
                "horizonte": b[0],
                "periodo": b[1],
                **{k: flow[k] for k in by},
                "escenario": v.scenario_id,
                "monto_liquidacion": 0.0,
                "monto_usd": 0.0,
                "n_flujos": 0,
                "n_sin_monto_liquidacion": 0,
                "n_sin_monto_usd": 0,
            },
        )
        g["n_flujos"] += 1  # type: ignore[operator]
        for col, value in (
            ("monto_liquidacion", v.amount_settlement),
            ("monto_usd", v.amount_usd),
        ):
            if value is None:
                g[f"n_sin_{col}"] += 1  # type: ignore[operator]
            else:
                g[col] += value  # type: ignore[operator]
    return sorted(groups.values(), key=lambda g: (g["horizonte"] != "mensual", str(g["periodo"])))
