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
