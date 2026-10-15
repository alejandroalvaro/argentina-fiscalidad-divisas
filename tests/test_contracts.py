from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

import pytest

from argfx.contracts.buckets import aggregate, bucket
from argfx.contracts.daycount import year_fraction
from argfx.contracts.engine import FixedRate, FloatingRate, TermSheet, ZeroRate, generate
from argfx.contracts.model import CashFlow, Obligation
from argfx.contracts.options import dual_max
from argfx.contracts.scenario import Scenario, value_flow
from argfx.contracts.schedule import add_months, regular_dates
from argfx.contracts.sigade import load_sigade_flows, read_instrument_index
from argfx.contracts.terms import TERM_FILES, load_term_sheets, merge_term_folders

CUTOFF = date(2026, 6, 30)


def obligation(**kw: object) -> Obligation:
    base = dict(
        instrument_id="INS-C-0001", name="test", debtor="Tesoro", creditor_type="desconocido",
        holder_residency="desconocida", currency_of_account="USD", indexation="ninguna",
        currency_of_settlement="USD",
    )  # fmt: skip
    return Obligation(**{**base, **kw})  # type: ignore[arg-type]


def semiannual(first: date, last: date) -> tuple[date, ...]:
    return tuple(regular_dates(first, last, 6))


# Global 2030 (GD30) at the 2026-06-30 cut-off, as SIGADE projects it (SRC-0102).
GD30_BALANCE = 9_782_950_290.48
GD30_SIGADE_INTEREST = {
    date(2026, 7, 9): 36_686_063.58929999,
    date(2027, 1, 9): 32_609_834.3016,
    date(2027, 7, 9): 28_533_605.0139,
    date(2028, 1, 9): 57_067_210.02779999,
    date(2028, 7, 9): 47_556_008.35650001,
    date(2029, 1, 9): 38_044_806.6852,
    date(2029, 7, 9): 28_533_605.0139,
    date(2030, 1, 9): 19_022_403.3426,
    date(2030, 7, 9): 9_511_201.6713,
}


def gd30() -> TermSheet:
    dates = semiannual(date(2021, 7, 9), date(2030, 7, 9))
    amort = [(date(2024, 7, 9), 0.04)] + [(d, 0.08) for d in dates if d > date(2024, 7, 9)]
    return TermSheet(
        obligation=obligation(instrument_id="INS-C-0398"),
        as_of=CUTOFF, outstanding=GD30_BALANCE, period_dates=dates,
        accrual_start=date(2020, 9, 4), day_count="30/360",
        rate=FixedRate(((date(2020, 9, 4), 0.00125), (date(2021, 7, 9), 0.005),
                        (date(2023, 7, 9), 0.0075), (date(2027, 7, 9), 0.0175))),
        amortization=tuple(amort),
    )  # fmt: skip


def test_day_counts() -> None:
    assert year_fraction(date(2026, 1, 9), date(2026, 7, 9), "30/360") == 0.5
    assert year_fraction(date(2026, 1, 31), date(2026, 3, 31), "30/360") == 60 / 360
    assert year_fraction(date(2026, 1, 1), date(2027, 1, 1), "ACT/365") == 1.0
    # ISDA splits by calendar year: 184 days of 2027 over 365, 182 days of 2028 over 366.
    expected = 184 / 365 + 182 / 366
    assert year_fraction(date(2027, 7, 1), date(2028, 7, 1), "ACT/ACT") == pytest.approx(expected)


def test_schedule() -> None:
    assert add_months(date(2026, 1, 31), 1) == date(2026, 2, 28)
    assert add_months(date(2026, 2, 28), 1, eom=True) == date(2026, 3, 31)
    assert len(semiannual(date(2021, 7, 9), date(2030, 7, 9))) == 19
    with pytest.raises(ValueError):
        regular_dates(date(2021, 7, 9), date(2030, 7, 10), 6)


