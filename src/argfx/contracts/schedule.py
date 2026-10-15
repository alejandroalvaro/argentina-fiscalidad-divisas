"""Payment-date generation. Dates are the contractual (unadjusted) dates, as SIGADE reports them."""

from __future__ import annotations

import calendar
from datetime import date


def add_months(d: date, months: int, day: int | None = None, eom: bool = False) -> date:
    """Shift by whole months, keeping `day` (or d.day); clamp to month end, or force it with eom."""
    month_index = d.year * 12 + (d.month - 1) + months
    year, month = divmod(month_index, 12)
    month += 1
    last = calendar.monthrange(year, month)[1]
    target = last if eom else min(day or d.day, last)
    return date(year, month, target)


def regular_dates(
    first: date, last: date, every_months: int, eom: bool = False, final_stub: bool = False
) -> list[date]:
    """Dates from `first` to `last` inclusive, every `every_months`, anchored on first's day.

    With `final_stub`, a `last` that falls off the grid closes a short final period.
    """
    if every_months <= 0:
        raise ValueError("every_months must be positive")
    out: list[date] = []
    k = 0
    while True:
        d = add_months(first, k * every_months, day=first.day, eom=eom)
        if d > last:
            break
        out.append(d)
        k += 1
    if final_stub and (not out or out[-1] != last):
        out.append(last)
    if not out or out[-1] != last:
        raise ValueError(f"{last} is not on the schedule that starts {first} every {every_months}m")
    return out
