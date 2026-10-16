from __future__ import annotations

import csv
from datetime import date
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


def test_consolidation_splits_public_holdings_by_method_and_law(tmp_path: Path) -> None:
    from datetime import date

    from argfx.contracts.terms import TERM_FILES
    from argfx.reconcile.consolidacion import build_consolidation

    repo = Path(__file__).resolve().parent.parent / "contratos"
    terms = tmp_path / "contratos"
    terms.mkdir()
    for name in TERM_FILES:  # headers only: no term sheets, every bond is bullet
        header = (repo / name).read_text(encoding="utf-8").splitlines()[0]
        (terms / name).write_text(header + "\n", encoding="utf-8")

    def write(name: str, rows: list[list[object]]) -> Path:
        p = tmp_path / name
        with p.open("w", newline="", encoding="utf-8") as fh:
            csv.writer(fh).writerows(rows)
        return p

    comp = write("comp.csv", [
        ["partida", "millones_usd", "porcentaje", "source_id", "referencia"],
        ["agencias_sector_publico", 100, "", "SRC-0001", "x"],
        ["sector_publico_moneda_total", 100, "", "SRC-0001", "x"],
        ["sector_publico_dolares", "", 60, "SRC-0001", "x"],
        ["sector_publico_legislacion_extranjera", "", 10, "SRC-0001", "x"],
    ])  # fmt: skip
    holdings = write("ten.csv", [
        ["instrument_id", "tenedor", "valor_nominal_original_usd", "metodo", "fecha_dato",
         "source_id", "referencia"],
        ["INS-C-0001", "BCRA", 30e6, "directo", "2026-06-30", "SRC-0001", "x"],
        ["INS-C-0003", "BCRA", 5e6, "estimado", "2026-06-30", "SRC-0001", "x"],
    ])  # fmt: skip
    inst = write("inst.csv", [
        ["instrument_id", "instrument_family", "operation_name_sigade",
         "outstanding_usd_equiv_sigade"],
        ["INS-C-0001", "USD", "LETRA/U$S/BCRA", 30e6],
        ["INS-C-0002", "USD", "BONO GLOBAL/U$S/2030", 50e6],
        ["INS-C-0003", "USD", "BONO R.A./U$S/2030", 40e6],
        ["INS-C-0004", "multilateral", "BID", 20e6],
    ])  # fmt: skip
    head = ["instrument_id", "date", "base", "is_payment", "status", "currency_of_settlement",
            "monto_usd"]  # fmt: skip
    flows = write("flujos.csv", [head] + [
        [iid, "2026-07-09", "True", "True", "firme", "USD", 10e6]
        for iid in ("INS-C-0001", "INS-C-0002", "INS-C-0003", "INS-C-0004")
    ])  # fmt: skip
    out = tmp_path / "out"
    t = build_consolidation(comp, holdings, inst, flows, terms, date(2026, 6, 30), out)
    # Public USD 60: identified 30 (direct) + 5 (estimated); foreign law 10 goes to the
    # Global (10/50 = 20%); the remaining 15 to the free part of the local bond (15/35).
    assert t["bruta_musd"] == 40.0
    assert t["sector_publico_directo_musd"] == 10.0
    assert t["sector_publico_estimado_musd"] == 1.2  # 10 x 5/40, rounded
    assert t["proporcion_ley_extranjera_pct"] == 20.0
    assert t["proporcion_ley_nacional_pct"] == 42.86
    assert t["consolidada_musd"] == 23.0  # 40 - 10 - 1.25 - 2 - 3.75
    with (out / "necesidad_divisas_consolidada.csv").open(encoding="utf-8") as fh:
        rows = {r["instrument_id"]: r for r in csv.DictReader(fh)}
    assert float(rows["INS-C-0004"]["consolidada_musd"]) == 10.0
    assert float(rows["INS-C-0002"]["sector_publico_proporcional_musd"]) == 2.0
    assert float(rows["INS-C-0003"]["sector_publico_proporcional_musd"]) == 3.75


