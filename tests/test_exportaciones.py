from __future__ import annotations

import zipfile
from datetime import date
from pathlib import Path

from argfx.simulation.alicuotas import Event, RateBook
from argfx.simulation.exportaciones import build_duty_table, estimate, group_of, read_month

LST = """FECHA_'POS_NCM   'UN'PESO_NETO_KILOS'MONTO_FOB_DOLAR'CANT_DECLARACIONES
------'----------'--'---------------'---------------'------------------
202606'1201.90.00'01'     1000.0'     2000000.00'      3
202606'2709.00.10'01'     1000.0'     1000000.00'      1
202606'8703.23.10'01'      100.0'      500000.00'      2
202606'9999.99.99'01'      100.0'      100000.00'      1
"""


def test_reads_the_export_member_and_estimates_by_position(tmp_path: Path) -> None:
    z = tmp_path / "202606.zip"
    with zipfile.ZipFile(z, "w") as zf:
        zf.writestr("impo_202606.lst", "ignored")
        zf.writestr("total_expo_agregado_202606.lst", LST)
    month, fob = read_month(z)
    assert month == "2026-06" and fob["1201.90.00"] == 2_000_000.0
    book = RateBook([Event(date(2025, 12, 12), None, {"1201.90.00": 24.0, "8703.23.10": 4.5},
                           "x", "S")])  # fmt: skip
    e = estimate(month, fob, book)
    assert e.duty_usd == 2_000_000 * 0.24 + 500_000 * 0.045
    assert e.fob_with_rate_usd == 2_500_000  # crude and the unknown position have no rate here
    assert group_of("1201.90.00") == "soja" and group_of("2304.00.10") == "soja"
    assert group_of("8703.23.10") == "otros"
    (row,) = build_duty_table([(month, fob)], book, {"2026-06": 70.0}, {"2026-06": 1.0}, tmp_path)
    # Crude at a price of 70 pays the top 8%: 80.000 USD more.
    assert row["derecho_estimado_musd"] == round((480_000 + 22_500 + 80_000) / 1e6, 1)
    assert row["fob_con_alicuota_musd"] == 3.5


def test_reads_members_nested_in_a_month_folder(tmp_path: Path) -> None:
    z = tmp_path / "201712.zip"
    with zipfile.ZipFile(z, "w") as zf:
        zf.writestr("202606/impo_agregado_2026_06.lst", "ignored")
        zf.writestr("202606/total_expo_agregado_2026_06.lst", LST)
    assert read_month(z)[1]["1201.90.00"] == 2_000_000.0


def test_fuels_follow_the_crude_formula_with_the_566_top(tmp_path: Path) -> None:
    from argfx.simulation.alicuotas import formula_top

    assert formula_top("2710.12.10", "2026-06") == 8.0
    assert round(formula_top("2710.12.10", "2026-07"), 4) == 7.3333
    assert formula_top("2710.12.10", "2027-06") == 0.0
    assert formula_top("2711.11.00", "2026-09") == 8.0  # gas keeps the 8% top
    fob = {"2710.12.10": 100e6, "2711.11.00": 100e6}
    (row,) = build_duty_table([("2026-09", fob)], RateBook([]), {"2026-09": 70.0}, {}, tmp_path)
    assert row["derecho_estimado_musd"] == 6.0 + 8.0  # September top is 6%
    assert row["fob_con_alicuota_musd"] == 200.0
