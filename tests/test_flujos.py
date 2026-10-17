from argfx.informe.flujos import (
    CROSS_ARS,
    CROSS_USD,
    GAP,
    HUB_BCRA,
    FxMonth,
    ars_flows,
    bcra_flows,
    sankey_html,
    treasury_usd_flows,
    usd_flows,
)


def _bc(month: str, **codes: float) -> dict[str, dict[str, float]]:
    return {month: codes}


def test_usd_flows_close_with_reserves() -> None:
    monthly = _bc("2024-01", bal003=100, bal004=-70, bal042=-20, bal045=5, bal050=15)
    f = usd_flows(monthly, "2024-01", "2024-01")
    assert f.entradas["Exportaciones de bienes"] == 100
    assert f.salidas["Importaciones de bienes"] == 70
    assert f.entradas["Activos externos del sector público"] == 5
    assert f.salidas["Aumento de reservas"] == 15
    assert f.descuadre == 0


def test_usd_flows_reserve_loss_is_an_inflow() -> None:
    f = usd_flows(_bc("2024-01", bal004=-30, bal050=-30), "2024-01", "2024-01")
    assert f.entradas["Caída de reservas"] == 30
    assert f.descuadre == 0


def _aif(mes: str, **v: float) -> dict[str, str]:
    return {"mes": mes, **{k + "_millones_pesos_corrientes": str(x) for k, x in v.items()}}


RES = dict(
    ingresos_totales=100,
    ingresos_tributarios=90,
    derechos_de_exportacion=10,
    rentas_de_la_propiedad=4,
    gastos_corrientes_primarios=70,
    prestaciones_sociales=40,
    subsidios_economicos=5,
    transferencias_corrientes_a_provincias=3,
    transferencias_a_universidades=2,
    gastos_de_capital=10,
    intereses_netos=15,
)  # financial result: 100 - 80 - 15 = 5
FIN = dict(
    endeudamiento_moneda_local_total_spn=40,
    disminucion_inversion_financiera_total_spn=6,
    rentas_percibidas_del_bcra_total_spn=4,
    amortizacion_moneda_local_total_spn=35,
    inversion_financiera_total_spn=20,
)  # sources 50 - uses 55 = -5, the financial result with the sign reversed


def test_ars_flows_close_and_deflate() -> None:
    cpi = {"2024-01": 100.0, "2024-02": 200.0}
    res = [_aif("2024-01", **RES), _aif("2024-02", **RES)]
    fin = [{"mes": m, **{k: str(x) for k, x in FIN.items()}} for m in ("2024-01", "2024-02")]
    fx = {m: FxMonth(1.0, 0.0, 0.0) for m in cpi}
    f = ars_flows(res, fin, cpi, fx, "2024-01", "2024-12")
    assert f.unidad == "millones de pesos de 2024-02"
    assert f.entradas["Derechos de exportación"] == 10 * 2 + 10
    assert f.entradas["Utilidades del BCRA (rentas percibidas)"] == 4 * 3
    assert f.salidas["Activos financieros (aumento)"] == 20 * 3
    assert f.salidas["Funcionamiento y otros gastos corrientes"] == 20 * 3
    assert abs(f.descuadre) < 1e-9


def test_gap_is_drawn_not_absorbed() -> None:
    fin = [
        {
            "mes": "2024-01",
            **{k: str(x) for k, x in FIN.items()},
            "inversion_financiera_total_spn": "30",
        }
    ]
    fx = {"2024-01": FxMonth(1.0, 0.0, 0.0)}
    f = ars_flows([_aif("2024-01", **RES)], fin, {"2024-01": 1.0}, fx, "2024-01", "2024-01")
    assert f.descuadre == -10
    assert (GAP, f.hub, 10) in f.links()
    assert "plotly" in sankey_html(f, "t")


