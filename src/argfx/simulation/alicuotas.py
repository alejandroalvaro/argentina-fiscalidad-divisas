"""Export-duty rates by NCM position over time, from the decree annexes (D-005, D-014).

Each decree is an event: from a date (and, if temporary, until a date) a set of positions pays
a rate. The rate of a position on a day is the one of the latest event in force that lists it;
when a temporary event ends, the previous one applies again. Events, in order:

- Decreto 230/2020 (from 2020-03-05) and Decreto 1060/2020 (from 2021-01-01): the general
  annexes, rate per position;
- Decreto 506/2023 (from 2023-10-05): dairy at 0%, extended by 9/2024 and 557/2024 and made
  permanent by 697/2024;
- Decreto 697/2024 (from 2024-08-07): meat and dairy, rate per position;
- Decreto 38/2025 (from 2025-01-28): Annex I at 0%; Annex II, temporary rates until 2025-06-30;
- Decreto 305/2025 (from 2025-05-08) and 563/2025 (from 2025-08-08): positions at 0%;
- Decreto 526/2025 (from 2025-08-01): grains and meat, rate per position;
- Decreto 877/2025 (from 2025-12-12): the 2026 column of Annex II of Decreto 423/2026;
- Decreto 423/2026: Annex I (from 2026-06-04) and the monthly schedule of Annex II for 2027 and
  2028, which applies by the start of the shipment period of the DJVE;
- Decreto 566/2026: Annex I at 0% (from 2026-07-02); positions paying 4.5% or 3% on 2026-06-30
  outside chapters 1 to 24 go down by one twelfth a month to 0% on 2027-06-01 (Annex II).

Approximations, all flagged in the output:
- when an annex lists several rates for one position (by presentation, variety or reference),
  the highest is taken: it is usually the bulk shipment;
- the rate is applied by the month of shipment, while the law fixes it at the registration of
  the DJVE. Around a change (the 0% window of Decreto 682/2025 in September 2025, for instance)
  the estimate moves the change to later months;
- crude oil (2709) and fuels pay a moving rate that depends on the international price; they
  are left to `crude_rate`.
"""

from __future__ import annotations

import bisect
import csv
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

NCM = re.compile(r"\b(\d{4}\.\d{2}\.\d{2})\b")
RATE = re.compile(r"(\d+(?:,\d+)?)\s*%")
BARE_RATE = re.compile(r"(?<![\d.])(\d{1,2},\d{2})(?![\d.])")  # "5,50" in annexes without "%"

# Decreto 566/2026 Annex II (SRC-1521): monthly rates for positions that paid 4.5% and 3%.
PHASE_OUT_566 = [
    (date(2026, 7, 1), 4.125, 2.75),
    (date(2026, 8, 1), 3.75, 2.5),
    (date(2026, 9, 1), 3.375, 2.25),
    (date(2026, 10, 1), 3.0, 2.0),
    (date(2026, 11, 1), 2.625, 1.75),
    (date(2026, 12, 1), 2.25, 1.5),
    (date(2027, 1, 1), 1.875, 1.25),
    (date(2027, 2, 1), 1.5, 1.0),
    (date(2027, 3, 1), 1.125, 0.75),
    (date(2027, 4, 1), 0.75, 0.5),
    (date(2027, 5, 1), 0.375, 0.25),
    (date(2027, 6, 1), 0.0, 0.0),
]


@dataclass(frozen=True)
class Event:
    start: date
    end: date | None  # inclusive; None for permanent
    rates: dict[str, float]  # NCM 8 digits (with dots) -> percent
    norm: str
    source_id: str


QUALIFIER = re.compile(r"\(\d+\)|Excepto|Exclusivamente|Únicamente|Unicamente", re.IGNORECASE)


def rates_from_annex(text: str) -> tuple[dict[str, float], set[str]]:
    """Rate per position from an annex with a rate column; the highest when there are several.

    A position whose rate is on a following line (wrapped descriptions) takes the first rate
    found within the next two lines. Also returns the positions listed only with a qualifier
    (a footnote reference, "Excepto", "Exclusivamente"): the annex covers part of the position,
    and an earlier rate for the rest should not be overwritten."""
    lines = text.splitlines()
    out: dict[str, float] = {}
    plain: set[str] = set()
    for i, line in enumerate(lines):
        m = re.match(r"\s*(\d{4}\.\d{2}\.\d{2})\b(.*)", line)
        if not m:
            continue
        r = _last_rate(m.group(2))
        j = i + 1
        while r is None and j <= i + 2 and j < len(lines) and not NCM.match(lines[j].strip()):
            r = _last_rate(lines[j])
            j += 1
        if r is not None:
            v = r
            out[m.group(1)] = max(v, out.get(m.group(1), 0.0))
            if not QUALIFIER.search(m.group(2)):
                plain.add(m.group(1))
    return out, set(out) - plain


