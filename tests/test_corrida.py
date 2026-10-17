from __future__ import annotations

from pathlib import Path

import pytest

from argfx.simulation.corrida import (
    MandateMonth,
    bcra_interest_on_purchases,
    drought,
    mandate_counterfactual,
    month_range,
    project_duties,
    projected_payments,
)


def _month(mes: str, duty: float, bought: float, market: float = 0.0, debt: float = 0.0,
           bcra: float = 0.0, rate: float = 0.0, e: float = 1000.0) -> MandateMonth:  # fmt: skip
    return MandateMonth(mes, e, duty, 100.0, bcra, bought, market, debt, rate)


def test_duty_dollars_replace_purchases_and_leave_only_the_timing_in_pesos() -> None:
    months = [_month("2024-01", 10, 0), _month("2024-02", 10, 15), _month("2024-03", 0, 20)]
    rows, s = mandate_counterfactual(months, "compras")
    assert [r["compras_tesoro_evitadas_usd"] for r in rows] == [0.0, 15.0, 5.0]
    # With one exchange rate and no interest, the pesos not collected equal the pesos not spent.
    assert s["brecha_pesos_tesoro_al_cierre_ars"] == 0
    # The BCRA bought nothing, so every duty dollar adds to the consolidated public sector.
    assert s["reservas_consolidadas_dif_usd"] == 20


def test_purchases_in_the_market_avoided_do_not_add_reserves() -> None:
    _, s = mandate_counterfactual([_month("2024-01", 10, 10, market=10)], "compras")
    assert s["reservas_consolidadas_dif_usd"] == 0


def test_the_bcra_share_of_the_market_is_bought_less() -> None:
    _, s = mandate_counterfactual([_month("2024-01", 10, 0, bcra=50)], "compras")
    assert s["compras_bcra_menos_usd"] == 5 and s["reservas_consolidadas_dif_usd"] == 5


def test_replacing_dollar_debt_carries_both_debts_to_the_close() -> None:
    months = [_month("2024-01", 12, 0, debt=12, rate=12.0, e=1000),
              _month("2024-02", 0, 0, rate=12.0, e=1100)]  # fmt: skip
    _, s = mandate_counterfactual(months, "deuda", usd_rate=12.0)
    assert s["deuda_en_divisas_evitada_usd"] == 12
    assert s["brecha_pesos_tesoro_al_cierre_ars"] == round(12_000 * 1.01)
    assert s["intereses_en_divisas_evitados_usd"] == 0  # 0.12 rounds to zero
    assert s["costo_neto_en_pesos_ars"] == round(12_000 * 1.01 - 12.12 * 1100)


def test_unknown_use_is_refused() -> None:
    with pytest.raises(ValueError):
        mandate_counterfactual([_month("2024-01", 1, 0)], "otro")


def test_bcra_interest_is_split_by_the_pesos_its_purchases_created() -> None:
    factors = {
        "2024-01": {"Compra de divisas al sector privado": 30.0, "Pases": 70.0,
                    "Intereses, primas y remuneración de cuentas corrientes": 10.0},
        "2024-02": {"Divisas con el Tesoro": -30.0,
                    "Intereses, primas y remuneración de cuentas corrientes": 10.0},
    }  # fmt: skip
    out = bcra_interest_on_purchases(factors, "2024-01", "2024-02")
    # January: 30 of 110 created; February: net purchases fall to zero.
    assert out["intereses_pagados_ars"] == 20
    assert out["atribuidos_a_compras_netas_ars"] == round(10 * 30 / 110)


def test_duties_follow_the_rate_of_each_month_and_the_shock() -> None:
    base = {1: {"1201.90.00": 1e9, "8703.23.10": 1e9}, 2: {"1201.90.00": 2e9}}

    def rate_of(code: str, mes: str) -> float | None:
        if code.startswith("1201"):
            return 26.0 if mes < "2027-01" else 24.0
        return None

    months = ["2026-01", "2026-02", "2027-01"]
    duty, fob = project_duties(base, rate_of, months, 0.5, drought(months, "2026"))
    assert duty == {"2026-01": 130.0, "2026-02": 260.0, "2027-01": 120.0 * 0.65}
    assert fob["2026-01"] == 2000.0 and fob["2027-01"] == 650.0 + 1000.0


def test_payments_leave_out_the_public_sector_and_optionally_the_agencies(tmp_path: Path) -> None:
    flows = tmp_path / "flujos.csv"
    head = "instrument_id,date,flow_type,status,is_payment,base,currency_of_settlement,monto_usd"
    flows.write_text("\n".join([
        head,
        "B,2027-01-09,amortizacion,firme,True,True,USD,1000000000",
        "B,2027-01-09,interes,firme,True,True,USD,100000000",
        "M,2027-01-15,amortizacion,firme,True,True,USD,500000000",
        "M,2027-01-15,interes,firme,True,True,USD,50000000",
        "P,2027-01-20,amortizacion,firme,True,True,ARS,999000000",
        "B,2027-01-09,interes,estimado,True,True,USD,7000000",
    ]))  # fmt: skip
    shares = tmp_path / "shares.csv"
    shares.write_text("instrument_id,directo,estimado,proporcional\nB,0.5,0,0.1\n")
    inst = tmp_path / "inst.csv"
    inst.write_text("instrument_id,instrument_family\nB,USD\nM,multilateral\nP,ARS\n")
    m = ["2027-01"]
    assert projected_payments(flows, shares, inst, m, False) == {"2027-01": pytest.approx(990.0)}
    assert projected_payments(flows, shares, inst, m, True) == {"2027-01": pytest.approx(490.0)}


def test_month_range_crosses_the_year() -> None:
    assert month_range("2026-11", "2027-02") == ["2026-11", "2026-12", "2027-01", "2027-02"]
