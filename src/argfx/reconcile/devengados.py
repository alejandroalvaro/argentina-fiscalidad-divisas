"""Interest capitalized and not paid, quarter by quarter, against the cash-basis fiscal result
(D-009).

The quarterly debt workbook of the Secretaría de Finanzas (A.2.2) has a line "Capitalización de
Bonos, Letras y otros préstamos", which, by its own footnote, includes the capitalization
accumulated on reopenings: when a LECAP or BONCAP is reopened, the new face value enters at
face and the capitalization it carries since issue enters through this line. That part was
paid in cash by the buyer; it is not interest accrued in the quarter. So:

    capitalized interest accrued = capitalization line - capitalization carried by reopenings

The second term comes from the placements of the Oficina Nacional de Crédito Público (sheets
of `colocaciones_<date>.xlsx`): for each placement of a fixed-rate LECAP or BONCAP settled
after its issue date, face x [(1 + TEM)^(DÍAS/30) - 1], with DÍAS from issue to settlement in
30E/360 (the legal formula). TAMAR and dual reopenings, whose TEM is not in the placement row,
use the effective value minus face as a proxy; rows without either are counted.

Placement discounts are accrued cost too: the Treasury owes the technical value and receives the
effective value. For each cash placement of a LECAP or BONCAP whose technical value is known
(face on a new issue, face times the capitalization factor on a fixed-rate reopening), the
difference is spread over the days from settlement to maturity. A negative difference is a
premium and lowers the cost.

Perimeter: net interest of the SPN leaves out interest paid inside it. The FGS holds part of
the LECAP and BONCAP, and its monthly report gives the portfolio by category, not by security
(`tenencias/fgs_cartera_categorias.csv`). Against the updated face of A.1.7, each category
bounds the FGS share of the capitalizing debt: at most what it holds, up to the capitalizing
stock of the category; at least what it holds beyond the non-capitalizing instruments that may
sit in the same category (LELINKs among the letters, fixed-rate BONTE among the bonds). The
accrued interest of the SPN perimeter is given at both bounds, for the quarters with a report.

The fiscal side is the monthly cash-basis result of the Sector Público Nacional (primary
result, net interest, financial result), summed by quarter. The perimeters differ: A.2.2 is the
Administración Central with every holder, while net interest of the SPN excludes interest paid
inside the SPN (to the FGS, for instance). Both are reported as they are.

Units: thousands of millions of pesos (miles de millones), current pesos.
"""

from __future__ import annotations

import csv
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path

from openpyxl import load_workbook

from argfx.contracts.calendar import _write
from argfx.contracts.daycount import year_fraction
from argfx.reconcile.finanzas import find, lines, peso_instruments

TEM_IN_COUPON = re.compile(r"(\d+(?:,\d+)?)\s*%")


def quarter(d: date) -> str:
    return f"{d.year}T{(d.month - 1) // 3 + 1}"


def capitalization_line(xlsx: Path) -> tuple[str, float]:
    """Label and amount (miles de millones de pesos) of the A.2.2 capitalization line."""
    for line in lines(xlsx, "A.2.2"):
        if line.label.lower().startswith("capitaliz"):
            return line.label, line.values[1] / 1e6
    raise KeyError(f"{xlsx}: no capitalization line in A.2.2")


@dataclass
class Reopenings:
    fixed: float = 0.0  # computed with the TEM of the placement
    proxy: float = 0.0  # effective value minus face (TAMAR, duals)
    rows_fixed: int = 0
    rows_proxy: int = 0
    rows_missing: int = 0


@dataclass(frozen=True)
class Discount:
    settle: date
    maturity: date
    amount: float  # technical value minus effective value; negative is a premium


def _as_date(v: object) -> date | None:
    return v.date() if isinstance(v, datetime) else None


def read_placements(workbooks: list[Path]) -> tuple[dict[str, Reopenings], list[Discount]]:
    out: dict[str, Reopenings] = defaultdict(Reopenings)
    discounts: list[Discount] = []
    for path in workbooks:
        wb = load_workbook(path, read_only=True, data_only=True)
        try:
            for sheet in wb.sheetnames:
                header: list[str] | None = None
                for row in wb[sheet].iter_rows(values_only=True):
                    cells = list(row)
                    if header is None:
                        if any(isinstance(c, str) and c.startswith("Nombre") for c in cells):
                            header = [str(c).split("\n")[0].strip() if c else "" for c in cells]
                        continue
                    _placement(dict(zip(header, cells, strict=False)), out, discounts)
        finally:
            wb.close()
    return out, discounts