def test_gd30_reproduces_sigade() -> None:
    flows = generate(gd30())
    interest = {f.date: f.amount for f in flows if f.flow_type == "interes"}
    principal = [f.amount for f in flows if f.flow_type == "amortizacion"]
    assert interest.keys() == GD30_SIGADE_INTEREST.keys()
    for d, expected in GD30_SIGADE_INTEREST.items():
        assert interest[d] == pytest.approx(expected, abs=1e-6)
    assert principal == pytest.approx([1_086_994_476.72] * 9, abs=1e-6)
    assert sum(principal) == pytest.approx(GD30_BALANCE, abs=1e-6)  # type: ignore[arg-type]
    assert all(not f.depends_on_scenario and f.status == "firme" for f in flows)


def test_rate_step_inside_a_period_is_split() -> None:
    ts = TermSheet(
        obligation=obligation(), as_of=CUTOFF, outstanding=100.0,
        period_dates=(date(2026, 12, 31),), accrual_start=date(2026, 6, 30), day_count="30/360",
        rate=FixedRate(((date(2026, 1, 1), 0.04), (date(2026, 9, 30), 0.08))),
        amortization=((date(2026, 12, 31), 1.0),),
    )  # fmt: skip
    (interest, _) = generate(ts)
    assert interest.amount == pytest.approx(100 * (0.04 * 0.25 + 0.08 * 0.25))


def floating_sheet(**kw: object) -> TermSheet:
    base = dict(
        obligation=obligation(currency_of_account="ARS", currency_of_settlement="ARS"),
        as_of=CUTOFF, outstanding=1000.0, period_dates=(date(2026, 12, 30),),
        accrual_start=date(2026, 6, 30), day_count="ACT/365",
        rate=FloatingRate("TAMAR", spread=0.05), amortization=((date(2026, 12, 30), 1.0),),
    )  # fmt: skip
    return TermSheet(**{**base, **kw})  # type: ignore[arg-type]


def test_floating_without_path_is_unknown_not_zero() -> None:
    interest, principal = generate(floating_sheet())
    assert interest.amount is None and interest.depends_on_scenario
    assert principal.amount == 1000.0 and not principal.depends_on_scenario

    s = Scenario("s", "test")
    s.set_path("TAMAR", [(date(2026, 1, 1), 0.30)])
    interest, _ = generate(floating_sheet(), s)
    days = (date(2026, 12, 30) - CUTOFF).days
    assert interest.amount == pytest.approx(1000 * 0.35 * days / 365)
    assert interest.scenario_id == "s"


def test_capitalizing_floating_without_path_leaves_principal_unknown() -> None:
    flows = generate(floating_sheet(capitalizes=True))
    assert [f.amount for f in flows] == [None, None]
    assert not flows[0].is_payment


def test_capitalization_at_monthly_effective_rate() -> None:
    ts = TermSheet(
        obligation=obligation(currency_of_account="ARS", currency_of_settlement="ARS"),
        as_of=CUTOFF, outstanding=1000.0,
        period_dates=tuple(regular_dates(date(2026, 7, 31), date(2026, 9, 30), 1, eom=True)),
        accrual_start=date(2026, 6, 30), day_count="30/360",
        rate=FixedRate(((date(2026, 1, 1), 0.02),), per_period=True), capitalizes=True,
        amortization=((date(2026, 9, 30), 1.0),),
    )  # fmt: skip
    flows = generate(ts)
    assert [f.flow_type for f in flows].count("interes_capitalizado") == 3
    assert not any(f.is_payment for f in flows if f.flow_type == "interes_capitalizado")
    assert flows[-1].amount == pytest.approx(1000 * 1.02**3)


def test_amortization_must_add_to_one() -> None:
    with pytest.raises(ValueError, match="adds to"):
        TermSheet(
            obligation=obligation(), as_of=CUTOFF, outstanding=1.0,
            period_dates=(date(2027, 1, 1),), accrual_start=CUTOFF, day_count="30/360",
            rate=ZeroRate(), amortization=((date(2027, 1, 1), 0.9),),
        )  # fmt: skip


