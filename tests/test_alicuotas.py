from __future__ import annotations

from datetime import date

from argfx.simulation.alicuotas import (
    Event,
    RateBook,
    crude_rate,
    industrial_phase_out,
    positions_in,
    rates_from_annex,
)

ANNEX = """
  NCM        REFERENCIA      Alícuota
1206.00.90   Las demas con mas de 15% de embolsado    7%
1206.00.90   Tipo confitería en envases                5%
1001.99.00                  12%
1001.19.00    5,50
1206.00.10   (5) (6)   0%
7408.29.19   Alambre de cobre
             refinado                     4,5%
"""


def test_annex_rates_take_the_rate_column_and_flag_partial_listings() -> None:
    rates, partial = rates_from_annex(ANNEX)
    assert rates == {"1206.00.90": 7.0, "1001.99.00": 12.0, "1001.19.00": 5.5,
                     "1206.00.10": 0.0, "7408.29.19": 4.5}  # fmt: skip
    assert partial == {"1206.00.10"}
    assert positions_in("2502.00.00  2809.20.20\n2817.00.10") == {
        "2502.00.00", "2809.20.20", "2817.00.10"}  # fmt: skip


def test_temporary_events_end_and_the_previous_rate_returns() -> None:
    book = RateBook([
        Event(date(2020, 3, 5), None, {"1201.90.00": 33.0}, "base", "S1"),
        Event(date(2025, 1, 28), date(2025, 6, 30), {"1201.90.00": 26.0}, "temporario", "S2"),
    ])  # fmt: skip
    assert book.rate("1201.90.00", date(2025, 3, 1)) == (26.0, "temporario")
    assert book.rate("1201.90.00", date(2025, 7, 1)) == (33.0, "base")
    assert book.rate("9999.99.99", date(2025, 7, 1)) is None


def test_industrial_phase_out_only_touches_positions_at_4_5_or_3_outside_food() -> None:
    base = RateBook([Event(date(2021, 1, 1), None, {"8703.23.10": 4.5, "7601.10.00": 3.0,
                    "1001.99.00": 3.0, "2709.00.10": 8.0}, "1060", "S")])  # fmt: skip
    events = industrial_phase_out(base, [(date(2026, 7, 1), 4.125, 2.75)])
    assert events[0].rates == {"8703.23.10": 4.125, "7601.10.00": 2.75}


def test_crude_rate_is_linear_between_the_reference_values() -> None:
    assert crude_rate(40) == 0.0 and crude_rate(70) == 8.0 and crude_rate(52.5) == 4.0
    assert crude_rate(72.5, vb=65, vr=80) == 4.0
