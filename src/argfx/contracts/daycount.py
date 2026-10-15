"""Day-count conventions used by Argentine sovereign debt."""

from __future__ import annotations

from datetime import date, timedelta
from typing import Literal

DayCount = Literal["30/360", "30E/360", "ACT/365", "ACT/360", "ACT/ACT", "ACT/ACT_INICIO"]


def _last_of_february(d: date) -> bool:
    return d.month == 2 and (d + timedelta(days=1)).month == 3


def year_fraction(start: date, end: date, convention: DayCount) -> float:
    if end < start:
        raise ValueError(f"end {end} before start {start}")
    if convention == "30/360":
        # US bond basis: day 31 becomes 30, and so does the last day of February at the start;
        # the end day only when the start is 30 (SIGADE: 29-02-2028 to 31-03-2028 is 30 days).
        d1 = 30 if _last_of_february(start) else min(start.day, 30)
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
    if convention == "ACT/ACT_INICIO":
        # Actual days over the length of the year in which the period starts, without splitting
        # a period that crosses into the next year (BONTE BADLAR payment notices, lote O).
        year_days = (date(start.year + 1, 1, 1) - date(start.year, 1, 1)).days
        return (end - start).days / year_days
    raise ValueError(f"unknown day count {convention}")