def flow(**kw: object) -> CashFlow:
    base = dict(
        instrument_id="INS-C-0001", date=date(2026, 8, 1), flow_type="amortizacion", amount=10.0,
        unit="USD", currency_of_account="USD", indexation="ninguna", currency_of_settlement="USD",
        status="firme", is_payment=True, depends_on_scenario=False, source="motor",
        debtor="Tesoro", creditor_type="desconocido", holder_residency="desconocida",
    )  # fmt: skip
    return CashFlow(**{**base, **kw})  # type: ignore[arg-type]


def frozen() -> Scenario:
    s = Scenario("frozen", "test")
    s.set_path("FX:ARS", [(CUTOFF, 1500.0)])
    s.set_path("FX:EUR", [(CUTOFF, 0.8)])
    s.set_path("CER", [(CUTOFF, 800.0)])
    return s


def test_cer_dollar_linked_and_cross_currency_valuation() -> None:
    cer = value_flow(flow(unit="CER", currency_of_account="ARS", indexation="CER",
                          currency_of_settlement="ARS"), frozen())  # fmt: skip
    assert cer.amount_account == 8000.0 and cer.amount_usd == pytest.approx(8000 / 1500)

    dlk = value_flow(flow(indexation="dolar_linked", currency_of_settlement="ARS"), frozen())
    assert dlk.amount_account == 10.0 and dlk.amount_settlement == 15000.0

    kwd = value_flow(flow(unit="KWD", currency_of_account="KWD", currency_of_settlement="EUR"),
                     frozen())  # fmt: skip
    assert kwd.amount_account == 10.0 and kwd.amount_usd is None  # no KWD path: unknown

    early = value_flow(flow(date=date(2026, 1, 1), unit="CER", currency_of_account="ARS",
                            indexation="CER"), frozen())  # fmt: skip
    assert early.amount_account is None  # before the path starts


def test_dual_takes_the_larger_leg_or_unknown() -> None:
    fixed = floating_sheet(rate=FixedRate(((date(2026, 1, 1), 0.30),)))
    floating = floating_sheet()
    s = frozen()
    s.set_path("TAMAR", [(date(2026, 1, 1), 0.40)])
    chosen = dual_max(fixed, floating, s)
    assert chosen[0].note and "rama b" in chosen[0].note
    assert all(f.depends_on_scenario for f in chosen)
    assert all(f.amount is None for f in dual_max(fixed, floating, frozen()))


def test_buckets_and_unknown_amounts() -> None:
    assert bucket(date(2026, 6, 30), CUTOFF) is None
    assert bucket(date(2026, 7, 1), CUTOFF) == ("mensual", "M01")
    assert bucket(date(2029, 6, 30), CUTOFF) == ("mensual", "M36")
    assert bucket(date(2029, 7, 1), CUTOFF) == ("anual", "A04")
    assert bucket(date(2046, 6, 30), CUTOFF) == ("anual", "A20")
    assert bucket(date(2046, 7, 1), CUTOFF) == ("anual", "mas_de_20")

    s = frozen()
    rows = aggregate([value_flow(flow(), s), value_flow(flow(amount=None), s)], CUTOFF)
    assert len(rows) == 1
    assert rows[0]["monto_usd"] == 10.0 and rows[0]["n_sin_monto_usd"] == 1
    with pytest.raises(ValueError):
        aggregate([], CUTOFF, by=("source",))


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


SALDO = "sigade_2026-06-30_saldo_de_deuda_en_situacion_de_pago_normal.csv"
VENC = "sigade_2026-06-30_vencimientos_de_la_deuda_en_situacion_de_pago_normal.csv"


def balance_row(name: str, code: str, pay: str, cls: str, rate: str) -> dict[str, object]:
    return {
        "Clasificación de la Deuda": cls,
        "Nombre de la Operación": name,
        "Tipo de Tasa": rate,
        "Moneda del Prestamo": code,
        "Moneda de Pago": pay,
        "Saldo en Moneda de Origen": "1",
    }


