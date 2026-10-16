from __future__ import annotations

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

# A harvest year in miniature: duties arrive in months 2 and 3, payments fall in months 1 and 4.
PATH = [
    Month("2027-01", exports_usd=100, duty_usd=10, ars_per_usd=1000, payments_usd=30),
    Month("2027-02", exports_usd=300, duty_usd=30, ars_per_usd=1000, payments_usd=0),
    Month("2027-03", exports_usd=300, duty_usd=30, ars_per_usd=1000, payments_usd=0),
    Month("2027-04", exports_usd=100, duty_usd=10, ars_per_usd=1000, payments_usd=40),
]
OPEN = Opening(reserves_usd=500, treasury_usd=0, treasury_ars=0, debt_usd=1000)


def test_every_regime_keeps_the_columns_closed() -> None:
    for regime in (*REGIMES.values(), Regime("d", True, fund=FundRule(20))):
        res = simulate(PATH, regime, Behavior(bcra_buys=0.7, sterilized=0.5), OPEN)
        assert summary(res)["columnas_cierran"]


def test_with_the_bcra_buying_everything_pesos_and_dollars_only_change_pockets() -> None:
    a = summary(simulate(PATH, REGIMES["a"], Behavior(bcra_buys=1.0), OPEN))
    c = summary(simulate(PATH, REGIMES["c"], Behavior(bcra_buys=1.0), OPEN))
    # Same dollars in the consolidated public sector...
    assert a["reservas_brutas_finales_usd"] == c["reservas_brutas_finales_usd"] == 1230
    # ...but in (a) the Treasury buys them with pesos: 30 in January, 40 in April.
    assert a["compras_tesoro_al_bcra_usd"] == 70.0 and a["meses_con_faltante"] == 2
    # In (c) it holds the 10 of January's duty (buys 20) and 70 by April (buys nothing).
    assert c["compras_tesoro_al_bcra_usd"] == 20.0 and c["meses_con_faltante"] == 1
    # Starting with no pesos, the January shortfall is 20 in both: in (a) the 10.000 pesos of
    # duty pay for a third of the 30 bought; the rest is peso debt. In (a) the duty pesos of
    # February and March pay for April.
    assert a["deuda_en_pesos_para_comprar_ars"] == c["deuda_en_pesos_para_comprar_ars"] == 20_000


def test_when_the_bcra_buys_part_the_dollar_duty_keeps_more_reserves() -> None:
    half = Behavior(bcra_buys=0.5)
    a = summary(simulate(PATH, REGIMES["a"], half, OPEN))
    c = summary(simulate(PATH, REGIMES["c"], half, OPEN))
    # (a): the BCRA buys half of 800; (c): all of the 80 of duty plus half of the other 720.
    assert a["reservas_brutas_finales_usd"] == 500 + 400 - 70
    assert c["reservas_brutas_finales_usd"] == 500 + 80 + 360 - 70


def test_the_fund_turns_the_harvest_into_a_steady_monthly_transfer() -> None:
    d = simulate(PATH, Regime("d", True, fund=FundRule(reference_monthly_usd=20, cap_months=12)),
                 Behavior(), OPEN)  # fmt: skip
    inflow = [r["ingreso_tesoro_divisas_usd"] for r in d.rows]
    assert inflow == [10, 20, 20, 20]  # January: only the 10 that came in
    # 80 in, 70 transferred; with no payments left in the horizon, the 10 over the cap prepay.
    assert d.rows[-1]["fondo_usd"] == 0 and d.rows[-1]["cancelacion_anticipada_usd"] == 10
    c = simulate(PATH, REGIMES["c"], Behavior(), OPEN)
    assert summary(d)["ingreso_tesoro_divisas_cv"] < summary(c)["ingreso_tesoro_divisas_cv"]
