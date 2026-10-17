"""Phase 4 run with data: the mandate seen under a duty paid in dollars, and the years ahead.

Two exercises, kept apart (docs/FASE4_DISENO.md, D-007, D-012, D-015):

1. The mandate, December 2023 to August 2026. What was observed is regime (a). The
   counterfactual (c) changes one thing: the duty collected each month, in dollars at the month's
   A 3500, goes to the Treasury's account at the BCRA instead of being paid in pesos. Everything
   else stays as observed: exports, spending, the debt paid, the BCRA's share of the market. Two
   uses of those dollars are measured separately, because the sources cannot say which one the
   Treasury would have chosen:
   - `compras`: they replace dollars the Treasury bought with pesos;
   - `deuda`: they replace new debt in dollars.
   The Treasury then has fewer pesos (it did not collect the duty in pesos) and either spends
   fewer pesos on dollars or owes less in dollars. The peso gap is carried at BADLAR, the dollar
   debt avoided at an assumed rate; both are assumptions and are reported as such.

2. The years ahead, from the month after the last observed one to 2036. The accounting layer of
   `regimes.simulate` runs (a), (c) and (d) on the same path: duties projected from the last
   twelve months of exports at the rates already decreed, and the firm foreign-currency payments
   of the phase 2 calendar to holders outside the public sector (phase 3 shares).

Units: millions of USD and millions of current pesos, unless a column says otherwise.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from argfx.simulation.regimes import (
    REGIMES,
    Behavior,
    FundRule,
    Month,
    Opening,
    Regime,
    simulate,
    summary,
)

AGRO = {"soja", "maiz", "trigo y cebada", "girasol", "sorgo"}
MULTILATERAL = {"multilateral", "bilateral"}


# ---------------------------------------------------------------- the mandate


@dataclass(frozen=True)
class MandateMonth:
    mes: str
    tipo_de_cambio: float  # A 3500, monthly average
    derecho_usd: float  # duty collected, at the month's A 3500
    exportaciones_mlc_usd: float  # exporters' sales in the FX market (balance cambiario)
    compras_bcra_usd: float  # BCRA purchases from the private sector (base factor / rate)
    compras_tesoro_usd: float  # Treasury purchases with pesos, from the BCRA and in the market
    compras_tesoro_mercado_usd: float  # of which in the market
    deuda_desembolsada_usd: float  # new FX debt disbursed to the Treasury
    tasa_pesos: float  # BADLAR, percent per year, monthly average

    @property
    def bcra_share(self) -> float:
        if self.exportaciones_mlc_usd <= 0:
            return 0.0
        return min(1.0, max(0.0, self.compras_bcra_usd / self.exportaciones_mlc_usd))


def mandate_counterfactual(
    months: list[MandateMonth], uso: str, usd_rate: float = 7.0
) -> tuple[list[dict[str, object]], dict[str, object]]:
    """Regime (c) over the observed months. `uso` is `compras` or `deuda`. Returns the monthly
    rows and a summary; every amount is the difference (c) minus observed."""
    if uso not in ("compras", "deuda"):
        raise ValueError(f"uso desconocido: {uso}")
    rows: list[dict[str, object]] = []
    stock = 0.0  # duty dollars not yet used, in the Treasury's account
    peso_gap = 0.0  # pesos the Treasury lacks against the observed path, carried at BADLAR
    peso_interest = 0.0
    usd_debt_avoided = 0.0
    usd_interest = 0.0
    for m in months:
        e = m.tipo_de_cambio
        # Interest accrues on the stocks carried from earlier months.
        peso_interest += peso_gap * m.tasa_pesos / 100 / 12
        peso_gap += peso_gap * m.tasa_pesos / 100 / 12
        usd_interest += usd_debt_avoided * usd_rate / 100 / 12
        stock += m.derecho_usd
        peso_gap += m.derecho_usd * e  # the duty is no longer collected in pesos
        used = 0.0
        market = 0.0
        if uso == "compras":
            used = min(stock, m.compras_tesoro_usd)
            share = (
                m.compras_tesoro_mercado_usd / m.compras_tesoro_usd if m.compras_tesoro_usd else 0
            )
            market = used * share
            peso_gap -= used * e  # pesos not spent on dollars
        else:
            used = min(stock, max(0.0, m.deuda_desembolsada_usd))
            usd_debt_avoided += used
            market = used  # dollars that no longer come in as debt
        stock -= used
        # The exporter sells the duty less in the market: the BCRA buys its share of it less.
        bcra_less = m.derecho_usd * m.bcra_share
        rows.append(
            {
                "uso": uso,
                "mes": m.mes,
                "tipo_de_cambio": round(e, 2),
                "derecho_usd": round(m.derecho_usd, 1),
                "proporcion_compra_bcra": round(m.bcra_share, 3),
                "compras_bcra_menos_usd": round(bcra_less, 1),
                "dolares_del_derecho_usados_usd": round(used, 1),
                "dolares_del_derecho_sin_usar_usd": round(stock, 1),
                "compras_tesoro_evitadas_usd": round(used if uso == "compras" else 0.0, 1),
                "deuda_en_divisas_evitada_acumulada_usd": round(usd_debt_avoided, 1),
                "brecha_pesos_tesoro_acumulada_ars": round(peso_gap, 0),
                "reservas_consolidadas_dif_usd": round(m.derecho_usd - bcra_less - market, 1),
            }
        )
    last = months[-1]
    total_duty = sum(m.derecho_usd for m in months)
    reserves = sum(float(r["reservas_consolidadas_dif_usd"]) for r in rows)  # type: ignore[arg-type]
    out: dict[str, object] = {
        "uso": uso,
        "desde": months[0].mes,
        "hasta": last.mes,
        "derechos_usd": round(total_duty, 0),
        "derechos_en_pesos_corrientes_ars": round(
            sum(m.derecho_usd * m.tipo_de_cambio for m in months), 0
        ),
        "dolares_usados_usd": round(total_duty - stock, 0),
        "dolares_sin_usar_al_cierre_usd": round(stock, 0),
        "compras_tesoro_observadas_usd": round(sum(m.compras_tesoro_usd for m in months), 0),
        "compras_bcra_menos_usd": round(sum(m.derecho_usd * m.bcra_share for m in months), 0),
        "reservas_consolidadas_dif_usd": round(reserves, 0),
        "brecha_pesos_tesoro_al_cierre_ars": round(peso_gap, 0),
        "intereses_en_pesos_de_la_brecha_ars": round(peso_interest, 0),
        "deuda_en_divisas_evitada_usd": round(usd_debt_avoided, 0),
        "intereses_en_divisas_evitados_usd": round(usd_interest, 0),
        "tasa_supuesta_deuda_en_divisas_pct": usd_rate,
        "tipo_de_cambio_al_cierre": round(last.tipo_de_cambio, 2),
    }
    if uso == "deuda":
        # Both positions valued at the closing rate: pesos owed against dollars no longer owed.
        owed_usd = (usd_debt_avoided + usd_interest) * last.tipo_de_cambio
        out["deuda_en_divisas_evitada_con_intereses_en_pesos_ars"] = round(owed_usd, 0)
        out["costo_neto_en_pesos_ars"] = round(peso_gap - owed_usd, 0)
    return rows, out


def bcra_interest_on_purchases(
    factors: dict[str, dict[str, float]], desde: str, hasta: str
) -> dict[str, float]:
    """Interest the BCRA paid, split pro rata by what created the pesos it was absorbing.

    The share of each month is the cumulative net purchases of dollars (from the private sector
    less the sales to the Treasury) over the cumulative pesos created by every factor, both from
    `desde`. It is an assumption: the sources do not tie each peso absorbed to its origin."""
    created_fx = created_all = paid = attributed = 0.0
    for m in sorted(k for k in factors if desde <= k <= hasta):
        f = factors[m]
        fx = f.get("Compra de divisas al sector privado", 0.0) + f.get("Divisas con el Tesoro", 0.0)
        created_fx += fx
        created_all += sum(v for k, v in f.items() if k != "base" and v > 0)
        interest = f.get("Intereses, primas y remuneración de cuentas corrientes", 0.0)
        share = min(1.0, max(0.0, created_fx / created_all)) if created_all else 0.0
        paid += interest
        attributed += interest * share
    return {"intereses_pagados_ars": round(paid, 0), "atribuidos_a_compras_netas_ars":
            round(attributed, 0)}  # fmt: skip


# ---------------------------------------------------------------- the years ahead


def month_range(desde: str, hasta: str) -> list[str]:
    y, m = int(desde[:4]), int(desde[5:])
    out = []
    while f"{y}-{m:02d}" <= hasta:
        out.append(f"{y}-{m:02d}")
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return out


def project_duties(
    base: dict[int, dict[str, float]],
    rate_of,
    months: list[str],
    ratio: float,
    shock: dict[str, dict[str, float]] | None = None,
) -> tuple[dict[str, float], dict[str, float]]:
    """(duty, FOB) in millions of USD for each month: the FOB of the same calendar month of the base
    year (USD by position), at the rate in force that month (`rate_of(code, month)`, percent or
    None), times the ratio of collected to estimated duties of the base year. `shock` maps a
    month to {group or "*": factor} applied to the FOB."""
    from argfx.simulation.exportaciones import group_of

    duties, fobs = {}, {}
    for mes in months:
        factors = (shock or {}).get(mes, {})
        duty = total = 0.0
        for code, fob in base[int(mes[5:])].items():
            k = factors.get(group_of(code), factors.get("*", 1.0))
            total += fob * k
            r = rate_of(code, mes)
            if r:
                duty += fob * k * r / 100
        duties[mes] = duty / 1e6 * ratio
        fobs[mes] = total / 1e6
    return duties, fobs


def drought(months: list[str], year: str, factor: float = 0.65) -> dict[str, dict[str, float]]:
    """A harvest like 2023: grains and oilseeds fall to `factor` of the base year for twelve
    months from April of `year` (exports of 2023 against 2022 in ARCA's files)."""
    window = month_range(f"{year}-04", f"{int(year) + 1}-03")
    return {m: {g: factor for g in AGRO} for m in months if m in window}


def price_fall(months: list[str], factor: float = 0.8) -> dict[str, dict[str, float]]:
    return {m: {"*": factor} for m in months}


def projected_payments(
    flows_csv: Path,
    shares_csv: Path,
    instruments_csv: Path,
    months: list[str],
    renew_agencies: bool,
) -> dict[str, float]:
    """Firm foreign-currency payments to holders outside the public sector, millions of USD by
    month. With `renew_agencies`, multilateral and bilateral lenders, the IMF included, roll over
    their principal (as the non-IMF agencies did in the mandate, chapter 4)."""
    with shares_csv.open(newline="", encoding="utf-8") as fh:
        public = {
            r["instrument_id"]: sum(
                float(r[k] or 0) for k in ("directo", "estimado", "proporcional")
            )
            for r in csv.DictReader(fh)
        }
    with instruments_csv.open(newline="", encoding="utf-8") as fh:
        family = {r["instrument_id"]: r["instrument_family"] for r in csv.DictReader(fh)}
    wanted = set(months)
    out: dict[str, float] = defaultdict(float)
    with flows_csv.open(newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            mes = r["date"][:7]
            if (
                mes not in wanted
                or r["base"] != "True"
                or r["is_payment"] != "True"
                or r["status"] != "firme"
                or r["currency_of_settlement"] == "ARS"
                or not r["monto_usd"]
            ):
                continue
            iid = r["instrument_id"]
            if (
                renew_agencies
                and r["flow_type"] == "amortizacion"
                and family.get(iid) in MULTILATERAL
            ):
                continue
            out[mes] += float(r["monto_usd"]) / 1e6 * (1 - min(1.0, public.get(iid, 0.0)))
    return {m: out.get(m, 0.0) for m in months}


@dataclass(frozen=True)
class Scenario:
    name: str
    shock: dict[str, dict[str, float]]
    renew_agencies: bool
    bcra_buys: float


def run_projection(
    months: list[str],
    duties_by_scenario: dict[str, tuple[dict[str, float], dict[str, float]]],
    payments_by_renewal: dict[bool, dict[str, float]],
    rate: float,
    scenarios: list[Scenario],
    opening: Opening,
) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    """Run (a), (c) and (d) for every scenario, with the Treasury buying from the BCRA what its
    FX deposits do not cover. The fund of (d) transfers one twelfth of the
    yearly average of the first five projected years (D-012: five years at the rates in force).
    The exchange rate is held at `rate`: the run measures dollars, and pesos only as the pesos
    the Treasury spends on dollars at that rate."""
    monthly_rows: list[dict[str, object]] = []
    summaries: list[dict[str, object]] = []
    for sc in scenarios:
        duties, exports_usd = duties_by_scenario[sc.name]
        payments = payments_by_renewal[sc.renew_agencies]
        path = [
            Month(m, exports_usd[m], duties[m], rate, payments[m]) for m in months
        ]  # fmt: skip
        first5 = [duties[m] for m in months[:60]]
        reference = sum(first5) / len(first5)
        regimes = [REGIMES["a"], REGIMES["c"], Regime("d", True, fund=FundRule(reference))]
        for regime in regimes:
            res = simulate(path, regime, Behavior(bcra_buys=sc.bcra_buys), opening)
            for row in res.rows:
                monthly_rows.append(
                    {"escenario": sc.name, "renuevan_organismos": sc.renew_agencies, **row}
                )
            # Gross reserves leave the summary: without imports and the rest of the balance of
            # payments, their level ahead means nothing. The Treasury's measures do not depend on
            # how much the BCRA buys.
            s = {k: v for k, v in summary(res).items() if k != "reservas_brutas_finales_usd"}
            by_year: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
            for row in res.rows:
                y = str(row["mes"])[:4]
                for k in ("servicio_usd", "ingreso_tesoro_divisas_usd", "compra_tesoro_al_bcra_usd",
                          "cancelacion_anticipada_usd", "derecho_usd"):  # fmt: skip
                    by_year[y][k] += float(row[k])  # type: ignore[arg-type]
            payments_total = sum(payments.values())
            summaries.append(
                {
                    "escenario": sc.name,
                    "renuevan_organismos": sc.renew_agencies,
                    "bcra_compra": sc.bcra_buys,
                    **s,
                    "derechos_usd": round(sum(duties.values()), 0),
                    "servicio_usd": round(payments_total, 0),
                    "cobertura_con_derechos_pct": round(
                        100 * sum(duties.values()) / payments_total, 1) if payments_total else None,
                    "fondo_referencia_mensual_usd": round(reference, 1) if regime.fund else None,
                    "fondo_maximo_usd": round(max(float(r["fondo_usd"]) for r in res.rows), 0),
                    "cancelacion_anticipada_usd": round(
                        sum(float(r["cancelacion_anticipada_usd"]) for r in res.rows), 0),
                    "por_anio": {y: {k: round(v, 0) for k, v in d.items()}
                                 for y, d in sorted(by_year.items())},
                }
            )  # fmt: skip
    return monthly_rows, summaries


def collection_ratio(table_csv: Path, months: list[str]) -> float:
    """Collected over estimated duties in `months` (output of `argfx derechos`)."""
    est = col = 0.0
    with table_csv.open(newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["mes"] in months and r["derecho_cobrado_musd"]:
                est += float(r["derecho_estimado_musd"])
                col += float(r["derecho_cobrado_musd"])
    if not est:
        raise ValueError("sin derechos estimados y cobrados en la base")
    return col / est


def observed_duties(table_csv: Path) -> dict[str, float]:
    with table_csv.open(newline="", encoding="utf-8") as fh:
        return {
            r["mes"]: float(r["derecho_cobrado_musd"])
            for r in csv.DictReader(fh)
            if r["derecho_cobrado_musd"]
        }


def monthly_rate(series_csv: Path) -> dict[str, float]:
    acc: dict[str, list[float]] = defaultdict(list)
    with series_csv.open(newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            acc[r["fecha"][:7]].append(float(r["valor"]))
    return {m: sum(v) / len(v) for m, v in acc.items()}


def rate_lookup(book, pi: dict[str, float]):
    """rate_of(code, month) in percent: the book, or the crude formula at the last known
    international price for the positions of Decreto 488/2020."""
    from argfx.simulation.alicuotas import FORMULA_488, crude_rate, formula_top

    last_pi = pi[max(pi)]

    def rate_of(code: str, mes: str) -> float | None:
        if code.startswith(FORMULA_488):
            return crude_rate(pi.get(mes, last_pi), top=formula_top(code, mes))
        hit = book.rate(code[:10], date(int(mes[:4]), int(mes[5:]), 15))
        return hit[0] if hit else None

    return rate_of
