from __future__ import annotations

from dataclasses import replace
from datetime import date, timedelta
from pathlib import Path

import pytest

from argfx.contracts.calendar import add_observed_history, read_series
from argfx.contracts.engine import FloatingRate, TermSheet, ZeroRate, generate
from argfx.contracts.habiles import BusinessCalendar, easter, read_extra_holidays, rule_holidays
from argfx.contracts.model import Obligation
from argfx.contracts.scenario import Scenario, value_flow
from argfx.contracts.schedule import add_months, regular_dates

SERIES = Path(__file__).resolve().parent.parent / "series"
CUTOFF = date(2026, 6, 30)


def observed() -> BusinessCalendar:
    return BusinessCalendar.from_series(
        SERIES / "bcra_a3500.csv", read_extra_holidays(SERIES / "feriados_decretados.csv")
    )


def test_rules_of_ley_27399() -> None:
    assert easter(2026) == date(2026, 4, 5) and easter(2027) == date(2027, 3, 28)
    h = rule_holidays(2027)
    assert {date(2027, 2, 8), date(2027, 2, 9), date(2027, 3, 25), date(2027, 3, 26)} <= h
    # 17-06-2027 is a Thursday: moves to Monday 21; 20-11-2027 is a Saturday: stays.
    assert date(2027, 6, 21) in h and date(2027, 6, 17) not in h
    assert date(2027, 11, 6) in h and date(2027, 12, 24) in h


def test_rules_never_call_an_observed_business_day_a_holiday() -> None:
    # Past the observed data the rules project; on 2024-2026 they miss only decreed days.
    cal, rules = observed(), BusinessCalendar()
    d = date(2024, 1, 2)
    while d <= date(2026, 10, 14):
        assert not (cal.is_business(d) and not rules.is_business(d)), d
        d += timedelta(days=1)


def test_tenth_business_day_before() -> None:
    cal = observed()
    assert cal.shift(date(2026, 6, 12), 10) == date(2026, 5, 29)  # 25-05 holiday
    assert cal.shift(date(2026, 4, 30), 10) == date(2026, 4, 16)
    # After the observed data: 07-12 decreed non-working (SRC-1903), 08-12 holiday.
    assert cal.shift(date(2026, 12, 9), 1) == date(2026, 12, 4)
    assert BusinessCalendar().shift(date(2026, 12, 9), 1) == date(2026, 12, 7)


def cer_bond(units: float, issue: date, maturity: date, cal: BusinessCalendar) -> TermSheet:
    ob = Obligation(
        instrument_id="INS-C-0001", name="t", debtor="Tesoro", creditor_type="desconocido",
        holder_residency="desconocida", currency_of_account="ARS", indexation="CER",
        currency_of_settlement="ARS",
    )  # fmt: skip
    return TermSheet(
        obligation=ob, as_of=CUTOFF, outstanding=units, period_dates=(maturity,),
        accrual_start=issue, day_count="30/360", rate=ZeroRate(),
        amortization=((maturity, 1.0),), index_lag_days=10, calendar=cal,
    )  # fmt: skip


def test_cer_lag_pays_face_times_the_ratio_of_lagged_indices() -> None:
    # 1000 pesos of face issued 2026-06-12: SIGADE keeps 1000 / CER(issue) units; the norm pays
    # 1000 x CER(maturity - 10 business days) / CER(issue - 10 business days).
    cal = observed()
    cer = dict(read_series(SERIES / "bcra_cer.csv"))
    issue, maturity = date(2026, 6, 12), date(2026, 10, 9)
    units = 1000 / cer[issue]
    rebase = cer[issue] / cer[date(2026, 5, 29)]
    ts = cer_bond(units * rebase, issue, maturity, cal)
    s = Scenario("s", "observado")
    s.set_path("CER", read_series(SERIES / "bcra_cer.csv"))
    (flow,) = generate(ts, s)
    lagged = cal.shift(maturity, 10)
    assert flow.index_date == lagged == date(2026, 9, 25)
    paid = value_flow(flow, s).amount_settlement
    assert paid == pytest.approx(1000 * cer[lagged] / cer[date(2026, 5, 29)])


