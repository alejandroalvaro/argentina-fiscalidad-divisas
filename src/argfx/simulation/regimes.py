"""Accounting layer of the phase 4 simulation: one month at a time, every regime on the same path.

Equal tax burden: the duty is the same amount of dollars in every regime (the rate times the
FOB value, an input); what changes is the currency in which it is paid, where the rest of the
exporter's dollars go and, in regime (d), how the Treasury receives them. See
docs/FASE4_DISENO.md and decisions D-007, D-012 and D-013.

Order inside a month:
1. exports: the rest of the world pays the exporters in dollars;
2. duty in dollars, regimes (c) and (d): the exporter hands the dollars to the Treasury account
   at the BCRA, where they become reserves (D-001: counted once);
3. liquidation: of what is left, the exporter sells a fraction (all of it unless it may retain
   abroad); the BCRA buys a share and issues pesos, the rest of the private sector buys the rest;
4. duty in pesos, regimes (a) and (b): paid out of the pesos obtained, into the Treasury peso
   account (base money shrinks);
5. sterilization of part of the pesos the BCRA issued;
6. the fund rule of regime (d);
7. debt service: new FX debt, if any, enters the Treasury's FX deposits, and the Treasury pays
   out of them; what is missing it buys from the BCRA with its pesos and, if those fall short,
   with pesos borrowed from the private sector.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from argfx.simulation.ledger import Ledger


@dataclass(frozen=True)
class Month:
    month: str  # YYYY-MM
    exports_usd: float  # FOB exports subject to the duty, millions of USD
    duty_usd: float  # duty assessed, millions of USD (same in every regime)
    ars_per_usd: float
    payments_usd: float  # Treasury FX debt service to holders outside the public sector
    new_debt_usd: float = 0.0  # FX debt disbursed to the Treasury in the month
    bcra_buys: float | None = None  # overrides Behavior.bcra_buys for the month


@dataclass(frozen=True)
class FundRule:
    """Regime (d), D-012: a fixed monthly transfer to the Treasury, the rest to the fund."""

    reference_monthly_usd: float  # one twelfth of the reference revenue
    cap_months: int = 12  # months of debt service above which the fund prepays debt


@dataclass(frozen=True)
class Regime:
    name: str
    duty_in_usd: bool
    retained_abroad: float = 0.0  # share of the rest the exporter keeps abroad (regime (b))
    fund: FundRule | None = None


@dataclass(frozen=True)
class Behavior:
    bcra_buys: float = 1.0  # share of the liquidated dollars the BCRA buys
    sterilized: float = 0.0  # share of the pesos issued for those purchases it absorbs


@dataclass(frozen=True)
class Opening:
    reserves_usd: float = 0.0
    treasury_usd: float = 0.0
    treasury_ars: float = 0.0
    debt_usd: float = 0.0


REGIMES = {
    "a": Regime("a", duty_in_usd=False),
    "b": Regime("b", duty_in_usd=False, retained_abroad=0.2),
    "c": Regime("c", duty_in_usd=True),
}


@dataclass
class Result:
    regime: str
    ledger: Ledger
    rows: list[dict[str, object]] = field(default_factory=list)


def simulate(path: list[Month], regime: Regime, behavior: Behavior, opening: Opening) -> Result:
    led = Ledger()
    t0 = path[0].month if path else ""
    led.transfer(t0, "apertura", "divisas", "ROW", "BCRA", opening.reserves_usd)
    led.transfer(t0, "apertura", "dep_tes_usd", "BCRA", "TES", opening.treasury_usd)
    led.transfer(t0, "apertura", "dep_tes_ars", "BCRA", "TES", opening.treasury_ars)
    led.transfer(t0, "apertura", "deuda_tes_usd", "TES", "ROW", opening.debt_usd)
    res = Result(regime.name, led)
    for i, m in enumerate(path):
        e = m.ars_per_usd
        led.transfer(m.month, "exportaciones", "divisas", "ROW", "EXP", m.exports_usd)

        to_treasury = to_fund = 0.0
        if regime.duty_in_usd:
            led.transfer(m.month, "derecho en dolares", "divisas", "EXP", "BCRA", m.duty_usd)
            account = "fondo_usd" if regime.fund else "dep_tes_usd"
            led.transfer(m.month, "derecho en dolares", account, "BCRA", "TES", m.duty_usd)
            to_fund = m.duty_usd if regime.fund else 0.0
            to_treasury = 0.0 if regime.fund else m.duty_usd
        rest = m.exports_usd - (m.duty_usd if regime.duty_in_usd else 0.0)
        sold = rest * (1 - regime.retained_abroad)
        bcra = sold * (behavior.bcra_buys if m.bcra_buys is None else m.bcra_buys)
        led.post(m.month, "liquidacion al BCRA",
                 ("EXP", "divisas", -bcra), ("BCRA", "divisas", bcra),
                 ("BCRA", "base", -bcra * e), ("EXP", "base", bcra * e))  # fmt: skip
        private = sold - bcra
        led.post(m.month, "liquidacion a privados",
                 ("EXP", "divisas", -private), ("PRIV", "divisas", private),
                 ("PRIV", "base", -private * e), ("EXP", "base", private * e))  # fmt: skip
        duty_ars = 0.0
        if not regime.duty_in_usd:
            duty_ars = m.duty_usd * e
            led.post(m.month, "derecho en pesos",
                     ("EXP", "base", -duty_ars), ("BCRA", "base", duty_ars),
                     ("BCRA", "dep_tes_ars", -duty_ars),
                     ("TES", "dep_tes_ars", duty_ars))  # fmt: skip
        sterilized = bcra * e * behavior.sterilized
        led.post(m.month, "esterilizacion",
                 ("PRIV", "base", -sterilized), ("BCRA", "base", sterilized),
                 ("BCRA", "pasivos_remunerados", -sterilized),
                 ("PRIV", "pasivos_remunerados", sterilized))  # fmt: skip

        prepaid = 0.0
        if regime.fund:
            available = led.get("TES", "fondo_usd")
            transfer = min(regime.fund.reference_monthly_usd, available)
            led.post(m.month, "transferencia del fondo",
                     ("TES", "fondo_usd", -transfer), ("BCRA", "fondo_usd", transfer),
                     ("BCRA", "dep_tes_usd", -transfer),
                     ("TES", "dep_tes_usd", transfer))  # fmt: skip
            to_treasury += transfer
            ahead = sum(x.payments_usd for x in path[i + 1 : i + 1 + regime.fund.cap_months])
            prepaid = max(0.0, led.get("TES", "fondo_usd") - ahead)
            if prepaid:
                _pay(led, m.month, "cancelacion anticipada", "fondo_usd", prepaid)

        if m.new_debt_usd:
            led.post(m.month, "deuda nueva en divisas",
                     ("ROW", "divisas", -m.new_debt_usd), ("BCRA", "divisas", m.new_debt_usd),
                     ("BCRA", "dep_tes_usd", -m.new_debt_usd),
                     ("TES", "dep_tes_usd", m.new_debt_usd),
                     ("TES", "deuda_tes_usd", -m.new_debt_usd),
                     ("ROW", "deuda_tes_usd", m.new_debt_usd))  # fmt: skip
        need = m.payments_usd
        bought = max(0.0, need - led.get("TES", "dep_tes_usd"))
        borrowed = max(0.0, bought * e - led.get("TES", "dep_tes_ars"))
        led.post(m.month, "deuda en pesos para comprar divisas",
                 ("PRIV", "base", -borrowed), ("BCRA", "base", borrowed),
                 ("BCRA", "dep_tes_ars", -borrowed), ("TES", "dep_tes_ars", borrowed),
                 ("TES", "deuda_tes_ars", -borrowed),
                 ("PRIV", "deuda_tes_ars", borrowed))  # fmt: skip
        led.post(m.month, "compra de divisas del Tesoro al BCRA",
                 ("TES", "dep_tes_ars", -bought * e), ("BCRA", "dep_tes_ars", bought * e),
                 ("BCRA", "dep_tes_usd", -bought), ("TES", "dep_tes_usd", bought))  # fmt: skip
        _pay(led, m.month, "servicio de deuda en divisas", "dep_tes_usd", need)

        res.rows.append(
            {
                "regimen": regime.name,
                "mes": m.month,
                "derecho_usd": round(m.duty_usd, 3),
                "derecho_cobrado_en_pesos_ars": round(duty_ars, 3),
                "ingreso_tesoro_divisas_usd": round(to_treasury, 3),
                "aporte_al_fondo_usd": round(to_fund, 3),
                "servicio_usd": round(need, 3),
                "compra_tesoro_al_bcra_usd": round(bought, 3),
                "pesos_usados_en_compras_ars": round(bought * e, 3),
                "deuda_en_pesos_para_comprar_ars": round(borrowed, 3),
                "pesos_emitidos_por_compras_bcra_ars": round(bcra * e, 3),
                "pesos_esterilizados_ars": round(sterilized, 3),
                "cancelacion_anticipada_usd": round(prepaid, 3),
                "depositos_tesoro_usd": round(led.get("TES", "dep_tes_usd"), 3),
                "fondo_usd": round(led.get("TES", "fondo_usd"), 3),
                "reservas_brutas_bcra_usd": round(led.get("BCRA", "divisas"), 3),
                "divisas_retenidas_exportadores_usd": round(led.get("EXP", "divisas"), 3),
                "mes_con_faltante": bought > 0,
            }
        )
    return res


def _pay(led: Ledger, month: str, kind: str, account: str, amount: float) -> None:
    """Pay non-residents out of a Treasury FX account: reserves leave, debt falls."""
    led.post(month, kind,
             ("TES", account, -amount), ("BCRA", account, amount),
             ("BCRA", "divisas", -amount), ("ROW", "divisas", amount),
             ("TES", "deuda_tes_usd", amount), ("ROW", "deuda_tes_usd", -amount))  # fmt: skip


def summary(res: Result) -> dict[str, object]:
    rows = res.rows
    inflow = [float(r["ingreso_tesoro_divisas_usd"]) for r in rows]  # type: ignore[arg-type]
    mean = sum(inflow) / len(inflow) if inflow else 0.0
    sd = (sum((x - mean) ** 2 for x in inflow) / len(inflow)) ** 0.5 if inflow else 0.0

    def total(k: str) -> float:
        return round(sum(float(r[k]) for r in rows), 1)  # type: ignore[arg-type]

    return {
        "regimen": res.regime,
        "meses": len(rows),
        "ingreso_tesoro_divisas_medio_usd": round(mean, 1),
        "ingreso_tesoro_divisas_cv": round(sd / mean, 3) if mean else None,
        "meses_con_faltante": sum(bool(r["mes_con_faltante"]) for r in rows),
        "compras_tesoro_al_bcra_usd": total("compra_tesoro_al_bcra_usd"),
        "pesos_usados_en_compras_ars": total("pesos_usados_en_compras_ars"),
        "deuda_en_pesos_para_comprar_ars": total("deuda_en_pesos_para_comprar_ars"),
        "pesos_emitidos_por_compras_bcra_ars": total("pesos_emitidos_por_compras_bcra_ars"),
        "reservas_brutas_finales_usd": rows[-1]["reservas_brutas_bcra_usd"] if rows else None,
        "columnas_cierran": all(abs(v) < 1e-3 for v in res.ledger.column_sums().values()),
    }