def test_capitalized_interest_accrued_nets_out_reopenings(tmp_path: Path) -> None:
    from datetime import datetime

    from argfx.reconcile.devengados import build_accrual_table

    fin = Workbook()
    a22 = fin.active
    a22.title = "A.2.2"
    a22.append(["Capitalización de Bonos, Letras y otros préstamos (*)", 1.0, 5e9])  # miles de $
    a11 = fin.create_sheet("A.1.1")
    a11.append(["III- DEUDA EN SITUACIÓN DE PAGO NORMAL", 1.0, 1000.0])  # 1.000 pesos per USD
    a17 = fin.create_sheet("A.1.7")
    a17.append(["Fecha de emisión", "Denominación", "Tasa vigente", "Vencimiento",
                "Valor nominal original en circulación",
                "Valor nominal residual en circulación (1)",
                "Valor nominal actualizado en circulación (2)"])  # fmt: skip
    a17.append(["LETRAS DEL TESORO", None, None, None, 9.0, 9.0, 9.0])  # subtotal: skipped
    for name, rate, usd_thousands in [
        ("LECAP/$/2,00%/30-06-2026 (4)", 0.02, 4e6),  # 4.000 miles de millones de pesos
        ("BONCAP/$/TAMAR+5%/31-08-2026", "Tamar + 5,00%", 4e6),
        ("LELINKS/DLK/31-07-2026 (3)", "Tasa Cero", 1e6),
        ("BONTE/$/29,50%/30-05-2030", 0.295, 2e6),
    ]:
        a17.append([datetime(2026, 1, 1), name, rate, 2026, 1.0, 1.0, usd_thousands])
    fin_path = tmp_path / "fin.xlsx"
    fin.save(fin_path)  # 5.000 miles de millones of capitalization in the quarter

    oncp = Workbook()
    letras = oncp.active
    letras.title = "Letras"
    letras.append(["Nombre del Instrumento", "Fecha de emisión", "Vencimiento", "Cupón",
                   "Amortización", "Tipo Moneda", "Moneda de Origen",
                   "Fecha colocación/liquidación", "Valor Nominal", "Valor Efectivo"])  # fmt: skip
    letras.append(["LECAP/$/30-06-2026", datetime(2026, 1, 30), datetime(2026, 6, 30),
                   "Tasa efectiva mensual capitalizable 2%", "Íntegra", "MN", "ARP",
                   datetime(2026, 1, 30), 1_000_000.0, 1_000_000.0])  # new issue  # fmt: skip
    letras.append(["LECAP/$/30-06-2026", datetime(2026, 1, 30), datetime(2026, 6, 30),
                   "Tasa efectiva mensual capitalizable 2%", "Íntegra", "MN", "ARP",
                   datetime(2026, 4, 30), 1_000_000.0, 1_080_000.0])  # 3 months later  # fmt: skip
    letras.append(["LECAP/$/TAMAR+5%/31-08-2026", datetime(2026, 1, 15), datetime(2026, 8, 31),
                   "Tasa efectiva mensual “TAMAR TEM”", "Íntegra", "MN", "ARP",
                   datetime(2026, 5, 15), 100_000.0, 110_000.0])  # fmt: skip
    oncp_path = tmp_path / "oncp.xlsx"
    oncp.save(oncp_path)

    spn = tmp_path / "spn.csv"
    with spn.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["series_id", "fecha", "valor", "unidad", "source_id"])
        for m in ("2026-04-30", "2026-05-31", "2026-06-30"):
            w.writerow(["spn_caja_resultado_financiero", m, 100_000.0, "millones", "SRC-0001"])
    fgs = tmp_path / "fgs.csv"
    with fgs.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["fecha", "categoria", "millones_ars", "source_id", "referencia"])
        w.writerow(["2026-06-30", "Letras, $", 1_600_000, "SRC-0001", "x"])  # 1.600 mm
        w.writerow(["2026-06-30", "Bonos, $, tasa fija", 2_400_000, "SRC-0001", "x"])
        w.writerow(["2026-06-30", "Bonos, $, tasa variable (TAMAR)", 800_000, "SRC-0001", "x"])
    (row,) = build_accrual_table([(date(2026, 6, 30), fin_path)], [oncp_path], spn, tmp_path, fgs)
    carried = 1_000_000.0 * (1.02**3 - 1) / 1e3  # 61,208 miles de millones
    assert row["trimestre"] == "2026T2"
    assert row["capitalizacion_en_ampliaciones_tasa_fija"] == round(carried, 1)
    assert row["capitalizacion_en_ampliaciones_aproximada"] == 10.0
    accrued = 5000.0 - carried - 10.0
    assert row["interes_capitalizado_devengado"] == round(accrued, 1)
    assert row["spn_resultado_financiero_caja"] == 300.0
    assert row["resultado_financiero_con_capitalizado"] == round(300.0 - accrued, 1)
    # The reopening paid 1.080.000 for a technical value of 1.061.208: a premium, accrued
    # between settlement and maturity, all inside the quarter. The new issue was at face.
    premium = (1_080_000.0 - 1_000_000.0 * 1.02**3) / 1e3
    assert row["descuento_colocacion_devengado"] == round(-premium, 1)
    total = accrued - premium
    # FGS over 8.000 of LECAP and BONCAP. Letters 1.600: at least 600 beyond the LELINKs (1.000),
    # at most 1.600. Fixed-rate bonds 2.400: none, since no fixed-rate bond capitalizes here
    # (what exceeds the BONTE belongs to bonds outside A.1.7). TAMAR 800: all of it.
    assert (row["fgs_participacion_min_pct"], row["fgs_participacion_max_pct"]) == (17.5, 30.0)
    assert row["devengado_no_pagado_spn_min"] == round(total * (1 - 2400 / 8000), 1)
    assert row["devengado_no_pagado_spn_max"] == round(total * (1 - 1400 / 8000), 1)