def test_lagged_tamar_window_is_a_simple_mean_of_business_days() -> None:
    cal = observed()
    issue, maturity = date(2026, 4, 30), date(2026, 8, 31)
    ts = TermSheet(
        obligation=Obligation(
            instrument_id="INS-C-0001", name="t", debtor="Tesoro", creditor_type="desconocido",
            holder_residency="desconocida", currency_of_account="ARS", indexation="ninguna",
            currency_of_settlement="ARS",
        ),
        as_of=CUTOFF, outstanding=1000.0, outstanding_is_face=True,
        period_dates=tuple(regular_dates(add_months(issue, 1), maturity, 1, final_stub=True)),
        accrual_start=issue, day_count="30/360",
        rate=FloatingRate("TAMAR", 0.069, tem_days=32, whole_term=True, lag_days=10),
        capitalizes=True, frequency_months=1, amortization=((maturity, 1.0),), calendar=cal,
    )  # fmt: skip
    tamar = [(d, v) for d, v in read_series(SERIES / "bcra_tamar.csv", 0.01)]
    s = Scenario("s", "observado")
    s.set_path("TAMAR", tamar)
    a, b = cal.shift(issue, 10), cal.shift(maturity, 10)
    window = [v for d, v in tamar if a <= d <= b]
    n = 365 / 32
    tem = (1 + (sum(window) / len(window) + 0.069) / n) ** (n / 12) - 1
    paid = [f for f in generate(ts, s) if f.is_payment]
    assert paid[0].amount == pytest.approx(1000 * (1 + tem) ** 4)
    # Without the lag the window and the weights change.
    no_lag = replace(ts, rate=replace(ts.rate, lag_days=0))
    assert next(f for f in generate(no_lag, s) if f.is_payment).amount != pytest.approx(
        paid[0].amount, rel=1e-6
    )


def test_observed_history_does_not_project_tamar() -> None:
    s = Scenario("s", "congelado")
    s.set_path("CER", [(CUTOFF, 799.2033)])
    add_observed_history(s, SERIES, CUTOFF)
    assert s.value("CER", date(2026, 6, 15)) is not None
    assert s.value("CER", date(2030, 1, 1)) == 799.2033
    assert s.value("TAMAR", CUTOFF) is not None
    assert s.value("TAMAR", date(2026, 7, 1)) is None
    assert s.average("TAMAR", date(2026, 6, 1), date(2026, 7, 15)) is None


def test_actual_over_the_year_of_the_period_start() -> None:
    from argfx.contracts.daycount import year_fraction

    # A period from November 2024 into 2025 counts over 366 days, without splitting.
    assert year_fraction(date(2024, 11, 17), date(2025, 2, 17), "ACT/ACT_INICIO") == 92 / 366
    assert year_fraction(date(2025, 11, 17), date(2026, 2, 17), "ACT/ACT_INICIO") == 92 / 365


def test_dollar_linked_settles_at_the_a3500_of_three_business_days_before() -> None:
    # D30S6 paid on 2026-09-30 with the A 3500 of 2026-09-25 (payment notice, lote O).
    cal = observed()
    ob = Obligation(
        instrument_id="INS-C-0627", name="t", debtor="Tesoro", creditor_type="desconocido",
        holder_residency="desconocida", currency_of_account="USD", indexation="dolar_linked",
        currency_of_settlement="ARS",
    )  # fmt: skip
    pay = date(2026, 9, 30)
    ts = TermSheet(
        obligation=ob, as_of=CUTOFF, outstanding=1.0, period_dates=(pay,), accrual_start=CUTOFF,
        day_count="30/360", rate=ZeroRate(), amortization=((pay, 1.0),), index_lag_days=3,
        calendar=cal,
    )  # fmt: skip
    s = Scenario("s", "observado")
    s.set_path("FX:ARS", read_series(SERIES / "bcra_a3500.csv"))
    (flow,) = generate(ts, s)
    assert flow.index_date == date(2026, 9, 25)
    v = value_flow(flow, s)
    assert v.amount_usd == 1.0
    assert v.amount_settlement == pytest.approx(1523.9662, abs=1e-4)
