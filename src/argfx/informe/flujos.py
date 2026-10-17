"""Where pesos and dollars came in and went out over the mandate (D-016, D-017).

Two flow tables, one per currency, never added to each other:
- dollars: the BCRA balance cambiario (lote AH, SRC-1604), gross inflows and outflows of the
  foreign-exchange market, closed by the change in reserves from transactions. Millions of USD.
- pesos: the cash-basis result of the national public sector and its financial sources and uses
  (lote AM, Secretaría de Hacienda), closed by the financial result. Millions of pesos at the
  prices of the last month with a CPI index (INDEC, lote AM), deflated month by month.

Each table is a list of (origen, destino, monto) links around a single hub node, ready for a
Sankey diagram. Inflows go origin -> hub and outflows hub -> destination; both sides add up to
the same total, and any gap is reported, never absorbed.
"""

from __future__ import annotations

import csv
import datetime as dt
import json
from dataclasses import dataclass
from pathlib import Path

HUB_USD = "Mercado de cambios"
HUB_ARS = "Sector Público Nacional"
GAP = "Sin identificar en la fuente"

# Balance cambiario columns (sheet "Balance Cambiario", codes on row 11).
USD_IN = {
    "Exportaciones de bienes": "bal003",
    "Servicios (cobros)": "bal006",
    "Intereses cobrados": "bal010",
    "Utilidades cobradas": "bal017",
    "Ingreso secundario (cobros)": "bal020",
    "Inversión directa (ingresos)": "bal026",
    "Portafolio (ingresos)": "bal029",
    "Préstamos y títulos (ingresos)": "bal032",
    "FMI (desembolsos)": "bal035",
    "Otros organismos (desembolsos)": "bal038",
    "Venta de billetes y divisas de privados": "bal041",
}
USD_OUT = {
    "Importaciones de bienes": "bal004",
    "Servicios (pagos)": "bal007",
    "Intereses al FMI": "bal012",
    "Intereses a otros organismos": "bal013",
    "Otros intereses": "bal014",
    "Intereses del Gobierno Nacional": "bal015",
    "Utilidades y dividendos": "bal018",
    "Ingreso secundario (pagos)": "bal021",
    "Inversión directa (egresos)": "bal027",
    "Portafolio (egresos)": "bal030",
    "Préstamos y títulos (egresos)": "bal033",
    "FMI (capital)": "bal036",
    "Otros organismos (capital)": "bal039",
    "Compra de billetes y divisas de privados": "bal042",
}
# Net items: an inflow when positive, an outflow when negative.
USD_NET = {
    "Cuenta capital": "bal023",
    "Canje": "bal043",
    "Activos externos del sector financiero": "bal044",
    "Activos externos del sector público": "bal045",
    "Compra-venta de títulos": "bal046",
    "Otras operaciones del sector público": "bal047",
    "Otros movimientos": "bal048",
    "Concepto no informado": "bal049",
}
USD_RESERVES = "bal050"


@dataclass
class Flows:
    moneda: str
    unidad: str
    desde: str
    hasta: str
    hub: str
    entradas: dict[str, float]
    salidas: dict[str, float]

    @property
    def descuadre(self) -> float:
        return sum(self.entradas.values()) - sum(self.salidas.values())

    def links(self) -> list[tuple[str, str, float]]:
        """Sankey links; a gap between the two sides is drawn as its own node."""
        out = [(k, self.hub, v) for k, v in self.entradas.items() if v > 0]
        out += [(self.hub, k, v) for k, v in self.salidas.items() if v > 0]
        gap = self.descuadre
        if gap < -0.5:
            out.append((GAP, self.hub, -gap))
        elif gap > 0.5:
            out.append((self.hub, GAP, gap))
        return out


def _add_signed(name: str, value: float, ins: dict[str, float], outs: dict[str, float]) -> None:
    if value >= 0:
        ins[name] = ins.get(name, 0.0) + value
    else:
        outs[name] = outs.get(name, 0.0) - value