def maturity_row(name: str, code: str, cls: str, rate: str, ymd: tuple[int, int, int],
                 principal: str, interest: str) -> dict[str, object]:  # fmt: skip
    y, m, d = ymd
    return {
        "BOLETIN": cls,
        "Nombre de la Operación": name,
        "Año": str(y),
        "Mes": str(m),
        "Día": str(d),
        "Tipo de Tasa": rate,
        "Moneda de Origen": code,
        "Fecha de Servicio": date(y, m, d).strftime("%m/%d/%y 00:00:00"),
        "Principal en Moneda del Prestamo": principal,
        "Interes en Moneda del Prestamo": interest,
    }


def test_sigade_loader(tmp_path: Path) -> None:
    write_csv(tmp_path / SALDO, [
        balance_row("BONO X", "UCP", "ARP", "BONOS", "TASA CERO"),
        balance_row("AVAL 1", "USD", "USD", "AVALES", "TASA SOFR"),
    ])  # fmt: skip
    write_csv(tmp_path / VENC, [
        maturity_row("BONO X", "UCP", "BONOS", "TASA CERO", (2069, 1, 2), "5", "0"),
        maturity_row("AVAL 1", "USD", "AVALES", "TASA SOFR", (2027, 3, 1), "7", "1"),
    ])  # fmt: skip
    ins = tmp_path / "instruments.csv"
    write_csv(ins, [{
        "instrument_id": "INS-C-0009", "issuer": "Tesoro", "operation_name_sigade": "BONO X",
        "currency_code_sigade": "UCP", "notes": "tipo de tasa SIGADE: TASA CERO; x",
    }])  # fmt: skip
    flows = load_sigade_flows(tmp_path, "2026-06-30", read_instrument_index(ins))
    bono = next(f for f in flows if f.instrument_id == "INS-C-0009")
    assert bono.date == date(2069, 1, 2)  # "01/02/69" is 2069, not 1969
    assert (bono.unit, bono.currency_of_account, bono.indexation) == ("CER", "ARS", "CER")
    aval = [f for f in flows if f.instrument_id == "AVAL 1"]
    assert {f.status for f in aval} == {"contingente"}
    assert [f.depends_on_scenario for f in aval] == [False, True]  # principal, SOFR interest


def test_term_loader_rejects_unknown_rate_rows(tmp_path: Path) -> None:
    repo = Path(__file__).resolve().parent.parent / "contratos"
    sheets = load_term_sheets(repo)
    assert {ts.obligation.instrument_id for ts in sheets} >= {"INS-C-0398", "INS-C-0405"}

    for name in TERM_FILES[:1] + TERM_FILES[2:]:
        (tmp_path / name).write_text((repo / name).read_text(encoding="utf-8"), encoding="utf-8")
    rates = (repo / "tasas.csv").read_text(encoding="utf-8")
    (tmp_path / "tasas.csv").write_text(rates + "INS-C-9999,2020-01-01,0.1,SRC-0106,x\n")
    with pytest.raises(ValueError, match="not in terminos"):
        load_term_sheets(tmp_path)


def test_final_stub_and_thirty_e_day_count() -> None:
    dates = regular_dates(date(2026, 7, 15), date(2026, 10, 31), 1, final_stub=True)
    assert dates[-2:] == [date(2026, 10, 15), date(2026, 10, 31)]
    with pytest.raises(ValueError, match="not on the schedule"):
        regular_dates(date(2026, 7, 15), date(2026, 10, 31), 1)
    # Months of thirty days: day 31 counts as 30 at the end even when the start is the 15th.
    assert year_fraction(date(2027, 5, 15), date(2027, 5, 31), "30E/360") * 360 == 15
    assert year_fraction(date(2027, 5, 15), date(2027, 5, 31), "30/360") * 360 == 16


