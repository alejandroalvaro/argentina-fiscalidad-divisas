from __future__ import annotations

import csv
from pathlib import Path

from openpyxl import Workbook

from argfx.reconcile.conciliacion import Materiality, flow_identities, stock_controls
from argfx.reconcile.finanzas import find, lines, maturity_profile


def workbook(path: Path) -> Path:
    wb = Workbook()
    a11 = wb.active
    a11.title = "A.1.1"
    a11.append(["Indice"])
    a11.append(["III- DEUDA EN SITUACIÓN DE PAGO NORMAL", 1000.0, 1_480_000.0])
    a11.append(["    ORGANISMOS INTERNACIONALES", 300.0, 444_000.0])
    a11.append(["    ADELANTOS TRANSITORIOS BCRA", 0, 0])
    a11.append(["    ADELANTOS TRANSITORIOS BCRA", 50.0, 74_000.0])
    a22 = wb.create_sheet("A.2.2")
    for label, value in [
        ("I - DEUDA BRUTA", 900.0), ("II - DEUDA ELEGIBLE", 20.0), ("1 - Financiamiento", 300.0),
        ("2 - Amortizaciones", 250.0), ("a) Operaciones", 50.0), ("b) Avales", -5.0),
        ("c) Letras", 0.0), ("d) Ajustes", 35.0), ("e) Ajustes", 0.0),
        ("IV - TOTAL VARIACIONES", 80.0), ("V - DEUDA BRUTA", 1000.0),
        ("VI - DEUDA ELEGIBLE", 20.0), ("VII - DEUDA BRUTA", 980.0),
    ]:  # fmt: skip
        a22.append([label, value, value * 1480])
    a31 = wb.create_sheet("A.3.1")
    a31.append([2026, 2027, "Total"])
    a31.append(["Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre", "Subtotal",
                "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Subtotal"])  # fmt: skip
    a31.append([" TÍTULOS PÚBLICOS", *[10.0] * 6, 60.0, *[20.0] * 6, 120.0, 180.0])
    a31.append(["    CAPITAL", *[8.0] * 6, 48.0, *[15.0] * 6, 90.0, 138.0])
    a31.append(["    INTERÉS", *[2.0] * 6, 12.0, *[5.0] * 6, 30.0, 42.0])
    a31.append([" TOTAL", *[10.0] * 6, 60.0, *[20.0] * 6, 120.0, 180.0])
    out = path / "finanzas.xlsx"
    wb.save(out)
    return out


def test_finanzas_reader_and_profile(tmp_path: Path) -> None:
    x = workbook(tmp_path)
    assert find(lines(x, "A.1.1"), "III-").values == (1000.0, 1_480_000.0)
    prof = maturity_profile(x)
    cap = {r.month: r.usd_thousands for r in prof if r.group == "TÍTULOS PÚBLICOS"
           and r.concept == "capital"}  # fmt: skip
    assert len(cap) == 12 and cap["2026-07"] == 8.0 and cap["2027-06"] == 15.0
    assert {r.group for r in prof} == {"TÍTULOS PÚBLICOS", "TOTAL"}


def test_stock_and_flow_controls(tmp_path: Path) -> None:
    x = workbook(tmp_path)
    inst = tmp_path / "instruments.csv"
    with inst.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["instrument_id", "instrument_family", "outstanding_usd_equiv_sigade"])
        w.writerow(["INS-C-0001", "multilateral", 300_000.0])
        w.writerow(["INS-C-0002", "USD", 650_000.0])
        w.writerow(["INS-C-0003", "adelantos transitorios BCRA (intra sector público)", 49_000.0])
    m = Materiality(abs_musd=0.5, rel=0.0)
    stock = {r["partida"][:20]: r for r in stock_controls(lines(x, "A.1.1"), inst, m)}
    assert not stock["Deuda en situación d"]["material"]
    adv = stock["Adelantos transitori"]
    assert adv["diferencia_musd"] == -0.001 and not adv["material"]
    flows = flow_identities(lines(x, "A.2.2"), m)
    assert [r["material"] for r in flows] == [False, False, False, False]
