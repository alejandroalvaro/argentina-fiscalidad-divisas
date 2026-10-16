"""Consolidate the Treasury with the rest of the public sector: debt held inside it, and the
foreign-currency need once payments to public-sector holders are taken out.

Two layers, kept apart:
- official (top-down): the creditor breakdown of the Secretaría de Finanzas (agencies of the
  public sector, private sector, multilateral and bilateral) and the currency composition of
  the debt held by the public sector (`tenencias/composicion_acreedor_<date>.csv`);
- identified (bottom-up): holdings instrument by instrument
  (`tenencias/tenencias_identificadas_<date>.csv`), each row `directo` (SIGADE gives the
  holder) or `estimado` (an older statement or an operation, assumed unchanged to the cut-off).

The USD the public sector holds beyond what is identified is allocated pro rata over the USD
instruments of SIGADE that are not wholly held by it (`proporcional`). Multilateral, bilateral
and IMF loans are never allocated: their creditors are outside the public sector.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from argfx.contracts.calendar import _write
from argfx.contracts.terms import load_term_sheets

POOL_FAMILY = "USD"  # SIGADE family of USD bonds and letters held by private or public holders


@dataclass(frozen=True)
class Holding:
    instrument_id: str
    holder: str
    face_usd: float  # residual face at the cut-off
    method: str
    source_id: str


def _read(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def remaining_share(terms_dir: Path, cutoff: date) -> dict[str, float]:
    """Fraction of original face still outstanding after the cut-off, from the term sheets."""
    return {
        ts.obligation.instrument_id: sum(f for d, f in ts.amortization if d > cutoff)
        for ts in load_term_sheets(terms_dir)
    }


def identified_holdings(path: Path, terms_dir: Path, cutoff: date) -> list[Holding]:
    remaining = remaining_share(terms_dir, cutoff)
    out = []
    for r in _read(path):
        face = float(r["valor_nominal_original_usd"])
        if r["metodo"] != "directo":  # original face of a bond: keep the part not yet amortized
            face *= remaining.get(r["instrument_id"], 1.0)
        out.append(Holding(r["instrument_id"], r["tenedor"], face, r["metodo"], r["source_id"]))
    return out


def build_consolidation(
    composition_csv: Path,
    holdings_csv: Path,
    instruments_csv: Path,
    flows_csv: Path,
    terms_dir: Path,
    cutoff: date,
    out: Path,
) -> dict[str, float]:
    comp = {r["partida"]: r for r in _read(composition_csv)}
    inst = {r["instrument_id"]: r for r in _read(instruments_csv)}
    holdings = identified_holdings(holdings_csv, terms_dir, cutoff)

    outstanding = {
        iid: float(r["outstanding_usd_equiv_sigade"] or 0) for iid, r in inst.items()
    }  # fmt: skip
    held: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for h in holdings:
        held[h.instrument_id][h.method] += h.face_usd
    share: dict[str, dict[str, float]] = {}
    for iid, by_method in held.items():
        total = outstanding.get(iid) or 0.0
        if total <= 0:
            continue
        share[iid] = {m: min(1.0, v / total) for m, v in by_method.items()}

    public_usd = float(comp["sector_publico_moneda_total"]["millones_usd"]) * 1e6 * float(
        comp["sector_publico_dolares"]["porcentaje"]
    ) / 100  # fmt: skip
    identified_usd = sum(
        min(h.face_usd, outstanding.get(h.instrument_id, h.face_usd)) for h in holdings
    )

    # The unidentified USD is split by governing law: the official composition gives the share
    # of the public sector's holdings under foreign law, and Globales are the foreign-law USD
    # bonds of the pool. The rest goes to local-law USD instruments.
    def law(iid: str) -> str:
        return (
            "extranjera" if "GLOBAL" in inst[iid]["operation_name_sigade"].upper() else "nacional"
        )

    pool: dict[str, dict[str, float]] = {"extranjera": {}, "nacional": {}}
    for iid, v in outstanding.items():
        if inst[iid]["instrument_family"] == POOL_FAMILY and v > 0:
            free = v * (1 - sum(share.get(iid, {}).values()))
            if free > 0:
                pool[law(iid)][iid] = free
    residual = max(0.0, public_usd - identified_usd)
    foreign_public = float(comp["agencias_sector_publico"]["millones_usd"]) * 1e6 * float(
        comp["sector_publico_legislacion_extranjera"]["porcentaje"]
    ) / 100  # fmt: skip
    identified_foreign = sum(
        min(h.face_usd, outstanding.get(h.instrument_id, h.face_usd))
        for h in holdings
        if h.instrument_id in inst and law(h.instrument_id) == "extranjera"
    )
    residual_by_law = {"extranjera": min(residual, max(0.0, foreign_public - identified_foreign))}
    residual_by_law["nacional"] = residual - residual_by_law["extranjera"]
    pro_rata: dict[str, float] = {}
    for lw, members in pool.items():
        total = sum(members.values())
        pro_rata[lw] = residual_by_law[lw] / total if total else 0.0
        for iid, free in members.items():
            share.setdefault(iid, {})["proporcional"] = pro_rata[lw] * free / outstanding[iid]

    months = _months(cutoff)
    need: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
    with flows_csv.open(newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            if (
                r["base"] != "True"
                or r["is_payment"] != "True"
                or r["status"] != "firme"
                or r["currency_of_settlement"] == "ARS"
                or r["date"][:7] not in months
                or not r["monto_usd"]
            ):
                continue
            iid, amount = r["instrument_id"], float(r["monto_usd"])
            need[iid]["bruta"] += amount
            for method, s in share.get(iid, {}).items():
                need[iid][method] += amount * s

    methods = ("directo", "estimado", "proporcional")
    rows = []
    for iid in sorted(need, key=lambda k: -need[k]["bruta"]):
        n = need[iid]
        intra = sum(n[m] for m in methods)
        rows.append(
            {
                "instrument_id": iid,
                "nombre": inst.get(iid, {}).get("operation_name_sigade", ""),
                "familia": inst.get(iid, {}).get("instrument_family", ""),
                "bruta_musd": round(n["bruta"] / 1e6, 3),
                **{f"sector_publico_{m}_musd": round(n[m] / 1e6, 3) for m in methods},
                "consolidada_musd": round((n["bruta"] - intra) / 1e6, 3),
            }
        )
    totals = {k: sum(r[k] for r in rows) for k in rows[0] if k.endswith("_musd")} if rows else {}

    stock = [
        {"capa": "oficial", "partida": p, "millones_usd": comp[p]["millones_usd"] or None,
         "porcentaje": comp[p]["porcentaje"] or None, "source_id": comp[p]["source_id"]}
        for p in comp
    ]  # fmt: skip
    stock.append({"capa": "oficial (derivado)", "partida": "sector_publico_en_dolares",
                  "millones_usd": round(public_usd / 1e6, 1), "porcentaje": None,
                  "source_id": comp["sector_publico_dolares"]["source_id"]})  # fmt: skip
    for method in ("directo", "estimado"):
        v = sum(min(h.face_usd, outstanding.get(h.instrument_id, h.face_usd))
                for h in holdings if h.method == method)  # fmt: skip
        stock.append({"capa": "identificado", "partida": f"tenencias en dólares, {method}",
                      "millones_usd": round(v / 1e6, 1), "porcentaje": None,
                      "source_id": "tenencias/tenencias_identificadas"})  # fmt: skip
    for lw in ("extranjera", "nacional"):
        stock.append({"capa": "proporcional",
                      "partida": f"dólares del sector público sin identificar, ley {lw}",
                      "millones_usd": round(residual_by_law[lw] / 1e6, 1),
                      "porcentaje": round(100 * pro_rata[lw], 2),
                      "source_id": "derivado"})  # fmt: skip

    _write(out / "sector_publico.csv", stock)
    _write(out / "necesidad_divisas_consolidada.csv", rows)
    return {k: round(v, 1) for k, v in totals.items()} | {
        "dolares_sin_identificar_musd": round(residual / 1e6, 1),
        "proporcion_ley_extranjera_pct": round(100 * pro_rata["extranjera"], 2),
        "proporcion_ley_nacional_pct": round(100 * pro_rata["nacional"], 2),
    }


def _months(cutoff: date) -> list[str]:
    out, y, mo = [], cutoff.year, cutoff.month
    for _ in range(12):
        mo += 1
        if mo > 12:
            y, mo = y + 1, 1
        out.append(f"{y}-{mo:02d}")
    return out
