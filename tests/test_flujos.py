from argfx.informe.flujos import GAP, ars_flows, sankey_html, usd_flows


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
    f = ars_flows(res, fin, cpi, "2024-01", "2024-12")
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
            "aplicaciones_financieras_total_spn": "65",
        }
    ]
    f = ars_flows([_aif("2024-01", **RES)], fin, {"2024-01": 1.0}, "2024-01", "2024-01")
    assert f.descuadre == -10
    assert (GAP, f.hub, 10) in f.links()
    assert "plotly" in sankey_html(f, "t")
