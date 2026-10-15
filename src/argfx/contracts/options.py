"""Embedded options. Duals pay the larger of two legs, so the chosen leg depends on the scenario.

Argentine duals (BONCAP DUAL fixed or TAMAR, BONCER DUAL CER or TAMAR+3, BONAR/BONTE DUAL
dollar-linked or another leg) compare the legs over the life of the bond. Here each leg is a full
term sheet; both are valued in the currency of settlement, where they meet, and the leg with the
larger total payment is kept. If either leg cannot be valued, every flow of the first leg comes
out with amount None and, when the first leg itself is known, its amount as `lower_bound`: the
dual pays at least that.
"""

from __future__ import annotations

from dataclasses import replace

from argfx.contracts.engine import TermSheet, generate
from argfx.contracts.model import CashFlow
from argfx.contracts.scenario import Scenario, value_flow


def _total_paid(flows: list[CashFlow], scenario: Scenario) -> float | None:
    total = 0.0
    for f in flows:
        if not f.is_payment:
            continue
        v = value_flow(f, scenario).amount_settlement
        if v is None:
            return None
        total += v
    return total


def dual_max(leg_a: TermSheet, leg_b: TermSheet, scenario: Scenario) -> list[CashFlow]:
    if leg_a.obligation.instrument_id != leg_b.obligation.instrument_id:
        raise ValueError("both legs must belong to the same instrument")
    if leg_a.obligation.currency_of_settlement != leg_b.obligation.currency_of_settlement:
        raise ValueError("both legs must settle in the same currency")
    flows_a, flows_b = generate(leg_a, scenario), generate(leg_b, scenario)
    total_a, total_b = _total_paid(flows_a, scenario), _total_paid(flows_b, scenario)
    if total_a is None or total_b is None:
        return [
            replace(f, amount=None, lower_bound=f.amount if total_a is not None else None,
                    depends_on_scenario=True, scenario_id=scenario.scenario_id,
                    note="dual: falta trayectoria para comparar; lower_bound es la rama a")
            for f in flows_a
        ]  # fmt: skip
    chosen, label = (flows_a, "a") if total_a >= total_b else (flows_b, "b")
    return [
        replace(f, depends_on_scenario=True, scenario_id=scenario.scenario_id,
                note=f"dual: rama {label} bajo {scenario.scenario_id}")
        for f in chosen
    ]  # fmt: skip