def usd_flows(monthly: dict[str, dict[str, float]], desde: str, hasta: str) -> Flows:
    """`monthly` maps YYYY-MM to balance cambiario codes (millions of USD)."""
    months = sorted(m for m in monthly if desde <= m <= hasta)
    if not months:
        raise ValueError(f"sin datos del balance cambiario entre {desde} y {hasta}")

    def total(code: str) -> float:
        return sum(monthly[m].get(code) or 0.0 for m in months)

    ins = {k: total(c) for k, c in USD_IN.items()}
    outs = {k: abs(total(c)) for k, c in USD_OUT.items()}
    for k, c in USD_NET.items():
        _add_signed(k, total(c), ins, outs)
    reserves = total(USD_RESERVES)
    if reserves >= 0:
        outs["Aumento de reservas"] = reserves
    else:
        ins["Caída de reservas"] = -reserves
    return Flows("USD", "millones de USD", months[0], months[-1], HUB_USD, ins, outs)


def read_balance_cambiario(xlsx: Path) -> dict[str, dict[str, float]]:
    from openpyxl import load_workbook

    wb = load_workbook(xlsx, read_only=True, data_only=True)
    rows = list(wb["Balance Cambiario"].iter_rows(values_only=True))
    codes = {j: c for j, c in enumerate(rows[10]) if isinstance(c, str) and c.startswith("bal")}
    out: dict[str, dict[str, float]] = {}
    for r in rows[11:]:
        if isinstance(r[0], dt.datetime):
            out[f"{r[0].year}-{r[0].month:02d}"] = {
                c: float(r[j]) for j, c in codes.items() if isinstance(r[j], (int, float))
            }
    return out


# AIF columns (lote AM), millions of current pesos. Revenue and primary spending come from the
# result table; financing from the sources and uses table, total national public sector, so that
# both sides cover the same perimeter.
SPENDING = {
    "Prestaciones sociales": "prestaciones_sociales",
    "Subsidios económicos": "subsidios_economicos",
    "Transferencias a provincias": "transferencias_corrientes_a_provincias",
    "Universidades": "transferencias_a_universidades",
}
FIN_IN = {
    "Deuda en pesos colocada": "endeudamiento_moneda_local_total_spn",
    "Deuda en divisas desembolsada (en pesos)": "endeudamiento_moneda_extranjera_total_spn",
    "Otros pasivos (aumento)": "incremento_otros_pasivos_total_spn",
}
FIN_OUT = {
    "Deuda en pesos amortizada": "amortizacion_moneda_local_total_spn",
    "Deuda en divisas amortizada (en pesos)": "amortizacion_moneda_extranjera_total_spn",
    "Otros pasivos (disminución)": "disminucion_otros_pasivos_total_spn",
}
# The financial-asset lines are taken as the rest of each side's total: in lote AM the
# `inversion_financiera_total_spn` column is near zero while total uses exceed amortizations by
# trillions, and the totals do close with the financial result every month.
FIN_IN_REST = ("Uso de activos financieros", "fuentes_financieras_total_spn")
FIN_OUT_REST = ("Activos financieros (aumento)", "aplicaciones_financieras_total_spn")
SUFFIX = "_millones_pesos_corrientes"


def _num(row: dict[str, str], col: str) -> float:
    v = row.get(col + SUFFIX, row.get(col, ""))
    return float(v) if v not in ("", None) else 0.0


def ars_month(r: dict[str, str], f: dict[str, str]) -> tuple[dict[str, float], dict[str, float]]:
    """One month of the peso circuit, in current pesos: (inflows, outflows)."""
    tax, dex, rent = (
        _num(r, c)
        for c in ("ingresos_tributarios", "derechos_de_exportacion", "rentas_de_la_propiedad")
    )
    ins = {
        "Derechos de exportación": dex,
        "Otros impuestos y aportes": tax - dex,
        "Rentas de la propiedad": rent,
        "Otros ingresos corrientes y de capital": _num(r, "ingresos_totales") - tax - rent,
    }
    outs = {k: _num(r, c) for k, c in SPENDING.items()}
    outs["Funcionamiento y otros gastos corrientes"] = _num(r, "gastos_corrientes_primarios") - sum(
        outs.values()
    )
    outs["Gasto de capital"] = _num(r, "gastos_de_capital")
    _add_signed("Intereses (deuda en pesos y en divisas)", -_num(r, "intereses_netos"), ins, outs)
    for side, table, (rest, total) in ((ins, FIN_IN, FIN_IN_REST), (outs, FIN_OUT, FIN_OUT_REST)):
        lines = {k: _num(f, c) for k, c in table.items()}
        side.update(lines)
        side[rest] = _num(f, total) - sum(lines.values())
    return ins, outs


