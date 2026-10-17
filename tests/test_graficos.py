from __future__ import annotations

import json
from pathlib import Path

from argfx.informe.graficos import chart_html, creditor_class, debt_by_holder


def test_debt_by_holder_keeps_each_currency_in_its_panel(tmp_path: Path) -> None:
    comp = tmp_path / "sp.csv"
    comp.write_text(
        "capa,partida,millones_usd,porcentaje,source_id\n"
        "oficial,multilaterales_y_bilaterales,100,,X\n"
        "oficial (derivado),sector_publico_en_dolares,60,,X\n"
    )
    pesos = tmp_path / "pesos.csv"
    pesos.write_text("grupo,bruta_musd,sector_publico_oficial_musd\ncer,150,100\npesos,50,20\n")
    g = debt_by_holder(comp, pesos, normal_musd=450, ars_per_usd=1000)
    by = {(s.nombre, s.panel): s.valores[0] for s in g.series}
    assert by[("Sector público", 0)] == 0.12 and by[("Privados", 0)] == 0.08  # trillions
    assert by[("Privados", 1)] == 450 - 200 - 60 - 100
    html = chart_html(g)
    traces = json.loads(html.split("Plotly.newPlot('g',")[1].split(',{"title"')[0])
    # One legend entry per holder, although it appears in both panels.
    assert sum(t["showlegend"] for t in traces if t["name"] == "Privados") == 1
    assert {t["yaxis"] for t in traces} == {"y", "y2"}


def test_creditor_classes() -> None:
    def c(name: str, family: str) -> str:
        return creditor_class({"operation_name_sigade": name, "instrument_family": family})

    assert c("Extended Fund Facility  2022", "multilateral") == "FMI"
    assert c("BID 1234/OC-AR", "multilateral") == "Otros organismos"
    assert c("BONO GLOBAL/U$S/STEP UP/9-7-30", "USD") == "Globales"
    assert c("BONO R.A./U$S/STEP UP/9-7-2030", "USD") == "Bonares"
    assert c("LETRA/U$S/BCRA/2032", "USD") == "Letras con el BCRA y el sector público"
    assert c("BONAR/U$S/6%/29-10-2027", "USD") == "BONAR y BONTE nuevos"
    assert c("PAR/EUR/T.FIJA/2038", "moneda extranjera no USD") == "Bilaterales y otras monedas"