def test_lecap_pays_the_legal_formula_from_a_mid_life_balance() -> None:
    # BONCAP 2,05% 15-01-2027 (INS-C-0363): issued 2025-01-31, anniversaries at month end.
    # SIGADE carries VNO x 1.0205^17 at the cut-off; the legal value at maturity is
    # VNO x (1+Tm)^((DIAS/360) x 12) with DIAS on months of thirty days (RC 23/2026).
    issue, maturity, tem, vno = date(2025, 1, 31), date(2027, 1, 15), 0.0205, 1000.0
    ts = TermSheet(
        obligation=obligation(currency_of_account="ARS", currency_of_settlement="ARS"),
        as_of=CUTOFF, outstanding=vno * (1 + tem) ** 17,
        period_dates=tuple(regular_dates(date(2025, 2, 28), maturity, 1, eom=True,
                                         final_stub=True)),
        accrual_start=issue, day_count="30E/360",
        rate=FixedRate(((issue, tem),), per_period=True), capitalizes=True,
        frequency_months=1, amortization=((maturity, 1.0),),
    )  # fmt: skip
    flows = generate(ts)
    dias = year_fraction(issue, maturity, "30E/360") * 360
    assert dias == 705
    assert flows[-1].amount == pytest.approx(vno * (1 + tem) ** (dias / 360 * 12))
    stub = ts.outstanding * (1 + tem) ** 6 * ((1 + tem) ** 0.5 - 1)  # 31-12 to 15-01: half a month
    assert flows[-2].amount == pytest.approx(stub)


def test_floating_rate_cap() -> None:
    ts = floating_sheet(rate=FloatingRate("RESERVAS", cap_index="SOFR", cap_spread=-0.01))
    s = Scenario("s", "test")
    s.set_path("RESERVAS", [(date(2026, 1, 1), 0.05)])
    assert generate(ts, s)[0].amount is None  # cap index without a path
    s.set_path("SOFR", [(date(2026, 1, 1), 0.04)])
    days = (date(2026, 12, 30) - CUTOFF).days
    assert generate(ts, s)[0].amount == pytest.approx(1000 * 0.03 * days / 365)
    s.set_path("SOFR", [(date(2026, 1, 1), 0.08)])
    assert generate(ts, s)[0].amount == pytest.approx(1000 * 0.05 * days / 365)


