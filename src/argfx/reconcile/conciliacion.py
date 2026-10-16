"""Reconcile the inventory and the obligations calendar with the Secretaría de Finanzas workbook.

Controls, each row with the official figure, ours, the difference and a materiality flag:
- `stock.csv`: SIGADE balances at the cut-off against A.1.1 (debt in normal payment status,
  international organizations, transitory advances);
- `flujos_trimestre.csv`: the identities of A.2.2 (opening + variations = closing);
- `perfil.csv`: the twelve-month profile of A.3.1 against the SIGADE projection and against
  the calendar (engine where there are terms, SIGADE elsewhere), by month and concept;
- `atribucion.csv`: the calendar minus SIGADE, by month, concept and cause, so that every
  difference with the official profile has a contractual reason or is flagged.

All amounts are in millions of USD at the cut-off exchange rates (A.3.1 and the frozen SIGADE
scenario use the same rates). Unknown amounts stay out of the sums and are counted.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from argfx.contracts.calendar import _write
from argfx.contracts.terms import load_duals, load_term_sheets
from argfx.reconcile.finanzas import Line, find, lines, maturity_profile


@dataclass(frozen=True)
class Materiality:
    abs_musd: float = 10.0
    rel: float = 0.001

    def material(self, official: float | None, ours: float | None) -> bool:
        if official is None or ours is None:
            return True
        diff = abs(ours - official)
        return diff > self.abs_musd and diff > self.rel * abs(official)


def _row(control: str, item: str, official: float | None, ours: float | None,
         m: Materiality, note: str = "") -> dict[str, object]:  # fmt: skip
    diff = None if official is None or ours is None else ours - official
    return {
        "control": control,
        "partida": item,
        "oficial_musd": None if official is None else round(official, 3),
        "propio_musd": None if ours is None else round(ours, 3),
        "diferencia_musd": None if diff is None else round(diff, 3),
        "diferencia_rel": None if diff is None or not official else float(f"{diff / official:.3g}"),
        "material": m.material(official, ours),
        "nota": note,
    }


def stock_controls(a11: list[Line], instruments_csv: Path, m: Materiality) -> list[dict]:
    by_family: dict[str, float] = defaultdict(float)
    with instruments_csv.open(newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            by_family[r["instrument_family"]] += float(r["outstanding_usd_equiv_sigade"] or 0)
    total = sum(by_family.values()) / 1e6
    at = sum(v for k, v in by_family.items() if k.startswith("adelantos transitorios")) / 1e6
    official_at = sum(
        line.values[0] for line in a11 if line.label.upper().startswith("ADELANTOS TRANSITORIOS")
    ) / 1e3  # fmt: skip
    return [
        _row("stock", "Deuda en situación de pago normal (A.1.1 III)",
             find(a11, "III-").values[0] / 1e3, total, m, "SIGADE, todas las operaciones"),
        _row("stock", "Organismos internacionales (A.1.1)",
             find(a11, "ORGANISMOS INTERNACIONALES").values[0] / 1e3,
             by_family.get("multilateral", 0.0) / 1e6, m, "SIGADE, familia multilateral"),
        _row("stock", "Adelantos transitorios del BCRA (A.1.1, mediano y corto plazo)",
             official_at, at, m, "SIGADE, familia de adelantos transitorios"),
    ]  # fmt: skip


def flow_identities(a22: list[Line], m: Materiality) -> list[dict]:
    def v(prefix: str) -> float:
        return find(a22, prefix).values[0] / 1e3

    opening = v("I -") + v("II -")
    variations = [v(f"{x})") for x in "abcde"]
    return [
        _row("flujos", "Saldo inicial + variación total = deuda bruta final (A.2.2: III + IV = V)",
             v("V -"), opening + v("IV -"), m),
        _row("flujos", "Variación total = a + b + c + d + e (A.2.2 IV)",
             v("IV -"), sum(variations), m),
        _row("flujos", "Operaciones de crédito público = financiamiento - amortizaciones (A.2.2 a)",
             v("a)"), v("1 -") - v("2 -"), m),
        _row("flujos", "Deuda bruta sin elegible = V - VI (A.2.2 VII)",
             v("VII -"), v("V -") - v("VI -"), m),
    ]  # fmt: skip


def _months(cutoff: date) -> list[str]:
    out, y, mo = [], cutoff.year, cutoff.month
    for _ in range(12):
        mo += 1
        if mo > 12:
            y, mo = y + 1, 1
        out.append(f"{y}-{mo:02d}")
    return out


def _cause(iid: str, attrs: dict[str, dict[str, bool]]) -> str:
    a = attrs.get(iid)
    if a is None:
        return "emitido después del corte"
    if a["operaciones"]:
        return "operaciones posteriores al corte"
    if a["dual"]:
        return "dual"
    if a["capitaliza"]:
        return "capitalización (LECAP, BONCAP)"
    if a["rezago"]:
        return "base y rezago de índices"
    return "otros términos"


def profile_controls(
    path: Path, flows_csv: Path, terms_dir: Path, cutoff: date, m: Materiality
) -> tuple[list[dict], list[dict]]:
    months = _months(cutoff)
    official: dict[tuple[str, str], float] = {
        (r.month, r.concept): r.usd_thousands / 1e3
        for r in maturity_profile(path)
        if r.group.upper() == "TOTAL" and r.concept in ("capital", "interes")
    }
    sheets = load_term_sheets(terms_dir)
    duals = load_duals(terms_dir, sheets)
    attrs = {
        ts.obligation.instrument_id: {
            "operaciones": bool(ts.face_changes),
            "dual": ts.obligation.instrument_id in duals,
            "capitaliza": ts.capitalizes,
            "rezago": bool(ts.index_lag_days) or getattr(ts.rate, "lag_days", 0) > 0,
        }
        for ts in sheets
    }
    sigade: dict[tuple[str, str], float] = defaultdict(float)
    calendar: dict[tuple[str, str], float] = defaultdict(float)
    unknown: dict[tuple[str, str], int] = defaultdict(int)
    by_inst: dict[tuple[str, str, str], list[float | None]] = defaultdict(lambda: [0.0, 0.0])
    with flows_csv.open(newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if r["is_payment"] != "True" or r["date"][:7] not in months:
                continue
            key = (r["date"][:7], "capital" if r["flow_type"] == "amortizacion" else "interes")
            amount = float(r["monto_usd"]) / 1e6 if r["monto_usd"] else None
            iid = r["instrument_id"]
            if r["source"] == "sigade":
                sigade[key] += amount or 0.0
                if iid in attrs:
                    by_inst[(*key, iid)][1] += amount or 0.0  # type: ignore[operator]
            if r["base"] == "True":
                if amount is None:
                    unknown[key] += 1
                else:
                    calendar[key] += amount
                if r["source"] == "motor":
                    cell = by_inst[(*key, iid)]
                    cell[0] = None if amount is None or cell[0] is None else cell[0] + amount
    profile = []
    for month in months:
        for concept in ("capital", "interes"):
            k = (month, concept)
            off = official.get(k)
            profile.append(
                {
                    **_row("perfil", f"{month} {concept}: SIGADE", off, sigade[k], m),
                    "mes": month,
                    "concepto": concept,
                }
            )
            note = f"{unknown[k]} flujos sin monto en el escenario" if unknown[k] else ""
            profile.append(
                {
                    **_row("perfil", f"{month} {concept}: calendario", off, calendar[k], m, note),
                    "mes": month,
                    "concepto": concept,
                }
            )
    causes: dict[tuple[str, str, str], list[float]] = defaultdict(lambda: [0.0, 0.0, 0])
    for (month, concept, iid), (engine, sig) in by_inst.items():
        cause = "sin monto en el escenario" if engine is None else _cause(iid, attrs)
        cell = causes[(month, concept, cause)]
        cell[0] += (engine or 0.0) - sig  # type: ignore[operator]
        cell[1] += sig  # type: ignore[operator]
        cell[2] += 1
    attribution = [
        {
            "mes": month,
            "concepto": concept,
            "causa": cause,
            "calendario_menos_sigade_musd": round(d, 3),
            "sigade_musd": round(s, 3),
            "instrumentos": int(n),
        }
        for (month, concept, cause), (d, s, n) in sorted(causes.items())
        if abs(d) > 1e-6 or cause == "sin monto en el escenario"
    ]
    return profile, attribution


def build_reconciliation(
    finanzas_xlsx: Path,
    instruments_csv: Path,
    calendar_dir: Path,
    terms_dir: Path,
    cutoff: date,
    out: Path,
    m: Materiality | None = None,
) -> dict[str, int]:
    m = m or Materiality()
    stock = stock_controls(lines(finanzas_xlsx, "A.1.1"), instruments_csv, m)
    flows = flow_identities(lines(finanzas_xlsx, "A.2.2"), m)
    profile, attribution = profile_controls(
        finanzas_xlsx, calendar_dir / "flujos.csv", terms_dir, cutoff, m
    )
    _write(out / "stock.csv", stock)
    _write(out / "flujos_trimestre.csv", flows)
    _write(out / "perfil.csv", profile)
    _write(out / "atribucion.csv", attribution)
    sigade_rows = [r for r in profile if r["partida"].endswith("SIGADE")]
    return {
        "controles_stock_materiales": sum(bool(r["material"]) for r in stock),
        "identidades_flujos_materiales": sum(bool(r["material"]) for r in flows),
        "meses_sigade_vs_perfil_materiales": sum(bool(r["material"]) for r in sigade_rows),
        "filas_atribucion": len(attribution),
    }