def _field(rec: dict[str, object], prefix: str) -> object:
    return next((v for k, v in rec.items() if k.startswith(prefix)), None)


def _placement(
    rec: dict[str, object], out: dict[str, Reopenings], discounts: list[Discount]
) -> None:
    name = str(rec.get("Nombre del Instrumento") or "").upper()
    if "LECAP" not in name and "BONCAP" not in name:
        return
    issue = _as_date(rec.get("Fecha de emisión"))
    settle = _as_date(_field(rec, "Fecha coloc"))
    maturity = _as_date(rec.get("Vencimiento"))
    face = rec.get("Valor Nominal")
    cash = _field(rec, "Valor Efectivo")
    if issue is None or settle is None or not isinstance(face, int | float):
        return

    def discount(technical: float) -> None:
        if maturity is not None and maturity > settle and isinstance(cash, int | float):
            discounts.append(Discount(settle, maturity, (technical - cash) / 1e3))

    if settle <= issue:  # a new issue carries no capitalization
        discount(face)
        return
    r = out[quarter(settle)]
    match = TEM_IN_COUPON.search(str(_field(rec, "Cupón") or ""))
    if match and "TAMAR" not in name and "DUAL" not in name:
        tem = float(match.group(1).replace(",", ".")) / 100
        factor = (1 + tem) ** (year_fraction(issue, settle, "30E/360") * 12)
        r.fixed += face * (factor - 1) / 1e3
        r.rows_fixed += 1
        discount(face * factor)
        return
    value = cash
    if not isinstance(value, int | float):
        value = _field(rec, "Valor Técnico")
    if isinstance(value, int | float):
        r.proxy += max(0.0, value - face) / 1e3
        r.rows_proxy += 1
    else:
        r.rows_missing += 1


def accrue_discounts(discounts: list[Discount]) -> dict[str, float]:
    """Each discount spread evenly over the days from settlement to maturity, by quarter."""
    out: dict[str, float] = defaultdict(float)
    for d in discounts:
        days = (d.maturity - d.settle).days
        start = d.settle
        while start < d.maturity:
            first = (start.month - 1) // 3 * 3 + 4  # first month of the next quarter
            q_end = date(start.year, first, 1) if first <= 12 else date(start.year + 1, 1, 1)
            end = min(q_end, d.maturity)
            out[quarter(start)] += d.amount * (end - start).days / days
            start = end
    return out


# Categories of the FGS monthly report and the A.1.7 instruments that may sit in each:
# (category, capitalizing?) for an instrument, from its name and published rate.
FGS_LETRAS, FGS_FIJA, FGS_TAMAR = (
    "Letras, $",
    "Bonos, $, tasa fija",
    "Bonos, $, tasa variable (TAMAR)",
)


def _fgs_categories(name: str, rate: object) -> tuple[tuple[str, ...], bool]:
    n = name.upper()
    if n.startswith("LECAP"):
        return (FGS_LETRAS,), True
    if n.startswith("BONCAP DUAL"):
        return (FGS_FIJA, FGS_TAMAR), True
    if n.startswith("BONCAP"):
        return ((FGS_TAMAR,) if "TAMAR" in n else (FGS_FIJA,)), True
    if n.startswith("LE"):
        return (FGS_LETRAS,), False
    if "DLK" in n or "CER" in n:
        return (), False
    if isinstance(rate, int | float):
        return (FGS_FIJA,), False
    if "TAMAR" in str(rate).upper():
        return (FGS_TAMAR,), False
    return (), False


def fgs_share(xlsx: Path, fgs: dict[str, float]) -> tuple[float, float, float]:
    """Bounds of the FGS share of the capitalizing LECAP and BONCAP at a cut-off, and that
    stock (miles de millones de pesos). `fgs` maps category to holdings (same unit)."""
    iii = find(lines(xlsx, "A.1.1"), "III-").values
    ars_per_usd = iii[1] / iii[0]
    cap: dict[str, float] = defaultdict(float)
    other: dict[str, float] = defaultdict(float)
    total = 0.0
    for inst in peso_instruments(xlsx):
        cats, capitalizes = _fgs_categories(inst.name, inst.rate)
        ars = (
            inst.updated_usd_thousands * ars_per_usd / 1e6
        )  # thousands of pesos to miles de millones
        total += ars if capitalizes else 0.0
        for c in cats:
            (cap if capitalizes else other)[c] += ars
    cats = (FGS_LETRAS, FGS_FIJA, FGS_TAMAR)
    low = min(total, sum(min(cap[c], max(0.0, fgs.get(c, 0.0) - other[c])) for c in cats))
    high = min(total, sum(min(fgs.get(c, 0.0), cap[c]) for c in cats))
    return low / total, high / total, total


