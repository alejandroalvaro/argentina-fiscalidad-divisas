"""Build the obligations calendar: engine flows where there is a term sheet, SIGADE elsewhere.

Outputs (CSV, small enough for review):
- `flujos.csv`: every flow from both sources, valued under the scenario, with `base` marking
  the flows that enter the calendar (engine if the instrument has a term sheet, else SIGADE);
- `calendario.csv`: base flows by protocol bucket and by every dimension, kept separate;
- `necesidad_divisas.csv`: firm payments settled in a currency other than ARS, by bucket and
  settlement currency (dollar-linked debt payable in ARS is excluded by construction);
- `comparacion_sigade.csv`: engine against SIGADE, instrument by instrument and date by date.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import asdict
from datetime import date
from pathlib import Path

from argfx.contracts.buckets import aggregate, bucket
from argfx.contracts.engine import generate
from argfx.contracts.model import CashFlow
from argfx.contracts.scenario import Scenario, Valuation, value_flow
from argfx.contracts.sigade import load_sigade_flows, read_instrument_index
from argfx.contracts.terms import load_term_sheets


def _write(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        if not rows:
            fh.write("")
            return
        w = csv.DictWriter(fh, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        for r in rows:
            w.writerow({k: "" if v is None else v for k, v in r.items()})


def compare_with_sigade(
    engine: list[CashFlow],
    sigade: list[CashFlow],
    tolerance: float = 0.01,
    rel_tolerance: float = 1e-8,
) -> list[dict[str, object]]:
    """One row per instrument with a term sheet: matched keys and the largest difference.

    A flow matches within `tolerance` (absolute, in contract units) or `rel_tolerance` (relative
    to the SIGADE amount): SIGADE rounds each flow, and large CER balances accumulate cents.
    """
    s: dict[tuple[str, date, str], float] = defaultdict(float)
    e: dict[tuple[str, date, str], float | None] = {}
    for f in sigade:
        s[(f.instrument_id, f.date, f.flow_type)] += f.amount or 0.0
    for f in engine:
        if f.is_payment:
            e[(f.instrument_id, f.date, f.flow_type)] = f.amount
    rows = []
    for iid in sorted({k[0] for k in e}):
        keys = {k for k in e if k[0] == iid} | {k for k in s if k[0] == iid}
        unknown = sum(1 for k in keys if k in e and e[k] is None)
        known = [k for k in keys if e.get(k, 0.0) is not None]
        diffs = [abs((e.get(k) or 0.0) - s.get(k, 0.0)) for k in known]
        rels = [
            d / abs(s[k]) if s.get(k) else (0.0 if d == 0 else 1.0)
            for k, d in zip(known, diffs, strict=True)
        ]
        worst = max(diffs, default=0.0)
        worst_rel = max(rels, default=0.0)
        rows.append(
            {
                "instrument_id": iid,
                "fechas_y_tipos": len(keys),
                "solo_motor": sum(1 for k in keys if k not in s),
                "solo_sigade": sum(1 for k in keys if k not in e),
                "motor_sin_monto": unknown,
                "max_dif_abs": round(worst, 6),
                "max_dif_rel": float(f"{worst_rel:.3g}"),
                "coincide": unknown == 0
                and all(
                    d <= tolerance or r <= rel_tolerance for d, r in zip(diffs, rels, strict=True)
                ),
            }
        )
    return rows


def build_calendar(
    terms_dir: Path, sigade_dir: Path, instruments_csv: Path, cutoff: date, out: Path
) -> dict[str, int]:
    scenario = Scenario.frozen_from_sigade(sigade_dir / f"sigade_{cutoff}_tipos_de_cambio.csv")
    sigade = load_sigade_flows(
        sigade_dir, cutoff.isoformat(), read_instrument_index(instruments_csv)
    )
    sheets = load_term_sheets(terms_dir)
    for ts in sheets:
        if ts.as_of != cutoff:
            raise ValueError(f"{ts.obligation.instrument_id}: cut-off {ts.as_of} != {cutoff}")
    engine = [f for ts in sheets for f in generate(ts, scenario)]
    with_terms = {ts.obligation.instrument_id for ts in sheets}

    valued: list[tuple[Valuation, bool]] = []
    for f in engine:
        valued.append((value_flow(f, scenario), True))
    for f in sigade:
        valued.append((value_flow(f, scenario), f.instrument_id not in with_terms))

    flow_rows = []
    for v, base in valued:
        b = bucket(v.flow.date, cutoff)
        flow_rows.append(
            {
                **asdict(v.flow),
                "base": base,
                "horizonte": b[0] if b else None,
                "periodo": b[1] if b else None,
                "escenario_valuacion": v.scenario_id,
                "monto_cuenta": v.amount_account,
                "monto_liquidacion": v.amount_settlement,
                "monto_usd": v.amount_usd,
            }
        )
    base_vals = [v for v, base in valued if base]
    calendar = aggregate(base_vals, cutoff)
    fx_need = aggregate(
        (
            v
            for v in base_vals
            if v.flow.status == "firme"
            and v.flow.is_payment
            and v.flow.currency_of_settlement != "ARS"
        ),
        cutoff,
        by=("source", "flow_type", "currency_of_settlement", "depends_on_scenario"),
    )
    comparison = compare_with_sigade(engine, sigade)
    # SIGADE projects the balance at the cut-off; operations after it are expected differences.
    with_ops = {ts.obligation.instrument_id for ts in sheets if ts.face_changes}
    for row in comparison:
        row["con_operaciones"] = row["instrument_id"] in with_ops

    _write(out / "flujos.csv", flow_rows)
    _write(out / "calendario.csv", calendar)
    _write(out / "necesidad_divisas.csv", fx_need)
    _write(out / "comparacion_sigade.csv", comparison)
    return {
        "flujos_sigade": len(sigade),
        "flujos_motor": len(engine),
        "instrumentos_con_terminos": len(with_terms),
        "instrumentos_coinciden_con_sigade": sum(bool(r["coincide"]) for r in comparison),
        "instrumentos_con_operaciones": len(with_ops),
    }
