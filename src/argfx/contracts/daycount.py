"""Day-count conventions used by Argentine sovereign debt."""

from __future__ import annotations

from datetime import date
from typing import Literal

DayCount = Literal["30/360", "30E/360", "ACT/365", "ACT/360", "ACT/ACT"]


def year_fraction(start: date, end: date, convention: DayCount) -> float:
    if end < start:
        raise ValueError(f"end {end} before start {start}")
    if convention == "30/360":
        # US bond basis (30/360 ISDA): day 31 becomes 30; the end day only when the start is 30.
        d1 = min(start.day, 30)
        d2 = 30 if end.day == 31 and d1 == 30 else end.day
        days = 360 * (end.year - start.year) + 30 * (end.month - start.month) + (d2 - d1)
        return days / 360
    if convention == "30E/360":
        # Months of thirty days: day 31 counts as 30 at both ends (Argentine LECAP and BONCAP).
        d1, d2 = min(start.day, 30), min(end.day, 30)
        days = 360 * (end.year - start.year) + 30 * (end.month - start.month) + (d2 - d1)
        return days / 360
    if convention == "ACT/365":
        return (end - start).days / 365
    if convention == "ACT/360":
        return (end - start).days / 360
    if convention == "ACT/ACT":
        # ISDA: split by calendar year, each piece over that year's length.
        total = 0.0
        cursor = start
        while cursor < end:
            year_end = date(cursor.year + 1, 1, 1)
            piece_end = min(end, year_end)
            year_days = (year_end - date(cursor.year, 1, 1)).days
            total += (piece_end - cursor).days / year_days
            cursor = piece_end
        return total
    raise ValueError(f"unknown day count {convention}")