def test_discounts_accrue_by_days_across_quarters() -> None:
    from argfx.reconcile.devengados import Discount, accrue_discounts

    out = accrue_discounts([Discount(date(2026, 3, 1), date(2026, 4, 30), 60.0)])
    assert round(out["2026T1"], 6) == round(60.0 * 31 / 60, 6)  # 1 Mar to 1 Apr
    assert round(out["2026T2"], 6) == round(60.0 * 29 / 60, 6)
    out = accrue_discounts([Discount(date(2026, 12, 15), date(2027, 1, 14), 30.0)])
    assert out == {"2026T4": 17.0, "2027T1": 13.0}


def test_peso_consolidation_applies_official_shares_and_converts_holdings(tmp_path: Path) -> None:
    from argfx.reconcile.pesos import build_peso_consolidation

    def write(name: str, rows: list[list[object]]) -> Path:
        p = tmp_path / name
        with p.open("w", newline="", encoding="utf-8") as fh:
            csv.writer(fh).writerows(rows)
        return p

    comp = write("comp.csv", [
        ["partida", "millones_usd", "porcentaje", "source_id", "referencia"],
        ["sector_publico_moneda_total", 100, "", "SRC-0001", "x"],
        ["sector_publico_pesos_cer", "", 40, "SRC-0001", "x"],
        ["sector_publico_pesos", "", 20, "SRC-0001", "x"],
        ["sector_publico_dolar_linked", "", 0, "SRC-0001", "x"],
    ])  # fmt: skip
    inst = write("inst.csv", [
        ["instrument_id", "instrument_family", "outstanding_usd_equiv_sigade"],
        ["A", "ARS CER", 50e6],
        ["B", "ARS nominal", 30e6],
        ["C", "dual", 10e6],
        ["D", "dólar-linked", 5e6],
        ["E", "USD", 99e6],  # not payable in pesos
    ])  # fmt: skip
    holdings = write("ten.csv", [
        ["tenedor", "categoria", "millones_ars", "valuacion", "source_id", "referencia"],
        ["BCRA", "x", 30_000, "contable", "SRC-0001", "x"],
        ["FGS", "x", 15_000, "mercado", "SRC-0001", "x"],
        ["FGS", "y", 5_000, "mercado", "SRC-0001", "x"],
    ])  # fmt: skip
    t = build_peso_consolidation(comp, holdings, inst, 1000.0, tmp_path)
    assert t == {
        "pesos_bruta_musd": 95.0,
        "pesos_sector_publico_oficial_musd": 60.0,
        "pesos_sector_publico_pct": 63.2,
        "pesos_identificado_musd": 50.0,
    }
    with (tmp_path / "pesos_sector_publico.csv").open(encoding="utf-8") as fh:
        rows = {r["grupo"]: r for r in csv.DictReader(fh)}
    assert float(rows["cer"]["sector_publico_pct"]) == 80.0
    assert float(rows["pesos"]["en_otras_manos_musd"]) == 20.0
