"""Read the quarterly debt workbook of the Secretaría de Finanzas ("deuda_publica_<date>.xlsx").

Sheets used, all in thousands of USD:
- A.1.1: stock of the Administración Central by instrument and term;
- A.2.2: flows and variations of the quarter;
- A.3.1: monthly maturity profile (capital and interest) for the next twelve months, by
  instrument group, of the debt in normal payment status.

The workbook is presentation-oriented: a row is a label followed by numbers. These readers keep
the label as published (stripped) and the numeric cells in order, without interpreting more
than the layout requires.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from openpyxl import load_workbook

MONTHS_ES = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6, "julio": 7,
    "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12,
}  # fmt: skip


@dataclass(frozen=True)
class Line:
    sheet: str
    row: int
    label: str
    values: tuple[float, ...]


def _rows(path: Path, sheet: str) -> list[tuple[int, list[object]]]:
    wb = load_workbook(path, read_only=True, data_only=True)
    try:
        return [
            (i, [c for c in row if c is not None])
            for i, row in enumerate(wb[sheet].iter_rows(values_only=True), 1)
        ]
    finally:
        wb.close()


def lines(path: Path, sheet: str) -> list[Line]:
    """Rows that start with a text label and carry at least one number."""
    out = []
    for i, cells in _rows(path, sheet):
        if not cells or not isinstance(cells[0], str):
            continue
        nums = tuple(float(c) for c in cells[1:] if isinstance(c, int | float))
        if nums:
            out.append(Line(sheet, i, " ".join(cells[0].split()), nums))
    return out


def find(lines_: list[Line], prefix: str) -> Line:
    """The first line whose label starts with `prefix` (case and spacing ignored)."""
    key = " ".join(prefix.split()).lower()
    for line in lines_:
        if line.label.lower().startswith(key):
            return line
    raise KeyError(f"no line starting with {prefix!r}")


@dataclass(frozen=True)
class ProfileRow:
    group: str
    concept: str  # "total", "capital" or "interes"
    month: str  # YYYY-MM
    usd_thousands: float


def maturity_profile(path: Path, sheet: str = "A.3.1") -> list[ProfileRow]:
    """A.3.1 by group, concept and month; subtotals and the twelve-month total are dropped."""
    rows = _rows(path, sheet)
    years: list[int] = []
    months: list[int | None] = []
    for _, cells in rows:
        texts = [c for c in cells if isinstance(c, str | int)]
        if not years and texts and all(isinstance(c, int) or str(c).isdigit() for c in texts[:2]):
            years = [int(c) for c in texts if str(c).isdigit()]
            continue
        if years and not months and cells and str(cells[0]).strip().lower() in MONTHS_ES:
            months = [MONTHS_ES.get(str(c).strip().lower()) for c in cells]
            break
    if len(years) < 2 or not months:
        raise ValueError(f"{sheet}: month header not found")
    # Columns: six months and a subtotal per year, then the total.
    calendar: list[str | None] = []
    year_i = 0
    for m in months:
        if m is None:
            calendar.append(None)  # subtotal of the year
            year_i += 1
        else:
            calendar.append(f"{years[year_i]}-{m:02d}")
    out: list[ProfileRow] = []
    group = ""
    for _, cells in rows:
        if not cells or not isinstance(cells[0], str):
            continue
        label = " ".join(cells[0].split())
        nums = [float(c) for c in cells[1:] if isinstance(c, int | float)]
        if len(nums) < len(calendar):
            continue
        low = label.lower()
        if low in ("capital", "interés", "interes"):
            concept = "capital" if low == "capital" else "interes"
        else:
            group, concept = label, "total"
        for month, value in zip(calendar, nums, strict=False):
            if month is not None:
                out.append(ProfileRow(group, concept, month, value))
    return out
