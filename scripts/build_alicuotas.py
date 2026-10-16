"""Build alicuotas/eventos.csv: export-duty rate events by NCM position, from the decree annexes.

Downloads each annex from R2 by its sha256 (manifests/downloads.csv), extracts its text with
`pdftotext -layout` (poppler) and parses it with argfx.simulation.alicuotas. The schedule of
Decreto 423/2026 Annex II comes from the lote AF transcription, checked against the annex. The
Decreto 566/2026 phase-out is a rule applied when the table is loaded (`load_book`).

Run: uv run python scripts/build_alicuotas.py (needs R2 credentials and pdftotext).
"""

from __future__ import annotations

import csv
import re
import subprocess
import tempfile
from datetime import date
from pathlib import Path

from argfx.config import get_settings
from argfx.simulation.alicuotas import (
    RATE,
    Event,
    positions_in,
    rates_from_annex,
    schedule_423,
)
from argfx.storage import fetch_verified, get_store

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "alicuotas" / "eventos.csv"

# (source_id, norm, start, end, kind): kind "tasas" parses a rate column, a number sets every
# listed position to that rate.
ANNEXES = [
    ("SRC-1496", "Decreto 230/2020", date(2020, 3, 5), None, "tasas"),
    ("SRC-1533", "Decreto 1060/2020", date(2021, 1, 1), None, "tasas"),
    ("SRC-1549", "Decreto 506/2023 (0%, prorrogado por 9/2024, 557/2024 y 697/2024)",
     date(2023, 10, 5), None, 0.0),
    ("SRC-1502", "Decreto 754/2021", date(2021, 11, 6), None, "tasas"),
    ("SRC-1546", "Decreto 697/2024", date(2024, 8, 7), None, "tasas"),
    ("SRC-1537", "Decreto 38/2025 Anexo I", date(2025, 1, 28), None, 0.0),
    ("SRC-1538", "Decreto 38/2025 Anexo II (temporario)", date(2025, 1, 28), date(2025, 6, 30),
     "tasas"),
    ("SRC-1541", "Decreto 305/2025", date(2025, 5, 8), None, 0.0),
    ("SRC-1510", "Decreto 526/2025", date(2025, 8, 1), None, "tasas"),
    ("SRC-1544", "Decreto 563/2025", date(2025, 8, 8), None, 0.0),
    ("SRC-1516", "Decreto 423/2026 Anexo I", date(2026, 6, 4), None, "tasas"),
    ("SRC-1520", "Decreto 566/2026 Anexo I", date(2026, 7, 2), None, 0.0),
]  # fmt: skip


def _sha(source_id: str) -> str:
    with (ROOT / "manifests" / "downloads.csv").open(newline="", encoding="utf-8") as fh:
        hashes = [r["sha256"] for r in csv.DictReader(fh)
                  if r["source_id"] == source_id and r["sha256"]]  # fmt: skip
    return hashes[-1]


def _text(source_id: str, tmp: Path) -> str:
    settings = get_settings()
    pdf = tmp / f"{source_id}.pdf"
    fetch_verified(get_store(settings), _sha(source_id), pdf, settings.cache_dir)
    out = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], check=True,
                         capture_output=True, text=True)  # fmt: skip
    return out.stdout


def soy_schedule_790(events: list[Event], tmp: Path) -> list[Event]:
    """Decreto 790/2020 (SRC-1498): soy complex, four columns (October, November and December
    2020, and from 2021-01-01). Decreto 131/2022 suspended it from 2022-03-19 to 2022-12-31,
    when the Decreto 230/2020 rates applied again (CLM-AD-018)."""
    starts = [date(2020, 10, 1), date(2020, 11, 1), date(2020, 12, 1), date(2021, 1, 1)]
    cols: list[dict[str, float]] = [{} for _ in starts]
    for line in _text("SRC-1498", tmp).splitlines():
        m = re.match(r"\s*(\d{4}\.\d{2}\.\d{2})\b(.*)", line)
        found = RATE.findall(m.group(2)) if m else []
        if m and len(found) >= 4:
            for k, v in enumerate(found[-4:]):
                cols[k][m.group(1)] = max(float(v.replace(",", ".")), cols[k].get(m.group(1), 0))
    out = [
        Event(s, None, c, "Decreto 790/2020", "SRC-1498") for s, c in zip(starts, cols, strict=True)
    ]
    base = next(e for e in events if e.norm == "Decreto 230/2020").rates
    back = {c: base[c] for c in cols[-1] if c in base}
    out.append(Event(date(2022, 3, 19), date(2022, 12, 31), back,
                     "Decreto 131/2022 (vuelven las del 230/2020)", "SRC-1338"))  # fmt: skip
    return out


def main() -> None:
    events: list[Event] = []
    with tempfile.TemporaryDirectory() as t:
        for sid, norm, start, end, kind in ANNEXES:
            text = _text(sid, Path(t))
            if kind == "tasas":
                rates, partial = rates_from_annex(text)
                listed = set().union(*(e.rates for e in events)) if events else set()
                rates = {c: v for c, v in rates.items() if c not in partial or c not in listed}
            else:
                rates = dict.fromkeys(positions_in(text), float(kind))
            events.append(Event(start, end, rates, norm, sid))
        events += soy_schedule_790(events, Path(t))
    events += schedule_423(ROOT / "inbox/lote-af/tablas/cronograma_decreto_423_2026_anexo_ii.csv")
    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["ncm", "desde", "hasta", "alicuota_pct", "norma", "source_id"])
        for e in sorted(events, key=lambda e: e.start):
            for code, rate in sorted(e.rates.items()):
                w.writerow([code, e.start, e.end or "", rate, e.norm, e.source_id])
    print(f"{sum(len(e.rates) for e in events):,} filas en {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
