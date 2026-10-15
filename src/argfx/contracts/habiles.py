"""Business days of the Argentine financial system, for the 10-business-day lags of CER and TAMAR.

Up to the last observed date, a business day is a day with a BCRA reference exchange rate
(Com. A 3500) published: that series already reflects national holidays, the days decreed
non-working and the bank holidays. After it, the calendar follows Ley 27.399:

- fixed holidays: 1 Jan, 24 Mar, 2 Apr, 1 May, 25 May, 20 Jun, 9 Jul, 8 Dec, 25 Dec;
- Carnival Monday and Tuesday, Holy Thursday and Good Friday, from Easter;
- movable holidays (17 Jun, 17 Aug, 12 Oct, 20 Nov): on a Tuesday or Wednesday they move to the
  previous Monday, on a Thursday or Friday to the following Monday (art. 6);
- bank holidays: 6 Nov (Día del Bancario), 24 and 31 Dec;
- days decreed non-working for tourism, when a norm already lists them (`extra`).

Movable holidays are sometimes moved otherwise by decree; past the observed data the calendar is
a projection, and a one-day error moves a 10-day CER or TAMAR window by one day.
"""

from __future__ import annotations

import csv
from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path

FIXED = ((1, 1), (3, 24), (4, 2), (5, 1), (5, 25), (6, 20), (7, 9), (12, 8), (12, 25))
MOVABLE = ((6, 17), (8, 17), (10, 12), (11, 20))
BANK = ((11, 6), (12, 24), (12, 31))


def easter(year: int) -> date:
    """Gregorian Easter Sunday (anonymous algorithm)."""
    a, b, c = year % 19, year // 100, year % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l_ = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l_) // 451
    month = (h + l_ - 7 * m + 114) // 31
    day = (h + l_ - 7 * m + 114) % 31 + 1
    return date(year, month, day)


def _moved(d: date) -> date:
    wd = d.weekday()
    if wd in (1, 2):
        return d - timedelta(days=wd)
    if wd in (3, 4):
        return d + timedelta(days=7 - wd)
    return d


def rule_holidays(year: int) -> set[date]:
    e = easter(year)
    days = {date(year, m, d) for m, d in FIXED + BANK}
    days |= {e - timedelta(days=n) for n in (48, 47, 3, 2)}
    days |= {_moved(date(year, m, d)) for m, d in MOVABLE}
    return days


@dataclass
class BusinessCalendar:
    observed: frozenset[date] = frozenset()
    """Business days observed up to `observed_until` (days with Com. A 3500 published)."""
    observed_until: date | None = None
    extra: frozenset[date] = frozenset()
    """Non-working days decreed after `observed_until`."""
    _rules: dict[int, set[date]] = field(default_factory=dict, repr=False)

    def is_business(self, d: date) -> bool:
        if self.observed_until is not None and d <= self.observed_until:
            return d in self.observed
        if d.weekday() >= 5 or d in self.extra:
            return False
        if d.year not in self._rules:
            self._rules[d.year] = rule_holidays(d.year)
        return d not in self._rules[d.year]

    def shift(self, d: date, n: int) -> date:
        """The n-th business day before d (n > 0 goes back); d itself does not count."""
        step = timedelta(days=-1 if n > 0 else 1)
        left = abs(n)
        while left:
            d += step
            if self.is_business(d):
                left -= 1
        return d

    @classmethod
    def from_series(cls, a3500_csv: Path, extra: Iterable[date] = ()) -> BusinessCalendar:
        with a3500_csv.open(newline="", encoding="utf-8") as fh:
            days = frozenset(date.fromisoformat(r["fecha"]) for r in csv.DictReader(fh))
        return cls(observed=days, observed_until=max(days), extra=frozenset(extra))


def read_extra_holidays(path: Path) -> list[date]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as fh:
        return [date.fromisoformat(r["fecha"]) for r in csv.DictReader(fh)]