def read_fgs(path: Path) -> dict[date, dict[str, float]]:
    out: dict[date, dict[str, float]] = defaultdict(dict)
    if path.exists():
        with path.open(newline="", encoding="utf-8") as fh:
            for r in csv.DictReader(fh):
                out[date.fromisoformat(r["fecha"])][r["categoria"]] = float(r["millones_ars"]) / 1e3
    return out


def spn_quarterly(series_csv: Path) -> dict[str, dict[str, float]]:
    out: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    months: dict[str, set[str]] = defaultdict(set)
    with series_csv.open(newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            d = date.fromisoformat(r["fecha"])
            q = quarter(d)
            out[q][r["series_id"]] += float(r["valor"]) / 1e3
            months[q].add(r["fecha"][:7])
    for q, ms in months.items():
        out[q]["meses"] = len(ms)
    return out


def build_accrual_table(
    quarterly: list[tuple[date, Path]],
    placements: list[Path],
    spn_csv: Path,
    out: Path,
    fgs_csv: Path | None = None,
) -> list[dict[str, object]]:
    reopenings, discounts = read_placements(placements)
    accrued_discount = accrue_discounts(discounts)
    spn = spn_quarterly(spn_csv)
    fgs = read_fgs(fgs_csv) if fgs_csv else {}
    rows = []
    for cutoff, xlsx in sorted(quarterly):
        q = quarter(cutoff)
        label, cap = capitalization_line(xlsx)
        reo = reopenings.get(q, Reopenings())
        accrued = cap - reo.fixed - reo.proxy
        discount = accrued_discount.get(q, 0.0)
        fiscal = spn.get(q, {})
        complete = fiscal.get("meses") == 3
        financial = fiscal.get("spn_caja_resultado_financiero") if complete else None
        low = high = None
        if cutoff in fgs:
            low, high, _ = fgs_share(xlsx, fgs[cutoff])
        total = accrued + discount
        spn_low, spn_high = _outside(total, high), _outside(total, low)
        rows.append(
            {
                "trimestre": q,
                "capitalizacion_a22": round(cap, 1),
                "capitalizacion_en_ampliaciones_tasa_fija": round(reo.fixed, 1),
                "capitalizacion_en_ampliaciones_aproximada": round(reo.proxy, 1),
                "filas_sin_dato": reo.rows_missing,
                "interes_capitalizado_devengado": round(accrued, 1),
                "descuento_colocacion_devengado": round(discount, 1),
                "devengado_no_pagado_ac": round(total, 1),
                "fgs_participacion_min_pct": None if low is None else round(100 * low, 1),
                "fgs_participacion_max_pct": None if high is None else round(100 * high, 1),
                # the larger FGS share leaves the smaller cost to the SPN
                "devengado_no_pagado_spn_min": spn_low,
                "devengado_no_pagado_spn_max": spn_high,
                "spn_resultado_primario_caja": _r(
                    fiscal.get("spn_caja_resultado_primario"), complete
                ),
                "spn_intereses_netos_caja": _r(fiscal.get("spn_caja_intereses_netos"), complete),
                "spn_resultado_financiero_caja": _r(financial, True),
                "resultado_financiero_con_capitalizado": _minus(financial, accrued),
                "resultado_financiero_con_devengado_ac": _minus(financial, total),
                "resultado_financiero_con_devengado_spn_min": _minus(financial, spn_high),
                "resultado_financiero_con_devengado_spn_max": _minus(financial, spn_low),
                "rotulo_a22": label,
            }
        )
    _write(out / "devengados_trimestral.csv", rows)
    return rows


def _outside(total: float, fgs_share: float | None) -> float | None:
    """The part of the accrued cost not owed to the FGS."""
    return None if fgs_share is None else round(total * (1 - fgs_share), 1)


def _minus(result: float | None, cost: float | None) -> float | None:
    return None if result is None or cost is None else round(result - cost, 1)


def _r(v: float | None, ok: bool) -> float | None:
    return round(v, 1) if ok and v is not None else None