def _last_rate(text: str) -> float | None:
    """The rightmost rate on a line: the rate column, not a percentage in the description."""
    found = RATE.findall(text) or BARE_RATE.findall(text)
    return float(found[-1].replace(",", ".")) if found else None


def positions_in(text: str) -> set[str]:
    return set(NCM.findall(text))


def _expand(spec: str) -> set[str]:
    """Positions in a cell like '1702.30.11, .19 y .20; 1515.21.00'."""
    out: set[str] = set()
    last = ""
    for tok in re.findall(r"\d{4}\.\d{2}\.\d{2}|\.\d{2}\b", spec):
        if tok.startswith("."):
            if last:
                out.add(last[:7] + tok[1:])
        else:
            out.add(tok)
            last = tok
    return out


def schedule_423(csv_path: Path) -> list[Event]:
    """Annex II of Decreto 423/2026 (lote AF transcription): the 2026 column is the rate set by
    Decreto 877/2025 from 2025-12-12; then one event per month of 2027 and 2028."""
    groups: dict[str, set[str]] = {}
    by_date: dict[date, dict[str, float]] = {}
    with csv_path.open(newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            codes = groups.setdefault(r["grupo"], _expand(r["posiciones_ncm_y_referencias"]))
            raw = r["fecha_desde"]
            start = date(2025, 12, 12) if raw.startswith("2026") else date.fromisoformat(raw)
            rate = float(r["alicuota_porcentaje"])
            cell = by_date.setdefault(start, {})
            for c in codes:
                cell[c] = max(rate, cell.get(c, 0.0))
    return [
        Event(d, None, rates, "Decreto 877/2025" if d.year == 2025 else "Decreto 423/2026 Anexo II",
              "SRC-1517")
        for d, rates in sorted(by_date.items())
    ]  # fmt: skip


class RateBook:
    def __init__(self, events: list[Event]) -> None:
        self.events = sorted(events, key=lambda e: e.start)
        self._by_code: dict[str, list[tuple[date, int]]] = {}
        for i, e in enumerate(self.events):
            for code in e.rates:
                self._by_code.setdefault(code, []).append((e.start, i))

    def rate(self, code: str, day: date) -> tuple[float, str] | None:
        """Rate in percent and the norm, or None if no annex lists the position."""
        hits = self._by_code.get(code)
        if not hits:
            return None
        k = bisect.bisect_right([s for s, _ in hits], day)
        for _, i in reversed(hits[:k]):
            e = self.events[i]
            if e.end is None or day <= e.end:
                return e.rates[code], e.norm
        return None

    def codes(self) -> set[str]:
        return set(self._by_code)


def industrial_phase_out(book: RateBook, annex_ii_schedule: list[tuple[date, float, float]]
                         ) -> list[Event]:  # fmt: skip
    """Decreto 566/2026 Annex II: positions outside chapters 1 to 24 paying 4.5% or 3% on
    2026-06-30 follow the monthly schedule (date, rate for 4.5, rate for 3)."""
    cut = date(2026, 6, 30)
    at_cut = {c: book.rate(c, cut) for c in book.codes() if int(c[:2]) > 24}
    four = [c for c, r in at_cut.items() if r and abs(r[0] - 4.5) < 1e-9]
    three = [c for c, r in at_cut.items() if r and abs(r[0] - 3.0) < 1e-9]
    return [
        Event(d, None, {**dict.fromkeys(four, a), **dict.fromkeys(three, b)},
              "Decreto 566/2026 Anexo II", "SRC-1521")
        for d, a, b in annex_ii_schedule
    ]  # fmt: skip


def crude_rate(pi_usd: float, vb: float = 45.0, vr: float = 60.0, top: float = 8.0) -> float:
    """Decreto 488/2020 art. 7: 0% up to VB, the top from VR, linear in between."""
    if pi_usd <= vb:
        return 0.0
    if pi_usd >= vr:
        return top
    return top * (pi_usd - vb) / (vr - vb)


def load_book(path: Path) -> RateBook:
    """The rate book from alicuotas/eventos.csv, with the Decreto 566/2026 phase-out added."""
    events = load_events(path)
    return RateBook(events + industrial_phase_out(RateBook(events), PHASE_OUT_566))


def load_events(path: Path) -> list[Event]:
    """Events from alicuotas/eventos.csv (scripts/build_alicuotas.py)."""
    grouped: dict[tuple[str, str, str, str], dict[str, float]] = {}
    with path.open(newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            key = (r["desde"], r["hasta"], r["norma"], r["source_id"])
            grouped.setdefault(key, {})[r["ncm"]] = float(r["alicuota_pct"])
    return [
        Event(date.fromisoformat(s), date.fromisoformat(e) if e else None, rates, n, sid)
        for (s, e, n, sid), rates in grouped.items()
    ]