def test_explicit_dates_replace_the_grid(tmp_path: Path) -> None:
    repo = Path(__file__).resolve().parent.parent / "contratos"
    for name in TERM_FILES:
        (tmp_path / name).write_text((repo / name).read_text(encoding="utf-8"), encoding="utf-8")
    dates = [d.isoformat() for d in semiannual(date(2021, 7, 9), date(2030, 7, 9))]
    listed = (repo / "fechas.csv").read_text(encoding="utf-8").splitlines()[1:]
    rows = listed + [f"INS-C-0398,{d},SRC-0108,x" for d in dates]
    (tmp_path / "fechas.csv").write_text(
        "instrument_id,fecha,source_id,referencia\n" + "\n".join(rows) + "\n", encoding="utf-8"
    )
    by_id = {ts.obligation.instrument_id: ts for ts in load_term_sheets(tmp_path)}
    grid = {ts.obligation.instrument_id: ts for ts in load_term_sheets(repo)}
    assert by_id["INS-C-0398"].period_dates == grid["INS-C-0398"].period_dates
    (tmp_path / "fechas.csv").write_text(
        "instrument_id,fecha,source_id,referencia\n" + "\n".join(rows[:-1]) + "\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="does not end at maturity"):
        load_term_sheets(tmp_path)


def test_reopening_of_a_lecap_adds_face_times_capitalization() -> None:
    # A reopening after the cut-off adds face; the holder gets the same value per unit of face
    # at maturity as the original holders, so the payment scales with total face.
    issue, maturity, tem = date(2026, 1, 30), date(2026, 12, 30), 0.02
    dates = tuple(regular_dates(date(2026, 2, 28), maturity, 1, eom=False, final_stub=True))

    def sheet(outstanding: float, changes: tuple[tuple[date, float], ...]) -> TermSheet:
        return TermSheet(
            obligation=obligation(currency_of_account="ARS", currency_of_settlement="ARS"),
            as_of=CUTOFF, outstanding=outstanding, period_dates=dates, accrual_start=issue,
            day_count="30E/360", rate=FixedRate(((issue, tem),), per_period=True),
            capitalizes=True, frequency_months=1, amortization=((maturity, 1.0),),
            face_changes=changes,
        )  # fmt: skip

    past = sum(1 for d in dates if d <= CUTOFF)
    base = generate(sheet(1000 * (1 + tem) ** past, ()))[-1].amount
    reopened = generate(sheet(1000 * (1 + tem) ** past, ((date(2026, 8, 14), 500.0),)))
    assert reopened[-1].amount == pytest.approx(base * 1.5)
    bought_back = generate(sheet(1000 * (1 + tem) ** past, ((date(2026, 9, 1), -1000.0),)))
    assert bought_back[-1].amount == pytest.approx(0.0, abs=1e-9)


def test_issue_after_the_cutoff_and_amortizing_buyback() -> None:
    issue, maturity = date(2026, 8, 15), date(2028, 8, 15)
    dates = semiannual(date(2027, 2, 15), maturity)
    amort = ((date(2027, 8, 15), 0.5), (maturity, 0.5))
    ts = TermSheet(
        obligation=obligation(), as_of=CUTOFF, outstanding=0.0, period_dates=dates,
        accrual_start=issue, day_count="30/360", rate=FixedRate(((issue, 0.06),)),
        amortization=amort,
        face_changes=((issue, 1000.0), (date(2027, 10, 1), -200.0)),
    )  # fmt: skip
    flows = {(f.date, f.flow_type): f.amount for f in generate(ts)}
    assert flows[(date(2027, 2, 15), "interes")] == pytest.approx(30.0)
    assert flows[(date(2027, 8, 15), "amortizacion")] == pytest.approx(500.0)
    # 200 of original face bought back with half amortized removes 100 of balance.
    assert flows[(date(2028, 2, 15), "interes")] == pytest.approx(400 * 0.03)
    assert flows[(maturity, "amortizacion")] == pytest.approx(400.0)
    with pytest.raises(ValueError, match="outside"):
        TermSheet(**{**ts.__dict__, "face_changes": ((CUTOFF, 1.0),)})


def test_loader_requires_an_issue_row_for_post_cutoff_instruments(tmp_path: Path) -> None:
    repo = Path(__file__).resolve().parent.parent / "contratos"
    for name in TERM_FILES:
        (tmp_path / name).write_text((repo / name).read_text(encoding="utf-8"), encoding="utf-8")
    with (tmp_path / "terminos.csv").open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    gd30 = next(r for r in rows if r["instrument_id"] == "INS-C-0398")
    new = {**gd30, "instrument_id": "INS-C-9001", "saldo_corte": "0",
           "fecha_emision": "2026-08-01"}  # fmt: skip
    with (tmp_path / "terminos.csv").open("a", newline="", encoding="utf-8") as fh:
        csv.DictWriter(fh, fieldnames=list(gd30), lineterminator="\n").writerow(new)
    rates = (tmp_path / "tasas.csv").read_text(encoding="utf-8").splitlines()
    extra = [r.replace("INS-C-0398", "INS-C-9001") for r in rates if r.startswith("INS-C-0398")]
    (tmp_path / "tasas.csv").write_text("\n".join(rates + extra) + "\n", encoding="utf-8")
    amorts = (tmp_path / "amortizaciones.csv").read_text(encoding="utf-8").splitlines()
    extra = [r.replace("INS-C-0398", "INS-C-9001") for r in amorts if r.startswith("INS-C-0398")]
    (tmp_path / "amortizaciones.csv").write_text("\n".join(amorts + extra) + "\n", encoding="utf-8")
    with pytest.raises(ValueError, match="emision row"):
        load_term_sheets(tmp_path)
    with (tmp_path / "operaciones.csv").open("a", encoding="utf-8") as fh:
        fh.write("INS-C-9001,2026-08-01,emision,1000,SRC-0108,x\n")
    sheets = {s.obligation.instrument_id: s for s in load_term_sheets(tmp_path)}
    sheet = sheets["INS-C-9001"]
    assert sheet.face_changes == ((date(2026, 8, 1), 1000.0),)


def test_thirty_360_february_and_full_monthly_periods() -> None:
    # US basis: the last day of February at the start counts as day 30.
    assert year_fraction(date(2028, 2, 29), date(2028, 3, 31), "30/360") * 360 == 30
    assert year_fraction(date(2027, 2, 26), date(2027, 3, 31), "30/360") * 360 == 35
    # On a regular month-end grid each full month is 1/12, as SIGADE pays the Consenso Fiscal
    # bond; with dates listed in the norm, the plain day count applies.
    dates = tuple(regular_dates(date(2026, 7, 31), date(2027, 3, 31), 1, eom=True))
    kw = dict(
        obligation=obligation(currency_of_account="ARS", currency_of_settlement="ARS"),
        as_of=CUTOFF, outstanding=1200.0, period_dates=dates, accrual_start=date(2026, 6, 30),
        day_count="30/360", rate=FixedRate(((date(2026, 1, 1), 0.12),)),
        amortization=((dates[-1], 1.0),), frequency_months=1,
    )  # fmt: skip
    grid = {f.date: f.amount for f in generate(TermSheet(**kw)) if f.flow_type == "interes"}
    assert grid[date(2027, 2, 28)] == pytest.approx(12.0)
    listed = TermSheet(**{**kw, "listed_dates": True})
    flows = {f.date: f.amount for f in generate(listed) if f.flow_type == "interes"}
    assert flows[date(2027, 2, 28)] == pytest.approx(1200 * 0.12 * 28 / 360)


def test_merge_term_folders_replaces_rows_in_place(tmp_path: Path) -> None:
    base, over, out = tmp_path / "b", tmp_path / "o", tmp_path / "m"
    base.mkdir()
    over.mkdir()
    (base / "terminos.csv").write_text("instrument_id,x\nA,1\nB,1\nC,1\n", encoding="utf-8")
    (base / "tasas.csv").write_text("instrument_id,x\nA,1\nB,1\nB,2\nC,1\n", encoding="utf-8")
    (over / "terminos.csv").write_text("instrument_id,x\nB,9\nD,9\n", encoding="utf-8")
    (over / "tasas.csv").write_text("instrument_id,x\nB,9\nD,9\n", encoding="utf-8")
    (over / "operaciones.csv").write_text("instrument_id,y\nA,5\n", encoding="utf-8")
    merge_term_folders(base, over, out)
    assert (out / "tasas.csv").read_text().splitlines() == [
        "instrument_id,x", "A,1", "B,9", "C,1", "D,9",
    ]  # fmt: skip
    assert (out / "operaciones.csv").read_text().splitlines() == ["instrument_id,y", "A,5"]


def test_operations_turn_pesos_into_cer_units_and_refuse_negative_balances(
    tmp_path: Path,
) -> None:
    repo = Path(__file__).resolve().parent.parent / "contratos"
    for name in TERM_FILES:
        (tmp_path / name).write_text((repo / name).read_text(encoding="utf-8"), encoding="utf-8")
    with (tmp_path / "terminos.csv").open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    cer = next(r for r in rows if r["indexacion"] == "CER" and r["tipo_tasa"] == "cero")
    iid = cer["instrument_id"]
    with (tmp_path / "operaciones.csv").open("a", encoding="utf-8") as fh:
        fh.write(f"{iid},2026-07-17,reapertura,800,SRC-0108,x\n")
    with pytest.raises(ValueError, match="indice_inicial"):
        load_term_sheets(tmp_path)
    for r in rows:
        r["indice_inicial"] = "400" if r["instrument_id"] == iid else ""
    with (tmp_path / "terminos.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    sheet = {s.obligation.instrument_id: s for s in load_term_sheets(tmp_path)}[iid]
    assert sheet.face_changes == ((date(2026, 7, 17), 2.0),)
    too_much = TermSheet(**{**sheet.__dict__, "face_changes": ((date(2026, 7, 17), -1e18),)})
    with pytest.raises(ValueError, match="negative"):
        generate(too_much)