def ars_flows(
    results: list[dict[str, str]],
    financing: list[dict[str, str]],
    cpi: dict[str, float],
    desde: str,
    hasta: str,
) -> Flows:
    """Pesos of the national public sector, at prices of the last month of the window.

    Only months present in both tables and with a CPI index are used; the window shrinks to them.
    """
    res = {r["mes"]: r for r in results}
    fin = {r["mes"]: r for r in financing}
    months = sorted(m for m in res if desde <= m <= hasta and m in fin and m in cpi)
    if not months:
        raise ValueError(f"sin meses con resultado, financiamiento e IPC entre {desde} y {hasta}")
    base = cpi[months[-1]]
    ins: dict[str, float] = {}
    outs: dict[str, float] = {}
    for m in months:
        k = base / cpi[m]
        m_ins, m_outs = ars_month(res[m], fin[m])
        for name, v in m_ins.items():
            _add_signed(name, k * v, ins, outs)
        for name, v in m_outs.items():
            _add_signed(name, -k * v, ins, outs)
    ins = {n: v for n, v in ins.items() if v > 0}
    outs = {n: v for n, v in outs.items() if v > 0}
    return Flows(
        "ARS", f"millones de pesos de {months[-1]}", months[0], months[-1], HUB_ARS, ins, outs
    )


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def read_cpi(path: Path) -> dict[str, float]:
    out = {}
    for r in read_csv(path):
        idx = next((r[c] for c in r if c.startswith("indice")), "")
        if idx not in ("", None):
            out[r["mes"]] = float(idx)
    return out


def write_flows(flows: Flows, out_dir: Path) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"flujos_{flows.moneda.lower()}_{flows.desde}_{flows.hasta}.csv"
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["origen", "destino", "monto", "unidad"])
        for a, b, v in flows.links():
            w.writerow([a, b, round(v, 1), flows.unidad])
    return path


PLOTLY = "https://cdnjs.cloudflare.com/ajax/libs/plotly.js/2.35.2/plotly.min.js"


def sankey_html(flows: Flows, title: str) -> str:
    links = flows.links()
    nodes = list(dict.fromkeys([a for a, _, _ in links] + [b for _, b, _ in links]))
    pos = {n: i for i, n in enumerate(nodes)}
    color = "#4E80EE" if flows.moneda == "USD" else "#E1B53E"
    data = {
        "type": "sankey",
        "valueformat": ",.0f",
        "valuesuffix": f" {flows.unidad}",
        "node": {"label": nodes, "pad": 14, "thickness": 16, "color": "#20293A"},
        "link": {
            "source": [pos[a] for a, _, _ in links],
            "target": [pos[b] for _, b, _ in links],
            "value": [round(v, 1) for _, _, v in links],
            "color": [color + "66"] * len(links),
        },
    }
    layout = {
        "title": {"text": title},
        "font": {"family": "DM Sans, system-ui, sans-serif", "size": 12},
        "height": 760,
    }
    return (
        "<!doctype html><html lang='es'><head><meta charset='utf-8'>"
        f"<title>{title}</title><script src='{PLOTLY}'></script></head><body>"
        "<div id='s'></div><script>"
        f"Plotly.newPlot('s',[{json.dumps(data, ensure_ascii=False)}],"
        f"{json.dumps(layout, ensure_ascii=False)},{{responsive:true}});"
        "</script></body></html>"
    )