def test_dollars_leave_the_peso_table_through_one_crossing() -> None:
    # 12 of the 15 of interest are in dollars (2 USD at 6 pesos). The Treasury takes 60 pesos
    # (10 USD) of new foreign debt, amortizes 90 (15 USD) and its dollar deposits fall by 1 USD
    # (6 pesos), which the table counts among the 6 of "use of financial assets".
    fin = {
        **FIN,
        "endeudamiento_moneda_extranjera_total_spn": 60,
        "amortizacion_moneda_extranjera_total_spn": 90,
        "endeudamiento_moneda_local_total_spn": 40 + 30,
    }
    # Of the 46 pesos that cross, 3 USD (18 pesos) were bought and 12 cancelled debt with pesos.
    fx = {"2024-01": FxMonth(6.0, 2.0, -1.0, 3.0, 12.0)}
    rows = [{"mes": "2024-01", **{k: str(x) for k, x in fin.items()}}]
    f = ars_flows([_aif("2024-01", **RES)], rows, {"2024-01": 1.0}, fx, "2024-01", "2024-01")
    assert abs(f.descuadre) < 1e-9
    assert f.salidas["Intereses de la deuda en pesos (netos)"] == 15 - 12
    assert "Uso de activos financieros" not in f.entradas  # 6 - 6
    assert f.salidas[CROSS_ARS["compras"]] == 18
    assert f.salidas[CROSS_ARS["cancelado"]] == 12
    assert f.salidas[CROSS_ARS["resto"]] == 90 + 12 - 6 - 60 - 18 - 12
    assert not any("divisas" in n for n in [*f.entradas, *f.salidas])

    t = treasury_usd_flows(rows, fx, "2024-01", "2024-01")
    assert t.unidad == "millones de USD" and t.clave == "usd_tesoro"
    assert t.entradas == {
        "Deuda en divisas desembolsada": 10,
        CROSS_USD["compras"]: 3,
        CROSS_USD["cancelado"]: 2,
        CROSS_USD["resto"]: 1,
        "Depósitos en dólares en el BCRA (variación)": 1,
    }
    assert t.salidas == {"Deuda en divisas amortizada": 15, "Intereses en divisas": 2}
    assert abs(t.descuadre) < 1e-9


def test_dollar_debt_paid_in_pesos_moves_to_the_peso_table() -> None:
    # Of the 90 pesos of foreign-currency amortization, 5 USD (30 pesos) were a dual bond paid
    # in pesos; of the 60 disbursed, 1 USD (6 pesos) was a LELINK placed for pesos.
    fin = {
        **FIN,
        "endeudamiento_moneda_extranjera_total_spn": 60,
        "amortizacion_moneda_extranjera_total_spn": 90,
        "endeudamiento_moneda_local_total_spn": 40 + 30,
    }
    fx = {"2024-01": FxMonth(6.0, 2.0, -1.0, 3.0, 12.0, 5.0, 1.0)}
    rows = [{"mes": "2024-01", **{k: str(x) for k, x in fin.items()}}]
    f = ars_flows([_aif("2024-01", **RES)], rows, {"2024-01": 1.0}, fx, "2024-01", "2024-01")
    assert abs(f.descuadre) < 1e-9
    assert f.salidas["Deuda escrita en dólares, pagada en pesos"] == 30
    assert f.entradas["Deuda escrita en dólares, colocada por pesos"] == 6
    # 90 + 12 - 6 - 60 - 18 - 12 - 30 + 6 = -18: the rest flows back, an inflow
    assert f.entradas[CROSS_ARS["resto"]] == 18
    t = treasury_usd_flows(rows, fx, "2024-01", "2024-01")
    assert t.salidas["Deuda en divisas amortizada"] == 15 - 5
    assert t.entradas["Deuda en divisas desembolsada"] == 10 - 1
    assert abs(t.descuadre) < 1e-9


def test_bcra_flows_close_with_the_change_of_the_base() -> None:
    # January: buys 100 of dollars from the private sector, absorbs 70 with pases and pays 10
    # of interest; the base grows 40. February, prices doubled: the base falls 5.
    factors = {
        "2024-01": {"Compra de divisas al sector privado": 100.0, "Pases": -70.0,
                    "Intereses, primas y remuneración de cuentas corrientes": 10.0, "base": 40.0},
        "2024-02": {"Pases": -5.0, "base": -5.0},
    }  # fmt: skip
    f = bcra_flows(factors, {"2024-01": 1.0, "2024-02": 2.0}, "2024-01", "2024-12")
    assert f.hub == HUB_BCRA and f.clave == "ars_bcra"
    # Buying dollars and paying interest take pesos out of the BCRA; pases bring them in.
    assert f.salidas["Compra de divisas al sector privado"] == 200
    assert f.entradas["Pases"] == 145
    assert f.entradas["Emisión neta (aumento de la base monetaria)"] == 80 - 5
    assert abs(f.descuadre) < 1e-9
