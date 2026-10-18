"""Bar charts of the report, one currency per panel (D-017).

Each chart is a small HTML page with Plotly, like the Sankey diagrams of `flujos`, and a CSV
with the numbers behind it. A chart with pesos and dollars draws them in two panels, each with
its own axis and unit, never on one axis.
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from argfx.informe.flujos import PLOTLY

NAVY, BLUE, GOLD, GRAY = "#20293A", "#4E80EE", "#E1B53E", "#8B8580"
SAGE, ICE, PLUM, CORAL = "#CEE69E", "#B2F6FF", "#532E37", "#F15B40"
GREEN, RED = "#65C97A", "#C4302B"


@dataclass
class Serie:
    nombre: str
    valores: list[float | None]
    color: str
    panel: int = 0


@dataclass
class Grafico:
    clave: str
    titulo: str
    x: list[str]
    series: list[Serie]
    unidades: list[str]  # one per panel
    modo: str = "stack"  # Plotly barmode: stack or group
    titulos_panel: list[str] = field(default_factory=list)
    x_por_panel: list[list[str]] | None = None  # when the panels have different categories

    def filas(self) -> list[dict[str, object]]:
        rows = []
        for s in self.series:
            xs = self.x_por_panel[s.panel] if self.x_por_panel else self.x
            for x, v in zip(xs, s.valores, strict=True):
                rows.append(
                    {
                        "serie": s.nombre,
                        "panel": self.unidades[s.panel],
                        "x": x,
                        "valor": None if v is None else round(v, 1),
                    }
                )
        return rows


def chart_html(g: Grafico) -> str:
    n = len(g.unidades)
    gap = 0.12 if n > 1 else 0.0
    width = (1 - gap * (n - 1)) / n
    traces = []
    seen: set[str] = set()
    for s in g.series:
        k = "" if s.panel == 0 else str(s.panel + 1)
        # A holder that appears in both panels gets one legend entry.
        traces.append(
            {
                "type": "bar",
                "name": s.nombre,
                "legendgroup": s.nombre,
                "showlegend": s.nombre not in seen,
                "x": g.x_por_panel[s.panel] if g.x_por_panel else g.x,
                "y": [None if v is None else round(v, 1) for v in s.valores],
                "marker": {"color": s.color},
                "xaxis": f"x{k}",
                "yaxis": f"y{k}",
                "hovertemplate": (
                    f"%{{x}}: %{{y:,.1f}} {g.unidades[s.panel]}<extra>{s.nombre}</extra>"
                ),
            }
        )
        seen.add(s.nombre)
    layout: dict[str, object] = {
        "title": {"text": g.titulo, "font": {"size": 15}},
        "barmode": g.modo,
        "font": {"family": "DM Sans, system-ui, sans-serif", "size": 12, "color": NAVY},
        "height": 480,
        "margin": {"l": 70, "r": 20, "t": 70, "b": 90},
        "legend": {"orientation": "h", "y": -0.18},
        "separators": ",.",
        "paper_bgcolor": "#ffffff",
        "plot_bgcolor": "#ffffff",
        "annotations": [],
    }
    for i, unit in enumerate(g.unidades):
        k = "" if i == 0 else str(i + 1)
        lo = i * (width + gap)
        layout[f"xaxis{k}"] = {"domain": [lo, lo + width], "anchor": f"y{k}", "type": "category"}
        layout[f"yaxis{k}"] = {
            "anchor": f"x{k}",
            "title": {"text": unit},
            "gridcolor": "#e6dccb",
            "zerolinecolor": NAVY,
            "tickformat": ",.0f",
        }
        if g.titulos_panel:
            layout["annotations"].append(  # type: ignore[union-attr]
                {
                    "text": f"<b>{g.titulos_panel[i]}</b>",
                    "x": lo + width / 2,
                    "y": 1.04,
                    "xref": "paper",
                    "yref": "paper",
                    "showarrow": False,
                }
            )
    return (
        "<!doctype html><html lang='es'><head><meta charset='utf-8'>"
        f"<title>{g.titulo}</title><script src='{PLOTLY}'></script>"
        "<style>html,body{margin:0;background:#fff}</style></head><body>"
        "<div id='g'></div><script>"
        "if (typeof Plotly === 'undefined') { document.getElementById('g').textContent ="
        f" 'No se pudo cargar Plotly desde {PLOTLY}. Los datos están en el CSV de al lado.'; }}"
        f" else {{ Plotly.newPlot('g',{json.dumps(traces, ensure_ascii=False)},"
        f"{json.dumps(layout, ensure_ascii=False)},{{responsive:true,displayModeBar:false}}); }}"
        "</script></body></html>"
    )


def write_chart(g: Grafico, out_dir: Path) -> Path:
    from argfx.contracts.calendar import _write

    out_dir.mkdir(parents=True, exist_ok=True)
    _write(out_dir / f"grafico_{g.clave}.csv", g.filas())
    path = out_dir / f"grafico_{g.clave}.html"
    path.write_text(chart_html(g), encoding="utf-8")
    return path


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


# ---------------------------------------------------------------- the charts


def debt_by_holder(
    sector_publico_csv: Path, pesos_csv: Path, normal_musd: float, ars_per_usd: float
) -> Grafico:
    """The stock at the cut-off by currency of payment and holder: pesos in trillions of pesos,
    dollars in millions of USD. Agencies hold only foreign-currency debt."""
    comp = {r["partida"]: r for r in _read(sector_publico_csv)}
    pesos = _read(pesos_csv)
    total_ars = sum(float(r["bruta_musd"]) for r in pesos)
    public_ars = sum(float(r["sector_publico_oficial_musd"]) for r in pesos)
    total_fx = normal_musd - total_ars
    public_fx = float(comp["sector_publico_en_dolares"]["millones_usd"])
    agencies = float(comp["multilaterales_y_bilaterales"]["millones_usd"])
    private_fx = total_fx - public_fx - agencies
    k = ars_per_usd / 1e6  # millions of USD to trillions of pesos
    return Grafico(
        "deuda_por_tenedor",
        "Quién tiene la deuda, al 30-06-2026",
        [],
        [
            Serie("Sector público", [public_ars * k], GRAY, 0),
            Serie("Privados", [(total_ars - public_ars) * k], GOLD, 0),
            Serie("Sector público", [public_fx], GRAY, 1),
            Serie("Privados", [private_fx], GOLD, 1),
            Serie("Organismos internacionales", [agencies], NAVY, 1),
        ],
        ["billones de pesos", "millones de USD"],
        titulos_panel=["Deuda que se paga en pesos", "Deuda que se paga en divisas"],
        x_por_panel=[["Se paga en pesos"], ["Se paga en divisas"]],
    )


def third_parties(rows: list[dict[str, object]]) -> Grafico:
    """Debt with holders outside the public sector at each cut-off: in pesos, the Treasury's
    with private holders plus the BCRA's remunerated liabilities, in constant pesos; in foreign
    currency, private holders and agencies, in millions of USD (`terceros`)."""
    months = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
    x = [
        f"{months[int(str(r['corte'])[5:7]) - 1].capitalize()} {str(r['corte'])[:4]}" for r in rows
    ]

    def col(k: str) -> list[float | None]:
        return [float(r[k]) for r in rows]  # type: ignore[arg-type]

    base = str(rows[0]["pesos_de"])
    return Grafico(
        "deuda_con_terceros",
        "Deuda con acreedores fuera del sector público, por moneda de pago",
        x,
        [
            Serie(
                "Tesoro: deuda en pesos con privados",
                col("pesos_privados_tesoro_constantes"),
                GOLD,
                0,
            ),
            Serie(
                "BCRA: pases, LELIQ y otros pasivos remunerados",
                col("pasivos_remunerados_bcra_constantes"),
                BLUE,
                0,
            ),
            Serie("Privados", col("divisas_privados_usd"), GOLD, 1),
            Serie("Deuda en default no reestructurada", col("divisas_holdouts_usd"), GRAY, 1),
            Serie("Organismos internacionales", col("divisas_organismos_usd"), NAVY, 1),
        ],
        [f"billones de pesos de {months[int(base[5:7]) - 1]} de {base[:4]}", "millones de USD"],
        titulos_panel=["Se paga en pesos", "Se paga en divisas"],
    )


def creditor_class(row: dict[str, str]) -> str:
    name = row.get("operation_name_sigade", "").upper()
    family = row.get("instrument_family", "")
    if "FUND FACILITY" in name:
        return "FMI"
    if family == "multilateral":
        return "Otros organismos"
    if family == "USD" and "LETRA" in name:
        return "Letras con el BCRA y el sector público"
    if "GLOBAL" in name:
        return "Globales"
    if family == "USD" and ("BONO R.A." in name or name.startswith("PAR/")):
        return "Bonares"
    if family == "USD":
        return "BONAR y BONTE nuevos"
    return "Bilaterales y otras monedas"


CLASSES = [
    "FMI",
    "Otros organismos",
    "Globales",
    "Bonares",
    "BONAR y BONTE nuevos",
    "Bilaterales y otras monedas",
    "Letras con el BCRA y el sector público",
]
CLASS_COLORS = [NAVY, PLUM, BLUE, ICE, SAGE, GOLD, GRAY]


def maturities_by_creditor(flows_csv: Path, instruments_csv: Path, years: list[str]) -> Grafico:
    """Firm foreign-currency payments by calendar year and creditor (phase 2 calendar)."""
    inst = {r["instrument_id"]: r for r in _read(instruments_csv)}
    acc: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for r in _read(flows_csv):
        y = r["date"][:4]
        if (
            y not in years
            or r["base"] != "True"
            or r["is_payment"] != "True"
            or r["status"] != "firme"
            or r["currency_of_settlement"] == "ARS"
            or not r["monto_usd"]
        ):
            continue
        acc[creditor_class(inst.get(r["instrument_id"], {}))][y] += float(r["monto_usd"]) / 1e6
    return Grafico(
        "vencimientos_por_acreedor",
        "Vencimientos en divisas por acreedor, capital e interés, sin refinanciación",
        years,
        [
            Serie(c, [acc[c][y] for y in years], col)
            for c, col in zip(CLASSES, CLASS_COLORS, strict=True)
        ],
        ["millones de USD"],
    )


def trade_vs_service(imf_csv: Path, projection_csv: Path) -> Grafico:
    """The IMF's projected goods surplus against the foreign-currency service to holders outside
    the public sector (phase 4 projection), by year."""
    imf = {r["anio"]: float(r["balanza_bienes_musd"]) for r in _read(imf_csv)}
    service: dict[str, float] = defaultdict(float)
    for r in _read(projection_csv):
        service[r["mes"][:4]] += float(r["servicio_consolidado_usd"])
    years = [y for y in sorted(imf) if y in service and service[y] > 0 and y >= "2027"]
    return Grafico(
        "balanza_vs_servicio",
        "Superávit comercial proyectado y vencimientos en divisas con terceros",
        years,
        [
            Serie("Saldo de bienes proyectado por el FMI", [imf[y] for y in years], GREEN),
            Serie(
                "Vencimientos en divisas fuera del sector público",
                [service[y] for y in years],
                NAVY,
            ),
        ],
        ["millones de USD"],
        modo="group",
    )


def accrued_result(devengados_csv: Path) -> Grafico:
    """Published cash financial result against the result with the capitalized interest of the
    national public sector (middle of the FGS range), current pesos by quarter."""
    rows = _read(devengados_csv)
    q = [r["trimestre"] for r in rows]
    published = [float(r["spn_resultado_financiero_caja"]) / 1000 for r in rows]
    accrued = [
        (
            float(r["resultado_financiero_con_devengado_spn_min"])
            + float(r["resultado_financiero_con_devengado_spn_max"])
        )
        / 2000
        for r in rows
    ]
    return Grafico(
        "resultado_devengado",
        "Resultado financiero en base caja y con intereses capitalizados devengados",
        q,
        [
            Serie("En base caja (publicado)", published, GREEN),
            Serie("Con intereses capitalizados devengados, sin ajuste CER", accrued, RED),
        ],
        ["billones de pesos corrientes"],
        modo="group",
    )


def duties_vs_service(projection_csv: Path) -> Grafico:
    """Phase 4 projection: duties paid in dollars against the service to holders outside the
    public sector, by year, with and without the agencies rolling over their principal."""
    acc: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for r in _read(projection_csv):
        y = r["mes"][:4]
        for k in (
            "derecho_base_usd",
            "servicio_consolidado_usd",
            "servicio_si_renuevan_organismos_usd",
        ):
            acc[y][k] += float(r[k])
    years = [
        y
        for y in sorted(acc)
        if len(y) == 4 and acc[y]["servicio_consolidado_usd"] > 0 and y >= "2027"
    ]
    return Grafico(
        "derechos_vs_servicio",
        "Derechos de exportación cobrados en dólares y vencimientos con terceros",
        years,
        [
            Serie(
                "Derechos en dólares (proyección base)",
                [acc[y]["derecho_base_usd"] for y in years],
                GREEN,
            ),
            Serie(
                "Vencimientos si los organismos renuevan el capital",
                [acc[y]["servicio_si_renuevan_organismos_usd"] for y in years],
                BLUE,
            ),
            Serie(
                "Vencimientos sin refinanciación",
                [acc[y]["servicio_consolidado_usd"] for y in years],
                NAVY,
            ),
        ],
        ["millones de USD"],
        modo="group",
    )


def fund_smoothing(monthly_csv: Path, desde: str, hasta: str) -> Grafico:
    """Dollars reaching the Treasury each month in (c) and (d), base scenario."""
    acc: dict[str, dict[str, float]] = defaultdict(dict)
    for r in _read(monthly_csv):
        if (
            r["escenario"] == "base"
            and r["renuevan_organismos"] == "False"
            and desde <= r["mes"] <= hasta
            and r["regimen"] in ("c", "d")
        ):
            acc[r["regimen"]].setdefault(r["mes"], float(r["ingreso_tesoro_divisas_usd"]))
    months = sorted(acc["c"])
    return Grafico(
        "fondo_mensual",
        "Dólares que recibe el Tesoro cada mes: cobro directo y con fondo",
        months,
        [
            Serie("(c) Cobro en dólares", [acc["c"][m] for m in months], GOLD),
            Serie("(d) Con fondo de estabilización", [acc["d"][m] for m in months], NAVY),
        ],
        ["millones de USD"],
        modo="group",
    )
